# --- ABA: SOLICITAR ART ---
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
                else: st.error("Preencha os campos obrigatórios.")
    else:
        # --- NOVO BLOCO DE PAGAMENTO COM COPIA E COLA ---
        st.markdown("""
            <div style="background-color: #ffffff; padding: 25px; border: 3px solid #000000; text-align: center; border-radius: 10px;">
                <h3 style="color: #000000; margin-bottom: 5px;">PAGAMENTO VIA PIX</h3>
                <p style="color: #333; font-weight: bold; font-size: 18px; margin-bottom: 10px;">Chave (E-mail): guilhermesantosenf@gmail.com</p>
                <div style="font-size: 50px; color: #000000; font-weight: 800; margin-bottom: 20px;">R$ 500,00</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Campo de Copia e Cola prático
        st.text_input("Clique abaixo para copiar a chave PIX:", value="guilhermesantosenf@gmail.com", help="Selecione e copie para o seu banco")
        
        st.markdown("---")
        comp = st.file_uploader("Anexe o Comprovante", type=['png', 'jpg', 'pdf'])
        
        if comp and st.button("CONFIRMAR ENVIO"):
            st.session_state['db_pedidos'][st.session_state['dados_temp']['cpf']] = {
                "nome": st.session_state['dados_temp']['nome'], 
                "status": "Pagamento em análise", 
                "condo": st.session_state['dados_temp']['condo']
            }
            enviar_email_ge(st.session_state['dados_temp'], f"✅ ART PAGA - {st.session_state['dados_temp']['nome']}", "guilhermesantosenf@gmail.com", comp)
            st.success("✅ Comprovante enviado! Nossa equipe analisará o pagamento em instantes.")
            st.session_state['dados_temp'] = None
