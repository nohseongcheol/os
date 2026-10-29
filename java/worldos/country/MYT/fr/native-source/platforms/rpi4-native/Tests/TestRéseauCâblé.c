/* 가짜 MMIO/MDIO 장치로 valeurBoucle valeurDébordement·longueur·링크 전환을 검사한다. matérielPhysique 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registreProcesseur[0x10000/4];
#define registresCâblé(adresse) registreProcesseur[(adresse)/4]
#define JKOROS_GENET_TEST 1
#include "../PileRéseau/réseauCâblé.c"
static uintptr_t valeurHorodatage;
static int opérationPhysique=1,matérielPhysique=1,nombreÉlémentsArrivant;
static unsigned short valeurPhysique[32];
uintptr_t millisecondesÉcouléesCarteMatérielle(void){
    uint32_t texteMot=registresCâblé(0xe14);
    if(opérationPhysique&&(texteMot&(1u<<29))){unsigned adresse=(texteMot>>21)&31,numéro=(texteMot>>16)&31;
        if(adresse!=1)registresCâblé(0xe14)=1<<28;
        else{if(((texteMot>>26)&3)==1)valeurPhysique[numéro]=texteMot&65535;registresCâblé(0xe14)=valeurPhysique[numéro];}}
    return valeurHorodatage++;
}
int matérielPhysiqueCarteMatérielle(void){return matérielPhysique;}
int adresseMachineCarteMatérielle(unsigned char *adresse){const unsigned char valeur[]={2,1,2,3,4,5};memcpy(adresse,valeur,6);return 1;}
void netif_set_link_up(struct netif *Périphérique){Périphérique->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *Périphérique){Périphérique->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *Périphérique,struct pbuf *datagramme,const ip4_addr_t *adresse){(void)Périphérique;(void)datagramme;(void)adresse;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer indiceCouche,u16_t nombre,pbuf_type valeurGenre){
    (void)indiceCouche;(void)valeurGenre;struct pbuf *Données=calloc(1,sizeof(*Données)+nombre);assert(Données);Données->payload=Données+1;Données->len=Données->tot_len=nombre;return Données;
}
u8_t pbuf_free(struct pbuf *Données){free(Données);return 1;}
err_t pbuf_take(struct pbuf *Données,const void *original,u16_t nombre){assert(nombre<=Données->len);memcpy(Données->payload,original,nombre);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *Données,void *valeurDestination,u16_t nombre,u16_t lancer){assert(lancer+nombre<=Données->len);memcpy(valeurDestination,(char*)Données->payload+lancer,nombre);return nombre;}
static err_t accepterConnexion(struct pbuf *Données,struct netif *Périphérique){(void)Périphérique;assert(Données->len==60);assert(((unsigned char*)Données->payload)[0]==0x42);nombreÉlémentsArrivant++;pbuf_free(Données);return ERR_OK;}
int main(void){
    struct netif Périphérique;memset(&Périphérique,0,sizeof(Périphérique));Périphérique.input=accepterConnexion;
    registresCâblé(0)=6u<<24;valeurPhysique[2]=0x600d;valeurPhysique[1]=4;valeurPhysique[25]=7<<8;
    matérielPhysique=0;assert(!possèdePériphériqueCâblé());matérielPhysique=1;assert(possèdePériphériqueCâblé());
    
    assert(préparerRéseauCâblé(&Périphérique)==ERR_OK);assert(valeurCâblé.adressePhysique==1);
    assert(registresCâblé(GENET_RX_DMA_CTRL)==0x20001&&registresCâblé(GENET_TX_DMA_CTRL)==0x20001);
    assert(registresCâblé(0x80c)==0x02010203&&registresCâblé(0x810)==0x0405);
    inspecterRéseauCâblé(&Périphérique);assert(netif_is_link_up(&Périphérique));assert(valeurCâblé.valeurVitesse==1000);
    valeurCâblé.valeurProduire=valeurCâblé.consommerValeur=65534;registresCâblé(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagramme=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagramme->payload,0x42,40);
    for(unsigned indiceOrdinal=0;indiceOrdinal<3;indiceOrdinal++){assert(envoyerDatagramme(&Périphérique,datagramme)==ERR_OK);registresCâblé(GENET_TX_DMA_CONS_INDEX(16))=valeurCâblé.valeurProduire;}
    assert(valeurCâblé.valeurProduire==1);assert((registresCâblé(0x4000)>>16)==60);assert(valeurCâblé.envoyer[0][0]==0x42&&valeurCâblé.envoyer[0][59]==0);pbuf_free(datagramme);
    registresCâblé(GENET_TX_DMA_CONS_INDEX(16))=(valeurCâblé.valeurProduire-255)&65535;datagramme=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(envoyerDatagramme(&Périphérique,datagramme)==ERR_MEM);pbuf_free(datagramme);
    memset(valeurCâblé.recevoir[254],0x42,64);registresCâblé(0x2000+254*12)=(62<<16)|0x6000;registresCâblé(GENET_RX_DMA_PROD_INDEX(16))=65535;
    inspecterRéseauCâblé(&Périphérique);assert(nombreÉlémentsArrivant==1&&valeurCâblé.consommerValeur==65535);
    registresCâblé(0x2000+255*12)=(4095u<<16)|0x6000;registresCâblé(GENET_RX_DMA_PROD_INDEX(16))=0;inspecterRéseauCâblé(&Périphérique);
    assert(valeurCâblé.consommerValeur==0&&nombreÉlémentsArrivant==1&&valeurCâblé.valeurStatistiques[4]==1);
    valeurPhysique[1]=0;valeurHorodatage+=1000;inspecterRéseauCâblé(&Périphérique);assert(!netif_is_link_up(&Périphérique));
    opérationPhysique=0;assert(transfertPhysique(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
