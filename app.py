import streamlit as stfrom datetime import datetime
st.set_page_config(page_title="Comandas Restaurante")
st.title(" Sistema de Comandas")
mesa = st.text_input("Mesa")cliente = st.text_input("Cliente")item = st.text_input("Item")
quantidade = st.number_input("Quantidade", min_value=1, value=1)
valor = st.number_input(    "Valor Unitário (R$)",    min_value=0.0,    format="%.2f")
taxa = st.number_input(    "Taxa de Serviço (%)",    min_value=0,    max_value=20,    value=10)
subtotal = quantidade * valorservico = subtotal * (taxa / 100)total = subtotal + servico
st.divider()
st.subheader("Resumo")
st.write(f"Mesa: {mesa}")st.write(f"Cliente: {cliente}")st.write(f"Item: {item}")st.write(f"Quantidade: {quantidade}")st.write(f"Subtotal: R$ {subtotal:.2f}")st.write(f"Serviço: R$ {servico:.2f}")
st.success(f"Total: R$ {total:.2f}")
if st.button(" Imprimir Comanda"):
    html = f'''    <html>    <body>        <h2>COMANDA</h2>        <p>Mesa: {mesa}</p>        <p>Cliente: {cliente}</p>        <p>Item: {item}</p>        <p>Quantidade: {quantidade}</p>        <p>Total: R$ {total:.2f}</p>        <p>{datetime.now()}</p>
        <script>            window.print();        </script>    </body>    </html>    '''
    st.download_button(        "Baixar Comanda",        html,        file_name="comanda.html",        mime="text/html"    )
