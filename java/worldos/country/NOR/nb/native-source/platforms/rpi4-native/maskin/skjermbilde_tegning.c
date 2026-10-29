/* faktisk_data skjermbilde 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 KILDE/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "skjermbilde_info.h"
static volatile uint32_t *화소들;
static unsigned skjermbilde_RAD_ord_ANTALL, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t vertikal_plassere){
    return 화소들&&가로<화면너비&&vertikal_plassere<화면높이?화소들[vertikal_plassere*skjermbilde_RAD_ord_ANTALL+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t vertikal_plassere,uintptr_t 색){
    if(화소들&&가로<화면너비&&vertikal_plassere<화면높이)화소들[vertikal_plassere*skjermbilde_RAD_ord_ANTALL+가로]=(uint32_t)색;
}
void Tavle_Forbered_tegning(volatile uint32_t *data,unsigned 폭,unsigned lengde_VERDI,unsigned linjeavstand_VERDI){
    화소들=data;화면너비=폭;화면높이=lengde_VERDI;skjermbilde_RAD_ord_ANTALL=linjeavstand_VERDI/4;자바그림준비((int)폭,(int)lengde_VERDI);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Tavle_tegning_ANTALL(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned vertikal_plassere){return (uint32_t)보드표시화소읽기(가로,vertikal_plassere);}
int 보드그림범위(int *가로,int *vertikal_plassere,int *폭,int *lengde_VERDI){
    if(!자바그림범위(*가로,*vertikal_plassere,*폭,*lengde_VERDI))return 0;
    *가로=자바그림범위값(0);*vertikal_plassere=자바그림범위값(1);*폭=자바그림범위값(2);*lengde_VERDI=자바그림범위값(3);return 1;
}
int Tavle_START_tegning(int 가로,int vertikal_plassere,int 폭,int lengde_VERDI){return 자바그림시작(가로,vertikal_plassere,폭,lengde_VERDI);}
void Tavle_slutt_tegning(void){자바그림마침();}
uintptr_t Tavle_piksel(uintptr_t 가로,uintptr_t vertikal_plassere,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)vertikal_plassere,(int)색);}
void Tavle_rektangel_fyll(int 가로,int vertikal_plassere,int 폭,int lengde_VERDI,uint32_t 색){자바사각그림(가로,vertikal_plassere,폭,lengde_VERDI,(int)색);}
void Tavle_peker(int 가로,int vertikal_plassere,unsigned figur_VERDI){자바포인터(가로,vertikal_plassere,(int)figur_VERDI);}
