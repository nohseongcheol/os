/* skutečný_data 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 zdrojový_soubor/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Svislá_pozice){
    return 화소들&&가로<화면너비&&Svislá_pozice<화면높이?화소들[Svislá_pozice*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Svislá_pozice,uintptr_t 색){
    if(화소들&&가로<화면너비&&Svislá_pozice<화면높이)화소들[Svislá_pozice*화면줄낱말수+가로]=(uint32_t)색;
}
void Panel_Připravit_kreslení(volatile uint32_t *data,unsigned 폭,unsigned délka_HODNOTA,unsigned řádkování_HODNOTA){
    화소들=data;화면너비=폭;화면높이=délka_HODNOTA;화면줄낱말수=řádkování_HODNOTA/4;자바그림준비((int)폭,(int)délka_HODNOTA);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Panel_kreslení_POČET(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Svislá_pozice){return (uint32_t)보드표시화소읽기(가로,Svislá_pozice);}
int 보드그림범위(int *가로,int *Svislá_pozice,int *폭,int *délka_HODNOTA){
    if(!자바그림범위(*가로,*Svislá_pozice,*폭,*délka_HODNOTA))return 0;
    *가로=자바그림범위값(0);*Svislá_pozice=자바그림범위값(1);*폭=자바그림범위값(2);*délka_HODNOTA=자바그림범위값(3);return 1;
}
int Panel_START_kreslení(int 가로,int Svislá_pozice,int 폭,int délka_HODNOTA){return 자바그림시작(가로,Svislá_pozice,폭,délka_HODNOTA);}
void Panel_Dokončit_kreslení(void){자바그림마침();}
uintptr_t Panel_pixel(uintptr_t 가로,uintptr_t Svislá_pozice,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Svislá_pozice,(int)색);}
void Panel_obdélník_výplň(int 가로,int Svislá_pozice,int 폭,int délka_HODNOTA,uint32_t 색){자바사각그림(가로,Svislá_pozice,폭,délka_HODNOTA,(int)색);}
void Panel_ukazatel(int 가로,int Svislá_pozice,unsigned tvar_HODNOTA){자바포인터(가로,Svislá_pozice,(int)tvar_HODNOTA);}
