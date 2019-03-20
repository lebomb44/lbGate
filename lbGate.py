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

class Serial2Http(threading.Thread):
    def __init__(self, name):
        self.is_loop_enabled = True
        threading.Thread.__init__(self, name=name)

    def run(self):
        loop_nb = 1
        while self.is_loop_enabled is True:
            for node in settings.node_list:
                try:
                    if loop_nb % 100 == 0:
                        if settings.node_list[node]['fd'].isOpen() is False:
                            fct.log("Opening " + settings.node_list[node]['fd'].port)
                            # fct.log(node_list[node]['fd'].get_settings())
                            settings.node_list[node]['fd'].baudrate = 9600
                            settings.node_list[node]['fd'].open()
                            time.sleep(1.0)
                            settings.node_list[node]['fd'].close()
                            settings.node_list[node]['fd'].baudrate = 115200
                            settings.node_list[node]['fd'].open()
                            time.sleep(3.0)
                            settings.node_list[node]['fd'].reset_input_buffer()
                            settings.node_list[node]['fd'].reset_output_buffer()
                    if settings.node_list[node]['fd'].isOpen() is True:
                        line = ""
                        while settings.node_list[node]['fd'].inWaiting() > 0:
                            try:
                                cserial = settings.node_list[node]['fd'].read(1).decode("utf-8")
                                #if "kitchen" == node:
                                #    print(cserial, end='', flush=True)
                                if cserial == "\n":
                                    line = settings.node_list[node]['line'].rstrip()
                                    settings.node_list[node]['line'] = ""
                                    # fct.log("New line create=" + line)
                                    break
                                else:
                                    settings.node_list[node]['line'] = settings.node_list[node]['line'] + cserial
                            except Exception as ex:
                                settings.node_list[node]['line'] = ""
                                fct.log("ERROR while decoding data on " + settings.node_list[node]['fd'].port)
                                try:
                                    # OCM settings.node_list[node]['fd'].close()
                                    pass
                                except:
                                    pass
                        if line != "":
                            if line in settings.jeedom_url:
                                if settings.jeedom_url[line]['fct'] is not None:
                                    # fct.log("Serial CMD=" + line)
                                    settings.jeedom_url[line]['fct'](settings.jeedom_url[line]['url'])
                                    settings.node_list[node]['cmdRxCnt'] += 1
                                fct.timeout_reset(node, "0")
                            else:
                                line_array = line.split(" ")
                                if len(line_array) > 2:
                                    cmd = line_array[0]
                                    for token in line_array[1:-1]:
                                        cmd = cmd + " " + token
                                    if cmd in settings.jeedom_url:
                                        if settings.jeedom_url[cmd]['fct'] is not None:
                                            # fct.log("Serial CMD-1=" + line + " (" + cmd + ")")
                                            settings.jeedom_url[cmd]['fct'](settings.jeedom_url[cmd]['url'], line_array[-1])
                                            settings.node_list[node]['cmdRxCnt'] += 1
                                        fct.timeout_reset(node, "0")
                                    else:
                                        fct.log("ERROR: Serial CMD \"" + line + "\" or \"" + cmd + "\" not found !")
                                else:
                                    fct.log("ERROR: Serial CMD \"" + line + "\" not found and too short")
                        if loop_nb % 500 == 0:
                            # fct.write_serial(node, "ping get")
                            # OCM fct.log("PING to node " + node)
                            settings.node_list[node]['pingTxCnt'] += 1
                except Exception as ex:
                    fct.log("ERROR Exception: " + str(ex))
                    try:
                        settings.node_list[node]['fd'].close()
                    except Exception as ex:
                        fct.log("ERROR Exception: " + str(ex))
                fct.timeout_check(node)
            if loop_nb % 50 == 0:
                alarm.run()
                move.run()
                settings.run()
            loop_nb += 1
            if loop_nb >= 1000000:
                loop_nb = 0
            time.sleep(0.01)

    def stop(self):
        fct.log("Stopping serial2http thread...")
        self.is_loop_enabled = False
        time.sleep(2.0)
        fct.log("Closing all serial nodes...")
        for node in settings.node_list:
            try:
                if settings.node_list[node]['fd'].isOpen() is True:
                    settings.node_list[node]['fd'].close()
            except Exception as e:
                fct.log("ERROR Exception while closing " + settings.node_list[node]['port'] + " : " + str(e))


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
                            fct.write_serial(node, cmd)
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
                                        self.ok200("Alarm is enabled: " +
                                                   "<br/>" + "Contacts = " + str(settings.contact_status) +
                                                   "<br/>" + "Move = " + str(settings.move_status))
                                    elif url_tokens[4] == "disable":
                                        settings.alarm_is_enabled = False
                                        settings.alarm_triggered = False
                                        self.ok200("Alarm is disabled")
                                    else:
                                        self.ok200("Alarm is = " + str(settings.alarm_is_enabled) +
                                                   "<br/>Trigger = " + str(settings.alarm_triggered) +
                                                   "<br/>Timer = " + str(settings.alarm_timeout) +
                                                   "<br/>Contacts = " + str(settings.contact_status) +
                                                   "<br/>Move = " + str(settings.move_status))
                                else:
                                    self.ok200("Alarm is = " + str(settings.alarm_is_enabled) +
                                               "<br/>Trigger = " + str(settings.alarm_triggered) +
                                               "<br/>Timer = " + str(settings.alarm_timeout) +
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


serial2http = Serial2Http("Serial2Http")
http2serial = http.server.HTTPServer(("", settings.HTTPD_PORT), CustomHandler)


def signal_term_handler(signal_, frame_):
    global http2serial
    global serial2http
    fct.log('Got SIGTERM, exiting...')
    http2serial.server_close()
    global serial2http
    serial2http.stop()
    time.sleep(2.0)
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    serial2http.start()
    fct.log("Serving at port " + str(settings.HTTPD_PORT))
    try:
        http2serial.serve_forever()
    except KeyboardInterrupt:
        serial2http.stop()
    fct.log("Stopping HTTP server")
    http2serial.server_close()
