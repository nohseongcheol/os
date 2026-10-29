"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(fréamh_cosán, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Rith_ordú):
    tomhas_sonraí = fréamh_cosán / 'build/ccompiler'; tomhas_sonraí.mkdir(exist_ok=True)
    원본자료 = fréamh_cosán / '시언어번역기'
    외부원문 = fréamh_cosán / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = fréamh_cosán / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Socruithe_VALUE for Socruithe_VALUE in 설정비트 if Socruithe_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', fréamh_cosán/'úsáideoir', '-I', tomhas_sonraí, '-isystem', 개발꾸러미/'usr/include']
    Rith_ordú([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'tosú_Tacaíocht.c','-o',tomhas_sonraí/'crt.o'])
    Rith_ordú([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',tomhas_sonraí/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+sonraí_suíomh.name,sonraí_suíomh) for sonraí_suíomh in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+sonraí_suíomh.name,sonraí_suíomh) for sonraí_suíomh in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+sonraí_suíomh.name,sonraí_suíomh) for sonraí_suíomh in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',fréamh_cosán/'build/user/start.o'),('/sdk/lib/crt.o',tomhas_sonraí/'crt.o'),('/sdk/lib/aot-runtime.o',tomhas_sonraí/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',fréamh_cosán/'build/libposix-kor-user.a')]
    Ceanntásc_VALUE=['typedef struct { const char *Ainm; const unsigned char *sonraí; unsigned Méid; } 번역기자원;']
    for 순번,(_,CONAIR) in enumerate(탑재자료):
        Ceanntásc_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in CONAIR.read_bytes())))
    Ceanntásc_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Ainm,CONAIR) in enumerate(탑재자료): Ceanntásc_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Ainm,ensure_ascii=False),순번,CONAIR.stat().st_size))
    Ceanntásc_VALUE.append('};');(tomhas_sonraí/'resources.h').write_text('\n'.join(Ceanntásc_VALUE)+'\n',encoding='utf-8')
    sprioc_Comhaid=[]
    for Ainm in ('번역기.c','am_rite_teanga_coiteann_Tacaíocht.c','Rith_2.c','미리번역.c','return_traschóiritheoir.S'):
        comhad_sprice=tomhas_sonraí/(Path(Ainm).stem+'.o');sprioc_Comhaid.append(comhad_sprice)
        Rith_ordú([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Ainm,'-o',comhad_sprice])
    실행파일=fréamh_cosán/'build/user/cc.elf'
    Rith_ordú([연결편집기,'--gc-sections','-T',fréamh_cosán/'úsáideoir/Nasc_dáileadh.ld','-z','max-page-size=4096','-o',실행파일,
         fréamh_cosán/'build/user/start.o',fréamh_cosán/'build/user/runtime.o']+sprioc_Comhaid+
         [fréamh_cosán/'build/user'/Ainm for Ainm in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
