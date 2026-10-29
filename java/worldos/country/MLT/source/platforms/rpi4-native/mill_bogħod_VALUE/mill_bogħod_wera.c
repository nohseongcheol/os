/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 AQBAD, 제한된 입력 tul_VALUE, 비동기 bagħat_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "mill_bogħod_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../netwerk_Munzell/netwerk_Munzell.h"
#include "../kompjuter/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t bord_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,peer_VALUE=-1,palk_VALUE,닫을예정;
static uintptr_t konnessjoni_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],sfida_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pel_daqqas=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned tajl_COUNT,tajl_pożizzjoni,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_pożizzjoni){return(unsigned)data_pożizzjoni[0]*256+data_pożizzjoni[1];}
static uint32_t 읽기32(const unsigned char *data_pożizzjoni){return(uint32_t)data_pożizzjoni[0]<<24|(uint32_t)data_pożizzjoni[1]<<16|(uint32_t)data_pożizzjoni[2]<<8|data_pożizzjoni[3];}
static void kiteb_16(unsigned char *data_pożizzjoni,unsigned VALUE){data_pożizzjoni[0]=VALUE>>8;data_pożizzjoni[1]=VALUE;}
static void kiteb_32(unsigned char *data_pożizzjoni,uint32_t VALUE){data_pożizzjoni[0]=VALUE>>24;data_pożizzjoni[1]=VALUE>>16;data_pożizzjoni[2]=VALUE>>8;data_pożizzjoni[3]=VALUE;}
static void agħlaq(void){if(peer_VALUE>=0)agħlaq_netwerk(peer_VALUE);peer_VALUE=-1;palk_VALUE=0;입력수=출력수=보낸수=0;tajl_COUNT=tajl_pożizzjoni=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(출력,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int kontroll_mill_bogħod_wera(unsigned azzjoni){
    if(azzjoni==0){agħlaq();if(듣는곳>=0)agħlaq_netwerk(듣는곳);듣는곳=-1;return 0;}
    if(azzjoni!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int miżura=망주소묶기(port_VALUE,0,5900);if(!miżura)miżura=연결기다리기(port_VALUE);
    if(miżura<0){agħlaq_netwerk(port_VALUE);return miżura;}듣는곳=port_VALUE;return 0;
}
static uint32_t tajl_sommarju(unsigned 가로,unsigned Vertikali_pożizzjoni){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=Vertikali_pożizzjoni;세로좌표<Vertikali_pożizzjoni+16&&세로좌표<높이;세로좌표++)for(unsigned koordinat_x=가로;koordinat_x<가로+32&&koordinat_x<너비;koordinat_x++)VALUE=(VALUE^보드화면읽기(koordinat_x,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *data_pożizzjoni){
    요청가로=읽기16(data_pożizzjoni+2);요청세로=읽기16(data_pożizzjoni+4);요청폭=읽기16(data_pożizzjoni+6);요청높이=읽기16(data_pożizzjoni+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    tajl_COUNT=tajl_pożizzjoni=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned koordinat_x=요청가로/32;koordinat_x<=(요청가로+요청폭-1)/32;koordinat_x++){
        unsigned pożizzjoni_INDEX=세로좌표*60+koordinat_x;uint32_t sommarju_VALUE=tajl_sommarju(koordinat_x*32,세로좌표*16);
        if(!data_pożizzjoni[1]||지난요약[pożizzjoni_INDEX]!=sommarju_VALUE)바뀐타일[tajl_COUNT++]=pożizzjoni_INDEX;
    }
    출력[0]=출력[1]=0;kiteb_16(출력+2,tajl_COUNT);출력수=4;보낸수=0;
}
static void bagħat_tajl(void){
    unsigned pożizzjoni_INDEX=바뀐타일[tajl_pożizzjoni++],가로=(pożizzjoni_INDEX%60)*32,Vertikali_pożizzjoni=(pożizzjoni_INDEX/60)*16;
    unsigned 끝가로=가로+32,끝세로=Vertikali_pożizzjoni+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Vertikali_pożizzjoni>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[pożizzjoni_INDEX]=tajl_sommarju(가로,Vertikali_pożizzjoni);
    if(가로<요청가로)가로=요청가로;if(Vertikali_pożizzjoni<요청세로)Vertikali_pożizzjoni=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    kiteb_16(출력,가로);kiteb_16(출력+2,Vertikali_pożizzjoni);kiteb_16(출력+4,끝가로-가로);kiteb_16(출력+6,끝세로-Vertikali_pożizzjoni);kiteb_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=Vertikali_pożizzjoni;세로좌표<끝세로;세로좌표++)for(unsigned koordinat_x=가로;koordinat_x<끝가로;koordinat_x++){
        uint32_t 색=보드화면읽기(koordinat_x,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pel_daqqas;순번++)출력[출력수++]=VALUE>>(8*(큰끝?pel_daqqas-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(peer_VALUE<0){if(보드밀리초()<다시받을때)return;peer_VALUE=망연결받기(듣는곳);if(peer_VALUE<0)return;
        konnessjoni_TIME=보드밀리초();palk_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pel_daqqas=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(palk_VALUE<5&&보드밀리초()-konnessjoni_TIME>15000){agħlaq();return;}
    if(출력수){int 수=통신쓰기(peer_VALUE,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){agħlaq();return;}}
    if(!출력수&&닫을예정){agħlaq();return;}
    if(!출력수&&tajl_pożizzjoni<tajl_COUNT)bagħat_tajl();
    if(입력수==sizeof(입력)){agħlaq();return;}
    int RECEIVED_COUNT=통신읽기(peer_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){agħlaq();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||tajl_pożizzjoni<tajl_COUNT)return;
    if(palk_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){agħlaq();return;}소비(12);const unsigned char metodu_ta_awtentikazzjoni[]={1,2};내보내기(metodu_ta_awtentikazzjoni,2);palk_VALUE=2;return;}
    if(palk_VALUE==2&&입력수){if(입력[0]!=2||원격난수(sfida_VALUE,16)){agħlaq();return;}소비(1);내보내기(sfida_VALUE,16);palk_VALUE=3;return;}
    if(palk_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys password_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&password_VALUE,열쇠,8);memcpy(정답,sfida_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vettur_VALUE[8]={0};br_des_ct_cbcenc_run(&password_VALUE,vettur_VALUE,정답+순번,8);memset(vettur_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&password_VALUE,0,sizeof(password_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(sfida_VALUE,0,16);
        kiteb_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){kiteb_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else palk_VALUE=4;return;}
    if(palk_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){agħlaq();return;}
        if(!bord_Terminal(7)){const unsigned char avveniment[]={30,2,1,0,0,0,0};원격입력넣기(avveniment,7);}
        memset(출력,0,40);kiteb_16(출력,너비);kiteb_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        kiteb_16(출력+8,255);kiteb_16(출력+10,255);kiteb_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *isem="jkoros native";kiteb_32(출력+20,strlen(isem));memcpy(출력+24,isem,strlen(isem));출력수=24+strlen(isem);보낸수=0;palk_VALUE=5;return;}
    if(palk_VALUE!=5||!입력수)return;
    unsigned TYPE_kategorija=입력[0],필요=TYPE_kategorija==0?20:TYPE_kategorija==2?4:TYPE_kategorija==3?10:TYPE_kategorija==4?8:TYPE_kategorija==5?6:TYPE_kategorija==6?8:0;
    if(!필요){agħlaq();return;}if(입력수<필요)return;
    if(TYPE_kategorija==2){unsigned 수=읽기16(입력+2);if(수>128){agħlaq();return;}필요+=수*4;}
    if(TYPE_kategorija==6){unsigned 수=읽기32(입력+4);if(수>4096){agħlaq();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_kategorija==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){agħlaq();return;}
        pel_daqqas=bit_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_kategorija==3)화면요청(입력);
    else if(TYPE_kategorija==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_kategorija==5){unsigned koordinat_x=읽기16(입력+2),세로좌표=읽기16(입력+4);if(koordinat_x>=너비)koordinat_x=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char avveniment[]={30,1,입력[1],koordinat_x&255,koordinat_x>>8,세로좌표&255,세로좌표>>8};원격입력넣기(avveniment,sizeof(avveniment));}
    소비(필요);
}
