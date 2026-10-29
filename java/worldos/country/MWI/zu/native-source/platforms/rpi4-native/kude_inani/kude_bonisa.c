/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Xhumanisa, 제한된 입력 ubude_inani, 비동기 Thumela_inani, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 imininingwane 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "kude_inani.h"
#include "암호기반.h"
#include "Iphrofayili.h"
#include "../iNethiwekhi_Isitaki/iNethiwekhi_Isitaki.h"
#include "../umshini/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t 보드터미널(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,untanga_inani=-1,isigaba_inani_29ee1bb7,닫을예정;
static uintptr_t 접속시각,다시받을때;
static unsigned char 입력[8192],출력[4096],inselele_inani[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,i_pel_linganisa=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned 타일수,타일자리,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *자료위치){return(unsigned)자료위치[0]*256+자료위치[1];}
static uint32_t 읽기32(const unsigned char *자료위치){return(uint32_t)자료위치[0]<<24|(uint32_t)자료위치[1]<<16|(uint32_t)자료위치[2]<<8|자료위치[3];}
static void bhala_16(unsigned char *자료위치,unsigned inani){자료위치[0]=inani>>8;자료위치[1]=inani;}
static void bhala_32(unsigned char *자료위치,uint32_t inani){자료위치[0]=inani>>24;자료위치[1]=inani>>16;자료위치[2]=inani>>8;자료위치[3]=inani;}
static void Vala(void){if(untanga_inani>=0)vala_iNethiwekhi(untanga_inani);untanga_inani=-1;isigaba_inani_29ee1bb7=0;입력수=출력수=보낸수=0;타일수=타일자리=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *imininingwane,unsigned 수){memcpy(출력,imininingwane,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int isilawuli_kude_bonisa(unsigned Isenzo){
    if(Isenzo==0){Vala();if(듣는곳>=0)vala_iNethiwekhi(듣는곳);듣는곳=-1;return 0;}
    if(Isenzo!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int intuba_inani=통신끝점만들기(1);if(intuba_inani<0)return intuba_inani;통신주소재사용(intuba_inani);
    int 결과=망주소묶기(intuba_inani,0,5900);if(!결과)결과=연결기다리기(intuba_inani);
    if(결과<0){vala_iNethiwekhi(intuba_inani);return 결과;}듣는곳=intuba_inani;return 0;
}
static uint32_t I_tile_isifinyezo(unsigned 가로,unsigned 세로){
    uint32_t inani=2166136261u;
    for(unsigned 세로좌표=세로;세로좌표<세로+16&&세로좌표<높이;세로좌표++)for(unsigned okuxhumanisa_u_x=가로;okuxhumanisa_u_x<가로+32&&okuxhumanisa_u_x<너비;okuxhumanisa_u_x++)inani=(inani^보드화면읽기(okuxhumanisa_u_x,세로좌표))*16777619u;
    return inani;
}
static void 화면요청(const unsigned char *자료위치){
    요청가로=읽기16(자료위치+2);요청세로=읽기16(자료위치+4);요청폭=읽기16(자료위치+6);요청높이=읽기16(자료위치+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    타일수=타일자리=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned okuxhumanisa_u_x=요청가로/32;okuxhumanisa_u_x<=(요청가로+요청폭-1)/32;okuxhumanisa_u_x++){
        unsigned 자리=세로좌표*60+okuxhumanisa_u_x;uint32_t isifinyezo_inani=I_tile_isifinyezo(okuxhumanisa_u_x*32,세로좌표*16);
        if(!자료위치[1]||지난요약[자리]!=isifinyezo_inani)바뀐타일[타일수++]=자리;
    }
    출력[0]=출력[1]=0;bhala_16(출력+2,타일수);출력수=4;보낸수=0;
}
static void Thumela_I_tile(void){
    unsigned 자리=바뀐타일[타일자리++],가로=(자리%60)*32,세로=(자리/60)*16;
    unsigned 끝가로=가로+32,끝세로=세로+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&세로>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[자리]=I_tile_isifinyezo(가로,세로);
    if(가로<요청가로)가로=요청가로;if(세로<요청세로)세로=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    bhala_16(출력,가로);bhala_16(출력+2,세로);bhala_16(출력+4,끝가로-가로);bhala_16(출력+6,끝세로-세로);bhala_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=세로;세로좌표<끝세로;세로좌표++)for(unsigned okuxhumanisa_u_x=가로;okuxhumanisa_u_x<끝가로;okuxhumanisa_u_x++){
        uint32_t 색=보드화면읽기(okuxhumanisa_u_x,세로좌표),inani=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<i_pel_linganisa;순번++)출력[출력수++]=inani>>(8*(큰끝?i_pel_linganisa-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(untanga_inani<0){if(보드밀리초()<다시받을때)return;untanga_inani=망연결받기(듣는곳);if(untanga_inani<0)return;
        접속시각=보드밀리초();isigaba_inani_29ee1bb7=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        i_pel_linganisa=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(isigaba_inani_29ee1bb7<5&&보드밀리초()-접속시각>15000){Vala();return;}
    if(출력수){int 수=통신쓰기(untanga_inani,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Vala();return;}}
    if(!출력수&&닫을예정){Vala();return;}
    if(!출력수&&타일자리<타일수)Thumela_I_tile();
    if(입력수==sizeof(입력)){Vala();return;}
    int 받은수=통신읽기(untanga_inani,입력+입력수,sizeof(입력)-입력수);
    if(받은수==0||(받은수<0&&받은수!=-11)){Vala();return;}if(받은수>0)입력수+=받은수;
    if(출력수||타일자리<타일수)return;
    if(isigaba_inani_29ee1bb7==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Vala();return;}소비(12);const unsigned char i_auth_method[]={1,2};내보내기(i_auth_method,2);isigaba_inani_29ee1bb7=2;return;}
    if(isigaba_inani_29ee1bb7==2&&입력수){if(입력[0]!=2||원격난수(inselele_inani,16)){Vala();return;}소비(1);내보내기(inselele_inani,16);isigaba_inani_29ee1bb7=3;return;}
    if(isigaba_inani_29ee1bb7==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys iphasiwedi_inani;
        for(unsigned 순번=0;순번<8;순번++){unsigned inani=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(inani&1);inani>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&iphasiwedi_inani,열쇠,8);memcpy(정답,inselele_inani,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char i_vector_inani[8]={0};br_des_ct_cbcenc_run(&iphasiwedi_inani,i_vector_inani,정답+순번,8);memset(i_vector_inani,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&iphasiwedi_inani,0,sizeof(iphasiwedi_inani));memset(열쇠,0,8);memset(정답,0,16);memset(inselele_inani,0,16);
        bhala_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){bhala_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else isigaba_inani_29ee1bb7=4;return;}
    if(isigaba_inani_29ee1bb7==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Vala();return;}
        if(!보드터미널(7)){const unsigned char isigameko[]={30,2,1,0,0,0,0};원격입력넣기(isigameko,7);}
        memset(출력,0,40);bhala_16(출력,너비);bhala_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        bhala_16(출력+8,255);bhala_16(출력+10,255);bhala_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Igama="jkoros native";bhala_32(출력+20,strlen(Igama));memcpy(출력+24,Igama,strlen(Igama));출력수=24+strlen(Igama);보낸수=0;isigaba_inani_29ee1bb7=5;return;}
    if(isigaba_inani_29ee1bb7!=5||!입력수)return;
    unsigned thayipha_umunxa=입력[0],필요=thayipha_umunxa==0?20:thayipha_umunxa==2?4:thayipha_umunxa==3?10:thayipha_umunxa==4?8:thayipha_umunxa==5?6:thayipha_umunxa==6?8:0;
    if(!필요){Vala();return;}if(입력수<필요)return;
    if(thayipha_umunxa==2){unsigned 수=읽기16(입력+2);if(수>128){Vala();return;}필요+=수*4;}
    if(thayipha_umunxa==6){unsigned 수=읽기32(입력+4);if(수>4096){Vala();return;}필요+=수;}
    if(입력수<필요)return;
    if(thayipha_umunxa==0){unsigned ibhithi_inani=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((ibhithi_inani!=16&&ibhithi_inani!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<ibhithi_inani)-1)||((uint64_t)초<<초이)>((1ull<<ibhithi_inani)-1)||((uint64_t)파<<파이)>((1ull<<ibhithi_inani)-1)){Vala();return;}
        i_pel_linganisa=ibhithi_inani/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(thayipha_umunxa==3)화면요청(입력);
    else if(thayipha_umunxa==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(thayipha_umunxa==5){unsigned okuxhumanisa_u_x=읽기16(입력+2),세로좌표=읽기16(입력+4);if(okuxhumanisa_u_x>=너비)okuxhumanisa_u_x=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char isigameko[]={30,1,입력[1],okuxhumanisa_u_x&255,okuxhumanisa_u_x>>8,세로좌표&255,세로좌표>>8};원격입력넣기(isigameko,sizeof(isigameko));}
    소비(필요);
}
