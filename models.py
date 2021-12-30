from mongoengine import Document
from mongoengine import (
    IntField,
    StringField,
    ReferenceField,
    ListField,
)


class NFT:
    name = StringField()
    baseURI = StringField()

    def __repr__(self):
        return "%s : %s\n" % (self.name, self.baseURI)


class Members(Document):
    nfts = ListField(ReferenceField(NFT))
    guilds = ListField(IntField)

    def __repr__(self):
        return "%s : %s\n" % (str(self.nfts), str(self.guilds))


class Guild(Document):
    name = StringField()
    email = StringField()
    desc = StringField()
    creator = StringField()
    signature = StringField()
    members = ReferenceField(Members)

    def __repr__(self):
        return "%s : %s : %s : %s : %s : %s \n" % self.name, self.email, self.desc, self.creator, self.signature, self.members





