from configparser import ConfigParser


"""
    Loads configuration parameters from a specified section in a configuration file.
"""
def load_config(filename='./configs/database.ini', section='postgresql'):
    config = ConfigParser()
    config.read(filename)
    # get section, default to postgresql
    configObj = {}
    print(config.sections())
    if config.has_section(section):
        params = config.items(section)
        print("Printing params: ", params)
        for param in params:
            configObj[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return configObj

if __name__ == '__main__':
    config = load_config()
    print(config)