#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Papan_pel(uintptr_t,uintptr_t,uintptr_t),Papan_Terminal(uintptr_t);
extern void Terminal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int bidang_VALUE,부모항목,koordinat_x,Y_koordinat,너비값,높이값,보이는지,manual_Navigasi,Navigasi_dasar;unsigned Teks[128],kepanjangan_VALUE; } widget_status;
static widget_status 요소들[4][32];
static int Tumpuan[4],acara_Senarai[4][16];static unsigned 첫항목[4],pemasukan_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Peristiwa(int pemilik_objek,int VALUE){if(pemasukan_COUNT[pemilik_objek]<16){acara_Senarai[pemilik_objek][(첫항목[pemilik_objek]+pemasukan_COUNT[pemilik_objek])%16]=VALUE;pemasukan_COUNT[pemilik_objek]++;}}
static widget_status *unsur_VALUE(int pemilik_objek,int 식별자){return pemilik_objek>=0&&pemilik_objek<4&&식별자>0&&식별자<=32&&요소들[pemilik_objek][식별자-1].bidang_VALUE?&요소들[pemilik_objek][식별자-1]:0;}
static void 사각영역(int koordinat_x,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){Papan_segi_empat_tepat_isi(koordinat_x,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int pemilik_objek){if(pemilik_objek<0||pemilik_objek>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[pemilik_objek][순번].bidang_VALUE==1&&요소들[pemilik_objek][순번].보이는지)return 1;return 0;}
void 화면초기화(int pemilik_objek){memset(요소들[pemilik_objek],0,sizeof(요소들[pemilik_objek]));pemasukan_COUNT[pemilik_objek]=첫항목[pemilik_objek]=Tumpuan[pemilik_objek]=긴부호없는값[pemilik_objek]=0;}
static void Kedudukan(int pemilik_objek,widget_status *너비값,int *koordinat_x,int *Y_koordinat){*koordinat_x=너비값->koordinat_x;*Y_koordinat=너비값->Y_koordinat;int data_jawatan=너비값->부모항목;for(int item_COUNT=0;data_jawatan&&item_COUNT<32;item_COUNT++){widget_status *위쪽=unsur_VALUE(pemilik_objek,data_jawatan);if(!위쪽)break;*koordinat_x+=위쪽->koordinat_x;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->bidang_VALUE==1?30:0);data_jawatan=위쪽->부모항목;}}
static int 표시됨(int pemilik_objek,widget_status *너비값){for(int item_COUNT=0;item_COUNT<32;item_COUNT++){if(!너비값->보이는지)return 0;if(너비값->bidang_VALUE==1)return 1;너비값=unsur_VALUE(pemilik_objek,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Teks(int koordinat_x,int Y_koordinat,widget_status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->kepanjangan_VALUE;순번++){unsigned pengekodan_aksara=너비값->Teks[순번],너비=pengekodan_aksara>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminal_glif(koordinat_x+현재위치,Y_koordinat,pengekodan_aksara,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int pemilik_objek){
    if(!화면보임(pemilik_objek))return;
    for(int pemprosesan_tertib=1;pemprosesan_tertib<=5;pemprosesan_tertib++)for(int 순번=0;순번<32;순번++){
        widget_status *너비값=&요소들[pemilik_objek][순번];if(너비값->bidang_VALUE!=pemprosesan_tertib||!표시됨(pemilik_objek,너비값))continue;int koordinat_x,Y_koordinat;Kedudukan(pemilik_objek,너비값,&koordinat_x,&Y_koordinat);
        if(pemprosesan_tertib==1){사각영역(koordinat_x,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(koordinat_x,Y_koordinat,너비값->너비값,30,0x905020);Teks(koordinat_x+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(koordinat_x+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_glif(koordinat_x+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(pemprosesan_tertib==2)사각영역(koordinat_x,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(pemprosesan_tertib>=3){unsigned 배경색=pemprosesan_tertib==4?0xc0ab86:pemprosesan_tertib==5?0xffffff:0xeee9e0;if(pemprosesan_tertib!=3)사각영역(koordinat_x,Y_koordinat,너비값->너비값,너비값->높이값,배경색);Teks(koordinat_x+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(pemprosesan_tertib==5&&Tumpuan[pemilik_objek]==순번+1)사각영역(koordinat_x,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int pemilik_objek,int koordinat_x,int Y_koordinat){
    if(!화면보임(pemilik_objek))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_status *Tetingkap=&요소들[pemilik_objek][순번];
        if(Tetingkap->bidang_VALUE==1&&Tetingkap->보이는지&&koordinat_x>=Tetingkap->koordinat_x&&Y_koordinat>=Tetingkap->Y_koordinat&&
           koordinat_x<Tetingkap->koordinat_x+Tetingkap->너비값&&Y_koordinat<Tetingkap->Y_koordinat+Tetingkap->높이값)return 1;
    }return 0;
}
int 화면가리킴(int pemilik_objek,unsigned 눌림,int koordinat_x,int Y_koordinat){
    if(!화면보임(pemilik_objek))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_status *너비값=&요소들[pemilik_objek][순번];if(!너비값->bidang_VALUE||!표시됨(pemilik_objek,너비값))continue;int tetingkap_X,tetingkap_Y;Kedudukan(pemilik_objek,너비값,&tetingkap_X,&tetingkap_Y);
        if(koordinat_x<tetingkap_X||Y_koordinat<tetingkap_Y||koordinat_x>=tetingkap_X+너비값->너비값||Y_koordinat>=tetingkap_Y+너비값->높이값)continue;
        if(너비값->bidang_VALUE==1&&Y_koordinat<tetingkap_Y+30&&koordinat_x>=tetingkap_X+너비값->너비값-28){if(너비값->Navigasi_dasar!=0)너비값->보이는지=0;Peristiwa(pemilik_objek,0x10000+순번+1);Papan_Terminal(3);return 1;}
        if(너비값->bidang_VALUE==4){Peristiwa(pemilik_objek,순번+1);return 1;}if(너비값->bidang_VALUE==5){Tumpuan[pemilik_objek]=순번+1;Papan_Terminal(3);return 1;}
        if(너비값->bidang_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int pemilik_objek,unsigned SECOND_VALUE){
    widget_status *너비값=unsur_VALUE(pemilik_objek,Tumpuan[pemilik_objek]);if(!너비값||너비값->bidang_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Peristiwa(pemilik_objek,Tumpuan[pemilik_objek]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->kepanjangan_VALUE)너비값->kepanjangan_VALUE--;긴부호없는값[pemilik_objek]=0;}
    else{
        unsigned pengekodan_aksara=SECOND_VALUE;
        if(긴부호없는값[pemilik_objek]){if((SECOND_VALUE&192)!=128){긴부호없는값[pemilik_objek]=0;return;}부호없는결과[pemilik_objek]=(부호없는결과[pemilik_objek]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[pemilik_objek])return;pengekodan_aksara=부호없는결과[pemilik_objek];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[pemilik_objek]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[pemilik_objek]=SECOND_VALUE&((1u<<(6-긴부호없는값[pemilik_objek]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(pengekodan_aksara>0x10ffff||(pengekodan_aksara>=0xd800&&pengekodan_aksara<=0xdfff))return;if(너비값->kepanjangan_VALUE<127)너비값->Teks[너비값->kepanjangan_VALUE++]=pengekodan_aksara;
    }
    Papan_Terminal(3);
}
int 화면호출(int pemilik_objek,unsigned Aksi,int 식별자,int 첫째값,int SECOND_VALUE,int titik_kod,int destinasi_data){
    if(pemilik_objek<0||pemilik_objek>=4)return -22;widget_status *너비값=unsur_VALUE(pemilik_objek,식별자);
    if(Aksi==0){if(식별자<1||식별자>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[pemilik_objek][순번].bidang_VALUE==0){너비값=&요소들[pemilik_objek][순번];memset(너비값,0,sizeof(*너비값));너비값->bidang_VALUE=식별자;너비값->보이는지=식별자!=1;너비값->너비값=식별자==1?380:220;너비값->높이값=식별자==1?240:28;너비값->Navigasi_dasar=1;너비값->koordinat_x=식별자==1?130:16;너비값->Y_koordinat=식별자==1?110:16;return 순번+1;}return -28;}
    if(Aksi==5){if(!pemasukan_COUNT[pemilik_objek])return 0;int 반환값=acara_Senarai[pemilik_objek][첫항목[pemilik_objek]];첫항목[pemilik_objek]=(첫항목[pemilik_objek]+1)%16;pemasukan_COUNT[pemilik_objek]--;return 반환값;}
    if(Aksi==6)return 화면보임(pemilik_objek);
    if(!너비값)return -9;
    int 이전표시=표시됨(pemilik_objek,너비값);
    if(Aksi==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||titik_kod<1||destinasi_data<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||titik_kod>바탕너비-첫째값||destinasi_data>바탕높이-SECOND_VALUE)return -22;너비값->koordinat_x=첫째값;너비값->Y_koordinat=SECOND_VALUE;너비값->너비값=titik_kod;너비값->높이값=destinasi_data;너비값->manual_Navigasi=1;}
    else if(Aksi==2){widget_status *anak=unsur_VALUE(pemilik_objek,첫째값);if(!anak||anak==너비값||anak->bidang_VALUE==1)return -22;int data_jawatan=식별자;for(int 깊이=0;data_jawatan&&깊이<32;깊이++){if(data_jawatan==첫째값)return -22;widget_status *위쪽=unsur_VALUE(pemilik_objek,data_jawatan);data_jawatan=위쪽?위쪽->부모항목:0;}anak->부모항목=식별자;if(!anak->manual_Navigasi){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[pemilik_objek][순번]!=anak&&요소들[pemilik_objek][순번].부모항목==식별자)형제요소++;anak->Y_koordinat=16+형제요소*36;}}
    else if(Aksi==3)너비값->보이는지=첫째값!=0;
    else if(Aksi==4)너비값->보이는지=0;
    else if(Aksi==7)너비값->Navigasi_dasar=첫째값;
    else if(Aksi==8)return 너비값->kepanjangan_VALUE;
    else if(Aksi==9)return 첫째값>=0&&(unsigned)첫째값<너비값->kepanjangan_VALUE?너비값->Teks[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(pemilik_objek,너비값))Papan_Terminal(3);return 0;
}
int 화면글(int pemilik_objek,int 식별자,const uint32_t *data,unsigned item_COUNT){widget_status *너비값=unsur_VALUE(pemilik_objek,식별자);if(!너비값)return -9;if(item_COUNT>127)return -22;for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned pengekodan_aksara=data[순번];if(pengekodan_aksara>0x10ffff||(pengekodan_aksara>=0xd800&&pengekodan_aksara<=0xdfff))return -22;}for(unsigned 순번=0;순번<item_COUNT;순번++)너비값->Teks[순번]=data[순번];너비값->kepanjangan_VALUE=item_COUNT;if(표시됨(pemilik_objek,너비값))Papan_Terminal(3);return 0;}
