#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char دليل_ترتيب[8][256];
int صارف_شروع(int 미사용값){
    (void)미사용값;char *دليل_فهرست[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)دليل_ترتيب[순번],256,0,0,0)<0)return 126;دليل_فهرست[순번]=دليل_ترتيب[순번];}دليل_فهرست[인수개수]=0;
    return main(인수개수,دليل_فهرست);
}
void *memset(void*자료위치,int ڪئريڪٽر_ڪوڊ,size_t 개수){unsigned char*منزل_مقصود_ڪوائف=자료위치;while(개수--)*منزل_مقصود_ڪوائف++=ڪئريڪٽر_ڪوڊ;return 자료위치;}
void *memcpy(void*منزل_مقصود_ڪوائف,const void*اسٽرنگ_ڪوائف,size_t 개수){unsigned char*첫째값=منزل_مقصود_ڪوائف;const unsigned char*둘째값=اسٽرنگ_ڪوائف;while(개수--)*첫째값++=*둘째값++;return منزل_مقصود_ڪوائف;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_رطبو,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_رطبو,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned 세로,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,세로,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
