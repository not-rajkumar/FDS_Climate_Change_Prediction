

## Climate Change Analysis Dashboard

This project is a part of the Digital Assessment for **BCSE206L – Foundations of Data Science**. It provides forecasting and visualization of Earth's surface temperature using three models: **ARIMA**, **LSTM**, and a **Hybrid ARIMA-LSTM** model, integrated into an interactive **Dash dashboard**.




## Features

- Time-series forecasting using:
  - ARIMA
  - LSTM
  - ARIMA-LSTM Hybrid
-  Interactive geospatial dashboard (with `plotly`)
-  Comparison of actual vs predicted temperatures
-  Insight into climate trends and predictions

---

##  Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/your-username/climate-dashboard.git
cd climate-dashboard
pip install -r requirements.txt
```



## Running the App Locally

```bash
python app.py
```

Then open your browser at: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

##  Deployment

This app is ready to deploy on platforms like **Heroku** using the `Procfile`.

To deploy:
```bash
heroku login
heroku create climate-dashboard-demo
git push heroku main
heroku open
```


##  Contributors

- Madhur Vinayak Pophale (22BCE2478)
- M Rajkumar (22BCE0978)



## 📘 Acknowledgements

This dashboard and analysis are part of the course project for **BCSE206L – Foundations of Data Science** under VIT.
