#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char არგუმენტი_მასივი[8][256];
int მომხმარებელი_დაწყება(int 미사용값){
    (void)미사용값;char *არგუმენტი_სია[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)არგუმენტი_მასივი[순번],256,0,0,0)<0)return 126;არგუმენტი_სია[순번]=არგუმენტი_მასივი[순번];}არგუმენტი_სია[인수개수]=0;
    return main(인수개수,არგუმენტი_სია);
}
void *memset(void*მონაცემები_პოზიცია,int სიმბოლოს_კოდი,size_t 개수){unsigned char*მიმართულება_მონაცემები=მონაცემები_პოზიცია;while(개수--)*მიმართულება_მონაცემები++=სიმბოლოს_კოდი;return მონაცემები_პოზიცია;}
void *memcpy(void*მიმართულება_მონაცემები,const void*სტრიქონი_მონაცემები,size_t 개수){unsigned char*첫째값=მიმართულება_მონაცემები;const unsigned char*둘째값=სტრიქონი_მონაცემები;while(개수--)*첫째값++=*둘째값++;return მიმართულება_მონაცემები;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_კოორდინატა,unsigned Y_ღილაკი_კოორდინატი,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_კოორდინატა,Y_ღილაკი_კოორდინატი,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned ვერტიკალური_პოზიცია,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,ვერტიკალური_პოზიცია,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
