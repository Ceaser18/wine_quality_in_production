from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.datascience.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.datascience.pipeline.model_trainer_pipeline import ModelTrainerPipeline



STAGE_NAME = "data_ingestion_STAGE"

try:
    logger.info(f"initiating pipeline for {STAGE_NAME}")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f"pipeline for {STAGE_NAME} completed")
except Exception as e:
    logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
    raise e


STAGE_NAME = "data_validation_STAGE"

try:
    logger.info(f"initiating pipeline for {STAGE_NAME}")
    data_validation = DataValidationTrainingPipeline()
    data_validation.initiate_data_validation()
    logger.info(f"pipeline for {STAGE_NAME} completed")
except Exception as e:
    logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
    raise e


STAGE_NAME = "data_transformation_STAGE"
try:
    logger.info(f"initiating pipeline for {STAGE_NAME}")
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.initiate_data_transformation()
    logger.info(f"pipeline for {STAGE_NAME} completed")
except Exception as e:
    logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
    raise e


STAGE_NAME = "model_training_STAGE"
try:
    logger.info(f"initiating pipeline for {STAGE_NAME}")
    model_training = ModelTrainerPipeline()
    model_training.initiate_model_training()
    logger.info(f"pipeline for {STAGE_NAME} completed")
except Exception as e:
    logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
    raise e

