/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "gọiThựcHiện.h"
#include "ABITệp.h"
#define sứcChứaTrìnhSoạnThảo 16384
static unsigned char vănBản[sứcChứaTrìnhSoạnThảo],dữLiệuHoànTác[sứcChứaTrìnhSoạnThảo],dữLiệuĐãSaoChép[sứcChứaTrìnhSoạnThảo],dữLiệuKếtQuả[1024];
static int độDài,giáTrịChỉSố,mụcĐỉnh,bênTrái,đãĐổiĐãLà,chèn,độDàiHoànTác,bênThượng,cácThayĐổiHoànTác,hoànTácSởHữu,saoChépĐộDài,sứcChứaĐãDùng,cácCột=68,sốLượngHàng=19;
static char tênMụcTệp[64],lệnh[128],tìmMục[128];
static const char *vănBảnThôngBáo="NORMAL  i:insert  :w:save  :q:quit";
static unsigned phímĐangChờ;
static int loạiMụcTrợGiúp,ảnhTrạngThái,hàngĐợiTrạngThái;
static void đẩyĐệm(void){if(sứcChứaĐãDùng){gọiThựcHiệnNgườiDùng(1,1,(uintptr_t)dữLiệuKếtQuả,sứcChứaĐãDùng,0,0,0);sứcChứaĐãDùng=0;}}
static void dữLiệuByte(unsigned mãKýTự){if(ảnhTrạngThái){if((mãKýTự&192)!=128){hàngĐợiTrạngThái+=mãKýTự>=196?2:1;}if(hàngĐợiTrạngThái>=cácCột)return;}if(sứcChứaĐãDùng==(int)sizeof(dữLiệuKếtQuả))đẩyĐệm();dữLiệuKếtQuả[sứcChứaĐãDùng++]=mãKýTự;}
static void phátVănBản(const char *dữLiệuChuỗi){while(*dữLiệuChuỗi)dữLiệuByte((unsigned char)*dữLiệuChuỗi++);}
static void giáTrịThuộcSố(unsigned sốLượngPhầnMục){char giáTrịThứHai[12];int chỉSốThứBậc=0;do{giáTrịThứHai[chỉSốThứBậc++]='0'+sốLượngPhầnMục%10;sốLượngPhầnMục/=10;}while(sốLượngPhầnMục);while(chỉSốThứBậc)dữLiệuByte(giáTrịThứHai[--chỉSốThứBậc]);}
static void giáTrịDiChuyển(int vịTríHàng,int vịTríCột){phátVănBản("\033[");giáTrịThuộcSố(vịTríHàng);dữLiệuByte(';');giáTrịThuộcSố(vịTríCột);dữLiệuByte('H');}
static int trướcĐó(int vịTríDữLiệu){if(vịTríDữLiệu){vịTríDữLiệu--;while(vịTríDữLiệu>0&&(vănBản[vịTríDữLiệu]&192)==128)vịTríDữLiệu--;}return vịTríDữLiệu;}
static int phầnMụcKếTiếp(int vịTríDữLiệu){if(vịTríDữLiệu<độDài){vịTríDữLiệu++;while(vịTríDữLiệu<độDài&&(vănBản[vịTríDữLiệu]&192)==128)vịTríDữLiệu++;}return vịTríDữLiệu;}
static int chạy(int vịTríDữLiệu){while(vịTríDữLiệu>0&&vănBản[vịTríDữLiệu-1]!='\n')vịTríDữLiệu--;return vịTríDữLiệu;}
static int độLệchKếtThúc(int vịTríDữLiệu){while(vịTríDữLiệu<độDài&&vănBản[vịTríDữLiệu]!='\n')vịTríDữLiệu++;return vịTríDữLiệu;}
static int giáTrịRộng(unsigned mãKýTự){return mãKýTự>=196?2:1;}
static int cột(int vịTríDữLiệu){int mãKýTự=0;for(int chỉSốThứBậc=chạy(vịTríDữLiệu);chỉSốThứBậc<vịTríDữLiệu;chỉSốThứBậc=phầnMụcKếTiếp(chỉSốThứBậc))mãKýTự+=vănBản[chỉSốThứBậc]=='\t'?4-mãKýTự%4:giáTrịRộng(vănBản[chỉSốThứBậc]);return mãKýTự;}
static void điểmKiểmTra(void){for(int chỉSốThứBậc=0;chỉSốThứBậc<độDài;chỉSốThứBậc++)dữLiệuHoànTác[chỉSốThứBậc]=vănBản[chỉSốThứBậc];độDàiHoànTác=độDài;bênThượng=giáTrịChỉSố;cácThayĐổiHoànTác=đãĐổiĐãLà;hoànTácSởHữu=1;}
static void xóaSạchCácByte(int vịTríRờiĐi,int vịTríĐến){điểmKiểmTra();for(int chỉSốThứBậc=vịTríĐến;chỉSốThứBậc<độDài;chỉSốThứBậc++)vănBản[vịTríRờiĐi+chỉSốThứBậc-vịTríĐến]=vănBản[chỉSốThứBậc];độDài-=vịTríĐến-vịTríRờiĐi;giáTrịChỉSố=vịTríRờiĐi;đãĐổiĐãLà=1;}
static int thêmCuốiGiáTrị(const unsigned char *dữLiệuChuỗi,int sốLượngPhầnMục){if(sốLượngPhầnMục>sứcChứaTrìnhSoạnThảo-độDài){vănBảnThôngBáo="File full (16384 bytes)";return 0;}điểmKiểmTra();for(int chỉSốThứBậc=độDài-1;chỉSốThứBậc>=giáTrịChỉSố;chỉSốThứBậc--)vănBản[chỉSốThứBậc+sốLượngPhầnMục]=vănBản[chỉSốThứBậc];for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)vănBản[giáTrịChỉSố+chỉSốThứBậc]=dữLiệuChuỗi[chỉSốThứBậc];độDài+=sốLượngPhầnMục;giáTrịChỉSố+=sốLượngPhầnMục;đãĐổiĐãLà=1;return 1;}
static void dọc(int giáTrịKhácBiệt){int vịTríCột=cột(giáTrịChỉSố),vịTríDữLiệu=chạy(giáTrịChỉSố);if(giáTrịKhácBiệt<0){if(!vịTríDữLiệu)return;vịTríDữLiệu=chạy(vịTríDữLiệu-1);}else{vịTríDữLiệu=độLệchKếtThúc(vịTríDữLiệu);if(vịTríDữLiệu==độDài)return;vịTríDữLiệu++;}int mãKýTự=0;while(vịTríDữLiệu<độDài&&vănBản[vịTríDữLiệu]!='\n'&&mãKýTự<vịTríCột){mãKýTự+=vănBản[vịTríDữLiệu]=='\t'?4-mãKýTự%4:giáTrịRộng(vănBản[vịTríDữLiệu]);vịTríDữLiệu=phầnMụcKếTiếp(vịTríDữLiệu);}giáTrịChỉSố=vịTríDữLiệu;}
static void vẽMànHình(void){
    if(giáTrịChỉSố>độDài)giáTrịChỉSố=độDài;if(mụcĐỉnh>giáTrịChỉSố)mụcĐỉnh=chạy(giáTrịChỉSố);mụcĐỉnh=chạy(mụcĐỉnh);
    int vịTríHàng=0;for(int chỉSốThứBậc=mụcĐỉnh;chỉSốThứBậc<giáTrịChỉSố;chỉSốThứBậc++)if(vănBản[chỉSốThứBậc]=='\n')vịTríHàng++;
    while(vịTríHàng>=sốLượngHàng-1){mụcĐỉnh=độLệchKếtThúc(mụcĐỉnh);if(mụcĐỉnh<độDài)mụcĐỉnh++;vịTríHàng--;}
    int vịTríCột=cột(giáTrịChỉSố);if(vịTríCột<bênTrái)bênTrái=vịTríCột;if(vịTríCột-bênTrái>=cácCột-1)bênTrái=vịTríCột-cácCột+2;
    phátVănBản("\033[?25l");int vịTríDữLiệu=mụcĐỉnh;
    for(int giáTrịĐãTrảVề=0;giáTrịĐãTrảVề<sốLượngHàng-1;giáTrịĐãTrảVề++){
        giáTrịDiChuyển(giáTrịĐãTrảVề+1,1);phátVănBản("\033[0m\033[2K");int mãKýTự=0,làĐãTô=0;
        if(vịTríDữLiệu>=độDài&&giáTrịĐãTrảVề>vịTríHàng){phátVănBản("\033[90m~\033[0m");continue;}
        while(vịTríDữLiệu<độDài&&vănBản[vịTríDữLiệu]!='\n'){
            int độLệchKếTiếp=phầnMụcKếTiếp(vịTríDữLiệu),giáTrịRộngĐãYêuCầu=vănBản[vịTríDữLiệu]=='\t'?4-mãKýTự%4:giáTrịRộng(vănBản[vịTríDữLiệu]);
            if(mãKýTự>=bênTrái&&mãKýTự-bênTrái+giáTrịRộngĐãYêuCầu<cácCột){
                if(vănBản[vịTríDữLiệu]=='\t'){for(int thứBậcPhíaTrong=0;thứBậcPhíaTrong<giáTrịRộngĐãYêuCầu;thứBậcPhíaTrong++)dữLiệuByte(' ');}else if(vănBản[vịTríDữLiệu]<32||vănBản[vịTríDữLiệu]==127){dữLiệuByte('?');}else for(int thứBậcPhíaTrong=vịTríDữLiệu;thứBậcPhíaTrong<độLệchKếTiếp;thứBậcPhíaTrong++)dữLiệuByte(vănBản[thứBậcPhíaTrong]);làĐãTô+=giáTrịRộngĐãYêuCầu;
            }mãKýTự+=giáTrịRộngĐãYêuCầu;vịTríDữLiệu=độLệchKếTiếp;
        }
        (void)làĐãTô;if(vịTríDữLiệu<độDài)vịTríDữLiệu++;
    }
    giáTrịDiChuyển(sốLượngHàng,1);phátVănBản("\033[7m\033[2K");ảnhTrạngThái=1;hàngĐợiTrạngThái=0;phátVănBản(chèn?"INSERT ":"NORMAL ");
    int sốByteTên=0;while(tênMụcTệp[sốByteTên]&&sốByteTên<30)dữLiệuByte(tênMụcTệp[sốByteTên++]);phátVănBản(đãĐổiĐãLà?" [+] ":" ");
    phátVănBản("L");int dòng=1;for(int chỉSốThứBậc=0;chỉSốThứBậc<giáTrịChỉSố;chỉSốThứBậc++)if(vănBản[chỉSốThứBậc]=='\n')dòng++;giáTrịThuộcSố(dòng);phátVănBản(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(vănBảnThôngBáo){int sốLượngPhầnMục=0;phátVănBản(" | ");while(vănBảnThôngBáo[sốLượngPhầnMục]&&sốLượngPhầnMục<20)dữLiệuByte(vănBảnThôngBáo[sốLượngPhầnMục++]);}
    ảnhTrạngThái=0;phátVănBản("\033[0m");giáTrịDiChuyển(vịTríHàng+1,vịTríCột-bênTrái+1);phátVănBản("\033[?25h");đẩyĐệm();
}
static int giáTrịĐãNhấn(void){
    if(phímĐangChờ){int chỉSốThứBa=phímĐangChờ;phímĐangChờ=0;return chỉSốThứBa;}
    for(;;){
        int chỉSốThứBa=gọiThựcHiệnNgườiDùng(16,1,0,0,0,0,0);
        unsigned cỡ=gọiThựcHiệnNgườiDùng(16,3,0,0,0,0,0);
        if(cácCột!=(int)(cỡ&65535)||sốLượngHàng!=(int)(cỡ>>16)){
            cácCột=cỡ&65535;sốLượngHàng=cỡ>>16;vẽMànHình();
            if(loạiMụcTrợGiúp){giáTrịDiChuyển(sốLượngHàng,1);phátVănBản("\033[0m\033[2K");dữLiệuByte(loạiMụcTrợGiúp);phátVănBản(lệnh);đẩyĐệm();}
        }
        if(chỉSốThứBa>=0)return chỉSốThứBa;
    }
}
static int đãThoát(void){
    unsigned vịTríHiệnTại=gọiThựcHiệnNgườiDùng(7,0,0,0,0,0,0);int chỉSốThứBa=-1;
    while((unsigned)gọiThựcHiệnNgườiDùng(7,0,0,0,0,0,0)-vịTríHiệnTại<100){chỉSốThứBa=gọiThựcHiệnNgườiDùng(16,1,0,0,0,0,0);if(chỉSốThứBa>=0)break;}
    if(chỉSốThứBa<0)return 27;if(chỉSốThứBa!='['&&chỉSốThứBa!='O'){phímĐangChờ=chỉSốThứBa;return 27;}
    int sốLượngPhầnMục=0;for(int chỉSốThứBậc=0;chỉSốThứBậc<12;chỉSốThứBậc++){chỉSốThứBa=giáTrịĐãNhấn();if(chỉSốThứBa>='0'&&chỉSốThứBa<='9'){sốLượngPhầnMục=sốLượngPhầnMục*10+chỉSốThứBa-'0';continue;}if(chỉSốThứBa=='A')return 1001;if(chỉSốThứBa=='B')return 1002;if(chỉSốThứBa=='C')return 1003;if(chỉSốThứBa=='D')return 1004;if(chỉSốThứBa=='H')return 1005;if(chỉSốThứBa=='F')return 1006;if(chỉSốThứBa=='~')return sốLượngPhầnMục==3?1007:sốLượngPhầnMục==5?1008:sốLượngPhầnMục==6?1009:sốLượngPhầnMục==1?1005:sốLượngPhầnMục==4?1006:27;return 27;}return 27;
}
static int giáTrịCất(void){
    int thẻXửLýTệp=mởTệp(tênMụcTệp,GhiĐọc|ThiếuNếuTạo|CácNộiDungCắtNgắn,0600);if(thẻXửLýTệp<0){vănBảnThôngBáo="Cannot open for save";return 0;}
    intptr_t sốLượngPhầnMục=ghiDữLiệuTệp(thẻXửLýTệp,vănBản,độDài);đóngTệp(thẻXửLýTệp);if(sốLượngPhầnMục!=độDài){vănBảnThôngBáo="Write failed";return 0;}đãĐổiĐãLà=0;vănBảnThôngBáo="Saved (RAM)";return 1;
}
static int bằng(const char *giáTrịĐầuTiên,const char *giáTrịThứHai){while(*giáTrịĐầuTiên&&*giáTrịĐầuTiên==*giáTrịThứHai){giáTrịĐầuTiên++;giáTrịThứHai++;}return *giáTrịĐầuTiên==*giáTrịThứHai;}
static void tìmKếTiếp(void){int sốLượngPhầnMục=0;while(tìmMục[sốLượngPhầnMục])sốLượngPhầnMục++;if(!sốLượngPhầnMục){vănBảnThôngBáo="No search pattern";return;}for(int chỉSốThứBậc=1;chỉSốThứBậc<=độDài;chỉSốThứBậc++){int vịTríDữLiệu=(giáTrịChỉSố+chỉSốThứBậc)%(độDài?độDài:1),thứBậcPhíaTrong=0;while(thứBậcPhíaTrong<sốLượngPhầnMục&&vịTríDữLiệu+thứBậcPhíaTrong<độDài&&vănBản[vịTríDữLiệu+thứBậcPhíaTrong]==(unsigned char)tìmMục[thứBậcPhíaTrong])thứBậcPhíaTrong++;if(thứBậcPhíaTrong==sốLượngPhầnMục){giáTrịChỉSố=vịTríDữLiệu;vănBảnThôngBáo="Match";return;}}vănBảnThôngBáo="Pattern not found";}
static int dấuNhắc(int giáTrịLoạiMục){
    int sốLượngPhầnMục=0;lệnh[0]=0;
    for(;;){giáTrịDiChuyển(sốLượngHàng,1);phátVănBản("\033[0m\033[2K");dữLiệuByte(giáTrịLoạiMục);phátVănBản(lệnh);đẩyĐệm();loạiMụcTrợGiúp=giáTrịLoạiMục;int chỉSốThứBa=giáTrịĐãNhấn();loạiMụcTrợGiúp=0;
        if(chỉSốThứBa==27||chỉSốThứBa==3)return 0;if(chỉSốThứBa==13||chỉSốThứBa==10)break;
        if(chỉSốThứBa==127||chỉSốThứBa==8){if(sốLượngPhầnMục){sốLượngPhầnMục--;while(sốLượngPhầnMục>0&&((unsigned char)lệnh[sốLượngPhầnMục]&192)==128)sốLượngPhầnMục--;lệnh[sốLượngPhầnMục]=0;}continue;}
        if(chỉSốThứBa>=32&&chỉSốThứBa<256&&sốLượngPhầnMục<120){lệnh[sốLượngPhầnMục++]=chỉSốThứBa;lệnh[sốLượngPhầnMục]=0;}
    }
    if(giáTrịLoạiMục=='/'){for(int chỉSốThứBậc=0;chỉSốThứBậc<=sốLượngPhầnMục;chỉSốThứBậc++)tìmMục[chỉSốThứBậc]=lệnh[chỉSốThứBậc];tìmKếTiếp();return 0;}
    if(bằng(lệnh,"q!"))return 1;
    if(bằng(lệnh,"q")){if(!đãĐổiĐãLà)return 1;vănBảnThôngBáo="Unsaved: :w or :q!";return 0;}
    if(bằng(lệnh,"wq")||bằng(lệnh,"x"))return giáTrịCất();
    if(bằng(lệnh,"w")){giáTrịCất();return 0;}
    if(lệnh[0]=='w'&&lệnh[1]==' '){int chỉSốThứBậc=2;while(lệnh[chỉSốThứBậc]==' ')chỉSốThứBậc++;int cỡ=sốLượngPhầnMục-chỉSốThứBậc;if(cỡ<1||cỡ>63){vănBảnThôngBáo="Invalid file name";return 0;}for(int thứBậcPhíaTrong=0;thứBậcPhíaTrong<cỡ;thứBậcPhíaTrong++)tênMụcTệp[thứBậcPhíaTrong]=lệnh[chỉSốThứBậc+thứBậcPhíaTrong];tênMụcTệp[cỡ]=0;giáTrịCất();return 0;}
    int dòng=0;for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++){if(lệnh[chỉSốThứBậc]<'0'||lệnh[chỉSốThứBậc]>'9'){dòng=0;break;}dòng=dòng*10+lệnh[chỉSốThứBậc]-'0';if(dòng>16384){dòng=0;break;}}
    if(dòng){giáTrịChỉSố=0;while(--dòng&&giáTrịChỉSố<độDài){giáTrịChỉSố=độLệchKếtThúc(giáTrịChỉSố);if(giáTrịChỉSố<độDài)giáTrịChỉSố++;}return 0;}
    vănBảnThôngBáo="Unknown vi command";return 0;
}
int bắtChạyChươngTrìnhNgườiDùng(int giáTrịĐãBỏQua){
    (void)giáTrịĐãBỏQua;if(sốLượngĐốiSốNgườiDùng()!=1||đốiSốNgườiDùng(0,tênMụcTệp,sizeof(tênMụcTệp))<0){phátVănBản("Usage: vi FILE\n");đẩyĐệm();return 2;}
    int thẻXửLýTệp=mởTệp(tênMụcTệp,đọcGiáTrịChỉ,0);
    if(thẻXửLýTệp>=0){int sốLượngPhầnMục=cỡTệp(thẻXửLýTệp);if(sốLượngPhầnMục<0||sốLượngPhầnMục>sứcChứaTrìnhSoạnThảo){đóngTệp(thẻXửLýTệp);return 1;}độDài=đọcDữLiệuTệp(thẻXửLýTệp,vănBản,sốLượngPhầnMục);đóngTệp(thẻXửLýTệp);if(độDài!=sốLượngPhầnMục)return 1;for(int chỉSốThứBậc=0;chỉSốThứBậc<độDài;chỉSốThứBậc++)if(!vănBản[chỉSốThứBậc]){phátVănBản("vi: NUL byte in text file\n");đẩyĐệm();return 1;}}
    else if(sốLỗi!=2){phátVănBản("vi: cannot read file\n");đẩyĐệm();return 1;}
    int màuMờ=gọiThựcHiệnNgườiDùng(16,0,0,0,0,0,0);if(màuMờ<0){phátVănBản("vi: use a standalone interactive command\n");đẩyĐệm();return 1;}cácCột=màuMờ&65535;sốLượngHàng=(unsigned)màuMờ>>16;
    phátVănBản("\033[2J\033[H");đẩyĐệm();
    int phầnDẫnĐầu=0,chươngTrìnhThoátHẳn=0;
    while(!chươngTrìnhThoátHẳn){vẽMànHình();int chỉSốThứBa=giáTrịĐãNhấn();if(chỉSốThứBa==27)chỉSốThứBa=đãThoát();vănBảnThôngBáo=0;
        if(chỉSốThứBa==1001){dọc(-1);continue;}if(chỉSốThứBa==1002){dọc(1);continue;}if(chỉSốThứBa==1003){giáTrịChỉSố=phầnMụcKếTiếp(giáTrịChỉSố);continue;}if(chỉSốThứBa==1004){giáTrịChỉSố=trướcĐó(giáTrịChỉSố);continue;}
        if(chỉSốThứBa==1005){giáTrịChỉSố=chạy(giáTrịChỉSố);continue;}if(chỉSốThứBa==1006){giáTrịChỉSố=độLệchKếtThúc(giáTrịChỉSố);continue;}
        if(chỉSốThứBa==1008||chỉSốThứBa==1009){for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngHàng-2;chỉSốThứBậc++)dọc(chỉSốThứBa==1008?-1:1);continue;}
        if(chèn){
            if(chỉSốThứBa==27||chỉSốThứBa==3){chèn=0;continue;}
            if(chỉSốThứBa==127||chỉSốThứBa==8){if(giáTrịChỉSố)xóaSạchCácByte(trướcĐó(giáTrịChỉSố),giáTrịChỉSố);continue;}
            if(chỉSốThứBa==1007){if(giáTrịChỉSố<độDài)xóaSạchCácByte(giáTrịChỉSố,phầnMụcKếTiếp(giáTrịChỉSố));continue;}
            if(chỉSốThứBa==13)chỉSốThứBa=10;if(chỉSốThứBa==10||chỉSốThứBa==9||(chỉSốThứBa>=32&&chỉSốThứBa<256)){
                unsigned char giáTrịThứHai[4];giáTrịThứHai[0]=chỉSốThứBa;int sốLượngPhầnMục=chỉSốThứBa<128?1:chỉSốThứBa>=0xc2&&chỉSốThứBa<0xe0?2:chỉSốThứBa<0xf0?3:chỉSốThứBa<=0xf4?4:0;
                if(!sốLượngPhầnMục){vănBảnThôngBáo="Invalid UTF-8";continue;}int hợpLệ=1;for(int chỉSốThứBậc=1;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++){int mãKýTự=giáTrịĐãNhấn();if(mãKýTự<128||mãKýTự>191){phímĐangChờ=mãKýTự;hợpLệ=0;break;}giáTrịThứHai[chỉSốThứBậc]=mãKýTự;}
                if(hợpLệ)thêmCuốiGiáTrị(giáTrịThứHai,sốLượngPhầnMục);
            }continue;
        }
        if(phầnDẫnĐầu){int vịTríDữLiệu=phầnDẫnĐầu;phầnDẫnĐầu=0;if(vịTríDữLiệu=='g'&&chỉSốThứBa=='g'){giáTrịChỉSố=0;continue;}if(vịTríDữLiệu=='Z'&&chỉSốThứBa=='Z'){chươngTrìnhThoátHẳn=giáTrịCất();continue;}if((vịTríDữLiệu=='d'&&chỉSốThứBa=='d')||(vịTríDữLiệu=='y'&&chỉSốThứBa=='y')){int giáTrịĐầuTiên=chạy(giáTrịChỉSố),giáTrịThứHai=độLệchKếtThúc(giáTrịChỉSố);if(giáTrịThứHai<độDài)giáTrịThứHai++;saoChépĐộDài=giáTrịThứHai-giáTrịĐầuTiên;for(int chỉSốThứBậc=0;chỉSốThứBậc<saoChépĐộDài;chỉSốThứBậc++)dữLiệuĐãSaoChép[chỉSốThứBậc]=vănBản[giáTrịĐầuTiên+chỉSốThứBậc];if(vịTríDữLiệu=='d')xóaSạchCácByte(giáTrịĐầuTiên,giáTrịThứHai);continue;}}
        if(chỉSốThứBa=='i'){chèn=1;continue;}if(chỉSốThứBa=='a'){if(giáTrịChỉSố<độLệchKếtThúc(giáTrịChỉSố))giáTrịChỉSố=phầnMụcKếTiếp(giáTrịChỉSố);chèn=1;continue;}
        if(chỉSốThứBa=='I'){giáTrịChỉSố=chạy(giáTrịChỉSố);chèn=1;continue;}if(chỉSốThứBa=='A'){giáTrịChỉSố=độLệchKếtThúc(giáTrịChỉSố);chèn=1;continue;}
        if(chỉSốThứBa=='o'||chỉSốThứBa=='O'){unsigned char kếtThúcDòng='\n';giáTrịChỉSố=chỉSốThứBa=='o'?độLệchKếtThúc(giáTrịChỉSố):chạy(giáTrịChỉSố);if(thêmCuốiGiáTrị(&kếtThúcDòng,1)){if(chỉSốThứBa=='O')giáTrịChỉSố--;chèn=1;}continue;}
        if(chỉSốThứBa=='h'){giáTrịChỉSố=trướcĐó(giáTrịChỉSố);continue;}if(chỉSốThứBa=='l'){giáTrịChỉSố=phầnMụcKếTiếp(giáTrịChỉSố);continue;}if(chỉSốThứBa=='j'){dọc(1);continue;}if(chỉSốThứBa=='k'){dọc(-1);continue;}
        if(chỉSốThứBa=='0'){giáTrịChỉSố=chạy(giáTrịChỉSố);continue;}if(chỉSốThứBa=='$'){giáTrịChỉSố=độLệchKếtThúc(giáTrịChỉSố);continue;}if(chỉSốThứBa=='G'){giáTrịChỉSố=chạy(độDài);continue;}
        if(chỉSốThứBa=='g'||chỉSốThứBa=='d'||chỉSốThứBa=='y'||chỉSốThứBa=='Z'){phầnDẫnĐầu=chỉSốThứBa;continue;}
        if(chỉSốThứBa=='x'||chỉSốThứBa==1007){if(giáTrịChỉSố<độDài)xóaSạchCácByte(giáTrịChỉSố,phầnMụcKếTiếp(giáTrịChỉSố));continue;}
        if(chỉSốThứBa=='p'&&saoChépĐộDài){giáTrịChỉSố=độLệchKếtThúc(giáTrịChỉSố);if(giáTrịChỉSố<độDài)giáTrịChỉSố++;thêmCuốiGiáTrị(dữLiệuĐãSaoChép,saoChépĐộDài);continue;}
        if(chỉSốThứBa=='u'&&hoànTácSởHữu){for(int chỉSốThứBậc=0;chỉSốThứBậc<sứcChứaTrìnhSoạnThảo;chỉSốThứBậc++){unsigned char giáTrịThứHai=vănBản[chỉSốThứBậc];vănBản[chỉSốThứBậc]=dữLiệuHoànTác[chỉSốThứBậc];dữLiệuHoànTác[chỉSốThứBậc]=giáTrịThứHai;}int sốLượngPhầnMục=độDài;độDài=độDàiHoànTác;độDàiHoànTác=sốLượngPhầnMục;sốLượngPhầnMục=giáTrịChỉSố;giáTrịChỉSố=bênThượng;bênThượng=sốLượngPhầnMục;sốLượngPhầnMục=đãĐổiĐãLà;đãĐổiĐãLà=cácThayĐổiHoànTác;cácThayĐổiHoànTác=sốLượngPhầnMục;continue;}
        if(chỉSốThứBa==':'||chỉSốThứBa=='/'){chươngTrìnhThoátHẳn=dấuNhắc(chỉSốThứBa);continue;}if(chỉSốThứBa=='n'){tìmKếTiếp();continue;}
    }
    phátVănBản("\033[0m\033[?25h\033[2J\033[H");đẩyĐệm();gọiThựcHiệnNgườiDùng(16,2,0,0,0,0,0);return 0;
}
