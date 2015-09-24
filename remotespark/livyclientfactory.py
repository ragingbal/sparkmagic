# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.

from base64 import b64encode

from log import Log
from connectionstringutil import get_connection_string_elements
from livysession import LivySession
from livyclient import LivyClient
from reliablehttpclient import ReliableHttpClient


class LivyClientFactory(object):
    """Spark client for Livy endpoint"""
    logger = Log()

    def __init__(self):
        pass

    def build_client(self, connection_string):
        cso = get_connection_string_elements(connection_string)

        token = b64encode(bytes(cso.username + ":" + cso.password)).decode("ascii")
        headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(token)}

        http_client = ReliableHttpClient(cso.url, headers)

        spark_session = LivySession(http_client, "spark")
        pyspark_session = LivySession(http_client, "pyspark")

        return LivyClient(spark_session, pyspark_session)
