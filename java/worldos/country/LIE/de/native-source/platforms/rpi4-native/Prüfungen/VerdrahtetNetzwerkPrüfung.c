/* 가짜 MMIO/MDIO 장치로 schleifeWert überlaufWert·Länge·링크 전환을 검사한다. physischHardware 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t prozessorRegister[0x10000/4];
#define verdrahtetRegisterliste(adresse) prozessorRegister[(adresse)/4]
#define JKOROS_GENET_TEST 1
#include "../Netzwerkstapel/verdrahtetNetzwerk.c"
static uintptr_t zeitstempelWert;
static int physischVorgang=1,physischHardware=1,eintreffendAnzahl;
static unsigned short physischWert[32];
uintptr_t platineVergangeneMillisekunden(void){
    uint32_t maschinenwortText=verdrahtetRegisterliste(0xe14);
    if(physischVorgang&&(maschinenwortText&(1u<<29))){unsigned adresse=(maschinenwortText>>21)&31,Nummer=(maschinenwortText>>16)&31;
        if(adresse!=1)verdrahtetRegisterliste(0xe14)=1<<28;
        else{if(((maschinenwortText>>26)&3)==1)physischWert[Nummer]=maschinenwortText&65535;verdrahtetRegisterliste(0xe14)=physischWert[Nummer];}}
    return zeitstempelWert++;
}
int platinePhysischHardware(void){return physischHardware;}
int platineMaschineAdresse(unsigned char *adresse){const unsigned char Wert[]={2,1,2,3,4,5};memcpy(adresse,Wert,6);return 1;}
void netif_set_link_up(struct netif *Gerät){Gerät->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *Gerät){Gerät->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *Gerät,struct pbuf *datagramm,const ip4_addr_t *adresse){(void)Gerät;(void)datagramm;(void)adresse;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer schichtIndex,u16_t Zahl,pbuf_type artWert){
    (void)schichtIndex;(void)artWert;struct pbuf *Daten=calloc(1,sizeof(*Daten)+Zahl);assert(Daten);Daten->payload=Daten+1;Daten->len=Daten->tot_len=Zahl;return Daten;
}
u8_t pbuf_free(struct pbuf *Daten){free(Daten);return 1;}
err_t pbuf_take(struct pbuf *Daten,const void *ursprünglich,u16_t Zahl){assert(Zahl<=Daten->len);memcpy(Daten->payload,ursprünglich,Zahl);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *Daten,void *zielWert,u16_t Zahl,u16_t ausführenVorgang){assert(ausführenVorgang+Zahl<=Daten->len);memcpy(zielWert,(char*)Daten->payload+ausführenVorgang,Zahl);return Zahl;}
static err_t verbindungAnnehmen(struct pbuf *Daten,struct netif *Gerät){(void)Gerät;assert(Daten->len==60);assert(((unsigned char*)Daten->payload)[0]==0x42);eintreffendAnzahl++;pbuf_free(Daten);return ERR_OK;}
int main(void){
    struct netif Gerät;memset(&Gerät,0,sizeof(Gerät));Gerät.input=verbindungAnnehmen;
    verdrahtetRegisterliste(0)=6u<<24;physischWert[2]=0x600d;physischWert[1]=4;physischWert[25]=7<<8;
    physischHardware=0;assert(!hatVerdrahtetGerät());physischHardware=1;assert(hatVerdrahtetGerät());
    
    assert(verdrahtetNetzwerkVorbereiten(&Gerät)==ERR_OK);assert(verdrahtetWert.physischAdresse==1);
    assert(verdrahtetRegisterliste(GENET_RX_DMA_CTRL)==0x20001&&verdrahtetRegisterliste(GENET_TX_DMA_CTRL)==0x20001);
    assert(verdrahtetRegisterliste(0x80c)==0x02010203&&verdrahtetRegisterliste(0x810)==0x0405);
    verdrahtetNetzwerkUntersuchen(&Gerät);assert(netif_is_link_up(&Gerät));assert(verdrahtetWert.geschwindigkeitWert==1000);
    verdrahtetWert.erzeugenWert=verdrahtetWert.wertVerbrauchen=65534;verdrahtetRegisterliste(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagramm=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagramm->payload,0x42,40);
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<3;ordnungszahlIndex++){assert(datagrammSenden(&Gerät,datagramm)==ERR_OK);verdrahtetRegisterliste(GENET_TX_DMA_CONS_INDEX(16))=verdrahtetWert.erzeugenWert;}
    assert(verdrahtetWert.erzeugenWert==1);assert((verdrahtetRegisterliste(0x4000)>>16)==60);assert(verdrahtetWert.senden[0][0]==0x42&&verdrahtetWert.senden[0][59]==0);pbuf_free(datagramm);
    verdrahtetRegisterliste(GENET_TX_DMA_CONS_INDEX(16))=(verdrahtetWert.erzeugenWert-255)&65535;datagramm=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(datagrammSenden(&Gerät,datagramm)==ERR_MEM);pbuf_free(datagramm);
    memset(verdrahtetWert.empfangen[254],0x42,64);verdrahtetRegisterliste(0x2000+254*12)=(62<<16)|0x6000;verdrahtetRegisterliste(GENET_RX_DMA_PROD_INDEX(16))=65535;
    verdrahtetNetzwerkUntersuchen(&Gerät);assert(eintreffendAnzahl==1&&verdrahtetWert.wertVerbrauchen==65535);
    verdrahtetRegisterliste(0x2000+255*12)=(4095u<<16)|0x6000;verdrahtetRegisterliste(GENET_RX_DMA_PROD_INDEX(16))=0;verdrahtetNetzwerkUntersuchen(&Gerät);
    assert(verdrahtetWert.wertVerbrauchen==0&&eintreffendAnzahl==1&&verdrahtetWert.statistikWert[4]==1);
    physischWert[1]=0;zeitstempelWert+=1000;verdrahtetNetzwerkUntersuchen(&Gerät);assert(!netif_is_link_up(&Gerät));
    physischVorgang=0;assert(physischÜbertragung(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
