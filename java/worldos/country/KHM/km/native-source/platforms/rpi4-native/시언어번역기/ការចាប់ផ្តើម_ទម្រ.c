#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char អាគុយម៉ង់_អារេ[8][256];
int អ្នកប្រើ_ផ្តើម(int 미사용값){
    (void)미사용값;char *អាគុយម៉ង់_បញ្ជី[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)អាគុយម៉ង់_អារេ[순번],256,0,0,0)<0)return 126;អាគុយម៉ង់_បញ្ជី[순번]=អាគុយម៉ង់_អារេ[순번];}អាគុយម៉ង់_បញ្ជី[인수개수]=0;
    return main(인수개수,អាគុយម៉ង់_បញ្ជី);
}
void *memset(void*ទិន្នន័យ_កំណត់ទីតាំង,int កូដនៃតួអក្សរ,size_t 개수){unsigned char*ទិសដៅ_ទិន្នន័យ=ទិន្នន័យ_កំណត់ទីតាំង;while(개수--)*ទិសដៅ_ទិន្នន័យ++=កូដនៃតួអក្សរ;return ទិន្នន័យ_កំណត់ទីតាំង;}
void *memcpy(void*ទិសដៅ_ទិន្នន័យ,const void*សំនុំអក្សរ_ទិន្នន័យ,size_t 개수){unsigned char*첫째값=ទិសដៅ_ទិន្នន័យ;const unsigned char*둘째값=សំនុំអក្សរ_ទិន្នន័យ;while(개수--)*첫째값++=*둘째값++;return ទិសដៅ_ទិន្នន័យ;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned កូអរដោណេ_x,unsigned ប៊ូតុង_Y_កូអរដោនេ,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(កូអរដោណេ_x,ប៊ូតុង_Y_កូអរដោនេ,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned បញ្ឈរ_កំណត់ទីតាំង,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,បញ្ឈរ_កំណត់ទីតាំង,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
