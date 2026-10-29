/* fiili_veri 화면 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 kaynakKod/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "화면정보.h"
static volatile uint32_t *화소들;
static unsigned 화면줄낱말수, 화면너비, 화면높이;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Dikey_konum){
    return 화소들&&가로<화면너비&&Dikey_konum<화면높이?화소들[Dikey_konum*화면줄낱말수+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Dikey_konum,uintptr_t 색){
    if(화소들&&가로<화면너비&&Dikey_konum<화면높이)화소들[Dikey_konum*화면줄낱말수+가로]=(uint32_t)색;
}
void Pano_Hazırlan_çizim(volatile uint32_t *veri,unsigned 폭,unsigned süre_değer,unsigned satır_aralığı_değer){
    화소들=veri;화면너비=폭;화면높이=süre_değer;화면줄낱말수=satır_aralığı_değer/4;자바그림준비((int)폭,(int)süre_değer);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t 보드화면높이(void){return (unsigned)자바그림높이();}
uint64_t Pano_çizim_BAĞ_DEĞ_SAY(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Dikey_konum){return (uint32_t)보드표시화소읽기(가로,Dikey_konum);}
int 보드그림범위(int *가로,int *Dikey_konum,int *폭,int *süre_değer){
    if(!자바그림범위(*가로,*Dikey_konum,*폭,*süre_değer))return 0;
    *가로=자바그림범위값(0);*Dikey_konum=자바그림범위값(1);*폭=자바그림범위값(2);*süre_değer=자바그림범위값(3);return 1;
}
int Pano_Start_çizim(int 가로,int Dikey_konum,int 폭,int süre_değer){return 자바그림시작(가로,Dikey_konum,폭,süre_değer);}
void Pano_Son_çizim(void){자바그림마침();}
uintptr_t Pano_piksel(uintptr_t 가로,uintptr_t Dikey_konum,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Dikey_konum,(int)색);}
void Pano_dikdörtgen_dolgu(int 가로,int Dikey_konum,int 폭,int süre_değer,uint32_t 색){자바사각그림(가로,Dikey_konum,폭,süre_değer,(int)색);}
void Pano_işaretçi(int 가로,int Dikey_konum,unsigned şekil_değer){자바포인터(가로,Dikey_konum,(int)şekil_değer);}
