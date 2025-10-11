from library import *


def switch_url(driver: WebDriver, url: str, wait: int | float=None):
	driver.get(url)
	if wait:
		time.sleep(wait)


def get_content(driver: WebDriver, by: By, value: str):
	while not driver.find_elements(by, value):
		...

	return driver.find_elements(by, value)


def send_data(element: WebElement, value: str):
	element.send_keys(value)


def click_element(element: WebElement, wait: int | float=None):
	element.click()
	if wait:
		time.sleep(wait)


def switch_tab(driver: WebDriver, tab: int):
	driver.switch_to.window(driver.window_handles[tab])


def get_tabs(driver: WebDriver):
	return driver.window_handles


def close_tab(driver: WebDriver):
	driver.close()


def exist_xlsx():
	# return False
	return "money.xlsx" in os.listdir()


def writer_data(data: dict):
	for k, v in data.items():
		with pd.ExcelWriter("money.xlsx", "openpyxl", mode="a", if_sheet_exists="overlay") as writer:
			v.to_excel(writer, index=False, sheet_name=k)


def writer_total_data():
	total = {
		"Count free dialogs": [],
		"Money for free dialogs": [],
		"Count dialogs": [],
		"Money for dialogs": [],
		"Count calls": [],
		"Money for calls": [],
		"Count tasks": [],
		"Money for tasks": [],
		"Intermediate": [],
		"Total": []
	}
	total_keys = list(total.keys())

	with pd.ExcelFile("money.xlsx", engine="openpyxl") as df:
		sheet_names = df.sheet_names
		months = sheet_names[:-1] if "Total" in sheet_names else sheet_names

		for i, month in enumerate(months):
			df_month = df.parse(month)
			total["Count tasks"] += [df_month["Count tasks"].sum()]
			total["Money for tasks"] += [df_month["Money for tasks"].sum()]

			for k in total_keys[:-4]:
				total[k] += [0]
			
			intermediate = 0
			for k in total_keys[1:-2:2]:
				intermediate += total[k][i]

			total["Intermediate"] += [intermediate]
			total["Total"] += [intermediate * .87]
	
	with pd.ExcelWriter("money.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
		pd.DataFrame(
			data=total.values(),
			columns=months,
			index=total.keys()
		).to_excel(writer, sheet_name="Total")


def create_xlsx():
	if not exist_xlsx():
		wb = openpyxl.Workbook()
		wb.save("money.xlsx")


def delete_sheet():
	wb = openpyxl.load_workbook("money.xlsx")
	if "Sheet" in wb.sheetnames:
		wb.remove(wb["Sheet"])
	wb.save("money.xlsx")


def upload_data(data: dict):
	with pd.ExcelFile("money.xlsx", engine="openpyxl") as df:
		months = df.sheet_names[:-1]
		months_dict = {}
		for month in months:
			df_month = df.parse(month)
			df_month["Date"] = df_month["Date"].apply(lambda x: x.date())
			months_dict[month] = df_month

			if month not in data:
				data[month] = df_month

			else:
				data[month] = pd.concat([data[month], df_month])


def save_data(df):
	if isinstance(df, list):
		df = pd.DataFrame(
			df,
			columns=["Link", "Date", "Time", "Month", "Count tasks", "Money for tasks"],
		)

	months = df["Month"].unique()[::-1]
	months_dict = {}
	for month in months:
		df_month = df[df["Month"] == month]
		# df_month["Date"] = df_month["Date"].apply(lambda x: x.date())
		months_dict[month] = df_month
	
	if exist_xlsx():
		upload_data(months_dict)
	
	create_xlsx()
	writer_data(months_dict)
	delete_sheet()
	writer_total_data()


def get_data(condition=None):
	driver = webdriver.Edge()
	driver.maximize_window()
	switch_url(driver, "https://lms.partaonline.ru/auth")

	login, password, *_ = get_content(driver, By.TAG_NAME, "input")

	send_data(login, "beckish10@mail.ru")
	send_data(password, "beckish10")

	accept, *_ = get_content(driver, By.TAG_NAME, "button")
	click_element(accept, 3)

	switch_url(driver, "https://lms.partaonline.ru/mentor/homeworks?offset=0&limit=20&order=desc&homework_mentor=7029&subject=10")

	status = get_content(driver, By.TAG_NAME, "button")[3]
	click_element(status, 3)


	*_, next_page = get_content(driver, By.CLASS_NAME, "n-button__icon")
	data = []
	flag = True
	while True:
		homeworks = get_content(driver, By.TAG_NAME, "a")[5:]

		for i, homework in enumerate(homeworks):
			link = homework.get_attribute("href")
			
			if condition is None:
				check, *_ = get_content(homework, By.TAG_NAME, "span")
				[date] = re.match(r"Проверено:\s(?P<date>[\d]{2}\.[\d]{2}\.[\d]{4})\,\s[\d]{2}\:[\d]{2}", check.text).groups()
				date = datetime.strptime(date, "%d.%m.%Y").date()
	
				if date.month < 9:
					flag = False
					break
			
			else:
				if condition == link:
					flag = False
					break

			driver.execute_script(f"window.open('{link}', '_blank');")
			switch_tab(driver, 0)

		tabs = len(get_tabs(driver)[1:])
		for _ in range(tabs):
			switch_tab(driver, 1)

			link = driver.current_url
			place_tasks = get_content(driver, By.CLASS_NAME, "n-card__content")
			tasks = len(get_content(place_tasks[4], By.TAG_NAME, "span"))

			[place_check] = get_content(driver, By.CLASS_NAME, "mb-100px")
			check = get_content(place_check, By.TAG_NAME, "span")[3].text

			date, time_ = re.match(r"Проверено:\s(?P<date>[\d]{2}\.[\d]{2}\.[\d]{4})\,\s(?P<time>[\d]{2}\:[\d]{2})", check).groups()
			date = datetime.strptime(date, "%d.%m.%Y").date()
			time_ = datetime.strptime(time_, "%H:%M").time()
			month = datetime.strftime(date, "%B")

			stage = get_content(place_tasks[3], By.CLASS_NAME, "n-flex")[-1].text
			stage = 10 if "ЕГЭ" in stage else 18
			money_tasks = tasks * stage

			data += [(link, date, time_, month, tasks, money_tasks)]

			close_tab(driver)

	
		if not flag:
			break

		switch_tab(driver, 0)
		click_element(next_page, 3)
	
	return data


def get_last_load():
	with pd.ExcelFile("money.xlsx", engine="openpyxl") as df:
		return df.parse(df.sheet_names[-2]).loc[0]["Link"]