"""Declara as classes HtmlFormatter"""
import os

try:
    from formatters.BaseFormatter import VencimentoFormatter
except ModuleNotFoundError:  # For local execution
    from src.formatters.BaseFormatter import VencimentoFormatter

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")


class HtmlFormatter(VencimentoFormatter):
    """Formata as informações usando templates HTML"""

    ROW_TEMPLATE = os.path.join(TEMPLATES_PATH, "row.html")
    CORPO_TEMPLATE = os.path.join(TEMPLATES_PATH, "email.html")
    ERRORS_TEMPLATE = os.path.join(TEMPLATES_PATH, "errors.html")

    def __init__(self, titulo):
        self.titulo = titulo

    def formatar(self, contas, erros):
        pre_formatado = super(HtmlFormatter, self).formatar(contas)

        vencidas = self._formatar_contas(
            [conta.copy() for conta in pre_formatado if conta["Vencida"]]
        )
        em_aberto = self._formatar_contas(contas)
        erros = self._formatar_erros(erros)

        return self._formatar_corpo(em_aberto, vencidas, erros)

    def _formatar_data(self, conta):
        conta["Vencimento"] = conta["Vencimento"].strftime("%d/%m/%Y")
        if conta["Vencida"]:
            conta["Vencimento"] = '<span class="red">{}</span>'.format(
                conta["Vencimento"]
            )

        return conta

    def _formatar_contas(self, contas):
        contas = [self._formatar_data(conta) for conta in contas]

        with open(HtmlFormatter.ROW_TEMPLATE, "r", encoding="utf-8") as template:
            raw = template.read()

            return [
                self._replace_template(
                    raw,
                    DESCRICAO=conta["Descricao"],
                    MES=conta["MesReferencia"],
                    VENCIMENTO=conta["Vencimento"],
                    VALOR=conta["Valor"],
                    SVG=conta["SvgCodigoBarras"],
                    COD=conta["CodigoBarras"],
                )
                for conta in contas
            ]

    def _formatar_corpo(self, contas, contas_vencidas, erros):
        with open(HtmlFormatter.CORPO_TEMPLATE, "r", encoding="utf-8") as template:
            raw = template.read()
            contas = " ".join(contas)
            contas_vencidas = " ".join(contas_vencidas)

            return self._replace_template(
                raw,
                TITULO=self.titulo,
                LINHAS_VENCIDAS=contas_vencidas,
                LINHAS_ABERTO=contas,
                ERROS=erros,
            )

    def _formatar_erros(self, erros):
        if erros:
            with open(HtmlFormatter.ERRORS_TEMPLATE, "r", encoding="utf-8") as template:
                raw = template.read()
                wrapped = []

                for erro in erros:
                    wrapped.append("<li>{}</li>".format(erro))

            return self._replace_template(raw, LINHAS=" ".join(wrapped))

        return ""

    def _replace_template(self, template, **kwargs):
        formatted = template
        for key, value in kwargs.items():
            replace_this = "#{}#".format(key)
            formatted = formatted.replace(replace_this, value)

        return formatted
