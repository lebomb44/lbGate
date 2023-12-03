#! /usr/bin/env python3
# coding: utf-8


""" LbGate main """


import http.server
import threading
import signal
import sys
import time
import json

import settings
import fct
import alarm
import move
import presence
import lbsms
import lbemail

class Monitoring(threading.Thread):
    """ Monitoring class """
    def __init__(self, name):
        self.is_loop_enabled = True
        threading.Thread.__init__(self, name=name)

    def run(self):
        """ Cyclic execution for polling on alarm, move and settings """
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
        """ Stop monitoring thread """
        fct.log("Stopping Monitoring thread...")
        self.is_loop_enabled = False
        time.sleep(1.0)


class CustomHandler(http.server.BaseHTTPRequestHandler):
    """ Custom HTTP handler """
    def ok200(self, resp, content_type='text/plain'):
        """ Return OK page """
        try:
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            if content_type == 'text/plain':
                self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())
            else:
                self.wfile.write((resp).encode())
            self.wfile.flush()
        except Exception as ex:
            fct.log_exception(ex)

    def error404(self, resp):
        """ Return page not found """
        try:
            self.send_response(404)
            self.end_headers()
            self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())
            self.wfile.flush()
        except Exception as ex:
            fct.log_exception(ex)

    def log_message(self, format, *args):
        """ Overwrite default log function """
        return

    def do_GET(self):
        """ Callback on HTTP GET request """
        url_tokens = self.path.split('/')
        url_tokens_len = len(url_tokens)
        #fct.log(str(url_tokens))
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
                                        alarm.enable()
                                        self.ok200("Alarm is enabled")
                                    elif url_tokens[4] == "disable":
                                        alarm.disable()
                                        self.ok200("Alarm is disabled")
                                    elif url_tokens[4] == "use_move":
                                        settings.alarm['use_move'] = True
                                        self.ok200("Use Move")
                                    elif url_tokens[4] == "nouse_move":
                                        settings.alarm['use_move'] = False
                                        self.ok200("Do not use move")
                                    else:
                                        try:
                                            token_nbs = range(5, url_tokens_len)
                                            node_point = settings.alarm
                                            for token_index in token_nbs:
                                                node_point = node_point[url_tokens[token_index]]
                                            self.ok200(json.dumps(node_point, sort_keys=True, indent=4), content_type="application/json")
                                        except:
                                            self.error404("Bad path in 'alarm'")
                                else:
                                    self.ok200("Alarm is = " + str(settings.alarm['is_enabled']) +
                                               "\nUseMove = " + str(settings.alarm['use_move']) +
                                               "\nTrigger = " + str(settings.alarm['triggered']) +
                                               "\nTimer = " + str(settings.alarm['timeout']) +
                                               "\nStop = " + str(settings.alarm['stopped']))
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
                                        self.ok200("Move is enabled = " + str(settings.move_is_enabled) + "\nMove = ")
                                else:
                                    self.ok200("Move is enabled = " + str(settings.move_is_enabled) + "\nMove = ")
                            elif url_tokens[3] == "node":
                                self.ok200(str(settings.node_list))
                            elif url_tokens[3] == "json":
                                try:
                                    token_nbs = range(4, url_tokens_len)
                                    node_point = settings.acq
                                    for token_index in token_nbs:
                                        node_point = node_point[url_tokens[token_index]]
                                    self.ok200(json.dumps(node_point, sort_keys=True, indent=4), content_type="application/json")
                                except:
                                    self.error404("Bad path in 'acq'")
                            elif url_tokens[3] == "sendsms":
                                if url_tokens_len > 4:
                                    self.ok200("Sending SMS: " + url_tokens[4])
                                    fct.send_sms(url_tokens[4])
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.ok200(settings.log_msg)
                    elif node == "rts":
                        if url_tokens_len > 3:
                            cmd = url_tokens[3]
                            if url_tokens_len > 4:
                                for token in url_tokens[4:]:
                                    cmd = cmd + " " + token
                            settings.rts.write(cmd)
                            self.ok200(node + " " + cmd)
                        else:
                            self.error404("No command for node: " + node)
                    elif node == "sms":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "sendto":
                                if url_tokens_len == 6:
                                    self.ok200("Sending SMS to " + url_tokens[4] + ": " + url_tokens[5])
                                    sms.sendto(url_tokens[4], url_tokens[5])
                                else:
                                    self.error404("Bad number of argment for command sms.sendto")
                            elif url_tokens[3] == "send":
                                if url_tokens_len == 5:
                                    self.ok200("Sending SMS to all : " + url_tokens[4])
                                    fct.send_sms(url_tokens[4])
                                else:
                                    self.error404("Bad number of argment for command fct.send_sms")
                            elif url_tokens[3] == "json":
                                try:
                                    self.ok200(json.dumps(sms.dict, sort_keys=True, indent=4), content_type="application/json")
                                except:
                                    self.error404("Bad json dump of 'sms' node")
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.error404("No command for node: " + node)
                    elif node == "email":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "sendto":
                                if url_tokens_len == 7:
                                    lbemail.sendto(url_tokens[4], url_tokens[5], url_tokens[6])
                                    self.ok200("Sending email to " + url_tokens[4] + ", Object: " + url_tokens[5] + ", Message: " + url_tokens[6])
                                else:
                                    self.error404("Bad number of argment for command lbemail.sendto")
                            elif url_tokens[3] == "send":
                                if url_tokens_len == 5:
                                    fct.send_email(url_tokens[4])
                                    self.ok200("Sending email to all : " + url_tokens[4])
                                else:
                                    self.error404("Bad number of argment for command fct.send_email")
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.error404("No command for node: " + node)
                    elif node == "alert":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "send":
                                if url_tokens_len == 5:
                                    self.ok200("Sending alert to all : " + url_tokens[4])
                                    fct.send_alert(url_tokens[4])
                                else:
                                    self.error404("Bad number of argment for command fct.send_alert")
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


presence = presence.Presence("Presence")
monitoring = Monitoring("Monitoring")
http2serial = http.server.ThreadingHTTPServer(("", settings.HTTPD_PORT), CustomHandler)

sms=lbsms.Sms("sms")
fct.sms = sms


def exit():
    """ Stop HTTP server, stop serial threads and monitoring thread """
    global http2serial
    global monitoring
    global presence
    fct.log("Stopping HTTP server")
    http2serial.server_close()
    for key_node, value_node in settings.node_list.items():
        value_node.stop()
    monitoring.stop()
    presence.stop()
    settings.rts.stop()
    sms.stop()
    settings.ups.stop()
    time.sleep(2.0)


def signal_term_handler(signal_, frame_):
    """ Capture Ctrl+C signal and exit program """
    fct.log('Got SIGTERM, exiting...')
    exit()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    #settings.ups.start()
    sms.start()
    settings.rts.start()
    presence.start()
    monitoring.start()
    for key, value in settings.node_list.items():
        value.start()
    fct.log("Serving at port " + str(settings.HTTPD_PORT))
    try:
        http2serial.serve_forever()
    except KeyboardInterrupt:
        exit()

