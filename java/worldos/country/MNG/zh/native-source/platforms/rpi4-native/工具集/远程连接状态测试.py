#!/usr/bin/env python3
"""实际数据 OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from 执行命令 import 项目根, 命令
from 网络桥接 import 网络桥接


def 运行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--kernel', type=Path, default=项目根 / 'build/kernel8.img')
    解析器.add_argument('--access', type=Path, default=项目根 / 'build/remote/access.json')
    解析器.add_argument('--output', type=Path, default=项目根 / 'build/verification/native-remote')
    实参 = 解析器.parse_args()
    输出 = 实参.output
    输出.mkdir(parents=True, exist_ok=True)
    设置 = json.loads(实参.access.read_text())
    报告值 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(实参.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 空端口():
        with socket.socket() as 连接:
            连接.bind(('127.0.0.5', 0))
            return 连接.getsockname()[1]
    命令壳端口, 屏幕端口, 文件端口 = 空端口(), 空端口(), 空端口()
    日志记录 = bytearray()
    进程值 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 临时值, 网络桥接(文件端口,
                ['tcp:{}:22'.format(命令壳端口), 'tcp:{}:5900'.format(屏幕端口)], 宿主地址='127.0.0.5') as 桥接值:
            运行参数 = 命令()
            运行参数[运行参数.index('-kernel') + 1] = str(实参.kernel.resolve())
            进程值 = subprocess.Popen(运行参数 + ['-display','none','-monitor','none','-serial','stdio'] + 桥接值.已转发参数(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 汇集值列():
                while True:
                    数据 = 进程值.stdout.read(4096)
                    if not 数据: break
                    日志记录.extend(数据)
            线程值 = threading.Thread(target=汇集值列, daemon=True)
            线程值.start()
            def 等待状态状态(机器字文本, 初始项目=0, 限制值=60):
                结尾 = time.monotonic() + 限制值
                while 机器字文本 not in 日志记录[初始项目:]:
                    if time.monotonic()>结尾 or 进程值.poll() is not None:
                        raise AssertionError('Missing '+repr(机器字文本)+'\n'+日志记录[初始项目:].decode('utf-8','replace'))
                    time.sleep(.02)
            等待状态状态(b'jkoros-native> ')
            辅助器值 = Path(临时值)/'askpass'
            辅助器值.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            辅助器值.chmod(0o700)
            环境 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(辅助器值), SSH_ASKPASS_REQUIRE='force')
            def 安全命令壳(密码值, 指令值, 追加条目=()):
                环境['JKOROS_TEST_PASSWORD']=密码值
                实参=['ssh','-v']+list(追加条目)+['-p',str(命令壳端口),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(临时值)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',指令值]
                结果=subprocess.run(实参,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=环境,start_new_session=True,timeout=50)
                return 结果
            结果=安全命令壳('!' + 设置['ssh_password'], 'echo SHOULD_NOT_RUN')
            (输出/'ssh-rejected.log').write_bytes(结果.stderr)
            assert 结果.returncode!=0 and b'Permission denied' in 结果.stderr and b'SHOULD_NOT_RUN' not in 日志记录, 结果.stderr
            报告值['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            结果=安全命令壳(设置['ssh_password'], 'echo SSH_NATIVE_PASS')
            (输出/'ssh.log').write_bytes(结果.stderr)
            (输出/'ssh-output.txt').write_bytes(结果.stdout)
            assert 结果.returncode==0 and b'SSH_NATIVE_PASS' in 结果.stdout, (结果.returncode,结果.stdout,结果.stderr)
            报告值['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 结果.stderr, 结果.stderr
            报告值['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            结果=安全命令壳(设置['ssh_password'], 'cd /example/java; java 输出例; cd /')
            assert 结果.returncode==0 and 'JAVA 输出: 안녕하세요 😀'.encode() in 结果.stdout,结果.stdout
            报告值['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            结果=安全命令壳(设置['ssh_password'], 'missing_remote_command')
            assert 结果.returncode==127,结果.returncode
            报告值['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            结果=安全命令壳(设置['ssh_password'], 'cat /example/java/窗口例.java', ('-o', 'RekeyLimit=1K'))
            (输出/'ssh-rekey.log').write_bytes(结果.stderr)
            assert 结果.returncode==0 and 'class 窗口例'.encode() in 结果.stdout, (结果.returncode,结果.stdout,结果.stderr)
            assert 结果.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 结果.stderr
            报告值['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            交互式参数列=['ssh','-tt','-p',str(命令壳端口),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(临时值)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            交互式会话=subprocess.Popen(交互式参数列,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=环境,start_new_session=True,bufsize=0)
            执行记录=bytearray();选中状态值=selectors.DefaultSelector();选中状态值.register(交互式会话.stdout,selectors.EVENT_READ)
            def 读取交互式(显示值):
                截止时间值=time.monotonic()+30
                while 显示值 not in 执行记录:
                    if time.monotonic()>截止时间值 or 交互式会话.poll() is not None:raise AssertionError('SSH interactive missing '+repr(显示值)+' '+repr(bytes(执行记录)))
                    for 条目值,_ in 选中状态值.select(.1):
                        片段值=条目值.fileobj.read(4096)
                        if 片段值:执行记录.extend(片段值)
            try:
                读取交互式(b'shared native console')
                交互式会话.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');交互式会话.stdin.flush();读取交互式(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                交互式会话.stdin.write(b'\x04');交互式会话.stdin.flush();余数值,错误=交互式会话.communicate(timeout=15)
                assert 交互式会话.returncode==0 and b'PTY allocation request failed' not in 错误,(交互式会话.returncode,错误)
                (输出/'ssh-interactive.txt').write_bytes(执行记录+余数值)
            finally:
                选中状态值.close()
                if 交互式会话.poll() is None:交互式会话.kill();交互式会话.wait()
            报告值['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 精确地值(连接, 数):
                数据=bytearray()
                while len(数据)<数:
                    块片值=连接.recv(数-len(数据))
                    if not 块片值: raise AssertionError('RFB EOF')
                    数据.extend(块片值)
                return bytes(数据)
            def 屏幕身份验证(密码值):
                连接=socket.create_connection(('127.0.0.5',屏幕端口),10);连接.settimeout(30)
                assert 精确地值(连接,12)==b'RFB 003.008\n'
                连接.sendall(b'RFB 003.008\n');assert 精确地值(连接,2)==b'\x01\x02'
                连接.sendall(b'\x02');挑战值=精确地值(连接,16)
                输入密码=密码值.encode('ascii')[:8].ljust(8, b'\0')
                键材料=bytes(int('{:08b}'.format(数)[::-1],2) for 数 in 输入密码)
                连接.sendall(DES.new(键材料,DES.MODE_ECB).encrypt(挑战值))
                状态值=struct.unpack('!I',精确地值(连接,4))[0]
                return 连接,状态值
            无效密码='!' if not 设置['vnc_password'].startswith('!') else '?'
            连接,状态值=屏幕身份验证(无效密码);assert 状态值==1;连接.close();time.sleep(.6)
            报告值['checks'].append('VNC incorrect password rejected')
            连接,状态值=屏幕身份验证(设置['vnc_password']);assert 状态值==0
            with 连接:
                连接.sendall(b'\x01');初始状态=精确地值(连接,24);宽度值,高度值=struct.unpack('!HH',初始状态[:4]);名称=精确地值(连接,struct.unpack('!I',初始状态[20:24])[0])
                assert (宽度值,高度值)==(640,480) and b'jkoros native'==名称
                def 屏幕(递增步骤=0):
                    连接.sendall(struct.pack('!BBHHHH',3,递增步骤,0,0,宽度值,高度值));头值=精确地值(连接,4);数=struct.unpack('!H',头值[2:])[0];总计值=0
                    绘图=bytearray(宽度值*高度值*4)
                    for _ in range(数):
                        横坐标坐标,Y_按钮坐标,区域宽度,区域高度,方法模式=struct.unpack('!HHHHi',精确地值(连接,12));assert 方法模式==0 and 横坐标坐标+区域宽度<=宽度值 and Y_按钮坐标+区域高度<=高度值
                        像素=精确地值(连接,区域宽度*区域高度*4);总计值+=len(像素)
                        for 行 in range(区域高度):绘图[((Y_按钮坐标+行)*宽度值+横坐标坐标)*4:((Y_按钮坐标+行)*宽度值+横坐标坐标+区域宽度)*4]=像素[行*区域宽度*4:(行+1)*区域宽度*4]
                    if not 递增步骤:
                        from PIL import Image
                        Image.frombytes('RGB',(宽度值,高度值),bytes(绘图),'raw','BGRX').save(str(输出/'native-vnc.png'))
                    return 数,总计值
                数,总计值=屏幕();assert 数>0 and 总计值==宽度值*高度值*4
                报告值['checks'].append('Native framebuffer RFB full update {} bytes'.format(总计值))
                数,总计值=屏幕(1);assert 总计值<宽度值*高度值*4
                报告值['checks'].append('RFB incremental update')
                初始项目=len(日志记录)
                for 字符值 in 'echo VNC_NATIVE_PASS\r':
                    符号=0xff0d if 字符值=='\r' else ord(字符值)
                    连接.sendall(struct.pack('!BBHI',4,1,0,符号));连接.sendall(struct.pack('!BBHI',4,0,0,符号))
                等待状态状态(b'VNC_NATIVE_PASS',初始项目)
                报告值['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 键笔画(符号,按下值=1):连接.sendall(struct.pack('!BBHI',4,按下值,0,符号))
                初始项目=len(日志记录)
                for 字符值 in 'echo ':键笔画(ord(字符值))
                键笔画(0xffc6)
                for 字符值 in 'gksrmf':键笔画(ord(字符值))
                键笔画(0xffc6);键笔画(0xff0d)
                等待状态状态('\r\n한글\r\n'.encode(),初始项目)
                报告值['checks'].append('Native VNC F9 two-set Hangul composition')
                连接.sendall(struct.pack('!BBHH',5,0,120,100))
                报告值['checks'].append('VNC pointer input accepted')
            进程值.stdin.write(b'poweroff\n');进程值.stdin.flush();进程值.wait(timeout=15);assert 进程值.returncode==0
            报告值['passed']=True
    finally:
        if 进程值 and 进程值.poll() is None:
            进程值.terminate()
            try: 进程值.wait(timeout=5)
            except subprocess.TimeoutExpired: 进程值.kill();进程值.wait()
        (输出/'serial.log').write_bytes(日志记录)
        (输出/'report.json').write_text(json.dumps(报告值,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(报告值,ensure_ascii=False,indent=2))


if __name__=='__main__': 运行()
