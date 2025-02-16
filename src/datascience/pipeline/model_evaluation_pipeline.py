from src.datascience.config.configuration import ConfigurationManager

from src.datascience.components.model_evaluation import ModelEvaluation

from src.datascience import logger

STAGE_NAME = "model_evaluation_STAGE"

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def initiate_model_evaluation(self):
        config=ConfigurationManager()
        model_evaluation_config=config.get_model_evaluation_config()

        model_evaluation=ModelEvaluation(config=model_evaluation_config)
        model_evaluation.log_into_mlflow()

if __name__ == "__main__":
    try:
        logger.info(f"initiating pipeline for {STAGE_NAME}")
        obj = ModelEvaluationPipeline()
        obj.initiate_model_evaluation()
        logger.info(f"pipeline for {STAGE_NAME} completed")
    except Exception as e:
        logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
        raise
    
