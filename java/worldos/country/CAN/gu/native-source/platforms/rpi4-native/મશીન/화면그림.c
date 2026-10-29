/* વાસ્તવિક_ડેટા 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 સ્રોત/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t ઊભી_સ્થિતિ){
    return 화소들&&가로<화면너비&&ઊભી_સ્થિતિ<화면높이?화소들[ઊભી_સ્થિતિ*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t ઊભી_સ્થિતિ,uintptr_t 색){
    if(화소들&&가로<화면너비&&ઊભી_સ્થિતિ<화면높이)화소들[ઊભી_સ્થિતિ*화면줄낱말수+가로]=(uint32_t)색;
}
void બોર્ડ_તૈયાર_કરો_રેખાંકન(volatile uint32_t *ડેટા,unsigned 폭,unsigned લંબાઈ_મૂલ્ય,unsigned અંતર_મૂલ્ય){
    화소들=ડેટા;화면너비=폭;화면높이=લંબાઈ_મૂલ્ય;화면줄낱말수=અંતર_મૂલ્ય/4;자바그림준비((int)폭,(int)લંબાઈ_મૂલ્ય);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t 보드그림기록수(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned ઊભી_સ્થિતિ){return (uint32_t)보드표시화소읽기(가로,ઊભી_સ્થિતિ);}
int 보드그림범위(int *가로,int *ઊભી_સ્થિતિ,int *폭,int *લંબાઈ_મૂલ્ય){
    if(!자바그림범위(*가로,*ઊભી_સ્થિતિ,*폭,*લંબાઈ_મૂલ્ય))return 0;
    *가로=자바그림범위값(0);*ઊભી_સ્થિતિ=자바그림범위값(1);*폭=자바그림범위값(2);*લંબાઈ_મૂલ્ય=자바그림범위값(3);return 1;
}
int બોર્ડ_પ્રારંભ_રેખાંકન(int 가로,int ઊભી_સ્થિતિ,int 폭,int લંબાઈ_મૂલ્ય){return 자바그림시작(가로,ઊભી_સ્થિતિ,폭,લંબાઈ_મૂલ્ય);}
void બોર્ડ_સમાપ્ત_કરો_રેખાંકન(void){자바그림마침();}
uintptr_t બોર્ડ_પેલ(uintptr_t 가로,uintptr_t ઊભી_સ્થિતિ,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)ઊભી_સ્થિતિ,(int)색);}
void 보드사각그림(int 가로,int ઊભી_સ્થિતિ,int 폭,int લંબાઈ_મૂલ્ય,uint32_t 색){자바사각그림(가로,ઊભી_સ્થિતિ,폭,લંબાઈ_મૂલ્ય,(int)색);}
void બોર્ડ_સૂચક(int 가로,int ઊભી_સ્થિતિ,unsigned આકાર_મૂલ્ય){자바포인터(가로,ઊભી_સ્થિતિ,(int)આકાર_મૂલ્ય);}
