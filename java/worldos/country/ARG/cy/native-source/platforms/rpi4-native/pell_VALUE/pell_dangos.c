/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Cysylltu, 제한된 입력 hyd_VALUE, 비동기 anfon_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "pell_VALUE.h"
#include "암호기반.h"
#include "Proffil.h"
#include "../Rhwydwaith_pentwr/Rhwydwaith_pentwr.h"
#include "../peiriant/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t bwrdd_Terfynell(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,cymar_VALUE=-1,cam_VALUE,닫을예정;
static uintptr_t cyswllt_TIME,다시받을때;
static unsigned char 입력[8192],Allbwn[4096],her_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pel_newid_maint=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned teitl_COUNT,teitl_safle,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_safle){return(unsigned)data_safle[0]*256+data_safle[1];}
static uint32_t 읽기32(const unsigned char *data_safle){return(uint32_t)data_safle[0]<<24|(uint32_t)data_safle[1]<<16|(uint32_t)data_safle[2]<<8|data_safle[3];}
static void ysgrifennu_16(unsigned char *data_safle,unsigned VALUE){data_safle[0]=VALUE>>8;data_safle[1]=VALUE;}
static void ysgrifennu_32(unsigned char *data_safle,uint32_t VALUE){data_safle[0]=VALUE>>24;data_safle[1]=VALUE>>16;data_safle[2]=VALUE>>8;data_safle[3]=VALUE;}
static void Cau(void){if(cymar_VALUE>=0)cau_Rhwydwaith(cymar_VALUE);cymar_VALUE=-1;cam_VALUE=0;입력수=출력수=보낸수=0;teitl_COUNT=teitl_safle=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(Allbwn,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int rheoli_pell_dangos(unsigned Gweithrediad){
    if(Gweithrediad==0){Cau();if(듣는곳>=0)cau_Rhwydwaith(듣는곳);듣는곳=-1;return 0;}
    if(Gweithrediad!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int porth_VALUE=통신끝점만들기(1);if(porth_VALUE<0)return porth_VALUE;통신주소재사용(porth_VALUE);
    int mesur=망주소묶기(porth_VALUE,0,5900);if(!mesur)mesur=연결기다리기(porth_VALUE);
    if(mesur<0){cau_Rhwydwaith(porth_VALUE);return mesur;}듣는곳=porth_VALUE;return 0;
}
static uint32_t teitl_crynodeb(unsigned 가로,unsigned Ar_i_fyny_safle){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_cyfesuryn=Ar_i_fyny_safle;Y_cyfesuryn<Ar_i_fyny_safle+16&&Y_cyfesuryn<높이;Y_cyfesuryn++)for(unsigned cyfesuryn_x=가로;cyfesuryn_x<가로+32&&cyfesuryn_x<너비;cyfesuryn_x++)VALUE=(VALUE^보드화면읽기(cyfesuryn_x,Y_cyfesuryn))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *data_safle){
    요청가로=읽기16(data_safle+2);요청세로=읽기16(data_safle+4);요청폭=읽기16(data_safle+6);요청높이=읽기16(data_safle+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    teitl_COUNT=teitl_safle=0;
    if(요청폭&&요청높이)for(unsigned Y_cyfesuryn=요청세로/16;Y_cyfesuryn<=(요청세로+요청높이-1)/16;Y_cyfesuryn++)for(unsigned cyfesuryn_x=요청가로/32;cyfesuryn_x<=(요청가로+요청폭-1)/32;cyfesuryn_x++){
        unsigned safle_INDEX=Y_cyfesuryn*60+cyfesuryn_x;uint32_t crynodeb_VALUE=teitl_crynodeb(cyfesuryn_x*32,Y_cyfesuryn*16);
        if(!data_safle[1]||지난요약[safle_INDEX]!=crynodeb_VALUE)바뀐타일[teitl_COUNT++]=safle_INDEX;
    }
    Allbwn[0]=Allbwn[1]=0;ysgrifennu_16(Allbwn+2,teitl_COUNT);출력수=4;보낸수=0;
}
static void anfon_teitl(void){
    unsigned safle_INDEX=바뀐타일[teitl_safle++],가로=(safle_INDEX%60)*32,Ar_i_fyny_safle=(safle_INDEX/60)*16;
    unsigned gorffen_X=가로+32,gorffen_Y=Ar_i_fyny_safle+16;if(gorffen_X>너비)gorffen_X=너비;if(gorffen_Y>높이)gorffen_Y=높이;
    /* 부분 타일 cais_HTTP 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Ar_i_fyny_safle>=요청세로&&gorffen_X<=요청가로+요청폭&&gorffen_Y<=요청세로+요청높이;
    if(전부)지난요약[safle_INDEX]=teitl_crynodeb(가로,Ar_i_fyny_safle);
    if(가로<요청가로)가로=요청가로;if(Ar_i_fyny_safle<요청세로)Ar_i_fyny_safle=요청세로;
    if(gorffen_X>요청가로+요청폭)gorffen_X=요청가로+요청폭;if(gorffen_Y>요청세로+요청높이)gorffen_Y=요청세로+요청높이;
    ysgrifennu_16(Allbwn,가로);ysgrifennu_16(Allbwn+2,Ar_i_fyny_safle);ysgrifennu_16(Allbwn+4,gorffen_X-가로);ysgrifennu_16(Allbwn+6,gorffen_Y-Ar_i_fyny_safle);ysgrifennu_32(Allbwn+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_cyfesuryn=Ar_i_fyny_safle;Y_cyfesuryn<gorffen_Y;Y_cyfesuryn++)for(unsigned cyfesuryn_x=가로;cyfesuryn_x<gorffen_X;cyfesuryn_x++){
        uint32_t 색=보드화면읽기(cyfesuryn_x,Y_cyfesuryn),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pel_newid_maint;순번++)Allbwn[출력수++]=VALUE>>(8*(큰끝?pel_newid_maint-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(cymar_VALUE<0){if(보드밀리초()<다시받을때)return;cymar_VALUE=망연결받기(듣는곳);if(cymar_VALUE<0)return;
        cyswllt_TIME=보드밀리초();cam_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pel_newid_maint=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(cam_VALUE<5&&보드밀리초()-cyswllt_TIME>15000){Cau();return;}
    if(출력수){int 수=통신쓰기(cymar_VALUE,Allbwn+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Cau();return;}}
    if(!출력수&&닫을예정){Cau();return;}
    if(!출력수&&teitl_safle<teitl_COUNT)anfon_teitl();
    if(입력수==sizeof(입력)){Cau();return;}
    int RECEIVED_COUNT=통신읽기(cymar_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Cau();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||teitl_safle<teitl_COUNT)return;
    if(cam_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Cau();return;}소비(12);const unsigned char dull_dilysu[]={1,2};내보내기(dull_dilysu,2);cam_VALUE=2;return;}
    if(cam_VALUE==2&&입력수){if(입력[0]!=2||원격난수(her_VALUE,16)){Cau();return;}소비(1);내보내기(her_VALUE,16);cam_VALUE=3;return;}
    if(cam_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys cyfrinair_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&cyfrinair_VALUE,열쇠,8);memcpy(정답,her_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char fector_VALUE[8]={0};br_des_ct_cbcenc_run(&cyfrinair_VALUE,fector_VALUE,정답+순번,8);memset(fector_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&cyfrinair_VALUE,0,sizeof(cyfrinair_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(her_VALUE,0,16);
        ysgrifennu_32(Allbwn,차이?1:0);출력수=4;보낸수=0;
        if(차이){ysgrifennu_32(Allbwn+4,19);memcpy(Allbwn+8,"Authentication fail",19);출력수=27;닫을예정=1;}else cam_VALUE=4;return;}
    if(cam_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Cau();return;}
        if(!bwrdd_Terfynell(7)){const unsigned char digwyddiad[]={30,2,1,0,0,0,0};원격입력넣기(digwyddiad,7);}
        memset(Allbwn,0,40);ysgrifennu_16(Allbwn,너비);ysgrifennu_16(Allbwn+2,높이);Allbwn[4]=32;Allbwn[5]=24;Allbwn[7]=1;
        ysgrifennu_16(Allbwn+8,255);ysgrifennu_16(Allbwn+10,255);ysgrifennu_16(Allbwn+12,255);Allbwn[14]=16;Allbwn[15]=8;
        const char *Enw="jkoros native";ysgrifennu_32(Allbwn+20,strlen(Enw));memcpy(Allbwn+24,Enw,strlen(Enw));출력수=24+strlen(Enw);보낸수=0;cam_VALUE=5;return;}
    if(cam_VALUE!=5||!입력수)return;
    unsigned TYPE_ardal=입력[0],필요=TYPE_ardal==0?20:TYPE_ardal==2?4:TYPE_ardal==3?10:TYPE_ardal==4?8:TYPE_ardal==5?6:TYPE_ardal==6?8:0;
    if(!필요){Cau();return;}if(입력수<필요)return;
    if(TYPE_ardal==2){unsigned 수=읽기16(입력+2);if(수>128){Cau();return;}필요+=수*4;}
    if(TYPE_ardal==6){unsigned 수=읽기32(입력+4);if(수>4096){Cau();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_ardal==0){unsigned did_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((did_VALUE!=16&&did_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<did_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<did_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<did_VALUE)-1)){Cau();return;}
        pel_newid_maint=did_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_ardal==3)화면요청(입력);
    else if(TYPE_ardal==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_ardal==5){unsigned cyfesuryn_x=읽기16(입력+2),Y_cyfesuryn=읽기16(입력+4);if(cyfesuryn_x>=너비)cyfesuryn_x=너비-1;if(Y_cyfesuryn>=높이)Y_cyfesuryn=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char digwyddiad[]={30,1,입력[1],cyfesuryn_x&255,cyfesuryn_x>>8,Y_cyfesuryn&255,Y_cyfesuryn>>8};원격입력넣기(digwyddiad,sizeof(digwyddiad));}
    소비(필요);
}
