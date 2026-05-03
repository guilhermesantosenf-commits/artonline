import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
st.markdown('<meta name="google-site-verification" content="tZwifqB2_EGFetR2B8hrUvGWrvexjWUNNPv8DfuPGRk" />', unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE E-MAIL (GE Engenharia) ---
def enviar_email_ge(dados, assunto, destinatario_final, arquivo=None, eh_cliente=False):
    meu_email = "guilhermesantosenf@gmail.com"
    minha_senha = "lxxv ujrj jlae rpyr" 
    
    msg = MIMEMultipart()
    msg['From'] = f"GE Engenharia <{meu_email}>"
    msg['To'] = destinatario_final
    msg['Subject'] = assunto
    
    if eh_cliente:
        corpo = f"Olá {dados.get('nome', 'Cliente')},\n\nRecebemos sua solicitação na GE Engenharia e Construção! Nossa equipe técnica já iniciou o processamento."
    else:
        corpo = "Nova solicitação via sistema GE Engenharia:\n\n"
        for chave, valor in dados.items():
            corpo += f"{chave.capitalize()}: {valor}\n"
    
    msg.attach(MIMEText(corpo, 'plain'))
    if arquivo:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(arquivo.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={arquivo.name}")
        msg.attach(part)
    
    try:
        server = stplib.SMTP('smtp.gmail.com', 587)
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
    .valor-total { font-size: 50px; color: #000000; font-weight: 800; }
    .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; border-top: 1px solid #eee; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    if os.path.exists("logo_ge.png"): st.image("logo_ge.png", use_container_width=True)
    else: st.title("GE ENGENHARIA")
    
    aba = st.radio("NAVEGAÇÃO", [
        "🏠 Solicitar ART (Até 1h)", 
        "📋 Orçamento de Obra", 
        "🔍 Status do Pedido",
        "📂 Documentos & Exigências",
        "👥 Quem Somos",
        "🔐 Área do Engenheiro"
    ])
    st.markdown("---")
    st.write("🕒 **HORÁRIO:** 08:00 às 17:00")
    
    # AJUSTE: INFORMAÇÃO DE APENAS MENSAGENS
    st.markdown("### WHATSAPP (Apenas Mensagens)")
    st.markdown('<a href="https://wa.me/5519982604724" class="wpp-btn">👤 GUILHERME</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://wa.me/5519982474746" class="wpp-btn">👤 EDNALDO</a>', unsafe_allow_html=True)
    st.caption("⚠️ Não recebemos ligações. Atendimento exclusivo por texto.")

# --- ABA: QUEM SOMOS (MANTIDA COMPLETA) ---
if aba == "👥 Quem Somos":
    st.title("QUEM SOMOS")
    st.markdown("""
    ### GE Engenharia e Construção
    Fundada com o propósito de elevar o padrão de segurança e conformidade técnica no setor da construção civil, a **GE Engenharia e Construção** é referência em desburocratização e agilidade técnica.
    
    Sediada em **Americana** e com atuação estratégica em todo o **Estado de São Paulo**, entregamos soluções completas que vão desde a regularização documental através de ARTs até o gerenciamento integral de obras residenciais e comerciais.
    
    #### Nosso Diferencial Profissional:
    *   **Expertise Técnica:** Nossa equipe aplica rigorosos critérios de engenharia para garantir a integridade estrutural e a valorização do seu patrimônio.
    *   **Agilidade Digital:** Entendemos a urgência do mercado atual. Por isso, operamos com processos otimizados para que você receba sua documentação no menor prazo possível.
    *   **Transparência e Ética:** Atuamos com clareza em todas as etapas, garantindo que sua obra esteja 100% legalizada perante os órgãos competentes e condomínios.
    
    #### Condomínios Atendidos na Região:
    *   ✅ Residencial Garnet
    *   ✅ Condomínio Tripoli
    *   ✅ Portal dos Nobres
    *   *E mais de 50 condomínios parceiros em Americana e Campinas.*
    """)
    st.divider()
    st.write("📍 Sede: Americana - São Paulo | 🌐 Atendimento em todo o Estado.")

# --- ABA: SOLICITAR ART (MANTIDA COMPLETA) ---
elif aba == "🏠 Solicitar ART (Até 1h)":
    st.title("EMISSÃO DE ART EM ATÉ 1H")
    if 'dados_temp' not in st.session_state or st.session_state['dados_temp'] is None:
        st.info("Taxa fixa de emissão: **R$ 500,00**")
        with st.form("art_completa"):
            c1, c2 = st.columns(2)
            with c1:
                n = st.text_input("Nome Completo")
                cpf = st.text_input("CPF (Apenas números)")
                w = st.text_input("WhatsApp com DDD")
            with c2:
                e = st.text_input("E-mail")
                condo = st.text_input("Condomínio")
                unid = st.text_input("Unidade / Bloco")
            tipo = st.selectbox("Tipo de Obra", ["Reforma Geral", "Elétrica", "Estrutura", "Gás/Ar", "Piso/Revestimento"])
            obs = st.text_area("Descrição da reforma")
            if st.form_submit_button("AVANÇAR PARA PAGAMENTO"):
                if n and cpf and w and condo:
                    st.session_state['dados_temp'] = {"nome": n, "cpf": cpf, "whatsapp": w, "email": e, "condo": condo, "unidade": unid, "tipo": tipo, "obs": obs}
                    st.rerun()
                else: st.error("Campos obrigatórios: Nome, CPF, WhatsApp e Condomínio.")
    else:
        st.markdown(f'<div class="pix-box"><p>PIX (E-MAIL): <b>guilhermesantosenf@gmail.com</b></p><div class="valor-total">R$ 500,00</div></div>', unsafe_allow_html=True)
        comp = st.file_uploader("Anexe o Comprovante", type=['png', 'jpg', 'pdf'])
        if comp and st.button("CONFIRMAR ENVIO"):
            st.session_state['db_pedidos'][st.session_state['dados_temp']['cpf']] = {"nome": st.session_state['dados_temp']['nome'], "status": "Pagamento em análise", "condo": st.session_state['dados_temp']['condo']}
            enviar_email_ge(st.session_state['dados_temp'], f"✅ ART PAGA - {st.session_state['dados_temp']['nome']}", "guilhermesantosenf@gmail.com", comp)
            st.success("Enviado com sucesso!")
            st.session_state['dados_temp'] = None

# --- ABA: ORÇAMENTO TÉCNICO (MANTIDA COMPLETA) ---
elif aba == "📋 Orçamento de Obra":
    st.title("SOLICITAR ORÇAMENTO TÉCNICO")
    with st.form("orc_completo"):
        col1, col2 = st.columns(2)
        with col1:
            nome_o = st.text_input("Nome Completo / Empresa")
            zap_o = st.text_input("WhatsApp com DDD")
            mail_o = st.text_input("E-mail")
            loc_o = st.text_input("Cidade da Obra")
        with col2:
            serv_o = st.selectbox("Serviço", ["Construção do Zero", "Reforma Estrutural", "Gerenciamento", "Outros"])
            metragem_o = st.text_input("Metragem (m²)")
            prazo_o = st.selectbox("Prazo", ["Imediato", "3 a 6 meses", "Longo Prazo"])
        planta_o = st.file_uploader("Carregar Planta ou Referência", type=['pdf', 'png', 'jpg'])
        detalhes_o = st.text_area("Descrição detalhada do projeto:")
        if st.form_submit_button("SOLICITAR ANÁLISE"):
            if nome_o and zap_o:
                enviar_email_ge({"nome": nome_o, "detalhes": detalhes_o, "zap": zap_o}, f"📋 ORÇAMENTO - {nome_o}", "guilhermesantosenf@gmail.com", planta_o)
                st.success("Projeto enviado com sucesso!")

# --- ABA: DOCUMENTOS & EXIGÊNCIAS ---
elif aba == "📂 Documentos & Exigências":
    st.title("CENTRAL DE INFORMAÇÕES TÉCNICAS")
    st.markdown("#### Checklist NBR 16.280 para sua Reforma:\n1. ART Assinada\n2. Plano de Reforma\n3. Cronograma\n4. Lista de Prestadores")

# --- ABA: ÁREA DO ENGENHEIRO ---
elif aba == "🔐 Área do Engenheiro":
    st.title("PAINEL ADMINISTRATIVO")
    if not st.session_state['admin_logado']:
        senha_in = st.text_input("Senha Mestra", type="password")
        if st.button("LOGAR"):
            if senha_in == "ge2026":
                st.session_state['admin_logado'] = True
                st.rerun()
            else: st.error("Senha incorreta.")
    else:
        if st.sidebar.button("LOGOUT"):
            st.session_state['admin_logado'] = False
            st.rerun()
        for cpf, info in st.session_state['db_pedidos'].items():
            with st.expander(f"Cliente: {info['nome']} | Status: {info['status']}"):
                novo = st.selectbox("Mudar Status", ["Pagamento em análise", "✅ Confirmado", "🏗️ Em Geração", "📩 Enviada"], key=f"adm_{cpf}")
                if st.button("Salvar Status", key=f"sav_{cpf}"):
                    st.session_state['db_pedidos'][cpf]['status'] = novo
                    st.rerun()

# --- ABA: STATUS ---
elif aba == "🔍 Status do Pedido":
    st.title("CONSULTAR STATUS DA ART")
    busca = st.text_input("Insira seu CPF cadastrado")
    if st.button("Consultar"):
        if busca in st.session_state['db_pedidos']:
            st.success(f"Olá {st.session_state['db_pedidos'][busca]['nome']}! Status: **{st.session_state['db_pedidos'][busca]['status']}**")
        else: st.error("CPF não localizado.")

st.markdown('<div class="footer"><b>GE ENGENHARIA E CONSTRUÇÃO</b> | Americana - SP.</div>', unsafe_allow_html=True)
