#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int icyiciro_agaciro,부모항목,Ihuza_rya_x,세로좌표,너비값,높이값,보이는지,n_intoki_Imimerere,Imimerere_ingamba;unsigned Umwandiko[128],uburebure_agaciro; } wijeti_imimerere;
static wijeti_imimerere 요소들[4][32];
static int Kihariye[4],icyabaye_Urutonde[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void icyabaye(int nyirayo_ikintu,int agaciro){if(항목수[nyirayo_ikintu]<16){icyabaye_Urutonde[nyirayo_ikintu][(첫항목[nyirayo_ikintu]+항목수[nyirayo_ikintu])%16]=agaciro;항목수[nyirayo_ikintu]++;}}
static wijeti_imimerere *ikintu_agaciro(int nyirayo_ikintu,int indanga_agaciro){return nyirayo_ikintu>=0&&nyirayo_ikintu<4&&indanga_agaciro>0&&indanga_agaciro<=32&&요소들[nyirayo_ikintu][indanga_agaciro-1].icyiciro_agaciro?&요소들[nyirayo_ikintu][indanga_agaciro-1]:0;}
static void 사각영역(int Ihuza_rya_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(Ihuza_rya_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int nyirayo_ikintu){if(nyirayo_ikintu<0||nyirayo_ikintu>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[nyirayo_ikintu][순번].icyiciro_agaciro==1&&요소들[nyirayo_ikintu][순번].보이는지)return 1;return 0;}
void 화면초기화(int nyirayo_ikintu){memset(요소들[nyirayo_ikintu],0,sizeof(요소들[nyirayo_ikintu]));항목수[nyirayo_ikintu]=첫항목[nyirayo_ikintu]=Kihariye[nyirayo_ikintu]=긴부호없는값[nyirayo_ikintu]=0;}
static void 위치(int nyirayo_ikintu,wijeti_imimerere *너비값,int *Ihuza_rya_x,int *세로좌표){*Ihuza_rya_x=너비값->Ihuza_rya_x;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){wijeti_imimerere *위쪽=ikintu_agaciro(nyirayo_ikintu,자료위치);if(!위쪽)break;*Ihuza_rya_x+=위쪽->Ihuza_rya_x;*세로좌표+=위쪽->세로좌표+(위쪽->icyiciro_agaciro==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int nyirayo_ikintu,wijeti_imimerere *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->icyiciro_agaciro==1)return 1;너비값=ikintu_agaciro(nyirayo_ikintu,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Umwandiko(int Ihuza_rya_x,int 세로좌표,wijeti_imimerere *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->uburebure_agaciro;순번++){unsigned inyuguti_gusobeka=너비값->Umwandiko[순번],너비=inyuguti_gusobeka>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(Ihuza_rya_x+현재위치,세로좌표,inyuguti_gusobeka,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int nyirayo_ikintu){
    if(!화면보임(nyirayo_ikintu))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        wijeti_imimerere *너비값=&요소들[nyirayo_ikintu][순번];if(너비값->icyiciro_agaciro!=처리차례||!표시됨(nyirayo_ikintu,너비값))continue;int Ihuza_rya_x,세로좌표;위치(nyirayo_ikintu,너비값,&Ihuza_rya_x,&세로좌표);
        if(처리차례==1){사각영역(Ihuza_rya_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(Ihuza_rya_x,세로좌표,너비값->너비값,30,0x905020);Umwandiko(Ihuza_rya_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(Ihuza_rya_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(Ihuza_rya_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(Ihuza_rya_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(Ihuza_rya_x,세로좌표,너비값->너비값,너비값->높이값,배경색);Umwandiko(Ihuza_rya_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Kihariye[nyirayo_ikintu]==순번+1)사각영역(Ihuza_rya_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int nyirayo_ikintu,int Ihuza_rya_x,int 세로좌표){
    if(!화면보임(nyirayo_ikintu))return 0;
    for(int 순번=0;순번<32;순번++){
        wijeti_imimerere *idirishya=&요소들[nyirayo_ikintu][순번];
        if(idirishya->icyiciro_agaciro==1&&idirishya->보이는지&&Ihuza_rya_x>=idirishya->Ihuza_rya_x&&세로좌표>=idirishya->세로좌표&&
           Ihuza_rya_x<idirishya->Ihuza_rya_x+idirishya->너비값&&세로좌표<idirishya->세로좌표+idirishya->높이값)return 1;
    }return 0;
}
int 화면가리킴(int nyirayo_ikintu,unsigned 눌림,int Ihuza_rya_x,int 세로좌표){
    if(!화면보임(nyirayo_ikintu))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){wijeti_imimerere *너비값=&요소들[nyirayo_ikintu][순번];if(!너비값->icyiciro_agaciro||!표시됨(nyirayo_ikintu,너비값))continue;int 창가로,창세로;위치(nyirayo_ikintu,너비값,&창가로,&창세로);
        if(Ihuza_rya_x<창가로||세로좌표<창세로||Ihuza_rya_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->icyiciro_agaciro==1&&세로좌표<창세로+30&&Ihuza_rya_x>=창가로+너비값->너비값-28){if(너비값->Imimerere_ingamba!=0)너비값->보이는지=0;icyabaye(nyirayo_ikintu,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->icyiciro_agaciro==4){icyabaye(nyirayo_ikintu,순번+1);return 1;}if(너비값->icyiciro_agaciro==5){Kihariye[nyirayo_ikintu]=순번+1;보드터미널(3);return 1;}
        if(너비값->icyiciro_agaciro==1)return 1;
    }return 0;
}
void 화면누름(int nyirayo_ikintu,unsigned 둘째값){
    wijeti_imimerere *너비값=ikintu_agaciro(nyirayo_ikintu,Kihariye[nyirayo_ikintu]);if(!너비값||너비값->icyiciro_agaciro!=5)return;
    if(둘째값==13||둘째값==10){icyabaye(nyirayo_ikintu,Kihariye[nyirayo_ikintu]);return;}
    if(둘째값==8||둘째값==127){if(너비값->uburebure_agaciro)너비값->uburebure_agaciro--;긴부호없는값[nyirayo_ikintu]=0;}
    else{
        unsigned inyuguti_gusobeka=둘째값;
        if(긴부호없는값[nyirayo_ikintu]){if((둘째값&192)!=128){긴부호없는값[nyirayo_ikintu]=0;return;}부호없는결과[nyirayo_ikintu]=(부호없는결과[nyirayo_ikintu]<<6)|(둘째값&63);if(--긴부호없는값[nyirayo_ikintu])return;inyuguti_gusobeka=부호없는결과[nyirayo_ikintu];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[nyirayo_ikintu]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[nyirayo_ikintu]=둘째값&((1u<<(6-긴부호없는값[nyirayo_ikintu]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(inyuguti_gusobeka>0x10ffff||(inyuguti_gusobeka>=0xd800&&inyuguti_gusobeka<=0xdfff))return;if(너비값->uburebure_agaciro<127)너비값->Umwandiko[너비값->uburebure_agaciro++]=inyuguti_gusobeka;
    }
    보드터미널(3);
}
int 화면호출(int nyirayo_ikintu,unsigned Igikorwa,int indanga_agaciro,int 첫째값,int 둘째값,int 문자값,int aho_ijya_amakurushingiro){
    if(nyirayo_ikintu<0||nyirayo_ikintu>=4)return -22;wijeti_imimerere *너비값=ikintu_agaciro(nyirayo_ikintu,indanga_agaciro);
    if(Igikorwa==0){if(indanga_agaciro<1||indanga_agaciro>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[nyirayo_ikintu][순번].icyiciro_agaciro==0){너비값=&요소들[nyirayo_ikintu][순번];memset(너비값,0,sizeof(*너비값));너비값->icyiciro_agaciro=indanga_agaciro;너비값->보이는지=indanga_agaciro!=1;너비값->너비값=indanga_agaciro==1?380:220;너비값->높이값=indanga_agaciro==1?240:28;너비값->Imimerere_ingamba=1;너비값->Ihuza_rya_x=indanga_agaciro==1?130:16;너비값->세로좌표=indanga_agaciro==1?110:16;return 순번+1;}return -28;}
    if(Igikorwa==5){if(!항목수[nyirayo_ikintu])return 0;int 반환값=icyabaye_Urutonde[nyirayo_ikintu][첫항목[nyirayo_ikintu]];첫항목[nyirayo_ikintu]=(첫항목[nyirayo_ikintu]+1)%16;항목수[nyirayo_ikintu]--;return 반환값;}
    if(Igikorwa==6)return 화면보임(nyirayo_ikintu);
    if(!너비값)return -9;
    int 이전표시=표시됨(nyirayo_ikintu,너비값);
    if(Igikorwa==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||문자값<1||aho_ijya_amakurushingiro<1||첫째값>바탕너비||둘째값>바탕높이||문자값>바탕너비-첫째값||aho_ijya_amakurushingiro>바탕높이-둘째값)return -22;너비값->Ihuza_rya_x=첫째값;너비값->세로좌표=둘째값;너비값->너비값=문자값;너비값->높이값=aho_ijya_amakurushingiro;너비값->n_intoki_Imimerere=1;}
    else if(Igikorwa==2){wijeti_imimerere *ishami_999eb3de=ikintu_agaciro(nyirayo_ikintu,첫째값);if(!ishami_999eb3de||ishami_999eb3de==너비값||ishami_999eb3de->icyiciro_agaciro==1)return -22;int 자료위치=indanga_agaciro;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;wijeti_imimerere *위쪽=ikintu_agaciro(nyirayo_ikintu,자료위치);자료위치=위쪽?위쪽->부모항목:0;}ishami_999eb3de->부모항목=indanga_agaciro;if(!ishami_999eb3de->n_intoki_Imimerere){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[nyirayo_ikintu][순번]!=ishami_999eb3de&&요소들[nyirayo_ikintu][순번].부모항목==indanga_agaciro)형제요소++;ishami_999eb3de->세로좌표=16+형제요소*36;}}
    else if(Igikorwa==3)너비값->보이는지=첫째값!=0;
    else if(Igikorwa==4)너비값->보이는지=0;
    else if(Igikorwa==7)너비값->Imimerere_ingamba=첫째값;
    else if(Igikorwa==8)return 너비값->uburebure_agaciro;
    else if(Igikorwa==9)return 첫째값>=0&&(unsigned)첫째값<너비값->uburebure_agaciro?너비값->Umwandiko[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(nyirayo_ikintu,너비값))보드터미널(3);return 0;
}
int 화면글(int nyirayo_ikintu,int indanga_agaciro,const uint32_t *amakurushingiro,unsigned 개수){wijeti_imimerere *너비값=ikintu_agaciro(nyirayo_ikintu,indanga_agaciro);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned inyuguti_gusobeka=amakurushingiro[순번];if(inyuguti_gusobeka>0x10ffff||(inyuguti_gusobeka>=0xd800&&inyuguti_gusobeka<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->Umwandiko[순번]=amakurushingiro[순번];너비값->uburebure_agaciro=개수;if(표시됨(nyirayo_ikintu,너비값))보드터미널(3);return 0;}
