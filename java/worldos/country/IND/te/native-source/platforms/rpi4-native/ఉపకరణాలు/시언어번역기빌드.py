"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(మూలం_పథం, రిపోజిటరీ_పథం, 시언어번역기, 연결편집기, నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ, అమలు_చేయి_ఆదేశం):
    ప్రమాణం_డేటా = మూలం_పథం / 'build/ccompiler'; ప్రమాణం_డేటా.mkdir(exist_ok=True)
    원본자료 = మూలం_పథం / '시언어번역기'
    అప్_స్ట్రీమ్ = మూలం_పథం / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = మూలం_పథం / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ = [సెట్టింగ్_లు_మూల్యం for సెట్టింగ్_లు_మూల్యం in నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ if సెట్టింగ్_లు_మూల్యం != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', అప్_స్ట్రీమ్, '-I', మూలం_పథం/'వినియోగదారు', '-I', ప్రమాణం_డేటా, '-isystem', 개발꾸러미/'usr/include']
    అమలు_చేయి_ఆదేశం([시언어번역기]+నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'బూట్_మద్దతు.c','-o',ప్రమాణం_డేటా/'crt.o'])
    అమలు_చేయి_ఆదేశం([시언어번역기]+నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ+['-I',రిపోజిటరీ_పథం/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ప్రమాణం_డేటా/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+డేటా_స్థాయి.name,డేటా_స్థాయి) for డేటా_స్థాయి in sorted((రిపోజిటరీ_పథం/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+డేటా_స్థాయి.name,డేటా_స్థాయి) for డేటా_స్థాయి in sorted((అప్_స్ట్రీమ్/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+డేటా_స్థాయి.name,డేటా_స్థాయి) for డేటా_స్థాయి in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',మూలం_పథం/'build/user/start.o'),('/sdk/lib/crt.o',ప్రమాణం_డేటా/'crt.o'),('/sdk/lib/aot-runtime.o',ప్రమాణం_డేటా/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',మూలం_పథం/'build/libposix-kor-user.a')]
    శీర్షిక_మూల్యం=['typedef struct { const char *పేరు; const unsigned char *డేటా; unsigned పరిమాణం; } 번역기자원;']
    for 순번,(_,పాత్) in enumerate(탑재자료):
        శీర్షిక_మూల్యం.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in పాత్.read_bytes())))
    శీర్షిక_మూల్యం.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(పేరు,పాత్) in enumerate(탑재자료): శీర్షిక_మూల్యం.append('{%s, 탑재자원_%d, %d},'%(json.dumps(పేరు,ensure_ascii=False),순번,పాత్.stat().st_size))
    శీర్షిక_మూల్యం.append('};');(ప్రమాణం_డేటా/'resources.h').write_text('\n'.join(శీర్షిక_మూల్యం)+'\n',encoding='utf-8')
    గమ్యం_ఫైల్_లు=[]
    for పేరు in ('번역기.c','సాధారణ_భాష_అమలు_సమయం_మద్దతు.c','నడుపుము.c','미리번역.c','되돌림.S'):
        గమ్యఫైల్=ప్రమాణం_డేటా/(Path(పేరు).stem+'.o');గమ్యం_ఫైల్_లు.append(గమ్యఫైల్)
        అమలు_చేయి_ఆదేశం([시언어번역기]+నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/పేరు,'-o',గమ్యఫైల్])
    실행파일=మూలం_పథం/'build/user/cc.elf'
    అమలు_చేయి_ఆదేశం([연결편집기,'--gc-sections','-T',మూలం_పథం/'వినియోగదారు/బంధం_లేవుట్.ld','-z','max-page-size=4096','-o',실행파일,
         మూలం_పథం/'build/user/start.o',మూలం_పథం/'build/user/runtime.o']+గమ్యం_ఫైల్_లు+
         [మూలం_పథం/'build/user'/పేరు for పేరు in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
