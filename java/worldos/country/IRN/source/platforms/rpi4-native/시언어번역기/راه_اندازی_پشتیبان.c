#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char آرگومان_آرايه[8][256];
int کاربر_شروع(int 미사용값){
    (void)미사용값;char *آرگومان_لیست[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)آرگومان_آرايه[순번],256,0,0,0)<0)return 126;آرگومان_لیست[순번]=آرگومان_آرايه[순번];}آرگومان_لیست[인수개수]=0;
    return main(인수개수,آرگومان_لیست);
}
void *memset(void*داده_ها_مرتب_کردن,int کد_نویسه,size_t 개수){unsigned char*مقصد_داده_ها=داده_ها_مرتب_کردن;while(개수--)*مقصد_داده_ها++=کد_نویسه;return داده_ها_مرتب_کردن;}
void *memcpy(void*مقصد_داده_ها,const void*رشته_داده_ها,size_t 개수){unsigned char*첫째값=مقصد_داده_ها;const unsigned char*둘째값=رشته_داده_ها;while(개수--)*첫째값++=*둘째값++;return مقصد_داده_ها;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned مختصات_x,unsigned دکمه_Y_مختصات,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(مختصات_x,دکمه_Y_مختصات,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned عمودی_مرتب_کردن,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,عمودی_مرتب_کردن,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
