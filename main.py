import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURAÇÃO DE E-MAIL (GE Engenharia) ---
def enviar_email_ge(dados, assunto, destinatario_final, arquivo=None, eh_cliente=False):
    meu_email = "guilhermesantosenf@gmail.com"
    minha_senha = st.secrets["gmail"]["password"] # Pega a senha dos Secrets por segurança
    
    msg = MIMEMultipart()
    msg['From'] = f"GE Engenharia <{meu_email}>"
    msg['To'] = destinatario_final
    msg['Subject'] = assunto
    
    if eh_cliente:
        corpo = f"Olá {dados.get('nome', 'Cliente')},\n\nRecebemos sua solicitação! Nossa equipe técnica já iniciou o processamento."
    else:
        corpo = "Nova solicitação via sistema GE Engenharia:\n\n"
        for chave, valor in dados.items():
            corpo += f"{chave.capitalize()}: {valor}\n"
    
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(meu_email, minha_senha)
        server.send_message(msg)
        server.quit()
        return True
    except: return False

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GE Engenharia | Oficial", page_icon="🏗️", layout="wide")

if 'db_pedidos' not in st.session_state:
    st.session_state['db_pedidos'] = {}
if 'admin_logado' not in st.session_state:
    st.session_state['admin_logado'] = False

# --- CSS CUSTOMIZADO ---
st.markdown("""
    <style>
    header, [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; height: 0px !important; }
    [data-testid="stSidebar"] { background-color: #000000; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stButton>button { width: 100%; border-radius: 0px; font-weight: bold; background-color: #000000 !important; color: #ffffff !important; border: 1px solid #ffffff; text-transform: uppercase; letter-spacing: 2px; }
    .wpp-btn { background-color: #25d366; color: white !important; padding: 10px; text-align: center; border-radius: 5px; text-decoration: none; display: block; font-weight: bold; margin-top: 5px; }
    .pix-box { background-color: #ffffff; padding: 30px; border: 3px solid #000000; text-align: center; }
    .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; border-top: 1px solid #eee; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("GE ENGENHARIA")
    aba = st.radio("NAVEGAÇÃO", ["🏠 Solicitar ART (Até 1h)", "📋 Orçamento de Obra", "🔍 Status do Pedido", "📂 Documentos & Exigências", "👥 Quem Somos", "🔐 Área do Engenheiro"])
    st.markdown("---")
    st.write("🕒 **HORÁRIO:** 08:00 às 17:00")
    st.markdown("### WHATSAPP")
    st.markdown('<a href="https://wa.me/5519982604724" class="wpp-btn">👤 GUILHERME</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://wa.me/5519982474746" class="wpp-btn">👤 EDNALDO</a>', unsafe_allow_html=True)

# --- CONTEÚDO ---
if aba == "👥 Quem Somos":
    st.title("QUEM SOMOS")
    st.markdown("### GE Engenharia e Construção")
    st.write("Foco em desburocratização em Americana e região.")

elif aba == "🏠 Solicitar ART (Até 1h)":
    st.title("EMISSÃO DE ART")
    with st.form("art"):
        n = st.text_input("Nome")
        c = st.text_input("CPF")
        if st.form_submit_button("AVANÇAR"):
            st.session_state['db_pedidos'][c] = {"nome": n, "status": "Aguardando Pagamento"}
            st.info("Chave PIX: guilhermesantosenf@gmail.com")

elif aba == "🔐 Área do Engenheiro":
    st.title("ADMINISTRAÇÃO")
    senha = st.text_input("Senha", type="password")
    if senha == "ge2026":
        st.write("Pedidos Ativos:", st.session_state['db_pedidos'])

st.markdown('<div class="footer"><b>GE ENGENHARIA</b> | Americana - SP</div>', unsafe_allow_html=True)
