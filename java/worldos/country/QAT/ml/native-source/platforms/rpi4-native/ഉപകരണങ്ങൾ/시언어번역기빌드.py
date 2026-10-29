"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(വർഗ്ഗമൂലം_പാത, കലവറ_പാത, 시언어번역기, 연결편집기, കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്, നടപ്പാക്കുക_കമാന്_ഡ്):
    അളവ്_ഡാറ്റാ = വർഗ്ഗമൂലം_പാത / 'build/ccompiler'; അളവ്_ഡാറ്റാ.mkdir(exist_ok=True)
    원본자료 = വർഗ്ഗമൂലം_പാത / '시언어번역기'
    അപ്_സ്_ട്രീം = വർഗ്ഗമൂലം_പാത / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = വർഗ്ഗമൂലം_പാത / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ് = [ക്രമീകരണം_മൂല്യം for ക്രമീകരണം_മൂല്യം in കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ് if ക്രമീകരണം_മൂല്യം != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', അപ്_സ്_ട്രീം, '-I', വർഗ്ഗമൂലം_പാത/'ഉപയോക്താവ്', '-I', അളവ്_ഡാറ്റാ, '-isystem', 개발꾸러미/'usr/include']
    നടപ്പാക്കുക_കമാന്_ഡ്([시언어번역기]+കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ബൂട്ട്_പിന്തുണ.c','-o',അളവ്_ഡാറ്റാ/'crt.o'])
    നടപ്പാക്കുക_കമാന്_ഡ്([시언어번역기]+കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്+['-I',കലവറ_പാത/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',അളവ്_ഡാറ്റാ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ഡാറ്റാ_പദവി.name,ഡാറ്റാ_പദവി) for ഡാറ്റാ_പദവി in sorted((കലവറ_പാത/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ഡാറ്റാ_പദവി.name,ഡാറ്റാ_പദവി) for ഡാറ്റാ_പദവി in sorted((അപ്_സ്_ട്രീം/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ഡാറ്റാ_പദവി.name,ഡാറ്റാ_പദവി) for ഡാറ്റാ_പദവി in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',വർഗ്ഗമൂലം_പാത/'build/user/start.o'),('/sdk/lib/crt.o',അളവ്_ഡാറ്റാ/'crt.o'),('/sdk/lib/aot-runtime.o',അളവ്_ഡാറ്റാ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',വർഗ്ഗമൂലം_പാത/'build/libposix-kor-user.a')]
    ശീർഷകം_മൂല്യം=['typedef struct { const char *പേരു്; const unsigned char *ഡാറ്റാ; unsigned വലിപ്പം; } 번역기자원;']
    for 순번,(_,വഴി) in enumerate(탑재자료):
        ശീർഷകം_മൂല്യം.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in വഴി.read_bytes())))
    ശീർഷകം_മൂല്യം.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(പേരു്,വഴി) in enumerate(탑재자료): ശീർഷകം_മൂല്യം.append('{%s, 탑재자원_%d, %d},'%(json.dumps(പേരു്,ensure_ascii=False),순번,വഴി.stat().st_size))
    ശീർഷകം_മൂല്യം.append('};');(അളവ്_ഡാറ്റാ/'resources.h').write_text('\n'.join(ശീർഷകം_മൂല്യം)+'\n',encoding='utf-8')
    ഉദ്ദിഷ്ടസ്ഥാനം_ഫയലുകൾ=[]
    for പേരു് in ('번역기.c','പൊതുവായ_ഭാഷ_പ്രവര്_ത്തന_സമയം_പിന്തുണ.c','നടപ്പിലാക്കുക.c','미리번역.c','되돌림.S'):
        ഉദ്ദിഷ്ടസ്ഥാന_ഫയല്=അളവ്_ഡാറ്റാ/(Path(പേരു്).stem+'.o');ഉദ്ദിഷ്ടസ്ഥാനം_ഫയലുകൾ.append(ഉദ്ദിഷ്ടസ്ഥാന_ഫയല്)
        നടപ്പാക്കുക_കമാന്_ഡ്([시언어번역기]+കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/പേരു്,'-o',ഉദ്ദിഷ്ടസ്ഥാന_ഫയല്])
    നിര്_വ്വഹണക്ഷമമായ_ഫയല്=വർഗ്ഗമൂലം_പാത/'build/user/cc.elf'
    നടപ്പാക്കുക_കമാന്_ഡ്([연결편집기,'--gc-sections','-T',വർഗ്ഗമൂലം_പാത/'ഉപയോക്താവ്/ലിങ്ക്_ലേഔട്ട്.ld','-z','max-page-size=4096','-o',നിര്_വ്വഹണക്ഷമമായ_ഫയല്,
         വർഗ്ഗമൂലം_പാത/'build/user/start.o',വർഗ്ഗമൂലം_പാത/'build/user/runtime.o']+ഉദ്ദിഷ്ടസ്ഥാനം_ഫയലുകൾ+
         [വർഗ്ഗമൂലം_പാത/'build/user'/പേരു് for പേരു് in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
