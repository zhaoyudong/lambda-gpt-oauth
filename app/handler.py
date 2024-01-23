import serverless_wsgi
from application import app
from loguru import logger


def lambda_handler(event, context):
    """
    the entry point of the lambda function

    :param event:
    :param context:
    :return:
    """
    logger.info(event)
    res = serverless_wsgi.handle_request(app, event, context)
    logger.info(res)
    return res
