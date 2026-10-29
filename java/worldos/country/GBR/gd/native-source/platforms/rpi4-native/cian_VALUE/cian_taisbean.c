/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 CONNECT, 제한된 입력 faid_VALUE, 비동기 cuir_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 dàta 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "cian_VALUE.h"
#include "암호기반.h"
#include "Pròifil.h"
#include "../lìonra_stac/lìonra_stac.h"
#include "../inneal/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t bòrd_tèirmineal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,seise_VALUE=-1,stèidse_VALUE,닫을예정;
static uintptr_t ceangal_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],dùbhlan_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pel_atharraich_am_meud=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned leacag_COUNT,leacag_suidhich,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *dàta_suidhich){return(unsigned)dàta_suidhich[0]*256+dàta_suidhich[1];}
static uint32_t 읽기32(const unsigned char *dàta_suidhich){return(uint32_t)dàta_suidhich[0]<<24|(uint32_t)dàta_suidhich[1]<<16|(uint32_t)dàta_suidhich[2]<<8|dàta_suidhich[3];}
static void sgrìobh_16(unsigned char *dàta_suidhich,unsigned VALUE){dàta_suidhich[0]=VALUE>>8;dàta_suidhich[1]=VALUE;}
static void sgrìobh_32(unsigned char *dàta_suidhich,uint32_t VALUE){dàta_suidhich[0]=VALUE>>24;dàta_suidhich[1]=VALUE>>16;dàta_suidhich[2]=VALUE>>8;dàta_suidhich[3]=VALUE;}
static void dùin(void){if(seise_VALUE>=0)dùin_lìonra(seise_VALUE);seise_VALUE=-1;stèidse_VALUE=0;입력수=출력수=보낸수=0;leacag_COUNT=leacag_suidhich=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *dàta,unsigned 수){memcpy(출력,dàta,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int smachd_cian_taisbean(unsigned Gnìomh){
    if(Gnìomh==0){dùin();if(듣는곳>=0)dùin_lìonra(듣는곳);듣는곳=-1;return 0;}
    if(Gnìomh!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int tomhas=망주소묶기(port_VALUE,0,5900);if(!tomhas)tomhas=연결기다리기(port_VALUE);
    if(tomhas<0){dùin_lìonra(port_VALUE);return tomhas;}듣는곳=port_VALUE;return 0;
}
static uint32_t 타일요약(unsigned 가로,unsigned inghearach_suidhich){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=inghearach_suidhich;세로좌표<inghearach_suidhich+16&&세로좌표<높이;세로좌표++)for(unsigned co_chomharra_x=가로;co_chomharra_x<가로+32&&co_chomharra_x<너비;co_chomharra_x++)VALUE=(VALUE^보드화면읽기(co_chomharra_x,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *dàta_suidhich){
    요청가로=읽기16(dàta_suidhich+2);요청세로=읽기16(dàta_suidhich+4);요청폭=읽기16(dàta_suidhich+6);요청높이=읽기16(dàta_suidhich+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    leacag_COUNT=leacag_suidhich=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned co_chomharra_x=요청가로/32;co_chomharra_x<=(요청가로+요청폭-1)/32;co_chomharra_x++){
        unsigned suidhich_INDEX=세로좌표*60+co_chomharra_x;uint32_t 요약=타일요약(co_chomharra_x*32,세로좌표*16);
        if(!dàta_suidhich[1]||지난요약[suidhich_INDEX]!=요약)바뀐타일[leacag_COUNT++]=suidhich_INDEX;
    }
    출력[0]=출력[1]=0;sgrìobh_16(출력+2,leacag_COUNT);출력수=4;보낸수=0;
}
static void cuir_leacag(void){
    unsigned suidhich_INDEX=바뀐타일[leacag_suidhich++],가로=(suidhich_INDEX%60)*32,inghearach_suidhich=(suidhich_INDEX/60)*16;
    unsigned 끝가로=가로+32,끝세로=inghearach_suidhich+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&inghearach_suidhich>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[suidhich_INDEX]=타일요약(가로,inghearach_suidhich);
    if(가로<요청가로)가로=요청가로;if(inghearach_suidhich<요청세로)inghearach_suidhich=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    sgrìobh_16(출력,가로);sgrìobh_16(출력+2,inghearach_suidhich);sgrìobh_16(출력+4,끝가로-가로);sgrìobh_16(출력+6,끝세로-inghearach_suidhich);sgrìobh_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=inghearach_suidhich;세로좌표<끝세로;세로좌표++)for(unsigned co_chomharra_x=가로;co_chomharra_x<끝가로;co_chomharra_x++){
        uint32_t 색=보드화면읽기(co_chomharra_x,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pel_atharraich_am_meud;순번++)출력[출력수++]=VALUE>>(8*(큰끝?pel_atharraich_am_meud-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(seise_VALUE<0){if(보드밀리초()<다시받을때)return;seise_VALUE=망연결받기(듣는곳);if(seise_VALUE<0)return;
        ceangal_TIME=보드밀리초();stèidse_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pel_atharraich_am_meud=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(stèidse_VALUE<5&&보드밀리초()-ceangal_TIME>15000){dùin();return;}
    if(출력수){int 수=통신쓰기(seise_VALUE,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){dùin();return;}}
    if(!출력수&&닫을예정){dùin();return;}
    if(!출력수&&leacag_suidhich<leacag_COUNT)cuir_leacag();
    if(입력수==sizeof(입력)){dùin();return;}
    int RECEIVED_COUNT=통신읽기(seise_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){dùin();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||leacag_suidhich<leacag_COUNT)return;
    if(stèidse_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){dùin();return;}소비(12);const unsigned char dòigh_dearbhaidh[]={1,2};내보내기(dòigh_dearbhaidh,2);stèidse_VALUE=2;return;}
    if(stèidse_VALUE==2&&입력수){if(입력[0]!=2||원격난수(dùbhlan_VALUE,16)){dùin();return;}소비(1);내보내기(dùbhlan_VALUE,16);stèidse_VALUE=3;return;}
    if(stèidse_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys facal_faire_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&facal_faire_VALUE,열쇠,8);memcpy(정답,dùbhlan_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vector_VALUE[8]={0};br_des_ct_cbcenc_run(&facal_faire_VALUE,vector_VALUE,정답+순번,8);memset(vector_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&facal_faire_VALUE,0,sizeof(facal_faire_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(dùbhlan_VALUE,0,16);
        sgrìobh_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){sgrìobh_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else stèidse_VALUE=4;return;}
    if(stèidse_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){dùin();return;}
        if(!bòrd_tèirmineal(7)){const unsigned char tachartas[]={30,2,1,0,0,0,0};원격입력넣기(tachartas,7);}
        memset(출력,0,40);sgrìobh_16(출력,너비);sgrìobh_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        sgrìobh_16(출력+8,255);sgrìobh_16(출력+10,255);sgrìobh_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Ainm="jkoros native";sgrìobh_32(출력+20,strlen(Ainm));memcpy(출력+24,Ainm,strlen(Ainm));출력수=24+strlen(Ainm);보낸수=0;stèidse_VALUE=5;return;}
    if(stèidse_VALUE!=5||!입력수)return;
    unsigned TYPE_roinn_seòrsa=입력[0],필요=TYPE_roinn_seòrsa==0?20:TYPE_roinn_seòrsa==2?4:TYPE_roinn_seòrsa==3?10:TYPE_roinn_seòrsa==4?8:TYPE_roinn_seòrsa==5?6:TYPE_roinn_seòrsa==6?8:0;
    if(!필요){dùin();return;}if(입력수<필요)return;
    if(TYPE_roinn_seòrsa==2){unsigned 수=읽기16(입력+2);if(수>128){dùin();return;}필요+=수*4;}
    if(TYPE_roinn_seòrsa==6){unsigned 수=읽기32(입력+4);if(수>4096){dùin();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_roinn_seòrsa==0){unsigned biot_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((biot_VALUE!=16&&biot_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<biot_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<biot_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<biot_VALUE)-1)){dùin();return;}
        pel_atharraich_am_meud=biot_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_roinn_seòrsa==3)화면요청(입력);
    else if(TYPE_roinn_seòrsa==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_roinn_seòrsa==5){unsigned co_chomharra_x=읽기16(입력+2),세로좌표=읽기16(입력+4);if(co_chomharra_x>=너비)co_chomharra_x=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char tachartas[]={30,1,입력[1],co_chomharra_x&255,co_chomharra_x>>8,세로좌표&255,세로좌표>>8};원격입력넣기(tachartas,sizeof(tachartas));}
    소비(필요);
}
