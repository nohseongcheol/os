#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ

def ແລ່ນ():
    ມາດຕະການ_ຂໍ້ມູນ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/coding';ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True,exist_ok=True)
    ໃຊ້ໄດ້_ລາຍງານ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/개발꾸러미내보내기.py')])
        with tarfile.open(str(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(ມາດຕະການ_ຂໍ້ມູນ))
        개발꾸러미=ມາດຕະການ_ຂໍ້ມູນ/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for ຊື່ in ('통신종단점만들기','ຜູກ_ມັດ_ອີເມວ','자료전문보내기','자료전문받기','ສ້າງ_ຟາຍ','파일자료읽기','ຂຽນ_ຟາຍ_ຂໍ້ມູນ'):
            assert ' T '+ຊື່+'\n' in 심볼목록, ຊື່
        (ມາດຕະການ_ຂໍ້ມູນ/'korean-function-symbols.txt').write_text(심볼목록)
        ໃຊ້ໄດ້_ລາຍງານ['checks'].append('real-korean-c-function-symbols')
        def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຊື່,ທາງໂຄຈອນ,ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ,예상결과):
            ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ=subprocess.run(['python3',str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py'),str(ທາງໂຄຈອນ)]+ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ມາດຕະການ_ຂໍ້ມູນ/(ຊື່+'.log')).write_bytes(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout);assert ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.returncode==0,ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout,ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stdout;ໃຊ້ໄດ້_ລາຍງານ['checks'].append(ຊື່)
        for 뒷부분 in ('c','cpp'):
            실행파일=ມາດຕະການ_ຂໍ້ມູນ/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=ມາດຕະການ_ຂໍ້ມູນ/'ສະຕຣີມ_ຄ່າ.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ສະຕຣີມ_ຄ່າ.c'),'-o',str(실행파일)])
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('korean-python',ໂຄງ_ການ_ເລກຮາກ/'예제/한글코딩/인사.py',['--include',str(ໂຄງ_ການ_ເລກຮາກ/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('guest-korean-javac',ໂຄງ_ການ_ເລກຮາກ/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        ໃຊ້ໄດ້_ລາຍງານ['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ມາດຕະການ_ຂໍ້ມູນ/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ແລ່ນ()
