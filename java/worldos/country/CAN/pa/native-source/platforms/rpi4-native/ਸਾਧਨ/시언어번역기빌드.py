"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ਰੂਟ_ਰਸਤਾ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼):
    ਮਾਪ_ਸਮੱਗਰੀ = ਰੂਟ_ਰਸਤਾ / 'build/ccompiler'; ਮਾਪ_ਸਮੱਗਰੀ.mkdir(exist_ok=True)
    원본자료 = ਰੂਟ_ਰਸਤਾ / '시언어번역기'
    외부원문 = ਰੂਟ_ਰਸਤਾ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ਰੂਟ_ਰਸਤਾ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [ਸੈਟਿੰਗਾਂ_ਕੀਮਤ for ਸੈਟਿੰਗਾਂ_ਕੀਮਤ in 설정비트 if ਸੈਟਿੰਗਾਂ_ਕੀਮਤ != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', ਰੂਟ_ਰਸਤਾ/'ਉਪਭੋਗਤਾ', '-I', ਮਾਪ_ਸਮੱਗਰੀ, '-isystem', 개발꾸러미/'usr/include']
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ਬੂਟ_ਸਮਰਥਨ.c','-o',ਮਾਪ_ਸਮੱਗਰੀ/'crt.o'])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ਮਾਪ_ਸਮੱਗਰੀ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.name,ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ) for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.name,ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ) for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.name,ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ) for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ਰੂਟ_ਰਸਤਾ/'build/user/start.o'),('/sdk/lib/crt.o',ਮਾਪ_ਸਮੱਗਰੀ/'crt.o'),('/sdk/lib/aot-runtime.o',ਮਾਪ_ਸਮੱਗਰੀ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ਰੂਟ_ਰਸਤਾ/'build/libposix-kor-user.a')]
    ਸਿਰਲੇਖ_ਕੀਮਤ=['typedef struct { const char *ਨਾਂ; const unsigned char *ਸਮੱਗਰੀ; unsigned ਆਕਾਰ; } 번역기자원;']
    for 순번,(_,ਮਾਰਗ) in enumerate(탑재자료):
        ਸਿਰਲੇਖ_ਕੀਮਤ.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ਮਾਰਗ.read_bytes())))
    ਸਿਰਲੇਖ_ਕੀਮਤ.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ਨਾਂ,ਮਾਰਗ) in enumerate(탑재자료): ਸਿਰਲੇਖ_ਕੀਮਤ.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ਨਾਂ,ensure_ascii=False),순번,ਮਾਰਗ.stat().st_size))
    ਸਿਰਲੇਖ_ਕੀਮਤ.append('};');(ਮਾਪ_ਸਮੱਗਰੀ/'resources.h').write_text('\n'.join(ਸਿਰਲੇਖ_ਕੀਮਤ)+'\n',encoding='utf-8')
    ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ=[]
    for ਨਾਂ in ('번역기.c','ਸਾਧਾਰਨ_ਭਾਸ਼ਾ_ਰਨਟਾਈਮ_ਸਮਰਥਨ.c','ਚਲਾਓ_2.c','미리번역.c','되돌림.S'):
        ਮੰਜਿਲ_ਪਤਾ_ffac9b48=ਮਾਪ_ਸਮੱਗਰੀ/(Path(ਨਾਂ).stem+'.o');ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ.append(ਮੰਜਿਲ_ਪਤਾ_ffac9b48)
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ਨਾਂ,'-o',ਮੰਜਿਲ_ਪਤਾ_ffac9b48])
    실행파일=ਰੂਟ_ਰਸਤਾ/'build/user/cc.elf'
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([연결편집기,'--gc-sections','-T',ਰੂਟ_ਰਸਤਾ/'ਉਪਭੋਗਤਾ/ਲਿੰਕ_ਖਾਕਾ.ld','-z','max-page-size=4096','-o',실행파일,
         ਰੂਟ_ਰਸਤਾ/'build/user/start.o',ਰੂਟ_ਰਸਤਾ/'build/user/runtime.o']+ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ+
         [ਰੂਟ_ਰਸਤਾ/'build/user'/ਨਾਂ for ਨਾਂ in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
