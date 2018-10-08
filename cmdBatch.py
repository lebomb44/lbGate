#!/usr/bin/python

                                    lineArray = line.split(" ")
                                    if 2 < len(lineArray):
                                        cmd = lineArray[0]
                                        for token in lineArray[1:-1]:
                                            cmd = cmd + " " + token
                                        if cmd in jeedomUrl:
                                            if "" != jeedomUrl[cmd]:
                                                log("Serial CMD-1=" + line + " (" + cmd + ")")
                                        else:
                                            log("ERROR: Serial CMD '" + line + "' (" + cmd + ") not found !")
                                    else:

