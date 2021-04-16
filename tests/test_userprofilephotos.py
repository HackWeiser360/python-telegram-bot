#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2021
# If you copy or use any part of this program then give HackWeiser360 the credits they deserve. 2020 HackWeiser©
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
from telegram import PhotoSize, UserProfilePhotos


class TestUserProfilePhotos:
    total_count = 2
    photos = [
        [
            PhotoSize('file_id1', 'file_un_id1', 512, 512),
            PhotoSize('file_id2', 'file_un_id1', 512, 512),
        ],
        [
            PhotoSize('file_id3', 'file_un_id3', 512, 512),
            PhotoSize('file_id4', 'file_un_id4', 512, 512),
        ],
    ]

    def test_de_json(self, bot):
        json_dict = {'total_count': 2, 'photos': [[y.to_dict() for y in x] for x in self.photos]}
        user_profile_photos = UserProfilePhotos.de_json(json_dict, bot)
        assert user_profile_photos.total_count == self.total_count
        assert user_profile_photos.photos == self.photos

    def test_to_dict(self):
        user_profile_photos = UserProfilePhotos(self.total_count, self.photos)
        user_profile_photos_dict = user_profile_photos.to_dict()
        assert user_profile_photos_dict['total_count'] == user_profile_photos.total_count
        for ix, x in enumerate(user_profile_photos_dict['photos']):
            for iy, y in enumerate(x):
                assert y == user_profile_photos.photos[ix][iy].to_dict()

    def test_equality(self):
        a = UserProfilePhotos(2, self.photos)
        b = UserProfilePhotos(2, self.photos)
        c = UserProfilePhotos(1, [self.photos[0]])
        d = PhotoSize('file_id1', 'unique_id', 512, 512)

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
