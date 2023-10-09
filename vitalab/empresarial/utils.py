from random import choice, shuffle
from string import ascii_letters, punctuation, digits
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML


def gerar_senha_aleatoria(tamanho) -> str:

    senha: list[str] = []
    for _ in range(tamanho // 3):
        senha.append(choice(ascii_letters))
        senha.append(choice(punctuation))
        senha.append(choice(digits))

    for _ in range(tamanho % 3):
        senha.append(choice(ascii_letters))

    shuffle(senha)
    return ''.join(senha)


def gerar_pdf_exames(exame, paciente, senha) -> BytesIO:

    path_template = settings.BASE_DIR / 'templates/partials/senha_exame.html'
    template_render = render_to_string(path_template, {'exame': exame, 'paciente': paciente, 'senha': senha})

    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return path_output