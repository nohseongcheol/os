#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "gọiThựcHiện.h"
extern int main(int,char **);
static char mảngĐốiSố[8][256];
int bắtChạyNgườiDùng(int chưaDùng){
    (void)chưaDùng;char *danhSáchĐốiSố[9];int sốLượngCácĐốiSố=gọiThựcHiệnNgườiDùng(15,UINTPTR_MAX,0,0,0,0,0);
    if(sốLượngCácĐốiSố<0||sốLượngCácĐốiSố>8)return 126;
    for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngCácĐốiSố;chỉSốThứBậc++){if(gọiThựcHiệnNgườiDùng(15,chỉSốThứBậc,(uintptr_t)mảngĐốiSố[chỉSốThứBậc],256,0,0,0)<0)return 126;danhSáchĐốiSố[chỉSốThứBậc]=mảngĐốiSố[chỉSốThứBậc];}danhSáchĐốiSố[sốLượngCácĐốiSố]=0;
    return main(sốLượngCácĐốiSố,danhSáchĐốiSố);
}
void *memset(void*vịTríDữLiệu,int mãKýTự,size_t sốLượngPhầnMục){unsigned char*dữLiệuĐích=vịTríDữLiệu;while(sốLượngPhầnMục--)*dữLiệuĐích++=mãKýTự;return vịTríDữLiệu;}
void *memcpy(void*dữLiệuĐích,const void*dữLiệuChuỗi,size_t sốLượngPhầnMục){unsigned char*giáTrịĐầuTiên=dữLiệuĐích;const unsigned char*giáTrịThứHai=dữLiệuChuỗi;while(sốLượngPhầnMục--)*giáTrịĐầuTiên++=*giáTrịThứHai++;return dữLiệuĐích;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned tọaĐộX,unsigned tọaĐộY,unsigned giáTrịRộng,unsigned giáTrịCao,unsigned màuĐiểmẢnh){return hìnhChữNhậtMànHình(tọaĐộX,tọaĐộY,giáTrịRộng,giáTrịCao,màuĐiểmẢnh);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return gọiThựcHiệnNgườiDùng(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return chờPhímMànHìnhCho();}
int vẽHìnhChữNhật(unsigned vịTríNgang,unsigned vịTríDọc,unsigned giáTrịRộng,unsigned giáTrịCao,unsigned màuĐiểmẢnh){return pk_rectangle(vịTríNgang,vịTríDọc,giáTrịRộng,giáTrịCao,màuĐiểmẢnh);}
unsigned miliGiây(void){return pk_ticks_ms();}
int chờBảnVẽCho(void){return pk_graphics_wait();}
int rộngMànHình(void){return đọcRộngMànHình();}
int caoMànHình(void){return đọcCaoMànHình();}
