/* werkelijk_gegevens scherm 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 broncode/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "scherm_info.h"
static volatile uint32_t *화소들;
static unsigned scherm_RIJ_Aantal_woorden, 화면너비, scherm_hoogte;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Verticaal_functie){
    return 화소들&&가로<화면너비&&Verticaal_functie<scherm_hoogte?화소들[Verticaal_functie*scherm_RIJ_Aantal_woorden+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Verticaal_functie,uintptr_t 색){
    if(화소들&&가로<화면너비&&Verticaal_functie<scherm_hoogte)화소들[Verticaal_functie*scherm_RIJ_Aantal_woorden+가로]=(uint32_t)색;
}
void Bord_Bereid_voor_tekening(volatile uint32_t *gegevens,unsigned 폭,unsigned tijdsduur_WAARDE,unsigned interlinie_WAARDE){
    화소들=gegevens;화면너비=폭;scherm_hoogte=tijdsduur_WAARDE;scherm_RIJ_Aantal_woorden=interlinie_WAARDE/4;자바그림준비((int)폭,(int)tijdsduur_WAARDE);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t Bord_scherm_hoogte(void){return (unsigned)자바그림높이();}
uint64_t Bord_tekening_AANTAL(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Verticaal_functie){return (uint32_t)보드표시화소읽기(가로,Verticaal_functie);}
int 보드그림범위(int *가로,int *Verticaal_functie,int *폭,int *tijdsduur_WAARDE){
    if(!자바그림범위(*가로,*Verticaal_functie,*폭,*tijdsduur_WAARDE))return 0;
    *가로=자바그림범위값(0);*Verticaal_functie=자바그림범위값(1);*폭=자바그림범위값(2);*tijdsduur_WAARDE=자바그림범위값(3);return 1;
}
int Bord_START_tekening(int 가로,int Verticaal_functie,int 폭,int tijdsduur_WAARDE){return 자바그림시작(가로,Verticaal_functie,폭,tijdsduur_WAARDE);}
void Bord_Voltooien_tekening(void){자바그림마침();}
uintptr_t Bord_pixel(uintptr_t 가로,uintptr_t Verticaal_functie,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Verticaal_functie,(int)색);}
void Bord_rechthoek_vullen(int 가로,int Verticaal_functie,int 폭,int tijdsduur_WAARDE,uint32_t 색){자바사각그림(가로,Verticaal_functie,폭,tijdsduur_WAARDE,(int)색);}
void Bord_wijzer(int 가로,int Verticaal_functie,unsigned vorm_WAARDE){자바포인터(가로,Verticaal_functie,(int)vorm_WAARDE);}
