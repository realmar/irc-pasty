err_msg = 'Wrong config please consult README.md and have a look at the example config pasty_server.conf'

def configCheck(config):
    if config == None or \
        config.get('pasty') == None or \
        config.get('pasty').get('url') == None or \
        config.get('irc') == None or \
        config.get('irc').get('server') == None or \
        config.get('irc').get('port') == None or \
        config.get('irc').get('username') == None or \
        config.get('irc').get('channels') == None:
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
