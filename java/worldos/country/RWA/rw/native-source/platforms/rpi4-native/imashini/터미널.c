#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 idirishya 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t imashini_Ijambo;
extern imashini_Ijambo 보드화소(imashini_Ijambo,imashini_Ijambo,imashini_Ijambo),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,Ihuza_rya_x,세로좌표,행위치,열위치,맨위,gutembereza,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 창들[4];
static int Irebero=-1,출력결과,umujyo_agaciro[4],항목수,kunyereza_agaciro=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,biro_igaragaza,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned 문자값){return 문자값>=256?2:1;}
static void 사각영역(unsigned Ihuza_rya_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(Ihuza_rya_x,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned Ihuza_rya_x,unsigned 세로좌표,unsigned 문자값,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(문자값)*8;if(문자값==0xffffffffu)return;
    int 왼쪽=Ihuza_rya_x,위쪽=세로좌표,폭=너비,uburebure_agaciro=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&uburebure_agaciro))return;
    if(문자값==' '){보드사각그림(왼쪽,위쪽,폭,uburebure_agaciro,배경색);return;}
    unsigned 색인=문자값<65536?문자값:문자값>=0x1f600&&문자값<0x1f650?65536+문자값-0x1f600:0xfffd;
    const unsigned char *imyandikire_agaciro=터미널글꼴자료+색인*32;
    for(int umurongo=위쪽;umurongo<위쪽+uburebure_agaciro;umurongo++){unsigned 비트들=imyandikire_agaciro[(umurongo-세로좌표)*2]*256+imyandikire_agaciro[(umurongo-세로좌표)*2+1];for(int umwanya_icyinjizwa=왼쪽;umwanya_icyinjizwa<왼쪽+폭;umwanya_icyinjizwa++)보드화소(umwanya_icyinjizwa,umurongo,(비트들&(0x8000>>(umwanya_icyinjizwa-Ihuza_rya_x)))?전경색:배경색);}
}
static void izina_imbonerahamwe(unsigned Ihuza_rya_x,unsigned 세로좌표,const char *igicenteruro_amakurushingiro,unsigned 전경색,unsigned 배경색){while(*igicenteruro_amakurushingiro){unsigned 문자값=(unsigned char)*igicenteruro_amakurushingiro++, 남은수=0;if(문자값>=0xc0){남은수=문자값<0xe0?1:문자값<0xf0?2:3;문자값&=(1u<<(6-남은수))-1;while(남은수--&&*igicenteruro_amakurushingiro)문자값=(문자값<<6)|((unsigned char)*igicenteruro_amakurushingiro++&63);}터미널글자그림(Ihuza_rya_x,세로좌표,문자값,전경색,배경색);Ihuza_rya_x+=넓은글자(문자값)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Irebero>=0&&터미널항목==&창들[Irebero]&&!화면보임(Irebero);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->gutembereza||행위치>=첫항목()-터미널항목->gutembereza+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned 문자값=터미널항목->글자칸들[행위치%기록줄수][열위치],igicenteruro_amakurushingiro=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(문자값)==2&&열위치+1>=터미널항목->열수)문자값=' ';
    터미널글자그림(터미널항목->Ihuza_rya_x+12+열위치*8,터미널항목->세로좌표+36+(행위치-첫항목()+터미널항목->gutembereza)*16,문자값?문자값:' ',색상들[igicenteruro_amakurushingiro&15],색상들[igicenteruro_amakurushingiro>>4]);
}
static void kareti_agaciro(int kugaragaza_idirishya){if(!보이는지()||터미널항목->gutembereza||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!kugaragaza_idirishya||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->Ihuza_rya_x+12+터미널항목->열위치*8,터미널항목->세로좌표+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void Ibirimo_agaciro(void){
    사각영역(터미널항목->Ihuza_rya_x+12,터미널항목->세로좌표+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->Ihuza_rya_x+12,세로=터미널항목->세로좌표+36,폭=터미널항목->열수*8,uburebure_agaciro=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&uburebure_agaciro)){
    unsigned 첫줄=(세로-터미널항목->세로좌표-36)/16,끝줄=(세로+uburebure_agaciro-터미널항목->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->Ihuza_rya_x-12)/8,끝칸=(가로+폭-터미널항목->Ihuza_rya_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 umwanya_icyinjizwa 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned 문자값=첫칸;문자값<끝칸;문자값++){
        unsigned 행위치=첫항목()-터미널항목->gutembereza+반환값,inyuguti_agaciro=터미널항목->글자칸들[행위치%기록줄수][문자값],igicenteruro_amakurushingiro=터미널항목->모양들[행위치%기록줄수][문자값];
        if(넓은글자(inyuguti_agaciro)==2&&문자값+1>=터미널항목->열수)inyuguti_agaciro=' ';
        if((inyuguti_agaciro==0||inyuguti_agaciro==' ')&&(igicenteruro_amakurushingiro>>4)==0)continue;
        터미널글자그림(터미널항목->Ihuza_rya_x+12+문자값*8,터미널항목->세로좌표+36+반환값*16,inyuguti_agaciro?inyuguti_agaciro:' ',색상들[igicenteruro_amakurushingiro&15],색상들[igicenteruro_amakurushingiro>>4]);
    }}
    izina_imbonerahamwe(터미널항목->Ihuza_rya_x+12,터미널항목->세로좌표+터미널항목->높이-18,터미널항목->gutembereza?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kareti_agaciro(1);
}
static void 실행틀(int indanga_agaciro){
    터미널항목=&창들[indanga_agaciro];
    int 가로=터미널항목->Ihuza_rya_x,세로=터미널항목->세로좌표,폭=터미널항목->너비,uburebure_agaciro=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&uburebure_agaciro))return;
    사각영역(터미널항목->Ihuza_rya_x,터미널항목->세로좌표,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=indanga_agaciro==Irebero?0x905020:0x604438;사각영역(터미널항목->Ihuza_rya_x,터미널항목->세로좌표,터미널항목->너비,30,색상);
    izina_imbonerahamwe(터미널항목->Ihuza_rya_x+12,터미널항목->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+indanga_agaciro),0};izina_imbonerahamwe(터미널항목->Ihuza_rya_x+148,터미널항목->세로좌표+7,수치,0xffffff,색상);
    izina_imbonerahamwe(터미널항목->Ihuza_rya_x+240,터미널항목->세로좌표+7,터미널항목->너비>=500?(한글입력?"[RW] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[RW]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->Ihuza_rya_x+터미널항목->너비-32,터미널항목->세로좌표+4,26,22,0x5555b8);izina_imbonerahamwe(터미널항목->Ihuza_rya_x+터미널항목->너비-24,터미널항목->세로좌표+7,"X",0xffffff,0x5555b8);
    Ibirimo_agaciro();
}
static void 장면그리기(void){
    if(!biro_igaragaza)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);izina_imbonerahamwe(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(창들[순번].살아있음){unsigned 문자값=Irebero==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,문자값);izina_imbonerahamwe(160+순번*112,8,"Terminal",0xffffff,문자값);char igicenteruro_amakurushingiro[2]={(char)('1'+순번),0};izina_imbonerahamwe(232+순번*112,8,igicenteruro_amakurushingiro,0xffffff,문자값);}
    if(!항목수)izina_imbonerahamwe(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(umujyo_agaciro[순번]);화면다시그림(Irebero);터미널항목=&창들[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int uburebure_agaciro){
    if(!biro_igaragaza||!보드그림범위(&가로,&세로,&폭,&uburebure_agaciro))return;
    for(int umurongo=세로;umurongo<세로+uburebure_agaciro;umurongo+=32){
        int 띠높이=세로+uburebure_agaciro-umurongo;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,umurongo,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 idirishya 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int uburebure_agaciro,터미널상태 *idirishya){
    int 왼쪽=가로>(int)idirishya->Ihuza_rya_x?가로:(int)idirishya->Ihuza_rya_x;
    int 위쪽=세로>(int)idirishya->세로좌표?세로:(int)idirishya->세로좌표;
    int 오른쪽=가로+폭<(int)(idirishya->Ihuza_rya_x+idirishya->너비)?가로+폭:(int)(idirishya->Ihuza_rya_x+idirishya->너비);
    int 아래쪽=세로+uburebure_agaciro<(int)(idirishya->세로좌표+idirishya->높이)?세로+uburebure_agaciro:(int)(idirishya->세로좌표+idirishya->높이);
    영역그리기(idirishya->Ihuza_rya_x,idirishya->세로좌표,idirishya->너비,idirishya->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,uburebure_agaciro);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+uburebure_agaciro-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Irebero+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Irebero>=0){
        터미널상태 *idirishya_icyinjizwa=&창들[Irebero];
        izina_imbonerahamwe(idirishya_icyinjizwa->Ihuza_rya_x+240,idirishya_icyinjizwa->세로좌표+7,idirishya_icyinjizwa->너비>=500?(한글입력?"[RW] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[RW]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int indanga_agaciro){if(indanga_agaciro<0||indanga_agaciro>=4||!창들[indanga_agaciro].살아있음)return;int 현재위치=0;while(현재위치<항목수&&umujyo_agaciro[현재위치]!=indanga_agaciro)현재위치++;for(;현재위치+1<항목수;현재위치++)umujyo_agaciro[현재위치]=umujyo_agaciro[현재위치+1];umujyo_agaciro[항목수-1]=indanga_agaciro;Irebero=indanga_agaciro;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned 문자값=0;문자값<최대열수;문자값++){터미널항목->글자칸들[행위치%기록줄수][문자값]=0;터미널항목->모양들[행위치%기록줄수][문자값]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void gukuraho_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->gutembereza=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())Ibirimo_agaciro();}
static int kurema_icyinjizwa(void){
    if(!보드화면기억공간())return -19;int indanga_agaciro=0;while(indanga_agaciro<4&&창들[indanga_agaciro].살아있음)indanga_agaciro++;if(indanga_agaciro==4)return -28;
    biro_igaragaza=1;터미널항목=&창들[indanga_agaciro];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->Ihuza_rya_x=12+indanga_agaciro*16;터미널항목->세로좌표=48+indanga_agaciro*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);umujyo_agaciro[항목수++]=indanga_agaciro;Irebero=indanga_agaciro;대기중|=1u<<(4+indanga_agaciro);초점알리기();다시그리기();return indanga_agaciro+1;
}
static void gufunga_idirishya(int indanga_agaciro){
    if(indanga_agaciro<0||indanga_agaciro>=4||!창들[indanga_agaciro].살아있음)return;창들[indanga_agaciro].살아있음=0;대기중|=1u<<(8+indanga_agaciro);
    int 현재위치=0;while(현재위치<항목수&&umujyo_agaciro[현재위치]!=indanga_agaciro)현재위치++;for(;현재위치+1<항목수;현재위치++)umujyo_agaciro[현재위치]=umujyo_agaciro[현재위치+1];항목수--;
    if(Irebero==indanga_agaciro)Irebero=항목수?umujyo_agaciro[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())Ibirimo_agaciro();}}
static void 글자번호(unsigned 문자값){
    if(문자값==13){터미널항목->열위치=0;return;}if(문자값==10){줄바꿈();return;}if(문자값==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(문자값==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)글자번호(' ');return;}if(문자값<32||문자값==127)return;
    unsigned 너비값=넓은글자(문자값);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=문자값;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void umukondo_icunga_URUKURIKIRANE(unsigned 문자값){
    unsigned 개수=터미널항목->매개값[0]?터미널항목->매개값[0]:1;
    if(문자값=='m')for(unsigned 순번=0;순번<=터미널항목->매개색인;순번++){unsigned 자료위치=터미널항목->매개값[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(문자값=='J'&&(터미널항목->매개값[0]==2||터미널항목->매개값[0]==3))gukuraho_TOC();
    if(문자값=='K'){unsigned 출발위치=터미널항목->매개값[0]==2?0:터미널항목->열위치,도착위치=터미널항목->매개값[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned umurongo_agaciro_fc48bc81=터미널항목->행위치%기록줄수,inyuguti_agaciro=터미널항목->글자칸들[umurongo_agaciro_fc48bc81][순번],ishusho_agaciro_f1cd655a=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 imyandikire_agaciro 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(inyuguti_agaciro!=0&&inyuguti_agaciro!=' ')||터미널항목->모양들[umurongo_agaciro_fc48bc81][순번]!=ishusho_agaciro_f1cd655a;
        터미널항목->글자칸들[umurongo_agaciro_fc48bc81][순번]=' ';터미널항목->모양들[umurongo_agaciro_fc48bc81][순번]=ishusho_agaciro_f1cd655a;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(문자값=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(문자값=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(문자값=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(문자값=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(문자값=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(문자값=='H'||문자값=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned Ihuza_rya_x=터미널항목->매개값[1]?터미널항목->매개값[1]:1;터미널항목->열위치=(Ihuza_rya_x>터미널항목->열수?터미널항목->열수:Ihuza_rya_x)-1;}
    if(문자값=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(문자값=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((문자값=='h'||문자값=='l')&&터미널항목->매개값[0]==25)터미널항목->가리개보임=문자값=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return;kareti_agaciro(0);if(터미널항목->gutembereza){터미널항목->gutembereza=0;if(보이는지())Ibirimo_agaciro();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->매개색인=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->매개값[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->매개값[터미널항목->매개색인]<10000)터미널항목->매개값[터미널항목->매개색인]=터미널항목->매개값[터미널항목->매개색인]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->매개색인<3)터미널항목->매개색인++;else{umukondo_icunga_URUKURIKIRANE(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;글자번호(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)글자번호(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)글자번호(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else 글자번호(0xfffd);
    }kareti_agaciro(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 umugerekashakiro: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int guhindura_ingano_kunyereza=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int URUKURIKIRANE_agaciro=항목수-1;URUKURIKIRANE_agaciro>=0;URUKURIKIRANE_agaciro--){
        int indanga_agaciro=umujyo_agaciro[URUKURIKIRANE_agaciro];터미널상태 *idirishya=&창들[indanga_agaciro];
        if(가로>=(int)idirishya->Ihuza_rya_x&&세로>=(int)idirishya->세로좌표&&
           가로<(int)(idirishya->Ihuza_rya_x+idirishya->너비)&&세로<(int)(idirishya->세로좌표+idirishya->높이))return indanga_agaciro;
    }return -1;
}
static int 모서리찾기(int indanga_agaciro,int 가로,int 세로) {
    if(indanga_agaciro<0)return 0;터미널상태 *idirishya=&창들[indanga_agaciro];
    int 왼쪽=가로<(int)idirishya->Ihuza_rya_x+8,오른쪽=가로>=(int)(idirishya->Ihuza_rya_x+idirishya->너비)-8;
    int 위쪽=세로<(int)idirishya->세로좌표+8,아래쪽=세로>=(int)(idirishya->세로좌표+idirishya->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int mutandukanya_agaciro(int agaciro,int 최소,int 최대){return agaciro<최소?최소:agaciro>최대?최대:agaciro;}
static void kwimura_guhindura_ingano(int 가로,int 세로) {
    터미널상태 *idirishya=&창들[guhindura_ingano_kunyereza];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=mutandukanya_agaciro(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=mutandukanya_agaciro(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=mutandukanya_agaciro(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=mutandukanya_agaciro(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(idirishya->열수!=열수||idirishya->행수!=행수){
        idirishya->크기바뀜=1;idirishya->열수=열수;idirishya->행수=행수;
        if(idirishya->열위치>=열수)idirishya->열위치=열수-1;
        if(idirishya->행위치>=idirishya->맨위+행수)idirishya->맨위=idirishya->행위치-행수+1;
        unsigned 한도=idirishya->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(idirishya->gutembereza>한도)idirishya->gutembereza=한도;
    }
    int 옛가로=idirishya->Ihuza_rya_x,옛세로=idirishya->세로좌표,옛폭=idirishya->너비,옛길이=idirishya->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    idirishya->Ihuza_rya_x=왼쪽;idirishya->세로좌표=위쪽;idirishya->너비=오른쪽-왼쪽;idirishya->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,idirishya);
}
void 터미널가리킴(unsigned 다음,int Ihuza_rya_x,int 세로좌표){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!biro_igaragaza){kunyereza_agaciro=-1;guhindura_ingano_kunyereza=-1;보드포인터(Ihuza_rya_x,세로좌표,1);return;}
    if(!(다음&1)){kunyereza_agaciro=-1;guhindura_ingano_kunyereza=-1;}
    if(guhindura_ingano_kunyereza>=0&&!창들[guhindura_ingano_kunyereza].살아있음)guhindura_ingano_kunyereza=-1;
    if(kunyereza_agaciro>=0&&!창들[kunyereza_agaciro].살아있음)kunyereza_agaciro=-1;
    if(guhindura_ingano_kunyereza>=0){
        kwimura_guhindura_ingano(Ihuza_rya_x,세로좌표);보드포인터(Ihuza_rya_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(Ihuza_rya_x,세로좌표,1);
    if(kunyereza_agaciro>=0){
        터미널상태 *idirishya=&창들[kunyereza_agaciro];
        int 옛가로=idirishya->Ihuza_rya_x,옛세로=idirishya->세로좌표;
        idirishya->Ihuza_rya_x=mutandukanya_agaciro(Ihuza_rya_x-끌기가로,0,보드화면너비()-idirishya->너비);
        idirishya->세로좌표=mutandukanya_agaciro(세로좌표-끌기세로,34,보드화면높이()-idirishya->높이);
        if(옛가로!=(int)idirishya->Ihuza_rya_x||옛세로!=(int)idirishya->세로좌표)창자리그리기(옛가로,옛세로,idirishya->너비,idirishya->높이,idirishya);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Irebero,Ihuza_rya_x,세로좌표)){화면가리킴(Irebero,눌림,Ihuza_rya_x,세로좌표);return;}
    int indanga_agaciro=가리킨창(Ihuza_rya_x,세로좌표),모서리=모서리찾기(indanga_agaciro,Ihuza_rya_x,세로좌표);
    if(모서리)보드포인터(Ihuza_rya_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *idirishya=&창들[indanga_agaciro];guhindura_ingano_kunyereza=indanga_agaciro;잡은모서리=모서리;잡은가로=Ihuza_rya_x;잡은세로=세로좌표;
            처음가로=idirishya->Ihuza_rya_x;처음세로=idirishya->세로좌표;처음너비=idirishya->너비;처음높이=idirishya->높이;
            if(indanga_agaciro!=Irebero)앞으로올리기(indanga_agaciro);return;
        }
        if(세로좌표<32&&Ihuza_rya_x>=6&&Ihuza_rya_x<142){kurema_icyinjizwa();return;}
        if(세로좌표<32&&Ihuza_rya_x>=154&&Ihuza_rya_x<602){앞으로올리기((Ihuza_rya_x-154)/112);return;}
        if(indanga_agaciro>=0){
            터미널상태 *idirishya=&창들[indanga_agaciro];
            if(세로좌표<(int)idirishya->세로좌표+30&&Ihuza_rya_x>=(int)(idirishya->Ihuza_rya_x+idirishya->너비)-32){gufunga_idirishya(indanga_agaciro);return;}
            if(indanga_agaciro!=Irebero)앞으로올리기(indanga_agaciro);
            if(세로좌표<(int)idirishya->세로좌표+30){kunyereza_agaciro=indanga_agaciro;끌기가로=Ihuza_rya_x-idirishya->Ihuza_rya_x;끌기세로=세로좌표-idirishya->세로좌표;}return;
        }
    }
    if(Irebero>=0&&(눌림&(8|16))){터미널항목=&창들[Irebero];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->gutembereza=터미널항목->gutembereza+9>한도?한도:터미널항목->gutembereza+9;}else 터미널항목->gutembereza=터미널항목->gutembereza<9?0:터미널항목->gutembereza-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)kurema_icyinjizwa();if(누름값==2&&항목수)앞으로올리기(umujyo_agaciro[0]);if(누름값==3)gufunga_idirishya(Irebero);}
imashini_Ijambo 보드터미널(imashini_Ijambo Igikorwa){
    if(Igikorwa==300){if(!창들[출력결과].살아있음)return kurema_icyinjizwa();biro_igaragaza=1;다시그리기();return 0;}
    if(Igikorwa==0){gufunga_idirishya(Irebero);return 0;}if(Igikorwa==1)return (uint32_t)kurema_icyinjizwa();if(Igikorwa==2)return Irebero>=0;
    if(Igikorwa==9){biro_igaragaza=0;return 0;}if(Igikorwa==7)return 항목수;if(Igikorwa==10)return Irebero+1;if(Igikorwa==11)return 출력결과;
    if(Igikorwa==13){터미널상태 *idirishya=&창들[출력결과];return idirishya->살아있음?(idirishya->행수<<16)|idirishya->열수:(19<<16)|68;}
    if(Igikorwa==14){unsigned agaciro=창들[출력결과].크기바뀜;창들[출력결과].크기바뀜=0;return agaciro;}
    if(Igikorwa==12){unsigned agaciro=대기중;대기중=0;return agaciro;}
    if(Igikorwa>=20&&Igikorwa<24)return 창들[Igikorwa-20].살아있음;
    if(Igikorwa>=100&&Igikorwa<104){출력결과=Igikorwa-100;터미널항목=&창들[출력결과];return 0;}
    if(Igikorwa>=200&&Igikorwa<204){앞으로올리기(Igikorwa-200);return 0;}
    if(Igikorwa==3){다시그리기();return 0;}터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return 0;
    if(Igikorwa==4)gukuraho_TOC();if(Igikorwa==5||Igikorwa==6){unsigned 이전=단추들;터미널가리킴(Igikorwa==5?8:16,0,0);단추들=이전;}return 1;
}
