/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Conectează, 제한된 입력 lungime_VALUE, 비동기 trimite_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 date 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "la_distanță_VALUE.h"
#include "criptografie_suport.h"
#include "Profil.h"
#include "../rețea_Teanc/rețea_Teanc.h"
#include "../mașină/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Avizier_Terminal(uintptr_t);
void la_distanță_Cheie_Urmă_de_cerneală(unsigned,int);
void 원격글쇠초기화(void);
void comitere_la_distanță_Cheie(void);
static int Ascult_participant=-1,pereche_VALUE=-1,fază_VALUE,닫을예정;
static uintptr_t conexiune_oră,다시받을때;
static unsigned char 입력[8192],Rezultat[4096],verificare_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,element_imagine_dimensiona=4,big_endian_VALUE,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t Anteriorul_rezumat[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned dală_COUNT,dală_poziție,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *date_poziție){return(unsigned)date_poziție[0]*256+date_poziție[1];}
static uint32_t 읽기32(const unsigned char *date_poziție){return(uint32_t)date_poziție[0]<<24|(uint32_t)date_poziție[1]<<16|(uint32_t)date_poziție[2]<<8|date_poziție[3];}
static void scriere_16(unsigned char *date_poziție,unsigned VALUE){date_poziție[0]=VALUE>>8;date_poziție[1]=VALUE;}
static void scriere_32(unsigned char *date_poziție,uint32_t VALUE){date_poziție[0]=VALUE>>24;date_poziție[1]=VALUE>>16;date_poziție[2]=VALUE>>8;date_poziție[3]=VALUE;}
static void Închide(void){if(pereche_VALUE>=0)închide_rețea(pereche_VALUE);pereche_VALUE=-1;fază_VALUE=0;입력수=출력수=보낸수=0;dală_COUNT=dală_poziție=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *date,unsigned 수){memcpy(Rezultat,date,수);출력수=수;보낸수=0;}
static void consum_VALUE(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int control_la_distanță_afișa(unsigned Acțiuni){
    if(Acțiuni==0){Închide();if(Ascult_participant>=0)închide_rețea(Ascult_participant);Ascult_participant=-1;return 0;}
    if(Acțiuni!=1)return Ascult_participant>=0;
    if(Ascult_participant>=0)return 0;
    int muta_VALUE=통신끝점만들기(1);if(muta_VALUE<0)return muta_VALUE;통신주소재사용(muta_VALUE);
    int KR=NET_BIND(muta_VALUE,0,5900);if(!KR)KR=NET_asculta(muta_VALUE);
    if(KR<0){închide_rețea(muta_VALUE);return KR;}Ascult_participant=muta_VALUE;return 0;
}
static uint32_t dală_rezumat(unsigned 가로,unsigned Verticală_poziție){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=Verticală_poziție;세로좌표<Verticală_poziție+16&&세로좌표<높이;세로좌표++)for(unsigned coordonata_X=가로;coordonata_X<가로+32&&coordonata_X<너비;coordonata_X++)VALUE=(VALUE^보드화면읽기(coordonata_X,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *date_poziție){
    요청가로=읽기16(date_poziție+2);요청세로=읽기16(date_poziție+4);요청폭=읽기16(date_poziție+6);요청높이=읽기16(date_poziție+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    dală_COUNT=dală_poziție=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned coordonata_X=요청가로/32;coordonata_X<=(요청가로+요청폭-1)/32;coordonata_X++){
        unsigned index_de_poziție=세로좌표*60+coordonata_X;uint32_t rezumat_VALUE=dală_rezumat(coordonata_X*32,세로좌표*16);
        if(!date_poziție[1]||Anteriorul_rezumat[index_de_poziție]!=rezumat_VALUE)바뀐타일[dală_COUNT++]=index_de_poziție;
    }
    Rezultat[0]=Rezultat[1]=0;scriere_16(Rezultat+2,dală_COUNT);출력수=4;보낸수=0;
}
static void trimite_dală(void){
    unsigned index_de_poziție=바뀐타일[dală_poziție++],가로=(index_de_poziție%60)*32,Verticală_poziție=(index_de_poziție/60)*16;
    unsigned termina_un_apel_X=가로+32,termina_un_apel_Y=Verticală_poziție+16;if(termina_un_apel_X>너비)termina_un_apel_X=너비;if(termina_un_apel_Y>높이)termina_un_apel_Y=높이;
    /* 부분 타일 cerere 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Verticală_poziție>=요청세로&&termina_un_apel_X<=요청가로+요청폭&&termina_un_apel_Y<=요청세로+요청높이;
    if(전부)Anteriorul_rezumat[index_de_poziție]=dală_rezumat(가로,Verticală_poziție);
    if(가로<요청가로)가로=요청가로;if(Verticală_poziție<요청세로)Verticală_poziție=요청세로;
    if(termina_un_apel_X>요청가로+요청폭)termina_un_apel_X=요청가로+요청폭;if(termina_un_apel_Y>요청세로+요청높이)termina_un_apel_Y=요청세로+요청높이;
    scriere_16(Rezultat,가로);scriere_16(Rezultat+2,Verticală_poziție);scriere_16(Rezultat+4,termina_un_apel_X-가로);scriere_16(Rezultat+6,termina_un_apel_Y-Verticală_poziție);scriere_32(Rezultat+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=Verticală_poziție;세로좌표<termina_un_apel_Y;세로좌표++)for(unsigned coordonata_X=가로;coordonata_X<termina_un_apel_X;coordonata_X++){
        uint32_t 색=보드화면읽기(coordonata_X,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<element_imagine_dimensiona;순번++)Rezultat[출력수++]=VALUE>>(8*(big_endian_VALUE?element_imagine_dimensiona-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Ascult_participant<0)return;
    if(pereche_VALUE<0){if(보드밀리초()<다시받을때)return;pereche_VALUE=NET_accepta(Ascult_participant);if(pereche_VALUE<0)return;
        conexiune_oră=보드밀리초();fază_VALUE=1;내보내기("RFB 003.008\n",12);memset(Anteriorul_rezumat,0,sizeof(Anteriorul_rezumat));
        element_imagine_dimensiona=4;big_endian_VALUE=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(fază_VALUE<5&&보드밀리초()-conexiune_oră>15000){Închide();return;}
    if(출력수){int 수=NET_scriere(pereche_VALUE,Rezultat+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Închide();return;}}
    if(!출력수&&닫을예정){Închide();return;}
    if(!출력수&&dală_poziție<dală_COUNT)trimite_dală();
    if(입력수==sizeof(입력)){Închide();return;}
    int RECEIVED_COUNT=통신읽기(pereche_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Închide();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||dală_poziție<dală_COUNT)return;
    if(fază_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Închide();return;}consum_VALUE(12);const unsigned char metodă_de_autorizare[]={1,2};내보내기(metodă_de_autorizare,2);fază_VALUE=2;return;}
    if(fază_VALUE==2&&입력수){if(입력[0]!=2||la_distanță_aleator(verificare_VALUE,16)){Închide();return;}consum_VALUE(1);내보내기(verificare_VALUE,16);fază_VALUE=3;return;}
    if(fază_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys parolă_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&parolă_VALUE,열쇠,8);memcpy(정답,verificare_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vector_VALUE[8]={0};br_des_ct_cbcenc_run(&parolă_VALUE,vector_VALUE,정답+순번,8);memset(vector_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];consum_VALUE(16);memset(&parolă_VALUE,0,sizeof(parolă_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(verificare_VALUE,0,16);
        scriere_32(Rezultat,차이?1:0);출력수=4;보낸수=0;
        if(차이){scriere_32(Rezultat+4,19);memcpy(Rezultat+8,"Authentication fail",19);출력수=27;닫을예정=1;}else fază_VALUE=4;return;}
    if(fază_VALUE==4&&입력수){consum_VALUE(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Închide();return;}
        if(!Avizier_Terminal(7)){const unsigned char Eveniment[]={30,2,1,0,0,0,0};원격입력넣기(Eveniment,7);}
        memset(Rezultat,0,40);scriere_16(Rezultat,너비);scriere_16(Rezultat+2,높이);Rezultat[4]=32;Rezultat[5]=24;Rezultat[7]=1;
        scriere_16(Rezultat+8,255);scriere_16(Rezultat+10,255);scriere_16(Rezultat+12,255);Rezultat[14]=16;Rezultat[15]=8;
        const char *Nume="jkoros native";scriere_32(Rezultat+20,strlen(Nume));memcpy(Rezultat+24,Nume,strlen(Nume));출력수=24+strlen(Nume);보낸수=0;fază_VALUE=5;return;}
    if(fază_VALUE!=5||!입력수)return;
    unsigned Tip_zonă=입력[0],필요=Tip_zonă==0?20:Tip_zonă==2?4:Tip_zonă==3?10:Tip_zonă==4?8:Tip_zonă==5?6:Tip_zonă==6?8:0;
    if(!필요){Închide();return;}if(입력수<필요)return;
    if(Tip_zonă==2){unsigned 수=읽기16(입력+2);if(수>128){Închide();return;}필요+=수*4;}
    if(Tip_zonă==6){unsigned 수=읽기32(입력+4);if(수>4096){Închide();return;}필요+=수;}
    if(입력수<필요)return;
    if(Tip_zonă==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){Închide();return;}
        element_imagine_dimensiona=bit_VALUE/8;big_endian_VALUE=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(Anteriorul_rezumat,0,sizeof(Anteriorul_rezumat));
    }else if(Tip_zonă==3)화면요청(입력);
    else if(Tip_zonă==4)la_distanță_Cheie_Urmă_de_cerneală(읽기32(입력+4),입력[1]!=0);
    else if(Tip_zonă==5){unsigned coordonata_X=읽기16(입력+2),세로좌표=읽기16(입력+4);if(coordonata_X>=너비)coordonata_X=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])comitere_la_distanță_Cheie();
        unsigned char Eveniment[]={30,1,입력[1],coordonata_X&255,coordonata_X>>8,세로좌표&255,세로좌표>>8};원격입력넣기(Eveniment,sizeof(Eveniment));}
    consum_VALUE(필요);
}
