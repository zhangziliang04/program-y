"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import logging

class YLoggerSnapshot(object):

    def __init__(self, criticals=0, fatals=0, errors=0, exceptions=0, warnings=0, infos=0, debugs=0):
        self._criticals = criticals
        self._fatals = fatals
        self._errors = errors
        self._exceptions = exceptions
        self._warnings = warnings
        self._infos = infos
        self._debugs = debugs

    def __str__(self):
        return "Critical(%d) Fatal(%d) Error(%d) Exception(%d) Warning(%d) Info(%d), Debug(%d)" % (
            self._criticals, self._fatals, self._errors, self._exceptions, self._warnings, self._infos, self._debugs
        )


class YLogger(object):

    CRITICALS = 0
    FATALS = 0
    ERRORS = 0
    EXCEPTIONS = 0
    WARNINGS = 0
    INFOS = 0
    DEBUGS = 0

    @staticmethod
    def snapshot():
        return YLoggerSnapshot(YLogger.CRITICALS,
                               YLogger.FATALS,
                               YLogger.ERRORS,
                               YLogger.EXCEPTIONS,
                               YLogger.WARNINGS,
                               YLogger.INFOS,
                               YLogger.DEBUGS)

    @staticmethod
    def format_message(context, message):
        if context is None:
            return "[] [] [] [] [] - %s"%message
        return "[%s] - %s"%(str(context), message)

    @staticmethod
    def critical(context, message, *args, **kwargs):
        YLogger.CRITICALS += 1
        if logging.getLogger().isEnabledFor(logging.CRITICAL):
            logging.critical(YLogger.format_message(context, message), *args, **kwargs)

    @staticmethod
    def fatal(context, message, *args, **kwargs):
        YLogger.FATALS += 1
        if logging.getLogger().isEnabledFor(logging.FATAL):
            logging.fatal(YLogger.format_message(context, message), *args, **kwargs)

    @staticmethod
    def error(context, message, *args, **kwargs):
        YLogger.ERRORS += 1
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.error(YLogger.format_message(context, message), *args, **kwargs)

    @staticmethod
    def exception(context, message, *args, **kwargs):
        YLogger.EXCEPTIONS += 1
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.error(YLogger.format_message(context, message), *args, **kwargs)

    @staticmethod
    def warning(context, message, *args, **kwargs):
        YLogger.WARNINGS += 1
        if logging.getLogger().isEnabledFor(logging.WARNING):
            logging.warning(YLogger.format_message(context, message), *args, **kwargs)

    @staticmethod
    def info(context, message, *args, **kwargs):
        YLogger.INFOS += 1
        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info(YLogger.format_message(context, message), *args, **kwargs)

    @staticmethod
    def debug(context, message, *args, **kwargs):
        YLogger.DEBUGS += 1
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(YLogger.format_message(context, message), *args, **kwargs)


