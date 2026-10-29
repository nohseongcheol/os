/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Kopla_til, 제한된 입력 lengd_VALUE, 비동기 sende_VALUE_f993dacd, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "fjern_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Nettverk_Stabel/Nettverk_Stabel.h"
#include "../maskin/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tavle_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int Lyttar_endepunkt=-1,node_VALUE_6a3b6fa7=-1,stadium_VALUE,닫을예정;
static uintptr_t kontakt_TIME,다시받을때;
static unsigned char 입력[8192],Utdata[4096],utfordring_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,piksel_endre_storleik=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned flis_COUNT,flis_plassere,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_plassere){return(unsigned)data_plassere[0]*256+data_plassere[1];}
static uint32_t 읽기32(const unsigned char *data_plassere){return(uint32_t)data_plassere[0]<<24|(uint32_t)data_plassere[1]<<16|(uint32_t)data_plassere[2]<<8|data_plassere[3];}
static void skrive_16(unsigned char *data_plassere,unsigned VALUE){data_plassere[0]=VALUE>>8;data_plassere[1]=VALUE;}
static void skrive_32(unsigned char *data_plassere,uint32_t VALUE){data_plassere[0]=VALUE>>24;data_plassere[1]=VALUE>>16;data_plassere[2]=VALUE>>8;data_plassere[3]=VALUE;}
static void Lukk(void){if(node_VALUE_6a3b6fa7>=0)Lukk_Nettverk(node_VALUE_6a3b6fa7);node_VALUE_6a3b6fa7=-1;stadium_VALUE=0;입력수=출력수=보낸수=0;flis_COUNT=flis_plassere=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(Utdata,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int styring_fjern_vise(unsigned Handling){
    if(Handling==0){Lukk();if(Lyttar_endepunkt>=0)Lukk_Nettverk(Lyttar_endepunkt);Lyttar_endepunkt=-1;return 0;}
    if(Handling!=1)return Lyttar_endepunkt>=0;
    if(Lyttar_endepunkt>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int forretningsmål=망주소묶기(port_VALUE,0,5900);if(!forretningsmål)forretningsmål=연결기다리기(port_VALUE);
    if(forretningsmål<0){Lukk_Nettverk(port_VALUE);return forretningsmål;}Lyttar_endepunkt=port_VALUE;return 0;
}
static uint32_t flis_samandrag(unsigned 가로,unsigned vertikalvising_plassere){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_koordinat=vertikalvising_plassere;Y_koordinat<vertikalvising_plassere+16&&Y_koordinat<높이;Y_koordinat++)for(unsigned x_koordinat=가로;x_koordinat<가로+32&&x_koordinat<너비;x_koordinat++)VALUE=(VALUE^보드화면읽기(x_koordinat,Y_koordinat))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *data_plassere){
    요청가로=읽기16(data_plassere+2);요청세로=읽기16(data_plassere+4);요청폭=읽기16(data_plassere+6);요청높이=읽기16(data_plassere+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    flis_COUNT=flis_plassere=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinat=요청세로/16;Y_koordinat<=(요청세로+요청높이-1)/16;Y_koordinat++)for(unsigned x_koordinat=요청가로/32;x_koordinat<=(요청가로+요청폭-1)/32;x_koordinat++){
        unsigned plassere_INDEX=Y_koordinat*60+x_koordinat;uint32_t samandrag_VALUE=flis_samandrag(x_koordinat*32,Y_koordinat*16);
        if(!data_plassere[1]||지난요약[plassere_INDEX]!=samandrag_VALUE)바뀐타일[flis_COUNT++]=plassere_INDEX;
    }
    Utdata[0]=Utdata[1]=0;skrive_16(Utdata+2,flis_COUNT);출력수=4;보낸수=0;
}
static void sende_flis(void){
    unsigned plassere_INDEX=바뀐타일[flis_plassere++],가로=(plassere_INDEX%60)*32,vertikalvising_plassere=(plassere_INDEX/60)*16;
    unsigned avslutte_X=가로+32,avslutte_Y=vertikalvising_plassere+16;if(avslutte_X>너비)avslutte_X=너비;if(avslutte_Y>높이)avslutte_Y=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&vertikalvising_plassere>=요청세로&&avslutte_X<=요청가로+요청폭&&avslutte_Y<=요청세로+요청높이;
    if(전부)지난요약[plassere_INDEX]=flis_samandrag(가로,vertikalvising_plassere);
    if(가로<요청가로)가로=요청가로;if(vertikalvising_plassere<요청세로)vertikalvising_plassere=요청세로;
    if(avslutte_X>요청가로+요청폭)avslutte_X=요청가로+요청폭;if(avslutte_Y>요청세로+요청높이)avslutte_Y=요청세로+요청높이;
    skrive_16(Utdata,가로);skrive_16(Utdata+2,vertikalvising_plassere);skrive_16(Utdata+4,avslutte_X-가로);skrive_16(Utdata+6,avslutte_Y-vertikalvising_plassere);skrive_32(Utdata+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_koordinat=vertikalvising_plassere;Y_koordinat<avslutte_Y;Y_koordinat++)for(unsigned x_koordinat=가로;x_koordinat<avslutte_X;x_koordinat++){
        uint32_t 색=보드화면읽기(x_koordinat,Y_koordinat),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<piksel_endre_storleik;순번++)Utdata[출력수++]=VALUE>>(8*(큰끝?piksel_endre_storleik-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Lyttar_endepunkt<0)return;
    if(node_VALUE_6a3b6fa7<0){if(보드밀리초()<다시받을때)return;node_VALUE_6a3b6fa7=망연결받기(Lyttar_endepunkt);if(node_VALUE_6a3b6fa7<0)return;
        kontakt_TIME=보드밀리초();stadium_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        piksel_endre_storleik=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(stadium_VALUE<5&&보드밀리초()-kontakt_TIME>15000){Lukk();return;}
    if(출력수){int 수=통신쓰기(node_VALUE_6a3b6fa7,Utdata+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Lukk();return;}}
    if(!출력수&&닫을예정){Lukk();return;}
    if(!출력수&&flis_plassere<flis_COUNT)sende_flis();
    if(입력수==sizeof(입력)){Lukk();return;}
    int RECEIVED_COUNT=통신읽기(node_VALUE_6a3b6fa7,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Lukk();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||flis_plassere<flis_COUNT)return;
    if(stadium_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Lukk();return;}소비(12);const unsigned char godkjenningsmetode[]={1,2};내보내기(godkjenningsmetode,2);stadium_VALUE=2;return;}
    if(stadium_VALUE==2&&입력수){if(입력[0]!=2||원격난수(utfordring_VALUE,16)){Lukk();return;}소비(1);내보내기(utfordring_VALUE,16);stadium_VALUE=3;return;}
    if(stadium_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys passord_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&passord_VALUE,열쇠,8);memcpy(정답,utfordring_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&passord_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&passord_VALUE,0,sizeof(passord_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(utfordring_VALUE,0,16);
        skrive_32(Utdata,차이?1:0);출력수=4;보낸수=0;
        if(차이){skrive_32(Utdata+4,19);memcpy(Utdata+8,"Authentication fail",19);출력수=27;닫을예정=1;}else stadium_VALUE=4;return;}
    if(stadium_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Lukk();return;}
        if(!Tavle_Terminal(7)){const unsigned char Hending[]={30,2,1,0,0,0,0};원격입력넣기(Hending,7);}
        memset(Utdata,0,40);skrive_16(Utdata,너비);skrive_16(Utdata+2,높이);Utdata[4]=32;Utdata[5]=24;Utdata[7]=1;
        skrive_16(Utdata+8,255);skrive_16(Utdata+10,255);skrive_16(Utdata+12,255);Utdata[14]=16;Utdata[15]=8;
        const char *Namn="jkoros native";skrive_32(Utdata+20,strlen(Namn));memcpy(Utdata+24,Namn,strlen(Namn));출력수=24+strlen(Namn);보낸수=0;stadium_VALUE=5;return;}
    if(stadium_VALUE!=5||!입력수)return;
    unsigned TYPE_kategori=입력[0],필요=TYPE_kategori==0?20:TYPE_kategori==2?4:TYPE_kategori==3?10:TYPE_kategori==4?8:TYPE_kategori==5?6:TYPE_kategori==6?8:0;
    if(!필요){Lukk();return;}if(입력수<필요)return;
    if(TYPE_kategori==2){unsigned 수=읽기16(입력+2);if(수>128){Lukk();return;}필요+=수*4;}
    if(TYPE_kategori==6){unsigned 수=읽기32(입력+4);if(수>4096){Lukk();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_kategori==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){Lukk();return;}
        piksel_endre_storleik=bit_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_kategori==3)화면요청(입력);
    else if(TYPE_kategori==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_kategori==5){unsigned x_koordinat=읽기16(입력+2),Y_koordinat=읽기16(입력+4);if(x_koordinat>=너비)x_koordinat=너비-1;if(Y_koordinat>=높이)Y_koordinat=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char Hending[]={30,1,입력[1],x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8};원격입력넣기(Hending,sizeof(Hending));}
    소비(필요);
}
