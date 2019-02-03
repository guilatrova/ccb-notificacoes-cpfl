"""Declara a classe BaseNotification"""
import abc


class BaseNotification:
    """Classe abstrata que define o metodo notificar"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notificar(self, data):
        """Responsavel emitir os dados como notificacoes"""
