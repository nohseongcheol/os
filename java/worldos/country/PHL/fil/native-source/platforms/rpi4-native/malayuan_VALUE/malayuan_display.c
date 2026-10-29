/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 CONNECT, 제한된 입력 haba_VALUE, 비동기 i_email_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "malayuan_VALUE.h"
#include "암호기반.h"
#include "Profile.h"
#include "../Network_Stack/Network_Stack.h"
#include "../machine/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t board_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,peer_VALUE=-1,stage_VALUE,닫을예정;
static uintptr_t koneksyon_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],hamon_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pel_sukat=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned tile_COUNT,tile_posisyon,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_posisyon){return(unsigned)data_posisyon[0]*256+data_posisyon[1];}
static uint32_t 읽기32(const unsigned char *data_posisyon){return(uint32_t)data_posisyon[0]<<24|(uint32_t)data_posisyon[1]<<16|(uint32_t)data_posisyon[2]<<8|data_posisyon[3];}
static void sumulat_16(unsigned char *data_posisyon,unsigned VALUE){data_posisyon[0]=VALUE>>8;data_posisyon[1]=VALUE;}
static void sumulat_32(unsigned char *data_posisyon,uint32_t VALUE){data_posisyon[0]=VALUE>>24;data_posisyon[1]=VALUE>>16;data_posisyon[2]=VALUE>>8;data_posisyon[3]=VALUE;}
static void isara(void){if(peer_VALUE>=0)isara_Network(peer_VALUE);peer_VALUE=-1;stage_VALUE=0;입력수=출력수=보낸수=0;tile_COUNT=tile_posisyon=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(출력,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int control_malayuan_display(unsigned aksyon){
    if(aksyon==0){isara();if(듣는곳>=0)isara_Network(듣는곳);듣는곳=-1;return 0;}
    if(aksyon!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int sukat=망주소묶기(port_VALUE,0,5900);if(!sukat)sukat=연결기다리기(port_VALUE);
    if(sukat<0){isara_Network(port_VALUE);return sukat;}듣는곳=port_VALUE;return 0;
}
static uint32_t tile_buod(unsigned 가로,unsigned archive_posisyon){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_button_coordinate=archive_posisyon;Y_button_coordinate<archive_posisyon+16&&Y_button_coordinate<높이;Y_button_coordinate++)for(unsigned x_coordinate=가로;x_coordinate<가로+32&&x_coordinate<너비;x_coordinate++)VALUE=(VALUE^보드화면읽기(x_coordinate,Y_button_coordinate))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *data_posisyon){
    요청가로=읽기16(data_posisyon+2);요청세로=읽기16(data_posisyon+4);요청폭=읽기16(data_posisyon+6);요청높이=읽기16(data_posisyon+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    tile_COUNT=tile_posisyon=0;
    if(요청폭&&요청높이)for(unsigned Y_button_coordinate=요청세로/16;Y_button_coordinate<=(요청세로+요청높이-1)/16;Y_button_coordinate++)for(unsigned x_coordinate=요청가로/32;x_coordinate<=(요청가로+요청폭-1)/32;x_coordinate++){
        unsigned posisyon_INDEX=Y_button_coordinate*60+x_coordinate;uint32_t buod_VALUE=tile_buod(x_coordinate*32,Y_button_coordinate*16);
        if(!data_posisyon[1]||지난요약[posisyon_INDEX]!=buod_VALUE)바뀐타일[tile_COUNT++]=posisyon_INDEX;
    }
    출력[0]=출력[1]=0;sumulat_16(출력+2,tile_COUNT);출력수=4;보낸수=0;
}
static void i_email_tile(void){
    unsigned posisyon_INDEX=바뀐타일[tile_posisyon++],가로=(posisyon_INDEX%60)*32,archive_posisyon=(posisyon_INDEX/60)*16;
    unsigned tapusin_X_button=가로+32,tapusin_Y_button=archive_posisyon+16;if(tapusin_X_button>너비)tapusin_X_button=너비;if(tapusin_Y_button>높이)tapusin_Y_button=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&archive_posisyon>=요청세로&&tapusin_X_button<=요청가로+요청폭&&tapusin_Y_button<=요청세로+요청높이;
    if(전부)지난요약[posisyon_INDEX]=tile_buod(가로,archive_posisyon);
    if(가로<요청가로)가로=요청가로;if(archive_posisyon<요청세로)archive_posisyon=요청세로;
    if(tapusin_X_button>요청가로+요청폭)tapusin_X_button=요청가로+요청폭;if(tapusin_Y_button>요청세로+요청높이)tapusin_Y_button=요청세로+요청높이;
    sumulat_16(출력,가로);sumulat_16(출력+2,archive_posisyon);sumulat_16(출력+4,tapusin_X_button-가로);sumulat_16(출력+6,tapusin_Y_button-archive_posisyon);sumulat_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_button_coordinate=archive_posisyon;Y_button_coordinate<tapusin_Y_button;Y_button_coordinate++)for(unsigned x_coordinate=가로;x_coordinate<tapusin_X_button;x_coordinate++){
        uint32_t 색=보드화면읽기(x_coordinate,Y_button_coordinate),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pel_sukat;순번++)출력[출력수++]=VALUE>>(8*(큰끝?pel_sukat-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(peer_VALUE<0){if(보드밀리초()<다시받을때)return;peer_VALUE=망연결받기(듣는곳);if(peer_VALUE<0)return;
        koneksyon_TIME=보드밀리초();stage_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pel_sukat=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(stage_VALUE<5&&보드밀리초()-koneksyon_TIME>15000){isara();return;}
    if(출력수){int 수=통신쓰기(peer_VALUE,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){isara();return;}}
    if(!출력수&&닫을예정){isara();return;}
    if(!출력수&&tile_posisyon<tile_COUNT)i_email_tile();
    if(입력수==sizeof(입력)){isara();return;}
    int RECEIVED_COUNT=통신읽기(peer_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){isara();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||tile_posisyon<tile_COUNT)return;
    if(stage_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){isara();return;}소비(12);const unsigned char metodong_auth[]={1,2};내보내기(metodong_auth,2);stage_VALUE=2;return;}
    if(stage_VALUE==2&&입력수){if(입력[0]!=2||원격난수(hamon_VALUE,16)){isara();return;}소비(1);내보내기(hamon_VALUE,16);stage_VALUE=3;return;}
    if(stage_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys password_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&password_VALUE,열쇠,8);memcpy(정답,hamon_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vector_VALUE[8]={0};br_des_ct_cbcenc_run(&password_VALUE,vector_VALUE,정답+순번,8);memset(vector_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&password_VALUE,0,sizeof(password_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(hamon_VALUE,0,16);
        sumulat_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){sumulat_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else stage_VALUE=4;return;}
    if(stage_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){isara();return;}
        if(!board_Terminal(7)){const unsigned char kaganapan[]={30,2,1,0,0,0,0};원격입력넣기(kaganapan,7);}
        memset(출력,0,40);sumulat_16(출력,너비);sumulat_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        sumulat_16(출력+8,255);sumulat_16(출력+10,255);sumulat_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *pangalan="jkoros native";sumulat_32(출력+20,strlen(pangalan));memcpy(출력+24,pangalan,strlen(pangalan));출력수=24+strlen(pangalan);보낸수=0;stage_VALUE=5;return;}
    if(stage_VALUE!=5||!입력수)return;
    unsigned TYPE_kategorya=입력[0],필요=TYPE_kategorya==0?20:TYPE_kategorya==2?4:TYPE_kategorya==3?10:TYPE_kategorya==4?8:TYPE_kategorya==5?6:TYPE_kategorya==6?8:0;
    if(!필요){isara();return;}if(입력수<필요)return;
    if(TYPE_kategorya==2){unsigned 수=읽기16(입력+2);if(수>128){isara();return;}필요+=수*4;}
    if(TYPE_kategorya==6){unsigned 수=읽기32(입력+4);if(수>4096){isara();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_kategorya==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){isara();return;}
        pel_sukat=bit_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_kategorya==3)화면요청(입력);
    else if(TYPE_kategorya==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_kategorya==5){unsigned x_coordinate=읽기16(입력+2),Y_button_coordinate=읽기16(입력+4);if(x_coordinate>=너비)x_coordinate=너비-1;if(Y_button_coordinate>=높이)Y_button_coordinate=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char kaganapan[]={30,1,입력[1],x_coordinate&255,x_coordinate>>8,Y_button_coordinate&255,Y_button_coordinate>>8};원격입력넣기(kaganapan,sizeof(kaganapan));}
    소비(필요);
}
