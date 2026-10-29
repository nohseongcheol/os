/* tūturu_raraunga 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 pūtake/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Poutū_tūranga){
    return 화소들&&가로<화면너비&&Poutū_tūranga<화면높이?화소들[Poutū_tūranga*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Poutū_tūranga,uintptr_t 색){
    if(화소들&&가로<화면너비&&Poutū_tūranga<화면높이)화소들[Poutū_tūranga*화면줄낱말수+가로]=(uint32_t)색;
}
void papa_Whakarite_tātuhi(volatile uint32_t *raraunga,unsigned 폭,unsigned roa_uara,unsigned mokowā_raina_uara){
    화소들=raraunga;화면너비=폭;화면높이=roa_uara;화면줄낱말수=mokowā_raina_uara/4;자바그림준비((int)폭,(int)roa_uara);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t papa_tātuhi_COUNT(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Poutū_tūranga){return (uint32_t)보드표시화소읽기(가로,Poutū_tūranga);}
int 보드그림범위(int *가로,int *Poutū_tūranga,int *폭,int *roa_uara){
    if(!자바그림범위(*가로,*Poutū_tūranga,*폭,*roa_uara))return 0;
    *가로=자바그림범위값(0);*Poutū_tūranga=자바그림범위값(1);*폭=자바그림범위값(2);*roa_uara=자바그림범위값(3);return 1;
}
int papa_Start_tātuhi(int 가로,int Poutū_tūranga,int 폭,int roa_uara){return 자바그림시작(가로,Poutū_tūranga,폭,roa_uara);}
void papa_Mutu_tātuhi(void){자바그림마침();}
uintptr_t papa_pika(uintptr_t 가로,uintptr_t Poutū_tūranga,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Poutū_tūranga,(int)색);}
void 보드사각그림(int 가로,int Poutū_tūranga,int 폭,int roa_uara,uint32_t 색){자바사각그림(가로,Poutū_tūranga,폭,roa_uara,(int)색);}
void papa_atatohu(int 가로,int Poutū_tūranga,unsigned hanga_uara){자바포인터(가로,Poutū_tūranga,(int)hanga_uara);}
