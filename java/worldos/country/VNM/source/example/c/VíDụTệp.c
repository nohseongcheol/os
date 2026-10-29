#include "QuyƯớcVíDụ.h"
int main(void) {
    const char DữLiệu[]="C Tệp: Tiếng Việt 😀\n";
    int Tệp=mởTệp("c.txt",GhiĐọc|ThiếuNếuTạo|CácNộiDungCắtNgắn,0600);
    if(Tệp<0)return 1;
    if(ghiDữLiệuTệp(Tệp,DữLiệu,sizeof(DữLiệu)-1)!=sizeof(DữLiệu)-1)return 2;
    if(dịchVịTệp(Tệp,0,PhầnĐầuTừ)!=0)return 3;
    char đọcGiáTrịVănBản[128]={0};int độDài=đọcDữLiệuTệp(Tệp,đọcGiáTrịVănBản,sizeof(đọcGiáTrịVănBản)-1);
    đóngTệp(Tệp);
    if(độDài!=sizeof(DữLiệu)-1)return 4;
    for(int trịSố=0;trịSố<độDài;trịSố++)if(DữLiệu[trịSố]!=đọcGiáTrịVănBản[trịSố])return 5;
    return ĐầuRa(đọcGiáTrịVănBản);
}
