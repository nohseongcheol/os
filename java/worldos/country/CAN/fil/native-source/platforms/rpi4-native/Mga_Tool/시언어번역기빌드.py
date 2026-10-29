"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(root_path, repository_path, 시언어번역기, 연결편집기, kompigurasyon_Background_Intelligent_Transfer_Service, Mag_execute_utos):
    sukat_data = root_path / 'build/ccompiler'; sukat_data.mkdir(exist_ok=True)
    원본자료 = root_path / '시언어번역기'
    upstream = root_path / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = root_path / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    kompigurasyon_Background_Intelligent_Transfer_Service = [Mga_Setting_VALUE for Mga_Setting_VALUE in kompigurasyon_Background_Intelligent_Transfer_Service if Mga_Setting_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstream, '-I', root_path/'gumagamit', '-I', sukat_data, '-isystem', 개발꾸러미/'usr/include']
    Mag_execute_utos([시언어번역기]+kompigurasyon_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'magbukas_Suporta.c','-o',sukat_data/'crt.o'])
    Mag_execute_utos([시언어번역기]+kompigurasyon_Background_Intelligent_Transfer_Service+['-I',repository_path/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',sukat_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_posisyon.name,data_posisyon) for data_posisyon in sorted((repository_path/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_posisyon.name,data_posisyon) for data_posisyon in sorted((upstream/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_posisyon.name,data_posisyon) for data_posisyon in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',root_path/'build/user/start.o'),('/sdk/lib/crt.o',sukat_data/'crt.o'),('/sdk/lib/aot-runtime.o',sukat_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',root_path/'build/libposix-kor-user.a')]
    Header_VALUE=['typedef struct { const char *pangalan; const unsigned char *data; unsigned sukat_82232621; } 번역기자원;']
    for 순번,(_,path) in enumerate(탑재자료):
        Header_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in path.read_bytes())))
    Header_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(pangalan,path) in enumerate(탑재자료): Header_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(pangalan,ensure_ascii=False),순번,path.stat().st_size))
    Header_VALUE.append('};');(sukat_data/'resources.h').write_text('\n'.join(Header_VALUE)+'\n',encoding='utf-8')
    patutunguhan_Mga_File=[]
    for pangalan in ('번역기.c','common_language_runtime_Suporta.c','run.c','미리번역.c','되돌림.S'):
        patutunguhang_file=sukat_data/(Path(pangalan).stem+'.o');patutunguhan_Mga_File.append(patutunguhang_file)
        Mag_execute_utos([시언어번역기]+kompigurasyon_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/pangalan,'-o',patutunguhang_file])
    실행파일=root_path/'build/user/cc.elf'
    Mag_execute_utos([연결편집기,'--gc-sections','-T',root_path/'gumagamit/Link_Layout.ld','-z','max-page-size=4096','-o',실행파일,
         root_path/'build/user/start.o',root_path/'build/user/runtime.o']+patutunguhan_Mga_File+
         [root_path/'build/user'/pangalan for pangalan in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
