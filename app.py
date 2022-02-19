#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server
from urllib.parse import urlparse, parse_qs
import logging
import json
import redis
import http.server
import re 

# Redis settings
redis_host = "redis-master"
redis_port = 6379


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_header('Content-type', 'text/html')
        self.end_headers()  

    def do_GET(self):
        if isQueryOkay(self.path):
            # Log query
            logging.info("GET ,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            print(self.path)
            # Get parametr
            self.send_response(200)
            self._set_response()
            qs = parse_qs(urlparse(self.path).query)
            jsonDump = json.dumps(qs)
            jsonLoad = json.loads(jsonDump)['id']
            idParameter = jsonLoad[0]



            # Get data from Redis
            r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
            getRedisData = r.get(idParameter)
            if not getRedisData:
                self.send_response(404)
                self._set_response()
            else:
                # Serializing json & print to web server
                dictionary ={} 
                dictionary[getRedisData] = getRedisData
                json_object = json.dumps(dictionary, indent = 4) 
                self.wfile.write(format(json_object).encode('utf-8'))
            
        else:
            self.send_response(404)
            self._set_response()

    def do_POST(self):
        if isQueryOkay(self.path):
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length) 
            logging.info("POST ,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                    str(self.path), str(self.headers), post_data.decode('utf-8'))
            self.send_response(200)
            self._set_response()

            # Send ID to Redis
            r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
            qs = parse_qs(urlparse(self.path).query)
            jsonDump = json.dumps(qs)
            jsonLoads = json.loads(jsonDump)['id']
            idParameter = jsonLoads[0]
            r.set(idParameter,idParameter)

            # Serializing json & print to web server
            dictionary ={} 
            dictionary[idParameter] = idParameter
            jsonObject = json.dumps(dictionary, indent = 4) 
            self.wfile.write(format(jsonObject).encode('utf-8'))
        else:
            self.send_response(404)
            self._set_response()

    def do_DELETE(self):
        if isQueryOkay(self.path):
            logging.info("DELETE request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            
            ## Get parametr
            self.send_response(200)
            self._set_response()
            qs = parse_qs(urlparse(self.path).query)

            # Delete ID in Redis
            jsonDump = json.dumps(qs)
            jsonLoad = json.loads(jsonDump)['id']
            idParameter = jsonLoad[0]
            r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

            # If ID not exists return 404
            getRedisData = r.get(idParameter)
            if not getRedisData:
                self.send_response(404)
                self._set_response()
            else:
                r.delete(idParameter)
                # Serializing json & print to web server
                dictionary ={} 
                dictionary[idParameter] = idParameter
                jsonObject = json.dumps(dictionary, indent = 4) 
                self.wfile.write(format(jsonObject).encode('utf-8'))
        else:
            self.send_response(404)
            self._set_response()

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting http server...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping http server...\n')

def isQueryOkay (query):
    if re.match(r"\/\?id=.*\S.*", query):
        return True
    else:   
        return False


if __name__ == '__main__':
    from sys import argv
    # Start metrics
    start_http_server(8000)

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
