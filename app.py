import streamlit as st
from datetime import datetime

# 1. Configuração estrita de página (Sempre o primeiro comando)
st.set_page_config(page_title="Umai Sushi Premium", layout="wide", initial_sidebar_state="collapsed")

# 2. Design de Interface Profissional (Preto Premium & Ouro) - Sem elementos grotescos
st.markdown("""
    <style>
    /* Fundo Escuro Absoluto */
    .stApp {
        background-color: #0d0d0d !important;
        color: #e5e5e5 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Customização das Abas (Tabs) */
    div[data-testid="stTabBar"] {
        background-color: #141414;
        border-radius: 10px;
        padding: 5px;
        border: 1px solid #262626;
        margin-bottom: 25px;
    }
    button[data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Container de Produto (Estilo Card Cardápio) */
    .product-card {
        background: linear-gradient(135deg, #141414 0%, #1a1a1a 100%);
        border: 1px solid #262626;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .product-card:hover {
        border-color: #d4af37;
        transform: translateY(-2px);
    }
    .product-title {
        color: #ffffff;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .product-price {
        color: #d4af37;
        font-size: 15px;
        font-weight: 600;
    }
    
    /* Caixa de Totalizadores */
    .total-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #111111 100%);
        color: #d4af37;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #d4af37;
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 1px;
        box-shadow: 0 8px 16px rgba(212,175,55,0.1);
        margin: 20px 0;
    }
    
    /* Botões Padrão Ouro */
    div.stButton > button {
        background: linear-gradient(90deg, #d4af37 0%, #aa841c 100%) !important;
        color: #0d0d0d !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(212,175,55,0.2) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Botões de Perigo/Limpeza */
    div[data-testid="stHorizontalBlock"] button[style*="secondary"] {
        background: #1a1a1a !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
    }
    
    /* Tabelas e Inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #141414 !important;
        color: #ffffff !important;
        border: 1px solid #262626 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allowed_html=True)

# 3. Cardápio Completo Estruturado
CARDAPIO = {
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
    # TEMAKIS / HOTS
    "Temaki de Salmão com Arroz (1 un)": {"preco": 26.00, "categoria": "Temakis e Hots"},
    "Temaki Temperado de Camarão (1 un)": {"preco": 29.00, "categoria": "Temakis e Hots"},
    "Temaki Frito de Salmão (1 un)": {"preco": 30.00, "categoria": "Temakis e Hots"},
    "Temaki Frito de Camarão (1 un)": {"preco": 33.00, "categoria": "Temakis e Hots"},
    "Hot Philadelphia de Salmão (8 un)": {"preco": 32.00, "categoria": "Temakis e Hots"},
    "Hot de Camarão com Arroz (8 un)": {"preco": 36.00, "categoria": "Temakis e Hots"},
    # JOYS / SASHIMIS / NIGUIRIS
    "Joy com Cream Cheese (8 un)": {"preco": 32.00, "categoria": "Joys/Sashimis/Niguiris"},
    "Joy de Camarão (8 un)": {"preco": 39.00, "categoria": "Joys/Sashimis/Niguiris"},
    "Shakemaki (8 un)": {"preco": 39.00, "categoria": "Joys/Sashimis/Niguiris"},
    "Sashimi de Salmão (5 Lâminas)": {"preco": 30.00, "categoria": "Joys/Sashimis/Niguiris"},
    "Sashimi de Tilápia (5 Lâminas)": {"preco": 30.00, "categoria": "Joys/Sashimis/Niguiris"},
    "Niguiri de Salmão (4 un)": {"preco": 24.00, "categoria": "Joys/Sashimis/Niguiris"},
    "Niguiri de Camarão (4 un)": {"preco": 24.00, "categoria": "Joys/Sashimis/Niguiris"},
    # BOXES
    "Box 16 Peças": {"preco": 48.00, "categoria": "Boxes"},
    "Box 26 Peças": {"preco": 78.00, "categoria": "Boxes"},
    # BEBIDAS / SOBREMESAS
    "Coca-Cola (310ml)": {"preco": 6.50, "categoria": "Bebidas e Sobremesas"},
    "Coca-Cola Zero (310ml)": {"preco": 6.50, "categoria": "Bebidas e Sobremesas"},
    "Água Tônica (350ml)": {"preco": 5.50, "categoria": "Bebidas e Sobremesas"},
    "Água Sem Gás (500ml)": {"preco": 5.00, "categoria": "Bebidas e Sobremesas"},
    "Água Com Gás (500ml)": {"preco": 6.50, "categoria": "Bebidas e Sobremesas"},
    "Heineken (330ml)": {"preco": 10.00, "categoria": "Bebidas e Sobremesas"},
    "Heineken Zero (330ml)": {"preco": 10.00, "categoria": "Bebidas e Sobremesas"},
    "Harumaki Doce de Leite (1 un)": {"preco": 6.00, "categoria": "Bebidas e Sobremesas"},
    "Harumaki Beijinho (1 un)": {"preco": 6.00, "categoria": "Bebidas e Sobremesas"}
}

# 4. Inicialização Segura de Memória Local
if 'comandas' not in st.session_state:
    st.session_state.comandas = {}

st.title("🍣 Umai Sushi — PDV Premium")

aba = st.tabs(["🛒 Lançar Item", "📊 Painel do Caixa"])

# ----------------------------------------------------
# ABA 1: LANÇAMENTO DE ITENS
# ----------------------------------------------------
with aba[0]:
    st.markdown("<h3 style='color: #d4af37;'>🛒 Novo Pedido</h3>", unsafe_allowed_html=True)
    
    # Informações de Identificação
    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    with c1:
        garcom = st.selectbox("Atendente", ["Selecione...", "Lucas", "Paula", "Rosana", "Pedido Balcão / Sem Garçom"])
    with c2:
        mesa = st.text_input("Mesa / Cartão", placeholder="Ex: 05")
    with c3:
        cliente = st.text_input("Nome do Cliente (Opcional)")
        
    st.divider()
    
    # Filtro Dinâmico de Categorias do Cardápio
    categorias = ["Todos"] + sorted(list(set(info["categoria"] for info in CARDAPIO.values())))
    categoria_sel = st.selectbox("Filtrar Categoria", categorias)
    
    if categoria_sel == "Todos":
        itens_filtrados = list(CARDAPIO.keys())
    else:
        itens_filtrados = [p for p, info in CARDAPIO.items() if info["categoria"] == categoria_sel]
        
    produto_sel = st.selectbox("Escolha o Produto", ["Selecione um item..."] + itens_filtrados)
    
    # Exibição do Card em Destaque do Produto Selecionado
    if produto_sel != "Selecione um item...":
        preco_base = CARDAPIO[produto_sel]["preco"]
        st.markdown(f"""
            <div class="product-card">
                <div class="product-title">{produto_sel}</div>
                <div class="product-price">Preço Base: R$ {preco_base:.2f}</div>
            </div>
        """, unsafe_allowed_html=True)
    else:
        preco_base = 0.00
        
    col_q, col_p = st.columns(2)
    with col_q:
        quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
    with col_p:
        valor_unitario = st.number_input("Preço Unitário Praticado (R$)", min_value=0.0, value=preco_base, format="%.2f")
        
    if st.button("➕ ADICIONAR ITEM À COMANDA", use_container_width=True):
        if garcom == "Selecione...":
            st.error("Erro: Identifique o Atendente responsável.")
        elif not mesa:
            st.error("Erro: Insira o número da Mesa ou Cartão.")
        elif produto_sel == "Selecione um item...":
            st.warning("Aviso: Escolha um produto do cardápio.")
        else:
            subtotal = quantidade * valor_unitario
            if mesa not in st.session_state.comandas:
                st.session_state.comandas[mesa] = []
                
            st.session_state.comandas[mesa].append({
                "garcom": garcom,
                "cliente": cliente,
                "item": produto_sel,
                "qtd": quantidade,
                "valor": valor_unitario,
                "subtotal": subtotal
            })
            st.success(f"{produto_sel} (x{quantidade}) adicionado à Mesa {mesa}!")

# ----------------------------------------------------
# ABA 2: PAINEL DO CAIXA E IMPRESSÃO WI-FI
# ----------------------------------------------------
with aba[1]:
    st.markdown("<h3 style='color: #d4af37;'>📊 Contas Ativas</h3>", unsafe_allowed_html=True)
    mesas_ativas = sorted(list(st.session_state.comandas.keys()))
    
    if not mesas_ativas:
        st.info("Nenhuma mesa ou comanda em aberto no momento.")
    else:
        mesa_sel = st.selectbox("Selecione a Mesa para Visualizar / Fechar", mesas_ativas)
        comanda_foco = st.session_state.comandas[mesa_sel]
        
        if comanda_foco:
            info_base = comanda_foco[0]
            
            # Cabeçalho do Resumo da Conta
            st.markdown(f"""
                <div style="background-color: #141414; padding: 15px; border-radius: 8px; border-left: 4px solid #d4af37; margin-bottom: 20px;">
                    <b>MESA / CARTÃO:</b> {mesa_sel} | <b>ATENDENTE:</b> {info_base['garcom']}<br>
                    {'<b>CLIENTE:</b> ' + info_base['cliente'] if info_base['cliente'] else ''}
                </div>
            """, unsafe_allowed_html=True)
            
            total_produtos = 0.0
            
            # Listagem Limpa e Elegante dos Itens Consumidos
            for idx, i in enumerate(comanda_foco):
                c_item, c_del = st.columns([5, 1])
                with c_item:
                    st.markdown(f"🔹 **{i['qtd']}x** — {i['item']} — R$ {i['valor']:.2f} | **Subtotal: R$ {i['subtotal']:.2f}**")
                with c_del:
                    if st.button("🗑️", key=f"del_{mesa_sel}_{idx}"):
                        comanda_foco.pop(idx)
                        if not comanda_foco:
                            del st.session_state.comandas[mesa_sel]
                        st.rerun()
                total_produtos += i['subtotal']
                
            st.divider()
            
            # Regra de Taxa de Serviço Automática
            taxa_porcentagem = 0.0 if "Sem Garçom" in info_base['garcom'] else 10.0
            valor_taxa = total_produtos * (taxa_porcentagem / 100.0)
            total_geral = total_produtos + valor_taxa
            
            # Exibição Financeira Detalhada
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.write(f"Consumo de Produtos: R$ {total_produtos:.2f}")
                st.write(f"Taxa de Serviço ({taxa_porcentagem}%): R$ {valor_taxa:.2f}")
            with col_f2:
                st.markdown(f"<div class='total-box'>TOTAL: R$ {total_geral:.2f}</div>", unsafe_allowed_html=True)
            
            # Geração de Código HTML Puro para Impressora Térmica via Wi-Fi (Sem dependências quebradas)
            html_impressao = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{ size: 80mm auto; margin: 0; }}
                    body {{ font-family: 'Courier New', monospace; width: 72mm; font-size: 12px; color: #000; padding: 10px; }}
                    .center {{ text-align: center; font-weight: bold; font-size: 14px; }}
                    .line {{ border-top: 1px dashed #000; margin: 8px 0; }}
                    .item-row {{ margin-bottom: 5px; }}
                </style>
            </head>
            <body onload="window.print();">
                <div class="center">UMAI SUSHI PREMIUM</div>
                <div class="center">*** CONTA PROVISÓRIA ***</div>
                <div class="line"></div>
                <div><b>MESA:</b> {mesa_sel}</div>
                <div><b>ATENDENTE:</b> {info_base['garcom']}</div>
                <div><b>DATA/HORA:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
                <div class="line"></div>
            """
            for item in comanda_foco:
                html_impressao += f'<div class="item-row">{item["qtd"]}x {item["item"]}<br>&nbsp;&nbsp;-> R$ {item["subtotal"]:.2f}</div>'
                
            html_impressao += f"""
                <div class="line"></div>
                <div>SUBTOTAL: R$ {total_produtos:.2f}</div>
                <div>TAXA SERV ({taxa_porcentagem}%): R$ {valor_taxa:.2f}</div>
                <div style="font-weight: bold; font-size: 13px; margin-top: 5px;">TOTAL GERAL: R$ {total_geral:.2f}</div>
                <div class="line"></div>
                <div style="text-align: center; font-style: italic;">Obrigado pela preferência!</div>
            </body>
            </html>
            """
            
            st.divider()
            
            # Ações Principais do Caixa
            st.download_button("🖨️ MANDAR PARA IMPRESSORA WI-FI", data=html_impressao, file_name=f"comanda_mesa_{mesa_sel}.html", mime="text/html")
            
            st.write("")
            if st.button("❌ FINALIZAR PAGAMENTO E ZERAR MESA"):
                del st.session_state.comandas[mesa_sel]
                st.success(f"Mesa {mesa_sel} fechada e limpa com sucesso!")
                st.rerun()
