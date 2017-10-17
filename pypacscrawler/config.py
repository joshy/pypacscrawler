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
