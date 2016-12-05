from pyRango.api import ArangoHttpClient

USERNAME = 'root'
PASSWORD = 'SECRET'
HOSTNAME = 'localhost'
PORT = 8529


def print_summary(header, results, num_tabs=0):
    print('\n{TABS}{HEADER}\n{TABS}{UNDERLINE}'.format(HEADER=header,
                                                       UNDERLINE=''.join(['-' for _ in range(len(header))]),
                                                       TABS=''.join(['\t' for _ in range(num_tabs)])))
    if isinstance(results, dict):
        for key, value in results.items():
            print('{TABS}{KEY}: {VALUE}'.format(KEY=key, VALUE=value, TABS=''.join(['\t' for _ in range(num_tabs+1)])))
    elif isinstance(results, str):
        print('{TABS}{VALUE}'.format(TABS=''.join(['\t' for _ in range(num_tabs+1)]), VALUE=results))
    elif hasattr(results, '__iter__'):
        if header.endswith('s'):
            header = header[:-1]
        for count, item in enumerate(results):
            print_summary('{HEADER} {COUNT}:'.format(HEADER=header, COUNT=count+1), item, num_tabs=num_tabs+1)


def main():
    client = ArangoHttpClient(host=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD)
    print_summary('Current Database', client.database.current())
    print_summary('Databases', client.database.list())
    print_summary('Collections', client.collection.list(exclude_system=True))
    print_summary('Collection Info', client.collection.get('persons'))
    print_summary('Collection Info (Multi)', client.collection.get('persons', 'properties'))

if __name__ == '__main__':
    main()
