import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit.components.v1 as components

# 1. MANTIVE A CONFIGURAÇÃO QUE VOCÊ TINHA
st.set_page_config(page_title="GE Engenharia | ART Online", page_icon="🏗️")

# 2. MANTIVE O CÓDIGO DE VERIFICAÇÃO DO GOOGLE (Igual à imagem dfc8de)
if "google" in st.secrets:
    st.markdown(f'<meta name="google-site-verification" content="{st.secrets["google"]["verification"]}" />', unsafe_allow_html=True)

# 3. FUNÇÃO DE E-MAIL (Ajustada para usar sua senha dos Secrets)
def enviar_email(dados):
    try:
        senha_gmail = st.secrets["gmail"]["password"]
        email_destino = "geengenharia.americana@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = email_destino
        msg['To'] = email_destino
        msg['Subject'] = f"Novo Pedido de ART - {dados['nome']}"

        corpo = f"Nome: {dados['nome']}\nDocumento: {dados['documento']}\nTelefone: {dados['telefone']}\nEndereço: {dados['endereco']}\nServiço: {dados['servico']}"
        msg.attach(MIMEText(corpo, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_destino, senha_gmail)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False

# 4. INTERFACE DO SITE
st.title("🏗️ GE Engenharia - Solicitação de ART")

with st.form("form_art"):
    nome = st.text_input("Nome Completo")
    documento = st.text_input("CPF ou CNPJ")
    telefone = st.text_input("WhatsApp")
    endereco = st.text_area("Endereço da obra")
    servico = st.selectbox("Serviço", ["Residencial", "Comercial", "Reforma"])
    
    # --- CAMPO DO PIX QUE VOCÊ PEDIU ---
    st.divider()
    st.subheader("💰 Pagamento")
    st.write("Chave PIX (CNPJ): **COLOQUE_SEU_CNPJ_AQUI**")
    confirmou_pix = st.checkbox("Já realizei o pagamento via PIX")
    # -----------------------------------
    
    enviado = st.form_submit_button("Enviar")

if enviado:
    if confirmou_pix and nome:
        dados = {"nome": nome, "documento": documento, "telefone": telefone, "endereco": endereco, "servico": servico}
        if enviar_email(dados):
            st.success("Enviado com sucesso!")
        else:
            st.error("Erro no envio. Verifique a senha nos Secrets.")
    else:
        st.warning("Preencha o nome e confirme o PIX.")
