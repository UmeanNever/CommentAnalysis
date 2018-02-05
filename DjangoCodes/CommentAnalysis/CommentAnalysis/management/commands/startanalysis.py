# -*- coding: utf-8 -*-

import json

from django.core.management.base import BaseCommand
from django.conf import settings
import socket
from analysis.core import AnalysisCore

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        port = 8888
        analyzer = AnalysisCore()
        # Init
        analysis_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        analysis_server.bind(('127.0.0.1', port))
        analysis_server.listen(1)

        print("Analysis Server: listening to port {0}".format(port))
        while True:
            connection, client_addr = analysis_server.accept()
            try:
                raw_message = connection.recv(256)
                print("raw message:{0}".format(raw_message))
            except socket.error:
                print("Socket Error")
                connection.close()
            try:
                message = str(raw_message).decode("utf-8").strip()
            except:
                print("Decode Error")
                connection.send(json.dumps('Error'))
                continue
            if not message:
                connection.send(json.dumps('Error'))
                continue
            if message.lower() == 'ping':
                connection.send(json.dumps('Analysis Server listening'))
                continue
            connection.send(analyzer.analysis(message))
            # analyze
