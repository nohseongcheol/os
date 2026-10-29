/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Connetti, 제한된 input_VALORE durata_VALORE, 비동기 inviare_VALORE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 schermata dati 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "remoto_VALORE.h"
#include "crittografia_Supporto.h"
#include "Profilo.h"
#include "../rete_Pila/rete_Pila.h"
#include "../computer/schermata_info.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(schermata_password)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t scheda_Terminale(uintptr_t);
void remoto_tasto_Tratto(unsigned,int);
void inizializzare_remoto_tasto_Tratto(void);
void commit_remoto_tasto(void);
static int In_ascolto_endpoint=-1,peer_VALORE=-1,area_VALORE_29ee1bb7,닫을예정;
static uintptr_t connessione_time,다시받을때;
static unsigned char input_VALORE[8192],uscitaTesto[4096],test_VALORE[16];
static unsigned input_CONTA_NUMERI,output_CONTA_NUMERI,보낸수;
static unsigned 너비,altezza_VALORE,pixel_ridimensionare=4,big_endian_VALORE,빨강최대=255,초록최대=255,파랑최대=255,rosso_scorrere=16,verde_scorrere=8,blu_scorrere;
static uint32_t Indietro_riepilogo[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned parte_CONTA_NUMERI,parte_funzione,richiesto_X,richiesto_Y,요청폭,richiesto_altezza;
static unsigned 읽기16(const unsigned char *dati_funzione){return(unsigned)dati_funzione[0]*256+dati_funzione[1];}
static uint32_t 읽기32(const unsigned char *dati_funzione){return(uint32_t)dati_funzione[0]<<24|(uint32_t)dati_funzione[1]<<16|(uint32_t)dati_funzione[2]<<8|dati_funzione[3];}
static void scrivere_16(unsigned char *dati_funzione,unsigned VALORE){dati_funzione[0]=VALORE>>8;dati_funzione[1]=VALORE;}
static void scrivere_32(unsigned char *dati_funzione,uint32_t VALORE){dati_funzione[0]=VALORE>>24;dati_funzione[1]=VALORE>>16;dati_funzione[2]=VALORE>>8;dati_funzione[3]=VALORE;}
static void Chiudi(void){if(peer_VALORE>=0)Chiudi_rete(peer_VALORE);peer_VALORE=-1;area_VALORE_29ee1bb7=0;input_CONTA_NUMERI=output_CONTA_NUMERI=보낸수=0;parte_CONTA_NUMERI=parte_funzione=0;닫을예정=0;inizializzare_remoto_tasto_Tratto();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *dati,unsigned numero){memcpy(uscitaTesto,dati,numero);output_CONTA_NUMERI=numero;보낸수=0;}
static void consumo_VALORE(unsigned numero){input_CONTA_NUMERI-=numero;memmove(input_VALORE,input_VALORE+numero,input_CONTA_NUMERI);}
int controllo_remoto_display(unsigned Azione){
    if(Azione==0){Chiudi();if(In_ascolto_endpoint>=0)Chiudi_rete(In_ascolto_endpoint);In_ascolto_endpoint=-1;return 0;}
    if(Azione!=1)return In_ascolto_endpoint>=0;
    if(In_ascolto_endpoint>=0)return 0;
    int porta_VALORE=Crea_socket_endpoint(1);if(porta_VALORE<0)return porta_VALORE;통신주소재사용(porta_VALORE);
    int risultato=NET_BIND(porta_VALORE,0,5900);if(!risultato)risultato=NET_essere_in_ascolto(porta_VALORE);
    if(risultato<0){Chiudi_rete(porta_VALORE);return risultato;}In_ascolto_endpoint=porta_VALORE;return 0;
}
static uint32_t parte_riepilogo(unsigned 가로,unsigned Verticale_funzione){
    uint32_t VALORE=2166136261u;
    for(unsigned Y_coordinata=Verticale_funzione;Y_coordinata<Verticale_funzione+16&&Y_coordinata<altezza_VALORE;Y_coordinata++)for(unsigned coordinata_x=가로;coordinata_x<가로+32&&coordinata_x<너비;coordinata_x++)VALORE=(VALORE^보드화면읽기(coordinata_x,Y_coordinata))*16777619u;
    return VALORE;
}
static void schermata_richiesta(const unsigned char *dati_funzione){
    richiesto_X=읽기16(dati_funzione+2);richiesto_Y=읽기16(dati_funzione+4);요청폭=읽기16(dati_funzione+6);richiesto_altezza=읽기16(dati_funzione+8);
    if(richiesto_X>=너비||richiesto_Y>=altezza_VALORE)요청폭=richiesto_altezza=0;
    if(요청폭>너비-richiesto_X&&richiesto_X<너비)요청폭=너비-richiesto_X;
    if(richiesto_altezza>altezza_VALORE-richiesto_Y&&richiesto_Y<altezza_VALORE)richiesto_altezza=altezza_VALORE-richiesto_Y;
    parte_CONTA_NUMERI=parte_funzione=0;
    if(요청폭&&richiesto_altezza)for(unsigned Y_coordinata=richiesto_Y/16;Y_coordinata<=(richiesto_Y+richiesto_altezza-1)/16;Y_coordinata++)for(unsigned coordinata_x=richiesto_X/32;coordinata_x<=(richiesto_X+요청폭-1)/32;coordinata_x++){
        unsigned funzione_INDICE=Y_coordinata*60+coordinata_x;uint32_t riepilogo_VALORE=parte_riepilogo(coordinata_x*32,Y_coordinata*16);
        if(!dati_funzione[1]||Indietro_riepilogo[funzione_INDICE]!=riepilogo_VALORE)바뀐타일[parte_CONTA_NUMERI++]=funzione_INDICE;
    }
    uscitaTesto[0]=uscitaTesto[1]=0;scrivere_16(uscitaTesto+2,parte_CONTA_NUMERI);output_CONTA_NUMERI=4;보낸수=0;
}
static void inviare_parte(void){
    unsigned funzione_INDICE=바뀐타일[parte_funzione++],가로=(funzione_INDICE%60)*32,Verticale_funzione=(funzione_INDICE/60)*16;
    unsigned chiudere_X=가로+32,chiudere_Y=Verticale_funzione+16;if(chiudere_X>너비)chiudere_X=너비;if(chiudere_Y>altezza_VALORE)chiudere_Y=altezza_VALORE;
    /* 부분 타일 richiesta 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=richiesto_X&&Verticale_funzione>=richiesto_Y&&chiudere_X<=richiesto_X+요청폭&&chiudere_Y<=richiesto_Y+richiesto_altezza;
    if(전부)Indietro_riepilogo[funzione_INDICE]=parte_riepilogo(가로,Verticale_funzione);
    if(가로<richiesto_X)가로=richiesto_X;if(Verticale_funzione<richiesto_Y)Verticale_funzione=richiesto_Y;
    if(chiudere_X>richiesto_X+요청폭)chiudere_X=richiesto_X+요청폭;if(chiudere_Y>richiesto_Y+richiesto_altezza)chiudere_Y=richiesto_Y+richiesto_altezza;
    scrivere_16(uscitaTesto,가로);scrivere_16(uscitaTesto+2,Verticale_funzione);scrivere_16(uscitaTesto+4,chiudere_X-가로);scrivere_16(uscitaTesto+6,chiudere_Y-Verticale_funzione);scrivere_32(uscitaTesto+8,0);
    output_CONTA_NUMERI=12;보낸수=0;
    for(unsigned Y_coordinata=Verticale_funzione;Y_coordinata<chiudere_Y;Y_coordinata++)for(unsigned coordinata_x=가로;coordinata_x<chiudere_X;coordinata_x++){
        uint32_t 색=보드화면읽기(coordinata_x,Y_coordinata),VALORE=(((색>>16)&255)*빨강최대/255)<<rosso_scorrere|
            (((색>>8)&255)*초록최대/255)<<verde_scorrere|((색&255)*파랑최대/255)<<blu_scorrere;
        for(unsigned 순번=0;순번<pixel_ridimensionare;순번++)uscitaTesto[output_CONTA_NUMERI++]=VALORE>>(8*(big_endian_VALORE?pixel_ridimensionare-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(In_ascolto_endpoint<0)return;
    if(peer_VALORE<0){if(보드밀리초()<다시받을때)return;peer_VALORE=NET_accettare(In_ascolto_endpoint);if(peer_VALORE<0)return;
        connessione_time=보드밀리초();area_VALORE_29ee1bb7=1;내보내기("RFB 003.008\n",12);memset(Indietro_riepilogo,0,sizeof(Indietro_riepilogo));
        pixel_ridimensionare=4;big_endian_VALORE=0;빨강최대=초록최대=파랑최대=255;rosso_scorrere=16;verde_scorrere=8;blu_scorrere=0;}
    if(area_VALORE_29ee1bb7<5&&보드밀리초()-connessione_time>15000){Chiudi();return;}
    if(output_CONTA_NUMERI){int numero=NET_scrivere(peer_VALORE,uscitaTesto+보낸수,output_CONTA_NUMERI-보낸수);if(numero>0){보낸수+=numero;if(보낸수==output_CONTA_NUMERI)output_CONTA_NUMERI=보낸수=0;}else if(numero!=-11){Chiudi();return;}}
    if(!output_CONTA_NUMERI&&닫을예정){Chiudi();return;}
    if(!output_CONTA_NUMERI&&parte_funzione<parte_CONTA_NUMERI)inviare_parte();
    if(input_CONTA_NUMERI==sizeof(input_VALORE)){Chiudi();return;}
    int RICEV_SCAD_CONTA_NUMERI=통신읽기(peer_VALORE,input_VALORE+input_CONTA_NUMERI,sizeof(input_VALORE)-input_CONTA_NUMERI);
    if(RICEV_SCAD_CONTA_NUMERI==0||(RICEV_SCAD_CONTA_NUMERI<0&&RICEV_SCAD_CONTA_NUMERI!=-11)){Chiudi();return;}if(RICEV_SCAD_CONTA_NUMERI>0)input_CONTA_NUMERI+=RICEV_SCAD_CONTA_NUMERI;
    if(output_CONTA_NUMERI||parte_funzione<parte_CONTA_NUMERI)return;
    if(area_VALORE_29ee1bb7==1&&input_CONTA_NUMERI>=12){if(memcmp(input_VALORE,"RFB 003.008\n",12)){Chiudi();return;}consumo_VALORE(12);const unsigned char metodo_di_autenticazione[]={1,2};내보내기(metodo_di_autenticazione,2);area_VALORE_29ee1bb7=2;return;}
    if(area_VALORE_29ee1bb7==2&&input_CONTA_NUMERI){if(input_VALORE[0]!=2||remoto_casuale(test_VALORE,16)){Chiudi();return;}consumo_VALORE(1);내보내기(test_VALORE,16);area_VALORE_29ee1bb7=3;return;}
    if(area_VALORE_29ee1bb7==3&&input_CONTA_NUMERI>=16){unsigned char tasto_materiale[8],정답[16];br_des_ct_cbcenc_keys password_VALORE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALORE=schermata_password[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALORE&1);VALORE>>=1;}tasto_materiale[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&password_VALORE,tasto_materiale,8);memcpy(정답,test_VALORE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vettore_VALORE[8]={0};br_des_ct_cbcenc_run(&password_VALORE,vettore_VALORE,정답+순번,8);memset(vettore_VALORE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^input_VALORE[순번];consumo_VALORE(16);memset(&password_VALORE,0,sizeof(password_VALORE));memset(tasto_materiale,0,8);memset(정답,0,16);memset(test_VALORE,0,16);
        scrivere_32(uscitaTesto,차이?1:0);output_CONTA_NUMERI=4;보낸수=0;
        if(차이){scrivere_32(uscitaTesto+4,19);memcpy(uscitaTesto+8,"Authentication fail",19);output_CONTA_NUMERI=27;닫을예정=1;}else area_VALORE_29ee1bb7=4;return;}
    if(area_VALORE_29ee1bb7==4&&input_CONTA_NUMERI){consumo_VALORE(1);너비=보드화면너비();altezza_VALORE=scheda_schermata_altezza();if(!너비||!altezza_VALORE||너비>1920||altezza_VALORE>1080){Chiudi();return;}
        if(!scheda_Terminale(7)){const unsigned char Evento[]={30,2,1,0,0,0,0};feed_remoto_input(Evento,7);}
        memset(uscitaTesto,0,40);scrivere_16(uscitaTesto,너비);scrivere_16(uscitaTesto+2,altezza_VALORE);uscitaTesto[4]=32;uscitaTesto[5]=24;uscitaTesto[7]=1;
        scrivere_16(uscitaTesto+8,255);scrivere_16(uscitaTesto+10,255);scrivere_16(uscitaTesto+12,255);uscitaTesto[14]=16;uscitaTesto[15]=8;
        const char *Nome="jkoros native";scrivere_32(uscitaTesto+20,strlen(Nome));memcpy(uscitaTesto+24,Nome,strlen(Nome));output_CONTA_NUMERI=24+strlen(Nome);보낸수=0;area_VALORE_29ee1bb7=5;return;}
    if(area_VALORE_29ee1bb7!=5||!input_CONTA_NUMERI)return;
    unsigned TIPO_area=input_VALORE[0],필요=TIPO_area==0?20:TIPO_area==2?4:TIPO_area==3?10:TIPO_area==4?8:TIPO_area==5?6:TIPO_area==6?8:0;
    if(!필요){Chiudi();return;}if(input_CONTA_NUMERI<필요)return;
    if(TIPO_area==2){unsigned numero=읽기16(input_VALORE+2);if(numero>128){Chiudi();return;}필요+=numero*4;}
    if(TIPO_area==6){unsigned numero=읽기32(input_VALORE+4);if(numero>4096){Chiudi();return;}필요+=numero;}
    if(input_CONTA_NUMERI<필요)return;
    if(TIPO_area==0){unsigned bit_VALORE=input_VALORE[4],빨=읽기16(input_VALORE+8),초=읽기16(input_VALORE+10),파=읽기16(input_VALORE+12),rosso_Canale_scorrere=input_VALORE[14],verde_Canale_scorrere=input_VALORE[15],blu_Canale_scorrere=input_VALORE[16];
        if((bit_VALORE!=16&&bit_VALORE!=32)||!input_VALORE[7]||input_VALORE[6]>1||!빨||!초||!파||빨>255||초>255||파>255||rosso_Canale_scorrere>24||verde_Canale_scorrere>24||blu_Canale_scorrere>24||
           ((uint64_t)빨<<rosso_Canale_scorrere)>((1ull<<bit_VALORE)-1)||((uint64_t)초<<verde_Canale_scorrere)>((1ull<<bit_VALORE)-1)||((uint64_t)파<<blu_Canale_scorrere)>((1ull<<bit_VALORE)-1)){Chiudi();return;}
        pixel_ridimensionare=bit_VALORE/8;big_endian_VALORE=input_VALORE[6];빨강최대=빨;초록최대=초;파랑최대=파;rosso_scorrere=rosso_Canale_scorrere;verde_scorrere=verde_Canale_scorrere;blu_scorrere=blu_Canale_scorrere;memset(Indietro_riepilogo,0,sizeof(Indietro_riepilogo));
    }else if(TIPO_area==3)schermata_richiesta(input_VALORE);
    else if(TIPO_area==4)remoto_tasto_Tratto(읽기32(input_VALORE+4),input_VALORE[1]!=0);
    else if(TIPO_area==5){unsigned coordinata_x=읽기16(input_VALORE+2),Y_coordinata=읽기16(input_VALORE+4);if(coordinata_x>=너비)coordinata_x=너비-1;if(Y_coordinata>=altezza_VALORE)Y_coordinata=altezza_VALORE-1;
        if(input_VALORE[1])commit_remoto_tasto();
        unsigned char Evento[]={30,1,input_VALORE[1],coordinata_x&255,coordinata_x>>8,Y_coordinata&255,Y_coordinata>>8};feed_remoto_input(Evento,sizeof(Evento));}
    consumo_VALORE(필요);
}
