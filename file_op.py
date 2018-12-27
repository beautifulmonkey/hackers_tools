# -*- coding: utf-8 -*-
"""
	author: yx
	提供了默认的公钥和私钥, 如果需要重新生成新的密钥, 可以运行set_new_key.py
"""

from multiprocessing import cpu_count, Pool
import sys
import os
import rsa
import time

# 将不需要操作的文件后缀放入过滤器
FILTER_LIST = [
		".webp", ".bmp", ".jpg",".png", ".tif", ".gif",".jpeg"  # 图片
		".AVI", ".wma", ".rmvb", ".rm", ".flash", ".mp4", ".mid", ".3GP"  # 视频
	]

T_MAP = {
	"encode": "加密",
	"decode": "解密",
}


def read_key():
	with open("PublicKey.pem", "r") as f:
		_PublicKey = rsa.PublicKey.load_pkcs1(f.read())

	with open("PrivateKey.pem", "r") as f:
		_PrivateKey = rsa.PrivateKey.load_pkcs1(f.read())

	return [_PublicKey, _PrivateKey]


def encrypt(_PublicKey, addr):
	with open(addr, "r") as f:
		data = f.read()

	byte_size = rsa.common.byte_size(_PublicKey.n) - 11
	data_chunk = [data[i * byte_size:i * byte_size + byte_size] for i in range(len(data) / byte_size + 1)]

	with open(addr, "w") as f:
		for chunk in data_chunk:
			encrypt_data = rsa.encrypt(chunk, _PublicKey)
			f.write(encrypt_data)


def decrypt(_PrivateKey, addr):
	with open(addr, "r") as f:
		data = f.read()

	byte_size = rsa.common.byte_size(_PrivateKey.n)
	data_chunk = [data[i * byte_size:i * byte_size + byte_size] for i in range(len(data) / byte_size + 1)]

	with open(addr, "w") as f:
		try:
			for chunk in data_chunk:
				decrypt_data = rsa.decrypt(chunk, _PrivateKey)
				f.write(decrypt_data)
		except ValueError:
			pass


def file_action(task_list, _type):
	(PublicKey, PrivateKey) = read_key()

	pool = Pool(cpu_count())
	print "开启{}, CPU核数:{}, 生成任务{}个".format(T_MAP[_type], cpu_count(), len(task_list))
	for index, addr in enumerate(task_list, start=1):
		print "当前任务{}:{}".format(index, addr)
		if _type == "encode":
			pool.apply_async(encrypt, (PublicKey, addr, ))
		elif _type == "decode":
			pool.apply_async(decrypt, (PrivateKey, addr, ))

	pool.close()
	pool.join()


def path_decomposition(_path):

	if not os.path.isfile(_path):
		_path_lst = []
		for f_path, dirs, fs in os.walk(_path):
			for f in fs:
				ju_path = "{}/.".format(_path)
				jo_path = os.path.join(f_path, f)
				suffix = os.path.splitext(f)[1]
				if suffix in FILTER_LIST:
					print "过滤:{}".format(jo_path)
					continue
				if ju_path not in jo_path:
					_path_lst.append(jo_path)
		return _path_lst

	else:
		return [_path]


def check_argv(_path, _type):

	if _type not in ["encode", "decode"]:
		raise ValueError("Only in (encode,decode) intervals!")

	if not os.path.exists(_path):
		raise OSError("Path does not exist!")
	_start = int(time.time())
	task_list = path_decomposition(_path)
	file_action(task_list, _type)
	_end = int(time.time())
	print "已完成{}, 总耗时:{}秒".format(T_MAP[_type], _end - _start)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		_info = "\r\n参数: python xxx.py 文件目录 类型(encode:加密, decode:解密)"
		raise TypeError(_info)

	_path = sys.argv[1]
	_type = sys.argv[2]
	check_argv(_path, _type)
