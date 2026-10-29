#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char دەلىل_رەت[8][256];
int ئىشلەتكۈچى_باشلاش(int 미사용값){
    (void)미사용값;char *دەلىل_تىزىم[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)دەلىل_رەت[순번],256,0,0,0)<0)return 126;دەلىل_تىزىم[순번]=دەلىل_رەت[순번];}دەلىل_تىزىم[인수개수]=0;
    return main(인수개수,دەلىل_تىزىم);
}
void *memset(void*مەلۇمات_ئورۇنلاشتۇرۇش,int ھەرپ_كودى,size_t 개수){unsigned char*نىشان_مەلۇمات=مەلۇمات_ئورۇنلاشتۇرۇش;while(개수--)*نىشان_مەلۇمات++=ھەرپ_كودى;return مەلۇمات_ئورۇنلاشتۇرۇش;}
void *memcpy(void*نىشان_مەلۇمات,const void*ھەرپ_تىزمىسى_مەلۇمات,size_t 개수){unsigned char*첫째값=نىشان_مەلۇمات;const unsigned char*둘째값=ھەرپ_تىزمىسى_مەلۇمات;while(개수--)*첫째값++=*둘째값++;return نىشان_مەلۇمات;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_كوردىنات,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_كوردىنات,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned تىك_ئورۇنلاشتۇرۇش,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,تىك_ئورۇنلاشتۇرۇش,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
