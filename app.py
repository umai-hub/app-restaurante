import streamlit as st
from datetime import datetime
import sqlite3

# Configuração de Página
st.set_page_config(page_title="Umai Sushi PDV", layout="centered")

# Injeção de CSS para o Visual Preto e Dourado Estilo G6
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d !important; color: #e5e5e5 !important; }
    .total-box {
        background-color: #1a1a1a; color: #d4af37; padding: 20px;
        border-radius: 8px; border: 2px solid #d4af37;
        text-align: center; font-size: 24px; font-weight: bold; margin: 15px 0;
    }
    div.stButton > button:first-child {
        background-color: #d4af37 !important; color: #0d0d0d !important;
        font-weight: bold !important; border: none !important; width: 100% !important;
    }
    </style>
""", unsafe_allowed_html=True)

# Inicialização e Criação das Tabelas do Banco de Dados Compartilhado
def iniciar_banco():
    conn = sqlite3.connect("umai_sistema.db", check_same_thread=False)
    cursor = conn.cursor()
    # Tabela de Comandas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comandas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            garcom TEXT,
            mesa TEXT,
            cliente TEXT,
            item TEXT,
            qtd INTEGER,
            valor REAL,
            subtotal REAL,
            data TEXT
        )
    """)
    # Tabela de Cardápio para persistência
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cardapio (
            produto TEXT PRIMARY KEY,
            preco REAL,
            categoria TEXT
        )
    """)
    
    # Inserção inicial do cardápio padrão caso esteja vazio
    cursor.execute("SELECT COUNT(*) FROM cardapio")
    if cursor.fetchone()[0] == 0:
        itens_padrao = [
            ("Carpaccio de Salmão (15 un)", 39.00, "À La Carte"),
            ("Carpaccio de Tilápia (15 un)", 35.00, "À La Carte"),
            ("Tataki de Salmão (250g)", 36.00, "À La Carte"),
            ("Temaki de Salmão com Arroz (1 un)", 26.00, "Temakis"),
            ("Box 16 Peças", 48.00, "Boxes"),
            ("Box 26 Peças", 78.00, "Boxes"),
            ("Coca-Cola (310ml)", 6.50, "Bebidas/Sobremesas"),
            ("Heineken (330ml)", 10.00, "Bebidas/Sobremesas")
        ]
        cursor.executemany("INSERT INTO cardapio VALUES (?, ?, ?)", itens_padrao)
    conn.commit()
    return conn

conn = iniciar_banco()
cursor = conn.cursor()

st.title("🍣 Umai Sushi — PDV Sincronizado")

aba = st.tabs(["🛒 Lançar Item", "📊 Fechamento / Caixa", "⚙️ Cadastrar Produtos"])

# ----------------------------------------------------
# ABA 1: LANÇAMENTO (Qualquer celular grava no arquivo comum)
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
    
    # Puxa categorias reais do banco
    cursor.execute("SELECT DISTINCT categoria FROM cardapio")
    categorias = ["Todos"] + [row[0] for row in cursor.fetchall()]
    categoria_sel = st.selectbox("Filtrar por Categoria", categorias)
    
    if categoria_sel == "Todos":
        cursor.execute("SELECT produto FROM cardapio")
    else:
        cursor.execute("SELECT produto FROM cardapio WHERE categoria = ?", (categoria_sel,))
    itens_filtrados = [row[0] for row in cursor.fetchall()]
        
    produto_sel = st.selectbox("Escolha o Produto", ["Selecione..."] + itens_filtrados)
    
    col_q, col_p = st.columns(2)
    with col_q:
        quantidade = st.number_input("Qtd", min_value=1, value=1, step=1)
    with col_p:
        preco_sugerido = 0.00
        if produto_sel != "Selecione...":
            cursor.execute("SELECT preco FROM cardapio WHERE produto = ?", (produto_sel,))
            res = cursor.fetchone()
            if res: preco_sugerido = res[0]
        valor_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, value=preco_sugerido, format="%.2f")
        
    if st.button("➕ INCLUIR ITEM"):
        if garcom == "Selecione...":
            st.error("Selecione o Atendente antes de adicionar.")
        elif not mesa:
            st.error("Informe o número da Mesa.")
        elif produto_sel == "Selecione...":
            st.warning("Escolha um produto válido.")
        else:
            subtotal = quantidade * valor_unitario
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO comandas (garcom, mesa, cliente, item, qtd, valor, subtotal, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (garcom, mesa, cliente, produto_sel, quantidade, valor_unitario, subtotal, agora)
            )
            conn.commit()
            st.toast(f"{produto_sel} adicionado com sucesso para a Mesa {mesa}!")

# ----------------------------------------------------
# ABA 2: CAIXA / IMPRESSÃO (Puxa todas as mesas ativas do banco)
# ----------------------------------------------------
with aba[1]:
    st.markdown("<h3 style='color: #d4af37;'>🧾 Resumo da Conta</h3>", unsafe_allowed_html=True)
    
    # Lista mesas com consumo pendente
    cursor.execute("SELECT DISTINCT mesa FROM comandas")
    mesas_ativas = [row[0] for row in cursor.fetchall()]
    
    if not mesas_ativas:
        st.info("Nenhuma mesa com consumo ativo no momento.")
    else:
        mesa_sel = st.selectbox("Selecione a Mesa para Visualizar/Fechar", mesas_ativas)
        
        cursor.execute("SELECT garcom, cliente, item, qtd, valor, subtotal FROM comandas WHERE mesa = ?", (mesa_sel,))
        pedidos_mesa = cursor.fetchall()
        
        info_garcom = pedidos_mesa[0][0]
        info_cliente = pedidos_mesa[0][1]
        
        st.write(f"**Mesa:** {mesa_sel} | **Atendente:** {info_garcom}")
        if info_cliente: st.write(f"**Cliente:** {info_cliente}")
        st.write("---")
        
        total_produtos = 0.0
        for p in pedidos_mesa:
            st.write(f"🔹 {p[3]}x — {p[2]} — R$ {p[4]:.2f} | **R$ {p[5]:.2f}**")
            total_produtos += p[5]
            
        st.divider()
        taxa_porcentagem = 0.0 if "Não cobrar taxa" in info_garcom else 10.0
        valor_taxa = total_produtos * (taxa_porcentagem / 100.0)
        total_geral = total_produtos + valor_taxa
        
        st.write(f"Subtotal: R$ {total_produtos:.2f}")
        st.write(f"Taxa ({taxa_porcentagem}%): R$ {valor_taxa:.2f}")
        st.markdown(f"<div class='total-box'>TOTAL GERAL: R$ {total_geral:.2f}</div>", unsafe_allowed_html=True)
        
        # HTML estruturado para Cupom Térmico de 80mm
        html_impressao = f"""
        <html><body onload="window.print();" style="font-family:'Courier New',monospace; width:72mm; font-size:12px; color:black;">
            <div style="text-align:center; font-weight:bold; font-size:14px;">UMAI SUSHI PREMIUM</div>
            <hr>
            <div>MESA: {mesa_sel}<br>ATENDENTE: {info_garcom}<br>DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
            <hr>
        """
        for p in pedidos_mesa:
            html_impressao += f"<div>{p[3]}x {p[2]}<br>  R$ {p[5]:.2f}</div>"
        html_impressao += f"""
            <hr>
            <div>SUBTOTAL: R$ {total_produtos:.2f}</div>
            <div>TAXA: R$ {valor_taxa:.2f}</div>
            <div style="font-weight:bold; font-size:13px;">TOTAL: R$ {total_geral:.2f}</div>
        </body></html>
        """
        st.download_button("🖨️ IMPRIMIR CONTA", data=html_impressao, file_name=f"comanda_mesa_{mesa_sel}.html", mime="text/html")
        
        if st.button("❌ Finalizar Recebimento (Zerar Mesa)"):
            cursor.execute("DELETE FROM comandas WHERE mesa = ?", (mesa_sel,))
            conn.commit()
            st.success(f"Mesa {mesa_sel} encerrada com sucesso!")
            st.timer_refresh = 1
            st.rerun()

# ----------------------------------------------------
# ABA 3: CADASTRO E EDIÇÃO DE PRODUTOS DIRETO NO APP
# ----------------------------------------------------
with aba[2]:
    st.markdown("<h3 style='color: #d4af37;'>⚙️ Painel do Cardápio</h3>", unsafe_allowed_html=True)
    novo_nome = st.text_input("Nome do Produto")
    nova_cat = st.selectbox("Categoria", ["À La Carte", "Temakis", "Boxes", "Bebidas/Sobremesas", "Outros"])
    novo_preco = st.number_input("Preço", min_value=0.0, value=0.0, format="%.2f")
    
    if st.button("💾 SALVAR PRODUTO"):
        if novo_nome:
            cursor.execute("INSERT OR REPLACE INTO cardapio (produto, preco, categoria) VALUES (?, ?, ?)", (novo_nome, novo_preco, nova_cat))
            conn.commit()
            st.success(f"'{novo_nome}' salvo com sucesso no banco sincronizado!")
            st.rerun()
            
    st.write("---")
    st.write("### Itens Ativos no Cardápio:")
    cursor.execute("SELECT produto, preco, categoria FROM cardapio ORDER BY categoria")
    for row in cursor.fetchall():
        st.write(f"🔸 **{row[0]}** | R$ {row[1]:.2f} ({row[2]})")
