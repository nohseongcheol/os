#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char ነጋሪ_እሴት_ድርድር[8][256];
int ተጠቃሚ_ጀምር(int 미사용값){
    (void)미사용값;char *ነጋሪ_እሴት_ዝርዝር[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)ነጋሪ_እሴት_ድርድር[순번],256,0,0,0)<0)return 126;ነጋሪ_እሴት_ዝርዝር[순번]=ነጋሪ_እሴት_ድርድር[순번];}ነጋሪ_እሴት_ዝርዝር[인수개수]=0;
    return main(인수개수,ነጋሪ_እሴት_ዝርዝር);
}
void *memset(void*ውሂብ_በቦታ_አስቀመጠ,int የቁምፊ_ኮድ,size_t 개수){unsigned char*መድረሻ_ውሂብ=ውሂብ_በቦታ_አስቀመጠ;while(개수--)*መድረሻ_ውሂብ++=የቁምፊ_ኮድ;return ውሂብ_በቦታ_አስቀመጠ;}
void *memcpy(void*መድረሻ_ውሂብ,const void*ኅብረቁምፊ_ውሂብ,size_t 개수){unsigned char*첫째값=መድረሻ_ውሂብ;const unsigned char*둘째값=ኅብረቁምፊ_ውሂብ;while(개수--)*첫째값++=*둘째값++;return መድረሻ_ውሂብ;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned ኤክስ_አስተባባሪ,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(ኤክስ_አስተባባሪ,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned ቋሚ_በቦታ_አስቀመጠ,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,ቋሚ_በቦታ_አስቀመጠ,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
