#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char కారకం_శ్రేణి[8][256];
int వినియోగదారు_ప్రారంభం(int 미사용값){
    (void)미사용값;char *కారకం_జాబితా[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)కారకం_శ్రేణి[순번],256,0,0,0)<0)return 126;కారకం_జాబితా[순번]=కారకం_శ్రేణి[순번];}కారకం_జాబితా[인수개수]=0;
    return main(인수개수,కారకం_జాబితా);
}
void *memset(void*డేటా_స్థాయి,int అక్షర_కోడ్,size_t 개수){unsigned char*గమ్యం_డేటా=డేటా_స్థాయి;while(개수--)*గమ్యం_డేటా++=అక్షర_కోడ్;return డేటా_స్థాయి;}
void *memcpy(void*గమ్యం_డేటా,const void*అక్షరసరం_డేటా,size_t 개수){unsigned char*첫째값=గమ్యం_డేటా;const unsigned char*둘째값=అక్షరసరం_డేటా;while(개수--)*첫째값++=*둘째값++;return గమ్యం_డేటా;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_నిర్దేశాంకం,unsigned Y_బటన్_సమన్వయపరుచు,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned నిలువు_స్థాయి,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,నిలువు_స్థాయి,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
