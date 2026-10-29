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
from yürütmek_komut import işlem_kök


def çalıştır():
    KR_veri=işlem_kök/'build/verification/remmina';KR_veri.mkdir(parents=True,exist_ok=True)
    doğrulama_Rapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];seçici=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            sanal_monitör=shutil.which('Xvfb')
            if sanal_monitör: sunucu_değer=[sanal_monitör]
            else:
                뿌리파일계층=işlem_kök.parent/'rpi4/build/rootfs'
                sunucu_değer=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def çalıştır(bağımsız_değişken_DİZİ,ortam=None,**adlandırılmış_bağımsız_değişken):
                LOG_KAYIT=(KR_veri/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_KAYIT)
                veri_konum=subprocess.Popen(bağımsız_değişken_DİZİ,env=ortam,stdout=LOG_KAYIT,stderr=subprocess.STDOUT,**adlandırılmış_bağımsız_değişken)
                실행과정들.append(veri_konum);return veri_konum
            ortam=dict(os.environ)
            for İsim in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):ortam.pop(İsim,None)
            ortam.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(öğe_BAĞ_DEĞ_SAY for öğe_BAĞ_DEĞ_SAY in range(80,200) if not Path('/tmp/.X11-unix/X'+str(öğe_BAĞ_DEĞ_SAY)).exists() and not Path('/tmp/.X%d-lock'%öğe_BAĞ_DEĞ_SAY).exists())
            ortam['DISPLAY']=':'+str(수치)
            monitör=çalıştır(sunucu_değer+[ortam['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],ortam=ortam)
            son_tarih_saat=time.monotonic()+30
            while True:
                assert monitör.poll() is None and time.monotonic()<son_tarih_saat,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=ortam,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            konuk=subprocess.Popen(['python3',str(işlem_kök/'araçlar/yürütmek_komut.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(konuk);seçici.register(konuk.stdout,selectors.EVENT_READ)
            def 기다리기(işaret,Ofset_değer=0):
                son_tarih_saat=time.monotonic()+45
                while işaret not in 직렬입출력[Ofset_değer:]:
                    assert konuk.poll() is None and time.monotonic()<son_tarih_saat,직렬입출력[Ofset_değer:].decode('utf-8','replace')
                    for 누름값,_ in seçici.select(.1):
                        veri=누름값.fileobj.read(65536)
                        if veri:직렬입출력.extend(veri)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            bağlantı_noktası_numarası=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%bağlantı_noktası_numarası)
            çalıştır(['dbus-run-session','--','remmina','-c',str(Profil)],ortam=ortam,start_new_session=True)
            def sanal_artış_araç(*bağımsız_değişken_DİZİ):return subprocess.check_output(['xdotool']+list(bağımsız_değişken_DİZİ),env=ortam,stderr=subprocess.STDOUT)
            son_tarih_saat=time.monotonic()+60;Pencere=None
            while time.monotonic()<son_tarih_saat:
                Ara_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=ortam,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Ara_KR.returncode==0:
                    aday=Ara_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Odaklanmış=subprocess.run(['xdotool','windowfocus','--sync',aday],env=ortam,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Odaklanmış.returncode==0:Pencere=aday;break
                time.sleep(.1)
            assert Pencere,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            sanal_artış_araç('mousemove','--window',Pencere,'280','240','click','1')
            time.sleep(1)
            def 글자입력(metin):sanal_artış_araç('type','--clearmodifiers','--delay','50',metin)
            def 누름값(*누름열):sanal_artış_araç('key','--clearmodifiers',*누름열)
            Ofset_değer=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Ofset_değer)
            Ofset_değer=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Ofset_değer)
            Ofset_değer=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/sıfır_işlenen tuş_değer, Shift+Space 또는 F9'.encode(),Ofset_değer);기다리기(b'jkoros-native> ',Ofset_değer)
            Ofset_değer=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Ofset_değer)
            subprocess.check_call(['import','-display',ortam['DISPLAY'],'-window',Pencere,str(KR_veri/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Ofset_değer)
            # fiili_veri Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            çizim_değer=Image.open(str(KR_veri/'remmina-korean.png')).convert('RGB')
            başlık_çubuğu=None
            for Dikey_konum in range(çizim_değer.height):
                가로들=[가로 for 가로 in range(çizim_değer.width) if çizim_değer.getpixel((가로,Dikey_konum))==(32,80,144)]
                if len(가로들)>=500:başlık_çubuğu=(min(가로들),Dikey_konum);break
            assert başlık_çubuğu,'native terminal title bar not found'
            가로,Dikey_konum=başlık_çubuğu[0]+564,başlık_çubuğu[1]+356
            sanal_artış_araç('mousemove','--window',Pencere,str(가로),str(Dikey_konum))
            def 화상기다리기(İsim,점들):
                son_tarih_değer=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',ortam['DISPLAY'],'-window',Pencere,str(KR_veri/İsim)])
                    bit_eşlem_RESİM=Image.open(str(KR_veri/İsim)).convert('RGB')
                    if all(bit_eşlem_RESİM.getpixel(konum)==빛 for konum,빛 in 점들):return
                    assert time.monotonic()<son_tarih_değer,'Remmina framebuffer did not settle: '+İsim
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Dikey_konum-7),(255,255,255)),((가로+7,Dikey_konum+7),(255,255,255))])
            sanal_artış_araç('mousedown','1','mousemove','--window',Pencere,str(가로-120),str(Dikey_konum-80),'mouseup','1')
            time.sleep(.4)
            Ofset_değer=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Ofset_değer)
            sanal_artış_araç('mousemove','--window',Pencere,'500','45')
            화상기다리기('remmina-resized.png',[
                ((başlık_çubuğu[0]+447,başlık_çubuğu[1]+279),(39,49,64)),((가로,Dikey_konum),(24,32,48))])
            if shutil.which('dpkg-query'):
                sürüm_numarası=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                sürüm_numarası=subprocess.check_output(['remmina','--version'],env=ortam,stderr=subprocess.STDOUT).decode('utf-8','replace')
            doğrulama_Rapor.update(passed=True,display=ortam['DISPLAY'],remmina_version=sürüm_numarası,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not doğrulama_Rapor['passed'] and 'ortam' in locals() and ortam.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',ortam['DISPLAY'],'-window','root',str(KR_veri/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for veri_konum in reversed(실행과정들):
                if veri_konum.poll() is None:
                    if veri_konum.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(veri_konum.pid,signal.SIGTERM)
                    else:veri_konum.terminate()
                    try:veri_konum.wait(timeout=5)
                    except subprocess.TimeoutExpired:veri_konum.kill();veri_konum.wait()
            seçici.close()
            for Dosya_girdi in 기록들:Dosya_girdi.close()
            (KR_veri/'serial.log').write_bytes(직렬입출력)
            (KR_veri/'report.json').write_text(json.dumps(doğrulama_Rapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':çalıştır()
