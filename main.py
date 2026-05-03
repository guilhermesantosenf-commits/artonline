
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração da página e Verificação do Google
st.set_page_config(page_title="GE Engenharia | ART Online", page_icon="🏗️")

if "google" in st.secrets:
    st.markdown(f'<meta name="google-site-verification" content="{st.secrets["google"]["verification"]}" />', unsafe_allow_html=True)

def enviar_email(dados):
    try:
        # Puxa a senha configurada nos Secrets do Streamlit
        senha_gmail = st.secrets["gmail"]["password"]
        email_destino = "geengenharia.americana@gmail.com" # Verifique se seu e-mail é este mesmo

        msg = MIMEMultipart()
        msg['From'] = email_destino
        msg['To'] = email_destino
        msg['Subject'] = f"Novo Pedido de ART - {dados['nome']}"

        corpo = f"""
        Novo pedido de ART recebido:
        
        Nome: {dados['nome']}
        CPF/CNPJ: {dados['documento']}
        Telefone: {dados['telefone']}
        Endereço da Obra: {dados['endereco']}
        Tipo de Serviço: {dados['servico']}
        Valor do PIX: R$ {dados['valor']}
        """
        msg.attach(MIMEText(corpo, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_destino, senha_gmail)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
        return False

# Interface do Site
st.title("🏗️ GE Engenharia - Solicitação de ART")
st.write("Preencha os dados abaixo para gerar sua ART.")

with st.form("form_art"):
    nome = st.text_input("Nome Completo / Razão Social")
    documento = st.text_input("CPF ou CNPJ")
    telefone = st.text_input("WhatsApp para contato")
    endereco = st.text_area("Endereço completo da obra")
    servico = st.selectbox("Tipo de Serviço", ["Residencial", "Comercial", "Reforma", "Outros"])
    
    st.divider()
    st.subheader("💰 Pagamento via PIX")
    st.write("**Chave PIX (CNPJ): 12.345.678/0001-90**") # COLOQUE SEU CNPJ OU CHAVE AQUI
    st.info("Valor da Taxa: R$ 150,00") # AJUSTE O VALOR SE NECESSÁRIO
    
    confirmou_pix = st.checkbox("Confirmo que realizei o pagamento via PIX")
    
    enviado = st.form_submit_button("Enviar Solicitação")

if enviado:
    if not confirmou_pix:
        st.warning("Por favor, confirme o pagamento via PIX para continuar.")
    elif nome and documento:
        dados = {
            "nome": nome,
            "documento": documento,
            "telefone": telefone,
            "endereco": endereco,
            "servico": servico,
            "valor": "150,00"
        }
        if enviar_email(dados):
            st.success("✅ Solicitação enviada com sucesso! Em breve entraremos em contato.")
        else:
            st.error("❌ Houve um problema ao processar seu pedido. Tente novamente.")
    else:
        st.error("Preencha os campos obrigatórios (Nome e Documento).")
