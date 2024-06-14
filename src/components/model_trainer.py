import os
import sys
from dataclasses import dataclass

from catboost import CatBoostClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score,mean_squared_error,r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model




@dataclass
class ModelTainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split traiing and test input data")
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
                )
            
            models={
                "Random Forest":RandomForestClassifier(),
                "Decision Tree":DecisionTreeClassifier(),
                "Ada Boost":AdaBoostClassifier(),
                "Gradient Boost":GradientBoostingClassifier(),
                "XGBoost":XGBRegressor(),
                "CatBoost":CatBoostClassifier(verbose=False),
               
                "Linear Regression":LinearRegression(),
                "XGBRegressor":XGBRegressor()
            }
            

            model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)

            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("no best model found")
            logging.info("best found model on both training and test data")

            save_object(self.model_trainer_config.trained_model_file_path,
                        obj=best_model)
            predicted=best_model.predict(x_test)
            r2_square=r2_score(y_test,predicted)
            return r2_square
        except Exception as e:
            raise CustomException(e,sys)
