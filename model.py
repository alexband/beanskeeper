# -*- coding: utf-8 -*-
from ORZ import OrzField, OrzBase
from libs import beansdb as db

class BeansFile(OrzBase):
    __orz_table__ = "beansfile"
    filename = OrzField(as_key=OrzField.KeyType.DESC)
    filehash = OrzField(as_key=OrzField.KeyType.DESC)
    uploadTime = OrzField(as_key=OrzField.KeyType.DESC)
    mimetype = OrzField()

    @classmethod
    def add(cls, **kw):
        f = cls.create(**kw)
        return f

    @classmethod
    def get_by_filename(cls, name):
        pass

    @classmethod
    def get_by_filehash(cls, filehash):
        rs = cls.gets_by(filehash=filehash)
        return rs[0] if rs else None

    def content(self):
        return db.get(self.filehash, None)
