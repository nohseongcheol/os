/* dejanski_podatki 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 VIR/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Navpično_položaj){
    return 화소들&&가로<화면너비&&Navpično_položaj<화면높이?화소들[Navpično_položaj*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Navpično_položaj,uintptr_t 색){
    if(화소들&&가로<화면너비&&Navpično_položaj<화면높이)화소들[Navpično_položaj*화면줄낱말수+가로]=(uint32_t)색;
}
void Tabla_Pripravi_risba(volatile uint32_t *podatki,unsigned 폭,unsigned 길이,unsigned razmik_vrstic_VALUE){
    화소들=podatki;화면너비=폭;화면높이=길이;화면줄낱말수=razmik_vrstic_VALUE/4;자바그림준비((int)폭,(int)길이);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Tabla_risba_COUNT(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Navpično_položaj){return (uint32_t)보드표시화소읽기(가로,Navpično_položaj);}
int 보드그림범위(int *가로,int *Navpično_položaj,int *폭,int *길이){
    if(!자바그림범위(*가로,*Navpično_položaj,*폭,*길이))return 0;
    *가로=자바그림범위값(0);*Navpično_položaj=자바그림범위값(1);*폭=자바그림범위값(2);*길이=자바그림범위값(3);return 1;
}
int Tabla_Start_risba(int 가로,int Navpično_položaj,int 폭,int 길이){return 자바그림시작(가로,Navpično_položaj,폭,길이);}
void Tabla_konec_risba(void){자바그림마침();}
uintptr_t Tabla_slikovna_pika(uintptr_t 가로,uintptr_t Navpično_položaj,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Navpično_položaj,(int)색);}
void Tabla_pravokotnik_polnilo(int 가로,int Navpično_položaj,int 폭,int 길이,uint32_t 색){자바사각그림(가로,Navpično_položaj,폭,길이,(int)색);}
void Tabla_kazalec(int 가로,int Navpično_položaj,unsigned oblika_VALUE_f1cd655a){자바포인터(가로,Navpično_položaj,(int)oblika_VALUE_f1cd655a);}
