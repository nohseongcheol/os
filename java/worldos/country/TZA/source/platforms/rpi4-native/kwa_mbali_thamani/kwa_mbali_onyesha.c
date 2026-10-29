/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 UNGANISHA, 제한된 입력 urefu_thamani, 비동기 tuma_thamani, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "kwa_mbali_thamani.h"
#include "암호기반.h"
#include "Maelezo_mafupi.h"
#include "../Mtandao_Mpororo/Mtandao_Mpororo.h"
#include "../mashine/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t 보드터미널(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,kompyuta_rika_thamani=-1,hatua_thamani,닫을예정;
static uintptr_t muunganisho_saa,다시받을때;
static unsigned char 입력[8192],출력[4096],changamoto_thamani[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,elepi_panga_ukubwa=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned 타일수,타일자리,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *자료위치){return(unsigned)자료위치[0]*256+자료위치[1];}
static uint32_t 읽기32(const unsigned char *자료위치){return(uint32_t)자료위치[0]<<24|(uint32_t)자료위치[1]<<16|(uint32_t)자료위치[2]<<8|자료위치[3];}
static void andika_16(unsigned char *자료위치,unsigned thamani){자료위치[0]=thamani>>8;자료위치[1]=thamani;}
static void andika_32(unsigned char *자료위치,uint32_t thamani){자료위치[0]=thamani>>24;자료위치[1]=thamani>>16;자료위치[2]=thamani>>8;자료위치[3]=thamani;}
static void funga(void){if(kompyuta_rika_thamani>=0)funga_Mtandao(kompyuta_rika_thamani);kompyuta_rika_thamani=-1;hatua_thamani=0;입력수=출력수=보낸수=0;타일수=타일자리=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(출력,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int udhibiti_kwa_mbali_onyesha(unsigned Kitendo){
    if(Kitendo==0){funga();if(듣는곳>=0)funga_Mtandao(듣는곳);듣는곳=-1;return 0;}
    if(Kitendo!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int kituo_thamani=통신끝점만들기(1);if(kituo_thamani<0)return kituo_thamani;통신주소재사용(kituo_thamani);
    int 결과=망주소묶기(kituo_thamani,0,5900);if(!결과)결과=연결기다리기(kituo_thamani);
    if(결과<0){funga_Mtandao(kituo_thamani);return 결과;}듣는곳=kituo_thamani;return 0;
}
static uint32_t kigae_muhtasari(unsigned 가로,unsigned 세로){
    uint32_t thamani=2166136261u;
    for(unsigned Kitufe_cha_Y_kiratibu=세로;Kitufe_cha_Y_kiratibu<세로+16&&Kitufe_cha_Y_kiratibu<높이;Kitufe_cha_Y_kiratibu++)for(unsigned jira_x=가로;jira_x<가로+32&&jira_x<너비;jira_x++)thamani=(thamani^보드화면읽기(jira_x,Kitufe_cha_Y_kiratibu))*16777619u;
    return thamani;
}
static void 화면요청(const unsigned char *자료위치){
    요청가로=읽기16(자료위치+2);요청세로=읽기16(자료위치+4);요청폭=읽기16(자료위치+6);요청높이=읽기16(자료위치+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    타일수=타일자리=0;
    if(요청폭&&요청높이)for(unsigned Kitufe_cha_Y_kiratibu=요청세로/16;Kitufe_cha_Y_kiratibu<=(요청세로+요청높이-1)/16;Kitufe_cha_Y_kiratibu++)for(unsigned jira_x=요청가로/32;jira_x<=(요청가로+요청폭-1)/32;jira_x++){
        unsigned 자리=Kitufe_cha_Y_kiratibu*60+jira_x;uint32_t muhtasari_thamani=kigae_muhtasari(jira_x*32,Kitufe_cha_Y_kiratibu*16);
        if(!자료위치[1]||지난요약[자리]!=muhtasari_thamani)바뀐타일[타일수++]=자리;
    }
    출력[0]=출력[1]=0;andika_16(출력+2,타일수);출력수=4;보낸수=0;
}
static void tuma_kigae(void){
    unsigned 자리=바뀐타일[타일자리++],가로=(자리%60)*32,세로=(자리/60)*16;
    unsigned tamatia_Kitufe_cha_X=가로+32,tamatia_Kitufe_cha_Y=세로+16;if(tamatia_Kitufe_cha_X>너비)tamatia_Kitufe_cha_X=너비;if(tamatia_Kitufe_cha_Y>높이)tamatia_Kitufe_cha_Y=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&세로>=요청세로&&tamatia_Kitufe_cha_X<=요청가로+요청폭&&tamatia_Kitufe_cha_Y<=요청세로+요청높이;
    if(전부)지난요약[자리]=kigae_muhtasari(가로,세로);
    if(가로<요청가로)가로=요청가로;if(세로<요청세로)세로=요청세로;
    if(tamatia_Kitufe_cha_X>요청가로+요청폭)tamatia_Kitufe_cha_X=요청가로+요청폭;if(tamatia_Kitufe_cha_Y>요청세로+요청높이)tamatia_Kitufe_cha_Y=요청세로+요청높이;
    andika_16(출력,가로);andika_16(출력+2,세로);andika_16(출력+4,tamatia_Kitufe_cha_X-가로);andika_16(출력+6,tamatia_Kitufe_cha_Y-세로);andika_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned Kitufe_cha_Y_kiratibu=세로;Kitufe_cha_Y_kiratibu<tamatia_Kitufe_cha_Y;Kitufe_cha_Y_kiratibu++)for(unsigned jira_x=가로;jira_x<tamatia_Kitufe_cha_X;jira_x++){
        uint32_t 색=보드화면읽기(jira_x,Kitufe_cha_Y_kiratibu),thamani=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<elepi_panga_ukubwa;순번++)출력[출력수++]=thamani>>(8*(큰끝?elepi_panga_ukubwa-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(kompyuta_rika_thamani<0){if(보드밀리초()<다시받을때)return;kompyuta_rika_thamani=망연결받기(듣는곳);if(kompyuta_rika_thamani<0)return;
        muunganisho_saa=보드밀리초();hatua_thamani=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        elepi_panga_ukubwa=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(hatua_thamani<5&&보드밀리초()-muunganisho_saa>15000){funga();return;}
    if(출력수){int 수=통신쓰기(kompyuta_rika_thamani,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){funga();return;}}
    if(!출력수&&닫을예정){funga();return;}
    if(!출력수&&타일자리<타일수)tuma_kigae();
    if(입력수==sizeof(입력)){funga();return;}
    int 받은수=통신읽기(kompyuta_rika_thamani,입력+입력수,sizeof(입력)-입력수);
    if(받은수==0||(받은수<0&&받은수!=-11)){funga();return;}if(받은수>0)입력수+=받은수;
    if(출력수||타일자리<타일수)return;
    if(hatua_thamani==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){funga();return;}소비(12);const unsigned char njia_ya_uhalalishaji[]={1,2};내보내기(njia_ya_uhalalishaji,2);hatua_thamani=2;return;}
    if(hatua_thamani==2&&입력수){if(입력[0]!=2||원격난수(changamoto_thamani,16)){funga();return;}소비(1);내보내기(changamoto_thamani,16);hatua_thamani=3;return;}
    if(hatua_thamani==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys nywila_thamani;
        for(unsigned 순번=0;순번<8;순번++){unsigned thamani=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(thamani&1);thamani>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&nywila_thamani,열쇠,8);memcpy(정답,changamoto_thamani,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vekta_thamani[8]={0};br_des_ct_cbcenc_run(&nywila_thamani,vekta_thamani,정답+순번,8);memset(vekta_thamani,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&nywila_thamani,0,sizeof(nywila_thamani));memset(열쇠,0,8);memset(정답,0,16);memset(changamoto_thamani,0,16);
        andika_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){andika_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else hatua_thamani=4;return;}
    if(hatua_thamani==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){funga();return;}
        if(!보드터미널(7)){const unsigned char tukio[]={30,2,1,0,0,0,0};원격입력넣기(tukio,7);}
        memset(출력,0,40);andika_16(출력,너비);andika_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        andika_16(출력+8,255);andika_16(출력+10,255);andika_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Jina="jkoros native";andika_32(출력+20,strlen(Jina));memcpy(출력+24,Jina,strlen(Jina));출력수=24+strlen(Jina);보낸수=0;hatua_thamani=5;return;}
    if(hatua_thamani!=5||!입력수)return;
    unsigned aina_kategoria=입력[0],필요=aina_kategoria==0?20:aina_kategoria==2?4:aina_kategoria==3?10:aina_kategoria==4?8:aina_kategoria==5?6:aina_kategoria==6?8:0;
    if(!필요){funga();return;}if(입력수<필요)return;
    if(aina_kategoria==2){unsigned 수=읽기16(입력+2);if(수>128){funga();return;}필요+=수*4;}
    if(aina_kategoria==6){unsigned 수=읽기32(입력+4);if(수>4096){funga();return;}필요+=수;}
    if(입력수<필요)return;
    if(aina_kategoria==0){unsigned biti_thamani=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((biti_thamani!=16&&biti_thamani!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<biti_thamani)-1)||((uint64_t)초<<초이)>((1ull<<biti_thamani)-1)||((uint64_t)파<<파이)>((1ull<<biti_thamani)-1)){funga();return;}
        elepi_panga_ukubwa=biti_thamani/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(aina_kategoria==3)화면요청(입력);
    else if(aina_kategoria==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(aina_kategoria==5){unsigned jira_x=읽기16(입력+2),Kitufe_cha_Y_kiratibu=읽기16(입력+4);if(jira_x>=너비)jira_x=너비-1;if(Kitufe_cha_Y_kiratibu>=높이)Kitufe_cha_Y_kiratibu=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char tukio[]={30,1,입력[1],jira_x&255,jira_x>>8,Kitufe_cha_Y_kiratibu&255,Kitufe_cha_Y_kiratibu>>8};원격입력넣기(tukio,sizeof(tukio));}
    소비(필요);
}
