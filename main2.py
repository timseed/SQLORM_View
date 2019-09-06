from pprint import pprint
from db.Model import *
from db.Database import init_db
session = init_db()

u1 = User(name="Bob")
u2 = User(name="Fred")
ch1 = Channel(name="BBC")
ch2 = Channel(name="CNN")
ch3 = Channel(name="HKTV")
u1.channels.append(ch1)
u1.channels.append(ch2)
u2.channels.append(ch3)
session.add_all([u1, u2, ch1, ch2, ch3])
session.commit()


def show_res(q):
    # Show the columns created for the query
    pprint(q.column_descriptions)
    for rec in q.all():
        print(f"{rec.User.name} {rec.Channel.name} ")


p = session.query(User).first()
print(f"{p.name}")
for rec in session.query(Channel).all():
    print(f"{rec.name}")
#
# Check the Join table is there
#
for rec in session.query(UserChannel).all():
    print(f"{rec.user_id}   {rec.channel_id}")

# Query with no Join ... Bad result
q = Query([User, Channel, UserChannel], session=session)
pprint(q.count())

q = Query([User, Channel, UserChannel], session=session). \
    filter(User.user_id == UserChannel.user_id). \
    filter(Channel.channel_id == UserChannel.channel_id)
# Should be 3
pprint(q.count())

# Specify which fields
q = Query([User, Channel, UserChannel, User.name, Channel.name], session=session). \
    filter(User.user_id == UserChannel.user_id). \
    filter(Channel.channel_id == UserChannel.channel_id)
show_res(q)
