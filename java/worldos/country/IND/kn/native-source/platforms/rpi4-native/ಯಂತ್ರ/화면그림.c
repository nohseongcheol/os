/* ನಿಜವಾದ_ಡೇಟಾ 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 ಮೂಲ/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t ಲಂಬ_ಹುದ್ದೆ){
    return 화소들&&가로<화면너비&&ಲಂಬ_ಹುದ್ದೆ<화면높이?화소들[ಲಂಬ_ಹುದ್ದೆ*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t ಲಂಬ_ಹುದ್ದೆ,uintptr_t 색){
    if(화소들&&가로<화면너비&&ಲಂಬ_ಹುದ್ದೆ<화면높이)화소들[ಲಂಬ_ಹುದ್ದೆ*화면줄낱말수+가로]=(uint32_t)색;
}
void ಬೋರ್ಡ್_ಸಿದ್ಧಪಡಿಸು_ಚಿತ್ರರಚನೆ(volatile uint32_t *ಡೇಟಾ,unsigned 폭,unsigned ಉದ್ದ_ಮೌಲ್ಯ,unsigned ಲೀಡಿಂಗ್_ಮೌಲ್ಯ){
    화소들=ಡೇಟಾ;화면너비=폭;화면높이=ಉದ್ದ_ಮೌಲ್ಯ;화면줄낱말수=ಲೀಡಿಂಗ್_ಮೌಲ್ಯ/4;자바그림준비((int)폭,(int)ಉದ್ದ_ಮೌಲ್ಯ);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t 보드그림기록수(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned ಲಂಬ_ಹುದ್ದೆ){return (uint32_t)보드표시화소읽기(가로,ಲಂಬ_ಹುದ್ದೆ);}
int 보드그림범위(int *가로,int *ಲಂಬ_ಹುದ್ದೆ,int *폭,int *ಉದ್ದ_ಮೌಲ್ಯ){
    if(!자바그림범위(*가로,*ಲಂಬ_ಹುದ್ದೆ,*폭,*ಉದ್ದ_ಮೌಲ್ಯ))return 0;
    *가로=자바그림범위값(0);*ಲಂಬ_ಹುದ್ದೆ=자바그림범위값(1);*폭=자바그림범위값(2);*ಉದ್ದ_ಮೌಲ್ಯ=자바그림범위값(3);return 1;
}
int ಬೋರ್ಡ್_ಆರಂಭಿಸು_ಚಿತ್ರರಚನೆ(int 가로,int ಲಂಬ_ಹುದ್ದೆ,int 폭,int ಉದ್ದ_ಮೌಲ್ಯ){return 자바그림시작(가로,ಲಂಬ_ಹುದ್ದೆ,폭,ಉದ್ದ_ಮೌಲ್ಯ);}
void ಬೋರ್ಡ್_ಮುಗಿಸು_ಚಿತ್ರರಚನೆ(void){자바그림마침();}
uintptr_t ಬೋರ್ಡ್_ಪೆಲ್(uintptr_t 가로,uintptr_t ಲಂಬ_ಹುದ್ದೆ,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)ಲಂಬ_ಹುದ್ದೆ,(int)색);}
void 보드사각그림(int 가로,int ಲಂಬ_ಹುದ್ದೆ,int 폭,int ಉದ್ದ_ಮೌಲ್ಯ,uint32_t 색){자바사각그림(가로,ಲಂಬ_ಹುದ್ದೆ,폭,ಉದ್ದ_ಮೌಲ್ಯ,(int)색);}
void ಬೋರ್ಡ್_ಸೂಚಕ(int 가로,int ಲಂಬ_ಹುದ್ದೆ,unsigned ಆಕಾರ_ಮೌಲ್ಯ){자바포인터(가로,ಲಂಬ_ಹುದ್ದೆ,(int)ಆಕಾರ_ಮೌಲ್ಯ);}
