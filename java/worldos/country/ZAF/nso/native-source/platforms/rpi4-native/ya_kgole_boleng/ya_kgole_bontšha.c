/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Ikgokaganye, 제한된 입력 botelele_boleng, 비동기 Romela_boleng, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "ya_kgole_boleng.h"
#include "암호기반.h"
#include "Profaele.h"
#include "../Netweke_kgoboko/Netweke_kgoboko.h"
#include "../motšhene/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t 보드터미널(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,sedirišwa_sa_legoro_le_tee_boleng=-1,karolo_boleng_29ee1bb7,닫을예정;
static uintptr_t 접속시각,다시받을때;
static unsigned char 입력[8192],출력[4096],tlhohlo_boleng[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,phele_bogolo=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned 타일수,타일자리,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *자료위치){return(unsigned)자료위치[0]*256+자료위치[1];}
static uint32_t 읽기32(const unsigned char *자료위치){return(uint32_t)자료위치[0]<<24|(uint32_t)자료위치[1]<<16|(uint32_t)자료위치[2]<<8|자료위치[3];}
static void ngwala_16(unsigned char *자료위치,unsigned boleng){자료위치[0]=boleng>>8;자료위치[1]=boleng;}
static void ngwala_32(unsigned char *자료위치,uint32_t boleng){자료위치[0]=boleng>>24;자료위치[1]=boleng>>16;자료위치[2]=boleng>>8;자료위치[3]=boleng;}
static void Tswalela(void){if(sedirišwa_sa_legoro_le_tee_boleng>=0)tswalela_Netweke(sedirišwa_sa_legoro_le_tee_boleng);sedirišwa_sa_legoro_le_tee_boleng=-1;karolo_boleng_29ee1bb7=0;입력수=출력수=보낸수=0;타일수=타일자리=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(출력,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int taolo_ya_kgole_bontšha(unsigned Mogato){
    if(Mogato==0){Tswalela();if(듣는곳>=0)tswalela_Netweke(듣는곳);듣는곳=-1;return 0;}
    if(Mogato!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int phote_boleng=통신끝점만들기(1);if(phote_boleng<0)return phote_boleng;통신주소재사용(phote_boleng);
    int 결과=망주소묶기(phote_boleng,0,5900);if(!결과)결과=연결기다리기(phote_boleng);
    if(결과<0){tswalela_Netweke(phote_boleng);return 결과;}듣는곳=phote_boleng;return 0;
}
static uint32_t thaele_khutsofatšo(unsigned 가로,unsigned 세로){
    uint32_t boleng=2166136261u;
    for(unsigned 세로좌표=세로;세로좌표<세로+16&&세로좌표<높이;세로좌표++)for(unsigned kamano_ya_x=가로;kamano_ya_x<가로+32&&kamano_ya_x<너비;kamano_ya_x++)boleng=(boleng^보드화면읽기(kamano_ya_x,세로좌표))*16777619u;
    return boleng;
}
static void 화면요청(const unsigned char *자료위치){
    요청가로=읽기16(자료위치+2);요청세로=읽기16(자료위치+4);요청폭=읽기16(자료위치+6);요청높이=읽기16(자료위치+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    타일수=타일자리=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned kamano_ya_x=요청가로/32;kamano_ya_x<=(요청가로+요청폭-1)/32;kamano_ya_x++){
        unsigned 자리=세로좌표*60+kamano_ya_x;uint32_t khutsofatšo_boleng=thaele_khutsofatšo(kamano_ya_x*32,세로좌표*16);
        if(!자료위치[1]||지난요약[자리]!=khutsofatšo_boleng)바뀐타일[타일수++]=자리;
    }
    출력[0]=출력[1]=0;ngwala_16(출력+2,타일수);출력수=4;보낸수=0;
}
static void Romela_thaele(void){
    unsigned 자리=바뀐타일[타일자리++],가로=(자리%60)*32,세로=(자리/60)*16;
    unsigned 끝가로=가로+32,끝세로=세로+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&세로>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[자리]=thaele_khutsofatšo(가로,세로);
    if(가로<요청가로)가로=요청가로;if(세로<요청세로)세로=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    ngwala_16(출력,가로);ngwala_16(출력+2,세로);ngwala_16(출력+4,끝가로-가로);ngwala_16(출력+6,끝세로-세로);ngwala_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=세로;세로좌표<끝세로;세로좌표++)for(unsigned kamano_ya_x=가로;kamano_ya_x<끝가로;kamano_ya_x++){
        uint32_t 색=보드화면읽기(kamano_ya_x,세로좌표),boleng=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<phele_bogolo;순번++)출력[출력수++]=boleng>>(8*(큰끝?phele_bogolo-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(sedirišwa_sa_legoro_le_tee_boleng<0){if(보드밀리초()<다시받을때)return;sedirišwa_sa_legoro_le_tee_boleng=망연결받기(듣는곳);if(sedirišwa_sa_legoro_le_tee_boleng<0)return;
        접속시각=보드밀리초();karolo_boleng_29ee1bb7=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        phele_bogolo=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(karolo_boleng_29ee1bb7<5&&보드밀리초()-접속시각>15000){Tswalela();return;}
    if(출력수){int 수=통신쓰기(sedirišwa_sa_legoro_le_tee_boleng,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Tswalela();return;}}
    if(!출력수&&닫을예정){Tswalela();return;}
    if(!출력수&&타일자리<타일수)Romela_thaele();
    if(입력수==sizeof(입력)){Tswalela();return;}
    int 받은수=통신읽기(sedirišwa_sa_legoro_le_tee_boleng,입력+입력수,sizeof(입력)-입력수);
    if(받은수==0||(받은수<0&&받은수!=-11)){Tswalela();return;}if(받은수>0)입력수+=받은수;
    if(출력수||타일자리<타일수)return;
    if(karolo_boleng_29ee1bb7==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Tswalela();return;}소비(12);const unsigned char mokgwa_wa_kgonthišo[]={1,2};내보내기(mokgwa_wa_kgonthišo,2);karolo_boleng_29ee1bb7=2;return;}
    if(karolo_boleng_29ee1bb7==2&&입력수){if(입력[0]!=2||원격난수(tlhohlo_boleng,16)){Tswalela();return;}소비(1);내보내기(tlhohlo_boleng,16);karolo_boleng_29ee1bb7=3;return;}
    if(karolo_boleng_29ee1bb7==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys phasewete_boleng;
        for(unsigned 순번=0;순번<8;순번++){unsigned boleng=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(boleng&1);boleng>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&phasewete_boleng,열쇠,8);memcpy(정답,tlhohlo_boleng,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char bektha_boleng[8]={0};br_des_ct_cbcenc_run(&phasewete_boleng,bektha_boleng,정답+순번,8);memset(bektha_boleng,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&phasewete_boleng,0,sizeof(phasewete_boleng));memset(열쇠,0,8);memset(정답,0,16);memset(tlhohlo_boleng,0,16);
        ngwala_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){ngwala_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else karolo_boleng_29ee1bb7=4;return;}
    if(karolo_boleng_29ee1bb7==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Tswalela();return;}
        if(!보드터미널(7)){const unsigned char tiragalo[]={30,2,1,0,0,0,0};원격입력넣기(tiragalo,7);}
        memset(출력,0,40);ngwala_16(출력,너비);ngwala_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        ngwala_16(출력+8,255);ngwala_16(출력+10,255);ngwala_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Leina="jkoros native";ngwala_32(출력+20,strlen(Leina));memcpy(출력+24,Leina,strlen(Leina));출력수=24+strlen(Leina);보낸수=0;karolo_boleng_29ee1bb7=5;return;}
    if(karolo_boleng_29ee1bb7!=5||!입력수)return;
    unsigned thaepa_legoro=입력[0],필요=thaepa_legoro==0?20:thaepa_legoro==2?4:thaepa_legoro==3?10:thaepa_legoro==4?8:thaepa_legoro==5?6:thaepa_legoro==6?8:0;
    if(!필요){Tswalela();return;}if(입력수<필요)return;
    if(thaepa_legoro==2){unsigned 수=읽기16(입력+2);if(수>128){Tswalela();return;}필요+=수*4;}
    if(thaepa_legoro==6){unsigned 수=읽기32(입력+4);if(수>4096){Tswalela();return;}필요+=수;}
    if(입력수<필요)return;
    if(thaepa_legoro==0){unsigned paente_boleng=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((paente_boleng!=16&&paente_boleng!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<paente_boleng)-1)||((uint64_t)초<<초이)>((1ull<<paente_boleng)-1)||((uint64_t)파<<파이)>((1ull<<paente_boleng)-1)){Tswalela();return;}
        phele_bogolo=paente_boleng/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(thaepa_legoro==3)화면요청(입력);
    else if(thaepa_legoro==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(thaepa_legoro==5){unsigned kamano_ya_x=읽기16(입력+2),세로좌표=읽기16(입력+4);if(kamano_ya_x>=너비)kamano_ya_x=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char tiragalo[]={30,1,입력[1],kamano_ya_x&255,kamano_ya_x>>8,세로좌표&255,세로좌표>>8};원격입력넣기(tiragalo,sizeof(tiragalo));}
    소비(필요);
}
