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
from gnìomhaich_àithne import tilg_freumh


def ruith():
    tomhas_dàta=tilg_freumh/'build/verification/remmina';tomhas_dàta.mkdir(parents=True,exist_ok=True)
    dearbhadh_aithisg={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];roghnaichear=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            mas_fhìor_taisbean=shutil.which('Xvfb')
            if mas_fhìor_taisbean: frithealaiche_VALUE=[mas_fhìor_taisbean]
            else:
                뿌리파일계층=tilg_freumh.parent/'rpi4/build/rootfs'
                frithealaiche_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ruith(argamaid_ARRAY,환경=None,**이름붙인인수):
                LOG_ràgh=(tomhas_dàta/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_ràgh)
                dàta_suidhich=subprocess.Popen(argamaid_ARRAY,env=환경,stdout=LOG_ràgh,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(dàta_suidhich);return dàta_suidhich
            환경=dict(os.environ)
            for Ainm in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Ainm,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(nì_COUNT for nì_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(nì_COUNT)).exists() and not Path('/tmp/.X%d-lock'%nì_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            uidheam_taisbeanaidh=ruith(frithealaiche_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert uidheam_taisbeanaidh.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            aoigh=subprocess.Popen(['python3',str(tilg_freumh/'innealan/gnìomhaich_àithne.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(aoigh);roghnaichear.register(aoigh.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert aoigh.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in roghnaichear.select(.1):
                        dàta=누름값.fileobj.read(65536)
                        if dàta:직렬입출력.extend(dàta)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Pròifil=작업경로/'test.remmina'
            Pròifil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            ruith(['dbus-run-session','--','remmina','-c',str(Pròifil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argamaid_ARRAY):return subprocess.check_output(['xdotool']+list(argamaid_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;uinneag=None
            while time.monotonic()<마감시각:
                lorg_tomhas=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if lorg_tomhas.returncode==0:
                    후보=lorg_tomhas.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    fòcasaichte=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if fòcasaichte.returncode==0:uinneag=후보;break
                time.sleep(.1)
            assert uinneag,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',uinneag,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Iuchair_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',uinneag,str(tomhas_dàta/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # dearbh_dàta Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            tarraing_VALUE=Image.open(str(tomhas_dàta/'remmina-korean.png')).convert('RGB')
            bàr_tiotail=None
            for inghearach_suidhich in range(tarraing_VALUE.height):
                가로들=[가로 for 가로 in range(tarraing_VALUE.width) if tarraing_VALUE.getpixel((가로,inghearach_suidhich))==(32,80,144)]
                if len(가로들)>=500:bàr_tiotail=(min(가로들),inghearach_suidhich);break
            assert bàr_tiotail,'native terminal title bar not found'
            가로,inghearach_suidhich=bàr_tiotail[0]+564,bàr_tiotail[1]+356
            가상입력도구('mousemove','--window',uinneag,str(가로),str(inghearach_suidhich))
            def 화상기다리기(Ainm,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',uinneag,str(tomhas_dàta/Ainm)])
                    bitmap_IMAGE=Image.open(str(tomhas_dàta/Ainm)).convert('RGB')
                    if all(bitmap_IMAGE.getpixel(suidhich)==빛 for suidhich,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Ainm
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,inghearach_suidhich-7),(255,255,255)),((가로+7,inghearach_suidhich+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',uinneag,str(가로-120),str(inghearach_suidhich-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',uinneag,'500','45')
            화상기다리기('remmina-resized.png',[
                ((bàr_tiotail[0]+447,bàr_tiotail[1]+279),(39,49,64)),((가로,inghearach_suidhich),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            dearbhadh_aithisg.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not dearbhadh_aithisg['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(tomhas_dàta/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for dàta_suidhich in reversed(실행과정들):
                if dàta_suidhich.poll() is None:
                    if dàta_suidhich.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(dàta_suidhich.pid,signal.SIGTERM)
                    else:dàta_suidhich.terminate()
                    try:dàta_suidhich.wait(timeout=5)
                    except subprocess.TimeoutExpired:dàta_suidhich.kill();dàta_suidhich.wait()
            roghnaichear.close()
            for faidhle_cur_a_steach in 기록들:faidhle_cur_a_steach.close()
            (tomhas_dàta/'serial.log').write_bytes(직렬입출력)
            (tomhas_dàta/'report.json').write_text(json.dumps(dearbhadh_aithisg,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ruith()
