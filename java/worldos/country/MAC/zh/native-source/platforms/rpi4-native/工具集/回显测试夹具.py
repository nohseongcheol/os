"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class 回显测试夹具:
    def __enter__(自身值):
        自身值.连接状态控制 = socket.socket(); 自身值.连接状态控制.bind(('127.0.0.1', 0)); 自身值.连接状态控制.listen(1)
        自身值.数据报控制 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 自身值.数据报控制.bind(('127.0.0.1', 0))
        自身值.连接状态控制.settimeout(30); 自身值.数据报控制.settimeout(30)
        自身值.TCP端口 = 自身值.连接状态控制.getsockname()[1]; 自身值.UDP端口 = 自身值.数据报控制.getsockname()[1]
        自身值.错误列 = []; 自身值.拥有已接收 = {}
        def 连接状态控制():
            try:
                接通状态, _ = 自身值.连接状态控制.accept()
                with 接通状态:
                    接通状态.settimeout(5); 数据 = bytearray()
                    while b'\n' not in 数据:
                        片段值 = 接通状态.recv(512)
                        if not 片段值: raise RuntimeError('TCP EOF before request')
                        数据.extend(片段值)
                    自身值.拥有已接收['tcp'] = bytes(数据); 接通状态.sendall(数据)
            except Exception as 辅助条目: 自身值.错误列.append(str(辅助条目))
        def 数据报控制():
            try:
                数据, 对端值 = 自身值.数据报控制.recvfrom(512); 自身值.拥有已接收['udp'] = 数据; 自身值.数据报控制.sendto(数据, 对端值)
            except Exception as 辅助条目: 自身值.错误列.append(str(辅助条目))
        自身值.线程集 = [threading.Thread(target=文件条目, daemon=True) for 文件条目 in (连接状态控制, 数据报控制)]
        for 终端条目 in 自身值.线程集: 终端条目.start()
        return 自身值

    def __exit__(自身值, *参数数组):
        自身值.连接状态控制.close(); 自身值.数据报控制.close()
        for 终端条目 in 自身值.线程集: 终端条目.join(timeout=1)
