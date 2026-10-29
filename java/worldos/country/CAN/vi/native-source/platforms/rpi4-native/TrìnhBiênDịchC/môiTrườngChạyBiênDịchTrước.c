#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "gọiThựcHiện.h"
#include "ABITệp.h"
typedef unsigned long từMáy;
static từMáy lưuTrữVùngNhớĐộng[8192];static unsigned sứcChứaĐãDùng;
void thấtBạiJava(void){const char vănBản[]="AOT runtime error\n";ghiDữLiệuTệp(2,vănBản,sizeof(vănBản)-1);gọiThựcHiệnNgườiDùng(6,1,0,0,0,0,0);for(;;){}}
void đẩyJava(từMáy *lưuTrữNgănXếp,int *giáTrịĐộSâu,từMáy giáTrị){if(*giáTrịĐộSâu<0||*giáTrịĐộSâu>=128)thấtBạiJava();lưuTrữNgănXếp[(*giáTrịĐộSâu)++]=giáTrị;}
từMáy giáTrịLấyĐỉnhJava(từMáy *lưuTrữNgănXếp,int *giáTrịĐộSâu){if(*giáTrịĐộSâu<=0||*giáTrịĐộSâu>128)thấtBạiJava();return lưuTrữNgănXếp[--*giáTrịĐộSâu];}
từMáy mảngJava(int sốLượngPhầnMục){if(sốLượngPhầnMục<0||(unsigned)sốLượngPhầnMục+1>8192-sứcChứaĐãDùng)thấtBạiJava();từMáy*vịTríDữLiệu=lưuTrữVùngNhớĐộng+sứcChứaĐãDùng;sứcChứaĐãDùng+=sốLượngPhầnMục+1;vịTríDữLiệu[0]=sốLượngPhầnMục;return (từMáy)vịTríDữLiệu;}
từMáy *chỉSốJava(từMáy thamChiếuĐốiTượng,int sốLượngPhầnMục){từMáy*vịTríDữLiệu=(từMáy*)thamChiếuĐốiTượng;if(!vịTríDữLiệu||sốLượngPhầnMục<0||(từMáy)sốLượngPhầnMục>=vịTríDữLiệu[0])thấtBạiJava();return vịTríDữLiệu+sốLượngPhầnMục+1;}
int độDàiJava(từMáy thamChiếuĐốiTượng){if(!thamChiếuĐốiTượng)thấtBạiJava();return *(từMáy*)thamChiếuĐốiTượng;}
int chiaJava(int tọaĐộX,int tọaĐộY,int giáTrịSốDư){if(!tọaĐộY)thấtBạiJava();if(tọaĐộX==(-2147483647-1)&&tọaĐộY==-1)return giáTrịSốDư?0:tọaĐộX;return giáTrịSốDư?tọaĐộX%tọaĐộY:tọaĐộX/tọaĐộY;}
static unsigned độDài(const char*dữLiệuChuỗi){unsigned sốLượngPhầnMục=0;if(!dữLiệuChuỗi)thấtBạiJava();while(dữLiệuChuỗi[sốLượngPhầnMục])sốLượngPhầnMục++;return sốLượngPhầnMục;}
void inJava(từMáy vịTríDữLiệu,int giáTrịThuộcSố,int xuốngDòng){
    if(giáTrịThuộcSố){char giáTrịThứHai[16];unsigned sốLượngPhầnMục=0;int giáTrị=(int)vịTríDữLiệu;unsigned giáTrịKhôngDấu=giáTrị<0?0-(unsigned)giáTrị:giáTrị;do{giáTrịThứHai[sốLượngPhầnMục++]='0'+giáTrịKhôngDấu%10;giáTrịKhôngDấu/=10;}while(giáTrịKhôngDấu);if(giáTrị<0)giáTrịThứHai[sốLượngPhầnMục++]='-';while(sốLượngPhầnMục)ghiDữLiệuTệp(1,giáTrịThứHai+--sốLượngPhầnMục,1);}
    else{const char*dữLiệuChuỗi=vịTríDữLiệu?(const char*)vịTríDữLiệu:"null";ghiDữLiệuTệp(1,dữLiệuChuỗi,độDài(dữLiệuChuỗi));}if(xuốngDòng)ghiDữLiệuTệp(1,"\n",1);
}
từMáy ghiTệpJava(từMáy đườngDẫn,từMáy giáTrị){const char*dữLiệuChuỗi=(const char*)giáTrị;unsigned sốLượngPhầnMục=độDài(dữLiệuChuỗi);int thẻXửLýTệp=mởTệp((const char*)đườngDẫn,ghiGiáTrịChỉ|ThiếuNếuTạo|CácNộiDungCắtNgắn,0600);if(thẻXửLýTệp<0)thấtBạiJava();int giáTrịĐãTrảVề=ghiDữLiệuTệp(thẻXửLýTệp,dữLiệuChuỗi,sốLượngPhầnMục);đóngTệp(thẻXửLýTệp);if(giáTrịĐãTrảVề!=(int)sốLượngPhầnMục)thấtBạiJava();return 0;}
từMáy đọcTệpJava(từMáy đườngDẫn){int thẻXửLýTệp=mởTệp((const char*)đườngDẫn,đọcGiáTrịChỉ,0);if(thẻXửLýTệp<0)thấtBạiJava();int sốLượngPhầnMục=cỡTệp(thẻXửLýTệp);if(sốLượngPhầnMục<0||sốLượngPhầnMục>16384||(unsigned)(sốLượngPhầnMục+8)/8>8192-sứcChứaĐãDùng)thấtBạiJava();char*vịTríDữLiệu=(char*)(lưuTrữVùngNhớĐộng+sứcChứaĐãDùng);sứcChứaĐãDùng+=(sốLượngPhầnMục+8)/8;int giáTrịĐãTrảVề=đọcDữLiệuTệp(thẻXửLýTệp,vịTríDữLiệu,sốLượngPhầnMục);đóngTệp(thẻXửLýTệp);if(giáTrịĐãTrảVề!=sốLượngPhầnMục)thấtBạiJava();vịTríDữLiệu[sốLượngPhầnMục]=0;return (từMáy)vịTríDữLiệu;}
