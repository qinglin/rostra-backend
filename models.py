import mongoengine as me
from mongoengine import (
    IntField,
    StringField,
    ListField,
    EmbeddedDocumentField,
    UUIDField
)


class Nft(me.EmbeddedDocument):
    name = StringField()
    baseURI = StringField()

    def __repr__(self):
        return "%s : %s\n" % (self.name, self.baseURI)


class Requirements(me.EmbeddedDocument):
    nfts = ListField(EmbeddedDocumentField('Nft'))
    guilds = ListField(IntField())

    def __repr__(self):
        return "%s : %s\n" % (str(self.nfts), str(self.guilds))


class Guild(me.Document):
    guild_id = StringField()
    name = StringField()
    email = StringField()
    desc = StringField()
    creator = StringField()
    members = ListField(StringField())
    signature = StringField()
    requirements = EmbeddedDocumentField('Requirements')

    def __repr__(self):
        return "%s , %s , %s , %s , %s\n " % (self.guild_id, self.name, self.email, self.desc, self.creator)





