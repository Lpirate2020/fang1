from django.db import models


# Create your models here.
class Area(models.Model):
    """
    省区划
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级⾏政区划')
    # self指自关联表，外键指向自身
    # on_delete=models.SET_NULL外键允许为空，因为省级没有父级
    # related_name隐式生成字段更改名字，原本应为area_set

    class Meta:

        db_table = 'tb_areas'
        verbose_name = '⾏政区划'
        verbose_name_plural = '⾏政区划'

    def __str__(self):

        return self.name
