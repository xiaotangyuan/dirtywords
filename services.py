import hashlib
import datetime
from models import Member, WordLib, db


def md5(astring):
    return hashlib.md5(astring.encode('utf-8')).hexdigest()

def gen_useropenid(email):
    basekeystring = 'dirtywordschecker'
    concatstring = basekeystring+email
    return md5(concatstring)


class MemberService:

    def get_password_md5(self, password):
        return md5(password)

    def create(self, email, password):
        password = self.get_password_md5(password)
        openid = gen_useropenid(email)
        # print(password, openid)
        member = Member(email=email, password=password, openid=openid, created_date=datetime.datetime.utcnow())
        db.session.add(member)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()
    ms = MemberService()
    email = 'yt.luo@idiaoyan.com'
    password = '123456'
    ms.create(email, password)