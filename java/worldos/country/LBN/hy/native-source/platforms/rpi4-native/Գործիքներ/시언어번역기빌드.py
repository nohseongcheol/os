"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(արմատ_ուղի, 저장소경로, 시언어번역기, 연결편집기, 설정비트, կատարել_հրաման):
    չափ_տվյալ = արմատ_ուղի / 'build/ccompiler'; չափ_տվյալ.mkdir(exist_ok=True)
    원본자료 = արմատ_ուղի / '시언어번역기'
    외부원문 = արմատ_ուղի / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = արմատ_ուղի / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Կարգավորումներ_արժեք for Կարգավորումներ_արժեք in 설정비트 if Կարգավորումներ_արժեք != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', արմատ_ուղի/'օգտվող', '-I', չափ_տվյալ, '-isystem', 개발꾸러미/'usr/include']
    կատարել_հրաման([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'մեկնարկում_Աջակցում.c','-o',չափ_տվյալ/'crt.o'])
    կատարել_հրաման([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',չափ_տվյալ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+տվյալ_դիրք.name,տվյալ_դիրք) for տվյալ_դիրք in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+տվյալ_դիրք.name,տվյալ_դիրք) for տվյալ_դիրք in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+տվյալ_դիրք.name,տվյալ_դիրք) for տվյալ_դիրք in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',արմատ_ուղի/'build/user/start.o'),('/sdk/lib/crt.o',չափ_տվյալ/'crt.o'),('/sdk/lib/aot-runtime.o',չափ_տվյալ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',արմատ_ուղի/'build/libposix-kor-user.a')]
    Վերնագիր_արժեք=['typedef struct { const char *Անուն; const unsigned char *տվյալ; unsigned Չափս; } 번역기자원;']
    for 순번,(_,Ճանապարհ) in enumerate(탑재자료):
        Վերնագիր_արժեք.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Ճանապարհ.read_bytes())))
    Վերնագիր_արժեք.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Անուն,Ճանապարհ) in enumerate(탑재자료): Վերնագիր_արժեք.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Անուն,ensure_ascii=False),순번,Ճանապարհ.stat().st_size))
    Վերնագիր_արժեք.append('};');(չափ_տվյալ/'resources.h').write_text('\n'.join(Վերնագիր_արժեք)+'\n',encoding='utf-8')
    նպատակակետ_Նիշքեր=[]
    for Անուն in ('번역기.c','սովորական_լեզվի_աշխատաժամանակ_Աջակցում.c','Գործարկել.c','미리번역.c','վերադարձնել_կամուրջ.S'):
        նշանակման_նիշք=չափ_տվյալ/(Path(Անուն).stem+'.o');նպատակակետ_Նիշքեր.append(նշանակման_նիշք)
        կատարել_հրաման([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Անուն,'-o',նշանակման_նիշք])
    실행파일=արմատ_ուղի/'build/user/cc.elf'
    կատարել_հրաման([연결편집기,'--gc-sections','-T',արմատ_ուղի/'օգտվող/կապ_Դասավորություն.ld','-z','max-page-size=4096','-o',실행파일,
         արմատ_ուղի/'build/user/start.o',արմատ_ուղի/'build/user/runtime.o']+նպատակակետ_Նիշքեր+
         [արմատ_ուղի/'build/user'/Անուն for Անուն in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
