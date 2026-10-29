#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char যুক্তি_অ্যারে[8][256];
int ব্যবহারকারী_শুরু(int 미사용값){
    (void)미사용값;char *যুক্তি_তালিকা[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)যুক্তি_অ্যারে[순번],256,0,0,0)<0)return 126;যুক্তি_তালিকা[순번]=যুক্তি_অ্যারে[순번];}যুক্তি_তালিকা[인수개수]=0;
    return main(인수개수,যুক্তি_তালিকা);
}
void *memset(void*ডাটা_পদ,int অক্ষর_কোড,size_t 개수){unsigned char*গন্তব্য_ডাটা=ডাটা_পদ;while(개수--)*গন্তব্য_ডাটা++=অক্ষর_কোড;return ডাটা_পদ;}
void *memcpy(void*গন্তব্য_ডাটা,const void*স্ট্রিং_ডাটা,size_t 개수){unsigned char*첫째값=গন্তব্য_ডাটা;const unsigned char*둘째값=স্ট্রিং_ডাটা;while(개수--)*첫째값++=*둘째값++;return গন্তব্য_ডাটা;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned X_বোতাম_অক্ষবিন্দু,unsigned Y_বোতাম_অক্ষবিন্দু,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(X_বোতাম_অক্ষবিন্দু,Y_বোতাম_অক্ষবিন্দু,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned উল্লম্ব_পদ,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,উল্লম্ব_পদ,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
