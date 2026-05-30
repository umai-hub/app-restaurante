import streamlit as st

st.set_page_config(page_title="Umai Sushi - Sistema de Comandas", layout="centered")
st.title("🍣 Sistema de Comandas - Umai Sushi")

# CARDÁPIO COMPLETO INTEGRADO COPIADO DO SEU CATÁLOGO
CARDAPIO = {
    "Selecione um produto...": {"preco": 0.00, "categoria": "Status"},
    
    # ENTRADAS / PETISCOS
    "Sunomono Tradicional": {"preco": 15.00, "categoria": "Entradas"},
    "Shimeji na Manteiga": {"preco": 28.00, "categoria": "Entradas"},
    "Hot Roll Salmão (10 un)": {"preco": 25.00, "categoria": "Entradas"},
    "Gyoza de Carne (6 un)": {"preco": 22.00, "categoria": "Entradas"},
    "Harumaki de Queijo (4 un)": {"preco": 18.00, "categoria": "Entradas"},
    
    # TEMAKIS
    "Temaki Salmão Completo": {"preco": 32.00, "categoria": "Temakis"},
    "Temaki Salmão Grelhado": {"preco": 30.00, "categoria": "Temakis"},
    "Temaki Hot Frito": {"preco": 34.00, "categoria": "Temakis"},
    "Temaki Filadélfia": {"preco": 33.00, "categoria": "Temakis"},
    
    # COMBOS UMAI
    "Combo Individual (12 Peças)": {"preco": 45.00, "categoria": "Combos"},
    "Combo Umai Executivo (20 Peças)": {"preco": 65.00, "categoria": "Combos"},
    "Combo Casal Premium (40 Peças)": {"preco": 120.00, "categoria": "Combos"},
    "Combo Umai Família (60 Peças)": {"preco": 175.00, "categoria": "Combos"},
    "Festival Umai em Casa (30 Peças)": {"preco": 95.00, "categoria": "Combos"},
    
    # BEBIDAS
    "Refrigerante Lata": {"preco": 6.50, "categoria": "Bebidas"},
    "Água Mineral Sem Gás": {"preco": 5.00, "categoria": "Bebidas"},
    "Água Mineral Com Gás": {"preco": 5.50, "categoria": "Bebidas"},
    "Suco Natural Del Valle": {"preco": 8.00, "categoria": "Bebidas"},
    "Cerveja Long Neck": {"preco": 9.50, "categoria": "Bebidas"},
    
    # ADICIONAIS / OUTROS
    "Item Personalizado (Digitar valor)": {"preco": 0.00, "categoria": "Outros"}
}

if 'itens_comanda' not in st.session_state:
    st.session_state.itens_comanda = []

# Identificação na Barra Lateral
st.sidebar.header("📋 Dados de Identificação")

# Seleção do Atendente/Garçom com opção sem taxa
garçom = st.sidebar.selectbox(
    "Selecione o Garçom", 
    ["Selecione...", "Lucas", "Paula", "Rosana", "Pedido sem Garçom (Não cobrar taxa)"]
)

mesa = st.sidebar.text_input("Número da Mesa", placeholder="Ex: 05")
cliente = st.sidebar.text_input("Nome do Cliente", placeholder="Ex: João Silva")

st.subheader("🛒 Lançar Item na Comanda")

# Filtro por Categoria
categorias_disponiveis = ["Todos"] + sorted(list(set(info["categoria"] for info in CARDAPIO.values() if info["categoria"] != "Status")))
categoria_selecionada = st.selectbox("Filtrar por Categoria", categorias_disponiveis)

if categoria_selecionada == "Todos":
    itens_filtrados = list(CARDAPIO.keys())
else:
    itens_filtrados = ["Selecione um produto..."] + [item for item, info in CARDAPIO.items() if info["categoria"] == categoria_selecionada]

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    produto_selecionado = st.selectbox("Escolha o Produto", itens_filtrados)

with col3:
    preco_sugerido = CARDAPIO[produto_selecionado]["preco"] if produto_selecionado in CARDAPIO else 0.00
    valor_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, value=preco_sugerido, step=0.50, format="%.2f")

with col2:
    quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)

if produto_selecionado == "Item Personalizado (Digitar valor)":
    item_final = st.text_input("Nome do item personalizado:", placeholder="Ex: Adicional de Cream Cheese")
else:
    item_final = produto_selecionado

if st.button("Adicionar Item", use_container_width=True):
    if garçom == "Selecione...":
        st.error("Por favor, selecione o atendimento na barra lateral antes de adicionar itens.")
    elif produto_selecionado != "Selecione um produto..." and valor_unitario > 0:
        subtotal_item = quantidade * valor_unitario
        st.session_state.itens_comanda.append({
            "item": item_final,
            "qtd": quantidade,
            "valor": valor_unitario,
            "subtotal": subtotal_item
        })
        st.toast(f"{item_final} adicionado!")
    else:
        st.warning("Selecione um produto e defina o valor correto.")

st.divider()
st.subheader("🧾 Resumo da Comanda")

if st.session_state.itens_comanda:
    st.write(f"**Atendimento:** {garçom}")
    if mesa: st.write(f"**Mesa:** {mesa}")
    if cliente: st.write(f"**Cliente:** {cliente}")
    
    st.write("---")
    valor_produtos = 0.0
    for idx, i in enumerate(st.session_state.itens_comanda):
        st.write(f"{i['qtd']}x — {i['item']} — R$ {i['valor']:.2f} | **Subtotal: R$ {i['subtotal']:.2f}**")
        valor_produtos += i['subtotal']
    
    st.divider()
    
    # Lógica da Taxa de Serviço condicional
    if garçom == "Pedido sem Garçom (Não cobrar taxa)":
        taxa_servico_percentual = 0.0
    else:
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
    st.info("Nenhum item lançado para esta mesa.")
