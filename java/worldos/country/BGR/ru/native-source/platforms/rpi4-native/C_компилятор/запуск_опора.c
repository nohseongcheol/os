#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char аргумент_МАССИВ[8][256];
int пользователь_Пуск(int 미사용값){
    (void)미사용값;char *аргумент_Список[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)аргумент_МАССИВ[순번],256,0,0,0)<0)return 126;аргумент_Список[순번]=аргумент_МАССИВ[순번];}аргумент_Список[인수개수]=0;
    return main(인수개수,аргумент_Список);
}
void *memset(void*данные_позиция,int код_знака,size_t товар_СЧЁТ){unsigned char*цель_данные=данные_позиция;while(товар_СЧЁТ--)*цель_данные++=код_знака;return данные_позиция;}
void *memcpy(void*цель_данные,const void*строка_данные,size_t товар_СЧЁТ){unsigned char*첫째값=цель_данные;const unsigned char*СЕКУНДЫ_ЗНАЧЕН=строка_данные;while(товар_СЧЁТ--)*첫째값++=*СЕКУНДЫ_ЗНАЧЕН++;return цель_данные;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned координата_X,unsigned Y_координата,unsigned 너비,unsigned 높이,unsigned 색상){return экран_прямоугольник(координата_X,Y_координата,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int выписать_прямоугольник(unsigned 가로,unsigned Вертикаль_позиция,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Вертикаль_позиция,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
