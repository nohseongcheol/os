"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(रूट_बाटो, 저장소경로, 시언어번역기, 연결편집기, 설정비트, कार्यान्वयन_गर्नुहोस्_आदेश):
    मापन_लगत = रूट_बाटो / 'build/ccompiler'; मापन_लगत.mkdir(exist_ok=True)
    원본자료 = रूट_बाटो / '시언어번역기'
    외부원문 = रूट_बाटो / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = रूट_बाटो / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [सेटिङहरू_मान for सेटिङहरू_मान in 설정비트 if सेटिङहरू_मान != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', रूट_बाटो/'प्रयोगकर्ता', '-I', मापन_लगत, '-isystem', 개발꾸러미/'usr/include']
    कार्यान्वयन_गर्नुहोस्_आदेश([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'स्टार्टअप_समर्थन.c','-o',मापन_लगत/'crt.o'])
    कार्यान्वयन_गर्नुहोस्_आदेश([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',मापन_लगत/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+लगत_राख्नुहोस्.name,लगत_राख्नुहोस्) for लगत_राख्नुहोस् in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+लगत_राख्नुहोस्.name,लगत_राख्नुहोस्) for लगत_राख्नुहोस् in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+लगत_राख्नुहोस्.name,लगत_राख्नुहोस्) for लगत_राख्नुहोस् in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',रूट_बाटो/'build/user/start.o'),('/sdk/lib/crt.o',मापन_लगत/'crt.o'),('/sdk/lib/aot-runtime.o',मापन_लगत/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',रूट_बाटो/'build/libposix-kor-user.a')]
    हेडर_मान=['typedef struct { const char *नाम; const unsigned char *लगत; unsigned आकार; } 번역기자원;']
    for 순번,(_,मार्ग) in enumerate(탑재자료):
        हेडर_मान.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in मार्ग.read_bytes())))
    हेडर_मान.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(नाम,मार्ग) in enumerate(탑재자료): हेडर_मान.append('{%s, 탑재자원_%d, %d},'%(json.dumps(नाम,ensure_ascii=False),순번,मार्ग.stat().st_size))
    हेडर_मान.append('};');(मापन_लगत/'resources.h').write_text('\n'.join(हेडर_मान)+'\n',encoding='utf-8')
    गन्तव्य_फाइलहरू=[]
    for नाम in ('번역기.c','सामान्य_भाषा_चालु_समय_समर्थन.c','चलाउनुहोस्.c','미리번역.c','되돌림.S'):
        गन्तव्य_फाइल=मापन_लगत/(Path(नाम).stem+'.o');गन्तव्य_फाइलहरू.append(गन्तव्य_फाइल)
        कार्यान्वयन_गर्नुहोस्_आदेश([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/नाम,'-o',गन्तव्य_फाइल])
    실행파일=रूट_बाटो/'build/user/cc.elf'
    कार्यान्वयन_गर्नुहोस्_आदेश([연결편집기,'--gc-sections','-T',रूट_बाटो/'प्रयोगकर्ता/लिङ्क_लेआउट.ld','-z','max-page-size=4096','-o',실행파일,
         रूट_बाटो/'build/user/start.o',रूट_बाटो/'build/user/runtime.o']+गन्तव्य_फाइलहरू+
         [रूट_बाटो/'build/user'/नाम for नाम in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
