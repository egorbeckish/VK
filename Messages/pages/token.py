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
	table_token = st.data_editor(
		get_token(),
		column_config={
			'TOKEN': st.column_config.TextColumn(
				'Токен аккаунта',
				width=150,
			),
			'fullname': st.column_config.TextColumn(
				'Имя аккаунта'
			),
			'ID': st.column_config.NumberColumn(
				'ID аккаунта',
				format='%d'
			),
		},
		num_rows='dynamic',
		disabled=['fullname', 'ID'],
		width=1000,
		height=300,
	)

	columns_button = st.columns([1, 1])
	with columns_button[0]:
		save_token = st.button('Сохранить')
	with columns_button[1]:
		link_token = st.link_button('Получение ТОКЕН аккаунта', 'https://vkhost.github.io/')
	
	if save_token:
		with st.spinner('Сохранение данных, пожалуйста, подождите...'):
			time.sleep(5)
		
		table_token = table_token.set_index('TOKEN')
		for token in table_token.index:
			info = table_token.loc[token]
			__vk = VK(token)
			info['fullname'] = __vk.self_fullname
			info['ID'] = __vk.self_id
			table_token.loc[token] = info
		
		table_token.to_csv('token.csv')

		success = st.success('Успешное изменение данных', icon='✅')
		time.sleep(5)
		success.empty()

		st.rerun()