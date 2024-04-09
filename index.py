from flask import Flask, jsonify, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

@app.route('/get', methods=['POST'])
def receive_data():
    global age
    global height
    global weight
    age = request.form['age']
    height = request.form['height']
    weight = request.form['weight']
    print('User Age:', age)
    print('User Height:', height)
    print('User Weight:', weight)
    return 'Data received successfully'

@app.route('/send', methods=['GET'])
def send_data():
      dataset = pd.read_csv('meals.csv')

      X = dataset[['age', 'height', 'weight']]
      y = dataset['meal']

      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

      model = RandomForestClassifier()
      model.fit(X_train, y_train)

      y_pred = model.predict(X_test)

      userAge = age
      userHeight = height
      userWeight= weight

      today_data = pd.DataFrame([[userAge, userHeight, userWeight]], columns=['age', 'height', 'weight'])

      prediction = model.predict(today_data)

      listP = prediction.tolist()

      predStr = listP[0]

      spli_str = predStr.split('|')

      # Trim leading and trailing spaces from each menu item and store them in separate variables
      breakfast = spli_str[0].strip()
      lunch = spli_str[1].strip()
      dinner = spli_str[2].strip()

      # print('User Age:', age)
      # print('User Height:', height)
      # print('User Weight:', weight)

      print(breakfast)
      print(lunch)
      print(dinner)

      data = {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner}
      return jsonify(data)

if __name__ == '__main__':
    app.run()
  # app.run(host='0.0.0.0', port=5000)