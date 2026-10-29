#!/usr/bin/env python3
"""libclang እወጃ·ማጣቀሻ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

አሳይ_ስር = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ኅብረቁምፊ_እሴት(씨.Structure): _fields_ = [('ውሂብ',씨.c_void_p),('አሳይ_እሴት',씨.c_uint)]
class አመልካች_እሴት(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ውሂብ',씨.c_void_p*3)]
class አካባቢ(씨.Structure): _fields_ = [('ውሂብ',씨.c_void_p*2),('ዝንፍ_እሴት',씨.c_uint)]
def ተግባር_እሴት(ስም, 반환, *인수):
    ምዝግብ_እሴት = getattr(구현, ስም); ምዝግብ_እሴት.restype = 반환; ምዝግብ_እሴት.argtypes = list(인수); return ምዝግብ_እሴት
አግኝ_ጽሁፍ = ተግባር_እሴት('clang_getCString',씨.c_char_p,ኅብረቁምፊ_እሴት)
ልቀቅ_ጽሁፍ = ተግባር_እሴት('clang_disposeString',None,ኅብረቁምፊ_እሴት)
def ጽሁፍ(እሴት):
    ልኬት = (አግኝ_ጽሁፍ(እሴት) or b'').decode('utf-8'); ልቀቅ_ጽሁፍ(እሴት); return ልኬት
አግኝ_ስም = ተግባር_እሴት('clang_getCursorSpelling',ኅብረቁምፊ_እሴት,አመልካች_እሴት)
አግኝ_ማጣቀሻ = ተግባር_እሴት('clang_getCursorReferenced',አመልካች_እሴት,አመልካች_እሴት)
አግኝ_በቦታ_አስቀመጠ = ተግባር_እሴት('clang_getCursorLocation',አካባቢ,አመልካች_እሴት)
ፋይል_በቦታ_አስቀመጠ = ተግባር_እሴት('clang_getFileLocation',None,አካባቢ,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ፋይል_ምዝግብ_ስም = ተግባር_እሴት('clang_getFileName',ኅብረቁምፊ_እሴት,씨.c_void_p)
고유이름 = ተግባር_እሴት('clang_getCursorUSR',ኅብረቁምፊ_እሴት,አመልካች_እሴት)
연결종류 = ተግባር_እሴት('clang_getCursorLinkage',씨.c_uint,አመልካች_እሴት)
방문형 = 씨.CFUNCTYPE(씨.c_uint,አመልካች_እሴት,አመልካች_እሴት,씨.c_void_p)
방문 = ተግባር_እሴት('clang_visitChildren',씨.c_uint,አመልካች_እሴት,방문형,씨.c_void_p)
አዘጋጅ = ተግባር_እሴት('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ተግባር_እሴት('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ስር_እሴት = ተግባር_እሴት('clang_getTranslationUnitCursor',አመልካች_እሴት,씨.c_void_p)
ጨርሰህ_ውጣ_ፕሮግራም = ተግባር_እሴት('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ተግባር_እሴት('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ተግባር_እሴት('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
የጉዳት_መጠን_እሴት = ተግባር_እሴት('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ተግባር_እሴት('clang_getDiagnosticSpelling',ኅብረቁምፊ_እሴት,씨.c_void_p)
진단해제 = ተግባር_እሴት('clang_disposeDiagnostic',None,씨.c_void_p)

def በቦታ_አስቀመጠ_መረጃ_ጠቆመ(ምዝግብ_እሴት):
    ፋይል = 씨.c_void_p(); መስመር = 씨.c_uint(); ማስገቢያ_ቀዳዳ_ምዝግብ = 씨.c_uint(); ዝንፍ_እሴት = 씨.c_uint()
    ፋይል_በቦታ_አስቀመጠ(አግኝ_በቦታ_አስቀመጠ(ምዝግብ_እሴት),씨.byref(ፋይል),씨.byref(መስመር),씨.byref(ማስገቢያ_ቀዳዳ_ምዝግብ),씨.byref(ዝንፍ_እሴት))
    return (ጽሁፍ(ፋይል_ምዝግብ_ስም(ፋይል)) if ፋይል else '', ዝንፍ_እሴት.value, መስመር.value)

def ፈጽም_ትእዛዝ():
    ፍለጋ_መረጃ_ጠቆመ = አዘጋጅ(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 እወጃ 없이 TinyCC 외부 단일 ተርጉም_ምንጭ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ትክክለኛ_ውሂብ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(መተላለፊያ.resolve()) for መተላለፊያ in አሳይ_ስር.rglob('*') if መተላለፊያ.suffix in ('.c','.h','.cpp','.inc')
              and not set(መተላለፊያ.relative_to(አሳይ_ስር).parts)&{'build','dist','vendor','__pycache__'}
              and መተላለፊያ.relative_to(አሳይ_ስር).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(አሳይ_ስር/'ተጠቃሚ'),
          '-I'+str(አሳይ_ስር.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(አሳይ_ስር/'build'),'-I'+str(አሳይ_ስር/'build/user'),
          '-I'+str(አሳይ_ስር/'build/remote'),'-I'+str(አሳይ_ስር/'vendor/bearssl/inc'),
          '-I'+str(አሳይ_ስር/'vendor/bearssl/src'),'-I'+str(አሳይ_ስር/'vendor/libassh/src'),
          '-I'+str(አሳይ_ስር/'vendor/lwip/src/include'),'-I'+str(አሳይ_ስር/'መረብ_ክምር'),
          '-I'+str(አሳይ_ስር/'የሩቅ_እሴት'),'-I'+str(አሳይ_ስር/'시언어번역기')]
    for መተላለፊያ in sorted(Path(ስም) for ስም in 소유파일 if ስም.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if መተላለፊያ.suffix=='.cpp' else '-std=c11']
        if 'መረብ_ክምር' in መተላለፊያ.parts: 인수 += ['-I'+str(አሳይ_ስር/'መረብ_ክምር'),'-I'+str(አሳይ_ስር/'vendor/lwip/src/include')]
        if '시언어번역기' in መተላለፊያ.parts:
            인수 += ['-I'+str(አሳይ_ስር/'시언어번역기'),'-I'+str(አሳይ_ስር/'vendor/tinycc'),'-I'+str(አሳይ_ስር/'build/ccompiler'),
                    '-isystem',str(አሳይ_ስር.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in መተላለፊያ.parts:
            인수 += ['-I'+str(አሳይ_ስር/'파이썬연결'),'-I'+str(አሳይ_ስር/'build/micropython-1.24.1'),'-I'+str(አሳይ_ስር/'build/python'),'-isystem','/usr/include/newlib']
        if 'የሩቅ_እሴት' in መተላለፊያ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in መተላለፊያ.parts: 인수 += ['-D__JKOROS__=1']
        if መተላለፊያ.name=='ቀርቅብ.c': 인수 += ['-I'+str(አሳይ_ስር/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ቡድን_እሴት = (씨.c_char_p*len(인수))(*[ምዝግብ_እሴት.encode() for ምዝግብ_እሴት in 인수])
        ትርጉም_አሀዶች = 분석(ፍለጋ_መረጃ_ጠቆመ,str(መተላለፊያ).encode(),ቡድን_እሴት,len(인수),None,0,1)
        for መረጃ_ጠቆመ in range(진단수(ትርጉም_አሀዶች)):
            진단 = 진단얻기(ትርጉም_አሀዶች,መረጃ_ጠቆመ)
            if የጉዳት_መጠን_እሴት(진단)>=3: 오류들.append((str(መተላለፊያ.relative_to(አሳይ_ስር)),ጽሁፍ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ምዝግብ_እሴት,부모,ውሂብ):
            ፋይል,ዝንፍ_እሴት,መስመር = በቦታ_አስቀመጠ_መረጃ_ጠቆመ(ምዝግብ_እሴት)
            if ፋይል not in 소유파일: return 2 if ምዝግብ_እሴት.종류==300 else 1
            낱말 = ጽሁፍ(አግኝ_ስም(ምዝግብ_እሴት))
            if not 낱말 or any(ord(ቁምፊ_እሴት)>127 for ቁምፊ_እሴት in 낱말): return 2
            if ምዝግብ_እሴት.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ጽሁፍ(고유이름(ምዝግብ_እሴት)) or ፋይል+':'+str(ዝንፍ_እሴት)
                선언들[고유] = {'ፋይል':ፋይል,'ዝንፍ_እሴት':ዝንፍ_እሴት,'줄':መስመር,'종류':ምዝግብ_እሴት.종류,'ስም':낱말,'መገናኛ':연결종류(ምዝግብ_እሴት)}
                참조들.append((ፋይል,ዝንፍ_እሴት,낱말,고유))
            else:
                ማጣቀሻ = አግኝ_ማጣቀሻ(ምዝግብ_እሴት)
                ማጣቀሻ_ፋይል,_,_ = በቦታ_አስቀመጠ_መረጃ_ጠቆመ(ማጣቀሻ)
                if ማጣቀሻ_ፋይል in 소유파일:
                    고유 = ጽሁፍ(고유이름(ማጣቀሻ)); 참조들.append((ፋይል,ዝንፍ_እሴት,ጽሁፍ(አግኝ_ስም(ማጣቀሻ)),고유))
            return 2
        방문(ስር_እሴት(ትርጉም_አሀዶች),살피기,None)
        ጨርሰህ_ውጣ_ፕሮግራም(ትርጉም_አሀዶች)
    መድረሻ_እሴት = አሳይ_ስር/'build/한국어화/시언어분석.json'
    መድረሻ_እሴት.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ፋይል:hashlib.sha256(Path(ፋይል).read_bytes()).hexdigest() for ፋይል in sorted(소유파일)}
    መድረሻ_እሴት.write_text(json.dumps({'እወጃ':선언들,'ማጣቀሻ':참조들,'ስህተት':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('እወጃ',len(선언들),'ማጣቀሻ',len(참조들),'ስህተት',len(오류들))
    for ስህተት in 오류들: print(*ስህተት)

if __name__=='__main__': ፈጽም_ትእዛዝ()
