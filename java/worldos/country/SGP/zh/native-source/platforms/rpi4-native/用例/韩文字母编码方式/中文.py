"""内置 内核值 MicroPython에서 사용하는 한글 函数 名称."""
import jkoros as 操作系统
输出 = print
读取文件 = 操作系统.read
写入文件 = 操作系统.write
移除文件 = 操作系统.remove
读取输入 = 操作系统.stdin
绘制矩形 = 操作系统.rect
等待状态用于绘图 = 操作系统.wait_key
毫秒 = 操作系统.ticks_ms
打开数据报 = 操作系统.udp_open
发送数据报 = 操作系统.udp_send
发送外部数据报 = 操作系统.udp_sendto
接收数据报 = 操作系统.udp_recv
关闭网络 = 操作系统.udp_close

def 解码文本(数据):
    return 数据.decode("utf-8")
