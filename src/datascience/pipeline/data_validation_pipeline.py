from src.datascience.config.configuration import ConfigurationManager

from src.datascience.components.data_validation import DataValiadtion

from src.datascience import logger

STAGE_NAME = "data_validation_STAGE"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config=ConfigurationManager()
        data_validation_config=config.get_data_validation_config()

        data_validation=DataValiadtion(config=data_validation_config)
        data_validation.validate_all_columns()

if __name__ == "__main__":
    try:
        logger.info(f"initiating pipeline for {STAGE_NAME}")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f"pipeline for {STAGE_NAME} completed")
    except Exception as e:
        logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
        raise



