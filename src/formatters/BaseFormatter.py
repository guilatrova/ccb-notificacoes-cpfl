"""Declara as classes BaseFormatter e VencimentoFormatter"""

import abc
from datetime import datetime


class BaseFormatter:
    """Classe abstrata que define o metodo formatar"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def formatar(self, contas):
        """Altera os dados do dicionario de uma lista de contas"""


class VencimentoFormatter(BaseFormatter):
    """
    Formata as contas convertendo "Vencimento" para datetime e adicionando
    um novo item bool "Vencida"
    """

    def formatar(self, contas):
        return [self._formatar_uma(conta) for conta in contas]

    def _formatar_uma(self, conta):
        conta["Vencimento"] = datetime.strptime(
            conta["Vencimento"], "%Y-%m-%dT%H:%M:%S"
        )
        conta["Vencida"] = conta["Vencimento"] < datetime.today()
        return conta
