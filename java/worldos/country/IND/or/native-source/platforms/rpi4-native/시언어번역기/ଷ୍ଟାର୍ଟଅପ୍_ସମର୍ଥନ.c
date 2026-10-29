#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char ଯୁକ୍ତି_ଆରେ[8][256];
int ଉପଭୋକ୍ତା_ଆରମ୍ଭ(int 미사용값){
    (void)미사용값;char *ଯୁକ୍ତି_ତାଲିକା[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)ଯୁକ୍ତି_ଆରେ[순번],256,0,0,0)<0)return 126;ଯୁକ୍ତି_ତାଲିକା[순번]=ଯୁକ୍ତି_ଆରେ[순번];}ଯୁକ୍ତି_ତାଲିକା[인수개수]=0;
    return main(인수개수,ଯୁକ୍ତି_ତାଲିକା);
}
void *memset(void*ଡାଟା_ସ୍ଥିତି,int ବର୍ଣ୍ଣ_କୋଡ଼୍,size_t 개수){unsigned char*ଲକ୍ଷସ୍ଥଳ_ଡାଟା=ଡାଟା_ସ୍ଥିତି;while(개수--)*ଲକ୍ଷସ୍ଥଳ_ଡାଟା++=ବର୍ଣ୍ଣ_କୋଡ଼୍;return ଡାଟା_ସ୍ଥିତି;}
void *memcpy(void*ଲକ୍ଷସ୍ଥଳ_ଡାଟା,const void*ଷ୍ଟ୍ରିଂ_ଡାଟା,size_t 개수){unsigned char*첫째값=ଲକ୍ଷସ୍ଥଳ_ଡାଟା;const unsigned char*둘째값=ଷ୍ଟ୍ରିଂ_ଡାଟା;while(개수--)*첫째값++=*둘째값++;return ଲକ୍ଷସ୍ଥଳ_ଡାଟା;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_ସଂଯୋଜନ,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_ସଂଯୋଜନ,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned ଅନୁଲମ୍ବ_ସ୍ଥିତି,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,ଅନୁଲମ୍ବ_ସ୍ଥିତି,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
