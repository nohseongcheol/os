#!/usr/bin/env python3
"""libclang การประกาศ·อ้างอิง 위치를 수집한다. ภายนอก_ค่า 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

แสดง_ราก = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class สตริง_ค่า(씨.Structure): _fields_ = [('ข้อมูล',씨.c_void_p),('แสดง_ค่า',씨.c_uint)]
class เคอร์เซอร์_ค่า(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ข้อมูล',씨.c_void_p*3)]
class ตําแหน่ง(씨.Structure): _fields_ = [('ข้อมูล',씨.c_void_p*2),('ออฟเซต_ค่า',씨.c_uint)]
def ฟังก์ชัน_ค่า(ชื่อ, ส่งคืน_เมตริก, *อาร์กิวเมนต์):
    รายการ_ค่า = getattr(구현, ชื่อ); รายการ_ค่า.restype = ส่งคืน_เมตริก; รายการ_ค่า.argtypes = list(อาร์กิวเมนต์); return รายการ_ค่า
ดึง_ข้อความ = ฟังก์ชัน_ค่า('clang_getCString',씨.c_char_p,สตริง_ค่า)
ปล่อย_ข้อความ = ฟังก์ชัน_ค่า('clang_disposeString',None,สตริง_ค่า)
def ข้อความ(ค่า):
    ผลลัพธ์ = (ดึง_ข้อความ(ค่า) or b'').decode('utf-8'); ปล่อย_ข้อความ(ค่า); return ผลลัพธ์
ดึง_ชื่อ = ฟังก์ชัน_ค่า('clang_getCursorSpelling',สตริง_ค่า,เคอร์เซอร์_ค่า)
ดึง_อ้างอิง = ฟังก์ชัน_ค่า('clang_getCursorReferenced',เคอร์เซอร์_ค่า,เคอร์เซอร์_ค่า)
ดึง_ตําแหน่ง = ฟังก์ชัน_ค่า('clang_getCursorLocation',ตําแหน่ง,เคอร์เซอร์_ค่า)
แฟ้ม_ตําแหน่ง = ฟังก์ชัน_ค่า('clang_getFileLocation',None,ตําแหน่ง,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
แฟ้ม_รายการ_ชื่อ = ฟังก์ชัน_ค่า('clang_getFileName',สตริง_ค่า,씨.c_void_p)
고유이름 = ฟังก์ชัน_ค่า('clang_getCursorUSR',สตริง_ค่า,เคอร์เซอร์_ค่า)
연결종류 = ฟังก์ชัน_ค่า('clang_getCursorLinkage',씨.c_uint,เคอร์เซอร์_ค่า)
방문형 = 씨.CFUNCTYPE(씨.c_uint,เคอร์เซอร์_ค่า,เคอร์เซอร์_ค่า,씨.c_void_p)
방문 = ฟังก์ชัน_ค่า('clang_visitChildren',씨.c_uint,เคอร์เซอร์_ค่า,방문형,씨.c_void_p)
สร้าง_167eff27 = ฟังก์ชัน_ค่า('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
วิเคราะห์_ค่า = ฟังก์ชัน_ค่า('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ราก_ค่า = ฟังก์ชัน_ค่า('clang_getTranslationUnitCursor',เคอร์เซอร์_ค่า,씨.c_void_p)
ออก_แอป_55b3a1cd = ฟังก์ชัน_ค่า('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ฟังก์ชัน_ค่า('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ฟังก์ชัน_ค่า('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ความรุนแรง_ค่า = ฟังก์ชัน_ค่า('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ฟังก์ชัน_ค่า('clang_getDiagnosticSpelling',สตริง_ค่า,씨.c_void_p)
진단해제 = ฟังก์ชัน_ค่า('clang_disposeDiagnostic',None,씨.c_void_p)

def ดัชนีชี้ตําแหน่ง(รายการ_ค่า):
    แฟ้ม = 씨.c_void_p(); บรรทัด = 씨.c_uint(); 칸 = 씨.c_uint(); ออฟเซต_ค่า = 씨.c_uint()
    แฟ้ม_ตําแหน่ง(ดึง_ตําแหน่ง(รายการ_ค่า),씨.byref(แฟ้ม),씨.byref(บรรทัด),씨.byref(칸),씨.byref(ออฟเซต_ค่า))
    return (ข้อความ(แฟ้ม_รายการ_ชื่อ(แฟ้ม)) if แฟ้ม else '', ออฟเซต_ค่า.value, บรรทัด.value)

def ดําเนินการ_คําสั่ง():
    การค้นหา_ดัชนี = สร้าง_167eff27(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # คอมไพเลอร์_เครื่องมือ.c는 เอง การประกาศ 없이 TinyCC ภายนอก_ค่า 단일 แปล_แหล่ง 단위만 포함한다.
    # ภายนอก_ค่า 선언을 เอง 이름으로 세지 않으며, ค่าจริง_ข้อมูล 빌드에서는 계속 컴파일한다.
    소유파일 = {str(เส้นทาง.resolve()) for เส้นทาง in แสดง_ราก.rglob('*') if เส้นทาง.suffix in ('.c','.h','.cpp','.inc')
              and not set(เส้นทาง.relative_to(แสดง_ราก).parts)&{'build','dist','vendor','__pycache__'}
              and เส้นทาง.relative_to(แสดง_ราก).as_posix() != '시언어번역기/คอมไพเลอร์_เครื่องมือ.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(แสดง_ราก/'ผู้ใช้'),
          '-I'+str(แสดง_ราก.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(แสดง_ราก/'build'),'-I'+str(แสดง_ราก/'build/user'),
          '-I'+str(แสดง_ราก/'build/remote'),'-I'+str(แสดง_ราก/'vendor/bearssl/inc'),
          '-I'+str(แสดง_ราก/'vendor/bearssl/src'),'-I'+str(แสดง_ราก/'vendor/libassh/src'),
          '-I'+str(แสดง_ราก/'vendor/lwip/src/include'),'-I'+str(แสดง_ราก/'เครือข่าย_สแตก'),
          '-I'+str(แสดง_ราก/'ระยะไกล_ค่า'),'-I'+str(แสดง_ราก/'시언어번역기')]
    for เส้นทาง in sorted(Path(ชื่อ) for ชื่อ in 소유파일 if ชื่อ.endswith(('.c','.cpp'))):
        อาร์กิวเมนต์ = 공통 + ['-std=c++11' if เส้นทาง.suffix=='.cpp' else '-std=c11']
        if 'เครือข่าย_สแตก' in เส้นทาง.parts: อาร์กิวเมนต์ += ['-I'+str(แสดง_ราก/'เครือข่าย_สแตก'),'-I'+str(แสดง_ราก/'vendor/lwip/src/include')]
        if '시언어번역기' in เส้นทาง.parts:
            อาร์กิวเมนต์ += ['-I'+str(แสดง_ราก/'시언어번역기'),'-I'+str(แสดง_ราก/'vendor/tinycc'),'-I'+str(แสดง_ราก/'build/ccompiler'),
                    '-isystem',str(แสดง_ราก.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in เส้นทาง.parts:
            อาร์กิวเมนต์ += ['-I'+str(แสดง_ราก/'파이썬연결'),'-I'+str(แสดง_ราก/'build/micropython-1.24.1'),'-I'+str(แสดง_ราก/'build/python'),'-isystem','/usr/include/newlib']
        if 'ระยะไกล_ค่า' in เส้นทาง.parts:
            อาร์กิวเมนต์ += ['-isystem', '/usr/include/newlib']
        if 'การกระจาย_ค่า' in เส้นทาง.parts: อาร์กิวเมนต์ += ['-D__JKOROS__=1']
        if เส้นทาง.name=='รวม.c': อาร์กิวเมนต์ += ['-I'+str(แสดง_ราก/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        กลุ่ม_ค่า = (씨.c_char_p*len(อาร์กิวเมนต์))(*[รายการ_ค่า.encode() for รายการ_ค่า in อาร์กิวเมนต์])
        การแปล_หน่วย = วิเคราะห์_ค่า(การค้นหา_ดัชนี,str(เส้นทาง).encode(),กลุ่ม_ค่า,len(อาร์กิวเมนต์),None,0,1)
        for ดัชนี in range(진단수(การแปล_หน่วย)):
            진단 = 진단얻기(การแปล_หน่วย,ดัชนี)
            if ความรุนแรง_ค่า(진단)>=3: 오류들.append((str(เส้นทาง.relative_to(แสดง_ราก)),ข้อความ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(รายการ_ค่า,แม่_ค่า,ข้อมูล):
            แฟ้ม,ออฟเซต_ค่า,บรรทัด = ดัชนีชี้ตําแหน่ง(รายการ_ค่า)
            if แฟ้ม not in 소유파일: return 2 if รายการ_ค่า.종류==300 else 1
            낱말 = ข้อความ(ดึง_ชื่อ(รายการ_ค่า))
            if not 낱말 or any(ord(อักขระ_ค่า)>127 for อักขระ_ค่า in 낱말): return 2
            if รายการ_ค่า.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ข้อความ(고유이름(รายการ_ค่า)) or แฟ้ม+':'+str(ออฟเซต_ค่า)
                선언들[고유] = {'แฟ้ม':แฟ้ม,'ออฟเซต_ค่า':ออฟเซต_ค่า,'บรรทัด':บรรทัด,'종류':รายการ_ค่า.종류,'ชื่อ':낱말,'เชื่อมต่อ':연결종류(รายการ_ค่า)}
                참조들.append((แฟ้ม,ออฟเซต_ค่า,낱말,고유))
            else:
                อ้างอิง = ดึง_อ้างอิง(รายการ_ค่า)
                อ้างอิง_แฟ้ม,_,_ = ดัชนีชี้ตําแหน่ง(อ้างอิง)
                if อ้างอิง_แฟ้ม in 소유파일:
                    고유 = ข้อความ(고유이름(อ้างอิง)); 참조들.append((แฟ้ม,ออฟเซต_ค่า,ข้อความ(ดึง_ชื่อ(อ้างอิง)),고유))
            return 2
        방문(ราก_ค่า(การแปล_หน่วย),살피기,None)
        ออก_แอป_55b3a1cd(การแปล_หน่วย)
    ปลายทาง_ค่า_a0fbc067 = แสดง_ราก/'build/한국어화/시언어분석.json'
    ปลายทาง_ค่า_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {แฟ้ม:hashlib.sha256(Path(แฟ้ม).read_bytes()).hexdigest() for แฟ้ม in sorted(소유파일)}
    ปลายทาง_ค่า_a0fbc067.write_text(json.dumps({'การประกาศ':선언들,'อ้างอิง':참조들,'ข้อผิดพลาด':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('การประกาศ',len(선언들),'อ้างอิง',len(참조들),'ข้อผิดพลาด',len(오류들))
    for ข้อผิดพลาด in 오류들: print(*ข้อผิดพลาด)

if __name__=='__main__': ดําเนินการ_คําสั่ง()
