import configparser


def pacs_settings(file='config.ini'):
    """
    Reads the configuration from the config.ini file
    :param file: config file name (optional, default='config.ini')
    :return: str: pacs settings
    """
    config = configparser.ConfigParser()
    config.read(file)
    ae_called = config['PACS']['AE_CALLED']
    ae_peer_address = config['PACS']['PEER_ADDRESS']
    ae_peer_port = config['PACS']['PEER_PORT']
    ae_title = config['PACS']['AE_TITLE']
    return '-aec {} {} {} -aet {}'.format(ae_called, ae_peer_address,
                                          ae_peer_port, ae_title)
