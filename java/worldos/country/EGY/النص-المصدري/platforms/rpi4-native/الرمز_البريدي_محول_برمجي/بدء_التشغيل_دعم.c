#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char وسيطة_صفيف[8][256];
int مستخدم_بدء(int 미사용값){
    (void)미사용값;char *وسيطة_قائمة[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)وسيطة_صفيف[순번],256,0,0,0)<0)return 126;وسيطة_قائمة[순번]=وسيطة_صفيف[순번];}وسيطة_قائمة[인수개수]=0;
    return main(인수개수,وسيطة_قائمة);
}
void *memset(void*بيانات_منصب,int رمز_الحرف,size_t 개수){unsigned char*وجهة_بيانات=بيانات_منصب;while(개수--)*وجهة_بيانات++=رمز_الحرف;return بيانات_منصب;}
void *memcpy(void*وجهة_بيانات,const void*سلسلة_بيانات,size_t 개수){unsigned char*첫째값=وجهة_بيانات;const unsigned char*둘째값=سلسلة_بيانات;while(개수--)*첫째값++=*둘째값++;return وجهة_بيانات;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned الإحداثي_س,unsigned الزر_Y_إحداثيات,unsigned 너비,unsigned ارتفاع_قيمة,unsigned 색상){return 화면사각형(الإحداثي_س,الزر_Y_إحداثيات,너비,ارتفاع_قيمة,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int رسم_مستطيل(unsigned 가로,unsigned عمودي_منصب,unsigned 너비,unsigned ارتفاع_قيمة,unsigned 색상){return pk_rectangle(가로,عمودي_منصب,너비,ارتفاع_قيمة,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
