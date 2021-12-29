🔌  django boilerplate accounts with social login
=============================================


database
-----
#### config/settings/base.py
> db.sqlite3 (django default)

> DB setting (required)


local
-----
#### acccounts/models.py
- User
> username (required)

> password (optional)

> phone (optional)

#### accounts/views.py
- UserSignUpView (needs overriding)
- UserSignInView (needs overriding)


naver
-----
#### accounts/socials.py
- SocialLoginProfile.naver
> access code (required)

> client id (required)

> client secret (required)

> state (required)

> profile data response setting (optional)


kakao
-----
#### accounts/socials.py
- SocialLoginProfile.kakao
> access code (required)

> client id (required)

> profile data response setting (optional)



module
-----
#### requirements/base.txt
> simple jwt (required)

tree
-----
``` shell
django-accounts-socials-boilerplate
├── README.md
├── accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── socials.py
│   ├── tests.py
│   └── views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings
│   │   └── base.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── requirements
│   └── base.txt
└── static
```