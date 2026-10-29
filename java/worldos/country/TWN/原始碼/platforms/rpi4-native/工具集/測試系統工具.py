#!/usr/bin/env python3
"""實際資料 內建 커널의 IP/ICMP, 狀態值 查詢值, 현지어 命令, 게스트 退出程式 有效性校驗."""
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


def 運行():
    解析器=argparse.ArgumentParser();解析器.add_argument('--edition',type=Path);解析器.add_argument('--output',type=Path);解析器.add_argument('--poweroff-only',action='store_true');實參=解析器.parse_args()
    項目根=Path(__file__).resolve().parents[1];設置={};名稱表={}
    if 實參.edition:
        國家值=實參.edition.resolve();設置=json.loads((國家值/'native.json').read_text());名稱表=設置['identifiers'];項目根=國家值/設置['source']/設置['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(國家值/'native-edition.py'),'check'])
        宿主=國家值/'host/qemu'
        if 宿主.is_file():os.environ['QEMU_AARCH64']=str(宿主)
    工具集=項目根/Path(設置.get('runner','工具集/執行命令.py')).parent
    sys.path.insert(0,str(工具集))
    def 讀取(名稱):
        路徑=工具集/(名稱表.get(名稱,名稱)+'.py');契約值=importlib.util.spec_from_file_location('test_'+名稱,str(路徑));模塊值=importlib.util.module_from_spec(契約值);契約值.loader.exec_module(模塊值);return 模塊值
    執行狀態模塊=讀取('執行命令');網路模塊=讀取('網路橋接');命令=getattr(執行狀態模塊,名稱表.get('命令','命令'));橋接類型=getattr(網路模塊,名稱表.get('網路橋接','網路橋接'))
    別名值=設置.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP地址','ping':'測試響應','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'電源關閉側','help':'顯示幫助'})
    sys.path.insert(0,str(項目根/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(項目根);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    輸出=實參.output or 項目根/'build/verification/system-tools';輸出.mkdir(parents=True,exist_ok=True)
    報告值={'passed':False,'country':設置.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    日誌記錄=bytearray();序列值=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 臨時值:
        控制路徑=Path(臨時值)/'qmp.sock'
        while True:
            with socket.socket() as 搜索值:搜索值.bind(('127.0.0.1',0));埠編號=搜索值.getsockname()[1]
            if not 50000<=埠編號<=50007:break
        with 橋接類型(埠編號,捕獲=True,客戶機地址=ipTestText('10.0.2.20'),宿主地址='127.0.0.2') as 橋接值:
            程序值=subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(控制路徑)]+橋接值.已轉發實際參數(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            選取條目=selectors.DefaultSelector();選取條目.register(程序值.stdout,selectors.EVENT_READ)
            def 接收(顯示值,運行=0,限制值=45):
                結尾=time.monotonic()+限制值
                while 顯示值 not in 日誌記錄[運行:]:
                    if time.monotonic()>結尾 or 程序值.poll() is not None:raise AssertionError('Missing '+repr(顯示值)+'\n'+日誌記錄[運行:].decode('utf-8','replace'))
                    for 鍵值,_ in 選取條目.select(.1):
                        資料=鍵值.fileobj.read(65536)
                        if 資料:日誌記錄.extend(資料)
                return 日誌記錄[運行:].decode('utf-8','replace').replace('\r\n','\n')
            def 發送(資料):程序值.stdin.write(資料);程序值.stdin.flush()
            def 命令殼(文本):
                文本=ipTestText(文本)
                print(報告值['country'],文本,flush=True);序列值[0]+=1;顯示值='__SYSTEM_DONE_'+str(序列值[0])+'__';運行=len(日誌記錄)
                發送((文本+'; echo; echo '+顯示值+'\n').encode())
                結束標記=('\r\n'+顯示值+'\r\n').encode();接收(結束標記,運行)
                結束位置=日誌記錄.index(結束標記,運行)+len(結束標記)
                接收(b'jkoros-native> ',結束位置)
                return 日誌記錄[運行:].decode('utf-8','replace').replace('\r\n','\n')
            def 驗證(文本,*值列):
                回覆=命令殼(文本)
                for 值 in 值列:assert ipTestText(值) in 回覆,(文本,值,回覆)
                return 回覆
            try:
                接收(b'jkoros-native> ')
                if not 實參.poweroff_only:
                    幫助值=驗證('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 備用名稱 in 別名值.values():assert 備用名稱 in 幫助值,(備用名稱,幫助值)
                    驗證(別名值['help']+' system','Network / system')
                    驗證('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    驗證(別名值['ipconfig'],'inet 10.0.2.15');驗證('ip addr show','sl0: UP');驗證('ifconfig','sl0: UP')
                    for 無效設置 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        錯誤=驗證('ipconfig set '+無效設置+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in 錯誤,錯誤
                        驗證('ipconfig','inet 10.0.2.15')
                    驗證('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    驗證(別名值['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    驗證('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    驗證('ip link set dev sl0 down','sl0: DOWN');驗證('ping -c 1 10.0.2.2; echo STATUS=$?','錯誤 -100','STATUS=1')
                    驗證('ipconfig up','sl0: UP')
                    驗證(別名值['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    驗證('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    驗證('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');驗證(別名值['route'],'10.0.2.2 sl0')
                    驗證('ftpd start','FTP listening')
                    驗證(別名值['netstat'],'10.0.2.20:21','LISTEN');驗證('ss','LISTEN')
                    驗證('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','錯誤 -16')
                    with ftplib.FTP() as 客戶端值:
                        客戶端值.connect('127.0.0.2',埠編號,timeout=20);客戶端值.login();資料=b'Network address was changed in the guest.\n'
                        客戶端值.storbinary('STOR net-state.txt',io.BytesIO(資料));已接收資料=bytearray();客戶端值.retrbinary('RETR net-state.txt',已接收資料.extend);assert 已接收資料==資料;客戶端值.delete('net-state.txt')
                    驗證('ftpd stop','FTP stopped');驗證('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    報告值['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 已保存(文本):
                        已找到值=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',文本);assert 已找到值,文本;return tuple(map(int,已找到值.groups()))
                    之前值=已保存(驗證('df','RAM only'));驗證('echo disk-proof > sys-state.txt');之後狀態=已保存(驗證(別名值['df'],'RAM only'))
                    assert 之後狀態[1]-之前值[1]==16384 and 之後狀態[4]-之前值[4]==1 and 之後狀態[3]-之前值[3]==11,(之前值,之後狀態)
                    驗證('rm sys-state.txt');assert 已保存(命令殼('df'))==之前值
                    記憶體=驗證(別名值['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');數量值=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',記憶體).groups()));assert 0<數量值[1]<=數量值[0] and 數量值[1]+數量值[2]==數量值[0]
                    驗證(別名值['ps'],'kernel/shell');驗證(別名值['uptime'],'seconds')
                    運行狀態信息=驗證(別名值['top']+' -n 2','kernel/shell');assert 運行狀態信息.count('PID SLOT STATE')==2,運行狀態信息
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    驗證('terminal','TERMINAL READY');運行=len(日誌記錄);發送(b'vi process.txt\n');接收(b'NORMAL',運行)
                    運行=len(日誌記錄);發送(bytes([30,2,1,0,0,0,0]));接收(b'jkoros-native> ',運行)
                    條目列表=驗證('ps','SUSPENDED','vi process.txt');已找到值=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',條目列表);assert 已找到值 and int(已找到值.group(2))>0,條目列表
                    驗證('free','EL0 mapped KiB: '+已找到值.group(2))
                    運行=len(日誌記錄);發送(b'top\n');接收(b'PID SLOT STATE',運行);發送(b'q');接收(b'jkoros-native> ',運行)
                    # Test a multibyte prefix through the real shell completion path.
                    if 別名值['df']!='df':
                        運行=len(日誌記錄);發送((別名值['df'][:-1]+'\t\n').encode());接收(b'RAM only',運行);接收(b'jkoros-native> ',運行)
                    報告值['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as 控制值:
                    控制值.settimeout(15);控制值.connect(str(控制路徑));流值=控制值.makefile('rwb');json.loads(流值.readline());流值.write(b'{"execute":"qmp_capabilities"}\n');流值.flush()
                    while 'return' not in json.loads(流值.readline()):pass
                    發送((('poweroff' if 實參.poweroff_only else 別名值['poweroff'])+'\n').encode())
                    while True:
                        事件=json.loads(流值.readline())
                        if 事件.get('event')=='SHUTDOWN':break
                    assert 事件['data']['guest'] and 事件['data']['reason']=='guest-shutdown',事件
                    assert 程序值.wait(timeout=15)==0
                    報告值['shutdown']=事件;報告值['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                報告值['network_trace']=橋接值.追蹤日誌
                assert 實參.poweroff_only or any(條目值['protocol']==1 and 條目值['direction']=='from_guest' for 條目值 in 橋接值.追蹤日誌)
                報告值['passed']=True
            finally:
                if 程序值.poll() is None:os.killpg(程序值.pid,signal.SIGTERM)
                try:程序值.wait(timeout=10)
                except subprocess.TimeoutExpired:程序值.kill();程序值.wait()
                選取條目.close();(輸出/'serial.log').write_bytes(日誌記錄);(輸出/'report.json').write_text(json.dumps(報告值,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({鍵值:值 for 鍵值,值 in 報告值.items() if 鍵值!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':運行()
