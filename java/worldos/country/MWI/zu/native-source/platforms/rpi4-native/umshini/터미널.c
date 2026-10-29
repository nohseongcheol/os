#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 ifasitela 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t umshini_Amagama;
extern umshini_Amagama 보드화소(umshini_Amagama,umshini_Amagama,umshini_Amagama),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,okuxhumanisa_u_x,세로좌표,행위치,열위치,맨위,embula,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 창들[4];
static int Ukugxila=-1,출력결과,ukuhleleka_inani[4],항목수,donsa_inani=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,ideskithophu_buka,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned ikhodi_yohlamvu){return ikhodi_yohlamvu>=256?2:1;}
static void 사각영역(unsigned okuxhumanisa_u_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(okuxhumanisa_u_x,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned okuxhumanisa_u_x,unsigned 세로좌표,unsigned ikhodi_yohlamvu,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(ikhodi_yohlamvu)*8;if(ikhodi_yohlamvu==0xffffffffu)return;
    int 왼쪽=okuxhumanisa_u_x,위쪽=세로좌표,폭=너비,ubude_inani=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&ubude_inani))return;
    if(ikhodi_yohlamvu==' '){보드사각그림(왼쪽,위쪽,폭,ubude_inani,배경색);return;}
    unsigned 색인=ikhodi_yohlamvu<65536?ikhodi_yohlamvu:ikhodi_yohlamvu>=0x1f600&&ikhodi_yohlamvu<0x1f650?65536+ikhodi_yohlamvu-0x1f600:0xfffd;
    const unsigned char *ubuso_bohlamvu_ifonti_inani=터미널글꼴자료+색인*32;
    for(int umugqa=위쪽;umugqa<위쪽+ubude_inani;umugqa++){unsigned 비트들=ubuso_bohlamvu_ifonti_inani[(umugqa-세로좌표)*2]*256+ubuso_bohlamvu_ifonti_inani[(umugqa-세로좌표)*2+1];for(int isikhala_okufakwayo=왼쪽;isikhala_okufakwayo<왼쪽+폭;isikhala_okufakwayo++)보드화소(isikhala_okufakwayo,umugqa,(비트들&(0x8000>>(isikhala_okufakwayo-okuxhumanisa_u_x)))?전경색:배경색);}
}
static void igama_ithebula(unsigned okuxhumanisa_u_x,unsigned 세로좌표,const char *uchunge_imininingwane,unsigned 전경색,unsigned 배경색){while(*uchunge_imininingwane){unsigned ikhodi_yohlamvu=(unsigned char)*uchunge_imininingwane++, 남은수=0;if(ikhodi_yohlamvu>=0xc0){남은수=ikhodi_yohlamvu<0xe0?1:ikhodi_yohlamvu<0xf0?2:3;ikhodi_yohlamvu&=(1u<<(6-남은수))-1;while(남은수--&&*uchunge_imininingwane)ikhodi_yohlamvu=(ikhodi_yohlamvu<<6)|((unsigned char)*uchunge_imininingwane++&63);}터미널글자그림(okuxhumanisa_u_x,세로좌표,ikhodi_yohlamvu,전경색,배경색);okuxhumanisa_u_x+=넓은글자(ikhodi_yohlamvu)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Ukugxila>=0&&터미널항목==&창들[Ukugxila]&&!화면보임(Ukugxila);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->embula||행위치>=첫항목()-터미널항목->embula+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned ikhodi_yohlamvu=터미널항목->글자칸들[행위치%기록줄수][열위치],uchunge_imininingwane=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(ikhodi_yohlamvu)==2&&열위치+1>=터미널항목->열수)ikhodi_yohlamvu=' ';
    터미널글자그림(터미널항목->okuxhumanisa_u_x+12+열위치*8,터미널항목->세로좌표+36+(행위치-첫항목()+터미널항목->embula)*16,ikhodi_yohlamvu?ikhodi_yohlamvu:' ',색상들[uchunge_imininingwane&15],색상들[uchunge_imininingwane>>4]);
}
static void ikharethi_inani(int khombisa_ifasitela){if(!보이는지()||터미널항목->embula||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!khombisa_ifasitela||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->okuxhumanisa_u_x+12+터미널항목->열위치*8,터미널항목->세로좌표+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void Okuqukethwe_inani(void){
    사각영역(터미널항목->okuxhumanisa_u_x+12,터미널항목->세로좌표+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->okuxhumanisa_u_x+12,세로=터미널항목->세로좌표+36,폭=터미널항목->열수*8,ubude_inani=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&ubude_inani)){
    unsigned 첫줄=(세로-터미널항목->세로좌표-36)/16,끝줄=(세로+ubude_inani-터미널항목->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->okuxhumanisa_u_x-12)/8,끝칸=(가로+폭-터미널항목->okuxhumanisa_u_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 isikhala_okufakwayo 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned ikhodi_yohlamvu=첫칸;ikhodi_yohlamvu<끝칸;ikhodi_yohlamvu++){
        unsigned 행위치=첫항목()-터미널항목->embula+반환값,uhlamvusimo_inani=터미널항목->글자칸들[행위치%기록줄수][ikhodi_yohlamvu],uchunge_imininingwane=터미널항목->모양들[행위치%기록줄수][ikhodi_yohlamvu];
        if(넓은글자(uhlamvusimo_inani)==2&&ikhodi_yohlamvu+1>=터미널항목->열수)uhlamvusimo_inani=' ';
        if((uhlamvusimo_inani==0||uhlamvusimo_inani==' ')&&(uchunge_imininingwane>>4)==0)continue;
        터미널글자그림(터미널항목->okuxhumanisa_u_x+12+ikhodi_yohlamvu*8,터미널항목->세로좌표+36+반환값*16,uhlamvusimo_inani?uhlamvusimo_inani:' ',색상들[uchunge_imininingwane&15],색상들[uchunge_imininingwane>>4]);
    }}
    igama_ithebula(터미널항목->okuxhumanisa_u_x+12,터미널항목->세로좌표+터미널항목->높이-18,터미널항목->embula?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);ikharethi_inani(1);
}
static void 실행틀(int isivezi_inani){
    터미널항목=&창들[isivezi_inani];
    int 가로=터미널항목->okuxhumanisa_u_x,세로=터미널항목->세로좌표,폭=터미널항목->너비,ubude_inani=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&ubude_inani))return;
    사각영역(터미널항목->okuxhumanisa_u_x,터미널항목->세로좌표,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=isivezi_inani==Ukugxila?0x905020:0x604438;사각영역(터미널항목->okuxhumanisa_u_x,터미널항목->세로좌표,터미널항목->너비,30,색상);
    igama_ithebula(터미널항목->okuxhumanisa_u_x+12,터미널항목->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+isivezi_inani),0};igama_ithebula(터미널항목->okuxhumanisa_u_x+148,터미널항목->세로좌표+7,수치,0xffffff,색상);
    igama_ithebula(터미널항목->okuxhumanisa_u_x+240,터미널항목->세로좌표+7,터미널항목->너비>=500?(한글입력?"[ZU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[ZU]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->okuxhumanisa_u_x+터미널항목->너비-32,터미널항목->세로좌표+4,26,22,0x5555b8);igama_ithebula(터미널항목->okuxhumanisa_u_x+터미널항목->너비-24,터미널항목->세로좌표+7,"X",0xffffff,0x5555b8);
    Okuqukethwe_inani();
}
static void 장면그리기(void){
    if(!ideskithophu_buka)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);igama_ithebula(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(창들[순번].살아있음){unsigned ikhodi_yohlamvu=Ukugxila==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,ikhodi_yohlamvu);igama_ithebula(160+순번*112,8,"Terminal",0xffffff,ikhodi_yohlamvu);char uchunge_imininingwane[2]={(char)('1'+순번),0};igama_ithebula(232+순번*112,8,uchunge_imininingwane,0xffffff,ikhodi_yohlamvu);}
    if(!항목수)igama_ithebula(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(ukuhleleka_inani[순번]);화면다시그림(Ukugxila);터미널항목=&창들[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int ubude_inani){
    if(!ideskithophu_buka||!보드그림범위(&가로,&세로,&폭,&ubude_inani))return;
    for(int umugqa=세로;umugqa<세로+ubude_inani;umugqa+=32){
        int 띠높이=세로+ubude_inani-umugqa;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,umugqa,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 ifasitela 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int ubude_inani,터미널상태 *ifasitela){
    int 왼쪽=가로>(int)ifasitela->okuxhumanisa_u_x?가로:(int)ifasitela->okuxhumanisa_u_x;
    int 위쪽=세로>(int)ifasitela->세로좌표?세로:(int)ifasitela->세로좌표;
    int 오른쪽=가로+폭<(int)(ifasitela->okuxhumanisa_u_x+ifasitela->너비)?가로+폭:(int)(ifasitela->okuxhumanisa_u_x+ifasitela->너비);
    int 아래쪽=세로+ubude_inani<(int)(ifasitela->세로좌표+ifasitela->높이)?세로+ubude_inani:(int)(ifasitela->세로좌표+ifasitela->높이);
    영역그리기(ifasitela->okuxhumanisa_u_x,ifasitela->세로좌표,ifasitela->너비,ifasitela->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,ubude_inani);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+ubude_inani-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Ukugxila+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Ukugxila>=0){
        터미널상태 *ifasitela_okufakwayo=&창들[Ukugxila];
        igama_ithebula(ifasitela_okufakwayo->okuxhumanisa_u_x+240,ifasitela_okufakwayo->세로좌표+7,ifasitela_okufakwayo->너비>=500?(한글입력?"[ZU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[ZU]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int isivezi_inani){if(isivezi_inani<0||isivezi_inani>=4||!창들[isivezi_inani].살아있음)return;int 현재위치=0;while(현재위치<항목수&&ukuhleleka_inani[현재위치]!=isivezi_inani)현재위치++;for(;현재위치+1<항목수;현재위치++)ukuhleleka_inani[현재위치]=ukuhleleka_inani[현재위치+1];ukuhleleka_inani[항목수-1]=isivezi_inani;Ukugxila=isivezi_inani;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned ikhodi_yohlamvu=0;ikhodi_yohlamvu<최대열수;ikhodi_yohlamvu++){터미널항목->글자칸들[행위치%기록줄수][ikhodi_yohlamvu]=0;터미널항목->모양들[행위치%기록줄수][ikhodi_yohlamvu]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void sula_i_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->embula=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())Okuqukethwe_inani();}
static int yakha_okufakwayo(void){
    if(!보드화면기억공간())return -19;int isivezi_inani=0;while(isivezi_inani<4&&창들[isivezi_inani].살아있음)isivezi_inani++;if(isivezi_inani==4)return -28;
    ideskithophu_buka=1;터미널항목=&창들[isivezi_inani];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->okuxhumanisa_u_x=12+isivezi_inani*16;터미널항목->세로좌표=48+isivezi_inani*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);ukuhleleka_inani[항목수++]=isivezi_inani;Ukugxila=isivezi_inani;대기중|=1u<<(4+isivezi_inani);초점알리기();다시그리기();return isivezi_inani+1;
}
static void vala_ifasitela(int isivezi_inani){
    if(isivezi_inani<0||isivezi_inani>=4||!창들[isivezi_inani].살아있음)return;창들[isivezi_inani].살아있음=0;대기중|=1u<<(8+isivezi_inani);
    int 현재위치=0;while(현재위치<항목수&&ukuhleleka_inani[현재위치]!=isivezi_inani)현재위치++;for(;현재위치+1<항목수;현재위치++)ukuhleleka_inani[현재위치]=ukuhleleka_inani[현재위치+1];항목수--;
    if(Ukugxila==isivezi_inani)Ukugxila=항목수?ukuhleleka_inani[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())Okuqukethwe_inani();}}
static void ikhodi_yohlamvu_451f2815(unsigned ikhodi_yohlamvu){
    if(ikhodi_yohlamvu==13){터미널항목->열위치=0;return;}if(ikhodi_yohlamvu==10){줄바꿈();return;}if(ikhodi_yohlamvu==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(ikhodi_yohlamvu==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)ikhodi_yohlamvu_451f2815(' ');return;}if(ikhodi_yohlamvu<32||ikhodi_yohlamvu==127)return;
    unsigned 너비값=넓은글자(ikhodi_yohlamvu);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=ikhodi_yohlamvu;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void isibambo_isilawuli_UKULANDELANA(unsigned ikhodi_yohlamvu){
    unsigned 개수=터미널항목->매개값[0]?터미널항목->매개값[0]:1;
    if(ikhodi_yohlamvu=='m')for(unsigned 순번=0;순번<=터미널항목->매개색인;순번++){unsigned 자료위치=터미널항목->매개값[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(ikhodi_yohlamvu=='J'&&(터미널항목->매개값[0]==2||터미널항목->매개값[0]==3))sula_i_TOC();
    if(ikhodi_yohlamvu=='K'){unsigned 출발위치=터미널항목->매개값[0]==2?0:터미널항목->열위치,도착위치=터미널항목->매개값[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned umugqa_inani=터미널항목->행위치%기록줄수,uhlamvusimo_inani=터미널항목->글자칸들[umugqa_inani][순번],umumo_inani=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 ubuso_bohlamvu_ifonti_inani 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(uhlamvusimo_inani!=0&&uhlamvusimo_inani!=' ')||터미널항목->모양들[umugqa_inani][순번]!=umumo_inani;
        터미널항목->글자칸들[umugqa_inani][순번]=' ';터미널항목->모양들[umugqa_inani][순번]=umumo_inani;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(ikhodi_yohlamvu=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(ikhodi_yohlamvu=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(ikhodi_yohlamvu=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(ikhodi_yohlamvu=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(ikhodi_yohlamvu=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(ikhodi_yohlamvu=='H'||ikhodi_yohlamvu=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned okuxhumanisa_u_x=터미널항목->매개값[1]?터미널항목->매개값[1]:1;터미널항목->열위치=(okuxhumanisa_u_x>터미널항목->열수?터미널항목->열수:okuxhumanisa_u_x)-1;}
    if(ikhodi_yohlamvu=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(ikhodi_yohlamvu=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((ikhodi_yohlamvu=='h'||ikhodi_yohlamvu=='l')&&터미널항목->매개값[0]==25)터미널항목->가리개보임=ikhodi_yohlamvu=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return;ikharethi_inani(0);if(터미널항목->embula){터미널항목->embula=0;if(보이는지())Okuqukethwe_inani();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->매개색인=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->매개값[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->매개값[터미널항목->매개색인]<10000)터미널항목->매개값[터미널항목->매개색인]=터미널항목->매개값[터미널항목->매개색인]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->매개색인<3)터미널항목->매개색인++;else{isibambo_isilawuli_UKULANDELANA(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;ikhodi_yohlamvu_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)ikhodi_yohlamvu_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)ikhodi_yohlamvu_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else ikhodi_yohlamvu_451f2815(0xfffd);
    }ikharethi_inani(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 thola_inkomba: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ukulinganisa_kabusha_donsa=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int UKULANDELANA_inani=항목수-1;UKULANDELANA_inani>=0;UKULANDELANA_inani--){
        int isivezi_inani=ukuhleleka_inani[UKULANDELANA_inani];터미널상태 *ifasitela=&창들[isivezi_inani];
        if(가로>=(int)ifasitela->okuxhumanisa_u_x&&세로>=(int)ifasitela->세로좌표&&
           가로<(int)(ifasitela->okuxhumanisa_u_x+ifasitela->너비)&&세로<(int)(ifasitela->세로좌표+ifasitela->높이))return isivezi_inani;
    }return -1;
}
static int 모서리찾기(int isivezi_inani,int 가로,int 세로) {
    if(isivezi_inani<0)return 0;터미널상태 *ifasitela=&창들[isivezi_inani];
    int 왼쪽=가로<(int)ifasitela->okuxhumanisa_u_x+8,오른쪽=가로>=(int)(ifasitela->okuxhumanisa_u_x+ifasitela->너비)-8;
    int 위쪽=세로<(int)ifasitela->세로좌표+8,아래쪽=세로>=(int)(ifasitela->세로좌표+ifasitela->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int isihlukanisi_inani(int inani,int 최소,int 최대){return inani<최소?최소:inani>최대?최대:inani;}
static void susa_ukulinganisa_kabusha(int 가로,int 세로) {
    터미널상태 *ifasitela=&창들[ukulinganisa_kabusha_donsa];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=isihlukanisi_inani(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=isihlukanisi_inani(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=isihlukanisi_inani(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=isihlukanisi_inani(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(ifasitela->열수!=열수||ifasitela->행수!=행수){
        ifasitela->크기바뀜=1;ifasitela->열수=열수;ifasitela->행수=행수;
        if(ifasitela->열위치>=열수)ifasitela->열위치=열수-1;
        if(ifasitela->행위치>=ifasitela->맨위+행수)ifasitela->맨위=ifasitela->행위치-행수+1;
        unsigned 한도=ifasitela->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(ifasitela->embula>한도)ifasitela->embula=한도;
    }
    int 옛가로=ifasitela->okuxhumanisa_u_x,옛세로=ifasitela->세로좌표,옛폭=ifasitela->너비,옛길이=ifasitela->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    ifasitela->okuxhumanisa_u_x=왼쪽;ifasitela->세로좌표=위쪽;ifasitela->너비=오른쪽-왼쪽;ifasitela->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,ifasitela);
}
void 터미널가리킴(unsigned 다음,int okuxhumanisa_u_x,int 세로좌표){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!ideskithophu_buka){donsa_inani=-1;ukulinganisa_kabusha_donsa=-1;보드포인터(okuxhumanisa_u_x,세로좌표,1);return;}
    if(!(다음&1)){donsa_inani=-1;ukulinganisa_kabusha_donsa=-1;}
    if(ukulinganisa_kabusha_donsa>=0&&!창들[ukulinganisa_kabusha_donsa].살아있음)ukulinganisa_kabusha_donsa=-1;
    if(donsa_inani>=0&&!창들[donsa_inani].살아있음)donsa_inani=-1;
    if(ukulinganisa_kabusha_donsa>=0){
        susa_ukulinganisa_kabusha(okuxhumanisa_u_x,세로좌표);보드포인터(okuxhumanisa_u_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(okuxhumanisa_u_x,세로좌표,1);
    if(donsa_inani>=0){
        터미널상태 *ifasitela=&창들[donsa_inani];
        int 옛가로=ifasitela->okuxhumanisa_u_x,옛세로=ifasitela->세로좌표;
        ifasitela->okuxhumanisa_u_x=isihlukanisi_inani(okuxhumanisa_u_x-끌기가로,0,보드화면너비()-ifasitela->너비);
        ifasitela->세로좌표=isihlukanisi_inani(세로좌표-끌기세로,34,보드화면높이()-ifasitela->높이);
        if(옛가로!=(int)ifasitela->okuxhumanisa_u_x||옛세로!=(int)ifasitela->세로좌표)창자리그리기(옛가로,옛세로,ifasitela->너비,ifasitela->높이,ifasitela);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Ukugxila,okuxhumanisa_u_x,세로좌표)){화면가리킴(Ukugxila,눌림,okuxhumanisa_u_x,세로좌표);return;}
    int isivezi_inani=가리킨창(okuxhumanisa_u_x,세로좌표),모서리=모서리찾기(isivezi_inani,okuxhumanisa_u_x,세로좌표);
    if(모서리)보드포인터(okuxhumanisa_u_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *ifasitela=&창들[isivezi_inani];ukulinganisa_kabusha_donsa=isivezi_inani;잡은모서리=모서리;잡은가로=okuxhumanisa_u_x;잡은세로=세로좌표;
            처음가로=ifasitela->okuxhumanisa_u_x;처음세로=ifasitela->세로좌표;처음너비=ifasitela->너비;처음높이=ifasitela->높이;
            if(isivezi_inani!=Ukugxila)앞으로올리기(isivezi_inani);return;
        }
        if(세로좌표<32&&okuxhumanisa_u_x>=6&&okuxhumanisa_u_x<142){yakha_okufakwayo();return;}
        if(세로좌표<32&&okuxhumanisa_u_x>=154&&okuxhumanisa_u_x<602){앞으로올리기((okuxhumanisa_u_x-154)/112);return;}
        if(isivezi_inani>=0){
            터미널상태 *ifasitela=&창들[isivezi_inani];
            if(세로좌표<(int)ifasitela->세로좌표+30&&okuxhumanisa_u_x>=(int)(ifasitela->okuxhumanisa_u_x+ifasitela->너비)-32){vala_ifasitela(isivezi_inani);return;}
            if(isivezi_inani!=Ukugxila)앞으로올리기(isivezi_inani);
            if(세로좌표<(int)ifasitela->세로좌표+30){donsa_inani=isivezi_inani;끌기가로=okuxhumanisa_u_x-ifasitela->okuxhumanisa_u_x;끌기세로=세로좌표-ifasitela->세로좌표;}return;
        }
    }
    if(Ukugxila>=0&&(눌림&(8|16))){터미널항목=&창들[Ukugxila];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->embula=터미널항목->embula+9>한도?한도:터미널항목->embula+9;}else 터미널항목->embula=터미널항목->embula<9?0:터미널항목->embula-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)yakha_okufakwayo();if(누름값==2&&항목수)앞으로올리기(ukuhleleka_inani[0]);if(누름값==3)vala_ifasitela(Ukugxila);}
umshini_Amagama 보드터미널(umshini_Amagama Isenzo){
    if(Isenzo==300){if(!창들[출력결과].살아있음)return yakha_okufakwayo();ideskithophu_buka=1;다시그리기();return 0;}
    if(Isenzo==0){vala_ifasitela(Ukugxila);return 0;}if(Isenzo==1)return (uint32_t)yakha_okufakwayo();if(Isenzo==2)return Ukugxila>=0;
    if(Isenzo==9){ideskithophu_buka=0;return 0;}if(Isenzo==7)return 항목수;if(Isenzo==10)return Ukugxila+1;if(Isenzo==11)return 출력결과;
    if(Isenzo==13){터미널상태 *ifasitela=&창들[출력결과];return ifasitela->살아있음?(ifasitela->행수<<16)|ifasitela->열수:(19<<16)|68;}
    if(Isenzo==14){unsigned inani=창들[출력결과].크기바뀜;창들[출력결과].크기바뀜=0;return inani;}
    if(Isenzo==12){unsigned inani=대기중;대기중=0;return inani;}
    if(Isenzo>=20&&Isenzo<24)return 창들[Isenzo-20].살아있음;
    if(Isenzo>=100&&Isenzo<104){출력결과=Isenzo-100;터미널항목=&창들[출력결과];return 0;}
    if(Isenzo>=200&&Isenzo<204){앞으로올리기(Isenzo-200);return 0;}
    if(Isenzo==3){다시그리기();return 0;}터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return 0;
    if(Isenzo==4)sula_i_TOC();if(Isenzo==5||Isenzo==6){unsigned 이전=단추들;터미널가리킴(Isenzo==5?8:16,0,0);단추들=이전;}return 1;
}
