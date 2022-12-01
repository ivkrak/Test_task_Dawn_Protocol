from telethon.sync import TelegramClient
from crypt import api_keys

# test_url = 'https://t.me/pohod_irk'
api_id, api_hash = api_keys()
client = TelegramClient('name', api_id, api_hash)
client.start()

participants = client.get_participants('pohod_irk')
s = str(participants)
# print(participants)

try:
    [User(
        id=418704402,
        is_self=False,
        contact=True,
        mutual_contact=False,
        deleted=False,
        bot=False,
        bot_chat_history=False,
        bot_nochats=False,
        verified=False,
        restricted=False,
        min=False,
        bot_inline_geo=False,
        support=False,
        scam=False,
        apply_min_photo=True,
        fake=False,
        bot_attach_menu=False,
        premium=False,
        attach_menu_enabled=False,
        access_hash=-369047971591964061,
        first_name='Евгений Юрьевич',
        last_name='Александров',
        username=None,
        phone='79086603717',
        photo=UserProfilePhoto(
            photo_id=1798321713737476016,
            dc_id=2,
            has_video=False,
            stripped_thumb=b'\x01\x08\x08\x98\x18\xf7u\xe7\x1d(\xa2\x8a\x103'),
        status=UserStatusOffline(
            was_online=datetime.datetime(2022, 12, 1, 2, 57, 12, tzinfo=datetime.timezone.utc)
        ),
        bot_info_version=None,
        restriction_reason=[],
        bot_inline_placeholder=None,
        lang_code=None,
        emoji_status=None,
        usernames=[]
    )
    ]
except Exception as ex:
    print(ex)
    pass
