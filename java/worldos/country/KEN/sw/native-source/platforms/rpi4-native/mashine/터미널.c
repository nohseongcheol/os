#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 dirisha 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mashine_Neno;
extern mashine_Neno 보드화소(mashine_Neno,mashine_Neno,mashine_Neno),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,jira_x,Kitufe_cha_Y_kiratibu,행위치,열위치,맨위,biringiza,전경색,배경색,탈출상태,parameta_thamani[4],parameta_kielezo,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 Windows_Orodha[4];
static int Mlengo=-1,출력결과,mpangilio_thamani[4],항목수,kokota_thamani=-1,kokota_Kitufe_cha_X,kokota_Kitufe_cha_Y;
static unsigned teknolojia_ya_maelezo_inayosubiri,단추들,Eneo_kazi_Onesha,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned msimbo_wa_kibambo){return msimbo_wa_kibambo>=256?2:1;}
static void 사각영역(unsigned jira_x,unsigned Kitufe_cha_Y_kiratibu,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(jira_x,Kitufe_cha_Y_kiratibu,너비값,높이값,색상);
}
void 터미널글자그림(unsigned jira_x,unsigned Kitufe_cha_Y_kiratibu,unsigned msimbo_wa_kibambo,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(msimbo_wa_kibambo)*8;if(msimbo_wa_kibambo==0xffffffffu)return;
    int 왼쪽=jira_x,위쪽=Kitufe_cha_Y_kiratibu,폭=너비,urefu_thamani=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&urefu_thamani))return;
    if(msimbo_wa_kibambo==' '){보드사각그림(왼쪽,위쪽,폭,urefu_thamani,배경색);return;}
    unsigned 색인=msimbo_wa_kibambo<65536?msimbo_wa_kibambo:msimbo_wa_kibambo>=0x1f600&&msimbo_wa_kibambo<0x1f650?65536+msimbo_wa_kibambo-0x1f600:0xfffd;
    const unsigned char *fonti_thamani=터미널글꼴자료+색인*32;
    for(int laini=위쪽;laini<위쪽+urefu_thamani;laini++){unsigned Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma_Orodha=fonti_thamani[(laini-Kitufe_cha_Y_kiratibu)*2]*256+fonti_thamani[(laini-Kitufe_cha_Y_kiratibu)*2+1];for(int Sloti_ingizo=왼쪽;Sloti_ingizo<왼쪽+폭;Sloti_ingizo++)보드화소(Sloti_ingizo,laini,(Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma_Orodha&(0x8000>>(Sloti_ingizo-jira_x)))?전경색:배경색);}
}
static void jina_jedwali(unsigned jira_x,unsigned Kitufe_cha_Y_kiratibu,const char *tungo_data,unsigned 전경색,unsigned 배경색){while(*tungo_data){unsigned msimbo_wa_kibambo=(unsigned char)*tungo_data++, 남은수=0;if(msimbo_wa_kibambo>=0xc0){남은수=msimbo_wa_kibambo<0xe0?1:msimbo_wa_kibambo<0xf0?2:3;msimbo_wa_kibambo&=(1u<<(6-남은수))-1;while(남은수--&&*tungo_data)msimbo_wa_kibambo=(msimbo_wa_kibambo<<6)|((unsigned char)*tungo_data++&63);}터미널글자그림(jira_x,Kitufe_cha_Y_kiratibu,msimbo_wa_kibambo,전경색,배경색);jira_x+=넓은글자(msimbo_wa_kibambo)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Mlengo>=0&&터미널항목==&Windows_Orodha[Mlengo]&&!화면보임(Mlengo);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->biringiza||행위치>=첫항목()-터미널항목->biringiza+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned msimbo_wa_kibambo=터미널항목->글자칸들[행위치%기록줄수][열위치],tungo_data=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(msimbo_wa_kibambo)==2&&열위치+1>=터미널항목->열수)msimbo_wa_kibambo=' ';
    터미널글자그림(터미널항목->jira_x+12+열위치*8,터미널항목->Kitufe_cha_Y_kiratibu+36+(행위치-첫항목()+터미널항목->biringiza)*16,msimbo_wa_kibambo?msimbo_wa_kibambo:' ',색상들[tungo_data&15],색상들[tungo_data>>4]);
}
static void kareti_thamani(int onyesha_dirisha){if(!보이는지()||터미널항목->biringiza||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!onyesha_dirisha||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->jira_x+12+터미널항목->열위치*8,터미널항목->Kitufe_cha_Y_kiratibu+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void maudhui_thamani(void){
    사각영역(터미널항목->jira_x+12,터미널항목->Kitufe_cha_Y_kiratibu+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->jira_x+12,세로=터미널항목->Kitufe_cha_Y_kiratibu+36,폭=터미널항목->열수*8,urefu_thamani=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&urefu_thamani)){
    unsigned 첫줄=(세로-터미널항목->Kitufe_cha_Y_kiratibu-36)/16,끝줄=(세로+urefu_thamani-터미널항목->Kitufe_cha_Y_kiratibu-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->jira_x-12)/8,끝칸=(가로+폭-터미널항목->jira_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 Sloti_ingizo 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned msimbo_wa_kibambo=첫칸;msimbo_wa_kibambo<끝칸;msimbo_wa_kibambo++){
        unsigned 행위치=첫항목()-터미널항목->biringiza+반환값,kibambo_thamani=터미널항목->글자칸들[행위치%기록줄수][msimbo_wa_kibambo],tungo_data=터미널항목->모양들[행위치%기록줄수][msimbo_wa_kibambo];
        if(넓은글자(kibambo_thamani)==2&&msimbo_wa_kibambo+1>=터미널항목->열수)kibambo_thamani=' ';
        if((kibambo_thamani==0||kibambo_thamani==' ')&&(tungo_data>>4)==0)continue;
        터미널글자그림(터미널항목->jira_x+12+msimbo_wa_kibambo*8,터미널항목->Kitufe_cha_Y_kiratibu+36+반환값*16,kibambo_thamani?kibambo_thamani:' ',색상들[tungo_data&15],색상들[tungo_data>>4]);
    }}
    jina_jedwali(터미널항목->jira_x+12,터미널항목->Kitufe_cha_Y_kiratibu+터미널항목->높이-18,터미널항목->biringiza?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kareti_thamani(1);
}
static void 실행틀(int kitambulishi_thamani){
    터미널항목=&Windows_Orodha[kitambulishi_thamani];
    int 가로=터미널항목->jira_x,세로=터미널항목->Kitufe_cha_Y_kiratibu,폭=터미널항목->너비,urefu_thamani=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&urefu_thamani))return;
    사각영역(터미널항목->jira_x,터미널항목->Kitufe_cha_Y_kiratibu,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=kitambulishi_thamani==Mlengo?0x905020:0x604438;사각영역(터미널항목->jira_x,터미널항목->Kitufe_cha_Y_kiratibu,터미널항목->너비,30,색상);
    jina_jedwali(터미널항목->jira_x+12,터미널항목->Kitufe_cha_Y_kiratibu+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+kitambulishi_thamani),0};jina_jedwali(터미널항목->jira_x+148,터미널항목->Kitufe_cha_Y_kiratibu+7,수치,0xffffff,색상);
    jina_jedwali(터미널항목->jira_x+240,터미널항목->Kitufe_cha_Y_kiratibu+7,터미널항목->너비>=500?(한글입력?"[SW] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SW]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->jira_x+터미널항목->너비-32,터미널항목->Kitufe_cha_Y_kiratibu+4,26,22,0x5555b8);jina_jedwali(터미널항목->jira_x+터미널항목->너비-24,터미널항목->Kitufe_cha_Y_kiratibu+7,"X",0xffffff,0x5555b8);
    maudhui_thamani();
}
static void 장면그리기(void){
    if(!Eneo_kazi_Onesha)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);jina_jedwali(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Orodha[순번].살아있음){unsigned msimbo_wa_kibambo=Mlengo==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,msimbo_wa_kibambo);jina_jedwali(160+순번*112,8,"Terminal",0xffffff,msimbo_wa_kibambo);char tungo_data[2]={(char)('1'+순번),0};jina_jedwali(232+순번*112,8,tungo_data,0xffffff,msimbo_wa_kibambo);}
    if(!항목수)jina_jedwali(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(mpangilio_thamani[순번]);화면다시그림(Mlengo);터미널항목=&Windows_Orodha[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int urefu_thamani){
    if(!Eneo_kazi_Onesha||!보드그림범위(&가로,&세로,&폭,&urefu_thamani))return;
    for(int laini=세로;laini<세로+urefu_thamani;laini+=32){
        int 띠높이=세로+urefu_thamani-laini;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,laini,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 dirisha 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int urefu_thamani,터미널상태 *dirisha){
    int 왼쪽=가로>(int)dirisha->jira_x?가로:(int)dirisha->jira_x;
    int 위쪽=세로>(int)dirisha->Kitufe_cha_Y_kiratibu?세로:(int)dirisha->Kitufe_cha_Y_kiratibu;
    int 오른쪽=가로+폭<(int)(dirisha->jira_x+dirisha->너비)?가로+폭:(int)(dirisha->jira_x+dirisha->너비);
    int 아래쪽=세로+urefu_thamani<(int)(dirisha->Kitufe_cha_Y_kiratibu+dirisha->높이)?세로+urefu_thamani:(int)(dirisha->Kitufe_cha_Y_kiratibu+dirisha->높이);
    영역그리기(dirisha->jira_x,dirisha->Kitufe_cha_Y_kiratibu,dirisha->너비,dirisha->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,urefu_thamani);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+urefu_thamani-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){teknolojia_ya_maelezo_inayosubiri=(teknolojia_ya_maelezo_inayosubiri&~15u)|(unsigned)(Mlengo+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Mlengo>=0){
        터미널상태 *dirisha_ingizo=&Windows_Orodha[Mlengo];
        jina_jedwali(dirisha_ingizo->jira_x+240,dirisha_ingizo->Kitufe_cha_Y_kiratibu+7,dirisha_ingizo->너비>=500?(한글입력?"[SW] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SW]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int kitambulishi_thamani){if(kitambulishi_thamani<0||kitambulishi_thamani>=4||!Windows_Orodha[kitambulishi_thamani].살아있음)return;int 현재위치=0;while(현재위치<항목수&&mpangilio_thamani[현재위치]!=kitambulishi_thamani)현재위치++;for(;현재위치+1<항목수;현재위치++)mpangilio_thamani[현재위치]=mpangilio_thamani[현재위치+1];mpangilio_thamani[항목수-1]=kitambulishi_thamani;Mlengo=kitambulishi_thamani;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned msimbo_wa_kibambo=0;msimbo_wa_kibambo<최대열수;msimbo_wa_kibambo++){터미널항목->글자칸들[행위치%기록줄수][msimbo_wa_kibambo]=0;터미널항목->모양들[행위치%기록줄수][msimbo_wa_kibambo]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void ondoa_YAL(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->biringiza=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())maudhui_thamani();}
static int unda_ingizo(void){
    if(!보드화면기억공간())return -19;int kitambulishi_thamani=0;while(kitambulishi_thamani<4&&Windows_Orodha[kitambulishi_thamani].살아있음)kitambulishi_thamani++;if(kitambulishi_thamani==4)return -28;
    Eneo_kazi_Onesha=1;터미널항목=&Windows_Orodha[kitambulishi_thamani];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->jira_x=12+kitambulishi_thamani*16;터미널항목->Kitufe_cha_Y_kiratibu=48+kitambulishi_thamani*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);mpangilio_thamani[항목수++]=kitambulishi_thamani;Mlengo=kitambulishi_thamani;teknolojia_ya_maelezo_inayosubiri|=1u<<(4+kitambulishi_thamani);초점알리기();다시그리기();return kitambulishi_thamani+1;
}
static void funga_dirisha(int kitambulishi_thamani){
    if(kitambulishi_thamani<0||kitambulishi_thamani>=4||!Windows_Orodha[kitambulishi_thamani].살아있음)return;Windows_Orodha[kitambulishi_thamani].살아있음=0;teknolojia_ya_maelezo_inayosubiri|=1u<<(8+kitambulishi_thamani);
    int 현재위치=0;while(현재위치<항목수&&mpangilio_thamani[현재위치]!=kitambulishi_thamani)현재위치++;for(;현재위치+1<항목수;현재위치++)mpangilio_thamani[현재위치]=mpangilio_thamani[현재위치+1];항목수--;
    if(Mlengo==kitambulishi_thamani)Mlengo=항목수?mpangilio_thamani[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())maudhui_thamani();}}
static void msimbo_wa_kibambo_451f2815(unsigned msimbo_wa_kibambo){
    if(msimbo_wa_kibambo==13){터미널항목->열위치=0;return;}if(msimbo_wa_kibambo==10){줄바꿈();return;}if(msimbo_wa_kibambo==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(msimbo_wa_kibambo==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)msimbo_wa_kibambo_451f2815(' ');return;}if(msimbo_wa_kibambo<32||msimbo_wa_kibambo==127)return;
    unsigned 너비값=넓은글자(msimbo_wa_kibambo);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=msimbo_wa_kibambo;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void kishiko_udhibiti_MFUATANO(unsigned msimbo_wa_kibambo){
    unsigned 개수=터미널항목->parameta_thamani[0]?터미널항목->parameta_thamani[0]:1;
    if(msimbo_wa_kibambo=='m')for(unsigned 순번=0;순번<=터미널항목->parameta_kielezo;순번++){unsigned 자료위치=터미널항목->parameta_thamani[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(msimbo_wa_kibambo=='J'&&(터미널항목->parameta_thamani[0]==2||터미널항목->parameta_thamani[0]==3))ondoa_YAL();
    if(msimbo_wa_kibambo=='K'){unsigned 출발위치=터미널항목->parameta_thamani[0]==2?0:터미널항목->열위치,도착위치=터미널항목->parameta_thamani[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->parameta_thamani[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned kumbukumbu_thamani=터미널항목->행위치%기록줄수,kibambo_thamani=터미널항목->글자칸들[kumbukumbu_thamani][순번],umbo_thamani=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 fonti_thamani 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(kibambo_thamani!=0&&kibambo_thamani!=' ')||터미널항목->모양들[kumbukumbu_thamani][순번]!=umbo_thamani;
        터미널항목->글자칸들[kumbukumbu_thamani][순번]=' ';터미널항목->모양들[kumbukumbu_thamani][순번]=umbo_thamani;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(msimbo_wa_kibambo=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(msimbo_wa_kibambo=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(msimbo_wa_kibambo=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(msimbo_wa_kibambo=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(msimbo_wa_kibambo=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(msimbo_wa_kibambo=='H'||msimbo_wa_kibambo=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned jira_x=터미널항목->parameta_thamani[1]?터미널항목->parameta_thamani[1]:1;터미널항목->열위치=(jira_x>터미널항목->열수?터미널항목->열수:jira_x)-1;}
    if(msimbo_wa_kibambo=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(msimbo_wa_kibambo=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((msimbo_wa_kibambo=='h'||msimbo_wa_kibambo=='l')&&터미널항목->parameta_thamani[0]==25)터미널항목->가리개보임=msimbo_wa_kibambo=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&Windows_Orodha[출력결과];if(!터미널항목->살아있음)return;kareti_thamani(0);if(터미널항목->biringiza){터미널항목->biringiza=0;if(보이는지())maudhui_thamani();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->parameta_kielezo=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->parameta_thamani[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->parameta_thamani[터미널항목->parameta_kielezo]<10000)터미널항목->parameta_thamani[터미널항목->parameta_kielezo]=터미널항목->parameta_thamani[터미널항목->parameta_kielezo]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->parameta_kielezo<3)터미널항목->parameta_kielezo++;else{kishiko_udhibiti_MFUATANO(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;msimbo_wa_kibambo_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)msimbo_wa_kibambo_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)msimbo_wa_kibambo_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else msimbo_wa_kibambo_451f2815(0xfffd);
    }kareti_thamani(1);
}
int 터미널대기(void){return teknolojia_ya_maelezo_inayosubiri!=0;}
/* 모서리 kielezo: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int badilisha_ukubwa_kokota=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int MFUATANO_thamani=항목수-1;MFUATANO_thamani>=0;MFUATANO_thamani--){
        int kitambulishi_thamani=mpangilio_thamani[MFUATANO_thamani];터미널상태 *dirisha=&Windows_Orodha[kitambulishi_thamani];
        if(가로>=(int)dirisha->jira_x&&세로>=(int)dirisha->Kitufe_cha_Y_kiratibu&&
           가로<(int)(dirisha->jira_x+dirisha->너비)&&세로<(int)(dirisha->Kitufe_cha_Y_kiratibu+dirisha->높이))return kitambulishi_thamani;
    }return -1;
}
static int 모서리찾기(int kitambulishi_thamani,int 가로,int 세로) {
    if(kitambulishi_thamani<0)return 0;터미널상태 *dirisha=&Windows_Orodha[kitambulishi_thamani];
    int 왼쪽=가로<(int)dirisha->jira_x+8,오른쪽=가로>=(int)(dirisha->jira_x+dirisha->너비)-8;
    int 위쪽=세로<(int)dirisha->Kitufe_cha_Y_kiratibu+8,아래쪽=세로>=(int)(dirisha->Kitufe_cha_Y_kiratibu+dirisha->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int kitenganishi_thamani(int thamani,int 최소,int 최대){return thamani<최소?최소:thamani>최대?최대:thamani;}
static void hamisha_badilisha_ukubwa(int 가로,int 세로) {
    터미널상태 *dirisha=&Windows_Orodha[badilisha_ukubwa_kokota];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=kitenganishi_thamani(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=kitenganishi_thamani(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=kitenganishi_thamani(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=kitenganishi_thamani(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(dirisha->열수!=열수||dirisha->행수!=행수){
        dirisha->크기바뀜=1;dirisha->열수=열수;dirisha->행수=행수;
        if(dirisha->열위치>=열수)dirisha->열위치=열수-1;
        if(dirisha->행위치>=dirisha->맨위+행수)dirisha->맨위=dirisha->행위치-행수+1;
        unsigned 한도=dirisha->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(dirisha->biringiza>한도)dirisha->biringiza=한도;
    }
    int 옛가로=dirisha->jira_x,옛세로=dirisha->Kitufe_cha_Y_kiratibu,옛폭=dirisha->너비,옛길이=dirisha->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    dirisha->jira_x=왼쪽;dirisha->Kitufe_cha_Y_kiratibu=위쪽;dirisha->너비=오른쪽-왼쪽;dirisha->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,dirisha);
}
void 터미널가리킴(unsigned 다음,int jira_x,int Kitufe_cha_Y_kiratibu){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!Eneo_kazi_Onesha){kokota_thamani=-1;badilisha_ukubwa_kokota=-1;보드포인터(jira_x,Kitufe_cha_Y_kiratibu,1);return;}
    if(!(다음&1)){kokota_thamani=-1;badilisha_ukubwa_kokota=-1;}
    if(badilisha_ukubwa_kokota>=0&&!Windows_Orodha[badilisha_ukubwa_kokota].살아있음)badilisha_ukubwa_kokota=-1;
    if(kokota_thamani>=0&&!Windows_Orodha[kokota_thamani].살아있음)kokota_thamani=-1;
    if(badilisha_ukubwa_kokota>=0){
        hamisha_badilisha_ukubwa(jira_x,Kitufe_cha_Y_kiratibu);보드포인터(jira_x,Kitufe_cha_Y_kiratibu,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(jira_x,Kitufe_cha_Y_kiratibu,1);
    if(kokota_thamani>=0){
        터미널상태 *dirisha=&Windows_Orodha[kokota_thamani];
        int 옛가로=dirisha->jira_x,옛세로=dirisha->Kitufe_cha_Y_kiratibu;
        dirisha->jira_x=kitenganishi_thamani(jira_x-kokota_Kitufe_cha_X,0,보드화면너비()-dirisha->너비);
        dirisha->Kitufe_cha_Y_kiratibu=kitenganishi_thamani(Kitufe_cha_Y_kiratibu-kokota_Kitufe_cha_Y,34,보드화면높이()-dirisha->높이);
        if(옛가로!=(int)dirisha->jira_x||옛세로!=(int)dirisha->Kitufe_cha_Y_kiratibu)창자리그리기(옛가로,옛세로,dirisha->너비,dirisha->높이,dirisha);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Mlengo,jira_x,Kitufe_cha_Y_kiratibu)){화면가리킴(Mlengo,눌림,jira_x,Kitufe_cha_Y_kiratibu);return;}
    int kitambulishi_thamani=가리킨창(jira_x,Kitufe_cha_Y_kiratibu),모서리=모서리찾기(kitambulishi_thamani,jira_x,Kitufe_cha_Y_kiratibu);
    if(모서리)보드포인터(jira_x,Kitufe_cha_Y_kiratibu,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *dirisha=&Windows_Orodha[kitambulishi_thamani];badilisha_ukubwa_kokota=kitambulishi_thamani;잡은모서리=모서리;잡은가로=jira_x;잡은세로=Kitufe_cha_Y_kiratibu;
            처음가로=dirisha->jira_x;처음세로=dirisha->Kitufe_cha_Y_kiratibu;처음너비=dirisha->너비;처음높이=dirisha->높이;
            if(kitambulishi_thamani!=Mlengo)앞으로올리기(kitambulishi_thamani);return;
        }
        if(Kitufe_cha_Y_kiratibu<32&&jira_x>=6&&jira_x<142){unda_ingizo();return;}
        if(Kitufe_cha_Y_kiratibu<32&&jira_x>=154&&jira_x<602){앞으로올리기((jira_x-154)/112);return;}
        if(kitambulishi_thamani>=0){
            터미널상태 *dirisha=&Windows_Orodha[kitambulishi_thamani];
            if(Kitufe_cha_Y_kiratibu<(int)dirisha->Kitufe_cha_Y_kiratibu+30&&jira_x>=(int)(dirisha->jira_x+dirisha->너비)-32){funga_dirisha(kitambulishi_thamani);return;}
            if(kitambulishi_thamani!=Mlengo)앞으로올리기(kitambulishi_thamani);
            if(Kitufe_cha_Y_kiratibu<(int)dirisha->Kitufe_cha_Y_kiratibu+30){kokota_thamani=kitambulishi_thamani;kokota_Kitufe_cha_X=jira_x-dirisha->jira_x;kokota_Kitufe_cha_Y=Kitufe_cha_Y_kiratibu-dirisha->Kitufe_cha_Y_kiratibu;}return;
        }
    }
    if(Mlengo>=0&&(눌림&(8|16))){터미널항목=&Windows_Orodha[Mlengo];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->biringiza=터미널항목->biringiza+9>한도?한도:터미널항목->biringiza+9;}else 터미널항목->biringiza=터미널항목->biringiza<9?0:터미널항목->biringiza-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)unda_ingizo();if(누름값==2&&항목수)앞으로올리기(mpangilio_thamani[0]);if(누름값==3)funga_dirisha(Mlengo);}
mashine_Neno 보드터미널(mashine_Neno Kitendo){
    if(Kitendo==300){if(!Windows_Orodha[출력결과].살아있음)return unda_ingizo();Eneo_kazi_Onesha=1;다시그리기();return 0;}
    if(Kitendo==0){funga_dirisha(Mlengo);return 0;}if(Kitendo==1)return (uint32_t)unda_ingizo();if(Kitendo==2)return Mlengo>=0;
    if(Kitendo==9){Eneo_kazi_Onesha=0;return 0;}if(Kitendo==7)return 항목수;if(Kitendo==10)return Mlengo+1;if(Kitendo==11)return 출력결과;
    if(Kitendo==13){터미널상태 *dirisha=&Windows_Orodha[출력결과];return dirisha->살아있음?(dirisha->행수<<16)|dirisha->열수:(19<<16)|68;}
    if(Kitendo==14){unsigned thamani=Windows_Orodha[출력결과].크기바뀜;Windows_Orodha[출력결과].크기바뀜=0;return thamani;}
    if(Kitendo==12){unsigned thamani=teknolojia_ya_maelezo_inayosubiri;teknolojia_ya_maelezo_inayosubiri=0;return thamani;}
    if(Kitendo>=20&&Kitendo<24)return Windows_Orodha[Kitendo-20].살아있음;
    if(Kitendo>=100&&Kitendo<104){출력결과=Kitendo-100;터미널항목=&Windows_Orodha[출력결과];return 0;}
    if(Kitendo>=200&&Kitendo<204){앞으로올리기(Kitendo-200);return 0;}
    if(Kitendo==3){다시그리기();return 0;}터미널항목=&Windows_Orodha[출력결과];if(!터미널항목->살아있음)return 0;
    if(Kitendo==4)ondoa_YAL();if(Kitendo==5||Kitendo==6){unsigned 이전=단추들;터미널가리킴(Kitendo==5?8:16,0,0);단추들=이전;}return 1;
}
