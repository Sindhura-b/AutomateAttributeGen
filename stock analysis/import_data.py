import datetime

from Google import Create_Service
import pandas as pd
import yfinance as yf

CLIENT_SECRET_FILE = 'client_secret_602106804635-r22k1df9bp4d73qt1gat3v27mtgtr20t.apps.googleusercontent.com.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
gsheetId = '1mZghpSk7wSh0sOy3s_Mg9bxtSW2Am3Y8UUubND9y0Ng'

def get_symbol_value_by_date(symbol, date=datetime.datetime.now()):
    date1 = date + datetime.timedelta(days=1)
    data = yf.download(symbol, start=date.strftime("%Y-%m-%d"), end=date1.strftime("%Y-%m-%d"), progress=False)
    # pdb.set_trace()
    value = data['Close'].values[0]
    return value

s = Create_Service(CLIENT_SECRET_FILE,API_SERVICE_NAME,API_VERSION,SCOPES)
gs = s.spreadsheets()
rows = gs.values().get(spreadsheetId=gsheetId, range='Sheet1').execute()
data = rows.get('values')
df = pd.DataFrame(data, columns=['Ticker', 'Buy zone target 3', 'Buy zone target 2', 'Buy zone target 1'])
#print(df['Ticker'])
for key, value in df.iterrows():
    #print(value['Ticker'])
    curr_value = get_symbol_value_by_date(str(value['Ticker']), date=datetime.datetime.now())
    print(curr_value, value['Buy zone target 3'])
    if float(curr_value) <= float(value['Buy zone target 3']) and float(curr_value) >= float(value['Buy zone target 2']):
        print('Buy')
    elif float(curr_value) <= float(value['Buy zone target 2']) and float(curr_value) >= float(value['Buy zone target 1']):
        print('Strong Buy')
    else:
        print('Wait')



    #print()