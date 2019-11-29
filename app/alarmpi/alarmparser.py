import logging
import re
import quopri

LOGGER = logging.getLogger(__name__)


class AlarmParser:
    def __init__(self, config, msg):
        self.config = config
        self.msg = quopri.decodestring(msg.get_payload()).decode("utf-8")
        self._parse()

    def _parse(self):
        result = {}
        for item in self.config.get("parser"):
            var = item.get("var")
            regex = item.get("regex")
            split = item.get("split")
            r = re.search(regex, self.msg)
            if r:
                r = re.sub("\s{2,}", " ", r.group(1).strip())
                result[var] = r
        self.data = result
