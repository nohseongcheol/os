/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Tengjast, 제한된 입력 lengd_VALUE, 비동기 senda_VALUE_f993dacd, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 gögn 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "fjartengdur_VALUE.h"
#include "암호기반.h"
#include "prófíll.h"
#include "../Net_bunki/Net_bunki.h"
#include "../vél/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t bretti_Endastöð(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int Hlustar_endastöð=-1,jafningi_VALUE=-1,stig_VALUE,닫을예정;
static uintptr_t tenging_TIME,다시받을때;
static unsigned char 입력[8192],úttak[4096],áskorun_VALUE[16];
static unsigned 입력수,úttak_COUNT,보낸수;
static unsigned 너비,높이,díll_breyta_stærð=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned bútur_COUNT,bútur_staða,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *gögn_staða){return(unsigned)gögn_staða[0]*256+gögn_staða[1];}
static uint32_t 읽기32(const unsigned char *gögn_staða){return(uint32_t)gögn_staða[0]<<24|(uint32_t)gögn_staða[1]<<16|(uint32_t)gögn_staða[2]<<8|gögn_staða[3];}
static void skrifa_16(unsigned char *gögn_staða,unsigned VALUE){gögn_staða[0]=VALUE>>8;gögn_staða[1]=VALUE;}
static void skrifa_32(unsigned char *gögn_staða,uint32_t VALUE){gögn_staða[0]=VALUE>>24;gögn_staða[1]=VALUE>>16;gögn_staða[2]=VALUE>>8;gögn_staða[3]=VALUE;}
static void Loka(void){if(jafningi_VALUE>=0)loka_Net(jafningi_VALUE);jafningi_VALUE=-1;stig_VALUE=0;입력수=úttak_COUNT=보낸수=0;bútur_COUNT=bútur_staða=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *gögn,unsigned númer){memcpy(úttak,gögn,númer);úttak_COUNT=númer;보낸수=0;}
static void nota_VALUE(unsigned númer){입력수-=númer;memmove(입력,입력+númer,입력수);}
int stýring_fjartengdur_birta(unsigned Aðgerð){
    if(Aðgerð==0){Loka();if(Hlustar_endastöð>=0)loka_Net(Hlustar_endastöð);Hlustar_endastöð=-1;return 0;}
    if(Aðgerð!=1)return Hlustar_endastöð>=0;
    if(Hlustar_endastöð>=0)return 0;
    int gátt_VALUE=통신끝점만들기(1);if(gátt_VALUE<0)return gátt_VALUE;통신주소재사용(gátt_VALUE);
    int NIÐURSTAÐA=nettó_BIND(gátt_VALUE,0,5900);if(!NIÐURSTAÐA)NIÐURSTAÐA=nettó_hlusta(gátt_VALUE);
    if(NIÐURSTAÐA<0){loka_Net(gátt_VALUE);return NIÐURSTAÐA;}Hlustar_endastöð=gátt_VALUE;return 0;
}
static uint32_t bútur_samantekt(unsigned 가로,unsigned Lóðrétt_staða){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_hnit=Lóðrétt_staða;Y_hnit<Lóðrétt_staða+16&&Y_hnit<높이;Y_hnit++)for(unsigned x_hnit=가로;x_hnit<가로+32&&x_hnit<너비;x_hnit++)VALUE=(VALUE^보드화면읽기(x_hnit,Y_hnit))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *gögn_staða){
    요청가로=읽기16(gögn_staða+2);요청세로=읽기16(gögn_staða+4);요청폭=읽기16(gögn_staða+6);요청높이=읽기16(gögn_staða+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    bútur_COUNT=bútur_staða=0;
    if(요청폭&&요청높이)for(unsigned Y_hnit=요청세로/16;Y_hnit<=(요청세로+요청높이-1)/16;Y_hnit++)for(unsigned x_hnit=요청가로/32;x_hnit<=(요청가로+요청폭-1)/32;x_hnit++){
        unsigned staða_INDEX=Y_hnit*60+x_hnit;uint32_t samantekt_VALUE=bútur_samantekt(x_hnit*32,Y_hnit*16);
        if(!gögn_staða[1]||지난요약[staða_INDEX]!=samantekt_VALUE)바뀐타일[bútur_COUNT++]=staða_INDEX;
    }
    úttak[0]=úttak[1]=0;skrifa_16(úttak+2,bútur_COUNT);úttak_COUNT=4;보낸수=0;
}
static void senda_bútur(void){
    unsigned staða_INDEX=바뀐타일[bútur_staða++],가로=(staða_INDEX%60)*32,Lóðrétt_staða=(staða_INDEX/60)*16;
    unsigned ljúka_X=가로+32,ljúka_Y=Lóðrétt_staða+16;if(ljúka_X>너비)ljúka_X=너비;if(ljúka_Y>높이)ljúka_Y=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Lóðrétt_staða>=요청세로&&ljúka_X<=요청가로+요청폭&&ljúka_Y<=요청세로+요청높이;
    if(전부)지난요약[staða_INDEX]=bútur_samantekt(가로,Lóðrétt_staða);
    if(가로<요청가로)가로=요청가로;if(Lóðrétt_staða<요청세로)Lóðrétt_staða=요청세로;
    if(ljúka_X>요청가로+요청폭)ljúka_X=요청가로+요청폭;if(ljúka_Y>요청세로+요청높이)ljúka_Y=요청세로+요청높이;
    skrifa_16(úttak,가로);skrifa_16(úttak+2,Lóðrétt_staða);skrifa_16(úttak+4,ljúka_X-가로);skrifa_16(úttak+6,ljúka_Y-Lóðrétt_staða);skrifa_32(úttak+8,0);
    úttak_COUNT=12;보낸수=0;
    for(unsigned Y_hnit=Lóðrétt_staða;Y_hnit<ljúka_Y;Y_hnit++)for(unsigned x_hnit=가로;x_hnit<ljúka_X;x_hnit++){
        uint32_t 색=보드화면읽기(x_hnit,Y_hnit),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<díll_breyta_stærð;순번++)úttak[úttak_COUNT++]=VALUE>>(8*(큰끝?díll_breyta_stærð-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Hlustar_endastöð<0)return;
    if(jafningi_VALUE<0){if(보드밀리초()<다시받을때)return;jafningi_VALUE=nettó_samþykkja(Hlustar_endastöð);if(jafningi_VALUE<0)return;
        tenging_TIME=보드밀리초();stig_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        díll_breyta_stærð=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(stig_VALUE<5&&보드밀리초()-tenging_TIME>15000){Loka();return;}
    if(úttak_COUNT){int númer=nettó_skrifa(jafningi_VALUE,úttak+보낸수,úttak_COUNT-보낸수);if(númer>0){보낸수+=númer;if(보낸수==úttak_COUNT)úttak_COUNT=보낸수=0;}else if(númer!=-11){Loka();return;}}
    if(!úttak_COUNT&&닫을예정){Loka();return;}
    if(!úttak_COUNT&&bútur_staða<bútur_COUNT)senda_bútur();
    if(입력수==sizeof(입력)){Loka();return;}
    int RECEIVED_COUNT=통신읽기(jafningi_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Loka();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(úttak_COUNT||bútur_staða<bútur_COUNT)return;
    if(stig_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Loka();return;}nota_VALUE(12);const unsigned char sannvottunaraðferð[]={1,2};내보내기(sannvottunaraðferð,2);stig_VALUE=2;return;}
    if(stig_VALUE==2&&입력수){if(입력[0]!=2||원격난수(áskorun_VALUE,16)){Loka();return;}nota_VALUE(1);내보내기(áskorun_VALUE,16);stig_VALUE=3;return;}
    if(stig_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys aðgangsorð_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&aðgangsorð_VALUE,열쇠,8);memcpy(정답,áskorun_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vigur_VALUE[8]={0};br_des_ct_cbcenc_run(&aðgangsorð_VALUE,vigur_VALUE,정답+순번,8);memset(vigur_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];nota_VALUE(16);memset(&aðgangsorð_VALUE,0,sizeof(aðgangsorð_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(áskorun_VALUE,0,16);
        skrifa_32(úttak,차이?1:0);úttak_COUNT=4;보낸수=0;
        if(차이){skrifa_32(úttak+4,19);memcpy(úttak+8,"Authentication fail",19);úttak_COUNT=27;닫을예정=1;}else stig_VALUE=4;return;}
    if(stig_VALUE==4&&입력수){nota_VALUE(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Loka();return;}
        if(!bretti_Endastöð(7)){const unsigned char atvik[]={30,2,1,0,0,0,0};원격입력넣기(atvik,7);}
        memset(úttak,0,40);skrifa_16(úttak,너비);skrifa_16(úttak+2,높이);úttak[4]=32;úttak[5]=24;úttak[7]=1;
        skrifa_16(úttak+8,255);skrifa_16(úttak+10,255);skrifa_16(úttak+12,255);úttak[14]=16;úttak[15]=8;
        const char *Heiti="jkoros native";skrifa_32(úttak+20,strlen(Heiti));memcpy(úttak+24,Heiti,strlen(Heiti));úttak_COUNT=24+strlen(Heiti);보낸수=0;stig_VALUE=5;return;}
    if(stig_VALUE!=5||!입력수)return;
    unsigned TYPE_tegund=입력[0],필요=TYPE_tegund==0?20:TYPE_tegund==2?4:TYPE_tegund==3?10:TYPE_tegund==4?8:TYPE_tegund==5?6:TYPE_tegund==6?8:0;
    if(!필요){Loka();return;}if(입력수<필요)return;
    if(TYPE_tegund==2){unsigned númer=읽기16(입력+2);if(númer>128){Loka();return;}필요+=númer*4;}
    if(TYPE_tegund==6){unsigned númer=읽기32(입력+4);if(númer>4096){Loka();return;}필요+=númer;}
    if(입력수<필요)return;
    if(TYPE_tegund==0){unsigned biti_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((biti_VALUE!=16&&biti_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<biti_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<biti_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<biti_VALUE)-1)){Loka();return;}
        díll_breyta_stærð=biti_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_tegund==3)화면요청(입력);
    else if(TYPE_tegund==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_tegund==5){unsigned x_hnit=읽기16(입력+2),Y_hnit=읽기16(입력+4);if(x_hnit>=너비)x_hnit=너비-1;if(Y_hnit>=높이)Y_hnit=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char atvik[]={30,1,입력[1],x_hnit&255,x_hnit>>8,Y_hnit&255,Y_hnit>>8};원격입력넣기(atvik,sizeof(atvik));}
    nota_VALUE(필요);
}
