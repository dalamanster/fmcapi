import logging


def test__deploymentrequests(fmc):
    logging.info('Testing fmc.deploymentrequests() method.')
    logging.info(fmc.deploy_changes())
    logging.info(fmc.deploymentrequests())
    logging.info('Testing fmc.deploymentrequests() method done.\n')
