import streamlit as st
from datetime import datetime

# 1. Configuração inicial da página (obrigatório ser o primeiro comando)
st.set_page_config(page_title="Umai Sushi Premium", layout="centered")

# 2. CSS Customizado - Identidade Visual Preto e Dourado Premium
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

# 3. Cardápio Completo na Memória Local do Tablet
if 'cardapio' not in st.session_state:
    st.session_state.cardapio = {
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
        "Temaki de Salmão com Arroz (1 un)": {"preco": 26.00, "categoria": "Temakis"},
        "Temaki Temperado de Camarão (1 un)": {"preco": 29.00, "categoria": "Temakis"},
        "Temaki Frito de Salmão (1 un)": {"preco": 30.00, "categoria": "Temakis"},
        "Temaki Frito de Camarão (1 un)": {"preco": 33.00, "categoria": "Temakis"},
        "Hot Philadelphia de Salmão (8 un)": {"preco": 32.00, "categoria": "Temakis"},
        "Hot de Camarão com Arroz (8 un)": {"preco": 36.00, "categoria": "Temakis"},
        "Joy com Cream Cheese (8 un)": {"preco": 32.00, "categoria": "Joys/Sashimis"},
        "Joy de Camarão (8 un)": {"preco": 39.00, "categoria": "Joys/Sashimis"},
        "Shakemaki (8 un)": {"preco": 39.00, "categoria": "Joys/Sashimis"},
        "Sashimi de Salmão (5 Lâminas)": {"preco": 30.00, "categoria": "Joys/Sashimis"},
        "Sashimi de Tilápia (5 Lâminas)": {"preco": 30.00, "categoria": "Joys/Sashimis"},
        "Niguiri de Salmão (4 un)": {"preco": 24.00, "categoria": "Joys/Sashimis"},
        "Niguiri de Camarão (4 un)": {"preco": 24.00, "categoria": "Joys/Sashimis"},
        "Box 16 Peças": {"preco": 48.00, "categoria": "Boxes"},
        "Box 26 Peças": {"preco": 78.00, "categoria": "Boxes"},
        "Coca-Cola (310ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
        "Coca-Cola Zero (310ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
        "Água Tônica (350ml)": {"preco": 5.50, "categoria": "Bebidas/Sobremesas"},
        "Água Sem Gás (500ml)": {"preco": 5.00, "categoria": "Bebidas/Sobremesas"},
        "Água Com Gás (500ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
        "Heineken (330ml)": {"preco": 10.00, "categoria": "Bebidas/Sobremesas"},
        "Heineken Zero (330ml)": {"preco": 10.00, "categoria": "Bebidas/Sobremesas"},
        "Harumaki Doce de Leite (1 un)": {"preco": 6.00, "categoria": "Bebidas/Sobremesas"},
        "Harumaki Beijinho (1 un)": {"preco": 6.00, "categoria": "Bebidas/Sobremesas"}
    }

if 'comandas' not in st.session_state:
    st.session_state.comandas = {}

st.title("🍣 Umai Sushi — Tablet PDV")

# Abas de Navegação
aba = st.tabs(["🛒 Lançar Item", "📊 Fechamento / Caixa", "⚙️ Cadastrar Itens"])

# ----------------------------------------------------
# ABA 1: LANÇAMENTO DE ITENS
# ----------------------------------------------------
with aba[0]:
    st.markdown("<h3 style='color: #d4af37;'>🛒 Lançamento</h3>", unsafe_allowed_html=True)
    c1, c2 = st.columns(2)
    with c1:
        garcom = st.selectbox("Atendente", ["Selecione...", "Lucas", "Paula", "Rosana", "Pedido sem Garçom"])
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
        elif not mesa:
            st.error("Informe o número da Mesa ou Cartão.")
        elif produto_sel == "Selecione...":
            st.warning("Escolha um produto válido.")
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
            st.toast(f"{produto_sel} adicionado à Mesa {mesa}!")

# ----------------------------------------------------
# ABA 2: FECHAMENTO & IMPRESSÃO WI-FI
# ----------------------------------------------------
with aba[1]:
    st.markdown("<h3 style='color: #d4af37;'>🧾 Resumo da Conta</h3>", unsafe_allowed_html=True)
    mesas_ativas = list(st.session_state.comandas.keys())
    
    if not mesas_ativas:
        st.info("Nenhuma mesa ativa no momento.")
    else:
        mesa_sel = st.selectbox("Selecione a Mesa para Fechamento", mesas_ativas)
        comanda_foco = st.session_state.comandas[mesa_sel]
        
        if comanda_foco:
            info_base = comanda_foco[0]
            st.write(f"**Mesa:** {mesa_sel} | **Atendente:** {info_base['garcom']}")
            if info_base['cliente']: st.write(f"**Cliente:** {info_base['cliente']}")
            st.write("---")
            
            total_produtos = 0.0
            for i in comanda_foco:
                st.write(f"🔹 {i['qtd']}x — {i['item']} — R$ {i['valor']:.2f} | **R$ {i['subtotal']:.2f}**")
                total_produtos += i['subtotal']
                
            st.divider()
            taxa_porcentagem = 0.0 if "Pedido sem Garçom" in info_base['garcom'] else 10.0
            valor_taxa = total_produtos * (taxa_porcentagem / 100.0)
            total_geral = total_produtos + valor_taxa
            
            st.write(f"Subtotal: R$ {total_produtos:.2f}")
            st.write(f"Taxa ({taxa_porcentagem}%): R$ {valor_taxa:.2f}")
            st.markdown(f"<div class='total-box'>TOTAL GERAL: R$ {total_geral:.2f}</div>", unsafe_allowed_html=True)
            
            # HTML formatado para Cupom Térmico de 80mm/58mm padrão de rede
            html_impressao = f"""
            <html><body onload="window.print();" style="font-family:'Courier New',monospace; width:72mm; font-size:12px; color:black; padding:5px;">
                <div style="text-align:center; font-weight:bold; font-size:14px;">UMAI SUSHI PREMIUM</div>
                <hr style="border-top: 1px dashed #000;">
                <div>MESA: {mesa_sel}<br>ATENDENTE: {info_base['garcom']}<br>DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
                <hr style="border-top: 1px dashed #000;">
            """
            for item in comanda_foco:
                html_impressao += f"<div>{item['qtd']}x {item['item']}<br>  R$ {item['subtotal']:.2f}</div>"
            html_impressao += f"""
                <hr style="border-top: 1px dashed #000;">
                <div>SUBTOTAL: R$ {total_produtos:.2f}</div>
                <div>TAXA: R$ {valor_taxa:.2f}</div>
                <div style="font-weight:bold; font-size:13px;">TOTAL: R$ {total_geral:.2f}</div>
            </body></html>
            """
            
            # Dispara o arquivo para o sistema de impressão do tablet via Wi-Fi
            st.download_button("🖨️ ENVIAR PARA IMPRESSORA WI-FI", data=html_impressao, file_name=f"mesa_{mesa_sel}.html", mime="text/html")
            
            if st.button("❌ Finalizar e Zerar Mesa"):
                del st.session_state.comandas[mesa_sel]
                st.success(f"Mesa {mesa_sel} encerrada!")
                st.rerun()

# ----------------------------------------------------
# ABA 3: GERENCIAR E EDITAR CARDÁPIO
# ----------------------------------------------------
with aba[2]:
    st.markdown("<h3 style='color: #d4af37;'>⚙️ Gerenciar Cardápio</h3>", unsafe_allowed_html=True)
    novo_nome = st.text_input("Nome do Produto")
    nova_cat = st.selectbox("Categoria", ["À La Carte", "Temakis", "Boxes", "Bebidas/Sobremesas", "Outros"])
    novo_preco = st.number_input("Preço (R$)", min_value=0.0, value=0.0, format="%.2f")
    
    if st.button("💾 SALVAR PRODUTO"):
        if novo_nome:
            st.session_state.cardapio[novo_nome] = {"preco": novo_preco, "categoria": nova_cat}
            st.success(f"'{novo_nome}' atualizado com sucesso!")
            st.rerun()
            
    st.write("---")
    st.write("### Itens Ativos:")
    for p, info in st.session_state.cardapio.items():
        st.write(f"🔸 **{p}** | R$ {info['preco']:.2f} ({info['categoria']})")
