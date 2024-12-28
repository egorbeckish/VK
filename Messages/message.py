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
	if (token:=get_token()).empty:
		st.warning(
			'Для того, чтобы начать рассылку, перейдите на страницу "Сохраненные TOKEN 🔗" и добавьте данные',
			icon='⚠️'
		)
	
	else:

		columns_selectbox = st.columns(3, vertical_alignment='center')
		with columns_selectbox[1]:
			select_token = st.selectbox(
				'TOKEN',
				token['fullname'].values,
				None,
				placeholder='Choose TOKEN...'
			)

		columns_send = st.columns([1, 1])
		with columns_send[0]:
			list_ids = st.text_area(
				"Список ID's",
				height=400,
				placeholder="Заполните ID's...",
				help='Можно использовать до 100 ID одновременно'
			)

		with columns_send[1]:
			message = st.text_area(
				'Отправляемое сообщение',
				height=400,
				placeholder='Введите сообщение...'
			)

		send_message = st.button('Отправить')

		if send_message:
			if not select_token:
				warning_token = st.warning('Для того, чтобы сделать рассылку, необходимо выбрать аккаунт', icon='⚠️')
				time.sleep(10)
				warning_token.empty()			

			elif not (list_ids and message):
				print(f'{list_ids=}\t{message=}')
				warning_send = st.warning("Одно из полей Список ID's/Отправляемое сообщение - пустое! Пожалуйста, заполните, данное(ые) поле(я)", icon='⚠️')
				time.sleep(10)
				warning_send.empty()
			
			else:
				with st.spinner('Происходит рассылка сообщений, пожалуйста, подождите...'):
					time.sleep(5)

				if len(list_ids:=list_ids.split()) > 100:
					st.warning()
				
				else:
					if len(list_ids) > 1:
						list_ids = ','.join(list_ids)
					
					else:
						list_ids = list_ids[0]
				
				__vk = VK(token.set_index('fullname').loc[select_token]['TOKEN'])
				__vk.send_message(
					user_ids=list_ids,
					message=message
				)

				success = st.success('Рассылка прошла успешно. Проверьте вкладку "Закрыть приложение 🔒"', icon='✅')
				time.sleep(10)
				success.empty()