import streamlit as st
from datetime import datetime

# 1. Configuração de página (obrigatório ser o primeiro comando ativo)
st.set_page_config(page_title="Umai Sushi Premium", layout="centered")

# 2. Injeção de CSS para visual Preto e Dourado Estilo PDV G6
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d !important;
        color: #e5e5e5 !important;
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
        width: 100% !important;
    }
    </style>
""", unsafe_allowed_html=True)

# 3. Inicialização estável do cardápio e comandos
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

aba = st.tabs(["🛒 Lançar Item", "📊 Fechamento / Caixa", "⚙️ Cadastrar Produtos"])

# ABA 1: LANÇAMENTO
with aba[0]:
    st.markdown("<h3 style='color: #d4af37;'>🛒 Lançamento</h3>", unsafe_allowed_html=True)
    c1, c2 = st.columns(2)
    with c1:
        garcom = st.selectbox("Atendente", ["Selecione...", "Lucas", "Paula", "Rosana", "Pedido sem Garçom (Não cobrar taxa)"])
    with c2:
        mesa = st.text_input("Mesa/Cartão", placeholder="Ex: 05")
    
    cliente = st.text_input("Nome do Cliente (Opcional)")
    st.divider()
    
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
        
    if st.button("➕ INCLUIR ITEM"):
        if garcom == "Selecione...":
            st.error("Selecione o Atendente antes de adicionar.")
        elif produto_sel == "Selecione...":
            st.warning("Escolha um produto válido.")
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

# ABA 2: CAIXA / IMPRESSÃO
with aba[1]:
    st.markdown("<h3 style='color: #d4af37;'>🧾 Resumo da Conta</h3>", unsafe_allowed_html=True)
    if not st.session_state.comanda_atual:
        st.info("Nenhum item lançado.")
    else:
        info_base = st.session_state.comanda_atual[0]
        st.write(f"**Mesa:** {info_base['mesa']} | **Atendente:** {info_base['garcom']}")
        st.write("---")
        
        total_produtos = 0.0
        for i in st.session_state.comanda_atual:
            st.write(f"🔹 {i['qtd']}x — {i['item']} — R$ {i['valor']:.2f} | **R$ {i['subtotal']:.2f}**")
            total_produtos += i['subtotal']
            
        st.divider()
        taxa_porcentagem = 0.0 if "Não cobrar taxa" in info_base['garcom'] else 10.0
        valor_taxa = total_produtos * (taxa_porcentagem / 100.0)
        total_geral = total_produtos + valor_taxa
        
        st.write(f"Subtotal: R$ {total_produtos:.2f}")
        st.write(f"Taxa ({taxa_porcentagem}%): R$ {valor_taxa:.2f}")
        st.markdown(f"<div class='total-box'>TOTAL GERAL: R$ {total_geral:.2f}</div>", unsafe_allowed_html=True)
        
        # HTML do Cupom 80mm
        html_impressao = f"""
        <html><body onload="window.print();" style="font-family:'Courier New',monospace; width:72mm; font-size:12px; color:black;">
            <div style="text-align:center; font-weight:bold; font-size:14px;">UMAI SUSHI PREMIUM</div>
            <hr>
            <div>MESA: {info_base['mesa']}<br>ATENDENTE: {info_base['garcom']}<br>DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
            <hr>
        """
        for item in st.session_state.comanda_atual:
            html_impressao += f"<div>{item['qtd']}x {item['item']}<br>  R$ {item['subtotal']:.2f}</div>"
        html_impressao += f"""
            <hr>
            <div>SUBTOTAL: R$ {total_produtos:.2f}</div>
            <div>TAXA: R$ {valor_taxa:.2f}</div>
            <div style="font-weight:bold; font-size:13px;">TOTAL: R$ {total_geral:.2f}</div>
        </body></html>
        """
        st.download_button("🖨️ IMPRIMIR CONTA", data=html_impressao, file_name="comanda.html", mime="text/html")
        
        if st.button("❌ Limpar Caixa / Próxima Mesa"):
            st.session_state.comanda_atual = []
            st.rerun()

# ABA 3: CADASTRO
with aba[2]:
    st.markdown("<h3 style='color: #d4af37;'>⚙️ Painel do Cardápio</h3>", unsafe_allowed_html=True)
    novo_nome = st.text_input("Nome do Produto")
    nova_cat = st.selectbox("Categoria", ["À La Carte", "Temakis", "Boxes", "Bebidas/Sobremesas", "Outros"])
    novo_preco = st.number_input("Preço", min_value=0.0, value=0.0, format="%.2f")
    if st.button("💾 SALVAR PRODUTO"):
        if novo_nome:
            st.session_state.cardapio[novo_nome] = {"preco": novo_preco, "categoria": nova_cat}
            st.success(f"'{novo_nome}' salvo!")
            st.rerun()
