import streamlit as st
from datetime import datetime

# Configuração de Layout e Tema Escuro/Dourado
st.set_page_config(page_title="Umai Sushi Premium - PDV", layout="centered")

# CSS Customizado - Identidade Visual Umai Premium (Preto, Grafite e Dourado)
st.markdown("""
    <style>
    /* Fundo geral e textos */
    .stApp {
        background-color: #0d0d0d;
        color: #e5e5e5;
    }
    /* Cards de informação */
    .metric-box {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #d4af37;
        margin-bottom: 15px;
    }
    /* Caixa de Total Estilo PDV G6 Premium */
    .total-box {
        background-color: #1a1a1a;
        color: #d4af37;
        padding: 20px;
        border-radius: 8px;
        border: 2px solid #d4af37;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0px 0px 10px rgba(212, 175, 55, 0.2);
    }
    /* Estilização de botões do Streamlit */
    div.stButton > button:first-child {
        background-color: #d4af37 !important;
        color: #0d0d0d !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 5px !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #f3e5ab !important;
        transform: scale(1.02);
    }
    /* Inputs e caixas de seleção */
    .stSelectbox, .stTextInput, .stNumberInput {
        color: white !important;
    }
    </style>
""", unsafe_allowed_html=True)

# Inicialização do Banco de Dados em Memória Temporária (Enquanto estruturamos o Supabase)
if 'cardapio' not in st.session_state:
    st.session_state.cardapio = {
        "Carpaccio de Salmão (15 un)": {"preco": 39.00, "categoria": "À La Carte"},
        "Carpaccio de Tilápia (15 un)": {"preco": 35.00, "categoria": "À La Carte"},
        "Yakissoba de Carne (500g)": {"preco": 32.00, "categoria": "À La Carte"},
        "Temaki de Salmão com Arroz (1 un)": {"preco": 26.00, "categoria": "Temakis"},
        "Box 16 Peças": {"preco": 48.00, "categoria": "Boxes"},
        "Box 26 Peças": {"preco": 78.00, "categoria": "Boxes"},
        "Coca-Cola (310ml)": {"preco": 6.50, "categoria": "Bebidas"},
        "Heineken (330ml)": {"preco": 10.00, "categoria": "Bebidas"}
    }

if 'mesas_ativas' not in st.session_state:
    st.session_state.mesas_ativas = {}

# Menu Superior para navegação entre telas do sistema
aba = st.radio("Navegação", ["🛒 Lançar Comanda", "🖥️ Painel Caixa (Computador)", "⚙️ Gerenciar Cardápio"], horizontal=True)

# ----------------------------------------------------
# ABA 1: LANÇAMENTO (Para os Celulares dos Garçons)
# ----------------------------------------------------
if aba == "🛒 Lançar Comanda":
    st.markdown("<h2 style='color: #d4af37;'>🛒 Nova Venda / Comanda</h2>", unsafe_allowed_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        garcom = st.selectbox("Garçom", ["Selecione...", "Lucas", "Paula", "Rosana", "Pedido sem Garçom"])
    with c2:
        num_mesa = st.text_input("Nº Mesa / Cartão", placeholder="Ex: 05")
        
    cliente = st.text_input("Cliente (Opcional)")

    st.divider()

    # Filtro e Seleção do Produto
    categorias = ["Todos"] + sorted(list(set(info["categoria"] for info in st.session_state.cardapio.values())))
    cat_sel = st.selectbox("Categoria", categorias)
    
    if cat_sel == "Todos":
        produtos_f = list(st.session_state.cardapio.keys())
    else:
        produtos_f = [p for p, info in st.session_state.cardapio.items() if info["categoria"] == cat_sel]
        
    prod_sel = st.selectbox("Produto", ["Selecione..."] + produtos_f)
    
    cq, cp = st.columns(2)
    with cq:
        qtd = st.number_input("Quantidade", min_value=1, value=1)
    with cp:
        preco_base = st.session_state.cardapio[prod_sel]["preco"] if prod_sel != "Selecione..." else 0.0
        preco_un = st.number_input("Preço (R$)", min_value=0.0, value=preco_base, format="%.2f")

    if st.button("➕ ADICIONAR ITEM À MESA", use_container_width=True):
        if garcom == "Selecione..." or not num_mesa:
            st.error("Identifique o Garçom e o número da Mesa.")
        elif prod_sel == "Selecione...":
            st.warning("Escolha um produto válido.")
        else:
            # Inicializa a mesa caso não exista
            if num_mesa not in st.session_state.mesas_ativas:
                st.session_state.mesas_ativas[num_mesa] = {"garcom": garcom, "cliente": cliente, "itens": []}
            
            st.session_state.mesas_ativas[num_mesa]["itens"].append({
                "produto": prod_sel,
                "qtd": qtd,
                "preco": preco_un,
                "subtotal": qtd * preco_un
            })
            st.toast(f"{prod_sel} adicionado à Mesa {num_mesa}!")

# ----------------------------------------------------
# ABA 2: CAIXA E IMPRESSÃO (Para o Computador)
# ----------------------------------------------------
elif aba == "🖥️ Painel Caixa (Computador)":
    st.markdown("<h2 style='color: #d4af37;'>🖥️ Monitor de Mesas e Impressão</h2>", unsafe_allowed_html=True)
    
    if not st.session_state.mesas_ativas:
        st.info("Nenhuma mesa com consumo em aberto no momento.")
    else:
        mesa_foco = st.selectbox("Escolha a Mesa para Fechamento/Impressão", list(st.session_state.mesas_ativas.keys()))
        
        dados = st.session_state.mesas_ativas[mesa_foco]
        
        st.markdown(f"""
        <div class='metric-box'>
            <strong>Mesa:</strong> {mesa_foco} | <strong>Atendente:</strong> {dados['garcom']}<br>
            <strong>Cliente:</strong> {dados['cliente'] if dados['cliente'] else 'Não Informado'}
        </div>
        """, unsafe_allowed_html=True)
        
        total_itens = 0.0
        for item in dados["itens"]:
            st.write(f"▪️ {item['qtd']}x {item['produto']} — R$ {item['preco']:.2f} | **R$ {item['subtotal']:.2f}**")
            total_itens += item["subtotal"]
            
        taxa = 0.0 if dados["garcom"] == "Pedido sem Garçom" else total_itens * 0.10
        total_geral = total_itens + taxa
        
        st.markdown(f"""
            <div class='total-box'>
                SUBTOTAL: R$ {total_itens:.2f}<br>
                TAXA (10%): R$ {taxa:.2f}<br>
                TOTAL GERAL: R$ {total_geral:.2f}
            </div>
        """, unsafe_allowed_html=True)
        
        # Sistema de Impressão Térmica via Navegador (Otimizado para 80mm)
        cupom_html = f"""
        <html>
        <head>
            <style>
                @page {{ size: 80mm auto; margin: 0; }}
                body {{ font-family: 'Courier New', Courier, monospace; width: 72mm; font-size: 12px; padding: 5px; background: white; color: black; }}
                .text-center {{ text-align: center; }}
                .bold {{ font-weight: bold; }}
                .line {{ border-top: 1px dashed #000; margin: 5px 0; }}
            </style>
        </head>
        <body>
            <div class="text-center bold" style="font-size: 16px;">UMAI SUSHI PREMIUM</div>
            <div class="text-center">Comanda Eletrônica de Consumo</div>
            <div class="line"></div>
            <div><strong>MESA:</strong> {mesa_foco}</div>
            <div><strong>ATENDENTE:</strong> {dados['garcom']}</div>
            <div><strong>DATA:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
            <div class="line"></div>
            <div class="bold">ITENS LANÇADOS:</div>
        """
        for item in dados["itens"]:
            cupom_html += f"<div>{item['qtd']}x {item['produto']}<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;R$ {item['subtotal']:.2f}</div>"
            
        cupom_html += f"""
            <div class="line"></div>
            <div>SUBTOTAL: R$ {total_itens:.2f}</div>
            <div>TAXA SERV.: R$ {taxa:.2f}</div>
            <div class="bold" style="font-size: 14px;">TOTAL: R$ {total_geral:.2f}</div>
            <div class="line"></div>
            <div class="text-center bold">OBRIGADO PELA PREFERÊNCIA!</div>
            <script>window.print();</script>
        </body>
        </html>
        """
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.download_button("🖨️ DISPARAR IMPRESSÃO", data=cupom_html, file_name=f"comanda_{mesa_foco}.html", mime="text/html")
        with col_b2:
            if st.button("✅ FINALIZAR E PAGAR MESA", type="secondary"):
                del st.session_state.mesas_ativas[mesa_foco]
                st.rerun()

# ----------------------------------------------------
# ABA 3: ADMINISTRAÇÃO (Alterar Preços na Hora)
# ----------------------------------------------------
elif aba == "⚙️ Gerenciar Cardápio":
    st.markdown("<h2 style='color: #d4af37;'>⚙️ Painel de Controle de Itens</h2>", unsafe_allowed_html=True)
    
    st.write("### Adicionar ou Alterar Preço de Produto")
    nome_p = st.text_input("Nome do Produto")
    cat_p = st.selectbox("Categoria do Produto", ["À La Carte", "Temakis", "Boxes", "Bebidas", "Sobremesas", "Outros"])
    preco_p = st.number_input("Preço de Venda (R$)", min_value=0.0, value=0.0, format="%.2f")
    
    if st.button("💾 SALVAR PRODUTO NO CARDÁPIO"):
        if nome_p:
            st.session_state.cardapio[nome_p] = {"preco": preco_p, "categoria": cat_p}
            st.success(f"Produto '{nome_p}' salvo com sucesso!")
            st.rerun()
            
    st.write("---")
    st.write("### Itens Cadastrados Atualmente")
    for prod, info in st.session_state.cardapio.items():
        st.write(f"🔸 **{prod}** ({info['categoria']}) — R$ {info['preco']:.2f}")
