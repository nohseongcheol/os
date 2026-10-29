"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(રૂટ_પાથ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, અમલ_કરો_આદેશ):
    પરિમાણ_ડેટા = રૂટ_પાથ / 'build/ccompiler'; પરિમાણ_ડેટા.mkdir(exist_ok=True)
    원본자료 = રૂટ_પાથ / '시언어번역기'
    외부원문 = રૂટ_પાથ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = રૂટ_પાથ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [સેટિંગ્સ_મૂલ્ય for સેટિંગ્સ_મૂલ્ય in 설정비트 if સેટિંગ્સ_મૂલ્ય != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', રૂટ_પાથ/'ઉપયોગકર્તા', '-I', પરિમાણ_ડેટા, '-isystem', 개발꾸러미/'usr/include']
    અમલ_કરો_આદેશ([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'બૂટ_સપોર્ટ.c','-o',પરિમાણ_ડેટા/'crt.o'])
    અમલ_કરો_આદેશ([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',પરિમાણ_ડેટા/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ડેટા_સ્થિતિ.name,ડેટા_સ્થિતિ) for ડેટા_સ્થિતિ in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ડેટા_સ્થિતિ.name,ડેટા_સ્થિતિ) for ડેટા_સ્થિતિ in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ડેટા_સ્થિતિ.name,ડેટા_સ્થિતિ) for ડેટા_સ્થિતિ in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',રૂટ_પાથ/'build/user/start.o'),('/sdk/lib/crt.o',પરિમાણ_ડેટા/'crt.o'),('/sdk/lib/aot-runtime.o',પરિમાણ_ડેટા/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',રૂટ_પાથ/'build/libposix-kor-user.a')]
    શીર્ષલેખ_મૂલ્ય=['typedef struct { const char *નામ; const unsigned char *ડેટા; unsigned માપ; } 번역기자원;']
    for 순번,(_,પથ) in enumerate(탑재자료):
        શીર્ષલેખ_મૂલ્ય.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in પથ.read_bytes())))
    શીર્ષલેખ_મૂલ્ય.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(નામ,પથ) in enumerate(탑재자료): શીર્ષલેખ_મૂલ્ય.append('{%s, 탑재자원_%d, %d},'%(json.dumps(નામ,ensure_ascii=False),순번,પથ.stat().st_size))
    શીર્ષલેખ_મૂલ્ય.append('};');(પરિમાણ_ડેટા/'resources.h').write_text('\n'.join(શીર્ષલેખ_મૂલ્ય)+'\n',encoding='utf-8')
    ગંતવ્ય_ફાઇલો=[]
    for નામ in ('번역기.c','સામાન્ય_ભાષા_રનટાઇમ_સપોર્ટ.c','ચલાવો_2.c','미리번역.c','되돌림.S'):
        ગંતવ્ય_ફાઇલ=પરિમાણ_ડેટા/(Path(નામ).stem+'.o');ગંતવ્ય_ફાઇલો.append(ગંતવ્ય_ફાઇલ)
        અમલ_કરો_આદેશ([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/નામ,'-o',ગંતવ્ય_ફાઇલ])
    실행파일=રૂટ_પાથ/'build/user/cc.elf'
    અમલ_કરો_આદેશ([연결편집기,'--gc-sections','-T',રૂટ_પાથ/'ઉપયોગકર્તા/લિંક_લેઆઉટ.ld','-z','max-page-size=4096','-o',실행파일,
         રૂટ_પાથ/'build/user/start.o',રૂટ_પાથ/'build/user/runtime.o']+ગંતવ્ય_ફાઇલો+
         [રૂટ_પાથ/'build/user'/નામ for નામ in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
