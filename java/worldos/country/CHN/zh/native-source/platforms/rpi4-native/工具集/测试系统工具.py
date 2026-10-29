#!/usr/bin/env python3
"""实际数据 内置 커널의 IP/ICMP, 状态值 查询值, 현지어 命令, 게스트 退出程序 有效性校验."""
import argparse
import ftplib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import selectors
import signal
import socket
import subprocess
import sys
import tempfile
import time


def 运行():
    解析器=argparse.ArgumentParser();解析器.add_argument('--edition',type=Path);解析器.add_argument('--output',type=Path);解析器.add_argument('--poweroff-only',action='store_true');实参=解析器.parse_args()
    项目根=Path(__file__).resolve().parents[1];设置={};名称表={}
    if 实参.edition:
        国家值=实参.edition.resolve();设置=json.loads((国家值/'native.json').read_text());名称表=设置['identifiers'];项目根=国家值/设置['source']/设置['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(国家值/'native-edition.py'),'check'])
        宿主=国家值/'host/qemu'
        if 宿主.is_file():os.environ['QEMU_AARCH64']=str(宿主)
    工具集=项目根/Path(设置.get('runner','工具集/执行命令.py')).parent
    sys.path.insert(0,str(工具集))
    def 读取(名称):
        路径=工具集/(名称表.get(名称,名称)+'.py');契约值=importlib.util.spec_from_file_location('test_'+名称,str(路径));模块值=importlib.util.module_from_spec(契约值);契约值.loader.exec_module(模块值);return 模块值
    执行状态模块=读取('执行命令');网络模块=读取('网络桥接');命令=getattr(执行状态模块,名称表.get('命令','命令'));桥接类型=getattr(网络模块,名称表.get('网络桥接','网络桥接'))
    别名值=设置.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP地址','ping':'测试响应','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'电源关闭侧','help':'显示帮助'})
    sys.path.insert(0,str(项目根/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(项目根);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    输出=实参.output or 项目根/'build/verification/system-tools';输出.mkdir(parents=True,exist_ok=True)
    报告值={'passed':False,'country':设置.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    日志记录=bytearray();序列值=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 临时值:
        控制路径=Path(临时值)/'qmp.sock'
        while True:
            with socket.socket() as 搜索值:搜索值.bind(('127.0.0.1',0));端口编号=搜索值.getsockname()[1]
            if not 50000<=端口编号<=50007:break
        with 桥接类型(端口编号,捕获=True,客户机地址=ipTestText('10.0.2.20'),宿主地址='127.0.0.2') as 桥接值:
            进程值=subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(控制路径)]+桥接值.已转发参数(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            选取条目=selectors.DefaultSelector();选取条目.register(进程值.stdout,selectors.EVENT_READ)
            def 接收(显示值,运行=0,限制值=45):
                结尾=time.monotonic()+限制值
                while 显示值 not in 日志记录[运行:]:
                    if time.monotonic()>结尾 or 进程值.poll() is not None:raise AssertionError('Missing '+repr(显示值)+'\n'+日志记录[运行:].decode('utf-8','replace'))
                    for 键值,_ in 选取条目.select(.1):
                        数据=键值.fileobj.read(65536)
                        if 数据:日志记录.extend(数据)
                return 日志记录[运行:].decode('utf-8','replace').replace('\r\n','\n')
            def 发送(数据):进程值.stdin.write(数据);进程值.stdin.flush()
            def 命令壳(文本):
                文本=ipTestText(文本)
                print(报告值['country'],文本,flush=True);序列值[0]+=1;显示值='__SYSTEM_DONE_'+str(序列值[0])+'__';运行=len(日志记录)
                发送((文本+'; echo; echo '+显示值+'\n').encode())
                结束标记=('\r\n'+显示值+'\r\n').encode();接收(结束标记,运行)
                结束位置=日志记录.index(结束标记,运行)+len(结束标记)
                接收(b'jkoros-native> ',结束位置)
                return 日志记录[运行:].decode('utf-8','replace').replace('\r\n','\n')
            def 验证(文本,*值列):
                回复=命令壳(文本)
                for 值 in 值列:assert ipTestText(值) in 回复,(文本,值,回复)
                return 回复
            try:
                接收(b'jkoros-native> ')
                if not 实参.poweroff_only:
                    帮助值=验证('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 备用名称 in 别名值.values():assert 备用名称 in 帮助值,(备用名称,帮助值)
                    验证(别名值['help']+' system','Network / system')
                    验证('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    验证(别名值['ipconfig'],'inet 10.0.2.15');验证('ip addr show','sl0: UP');验证('ifconfig','sl0: UP')
                    for 无效设置 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        错误=验证('ipconfig set '+无效设置+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in 错误,错误
                        验证('ipconfig','inet 10.0.2.15')
                    验证('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    验证(别名值['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    验证('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    验证('ip link set dev sl0 down','sl0: DOWN');验证('ping -c 1 10.0.2.2; echo STATUS=$?','错误 -100','STATUS=1')
                    验证('ipconfig up','sl0: UP')
                    验证(别名值['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    验证('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    验证('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');验证(别名值['route'],'10.0.2.2 sl0')
                    验证('ftpd start','FTP listening')
                    验证(别名值['netstat'],'10.0.2.20:21','LISTEN');验证('ss','LISTEN')
                    验证('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','错误 -16')
                    with ftplib.FTP() as 客户端值:
                        客户端值.connect('127.0.0.2',端口编号,timeout=20);客户端值.login();数据=b'Network address was changed in the guest.\n'
                        客户端值.storbinary('STOR net-state.txt',io.BytesIO(数据));已接收数据=bytearray();客户端值.retrbinary('RETR net-state.txt',已接收数据.extend);assert 已接收数据==数据;客户端值.delete('net-state.txt')
                    验证('ftpd stop','FTP stopped');验证('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    报告值['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 已保存(文本):
                        已找到值=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',文本);assert 已找到值,文本;return tuple(map(int,已找到值.groups()))
                    之前值=已保存(验证('df','RAM only'));验证('echo disk-proof > sys-state.txt');之后状态=已保存(验证(别名值['df'],'RAM only'))
                    assert 之后状态[1]-之前值[1]==16384 and 之后状态[4]-之前值[4]==1 and 之后状态[3]-之前值[3]==11,(之前值,之后状态)
                    验证('rm sys-state.txt');assert 已保存(命令壳('df'))==之前值
                    内存=验证(别名值['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');数量值=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',内存).groups()));assert 0<数量值[1]<=数量值[0] and 数量值[1]+数量值[2]==数量值[0]
                    验证(别名值['ps'],'kernel/shell');验证(别名值['uptime'],'seconds')
                    运行状态信息=验证(别名值['top']+' -n 2','kernel/shell');assert 运行状态信息.count('PID SLOT STATE')==2,运行状态信息
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    验证('terminal','TERMINAL READY');运行=len(日志记录);发送(b'vi process.txt\n');接收(b'NORMAL',运行)
                    运行=len(日志记录);发送(bytes([30,2,1,0,0,0,0]));接收(b'jkoros-native> ',运行)
                    条目列表=验证('ps','SUSPENDED','vi process.txt');已找到值=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',条目列表);assert 已找到值 and int(已找到值.group(2))>0,条目列表
                    验证('free','EL0 mapped KiB: '+已找到值.group(2))
                    运行=len(日志记录);发送(b'top\n');接收(b'PID SLOT STATE',运行);发送(b'q');接收(b'jkoros-native> ',运行)
                    # Test a multibyte prefix through the real shell completion path.
                    if 别名值['df']!='df':
                        运行=len(日志记录);发送((别名值['df'][:-1]+'\t\n').encode());接收(b'RAM only',运行);接收(b'jkoros-native> ',运行)
                    报告值['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as 控制值:
                    控制值.settimeout(15);控制值.connect(str(控制路径));流值=控制值.makefile('rwb');json.loads(流值.readline());流值.write(b'{"execute":"qmp_capabilities"}\n');流值.flush()
                    while 'return' not in json.loads(流值.readline()):pass
                    发送((('poweroff' if 实参.poweroff_only else 别名值['poweroff'])+'\n').encode())
                    while True:
                        事件=json.loads(流值.readline())
                        if 事件.get('event')=='SHUTDOWN':break
                    assert 事件['data']['guest'] and 事件['data']['reason']=='guest-shutdown',事件
                    assert 进程值.wait(timeout=15)==0
                    报告值['shutdown']=事件;报告值['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                报告值['network_trace']=桥接值.追踪日志
                assert 实参.poweroff_only or any(条目值['protocol']==1 and 条目值['direction']=='from_guest' for 条目值 in 桥接值.追踪日志)
                报告值['passed']=True
            finally:
                if 进程值.poll() is None:os.killpg(进程值.pid,signal.SIGTERM)
                try:进程值.wait(timeout=10)
                except subprocess.TimeoutExpired:进程值.kill();进程值.wait()
                选取条目.close();(输出/'serial.log').write_bytes(日志记录);(输出/'report.json').write_text(json.dumps(报告值,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({键值:值 for 键值,值 in 报告值.items() if 键值!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':运行()
