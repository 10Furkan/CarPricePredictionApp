# Car Price Prediction App 

This project predicts secondhand car prices. This project does not requires any API, it works offline.

## Project Architecture (Monorepo)

This project is designed to house both data science processes and mobile application code in a single repository .:

* **`ML_model/`**: Data preprocessing, Python code that includes model training processes.
* **`AndroidApp/`**: A Kotlin-based Android Studio project that houses the user interface and an offline prediction algorithm.

## Machine Learning Part

The model predicts the price by considering parameters such as the car's year, mileage, fuel type, and transmission type.
* **Algorithm:** Random Forest Regressor
* **Optimization:** To avoid straining the mobile device's processor and to prevent the application (APK) from becoming excessively large, the number of trees (`n_estimators=15`) and depth (`max_depth=10`) have been optimized.
* **Model transformation:** The trained model was converted to pure Java code using the `m2cgen` library and directly integrated into the Android project.

## Technologies

* **Data Science:** Python, Pandas, Scikit-Learn, m2cgen
* **Mobile Development:** Kotlin, Android Studio, XML

## 📱 Screenshots
<img width="360" height="776" alt="image" src="https://github.com/user-attachments/assets/47261aa9-f60f-4d2d-bdc9-ff3c31a48b07" />

## Installation

# To run the Android application:
1. Clone the repository to your computer.
2. Open Android Studio and select the `AndroidApp` folder as the project.
3. Wait for Gradle synchronization to finish and run it on the emulator/device.

2. Gerekli kütüphaneleri kurun: `pip install pandas scikit-learn m2cgen`
3. `train.py` (veya sizin dosya adınız) dosyasını çalıştırın.
4. Çıkan yeni `.java` dosyasını Android projesindeki ilgili konuma kopyalayın.
