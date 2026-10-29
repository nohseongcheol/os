#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int legoro_boleng,부모항목,kamano_ya_x,세로좌표,너비값,높이값,보이는지,menyuale_Sebopego,Sebopego_pholisi;unsigned Sengwalwa[128],botelele_boleng; } witšete_boemo;
static witšete_boemo 요소들[4][32];
static int Šeditše[4],tiragalo_Lenaneo[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void tiragalo(int mong_selo,int boleng){if(항목수[mong_selo]<16){tiragalo_Lenaneo[mong_selo][(첫항목[mong_selo]+항목수[mong_selo])%16]=boleng;항목수[mong_selo]++;}}
static witšete_boemo *elemente_boleng(int mong_selo,int sešupi_boleng){return mong_selo>=0&&mong_selo<4&&sešupi_boleng>0&&sešupi_boleng<=32&&요소들[mong_selo][sešupi_boleng-1].legoro_boleng?&요소들[mong_selo][sešupi_boleng-1]:0;}
static void 사각영역(int kamano_ya_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(kamano_ya_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int mong_selo){if(mong_selo<0||mong_selo>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[mong_selo][순번].legoro_boleng==1&&요소들[mong_selo][순번].보이는지)return 1;return 0;}
void 화면초기화(int mong_selo){memset(요소들[mong_selo],0,sizeof(요소들[mong_selo]));항목수[mong_selo]=첫항목[mong_selo]=Šeditše[mong_selo]=긴부호없는값[mong_selo]=0;}
static void 위치(int mong_selo,witšete_boemo *너비값,int *kamano_ya_x,int *세로좌표){*kamano_ya_x=너비값->kamano_ya_x;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){witšete_boemo *위쪽=elemente_boleng(mong_selo,자료위치);if(!위쪽)break;*kamano_ya_x+=위쪽->kamano_ya_x;*세로좌표+=위쪽->세로좌표+(위쪽->legoro_boleng==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int mong_selo,witšete_boemo *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->legoro_boleng==1)return 1;너비값=elemente_boleng(mong_selo,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Sengwalwa(int kamano_ya_x,int 세로좌표,witšete_boemo *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->botelele_boleng;순번++){unsigned tlhaka_go_enkhouta=너비값->Sengwalwa[순번],너비=tlhaka_go_enkhouta>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(kamano_ya_x+현재위치,세로좌표,tlhaka_go_enkhouta,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int mong_selo){
    if(!화면보임(mong_selo))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        witšete_boemo *너비값=&요소들[mong_selo][순번];if(너비값->legoro_boleng!=처리차례||!표시됨(mong_selo,너비값))continue;int kamano_ya_x,세로좌표;위치(mong_selo,너비값,&kamano_ya_x,&세로좌표);
        if(처리차례==1){사각영역(kamano_ya_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(kamano_ya_x,세로좌표,너비값->너비값,30,0x905020);Sengwalwa(kamano_ya_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(kamano_ya_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(kamano_ya_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(kamano_ya_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(kamano_ya_x,세로좌표,너비값->너비값,너비값->높이값,배경색);Sengwalwa(kamano_ya_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Šeditše[mong_selo]==순번+1)사각영역(kamano_ya_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int mong_selo,int kamano_ya_x,int 세로좌표){
    if(!화면보임(mong_selo))return 0;
    for(int 순번=0;순번<32;순번++){
        witšete_boemo *lefastere=&요소들[mong_selo][순번];
        if(lefastere->legoro_boleng==1&&lefastere->보이는지&&kamano_ya_x>=lefastere->kamano_ya_x&&세로좌표>=lefastere->세로좌표&&
           kamano_ya_x<lefastere->kamano_ya_x+lefastere->너비값&&세로좌표<lefastere->세로좌표+lefastere->높이값)return 1;
    }return 0;
}
int 화면가리킴(int mong_selo,unsigned 눌림,int kamano_ya_x,int 세로좌표){
    if(!화면보임(mong_selo))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){witšete_boemo *너비값=&요소들[mong_selo][순번];if(!너비값->legoro_boleng||!표시됨(mong_selo,너비값))continue;int 창가로,창세로;위치(mong_selo,너비값,&창가로,&창세로);
        if(kamano_ya_x<창가로||세로좌표<창세로||kamano_ya_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->legoro_boleng==1&&세로좌표<창세로+30&&kamano_ya_x>=창가로+너비값->너비값-28){if(너비값->Sebopego_pholisi!=0)너비값->보이는지=0;tiragalo(mong_selo,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->legoro_boleng==4){tiragalo(mong_selo,순번+1);return 1;}if(너비값->legoro_boleng==5){Šeditše[mong_selo]=순번+1;보드터미널(3);return 1;}
        if(너비값->legoro_boleng==1)return 1;
    }return 0;
}
void 화면누름(int mong_selo,unsigned 둘째값){
    witšete_boemo *너비값=elemente_boleng(mong_selo,Šeditše[mong_selo]);if(!너비값||너비값->legoro_boleng!=5)return;
    if(둘째값==13||둘째값==10){tiragalo(mong_selo,Šeditše[mong_selo]);return;}
    if(둘째값==8||둘째값==127){if(너비값->botelele_boleng)너비값->botelele_boleng--;긴부호없는값[mong_selo]=0;}
    else{
        unsigned tlhaka_go_enkhouta=둘째값;
        if(긴부호없는값[mong_selo]){if((둘째값&192)!=128){긴부호없는값[mong_selo]=0;return;}부호없는결과[mong_selo]=(부호없는결과[mong_selo]<<6)|(둘째값&63);if(--긴부호없는값[mong_selo])return;tlhaka_go_enkhouta=부호없는결과[mong_selo];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[mong_selo]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[mong_selo]=둘째값&((1u<<(6-긴부호없는값[mong_selo]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(tlhaka_go_enkhouta>0x10ffff||(tlhaka_go_enkhouta>=0xd800&&tlhaka_go_enkhouta<=0xdfff))return;if(너비값->botelele_boleng<127)너비값->Sengwalwa[너비값->botelele_boleng++]=tlhaka_go_enkhouta;
    }
    보드터미널(3);
}
int 화면호출(int mong_selo,unsigned Mogato,int sešupi_boleng,int 첫째값,int 둘째값,int khouto_ya_tlhaka,int boyo_data){
    if(mong_selo<0||mong_selo>=4)return -22;witšete_boemo *너비값=elemente_boleng(mong_selo,sešupi_boleng);
    if(Mogato==0){if(sešupi_boleng<1||sešupi_boleng>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[mong_selo][순번].legoro_boleng==0){너비값=&요소들[mong_selo][순번];memset(너비값,0,sizeof(*너비값));너비값->legoro_boleng=sešupi_boleng;너비값->보이는지=sešupi_boleng!=1;너비값->너비값=sešupi_boleng==1?380:220;너비값->높이값=sešupi_boleng==1?240:28;너비값->Sebopego_pholisi=1;너비값->kamano_ya_x=sešupi_boleng==1?130:16;너비값->세로좌표=sešupi_boleng==1?110:16;return 순번+1;}return -28;}
    if(Mogato==5){if(!항목수[mong_selo])return 0;int 반환값=tiragalo_Lenaneo[mong_selo][첫항목[mong_selo]];첫항목[mong_selo]=(첫항목[mong_selo]+1)%16;항목수[mong_selo]--;return 반환값;}
    if(Mogato==6)return 화면보임(mong_selo);
    if(!너비값)return -9;
    int 이전표시=표시됨(mong_selo,너비값);
    if(Mogato==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||khouto_ya_tlhaka<1||boyo_data<1||첫째값>바탕너비||둘째값>바탕높이||khouto_ya_tlhaka>바탕너비-첫째값||boyo_data>바탕높이-둘째값)return -22;너비값->kamano_ya_x=첫째값;너비값->세로좌표=둘째값;너비값->너비값=khouto_ya_tlhaka;너비값->높이값=boyo_data;너비값->menyuale_Sebopego=1;}
    else if(Mogato==2){witšete_boemo *elemente_e_nnyane=elemente_boleng(mong_selo,첫째값);if(!elemente_e_nnyane||elemente_e_nnyane==너비값||elemente_e_nnyane->legoro_boleng==1)return -22;int 자료위치=sešupi_boleng;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;witšete_boemo *위쪽=elemente_boleng(mong_selo,자료위치);자료위치=위쪽?위쪽->부모항목:0;}elemente_e_nnyane->부모항목=sešupi_boleng;if(!elemente_e_nnyane->menyuale_Sebopego){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[mong_selo][순번]!=elemente_e_nnyane&&요소들[mong_selo][순번].부모항목==sešupi_boleng)형제요소++;elemente_e_nnyane->세로좌표=16+형제요소*36;}}
    else if(Mogato==3)너비값->보이는지=첫째값!=0;
    else if(Mogato==4)너비값->보이는지=0;
    else if(Mogato==7)너비값->Sebopego_pholisi=첫째값;
    else if(Mogato==8)return 너비값->botelele_boleng;
    else if(Mogato==9)return 첫째값>=0&&(unsigned)첫째값<너비값->botelele_boleng?너비값->Sengwalwa[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(mong_selo,너비값))보드터미널(3);return 0;
}
int 화면글(int mong_selo,int sešupi_boleng,const uint32_t *data,unsigned 개수){witšete_boemo *너비값=elemente_boleng(mong_selo,sešupi_boleng);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned tlhaka_go_enkhouta=data[순번];if(tlhaka_go_enkhouta>0x10ffff||(tlhaka_go_enkhouta>=0xd800&&tlhaka_go_enkhouta<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->Sengwalwa[순번]=data[순번];너비값->botelele_boleng=개수;if(표시됨(mong_selo,너비값))보드터미널(3);return 0;}
