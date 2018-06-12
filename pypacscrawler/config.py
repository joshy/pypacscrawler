import flask


def pacs_settings(app):
    """
    Reads the configuration from the default flask instance folder
    :param the flask app
    :return: str: PACS settings
    """
    ae_called = app.config['AE_CALLED']
    ae_peer_address = app.config['PEER_ADDRESS']
    ae_peer_port = app.config['PEER_PORT']
    ae_title = app.config['AE_TITLE']
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


def get_solr_upload_url(file='config.ini'):
    """
    Reads the configuration from the config.ini file
    :param file: config file name (optional, default='config.ini')
    :return: str: solr settings
    """
    config = configparser.ConfigParser()
    config.read(file)
    solr_core_url = config['SOLR']['UPLOAD_URL']
    last_char_is_slash = solr_core_url[-1] == '/'
    return solr_core_url[:-1] if last_char_is_slash else solr_core_url


def get_report_show_url(file='config.ini'):
    """
    Reads the configuration from the config.ini file
    :param file: config file name (optional, default='config.ini')
    :return: str: report settings
    """
    config = configparser.ConfigParser()
    config.read(file)
    report_show_url = config['REPORT']['REPORT_SHOW_URL']
    return report_show_url
