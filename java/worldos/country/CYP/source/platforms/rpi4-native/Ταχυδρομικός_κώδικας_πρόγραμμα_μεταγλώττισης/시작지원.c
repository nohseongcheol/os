#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char όρισμα_πίνακας[8][256];
int χρήστης_αρχή(int 미사용값){
    (void)미사용값;char *όρισμα_Λίστα[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)όρισμα_πίνακας[순번],256,0,0,0)<0)return 126;όρισμα_Λίστα[순번]=όρισμα_πίνακας[순번];}όρισμα_Λίστα[인수개수]=0;
    return main(인수개수,όρισμα_Λίστα);
}
void *memset(void*δεδομένα_θέση,int σημείο_κώδικα,size_t 개수){unsigned char*προορισμός_δεδομένα=δεδομένα_θέση;while(개수--)*προορισμός_δεδομένα++=σημείο_κώδικα;return δεδομένα_θέση;}
void *memcpy(void*προορισμός_δεδομένα,const void*συμβολοσειρά_δεδομένα,size_t 개수){unsigned char*첫째값=προορισμός_δεδομένα;const unsigned char*둘째값=συμβολοσειρά_δεδομένα;while(개수--)*첫째값++=*둘째값++;return προορισμός_δεδομένα;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned συντεταγμένη_x,unsigned κουμπί_Y_συντονισμός,unsigned 너비,unsigned ύψος_τιμή,unsigned 색상){return 화면사각형(συντεταγμένη_x,κουμπί_Y_συντονισμός,너비,ύψος_τιμή,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Σχεδίαση_ορθογώνιο(unsigned 가로,unsigned τομέας_θέση,unsigned 너비,unsigned ύψος_τιμή,unsigned 색상){return pk_rectangle(가로,τομέας_θέση,너비,ύψος_τιμή,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
