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
from կատարել_հրաման import արձակել_արմատ


def Գործարկել():
    չափ_տվյալ=արձակել_արմատ/'build/verification/remmina';չափ_տվյալ.mkdir(parents=True,exist_ok=True)
    վավերացում_զեկույց={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];ընտրիչ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            վիրտուալ_ցուցադրել=shutil.which('Xvfb')
            if վիրտուալ_ցուցադրել: սպասարկիչ_արժեք=[վիրտուալ_ցուցադրել]
            else:
                뿌리파일계층=արձակել_արմատ.parent/'rpi4/build/rootfs'
                սպասարկիչ_արժեք=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Գործարկել(արգումենտ_ԶԱՆԳՎԱԾ,환경=None,**이름붙인인수):
                մատյան_տող=(չափ_տվյալ/('process-%d.log'%len(기록들))).open('wb');기록들.append(մատյան_տող)
                տվյալ_դիրք=subprocess.Popen(արգումենտ_ԶԱՆԳՎԱԾ,env=환경,stdout=մատյան_տող,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(տվյալ_դիրք);return տվյալ_դիրք
            환경=dict(os.environ)
            for Անուն in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Անուն,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ցուցադրիչ=Գործարկել(սպասարկիչ_արժեք+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ցուցադրիչ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            հյուր=subprocess.Popen(['python3',str(արձակել_արմատ/'Գործիքներ/կատարել_հրաման.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(հյուր);ընտրիչ.register(հյուր.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,Տեղաշարժում_արժեք=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[Տեղաշարժում_արժեք:]:
                    assert հյուր.poll() is None and time.monotonic()<마감시각,직렬입출력[Տեղաշարժում_արժեք:].decode('utf-8','replace')
                    for 누름값,_ in ընտրիչ.select(.1):
                        տվյալ=누름값.fileobj.read(65536)
                        if տվյալ:직렬입출력.extend(տվյալ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Հատկագիր=작업경로/'test.remmina'
            Հատկագիր.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            Գործարկել(['dbus-run-session','--','remmina','-c',str(Հատկագիր)],환경=환경,start_new_session=True)
            def 가상입력도구(*արգումենտ_ԶԱՆԳՎԱԾ):return subprocess.check_output(['xdotool']+list(արգումենտ_ԶԱՆԳՎԱԾ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;պատուհան=None
            while time.monotonic()<마감시각:
                որոնել_չափ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if որոնել_չափ.returncode==0:
                    후보=որոնել_չափ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Կարեւոր_գործարքներ=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Կարեւոր_գործարքներ.returncode==0:պատուհան=후보;break
                time.sleep(.1)
            assert պատուհան,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',պատուհան,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Տեքստ):가상입력도구('type','--clearmodifiers','--delay','50',Տեքստ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Տեղաշարժում_արժեք=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Տեղաշարժում_արժեք)
            Տեղաշարժում_արժեք=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Տեղաշարժում_արժեք)
            Տեղաշարժում_արժեք=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ստեղն_արժեք, Shift+Space 또는 F9'.encode(),Տեղաշարժում_արժեք);기다리기(b'jkoros-native> ',Տեղաշարժում_արժեք)
            Տեղաշարժում_արժեք=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Տեղաշարժում_արժեք)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',պատուհան,str(չափ_տվյալ/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Տեղաշարժում_արժեք)
            # իրական_տվյալ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            նկար_արժեք_c143fe9e=Image.open(str(չափ_տվյալ/'remmina-korean.png')).convert('RGB')
            անվանագոտի=None
            for Ուղղահայաց_դիրք in range(նկար_արժեք_c143fe9e.height):
                가로들=[가로 for 가로 in range(նկար_արժեք_c143fe9e.width) if նկար_արժեք_c143fe9e.getpixel((가로,Ուղղահայաց_դիրք))==(32,80,144)]
                if len(가로들)>=500:անվանագոտի=(min(가로들),Ուղղահայաց_դիրք);break
            assert անվանագոտի,'native terminal title bar not found'
            가로,Ուղղահայաց_դիրք=անվանագոտի[0]+564,անվանագոտի[1]+356
            가상입력도구('mousemove','--window',պատուհան,str(가로),str(Ուղղահայաց_դիրք))
            def 화상기다리기(Անուն,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',պատուհան,str(չափ_տվյալ/Անուն)])
                    կետապատկեր_նկար=Image.open(str(չափ_տվյալ/Անուն)).convert('RGB')
                    if all(կետապատկեր_նկար.getpixel(Դիրք)==빛 for Դիրք,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Անուն
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Ուղղահայաց_դիրք-7),(255,255,255)),((가로+7,Ուղղահայաց_դիրք+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',պատուհան,str(가로-120),str(Ուղղահայաց_դիրք-80),'mouseup','1')
            time.sleep(.4)
            Տեղաշարժում_արժեք=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Տեղաշարժում_արժեք)
            가상입력도구('mousemove','--window',պատուհան,'500','45')
            화상기다리기('remmina-resized.png',[
                ((անվանագոտի[0]+447,անվանագոտի[1]+279),(39,49,64)),((가로,Ուղղահայաց_դիրք),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            վավերացում_զեկույց.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not վավերացում_զեկույց['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(չափ_տվյալ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for տվյալ_դիրք in reversed(실행과정들):
                if տվյալ_դիրք.poll() is None:
                    if տվյալ_դիրք.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(տվյալ_դիրք.pid,signal.SIGTERM)
                    else:տվյալ_դիրք.terminate()
                    try:տվյալ_դիրք.wait(timeout=5)
                    except subprocess.TimeoutExpired:տվյալ_դիրք.kill();տվյալ_դիրք.wait()
            ընտրիչ.close()
            for նիշք_մուտքագրում in 기록들:նիշք_մուտքագրում.close()
            (չափ_տվյալ/'serial.log').write_bytes(직렬입출력)
            (չափ_տվյալ/'report.json').write_text(json.dumps(վավերացում_զեկույց,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Գործարկել()
