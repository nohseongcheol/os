/* verklig_data skärmbild 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 källfil/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "skärmbild_info.h"
static volatile uint32_t *화소들;
static unsigned skärmbild_RAD_Ord_ANTAL, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t bransch_placera){
    return 화소들&&가로<화면너비&&bransch_placera<화면높이?화소들[bransch_placera*skärmbild_RAD_Ord_ANTAL+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t bransch_placera,uintptr_t 색){
    if(화소들&&가로<화면너비&&bransch_placera<화면높이)화소들[bransch_placera*skärmbild_RAD_Ord_ANTAL+가로]=(uint32_t)색;
}
void Tavla_Förbereda_ritning(volatile uint32_t *data,unsigned 폭,unsigned längd_värde,unsigned avstånd_värde){
    화소들=data;화면너비=폭;화면높이=längd_värde;skärmbild_RAD_Ord_ANTAL=avstånd_värde/4;자바그림준비((int)폭,(int)längd_värde);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Tavla_ritning_ANTAL(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t Tavla_läsa_skärmbild(unsigned 가로,unsigned bransch_placera){return (uint32_t)보드표시화소읽기(가로,bransch_placera);}
int 보드그림범위(int *가로,int *bransch_placera,int *폭,int *längd_värde){
    if(!자바그림범위(*가로,*bransch_placera,*폭,*längd_värde))return 0;
    *가로=자바그림범위값(0);*bransch_placera=자바그림범위값(1);*폭=자바그림범위값(2);*längd_värde=자바그림범위값(3);return 1;
}
int Tavla_START_ritning(int 가로,int bransch_placera,int 폭,int längd_värde){return 자바그림시작(가로,bransch_placera,폭,längd_värde);}
void Tavla_slut_ritning(void){자바그림마침();}
uintptr_t Tavla_bildpunkt(uintptr_t 가로,uintptr_t bransch_placera,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)bransch_placera,(int)색);}
void Tavla_rektangel_Fyll(int 가로,int bransch_placera,int 폭,int längd_värde,uint32_t 색){자바사각그림(가로,bransch_placera,폭,längd_värde,(int)색);}
void Tavla_markör(int 가로,int bransch_placera,unsigned form_värde){자바포인터(가로,bransch_placera,(int)form_värde);}
