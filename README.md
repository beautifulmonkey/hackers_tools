### 项目介绍
多进程,高效的把指定路径下的所有文件进行加密, 且外界无法破解, 只能通过项目本身进行解码

### 使用说明
本项目只有一个启动文件 file_op.py
启动参数:

 1. 路径: 可以是一个文件夹也可以是一个文件(如果是文件夹会递归这个的所有文件,包括无限子级)
 2. 类型: (encode或decode);指定脚本是要加密还是要进行解密

```
#示例1 说明:对桌面所有的文件进行加密
	python file_op.py ~/Desktop encode
#示例2 说明:对桌面所有的文件进行解密
	python file_op.py ~/Desktop decode
#示例3 说明:对桌面hello.py进行加密
	python file_op.py ~/Desktop/hello.py encode
```

#### 注:

	1.提供了默认的公钥和私钥, 如果需要重新生成新的密钥, 可以运行set_new_key.py
	2.图片和视频加解密速度较慢, 默认不会读图片和视频进行操作, 如果要取消该选项在file_op.py 中 FILTER_LIST更改
