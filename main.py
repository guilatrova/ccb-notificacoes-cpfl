"""
Utiliza o settings para configurar, recuperar contas em aberto e emitir as notificacoes via email
"""

from contextlib import contextmanager
from datetime import datetime

from args import handle_args
from src.CPFL import CPFL
from src.formatters import HtmlFormatter
from src.notifications import EmailNotification
from src.settings import CNPJ, CREDENTIALS, INSTALACOES, SMTP_SERVER


@contextmanager
def logging(
    action, prefix_action="* ", sufix_action="...", success="OK ", error="ERROR"
):
    """Usado para emitir notificacoes no inicio e fim de uma acao"""
    print("{}{}{}".format(prefix_action, action, sufix_action), end=" ")

    def finish(text):
        """
        Usado para emitir uma mensagem de fim customizada,
        se nao for invocada e exibida a mensagem padrao de sucesso
        """
        finish.has_been_called = True
        print("{}{}".format(success, text))

    finish.has_been_called = False

    try:
        yield finish
        if not finish.has_been_called:
            print("{}".format(success))
    except Exception as ex:
        print("{} {}".format(error, ex))
        raise


def pegar_contas_igrejas():
    """Recupera todas as contas em aberto das igrejas"""
    erros = []
    contas = []
    cpfl = CPFL()

    for igreja, instalacao in INSTALACOES.items():
        try:
            with logging(igreja) as finish:
                novas_contas = cpfl.recuperar_contas_abertas(CNPJ, instalacao)
                for conta in novas_contas:
                    conta["Descricao"] = igreja

                contas += novas_contas

                finish("({})".format(len(novas_contas)))
        except Exception as ex:
            erros.append("{}: {}".format(igreja, ex))

    return contas, erros


if __name__ == '__main__':
    config = handle_args()
    title = 'Relatório de contas CPFL da CCB ({})'.format(datetime.today().strftime('%d/%m/%Y'))
    html = HtmlFormatter(title)
    email = EmailNotification(SMTP_SERVER, CREDENTIALS)

    contas, erros = pegar_contas_igrejas()
    body = html.formatar(contas, erros)

    with logging('Sending mail', success='DONE'):
        email.notificar(body, subject=title, **config)
