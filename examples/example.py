from pyRango import ArangoClient

USERNAME = 'root'
PASSWORD = 'SECRET'
HOSTNAME = 'localhost'
PORT = 8529


def main():
    client = ArangoClient(host=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD)
    collection = client.create_collection('example_collection')
    collection.create_document({'foo': 'Test 1', 'bar': 'Test 2'})
    collection.commit()

if __name__ == '__main__':
    main()
