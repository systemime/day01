# -*- coding: utf-8 -*-
import random

from django.conf import settings

apps_labels = [app.split('.')[0] if not app.startswith('django')
               else app.split('.')[-1]
               for app in settings.INSTALLED_APPS]


class MasterSlaveDBRouter:
    """数据库主从读写分离路由"""

    read_db_labels = ('slave1_db', 'slave2_db')
    write_db_labels = 'master_db'

    def db_for_read(self, model, **hints):
        """读数据库 and 分库分表
        所有的读操作走从库
        """
        if model._meta.app_label in apps_labels:
            db = random.choice(self.read_db_labels)  # nosec
            return db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        允许迁移，db必须为master
        """
        # db.startswith(app_label) 返回app_label开头的数据库
        if app_label in apps_labels and db == 'master_db':
            return True
        return False

    def db_for_write(self, model, **hints):
        """写数据库
        写数据走master数据库
        """
        return self.write_db_labels

    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True


"""手动选择数据库
obj = models.Student.objects.using('deafult').get(pk=3)
"""
