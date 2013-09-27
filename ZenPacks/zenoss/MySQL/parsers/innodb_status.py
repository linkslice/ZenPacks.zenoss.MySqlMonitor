import re

from Products.ZenRRD.CommandParser import CommandParser

deadlock_re = re.compile('\n-+\n(LATEST DETECTED DEADLOCK\n-+\n.*?\n)-+\n', re.M | re.DOTALL)

class InnodbStatus(CommandParser):
    def processResults(self, cmd, result):
        stats = cmd.result.output.splitlines()[1].split('\t')[-1].replace('\\n', '\n')
        deadlock_match = deadlock_re.search(stats)
        if deadlock_match:
            result.events.append({
                'severity': 3,
                'eventKey': 'innodb_deadlock',
                'summary': deadlock_match.group(1),
            })
        else:
            result.events.append({
                'severity': 0,
                'eventKey': 'innodb_deadlock',
                'summary': 'No last deadlock data',
            })

innodb_status = InnodbStatus # because zenoss is not happy with pep8
