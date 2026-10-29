#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char ವಾದ_ಅರೇ[8][256];
int ಬಳಕೆದಾರ_ಆರಂಭಿಸು(int 미사용값){
    (void)미사용값;char *ವಾದ_ಪಟ್ಟಿ[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)ವಾದ_ಅರೇ[순번],256,0,0,0)<0)return 126;ವಾದ_ಪಟ್ಟಿ[순번]=ವಾದ_ಅರೇ[순번];}ವಾದ_ಪಟ್ಟಿ[인수개수]=0;
    return main(인수개수,ವಾದ_ಪಟ್ಟಿ);
}
void *memset(void*ಡೇಟಾ_ಹುದ್ದೆ,int ಅಕ್ಷರ_ಕೋಡ್,size_t 개수){unsigned char*ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ=ಡೇಟಾ_ಹುದ್ದೆ;while(개수--)*ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ++=ಅಕ್ಷರ_ಕೋಡ್;return ಡೇಟಾ_ಹುದ್ದೆ;}
void *memcpy(void*ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ,const void*ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ,size_t 개수){unsigned char*첫째값=ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ;const unsigned char*둘째값=ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ;while(개수--)*첫째값++=*둘째값++;return ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_ಸಮಭಾಜಕ,unsigned Y_ಬಟನ್_ಸಮನ್ವಯ,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned ಲಂಬ_ಹುದ್ದೆ,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,ಲಂಬ_ಹುದ್ದೆ,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
