import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines

# d_ta	napi középhőmérséklet [°C]
# d_tx	napi maximumhőmérséklet [°C]
# d_tn	napi minimumhőmérséklet [°C]
# d_rs	napi csapadékösszeg [mm]
# d_rf	napi csapadékösszeg fajtája
# d_ss	napfénytartam napi összege [óra]
# d_ssr	globálsugárzás napi összege [J/cm2]
# date range 1901-01-01 2020-12-31


df = pd.read_csv('BP_d.txt', delimiter=';')
df['Date'] = pd.to_datetime(df['#datum'])
df = df.drop(['#datum'], axis=1)

# 1901 - 1911
# 2009 - 2019


# 1901-01-01 - 1911-01-01 
df1 = df[(df['Date'] >= '1901-01-01') & (df['Date'] <= '1911-01-01')]
df1['Date'] = df1['Date'].dt.strftime('%m-%d')
df1 = df1[df1['Date'] != '02-29']
df1_mid = df1.groupby('Date').agg({'d_ta':np.mean}).reset_index(drop=False)


# 2009-01-01 - 2019-01-01 
df2 = df[(df['Date'] >= '2009-01-01') & (df['Date'] <= '2019-01-01')]
df2['Date'] = df2['Date'].dt.strftime('%m-%d')
df2 = df2[df2['Date'] != '02-29']
df2_mid = df2.groupby('Date').agg({'d_ta':np.mean}).reset_index(drop=False)


plt.figure()
ax = plt.gca()
#ax.set_aspect('1')
plt.xlim(0,364)


# 1901-01-01 - 1911-01-01
plt.plot(df1_mid['Date'], df1_mid['d_ta'], color='#3434ff', linewidth = 2, alpha=0.6)
legend1 = mlines.Line2D([], [], color='#3434ff')


# 2009-01-01 - 2019-01-01
plt.plot(df2_mid['Date'], df2_mid['d_ta'], color='#ff3434', linewidth = 2, alpha=0.6)

plt.gca().fill_between(range(len(df1_mid['d_ta'])), 
                       df1_mid['d_ta'], df2_mid['d_ta'], 
                       facecolor='#0000ff', 
                       alpha=0.10)
legend2 = mlines.Line2D([], [], color='#ff3434')

ax.legend([legend1, legend2],['daily mean temperatures 1901 - 1911','daily mean temperatures 2009 - 2019'])

x = plt.gca().xaxis

locator = mdates.MonthLocator()
fmt = mdates.DateFormatter('%b')

x.set_major_locator(locator)
x.set_major_formatter(fmt)

plt.xlabel('Month')
plt.ylabel('Temperature [°C]')
plt.title('Daily mean temperature comparison in Budapest / Hungary')

plt.show()