"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ເລກຮາກ_ທາງໂຄຈອນ, ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ, 시언어번역기, 연결편집기, ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ):
    ມາດຕະການ_ຂໍ້ມູນ = ເລກຮາກ_ທາງໂຄຈອນ / 'build/ccompiler'; ມາດຕະການ_ຂໍ້ມູນ.mkdir(exist_ok=True)
    원본자료 = ເລກຮາກ_ທາງໂຄຈອນ / '시언어번역기'
    ຕົ້ນນ້ໍາ = ເລກຮາກ_ທາງໂຄຈອນ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ເລກຮາກ_ທາງໂຄຈອນ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ = [ການຕັ້ງຄ່າ_ຄ່າ for ການຕັ້ງຄ່າ_ຄ່າ in ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ if ການຕັ້ງຄ່າ_ຄ່າ != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', ຕົ້ນນ້ໍາ, '-I', ເລກຮາກ_ທາງໂຄຈອນ/'ຜູ້ໃຊ້', '-I', ມາດຕະການ_ຂໍ້ມູນ, '-isystem', 개발꾸러미/'usr/include']
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([시언어번역기]+ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ການ_ເລີ່ມ_ຕົ້ນ_ການຮອງຮັບ.c','-o',ມາດຕະການ_ຂໍ້ມູນ/'crt.o'])
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([시언어번역기]+ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ+['-I',ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ມາດຕະການ_ຂໍ້ມູນ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.name,ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ) for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in sorted((ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.name,ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ) for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in sorted((ຕົ້ນນ້ໍາ/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.name,ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ) for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ເລກຮາກ_ທາງໂຄຈອນ/'build/user/start.o'),('/sdk/lib/crt.o',ມາດຕະການ_ຂໍ້ມູນ/'crt.o'),('/sdk/lib/aot-runtime.o',ມາດຕະການ_ຂໍ້ມູນ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ເລກຮາກ_ທາງໂຄຈອນ/'build/libposix-kor-user.a')]
    ສ່ວນຫົວ_ຄ່າ=['typedef struct { const char *ຊື່; const unsigned char *ຂໍ້ມູນ; unsigned ຂະ_ຫນາດ; } 번역기자원;']
    for 순번,(_,ທາງໂຄຈອນ) in enumerate(탑재자료):
        ສ່ວນຫົວ_ຄ່າ.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ທາງໂຄຈອນ.read_bytes())))
    ສ່ວນຫົວ_ຄ່າ.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ຊື່,ທາງໂຄຈອນ) in enumerate(탑재자료): ສ່ວນຫົວ_ຄ່າ.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ຊື່,ensure_ascii=False),순번,ທາງໂຄຈອນ.stat().st_size))
    ສ່ວນຫົວ_ຄ່າ.append('};');(ມາດຕະການ_ຂໍ້ມູນ/'resources.h').write_text('\n'.join(ສ່ວນຫົວ_ຄ່າ)+'\n',encoding='utf-8')
    ປາຍທາງ_ໄຟລ໌=[]
    for ຊື່ in ('번역기.c','실행지원.c','ແລ່ນ.c','미리번역.c','되돌림.S'):
        ຟາຍປາຍທາງ=ມາດຕະການ_ຂໍ້ມູນ/(Path(ຊື່).stem+'.o');ປາຍທາງ_ໄຟລ໌.append(ຟາຍປາຍທາງ)
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([시언어번역기]+ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ຊື່,'-o',ຟາຍປາຍທາງ])
    실행파일=ເລກຮາກ_ທາງໂຄຈອນ/'build/user/cc.elf'
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([연결편집기,'--gc-sections','-T',ເລກຮາກ_ທາງໂຄຈອນ/'ຜູ້ໃຊ້/ລິ້ງ_ຮູບແບບ.ld','-z','max-page-size=4096','-o',실행파일,
         ເລກຮາກ_ທາງໂຄຈອນ/'build/user/start.o',ເລກຮາກ_ທາງໂຄຈອນ/'build/user/runtime.o']+ປາຍທາງ_ໄຟລ໌+
         [ເລກຮາກ_ທາງໂຄຈອນ/'build/user'/ຊື່ for ຊື່ in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
