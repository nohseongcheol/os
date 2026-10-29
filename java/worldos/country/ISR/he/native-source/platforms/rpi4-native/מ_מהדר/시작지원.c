#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char ארגומנט_מערך[8][256];
int משתמש_התחל(int 미사용값){
    (void)미사용값;char *ארגומנט_רשימה[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)ארגומנט_מערך[순번],256,0,0,0)<0)return 126;ארגומנט_רשימה[순번]=ארגומנט_מערך[순번];}ארגומנט_רשימה[인수개수]=0;
    return main(인수개수,ארגומנט_רשימה);
}
void *memset(void*נתונים_עמדה,int נקודת_קוד,size_t 개수){unsigned char*יעד_נתונים=נתונים_עמדה;while(개수--)*יעד_נתונים++=נקודת_קוד;return נתונים_עמדה;}
void *memcpy(void*יעד_נתונים,const void*מחרוזת_נתונים,size_t 개수){unsigned char*첫째값=יעד_נתונים;const unsigned char*둘째값=מחרוזת_נתונים;while(개수--)*첫째값++=*둘째값++;return יעד_נתונים;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned קואורדינטת_x,unsigned 세로좌표,unsigned 너비,unsigned גובה_ערך,unsigned 색상){return 화면사각형(קואורדינטת_x,세로좌표,너비,גובה_ערך,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int ציור_מלבן(unsigned 가로,unsigned אנכי_עמדה,unsigned 너비,unsigned גובה_ערך,unsigned 색상){return pk_rectangle(가로,אנכי_עמדה,너비,גובה_ערך,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
