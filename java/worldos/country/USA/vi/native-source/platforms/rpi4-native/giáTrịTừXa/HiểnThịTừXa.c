/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 nốiKết, 제한된 giáTrịVào độDài, 비동기 gửiGiáTrị, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 MànHình DữLiệu 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "giáTrịTừXa.h"
#include "hỗTrợMậtMãHọc.h"
#include "hồSơ.h"
#include "../NgănXếpMạng/NgănXếpMạng.h"
#include "../máy/thôngTinMànHình.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(mậtKhẩuMànHình)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t miliGiâyGọnBoMạch(void);
extern uintptr_t thiếtBịCuốiBoMạch(uintptr_t);
void nétPhímTừXa(unsigned,int);
void khởiTạoNétPhímTừXa(void);
void phímTừXaChốt(void);
static int điểmCuốiĐangLắngNghe=-1,giáTrịĐốiTác=-1,giáTrịGiaiĐoạn,sẽĐóng;
static uintptr_t thờiGianKếtNối,lạiNhậnBậtTrạngThái;
static unsigned char giáTrịVào[8192],ĐầuRa[4096],giáTrịTháchThức[16];
static unsigned sốLượngĐầuVào,sốLượngĐầuRa,sốLượngĐãGửi;
static unsigned giáTrịRộng,giáTrịCao,cỡĐiểmẢnh=4,giáTrịThứTựByteLớn,tốiĐaĐỏ=255,tốiĐaXanhLục=255,tốiĐaXanhLam=255,dịchĐỏ=16,dịchXanhLục=8,dịchXanhLam;
static uint32_t tómLượcTrướcĐó[60*68];
static unsigned short ôLátĐãĐổi[60*68];
static unsigned sốLượngÔLát,vịTríÔLát,xĐãYêuCầu,yĐãYêuCầu,khoảngTrảiĐãYêuCầu,caoĐãYêuCầu;
static unsigned đọc16Bit(const unsigned char *vịTríDữLiệu){return(unsigned)vịTríDữLiệu[0]*256+vịTríDữLiệu[1];}
static uint32_t đọc32Bit(const unsigned char *vịTríDữLiệu){return(uint32_t)vịTríDữLiệu[0]<<24|(uint32_t)vịTríDữLiệu[1]<<16|(uint32_t)vịTríDữLiệu[2]<<8|vịTríDữLiệu[3];}
static void ghi16Bit(unsigned char *vịTríDữLiệu,unsigned giáTrị){vịTríDữLiệu[0]=giáTrị>>8;vịTríDữLiệu[1]=giáTrị;}
static void ghi32Bit(unsigned char *vịTríDữLiệu,uint32_t giáTrị){vịTríDữLiệu[0]=giáTrị>>24;vịTríDữLiệu[1]=giáTrị>>16;vịTríDữLiệu[2]=giáTrị>>8;vịTríDữLiệu[3]=giáTrị;}
static void đóng(void){if(giáTrịĐốiTác>=0)đóngMạng(giáTrịĐốiTác);giáTrịĐốiTác=-1;giáTrịGiaiĐoạn=0;sốLượngĐầuVào=sốLượngĐầuRa=sốLượngĐãGửi=0;sốLượngÔLát=vịTríÔLát=0;sẽĐóng=0;khởiTạoNétPhímTừXa();lạiNhậnBậtTrạngThái=miliGiâyGọnBoMạch()+500;}
static void phátGiáTrị(const void *DữLiệu,unsigned trịSố){memcpy(ĐầuRa,DữLiệu,trịSố);sốLượngĐầuRa=trịSố;sốLượngĐãGửi=0;}
static void tiêuThụGiáTrị(unsigned trịSố){sốLượngĐầuVào-=trịSố;memmove(giáTrịVào,giáTrịVào+trịSố,sốLượngĐầuVào);}
int hiểnThịTừXaĐiềuKhiển(unsigned hànhĐộng){
    if(hànhĐộng==0){đóng();if(điểmCuốiĐangLắngNghe>=0)đóngMạng(điểmCuốiĐangLắngNghe);điểmCuốiĐangLắngNghe=-1;return 0;}
    if(hànhĐộng!=1)return điểmCuốiĐangLắngNghe>=0;
    if(điểmCuốiĐangLắngNghe>=0)return 0;
    int giáTrịCổng=tạoĐiểmCuốiỔCắmMạng(1);if(giáTrịCổng<0)return giáTrịCổng;địaChỉỔCắmMạngDùngLại(giáTrịCổng);
    int kếtQuả=ràngBuộcMạngGọn(giáTrịCổng,0,5900);if(!kếtQuả)kếtQuả=lắngNgheMạngGọn(giáTrịCổng);
    if(kếtQuả<0){đóngMạng(giáTrịCổng);return kếtQuả;}điểmCuốiĐangLắngNghe=giáTrịCổng;return 0;
}
static uint32_t tómLượcÔLát(unsigned vịTríNgang,unsigned vịTríDọc){
    uint32_t giáTrị=2166136261u;
    for(unsigned tọaĐộY=vịTríDọc;tọaĐộY<vịTríDọc+16&&tọaĐộY<giáTrịCao;tọaĐộY++)for(unsigned tọaĐộX=vịTríNgang;tọaĐộX<vịTríNgang+32&&tọaĐộX<giáTrịRộng;tọaĐộX++)giáTrị=(giáTrị^mànHìnhĐọcBoMạch(tọaĐộX,tọaĐộY))*16777619u;
    return giáTrị;
}
static void yêuCầuMànHình(const unsigned char *vịTríDữLiệu){
    xĐãYêuCầu=đọc16Bit(vịTríDữLiệu+2);yĐãYêuCầu=đọc16Bit(vịTríDữLiệu+4);khoảngTrảiĐãYêuCầu=đọc16Bit(vịTríDữLiệu+6);caoĐãYêuCầu=đọc16Bit(vịTríDữLiệu+8);
    if(xĐãYêuCầu>=giáTrịRộng||yĐãYêuCầu>=giáTrịCao)khoảngTrảiĐãYêuCầu=caoĐãYêuCầu=0;
    if(khoảngTrảiĐãYêuCầu>giáTrịRộng-xĐãYêuCầu&&xĐãYêuCầu<giáTrịRộng)khoảngTrảiĐãYêuCầu=giáTrịRộng-xĐãYêuCầu;
    if(caoĐãYêuCầu>giáTrịCao-yĐãYêuCầu&&yĐãYêuCầu<giáTrịCao)caoĐãYêuCầu=giáTrịCao-yĐãYêuCầu;
    sốLượngÔLát=vịTríÔLát=0;
    if(khoảngTrảiĐãYêuCầu&&caoĐãYêuCầu)for(unsigned tọaĐộY=yĐãYêuCầu/16;tọaĐộY<=(yĐãYêuCầu+caoĐãYêuCầu-1)/16;tọaĐộY++)for(unsigned tọaĐộX=xĐãYêuCầu/32;tọaĐộX<=(xĐãYêuCầu+khoảngTrảiĐãYêuCầu-1)/32;tọaĐộX++){
        unsigned chỉSốVịTrí=tọaĐộY*60+tọaĐộX;uint32_t giáTrịTómLược=tómLượcÔLát(tọaĐộX*32,tọaĐộY*16);
        if(!vịTríDữLiệu[1]||tómLượcTrướcĐó[chỉSốVịTrí]!=giáTrịTómLược)ôLátĐãĐổi[sốLượngÔLát++]=chỉSốVịTrí;
    }
    ĐầuRa[0]=ĐầuRa[1]=0;ghi16Bit(ĐầuRa+2,sốLượngÔLát);sốLượngĐầuRa=4;sốLượngĐãGửi=0;
}
static void gửiÔLát(void){
    unsigned chỉSốVịTrí=ôLátĐãĐổi[vịTríÔLát++],vịTríNgang=(chỉSốVịTrí%60)*32,vịTríDọc=(chỉSốVịTrí/60)*16;
    unsigned xKếtThúc=vịTríNgang+32,yKếtThúc=vịTríDọc+16;if(xKếtThúc>giáTrịRộng)xKếtThúc=giáTrịRộng;if(yKếtThúc>giáTrịCao)yKếtThúc=giáTrịCao;
    /* giáTrịPhầnCon 타일 yêuCầu 뒤에도 giáTrịSốDư 화소를 보낸 것으로 처리하지 않는다. */
    int cácGiáTrịTấtCả=vịTríNgang>=xĐãYêuCầu&&vịTríDọc>=yĐãYêuCầu&&xKếtThúc<=xĐãYêuCầu+khoảngTrảiĐãYêuCầu&&yKếtThúc<=yĐãYêuCầu+caoĐãYêuCầu;
    if(cácGiáTrịTấtCả)tómLượcTrướcĐó[chỉSốVịTrí]=tómLượcÔLát(vịTríNgang,vịTríDọc);
    if(vịTríNgang<xĐãYêuCầu)vịTríNgang=xĐãYêuCầu;if(vịTríDọc<yĐãYêuCầu)vịTríDọc=yĐãYêuCầu;
    if(xKếtThúc>xĐãYêuCầu+khoảngTrảiĐãYêuCầu)xKếtThúc=xĐãYêuCầu+khoảngTrảiĐãYêuCầu;if(yKếtThúc>yĐãYêuCầu+caoĐãYêuCầu)yKếtThúc=yĐãYêuCầu+caoĐãYêuCầu;
    ghi16Bit(ĐầuRa,vịTríNgang);ghi16Bit(ĐầuRa+2,vịTríDọc);ghi16Bit(ĐầuRa+4,xKếtThúc-vịTríNgang);ghi16Bit(ĐầuRa+6,yKếtThúc-vịTríDọc);ghi32Bit(ĐầuRa+8,0);
    sốLượngĐầuRa=12;sốLượngĐãGửi=0;
    for(unsigned tọaĐộY=vịTríDọc;tọaĐộY<yKếtThúc;tọaĐộY++)for(unsigned tọaĐộX=vịTríNgang;tọaĐộX<xKếtThúc;tọaĐộX++){
        uint32_t giáTrịMàu=mànHìnhĐọcBoMạch(tọaĐộX,tọaĐộY),giáTrị=(((giáTrịMàu>>16)&255)*tốiĐaĐỏ/255)<<dịchĐỏ|
            (((giáTrịMàu>>8)&255)*tốiĐaXanhLục/255)<<dịchXanhLục|((giáTrịMàu&255)*tốiĐaXanhLam/255)<<dịchXanhLam;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<cỡĐiểmẢnh;chỉSốThứBậc++)ĐầuRa[sốLượngĐầuRa++]=giáTrị>>(8*(giáTrịThứTựByteLớn?cỡĐiểmẢnh-1-chỉSốThứBậc:chỉSốThứBậc));
    }
}
void xemXétHiểnThịTừXa(void){
    if(điểmCuốiĐangLắngNghe<0)return;
    if(giáTrịĐốiTác<0){if(miliGiâyGọnBoMạch()<lạiNhậnBậtTrạngThái)return;giáTrịĐốiTác=chấpNhậnMạngGọn(điểmCuốiĐangLắngNghe);if(giáTrịĐốiTác<0)return;
        thờiGianKếtNối=miliGiâyGọnBoMạch();giáTrịGiaiĐoạn=1;phátGiáTrị("RFB 003.008\n",12);memset(tómLượcTrướcĐó,0,sizeof(tómLượcTrướcĐó));
        cỡĐiểmẢnh=4;giáTrịThứTựByteLớn=0;tốiĐaĐỏ=tốiĐaXanhLục=tốiĐaXanhLam=255;dịchĐỏ=16;dịchXanhLục=8;dịchXanhLam=0;}
    if(giáTrịGiaiĐoạn<5&&miliGiâyGọnBoMạch()-thờiGianKếtNối>15000){đóng();return;}
    if(sốLượngĐầuRa){int trịSố=ghiMạngGọn(giáTrịĐốiTác,ĐầuRa+sốLượngĐãGửi,sốLượngĐầuRa-sốLượngĐãGửi);if(trịSố>0){sốLượngĐãGửi+=trịSố;if(sốLượngĐãGửi==sốLượngĐầuRa)sốLượngĐầuRa=sốLượngĐãGửi=0;}else if(trịSố!=-11){đóng();return;}}
    if(!sốLượngĐầuRa&&sẽĐóng){đóng();return;}
    if(!sốLượngĐầuRa&&vịTríÔLát<sốLượngÔLát)gửiÔLát();
    if(sốLượngĐầuVào==sizeof(giáTrịVào)){đóng();return;}
    int sốLượngĐãNhận=đọcMạngGọn(giáTrịĐốiTác,giáTrịVào+sốLượngĐầuVào,sizeof(giáTrịVào)-sốLượngĐầuVào);
    if(sốLượngĐãNhận==0||(sốLượngĐãNhận<0&&sốLượngĐãNhận!=-11)){đóng();return;}if(sốLượngĐãNhận>0)sốLượngĐầuVào+=sốLượngĐãNhận;
    if(sốLượngĐầuRa||vịTríÔLát<sốLượngÔLát)return;
    if(giáTrịGiaiĐoạn==1&&sốLượngĐầuVào>=12){if(memcmp(giáTrịVào,"RFB 003.008\n",12)){đóng();return;}tiêuThụGiáTrị(12);const unsigned char phươngThứcXácThực[]={1,2};phátGiáTrị(phươngThứcXácThực,2);giáTrịGiaiĐoạn=2;return;}
    if(giáTrịGiaiĐoạn==2&&sốLượngĐầuVào){if(giáTrịVào[0]!=2||ngẫuNhiênTừXa(giáTrịTháchThức,16)){đóng();return;}tiêuThụGiáTrị(1);phátGiáTrị(giáTrịTháchThức,16);giáTrịGiaiĐoạn=3;return;}
    if(giáTrịGiaiĐoạn==3&&sốLượngĐầuVào>=16){unsigned char vậtLiệuPhím[8],trảLờiĐúng[16];br_des_ct_cbcenc_keys giáTrịMậtKhẩu;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<8;chỉSốThứBậc++){unsigned giáTrị=mậtKhẩuMànHình[chỉSốThứBậc],làĐảoNgược=0;for(unsigned thứBậcPhíaTrong=0;thứBậcPhíaTrong<8;thứBậcPhíaTrong++){làĐảoNgược=(làĐảoNgược<<1)|(giáTrị&1);giáTrị>>=1;}vậtLiệuPhím[chỉSốThứBậc]=làĐảoNgược;}
        br_des_ct_cbcenc_init(&giáTrịMậtKhẩu,vậtLiệuPhím,8);memcpy(trảLờiĐúng,giáTrịTháchThức,16);
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<16;chỉSốThứBậc+=8){unsigned char giáTrịVécTơ[8]={0};br_des_ct_cbcenc_run(&giáTrịMậtKhẩu,giáTrịVécTơ,trảLờiĐúng+chỉSốThứBậc,8);memset(giáTrịVécTơ,0,8);}
        unsigned giáTrịKhácBiệt=0;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<16;chỉSốThứBậc++)giáTrịKhácBiệt|=trảLờiĐúng[chỉSốThứBậc]^giáTrịVào[chỉSốThứBậc];tiêuThụGiáTrị(16);memset(&giáTrịMậtKhẩu,0,sizeof(giáTrịMậtKhẩu));memset(vậtLiệuPhím,0,8);memset(trảLờiĐúng,0,16);memset(giáTrịTháchThức,0,16);
        ghi32Bit(ĐầuRa,giáTrịKhácBiệt?1:0);sốLượngĐầuRa=4;sốLượngĐãGửi=0;
        if(giáTrịKhácBiệt){ghi32Bit(ĐầuRa+4,19);memcpy(ĐầuRa+8,"Authentication fail",19);sốLượngĐầuRa=27;sẽĐóng=1;}else giáTrịGiaiĐoạn=4;return;}
    if(giáTrịGiaiĐoạn==4&&sốLượngĐầuVào){tiêuThụGiáTrị(1);giáTrịRộng=rộngMànHìnhBoMạch();giáTrịCao=caoMànHìnhBoMạch();if(!giáTrịRộng||!giáTrịCao||giáTrịRộng>1920||giáTrịCao>1080){đóng();return;}
        if(!thiếtBịCuốiBoMạch(7)){const unsigned char sựKiện[]={30,2,1,0,0,0,0};đầuVàoTừXaCấp(sựKiện,7);}
        memset(ĐầuRa,0,40);ghi16Bit(ĐầuRa,giáTrịRộng);ghi16Bit(ĐầuRa+2,giáTrịCao);ĐầuRa[4]=32;ĐầuRa[5]=24;ĐầuRa[7]=1;
        ghi16Bit(ĐầuRa+8,255);ghi16Bit(ĐầuRa+10,255);ghi16Bit(ĐầuRa+12,255);ĐầuRa[14]=16;ĐầuRa[15]=8;
        const char *tên="jkoros native";ghi32Bit(ĐầuRa+20,strlen(tên));memcpy(ĐầuRa+24,tên,strlen(tên));sốLượngĐầuRa=24+strlen(tên);sốLượngĐãGửi=0;giáTrịGiaiĐoạn=5;return;}
    if(giáTrịGiaiĐoạn!=5||!sốLượngĐầuVào)return;
    unsigned loạiMụcKiểu=giáTrịVào[0],giáTrịCầnĐến=loạiMụcKiểu==0?20:loạiMụcKiểu==2?4:loạiMụcKiểu==3?10:loạiMụcKiểu==4?8:loạiMụcKiểu==5?6:loạiMụcKiểu==6?8:0;
    if(!giáTrịCầnĐến){đóng();return;}if(sốLượngĐầuVào<giáTrịCầnĐến)return;
    if(loạiMụcKiểu==2){unsigned trịSố=đọc16Bit(giáTrịVào+2);if(trịSố>128){đóng();return;}giáTrịCầnĐến+=trịSố*4;}
    if(loạiMụcKiểu==6){unsigned trịSố=đọc32Bit(giáTrịVào+4);if(trịSố>4096){đóng();return;}giáTrịCầnĐến+=trịSố;}
    if(sốLượngĐầuVào<giáTrịCầnĐến)return;
    if(loạiMụcKiểu==0){unsigned giáTrịBit=giáTrịVào[4],tốiĐaKênhĐỏ=đọc16Bit(giáTrịVào+8),giáTrịGiây=đọc16Bit(giáTrịVào+10),tốiĐaKênhXanhLam=đọc16Bit(giáTrịVào+12),dịchKênhĐỏ=giáTrịVào[14],dịchKênhXanhLục=giáTrịVào[15],dịchKênhXanhLam=giáTrịVào[16];
        if((giáTrịBit!=16&&giáTrịBit!=32)||!giáTrịVào[7]||giáTrịVào[6]>1||!tốiĐaKênhĐỏ||!giáTrịGiây||!tốiĐaKênhXanhLam||tốiĐaKênhĐỏ>255||giáTrịGiây>255||tốiĐaKênhXanhLam>255||dịchKênhĐỏ>24||dịchKênhXanhLục>24||dịchKênhXanhLam>24||
           ((uint64_t)tốiĐaKênhĐỏ<<dịchKênhĐỏ)>((1ull<<giáTrịBit)-1)||((uint64_t)giáTrịGiây<<dịchKênhXanhLục)>((1ull<<giáTrịBit)-1)||((uint64_t)tốiĐaKênhXanhLam<<dịchKênhXanhLam)>((1ull<<giáTrịBit)-1)){đóng();return;}
        cỡĐiểmẢnh=giáTrịBit/8;giáTrịThứTựByteLớn=giáTrịVào[6];tốiĐaĐỏ=tốiĐaKênhĐỏ;tốiĐaXanhLục=giáTrịGiây;tốiĐaXanhLam=tốiĐaKênhXanhLam;dịchĐỏ=dịchKênhĐỏ;dịchXanhLục=dịchKênhXanhLục;dịchXanhLam=dịchKênhXanhLam;memset(tómLượcTrướcĐó,0,sizeof(tómLượcTrướcĐó));
    }else if(loạiMụcKiểu==3)yêuCầuMànHình(giáTrịVào);
    else if(loạiMụcKiểu==4)nétPhímTừXa(đọc32Bit(giáTrịVào+4),giáTrịVào[1]!=0);
    else if(loạiMụcKiểu==5){unsigned tọaĐộX=đọc16Bit(giáTrịVào+2),tọaĐộY=đọc16Bit(giáTrịVào+4);if(tọaĐộX>=giáTrịRộng)tọaĐộX=giáTrịRộng-1;if(tọaĐộY>=giáTrịCao)tọaĐộY=giáTrịCao-1;
        if(giáTrịVào[1])phímTừXaChốt();
        unsigned char sựKiện[]={30,1,giáTrịVào[1],tọaĐộX&255,tọaĐộX>>8,tọaĐộY&255,tọaĐộY>>8};đầuVàoTừXaCấp(sựKiện,sizeof(sựKiện));}
    tiêuThụGiáTrị(giáTrịCầnĐến);
}
