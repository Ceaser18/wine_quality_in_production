from src.datascience.config.configuration import ConfigurationManager

from src.datascience.components.model_trainer import ModelTrainer

from src.datascience import logger

STAGE_NAME = "model_training_STAGE"

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def initiate_model_training(self):
        config=ConfigurationManager()
        model_training_config=config.get_model_trainer_config()

        model_trainer=ModelTrainer(config=model_training_config)
        model_trainer.train()

if __name__ == "__main__":
    try:
        logger.info(f"initiating pipeline for {STAGE_NAME}")
        obj = ModelTrainerPipeline()
        obj.initiate_model_training()
        logger.info(f"pipeline for {STAGE_NAME} completed")
    except Exception as e:
        logger.error(f"pipeline for {STAGE_NAME} failed with error: {e}")
        raise
    




