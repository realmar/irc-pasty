"""Check config integrity."""

err_msg = 'Wrong config please consult README.md and have a look at the example config pasty_server.conf'


def configCheck(config):
    """Check config for existence of required options."""
    if config is None or \
            config.get('pasty') is None or \
            config.get('pasty').get('url') is None or \
            config.get('irc') is None or \
            config.get('irc').get('server') is None or \
            config.get('irc').get('port') is None or \
            config.get('irc').get('username') is None or \
            config.get('irc').get('channels') is None:
        print(err_msg)
        return False
    else:
        for c in config['irc']['channels']:
            try:
                tmp = c['name']
            except:
                print(err_msg + "\nName attribute missing in channels")
                return False

        return True
