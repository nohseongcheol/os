#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char ആര്_ഗ്യുമെന്_റ്_അരേ[8][256];
int ഉപയോക്താവ്_ആരംഭം(int 미사용값){
    (void)미사용값;char *ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)ആര്_ഗ്യുമെന്_റ്_അരേ[순번],256,0,0,0)<0)return 126;ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്[순번]=ആര്_ഗ്യുമെന്_റ്_അരേ[순번];}ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്[인수개수]=0;
    return main(인수개수,ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്);
}
void *memset(void*ഡാറ്റാ_പദവി,int പ്രതീകകോഡ്,size_t 개수){unsigned char*ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ=ഡാറ്റാ_പദവി;while(개수--)*ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ++=പ്രതീകകോഡ്;return ഡാറ്റാ_പദവി;}
void *memcpy(void*ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ,const void*സ്ട്രിംഗ്_ഡാറ്റാ,size_t 개수){unsigned char*첫째값=ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ;const unsigned char*둘째값=സ്ട്രിംഗ്_ഡാറ്റാ;while(개수--)*첫째값++=*둘째값++;return ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_ഏകോപനം,unsigned Y_ബട്ടൺ_ഏകോപനം,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned ലംബം_പദവി,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,ലംബം_പദവി,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
