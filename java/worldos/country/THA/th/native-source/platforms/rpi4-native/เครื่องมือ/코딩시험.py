#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ดําเนินการ_คําสั่ง import แสดง_ราก

def เรียกใช้งาน():
    เมตริก_ข้อมูล=แสดง_ราก/'build/verification/coding';เมตริก_ข้อมูล.mkdir(parents=True,exist_ok=True)
    การตรวจสอบความถูกต้อง_รายงาน={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(แสดง_ราก/'เครื่องมือ/개발꾸러미내보내기.py')])
        with tarfile.open(str(แสดง_ราก/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(เมตริก_ข้อมูล))
        ชุดเครื่องมือการพัฒนา=เมตริก_ข้อมูล/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(ชุดเครื่องมือการพัฒนา/'lib/libposix-kor-user.a')]).decode()
        for ชื่อ in ('เปิด_ปลายทาง','ผูก_อีเมล','ส่ง_เดตาแกรม_ข้อมูล','รับ_เดตาแกรม_ข้อมูล','เปิด_แฟ้ม','파일자료읽기','파일자료쓰기'):
            assert ' T '+ชื่อ+'\n' in 심볼목록, ชื่อ
        (เมตริก_ข้อมูล/'korean-function-symbols.txt').write_text(심볼목록)
        การตรวจสอบความถูกต้อง_รายงาน['checks'].append('real-korean-c-function-symbols')
        def ดําเนินการ_คําสั่ง(ชื่อ,เส้นทาง,อาร์กิวเมนต์_อาร์เรย์,예상결과):
            ข้อมูล_ตําแหน่ง=subprocess.run(['python3',str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_แฟ้ม.py'),str(เส้นทาง)]+อาร์กิวเมนต์_อาร์เรย์,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (เมตริก_ข้อมูล/(ชื่อ+'.log')).write_bytes(ข้อมูล_ตําแหน่ง.stdout);assert ข้อมูล_ตําแหน่ง.returncode==0,ข้อมูล_ตําแหน่ง.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ข้อมูล_ตําแหน่ง.stdout,ข้อมูล_ตําแหน่ง.stdout;การตรวจสอบความถูกต้อง_รายงาน['checks'].append(ชื่อ)
        for 뒷부분 in ('c','cpp'):
            แฟ้มปฏิบัติการ=เมตริก_ข้อมูล/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(ชุดเครื่องมือการพัฒนา/'compile.py'),str(ชุดเครื่องมือการพัฒนา/'examples'/('인사.'+뒷부분)),'-o',str(แฟ้มปฏิบัติการ)])
            ดําเนินการ_คําสั่ง('korean-'+뒷부분,แฟ้มปฏิบัติการ,[],'posix-kor 호출')
        แฟ้มปฏิบัติการ=เมตริก_ข้อมูล/'สตรีม_ค่า.elf'
        subprocess.check_call(['python3',str(ชุดเครื่องมือการพัฒนา/'compile.py'),str(ชุดเครื่องมือการพัฒนา/'examples/สตรีม_ค่า.c'),'-o',str(แฟ้มปฏิบัติการ)])
        ดําเนินการ_คําสั่ง('c-stream-queues',แฟ้มปฏิบัติการ,[],'C posix-kor 연결형 통신 PASS')
        ดําเนินการ_คําสั่ง('korean-python',แสดง_ราก/'예제/한글코딩/인사.py',['--include',str(แสดง_ราก/'예제/한글코딩/ไทย.py')],'안녕하세요 누리')
        ดําเนินการ_คําสั่ง('guest-korean-javac',แสดง_ราก/'예제/한글코딩/인사.java',[],'안녕하세요 · รวม_ค่า=42')
        การตรวจสอบความถูกต้อง_รายงาน['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(เมตริก_ข้อมูล/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':เรียกใช้งาน()
