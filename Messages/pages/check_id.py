from vk_class import *

st.set_page_config(
	page_title='Рассылка',
	page_icon='✉️',
	layout='wide'
)

columns_menu = st.columns([1, 4])

with columns_menu[0]:
	st.page_link('message.py', label='Рассылка 📨')
	st.page_link(r'pages/check_id.py', label='Непрошедшие ID 😶‍🌫️')
	st.page_link(r'pages/token.py', label='Сохраненные TOKEN 🔗')
	st.page_link(r'pages/close.py', label='Закрыть приложение 🔒')

with columns_menu[1]:
	table_error_id = st.data_editor(
		get_error_id(),
		column_config={
			'ID': st.column_config.NumberColumn(
				'ID аккаунта, которому отправили',
				format='%d',
			),
			'CODE': st.column_config.NumberColumn(
				'Код ошибки',
				format='%d',
			),
			'ERROR': st.column_config.TextColumn(
				'Причина неотправки',
			),
		},
		disabled=True,
		width=1000,
	)

	delete_id = st.button('Очистить ID')
	if delete_id:
		with st.spinner('Сохранение данных, пожалуйста, подождите...'):
			time.sleep(5)
		
		clear_error_id()

		success = st.success('Успешное изменение данных', icon='✅')
		time.sleep(5)
		success.empty()

		st.rerun()