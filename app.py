
import streamlit as st

st.set_page_config(page_title="Umai Sushi - Sistema de Comandas", layout="centered")
st.title("🍣 Sistema de Comandas - Umai Sushi")

if 'itens_comanda' not in st.session_state:
    st.session_state.itens_comanda = []

st.sidebar.header("📋 Dados de Identificação")
mesa = st.sidebar.text_input("Número da Mesa", placeholder="Ex: 05")
cliente = st.sidebar.text_input("Nome do Cliente", placeholder="Ex: João Silva")

st.subheader("🛒 Lançar Item na Comanda")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    item_nome = st.text_input("Produto/Item", placeholder="Ex: Combo Umai 20 Peças")
with col2:
    quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
with col3:
    valor_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, value=0.0, step=0.50, format="%.2f")

if st.button("Adicionar Item", use_container_width=True):
    if item_nome and valor_unitario > 0:
        subtotal_item = quantidade * valor_unitario
        st.session_state.itens_comanda.append({
            "item": item_nome,
            "qtd": quantidade,
            "valor": valor_unitario,
            "subtotal": subtotal_item
        })
        st.toast(f"{item_nome} adicionado com sucesso!")
    else:
        st.warning("Preencha o nome do item e o valor unitário.")

st.divider()
st.subheader("🧾 Resumo da Comanda")

if st.session_state.itens_comanda:
    if mesa: st.write(f"**Mesa:** {mesa}")
    if cliente: st.write(f"**Cliente:** {cliente}")
    
    st.write("---")
    valor_produtos = 0.0
    for idx, i in enumerate(st.session_state.itens_comanda):
        st.write(f"{i['qtd']}x — {i['item']} — R$ {i['valor']:.2f} | **Subtotal: R$ {i['subtotal']:.2f}**")
        valor_produtos += i['subtotal']
    
    st.divider()
    
    # Cálculos exatos da taxa de 10%
    taxa_servico_percentual = 10.0
    valor_taxa_servico = valor_produtos * (taxa_servico_percentual / 100.0)
    valor_total_geral = valor_produtos + valor_taxa_servico

    st.write(f"**Subtotal dos Produtos:** R$ {valor_produtos:.2f}")
    st.write(f"**Taxa de Serviço ({taxa_servico_percentual}%):** R$ {valor_taxa_servico:.2f}")
    st.success(f"### **Total Geral a Pagar:** R$ {valor_total_geral:.2f}")
    
    if st.button("Limpar Comanda", type="secondary"):
        st.session_state.itens_comanda = []
        st.rerun()
else:
    st.info("Nenhum item lançado na comanda até o momento.")
