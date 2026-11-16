import hashlib
import json


def test_variacao_percentual():
    preco_antigo = 100000
    preco_novo = 110000
    variacao = (preco_novo - preco_antigo) / preco_antigo
    assert round(variacao, 2) == 0.10


def test_sha256_deterministico():
    payload = json.dumps({"index": 1, "data": "teste"}, sort_keys=True).encode()
    assert hashlib.sha256(payload).hexdigest() == hashlib.sha256(payload).hexdigest()


def test_halving_reduz_recompensa_pela_metade():
    recompensa_inicial = 50.0
    blocos_por_halving = 10
    blocos_minerados = 25
    halvings = blocos_minerados // blocos_por_halving
    assert recompensa_inicial / (2 ** halvings) == 12.5
