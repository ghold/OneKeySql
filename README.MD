##__介绍__
------
OneKey定位为测试数据管理工具，目前支持数据模板（基于Oracle）制作和测试数据执行（模拟Oracle数据库的INSERT操作）

工具采用标签替代方式实现数据模板重用，支持默认数据一键与动态测试数据生成

OneKeyCli功能还支持通过命令行调用测试数据生成业务场景

__工具适用于多INSERT操作业务流系统的测试数据维护__
  
  
##__数据模板制作__
---------
![1st](http://ghold.net/wblog/wp-content/gallery/onekey/1.jpg?i=1124206133 "1st")

1.进入测试用例模块  
2.加号新增用例模板

![2nd](http://ghold.net/wblog/wp-content/gallery/onekey/2.jpg?i=1243912460 "2nd")


3.填写模板标题，分类，描述  
4.交叉取消新增，加号完成新增

![3rd](http://ghold.net/wblog/wp-content/gallery/onekey/3.jpg?i=774910141 "3rd")

5.完成新增后开始对模板添加步骤。双击刚新增的标题，进入模板编辑模式；单击为浏览模式

![4th](http://ghold.net/wblog/wp-content/gallery/onekey/4.jpg?i=799540066 "4th")

6.拖动单元块进中间列表，打开单元标签编辑

![5th](http://ghold.net/wblog/wp-content/gallery/onekey/5.jpg?i=1395581011 "5th")

7.这里的编辑功能简单来说就是给单元中标签给个名字（暂时只支持英文）和给个值。最后点击保存，保存单元步骤，退出单元标签编辑界面

__重复6和7__

![6th](http://ghold.net/wblog/wp-content/gallery/onekey/6.jpg?i=84593088 "6th")

8.在模板编辑模式下可以拖动选择的标题或最后一步单元块进行删除模板或单元步骤  
9.双击模板标题结束模板编辑模式


##__用例执行__
------

![7th](http://ghold.net/wblog/wp-content/gallery/onekey/7.jpg?i=9796836 "7th")

1.进入测试执行模块  
2.单击测试用例标题，查看描述  
3.点击右侧箭头，进入测试执行界面

![8th](http://ghold.net/wblog/wp-content/gallery/onekey/8.jpg?i=1406273068 "8th")

4.填写参数，如果有默认参数是目标参数，可以忽略这一步
5.点击执行运行用例

__在执行路径下会生成日志__


##__配置__
------

1.  环境变量需要添加ONEKEY_HOME，并把测试用例testcase.xml、测试单元testunit.xml、自增参数初始化config.conf文件放在ONEKEY_HOME路径下
2.  自增参数初始化文件config.conf中添加自增的字段如id，number之类的初始化值



> Written with [StackEdit](https://stackedit.io/).