#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from thựcThiLệnh import gốcCâyDựÁn

def chạy():
    dữLiệuKếtQuả=gốcCâyDựÁn/'build/verification/coding';dữLiệuKếtQuả.mkdir(parents=True,exist_ok=True)
    báoCáoViệcThẩmĐịnh={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(gốcCâyDựÁn/'CôngCụ/sDKXuất.py')])
        with tarfile.open(str(gốcCâyDựÁn/'dist/jkoros-native-aarch64-sdk.tar.gz')) as góiGộpĐãNén:góiGộpĐãNén.extractall(str(dữLiệuKếtQuả))
        bộCôngCụPhátTriển=dữLiệuKếtQuả/'jkoros-native-sdk'
        danhSáchCácKýHiệu=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(bộCôngCụPhátTriển/'lib/libposix-kor-user.a')]).decode()
        for tên in ('tạoĐiểmCuối','ràngBuộcĐịaChỉ','gửiDữLiệuĐiệnDữLiệu','nhậnDữLiệuĐiệnDữLiệu','mởTệp','đọcDữLiệuTệp','ghiDữLiệuTệp'):
            assert ' T '+tên+'\n' in danhSáchCácKýHiệu, tên
        (dữLiệuKếtQuả/'korean-function-symbols.txt').write_text(danhSáchCácKýHiệu)
        báoCáoViệcThẩmĐịnh['checks'].append('real-korean-c-function-symbols')
        def thựcThiLệnh(tên,đườngDẫn,mảngĐốiSố,dựKiến):
            vịTríDữLiệu=subprocess.run(['python3',str(gốcCâyDựÁn/'CôngCụ/thựcThiTệp.py'),str(đườngDẫn)]+mảngĐốiSố,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (dữLiệuKếtQuả/(tên+'.log')).write_bytes(vịTríDữLiệu.stdout);assert vịTríDữLiệu.returncode==0,vịTríDữLiệu.stdout.decode('utf-8','replace')
            assert dựKiến.encode() in vịTríDữLiệu.stdout,vịTríDữLiệu.stdout;báoCáoViệcThẩmĐịnh['checks'].append(tên)
        for giáTrịHậuTố in ('c','cpp'):
            tệpTệpThựcThi=dữLiệuKếtQuả/('LờiChào-'+giáTrịHậuTố+'.elf')
            subprocess.check_call(['python3',str(bộCôngCụPhátTriển/'compile.py'),str(bộCôngCụPhátTriển/'examples'/('LờiChào.'+giáTrịHậuTố)),'-o',str(tệpTệpThựcThi)])
            thựcThiLệnh('korean-'+giáTrịHậuTố,tệpTệpThựcThi,[],'posix-kor gọiThựcHiện')
        tệpTệpThựcThi=dữLiệuKếtQuả/'giáTrịLuồng.elf'
        subprocess.check_call(['python3',str(bộCôngCụPhátTriển/'compile.py'),str(bộCôngCụPhátTriển/'examples/giáTrịLuồng.c'),'-o',str(tệpTệpThựcThi)])
        thựcThiLệnh('c-stream-queues',tệpTệpThựcThi,[],'C posix-kor 연결형 TruyềnThông PASS')
        thựcThiLệnh('korean-python',gốcCâyDựÁn/'VíDụ/LậpTrìnhHangul/LờiChào.py',['--include',str(gốcCâyDựÁn/'VíDụ/LậpTrìnhHangul/tiếngViệt.py')],'안녕하세요 누리')
        thựcThiLệnh('guest-korean-javac',gốcCâyDựÁn/'VíDụ/LậpTrìnhHangul/LờiChào.java',[],'안녕하세요 · giáTrịTổngCộng=42')
        báoCáoViệcThẩmĐịnh['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(dữLiệuKếtQuả/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':chạy()
