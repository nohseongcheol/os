#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Papan_elgam(uintptr_t,uintptr_t,uintptr_t),Papan_Terminal(uintptr_t);
extern void Terminal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int area_VALUE,induk,koordinat_x,Y_koordinat,너비값,높이값,보이는지,manual_Navigasi,Navigasi_Policy;unsigned teks[128],panjang_VALUE; } Widget_Status;
static Widget_Status 요소들[4][32];
static int Prioritas[4],acara_Daftar[4][16];static unsigned 첫항목[4],entri_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Even(int pemilik_objek,int VALUE){if(entri_COUNT[pemilik_objek]<16){acara_Daftar[pemilik_objek][(첫항목[pemilik_objek]+entri_COUNT[pemilik_objek])%16]=VALUE;entri_COUNT[pemilik_objek]++;}}
static Widget_Status *elemen_VALUE(int pemilik_objek,int pengidentifikasi_VALUE){return pemilik_objek>=0&&pemilik_objek<4&&pengidentifikasi_VALUE>0&&pengidentifikasi_VALUE<=32&&요소들[pemilik_objek][pengidentifikasi_VALUE-1].area_VALUE?&요소들[pemilik_objek][pengidentifikasi_VALUE-1]:0;}
static void 사각영역(int koordinat_x,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){Papan_persegi_isi(koordinat_x,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int pemilik_objek){if(pemilik_objek<0||pemilik_objek>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[pemilik_objek][순번].area_VALUE==1&&요소들[pemilik_objek][순번].보이는지)return 1;return 0;}
void 화면초기화(int pemilik_objek){memset(요소들[pemilik_objek],0,sizeof(요소들[pemilik_objek]));entri_COUNT[pemilik_objek]=첫항목[pemilik_objek]=Prioritas[pemilik_objek]=긴부호없는값[pemilik_objek]=0;}
static void posisi(int pemilik_objek,Widget_Status *너비값,int *koordinat_x,int *Y_koordinat){*koordinat_x=너비값->koordinat_x;*Y_koordinat=너비값->Y_koordinat;int data_posisi=너비값->induk;for(int item_COUNT=0;data_posisi&&item_COUNT<32;item_COUNT++){Widget_Status *위쪽=elemen_VALUE(pemilik_objek,data_posisi);if(!위쪽)break;*koordinat_x+=위쪽->koordinat_x;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->area_VALUE==1?30:0);data_posisi=위쪽->induk;}}
static int 표시됨(int pemilik_objek,Widget_Status *너비값){for(int item_COUNT=0;item_COUNT<32;item_COUNT++){if(!너비값->보이는지)return 0;if(너비값->area_VALUE==1)return 1;너비값=elemen_VALUE(pemilik_objek,너비값->induk);if(!너비값)return 0;}return 0;}
static void teks(int koordinat_x,int Y_koordinat,Widget_Status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int saat_ini_posisi=0;for(unsigned 순번=0;순번<너비값->panjang_VALUE;순번++){unsigned pengodean_karakter=너비값->teks[순번],너비=pengodean_karakter>=256?16:8;if(saat_ini_posisi+(int)너비>최대값)break;Terminal_glif(koordinat_x+saat_ini_posisi,Y_koordinat,pengodean_karakter,색상,배경색);saat_ini_posisi+=너비;}}
void 화면다시그림(int pemilik_objek){
    if(!화면보임(pemilik_objek))return;
    for(int pemrosesan_urutan=1;pemrosesan_urutan<=5;pemrosesan_urutan++)for(int 순번=0;순번<32;순번++){
        Widget_Status *너비값=&요소들[pemilik_objek][순번];if(너비값->area_VALUE!=pemrosesan_urutan||!표시됨(pemilik_objek,너비값))continue;int koordinat_x,Y_koordinat;posisi(pemilik_objek,너비값,&koordinat_x,&Y_koordinat);
        if(pemrosesan_urutan==1){사각영역(koordinat_x,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(koordinat_x,Y_koordinat,너비값->너비값,30,0x905020);teks(koordinat_x+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(koordinat_x+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_glif(koordinat_x+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(pemrosesan_urutan==2)사각영역(koordinat_x,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(pemrosesan_urutan>=3){unsigned 배경색=pemrosesan_urutan==4?0xc0ab86:pemrosesan_urutan==5?0xffffff:0xeee9e0;if(pemrosesan_urutan!=3)사각영역(koordinat_x,Y_koordinat,너비값->너비값,너비값->높이값,배경색);teks(koordinat_x+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(pemrosesan_urutan==5&&Prioritas[pemilik_objek]==순번+1)사각영역(koordinat_x,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int pemilik_objek,int koordinat_x,int Y_koordinat){
    if(!화면보임(pemilik_objek))return 0;
    for(int 순번=0;순번<32;순번++){
        Widget_Status *Jendela=&요소들[pemilik_objek][순번];
        if(Jendela->area_VALUE==1&&Jendela->보이는지&&koordinat_x>=Jendela->koordinat_x&&Y_koordinat>=Jendela->Y_koordinat&&
           koordinat_x<Jendela->koordinat_x+Jendela->너비값&&Y_koordinat<Jendela->Y_koordinat+Jendela->높이값)return 1;
    }return 0;
}
int 화면가리킴(int pemilik_objek,unsigned 눌림,int koordinat_x,int Y_koordinat){
    if(!화면보임(pemilik_objek))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){Widget_Status *너비값=&요소들[pemilik_objek][순번];if(!너비값->area_VALUE||!표시됨(pemilik_objek,너비값))continue;int jendela_X,jendela_Y;posisi(pemilik_objek,너비값,&jendela_X,&jendela_Y);
        if(koordinat_x<jendela_X||Y_koordinat<jendela_Y||koordinat_x>=jendela_X+너비값->너비값||Y_koordinat>=jendela_Y+너비값->높이값)continue;
        if(너비값->area_VALUE==1&&Y_koordinat<jendela_Y+30&&koordinat_x>=jendela_X+너비값->너비값-28){if(너비값->Navigasi_Policy!=0)너비값->보이는지=0;Even(pemilik_objek,0x10000+순번+1);Papan_Terminal(3);return 1;}
        if(너비값->area_VALUE==4){Even(pemilik_objek,순번+1);return 1;}if(너비값->area_VALUE==5){Prioritas[pemilik_objek]=순번+1;Papan_Terminal(3);return 1;}
        if(너비값->area_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int pemilik_objek,unsigned SECOND_VALUE){
    Widget_Status *너비값=elemen_VALUE(pemilik_objek,Prioritas[pemilik_objek]);if(!너비값||너비값->area_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Even(pemilik_objek,Prioritas[pemilik_objek]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->panjang_VALUE)너비값->panjang_VALUE--;긴부호없는값[pemilik_objek]=0;}
    else{
        unsigned pengodean_karakter=SECOND_VALUE;
        if(긴부호없는값[pemilik_objek]){if((SECOND_VALUE&192)!=128){긴부호없는값[pemilik_objek]=0;return;}부호없는결과[pemilik_objek]=(부호없는결과[pemilik_objek]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[pemilik_objek])return;pengodean_karakter=부호없는결과[pemilik_objek];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[pemilik_objek]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[pemilik_objek]=SECOND_VALUE&((1u<<(6-긴부호없는값[pemilik_objek]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(pengodean_karakter>0x10ffff||(pengodean_karakter>=0xd800&&pengodean_karakter<=0xdfff))return;if(너비값->panjang_VALUE<127)너비값->teks[너비값->panjang_VALUE++]=pengodean_karakter;
    }
    Papan_Terminal(3);
}
int 화면호출(int pemilik_objek,unsigned Aksi,int pengidentifikasi_VALUE,int 첫째값,int SECOND_VALUE,int kode_karakter,int tujuan_data){
    if(pemilik_objek<0||pemilik_objek>=4)return -22;Widget_Status *너비값=elemen_VALUE(pemilik_objek,pengidentifikasi_VALUE);
    if(Aksi==0){if(pengidentifikasi_VALUE<1||pengidentifikasi_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[pemilik_objek][순번].area_VALUE==0){너비값=&요소들[pemilik_objek][순번];memset(너비값,0,sizeof(*너비값));너비값->area_VALUE=pengidentifikasi_VALUE;너비값->보이는지=pengidentifikasi_VALUE!=1;너비값->너비값=pengidentifikasi_VALUE==1?380:220;너비값->높이값=pengidentifikasi_VALUE==1?240:28;너비값->Navigasi_Policy=1;너비값->koordinat_x=pengidentifikasi_VALUE==1?130:16;너비값->Y_koordinat=pengidentifikasi_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Aksi==5){if(!entri_COUNT[pemilik_objek])return 0;int 반환값=acara_Daftar[pemilik_objek][첫항목[pemilik_objek]];첫항목[pemilik_objek]=(첫항목[pemilik_objek]+1)%16;entri_COUNT[pemilik_objek]--;return 반환값;}
    if(Aksi==6)return 화면보임(pemilik_objek);
    if(!너비값)return -9;
    int 이전표시=표시됨(pemilik_objek,너비값);
    if(Aksi==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||kode_karakter<1||tujuan_data<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||kode_karakter>바탕너비-첫째값||tujuan_data>바탕높이-SECOND_VALUE)return -22;너비값->koordinat_x=첫째값;너비값->Y_koordinat=SECOND_VALUE;너비값->너비값=kode_karakter;너비값->높이값=tujuan_data;너비값->manual_Navigasi=1;}
    else if(Aksi==2){Widget_Status *turunan=elemen_VALUE(pemilik_objek,첫째값);if(!turunan||turunan==너비값||turunan->area_VALUE==1)return -22;int data_posisi=pengidentifikasi_VALUE;for(int 깊이=0;data_posisi&&깊이<32;깊이++){if(data_posisi==첫째값)return -22;Widget_Status *위쪽=elemen_VALUE(pemilik_objek,data_posisi);data_posisi=위쪽?위쪽->induk:0;}turunan->induk=pengidentifikasi_VALUE;if(!turunan->manual_Navigasi){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[pemilik_objek][순번]!=turunan&&요소들[pemilik_objek][순번].induk==pengidentifikasi_VALUE)형제요소++;turunan->Y_koordinat=16+형제요소*36;}}
    else if(Aksi==3)너비값->보이는지=첫째값!=0;
    else if(Aksi==4)너비값->보이는지=0;
    else if(Aksi==7)너비값->Navigasi_Policy=첫째값;
    else if(Aksi==8)return 너비값->panjang_VALUE;
    else if(Aksi==9)return 첫째값>=0&&(unsigned)첫째값<너비값->panjang_VALUE?너비값->teks[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(pemilik_objek,너비값))Papan_Terminal(3);return 0;
}
int 화면글(int pemilik_objek,int pengidentifikasi_VALUE,const uint32_t *data,unsigned item_COUNT){Widget_Status *너비값=elemen_VALUE(pemilik_objek,pengidentifikasi_VALUE);if(!너비값)return -9;if(item_COUNT>127)return -22;for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned pengodean_karakter=data[순번];if(pengodean_karakter>0x10ffff||(pengodean_karakter>=0xd800&&pengodean_karakter<=0xdfff))return -22;}for(unsigned 순번=0;순번<item_COUNT;순번++)너비값->teks[순번]=data[순번];너비값->panjang_VALUE=item_COUNT;if(표시됨(pemilik_objek,너비값))Papan_Terminal(3);return 0;}
