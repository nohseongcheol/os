#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int otu_valuu_4b6d6445,부모항목,ngakọrịta_x,세로좌표,너비값,높이값,보이는지,nke_eji_aka_mèe_Nhàzi,Nhàzi_iwuikikere;unsigned SMS[128],ogologo_valuu; } ngwa_nkepụta_ọnọdụ;
static ngwa_nkepụta_ọnọdụ 요소들[4][32];
static int Mgbadoanya_f7e69dab[4],mmèrème_ndepụta[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void mmèrème(int nwe_ihe,int valuu){if(항목수[nwe_ihe]<16){mmèrème_ndepụta[nwe_ihe][(첫항목[nwe_ihe]+항목수[nwe_ihe])%16]=valuu;항목수[nwe_ihe]++;}}
static ngwa_nkepụta_ọnọdụ *njìmebe_valuu(int nwe_ihe,int ihe_nkọwapụta_valuu){return nwe_ihe>=0&&nwe_ihe<4&&ihe_nkọwapụta_valuu>0&&ihe_nkọwapụta_valuu<=32&&요소들[nwe_ihe][ihe_nkọwapụta_valuu-1].otu_valuu_4b6d6445?&요소들[nwe_ihe][ihe_nkọwapụta_valuu-1]:0;}
static void 사각영역(int ngakọrịta_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(ngakọrịta_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int nwe_ihe){if(nwe_ihe<0||nwe_ihe>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[nwe_ihe][순번].otu_valuu_4b6d6445==1&&요소들[nwe_ihe][순번].보이는지)return 1;return 0;}
void 화면초기화(int nwe_ihe){memset(요소들[nwe_ihe],0,sizeof(요소들[nwe_ihe]));항목수[nwe_ihe]=첫항목[nwe_ihe]=Mgbadoanya_f7e69dab[nwe_ihe]=긴부호없는값[nwe_ihe]=0;}
static void 위치(int nwe_ihe,ngwa_nkepụta_ọnọdụ *너비값,int *ngakọrịta_x,int *세로좌표){*ngakọrịta_x=너비값->ngakọrịta_x;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){ngwa_nkepụta_ọnọdụ *위쪽=njìmebe_valuu(nwe_ihe,자료위치);if(!위쪽)break;*ngakọrịta_x+=위쪽->ngakọrịta_x;*세로좌표+=위쪽->세로좌표+(위쪽->otu_valuu_4b6d6445==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int nwe_ihe,ngwa_nkepụta_ọnọdụ *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->otu_valuu_4b6d6445==1)return 1;너비값=njìmebe_valuu(nwe_ihe,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int ngakọrịta_x,int 세로좌표,ngwa_nkepụta_ọnọdụ *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->ogologo_valuu;순번++){unsigned mkpụrụedemede_ntinye_koòdù=너비값->SMS[순번],너비=mkpụrụedemede_ntinye_koòdù>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(ngakọrịta_x+현재위치,세로좌표,mkpụrụedemede_ntinye_koòdù,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int nwe_ihe){
    if(!화면보임(nwe_ihe))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        ngwa_nkepụta_ọnọdụ *너비값=&요소들[nwe_ihe][순번];if(너비값->otu_valuu_4b6d6445!=처리차례||!표시됨(nwe_ihe,너비값))continue;int ngakọrịta_x,세로좌표;위치(nwe_ihe,너비값,&ngakọrịta_x,&세로좌표);
        if(처리차례==1){사각영역(ngakọrịta_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(ngakọrịta_x,세로좌표,너비값->너비값,30,0x905020);SMS(ngakọrịta_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(ngakọrịta_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(ngakọrịta_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(ngakọrịta_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(ngakọrịta_x,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(ngakọrịta_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Mgbadoanya_f7e69dab[nwe_ihe]==순번+1)사각영역(ngakọrịta_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int nwe_ihe,int ngakọrịta_x,int 세로좌표){
    if(!화면보임(nwe_ihe))return 0;
    for(int 순번=0;순번<32;순번++){
        ngwa_nkepụta_ọnọdụ *windò=&요소들[nwe_ihe][순번];
        if(windò->otu_valuu_4b6d6445==1&&windò->보이는지&&ngakọrịta_x>=windò->ngakọrịta_x&&세로좌표>=windò->세로좌표&&
           ngakọrịta_x<windò->ngakọrịta_x+windò->너비값&&세로좌표<windò->세로좌표+windò->높이값)return 1;
    }return 0;
}
int 화면가리킴(int nwe_ihe,unsigned 눌림,int ngakọrịta_x,int 세로좌표){
    if(!화면보임(nwe_ihe))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){ngwa_nkepụta_ọnọdụ *너비값=&요소들[nwe_ihe][순번];if(!너비값->otu_valuu_4b6d6445||!표시됨(nwe_ihe,너비값))continue;int 창가로,창세로;위치(nwe_ihe,너비값,&창가로,&창세로);
        if(ngakọrịta_x<창가로||세로좌표<창세로||ngakọrịta_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->otu_valuu_4b6d6445==1&&세로좌표<창세로+30&&ngakọrịta_x>=창가로+너비값->너비값-28){if(너비값->Nhàzi_iwuikikere!=0)너비값->보이는지=0;mmèrème(nwe_ihe,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->otu_valuu_4b6d6445==4){mmèrème(nwe_ihe,순번+1);return 1;}if(너비값->otu_valuu_4b6d6445==5){Mgbadoanya_f7e69dab[nwe_ihe]=순번+1;보드터미널(3);return 1;}
        if(너비값->otu_valuu_4b6d6445==1)return 1;
    }return 0;
}
void 화면누름(int nwe_ihe,unsigned 둘째값){
    ngwa_nkepụta_ọnọdụ *너비값=njìmebe_valuu(nwe_ihe,Mgbadoanya_f7e69dab[nwe_ihe]);if(!너비값||너비값->otu_valuu_4b6d6445!=5)return;
    if(둘째값==13||둘째값==10){mmèrème(nwe_ihe,Mgbadoanya_f7e69dab[nwe_ihe]);return;}
    if(둘째값==8||둘째값==127){if(너비값->ogologo_valuu)너비값->ogologo_valuu--;긴부호없는값[nwe_ihe]=0;}
    else{
        unsigned mkpụrụedemede_ntinye_koòdù=둘째값;
        if(긴부호없는값[nwe_ihe]){if((둘째값&192)!=128){긴부호없는값[nwe_ihe]=0;return;}부호없는결과[nwe_ihe]=(부호없는결과[nwe_ihe]<<6)|(둘째값&63);if(--긴부호없는값[nwe_ihe])return;mkpụrụedemede_ntinye_koòdù=부호없는결과[nwe_ihe];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[nwe_ihe]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[nwe_ihe]=둘째값&((1u<<(6-긴부호없는값[nwe_ihe]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(mkpụrụedemede_ntinye_koòdù>0x10ffff||(mkpụrụedemede_ntinye_koòdù>=0xd800&&mkpụrụedemede_ntinye_koòdù<=0xdfff))return;if(너비값->ogologo_valuu<127)너비값->SMS[너비값->ogologo_valuu++]=mkpụrụedemede_ntinye_koòdù;
    }
    보드터미널(3);
}
int 화면호출(int nwe_ihe,unsigned mmèm,int ihe_nkọwapụta_valuu,int 첫째값,int 둘째값,int koòdù_nkeakàrà,int ebemwèga_datà){
    if(nwe_ihe<0||nwe_ihe>=4)return -22;ngwa_nkepụta_ọnọdụ *너비값=njìmebe_valuu(nwe_ihe,ihe_nkọwapụta_valuu);
    if(mmèm==0){if(ihe_nkọwapụta_valuu<1||ihe_nkọwapụta_valuu>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[nwe_ihe][순번].otu_valuu_4b6d6445==0){너비값=&요소들[nwe_ihe][순번];memset(너비값,0,sizeof(*너비값));너비값->otu_valuu_4b6d6445=ihe_nkọwapụta_valuu;너비값->보이는지=ihe_nkọwapụta_valuu!=1;너비값->너비값=ihe_nkọwapụta_valuu==1?380:220;너비값->높이값=ihe_nkọwapụta_valuu==1?240:28;너비값->Nhàzi_iwuikikere=1;너비값->ngakọrịta_x=ihe_nkọwapụta_valuu==1?130:16;너비값->세로좌표=ihe_nkọwapụta_valuu==1?110:16;return 순번+1;}return -28;}
    if(mmèm==5){if(!항목수[nwe_ihe])return 0;int 반환값=mmèrème_ndepụta[nwe_ihe][첫항목[nwe_ihe]];첫항목[nwe_ihe]=(첫항목[nwe_ihe]+1)%16;항목수[nwe_ihe]--;return 반환값;}
    if(mmèm==6)return 화면보임(nwe_ihe);
    if(!너비값)return -9;
    int 이전표시=표시됨(nwe_ihe,너비값);
    if(mmèm==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||koòdù_nkeakàrà<1||ebemwèga_datà<1||첫째값>바탕너비||둘째값>바탕높이||koòdù_nkeakàrà>바탕너비-첫째값||ebemwèga_datà>바탕높이-둘째값)return -22;너비값->ngakọrịta_x=첫째값;너비값->세로좌표=둘째값;너비값->너비값=koòdù_nkeakàrà;너비값->높이값=ebemwèga_datà;너비값->nke_eji_aka_mèe_Nhàzi=1;}
    else if(mmèm==2){ngwa_nkepụta_ọnọdụ *njìmebe_nnwā=njìmebe_valuu(nwe_ihe,첫째값);if(!njìmebe_nnwā||njìmebe_nnwā==너비값||njìmebe_nnwā->otu_valuu_4b6d6445==1)return -22;int 자료위치=ihe_nkọwapụta_valuu;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;ngwa_nkepụta_ọnọdụ *위쪽=njìmebe_valuu(nwe_ihe,자료위치);자료위치=위쪽?위쪽->부모항목:0;}njìmebe_nnwā->부모항목=ihe_nkọwapụta_valuu;if(!njìmebe_nnwā->nke_eji_aka_mèe_Nhàzi){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[nwe_ihe][순번]!=njìmebe_nnwā&&요소들[nwe_ihe][순번].부모항목==ihe_nkọwapụta_valuu)형제요소++;njìmebe_nnwā->세로좌표=16+형제요소*36;}}
    else if(mmèm==3)너비값->보이는지=첫째값!=0;
    else if(mmèm==4)너비값->보이는지=0;
    else if(mmèm==7)너비값->Nhàzi_iwuikikere=첫째값;
    else if(mmèm==8)return 너비값->ogologo_valuu;
    else if(mmèm==9)return 첫째값>=0&&(unsigned)첫째값<너비값->ogologo_valuu?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(nwe_ihe,너비값))보드터미널(3);return 0;
}
int 화면글(int nwe_ihe,int ihe_nkọwapụta_valuu,const uint32_t *datà,unsigned 개수){ngwa_nkepụta_ọnọdụ *너비값=njìmebe_valuu(nwe_ihe,ihe_nkọwapụta_valuu);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned mkpụrụedemede_ntinye_koòdù=datà[순번];if(mkpụrụedemede_ntinye_koòdù>0x10ffff||(mkpụrụedemede_ntinye_koòdù>=0xd800&&mkpụrụedemede_ntinye_koòdù<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->SMS[순번]=datà[순번];너비값->ogologo_valuu=개수;if(표시됨(nwe_ihe,너비값))보드터미널(3);return 0;}
