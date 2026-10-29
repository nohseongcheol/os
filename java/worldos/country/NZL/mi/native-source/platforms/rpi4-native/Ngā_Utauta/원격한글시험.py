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
from kawe_tono import whakaatu_pūtake


def whakahaere():
    mēhua_raraunga=whakaatu_pūtake/'build/verification/remmina';mēhua_raraunga.mkdir(parents=True,exist_ok=True)
    whakamana_pūrongo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];pūtīpako=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            mariko_whakaatu=shutil.which('Xvfb')
            if mariko_whakaatu: tūmau_uara=[mariko_whakaatu]
            else:
                뿌리파일계층=whakaatu_pūtake.parent/'rpi4/build/rootfs'
                tūmau_uara=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def whakahaere(tohenga_HUĀNGA,환경=None,**이름붙인인수):
                LOG_RECORD=(mēhua_raraunga/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                raraunga_tūranga=subprocess.Popen(tohenga_HUĀNGA,env=환경,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(raraunga_tūranga);return raraunga_tūranga
            환경=dict(os.environ)
            for Ingoa in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Ingoa,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(tuemi_COUNT for tuemi_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(tuemi_COUNT)).exists() and not Path('/tmp/.X%d-lock'%tuemi_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            whakaaturanga=whakahaere(tūmau_uara+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert whakaaturanga.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            manuhiri=subprocess.Popen(['python3',str(whakaatu_pūtake/'Ngā_Utauta/kawe_tono.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(manuhiri);pūtīpako.register(manuhiri.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_uara=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_uara:]:
                    assert manuhiri.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_uara:].decode('utf-8','replace')
                    for 누름값,_ in pūtīpako.select(.1):
                        raraunga=누름값.fileobj.read(65536)
                        if raraunga:직렬입출력.extend(raraunga)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Kōtaha=작업경로/'test.remmina'
            Kōtaha.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            whakahaere(['dbus-run-session','--','remmina','-c',str(Kōtaha)],환경=환경,start_new_session=True)
            def 가상입력도구(*tohenga_HUĀNGA):return subprocess.check_output(['xdotool']+list(tohenga_HUĀNGA),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;matapihi=None
            while time.monotonic()<마감시각:
                Rapu_mēhua=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Rapu_mēhua.returncode==0:
                    후보=Rapu_mēhua.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Arotahi_f7e69dab=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Arotahi_f7e69dab.returncode==0:matapihi=후보;break
                time.sleep(.1)
            assert matapihi,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',matapihi,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Ngā_kupu):가상입력도구('type','--clearmodifiers','--delay','50',Ngā_kupu)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_uara=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_uara)
            OFFSET_uara=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_uara)
            OFFSET_uara=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 kī_uara, Shift+Space 또는 F9'.encode(),OFFSET_uara);기다리기(b'jkoros-native> ',OFFSET_uara)
            OFFSET_uara=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_uara)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',matapihi,str(mēhua_raraunga/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_uara)
            # tūturu_raraunga Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            tātuhi_uara=Image.open(str(mēhua_raraunga/'remmina-korean.png')).convert('RGB')
            pae_taitara=None
            for Poutū_tūranga in range(tātuhi_uara.height):
                가로들=[가로 for 가로 in range(tātuhi_uara.width) if tātuhi_uara.getpixel((가로,Poutū_tūranga))==(32,80,144)]
                if len(가로들)>=500:pae_taitara=(min(가로들),Poutū_tūranga);break
            assert pae_taitara,'native terminal title bar not found'
            가로,Poutū_tūranga=pae_taitara[0]+564,pae_taitara[1]+356
            가상입력도구('mousemove','--window',matapihi,str(가로),str(Poutū_tūranga))
            def 화상기다리기(Ingoa,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',matapihi,str(mēhua_raraunga/Ingoa)])
                    maheremoka_IMAGE=Image.open(str(mēhua_raraunga/Ingoa)).convert('RGB')
                    if all(maheremoka_IMAGE.getpixel(tūranga)==빛 for tūranga,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Ingoa
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Poutū_tūranga-7),(255,255,255)),((가로+7,Poutū_tūranga+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',matapihi,str(가로-120),str(Poutū_tūranga-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_uara=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_uara)
            가상입력도구('mousemove','--window',matapihi,'500','45')
            화상기다리기('remmina-resized.png',[
                ((pae_taitara[0]+447,pae_taitara[1]+279),(39,49,64)),((가로,Poutū_tūranga),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            whakamana_pūrongo.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not whakamana_pūrongo['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(mēhua_raraunga/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for raraunga_tūranga in reversed(실행과정들):
                if raraunga_tūranga.poll() is None:
                    if raraunga_tūranga.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(raraunga_tūranga.pid,signal.SIGTERM)
                    else:raraunga_tūranga.terminate()
                    try:raraunga_tūranga.wait(timeout=5)
                    except subprocess.TimeoutExpired:raraunga_tūranga.kill();raraunga_tūranga.wait()
            pūtīpako.close()
            for kōnae_tāurunga in 기록들:kōnae_tāurunga.close()
            (mēhua_raraunga/'serial.log').write_bytes(직렬입출력)
            (mēhua_raraunga/'report.json').write_text(json.dumps(whakamana_pūrongo,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':whakahaere()
