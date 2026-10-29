/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Konektatu, 제한된 입력 luzera_balio, 비동기 bidali_balio, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 datuak 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "urruneko_balio.h"
#include "암호기반.h"
#include "profil.h"
#include "../sare_pila/sare_pila.h"
#include "../gailu/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t arbel_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int Entzuten_amaiera_puntu=-1,pareko_balio=-1,fase_balio,닫을예정;
static uintptr_t konexio_ordua,다시받을때;
static unsigned char 입력[8192],Irteera[4096],erronka_balio[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,화소크기=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned lauza_ZENBATU,lauza_kargu,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *datuak_kargu){return(unsigned)datuak_kargu[0]*256+datuak_kargu[1];}
static uint32_t 읽기32(const unsigned char *datuak_kargu){return(uint32_t)datuak_kargu[0]<<24|(uint32_t)datuak_kargu[1]<<16|(uint32_t)datuak_kargu[2]<<8|datuak_kargu[3];}
static void idatzi_16(unsigned char *datuak_kargu,unsigned balio){datuak_kargu[0]=balio>>8;datuak_kargu[1]=balio;}
static void idatzi_32(unsigned char *datuak_kargu,uint32_t balio){datuak_kargu[0]=balio>>24;datuak_kargu[1]=balio>>16;datuak_kargu[2]=balio>>8;datuak_kargu[3]=balio;}
static void Itxi(void){if(pareko_balio>=0)itxi_sare(pareko_balio);pareko_balio=-1;fase_balio=0;입력수=출력수=보낸수=0;lauza_ZENBATU=lauza_kargu=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *datuak,unsigned 수){memcpy(Irteera,datuak,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int kontrol_urruneko_pantaila(unsigned Ekintza){
    if(Ekintza==0){Itxi();if(Entzuten_amaiera_puntu>=0)itxi_sare(Entzuten_amaiera_puntu);Entzuten_amaiera_puntu=-1;return 0;}
    if(Ekintza!=1)return Entzuten_amaiera_puntu>=0;
    if(Entzuten_amaiera_puntu>=0)return 0;
    int ataka_balio=통신끝점만들기(1);if(ataka_balio<0)return ataka_balio;통신주소재사용(ataka_balio);
    int EMAITZA=망주소묶기(ataka_balio,0,5900);if(!EMAITZA)EMAITZA=연결기다리기(ataka_balio);
    if(EMAITZA<0){itxi_sare(ataka_balio);return EMAITZA;}Entzuten_amaiera_puntu=ataka_balio;return 0;
}
static uint32_t 타일요약(unsigned 가로,unsigned Bertikala_kargu){
    uint32_t balio=2166136261u;
    for(unsigned Y_koordenatu=Bertikala_kargu;Y_koordenatu<Bertikala_kargu+16&&Y_koordenatu<높이;Y_koordenatu++)for(unsigned X_koordenatu=가로;X_koordenatu<가로+32&&X_koordenatu<너비;X_koordenatu++)balio=(balio^보드화면읽기(X_koordenatu,Y_koordenatu))*16777619u;
    return balio;
}
static void 화면요청(const unsigned char *datuak_kargu){
    요청가로=읽기16(datuak_kargu+2);요청세로=읽기16(datuak_kargu+4);요청폭=읽기16(datuak_kargu+6);요청높이=읽기16(datuak_kargu+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    lauza_ZENBATU=lauza_kargu=0;
    if(요청폭&&요청높이)for(unsigned Y_koordenatu=요청세로/16;Y_koordenatu<=(요청세로+요청높이-1)/16;Y_koordenatu++)for(unsigned X_koordenatu=요청가로/32;X_koordenatu<=(요청가로+요청폭-1)/32;X_koordenatu++){
        unsigned kargu_INDIZE=Y_koordenatu*60+X_koordenatu;uint32_t 요약=타일요약(X_koordenatu*32,Y_koordenatu*16);
        if(!datuak_kargu[1]||지난요약[kargu_INDIZE]!=요약)바뀐타일[lauza_ZENBATU++]=kargu_INDIZE;
    }
    Irteera[0]=Irteera[1]=0;idatzi_16(Irteera+2,lauza_ZENBATU);출력수=4;보낸수=0;
}
static void bidali_lauza(void){
    unsigned kargu_INDIZE=바뀐타일[lauza_kargu++],가로=(kargu_INDIZE%60)*32,Bertikala_kargu=(kargu_INDIZE/60)*16;
    unsigned amaitu_X=가로+32,amaitu_Y=Bertikala_kargu+16;if(amaitu_X>너비)amaitu_X=너비;if(amaitu_Y>높이)amaitu_Y=높이;
    /* 부분 타일 eskaera 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Bertikala_kargu>=요청세로&&amaitu_X<=요청가로+요청폭&&amaitu_Y<=요청세로+요청높이;
    if(전부)지난요약[kargu_INDIZE]=타일요약(가로,Bertikala_kargu);
    if(가로<요청가로)가로=요청가로;if(Bertikala_kargu<요청세로)Bertikala_kargu=요청세로;
    if(amaitu_X>요청가로+요청폭)amaitu_X=요청가로+요청폭;if(amaitu_Y>요청세로+요청높이)amaitu_Y=요청세로+요청높이;
    idatzi_16(Irteera,가로);idatzi_16(Irteera+2,Bertikala_kargu);idatzi_16(Irteera+4,amaitu_X-가로);idatzi_16(Irteera+6,amaitu_Y-Bertikala_kargu);idatzi_32(Irteera+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_koordenatu=Bertikala_kargu;Y_koordenatu<amaitu_Y;Y_koordenatu++)for(unsigned X_koordenatu=가로;X_koordenatu<amaitu_X;X_koordenatu++){
        uint32_t 색=보드화면읽기(X_koordenatu,Y_koordenatu),balio=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<화소크기;순번++)Irteera[출력수++]=balio>>(8*(큰끝?화소크기-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Entzuten_amaiera_puntu<0)return;
    if(pareko_balio<0){if(보드밀리초()<다시받을때)return;pareko_balio=망연결받기(Entzuten_amaiera_puntu);if(pareko_balio<0)return;
        konexio_ordua=보드밀리초();fase_balio=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        화소크기=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(fase_balio<5&&보드밀리초()-konexio_ordua>15000){Itxi();return;}
    if(출력수){int 수=통신쓰기(pareko_balio,Irteera+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Itxi();return;}}
    if(!출력수&&닫을예정){Itxi();return;}
    if(!출력수&&lauza_kargu<lauza_ZENBATU)bidali_lauza();
    if(입력수==sizeof(입력)){Itxi();return;}
    int RECEIVED_ZENBATU=통신읽기(pareko_balio,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_ZENBATU==0||(RECEIVED_ZENBATU<0&&RECEIVED_ZENBATU!=-11)){Itxi();return;}if(RECEIVED_ZENBATU>0)입력수+=RECEIVED_ZENBATU;
    if(출력수||lauza_kargu<lauza_ZENBATU)return;
    if(fase_balio==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Itxi();return;}소비(12);const unsigned char autentif_metodo[]={1,2};내보내기(autentif_metodo,2);fase_balio=2;return;}
    if(fase_balio==2&&입력수){if(입력[0]!=2||원격난수(erronka_balio,16)){Itxi();return;}소비(1);내보내기(erronka_balio,16);fase_balio=3;return;}
    if(fase_balio==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys pasahitz_balio;
        for(unsigned 순번=0;순번<8;순번++){unsigned balio=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(balio&1);balio>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&pasahitz_balio,열쇠,8);memcpy(정답,erronka_balio,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char bektore_balio[8]={0};br_des_ct_cbcenc_run(&pasahitz_balio,bektore_balio,정답+순번,8);memset(bektore_balio,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&pasahitz_balio,0,sizeof(pasahitz_balio));memset(열쇠,0,8);memset(정답,0,16);memset(erronka_balio,0,16);
        idatzi_32(Irteera,차이?1:0);출력수=4;보낸수=0;
        if(차이){idatzi_32(Irteera+4,19);memcpy(Irteera+8,"Authentication fail",19);출력수=27;닫을예정=1;}else fase_balio=4;return;}
    if(fase_balio==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Itxi();return;}
        if(!arbel_Terminal(7)){const unsigned char Gertaera[]={30,2,1,0,0,0,0};원격입력넣기(Gertaera,7);}
        memset(Irteera,0,40);idatzi_16(Irteera,너비);idatzi_16(Irteera+2,높이);Irteera[4]=32;Irteera[5]=24;Irteera[7]=1;
        idatzi_16(Irteera+8,255);idatzi_16(Irteera+10,255);idatzi_16(Irteera+12,255);Irteera[14]=16;Irteera[15]=8;
        const char *Izena="jkoros native";idatzi_32(Irteera+20,strlen(Izena));memcpy(Irteera+24,Izena,strlen(Izena));출력수=24+strlen(Izena);보낸수=0;fase_balio=5;return;}
    if(fase_balio!=5||!입력수)return;
    unsigned MOTA_Kategoria=입력[0],필요=MOTA_Kategoria==0?20:MOTA_Kategoria==2?4:MOTA_Kategoria==3?10:MOTA_Kategoria==4?8:MOTA_Kategoria==5?6:MOTA_Kategoria==6?8:0;
    if(!필요){Itxi();return;}if(입력수<필요)return;
    if(MOTA_Kategoria==2){unsigned 수=읽기16(입력+2);if(수>128){Itxi();return;}필요+=수*4;}
    if(MOTA_Kategoria==6){unsigned 수=읽기32(입력+4);if(수>4096){Itxi();return;}필요+=수;}
    if(입력수<필요)return;
    if(MOTA_Kategoria==0){unsigned bit_balio=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_balio!=16&&bit_balio!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_balio)-1)||((uint64_t)초<<초이)>((1ull<<bit_balio)-1)||((uint64_t)파<<파이)>((1ull<<bit_balio)-1)){Itxi();return;}
        화소크기=bit_balio/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(MOTA_Kategoria==3)화면요청(입력);
    else if(MOTA_Kategoria==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(MOTA_Kategoria==5){unsigned X_koordenatu=읽기16(입력+2),Y_koordenatu=읽기16(입력+4);if(X_koordenatu>=너비)X_koordenatu=너비-1;if(Y_koordenatu>=높이)Y_koordenatu=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char Gertaera[]={30,1,입력[1],X_koordenatu&255,X_koordenatu>>8,Y_koordenatu&255,Y_koordenatu>>8};원격입력넣기(Gertaera,sizeof(Gertaera));}
    소비(필요);
}
