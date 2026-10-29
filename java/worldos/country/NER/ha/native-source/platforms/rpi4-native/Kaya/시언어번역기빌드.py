"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(기준경로, matattara_Hanyar_shiga, 시언어번역기, 연결편집기, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, gudanar_Umarni):
    결과자료 = 기준경로 / 'build/ccompiler'; 결과자료.mkdir(exist_ok=True)
    원본자료 = 기준경로 / '시언어번역기'
    tushe_99f91985 = 기준경로 / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = 기준경로 / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango = [Saituna_Daraja for Saituna_Daraja in saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango if Saituna_Daraja != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', tushe_99f91985, '-I', 기준경로/'Mai_anfani_da_kwamfuta', '-I', 결과자료, '-isystem', 개발꾸러미/'usr/include']
    gudanar_Umarni([시언어번역기]+saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'Matakan_kunna_kwamfuta_taimako.c','-o',결과자료/'crt.o'])
    gudanar_Umarni([시언어번역기]+saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango+['-I',matattara_Hanyar_shiga/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',결과자료/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((matattara_Hanyar_shiga/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((tushe_99f91985/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',기준경로/'build/user/start.o'),('/sdk/lib/crt.o',결과자료/'crt.o'),('/sdk/lib/aot-runtime.o',결과자료/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',기준경로/'build/libposix-kor-user.a')]
    Kai_Daraja=['typedef struct { const char *Suna; const unsigned char *Tarin_bayani; unsigned Girma; } 번역기자원;']
    for 순번,(_,Hanyar_shiga) in enumerate(탑재자료):
        Kai_Daraja.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Hanyar_shiga.read_bytes())))
    Kai_Daraja.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Suna,Hanyar_shiga) in enumerate(탑재자료): Kai_Daraja.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Suna,ensure_ascii=False),순번,Hanyar_shiga.stat().st_size))
    Kai_Daraja.append('};');(결과자료/'resources.h').write_text('\n'.join(Kai_Daraja)+'\n',encoding='utf-8')
    Zangon_ƙarshe_Fayiloli=[]
    for Suna in ('번역기.c','lokacin_bude_yaren_gama_gari_taimako.c','Tafiyar_da.c','미리번역.c','되돌림.S'):
        Fayil_na_zangon_ƙarshe=결과자료/(Path(Suna).stem+'.o');Zangon_ƙarshe_Fayiloli.append(Fayil_na_zangon_ƙarshe)
        gudanar_Umarni([시언어번역기]+saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Suna,'-o',Fayil_na_zangon_ƙarshe])
    실행파일=기준경로/'build/user/cc.elf'
    gudanar_Umarni([연결편집기,'--gc-sections','-T',기준경로/'Mai_anfani_da_kwamfuta/Kafa_Zagaye.ld','-z','max-page-size=4096','-o',실행파일,
         기준경로/'build/user/start.o',기준경로/'build/user/runtime.o']+Zangon_ƙarshe_Fayiloli+
         [기준경로/'build/user'/Suna for Suna in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
