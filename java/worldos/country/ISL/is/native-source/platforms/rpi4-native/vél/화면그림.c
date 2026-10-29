/* raun_gögn 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 Uppruni/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Lóðrétt_staða){
    return 화소들&&가로<화면너비&&Lóðrétt_staða<화면높이?화소들[Lóðrétt_staða*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Lóðrétt_staða,uintptr_t 색){
    if(화소들&&가로<화면너비&&Lóðrétt_staða<화면높이)화소들[Lóðrétt_staða*화면줄낱말수+가로]=(uint32_t)색;
}
void bretti_Undirbúa_teikning(volatile uint32_t *gögn,unsigned 폭,unsigned lengd_VALUE,unsigned línubil_VALUE){
    화소들=gögn;화면너비=폭;화면높이=lengd_VALUE;화면줄낱말수=línubil_VALUE/4;자바그림준비((int)폭,(int)lengd_VALUE);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t bretti_teikning_COUNT(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Lóðrétt_staða){return (uint32_t)보드표시화소읽기(가로,Lóðrétt_staða);}
int 보드그림범위(int *가로,int *Lóðrétt_staða,int *폭,int *lengd_VALUE){
    if(!자바그림범위(*가로,*Lóðrétt_staða,*폭,*lengd_VALUE))return 0;
    *가로=자바그림범위값(0);*Lóðrétt_staða=자바그림범위값(1);*폭=자바그림범위값(2);*lengd_VALUE=자바그림범위값(3);return 1;
}
int bretti_Opna_teikning(int 가로,int Lóðrétt_staða,int 폭,int lengd_VALUE){return 자바그림시작(가로,Lóðrétt_staða,폭,lengd_VALUE);}
void bretti_Ljúka_teikning(void){자바그림마침();}
uintptr_t bretti_díll(uintptr_t 가로,uintptr_t Lóðrétt_staða,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Lóðrétt_staða,(int)색);}
void 보드사각그림(int 가로,int Lóðrétt_staða,int 폭,int lengd_VALUE,uint32_t 색){자바사각그림(가로,Lóðrétt_staða,폭,lengd_VALUE,(int)색);}
void bretti_bendill(int 가로,int Lóðrétt_staða,unsigned form_VALUE){자바포인터(가로,Lóðrétt_staða,(int)form_VALUE);}
