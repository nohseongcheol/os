"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ስር_ዱካ, ማከማቻ_ዱካ, 시언어번역기, 연결편집기, ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት, ፈጽም_ትእዛዝ):
    ልኬት_ውሂብ = ስር_ዱካ / 'build/ccompiler'; ልኬት_ውሂብ.mkdir(exist_ok=True)
    원본자료 = ስር_ዱካ / '시언어번역기'
    ሽቅብ_ፍሰት = ስር_ዱካ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ስር_ዱካ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት = [ቅንብሮች_እሴት for ቅንብሮች_እሴት in ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት if ቅንብሮች_እሴት != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', ሽቅብ_ፍሰት, '-I', ስር_ዱካ/'ተጠቃሚ', '-I', ልኬት_ውሂብ, '-isystem', 개발꾸러미/'usr/include']
    ፈጽም_ትእዛዝ([시언어번역기]+ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'መጀመር_ድገፍ.c','-o',ልኬት_ውሂብ/'crt.o'])
    ፈጽም_ትእዛዝ([시언어번역기]+ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት+['-I',ማከማቻ_ዱካ/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ልኬት_ውሂብ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ውሂብ_በቦታ_አስቀመጠ.name,ውሂብ_በቦታ_አስቀመጠ) for ውሂብ_በቦታ_አስቀመጠ in sorted((ማከማቻ_ዱካ/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ውሂብ_በቦታ_አስቀመጠ.name,ውሂብ_በቦታ_አስቀመጠ) for ውሂብ_በቦታ_አስቀመጠ in sorted((ሽቅብ_ፍሰት/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ውሂብ_በቦታ_አስቀመጠ.name,ውሂብ_በቦታ_አስቀመጠ) for ውሂብ_በቦታ_አስቀመጠ in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ስር_ዱካ/'build/user/start.o'),('/sdk/lib/crt.o',ልኬት_ውሂብ/'crt.o'),('/sdk/lib/aot-runtime.o',ልኬት_ውሂብ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ስር_ዱካ/'build/libposix-kor-user.a')]
    ርእስ_እሴት=['typedef struct { const char *ስም; const unsigned char *ውሂብ; unsigned መጠን; } 번역기자원;']
    for 순번,(_,መተላለፊያ) in enumerate(탑재자료):
        ርእስ_እሴት.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in መተላለፊያ.read_bytes())))
    ርእስ_እሴት.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ስም,መተላለፊያ) in enumerate(탑재자료): ርእስ_እሴት.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ስም,ensure_ascii=False),순번,መተላለፊያ.stat().st_size))
    ርእስ_እሴት.append('};');(ልኬት_ውሂብ/'resources.h').write_text('\n'.join(ርእስ_እሴት)+'\n',encoding='utf-8')
    መድረሻ_ፋይሎች=[]
    for ስም in ('번역기.c','የጋራ_ቋንቋ_ማስኬጃ_ጊዜ_ድገፍ.c','ማስኬጃ.c','미리번역.c','되돌림.S'):
        መድረሻ_ፋይል=ልኬት_ውሂብ/(Path(ስም).stem+'.o');መድረሻ_ፋይሎች.append(መድረሻ_ፋይል)
        ፈጽም_ትእዛዝ([시언어번역기]+ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ስም,'-o',መድረሻ_ፋይል])
    실행파일=ስር_ዱካ/'build/user/cc.elf'
    ፈጽም_ትእዛዝ([연결편집기,'--gc-sections','-T',ስር_ዱካ/'ተጠቃሚ/አገናኝ_አሰሳ.ld','-z','max-page-size=4096','-o',실행파일,
         ስር_ዱካ/'build/user/start.o',ስር_ዱካ/'build/user/runtime.o']+መድረሻ_ፋይሎች+
         [ስር_ዱካ/'build/user'/ስም for ስም in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
