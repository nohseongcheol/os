#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char যুক্তি_শৃঙ্খলা[8][256];
int ব্যৱহাৰকৰ্তা_আৰম্ভ(int 미사용값){
    (void)미사용값;char *যুক্তি_সূচী[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)যুক্তি_শৃঙ্খলা[순번],256,0,0,0)<0)return 126;যুক্তি_সূচী[순번]=যুক্তি_শৃঙ্খলা[순번];}যুক্তি_সূচী[인수개수]=0;
    return main(인수개수,যুক্তি_সূচী);
}
void *memset(void*ডাটা_স্থান_সলনি_কৰক,int বৰ্ণ_ক_ড,size_t 개수){unsigned char*গন্তব্য_স্থান_ডাটা=ডাটা_স্থান_সলনি_কৰক;while(개수--)*গন্তব্য_স্থান_ডাটা++=বৰ্ণ_ক_ড;return ডাটা_স্থান_সলনি_কৰক;}
void *memcpy(void*গন্তব্য_স্থান_ডাটা,const void*ষ্ট্ৰিং_ডাটা,size_t 개수){unsigned char*첫째값=গন্তব্য_স্থান_ডাটা;const unsigned char*둘째값=ষ্ট্ৰিং_ডাটা;while(개수--)*첫째값++=*둘째값++;return গন্তব্য_স্থান_ডাটা;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_ক_ৰ্ডিনেট,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_ক_ৰ্ডিনেট,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned উলম্ব_স্থান_সলনি_কৰক,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,উলম্ব_স্থান_সলনি_কৰক,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
