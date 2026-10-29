#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char bağımsız_değişken_DİZİ[8][256];
int kullanıcı_Start(int 미사용값){
    (void)미사용값;char *bağımsız_değişken_Liste[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)bağımsız_değişken_DİZİ[순번],256,0,0,0)<0)return 126;bağımsız_değişken_Liste[순번]=bağımsız_değişken_DİZİ[순번];}bağımsız_değişken_Liste[인수개수]=0;
    return main(인수개수,bağımsız_değişken_Liste);
}
void *memset(void*veri_konum,int kod_noktası,size_t öğe_BAĞ_DEĞ_SAY){unsigned char*hedef_veri=veri_konum;while(öğe_BAĞ_DEĞ_SAY--)*hedef_veri++=kod_noktası;return veri_konum;}
void *memcpy(void*hedef_veri,const void*dize_veri,size_t öğe_BAĞ_DEĞ_SAY){unsigned char*첫째값=hedef_veri;const unsigned char*SANİYE_değer=dize_veri;while(öğe_BAĞ_DEĞ_SAY--)*첫째값++=*SANİYE_değer++;return hedef_veri;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_koordinatı,unsigned Y_koordinat,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_koordinatı,Y_koordinat,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Çizim_dikdörtgen(unsigned 가로,unsigned Dikey_konum,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Dikey_konum,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
