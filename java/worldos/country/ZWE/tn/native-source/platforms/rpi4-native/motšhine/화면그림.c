/* tota_tshedimosetso 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 Motswedi/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t 세로){
    return 화소들&&가로<화면너비&&세로<화면높이?화소들[세로*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t 세로,uintptr_t 색){
    if(화소들&&가로<화면너비&&세로<화면높이)화소들[세로*화면줄낱말수+가로]=(uint32_t)색;
}
void 보드그림준비(volatile uint32_t *tshedimosetso,unsigned 폭,unsigned boleele_Boleng,unsigned kgaoganyomela_Boleng){
    화소들=tshedimosetso;화면너비=폭;화면높이=boleele_Boleng;화면줄낱말수=kgaoganyomela_Boleng/4;자바그림준비((int)폭,(int)boleele_Boleng);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t 보드그림기록수(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned 세로){return (uint32_t)보드표시화소읽기(가로,세로);}
int 보드그림범위(int *가로,int *세로,int *폭,int *boleele_Boleng){
    if(!자바그림범위(*가로,*세로,*폭,*boleele_Boleng))return 0;
    *가로=자바그림범위값(0);*세로=자바그림범위값(1);*폭=자바그림범위값(2);*boleele_Boleng=자바그림범위값(3);return 1;
}
int 보드그림시작(int 가로,int 세로,int 폭,int boleele_Boleng){return 자바그림시작(가로,세로,폭,boleele_Boleng);}
void 보드그림마침(void){자바그림마침();}
uintptr_t 보드화소(uintptr_t 가로,uintptr_t 세로,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)세로,(int)색);}
void 보드사각그림(int 가로,int 세로,int 폭,int boleele_Boleng,uint32_t 색){자바사각그림(가로,세로,폭,boleele_Boleng,(int)색);}
void 보드포인터(int 가로,int 세로,unsigned popego_Boleng){자바포인터(가로,세로,(int)popego_Boleng);}
