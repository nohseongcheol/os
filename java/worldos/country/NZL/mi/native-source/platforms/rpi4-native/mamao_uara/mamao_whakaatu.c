/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 TŪHONO, 제한된 입력 roa_uara, 비동기 tuku_uara, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 raraunga 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "mamao_uara.h"
#include "암호기반.h"
#include "Kōtaha.h"
#include "../whatunga_Huinga/whatunga_Huinga.h"
#include "../mīhini/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t papa_Tauranga(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,hoa_uara=-1,atamira_uara,닫을예정;
static uintptr_t hononga_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],wero_uara[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pika_rahi=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned tapa_COUNT,tapa_tūranga,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *raraunga_tūranga){return(unsigned)raraunga_tūranga[0]*256+raraunga_tūranga[1];}
static uint32_t 읽기32(const unsigned char *raraunga_tūranga){return(uint32_t)raraunga_tūranga[0]<<24|(uint32_t)raraunga_tūranga[1]<<16|(uint32_t)raraunga_tūranga[2]<<8|raraunga_tūranga[3];}
static void tuhi_16(unsigned char *raraunga_tūranga,unsigned uara){raraunga_tūranga[0]=uara>>8;raraunga_tūranga[1]=uara;}
static void tuhi_32(unsigned char *raraunga_tūranga,uint32_t uara){raraunga_tūranga[0]=uara>>24;raraunga_tūranga[1]=uara>>16;raraunga_tūranga[2]=uara>>8;raraunga_tūranga[3]=uara;}
static void Kati(void){if(hoa_uara>=0)kati_whatunga(hoa_uara);hoa_uara=-1;atamira_uara=0;입력수=출력수=보낸수=0;tapa_COUNT=tapa_tūranga=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *raraunga,unsigned 수){memcpy(출력,raraunga,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int mana_mamao_whakaatu(unsigned hohenga){
    if(hohenga==0){Kati();if(듣는곳>=0)kati_whatunga(듣는곳);듣는곳=-1;return 0;}
    if(hohenga!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int kawe_uara=통신끝점만들기(1);if(kawe_uara<0)return kawe_uara;통신주소재사용(kawe_uara);
    int mēhua=망주소묶기(kawe_uara,0,5900);if(!mēhua)mēhua=연결기다리기(kawe_uara);
    if(mēhua<0){kati_whatunga(kawe_uara);return mēhua;}듣는곳=kawe_uara;return 0;
}
static uint32_t tapa_whakarāpoto(unsigned 가로,unsigned Poutū_tūranga){
    uint32_t uara=2166136261u;
    for(unsigned 세로좌표=Poutū_tūranga;세로좌표<Poutū_tūranga+16&&세로좌표<높이;세로좌표++)for(unsigned taunga_x=가로;taunga_x<가로+32&&taunga_x<너비;taunga_x++)uara=(uara^보드화면읽기(taunga_x,세로좌표))*16777619u;
    return uara;
}
static void 화면요청(const unsigned char *raraunga_tūranga){
    요청가로=읽기16(raraunga_tūranga+2);요청세로=읽기16(raraunga_tūranga+4);요청폭=읽기16(raraunga_tūranga+6);요청높이=읽기16(raraunga_tūranga+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    tapa_COUNT=tapa_tūranga=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned taunga_x=요청가로/32;taunga_x<=(요청가로+요청폭-1)/32;taunga_x++){
        unsigned tūranga_INDEX=세로좌표*60+taunga_x;uint32_t whakarāpoto_uara=tapa_whakarāpoto(taunga_x*32,세로좌표*16);
        if(!raraunga_tūranga[1]||지난요약[tūranga_INDEX]!=whakarāpoto_uara)바뀐타일[tapa_COUNT++]=tūranga_INDEX;
    }
    출력[0]=출력[1]=0;tuhi_16(출력+2,tapa_COUNT);출력수=4;보낸수=0;
}
static void tuku_tapa(void){
    unsigned tūranga_INDEX=바뀐타일[tapa_tūranga++],가로=(tūranga_INDEX%60)*32,Poutū_tūranga=(tūranga_INDEX/60)*16;
    unsigned 끝가로=가로+32,끝세로=Poutū_tūranga+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Poutū_tūranga>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[tūranga_INDEX]=tapa_whakarāpoto(가로,Poutū_tūranga);
    if(가로<요청가로)가로=요청가로;if(Poutū_tūranga<요청세로)Poutū_tūranga=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    tuhi_16(출력,가로);tuhi_16(출력+2,Poutū_tūranga);tuhi_16(출력+4,끝가로-가로);tuhi_16(출력+6,끝세로-Poutū_tūranga);tuhi_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=Poutū_tūranga;세로좌표<끝세로;세로좌표++)for(unsigned taunga_x=가로;taunga_x<끝가로;taunga_x++){
        uint32_t 색=보드화면읽기(taunga_x,세로좌표),uara=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pika_rahi;순번++)출력[출력수++]=uara>>(8*(큰끝?pika_rahi-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(hoa_uara<0){if(보드밀리초()<다시받을때)return;hoa_uara=망연결받기(듣는곳);if(hoa_uara<0)return;
        hononga_TIME=보드밀리초();atamira_uara=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pika_rahi=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(atamira_uara<5&&보드밀리초()-hononga_TIME>15000){Kati();return;}
    if(출력수){int 수=통신쓰기(hoa_uara,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Kati();return;}}
    if(!출력수&&닫을예정){Kati();return;}
    if(!출력수&&tapa_tūranga<tapa_COUNT)tuku_tapa();
    if(입력수==sizeof(입력)){Kati();return;}
    int RECEIVED_COUNT=통신읽기(hoa_uara,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Kati();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||tapa_tūranga<tapa_COUNT)return;
    if(atamira_uara==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Kati();return;}소비(12);const unsigned char aratuka_motuhēhēnga[]={1,2};내보내기(aratuka_motuhēhēnga,2);atamira_uara=2;return;}
    if(atamira_uara==2&&입력수){if(입력[0]!=2||원격난수(wero_uara,16)){Kati();return;}소비(1);내보내기(wero_uara,16);atamira_uara=3;return;}
    if(atamira_uara==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys kupuhipa_uara;
        for(unsigned 순번=0;순번<8;순번++){unsigned uara=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(uara&1);uara>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&kupuhipa_uara,열쇠,8);memcpy(정답,wero_uara,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char pere_uara[8]={0};br_des_ct_cbcenc_run(&kupuhipa_uara,pere_uara,정답+순번,8);memset(pere_uara,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&kupuhipa_uara,0,sizeof(kupuhipa_uara));memset(열쇠,0,8);memset(정답,0,16);memset(wero_uara,0,16);
        tuhi_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){tuhi_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else atamira_uara=4;return;}
    if(atamira_uara==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Kati();return;}
        if(!papa_Tauranga(7)){const unsigned char hui[]={30,2,1,0,0,0,0};원격입력넣기(hui,7);}
        memset(출력,0,40);tuhi_16(출력,너비);tuhi_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        tuhi_16(출력+8,255);tuhi_16(출력+10,255);tuhi_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Ingoa="jkoros native";tuhi_32(출력+20,strlen(Ingoa));memcpy(출력+24,Ingoa,strlen(Ingoa));출력수=24+strlen(Ingoa);보낸수=0;atamira_uara=5;return;}
    if(atamira_uara!=5||!입력수)return;
    unsigned TYPE_kāwai=입력[0],필요=TYPE_kāwai==0?20:TYPE_kāwai==2?4:TYPE_kāwai==3?10:TYPE_kāwai==4?8:TYPE_kāwai==5?6:TYPE_kāwai==6?8:0;
    if(!필요){Kati();return;}if(입력수<필요)return;
    if(TYPE_kāwai==2){unsigned 수=읽기16(입력+2);if(수>128){Kati();return;}필요+=수*4;}
    if(TYPE_kāwai==6){unsigned 수=읽기32(입력+4);if(수>4096){Kati();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_kāwai==0){unsigned moka_uara=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((moka_uara!=16&&moka_uara!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<moka_uara)-1)||((uint64_t)초<<초이)>((1ull<<moka_uara)-1)||((uint64_t)파<<파이)>((1ull<<moka_uara)-1)){Kati();return;}
        pika_rahi=moka_uara/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_kāwai==3)화면요청(입력);
    else if(TYPE_kāwai==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_kāwai==5){unsigned taunga_x=읽기16(입력+2),세로좌표=읽기16(입력+4);if(taunga_x>=너비)taunga_x=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char hui[]={30,1,입력[1],taunga_x&255,taunga_x>>8,세로좌표&255,세로좌표>>8};원격입력넣기(hui,sizeof(hui));}
    소비(필요);
}
