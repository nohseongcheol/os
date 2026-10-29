#include "giáTrịTừXa.h"
#include <string.h>
#include "bảngTraBànPhímĐặtGiáTrịHai.h"
static unsigned giáTrịĐiềuKhiển,phímDịch,vănBảnHangul;
typedef struct {unsigned phầnMụcĐầuTiên,giữa,phầnKết;} trạngTháiPhépGhép;
static trạngTháiPhépGhép PhốiHợp,bảnGhiNhậtKý[16];
static unsigned sốLượngNhậtKý;
void phímTừXaChốt(void){memset(&PhốiHợp,0,sizeof(PhốiHợp));sốLượngNhậtKý=0;}
void khởiTạoNétPhímTừXa(void){giáTrịĐiềuKhiển=phímDịch=vănBảnHangul=0;phímTừXaChốt();}
static void đặtVănBản(unsigned giáTrị){
    unsigned char vănBản[4];unsigned trịSố;
    if(giáTrị<128){vănBản[0]=giáTrị;trịSố=1;}else if(giáTrị<2048){vănBản[0]=0xc0|(giáTrị>>6);vănBản[1]=0x80|(giáTrị&63);trịSố=2;}
    else if(giáTrị<65536){vănBản[0]=0xe0|(giáTrị>>12);vănBản[1]=0x80|((giáTrị>>6)&63);vănBản[2]=0x80|(giáTrị&63);trịSố=3;}
    else{vănBản[0]=0xf0|(giáTrị>>18);vănBản[1]=0x80|((giáTrị>>12)&63);vănBản[2]=0x80|((giáTrị>>6)&63);vănBản[3]=0x80|(giáTrị&63);trịSố=4;}
    đầuVàoTừXaCấp(vănBản,trịSố);
}
static int tìmMục(const unsigned *danhSáchMục,unsigned trịSố,unsigned giáTrị){for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<trịSố;chỉSốThứBậc++)if(danhSáchMục[chỉSốThứBậc]==giáTrị)return chỉSốThứBậc;return -1;}
static unsigned tìmBảnSao(const unsigned Bảng[][3],unsigned trịSố,unsigned toánHạngĐầuTiên,unsigned toánHạngThứHai){for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<trịSố;chỉSốThứBậc++)if(Bảng[chỉSốThứBậc][0]==toánHạngĐầuTiên&&Bảng[chỉSốThứBậc][1]==toánHạngThứHai)return Bảng[chỉSốThứBậc][2];return 0;}
static unsigned vănBảnĐãGhép(void){
    if(PhốiHợp.phầnMụcĐầuTiên&&PhốiHợp.giữa)return 0xac00+(tìmMục(bảngTraJamoBanĐầu,19,PhốiHợp.phầnMụcĐầuTiên)*21+tìmMục(bảngTraJamoỞGiữa,21,PhốiHợp.giữa))*28+(PhốiHợp.phầnKết?tìmMục(bảngTraJamoCuốiCùng,28,PhốiHợp.phầnKết):0);
    return PhốiHợp.phầnMụcĐầuTiên?PhốiHợp.phầnMụcĐầuTiên:PhốiHợp.giữa;
}
static int hangulCấp(unsigned nétPhím){
    unsigned giáTrịJamo=0;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sizeof(bốTríPhím)/sizeof(bốTríPhím[0]);chỉSốThứBậc++)if(bốTríPhím[chỉSốThứBậc][0]==nétPhím)giáTrịJamo=bốTríPhím[chỉSốThứBậc][1];
    if(!giáTrịJamo&&nétPhím>='A'&&nétPhím<='Z')return hangulCấp(nétPhím+32);if(!giáTrịJamo)return 0;
    unsigned phầnMụcTrướcĐó=vănBảnĐãGhép(),giáTrịChốt=0;trạngTháiPhépGhép giáTrịTrướcKhi=PhốiHợp;
    if(sốLượngNhậtKý<16)bảnGhiNhậtKý[sốLượngNhậtKý++]=giáTrịTrướcKhi;
    if(tìmMục(bảngTraJamoBanĐầu,19,giáTrịJamo)>=0){
        if(PhốiHợp.phầnMụcĐầuTiên&&PhốiHợp.giữa&&!PhốiHợp.phầnKết&&tìmMục(bảngTraJamoCuốiCùng,28,giáTrịJamo)>=0)PhốiHợp.phầnKết=giáTrịJamo;
        else{unsigned giáTrịLớpPhủ=tìmBảnSao(jamoCuốiCùngPhứcHợp,11,PhốiHợp.phầnKết,giáTrịJamo);if(PhốiHợp.phầnKết&&giáTrịLớpPhủ)PhốiHợp.phầnKết=giáTrịLớpPhủ;
            else{giáTrịChốt=phầnMụcTrướcĐó;phímTừXaChốt();PhốiHợp.phầnMụcĐầuTiên=giáTrịJamo;sốLượngNhậtKý=1;memset(bảnGhiNhậtKý,0,sizeof(trạngTháiPhépGhép));}}
    }else if(PhốiHợp.phầnKết){
        unsigned bênTrái=0,phải=PhốiHợp.phầnKết;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<11;chỉSốThứBậc++)if(jamoCuốiCùngPhứcHợp[chỉSốThứBậc][2]==PhốiHợp.phầnKết){bênTrái=jamoCuốiCùngPhứcHợp[chỉSốThứBậc][0];phải=jamoCuốiCùngPhứcHợp[chỉSốThứBậc][1];break;}
        PhốiHợp.phầnKết=bênTrái;giáTrịChốt=vănBảnĐãGhép();phímTừXaChốt();PhốiHợp.phầnMụcĐầuTiên=phải;PhốiHợp.giữa=giáTrịJamo;sốLượngNhậtKý=2;
        memset(bảnGhiNhậtKý,0,2*sizeof(trạngTháiPhépGhép));bảnGhiNhậtKý[1].phầnMụcĐầuTiên=phải;
    }else if(PhốiHợp.giữa){unsigned giáTrịLớpPhủ=tìmBảnSao(jamoỞGiữaPhứcHợp,7,PhốiHợp.giữa,giáTrịJamo);
        if(giáTrịLớpPhủ)PhốiHợp.giữa=giáTrịLớpPhủ;else{giáTrịChốt=phầnMụcTrướcĐó;phímTừXaChốt();PhốiHợp.giữa=giáTrịJamo;sốLượngNhậtKý=1;memset(bảnGhiNhậtKý,0,sizeof(trạngTháiPhépGhép));}
    }else PhốiHợp.giữa=giáTrịJamo;
    if(phầnMụcTrướcĐó)đặtVănBản(127);if(giáTrịChốt)đặtVănBản(giáTrịChốt);unsigned giáTrịBâyGiờ=vănBảnĐãGhép();if(giáTrịBâyGiờ)đặtVănBản(giáTrịBâyGiờ);return 1;
}
void nétPhímTừXa(unsigned kýHiệu,int giáTrịNhấn){
    if(kýHiệu==0xffe3||kýHiệu==0xffe4){giáTrịĐiềuKhiển=giáTrịNhấn;return;}
    if(kýHiệu==0xffe1||kýHiệu==0xffe2){phímDịch=giáTrịNhấn;return;}
    if(!giáTrịNhấn)return;
    if(kýHiệu==0xffc6||kýHiệu==0xff31||(kýHiệu==32&&phímDịch&&!giáTrịĐiềuKhiển)){
        phímTừXaChốt();vănBảnHangul=!vănBảnHangul;unsigned char sựKiện[]={30,3,vănBảnHangul,0,0,0,0};đầuVàoTừXaCấp(sựKiện,7);return;
    }
    if(kýHiệu==0xff08&&vănBảnHangul&&!giáTrịĐiềuKhiển&&sốLượngNhậtKý){PhốiHợp=bảnGhiNhậtKý[--sốLượngNhậtKý];đặtVănBản(127);unsigned vănBản=vănBảnĐãGhép();if(vănBản)đặtVănBản(vănBản);return;}
    if(vănBảnHangul&&!giáTrịĐiềuKhiển&&kýHiệu<128&&hangulCấp(kýHiệu))return;
    phímTừXaChốt();
    if((giáTrịĐiềuKhiển&&phímDịch&&(kýHiệu=='t'||kýHiệu=='T'))||kýHiệu==0xffc3||kýHiệu==0xffc9){unsigned char sựKiện[]={30,2,kýHiệu==0xffc3?2:kýHiệu==0xffc9?3:1,0,0,0,0};đầuVàoTừXaCấp(sựKiện,7);return;}
    const char *giáTrịĐặcBiệt=kýHiệu==0xff08?"\177":kýHiệu==0xff09?"\t":kýHiệu==0xff0d?"\r":kýHiệu==0xff1b?"\033":
        kýHiệu==0xffff?"\033[3~":kýHiệu==0xff50?"\033[H":kýHiệu==0xff57?"\033[F":kýHiệu==0xff51?"\033[D":
        kýHiệu==0xff52?"\033[A":kýHiệu==0xff53?"\033[C":kýHiệu==0xff54?"\033[B":kýHiệu==0xff55?"\033[5~":kýHiệu==0xff56?"\033[6~":0;
    if(giáTrịĐặcBiệt){đầuVàoTừXaCấp((const unsigned char*)giáTrịĐặcBiệt,strlen(giáTrịĐặcBiệt));return;}
    unsigned giáTrị=(kýHiệu&0xff000000)==0x01000000?kýHiệu&0xffffff:kýHiệu;
    if(giáTrị>0x10ffff||(giáTrị>=0xd800&&giáTrị<=0xdfff)||(kýHiệu>=0xff00&&kýHiệu<0x1000000))return;
    if(giáTrịĐiềuKhiển){if(giáTrị>='a'&&giáTrị<='z')giáTrị-=96;else if(giáTrị>='A'&&giáTrị<='Z')giáTrị-=64;}
    đặtVănBản(giáTrị);
}
