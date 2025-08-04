from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def simpleSendMail(subject, message, recipient):
    """Send Mail by configuration on settings so basic"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        print(f"Correo enviado a {recipient} con asunto: {subject}")
    except Exception as e:
        print(f"Error al enviar correo a {recipient}: {e}")


def createTicketMessage(name, ticket) -> str:
    messageBody = (
        f"Hola {name or 'usuario'},\n\n"
        "¡Tu ticket ha sido creado exitosamente!\n\n"
        "Aquí están los detalles de tu ticket:\n"
        f"----------------------------------------------------\n"
        f"**Tipo de Ticket:** {ticket.get('typeTicket')}\n"
        f"**Fecha de Creación:** {ticket.get('submissionDate')}\n"
        f"**Código del Ticket:** {ticket.get('code')}\n"
        f"**Estado Actual:** {ticket.get('state')}\n"
        f"----------------------------------------------------\n\n"
        "Te notificaremos sobre cualquier actualización.\n\n"
        "¡Gracias por usar nuestro servicio de Tickets !\n"
        "Atentamente,\n"
        "El equipo de soporte de Área TIC de la Acadia de Cota."
    )

    return messageBody


def sendBeautifulMail(subject, recipient, context, html):
    """Send Mail by configuration on settings with HTML content."""
    try:
        htmlContent = render_to_string(html, context)
        textContent = strip_tags(htmlContent)

        msg = EmailMultiAlternatives(
            subject, textContent, settings.DEFAULT_FROM_EMAIL, [recipient]
        )
        msg.attach_alternative(htmlContent, "text/html")
        msg.send()
        print(f"Correo HTML enviado a {recipient} con asunto: {subject}")
    except Exception as e:
        print(f"Error al enviar correo HTML a {recipient}: {e}")
