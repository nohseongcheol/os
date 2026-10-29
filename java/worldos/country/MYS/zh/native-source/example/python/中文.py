"""内置 커널의 文件·通信·屏幕 호출과 中文 异常. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as 操作系统
import sys as 运行时

def 输出(*值, 分隔条=" ", 结尾="\n", **旧的参数列):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 旧的参数列: 旧的参数列["sep"] = 分隔条
    if "end" not in 旧的参数列: 旧的参数列["end"] = 结尾
    print(*值, **旧的参数列)

整数 = int
命令参数列 = 运行时.argv
尝试执行再次错误 = 11

class 系统错误(OSError):
    def __init__(自身值, 编号, 说明="操作系统 작업에 실패했습니다."):
        super().__init__(编号, 说明)
        自身值.编号 = 编号
        自身值.说明 = 说明

def 运行环境调用(函数, *实参):
    try:
        return 函数(*实参)
    except OSError as 错误:
        编号 = 错误.args[0] if 错误.args else 0
        raise 系统错误(编号)

def 编码文本(文本):
    return 文本.encode("utf-8")

def 解码文本(数据):
    return 数据.decode("utf-8")

def 读取文件(名称):
    return 运行环境调用(操作系统.read, 名称)

def 写入文件(名称, 数据):
    return 运行环境调用(操作系统.write, 名称, 数据)

def 移除文件(名称):
    return 运行环境调用(操作系统.remove, 名称)

def 打开数据报(端口编号):
    return 运行环境调用(操作系统.udp_open, 端口编号)

def 发送数据报(端点, 端口编号, 数据):
    return 运行环境调用(操作系统.udp_send, 端点, 端口编号, 数据)

def 发送外部数据报(端点, 地址, 端口编号, 数据):
    return 运行环境调用(操作系统.udp_sendto, 端点, 地址, 端口编号, 数据)

def 接收数据报(端点):
    return 运行环境调用(操作系统.udp_recv, 端点)

def 关闭网络(端点):
    return 运行环境调用(操作系统.udp_close, 端点)

def 绘制矩形(*实参):
    return 运行环境调用(操作系统.rect, *实参)

def 屏幕大小():
    return 运行环境调用(操作系统.screen_size)

def 等待状态用于绘图():
    return 运行环境调用(操作系统.wait_key)

毫秒 = 操作系统.ticks_ms
