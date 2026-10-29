/* real_date 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 SURSĂ/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Verticală_poziție){
    return 화소들&&가로<화면너비&&Verticală_poziție<화면높이?화소들[Verticală_poziție*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Verticală_poziție,uintptr_t 색){
    if(화소들&&가로<화면너비&&Verticală_poziție<화면높이)화소들[Verticală_poziție*화면줄낱말수+가로]=(uint32_t)색;
}
void Avizier_Pregătiți_desen(volatile uint32_t *date,unsigned 폭,unsigned lungime_VALUE,unsigned spațiere_VALUE){
    화소들=date;화면너비=폭;화면높이=lungime_VALUE;화면줄낱말수=spațiere_VALUE/4;자바그림준비((int)폭,(int)lungime_VALUE);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Avizier_desen_COUNT(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Verticală_poziție){return (uint32_t)보드표시화소읽기(가로,Verticală_poziție);}
int 보드그림범위(int *가로,int *Verticală_poziție,int *폭,int *lungime_VALUE){
    if(!자바그림범위(*가로,*Verticală_poziție,*폭,*lungime_VALUE))return 0;
    *가로=자바그림범위값(0);*Verticală_poziție=자바그림범위값(1);*폭=자바그림범위값(2);*lungime_VALUE=자바그림범위값(3);return 1;
}
int Avizier_buta_desen(int 가로,int Verticală_poziție,int 폭,int lungime_VALUE){return 자바그림시작(가로,Verticală_poziție,폭,lungime_VALUE);}
void Avizier_sfârșit_desen(void){자바그림마침();}
uintptr_t Avizier_element_imagine(uintptr_t 가로,uintptr_t Verticală_poziție,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Verticală_poziție,(int)색);}
void Avizier_dreptunghi_umple(int 가로,int Verticală_poziție,int 폭,int lungime_VALUE,uint32_t 색){자바사각그림(가로,Verticală_poziție,폭,lungime_VALUE,(int)색);}
void Avizier_cursor(int 가로,int Verticală_poziție,unsigned formă_VALUE){자바포인터(가로,Verticală_poziție,(int)formă_VALUE);}
