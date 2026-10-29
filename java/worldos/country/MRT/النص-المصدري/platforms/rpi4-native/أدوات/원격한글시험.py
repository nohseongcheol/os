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
from ينفذ_أمر import يعرض_جذر


def تشغيل():
    مقياس_بيانات=يعرض_جذر/'build/verification/remmina';مقياس_بيانات.mkdir(parents=True,exist_ok=True)
    التحقق_من_صحة_إبلاغ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];محدد=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ظاهري_يعرض=shutil.which('Xvfb')
            if ظاهري_يعرض: خادم_قيمة=[ظاهري_يعرض]
            else:
                뿌리파일계층=يعرض_جذر.parent/'rpi4/build/rootfs'
                خادم_قيمة=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def تشغيل(وسيطة_صفيف,بيئة_التشغيل=None,**وسيطات_مسمّاة):
                سجل_سجل=(مقياس_بيانات/('process-%d.log'%len(기록들))).open('wb');기록들.append(سجل_سجل)
                بيانات_منصب=subprocess.Popen(وسيطة_صفيف,env=بيئة_التشغيل,stdout=سجل_سجل,stderr=subprocess.STDOUT,**وسيطات_مسمّاة)
                실행과정들.append(بيانات_منصب);return بيانات_منصب
            بيئة_التشغيل=dict(os.environ)
            for اسم in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):بيئة_التشغيل.pop(اسم,None)
            بيئة_التشغيل.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            بيئة_التشغيل['DISPLAY']=':'+str(수치)
            جهاز_عرض=تشغيل(خادم_قيمة+[بيئة_التشغيل['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],بيئة_التشغيل=بيئة_التشغيل)
            موعد_نهائي_وقت=time.monotonic()+30
            while True:
                assert جهاز_عرض.poll() is None and time.monotonic()<موعد_نهائي_وقت,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=بيئة_التشغيل,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ضيف=subprocess.Popen(['python3',str(يعرض_جذر/'أدوات/ينفذ_أمر.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ضيف);محدد.register(ضيف.stdout,selectors.EVENT_READ)
            def 기다리기(علامة,إزاحة_قيمة=0):
                موعد_نهائي_وقت=time.monotonic()+45
                while علامة not in 직렬입출력[إزاحة_قيمة:]:
                    assert ضيف.poll() is None and time.monotonic()<موعد_نهائي_وقت,직렬입출력[إزاحة_قيمة:].decode('utf-8','replace')
                    for 누름값,_ in محدد.select(.1):
                        بيانات=누름값.fileobj.read(65536)
                        if بيانات:직렬입출력.extend(بيانات)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            رقم_المنفذ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            يحلل=작업경로/'test.remmina'
            يحلل.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%رقم_المنفذ)
            تشغيل(['dbus-run-session','--','remmina','-c',str(يحلل)],بيئة_التشغيل=بيئة_التشغيل,start_new_session=True)
            def ظاهري_إدخال_أداة(*وسيطة_صفيف):return subprocess.check_output(['xdotool']+list(وسيطة_صفيف),env=بيئة_التشغيل,stderr=subprocess.STDOUT)
            موعد_نهائي_وقت=time.monotonic()+60;نافذة=None
            while time.monotonic()<موعد_نهائي_وقت:
                بحث_مقياس=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=بيئة_التشغيل,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if بحث_مقياس.returncode==0:
                    후보=بحث_مقياس.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    المركّز_عليه=subprocess.run(['xdotool','windowfocus','--sync',후보],env=بيئة_التشغيل,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if المركّز_عليه.returncode==0:نافذة=후보;break
                time.sleep(.1)
            assert نافذة,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            ظاهري_إدخال_أداة('mousemove','--window',نافذة,'280','240','click','1')
            time.sleep(1)
            def 글자입력(نص):ظاهري_إدخال_أداة('type','--clearmodifiers','--delay','50',نص)
            def 누름값(*누름열):ظاهري_إدخال_أداة('key','--clearmodifiers',*누름열)
            إزاحة_قيمة=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),إزاحة_قيمة)
            إزاحة_قيمة=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),إزاحة_قيمة)
            إزاحة_قيمة=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/صفر_مُعامل مفتاح_قيمة, Shift+Space 또는 F9'.encode(),إزاحة_قيمة);기다리기(b'jkoros-native> ',إزاحة_قيمة)
            إزاحة_قيمة=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),إزاحة_قيمة)
            subprocess.check_call(['import','-display',بيئة_التشغيل['DISPLAY'],'-window',نافذة,str(مقياس_بيانات/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',إزاحة_قيمة)
            # الفعلي_بيانات Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            رسم_قيمة=Image.open(str(مقياس_بيانات/'remmina-korean.png')).convert('RGB')
            شريط_العناوين=None
            for عمودي_منصب in range(رسم_قيمة.height):
                가로들=[가로 for 가로 in range(رسم_قيمة.width) if رسم_قيمة.getpixel((가로,عمودي_منصب))==(32,80,144)]
                if len(가로들)>=500:شريط_العناوين=(min(가로들),عمودي_منصب);break
            assert شريط_العناوين,'native terminal title bar not found'
            가로,عمودي_منصب=شريط_العناوين[0]+564,شريط_العناوين[1]+356
            ظاهري_إدخال_أداة('mousemove','--window',نافذة,str(가로),str(عمودي_منصب))
            def 화상기다리기(اسم,점들):
                موعد_نهائي_قيمة=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',بيئة_التشغيل['DISPLAY'],'-window',نافذة,str(مقياس_بيانات/اسم)])
                    صورة_نقطية_صورة=Image.open(str(مقياس_بيانات/اسم)).convert('RGB')
                    if all(صورة_نقطية_صورة.getpixel(موضع)==빛 for موضع,빛 in 점들):return
                    assert time.monotonic()<موعد_نهائي_قيمة,'Remmina framebuffer did not settle: '+اسم
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,عمودي_منصب-7),(255,255,255)),((가로+7,عمودي_منصب+7),(255,255,255))])
            ظاهري_إدخال_أداة('mousedown','1','mousemove','--window',نافذة,str(가로-120),str(عمودي_منصب-80),'mouseup','1')
            time.sleep(.4)
            إزاحة_قيمة=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',إزاحة_قيمة)
            ظاهري_إدخال_أداة('mousemove','--window',نافذة,'500','45')
            화상기다리기('remmina-resized.png',[
                ((شريط_العناوين[0]+447,شريط_العناوين[1]+279),(39,49,64)),((가로,عمودي_منصب),(24,32,48))])
            if shutil.which('dpkg-query'):
                رقم_الإصدار=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                رقم_الإصدار=subprocess.check_output(['remmina','--version'],env=بيئة_التشغيل,stderr=subprocess.STDOUT).decode('utf-8','replace')
            التحقق_من_صحة_إبلاغ.update(passed=True,display=بيئة_التشغيل['DISPLAY'],remmina_version=رقم_الإصدار,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not التحقق_من_صحة_إبلاغ['passed'] and 'بيئة_التشغيل' in locals() and بيئة_التشغيل.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',بيئة_التشغيل['DISPLAY'],'-window','root',str(مقياس_بيانات/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for بيانات_منصب in reversed(실행과정들):
                if بيانات_منصب.poll() is None:
                    if بيانات_منصب.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(بيانات_منصب.pid,signal.SIGTERM)
                    else:بيانات_منصب.terminate()
                    try:بيانات_منصب.wait(timeout=5)
                    except subprocess.TimeoutExpired:بيانات_منصب.kill();بيانات_منصب.wait()
            محدد.close()
            for ملف_إدخال_3d0c1245 in 기록들:ملف_إدخال_3d0c1245.close()
            (مقياس_بيانات/'serial.log').write_bytes(직렬입출력)
            (مقياس_بيانات/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':تشغيل()
