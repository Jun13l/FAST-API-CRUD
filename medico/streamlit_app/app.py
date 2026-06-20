import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da URL da API
API_URL = os.getenv("API_URL", "https://fastapiprojeto.onrender.com")

st.set_page_config(page_title="CRUD Consultas", layout="centered")
st.title("🏥 Agendamento de  Consulta")

# --- Painel de Operações ---
st.subheader("✍️ Cadastro de Dados")


id_item = st.number_input("ID para Atualizar/Cancelar Agenda)", min_value=0, step=1, value=0)
paciente = st.text_input('Nome do Paciente')

lista_especialidades = ["Cardiologia", "Pediatria", "Dermatologia", "Clínica Médica"]

medicos_por_especialidade = {
    "Cardiologia": ["👩🏻‍⚕️ Dra. Ana (Cardio)", "🧑‍⚕️ Dr. Patrick (Cardio)", "🧑🏽‍⚕️ Dr. Roberto Melo (Cardio)"],
    "Pediatria": ["👩🏻‍⚕️ Dra. Vitoria (Pedi)", "🧑‍⚕️ Dr. Matheus Neves (Pedi)", "Dra. Marley Rodrigues (Pedi)"],
    "Dermatologia": ["👨🏾‍⚕️ Dr. Eder Carlos (Derma)", "🧑‍⚕️ Dr. Daniel Alves (Derma)", "🧑‍⚕️ Dr. Francisco Ribeiro (Derma)"],
    "Clínica Médica": ["👩🏽‍⚕️ Dra. Luzenir Sousa (Clínica)", "👩🏾‍⚕️ Dra. Isabelly Alves (Clínica)", "👨🏼‍⚕️ Dr. Manuel Silva (Clínica)"]
}

especialidade = st.selectbox("Selecione a Especialidade", options=lista_especialidades)


medicos_disponiveis = medicos_por_especialidade[especialidade]
medico = st.selectbox("Selecione o Médico", options=medicos_disponiveis)

data_consulta = st.date_input('DATA')
tipo_consulta = st.selectbox(
    'Tipo de Consulta',
    ['Primeira Consulta', 'Retorno', 'Exame', 'Avaliação']
)

# O formulário agora guarda apenas os botões de ação para evitar travamento de estado
with st.form("form_botoes"):
    col1, col2, col3 = st.columns(3)
    with col1:
        btn_criar = st.form_submit_button(" 🗓️ Agendar")
    with col2:
        btn_atualizar = st.form_submit_button(" 🔄 Atualizar Dados")
    with col3:
        btn_deletar = st.form_submit_button(" ✖️ Cancelar", type="primary")

 
payload = {
    "nome": paciente,
    "preco": 0.0,  
    "descricao": f"Médico: {medico} | Esp: {especialidade} | Tipo: {tipo_consulta} | Data: {data_consulta}"
}



if btn_criar:
    res = requests.post(f"{API_URL}/items/", json=payload)
    if res.status_code in [200, 201]:
        st.success("Consulta Agendada com sucesso!")
    else:
        st.error(f"Erro ao agendar consulta. Status: {res.status_code}")
        st.warning(f"Resposta detalhada da API: {res.text}")


if btn_atualizar and id_item > 0:
    res = requests.put(f"{API_URL}/items/{id_item}", json=payload)
    if res.status_code == 200:
        st.success(f"Consulta ID {id_item} atualizada com sucesso!")
    else:
        st.error(f"Não foi possível atualizar a consulta {id_item}. Detalhes: {res.text}")


if btn_deletar:
    if id_item > 0:
        res = requests.delete(f"{API_URL}/items/{id_item}")
        if res.status_code == 200:
            st.success(f"Consulta ID {id_item} Cancelada com sucesso!")
        else:
            st.error(f"Não foi possível cancelar a consulta {id_item}. Detalhes: {res.text}")
    else:
        st.warning("Por favor, insira um ID  válido (maior que 0) para poder cancelar.")


st.subheader(" 🗓️ Consultas Agendadas")
try:
   
    resposta_get = requests.get(f"{API_URL}/items/")
    if resposta_get.status_code == 200:
        lista_itens = resposta_get.json()
        if lista_itens:
            st.dataframe(lista_itens, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum item localizado no banco de dados.")
except Exception:
    st.error("A API de dados está inacessível no momento.")