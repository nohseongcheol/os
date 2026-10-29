"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def बनाएँ_सी_कंपाइलर(मूल_पथ, संग्रह_पथ, सी_कंपाइलर, 연결편집기, कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस, निष्पादित_करें_आदेश):
    परिणाम_डेटा = मूल_पथ / 'build/ccompiler'; परिणाम_डेटा.mkdir(exist_ok=True)
    원본자료 = मूल_पथ / 'सी_कंपाइलर'
    अपस्ट्रीम = मूल_पथ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    डेवलपमेंट_किट = मूल_पथ / 'vendor/sdk'
    if not (डेवलपमेंट_किट/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((डेवलपमेंट_किट/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस = [सेटिंग_मान for सेटिंग_मान in कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस if सेटिंग_मान != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', अपस्ट्रीम, '-I', मूल_पथ/'उपयोगकर्ता', '-I', परिणाम_डेटा, '-isystem', डेवलपमेंट_किट/'usr/include']
    निष्पादित_करें_आदेश([सी_कंपाइलर]+कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'स्टार्टअप_समर्थन.c','-o',परिणाम_डेटा/'crt.o'])
    निष्पादित_करें_आदेश([सी_कंपाइलर]+कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस+['-I',संग्रह_पथ/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',परिणाम_डेटा/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+डेटा_पद.name,डेटा_पद) for डेटा_पद in sorted((संग्रह_पथ/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+डेटा_पद.name,डेटा_पद) for डेटा_पद in sorted((अपस्ट्रीम/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+डेटा_पद.name,डेटा_पद) for डेटा_पद in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',मूल_पथ/'build/user/start.o'),('/sdk/lib/crt.o',परिणाम_डेटा/'crt.o'),('/sdk/lib/aot-runtime.o',परिणाम_डेटा/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',मूल_पथ/'build/libposix-kor-user.a')]
    हेडर_मान=['typedef struct { const char *नाम; const unsigned char *आँकड़े; unsigned आकार; } कंपाइलर_संसाधन;']
    for 순번,(_,पथ) in enumerate(탑재자료):
        हेडर_मान.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in पथ.read_bytes())))
    हेडर_मान.append('static const कंपाइलर_संसाधन कंपाइलर_संसाधन_0280c847[] = {')
    for 순번,(नाम,पथ) in enumerate(탑재자료): हेडर_मान.append('{%s, 탑재자원_%d, %d},'%(json.dumps(नाम,ensure_ascii=False),순번,पथ.stat().st_size))
    हेडर_मान.append('};');(परिणाम_डेटा/'resources.h').write_text('\n'.join(हेडर_मान)+'\n',encoding='utf-8')
    गंतव्य_फ़ाइलें=[]
    for नाम in ('कंपाइलर_उपकरण.c','निष्पादनसहायता.c','चलाएँ.c','미리번역.c','वापस_करें_ब्रिज.S'):
        गंतव्य_फ़ाइल=परिणाम_डेटा/(Path(नाम).stem+'.o');गंतव्य_फ़ाइलें.append(गंतव्य_फ़ाइल)
        निष्पादित_करें_आदेश([सी_कंपाइलर]+कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/नाम,'-o',गंतव्य_फ़ाइल])
    निष्पादन_योग्य_फ़ाइल=मूल_पथ/'build/user/cc.elf'
    निष्पादित_करें_आदेश([연결편집기,'--gc-sections','-T',मूल_पथ/'उपयोगकर्ता/लिंक_लेआउट.ld','-z','max-page-size=4096','-o',निष्पादन_योग्य_फ़ाइल,
         मूल_पथ/'build/user/start.o',मूल_पथ/'build/user/runtime.o']+गंतव्य_फ़ाइलें+
         [मूल_पथ/'build/user'/नाम for नाम in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
