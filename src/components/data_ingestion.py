import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split    
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts',"train.csv")
    test_data_path:str=os.path.join('artifacts',"test.csv")
    raw_data_path:str=os.path.join('artifacts',"raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingesion_config=DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or compoenent")
        try:
            df=pd.read_csv('notebook/data/StudentsPerformance.csv.csv')

            logging.info("exported the data as dataframe ")
            os.makedirs(os.path.dirname(self.ingesion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingesion_config.raw_data_path,index=False)

            logging.info("train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingesion_config.train_data_path,index=False)

            test_set.to_csv(self.ingesion_config.test_data_path,index=False)
            logging.info("ingestion of the data completed successfully")
            return(
                self.ingesion_config.train_data_path,
                self.ingesion_config.test_data_path,
                self.ingesion_config.raw_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data,raw_data=obj.initiate_data_ingestion()
    data_transformation_obj=DataTransformation()
    train_arr, test_arr,_=data_transformation_obj.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))


