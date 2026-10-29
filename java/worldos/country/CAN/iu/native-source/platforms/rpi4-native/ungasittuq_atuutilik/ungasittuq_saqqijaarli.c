/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 kasurli, 제한된 입력 takininga_atuutilik, 비동기 nassiutili_atuutilik, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 titiqqat 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "ungasittuq_atuutilik.h"
#include "암호기반.h"
#include "Miksaanuungajuq.h"
#include "../통신망/통신망.h"
#include "../기계/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t 보드터미널(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,ilagijaujuq_atuutilik=-1,단계,닫을예정;
static uintptr_t 접속시각,다시받을때;
static unsigned char 입력[8192],출력[4096],도전[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pel_anininga=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned 타일수,타일자리,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *자료위치){return(unsigned)자료위치[0]*256+자료위치[1];}
static uint32_t 읽기32(const unsigned char *자료위치){return(uint32_t)자료위치[0]<<24|(uint32_t)자료위치[1]<<16|(uint32_t)자료위치[2]<<8|자료위치[3];}
static void titiraq_16(unsigned char *자료위치,unsigned atuutilik){자료위치[0]=atuutilik>>8;자료위치[1]=atuutilik;}
static void titiraq_32(unsigned char *자료위치,uint32_t atuutilik){자료위치[0]=atuutilik>>24;자료위치[1]=atuutilik>>16;자료위치[2]=atuutilik>>8;자료위치[3]=atuutilik;}
static void matuli(void){if(ilagijaujuq_atuutilik>=0)matuli_Kasuqatigiitsimajut(ilagijaujuq_atuutilik);ilagijaujuq_atuutilik=-1;단계=0;입력수=출력수=보낸수=0;타일수=타일자리=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *titiqqat,unsigned 수){memcpy(출력,titiqqat,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int aulattivik_ungasittuq_saqqijaarli(unsigned sugiarut){
    if(sugiarut==0){matuli();if(듣는곳>=0)matuli_Kasuqatigiitsimajut(듣는곳);듣는곳=-1;return 0;}
    if(sugiarut!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int kapputigaq_atuutilik=통신끝점만들기(1);if(kapputigaq_atuutilik<0)return kapputigaq_atuutilik;통신주소재사용(kapputigaq_atuutilik);
    int 결과=망주소묶기(kapputigaq_atuutilik,0,5900);if(!결과)결과=연결기다리기(kapputigaq_atuutilik);
    if(결과<0){matuli_Kasuqatigiitsimajut(kapputigaq_atuutilik);return 결과;}듣는곳=kapputigaq_atuutilik;return 0;
}
static uint32_t sanililik_naiglitiqsimajuq(unsigned 가로,unsigned 세로){
    uint32_t atuutilik=2166136261u;
    for(unsigned 세로좌표=세로;세로좌표<세로+16&&세로좌표<높이;세로좌표++)for(unsigned 가로좌표=가로;가로좌표<가로+32&&가로좌표<너비;가로좌표++)atuutilik=(atuutilik^보드화면읽기(가로좌표,세로좌표))*16777619u;
    return atuutilik;
}
static void 화면요청(const unsigned char *자료위치){
    요청가로=읽기16(자료위치+2);요청세로=읽기16(자료위치+4);요청폭=읽기16(자료위치+6);요청높이=읽기16(자료위치+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    타일수=타일자리=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned 가로좌표=요청가로/32;가로좌표<=(요청가로+요청폭-1)/32;가로좌표++){
        unsigned 자리=세로좌표*60+가로좌표;uint32_t naiglitiqsimajuq_atuutilik=sanililik_naiglitiqsimajuq(가로좌표*32,세로좌표*16);
        if(!자료위치[1]||지난요약[자리]!=naiglitiqsimajuq_atuutilik)바뀐타일[타일수++]=자리;
    }
    출력[0]=출력[1]=0;titiraq_16(출력+2,타일수);출력수=4;보낸수=0;
}
static void nassiutili_sanililik(void){
    unsigned 자리=바뀐타일[타일자리++],가로=(자리%60)*32,세로=(자리/60)*16;
    unsigned 끝가로=가로+32,끝세로=세로+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&세로>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[자리]=sanililik_naiglitiqsimajuq(가로,세로);
    if(가로<요청가로)가로=요청가로;if(세로<요청세로)세로=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    titiraq_16(출력,가로);titiraq_16(출력+2,세로);titiraq_16(출력+4,끝가로-가로);titiraq_16(출력+6,끝세로-세로);titiraq_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=세로;세로좌표<끝세로;세로좌표++)for(unsigned 가로좌표=가로;가로좌표<끝가로;가로좌표++){
        uint32_t 색=보드화면읽기(가로좌표,세로좌표),atuutilik=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pel_anininga;순번++)출력[출력수++]=atuutilik>>(8*(큰끝?pel_anininga-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(ilagijaujuq_atuutilik<0){if(보드밀리초()<다시받을때)return;ilagijaujuq_atuutilik=망연결받기(듣는곳);if(ilagijaujuq_atuutilik<0)return;
        접속시각=보드밀리초();단계=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pel_anininga=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(단계<5&&보드밀리초()-접속시각>15000){matuli();return;}
    if(출력수){int 수=통신쓰기(ilagijaujuq_atuutilik,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){matuli();return;}}
    if(!출력수&&닫을예정){matuli();return;}
    if(!출력수&&타일자리<타일수)nassiutili_sanililik();
    if(입력수==sizeof(입력)){matuli();return;}
    int 받은수=통신읽기(ilagijaujuq_atuutilik,입력+입력수,sizeof(입력)-입력수);
    if(받은수==0||(받은수<0&&받은수!=-11)){matuli();return;}if(받은수>0)입력수+=받은수;
    if(출력수||타일자리<타일수)return;
    if(단계==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){matuli();return;}소비(12);const unsigned char ilisarijauniup_qanuq_pijauninga[]={1,2};내보내기(ilisarijauniup_qanuq_pijauninga,2);단계=2;return;}
    if(단계==2&&입력수){if(입력[0]!=2||원격난수(도전,16)){matuli();return;}소비(1);내보내기(도전,16);단계=3;return;}
    if(단계==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys isirut_atuutilik;
        for(unsigned 순번=0;순번<8;순번++){unsigned atuutilik=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(atuutilik&1);atuutilik>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&isirut_atuutilik,열쇠,8);memcpy(정답,도전,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char 벡터[8]={0};br_des_ct_cbcenc_run(&isirut_atuutilik,벡터,정답+순번,8);memset(벡터,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&isirut_atuutilik,0,sizeof(isirut_atuutilik));memset(열쇠,0,8);memset(정답,0,16);memset(도전,0,16);
        titiraq_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){titiraq_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else 단계=4;return;}
    if(단계==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){matuli();return;}
        if(!보드터미널(7)){const unsigned char piniku[]={30,2,1,0,0,0,0};원격입력넣기(piniku,7);}
        memset(출력,0,40);titiraq_16(출력,너비);titiraq_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        titiraq_16(출력+8,255);titiraq_16(출력+10,255);titiraq_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *atiq="jkoros native";titiraq_32(출력+20,strlen(atiq));memcpy(출력+24,atiq,strlen(atiq));출력수=24+strlen(atiq);보낸수=0;단계=5;return;}
    if(단계!=5||!입력수)return;
    unsigned qanuittuuninga_Ataqatigiivvik=입력[0],필요=qanuittuuninga_Ataqatigiivvik==0?20:qanuittuuninga_Ataqatigiivvik==2?4:qanuittuuninga_Ataqatigiivvik==3?10:qanuittuuninga_Ataqatigiivvik==4?8:qanuittuuninga_Ataqatigiivvik==5?6:qanuittuuninga_Ataqatigiivvik==6?8:0;
    if(!필요){matuli();return;}if(입력수<필요)return;
    if(qanuittuuninga_Ataqatigiivvik==2){unsigned 수=읽기16(입력+2);if(수>128){matuli();return;}필요+=수*4;}
    if(qanuittuuninga_Ataqatigiivvik==6){unsigned 수=읽기32(입력+4);if(수>4096){matuli();return;}필요+=수;}
    if(입력수<필요)return;
    if(qanuittuuninga_Ataqatigiivvik==0){unsigned bit_atuutilik=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_atuutilik!=16&&bit_atuutilik!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_atuutilik)-1)||((uint64_t)초<<초이)>((1ull<<bit_atuutilik)-1)||((uint64_t)파<<파이)>((1ull<<bit_atuutilik)-1)){matuli();return;}
        pel_anininga=bit_atuutilik/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(qanuittuuninga_Ataqatigiivvik==3)화면요청(입력);
    else if(qanuittuuninga_Ataqatigiivvik==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(qanuittuuninga_Ataqatigiivvik==5){unsigned 가로좌표=읽기16(입력+2),세로좌표=읽기16(입력+4);if(가로좌표>=너비)가로좌표=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char piniku[]={30,1,입력[1],가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8};원격입력넣기(piniku,sizeof(piniku));}
    소비(필요);
}
