from library import *

def get_token() -> None:
	return pd.read_csv('token.csv', dtype=str)

def get_error_id() -> None:
	return pd.read_csv('error_id.csv', dtype='str', index_col='ID')

def clear_error_id() -> None:
	pd.DataFrame({'ID': [], 'CODE': [], 'ERROR': []}).to_csv('error_id.csv', index=False)