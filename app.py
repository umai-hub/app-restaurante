 import streamlit as st
from datetime import datetime

# 1. Configuração inicial obrigatória da página
st.set_page_config(page_title="Umai Sushi Premium", layout="centered")

# 2. Injeção de CSS Seguro para o visual Preto e Dourado
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d !important;
        color: #e5e5e5 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #d4af37 !important;
    }
    .total-box {
        background-color: #1a1a1a;
        color: #d4af37;
        padding: 20px;
        border-radius: 8px;
        border: 2px solid #d4af37;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 15px 0;
    }
    div.stButton > button:first-child {
        background-color: #d4af37 !important;
        color: #0d0d0d !important;
        font-weight: bold !important;
        border: none !important;
    }
    </style>
""", unsafe_allowed_html=True)

# 3. Inicialização do Cardápio na Memória
if 'cardapio' not in st.session_state:
    st.session_state.cardapio = {
        "Carpaccio de Salmão (15 un)": {"preco": 39.00, "categoria": "À La Carte"},
        "Carpaccio de Tilápia (15 un)": {"preco": 35.00, "categoria": "À La Carte"},
        "Tataki de Salmão (250g)": {"preco": 36.00, "categoria": "À La Carte"},
        "Temaki de Salmão com Arroz (1 un)": {"preco": 26.00, "categoria": "Temakis"},
        "Box 16 Peças": {"preco": 48.00, "categoria": "Boxes"},
        "Box 26 Peças": {"preco": 78.00, "categoria": "Boxes"},
        "Coca-Cola (310ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
        "Heineken (330ml)": {"preco": 10.00, "categoria": "Bebidas/Sobremesas"}
    }

if 'comanda_atual' not in st.session_state:
    st.session_state.comanda_atual = []

st.title("🍣 Umai Sushi — Premium PDV")

# Abas de Navegação Principal
aba = st.tabs(["🛒 Lançar Item", "📊 Fechamento / Caixa", "⚙️ Cadastrar Produtos"])

# ----------------------------------------------------
# ABA 1: LANÇAMENTO DE ITENS
# ----------------------------------------------------
with aba[0]:
    st.markdown("<h3 style='color: #d4af37;'>🛒 Lançamento</h3>", unsafe_allowed_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        garcom = st.selectbox("Atendente", ["Selecione...", "Lucas", "Paula", "Rosana", "Pedido sem Garçom (Não cobrar taxa)"])
    with c2:
        mesa = st.text_input("Mesa/Cartão", placeholder="Ex: 05")
        
    cliente = st.text_input("Nome do Cliente (Opcional)")
    
    st.divider()
    
    # Filtro de Categoria
    categorias = ["Todos"] + sorted(list(set(info["categoria"] for info in st.session_state.cardapio.values())))
    categoria_sel = st.selectbox("Filtrar por Categoria", categorias)
    
    if categoria_sel == "Todos":
        itens_filtrados = list(st.session_state.cardapio.keys())
    else:
        itens_filtrados = [p for p, info in st.session_state.cardapio.items() if info["categoria"] == categoria_sel]
        
    produto_sel = st.selectbox("Escolha o Produto", ["Selecione..."] + itens_filtrados)
    
    col_q, col_p = st.columns(2)
    with col_q:
        quantidade = st.number_input("Qtd", min_value=1, value=1, step=1)
    with col_p:
        preco_sugerido = st.session_state.cardapio[produto_sel]["preco"] if produto_sel != "Selecione..." else 0.00
        valor_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, value=preco_sugerido, format="%.2f")
        
    if st.button("➕ INCLUIR ITEM", use_container_width=True):
        if garcom == "Selecione...":
            st.error("Por favor, selecione o Garçom antes de adicionar.")
        elif produto_sel == "Selecione...":
            st.warning("Escolha um produto válido da lista.")
        else:
            subtotal = quantidade * valor_unitario
            st.session_state.comanda_atual.append({
                "garcom": garcom,
                "mesa": mesa,
                "cliente": cliente,
                "item": produto_sel,
                "qtd": quantidade,
                "valor": valor_unitario,
                "subtotal": subtotal
            })
            st.toast(f"{produto_sel} adicionado!")

# ----------------------------------------------------
# ABA 2: VISUALIZAÇÃO E IMPRESSÃO (CAIXA COMPUTER)
# ----------------------------------------------------
with aba[1]:
    st.markdown("<h3 style='color: #d4af37;'>🧾 Resumo da Conta</h3>", unsafe_allowed_html=True)
    
    if not st.session_state.comanda_atual:
        st.info("Nenhum item lançado na comanda corrente.")
    else:
        # Pega dados básicos do primeiro item para o cabeçalho
        info_base = st.session_state.comanda_atual[0]
        st.write(f"**Mesa:** {info_base['mesa']} | **Atendente:** {info_base['garcom']}")
        if info_base['cliente']: st.write(f"**Cliente:** {info_base['cliente']}")
        st.write("---")
        
        total_produtos = 0.0
        for i in st.session_state.comanda_atual:
            st.write(f"🔹 {i['qtd']}x — {i['item']} — R$ {i['valor']:.2f} | **Subtotal: R$ {i['subtotal']:.2f}**")
            total_produtos += i['subtotal']
            
        st.divider()
        
        # Regra de taxa de serviço baseada no garçom
        if info_base['garcom'] == "Pedido sem Garçom (Não cobrar taxa)":
            taxa_porcentagem = 0.0
        else:
            taxa_porcentagem = 10.0
            
        valor_taxa = total_produtos * (taxa_porcentagem / 100.0)
        total_geral = total_produtos + valor_taxa
        
        st.write(f"Subtotal Itens: R$ {total_produtos:.2f}")
        st.write(f"Taxa de Serviço ({taxa_porcentagem}%): R$ {valor_taxa:.2f}")
        
        st.markdown(f"<div class='total-box'>TOTAL GERAL: R$ {total_geral:.2f}</div>", unsafe_allowed_html=True)
        
        # Script HTML para gerar a impressão térmica direta de 80mm
        html_impressao = f"""
        <html>
        <head>
            <style>
                @page {{ size: 80mm auto; margin: 0; }}
                body {{ font-family: 'Courier New', monospace; width: 72mm; font-size: 12px; padding: 10px; color: black; }}
