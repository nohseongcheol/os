"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(रूट_पाथ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, पाळो_दिवचो_आदेश):
    मेजप_डेटा = रूट_पाथ / 'build/ccompiler'; मेजप_डेटा.mkdir(exist_ok=True)
    원본자료 = रूट_पाथ / '시언어번역기'
    외부원문 = रूट_पाथ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = रूट_पाथ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [मांडावळी_मोल for मांडावळी_मोल in 설정비트 if मांडावळी_मोल != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', रूट_पाथ/'उपेगकर्तो', '-I', मेजप_डेटा, '-isystem', 개발꾸러미/'usr/include']
    पाळो_दिवचो_आदेश([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'स्टार्टअप_तेंको.c','-o',मेजप_डेटा/'crt.o'])
    पाळो_दिवचो_आदेश([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',मेजप_डेटा/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+डेटा_स्थिती.name,डेटा_स्थिती) for डेटा_स्थिती in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+डेटा_स्थिती.name,डेटा_स्थिती) for डेटा_स्थिती in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+डेटा_स्थिती.name,डेटा_स्थिती) for डेटा_स्थिती in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',रूट_पाथ/'build/user/start.o'),('/sdk/lib/crt.o',मेजप_डेटा/'crt.o'),('/sdk/lib/aot-runtime.o',मेजप_डेटा/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',रूट_पाथ/'build/libposix-kor-user.a')]
    माथाळो_मोल=['typedef struct { const char *नांव; const unsigned char *डेटा; unsigned आवाठ; } 번역기자원;']
    for 순번,(_,पाथ) in enumerate(탑재자료):
        माथाळो_मोल.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in पाथ.read_bytes())))
    माथाळो_मोल.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(नांव,पाथ) in enumerate(탑재자료): माथाळो_मोल.append('{%s, 탑재자원_%d, %d},'%(json.dumps(नांव,ensure_ascii=False),순번,पाथ.stat().st_size))
    माथाळो_मोल.append('};');(मेजप_डेटा/'resources.h').write_text('\n'.join(माथाळो_मोल)+'\n',encoding='utf-8')
    नियुक्त_स्थान_फायली=[]
    for नांव in ('번역기.c','सामान्य_भास_रनटायम_तेंको.c','चलोवप.c','미리번역.c','return_ब्रिज.S'):
        नियुक्त_स्थानाची_फायल=मेजप_डेटा/(Path(नांव).stem+'.o');नियुक्त_स्थान_फायली.append(नियुक्त_स्थानाची_फायल)
        पाळो_दिवचो_आदेश([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/नांव,'-o',नियुक्त_स्थानाची_फायल])
    실행파일=रूट_पाथ/'build/user/cc.elf'
    पाळो_दिवचो_आदेश([연결편집기,'--gc-sections','-T',रूट_पाथ/'उपेगकर्तो/लिंक_रचणाय.ld','-z','max-page-size=4096','-o',실행파일,
         रूट_पाथ/'build/user/start.o',रूट_पाथ/'build/user/runtime.o']+नियुक्त_स्थान_फायली+
         [रूट_पाथ/'build/user'/नांव for नांव in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
