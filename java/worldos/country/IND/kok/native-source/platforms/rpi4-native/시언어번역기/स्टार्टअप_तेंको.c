#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char युक्तीवाद_क्रम[8][256];
int उपेगकर्तो_Start(int 미사용값){
    (void)미사용값;char *युक्तीवाद_सुची[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)युक्तीवाद_क्रम[순번],256,0,0,0)<0)return 126;युक्तीवाद_सुची[순번]=युक्तीवाद_क्रम[순번];}युक्तीवाद_सुची[인수개수]=0;
    return main(인수개수,युक्तीवाद_सुची);
}
void *memset(void*डेटा_स्थिती,int वर्ण_कोड,size_t आयटम_COUNT){unsigned char*नियुक्त_स्थान_डेटा=डेटा_स्थिती;while(आयटम_COUNT--)*नियुक्त_स्थान_डेटा++=वर्ण_कोड;return डेटा_स्थिती;}
void *memcpy(void*नियुक्त_स्थान_डेटा,const void*स्ट्रिंग_डेटा,size_t आयटम_COUNT){unsigned char*첫째값=नियुक्त_स्थान_डेटा;const unsigned char*SECOND_मोल=स्ट्रिंग_डेटा;while(आयटम_COUNT--)*첫째값++=*SECOND_मोल++;return नियुक्त_स्थान_डेटा;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_coordinate,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_coordinate,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned उबें_स्थिती,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,उबें_स्थिती,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
