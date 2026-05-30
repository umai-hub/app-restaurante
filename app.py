
import streamlit as st

st.set_page_config(page_title="Umai Sushi - Sistema de Comandas", layout="centered")
st.title("🍣 Sistema de Comandas - Umai Sushi")

# CARDÁPIO REAL EXTRAÍDO DA SUA FOTO
CARDAPIO = {
    "Selecione um produto...": {"preco": 0.00, "categoria": "Status"},
    
    # À LA CARTE
    "Carpaccio de Salmão (15 un)": {"preco": 39.00, "categoria": "À La Carte"},
    "Carpaccio de Tilápia (15 un)": {"preco": 35.00, "categoria": "À La Carte"},
    "Tataki de Salmão (250g)": {"preco": 36.00, "categoria": "À La Carte"},
    "Tataki de Tilápia (250g)": {"preco": 32.00, "categoria": "À La Carte"},
    "Salmão Frito (6 un)": {"preco": 40.00, "categoria": "À La Carte"},
    "Camarão Frito (15 un)": {"preco": 29.00, "categoria": "À La Carte"},
    "Guioza (8 un)": {"preco": 34.00, "categoria": "À La Carte"},
    "Ceviche de Tilápia c/ Abacaxi (400g)": {"preco": 32.00, "categoria": "À La Carte"},
    "Ceviche de Salmão (250g)": {"preco": 36.00, "categoria": "À La Carte"},
    "Yakissoba de Carne (500g)": {"preco": 32.00, "categoria": "À La Carte"},
    "Yakissoba de Frango (500g)": {"preco": 28.00, "categoria": "À La Carte"},
    "Yakissoba de Camarão (500g)": {"preco": 36.00, "categoria": "À La Carte"},
    "Harumaki de Queijo (6 un)": {"preco": 30.00, "categoria": "À La Carte"},
    "Harumaki de Camarão (6 un)": {"preco": 30.00, "categoria": "À La Carte"},
    "Robatade Camarão com Queijo Coalho": {"preco": 36.00, "categoria": "À La Carte"},
    "Shimeji (200g)": {"preco": 33.00, "categoria": "À La Carte"},
    
    # TEMAKIS
    "Temaki de Salmão com Arroz (1 un)": {"preco": 26.00, "categoria": "Temakis"},
    "Temaki Temperado de Camarão (1 un)": {"preco": 29.00, "categoria": "Temakis"},
    "Temaki Frito de Salmão (1 un)": {"preco": 30.00, "categoria": "Temakis"},
    "Temaki Frito de Camarão (1 un)": {"preco": 33.00, "categoria": "Temakis"},
    "Hot Philadelphia de Salmão (8 un)": {"preco": 32.00, "categoria": "Temakis"},
    "Hot de Camarão com Arroz (8 un)": {"preco": 36.00, "categoria": "Temakis"},
    
    # JOYS / SASHIMIS / NIGUIRIS
    "Joy com Cream Cheese (8 un)": {"preco": 32.00, "categoria": "Joys/Sashimis"},
    "Joy de Camarão (8 un)": {"preco": 39.00, "categoria": "Joys/Sashimis"},
    "Shakemaki (8 un)": {"preco": 39.00, "categoria": "Joys/Sashimis"},
    "Sashimi de Salmão (5 Lâminas)": {"preco": 30.00, "categoria": "Joys/Sashimis"},
    "Sashimi de Tilápia (5 Lâminas)": {"preco": 30.00, "categoria": "Joys/Sashimis"},
    "Niguiri de Salmão (4 un)": {"preco": 24.00, "categoria": "Joys/Sashimis"},
    "Niguiri de Camarão (4 un)": {"preco": 24.00, "categoria": "Joys/Sashimis"},
    
    # BOXES
    "Box 16 Peças": {"preco": 48.00, "categoria": "Boxes"},
    "Box 26 Peças": {"preco": 78.00, "categoria": "Boxes"},
    
    # BEBIDAS / SOBREMESAS
    "Coca-Cola (310ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
    "Coca-Cola Zero (310ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
    "Água Tônica (350ml)": {"preco": 5.50, "categoria": "Bebidas/Sobremesas"},
    "Água Sem Gás (500ml)": {"preco": 5.00, "categoria": "Bebidas/Sobremesas"},
    "Água Com Gás (500ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
    "Heineken (330ml)": {"preco": 10.00, "categoria": "Bebidas/Sobremesas"},
    "Heineken Zero (330ml)": {"preco": 10.00, "categoria": "Bebidas/Sobremesas"},
    "Harumaki Doce de Leite (1 un)": {"preco": 6.00, "categoria": "Bebidas/Sobremesas"},
    "Harumaki Beijinho (1 un)": {"preco": 6.00, "categoria": "Bebidas/Sobremesas"},
    
    # OUTROS
    "Item Personalizado (Digitar valor)": {"preco": 0.00, "categoria": "Outros"}
}

if 'itens_comanda' not in st.session_state:
    st.session_state.itens_comanda = []

# Identificação na Barra Lateral
st.sidebar.header("📋 Dados de Identificação")

garcom = st.sidebar.selectbox(
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
    item_final = st.text_input("Nome do item personalizado:", placeholder="Ex: Adicional de Shoyu Especial")
else:
    item_final = produto_selecionado

if st.button("Adicionar Item", use_container_width=True):
    if garcom == "Selecione...":
        st.error("Selecione o garçom ou a opção de 'Pedido sem Garçom' na barra lateral.")
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
        st.warning("Selecione um produto válido.")

st.divider()
st.subheader("🧾 Resumo da Comanda")

if st.session_state.itens_comanda:
    st.write(f"**Atendimento:** {garcom}")
    if mesa: st.write(f"**Mesa:** {mesa}")
    if cliente: st.write(f"**Cliente:** {cliente}")
    
    st.write("---")
    valor_produtos = 0.0
    for idx, i in enumerate(st.session_state.itens_comanda):
        st.write(f"{i['qtd']}x — {i['item']} — R$ {i['valor']:.2f} | **Subtotal: R$ {i['subtotal']:.2f}**")
        valor_produtos += i['subtotal']
    
    st.divider()
    
    # Zera taxa caso seja pedido sem garçom
    if garcom == "Pedido sem Garçom (Não cobrar taxa)":
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
    st.info("Nenhum item lançado.")
