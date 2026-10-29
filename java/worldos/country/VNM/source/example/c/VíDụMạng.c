#include "QuyƯớcVíDụ.h"
#include <ABIMạng.h>
int main(int sốLượngĐốiSố,char **cácĐốiSố) {
    if(sốLượngĐốiSố!=2)return ĐầuRa("사용법: ./네트워크 UDP창구번호\n");
    unsigned giáTrịCổng=0;for(int trịSố=0;cácĐốiSố[1][trịSố];trịSố++) {
        if(cácĐốiSố[1][trịSố]<'0'||cácĐốiSố[1][trịSố]>'9')return 2;
        giáTrịCổng=giáTrịCổng*10+cácĐốiSố[1][trịSố]-'0';if(giáTrịCổng>65535)return 2;
    }
    if(!giáTrịCổng)return 2;
    int điểmCuối=tạoĐiểmCuối(HọLiênMạng,ỔCắmMạngĐiệnDữLiệu,GiaoThứcĐiệnDữLiệu);if(điểmCuối<0)return 3;
    struct ĐịaChỉỔCắmMạngLiênMạng địaChỉ={0};địaChỉ.họĐịaChỉ=HọLiênMạng;
    if(ràngBuộcĐịaChỉ(điểmCuối,(struct ĐịaChỉỔCắmMạng *)&địaChỉ,sizeof(địaChỉ))<0)return 4;
    địaChỉ.sốCổng=ngắnKiểuMạng(giáTrịCổng);địaChỉ.ĐịaChỉLiênMạng.giáTrịĐịaChỉ=sốNguyênMạng(0x0a000202);
    const char điệnDữLiệu[]="C UDP Tiếng Việt";
    if(gửiDữLiệuĐiệnDữLiệu(điểmCuối,điệnDữLiệu,sizeof(điệnDữLiệu)-1,0,(struct ĐịaChỉỔCắmMạng *)&địaChỉ,sizeof(địaChỉ))!=sizeof(điệnDữLiệu)-1)return 5;
    char lờiĐáp[512];unsigned chạy=miliGiây();int sốLượngĐãNhận;
    do {
        sốLượngĐãNhận=nhậnDữLiệuĐiệnDữLiệu(điểmCuối,lờiĐáp,sizeof(lờiĐáp),0,0,0);
        if(sốLượngĐãNhận<0&&sốLỗi!=LỗiLạiThửLàm)return 6;
    } while(sốLượngĐãNhận<0&&(unsigned)(miliGiây()-chạy)<700);
    đóngTệp(điểmCuối);if(sốLượngĐãNhận!=sizeof(điệnDữLiệu)-1)return 7;
    for(int trịSố=0;trịSố<sốLượngĐãNhận;trịSố++)if(điệnDữLiệu[trịSố]!=lờiĐáp[trịSố])return 8;
    return ĐầuRa("C 네트워크 xácMinh: UDP Tiếng Việt\n");
}
