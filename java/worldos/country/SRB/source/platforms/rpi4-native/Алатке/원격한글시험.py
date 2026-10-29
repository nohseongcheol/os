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
from Изврши_команда import пројектовати_корен


def Покрени():
    мера_подаци=пројектовати_корен/'build/verification/remmina';мера_подаци.mkdir(parents=True,exist_ok=True)
    провјера_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];бирач=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            виртуелно_екран=shutil.which('Xvfb')
            if виртуелно_екран: сервер_вриједност=[виртуелно_екран]
            else:
                뿌리파일계층=пројектовати_корен.parent/'rpi4/build/rootfs'
                сервер_вриједност=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Покрени(аргумент_низ,радно_окружење=None,**именовани_аргумент):
                евиденција_ред=(мера_подаци/('process-%d.log'%len(기록들))).open('wb');기록들.append(евиденција_ред)
                подаци_позиција=subprocess.Popen(аргумент_низ,env=радно_окружење,stdout=евиденција_ред,stderr=subprocess.STDOUT,**именовани_аргумент)
                실행과정들.append(подаци_позиција);return подаци_позиција
            радно_окружење=dict(os.environ)
            for Назив in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):радно_окружење.pop(Назив,None)
            радно_окружење.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            радно_окружење['DISPLAY']=':'+str(수치)
            екран=Покрени(сервер_вриједност+[радно_окружење['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],радно_окружење=радно_окружење)
            마감시각=time.monotonic()+30
            while True:
                assert екран.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=радно_окружење,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            гост=subprocess.Popen(['python3',str(пројектовати_корен/'Алатке/Изврши_команда.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(гост);бирач.register(гост.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,Помак_вриједност=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[Помак_вриједност:]:
                    assert гост.poll() is None and time.monotonic()<마감시각,직렬입출력[Помак_вриједност:].decode('utf-8','replace')
                    for 누름값,_ in бирач.select(.1):
                        подаци=누름값.fileobj.read(65536)
                        if подаци:직렬입출력.extend(подаци)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            број_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Профил=작업경로/'test.remmina'
            Профил.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%број_порта)
            Покрени(['dbus-run-session','--','remmina','-c',str(Профил)],радно_окружење=радно_окружење,start_new_session=True)
            def 가상입력도구(*аргумент_низ):return subprocess.check_output(['xdotool']+list(аргумент_низ),env=радно_окружење,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Прозор=None
            while time.monotonic()<마감시각:
                тражити_мера=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=радно_окружење,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if тражити_мера.returncode==0:
                    후보=тражити_мера.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    У_фокусу=subprocess.run(['xdotool','windowfocus','--sync',후보],env=радно_окружење,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if У_фокусу.returncode==0:Прозор=후보;break
                time.sleep(.1)
            assert Прозор,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Прозор,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Текст):가상입력도구('type','--clearmodifiers','--delay','50',Текст)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Помак_вриједност=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Помак_вриједност)
            Помак_вриједност=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Помак_вриједност)
            Помак_вриједност=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Кључ_вриједност, Shift+Space 또는 F9'.encode(),Помак_вриједност);기다리기(b'jkoros-native> ',Помак_вриједност)
            Помак_вриједност=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Помак_вриједност)
            subprocess.check_call(['import','-display',радно_окружење['DISPLAY'],'-window',Прозор,str(мера_подаци/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Помак_вриједност)
            # стваран_подаци Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            цртеж_вриједност=Image.open(str(мера_подаци/'remmina-korean.png')).convert('RGB')
            насловна_трака=None
            for вертикала_позиција in range(цртеж_вриједност.height):
                가로들=[가로 for 가로 in range(цртеж_вриједност.width) if цртеж_вриједност.getpixel((가로,вертикала_позиција))==(32,80,144)]
                if len(가로들)>=500:насловна_трака=(min(가로들),вертикала_позиција);break
            assert насловна_трака,'native terminal title bar not found'
            가로,вертикала_позиција=насловна_трака[0]+564,насловна_трака[1]+356
            가상입력도구('mousemove','--window',Прозор,str(가로),str(вертикала_позиција))
            def 화상기다리기(Назив,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',радно_окружење['DISPLAY'],'-window',Прозор,str(мера_подаци/Назив)])
                    растерска_слика_слика=Image.open(str(мера_подаци/Назив)).convert('RGB')
                    if all(растерска_слика_слика.getpixel(Положај)==빛 for Положај,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Назив
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,вертикала_позиција-7),(255,255,255)),((가로+7,вертикала_позиција+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Прозор,str(가로-120),str(вертикала_позиција-80),'mouseup','1')
            time.sleep(.4)
            Помак_вриједност=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Помак_вриједност)
            가상입력도구('mousemove','--window',Прозор,'500','45')
            화상기다리기('remmina-resized.png',[
                ((насловна_трака[0]+447,насловна_трака[1]+279),(39,49,64)),((가로,вертикала_позиција),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=радно_окружење,stderr=subprocess.STDOUT).decode('utf-8','replace')
            провјера_извештај.update(passed=True,display=радно_окружење['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not провјера_извештај['passed'] and 'радно_окружење' in locals() and радно_окружење.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',радно_окружење['DISPLAY'],'-window','root',str(мера_подаци/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for подаци_позиција in reversed(실행과정들):
                if подаци_позиција.poll() is None:
                    if подаци_позиција.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(подаци_позиција.pid,signal.SIGTERM)
                    else:подаци_позиција.terminate()
                    try:подаци_позиција.wait(timeout=5)
                    except subprocess.TimeoutExpired:подаци_позиција.kill();подаци_позиција.wait()
            бирач.close()
            for фајл_унос in 기록들:фајл_унос.close()
            (мера_подаци/'serial.log').write_bytes(직렬입출력)
            (мера_подаци/'report.json').write_text(json.dumps(провјера_извештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Покрени()
