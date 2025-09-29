let productos = [];

// Función para agregar productos a la factura
function agregarProducto() {
  const producto = document.getElementById("producto").value;
  const cantidad = parseInt(document.getElementById("cantidad").value);
  const precio = parseFloat(document.getElementById("precio").value);

  if (!producto || isNaN(cantidad) || isNaN(precio)) {
    alert("⚠️ Por favor ingrese todos los datos del producto");
    return;
  }

  // Guardamos el producto en un array
  productos.push({ producto, cantidad, precio });

  // Limpiamos los campos
  document.getElementById("producto").value = "";
  document.getElementById("cantidad").value = "";
  document.getElementById("precio").value = "";

  alert("✅ Producto agregado a la factura");
}

// Función para generar la factura
function generarFactura() {
  const cliente = document.getElementById("cliente").value;
  const documento = document.getElementById("documento").value;
  const fecha = document.getElementById("fecha").value;

  if (!cliente || !documento || !fecha || productos.length === 0) {
    alert("⚠️ Complete los datos del cliente y agregue al menos un producto.");
    return;
  }

  // Mostramos los datos del cliente en la factura
  document.getElementById("fCliente").textContent = cliente;
  document.getElementById("fDocumento").textContent = documento;
  document.getElementById("fFecha").textContent = fecha;

  // Llenamos la tabla con los productos
  const tbody = document.getElementById("fProductos");
  tbody.innerHTML = ""; // limpiar por si ya existía algo

  let total = 0;

  productos.forEach(p => {
    const fila = document.createElement("tr");

    const tdCantidad = document.createElement("td");
    tdCantidad.textContent = p.cantidad;

    const tdProducto = document.createElement("td");
    tdProducto.textContent = p.producto;

    const tdPrecio = document.createElement("td");
    tdPrecio.textContent = `$${p.precio.toFixed(2)}`;

    const tdTotal = document.createElement("td");
    const subtotal = p.cantidad * p.precio;
    tdTotal.textContent = `$${subtotal.toFixed(2)}`;

    total += subtotal;

    fila.appendChild(tdCantidad);
    fila.appendChild(tdProducto);
    fila.appendChild(tdPrecio);
    fila.appendChild(tdTotal);

    tbody.appendChild(fila);
  });

  // Mostramos el total
  document.getElementById("fTotal").textContent = total.toFixed(2);

  // Mostrar la factura
  document.getElementById("factura").classList.remove("oculto");
}
