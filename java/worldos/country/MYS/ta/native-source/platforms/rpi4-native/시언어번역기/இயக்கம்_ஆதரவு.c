#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char மதிப்புரு_கோவை[8][256];
int பயனர்_தொடங்கு(int 미사용값){
    (void)미사용값;char *மதிப்புரு_பட்டியல்[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)மதிப்புரு_கோவை[순번],256,0,0,0)<0)return 126;மதிப்புரு_பட்டியல்[순번]=மதிப்புரு_கோவை[순번];}மதிப்புரு_பட்டியல்[인수개수]=0;
    return main(인수개수,மதிப்புரு_பட்டியல்);
}
void *memset(void*தரவு_நிலை,int எழுத்துக்குறி_குறியீடு,size_t 개수){unsigned char*இலக்கு_தரவு=தரவு_நிலை;while(개수--)*இலக்கு_தரவு++=எழுத்துக்குறி_குறியீடு;return தரவு_நிலை;}
void *memcpy(void*இலக்கு_தரவு,const void*சரம்_தரவு,size_t 개수){unsigned char*첫째값=இலக்கு_தரவு;const unsigned char*둘째값=சரம்_தரவு;while(개수--)*첫째값++=*둘째값++;return இலக்கு_தரவு;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_ஒத்ததரமுள்ளது,unsigned Y_பொத்தான்_அச்சுத்_தொகுப்பு,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned வெர்டிகல்_நிலை,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,வெர்டிகல்_நிலை,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
