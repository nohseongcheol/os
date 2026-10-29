/* attwali_data 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 sors/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Vertikali_pożizzjoni){
    return 화소들&&가로<화면너비&&Vertikali_pożizzjoni<화면높이?화소들[Vertikali_pożizzjoni*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Vertikali_pożizzjoni,uintptr_t 색){
    if(화소들&&가로<화면너비&&Vertikali_pożizzjoni<화면높이)화소들[Vertikali_pożizzjoni*화면줄낱말수+가로]=(uint32_t)색;
}
void bord_Ħejji_tpinġija(volatile uint32_t *data,unsigned 폭,unsigned tul_VALUE,unsigned leading_VALUE){
    화소들=data;화면너비=폭;화면높이=tul_VALUE;화면줄낱말수=leading_VALUE/4;자바그림준비((int)폭,(int)tul_VALUE);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t bord_tpinġija_COUNT(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Vertikali_pożizzjoni){return (uint32_t)보드표시화소읽기(가로,Vertikali_pożizzjoni);}
int 보드그림범위(int *가로,int *Vertikali_pożizzjoni,int *폭,int *tul_VALUE){
    if(!자바그림범위(*가로,*Vertikali_pożizzjoni,*폭,*tul_VALUE))return 0;
    *가로=자바그림범위값(0);*Vertikali_pożizzjoni=자바그림범위값(1);*폭=자바그림범위값(2);*tul_VALUE=자바그림범위값(3);return 1;
}
int bord_Bidu_tpinġija(int 가로,int Vertikali_pożizzjoni,int 폭,int tul_VALUE){return 자바그림시작(가로,Vertikali_pożizzjoni,폭,tul_VALUE);}
void bord_Tmiem_tpinġija(void){자바그림마침();}
uintptr_t bord_pel(uintptr_t 가로,uintptr_t Vertikali_pożizzjoni,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Vertikali_pożizzjoni,(int)색);}
void 보드사각그림(int 가로,int Vertikali_pożizzjoni,int 폭,int tul_VALUE,uint32_t 색){자바사각그림(가로,Vertikali_pożizzjoni,폭,tul_VALUE,(int)색);}
void bord_pointer(int 가로,int Vertikali_pożizzjoni,unsigned forma_VALUE){자바포인터(가로,Vertikali_pożizzjoni,(int)forma_VALUE);}
