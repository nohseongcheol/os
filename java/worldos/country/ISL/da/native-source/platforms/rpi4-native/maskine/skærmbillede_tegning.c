/* faktisk_data skærmbillede 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 KILDE/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "skærmbillede_info.h"
static volatile uint32_t *화소들;
static unsigned skærmbillede_post_Ord_TÆL, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Lodret_placere){
    return 화소들&&가로<화면너비&&Lodret_placere<화면높이?화소들[Lodret_placere*skærmbillede_post_Ord_TÆL+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Lodret_placere,uintptr_t 색){
    if(화소들&&가로<화면너비&&Lodret_placere<화면높이)화소들[Lodret_placere*skærmbillede_post_Ord_TÆL+가로]=(uint32_t)색;
}
void Tavle_Tilrettelæg_tegning(volatile uint32_t *data,unsigned 폭,unsigned varighed_VÆRDI,unsigned skydning_VÆRDI){
    화소들=data;화면너비=폭;화면높이=varighed_VÆRDI;skærmbillede_post_Ord_TÆL=skydning_VÆRDI/4;자바그림준비((int)폭,(int)varighed_VÆRDI);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Tavle_tegning_TÆL(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Lodret_placere){return (uint32_t)보드표시화소읽기(가로,Lodret_placere);}
int 보드그림범위(int *가로,int *Lodret_placere,int *폭,int *varighed_VÆRDI){
    if(!자바그림범위(*가로,*Lodret_placere,*폭,*varighed_VÆRDI))return 0;
    *가로=자바그림범위값(0);*Lodret_placere=자바그림범위값(1);*폭=자바그림범위값(2);*varighed_VÆRDI=자바그림범위값(3);return 1;
}
int Tavle_START_tegning(int 가로,int Lodret_placere,int 폭,int varighed_VÆRDI){return 자바그림시작(가로,Lodret_placere,폭,varighed_VÆRDI);}
void Tavle_Udfør_tegning(void){자바그림마침();}
uintptr_t Tavle_pixel(uintptr_t 가로,uintptr_t Lodret_placere,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Lodret_placere,(int)색);}
void Tavle_rektangel_udfyld(int 가로,int Lodret_placere,int 폭,int varighed_VÆRDI,uint32_t 색){자바사각그림(가로,Lodret_placere,폭,varighed_VÆRDI,(int)색);}
void Tavle_markør(int 가로,int Lodret_placere,unsigned figur_VÆRDI){자바포인터(가로,Lodret_placere,(int)figur_VÆRDI);}
