from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Util:
    @staticmethod
    def send_email(username: str, absurl: str, email: str):

        data = {
            "username": username,
            "absurl": absurl,
            "email": email,
        }

        html_content = f"{data}" # render with dynamic value
        text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

        msg = EmailMultiAlternatives(f"Hello {data['username']} please verify your email", text_content, to=[data["email"]])

        msg.attach_alternative(html_content, "text/html")
        msg.send()