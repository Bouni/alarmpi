import logging
import re
import quopri

LOGGER = logging.getLogger(__name__)


class AlarmParser:
    def __init__(self, config, msg):
        self.config = config
        self.msg = self.decode(msg.get_payload())
        self._parse()

    def decode(self, msg):
        for e in ["utf-8", "cp1252", "latin1"]:
            try:
                return quopri.decodestring(msg).decode(e)
            except UnicodeDecodeError:
                pass
        LOGGER.error("Failed to decode message with utf-8, cp1252 and latin1")
        return None


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
