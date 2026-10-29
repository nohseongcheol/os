"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ราก_พาธ, ที่เก็บ_พาธ, 시언어번역기, ตัวเชื่อมโยง_เครื่องมือ, 설정비트, ดําเนินการ_คําสั่ง):
    เมตริก_ข้อมูล = ราก_พาธ / 'build/ccompiler'; เมตริก_ข้อมูล.mkdir(exist_ok=True)
    원본자료 = ราก_พาธ / '시언어번역기'
    อัพสตรีม = ราก_พาธ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    ชุดเครื่องมือการพัฒนา = ราก_พาธ / 'vendor/sdk'
    if not (ชุดเครื่องมือการพัฒนา/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((ชุดเครื่องมือการพัฒนา/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [การตั้งค่า_ค่า for การตั้งค่า_ค่า in 설정비트 if การตั้งค่า_ค่า != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', อัพสตรีม, '-I', ราก_พาธ/'ผู้ใช้', '-I', เมตริก_ข้อมูล, '-isystem', ชุดเครื่องมือการพัฒนา/'usr/include']
    ดําเนินการ_คําสั่ง([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'เริ่มต้นระบบ_สนับสนุน.c','-o',เมตริก_ข้อมูล/'crt.o'])
    ดําเนินการ_คําสั่ง([시언어번역기]+설정비트+['-I',ที่เก็บ_พาธ/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',เมตริก_ข้อมูล/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ข้อมูล_ตําแหน่ง.name,ข้อมูล_ตําแหน่ง) for ข้อมูล_ตําแหน่ง in sorted((ที่เก็บ_พาธ/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ข้อมูล_ตําแหน่ง.name,ข้อมูล_ตําแหน่ง) for ข้อมูล_ตําแหน่ง in sorted((อัพสตรีม/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ข้อมูล_ตําแหน่ง.name,ข้อมูล_ตําแหน่ง) for ข้อมูล_ตําแหน่ง in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ราก_พาธ/'build/user/start.o'),('/sdk/lib/crt.o',เมตริก_ข้อมูล/'crt.o'),('/sdk/lib/aot-runtime.o',เมตริก_ข้อมูล/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ราก_พาธ/'build/libposix-kor-user.a')]
    ส่วนหัว_ค่า=['typedef struct { const char *ชื่อ; const unsigned char *ข้อมูล; unsigned ขนาด; } คอมไพเลอร์_ทรัพยากร;']
    for 순번,(_,เส้นทาง) in enumerate(탑재자료):
        ส่วนหัว_ค่า.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in เส้นทาง.read_bytes())))
    ส่วนหัว_ค่า.append('static const คอมไพเลอร์_ทรัพยากร คอมไพเลอร์_แหล่งข้อมูล[] = {')
    for 순번,(ชื่อ,เส้นทาง) in enumerate(탑재자료): ส่วนหัว_ค่า.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ชื่อ,ensure_ascii=False),순번,เส้นทาง.stat().st_size))
    ส่วนหัว_ค่า.append('};');(เมตริก_ข้อมูล/'resources.h').write_text('\n'.join(ส่วนหัว_ค่า)+'\n',encoding='utf-8')
    ปลายทาง_ไฟล์=[]
    for ชื่อ in ('คอมไพเลอร์_เครื่องมือ.c','รันไทม์_สนับสนุน.c','เรียกใช้งาน.c','미리번역.c','ส่งคืน_บริดจ์.S'):
        แฟ้มปลายทาง=เมตริก_ข้อมูล/(Path(ชื่อ).stem+'.o');ปลายทาง_ไฟล์.append(แฟ้มปลายทาง)
        ดําเนินการ_คําสั่ง([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ชื่อ,'-o',แฟ้มปลายทาง])
    แฟ้มปฏิบัติการ=ราก_พาธ/'build/user/cc.elf'
    ดําเนินการ_คําสั่ง([ตัวเชื่อมโยง_เครื่องมือ,'--gc-sections','-T',ราก_พาธ/'ผู้ใช้/ลิงก์_การนําทาง.ld','-z','max-page-size=4096','-o',แฟ้มปฏิบัติการ,
         ราก_พาธ/'build/user/start.o',ราก_พาธ/'build/user/runtime.o']+ปลายทาง_ไฟล์+
         [ราก_พาธ/'build/user'/ชื่อ for ชื่อ in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
