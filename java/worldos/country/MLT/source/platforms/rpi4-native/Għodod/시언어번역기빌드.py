"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(għerq_mogħdija, 저장소경로, 시언어번역기, 연결편집기, 설정비트, eżegwixxa_kmand):
    miżura_data = għerq_mogħdija / 'build/ccompiler'; miżura_data.mkdir(exist_ok=True)
    원본자료 = għerq_mogħdija / '시언어번역기'
    외부원문 = għerq_mogħdija / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = għerq_mogħdija / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Settings_VALUE for Settings_VALUE in 설정비트 if Settings_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', għerq_mogħdija/'utent', '-I', miżura_data, '-isystem', 개발꾸러미/'usr/include']
    eżegwixxa_kmand([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ftuħ_Appoġġ.c','-o',miżura_data/'crt.o'])
    eżegwixxa_kmand([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',miżura_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_pożizzjoni.name,data_pożizzjoni) for data_pożizzjoni in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_pożizzjoni.name,data_pożizzjoni) for data_pożizzjoni in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_pożizzjoni.name,data_pożizzjoni) for data_pożizzjoni in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',għerq_mogħdija/'build/user/start.o'),('/sdk/lib/crt.o',miżura_data/'crt.o'),('/sdk/lib/aot-runtime.o',miżura_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',għerq_mogħdija/'build/libposix-kor-user.a')]
    Intestazzjoni_VALUE=['typedef struct { const char *isem; const unsigned char *data; unsigned daqqas; } 번역기자원;']
    for 순번,(_,mogħdija) in enumerate(탑재자료):
        Intestazzjoni_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in mogħdija.read_bytes())))
    Intestazzjoni_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(isem,mogħdija) in enumerate(탑재자료): Intestazzjoni_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(isem,ensure_ascii=False),순번,mogħdija.stat().st_size))
    Intestazzjoni_VALUE.append('};');(miżura_data/'resources.h').write_text('\n'.join(Intestazzjoni_VALUE)+'\n',encoding='utf-8')
    destinazzjoni_Fajls=[]
    for isem in ('번역기.c','tħaddim_tal_lingwa_komuni_Appoġġ.c','serje.c','미리번역.c','되돌림.S'):
        fajl_tad_destinazzjoni=miżura_data/(Path(isem).stem+'.o');destinazzjoni_Fajls.append(fajl_tad_destinazzjoni)
        eżegwixxa_kmand([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/isem,'-o',fajl_tad_destinazzjoni])
    실행파일=għerq_mogħdija/'build/user/cc.elf'
    eżegwixxa_kmand([연결편집기,'--gc-sections','-T',għerq_mogħdija/'utent/Link_Tqassim.ld','-z','max-page-size=4096','-o',실행파일,
         għerq_mogħdija/'build/user/start.o',għerq_mogħdija/'build/user/runtime.o']+destinazzjoni_Fajls+
         [għerq_mogħdija/'build/user'/isem for isem in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
