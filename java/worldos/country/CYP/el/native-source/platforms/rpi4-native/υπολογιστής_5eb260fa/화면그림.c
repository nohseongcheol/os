/* πραγματικός_δεδομένα 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 ΠΗΓΗ/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t τομέας_θέση){
    return 화소들&&가로<화면너비&&τομέας_θέση<화면높이?화소들[τομέας_θέση*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t τομέας_θέση,uintptr_t 색){
    if(화소들&&가로<화면너비&&τομέας_θέση<화면높이)화소들[τομέας_θέση*화면줄낱말수+가로]=(uint32_t)색;
}
void Πίνακας_Προετοίμασε_σχέδιο(volatile uint32_t *δεδομένα,unsigned 폭,unsigned διάρκεια_τιμή,unsigned διάστιχο_τιμή){
    화소들=δεδομένα;화면너비=폭;화면높이=διάρκεια_τιμή;화면줄낱말수=διάστιχο_τιμή/4;자바그림준비((int)폭,(int)διάρκεια_τιμή);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t 보드그림기록수(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned τομέας_θέση){return (uint32_t)보드표시화소읽기(가로,τομέας_θέση);}
int 보드그림범위(int *가로,int *τομέας_θέση,int *폭,int *διάρκεια_τιμή){
    if(!자바그림범위(*가로,*τομέας_θέση,*폭,*διάρκεια_τιμή))return 0;
    *가로=자바그림범위값(0);*τομέας_θέση=자바그림범위값(1);*폭=자바그림범위값(2);*διάρκεια_τιμή=자바그림범위값(3);return 1;
}
int Πίνακας_αρχή_σχέδιο(int 가로,int τομέας_θέση,int 폭,int διάρκεια_τιμή){return 자바그림시작(가로,τομέας_θέση,폭,διάρκεια_τιμή);}
void Πίνακας_Τέλος_σχέδιο(void){자바그림마침();}
uintptr_t 보드화소(uintptr_t 가로,uintptr_t τομέας_θέση,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)τομέας_θέση,(int)색);}
void Πίνακας_ορθογώνιο_γεμίζω(int 가로,int τομέας_θέση,int 폭,int διάρκεια_τιμή,uint32_t 색){자바사각그림(가로,τομέας_θέση,폭,διάρκεια_τιμή,(int)색);}
void Πίνακας_δείκτης(int 가로,int τομέας_θέση,unsigned σχήμα_τιμή){자바포인터(가로,τομέας_θέση,(int)σχήμα_τιμή);}
