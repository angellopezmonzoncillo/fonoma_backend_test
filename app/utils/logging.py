import logging

app_logger = None

LOG_LEVEL = "INFO"

def get_app_logger(name) -> logging.Logger:
    logging.basicConfig(filename=f'logs_{name.lower()}.log', filemode='a', level=logging.INFO)
    """returns a configured logger"""
    global app_logger
    if app_logger != None:
        return app_logger

    # remove handlers from rootLogger
    # logging.getLogger().handlers.clear()
    logger = logging.getLogger(name)
    log_level = getattr(logging, LOG_LEVEL)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(
        # se saca formateo de fecha "%(asctime)s " si se usa aws ya que es redundante en cloudwatch
        logging.Formatter(
            "%(asctime)s - %(levelname)s [%(filename)s][%(funcName)s] %(message)s")
    )

    log_handler.setLevel(log_level)
    logger.level = log_level
    # logger.handlers.clear()
    logger.addHandler(log_handler)
    app_logger = logger

    return app_logger