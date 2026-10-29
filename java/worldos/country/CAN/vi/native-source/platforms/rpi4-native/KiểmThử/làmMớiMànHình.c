#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "../máy/thôngTinMànHình.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void dừngKhẩnNhân(const char *môTả){fputs(môTả,stderr);abort();}
extern uintptr_t thiếtBịCuốiBoMạch(uintptr_t),điểmẢnhBoMạch(uintptr_t,uintptr_t,uintptr_t);
extern void conTrỏThiếtBịCuối(unsigned,int,int),byteThiếtBịCuối(unsigned);
extern int gọiThựcHiệnMànHình(int,unsigned,int,int,int,int,int);
static uint32_t MànHình[1080][1936],ảnhPhépSoSánh[1080][1936];
uintptr_t bộĐệmKhungBoMạch(void){return 1;}
static void soSánhToànBộ(void){
    conTrỏBoMạch(0,0,0);memcpy(ảnhPhépSoSánh,MànHình,sizeof(MànHình));
    uint64_t phầnMụcTrướcĐó=sốLượngBảnVẽBoMạch();thiếtBịCuốiBoMạch(3);
    assert(memcmp(ảnhPhépSoSánh,MànHình,sizeof(MànHình))==0);
    assert(sốLượngBảnVẽBoMạch()==phầnMụcTrướcĐó); /* 같은 화면을 giáTrịThửLại 그려도 hiệnGiáTrị 메모리에 쓰지 않는다. */
}
static void ghiVănBản(const char *vănBản){while(*vănBản)byteThiếtBịCuối((unsigned char)*vănBản++);}
int main(void){
    bảnVẽChuẩnBịBoMạch(&MànHình[0][0],1920,1080,sizeof(MànHình[0]));
    thiếtBịCuốiBoMạch(300);ghiVănBản("phầnMụcĐầuTiên 창의 한글 DữLiệu\n");
    for(int sốHiệu=1;sốHiệu<4;sốHiệu++){thiếtBịCuốiBoMạch(1);thiếtBịCuốiBoMạch(100+sốHiệu);ghiVănBản("겹친 창의 한글 DữLiệu\n\033[41m색칠한 bỏKhoảngTrắng     \033[0m\n");}
    soSánhToànBộ();
    int vịTríNgang=60,vịTríDọc=102,khoảngTrảiRộng=568,giáTrịCao=360;
    uint64_t nhậtKýDiChuyển=0;double thờiGianChuyểnĐộng=0;
    for(int giáTrịDãy=0;giáTrịDãy<80;giáTrịDãy++){
        conTrỏThiếtBịCuối(1,vịTríNgang+100,vịTríDọc+15);
        int vịTríNgangMới=80+(giáTrịDãy*37)%850,vịTríDọcMới=50+(giáTrịDãy*13)%450;
        điểmẢnhBoMạch(1900,1050,0x123456); /* làmMới giáTrịMiền 밖의 NgườiDùng HìnhVẽ */
        uint64_t phầnMụcTrướcĐó=sốLượngBảnVẽBoMạch();clock_t chạy=clock();
        conTrỏThiếtBịCuối(1,vịTríNgangMới+100,vịTríDọcMới+15);
        thờiGianChuyểnĐộng+=(double)(clock()-chạy)/CLOCKS_PER_SEC;
        nhậtKýDiChuyển+=sốLượngBảnVẽBoMạch()-phầnMụcTrướcĐó;
        assert(sốLượngBảnVẽBoMạch()-phầnMụcTrướcĐó<=2u*khoảngTrảiRộng*giáTrịCao);
        assert(MànHình[1050][1900]==0x123456);
        điểmẢnhBoMạch(1900,1050,0x302018);
        conTrỏThiếtBịCuối(0,vịTríNgangMới+100,vịTríDọcMới+15);vịTríNgang=vịTríNgangMới;vịTríDọc=vịTríDọcMới;
        soSánhToànBộ();
    }
    for(int giáTrịDãy=0;giáTrịDãy<40;giáTrịDãy++){
        int rộngMới=360+(giáTrịDãy*29)%700,caoMới=216+(giáTrịDãy*17)%350;
        if(rộngMới>1920-vịTríNgang)rộngMới=1920-vịTríNgang;if(caoMới>1080-vịTríDọc)caoMới=1080-vịTríDọc;
        conTrỏThiếtBịCuối(1,vịTríNgang+khoảngTrảiRộng-4,vịTríDọc+giáTrịCao-4);
        conTrỏThiếtBịCuối(1,vịTríNgang+rộngMới-4,vịTríDọc+caoMới-4);
        uint64_t phầnMụcTrướcĐó=sốLượngBảnVẽBoMạch();
        conTrỏThiếtBịCuối(1,vịTríNgang+rộngMới-4,vịTríDọc+caoMới-4);
        assert(sốLượngBảnVẽBoMạch()==phầnMụcTrướcĐó); /* 같은 좌표의 중복 sựKiện */
        conTrỏThiếtBịCuối(0,vịTríNgang+rộngMới-4,vịTríDọc+caoMới-4);khoảngTrảiRộng=rộngMới;giáTrịCao=caoMới;
        soSánhToànBộ();
    }
    /* giáTrịĐãCắtXén 범위와 dữLiệuThựcTế dòng 간격을 지킨다. */
    for(int dòng=0;dòng<1080;dòng++)for(int mụcÔ=1920;mụcÔ<1936;mụcÔ++)assert(MànHình[dòng][mụcÔ]==0);
    assert(!bảnVẽBắtChạyBoMạch(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",thờiGianChuyểnĐộng*1000/80,(unsigned long long)(nhậtKýDiChuyển/80));
    return 0;
}
