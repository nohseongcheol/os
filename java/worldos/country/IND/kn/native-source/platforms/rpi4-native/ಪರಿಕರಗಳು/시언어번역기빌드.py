"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ಮೂಲ_ಹಾದಿ, ಸಂಗ್ರಹಣೆ_ಹಾದಿ, 시언어번역기, 연결편집기, ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ, ಪೂರೈಸು_ಆದೇಶ):
    ಮಾಪನ_ಡೇಟಾ = ಮೂಲ_ಹಾದಿ / 'build/ccompiler'; ಮಾಪನ_ಡೇಟಾ.mkdir(exist_ok=True)
    원본자료 = ಮೂಲ_ಹಾದಿ / '시언어번역기'
    ಅಪ್_ಸ್ಟ್ರೀಮ್ = ಮೂಲ_ಹಾದಿ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ಮೂಲ_ಹಾದಿ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ = [ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ for ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ in ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ if ಸೆಟ್ಟಿಂಗ್ಸ್_ಮೌಲ್ಯ != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', ಅಪ್_ಸ್ಟ್ರೀಮ್, '-I', ಮೂಲ_ಹಾದಿ/'ಬಳಕೆದಾರ', '-I', ಮಾಪನ_ಡೇಟಾ, '-isystem', 개발꾸러미/'usr/include']
    ಪೂರೈಸು_ಆದೇಶ([시언어번역기]+ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ಬೂಟ್_ಬೆಂಬಲ.c','-o',ಮಾಪನ_ಡೇಟಾ/'crt.o'])
    ಪೂರೈಸು_ಆದೇಶ([시언어번역기]+ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ+['-I',ಸಂಗ್ರಹಣೆ_ಹಾದಿ/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ಮಾಪನ_ಡೇಟಾ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ಡೇಟಾ_ಹುದ್ದೆ.name,ಡೇಟಾ_ಹುದ್ದೆ) for ಡೇಟಾ_ಹುದ್ದೆ in sorted((ಸಂಗ್ರಹಣೆ_ಹಾದಿ/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ಡೇಟಾ_ಹುದ್ದೆ.name,ಡೇಟಾ_ಹುದ್ದೆ) for ಡೇಟಾ_ಹುದ್ದೆ in sorted((ಅಪ್_ಸ್ಟ್ರೀಮ್/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ಡೇಟಾ_ಹುದ್ದೆ.name,ಡೇಟಾ_ಹುದ್ದೆ) for ಡೇಟಾ_ಹುದ್ದೆ in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ಮೂಲ_ಹಾದಿ/'build/user/start.o'),('/sdk/lib/crt.o',ಮಾಪನ_ಡೇಟಾ/'crt.o'),('/sdk/lib/aot-runtime.o',ಮಾಪನ_ಡೇಟಾ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ಮೂಲ_ಹಾದಿ/'build/libposix-kor-user.a')]
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ=['typedef struct { const char *ಹೆಸರು; const unsigned char *ಡೇಟಾ; unsigned ಗಾತ್ರ; } 번역기자원;']
    for 순번,(_,ಮಾರ್ಗ) in enumerate(탑재자료):
        ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ಮಾರ್ಗ.read_bytes())))
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ಹೆಸರು,ಮಾರ್ಗ) in enumerate(탑재자료): ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ಹೆಸರು,ensure_ascii=False),순번,ಮಾರ್ಗ.stat().st_size))
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('};');(ಮಾಪನ_ಡೇಟಾ/'resources.h').write_text('\n'.join(ಶಿರೋಲೇಖ_ಮೌಲ್ಯ)+'\n',encoding='utf-8')
    ಗಮ್ಯಸ್ಥಾನ_ಫೈಲ್_ಗಳು=[]
    for ಹೆಸರು in ('번역기.c','ಸಾಮಾನ್ಯ_ಭಾಷೆಯ_ಚಾಲ್ತಿ_ಸಮಯ_ಬೆಂಬಲ.c','ಚಲಾಯಿಸು_2.c','미리번역.c','되돌림.S'):
        ತಲುಪುವ_ಫೈಲ್=ಮಾಪನ_ಡೇಟಾ/(Path(ಹೆಸರು).stem+'.o');ಗಮ್ಯಸ್ಥಾನ_ಫೈಲ್_ಗಳು.append(ತಲುಪುವ_ಫೈಲ್)
        ಪೂರೈಸು_ಆದೇಶ([시언어번역기]+ಸಂರಚನೆ_ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ಹೆಸರು,'-o',ತಲುಪುವ_ಫೈಲ್])
    실행파일=ಮೂಲ_ಹಾದಿ/'build/user/cc.elf'
    ಪೂರೈಸು_ಆದೇಶ([연결편집기,'--gc-sections','-T',ಮೂಲ_ಹಾದಿ/'ಬಳಕೆದಾರ/ಜೋಡಣೆ_ಲೇಔಟ್.ld','-z','max-page-size=4096','-o',실행파일,
         ಮೂಲ_ಹಾದಿ/'build/user/start.o',ಮೂಲ_ಹಾದಿ/'build/user/runtime.o']+ಗಮ್ಯಸ್ಥಾನ_ಫೈಲ್_ಗಳು+
         [ಮೂಲ_ಹಾದಿ/'build/user'/ಹೆಸರು for ಹೆಸರು in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
