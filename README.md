# Simulador Bitcoin 💱


Esse projeto é um **Simulador didático sobre Blockchain**, implementado na linguagem **python** com o **Streamlit**. Ele foi desenvolvido para demonstrar dois conceitos cruciais no universo das criptomoedas.

1.  **Política Monetária (Halving):** A lógica de escassez programada do Bitcoin.
2.  **Mecânica da Blockchain:** O processo de mineração e validação de blocos via **Proof-of-Work (PoW)**.

## Funcionalidades em Destaque

* **Simulação Fiel do Halving:** A recompensa do bloco é automaticamente reduzida pela metade a cada **10 blocos** (ciclo configurável no código), simulando os ciclos de 4 anos do Bitcoin.
* **Proof-of-Work (PoW):** A mineração exige a busca por um `Nonce` que satisfaça o nível de dificuldade (definido pela quantidade de zeros iniciais no Hash).
* **Controle de Emissão (Supply):** As métricas acompanham a **Recompensa Atual por Bloco** e o **Total de BTC Emitido**, respeitando o limite teórico de **21 milhões** de moedas.

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
| :--- | :--- |
| **Python** | Linguagem principal do projeto. |
| **Streamlit** | Framework para construção da interface web interativa com painéis e métricas dinâmicas. |
| **Hashlib** | Utilizado para implementar a função criptográfica SHA-256 (Hashing) dos blocos. |
| **Pandas** | Utilizado para estruturar e exibir os dados da Blockchain em formato de tabela (`st.dataframe`). |

---

##  Como Rodar o Projeto Localmente

Siga estes passos para ter o simulador rodando em sua máquina:

### 1. Pré-requisitos

Certifique-se de ter o **Python (versão 3.8+)** instalado em seu sistema.

### 2. Instalação das Dependências

Primeiro, crie e ative um ambiente virtual (recomendado) e, em seguida, instale as bibliotecas necessárias:

```bash
# Crie o ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
.\venv\Scripts\activate   # Windows
```

# Instale as dependências
```pip install -r requirements.txt```

3. Execução
Execute o arquivo src/app.py usando o comando do Streamlit:
```
streamlit run src/app.py
```
O projeto será aberto automaticamente no seu navegador, geralmente em http://localhost:8501.

## ⚙️ Arquitetura e Estrutura do Código (app.py)
A lógica do simulador está encapsulada em duas classes principais:

```class Block:```
Responsável por modelar o objeto de um bloco, contendo seu índice, o hash do bloco anterior, o timestamp, os dados da transação, o nonce encontrado e a recompensa (reward).

```class Blockchain:```
Gerencia a cadeia de blocos. Implementa a função de dificuldade (proof_of_work) e, o mais importante, a lógica de política monetária (get_reward) para calcular a recompensa atual com base no ciclo de Halving.

Constantes Cruciais:
Você pode ajustar a simulação editando as constantes no topo do app.py:

```Python

BLOCKS_PER_HALVING = 10     # O Halving ocorre a cada 10 blocos (simulação)
INITIAL_REWARD = 50.0       # Recompensa inicial (50 BTC)
MAX_SUPPLY = 21000000.0     # Limite máximo de BTC
```

## ⚠ Avisos importantes!

- Esse programa não pode ser utilizado para minerar bitcoin, ou até mesmo guardá-los.
- Segurança: Embora o código use criptografia, ele não deve ser usado para fins de segurança ou trnasações reais.
- Simulação de Ciclo: O ciclo do Halving foi reduzido para fins de demonstração (10 blocos) e não refle o real ciclo do Bitcoin, que é 210.000 blocos da rede Bitcoin real.


## 🔄 Integração Contínua (CI/CD)

O projeto usa **GitHub Actions**, com dois workflows em `.github/workflows/`.

### CI: `ci.yml`

Roda automaticamente em:
- **Pull Requests** para `main` ou `develop`;
- **Push** na `develop`.

O job `build-and-test` executa:

1. Checkout do código.
2. Configuração do Python 3.10.
3. Instalação das dependências (`requirements.txt` e `requirements-dev.txt`).
4. Execução dos testes com `pytest tests/`.

O check `build-and-test` é **obrigatório** para fazer merge na `main`: se os testes falharem, o PR fica bloqueado.

Para rodar localmente:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/
```

### CD: `deploy.yml`

Roda a cada push na `develop` ou na `main`:

| Job | Quando roda | Aprovação |
| :--- | :--- | :--- |
| `deploy-staging` | `develop` e `main` | Automática |
| `deploy-production` | Somente `main`, após o staging | **Manual**, pelo revisor obrigatório (`@itsandrezl`) |

O deploy é simulado (apenas registra a publicação), mas os environments `staging` e `production` e a aprovação manual são reais.

### Fluxo completo de uma mudança

`feature/*` → Pull Request → CI verde + aprovação do par → merge em `develop` → staging → Pull Request para `main` → merge → staging → aprovação manual → production.

Detalhes do processo no [Plano de GCS](docs/gcs/plano-gcs.md).

## 📁 Estrutura do repositório e GCS

| Caminho | Conteúdo |
| :--- | :--- |
| `src/` | Código-fonte (`app.py`) |
| `tests/` | Testes automatizados (pytest) |
| `docs/gcs/plano-gcs.md` | **Plano de Gerência de Configuração de Software** |
| `docs/gcs/evidencias/` | Evidências (push recusado, revisores, environments) |
| `.github/` | Workflows de CI/CD, CODEOWNERS e templates |

Rodar os testes: `pip install -r requirements.txt -r requirements-dev.txt && pytest tests/`

Contribuição: veja [CONTRIBUTING.md](CONTRIBUTING.md).
