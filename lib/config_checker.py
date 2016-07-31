def configCheck(config):
    if config == None or \
        config.get('pasty') == None or \
        config.get('pasty').get('url') == None or \
        config.get('irc') == None or \
        config.get('irc').get('server') == None or \
        config.get('irc').get('port') == None or \
        config.get('irc').get('username') == None or \
        config.get('irc').get('channels') == None:
        print('Wrong config please consult README.md and have a look at the example config pasty_server.conf')

        return False
    else:
        return True
