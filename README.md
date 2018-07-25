# 题目说明

网站采用 Django 框架编写，并使用 Gunicorn 部署。后端数据库为 MySQL。

项目文件结构如下：

```
deploy
├── docker-compose.yml
├── Dockerfile
├── init_sshop.sh
├── requirement.pip
├── sshop.template
└── www
    ├── gunicorn.conf.py
    ├── manage.py
    ├── set_admin.py
    ├── set_database.py
    ├── set_flag.py
    ├── sshop
    │   ├── admin.py
    │   ├── apps.py
    │   ├── captcha
    │   │   ├── ans
    │   │   │   ├── ans0_1_1525969416786.txt
    │   │   │   ├── ...
    │   │   │   └── ans99_1_1525970610284.txt
    │   │   └── jpgs
    │   │       ├── ques0_1_1525969416786.jpg
    │   │       ├── ...
    │   │       └── ques99_1_1525970610284.jpg
    │   ├── forms.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── static
    │   │   ├── admin
    │   │   │   ├── css
    │   │   │   │   ├── autocomplete.css
    │   │   │   │   ├── ...
    │   │   │   │   ├── rtl.css
    │   │   │   │   ├── vendor
    │   │   │   │   │   └── select2
    │   │   │   │   │       ├── LICENSE-SELECT2.md
    │   │   │   │   │       ├── select2.css
    │   │   │   │   │       └── select2.min.css
    │   │   │   │   └── widgets.css
    │   │   │   ├── fonts
    │   │   │   │   ├── LICENSE.txt
    │   │   │   │   ├── ...
    │   │   │   │   └── Roboto-Regular-webfont.woff
    │   │   │   ├── img
    │   │   │   │   ├── calendar-icons.svg
    │   │   │   │   ├── gis
    │   │   │   │   │   ├── move_vertex_off.svg
    │   │   │   │   │   └── move_vertex_on.svg
    │   │   │   │   ├── icon-addlink.svg
    │   │   │   │   ├── ...
    │   │   │   │   └── tooltag-arrowright.svg
    │   │   │   └── js
    │   │   │       ├── actions.js
    │   │   │       ├── actions.min.js
    │   │   │       ├── admin
    │   │   │       │   ├── DateTimeShortcuts.js
    │   │   │       │   └── RelatedObjectLookups.js
    │   │   │       ├── autocomplete.js
    │   │   │       ├── ...
    │   │   │       ├── urlify.js
    │   │   │       └── vendor
    │   │   │           ├── jquery
    │   │   │           │   ├── jquery.js
    │   │   │           │   ├── jquery.min.js
    │   │   │           │   └── LICENSE-JQUERY.txt
    │   │   │           ├── select2
    │   │   │           │   ├── i18n
    │   │   │           │   │   ├── ar.js
    │   │   │           │   │   ├── ...
    │   │   │           │   │   └── zh-TW.js
    │   │   │           │   ├── LICENSE-SELECT2.md
    │   │   │           │   ├── select2.full.js
    │   │   │           │   └── select2.full.min.js
    │   │   │           └── xregexp
    │   │   │               ├── LICENSE-XREGEXP.txt
    │   │   │               ├── xregexp.js
    │   │   │               └── xregexp.min.js
    │   │   ├── css
    │   │   │   ├── bootstrap.css
    │   │   │   ├── ...
    │   │   │   └── jumbotron-narrow.css
    │   │   ├── fonts
    │   │   │   ├── glyphicons-halflings-regular.eot
    │   │   │   ├── ...
    │   │   │   └── glyphicons-halflings-regular.woff2
    │   │   └── js
    │   │       ├── bootstrap.js
    │   │       ├── ...
    │   │       └── npm.js
    │   ├── templates
    │   │   ├── captcha.html
    │   │   ├── change.html
    │   │   ├── index.html
    │   │   ├── info.html
    │   │   ├── layout.html
    │   │   ├── login.html
    │   │   ├── register.html
    │   │   ├── reset.html
    │   │   ├── seckill.html
    │   │   ├── shopcar.html
    │   │   └── user.html
    │   ├── urls.py
    │   └── views.py
    └── www
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

26 directories, 573 files
```

## 1. 部署过程

`deploy/docker-compose.yml` 中定义初始 Flag

`deploy/docker-compose.yml` 中定义后端数据库密码

`deploy/www/www/settings.py` 中定义网站管理员用户名、初始积分、邀请奖励、商品价格区间（可选）

### 1.1 验证码数据集

由于附件中的验证码数据集容量过大，`deploy/www/sshop/captcha` 中的为模板中的部分数据，部署前可将其中的文件替换为附件中的验证码数据集。

### 1.2 部署指令

在 `deploy` 目录下运行以下命令即可部署上线：

```
docker-compose up -d
```

## 2. Flag 更新

Flag 存储于后端数据库中，`docker-compose.yml` 中内置的初始 Flag 为 `CISCN{this_is_a_sample_flag}`，更新时在 Docker 内部运行以下命令即可：

```
python3 /home/ciscn/set_flag.py "CISCN{xxxxxxxflag}"
```

## 3. Hints

1. when you are admin, you could pay faster.
2. django also troubled by format string.
3. the treasure is in mysql
