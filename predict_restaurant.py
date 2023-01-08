import joblib
import numpy
from keras.models import load_model

class PredictRestaurant:
    def predictRestaurent(self,df):
        try:
            #checkiing scraped data is empty
            if len(df) == 0:
                print("array is empty")
                return 0.0
            print("predicting started")
            # load pre trained model
            text_model = joblib.load('Project')
            # predict
            a = text_model.predict(df)
            #return predicted best restaurents
            return numpy.average(a)

        except Exception as e:
            print(f"predict restaurant failed {e}")
            return 0.0