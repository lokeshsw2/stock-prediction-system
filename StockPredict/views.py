from django.shortcuts import render
###############################
from yahoo_fin import stock_info as si
from datetime import date, timedelta
import pandas as pd
import datetime as dt
from sklearn.linear_model import LinearRegression
import math


# op = [53.16999816894531, 218.9499969482422, 139.22999572753906, 117.77999877929688, 1226.5699462890625, 1777, 275.92999267578125, 53.16999816894531, 189.33999633789062]
# cl = [218.72000122070312, 139.13999938964844, 118.87999725341797, 1234.68994140625, 1785.300048828125, 277.44000244140625, 54.02000045776367, 186.82000732421875]
# vol = [16786679, 13188152, 6892877, 776509, 2635300, 1706319, 13248587, 12657349]
# maxStockCompany = 'Amazon'

op = list()
cl = list()
vol = list()
k = 0
names = ['Apple', 'Microsoft', 'JP Morgan', 'Google', 'Amazon', 'Adobe', 'Oracle', 'Facebook']


df = pd.read_csv('apple.csv')
data = df.sort_index(ascending=False, axis=0)
dc1 = data['Date']
dc2 = data['Close']
dc1_list = list(dc1)
dc2_list = list(dc2)
df.index = df['Date']
df['Date'] = pd.to_datetime(df.Date, format='%d-%m-%Y')
new_data = pd.DataFrame(index=range(0, len(df)), columns=['Date', 'Close'])
data = df.sort_index(ascending=True, axis=0)
df.index = df['Date']

for i in range(0, len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]

new_data['Date'] = pd.to_datetime(new_data['Date'])
new_data['Date'] = new_data['Date'].map(dt.datetime.toordinal)
model = LinearRegression()
model.fit(new_data['Date'].values.reshape(-1, 1), new_data['Close'])

df2 = pd.read_csv('demo.csv')
df2['Date'] = pd.to_datetime(df2.Date, format='%d-%m-%Y')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['Date'] = df2['Date'].map(dt.datetime.toordinal)
preds = model.predict(df2['Date'].values.reshape(-1, 1))

df3 = pd.read_csv('demo.csv')
df3['Date'] = pd.to_datetime(df3.Date, format='%d-%m-%Y')##############


# l1 = []

def demo():
    l_copy = [];
    v1 = 1999
    for i in range(240):
        if i % 21 == 0:
            l_copy.append(str(v1))
            v1 = v1 + 1
        else:
            l_copy.append('')
    # print(l)
    return l_copy
    # l1 = list(preds)
    #
            # plt.plot(df3, preds)
            ###################################################################



def liveStock():

    global maxStock, maxStockCompany, names
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    i = 0

    names = ['Apple', 'Microsoft', 'JP Morgan', 'Google', 'Amazon', 'Adobe', 'Oracle', 'Facebook']
    for sym in ['AAPL', 'MSFT', 'JPM', 'GOOGL', 'AMZN', 'ADBE', 'ORCL', 'FB']:
        df = si.get_data(sym, start_date=yesterday, end_date=today)

        op.append(math.trunc(list(df['open'])[0]))
        cl.append(math.trunc(list(df['adjclose'])[0]))
        vol.append((list(df['volume'])[0]))

    ind = cl.index(max(cl))
    maxStock = max(cl)
    maxStockCompany = names[0]


def dashboard(request):

    #############################################################
    # l_copy = l1.copy()
    # l_copy = [80.125, 21.625, 14.36, 76.9, 85.73, 90.13, 339.32, 455.49, 117.16, 143.66, 166, 350]
    # y = int(l_copy[-1])

    global k

    if k == 0:
        liveStock()
        k = k + 1


    l_copy = demo()


    graphType = "Year"
    year = "year"


    companyName = maxStockCompany
    y = cl[names.index(companyName)]

    # companyName = 'Amazon'
    # y = cl[names.index(companyName)]

    print(request.POST.get('1 day'))
    if isinstance(request.POST.get('1 day'), str):
        if request.POST.get('1 day') in ['1 day', '1 week', '1 month', '5 year', '1 year', 'Overall', "Max"]:
            companyName = request.POST.get('dashCompany')
            y = cl[names.index(companyName)]

    if request.POST.get('company') in ["Apple", "Microsoft", "JP Morgan", "Google", "Amazon", "Oracle", "Adobe",
                                       "Facebook"]:
        companyName = request.POST.get('company')
        y = cl[names.index(companyName)]


    # print(year)


    return render(request, 'dashboard.html', {'x': dc1_list, 'y': math.trunc(y), 'year': year,
                                              'graphType': graphType,
                                            'z': dc2_list, 'companyName':companyName, 'maxStock':maxStock,
                                            'maxStockCompany': maxStockCompany, 'sp': cl})


def about(request):

    return render(request, 'user.html')


def document(request):

    return render(request, 'document.html')


def companyList(request):

    # op = [1, 2, 3, 4, 5, 6, 7, 8]
    # cl = [1, 2, 3, 4, 5, 6, 7, 8]
    # vol = [1, 2, 3, 4, 5, 6, 7, 8]
    return render(request, 'tables.html', {'close': cl, 'open': op, 'revenue':vol})


