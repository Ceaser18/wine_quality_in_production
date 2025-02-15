from src.datascience import logger
from src.datascience.pipeline.data_ingestion import DataIngestionTrainingPipeline

STAGE_NAME = "data_ingestion_STAGE"

try:
    logger.info(f"initiating pipeline for {STAGE_NAME}")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f"pipeline for {STAGE_NAME} completed")
except Exception as e:
    logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
    raise e


