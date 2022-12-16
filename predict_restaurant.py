import joblib
import numpy
from keras.models import load_model

class PredictRestaurant:
    def predictRestaurent(self,df):
        try:
            if len(df) == 0:
                print("array is empty")
                return 0.0
            print("predicting started")
            text_model = joblib.load('Project')
            a = text_model.predict(df)
            return numpy.average(a)

        except Exception as e:
            print(f"predict restaurant failed {e}")
            return 0.0