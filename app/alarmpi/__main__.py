import logging
import os
import sys
import time
from datetime import datetime as dt

import click
import yaml
from feuersoftware import PublicAPI

from alarmparser import AlarmParser
from mailcheck import Mail

LOGLEVEL = "INFO"

format = "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s"
dateformat = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=LOGLEVEL, format=format, datefmt=dateformat)
LOGGER = logging.getLogger("AlarmPi")


class Observer:
    def __init__(self, config):
        self.config = config

    def run(self):
        while True:
            try:
                for account in self.config.get("accounts"):
                    self.check_mail(account)
            except KeyboardInterrupt:
                LOGGER.info("Ctrl + C received. Stopping now!")
                sys.exit(0)
            time.sleep(2)

    def check_mail(self, account):
        """Check a mail account for new alarm mails."""
        name = account.get("name")
        mailcfg = account.get("mail")
        mail = Mail(mailcfg.get("host"), mailcfg.get("user"), mailcfg.get("password"))
        msgids = mail.search_mails(mailcfg.get("subject"))
        text = mail.get_text(msgids)
        if not text:
            return
        data = AlarmParser(self.config, text).data
        alarmdata = self.assign_data(data)
        self.alert(account, alarmdata)

    def assign_data(self, data):
        """Assign data to right api fields, transform values if necessary."""
        alarmdata = {
            # "start": dt.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "start": f"{dt.now().strftime('%Y-%m-%d')}T{data.get('start')}:00",
            "keyword": data.get("keyword"),
            "number": data.get("number"),
            "address": f"{data.get('street')} {data.get('housenumber')}, {data.get('city')} - {data.get('district')}",
            "facts": data.get("comment"),
            "properties": [
                {"key": "Objekt", "value": data.get("object")},
                {"key": "Sondersignal", "value": data.get("siren")},
            ],
            "ric": data.get("assigned"),
        }
        return alarmdata

    def alert(self, account, alarmdata):
        """Send alarm data to Feuersoftware API."""
        api = PublicAPI(account.get("connect").get("token"))
        r = api.post_operation(
            start=alarmdata.get("start"),
            keyword=alarmdata.get("keyword"),
            status="new",
            alarmenabled=True,
            address=alarmdata.get("address"),
            facts=alarmdata.get("facts"),
            # number=alarmdata.get("number"),
            number="12121212",
            properties=alarmdata.get("properties"),
            ric=alarmdata.get("ric"),
        )


@click.command()
@click.argument("configfile", type=click.Path(exists=True))
def main(configfile):

    with open(configfile) as cfg:
        config = yaml.load(cfg, Loader=yaml.BaseLoader)

    if not config:
        LOGGER.error("No config file found at %s!", configfile)
        sys.exit(1)

    observer = Observer(config)
    observer.run()


if __name__ == "__main__":
    main()
