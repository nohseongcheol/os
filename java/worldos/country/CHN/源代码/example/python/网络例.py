from 中文 import 输出, 打开数据报, 发送外部数据报, 接收数据报, 关闭网络, 毫秒
from 中文 import 系统错误, 尝试执行再次错误, 编码文本, 命令参数列, 整数
端点 = 打开数据报(0)
try:
    数据报 = 编码文本("PYTHON UDP Chinese")
    发送外部数据报(端点, "10.0.2.2", 整数(命令参数列[1]), 数据报)
    运行 = 毫秒()
    while True:
        try:
            回复, 端口值 = 接收数据报(端点)
            break
        except 系统错误 as 错误:
            if 错误.编号 != 尝试执行再次错误 or 毫秒() - 运行 >= 700:
                raise
    assert 回复 == 数据报
    输出("PYTHON 네트워크 验证: UDP Chinese")
finally:
    关闭网络(端点)
