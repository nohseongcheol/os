#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void 통신망준비(void);
void 통신망살피기(void);
int बनाएँ_सॉकेट_एंडपॉइंट(int लिखें_श्रेणी);
int 망주소묶기(int फ़ाइल_हैंडल, uint32_t पता, unsigned पोर्ट_संख्या);
int 연결기다리기(int फ़ाइल_हैंडल);
void 통신주소재사용(int फ़ाइल_हैंडल);
int 망연결하기(int फ़ाइल_हैंडल, uint32_t पता, unsigned पोर्ट_संख्या);
int 망연결받기(int फ़ाइल_हैंडल);
int 통신읽기(int फ़ाइल_हैंडल, void *आँकड़े, unsigned 개수);
int 통신쓰기(int फ़ाइल_हैंडल, const void *आँकड़े, unsigned 개수);
int 전문보내기(int फ़ाइल_हैंडल, const void *आँकड़े, unsigned 개수, uint32_t पता, unsigned पोर्ट_संख्या);
int 전문받기(int फ़ाइल_हैंडल, void *आँकड़े, unsigned 개수);
unsigned नेटवर्क_पोर्ट_संख्या(int फ़ाइल_हैंडल);
unsigned पीअर_पोर्ट_संख्या(int फ़ाइल_हैंडल);
uint32_t 상대통신주소(int फ़ाइल_हैंडल);
void बंद_नेटवर्क(int फ़ाइल_हैंडल);
int फ़ाइल_स्थानांतरण_नियंत्रण(int क्रिया);
void 파일전송살피기(void);
uint32_t पढें_नेटवर्क_स्थिति(unsigned एन्ट्री_मान, unsigned इंडेक्स);
int कॉन्फ़गर_करें_नेटवर्क(unsigned क्रिया, uint32_t पता, uint32_t मास्क_मान, uint32_t गेटवे_मान);
int 응답시험시작(uint32_t पता, unsigned क्रम_मान);
int 응답시험읽기(unsigned एन्ट्री_मान);
#endif
