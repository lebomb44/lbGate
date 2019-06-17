#! /usr/bin/env python3
# coding: utf-8


""" LbGate main """


import http.server
import threading
import signal
import sys
import time

import settings
import fct
import alarm
import move

class Monitoring(threading.Thread):
    def __init__(self, name):
        self.is_loop_enabled = True
        threading.Thread.__init__(self, name=name)

    def run(self):
        loop_nb = 1
        while self.is_loop_enabled is True:
            #fct.log("DEBUG: Monitoring loop " + str(loop_nb))
            if loop_nb % 10 == 0:
                alarm.run()
                move.run()
                settings.run()
            loop_nb += 1
            if loop_nb >= 1000000:
                loop_nb = 0
            time.sleep(0.1)

    def stop(self):
        fct.log("Stopping Monitoring thread...")
        self.is_loop_enabled = False
        time.sleep(1.0)


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def ok200(self, resp):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())

    def error404(self, resp):
        self.send_response(404)
        self.end_headers()
        self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())

    def do_GET(self):
        url_tokens = self.path.split('/')
        url_tokens_len = len(url_tokens)
        fct.log(str(url_tokens))
        if url_tokens_len > 1:
            api = url_tokens[1]
            if api == "api":
                if url_tokens_len > 2:
                    node = url_tokens[2]
                    if node in settings.node_list:
                        if url_tokens_len > 3:
                            cmd = url_tokens[3]
                            if url_tokens_len > 4:
                                for token in url_tokens[4:]:
                                    cmd = cmd + " " + token
                            settings.node_list[node].write(cmd)
                            self.ok200(node + " " + cmd)
                        else:
                            self.error404("No command for node: " + node)
                    elif node == "lbgate":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "alarm":
                                if url_tokens_len > 4:
                                    if url_tokens[4] == "enable":
                                        settings.alarm_is_enabled = True
                                        settings.alarm_triggered = False
                                        settings.alarm_timeout = 0
                                        settings.alarm_stopped = False
                                        self.ok200("Alarm is enabled: " +
                                                   "<br/>" + "Contacts = " + str(settings.contact_status) +
                                                   "<br/>" + "Move = " + str(settings.move_status))
                                    elif url_tokens[4] == "disable":
                                        settings.alarm_is_enabled = False
                                        settings.alarm_triggered = False
                                        settings.alarm_timeout = 0
                                        settings.alarm_stopped = False
                                        self.ok200("Alarm is disabled")
                                    else:
                                        self.ok200("Alarm is = " + str(settings.alarm_is_enabled) +
                                                   "<br/>Trigger = " + str(settings.alarm_triggered) +
                                                   "<br/>Timer = " + str(settings.alarm_timeout) +
                                                   "<br/>Stop = " + str(settings.alarm_stopped) +
                                                   "<br/>Contacts = " + str(settings.contact_status) +
                                                   "<br/>Move = " + str(settings.move_status))
                                else:
                                    self.ok200("Alarm is = " + str(settings.alarm_is_enabled) +
                                               "<br/>Trigger = " + str(settings.alarm_triggered) +
                                               "<br/>Timer = " + str(settings.alarm_timeout) +
                                               "<br/>Stop = " + str(settings.alarm_stopped) +
                                               "<br/>Contacts = " + str(settings.contact_status) +
                                               "<br/>Move = " + str(settings.move_status))
                            elif url_tokens[3] == "presence":
                                if url_tokens_len > 4:
                                    if url_tokens[4] == "enable":
                                        settings.presence_is_enabled = True
                                        self.ok200("Presence is enabled")
                                    elif url_tokens[4] == "disable":
                                        settings.presence_is_enabled = False
                                        self.ok200("Presence is disabled")
                                    else:
                                        self.ok200("Presence is enabled = " + str(settings.presence_is_enabled))
                                else:
                                    self.ok200("Presence is enabled = " + str(settings.presence_is_enabled))
                            elif url_tokens[3] == "move":
                                if url_tokens_len > 4:
                                    if url_tokens[4] == "enable":
                                        settings.move_is_enabled = True
                                        self.ok200("Move is enabled")
                                    elif url_tokens[4] == "disable":
                                        settings.move_is_enabled = False
                                        self.ok200("Move is disabled")
                                    else:
                                        self.ok200("Move is enabled = " + str(settings.move_is_enabled) + "<br/>" + "Move = " + str(settings.move_status))
                                else:
                                    self.ok200("Move is enabled = " + str(settings.move_is_enabled) + "<br/>" + "Move = " + str(settings.move_status))
                            elif url_tokens[3] == "node":
                                self.ok200(str(settings.node_list))
                            elif url_tokens[3] == "sendsms":
                                if url_tokens_len > 4:
                                    self.ok200("Sending SMS: " + url_tokens[4])
                                    fct.send_sms(url_tokens[4])
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.error404("No command for node: " + node)
                    else:
                        self.error404("Bad node: " + node)
                else:
                    self.error404("Command too short: " + api)
            else:
                self.error404("Bad location: " + api)
        else:
            self.error404("Url too short")


monitoring = Monitoring("Monitoring")
http2serial = http.server.HTTPServer(("", settings.HTTPD_PORT), CustomHandler)


def exit():
    global http2serial
    global monitoring
    fct.log("Stopping HTTP server")
    http2serial.server_close()
    for key, value in settings.node_list.items():
        value.stop()
    monitoring.stop()
    time.sleep(2.0)


def signal_term_handler(signal_, frame_):
    fct.log('Got SIGTERM, exiting...')
    exit()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    monitoring.start()
    for key, value in settings.node_list.items():
        value.start()
    fct.log("Serving at port " + str(settings.HTTPD_PORT))
    try:
        http2serial.serve_forever()
    except KeyboardInterrupt:
        exit()

