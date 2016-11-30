import abc


class HttpVersionError(Exception):
    pass


class ContentLengthError(Exception):
    pass


class RequestLengthError(Exception):
    pass


class HeaderLengthError(Exception):
    pass


class UnsupportedActionError(Exception):
    pass


class ArangoError(Exception):
    pass


def raise_for_status(response):
    if response.status_code == 405:
        raise UnsupportedActionError('The HTTP Request Type Is Not Supported At This Endpoint')
    elif response.status_code == 414:
        raise RequestLengthError('The Request URI is longer than the maximum supported length (16K)')
    elif response.status_code == 431:
        raise HeaderLengthError('The Request Header is larger than the maximum supported size (1 MB)')
    elif response.status_code == 400:
        raise ContentLengthError('The HTTP Request payload was contained less than the ContentLength.')
    elif response.status_code == 411:
        raise ContentLengthError('The HTTP Request Method requires a ContentLength header but it was not provided')
    elif response.status_code == 413:
        raise ContentLengthError('The HTTP Request payload was larger than the maximum supported size (512 MB)')
    elif response.status_code == 505:
        raise HttpVersionError('The HTTP Version being used is not supported, you must use HTTP/1.0 or HTTP/1.1')

    response.raise_for_status()


def parse_response(response, ignore_errors=False):
    raise_for_status(response)
    output = response.json()

    if output.get('error', False) and not ignore_errors:
        raise ArangoError('Request Failed!')

    return output.get('result', dict())


class Endpoint(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, client, route='DB'):
        self.client = client
        self.route = route
        self.suffix = None

    @property
    def endpoint_uri(self):
        if self.route.upper() == 'DB':
            base = self.client.db_uri
        else:
            base = self.client.admin_uri

        return '{BASE}/{SUFFIX}'.format(BASE=base, SUFFIX=self.suffix)

    def build_uri(self, *args):
        if not len(args):
            return self.endpoint_uri
        return '{BASE}/{ARGS}'.format(BASE=self.endpoint_uri, ARGS='/'.join(args))

    def get(self, uri):
        return parse_response(self.client.session.get(uri))

    def post(self, uri, payload=None):
        if not payload:
            payload = dict()

        parse_response(self.client.session.post(uri, json=payload))

    def delete(self, uri):
        parse_response(self.client.session.delete(uri))
