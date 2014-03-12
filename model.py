# -*- coding: utf-8 -*-
from ORZ import OrzField, OrzBase, setup

class BeansFile(OrzBase):
    __orz_table__ = "beansfile"
    filename = OrzField()
    filehash = OrzField(as_key=OrzField.KeyType.ONLY_INDEX)
    uploadTime = OrzField()
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
