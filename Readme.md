# 接口自动化使用说明：

# 功能说明

## 按照流程图执行测试用例

## 变量替换功能

1. 实现用例中的变量替换，变量使用{}括号表示，变量名要求{字母、数字和下划线}
2. 变量作用域：初始化sheet中的变量整个测试周期内有效，单个测试sheet中的变量在当前测试sheet有效
   1. 接口变量：接口变量只能从接口响应中获取，在每个接口用例中（包括初始化和恢复用例）设置interface_var（单个用例的初始化和恢复用例需在json中编辑interface_var字段，格式和普通用例的一样
   2. 用例变量：用例变量设置用于事前定义好需要使用的变量名和变量值，格式使用json，在具体用例的用例变量列添加，格式和接口变量的一样，用例变量只支持在Excel表格的用例变量列设置，不支持在单个用例的初始化和恢复用例中设置，因为用例变量的作用域是整个测试sheet，并且用例开始前，会先进行用例变量的置换
   3. 接口变量和用例变量作用域都是测试sheet
3. 变量随机添加字符串：在变量的后面随机添加8位随机字符串，格式："$变量名$"

## 用例执行顺序功能

1. 用例顺序：
   1. 规定初始化sheet中的用例>测试任务sheet >恢复数据sheet的用例
   2. 每个sheet中的用例，设置了顺序的用例>未设置顺序的用例
   3. 设置了顺序的用例数值越小优先级越高

## 测试报告展示

1. 报告展示：allure报告默认生成在工程目录的reports/{当时的时间}目录中，Excel报告默认生成在工程目录的reports/Excel目录中，以日期作为文件名

   1. 从工程目录的tools_pkg目录中复制allure-commandline-2.13.8.zip文件到任意地方，解压文件，将解压后的bin目录路径添加到环境变量中，即可以生成allure的测试报告，如下图所示![1619148945483](C:\Users\leo\AppData\Roaming\Typora\typora-user-images\1619148945483.png)

   2. 重新打开一个终端，找到对应的测试报告的目录（测试报告位于工程目录的reports目录下，默认每次执行的allure报告放在执行时对应的日期目录内，目前生成网页版的测试报告还需要手动在终端中输入命令行，具体命令行如下

      ```shell
      allure generate ./2021-04-16_16-08-27 -o results -c
      # 命令解释： allure generate 固定格式，生成本地可查看的报告  ./2021-04-16_16-08-27 allure默认生成的json文件所在目录  -o results 指定生成的html报告存放的位置   -c 生成前清空之前的报告
      ```

      ![1619149514512](C:\Users\leo\AppData\Roaming\Typora\typora-user-images\1619149514512.png)

      

      ```shell
      allure serve  # 此命令可以生成远程可访问的html页面 可以加入-h -p等参数配置host和port
      ```

      ![1619149591041](C:\Users\leo\AppData\Roaming\Typora\typora-user-images\1619149591041.png)



## 旧平台用例转换功能

1. 旧平台用例转换功能，在执行main.py文件时，传入命令行参数-t old 即代表运行旧平台用例转换，默认转换后的用例存放在工程目录下的testcase中，命名规则为：new_旧用例名字.xls

   **使用步骤**：

   1. 从 **云ERP个性化应用测试平台 v1.0** 平台导出相关的测试用例

   2. 运行main.py文件时，使用参数-f 需要转换的excel文件路径（使用相对路径和绝对路径均可） -t old

      ```shell
      python main.py -f ./testcase/test_case_ECS_gcloud8.0_1618988860581.xls -t old
      # 说明：-f 需要处理的Excel文件，-t new：直接执行新写的用例，old：转换旧平台的用例
      ```

   3. 运行完后，终端会提示新文件的存放路径

   4. 用例转换后，还需要手动添加一些基本的配置内容：
      1. 全局变量：目前旧平台的全局变量配置是在服务器上的配置文件中读取的，导出的测试用例中没有对应的值，需要手动修改添加
      2. 基础配置：目前旧平台的hostname是在后台中配置的，在测试用例中无法获取，需要手动在对应的地方配置即可
      3. 请求头：目前请求头默认配置的是：content-type:'application/x-www-form-urlencoded; charset=UTF-8'和X-Auth-Token：{token}，其中token是接口变量，需要再另外配置接口进行获取
      
   5. 配置完成后，即可和正常执行用例一样进行测试



## 数据库查看验证功能

1. 数据库验证功能，接口测试时，可以通过在用例中配置数据验证，填入对应的sql信息，就可以进行数据查询验证功能，目前仅支持mysql数据库查询

   **使用步骤**

   1. 在基础配置中配置数据库信息

      1. 配置项中输入database

      2. 配置值中填入类似以下的字段，需要符合json语法：

         ```json
         {
             "db1":  # 定义数据库的名称，后面在用例中填具体的查询时，需要填入这里对应的数据库名称
             	{"type": "mysql",  # 数据库的类型，考虑后续可能会使用sqlserver、redis、mongo								等数据库
                  "ip": "192.168.203.38",  # 连接数据的ip地址
                  "user": "root",  # 连接数据库的用户名
                  "pwd": "Kd1mwoeX5v65pf3cQzSFbLRZl9SxRoNzgsZHhdqR",  # 连接数据的密码
                  "port": "3306" # 连接数据的端口号
                 },
         	"db2":  # 定义数据库的名称，后面在用例中填具体的查询时，需要填入这里对应的数据库名称
             	{"type": "redis",  # 数据库的类型，考虑后续可能会使用sqlserver、redis、mongo								等数据库
                  "ip": "192.168.203.38",  # 连接数据的ip地址
                  "user": "root",  # 连接数据库的用户名
                  "pwd": "Kd1mwoeX5v65pf3cQzSFbLRZl9SxRoNzgsZHhdqR",  # 连接数据的密码
                  "port": "6379" # 连接数据的端口号
                 }
         }
         ```

   2. 在具体的测试用例中，填写相关的sql信息，具体举例如下：输入的内容需要符合json语法

      ```json
      {
      	"sql1":  # sql名字，方便查看，名字可以随意起
          	{"sql": "select * from cmp.cmp_config", # 需要执行的sql语句
               "db": "db1", # 在基础配置中配置的数据库名字
               "check": # 需要验证的内容
               	{"code": "cmp.monitorgcloud.router.host", # 前面是查询结果中包含的键名，后面			# 是预期值，这里表示查询结果中的code是否于"cmp.monitorgcloud.router.host"
                   "value": "192.168.203.38:9090"
                  }, 
               "type":"=" # 验证的类型，支持以下选项：如果不填的话，默认是=
      					# =或者== 表示预期值要和查询结果相关，如果查询结果有多条，默认选第一条进行					# 较比
      					# !或者!= 表示查询值不等于预期值，如果查询结果有多条，默认取第一条进行比较
      					# ~或者~= 表示预期值是否包含在查询值中，主要用于查询结果有多条时做比较
      					# !~或者~! 表示预期值不能包含在查询值中，主要用于查询结果有多条时做比较
              },
      	"sql2": # 第二条查询信息
          	{"sql": "select * from cmp.cmp_config", 
               "db": "db1", 
               "check":
               	{"name": "monitor"},
               "type": "~"
              }
      }
      ```



## 动态参数功能

1. 动态参数功能：支持通过查询数据库的方式定义变量

   **使用方式**

   1. 参考功能8在基础配置中配置数据参数

   2. 在测试用例的动态参数dyparam列中输入查询和变量定义信息，具体举例如下：

      ```json
      {
      	"sql1": # sql名字，方便查看，名字可以随意起
          	{"sql": "select * from cmp.cmp_config",  # 需要执行的sql语句
               "db": "db1", # 在基础配置中配置的数据库名字
               "values":  # 需要定义的变量信息
               	{"code_value": "code",  # code_value：需要定义的变量名，定义后，可以在当前用									# 例和后续执行的用例中使用{code_value} 获取到对应的值
          								# code：表示从数据库中查询出来的字段名，获取该字段名的									  # 值
                   "value_value": "value" # 同一条查询语句的第二个变量定义，含义和上述第一条一样
                  }
              },
      	"sql2": # 第二条查询信息，含义和上述sql1一样
          	{"sql": "select * from cmp.cmp_user", 
               "db": "db1", 
               "values": 
               	{"user_id_mysql": "user_id"
                  }
              }
      }
      ```

      



# 版本说明

### 2021-04-29

新增功能：

1. 新增测试结果邮件发送和钉钉群消息发送
2. allure测试报告中增加用例测试结果趋势图



调整：

1. 测试结果存放位置调整，保存测试结果时，以测试用例名为目录名字，保存allure测试报告和Excel报告
2. 自动生成allure html报告，并在执行机端生成对应的报告服务，通过邮件和钉钉群消息通知

### 2021-04-27

新增功能：

1. 数据库验证功能，接口测试时，可以通过在用例中配置数据验证，填入对应的sql信息，就可以进行数据库查询验证功能，具体内容可查看实现功能第8条
2. 动态参数dyparam功能实现，接口测试时，可以在用例中配置对应的信息，定义从数据库中获取的数值赋值给某个变量，具体使用查看实现功能的第9条



调整内容：

1. 调整Excel测试用例的位置，把数据库校验列的value列删除和把数据库列删除，使用json格式填写数据查询信息
2. 调整具体测试任务的日志存放的目录，采用当天的日志存放在以当天日期为目录的文件夹中，方便查看

### 2021-04-25:

新增功能：

1. 旧平台用例兼容功能：

   旧平台用例转换功能，在执行main.py文件时，传入命令行参数-t old 即代表运行旧平台用例转换，默认转换后的用例存放在工程目录下的testcase中，命名规则为：new_旧用例名字.xls

   **使用步骤**：

   1. 从 **云ERP个性化应用测试平台 v1.0** 平台导出相关的测试用例

   2. 运行main.py文件时，使用参数-f 需要转换的excel文件路径（使用相对路径和绝对路径均可） -t old

      ```shell
      python main.py -f ./testcase/test_case_ECS_gcloud8.0_1618988860581.xls -t old
      # 说明：-f 需要处理的Excel文件，-t new：直接执行新写的用例，old：转换旧平台的用例
      ```

   3. 运行完后，终端会提示新文件的存放路径
   4. 用例转换后，还需要手动添加一些基本的配置内容：
      1. 全局变量：目前旧平台的全局变量配置是在服务器上的配置文件中读取的，导出的测试用例中没有对应的值，需要手动修改添加
      2. 基础配置：目前旧平台的hostname是在后台中配置的，在测试用例中无法获取，需要手动在对应的地方配置即可
      3. 请求头：目前请求头默认配置的是：content-type:'application/x-www-form-urlencoded; charset=UTF-8'和X-Auth-Token：{token}，其中token是接口变量，需要再另外配置接口进行获取
   5. 配置完成后，即可和正常执行用例一样进行测试

调整的内容：

1. 自动生成的测试脚本存放路径调整到工程目录下 testcase/auto_create目录中
2. main.py文件的运行方式调整：需要处理的Excel文件需要通过命令行参数-f的形式入参，需要执行的功能通过-t参数，new代表新用例，可执行进行接口测试，old代表对旧平台的用例进行转换
3. core.base.Process增强对数据初始化sheet、数据恢复sheet、全局变量sheet、基础配置sheet的容错处理
4. 调整用例模板的部分生成顺序和位置
5. 提取Excel处理类到公共模块中
6. 其他部分新发现的问题修复

### 2021-04-21:

新增功能：

1. 日期解析：引用的格式为<#d日期参数>
   1. now()：表示当前时间（使用yyyy-MM-dd HH:mm:ss格式）
   2. yyyy-MM-dd HH:mm:ss形式的字符串：表示某个日期
   3. now()+N形式的表达式：表示在当前时间的基础上加上具体的分钟数
   4. yyyy-MM-dd HH:mm:ss+N形式的表达式：表示在某个日期的基础上加上具体的分钟数

### 2021-04-20：

新增功能：

1. 增加用例变量，主要解决测试用例需要一些基本的变量提供后续操作时使用，使用方式：

   1. 在原有的Excel表格增加了用例变量列，变量的定义仍然采用json的格式，测试sheet中定义的用例变量，在整个测试sheet中生效，引用声明的变量方式仍然使用："{变量名}"
   2. 举例：定义用例变量：{"namespace": "autotestnamespace", "pv_name": "autotestpvname"}，变量引用：例如某用例的输入参数为：{"namespace": "{namespace}"}，变量替换的结果为：{"namespace": "autotestnamespace"}
   3. 说明：如果在整个测试sheet中，变量名冲突，则会对原有的值进行覆盖

2. 新增响应结果正则表达式匹配功能，使用方式：

   1. 在原有的基础上，增加正则标识：需要校验的字段值如果以<#reg>开头的则进行正则表达式校验，如果校验通过则认为用例执行通过，否则用例执行失败
   2. 举例：{"requireId": "<#reg>\w+-\w+-\w+-\w+-\w+"}：表示需要校验响应返回的结果中，字段requireId符合\w+-\w+-\w+-\w+-\w+这个正则表达式规则，则校验通过

3. 新增校验响应结果时可增加附加条件，如果响应结果返回的是列表类型，支持选定特定选项后再进行结果比对

   1. 使用方式：在校验字段列中输入json校验表达式，在有多个值的地方使用?key==’value‘形式匹配特定结果，假如用例接口返回结果：

   2. ```json
      {"data":{"firstPage":true,"firstResult":0,"lastPage":false,"list":[  {"bindingEnabled":true,"comments":null,"connectionType":"bridge","createTime":"2015-02-09T13:49:36","creator":"zhangzj","dns":null,"gateway":null,"macAddress":"d0:0d:be:28:3e:1e","marked":false,"netcardId":237,"netcardName":"234234234_本地连接","netcardState":"extant","netcardStateCn":"已用","netcardUsage":"GcloudManagement","netcardUsageCn":"G-Cloud数据通道","netmask":null,"node":"gcloud39104","planId":null,"privateIp":null,"vlan":1,"vmAlias":"234234234","vmOwner":"zhangzj"},
      {"bindingEnabled":true,"comments":null,"connectionType":"bridge","createTime":"2015-02-05T10:56:44","creator":"dengyf","dns":null,"gateway":null,"macAddress":"d0:0d:71:60:3d:bc","marked":false,"netcardId":225,"netcardName":"dengyf_本地连接","netcardState":"idle","netcardStateCn":"可用","netcardUsage":"GcloudManagement","netcardUsageCn":"G-Cloud管理通道","netmask":null,"node":null,"planId":null,"privateIp":null,"vlan":1,"vmAlias":null,"vmOwner":null}],"nextPage":2,"pageNo":1,"pageSize":10,"prePage":1,"totalCount":208,"totalPage":21},"success":true}
      
      ```

   3. 结果校验输入："data.list[?netcardUsageCn=='G-Cloud数据通道'].netcardId" 表达式将取到值：237

   4. 完整的字段校验举例：{"data.list[?netcardUsageCn=='G-Cloud数据通道'].netcardId": 237}：表示需要校验：netcardUsageCn=='G-Cloud数据通道'所对应的netcardId的值是否等于237

   5. 适用范围：接口变量和字段校验

### 2021-04-19：

新增功能：

1. 新增api调试入口，api调试器，通过使用命令行命令：python debug_api.py -f file_path 传入api调试信息    api文件编写规则：1. 可以使用单个json格式传入单个api调试信息；2. 可以使用[]列表形式，传入多个api调试信息

调整

1. 调整测试结果log输出的内容
2. 调整序列化用例参数时，hostname的传参方式
3. 增加自定义异常的错误信息返回
4. 考虑到和旧平台的兼容性，调整用例中接口变量的作用范围，使具体用例中定义的接口变量可应用到整个测试sheet中

### 2021-04-16：

新增功能：

1. 新增测试结果保存到Excel文件中的功能，Excel文件默认存放在reports目录中，以运行时的时间作为文件名

调整：

1. 修复多个测试sheet时，用例顺序重复的问题
2. 调整部分代码结构

### 2021-04-15：

新增功能：

1. 用例等待时间，在“等待时间”列中输入整数或者小数，可实现用例执行完后，再等待对应的时间后再继续执行，单位**秒**
2. 用例执行顺序:
	1. 初始化sheet中的用例最新执行，表格中的用例按照Excel表格的顺序执行
	2. 数据恢复sheet中的用例最后执行，表格中的用例按照Excel表格的顺序执行
	3. 每一个用例sheet中的用例
	   1. 初始化中的用例先执行，按Excel中的顺序执行
	   2. 恢复数据中的用例最后执行，按Excel表中的顺序执行
	   3. 其他接口测试用例：标识的用例执行顺序的比未标识执行顺序的先执行，标识的执行顺序的，数值小的比数值大的先执行

### 2021-04-14：

新增功能

1. 增加全局变量
2. 增加变量名可随机添加字符串（变量命名规则：变量使用两个$$括起来，中间的是变量名，类似：$变量名$，添加的随机字符在变量后面
3. 新增可将用例入参作为变量传递给后面需要校验的校验值
4. 新增python表达式校验，入参说明：可传入符合python语法的表达，可传入list和string，表达式中response表示接口返回的json数据，举例："len(response['data'])>1" 表示接口返回的响应数据data的长度不小于1