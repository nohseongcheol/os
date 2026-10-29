#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from 桌面视图 import 精确值
from 回显示例服务器 import 回显服务器列
from 执行命令 import 项目根


def 测试语言(语言,回显服务器条目,结果数据):
    with socket.socket() as 临时:
        临时.bind(('127.0.0.1',0));文件传送端口编号=临时.getsockname()[1]
    进程=subprocess.Popen(['python3',str(项目根/'工具集/执行命令.py'),'--desktop','--network','--port','0','--ftp-port',str(文件传送端口编号)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    就绪选择器=selectors.DefaultSelector();就绪选择器.register(进程.stdout,selectors.EVENT_READ)
    执行记录=bytearray();客户端=None;文件传送连接状态=None
    def 接收消息(标记,运行=0):
        结束偏移=time.monotonic()+60
        while 标记 not in 执行记录[运行:]:
            if time.monotonic()>结束偏移 or 进程.poll() is not None:raise AssertionError(执行记录[运行:].decode('utf-8','replace'))
            for 已按下值,_ in 就绪选择器.select(.1):
                数据=已按下值.fileobj.read(65536)
                if 数据:执行记录.extend(数据)
        return 执行记录[运行:].decode('utf-8','replace').replace('\r\n','\n')
    def 已按下值(符号值,是否按下中=True):客户端.sendall(struct.pack('>BBHI',4,int(是否按下中),0,符号值))
    def 开始偏移(行):
        运行=len(执行记录)
        for 字符代码 in 行+'\n':
            符号值=0xff0d if 字符代码=='\n' else ord(字符代码) if ord(字符代码)<256 else 0x1000000|ord(字符代码)
            已按下值(符号值);已按下值(符号值,False)
        return 运行
    def 命令壳(行):return 接收消息(b'jkoros-native> ',开始偏移(行))
    def 执行命令(行,预期):
        文本=命令壳(行);assert 预期 in 文本 and 'exit 0' in 文本,(行,文本)
        return 文本
    def 像素列列表():
        客户端.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        红_绿_蓝颜色=bytearray(640*480*3)
        while True:
            分类值=精确值(客户端,1)[0]
            if 分类值==2:continue
            if 分类值==3:
                项目个数=struct.unpack('>I',精确值(客户端,7)[3:])[0];精确值(客户端,项目个数);continue
            assert 分类值==0,分类值
            条目个数=struct.unpack('>H',精确值(客户端,3)[1:])[0]
            for _ in range(条目个数):
                横坐标坐标,Y_按钮坐标,已请求宽度值,已请求高度值,字符设定=struct.unpack('>HHHHi',精确值(客户端,12));assert 字符设定==0,字符设定
                数据=精确值(客户端,已请求宽度值*已请求高度值*4)
                for 行位置 in range(已请求高度值):
                    for 列位置 in range(已请求宽度值):
                        原始数据=(行位置*已请求宽度值+列位置)*4;目标值=((Y_按钮坐标+行位置)*640+横坐标坐标+列位置)*3
                        红_绿_蓝颜色[目标值:目标值+3]=bytes((数据[原始数据+2],数据[原始数据+1],数据[原始数据]))
            if 条目个数:return 红_绿_蓝颜色
    try:
        接收消息(b'TERMINAL READY');接收消息(b'jkoros-native> ',执行记录.rfind(b'TERMINAL READY'))
        端口编号=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',执行记录).group(1))
        客户端=socket.create_connection(('127.0.0.1',端口编号),timeout=10)
        assert 精确值(客户端,12)==b'RFB 003.008\n';客户端.sendall(b'RFB 003.008\n')
        assert 1 in 精确值(客户端,精确值(客户端,1)[0]);客户端.sendall(b'\x01');assert 精确值(客户端,4)==b'\0'*4
        客户端.sendall(b'\x01');初始值=精确值(客户端,24);精确值(客户端,struct.unpack('>I',初始值[20:])[0])
        客户端.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        客户端.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in 命令壳('ftpd start')
        文件传送连接状态=ftplib.FTP();文件传送连接状态.encoding='utf-8';文件传送连接状态.connect('127.0.0.1',文件传送端口编号,timeout=20);文件传送连接状态.login()
        载荷数据数据=('GUI와 FTP 동시 使用值 '+语言+' 😀\n').encode()
        文件传送连接状态.storbinary('STOR 함께.txt',io.BytesIO(载荷数据数据))
        assert 载荷数据数据.decode().strip() in 命令壳('cat /함께.txt')
        已接收个数=bytearray();文件传送连接状态.retrbinary('RETR 함께.txt',已接收个数.extend);assert 已接收个数==载荷数据数据;文件传送连接状态.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        发送列表=命令壳('ls /example')
        assert all(名称 in 发送列表 for 名称 in ('java/','c/','python/','README.md')),发送列表
        if 语言=='java':
            捆绑构建清单=json.loads((项目根/'build/examples/manifest.json').read_text())
            for 路径,条目分 in 捆绑构建清单.items():
                命令壳('cp '+路径+' /example-check.bin')
                内容值=bytearray();文件传送连接状态.retrbinary('RETR example-check.bin',内容值.extend)
                assert len(内容值)==条目分['bytes'] and hashlib.sha256(内容值).hexdigest()==条目分['sha256'],路径
            文件传送连接状态.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            二进制=bytes(range(256))*64
            文件传送连接状态.storbinary('STOR boundary.bin',io.BytesIO(二进制))
            内容值=bytearray();文件传送连接状态.retrbinary('RETR boundary.bin',内容值.extend)
            assert 内容值==二进制 and 'boundary.bin' in 文件传送连接状态.nlst()
            命令壳('cp /boundary.bin /boundary-copy.bin')
            内容值=bytearray();文件传送连接状态.retrbinary('RETR boundary-copy.bin',内容值.extend)
            assert 内容值==二进制
            文件传送连接状态.delete('boundary.bin');文件传送连接状态.delete('boundary-copy.bin')
        assert '输出例' in 命令壳('ls /example/'+语言)
        命令壳('cd /example/'+语言)
        名称表={'java':'JAVA','c':'C','python':'PYTHON'}[语言]
        预期文件=名称表+' 文件: 한글 数据 😀\n'
        if 语言=='java':
            执行命令('javac 输出例.java','Compiled:');执行命令('java 输出例','JAVA 输出: 안녕하세요 😀')
            执行命令('javac 文件例.java','Compiled:');执行命令('java 文件例',预期文件)
            执行命令('java 网络例 {} {}'.format(回显服务器条目.TCP端口,回显服务器条目.UDP端口),'JAVA 네트워크 验证: TCP UDP 한글')
            图形命令='java 绘图例'
        elif 语言=='c':
            for 名称,已转发值,预期 in [('输出','', 'C 输出: 안녕하세요 😀'),('文件','',预期文件),
                    ('네트워크',' '+str(回显服务器条目.UDP端口),'C 네트워크 验证: UDP 한글')]:
                执行命令('cc '+名称+'用例.c -o 执行命令','Compiled native ARM64 ELF:')
                执行命令('./执行命令'+已转发值,预期)
            执行命令('cc 绘图例.c -o 执行命令','Compiled native ARM64 ELF:');图形命令='./执行命令'
        else:
            for 名称,已转发值,预期 in [('输出','','PYTHON 输出: 안녕하세요 😀'),('文件','',预期文件),
                    ('네트워크',' '+str(回显服务器条目.UDP端口),'PYTHON 네트워크 验证: UDP 한글')]:
                执行命令('python '+名称+'用例.py'+已转发值,预期)
            图形命令='python 绘图例.py'
        开始绘图=开始偏移(图形命令)
        文本=接收消息('그림을 확인한 后端值 Enter를 누르세요.\r\n'.encode(),开始绘图)
        assert 名称表+' 그래픽: 빨강 초록 파랑' in 文本 and 'exit 0' not in 文本,文本
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        文件传送连接状态.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        已接收个数=bytearray();文件传送连接状态.retrbinary('RETR 도중.txt',已接收个数.extend);assert 已接收个数==b'FTP DURING GRAPHICS';文件传送连接状态.delete('도중.txt')
        红_绿_蓝颜色=像素列列表()
        for Y_按钮坐标,像素颜色 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            偏移值=(Y_按钮坐标*640+610)*3;assert tuple(红_绿_蓝颜色[偏移值:偏移值+3])==像素颜色,(语言,Y_按钮坐标,tuple(红_绿_蓝颜色[偏移值:偏移值+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(红_绿_蓝颜色)).save(str(结果数据/(语言+'-graphics.png')))
        已按下值(0xff0d);已按下值(0xff0d,False)
        assert 'exit 0' in 接收消息(b'jkoros-native> ',开始绘图)
        if 语言=='java':
            开始窗口=开始偏移('java 窗口例')
            接收消息('GUI 用例 准备: 窗口例'.encode(),开始窗口)
            def 单击值(水平位置,垂直位置):
                for 按钮 in (1,0):客户端.sendall(struct.pack('>BBHH',5,按钮,水平位置,垂直位置))
            time.sleep(.3)
            上一个映像=Image.frombytes('RGB',(640,480),bytes(像素列列表()))
            单击值(160,196)
            for _ in range(2):已按下值(0xff08);已按下值(0xff08,False)
            for 字符值 in '한글':已按下值(0x1000000|ord(字符值));已按下值(0x1000000|ord(字符值),False)
            for 重复状态个数 in (1,2):
                运行=len(执行记录);单击值(180,242)
                接收消息(('GUI 问候例: 안녕하세요, 한글님! ('+str(重复状态个数)+')').encode(),运行)
            time.sleep(.3)
            窗口绘图=Image.frombytes('RGB',(640,480),bytes(像素列列表()))
            assert 上一个映像.crop((110,272,530,300)).tobytes()!=窗口绘图.crop((110,272,530,300)).tobytes()
            窗口绘图.save(str(结果数据/'java-swing.png'))
            运行=len(执行记录);单击值(535,105)
            assert 'exit 0' in 接收消息(b'jkoros-native> ',运行)
        # Download the guest-created bytes through FTP in the same GUI VM.
        文件条目名称={'java':'java.txt','c':'c.txt','python':'python.txt'}[语言]
        命令壳('cp '+文件条目名称+' /有效性校验.txt')
        已接收个数=bytearray();文件传送连接状态.retrbinary('RETR 有效性校验.txt',已接收个数.extend);assert 已接收个数==预期文件.encode()
        命令壳('echo preserved > 输出例.'+('py' if 语言=='python' else 语言))
        assert 'EXAMPLES READY' in 命令壳('example '+语言)
        assert '\npreserved\n' in 命令壳('cat 输出例.'+('py' if 语言=='python' else 语言))
        assert '한/零操作数 键值, Shift+Space 또는 F9' in 命令壳('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in 命令壳('echo GUI NETWORK TOGETHER')
        文件传送连接状态.quit();文件传送连接状态=None;assert 'FTP stopped' in 命令壳('ftpd stop')
        print('PASS '+语言+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if 文件传送连接状态:
            try:文件传送连接状态.close()
            except OSError:pass
        if 客户端:客户端.close()
        进程.terminate()
        try:进程.wait(timeout=8)
        except subprocess.TimeoutExpired:进程.kill();进程.wait()
        就绪选择器.close();进程.stdout.close();(结果数据/(语言+'-serial.log')).write_bytes(执行记录)


def 运行():
    结果数据=项目根/'build/verification/examples';结果数据.mkdir(parents=True,exist_ok=True)
    有效性验证报告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 回显服务器列() as 回显服务器条目:
            for 语言 in ('java','c','python'):
                测试语言(语言,回显服务器条目,结果数据);有效性验证报告['languages'].append(语言)
            预期=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 回显服务器条目.拥有已接收==[(分类值,数据.encode()) for 分类值,数据 in 预期],回显服务器条目.拥有已接收
            有效性验证报告['host_network_payloads']=[{'protocol':分类值,'text':数据.decode()} for 分类值,数据 in 回显服务器条目.拥有已接收]
        有效性验证报告.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(结果数据/'report.json').write_text(json.dumps(有效性验证报告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':运行()
