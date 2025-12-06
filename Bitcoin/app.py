"""
André Felipe — Simulador didático de Bitcoin (Streamlit)
"""

from dataclasses import dataclass, asdict
from time import time, perf_counter
import hashlib
import json
from typing import List, Optional, Dict, Any
import math
import streamlit as st
import pandas as pd
from datetime import datetime

BLOCKS_PER_HALVING = 10        # A partir de 10 blocos minerados, a recompensa é cortada pela metade, exemplo: 50/25/12,5...
INITIAL_REWARD = 50.0          # Recompensa inicial implementada pelo Satoshi Nakamoto.
MAX_SUPPLY = 21_000_000.0      # 21 milhões, esse valor é o máximo de bitcoin's que podem ser minerados.
MINER_ADDRESS = "Minerador_Padrão"

@dataclass
class Block:
    index: int
    previous_hash: str
    timestamp: float
    data: str
    nonce: int = 0
    reward: float = 0.0
    hash: str = ""

    def compute_hash(self) -> str:
        payload = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "nonce": self.nonce,
            "reward": self.reward
        }, sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()

    def finalize_hash(self):
        self.hash = self.compute_hash()


class SimpleBlockchain:
    def __init__(self, blocks_per_halving: int = BLOCKS_PER_HALVING):
        self.blocks_per_halving = blocks_per_halving
        self.chain: List[Block] = []
        self.create_genesis()

    def create_genesis(self):
        genesis = Block(
            index=1,
            previous_hash="0",
            timestamp=time(),
            data="Bloco Gênesis - Início da cadeia",
            nonce=0,
            reward=0.0
        )
        genesis.finalize_hash()
        self.chain = [genesis]

    # número de blocos minerados (excluindo o gênesis)
    @property
    def blocks_mined(self) -> int:
        return max(len(self.chain) - 1, 0)

    def current_reward(self) -> float:
        # quantos halvings já aconteceram (descontando o gênesis)
        halving_count = math.floor(self.blocks_mined / self.blocks_per_halving)
        if halving_count >= 64:  
            return 0.0
        return INITIAL_REWARD / (2 ** halving_count)

    def total_supply(self) -> float:
        # Soma apenas as recompensas dos blocos após o gênesis.
        return sum(block.reward for block in self.chain[1:])

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: str, reward: float) -> Block:
        last = self.get_last_block()
        new_block = Block(
            index=len(self.chain) + 1,
            previous_hash=last.hash,
            timestamp=time(),
            data=data,
            nonce=0,
            reward=reward
        )
        self.chain.append(new_block)
        return new_block

    def proof_of_work(self, block: Block, difficulty: int, max_nonce: Optional[int] = None) -> Block:
        if max_nonce is None:
            max_nonce = 10**9 
        block.nonce = 0
        computed = block.compute_hash()
        target_prefix = "0" * difficulty
        while not computed.startswith(target_prefix) and block.nonce < max_nonce:
            block.nonce += 1
            computed = block.compute_hash()
        block.hash = computed
        return block

    def to_list_of_dicts(self) -> List[Dict[str, Any]]:
        return [asdict(b) for b in self.chain]

    def export_json(self) -> str:
        return json.dumps(self.to_list_of_dicts(), indent=2)

    def import_from_list(self, data: List[Dict[str, Any]]):
        loaded = []
        for item in data:
            b = Block(**item)
            loaded.append(b)
        self.chain = loaded

def fmt_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

# Visual (UI)

st.set_page_config(page_title="André — Simulador Bitcoin (didático)", layout="wide")
st.title("André Felipe — Simulador didático de Bitcoin")
st.markdown(
    "Demonstração da **escassez programada** do Bitcoin com halving. "
    "Este simulador é didático: para ver o comportamento real, ajuste `BLOCKS_PER_HALVING = 210000`."
)

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = SimpleBlockchain()

bc: SimpleBlockchain = st.session_state.blockchain

# painel principal: política monetária
current_reward = bc.current_reward()
total_supply = bc.total_supply()
remaining = max(MAX_SUPPLY - total_supply, 0.0)
remaining_pct = remaining / MAX_SUPPLY * 100.0 if MAX_SUPPLY != 0 else 0.0

st.header("Política Monetária (resumo)")
c1, c2, c3 = st.columns(3)
c1.metric("Recompensa atual por bloco:", f"{current_reward:.4f} BTC")
c2.metric("Total de BTC emitidos (soma de recompensas)", f"{total_supply:,.4f} BTC", f"{remaining_pct:.1f}% restante")
c3.metric("Limite programado (máx.)", f"{MAX_SUPPLY:,.0f} BTC")
st.caption(f"Blocos minerados (exclui gênesis): {bc.blocks_mined} — Halving a cada {bc.blocks_per_halving} blocos")

st.markdown("---")

st.sidebar.header("Mineração e Controles")
difficulty = st.sidebar.slider("Dificuldade (zeros iniciais no hash)", 1, 5, 2)
sender = st.sidebar.text_input("Remetente", value="André")
receiver = st.sidebar.text_input("Destinatário", value="Mercado")
amount = st.sidebar.number_input("Valor da transação (BTC)", min_value=0.0, value=1.0, step=0.1, format="%.1f")
miner_addr = st.sidebar.text_input("Endereço do minerador (recebe a recompensa)", value=MINER_ADDRESS)

st.sidebar.markdown("**Ajustes didáticos**")
if st.sidebar.checkbox("Usar halving real (210000)"):
    bc.blocks_per_halving = 210_000
else:
    bc.blocks_per_halving = st.sidebar.number_input("Blocos por Halving (didático)", min_value=1, value=BLOCKS_PER_HALVING, step=1)

st.sidebar.markdown("---")

def reset_chain():
    st.session_state.blockchain = SimpleBlockchain(blocks_per_halving=bc.blocks_per_halving)
    st.success("Blockchain resetada — Gênesis recriado.")

if st.sidebar.button("Resetar Blockchain"):
    reset_chain()
    st.experimental_rerun()

# minerar bloco
def mine_one_block() -> None:
    # verifica novamente o estado atual
    bc_local: SimpleBlockchain = st.session_state.blockchain

    if bc_local.total_supply() >= MAX_SUPPLY:
        st.warning("Limite de emissão atingido — não há mais recompensa por bloco.")
        return

    reward = bc_local.current_reward()
    if reward <= 0:
        st.warning("Recompensa atual é 0 BTC — nenhum novo BTC será emitido.")
        return

    tx_data = f"{sender} -> {receiver}: {amount:.4f} BTC | recompensa para {miner_addr}"
    new_block = bc_local.add_block(data=tx_data, reward=reward)

    t0 = perf_counter()
    solved = bc_local.proof_of_work(new_block, difficulty)
    elapsed = perf_counter() - t0

    # mensagem de feedback
    st.success(f"Bloco minerado: #{solved.index - 1} — Recompensa: {solved.reward:.4f} BTC")
    st.caption(f"Nonce: {solved.nonce} • Tempo de mineração: {elapsed:.3f}s • Hash: {solved.hash[:14]}...")

    # atualiza o objeto no session_state explicitamente (não estritamente necessário, mas fica claro)
    st.session_state.blockchain = bc_local


if st.sidebar.button("Minerar 1 bloco"):
    with st.spinner("Minerando — buscando..."):
        mine_one_block()
    st.experimental_rerun()

# permitir minerar N blocos rapidamente (útil para demonstrar halvings)
st.sidebar.markdown("Minerar blocos em sequência (para testar halving)")
to_mine = st.sidebar.number_input("Quantidade de blocos para minerar (rápido)", min_value=1, value=1, step=1)
if st.sidebar.button("Minerar N blocos"):
    with st.spinner("Minerando blocos..."):
        for _ in range(int(to_mine)):
            # atualiza referência a cada iteração
            if st.session_state.blockchain.total_supply() >= MAX_SUPPLY:
                st.warning("Limite de emissão atingido — interrompendo.")
                break
            mine_one_block()
    # força re-render ao final da mineração em lote
    st.experimental_rerun()

st.markdown("---")
st.header("Livro-razão (visualização e export)")

# dataframe para mostrar
rows = []
for b in bc.chain:
    rows.append({
        "Index (didático)": b.index - 1,
        "Timestamp": fmt_time(b.timestamp),
        "Recompensa (BTC)": f"{b.reward:.4f}",
        "Transação / Dados": b.data,
        "Hash Anterior": b.previous_hash[:12] + "..." if b.previous_hash != "0" else b.previous_hash,
        "Hash Atual (prefixo)": b.hash[:16],
        "Nonce": b.nonce
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)

col_export, col_import = st.columns(2)
with col_export:
    if st.button("Exportar JSON da cadeia"):
        payload = bc.export_json()
        st.download_button("Download JSON da chain", payload, file_name="chain_export.json", mime="application/json")

with col_import:
    uploaded = st.file_uploader("Importar cadeia (JSON)", type=["json"])
    if uploaded is not None:
        try:
            loaded = json.load(uploaded)
            bc.import_from_list(loaded)
            st.success("Cadeia importada com sucesso.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Erro ao importar: {e}")

st.markdown("---")
st.subheader("Notas didáticas e observações")
st.markdown(
    "- Esse programa é um **simulador**, você não pode minerar de verdade ou comprar bitcoins por aqui!\n"
    "- Se você quer reproduzir o número real de blocos por halving, use 210000 (o comportamento será mais lento para testar).\n"
    "- Em redes reais, a segurança, propagação e validação são muito mais complexas."
)

st.markdown("---")
st.caption("André Felipe dos Santos Ricardo - 2025.")
