#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void તૈયાર_કરો_નેટવર્ક(void);
void 통신망살피기(void);
int 통신끝점만들기(int લખો_શ્રેણી);
int 망주소묶기(int ફાઇલ_હેન્ડલ, uint32_t સરનામું, unsigned પોર્ટ_નંબર);
int 연결기다리기(int ફાઇલ_હેન્ડલ);
void 통신주소재사용(int ફાઇલ_હેન્ડલ);
int 망연결하기(int ફાઇલ_હેન્ડલ, uint32_t સરનામું, unsigned પોર્ટ_નંબર);
int 망연결받기(int ફાઇલ_હેન્ડલ);
int 통신읽기(int ફાઇલ_હેન્ડલ, void *ડેટા, unsigned 개수);
int 통신쓰기(int ફાઇલ_હેન્ડલ, const void *ડેટા, unsigned 개수);
int 전문보내기(int ફાઇલ_હેન્ડલ, const void *ડેટા, unsigned 개수, uint32_t સરનામું, unsigned પોર્ટ_નંબર);
int 전문받기(int ફાઇલ_હેન્ડલ, void *ડેટા, unsigned 개수);
unsigned નેટવર્ક_પોર્ટ_નંબર(int ફાઇલ_હેન્ડલ);
unsigned પીઅર_પોર્ટ_નંબર(int ફાઇલ_હેન્ડલ);
uint32_t 상대통신주소(int ફાઇલ_હેન્ડલ);
void બંધ_કરો_નેટવર્ક(int ફાઇલ_હેન્ડલ);
int ફાઇલ_સ્થાનાંતર_નિયંત્રણ(int ક્રિયા);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned પ્રવેશ_મૂલ્ય, unsigned અનુક્રમણિકા);
int કન્ફિગર_કરો_નેટવર્ક(unsigned ક્રિયા, uint32_t સરનામું, uint32_t માસ્ક_મૂલ્ય, uint32_t ગેટવે_મૂલ્ય);
int 응답시험시작(uint32_t સરનામું, unsigned ક્રમ_મૂલ્ય);
int 응답시험읽기(unsigned પ્રવેશ_મૂલ્ય);
#endif
