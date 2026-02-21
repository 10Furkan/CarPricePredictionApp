import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
import statsmodels.api as sm
from sklearn import preprocessing


# 1. Veriyi yükle
datas = pd.read_csv('car_price_data.csv')

owner_mapping = {
    'First Owner': '1st',
    'Second Owner': '2nd',
    'Third Owner': '3rd',
    'Fourth & Above Owner': '4plus',
    'Test Drive Car': 'test'
}

datas['owner'] = datas['owner'].replace(owner_mapping)

# Şimdi get_dummies yaparsan isimler şöyle olur: owner_1st, owner_2nd, owner_4plus
owner_df = pd.get_dummies(datas['owner'], prefix='owner', drop_first=True, dtype=int)
# 2. Filtreleme ve İndeks Sıfırlama
datas = datas[datas['fuel'].isin(['Petrol', 'Diesel'])]
datas = datas[datas['seller_type'].isin(['Individual', 'Dealer'])].reset_index(drop=True)

# 3. Label Encoding (İki seçenekli kategorik veriler için)
le = preprocessing.LabelEncoder()
datas["fuel"] = le.fit_transform(datas["fuel"])
datas["seller_type"] = le.fit_transform(datas["seller_type"])
datas["transmission"] = le.fit_transform(datas["transmission"])

# 4. One-Hot Encoding (Çok seçenekli 'owner' sütunu için)
# dtype=int parametresi True/False yerine doğrudan 1/0 üretmesini sağlar
owner_df = pd.get_dummies(datas['owner'], prefix='owner', drop_first=True, dtype=int)

# 5. Birleştirme ve Temizlik
datas = pd.concat([datas, owner_df], axis=1)
datas = datas.drop(["owner", "name"], axis=1) # 'name' model için gereksizdir

# 6. Bağımsız ve Bağımlı Değişkenlerin Ayrılması
# selling_price (Y) hariç her şey X'tir
x = datas.drop("selling_price", axis=1)
y = datas["selling_price"]

# Numpy array'e dönüştürme (Model eğitimi için bu format istenir)
X = x.values
Y = y.values

# Sadece sayısal bir sütun için (örneğin selling_price)
Q1 = datas['selling_price'].quantile(0.25)
Q3 = datas['selling_price'].quantile(0.75)
IQR = Q3 - Q1

alt_sinir = Q1 - 1.5 * IQR
ust_sinir = Q3 + 1.5 * IQR

# Aykırı değerleri filtreleme
temiz_datas = datas[(datas['selling_price'] >= alt_sinir) & (datas['selling_price'] <= ust_sinir)]

print(f"Silinen veri sayısı: {len(datas) - len(temiz_datas)}")
datas = temiz_datas.reset_index(drop=True)

'''
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X,Y)
model = sm.OLS(lin_reg.predict(X),X)
#print(model.fit().summary())
print("Linear R2 degeri:")
print(r2_score(Y, lin_reg.predict((X))))


from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 4)
x_poly = poly_reg.fit_transform(X)
#print(x_poly)
lin_reg2 = LinearRegression()
lin_reg2.fit(x_poly,y)
model2 = sm.OLS(lin_reg2.predict(poly_reg.fit_transform(X)),X)
print("Polynomial R2 degeri:")
print(r2_score(Y, lin_reg2.predict(poly_reg.fit_transform(X)) ))


from sklearn.preprocessing import StandardScaler
sc1 = StandardScaler()
x_olcekli = sc1.fit_transform(X)
sc2 = StandardScaler()
y_olcekli = np.ravel(sc2.fit_transform(Y.reshape(-1,1)))
from sklearn.svm import SVR
svr_reg = SVR(kernel = 'rbf')
svr_reg.fit(x_olcekli,y_olcekli)
model3 = sm.OLS(svr_reg.predict(x_olcekli),x_olcekli)
#print(model3.fit().summary())
print("SVR R2 degeri:")
print(r2_score(y_olcekli, svr_reg.predict(x_olcekli)) )


from sklearn.tree import DecisionTreeRegressor
r_dt = DecisionTreeRegressor(random_state=0)
r_dt.fit(X,Y)
#print('Decision Tree OLS')
model4 = sm.OLS(r_dt.predict(X),X)
#print(model4.fit().summary())
print("Decision Tree R2 degeri:")
print(r2_score(Y, r_dt.predict(X)) )

'''

from sklearn.ensemble import RandomForestRegressor
import m2cgen as m2c
rf_reg = RandomForestRegressor(n_estimators = 15,max_depth = 10, random_state=0)
rf_reg.fit(X,Y.ravel())
print("Random Forest R2 degeri:")
print(r2_score(Y,rf_reg.predict(X)) )
code = m2c.export_to_java(rf_reg)

with open("CarPrediction","w") as f:
    f.write(code)



#şimdilik en iyi gözükenler decisiontree ve random forest, ama veri setini bölüp tekrar deneyecem