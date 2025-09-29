from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from functools import wraps
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import enviar_factura_email

from config import conectar, desconectar





app = Flask(__name__)
app.secret_key = "secreto123"

def rol_requerido(*roles_permitidos):
    """
    Decorador para proteger rutas según el rol del usuario.
    Ejemplo:
        @rol_requerido("dueño", "administrador")
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "rol" not in session:
                flash("Debes iniciar sesión", "error")
                return redirect(url_for("login"))
            if session["rol"] not in roles_permitidos:
                flash("No tienes permisos para acceder a esta página", "error")
                return redirect(url_for("index"))
            return func(*args, **kwargs)
        return wrapper
    return decorador


@app.route("/proyectojjsweet/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_usu, usu_nombre, usu_clave, usu_rol
            FROM usuario
            WHERE usu_nombre = %s AND usu_estado = TRUE
        """, (usuario,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        # ⚡ Verificar la contraseña encriptada
        if user and check_password_hash(user[2], clave):
            session["usuario"] = user[1]
            session["rol"] = user[3]
            session["show_welcome"] = True  # Solo mostrar en el primer index
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for("login"))

    return render_template("Login.html")


@app.route('/proyectojjsweet/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['usuario']
        clave = request.form['clave']
        correo = request.form['correo']
        genero = request.form['genero']
        rol = request.form['rol']  # viene del select del HTML

        conn = conectar()
        cur = conn.cursor()

        # Verificar si ya existe un dueño
        cur.execute("SELECT COUNT(*) FROM usuario WHERE usu_rol = 'dueño'")
        dueño_existente = cur.fetchone()[0] > 0

        # Verificar si ya existe un administrador
        cur.execute("SELECT COUNT(*) FROM usuario WHERE usu_rol = 'administrador'")
        administrador_existente = cur.fetchone()[0] > 0

        # Evitar registrar más de un dueño o administrador
        if rol == 'dueño' and dueño_existente:
            flash("Ya existe un dueño registrado. Solo se permiten empleados.", "danger")
            cur.close()
            conn.close()
            return redirect(url_for('registro'))

        if rol == 'administrador' and administrador_existente:
            flash("Ya existe un administrador registrado. Solo se permiten empleados.", "danger")
            cur.close()
            conn.close()
            return redirect(url_for('registro'))

        # Encriptar la contraseña antes de guardar
        clave_encriptada = generate_password_hash(clave)

        # Insertar usuario en la tabla
        cur.execute("""
            INSERT INTO usuario (usu_nombre, usu_clave, usu_correo, usu_genero, usu_rol, usu_estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, clave_encriptada, correo, genero, rol, True))

        conn.commit()
        cur.close()
        conn.close()

        flash("Usuario registrado con éxito. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))

    # Renderizar el formulario
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM usuario WHERE usu_rol = 'dueño'")
    dueño_existente = cur.fetchone()[0] > 0
    cur.execute("SELECT COUNT(*) FROM usuario WHERE usu_rol = 'administrador'")
    administrador_existente = cur.fetchone()[0] > 0
    cur.close()
    conn.close()

    return render_template("registro.html", dueño_existente=dueño_existente, administrador_existente=administrador_existente)







# ---------- Index ----------
@app.route("/proyectojjsweet/index")
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))

    usuario = session.get("usuario")
    rol = session.get("rol")
    # ⚡ sacamos y borramos la bandera (solo se usa una vez)
    show_welcome = session.pop("show_welcome", False)
    
    return render_template("index.html", usuario=usuario, rol=rol, show_welcome=show_welcome)




# ---------- Otras páginas ----------
@app.route("/proyectojjsweet/ventas")
@rol_requerido('dueño', 'administrador', 'empleado')
def ventas():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_prod, prod_nombre, prod_precio FROM producto WHERE prod_estado = 'Activo'")
    productos = cur.fetchall()
    cur.close()
    conn.close()

    fecha_hoy = date.today().isoformat()  # Ejemplo: "2025-09-07"

    return render_template("ventas.html", productos=productos, fecha_hoy=fecha_hoy)


@app.route("/proyectojjsweet/buscar_cliente")
def buscar_cliente():
    documento = request.args.get("documento")
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT cli_nombre, cli_telefono, cli_direccion, cli_correo
        FROM cliente
        WHERE cli_documento = %s
    """, (documento,))
    cliente = cur.fetchone()
    conn.close()

    if cliente:
        return jsonify({
            "existe": True,
            "nombre": cliente[0],
            "telefono": cliente[1] if len(cliente) > 1 else "",
            "direccion": cliente[2] if len(cliente) > 2 else "",
            "correo": cliente[3] if len(cliente) > 3 else ""   # ✅ Nuevo
        })
    else:
        return jsonify({"existe": False})




@app.route("/proyectojjsweet/factura", methods=["POST"])
@rol_requerido('dueño', 'administrador', 'empleado')
def factura():
    conn = conectar()
    cur = conn.cursor()

    # Datos del cliente
    cliente = request.form["cliente"]
    documento = request.form["documento"]
    telefono = request.form.get("telefono", "")
    correo = request.form.get("correo", "")

    direccion = request.form.get("direccion", "")
    fecha = datetime.now()

    # Insertar cliente si no existe
    cur.execute("SELECT id_cli FROM cliente WHERE cli_documento = %s", (documento,))
    cliente_existente = cur.fetchone()

    if cliente_existente:
        id_cliente = cliente_existente[0]
        cur.execute("""
            UPDATE cliente
            SET cli_telefono = %s, cli_direccion = %s, cli_correo = %s
            WHERE id_cli = %s
        """, (telefono, direccion, correo, id_cliente))

    else:
        cur.execute("""
            INSERT INTO cliente (cli_nombre, cli_documento, cli_telefono, cli_direccion, cli_correo, cli_estado)
            VALUES (%s, %s, %s, %s, %s, TRUE) RETURNING id_cli
        """, (cliente, documento, telefono, direccion, correo))
        id_cliente = cur.fetchone()[0]


    # Lista de productos
    productos_json = request.form.get("productos_json")
    productos = json.loads(productos_json) if productos_json else []

    if not productos:
        flash("❌ No se enviaron productos en la factura", "error")
        return redirect(url_for("ventas"))

    # Validar stock
    for prod in productos:
        producto_id = int(prod["id"])
        cantidad = int(prod["cantidad"])

        cur.execute("""
            SELECT prod_nombre, prod_precio, prod_stock
            FROM producto
            WHERE id_prod = %s AND prod_estado = 'Activo'
        """, (producto_id,))
        producto_data = cur.fetchone()

        if not producto_data:
            flash(f"⚠️ El producto con ID {producto_id} no existe o está inactivo", "warning")
            conn.rollback()
            cur.close()
            conn.close()
            return redirect(url_for("ventas"))

        nombre, precio_real, stock_disponible = producto_data

        if cantidad > stock_disponible:
            flash(f"⚠️ Stock insuficiente para {nombre}. Disponible: {stock_disponible}", "warning")
            conn.rollback()
            cur.close()
            conn.close()
            return redirect(url_for("ventas"))

    # Crear la venta
    total_venta = 0
    detalles = []

    cur.execute("""
        INSERT INTO venta (ven_fecha, ven_condicion, ven_pago, ven_total, ven_estado, fk_id_cli)
        VALUES (%s, %s, %s, %s, TRUE, %s)
        RETURNING id_ven
    """, (fecha, "contado", "efectivo", 0, id_cliente))
    id_venta = cur.fetchone()[0]

    for prod in productos:
        producto_id = int(prod["id"])
        cantidad = int(prod["cantidad"])

        cur.execute("""
            SELECT prod_nombre, prod_precio
            FROM producto
            WHERE id_prod = %s
        """, (producto_id,))
        nombre, precio_real = cur.fetchone()

        total = cantidad * float(precio_real)
        total_venta += total

        cur.execute("""
            INSERT INTO detalle_venta (fk_id_ven, fk_id_prod, dv_precio_uni, dv_total, dv_cantidad, dv_estado)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """, (id_venta, producto_id, precio_real, total, cantidad))

        cur.execute("""
            UPDATE producto
            SET prod_stock = prod_stock - %s
            WHERE id_prod = %s
        """, (cantidad, producto_id))

        detalles.append({
            "prod_nombre": nombre,
            "dv_cantidad": cantidad,
            "dv_precio_uni": float(precio_real),
            "dv_total": total
        })

    cur.execute("UPDATE venta SET ven_total = %s WHERE id_ven = %s", (total_venta, id_venta))

    conn.commit()
    cur.close()
    conn.close()

    venta_dict = {
        "id_ven": id_venta,
        "ven_fecha": fecha,
        "ven_condicion": "contado",
        "ven_pago": "efectivo",
        "ven_total": total_venta
    }

    # Generar PDF temporal
    pdf_path = f"factura_{id_venta}.pdf"
    from xhtml2pdf import pisa
    html = render_template("factura.html", venta=venta_dict, detalles=detalles,
                       cliente=cliente, documento=documento,
                       telefono=telefono, direccion=direccion,
                       correo=correo, pdf=True)
    with open(pdf_path, "wb") as f:
        pisa.CreatePDF(html, dest=f)

# 🔹 Enviar correo
    print(f"[DEBUG] Enviando factura a {correo}...")
    enviar_factura_email(correo, cliente, pdf_path)
    print("[DEBUG] Correo enviado ✅")


    return render_template(
        "factura.html",
        venta=venta_dict,
        detalles=detalles,
        cliente=cliente,
        documento=documento,
        telefono=telefono,
        direccion=direccion,
        correo=correo,
        pdf=False
    )   


@app.route("/proyectojjsweet/factura/pdf/<int:id_ven>")
@rol_requerido('dueño', 'administrador', 'empleado')
def factura_pdf(id_ven):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT v.id_ven, v.ven_fecha, v.ven_condicion, v.ven_pago, v.ven_total,
           c.cli_nombre, c.cli_documento, c.cli_telefono, c.cli_direccion, c.cli_correo
        FROM venta v
        JOIN cliente c ON v.fk_id_cli = c.id_cli
        WHERE v.id_ven = %s
    """, (id_ven,))
    venta = cur.fetchone()


    if not venta:
        return "Factura no encontrada", 404

    venta_dict = {
        "id_ven": venta[0],
        "ven_fecha": venta[1],
        "ven_condicion": venta[2],
        "ven_pago": venta[3],
        "ven_total": float(venta[4])
    }

    cliente = venta[5]
    documento = venta[6]
    telefono = venta[7]
    direccion = venta[8]
    correo = venta[9]

    cur.execute("""
        SELECT p.prod_nombre, d.dv_cantidad, d.dv_precio_uni, d.dv_total
        FROM detalle_venta d
        JOIN producto p ON p.id_prod = d.fk_id_prod
        WHERE d.fk_id_ven = %s
    """, (id_ven,))
    detalles_raw = cur.fetchall()
    cur.close()
    conn.close()

    detalles = []
    for d in detalles_raw:
        detalles.append({
            "prod_nombre": d[0],
            "dv_cantidad": int(d[1]),
            "dv_precio_uni": float(d[2]),
            "dv_total": float(d[3])
        })

    # Renderizar factura en modo PDF (sin botones extras)
    return render_template(
        "factura.html",
        venta=venta_dict,
        detalles=detalles,
        cliente=cliente,
        documento=documento,
        telefono=telefono,
        direccion=direccion,
        correo=correo,
        pdf=True
    )


@app.route("/proyectojjsweet/factura/<int:id_ven>")
@rol_requerido('dueño', 'administrador', 'empleado')
def ver_factura(id_ven):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT v.id_ven, v.ven_fecha, v.ven_condicion, v.ven_pago, v.ven_total,
               c.cli_nombre, c.cli_documento, c.cli_telefono, c.cli_direccion, c.cli_correo
        FROM venta v
        JOIN cliente c ON v.fk_id_cli = c.id_cli
        WHERE v.id_ven = %s
    """, (id_ven,))
    venta = cur.fetchone()

    if not venta:
        return "Factura no encontrada", 404

    venta_dict = {
        "id_ven": venta[0],
        "ven_fecha": venta[1],
        "ven_condicion": venta[2],
        "ven_pago": venta[3],
        "ven_total": float(venta[4])
    }

    cliente = venta[5]
    documento = venta[6]
    telefono = venta[7]
    direccion = venta[8]
    correo = venta[9]

    cur.execute("""
        SELECT p.prod_nombre, d.dv_cantidad, d.dv_precio_uni, d.dv_total
        FROM detalle_venta d
        JOIN producto p ON p.id_prod = d.fk_id_prod
        WHERE d.fk_id_ven = %s
    """, (id_ven,))
    detalles_raw = cur.fetchall()
    cur.close()
    conn.close()

    detalles = []
    for d in detalles_raw:
        detalles.append({
            "prod_nombre": d[0],
            "dv_cantidad": int(d[1]),
            "dv_precio_uni": float(d[2]),
            "dv_total": float(d[3])
        })

    # Renderizar factura en modo normal (con botones Imprimir/Volver)
    return render_template(
        "factura.html",
        venta=venta_dict,
        detalles=detalles,
        cliente=cliente,
        documento=documento,
        telefono=telefono,
        direccion=direccion,
        correo=correo, 
        pdf=False
    )

@app.route("/proyectojjsweet/enviar_factura/<int:id_ven>")
def enviar_factura(id_ven):
    # Obtener datos del cliente
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.cli_correo, c.cli_nombre
        FROM venta v
        JOIN cliente c ON v.fk_id_cli = c.id_cli
        WHERE v.id_ven = %s
    """, (id_ven,))
    cliente = cur.fetchone()
    cur.close()
    conn.close()

    if not cliente:
        return "Cliente no encontrado", 404

    correo, nombre = cliente

    # Generar el PDF en disco (usamos la misma plantilla de factura)
    pdf_path = f"factura_{id_ven}.pdf"

    # Renderizar HTML de la factura
    html = render_template("factura.html", pdf=True, venta={}, detalles=[], cliente=nombre, documento="", telefono="", direccion="")
    
    from xhtml2pdf import pisa
    with open(pdf_path, "wb") as f:
        pisa.CreatePDF(html, dest=f)

    # Enviar por correo
    enviar_factura_email(correo, nombre, pdf_path)

    return f"📧 Factura enviada a {correo}"







@app.route("/proyectojjsweet/historial/eliminar/<int:id_ven>", methods=["POST"])
@rol_requerido('dueño', 'administrador', 'empleado')
def eliminar_venta(id_ven):
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    conn = conectar()
    cur = conn.cursor()

    # 1️⃣ Consultar los productos y cantidades vendidos en esa factura
    cur.execute("""
        SELECT fk_id_prod, dv_cantidad
        FROM detalle_venta
        WHERE fk_id_ven = %s
    """, (id_ven,))
    productos_vendidos = cur.fetchall()

    # 2️⃣ Devolver las cantidades al inventario
    for prod_id, cantidad in productos_vendidos:
        cur.execute("""
            UPDATE producto
            SET prod_stock = prod_stock + %s
            WHERE id_prod = %s
        """, (cantidad, prod_id))

    # 3️⃣ Marcar la venta como anulada (no se borra)
    cur.execute("UPDATE venta SET ven_estado = FALSE WHERE id_ven = %s", (id_ven,))

    conn.commit()
    cur.close()
    conn.close()

    flash("⚠️ Factura ANULADA y stock RESTABLECIDO", "warning")
    return redirect(url_for("historial"))


@app.route("/proyectojjsweet/facturas_anuladas", methods=["GET", "POST"])
@rol_requerido('dueño', 'administrador', 'empleado')
def facturas_anuladas():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = conectar()
    cur = conn.cursor()

    fecha_hoy = date.today()
    fecha_inicio = request.form.get("fecha_inicio", fecha_hoy.isoformat())
    fecha_fin = request.form.get("fecha_fin", fecha_hoy.isoformat())

    cur.execute("""
        SELECT id_ven, ven_fecha, ven_condicion, ven_pago, ven_total
        FROM venta
        WHERE ven_estado = FALSE
        AND DATE(ven_fecha) BETWEEN %s AND %s
        ORDER BY ven_fecha DESC
    """, (fecha_inicio, fecha_fin))

    ventas = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("facturas_anuladas.html",
                           ventas=ventas,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin)









@app.route("/proyectojjsweet/historial", methods=["GET", "POST"])
def historial():
    conn = conectar()
    cur = conn.cursor()

    fecha_inicio = request.form.get("fecha_inicio", "2000-01-01")
    fecha_fin = request.form.get("fecha_fin", datetime.now().date())

    cur.execute("""
        SELECT v.id_ven, v.ven_fecha, v.ven_condicion, v.ven_pago, v.ven_total,
           c.cli_nombre, c.cli_correo
        FROM venta v
        JOIN cliente c ON v.fk_id_cli = c.id_cli
        WHERE v.ven_estado = TRUE
        AND DATE(v.ven_fecha) BETWEEN %s AND %s
        ORDER BY v.ven_fecha DESC
    """, (fecha_inicio, fecha_fin))


    ventas = cur.fetchall()
    conn.close()

    return render_template("historial.html", ventas=ventas,
                           fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


















@app.route("/proyectojjsweet/resumen")
@rol_requerido('dueño', 'administrador', 'empleado')
def resumen():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = conectar()
    cur = conn.cursor()


# Ventas de hoy (solo activas)
    cur.execute("""
        SELECT COUNT(*), COALESCE(SUM(ven_total), 0)
        FROM venta
        WHERE DATE(ven_fecha) = CURRENT_DATE
        AND ven_estado = TRUE
    """)
    cantidad_hoy, total_hoy = cur.fetchone()

# Ventas del mes (solo activas)
    cur.execute("""
        SELECT COALESCE(SUM(ven_total), 0), COUNT(*)
        FROM venta
        WHERE EXTRACT(MONTH FROM ven_fecha) = EXTRACT(MONTH FROM CURRENT_DATE)
        AND EXTRACT(YEAR FROM ven_fecha) = EXTRACT(YEAR FROM CURRENT_DATE)
        AND ven_estado = TRUE
    """)
    total_mes, cantidad_mes = cur.fetchone()

# Productos más vendidos (excluir anuladas)
    cur.execute("""
        SELECT p.prod_nombre, SUM(d.dv_cantidad) as cantidad
        FROM detalle_venta d
        JOIN producto p ON p.id_prod = d.fk_id_prod
        JOIN venta v ON v.id_ven = d.fk_id_ven
        WHERE v.ven_estado = TRUE
        GROUP BY p.prod_nombre
        ORDER BY cantidad DESC
        LIMIT 15
    """)
    top_productos = cur.fetchall()


    # Stock bajo
    cur.execute("SELECT prod_nombre, prod_stock FROM producto WHERE prod_stock <= 15 ORDER BY prod_stock ASC")
    stock_bajo = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("resumen.html",
                           total_hoy=total_hoy, cantidad_hoy=cantidad_hoy,
                           total_mes=total_mes, cantidad_mes=cantidad_mes,
                           top_productos=top_productos, stock_bajo=stock_bajo)






@app.route('/proyectojjsweet/inventario')
def inventario():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_cat, nombre FROM categoria ORDER BY nombre")
    categorias = cur.fetchall()
    cur.close()
    desconectar(conn)
    return render_template("inventario.html", categorias=categorias)




@app.route('/proyectojjsweet/agregar_producto', methods=["POST"])
@rol_requerido('dueño', 'administrador', )
def agregar_producto():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]

    categoria_raw = request.form["categoria"]
    print("DEBUG valor recibido de categoria:", categoria_raw)  # 👀 importante

    try:
        categoria = int(categoria_raw)   # debería ser un número (id)
    except ValueError:
        flash(f"❌ Error: se recibió '{categoria_raw}' en lugar de un ID", "error")
        return redirect(url_for("inventario"))

    precio = request.form["precio"]
    stock = request.form["stock"]
    estado = request.form["estado"]

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO producto (prod_nombre, prod_descripcion, prod_categoria, prod_precio, prod_stock, prod_estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, descripcion, categoria, precio, stock, estado))
    conn.commit()
    cur.close()
    desconectar(conn)

    flash("✅ Producto agregado con éxito", "success")
    return redirect(url_for("inventario"))







@app.route("/proyectojjsweet/inventario/eliminar/<int:id_prod>")
@rol_requerido('dueño', 'administrador',)
def eliminar_producto(id_prod):
    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()
    cur = conexion.cursor()
    cur.execute("DELETE FROM producto WHERE id_prod = %s", (id_prod,))
    conexion.commit()
    conexion.close()
    return redirect(url_for("consulta"))



@app.route("/proyectojjsweet/editar/<int:id_prod>", methods=["GET", "POST"])
@rol_requerido('dueño', 'administrador',)
def editar_producto(id_prod):
    conn = conectar()
    cur = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        categoria = request.form["categoria"]  # aquí ya será el id_cat (entero)
        precio = request.form["precio"]
        estado = request.form["estado"]

        cur.execute("""
            UPDATE producto
            SET prod_nombre=%s, 
                prod_descripcion=%s, 
                prod_categoria=%s, 
                prod_precio=%s,  
                prod_estado=%s
            WHERE id_prod=%s
        """, (nombre, descripcion, categoria, precio, estado, id_prod))

        conn.commit()
        cur.close()
        desconectar(conn)
        return redirect(url_for("consulta"))

    # Si es GET → traer el producto
    cur.execute("""
        SELECT id_prod, prod_nombre, prod_descripcion, prod_categoria, prod_precio, prod_stock, prod_estado
        FROM producto
        WHERE id_prod = %s
    """, (id_prod,))
    producto = cur.fetchone()


    # Traer todas las categorías para el <select>
    cur.execute("SELECT id_cat, nombre FROM categoria ORDER BY nombre;")
    categorias = cur.fetchall()

    cur.close()
    desconectar(conn)

    return render_template("editar.html", producto=producto, categorias=categorias)

    cur.close()
    desconectar(conn)

    return render_template("editar.html", producto=producto)

@app.route("/proyectojjsweet/consulta")
@rol_requerido('dueño', 'administrador', 'empleado')
def consulta():
    conn = conectar()
    cur = conn.cursor()

    # Traer categorías disponibles
    cur.execute("SELECT id_cat, nombre FROM categoria ORDER BY nombre;")
    categorias = cur.fetchall()

    # Revisar si el usuario seleccionó filtro
    categoria = request.args.get("categoria")

    if categoria:
        # Filtrar por categoría seleccionada
        cur.execute("""
            SELECT p.id_prod, p.prod_nombre, p.prod_descripcion, c.nombre, 
                   p.prod_precio, p.prod_stock, p.prod_estado
            FROM producto p
            JOIN categoria c ON p.prod_categoria = c.id_cat
            WHERE c.id_cat = %s
            ORDER BY c.nombre, p.prod_nombre;
        """, (categoria,))
    else:
        # Mostrar todo si no hay filtro
        cur.execute("""
            SELECT p.id_prod, p.prod_nombre, p.prod_descripcion, c.nombre, 
                   p.prod_precio, p.prod_stock, p.prod_estado
            FROM producto p
            JOIN categoria c ON p.prod_categoria = c.id_cat
            ORDER BY c.nombre, p.prod_nombre;
        """)

    productos = cur.fetchall()
    conn.close()

    return render_template("consulta.html", productos=productos, categorias=categorias)


@app.route("/proyectojjsweet/agregar_stock", methods=["POST"])
@rol_requerido('dueño', 'administrador',)
def agregar_stock():
    id_prod = request.form["id_prod"]
    cantidad = int(request.form["cantidad"])

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE producto
        SET prod_stock = prod_stock + %s
        WHERE id_prod = %s
    """, (cantidad, id_prod))
    conn.commit()
    cur.close()
    conn.close()

    flash("✅ Stock actualizado con éxito", "success")
    return redirect(url_for("consulta"))  # <-- cámbialo por el nombre real de tu ruta de inventario


@app.route('/proyectojjsweet/usuarios')
@rol_requerido('dueño', 'administrador',)
def usuarios():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT id_usu, usu_nombre, usu_correo, usu_rol, usu_estado FROM usuario")
    usuarios = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/proyectojjsweet/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    # 🔐 Solo dueño o administrador puede eliminar
    if session.get("rol") not in ["dueño", "administrador"]:
        flash("❌ No tienes permiso para eliminar usuarios", "error")
        return redirect(url_for("usuarios"))

    conn = conectar()
    cur = conn.cursor()

    # 🔹 Borrar físicamente el usuario
    cur.execute("DELETE FROM usuario WHERE id_usu = %s", (id,))
    conn.commit()
    cur.close()
    desconectar(conn)

    flash("✅ Usuario eliminado permanentemente", "success")
    return redirect(url_for('usuarios'))







@app.route("/proyectojjsweet/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="10.60.84.120", port=5000, debug=True)





