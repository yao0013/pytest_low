# -*- coding: utf-8 -*-
import time
from core.message_notify import MsgNotify
from core.logs import log


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = len(terminalreporter.stats.get('passed') or [])
    failed = len(terminalreporter.stats.get('failed') or [])
    xfailed = len(terminalreporter.stats.get('xfailed') or [])
    skipped = len(terminalreporter.stats.get('skipped') or [])
    duration = int(time.time() - terminalreporter._sessionstarttime)
    log.info('passed amount: {}'.format(passed))
    log.info('failed amount: {}'.format(failed))
    log.info('xfailed amount: {}'.format(xfailed))
    log.info('skipped amount: {}'.format(skipped))
    log.info('duration: {} seconds'.format(duration))
    report_info = {
        "count": passed + failed + xfailed + skipped,
        "passed": passed,
        "failed": failed,
        "xfailed": xfailed,
        "skipped": skipped,
        "duration": duration
    }
    log.info('set testreport to MsgNotify')
    MsgNotify().set_testresult(**report_info)

