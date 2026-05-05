from flask import Flask, request, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Delegaciones 
DELEGACIONES = {
    "bizkaia bilbao": ["j.prado@axor-rentals.com"],
    "bizkaia erletxes": ["j.prado@axor-rentals.com"],
    "gipuzkoa": ["p.gonzalez@axor-rentals.com", "astigarraga@axor-rentals.com"],
    "araba": ["a.urresola@axor-rentals.com", "vitoria@axor-rentals.com"],
    "navarra": ["comercial.navarra@axor-rentals.com", "pamplona@axor-rentas.com"],
    "cantabria santander": ["c.delcampo@axor-rentals.com", "r.garcia@axor-rentals.com"],
    "cantabria reinosa": ["c.delcampo@axor-rentals.com", "r.garcia@axor-rentals.com"],
    "asturias": ["m.buelga@axor-rentals.com", "gijon@axor-rentals.com"],
    "burgos": ["a.pastor@axor-rentals.com", "comercial.burgos@axor-rentals.com", "burgos@axor-rentals.com"],
    "madrid torrejón": ["b.crespo@axor-rentals.com", "madrid@axor-rentals.com"],
    "madrid pinto": ["b.crespo@axor-rentals.com", "pinto@axor-rentals.com", "comercial.pinto@axor-rentals.com"],
    "cáceres": ["d.sanchez@axor-rentals.com", "caceres@axor-rentals.com"],
    "zaragoza": ["r.montuenga@axor-rentals.com", "zaragoza@axor-rentals.com"],
    "barcelona": ["r.salichs@axor-rentals.com", "comercial.barcelona@axor-rentals.com", "barcelona@axor-rentals.com"],
    "tarragona": ["x.calero@axor-rentals.com", "tarragona@axor-rentals.com"],
    "córdoba": ["m.funes@axor-rentals.com", "cordoba@axor-rentals.com"],
    "jaén": ["jj.gaitan@axor-rentals.com", "linares@axor-rentals.com"],
    "cádiz": ["c.perez@axor-rentals.com", "cadiz@axor-rentals.com"],
    "málaga": ["comercial.malaga@axor-rentals.com", "malaga@axor-rentals.com"],
    "sevilla": ["j.martin@axor-rentals.com", "comercial.sevilla@axor-rentals.com", "sevilla@axor-rentals.com"],
    "huelva": ["c.martin@axor-rentals.com", "huelva@axor-rentals.com"],
    "ourense": ["x.magallais@axor-rentals.com", "ourense@axor-rentals.com"],
}

# SERVIR HTML
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "formularioes.html")

# SERVIR ARCHIVOS (css, js, imágenes)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(BASE_DIR, path)

# FORMULARIO
@app.route("/enviar", methods=["POST"])
def enviar():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    telefono = request.form.get("telefono")
    delegacion = request.form.get("delegacion")
    asunto = request.form.get("asunto")
    mensaje = request.form.get("mensaje")

    fecha = datetime.datetime.now().strftime("%d-%m-%Y")
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    enviar_email(delegacion, fecha, hora, nombre, email, telefono, asunto, mensaje)

    return "FORMULARIO ENVIADO"

# EMAIL
def enviar_email(delegacion, fecha, hora, nombre, email, telefono, asunto, mensaje):
    delegacion = delegacion.lower()

    if delegacion not in DELEGACIONES:
        print("Delegación no válida")
        return

    destinatarios = DELEGACIONES[delegacion]

    try:
        server = smtplib.SMTP_SSL('smtp.serviciodecorreo.es', 465)

        import os

        servidor_email = os.environ.get("EMAIL_USER")
        contraseña_email = os.environ.get("EMAIL_PASSWORD")

        server.login(servidor_email, contraseña_email)

        msg = MIMEMultipart()
        msg['From'] = servidor_email
        msg['Subject'] = f"Nuevo formulario: {asunto}"

        cuerpo = f"""
        <h2>Formulario recibido</h2>
        <p><b>Fecha:</b> {fecha} {hora}</p>
        <p><b>Nombre:</b> {nombre}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Teléfono:</b> {telefono}</p>
        <p><b>Delegación:</b> {delegacion}</p>
        <p><b>Mensaje:</b><br>{mensaje}</p>
        """

        msg.attach(MIMEText(cuerpo, 'html'))

        for destinatario in destinatarios:
            msg['To'] = destinatario
            server.sendmail(servidor_email, destinatario, msg.as_string())

        server.quit()
        print("Correo enviado")

    except Exception as e:
        print("Error enviando correo:", e)