#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "gọiThựcHiện.h"
#include "GóiGộp.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char DữLiệu[16384];static unsigned độDài,vịTríHiệnTại;static int làKhôngHợpLệ;
static unsigned danhSáchCácThẻ[512],giáTrịĐầuTiên[512],giáTrịThứHai[512],vùngDùngChungHằng,lớpHiệnTại;
static char vănBản[65536];static unsigned cỡVănBản;
typedef struct {unsigned cácBitCấuHình,tên,dữLiệuBộMôTả,dãyChỉLệnh,cỡ,cácBiếnCụcBộ,lưuTrữNgănXếp;} mụcPhươngThức;
static mụcPhươngThức cácPhươngThứcĐãKhaiBáo[64];static unsigned sốLượngPhươngThứcĐãKhaiBáo;
static unsigned tênTrường[64],bộMôTảTrường[64],hằngTrường[64],sốLượngTrườngĐãKhaiBáo;
static unsigned giáTrịThu(unsigned sốLượngPhầnMục){if(vịTríHiệnTại>độDài||sốLượngPhầnMục>độDài-vịTríHiệnTại){làKhôngHợpLệ=1;return 0;}unsigned vịTríDữLiệu=vịTríHiệnTại;vịTríHiệnTại+=sốLượngPhầnMục;return vịTríDữLiệu;}
static unsigned dữLiệuByte(void){unsigned vịTríDữLiệu=giáTrịThu(1);return làKhôngHợpLệ?0:DữLiệu[vịTríDữLiệu];}
static unsigned giáTrịNửa(void){unsigned tọaĐộX=dữLiệuByte();return tọaĐộX<<8|dữLiệuByte();}
static uint32_t làĐầy(void){uint32_t tọaĐộX=giáTrịNửa();return tọaĐộX<<16|giáTrịNửa();}
static int giáTrịUnicode(unsigned chỉSốThứBậc,const char*dữLiệuChuỗi){return chỉSốThứBậc>0&&chỉSốThứBậc<vùngDùngChungHằng&&danhSáchCácThẻ[chỉSốThứBậc]==1&&strlen(dữLiệuChuỗi)==giáTrịThứHai[chỉSốThứBậc]&&!memcmp(DữLiệu+giáTrịĐầuTiên[chỉSốThứBậc],dữLiệuChuỗi,giáTrịThứHai[chỉSốThứBậc]);}
static int vănBảnBằng(unsigned tọaĐộX,unsigned tọaĐộY){return tọaĐộX>0&&tọaĐộX<vùngDùngChungHằng&&tọaĐộY>0&&tọaĐộY<vùngDùngChungHằng&&danhSáchCácThẻ[tọaĐộX]==1&&danhSáchCácThẻ[tọaĐộY]==1&&giáTrịThứHai[tọaĐộX]==giáTrịThứHai[tọaĐộY]&&!memcmp(DữLiệu+giáTrịĐầuTiên[tọaĐộX],DữLiệu+giáTrịĐầuTiên[tọaĐộY],giáTrịThứHai[tọaĐộX]);}
static void phátGiáTrị(const char*mụcTệp,...){if(làKhôngHợpLệ)return;va_list mảngĐốiSố;va_start(mảngĐốiSố,mụcTệp);int sốLượngPhầnMục=vsnprintf(vănBản+cỡVănBản,sizeof(vănBản)-cỡVănBản,mụcTệp,mảngĐốiSố);va_end(mảngĐốiSố);if(sốLượngPhầnMục<0||(unsigned)sốLượngPhầnMục>=sizeof(vănBản)-cỡVănBản){làKhôngHợpLệ=1;return;}cỡVănBản+=sốLượngPhầnMục;}
static int mụcBộMôTả(unsigned giáTrịĐịnhDanh,int*kếtQuả){
    if(giáTrịĐịnhDanh<1||giáTrịĐịnhDanh>=vùngDùngChungHằng||danhSáchCácThẻ[giáTrịĐịnhDanh]!=1)return -1;unsigned vịTríDữLiệu=giáTrịĐầuTiên[giáTrịĐịnhDanh],độLệchKếtThúc=vịTríDữLiệu+giáTrịThứHai[giáTrịĐịnhDanh];if(vịTríDữLiệu>=độLệchKếtThúc||DữLiệu[vịTríDữLiệu++]!='(')return -1;int sốLượngMục=0;
    while(vịTríDữLiệu<độLệchKếtThúc&&DữLiệu[vịTríDữLiệu]!=')'){
        unsigned mãKýTự=DữLiệu[vịTríDữLiệu++];while(mãKýTự=='['&&vịTríDữLiệu<độLệchKếtThúc)mãKýTự=DữLiệu[vịTríDữLiệu++];
        if(mãKýTự=='L'){while(vịTríDữLiệu<độLệchKếtThúc&&DữLiệu[vịTríDữLiệu]!=';')vịTríDữLiệu++;if(vịTríDữLiệu==độLệchKếtThúc)return -1;vịTríDữLiệu++;}
        else if(mãKýTự!='I'&&mãKýTự!='Z'&&mãKýTự!='B'&&mãKýTự!='C'&&mãKýTự!='S')return -1;
        if(++sốLượngMục>16)return -1;
    }
    if(vịTríDữLiệu+1>=độLệchKếtThúc||DữLiệu[vịTríDữLiệu++]!=')')return -1;*kếtQuả=DữLiệu[vịTríDữLiệu]=='V'?0:1;
    if(DữLiệu[vịTríDữLiệu]=='J'||DữLiệu[vịTríDữLiệu]=='D'||DữLiệu[vịTríDữLiệu]=='F')return -1;return sốLượngMục;
}
static void cácThuộcTính(void){unsigned sốLượngPhầnMục=giáTrịNửa();for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục&&!làKhôngHợpLệ;chỉSốThứBậc++){giáTrịNửa();unsigned cỡ=làĐầy();giáTrịThu(cỡ);}}
static int phânTíchCúPhápĐầuVào(void){
    if(làĐầy()!=0xcafebabe)return -1;unsigned phiênBảnThứYếu=giáTrịNửa(),sốPhiênBản=giáTrịNửa();if(phiênBảnThứYếu||sốPhiênBản<45||sốPhiênBản>52)return -1;
    vùngDùngChungHằng=giáTrịNửa();if(vùngDùngChungHằng<1||vùngDùngChungHằng>512)return -1;
    for(unsigned chỉSốThứBậc=1;chỉSốThứBậc<vùngDùngChungHằng&&!làKhôngHợpLệ;chỉSốThứBậc++){
        danhSáchCácThẻ[chỉSốThứBậc]=dữLiệuByte();switch(danhSáchCácThẻ[chỉSốThứBậc]){
        case 1:giáTrịThứHai[chỉSốThứBậc]=giáTrịNửa();giáTrịĐầuTiên[chỉSốThứBậc]=giáTrịThu(giáTrịThứHai[chỉSốThứBậc]);break;case 3:case 4:giáTrịĐầuTiên[chỉSốThứBậc]=làĐầy();break;
        case 5:case 6:giáTrịThu(8);if(++chỉSốThứBậc>=vùngDùngChungHằng)return -1;break;
        case 7:case 8:case 16:giáTrịĐầuTiên[chỉSốThứBậc]=giáTrịNửa();break;
        case 9:case 10:case 11:case 12:case 18:giáTrịĐầuTiên[chỉSốThứBậc]=giáTrịNửa();giáTrịThứHai[chỉSốThứBậc]=giáTrịNửa();break;
        case 15:giáTrịĐầuTiên[chỉSốThứBậc]=dữLiệuByte();giáTrịThứHai[chỉSốThứBậc]=giáTrịNửa();break;default:return -1;
        }
    }
    giáTrịNửa();lớpHiệnTại=giáTrịNửa();giáTrịNửa();if(lớpHiệnTại<1||lớpHiệnTại>=vùngDùngChungHằng||danhSáchCácThẻ[lớpHiệnTại]!=7||giáTrịĐầuTiên[lớpHiệnTại]<1||giáTrịĐầuTiên[lớpHiệnTại]>=vùngDùngChungHằng||danhSáchCácThẻ[giáTrịĐầuTiên[lớpHiệnTại]]!=1)return -1;unsigned cácGiaoDiện=giáTrịNửa();giáTrịThu(cácGiaoDiện*2);
    sốLượngTrườngĐãKhaiBáo=giáTrịNửa();if(sốLượngTrườngĐãKhaiBáo>64)return -1;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngTrườngĐãKhaiBáo&&!làKhôngHợpLệ;chỉSốThứBậc++){
        unsigned cácBitCấuHình=giáTrịNửa();tênTrường[chỉSốThứBậc]=giáTrịNửa();bộMôTảTrường[chỉSốThứBậc]=giáTrịNửa();
        if(!(cácBitCấuHình&8))return -1;
        unsigned sốLượngMục=giáTrịNửa();for(unsigned thứBậcPhíaTrong=0;thứBậcPhíaTrong<sốLượngMục&&!làKhôngHợpLệ;thứBậcPhíaTrong++){
            unsigned tên=giáTrịNửa(),cỡ=làĐầy();
            if(giáTrịUnicode(tên,"ConstantValue")){if(cỡ!=2)return -1;hằngTrường[chỉSốThứBậc]=giáTrịNửa();}
            else giáTrịThu(cỡ);
        }
    }
    sốLượngPhươngThứcĐãKhaiBáo=giáTrịNửa();if(sốLượngPhươngThứcĐãKhaiBáo>64)return -1;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhươngThứcĐãKhaiBáo&&!làKhôngHợpLệ;chỉSốThứBậc++){
        mụcPhươngThức*cỡNhóm=cácPhươngThứcĐãKhaiBáo+chỉSốThứBậc;cỡNhóm->cácBitCấuHình=giáTrịNửa();cỡNhóm->tên=giáTrịNửa();cỡNhóm->dữLiệuBộMôTả=giáTrịNửa();unsigned sốLượngMục=giáTrịNửa();
        for(unsigned thứBậcPhíaTrong=0;thứBậcPhíaTrong<sốLượngMục&&!làKhôngHợpLệ;thứBậcPhíaTrong++){
            unsigned tên=giáTrịNửa(),cỡ=làĐầy(),chạy=vịTríHiệnTại;
            if(cỡ>độDài-vịTríHiệnTại)return -1;
            if(giáTrịUnicode(tên,"Code")){
                cỡNhóm->lưuTrữNgănXếp=giáTrịNửa();cỡNhóm->cácBiếnCụcBộ=giáTrịNửa();cỡNhóm->cỡ=làĐầy();cỡNhóm->dãyChỉLệnh=giáTrịThu(cỡNhóm->cỡ);
                if(cỡNhóm->lưuTrữNgănXếp>128||cỡNhóm->cácBiếnCụcBộ>128||cỡNhóm->cỡ>8192||giáTrịNửa())return -1;cácThuộcTính();
            }else giáTrịThu(cỡ);
            if(vịTríHiệnTại!=chạy+cỡ)return -1;
        }
        if(!giáTrịUnicode(cỡNhóm->tên,"<init>")&&(!(cỡNhóm->cácBitCấuHình&8)||(cỡNhóm->cácBitCấuHình&(0x100|0x20))||!cỡNhóm->cỡ))return -1;
    }
    cácThuộcTính();return làKhôngHợpLệ||vịTríHiệnTại!=độDài?-1:0;
}
static void giáTrịHằng(unsigned giáTrịĐịnhDanh){
    if(!giáTrịĐịnhDanh||giáTrịĐịnhDanh>=vùngDùngChungHằng){làKhôngHợpLệ=1;return;}
    if(danhSáchCácThẻ[giáTrịĐịnhDanh]==3)phátGiáTrị("P(%uU);",giáTrịĐầuTiên[giáTrịĐịnhDanh]);
    else if(danhSáchCácThẻ[giáTrịĐịnhDanh]==8)phátGiáTrị("P((W)k%u);",giáTrịĐịnhDanh);else làKhôngHợpLệ=1;
}
static void gọiThựcHiện(unsigned giáTrịĐịnhDanh,int gọiẢo){
    if(giáTrịĐịnhDanh<1||giáTrịĐịnhDanh>=vùngDùngChungHằng||(danhSáchCácThẻ[giáTrịĐịnhDanh]!=10&&danhSáchCácThẻ[giáTrịĐịnhDanh]!=11)||giáTrịĐầuTiên[giáTrịĐịnhDanh]<1||giáTrịĐầuTiên[giáTrịĐịnhDanh]>=vùngDùngChungHằng||danhSáchCácThẻ[giáTrịĐầuTiên[giáTrịĐịnhDanh]]!=7||giáTrịThứHai[giáTrịĐịnhDanh]<1||giáTrịThứHai[giáTrịĐịnhDanh]>=vùngDùngChungHằng||danhSáchCácThẻ[giáTrịThứHai[giáTrịĐịnhDanh]]!=12){làKhôngHợpLệ=1;return;}
    unsigned đốiTượngChủSởHữu=giáTrịĐầuTiên[giáTrịĐầuTiên[giáTrịĐịnhDanh]],tên=giáTrịĐầuTiên[giáTrịThứHai[giáTrịĐịnhDanh]],dữLiệuBộMôTả=giáTrịThứHai[giáTrịThứHai[giáTrịĐịnhDanh]];int kếtQuả=0,sốLượngPhầnMục=mụcBộMôTả(dữLiệuBộMôTả,&kếtQuả);if(sốLượngPhầnMục<0){làKhôngHợpLệ=1;return;}
    for(int chỉSốThứBậc=sốLượngPhầnMục;chỉSốThứBậc>0;chỉSốThứBậc--)phátGiáTrị("x[%d]=Q();",chỉSốThứBậc-1);if(gọiẢo)phátGiáTrị("Q();");
    if(!gọiẢo&&vănBảnBằng(đốiTượngChủSởHữu,giáTrịĐầuTiên[lớpHiệnTại])){
        unsigned cỡNhóm=0;for(;cỡNhóm<sốLượngPhươngThứcĐãKhaiBáo;cỡNhóm++)if(vănBảnBằng(tên,cácPhươngThứcĐãKhaiBáo[cỡNhóm].tên)&&vănBảnBằng(dữLiệuBộMôTả,cácPhươngThứcĐãKhaiBáo[cỡNhóm].dữLiệuBộMôTả))break;
        if(cỡNhóm==sốLượngPhươngThứcĐãKhaiBáo||!(cácPhươngThứcĐãKhaiBáo[cỡNhóm].cácBitCấuHình&8)){làKhôngHợpLệ=1;return;}
        if(kếtQuả)phátGiáTrị("P(");phátGiáTrị("m%u(",cỡNhóm);for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)phátGiáTrị(chỉSốThứBậc?",x[%d]":"x[%d]",chỉSốThứBậc);phátGiáTrị(kếtQuả?"));":" );");return;
    }
    if((gọiẢo&&giáTrịUnicode(đốiTượngChủSởHữu,"java/io/PrintStream")&& (giáTrịUnicode(tên,"print")||giáTrịUnicode(tên,"println")))||(!gọiẢo&&giáTrịUnicode(đốiTượngChủSởHữu,"tiếngViệt/tựThân/ĐầuRa"))){
        if(giáTrịUnicode(dữLiệuBộMôTả,"(I)V")&&(giáTrịUnicode(tên,"print")||giáTrịUnicode(tên,"println")||giáTrịUnicode(tên,"ghiSố"))){phátGiáTrị("jprint(x[0],1,%d);",giáTrịUnicode(tên,"print")?0:1);return;}
        if(giáTrịUnicode(dữLiệuBộMôTả,"(Ljava/lang/String;)V")&&(giáTrịUnicode(tên,"print")||giáTrịUnicode(tên,"println")||giáTrịUnicode(tên,"ghi")||giáTrịUnicode(tên,"ghiDòng"))){phátGiáTrị("jprint(x[0],0,%d);",giáTrịUnicode(tên,"print")||giáTrịUnicode(tên,"ghi")?0:1);return;}
        if(giáTrịUnicode(dữLiệuBộMôTả,"()V")&&giáTrịUnicode(tên,"println")){phátGiáTrị("jprint((W)\"\",0,1);");return;}
    }
    if(!gọiẢo&&giáTrịUnicode(đốiTượngChủSởHữu,"tiếngViệt/tựThân/Tệp")){
        if(giáTrịUnicode(tên,"ghi")&&giáTrịUnicode(dữLiệuBộMôTả,"(Ljava/lang/String;Ljava/lang/String;)V")){phátGiáTrị("jfwrite(x[0],x[1]);");return;}
        if(giáTrịUnicode(tên,"đọc")&&giáTrịUnicode(dữLiệuBộMôTả,"(Ljava/lang/String;)Ljava/lang/String;")){phátGiáTrị("P(jfread(x[0]));");return;}
    }
    làKhôngHợpLệ=1;
}
static void biênDịchPhươngThức(unsigned chỉSốTraCứu){
    mụcPhươngThức*cỡNhóm=cácPhươngThứcĐãKhaiBáo+chỉSốTraCứu;if(giáTrịUnicode(cỡNhóm->tên,"<init>"))return;int kếtQuả,sốLượngPhầnMục=mụcBộMôTả(cỡNhóm->dữLiệuBộMôTả,&kếtQuả);if(sốLượngPhầnMục<0){làKhôngHợpLệ=1;return;}
    phátGiáTrị("static W m%u(",chỉSốTraCứu);for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)phátGiáTrị(chỉSốThứBậc?",W a%d":"W a%d",chỉSốThứBậc);if(!sốLượngPhầnMục)phátGiáTrị("void");
    if((unsigned)sốLượngPhầnMục>cỡNhóm->cácBiếnCụcBộ){làKhôngHợpLệ=1;return;}
    phátGiáTrị("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",cỡNhóm->cácBiếnCụcBộ?cỡNhóm->cácBiếnCụcBộ:1);for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)phátGiáTrị("v[%d]=a%d;",chỉSốThứBậc,chỉSốThứBậc);
    unsigned đãLưu=độDài;độDài=cỡNhóm->dãyChỉLệnh+cỡNhóm->cỡ;vịTríHiệnTại=cỡNhóm->dãyChỉLệnh;
    while(vịTríHiệnTại<độDài&&!làKhôngHợpLệ){unsigned vịTríLệnh=vịTríHiệnTại-cỡNhóm->dãyChỉLệnh,giáTrịThaoTác=dữLiệuByte();phátGiáTrị("L%u:;",vịTríLệnh);
        if(giáTrịThaoTác==0){}
        else if(giáTrịThaoTác==1)phátGiáTrị("P(0);");
        else if(giáTrịThaoTác>=2&&giáTrịThaoTác<=8)phátGiáTrị("P(%uU);",giáTrịThaoTác-3);
        else if(giáTrịThaoTác==16){int giáTrị=(int8_t)dữLiệuByte();phátGiáTrị("P(%uU);",(unsigned)giáTrị);}
        else if(giáTrịThaoTác==17){int giáTrị=(int16_t)giáTrịNửa();phátGiáTrị("P(%uU);",(unsigned)giáTrị);}
        else if(giáTrịThaoTác==18||giáTrịThaoTác==19)giáTrịHằng(giáTrịThaoTác==18?dữLiệuByte():giáTrịNửa());
        else if(giáTrịThaoTác==21||giáTrịThaoTác==25){unsigned chỉSốThứBậc=dữLiệuByte();if(chỉSốThứBậc>=cỡNhóm->cácBiếnCụcBộ)làKhôngHợpLệ=1;phátGiáTrị("P(v[%u]);",chỉSốThứBậc);}
        else if((giáTrịThaoTác>=26&&giáTrịThaoTác<=29)||(giáTrịThaoTác>=42&&giáTrịThaoTác<=45)){unsigned chỉSốThứBậc=giáTrịThaoTác>=42?giáTrịThaoTác-42:giáTrịThaoTác-26;if(chỉSốThứBậc>=cỡNhóm->cácBiếnCụcBộ)làKhôngHợpLệ=1;phátGiáTrị("P(v[%u]);",chỉSốThứBậc);}
        else if(giáTrịThaoTác==54||giáTrịThaoTác==58){unsigned chỉSốThứBậc=dữLiệuByte();if(chỉSốThứBậc>=cỡNhóm->cácBiếnCụcBộ)làKhôngHợpLệ=1;phátGiáTrị("v[%u]=Q();",chỉSốThứBậc);}
        else if((giáTrịThaoTác>=59&&giáTrịThaoTác<=62)||(giáTrịThaoTác>=75&&giáTrịThaoTác<=78)){unsigned chỉSốThứBậc=giáTrịThaoTác>=75?giáTrịThaoTác-75:giáTrịThaoTác-59;if(chỉSốThứBậc>=cỡNhóm->cácBiếnCụcBộ)làKhôngHợpLệ=1;phátGiáTrị("v[%u]=Q();",chỉSốThứBậc);}
        else if(giáTrịThaoTác==46||giáTrịThaoTác==50||giáTrịThaoTác==51||giáTrịThaoTác==52||giáTrịThaoTác==53)phátGiáTrị("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(giáTrịThaoTác==79||giáTrịThaoTác==83||giáTrịThaoTác==84||giáTrịThaoTác==85||giáTrịThaoTác==86)phátGiáTrị("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",giáTrịThaoTác==84?"(unsigned)(signed char)q":giáTrịThaoTác==85?"(unsigned short)q":giáTrịThaoTác==86?"(unsigned)(short)q":"q");
        else if(giáTrịThaoTác==87)phátGiáTrị("Q();");
        else if(giáTrịThaoTác==89)phátGiáTrị("q=Q();P(q);P(q);");
        else if(giáTrịThaoTác==90)phátGiáTrị("q=Q();r=Q();P(q);P(r);P(q);");
        else if(giáTrịThaoTác==95)phátGiáTrị("q=Q();r=Q();P(q);P(r);");
        else if(giáTrịThaoTác==96||giáTrịThaoTác==100||giáTrịThaoTác==104||giáTrịThaoTác==120||giáTrịThaoTác==124||giáTrịThaoTác==126||giáTrịThaoTác==128||giáTrịThaoTác==130){const char*giáTrịBảngMã=giáTrịThaoTác==96?"+":giáTrịThaoTác==100?"-":giáTrịThaoTác==104?"*":giáTrịThaoTác==120?"<<":giáTrịThaoTác==124?">>":giáTrịThaoTác==126?"&":giáTrịThaoTác==128?"|":"^";phátGiáTrị("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",giáTrịBảngMã,giáTrịThaoTác==120||giáTrịThaoTác==124?"%32":"");}
        else if(giáTrịThaoTác==108||giáTrịThaoTác==112)phátGiáTrị("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",giáTrịThaoTác==112);
        else if(giáTrịThaoTác==116)phátGiáTrị("P(0U-(unsigned)Q());");
        else if(giáTrịThaoTác==122)phátGiáTrị("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(giáTrịThaoTác==132){unsigned chỉSốThứBậc=dữLiệuByte();int giáTrịKhácBiệt=(int8_t)dữLiệuByte();if(chỉSốThứBậc>=cỡNhóm->cácBiếnCụcBộ)làKhôngHợpLệ=1;phátGiáTrị("v[%u]=(unsigned)v[%u]+%uU;",chỉSốThứBậc,chỉSốThứBậc,(unsigned)giáTrịKhácBiệt);}
        else if(giáTrịThaoTác>=145&&giáTrịThaoTác<=147)phátGiáTrị("P((unsigned)(%s)Q());",giáTrịThaoTác==145?"signed char":giáTrịThaoTác==146?"unsigned short":"short");
        else if(giáTrịThaoTác>=153&&giáTrịThaoTác<=166){int giáTrịĐốiĐích=(int)vịTríLệnh+(int16_t)giáTrịNửa();const char*giáTrịPhépSoSánh[]={"==","!=","<",">=",">","<="};if(giáTrịĐốiĐích<0||giáTrịĐốiĐích>=(int)cỡNhóm->cỡ){làKhôngHợpLệ=1;break;}if(giáTrịThaoTác<159)phátGiáTrị("if((int)Q()%s0)goto L%d;",giáTrịPhépSoSánh[giáTrịThaoTác-153],giáTrịĐốiĐích);else if(giáTrịThaoTác<165)phátGiáTrị("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",giáTrịPhépSoSánh[giáTrịThaoTác-159],giáTrịĐốiĐích);else phátGiáTrị("q=Q();r=Q();if(r%sq)goto L%d;",giáTrịThaoTác==165?"==":"!=",giáTrịĐốiĐích);}
        else if(giáTrịThaoTác==167){int giáTrịĐốiĐích=(int)vịTríLệnh+(int16_t)giáTrịNửa();if(giáTrịĐốiĐích<0||giáTrịĐốiĐích>=(int)cỡNhóm->cỡ)làKhôngHợpLệ=1;phátGiáTrị("goto L%d;",giáTrịĐốiĐích);}
        else if(giáTrịThaoTác==172||giáTrịThaoTác==176)phátGiáTrị("return Q();");else if(giáTrịThaoTác==177)phátGiáTrị("return 0;");
        else if(giáTrịThaoTác==178||giáTrịThaoTác==179){unsigned giáTrịĐịnhDanh=giáTrịNửa();if(giáTrịĐịnhDanh<1||giáTrịĐịnhDanh>=vùngDùngChungHằng||danhSáchCácThẻ[giáTrịĐịnhDanh]!=9||giáTrịĐầuTiên[giáTrịĐịnhDanh]>=vùngDùngChungHằng||giáTrịThứHai[giáTrịĐịnhDanh]>=vùngDùngChungHằng||danhSáchCácThẻ[giáTrịĐầuTiên[giáTrịĐịnhDanh]]!=7||danhSáchCácThẻ[giáTrịThứHai[giáTrịĐịnhDanh]]!=12){làKhôngHợpLệ=1;break;}unsigned đốiTượngChủSởHữu=giáTrịĐầuTiên[giáTrịĐầuTiên[giáTrịĐịnhDanh]],tên=giáTrịĐầuTiên[giáTrịThứHai[giáTrịĐịnhDanh]],dữLiệuBộMôTả=giáTrịThứHai[giáTrịThứHai[giáTrịĐịnhDanh]];
            if(giáTrịThaoTác==178&&giáTrịUnicode(đốiTượngChủSởHữu,"java/lang/System")&&giáTrịUnicode(tên,"out")&&giáTrịUnicode(dữLiệuBộMôTả,"Ljava/io/PrintStream;"))phátGiáTrị("P(1);");
            else {unsigned mụcTệp=0;while(mụcTệp<sốLượngTrườngĐãKhaiBáo&&(!vănBảnBằng(tên,tênTrường[mụcTệp])||!vănBảnBằng(dữLiệuBộMôTả,bộMôTảTrường[mụcTệp])))mụcTệp++;if(!vănBảnBằng(đốiTượngChủSởHữu,giáTrịĐầuTiên[lớpHiệnTại])||mụcTệp==sốLượngTrườngĐãKhaiBáo){làKhôngHợpLệ=1;break;}phátGiáTrị(giáTrịThaoTác==178?"P(fields[%u]);":"fields[%u]=Q();",mụcTệp);}}
        else if(giáTrịThaoTác==182||giáTrịThaoTác==184)gọiThựcHiện(giáTrịNửa(),giáTrịThaoTác==182);
        else if(giáTrịThaoTác==188){unsigned loạiMụcKiểu=dữLiệuByte();if(loạiMụcKiểu!=4&&loạiMụcKiểu!=5&&loạiMụcKiểu!=8&&loạiMụcKiểu!=9&&loạiMụcKiểu!=10)làKhôngHợpLệ=1;phátGiáTrị("P(jarray((int)Q()));");}
        else if(giáTrịThaoTác==190)phátGiáTrị("P(jlength(Q()));");
        else if(giáTrịThaoTác==198||giáTrịThaoTác==199){int giáTrịĐốiĐích=(int)vịTríLệnh+(int16_t)giáTrịNửa();if(giáTrịĐốiĐích<0||giáTrịĐốiĐích>=(int)cỡNhóm->cỡ)làKhôngHợpLệ=1;phátGiáTrị("if(Q()%s0)goto L%d;",giáTrịThaoTác==198?"==":"!=",giáTrịĐốiĐích);}
        else làKhôngHợpLệ=1;
        if(làKhôngHợpLệ)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",chỉSốTraCứu,giáTrịThaoTác,vịTríLệnh);
        phátGiáTrị("\n");
    }
    độDài=đãLưu;phátGiáTrị("jfail();return 0;}\n");
}
static unsigned đơnVịChuỗi(unsigned *vịTríDữLiệu,unsigned độLệchKếtThúc){
    if(*vịTríDữLiệu>=độLệchKếtThúc){làKhôngHợpLệ=1;return 0;}unsigned mãKýTự=DữLiệu[(*vịTríDữLiệu)++];
    if(mãKýTự<128)return mãKýTự;
    unsigned sốLượngPhầnMục=mãKýTự>=0xc0&&mãKýTự<=0xdf?1:mãKýTự>=0xe0&&mãKýTự<=0xef?2:3;
    if(sốLượngPhầnMục==3||sốLượngPhầnMục>độLệchKếtThúc-*vịTríDữLiệu){làKhôngHợpLệ=1;return 0;}unsigned giáTrị=mãKýTự&((1u<<(6-sốLượngPhầnMục))-1);
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++){unsigned phầnMụcKếTiếp=DữLiệu[(*vịTríDữLiệu)++];if((phầnMụcKếTiếp&0xc0)!=0x80)làKhôngHợpLệ=1;giáTrị=giáTrị<<6|(phầnMụcKếTiếp&63);}
    if((sốLượngPhầnMục==1&&giáTrị<128&&giáTrị!=0)||(sốLượngPhầnMục==2&&giáTrị<2048))làKhôngHợpLệ=1;return giáTrị;
}
static void hằngChuỗi(unsigned giáTrịĐịnhDanh){
    unsigned giáTrịKhôngDấu=giáTrịĐầuTiên[giáTrịĐịnhDanh];if(giáTrịKhôngDấu<1||giáTrịKhôngDấu>=vùngDùngChungHằng||danhSáchCácThẻ[giáTrịKhôngDấu]!=1){làKhôngHợpLệ=1;return;}phátGiáTrị("static const unsigned char k%u[]={",giáTrịĐịnhDanh);
    unsigned vịTríDữLiệu=giáTrịĐầuTiên[giáTrịKhôngDấu],độLệchKếtThúc=vịTríDữLiệu+giáTrịThứHai[giáTrịKhôngDấu];
    while(vịTríDữLiệu<độLệchKếtThúc&&!làKhôngHợpLệ){unsigned mãKýTự=đơnVịChuỗi(&vịTríDữLiệu,độLệchKếtThúc);
        if(mãKýTự>=0xd800&&mãKýTự<=0xdbff){unsigned phầnThấp=đơnVịChuỗi(&vịTríDữLiệu,độLệchKếtThúc);if(phầnThấp<0xdc00||phầnThấp>0xdfff){làKhôngHợpLệ=1;break;}mãKýTự=0x10000+((mãKýTự-0xd800)<<10)+phầnThấp-0xdc00;}
        else if(mãKýTự>=0xdc00&&mãKýTự<=0xdfff){làKhôngHợpLệ=1;break;}
        if(!mãKýTự){printf("jaot: embedded NUL string needs JVM mode\n");làKhôngHợpLệ=1;break;}
        if(mãKýTự<128)phátGiáTrị("%u,",mãKýTự);
        else{unsigned sốLượngPhầnMục=mãKýTự<2048?2:mãKýTự<65536?3:4;phátGiáTrị("%u,",(sốLượngPhầnMục==2?0xc0:sốLượngPhầnMục==3?0xe0:0xf0)|(mãKýTự>>(6*(sốLượngPhầnMục-1))));for(unsigned chỉSốThứBậc=sốLượngPhầnMục-1;chỉSốThứBậc;chỉSốThứBậc--)phátGiáTrị("%u,",0x80|((mãKýTự>>(6*(chỉSốThứBậc-1)))&63));}
    }phátGiáTrị("0};\n");
}
const char *nguồnBiênDịchTrướcJava(const char*tên){
    size_t sốLượngPhầnMục=strlen(tên);
    if(sốLượngPhầnMục>4&&!strcmp(tên+sốLượngPhầnMục-4,".jar")){
        if(mởJAR(tên)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char đườngDẫn[256];const char*phươngThứcMục=chínhJAR();sốLượngPhầnMục=strlen(phươngThứcMục);if(sốLượngPhầnMục+6>=sizeof(đườngDẫn))return 0;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)đườngDẫn[chỉSốThứBậc]=phươngThứcMục[chỉSốThứBậc]=='.'?'/':phươngThứcMục[chỉSốThứBậc];strcpy(đườngDẫn+sốLượngPhầnMục,".class");int sốLượngMục=đọcJAR(đườngDẫn,DữLiệu,sizeof(DữLiệu));if(sốLượngMục<0)return 0;độDài=sốLượngMục;
    }else{intptr_t thẻXửLýTệp=gọiThựcHiệnNgườiDùng(3,(uintptr_t)tên,0,0,0,0,0);if(thẻXửLýTệp<0)return 0;intptr_t sốLượngMục=gọiThựcHiệnNgườiDùng(9,thẻXửLýTệp,0,0,0,0,0);if(sốLượngMục<0||sốLượngMục>sizeof(DữLiệu)){gọiThựcHiệnNgườiDùng(4,thẻXửLýTệp,0,0,0,0,0);return 0;}intptr_t sốLượngĐãNhận=gọiThựcHiệnNgườiDùng(2,thẻXửLýTệp,(uintptr_t)DữLiệu,sốLượngMục,0,0,0);gọiThựcHiệnNgườiDùng(4,thẻXửLýTệp,0,0,0,0,0);if(sốLượngĐãNhận!=sốLượngMục)return 0;độDài=sốLượngMục;}
    if(phânTíchCúPhápĐầuVào()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    phátGiáTrị("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned chỉSốThứBậc=1;chỉSốThứBậc<vùngDùngChungHằng&&!làKhôngHợpLệ;chỉSốThứBậc++)if(danhSáchCácThẻ[chỉSốThứBậc]==8)hằngChuỗi(chỉSốThứBậc);
    if(làKhôngHợpLệ)return 0;
    int điểmMục=-1,giáTrịBanĐầu=-1;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhươngThứcĐãKhaiBáo;chỉSốThứBậc++)if(!giáTrịUnicode(cácPhươngThứcĐãKhaiBáo[chỉSốThứBậc].tên,"<init>")){
        int kếtQuả,sốLượngMục=mụcBộMôTả(cácPhươngThứcĐãKhaiBáo[chỉSốThứBậc].dữLiệuBộMôTả,&kếtQuả);if(sốLượngMục<0)return 0;phátGiáTrị("static W m%u(",chỉSốThứBậc);for(int thứBậcPhíaTrong=0;thứBậcPhíaTrong<sốLượngMục;thứBậcPhíaTrong++)phátGiáTrị(thứBậcPhíaTrong?",W":"W");if(!sốLượngMục)phátGiáTrị("void");phátGiáTrị(");\n");
        if(giáTrịUnicode(cácPhươngThứcĐãKhaiBáo[chỉSốThứBậc].tên,"main")&&giáTrịUnicode(cácPhươngThứcĐãKhaiBáo[chỉSốThứBậc].dữLiệuBộMôTả,"([Ljava/lang/String;)V")&&(cácPhươngThứcĐãKhaiBáo[chỉSốThứBậc].cácBitCấuHình&9)==9)điểmMục=chỉSốThứBậc;
        if(giáTrịUnicode(cácPhươngThứcĐãKhaiBáo[chỉSốThứBậc].tên,"<clinit>"))giáTrịBanĐầu=chỉSốThứBậc;
    }
    if(điểmMục<0)return 0;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhươngThứcĐãKhaiBáo&&!làKhôngHợpLệ;chỉSốThứBậc++)biênDịchPhươngThức(chỉSốThứBậc);
    phátGiáTrị("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngTrườngĐãKhaiBáo;chỉSốThứBậc++)if(hằngTrường[chỉSốThứBậc]){
        unsigned mãKýTự=hằngTrường[chỉSốThứBậc];if(mãKýTự>=vùngDùngChungHằng)return 0;
        if(danhSáchCácThẻ[mãKýTự]==3)phátGiáTrị("fields[%u]=%uU;",chỉSốThứBậc,giáTrịĐầuTiên[mãKýTự]);else if(danhSáchCácThẻ[mãKýTự]==8)phátGiáTrị("fields[%u]=(W)k%u;",chỉSốThứBậc,mãKýTự);else return 0;
    }
    if(giáTrịBanĐầu>=0)phátGiáTrị("m%d();",giáTrịBanĐầu);phátGiáTrị("m%d((W)a);return 0;}\n",điểmMục);
    return làKhôngHợpLệ?0:vănBản;
}
