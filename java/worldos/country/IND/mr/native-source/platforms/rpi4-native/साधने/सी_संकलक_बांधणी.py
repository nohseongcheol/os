"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def सी_संकलक_तयार_करा(मूळ_पथ, भांडार_पथ, सी_संकलक, जोडणीकार_साधन, कॉन्फिगरेशन_द्व्यंक, आज्ञा_कार्यवाही_करा):
    मोजमाप_डेटा = मूळ_पथ / 'build/ccompiler'; मोजमाप_डेटा.mkdir(exist_ok=True)
    मूळ_डेटा = मूळ_पथ / 'सी_संकलक'
    मूळप्रवाह = मूळ_पथ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    विकास_संच = मूळ_पथ / 'vendor/sdk'
    if not (विकास_संच/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    अंगभूत = sorted((विकास_संच/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not अंगभूत: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    कॉन्फिगरेशन_द्व्यंक = [सेटिंग्ज_मूल्य for सेटिंग्ज_मूल्य in कॉन्फिगरेशन_द्व्यंक if सेटिंग्ज_मूल्य != '-mgeneral-regs-only']
    समावेश = ['-I', मूळ_डेटा, '-I', मूळप्रवाह, '-I', मूळ_पथ/'प्रयोक्ता', '-I', मोजमाप_डेटा, '-isystem', विकास_संच/'usr/include']
    आज्ञा_कार्यवाही_करा([सी_संकलक]+कॉन्फिगरेशन_द्व्यंक+['-ffunction-sections','-fdata-sections']+समावेश+['-c',मूळ_डेटा/'बूट_समर्थन.c','-o',मोजमाप_डेटा/'crt.o'])
    आज्ञा_कार्यवाही_करा([सी_संकलक]+कॉन्फिगरेशन_द्व्यंक+['-I',भांडार_पथ/'posix-kor/arm64-native/घोषणाशीर्षे']+समावेश+['-c',मूळ_डेटा/'पूर्वसंकलन_सामान्य_भाषा_रनटाइम.c','-o',मोजमाप_डेटा/'aot-runtime.o'])
    साधनसामग्री = [('/sdk/include/'+डेटा_स्थान.name,डेटा_स्थान) for डेटा_स्थान in sorted((भांडार_पथ/'posix-kor/arm64-native/घोषणाशीर्षे').glob('*.h'))]
    साधनसामग्री += [('/sdk/include/'+डेटा_स्थान.name,डेटा_स्थान) for डेटा_स्थान in sorted((मूळप्रवाह/'include').glob('*.h'))]
    साधनसामग्री += [('/sdk/include/'+डेटा_स्थान.name,डेटा_स्थान) for डेटा_स्थान in sorted((मूळ_डेटा/'विकास_घोषणाशीर्षे').glob('*.h'))]
    साधनसामग्री += [('/sdk/lib/start.o',मूळ_पथ/'build/user/start.o'),('/sdk/lib/crt.o',मोजमाप_डेटा/'crt.o'),('/sdk/lib/aot-runtime.o',मोजमाप_डेटा/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',मूळ_पथ/'build/libposix-kor-user.a')]
    शीर्षलेख_मूल्य=['typedef struct { const char *नाव; const unsigned char *डेटा; unsigned आकार; } संकलक_संसाधन;']
    for क्रमांक_अनुक्रमणिका,(_,मार्ग) in enumerate(साधनसामग्री):
        शीर्षलेख_मूल्य.append('static const unsigned char 탑재자원_%d[] = {%s};'%(क्रमांक_अनुक्रमणिका,','.join(str(तात्पुरते_डेटा) for तात्पुरते_डेटा in मार्ग.read_bytes())))
    शीर्षलेख_मूल्य.append('static const संकलक_संसाधन संकलक_संसाधने[] = {')
    for क्रमांक_अनुक्रमणिका,(नाव,मार्ग) in enumerate(साधनसामग्री): शीर्षलेख_मूल्य.append('{%s, 탑재자원_%d, %d},'%(json.dumps(नाव,ensure_ascii=False),क्रमांक_अनुक्रमणिका,मार्ग.stat().st_size))
    शीर्षलेख_मूल्य.append('};');(मोजमाप_डेटा/'resources.h').write_text('\n'.join(शीर्षलेख_मूल्य)+'\n',encoding='utf-8')
    गंतव्यस्थान_संचिका=[]
    for नाव in ('संकलक_साधन.c','सामान्य_भाषा_रनटाइम_समर्थन.c','सुरू_करा.c','आगाऊ_संबंधित_वेळ.c','परतकरा_ब्रिज.S'):
        गंतव्य_फाइल=मोजमाप_डेटा/(Path(नाव).stem+'.o');गंतव्यस्थान_संचिका.append(गंतव्य_फाइल)
        आज्ञा_कार्यवाही_करा([सी_संकलक]+कॉन्फिगरेशन_द्व्यंक+['-ffunction-sections','-fdata-sections']+समावेश+['-c',मूळ_डेटा/नाव,'-o',गंतव्य_फाइल])
    निष्पादनीय_संचिका=मूळ_पथ/'build/user/cc.elf'
    आज्ञा_कार्यवाही_करा([जोडणीकार_साधन,'--gc-sections','-T',मूळ_पथ/'प्रयोक्ता/लिंक_लेआउट.ld','-z','max-page-size=4096','-o',निष्पादनीय_संचिका,
         मूळ_पथ/'build/user/start.o',मूळ_पथ/'build/user/runtime.o']+गंतव्यस्थान_संचिका+
         [मूळ_पथ/'build/user'/नाव for नाव in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[अंगभूत[-1]])
