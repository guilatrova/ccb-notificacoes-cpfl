"""Declara a classe CPFL"""

import json

import requests

TOKEN_URL = "https://servicosonline.cpfl.com.br/agencia-webapi/api/token"
SITUACAO_URL = "https://servicosonline.cpfl.com.br/agencia-webapi/api/historico-contas/validar-situacao"

INFO_KEYS = [
    "CodigoFase",
    "IndGrupoA",
    "Situacao",
    "CodClasse",
    "CodEmpresaSAP",
    "CodigoTipoParceiro",
    "ParceiroNegocio",
]


class CPFL:
    def _gerar_token(self, cnpj, nr_instalacao):
        payload = {
            "client_id": "agencia-virtual-cpfl-web",
            "grant_type": "instalacao",
            "numero_documento": cnpj,
            "numero_instalacao": nr_instalacao,
        }

        resp = requests.post(TOKEN_URL, payload)
        if resp.ok:
            dic = resp.json()
            token = dic.get("access_token")
            instalacao = json.loads(dic.get("Instalacao"))

            info = dict([(k, v) for k, v in instalacao.items() if k in INFO_KEYS])
            info["CodigoClasse"] = info.pop("CodClasse")
            return token, info

        raise Exception(resp.json().get("error"))

    def _obter_contas_aberto(self, token, instalacao, **kwargs):
        payload = {
            "RetornarDetalhes": True,
            "GerarProtocolo": False,
            "Instalacao": instalacao,
        }
        payload.update(kwargs)
        assert len(payload) == 10

        headers = {"Authorization": "Bearer {}".format(token)}
        resp = requests.post(SITUACAO_URL, payload, headers=headers)

        if resp.ok:
            return resp.json().get("ContasAberto", [])

        raise Exception(resp.json().get("error"))

    def recuperar_contas_abertas(self, cnpj, instalacao):
        """Autentica e recupera todas as contas em aberta do cnpj e instalacao"""
        token, info = self._gerar_token(cnpj, instalacao)
        contas = self._obter_contas_aberto(token, instalacao, **info)
        return contas
