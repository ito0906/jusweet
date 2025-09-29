import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def enviar_factura_email(destinatario, nombre, pdf_path):
    remitente = "alvaromanjarrez0906@gmail.com"
    password = "amqp hfli nrhw snga"  # contraseña de aplicación de Google

    # Crear mensaje
    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = "Factura de compra - JJ Sweet"

    cuerpo = f"""
Hola {nombre},

Adjuntamos la factura de tu compra realizada en JJ Sweet. 
Gracias por preferirnos 💜.

Atentamente,  
El equipo de JJ Sweet
"""
    msg.attach(MIMEText(cuerpo, "plain"))

    # Adjuntar PDF
    with open(pdf_path, 'rb') as f:
        adjunto = MIMEApplication(f.read(), _subtype="pdf")
        adjunto.add_header('Content-Disposition', 'attachment', filename=pdf_path)
        msg.attach(adjunto)

    # Enviar correo con Gmail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
