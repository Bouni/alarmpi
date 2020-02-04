import email
import logging
import os
import ssl
import sys
from imaplib import IMAP4_SSL

LOGGER = logging.getLogger(__name__)


class Mail:
    """ search and download from IMAP server """

    def __init__(self, host, user, password, mailbox="INBOX"):
        self.host = host
        self.user = user
        self.password = password
        self._connect()
        self._login()
        self._select_mailbox(mailbox)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.imap:
            self.imap.close()
            self.imap.logout()

    def _connect(self):
        """ connect to IMAP server """
        try:
            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            self.imap = IMAP4_SSL(self.host, ssl_context=ssl_ctx)
            LOGGER.info("Successfully connected to IMAP server %s", self.host)
        except Exception as e:
            LOGGER.error("Mail connection error %s", e)
            sys.exit()

    def _login(self):
        """ login to email account """
        try:
            self.imap.login(self.user, self.password)
            LOGGER.info("Successfully logged in to IMAP server as %s", self.user)
        except Exception as e:
            LOGGER.error("Mail Login Error: %s", e)
            sys.exit()

    def _select_mailbox(self, mailbox="INBOX"):
        try:
            self.imap.select(mailbox)
            LOGGER.info("Successfully selected mailbox %s", mailbox)
        except Exception as e:
            LOGGER.error("Mail select mailbox Error: %s", e)
            sys.exit()

    def search_mails(self, subject, unseen=True):
        """ serach selected inbox for mails with a certain subject """
        if unseen:
            unseen = " UNSEEN"
        else:
            unseen = ""
        sort = "REVERSE DATE"
        charset = "UTF-8"
        search = f'(HEADER Subject "{subject}"{unseen})'
        status, data = self.imap.sort(sort, charset, search)
        if data[0]:
            LOGGER.info("%s neue E-Mails", len(data[0].split()))
            return data[0].split()
        LOGGER.info("Keine neuen E-Mails")
        return None

    def get_text(self, msgids):
        """Get body of an email"""
        if not msgids:
            return None
        content_types = ["text/html", "text/plain"]
        for msgid in msgids:
            status, data = self.imap.fetch(msgid, "(RFC822)")
            msg = email.message_from_string(data[0][1].decode("utf-8"))
            for part in msg.walk():
                if part.get_content_type() in content_types:
                    return part
