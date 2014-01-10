# Copyright (c) 2014 Martin Abente Lahaye. - martin.abente.lahaye@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

_index = {}
_data = {}
_current_id = 0


def upload(data, title, activity_id):
        global _index, _data, _current_id

        properties = {}
        properties['id'] = _current_id
        properties['title'] = title
        properties['activity_id'] = activity_id

        _index[_current_id] = properties
        _data[_current_id] = data

        _current_id += 1
        return (_current_id - 1)


def download(id):
    global _data
    return _data[id]


def delete(id):
    global _index, _data
    del _index[id]
    del _data[id]


def properties(id):
    global _index
    return _index.get(id, None)


def list():
    global _index
    _list = []
    for id, item in _index.items():
        _list.append(item)
    return _list
