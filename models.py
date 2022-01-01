import mongoengine as me
from mongoengine import (
    IntField,
    StringField,
    ListField,
    EmbeddedDocumentField
)


class Nft(me.EmbeddedDocument):
    name = StringField()
    baseURI = StringField()

    def __repr__(self):
        return "%s : %s\n" % (self.name, self.baseURI)


class Members(me.EmbeddedDocument):
    nfts = ListField(EmbeddedDocumentField('Nft'))
    guilds = ListField(IntField())

    def __repr__(self):
        return "%s : %s\n" % (str(self.nfts), str(self.guilds))


class Guild(me.Document):
    guild_id = IntField()
    name = StringField()
    email = StringField()
    desc = StringField()
    creator = StringField()
    wallet_address = StringField()
    signature = StringField()
    members = EmbeddedDocumentField('Members')

    def __repr__(self):
        return "%s : %s : %s : %s : %s : %s : %s \n" % self.guild_id, self.name, self.email, self.desc, self.creator, self.signature, self.members




