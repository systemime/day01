## master mysql中
```shell script
show master status;
```

```shell script
mysql> show master status;
+---------------------------+----------+--------------+------------------+-------------------+
| File                      | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+---------------------------+----------+--------------+------------------+-------------------+
| replicas-mysql-bin.000003 |      154 |              | mysql            |                   |
+---------------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

## slave1 and slave2 的mysql中分别执行
```shell script
CHANGE MASTER TO
MASTER_HOST='mysql-master',
MASTER_USER='root',
MASTER_PASSWORD='xxxxx',
MASTER_LOG_FILE='replicas-mysql-bin.000003', -- File文件名
MASTER_LOG_POS=154; -- binlog记录位置
```

## 重启slave1和slave2
```shell script
docker restart mysql-slave1 mysql-slave1
```

## 检查同步状态 SQL中
````shell script
# # 启动salve功能
start slave;

# # 检查slave同步状态
show slave status\G
# # 主要一下两个状态必须为YES
# Slave_IO_Running: Yes
# Slave_SQL_Running: Yes
# # 输出示例
----
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: mysql-master
                  Master_User: root
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: replicas-mysql-bin.000003
          Read_Master_Log_Pos: 463
               Relay_Log_File: replicas-mysql-relay-bin.000002
                Relay_Log_Pos: 329
        Relay_Master_Log_File: replicas-mysql-bin.000003
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 463
              Relay_Log_Space: 545
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 100
                  Master_UUID: 27d3cd96-ee89-11ea-9da7-0242ac150010
             Master_Info_File: /var/lib/mysql/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
1 row in set (0.00 sec)
----
````

### 同步线程出现问题
#### 手动重新同步
```shell script
# slave中
stop slave;
# master 中
show master status;
# slave中
CHANGE MASTER TO
MASTER_HOST='mysql-master',
MASTER_USER='root',
MASTER_PASSWORD='xxxxx',
MASTER_LOG_FILE='replicas-mysql-bin.000003', -- File文件名
MASTER_LOG_POS=xxx; -- binlog记录位置

start slave
```

#### 因为事务的原因导致的sql进程停止
```shell script
stop slave;
set GLOBAL SQL_SLAVE_SKIP_COUNTER=1;
start slave;
```
