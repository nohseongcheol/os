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
from اجرا_فرمان import نمایش_دادن_جذر


def اجرا_2():
    سنجش_داده_ها=نمایش_دادن_جذر/'build/verification/remmina';سنجش_داده_ها.mkdir(parents=True,exist_ok=True)
    اعتبارسنجی_گزارش={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];انتخاب_کننده=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            مجازی_صفحه_نمایش=shutil.which('Xvfb')
            if مجازی_صفحه_نمایش: سرور_مقدار=[مجازی_صفحه_نمایش]
            else:
                뿌리파일계층=نمایش_دادن_جذر.parent/'rpi4/build/rootfs'
                سرور_مقدار=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def اجرا_2(آرگومان_آرايه,환경=None,**이름붙인인수):
                واقعه_نگار_ردیف=(سنجش_داده_ها/('process-%d.log'%len(기록들))).open('wb');기록들.append(واقعه_نگار_ردیف)
                داده_ها_مرتب_کردن=subprocess.Popen(آرگومان_آرايه,env=환경,stdout=واقعه_نگار_ردیف,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(داده_ها_مرتب_کردن);return داده_ها_مرتب_کردن
            환경=dict(os.environ)
            for نام in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(نام,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            صفحه_نمایش=اجرا_2(سرور_مقدار+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert صفحه_نمایش.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            مهمان=subprocess.Popen(['python3',str(نمایش_دادن_جذر/'ابزارها/اجرا_فرمان.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(مهمان);انتخاب_کننده.register(مهمان.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,جابجایی_لایه_ای_مقدار=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[جابجایی_لایه_ای_مقدار:]:
                    assert مهمان.poll() is None and time.monotonic()<마감시각,직렬입출력[جابجایی_لایه_ای_مقدار:].decode('utf-8','replace')
                    for 누름값,_ in انتخاب_کننده.select(.1):
                        داده_ها=누름값.fileobj.read(65536)
                        if داده_ها:직렬입출력.extend(داده_ها)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            شماره_درگاه=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            نمایه=작업경로/'test.remmina'
            نمایه.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%شماره_درگاه)
            اجرا_2(['dbus-run-session','--','remmina','-c',str(نمایه)],환경=환경,start_new_session=True)
            def 가상입력도구(*آرگومان_آرايه):return subprocess.check_output(['xdotool']+list(آرگومان_آرايه),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;پنجره=None
            while time.monotonic()<마감시각:
                جستجو_سنجش=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if جستجو_سنجش.returncode==0:
                    후보=جستجو_سنجش.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    متمرکز=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if متمرکز.returncode==0:پنجره=후보;break
                time.sleep(.1)
            assert پنجره,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',پنجره,'280','240','click','1')
            time.sleep(1)
            def 글자입력(متن):가상입력도구('type','--clearmodifiers','--delay','50',متن)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            جابجایی_لایه_ای_مقدار=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 کلید_مقدار, Shift+Space 또는 F9'.encode(),جابجایی_لایه_ای_مقدار);기다리기(b'jkoros-native> ',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),جابجایی_لایه_ای_مقدار)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',پنجره,str(سنجش_داده_ها/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',جابجایی_لایه_ای_مقدار)
            # واقعی_داده_ها Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            نقاشی_مقدار=Image.open(str(سنجش_داده_ها/'remmina-korean.png')).convert('RGB')
            نوارعنوان=None
            for عمودی_مرتب_کردن in range(نقاشی_مقدار.height):
                가로들=[가로 for 가로 in range(نقاشی_مقدار.width) if نقاشی_مقدار.getpixel((가로,عمودی_مرتب_کردن))==(32,80,144)]
                if len(가로들)>=500:نوارعنوان=(min(가로들),عمودی_مرتب_کردن);break
            assert نوارعنوان,'native terminal title bar not found'
            가로,عمودی_مرتب_کردن=نوارعنوان[0]+564,نوارعنوان[1]+356
            가상입력도구('mousemove','--window',پنجره,str(가로),str(عمودی_مرتب_کردن))
            def 화상기다리기(نام,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',پنجره,str(سنجش_داده_ها/نام)])
                    نقش_نقطه_ای_عکس=Image.open(str(سنجش_داده_ها/نام)).convert('RGB')
                    if all(نقش_نقطه_ای_عکس.getpixel(مرتب_کردن)==빛 for مرتب_کردن,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+نام
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,عمودی_مرتب_کردن-7),(255,255,255)),((가로+7,عمودی_مرتب_کردن+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',پنجره,str(가로-120),str(عمودی_مرتب_کردن-80),'mouseup','1')
            time.sleep(.4)
            جابجایی_لایه_ای_مقدار=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',جابجایی_لایه_ای_مقدار)
            가상입력도구('mousemove','--window',پنجره,'500','45')
            화상기다리기('remmina-resized.png',[
                ((نوارعنوان[0]+447,نوارعنوان[1]+279),(39,49,64)),((가로,عمودی_مرتب_کردن),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            اعتبارسنجی_گزارش.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not اعتبارسنجی_گزارش['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(سنجش_داده_ها/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for داده_ها_مرتب_کردن in reversed(실행과정들):
                if داده_ها_مرتب_کردن.poll() is None:
                    if داده_ها_مرتب_کردن.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(داده_ها_مرتب_کردن.pid,signal.SIGTERM)
                    else:داده_ها_مرتب_کردن.terminate()
                    try:داده_ها_مرتب_کردن.wait(timeout=5)
                    except subprocess.TimeoutExpired:داده_ها_مرتب_کردن.kill();داده_ها_مرتب_کردن.wait()
            انتخاب_کننده.close()
            for فایل_ورودی in 기록들:فایل_ورودی.close()
            (سنجش_داده_ها/'serial.log').write_bytes(직렬입출력)
            (سنجش_داده_ها/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':اجرا_2()
