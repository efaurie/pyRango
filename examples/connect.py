from pyRango import ArangoClient

USERNAME = 'root'
PASSWORD = 'SECRET'
HOSTNAME = 'localhost'
PORT = 8529


def main():
    client = ArangoClient(host=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD)
    current_info = client.database.current()
    print('\nCurrent Database\n----------------')
    for key, value in current_info.items():
        print('{KEY}: {VALUE}'.format(KEY=key, VALUE=value))

if __name__ == '__main__':
    main()
