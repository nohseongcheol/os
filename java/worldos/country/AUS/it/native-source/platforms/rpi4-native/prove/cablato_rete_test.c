/* 가짜 MMIO/MDIO 장치로 Loop_VALORE overflow_VALORE·durata_VALORE·링크 전환을 검사한다. fisico_hardware 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registro[0x10000/4];
#define 유선저장기(e_mail) registro[(e_mail)/4]
#define JKOROS_GENET_TEST 1
#include "../rete_Pila/cablato_rete.c"
static uintptr_t timestamp_VALORE;
static int fisico_operazione=1,fisico_hardware=1,Ricevuta_CONTA_NUMERI;
static unsigned short fisico_VALORE[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(fisico_operazione&&(Word_SMS&(1u<<29))){unsigned e_mail=(Word_SMS>>21)&31,INDICE=(Word_SMS>>16)&31;
        if(e_mail!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)fisico_VALORE[INDICE]=Word_SMS&65535;유선저장기(0xe14)=fisico_VALORE[INDICE];}}
    return timestamp_VALORE++;
}
int scheda_fisico_hardware(void){return fisico_hardware;}
int scheda_indirizzo_reale(unsigned char *e_mail){const unsigned char VALORE[]={2,1,2,3,4,5};memcpy(e_mail,VALORE,6);return 1;}
void netif_set_link_up(struct netif *cellulare_VALORE){cellulare_VALORE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *cellulare_VALORE){cellulare_VALORE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *cellulare_VALORE,struct pbuf *datagramma,const ip4_addr_t *e_mail){(void)cellulare_VALORE;(void)datagramma;(void)e_mail;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer layer_INDICE,u16_t numero,pbuf_type Kind_VALORE){
    (void)layer_INDICE;(void)Kind_VALORE;struct pbuf *dati=calloc(1,sizeof(*dati)+numero);assert(dati);dati->payload=dati+1;dati->len=dati->tot_len=numero;return dati;
}
u8_t pbuf_free(struct pbuf *dati){free(dati);return 1;}
err_t pbuf_take(struct pbuf *dati,const void *원본,u16_t numero){assert(numero<=dati->len);memcpy(dati->payload,원본,numero);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *dati,void *meta_VALORE,u16_t numero,u16_t avvia){assert(avvia+numero<=dati->len);memcpy(meta_VALORE,(char*)dati->payload+avvia,numero);return numero;}
static err_t accettare_connessione(struct pbuf *dati,struct netif *cellulare_VALORE){(void)cellulare_VALORE;assert(dati->len==60);assert(((unsigned char*)dati->payload)[0]==0x42);Ricevuta_CONTA_NUMERI++;pbuf_free(dati);return ERR_OK;}
int main(void){
    struct netif cellulare_VALORE;memset(&cellulare_VALORE,0,sizeof(cellulare_VALORE));cellulare_VALORE.input=accettare_connessione;
    유선저장기(0)=6u<<24;fisico_VALORE[2]=0x600d;fisico_VALORE[1]=4;fisico_VALORE[25]=7<<8;
    fisico_hardware=0;assert(!유선장치있음());fisico_hardware=1;assert(유선장치있음());
    
    assert(Prepara_cablato_rete(&cellulare_VALORE)==ERR_OK);assert(cablato_VALORE.fisico_e_mail==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&cellulare_VALORE);assert(netif_is_link_up(&cellulare_VALORE));assert(cablato_VALORE.속도==1000);
    cablato_VALORE.생산=cablato_VALORE.consumo_VALORE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagramma=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagramma->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(inviare_datagramma(&cellulare_VALORE,datagramma)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=cablato_VALORE.생산;}
    assert(cablato_VALORE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(cablato_VALORE.inviare[0][0]==0x42&&cablato_VALORE.inviare[0][59]==0);pbuf_free(datagramma);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(cablato_VALORE.생산-255)&65535;datagramma=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(inviare_datagramma(&cellulare_VALORE,datagramma)==ERR_MEM);pbuf_free(datagramma);
    memset(cablato_VALORE.ricevere[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&cellulare_VALORE);assert(Ricevuta_CONTA_NUMERI==1&&cablato_VALORE.consumo_VALORE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&cellulare_VALORE);
    assert(cablato_VALORE.consumo_VALORE==0&&Ricevuta_CONTA_NUMERI==1&&cablato_VALORE.Statistiche_VALORE[4]==1);
    fisico_VALORE[1]=0;timestamp_VALORE+=1000;유선망살피기(&cellulare_VALORE);assert(!netif_is_link_up(&cellulare_VALORE));
    fisico_operazione=0;assert(fisico_trasferire(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
