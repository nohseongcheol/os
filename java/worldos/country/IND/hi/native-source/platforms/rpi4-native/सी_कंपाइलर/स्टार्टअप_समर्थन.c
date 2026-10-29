#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char तर्क_सरणी[8][256];
int उपयोगकर्ता_प्रारंभ(int 미사용값){
    (void)미사용값;char *तर्क_सूची[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)तर्क_सरणी[순번],256,0,0,0)<0)return 126;तर्क_सूची[순번]=तर्क_सरणी[순번];}तर्क_सूची[인수개수]=0;
    return main(인수개수,तर्क_सूची);
}
void *memset(void*डेटा_पद,int वर्ण_कोड,size_t 개수){unsigned char*गंतव्य_डेटा=डेटा_पद;while(개수--)*गंतव्य_डेटा++=वर्ण_कोड;return डेटा_पद;}
void *memcpy(void*गंतव्य_डेटा,const void*स्ट्रिंग_डेटा,size_t 개수){unsigned char*첫째값=गंतव्य_डेटा;const unsigned char*둘째값=स्ट्रिंग_डेटा;while(개수--)*첫째값++=*둘째값++;return गंतव्य_डेटा;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_निर्देशांक,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_निर्देशांक,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int आरेखित_करना_रेक्_टेंगल(unsigned 가로,unsigned अनुलंब_पद,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,अनुलंब_पद,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
