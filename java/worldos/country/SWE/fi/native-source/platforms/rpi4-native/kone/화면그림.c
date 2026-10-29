/* todellinen_data 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 lähdetiedosto/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t toimiala_toimi){
    return 화소들&&가로<화면너비&&toimiala_toimi<화면높이?화소들[toimiala_toimi*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t toimiala_toimi,uintptr_t 색){
    if(화소들&&가로<화면너비&&toimiala_toimi<화면높이)화소들[toimiala_toimi*화면줄낱말수+가로]=(uint32_t)색;
}
void Taulu_Valmistele_piirustus(volatile uint32_t *data,unsigned 폭,unsigned kesto_ARVO,unsigned riviväli_ARVO){
    화소들=data;화면너비=폭;화면높이=kesto_ARVO;화면줄낱말수=riviväli_ARVO/4;자바그림준비((int)폭,(int)kesto_ARVO);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Taulu_piirustus_LASKE(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned toimiala_toimi){return (uint32_t)보드표시화소읽기(가로,toimiala_toimi);}
int 보드그림범위(int *가로,int *toimiala_toimi,int *폭,int *kesto_ARVO){
    if(!자바그림범위(*가로,*toimiala_toimi,*폭,*kesto_ARVO))return 0;
    *가로=자바그림범위값(0);*toimiala_toimi=자바그림범위값(1);*폭=자바그림범위값(2);*kesto_ARVO=자바그림범위값(3);return 1;
}
int Taulu_alku_piirustus(int 가로,int toimiala_toimi,int 폭,int kesto_ARVO){return 자바그림시작(가로,toimiala_toimi,폭,kesto_ARVO);}
void Taulu_loppu_piirustus(void){자바그림마침();}
uintptr_t Taulu_kuvapiste(uintptr_t 가로,uintptr_t toimiala_toimi,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)toimiala_toimi,(int)색);}
void Taulu_suorakulmio_täyttö(int 가로,int toimiala_toimi,int 폭,int kesto_ARVO,uint32_t 색){자바사각그림(가로,toimiala_toimi,폭,kesto_ARVO,(int)색);}
void Taulu_osoitin(int 가로,int toimiala_toimi,unsigned muoto_ARVO_f1cd655a){자바포인터(가로,toimiala_toimi,(int)muoto_ARVO_f1cd655a);}
