#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t yozuv_taxtasi_piksel(uintptr_t,uintptr_t,uintptr_t),yozuv_taxtasi_Terminal(uintptr_t);
extern void Terminal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int toifa_VALUE,부모항목,x_koordinata,Y_tugmasi_koordinat,너비값,높이값,보이는지,qo_llanma_Maket,Maket_siyosat;unsigned Matn[128],uzunlik_VALUE; } vidjet_holat;
static vidjet_holat 요소들[4][32];
static int Muhim[4],hodisa_Ro_yxat[4][16];static unsigned 첫항목[4],kiritish_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void hodisa(int egasi_obyekt,int VALUE){if(kiritish_COUNT[egasi_obyekt]<16){hodisa_Ro_yxat[egasi_obyekt][(첫항목[egasi_obyekt]+kiritish_COUNT[egasi_obyekt])%16]=VALUE;kiritish_COUNT[egasi_obyekt]++;}}
static vidjet_holat *element_VALUE(int egasi_obyekt,int identifikator_VALUE){return egasi_obyekt>=0&&egasi_obyekt<4&&identifikator_VALUE>0&&identifikator_VALUE<=32&&요소들[egasi_obyekt][identifikator_VALUE-1].toifa_VALUE?&요소들[egasi_obyekt][identifikator_VALUE-1]:0;}
static void 사각영역(int x_koordinata,int Y_tugmasi_koordinat,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_koordinata,Y_tugmasi_koordinat,너비값,높이값,색상);}
int 화면보임(int egasi_obyekt){if(egasi_obyekt<0||egasi_obyekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[egasi_obyekt][순번].toifa_VALUE==1&&요소들[egasi_obyekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int egasi_obyekt){memset(요소들[egasi_obyekt],0,sizeof(요소들[egasi_obyekt]));kiritish_COUNT[egasi_obyekt]=첫항목[egasi_obyekt]=Muhim[egasi_obyekt]=긴부호없는값[egasi_obyekt]=0;}
static void Holati(int egasi_obyekt,vidjet_holat *너비값,int *x_koordinata,int *Y_tugmasi_koordinat){*x_koordinata=너비값->x_koordinata;*Y_tugmasi_koordinat=너비값->Y_tugmasi_koordinat;int ma_lumotlar_holat=너비값->부모항목;for(int element_COUNT=0;ma_lumotlar_holat&&element_COUNT<32;element_COUNT++){vidjet_holat *위쪽=element_VALUE(egasi_obyekt,ma_lumotlar_holat);if(!위쪽)break;*x_koordinata+=위쪽->x_koordinata;*Y_tugmasi_koordinat+=위쪽->Y_tugmasi_koordinat+(위쪽->toifa_VALUE==1?30:0);ma_lumotlar_holat=위쪽->부모항목;}}
static int 표시됨(int egasi_obyekt,vidjet_holat *너비값){for(int element_COUNT=0;element_COUNT<32;element_COUNT++){if(!너비값->보이는지)return 0;if(너비값->toifa_VALUE==1)return 1;너비값=element_VALUE(egasi_obyekt,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Matn(int x_koordinata,int Y_tugmasi_koordinat,vidjet_holat *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->uzunlik_VALUE;순번++){unsigned belgi_kodlash=너비값->Matn[순번],너비=belgi_kodlash>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminal_glif(x_koordinata+현재위치,Y_tugmasi_koordinat,belgi_kodlash,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int egasi_obyekt){
    if(!화면보임(egasi_obyekt))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        vidjet_holat *너비값=&요소들[egasi_obyekt][순번];if(너비값->toifa_VALUE!=처리차례||!표시됨(egasi_obyekt,너비값))continue;int x_koordinata,Y_tugmasi_koordinat;Holati(egasi_obyekt,너비값,&x_koordinata,&Y_tugmasi_koordinat);
        if(처리차례==1){사각영역(x_koordinata,Y_tugmasi_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinata,Y_tugmasi_koordinat,너비값->너비값,30,0x905020);Matn(x_koordinata+10,Y_tugmasi_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinata+너비값->너비값-28,Y_tugmasi_koordinat+4,24,22,0x5555b8);Terminal_glif(x_koordinata+너비값->너비값-20,Y_tugmasi_koordinat+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_koordinata,Y_tugmasi_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_koordinata,Y_tugmasi_koordinat,너비값->너비값,너비값->높이값,배경색);Matn(x_koordinata+4,Y_tugmasi_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Muhim[egasi_obyekt]==순번+1)사각영역(x_koordinata,Y_tugmasi_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int egasi_obyekt,int x_koordinata,int Y_tugmasi_koordinat){
    if(!화면보임(egasi_obyekt))return 0;
    for(int 순번=0;순번<32;순번++){
        vidjet_holat *oyna=&요소들[egasi_obyekt][순번];
        if(oyna->toifa_VALUE==1&&oyna->보이는지&&x_koordinata>=oyna->x_koordinata&&Y_tugmasi_koordinat>=oyna->Y_tugmasi_koordinat&&
           x_koordinata<oyna->x_koordinata+oyna->너비값&&Y_tugmasi_koordinat<oyna->Y_tugmasi_koordinat+oyna->높이값)return 1;
    }return 0;
}
int 화면가리킴(int egasi_obyekt,unsigned 눌림,int x_koordinata,int Y_tugmasi_koordinat){
    if(!화면보임(egasi_obyekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){vidjet_holat *너비값=&요소들[egasi_obyekt][순번];if(!너비값->toifa_VALUE||!표시됨(egasi_obyekt,너비값))continue;int oyna_X_tugmasi,oyna_Y_tugmasi;Holati(egasi_obyekt,너비값,&oyna_X_tugmasi,&oyna_Y_tugmasi);
        if(x_koordinata<oyna_X_tugmasi||Y_tugmasi_koordinat<oyna_Y_tugmasi||x_koordinata>=oyna_X_tugmasi+너비값->너비값||Y_tugmasi_koordinat>=oyna_Y_tugmasi+너비값->높이값)continue;
        if(너비값->toifa_VALUE==1&&Y_tugmasi_koordinat<oyna_Y_tugmasi+30&&x_koordinata>=oyna_X_tugmasi+너비값->너비값-28){if(너비값->Maket_siyosat!=0)너비값->보이는지=0;hodisa(egasi_obyekt,0x10000+순번+1);yozuv_taxtasi_Terminal(3);return 1;}
        if(너비값->toifa_VALUE==4){hodisa(egasi_obyekt,순번+1);return 1;}if(너비값->toifa_VALUE==5){Muhim[egasi_obyekt]=순번+1;yozuv_taxtasi_Terminal(3);return 1;}
        if(너비값->toifa_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int egasi_obyekt,unsigned SECOND_VALUE){
    vidjet_holat *너비값=element_VALUE(egasi_obyekt,Muhim[egasi_obyekt]);if(!너비값||너비값->toifa_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){hodisa(egasi_obyekt,Muhim[egasi_obyekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->uzunlik_VALUE)너비값->uzunlik_VALUE--;긴부호없는값[egasi_obyekt]=0;}
    else{
        unsigned belgi_kodlash=SECOND_VALUE;
        if(긴부호없는값[egasi_obyekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[egasi_obyekt]=0;return;}부호없는결과[egasi_obyekt]=(부호없는결과[egasi_obyekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[egasi_obyekt])return;belgi_kodlash=부호없는결과[egasi_obyekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[egasi_obyekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[egasi_obyekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[egasi_obyekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(belgi_kodlash>0x10ffff||(belgi_kodlash>=0xd800&&belgi_kodlash<=0xdfff))return;if(너비값->uzunlik_VALUE<127)너비값->Matn[너비값->uzunlik_VALUE++]=belgi_kodlash;
    }
    yozuv_taxtasi_Terminal(3);
}
int 화면호출(int egasi_obyekt,unsigned Amal,int identifikator_VALUE,int 첫째값,int SECOND_VALUE,int belgi_kodi,int ko_chirish_joyi_ma_lumotlar){
    if(egasi_obyekt<0||egasi_obyekt>=4)return -22;vidjet_holat *너비값=element_VALUE(egasi_obyekt,identifikator_VALUE);
    if(Amal==0){if(identifikator_VALUE<1||identifikator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[egasi_obyekt][순번].toifa_VALUE==0){너비값=&요소들[egasi_obyekt][순번];memset(너비값,0,sizeof(*너비값));너비값->toifa_VALUE=identifikator_VALUE;너비값->보이는지=identifikator_VALUE!=1;너비값->너비값=identifikator_VALUE==1?380:220;너비값->높이값=identifikator_VALUE==1?240:28;너비값->Maket_siyosat=1;너비값->x_koordinata=identifikator_VALUE==1?130:16;너비값->Y_tugmasi_koordinat=identifikator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Amal==5){if(!kiritish_COUNT[egasi_obyekt])return 0;int 반환값=hodisa_Ro_yxat[egasi_obyekt][첫항목[egasi_obyekt]];첫항목[egasi_obyekt]=(첫항목[egasi_obyekt]+1)%16;kiritish_COUNT[egasi_obyekt]--;return 반환값;}
    if(Amal==6)return 화면보임(egasi_obyekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(egasi_obyekt,너비값);
    if(Amal==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||belgi_kodi<1||ko_chirish_joyi_ma_lumotlar<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||belgi_kodi>바탕너비-첫째값||ko_chirish_joyi_ma_lumotlar>바탕높이-SECOND_VALUE)return -22;너비값->x_koordinata=첫째값;너비값->Y_tugmasi_koordinat=SECOND_VALUE;너비값->너비값=belgi_kodi;너비값->높이값=ko_chirish_joyi_ma_lumotlar;너비값->qo_llanma_Maket=1;}
    else if(Amal==2){vidjet_holat *yordamchi_qism=element_VALUE(egasi_obyekt,첫째값);if(!yordamchi_qism||yordamchi_qism==너비값||yordamchi_qism->toifa_VALUE==1)return -22;int ma_lumotlar_holat=identifikator_VALUE;for(int 깊이=0;ma_lumotlar_holat&&깊이<32;깊이++){if(ma_lumotlar_holat==첫째값)return -22;vidjet_holat *위쪽=element_VALUE(egasi_obyekt,ma_lumotlar_holat);ma_lumotlar_holat=위쪽?위쪽->부모항목:0;}yordamchi_qism->부모항목=identifikator_VALUE;if(!yordamchi_qism->qo_llanma_Maket){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[egasi_obyekt][순번]!=yordamchi_qism&&요소들[egasi_obyekt][순번].부모항목==identifikator_VALUE)형제요소++;yordamchi_qism->Y_tugmasi_koordinat=16+형제요소*36;}}
    else if(Amal==3)너비값->보이는지=첫째값!=0;
    else if(Amal==4)너비값->보이는지=0;
    else if(Amal==7)너비값->Maket_siyosat=첫째값;
    else if(Amal==8)return 너비값->uzunlik_VALUE;
    else if(Amal==9)return 첫째값>=0&&(unsigned)첫째값<너비값->uzunlik_VALUE?너비값->Matn[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(egasi_obyekt,너비값))yozuv_taxtasi_Terminal(3);return 0;
}
int 화면글(int egasi_obyekt,int identifikator_VALUE,const uint32_t *ma_lumotlar,unsigned element_COUNT){vidjet_holat *너비값=element_VALUE(egasi_obyekt,identifikator_VALUE);if(!너비값)return -9;if(element_COUNT>127)return -22;for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned belgi_kodlash=ma_lumotlar[순번];if(belgi_kodlash>0x10ffff||(belgi_kodlash>=0xd800&&belgi_kodlash<=0xdfff))return -22;}for(unsigned 순번=0;순번<element_COUNT;순번++)너비값->Matn[순번]=ma_lumotlar[순번];너비값->uzunlik_VALUE=element_COUNT;if(표시됨(egasi_obyekt,너비값))yozuv_taxtasi_Terminal(3);return 0;}
