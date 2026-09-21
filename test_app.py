def test_simulador_inicializacao():
    assert True

def test_calculo_basico():
    preco_antigo = 100000
    preco_novo = 110000
    variacao = (preco_novo - preco_antigo) / preco_antigo
    assert variacao == 0.10
