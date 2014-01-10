# Copyright (c) 2014 Martin Abente Lahaye. - tch@sugarlabs.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import logging

from sugar3 import util
from sugar3.graphics.palette import Palette
from jarabe.journal.volumestoolbar import BaseButton
from jarabe.journal.model import BaseResultSet

from jarabe.webservice import account
from jarabe.webservice import account, accountsmanager

SERVICE_MOUNT_POINT = 'WS_FAKECLOUD'

class Account(account.Account):

    def __init__(self):
        logging.debug('started FakeCloud service')
        self._service = accountsmanager.get_service('fakecloud')

    def get_token_state(self):
        return self.STATE_VALID

    def get_mount_point(self):
        return SERVICE_MOUNT_POINT

    def get_store(self):
        return FakeStore(self._service)

def _sugarize(file):
    return {'uid': _id_to_journal(file['id']),
            'title': file['title'],
            'timestamp': 0,
            'filesize': 0,
            'mime_type': '',
            'activity': '',
            'activity_id': file['activity_id'],
            'icon-color': '#000000,#ffffff',
            'description': '',
            'mountpoint': SERVICE_MOUNT_POINT}

def _id_to_journal(id):
    return SERVICE_MOUNT_POINT + str(id)

def _id_from_journal(object_id):
    return object_id.replace(SERVICE_MOUNT_POINT, '')

class FakeStore():

    def __init__(self, service):
        self._service = service

    def get_button(self):
        button = FakeButton()
        button.set_palette(Palette('FakeCloud'))
        return button

    def find(self, query, page_size):
        logging.debug('FakeCloud searching for %s', str(query))
        return FakeSet(query, page_size, self._service)

    def write(self, metadata, file_path):
        logging.debug('FakeCloud uploading new file')

        with open(file_path, 'r') as file:
            data = file.read()

        id = self._service.upload(data,
                                  str(metadata['title']),
                                  str(metadata['activity_id']))
        return _id_to_journal(id)

    def delete(self, object_id):
        logging.debug('FakeCloud deleting %s', object_id)
        id = _id_from_journal(object_id) 
        self._service.delete(int(id))

    def get_metadata(self, object_id):
        logging.debug('FakeCloud looking into %s', object_id)
        id = _id_from_journal(object_id)
        return _sugarize(self._service.properties(int(id)))

    def get_file(self, object_id):
        logging.debug('FakeCloud downloading %s', object_id)

        id = _id_from_journal(object_id)
        data = self._service.download(int(id))

        path = util.TempFilePath()
        with open(path, 'w') as file:
            file.write(data)
        return path

class FakeButton(BaseButton):

    def __init__(self):
        BaseButton.__init__(self, mount_point=SERVICE_MOUNT_POINT)
        self.props.icon_name = 'document-send'

class FakeSet(BaseResultSet):

    def __init__(self, query, page_size, service):
        BaseResultSet.__init__(self, query, page_size)
        self._service = service

    def find_ids(self, query):
        ids = []
        for file in self._service.list():
            ids.append(_id_to_journal(file['id']))
        return ids

    def find(self, query):
        files = self._service.list()
        entries = []
        for file in files:
            entry = _sugarize(file)
            logging.debug('FakeCloud returning %s', str(entry))
            entries.append(entry)
        return entries, len(entries)

def get_account():
    return Account()
