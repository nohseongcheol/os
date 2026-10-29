#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from 执行命令 import 项目根


def 运行():
    结果数据=项目根/'build/verification/remmina';结果数据.mkdir(parents=True,exist_ok=True)
    有效性验证报告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 工作中路径:
        工作中路径=Path(工作中路径);运行中进程列=[];就绪选择器=selectors.DefaultSelector();串行输入输出=bytearray()
        日志记录列=[]
        try:
            虚拟显示操作=shutil.which('Xvfb')
            if 虚拟显示操作: 服务器值=[虚拟显示操作]
            else:
                根文件系统=项目根.parent/'rpi4/build/rootfs'
                服务器值=['qemu-aarch64','-L',str(根文件系统),str(根文件系统/'usr/bin/Xvfb')]
            def 运行(参数数组,环境=None,**已命名参数):
                日志记录=(结果数据/('process-%d.log'%len(日志记录列))).open('wb');日志记录列.append(日志记录)
                数据位置=subprocess.Popen(参数数组,env=环境,stdout=日志记录,stderr=subprocess.STDOUT,**已命名参数)
                运行中进程列.append(数据位置);return 数据位置
            环境=dict(os.environ)
            for 名称 in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):环境.pop(名称,None)
            环境.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(工作中路径/'config'),XDG_DATA_HOME=str(工作中路径/'data'),XDG_CACHE_HOME=str(工作中路径/'cache'))
            数值值=next(项目个数 for 项目个数 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(项目个数)).exists() and not Path('/tmp/.X%d-lock'%项目个数).exists())
            环境['DISPLAY']=':'+str(数值值)
            显示操作设备=运行(服务器值+[环境['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],环境=环境)
            截止时间时间=time.monotonic()+30
            while True:
                assert 显示操作设备.poll() is None and time.monotonic()<截止时间时间,'Xvfb failed; see process-0.log'
                准备状态完成=subprocess.run(['xdotool','getdisplaygeometry'],env=环境,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 准备状态完成.returncode==0:break
                time.sleep(.1)
            客户机=subprocess.Popen(['python3',str(项目根/'工具集/执行命令.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            运行中进程列.append(客户机);就绪选择器.register(客户机.stdout,selectors.EVENT_READ)
            def 等待(标记,偏移值=0):
                截止时间时间=time.monotonic()+45
                while 标记 not in 串行输入输出[偏移值:]:
                    assert 客户机.poll() is None and time.monotonic()<截止时间时间,串行输入输出[偏移值:].decode('utf-8','replace')
                    for 已按下值,_ in 就绪选择器.select(.1):
                        数据=已按下值.fileobj.read(65536)
                        if 数据:串行输入输出.extend(数据)
            等待(b'TERMINAL READY');等待(b'jkoros-native> ',串行输入输出.rfind(b'TERMINAL READY'))
            端口编号=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',串行输入输出).group(1))
            配置档=工作中路径/'test.remmina'
            配置档.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%端口编号)
            运行(['dbus-run-session','--','remmina','-c',str(配置档)],环境=环境,start_new_session=True)
            def 虚拟输入工具(*参数数组):return subprocess.check_output(['xdotool']+list(参数数组),env=环境,stderr=subprocess.STDOUT)
            截止时间时间=time.monotonic()+60;窗口=None
            while time.monotonic()<截止时间时间:
                搜索结果=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=环境,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if 搜索结果.returncode==0:
                    候选=搜索结果.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    已聚焦=subprocess.run(['xdotool','windowfocus','--sync',候选],env=环境,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if 已聚焦.returncode==0:窗口=候选;break
                time.sleep(.1)
            assert 窗口,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            虚拟输入工具('mousemove','--window',窗口,'280','240','click','1')
            time.sleep(1)
            def 已输入字符(文本):虚拟输入工具('type','--clearmodifiers','--delay','50',文本)
            def 已按下值(*已按下键列):虚拟输入工具('key','--clearmodifiers',*已按下键列)
            偏移值=len(串行输入输出);已输入字符('echo ');已按下值('F9');已输入字符('dkssudgktpdy gksrmf');已按下值('F9','Return')
            等待('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(串行输入输出);已输入字符('echo ');已按下值('shift+space');已输入字符('rhk rkqtk');已按下值('shift+space','Return')
            等待('\r\n과 갑사\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(串行输入输出);已输入字符('help ko');已按下值('Return')
            等待('한/零操作数 键值, Shift+Space 또는 F9'.encode(),偏移值);等待(b'jkoros-native> ',偏移值)
            偏移值=len(串行输入输出);已输入字符('echo ');已按下值('F9');已输入字符('gksrmf dlfr')
            等待('읽'.encode(),偏移值)
            subprocess.check_call(['import','-display',环境['DISPLAY'],'-window',窗口,str(结果数据/'remmina-korean.png')])
            已按下值('F9','Return')
            等待(b'jkoros-native> ',偏移值)
            # 实际数据 Remmina의 屏幕 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            绘图=Image.open(str(结果数据/'remmina-korean.png')).convert('RGB')
            标题栏=None
            for 垂直位置 in range(绘图.height):
                水平位置列=[水平位置 for 水平位置 in range(绘图.width) if 绘图.getpixel((水平位置,垂直位置))==(32,80,144)]
                if len(水平位置列)>=500:标题栏=(min(水平位置列),垂直位置);break
            assert 标题栏,'native terminal title bar not found'
            水平位置,垂直位置=标题栏[0]+564,标题栏[1]+356
            虚拟输入工具('mousemove','--window',窗口,str(水平位置),str(垂直位置))
            def 等待状态用于位图(名称,点列列表):
                截止时间值=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',环境['DISPLAY'],'-window',窗口,str(结果数据/名称)])
                    位图映像=Image.open(str(结果数据/名称)).convert('RGB')
                    if all(位图映像.getpixel(位置)==颜色 for 位置,颜色 in 点列列表):return
                    assert time.monotonic()<截止时间值,'Remmina framebuffer did not settle: '+名称
                    time.sleep(.1)
            等待状态用于位图('remmina-resize-cursor.png',[
                ((水平位置-7,垂直位置-7),(255,255,255)),((水平位置+7,垂直位置+7),(255,255,255))])
            虚拟输入工具('mousedown','1','mousemove','--window',窗口,str(水平位置-120),str(垂直位置-80),'mouseup','1')
            time.sleep(.4)
            偏移值=len(串行输入输出);已输入字符('terminal size');已按下值('Return')
            等待(b'TERMINAL SIZE 53x14\r\n',偏移值)
            虚拟输入工具('mousemove','--window',窗口,'500','45')
            等待状态用于位图('remmina-resized.png',[
                ((标题栏[0]+447,标题栏[1]+279),(39,49,64)),((水平位置,垂直位置),(24,32,48))])
            if shutil.which('dpkg-query'):
                版本编号=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                版本编号=subprocess.check_output(['remmina','--version'],env=环境,stderr=subprocess.STDOUT).decode('utf-8','replace')
            有效性验证报告.update(passed=True,display=环境['DISPLAY'],remmina_version=版本编号,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not 有效性验证报告['passed'] and '环境' in locals() and 环境.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',环境['DISPLAY'],'-window','root',str(结果数据/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for 数据位置 in reversed(运行中进程列):
                if 数据位置.poll() is None:
                    if 数据位置.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(数据位置.pid,signal.SIGTERM)
                    else:数据位置.terminate()
                    try:数据位置.wait(timeout=5)
                    except subprocess.TimeoutExpired:数据位置.kill();数据位置.wait()
            就绪选择器.close()
            for 文件条目 in 日志记录列:文件条目.close()
            (结果数据/'serial.log').write_bytes(串行输入输出)
            (结果数据/'report.json').write_text(json.dumps(有效性验证报告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':运行()
