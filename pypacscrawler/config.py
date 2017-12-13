import configparser


def pacs_settings(file='config.ini'):
    """
    Reads the configuration from the config.ini file
    :param file: config file name (optional, default='config.ini')
    :return: str: PACS settings
    """
    config = configparser.ConfigParser()
    config.read(file)
    ae_called = config['PACS']['AE_CALLED']
    ae_peer_address = config['PACS']['PEER_ADDRESS']
    ae_peer_port = config['PACS']['PEER_PORT']
    ae_title = config['PACS']['AE_TITLE']
    return '-aec {} {} {} -aet {}'.format(ae_called, ae_peer_address,
                                          ae_peer_port, ae_title)


def get_solr_core_url(file='config.ini'):
    """
    Reads the configuration from the config.ini file
    :param file: config file name (optional, default='config.ini')
    :return: str: solr settings
    """
    config = configparser.ConfigParser()
    config.read(file)
    solr_core_url = config['SOLR']['CORE_PATH']
    last_char_is_slash = solr_core_url[-1] == '/'
    return solr_core_url if last_char_is_slash else solr_core_url + '/'


def get_report_show_url(file='config.ini'):
    """
    Reads the configuration from the config.ini file
    :param file: config file name (optional, default='config.ini')
    :return: str: report settings
    """
    config = configparser.ConfigParser()
    config.read(file)
    report_show_url = ['REPORT']['REPORT_SHOW_URL']
    return report_show_url
