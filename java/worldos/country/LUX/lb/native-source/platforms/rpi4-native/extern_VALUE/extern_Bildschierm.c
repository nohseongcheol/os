/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Verbannen, 제한된 입력 Längt_VALUE, 비동기 mailen_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 Daten 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "extern_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Reseau_Stapel/Reseau_Stapel.h"
#include "../Computer/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Board_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,Peer_VALUE=-1,Phas_VALUE,닫을예정;
static uintptr_t Verbindung_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],Opfuerderung_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,Pel_d_Gréisst_veränneren=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned Deel_COUNT,Deel_positionéieren,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *Daten_positionéieren){return(unsigned)Daten_positionéieren[0]*256+Daten_positionéieren[1];}
static uint32_t 읽기32(const unsigned char *Daten_positionéieren){return(uint32_t)Daten_positionéieren[0]<<24|(uint32_t)Daten_positionéieren[1]<<16|(uint32_t)Daten_positionéieren[2]<<8|Daten_positionéieren[3];}
static void schreiwen_16(unsigned char *Daten_positionéieren,unsigned VALUE){Daten_positionéieren[0]=VALUE>>8;Daten_positionéieren[1]=VALUE;}
static void schreiwen_32(unsigned char *Daten_positionéieren,uint32_t VALUE){Daten_positionéieren[0]=VALUE>>24;Daten_positionéieren[1]=VALUE>>16;Daten_positionéieren[2]=VALUE>>8;Daten_positionéieren[3]=VALUE;}
static void Clôture(void){if(Peer_VALUE>=0)Clôture_Reseau(Peer_VALUE);Peer_VALUE=-1;Phas_VALUE=0;입력수=출력수=보낸수=0;Deel_COUNT=Deel_positionéieren=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *Daten,unsigned 수){memcpy(출력,Daten,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int Kontroll_extern_Bildschierm(unsigned Aktioun){
    if(Aktioun==0){Clôture();if(듣는곳>=0)Clôture_Reseau(듣는곳);듣는곳=-1;return 0;}
    if(Aktioun!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int Port_VALUE=통신끝점만들기(1);if(Port_VALUE<0)return Port_VALUE;통신주소재사용(Port_VALUE);
    int Mooss=망주소묶기(Port_VALUE,0,5900);if(!Mooss)Mooss=연결기다리기(Port_VALUE);
    if(Mooss<0){Clôture_Reseau(Port_VALUE);return Mooss;}듣는곳=Port_VALUE;return 0;
}
static uint32_t Deel_Zesummefaassung(unsigned 가로,unsigned Vertikal_positionéieren){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=Vertikal_positionéieren;세로좌표<Vertikal_positionéieren+16&&세로좌표<높이;세로좌표++)for(unsigned X_Koordinat=가로;X_Koordinat<가로+32&&X_Koordinat<너비;X_Koordinat++)VALUE=(VALUE^보드화면읽기(X_Koordinat,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *Daten_positionéieren){
    요청가로=읽기16(Daten_positionéieren+2);요청세로=읽기16(Daten_positionéieren+4);요청폭=읽기16(Daten_positionéieren+6);요청높이=읽기16(Daten_positionéieren+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    Deel_COUNT=Deel_positionéieren=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned X_Koordinat=요청가로/32;X_Koordinat<=(요청가로+요청폭-1)/32;X_Koordinat++){
        unsigned positionéieren_INDEX=세로좌표*60+X_Koordinat;uint32_t Zesummefaassung_VALUE=Deel_Zesummefaassung(X_Koordinat*32,세로좌표*16);
        if(!Daten_positionéieren[1]||지난요약[positionéieren_INDEX]!=Zesummefaassung_VALUE)바뀐타일[Deel_COUNT++]=positionéieren_INDEX;
    }
    출력[0]=출력[1]=0;schreiwen_16(출력+2,Deel_COUNT);출력수=4;보낸수=0;
}
static void mailen_Deel(void){
    unsigned positionéieren_INDEX=바뀐타일[Deel_positionéieren++],가로=(positionéieren_INDEX%60)*32,Vertikal_positionéieren=(positionéieren_INDEX/60)*16;
    unsigned 끝가로=가로+32,끝세로=Vertikal_positionéieren+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Vertikal_positionéieren>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[positionéieren_INDEX]=Deel_Zesummefaassung(가로,Vertikal_positionéieren);
    if(가로<요청가로)가로=요청가로;if(Vertikal_positionéieren<요청세로)Vertikal_positionéieren=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    schreiwen_16(출력,가로);schreiwen_16(출력+2,Vertikal_positionéieren);schreiwen_16(출력+4,끝가로-가로);schreiwen_16(출력+6,끝세로-Vertikal_positionéieren);schreiwen_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=Vertikal_positionéieren;세로좌표<끝세로;세로좌표++)for(unsigned X_Koordinat=가로;X_Koordinat<끝가로;X_Koordinat++){
        uint32_t 색=보드화면읽기(X_Koordinat,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<Pel_d_Gréisst_veränneren;순번++)출력[출력수++]=VALUE>>(8*(큰끝?Pel_d_Gréisst_veränneren-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(Peer_VALUE<0){if(보드밀리초()<다시받을때)return;Peer_VALUE=망연결받기(듣는곳);if(Peer_VALUE<0)return;
        Verbindung_TIME=보드밀리초();Phas_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        Pel_d_Gréisst_veränneren=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(Phas_VALUE<5&&보드밀리초()-Verbindung_TIME>15000){Clôture();return;}
    if(출력수){int 수=통신쓰기(Peer_VALUE,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Clôture();return;}}
    if(!출력수&&닫을예정){Clôture();return;}
    if(!출력수&&Deel_positionéieren<Deel_COUNT)mailen_Deel();
    if(입력수==sizeof(입력)){Clôture();return;}
    int RECEIVED_COUNT=통신읽기(Peer_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Clôture();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||Deel_positionéieren<Deel_COUNT)return;
    if(Phas_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Clôture();return;}소비(12);const unsigned char Authentifizéierungsmethod[]={1,2};내보내기(Authentifizéierungsmethod,2);Phas_VALUE=2;return;}
    if(Phas_VALUE==2&&입력수){if(입력[0]!=2||원격난수(Opfuerderung_VALUE,16)){Clôture();return;}소비(1);내보내기(Opfuerderung_VALUE,16);Phas_VALUE=3;return;}
    if(Phas_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys Passwuert_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&Passwuert_VALUE,열쇠,8);memcpy(정답,Opfuerderung_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char Vecteur_VALUE[8]={0};br_des_ct_cbcenc_run(&Passwuert_VALUE,Vecteur_VALUE,정답+순번,8);memset(Vecteur_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&Passwuert_VALUE,0,sizeof(Passwuert_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(Opfuerderung_VALUE,0,16);
        schreiwen_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){schreiwen_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else Phas_VALUE=4;return;}
    if(Phas_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Clôture();return;}
        if(!Board_Terminal(7)){const unsigned char Evenement[]={30,2,1,0,0,0,0};원격입력넣기(Evenement,7);}
        memset(출력,0,40);schreiwen_16(출력,너비);schreiwen_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        schreiwen_16(출력+8,255);schreiwen_16(출력+10,255);schreiwen_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Numm="jkoros native";schreiwen_32(출력+20,strlen(Numm));memcpy(출력+24,Numm,strlen(Numm));출력수=24+strlen(Numm);보낸수=0;Phas_VALUE=5;return;}
    if(Phas_VALUE!=5||!입력수)return;
    unsigned TYPE_Kategorie=입력[0],필요=TYPE_Kategorie==0?20:TYPE_Kategorie==2?4:TYPE_Kategorie==3?10:TYPE_Kategorie==4?8:TYPE_Kategorie==5?6:TYPE_Kategorie==6?8:0;
    if(!필요){Clôture();return;}if(입력수<필요)return;
    if(TYPE_Kategorie==2){unsigned 수=읽기16(입력+2);if(수>128){Clôture();return;}필요+=수*4;}
    if(TYPE_Kategorie==6){unsigned 수=읽기32(입력+4);if(수>4096){Clôture();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_Kategorie==0){unsigned Bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((Bit_VALUE!=16&&Bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<Bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<Bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<Bit_VALUE)-1)){Clôture();return;}
        Pel_d_Gréisst_veränneren=Bit_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_Kategorie==3)화면요청(입력);
    else if(TYPE_Kategorie==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_Kategorie==5){unsigned X_Koordinat=읽기16(입력+2),세로좌표=읽기16(입력+4);if(X_Koordinat>=너비)X_Koordinat=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char Evenement[]={30,1,입력[1],X_Koordinat&255,X_Koordinat>>8,세로좌표&255,세로좌표>>8};원격입력넣기(Evenement,sizeof(Evenement));}
    소비(필요);
}
