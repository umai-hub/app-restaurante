import streamlit as st
from datetime import datetime
import requests
import json

# 1. Configuração estrita de página inicial
st.set_page_config(page_title="Umai Sushi Premium", layout="centered")

# 2. Injeção de CSS - Identidade Visual Preto e Dourado Estilo G6
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

# 3. Definição do Cardápio Fixo para Evitar Falhas de Inicialização Móvel
CARDAPIO_FIXO = {
    "Carpaccio de Salmão (15 un)": {"preco": 39.00, "categoria": "À La Carte"},
    "Carpaccio de Tilápia (15 un)": {"preco": 35.00, "categoria": "À La Carte"},
    "Tataki de Salmão (250g)": {"preco": 36.00, "categoria": "À La Carte"},
    "Temaki de Salmão com Arroz (1 un)": {"preco": 26.00, "categoria": "Temakis"},
    "Box 16 Peças": {"preco": 48.00, "categoria": "Boxes"},
    "Box 26 Peças": {"preco": 78.00, "categoria": "Boxes"},
    "Coca-Cola (310ml)": {"preco": 6.50, "categoria": "Bebidas/Sobremesas"},
    "Heineken (330ml)": {"preco": 10.00, "categoria": "Bebidas/Sobremesas"}
}

# URL do Repositório de Dados em Nuvem Sincronizado (Uso Público e Gratuito)
# Usamos o prefixo do seu repositório para isolar as suas comandas das de outros utilizadores
BIN_URL = "https://kvdb.io/MN8N9Xm4V2Ww8vX7yZ5q2D/umai_sushi_comandas"

def puxar_dados_nuvem():
    try:
        resposta = requests.get(BIN_URL, timeout=5)
        if resposta.status_code == 200:
            return json.loads(resposta.text)
    except:
        pass
    return {}

def salvar_dados_nuvem(dados):
    try:
        requests.post(BIN_URL, data=json.dumps(dados), timeout=5)
    except:
        pass

# Carrega os dados sincronizados da nuvem
comandas_sincronizadas = puxar_dados_nuvem()

st.title("🍣 Umai Sushi — Premium PDV")

aba = st.tabs(["🛒 Lançar Item", "📊 Fechamento / Caixa"])

# ----------------------------------------------------
# ABA 1: LANÇAMENTO (Gravação Sincronizada Multi-Dispositivo)
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
    
    categorias = ["Todos"] + sorted(list(set(info["categoria"] for info in CARDAPIO_FIXO.values())))
    categoria_sel = st.selectbox("Filtrar por Categoria", categorias)
    
    if categoria_sel == "Todos":
        itens_filtrados = list(CARDAPIO_FIXO.keys())
    else:
        itens_filtrados = [p for p, info in CARDAPIO_FIXO.items() if info["categoria"] == categoria_sel]
        
    produto_sel = st.selectbox("Escolha o Produto", ["Selecione..."] + itens_filtrados)
    
    col_q, col_p = st.columns(2)
    with col_q:
        quantidade = st.number_input("Qtd", min_value=1, value=1, step=1)
    with col_p:
        preco_sugerido = CARDAPIO_FIXO[produto_sel]["preco"] if produto_sel != "Selecione..." else 0.00
        valor_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, value=preco_sugerido, format="%.2f")
        
    if st.button("➕ INCLUIR ITEM"):
        if garcom == "Selecione...":
            st.error("Selecione o Atendente antes de adicionar.")
        elif not mesa:
            st.error("Digite o número da Mesa ou Cartão.")
        elif produto_sel == "Selecione...":
            st.warning("Escolha um produto válido.")
        else:
            subtotal = quantidade * valor_unitario
            
            # Adiciona à estrutura existente vinda da nuvem
            if mesa not in comandas_sincronizadas:
                comandas_sincronizadas[mesa] = []
                
            comandas_sincronizadas[mesa].append({
                "garcom": garcom,
                "cliente": cliente,
                "item": produto_sel,
                "qtd": quantidade,
                "valor": valor_unitario,
                "subtotal": subtotal
            })
            
            # Envia imediatamente para a nuvem
            salvar_dados_nuvem(comandas_sincronizadas)
            st.toast(f"{produto_sel} enviado para a Mesa {mesa}!")

# ----------------------------------------------------
# ABA 2: CAIXA / MONITOR DE MESAS ATIVAS
# ----------------------------------------------------
with aba[1]:
    st.markdown("<h3 style='color: #d4af37;'>🧾 Resumo da Conta</h3>", unsafe_allowed_html=True)
    
    mesas_ativas = list(comandas_sincronizadas.keys())
    
    if not mesas_ativas:
        st.info("Nenhuma mesa aberta com consumo ativo no momento.")
    else:
        mesa_selecionada = st.selectbox("Selecione a Mesa para Fechamento", mesas_ativas)
        comanda_foco = comandas_sincronizadas[mesa_selecionada]
        
        if comanda_foco:
            info_base = comanda_foco[0]
            st.write(f"**Mesa:** {mesa_selecionada} | **Atendente:** {info_base['garcom']}")
            if info_base['cliente']: st.write(f"**Cliente:** {info_base['cliente']}")
            st.write("---")
            
            total_produtos = 0.0
            for i in comanda_foco:
                st.write(f"🔹 {i['qtd']}x — {i['item']} — R$ {i['valor']:.2f} | **R$ {i['subtotal']:.2f}**")
                total_produtos += i['subtotal']
                
            st.divider()
            taxa_porcentagem = 0.0 if "Não cobrar taxa" in info_base['garcom'] else 10.0
            valor_taxa = total_produtos * (taxa_porcentagem / 100.0)
            total_geral = total_produtos + valor_taxa
            
            st.write(f"Subtotal Itens: R$ {total_produtos:.2f}")
            st.write(f"Taxa ({taxa_porcentagem}%): R$ {valor_taxa:.2f}")
            st.markdown(f"<div class='total-box'>TOTAL GERAL: R$ {total_geral:.2f}</div>", unsafe_allowed_html=True)
            
            # HTML estruturado para Cupom Térmico de 80mm
            html_impressao = f"""
            <html><body onload="window.print();" style="font-family:'Courier New',monospace; width:72mm; font-size:12px; color:black;">
                <div style="text-align:center; font-weight:bold; font-size:14px;">UMAI SUSHI PREMIUM</div>
                <hr>
                <div>MESA: {mesa_selecionada}<br>ATENDENTE: {info_base['garcom']}<br>DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
                <hr>
            """
            for item in comanda_foco:
                html_impressao += f"<div>{item['qtd']}x {item['item']}<br>  R$ {item['subtotal']:.2f}</div>"
            html_impressao += f"""
                <hr>
                <div>SUBTOTAL: R$ {total_produtos:.2f}</div>
                <div>TAXA: R$ {valor_taxa:.2f}</div>
                <div style="font-weight:bold; font-size:13px;">TOTAL: R$ {total_geral:.2f}</div>
            </body></html>
            """
            st.download_button("🖨️ EMITIR CUPOM TÉRMICO", data=html_impressao, file_name=f"mesa_{mesa_selecionada}.html", mime="text/html")
            
            if st.button("❌ Finalizar e Zerar Mesa"):
                del comandas_sincronizadas[mesa_selecionada]
                salvar_dados_nuvem(comandas_sincronizadas)
                st.success(f"Mesa {mesa_selecionada} fechada!")
                st.rerun()
