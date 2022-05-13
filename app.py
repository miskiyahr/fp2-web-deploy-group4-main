# from crypt import methods
import flask

# Editing app.py to load the model
import numpy as np
import pickle
from datetime import datetime


# Untuk nyari template
app = flask.Flask(__name__, template_folder='templates')

# Columns
columns = ['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
       'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am',
       'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm',
       'Temp3pm', 'RainToday', 'year', 'month', 'day']

places = ['Adelaide', 'Albany', 'Albury', 'AliceSprings', 'BadgerysCreek', 'Ballarat', 'Bendigo', 'Brisbane', 'Cairns', 'Canberra', 'Cobar', 'CoffsHarbour', 'Dartmoor', 'Darwin', 'GoldCoast', 'Hobart', 'Katherine', 'Launceston', 'Melbourne', 'MelbourneAirport', 'Mildura', 'Moree', 'MountGambier', 'MountGinini', 'Newcastle', 'Nhil', 'NorahHead', 'NorfolkIsland', 'Nuriootpa', 'PearceRAAF', 'Penrith', 'Perth', 'PerthAirport', 'Portland', 'Richmond', 'Sale', 'SalmonGums', 'Sydney', 'SydneyAirport', 'Townsville', 'Tuggeranong', 'Uluru', 'WaggaWagga', 'Walpole', 'Watsonia', 'Williamtown', 'Witchcliffe', 'Wollongong', 'Woomera']

descriptions =  ['Weather Station', 'Minimum temperature (celsius)', 'Maximum temperature (celsius)', 
        'Amount Rainfall per day (mm)', 'evaoration for 24 hour (mm) ', 'bright sunshine in the day (hours)',
        'Strongest Wind speed (km/h)', 'Wind Speed in 10 minutes to 9am (km/h)', 
        'Wind Speed in 10 minutes to 3pm (km/h)', 'humidity at 9am (percent)', 'humidity at 3pm (percent)',
        'Atmospheric pressure at 9am (hpa)', 'Atmospheric pressure at 3pm (hpa)',
        'Fraction of sky obscured by cloud at 9am (oktas)', 'Fraction of sky obscured by cloud at 3pm (oktas)', 
        'Temperatur 3pm (celsius)' ,'Rain or not (0 = no, 1 = yes)']

# Rute
@app.route('/')
def main():
  return(flask.render_template('main.html', descriptions = descriptions, len = len(columns), columns = columns, float_features = columns, algorithm='algorithm', places = places, lenplaces = len(places), place="Location"))
if __name__ == '__main__':
  app.run(debug=True)

logress = pickle.load(open('./model/logistic_regression.pkl', 'rb'))
svm = pickle.load(open('./model/svm.pkl', 'rb'))

# Redirecting the API to predict the result 
@app.route('/predict',methods=['POST'])
def predict():
  '''
  For rendering results on HTML GUI
  '''
  name_predict = ['Logistic Regression', 'SVM']
  request = [x for x in flask.request.form.values()]
  just_date = datetime.strptime(request.pop(), "%Y-%m-%d")
  
  try:
    float_features = [float(x) for x in request]
    in_predict = int(float_features.pop(0))

    # Mengubah inputan date jadi year month day

    float_features.append(just_date.year)
    float_features.append(just_date.month)
    float_features.append(just_date.day)
  except:
    float_features = columns
    return flask.render_template('main.html',
      alert_message='Inputnya harus angka', 
      float_features = columns,
      len = len(columns),
      columns = columns,
      algorithm='algorithm',
      places = places,
      lenplaces = len(places),
      place="Location",
      descriptions = descriptions,
    )

  final_features = [np.array(float_features)]

  # Memilih prediksi yang digunakan
  prediction = 0
  if(in_predict == 0):
    prediction = logress.predict(final_features)
  else:
    prediction = svm.predict(final_features)



  return flask.render_template('main.html',
    prediction_text=prediction[0],
    float_features=float_features,
    len = len(columns),
    columns = columns,
    algorithm = name_predict[in_predict],
    places = places,
    lenplaces = len(places),
    place=places[int(float_features[0])],
    descriptions = descriptions,
  )
