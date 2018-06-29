# 题目说明

网站采用 Django 框架编写，并使用 Gunicorn 部署。后端数据库为 MySQL。

项目文件结构如下：

```
deploy
├── docker-compose.yml
├── Dockerfile
├── mysql_init.sh
├── nginx.conf
├── requirement.pip
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
    │   │   ├── 0h_y0u_f1n411y_g0t_m3.lst
    │   │   ├── css
    │   │   │   ├── bootstrap.css
    │   │   │   ├── ...
    │   │   │   └── jumbotron-narrow.css
    │   │   ├── fonts
    │   │   │   ├── glyphicons-halflings-regular.eot
    │   │   │   ├── ...
    │   │   │   └── glyphicons-halflings-regular.woff2
    │   │   ├── js
    │   │   │   ├── bootstrap.js
    │   │   │   ├── ...
    │   │   │   └── npm.js
    │   │   └── www.bak
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
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    └── www
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

`exploit` 使用方式：

```
python run.py 1.2.3.4 80 csrfmiddlewaretoken
```

## 1. 部署过程

`deploy/Dockerfile` 中定义后端数据库账户密码、初始 Flag

`deploy/www/www/settings.py` 中定义网站管理员账户（不建议更改）、初始积分、邀请奖励、商品价格区间

### 1.1 验证码数据集

由于附件中的验证码数据集容量过大，`deploy/www/sshop/captcha` 中的为模板中的部分数据，部署前可将其中的文件替换为附件中的验证码数据集。

### 1.2 部署指令

在 `deploy` 目录下运行以下命令即可部署上线：

```
docker-compose up -d
```

## 2. Flag 更新

Flag 存储于后端数据库中，`Dockerfile` 中内置的初始 Flag 为 `CISCN{this_is_a_sample_flag}`，更新时在 Docker 内部运行以下命令即可：

```
python /app/www/set_flag.py "CISCN{xxxxxxxflag}"
```

## 3. Hints

1. the admin always forgets his account, so he make the recovery process easier.
2. maybe you could pay faster.
3. you should try django's hasher.
