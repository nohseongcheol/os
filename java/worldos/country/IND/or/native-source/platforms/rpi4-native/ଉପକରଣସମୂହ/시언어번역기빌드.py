"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ରୁଟ୍_ପଥ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ):
    ମାପ_ଡାଟା = ରୁଟ୍_ପଥ / 'build/ccompiler'; ମାପ_ଡାଟା.mkdir(exist_ok=True)
    원본자료 = ରୁଟ୍_ପଥ / '시언어번역기'
    외부원문 = ରୁଟ୍_ପଥ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ରୁଟ୍_ପଥ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [ସେଟିଂସ୍_ମୂଲ୍ୟ for ସେଟିଂସ୍_ମୂଲ୍ୟ in 설정비트 if ସେଟିଂସ୍_ମୂଲ୍ୟ != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', ରୁଟ୍_ପଥ/'ଉପଭୋକ୍ତା', '-I', ମାପ_ଡାଟା, '-isystem', 개발꾸러미/'usr/include']
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ଷ୍ଟାର୍ଟଅପ୍_ସମର୍ଥନ.c','-o',ମାପ_ଡାଟା/'crt.o'])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ମାପ_ଡାଟା/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ଡାଟା_ସ୍ଥିତି.name,ଡାଟା_ସ୍ଥିତି) for ଡାଟା_ସ୍ଥିତି in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ଡାଟା_ସ୍ଥିତି.name,ଡାଟା_ସ୍ଥିତି) for ଡାଟା_ସ୍ଥିତି in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ଡାଟା_ସ୍ଥିତି.name,ଡାଟା_ସ୍ଥିତି) for ଡାଟା_ସ୍ଥିତି in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ରୁଟ୍_ପଥ/'build/user/start.o'),('/sdk/lib/crt.o',ମାପ_ଡାଟା/'crt.o'),('/sdk/lib/aot-runtime.o',ମାପ_ଡାଟା/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ରୁଟ୍_ପଥ/'build/libposix-kor-user.a')]
    ଶୀର୍ଷକ_ମୂଲ୍ୟ=['typedef struct { const char *ନାମ; const unsigned char *ଡାଟା; unsigned ଆକାର; } 번역기자원;']
    for 순번,(_,ପଥ) in enumerate(탑재자료):
        ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ପଥ.read_bytes())))
    ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ନାମ,ପଥ) in enumerate(탑재자료): ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ନାମ,ensure_ascii=False),순번,ପଥ.stat().st_size))
    ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('};');(ମାପ_ଡାଟା/'resources.h').write_text('\n'.join(ଶୀର୍ଷକ_ମୂଲ୍ୟ)+'\n',encoding='utf-8')
    ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ=[]
    for ନାମ in ('번역기.c','ସାଧାରଣ_ଭାଷା_ରନ୍_ଟାଇମ୍_ସମର୍ଥନ.c','ଚଳାନ୍ତୁ.c','미리번역.c','되돌림.S'):
        ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍=ମାପ_ଡାଟା/(Path(ନାମ).stem+'.o');ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ.append(ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍)
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ନାମ,'-o',ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍])
    실행파일=ରୁଟ୍_ପଥ/'build/user/cc.elf'
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([연결편집기,'--gc-sections','-T',ରୁଟ୍_ପଥ/'ଉପଭୋକ୍ତା/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld','-z','max-page-size=4096','-o',실행파일,
         ରୁଟ୍_ପଥ/'build/user/start.o',ରୁଟ୍_ପଥ/'build/user/runtime.o']+ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ+
         [ରୁଟ୍_ପଥ/'build/user'/ନାମ for ନାମ in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
