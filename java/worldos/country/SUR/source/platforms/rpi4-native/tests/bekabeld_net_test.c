/* 가짜 MMIO/MDIO 장치로 lus_WAARDE overloop_WAARDE·tijdsduur_WAARDE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register[0x10000/4];
#define 유선저장기(ADRES) register[(ADRES)/4]
#define JKOROS_GENET_TEST 1
#include "../net_stack/bekabeld_net.c"
static uintptr_t timestamp_WAARDE;
static int 물리작동=1,실물=1,Inkomend_AANTAL;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_sms=유선저장기(0xe14);
    if(물리작동&&(Word_sms&(1u<<29))){unsigned ADRES=(Word_sms>>21)&31,INDEX=(Word_sms>>16)&31;
        if(ADRES!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_sms>>26)&3)==1)물리값[INDEX]=Word_sms&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return timestamp_WAARDE++;
}
int 보드실물(void){return 실물;}
int Bord_absoluut_adres(unsigned char *ADRES){const unsigned char WAARDE[]={2,1,2,3,4,5};memcpy(ADRES,WAARDE,6);return 1;}
void netif_set_link_up(struct netif *mobiel_WAARDE){mobiel_WAARDE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *mobiel_WAARDE){mobiel_WAARDE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *mobiel_WAARDE,struct pbuf *datagram,const ip4_addr_t *ADRES){(void)mobiel_WAARDE;(void)datagram;(void)ADRES;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer laag_INDEX,u16_t nummer,pbuf_type soort_WAARDE){
    (void)laag_INDEX;(void)soort_WAARDE;struct pbuf *gegevens=calloc(1,sizeof(*gegevens)+nummer);assert(gegevens);gegevens->payload=gegevens+1;gegevens->len=gegevens->tot_len=nummer;return gegevens;
}
u8_t pbuf_free(struct pbuf *gegevens){free(gegevens);return 1;}
err_t pbuf_take(struct pbuf *gegevens,const void *원본,u16_t nummer){assert(nummer<=gegevens->len);memcpy(gegevens->payload,원본,nummer);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *gegevens,void *doel_WAARDE,u16_t nummer,u16_t starten){assert(starten+nummer<=gegevens->len);memcpy(doel_WAARDE,(char*)gegevens->payload+starten,nummer);return nummer;}
static err_t accepteren_verbinding(struct pbuf *gegevens,struct netif *mobiel_WAARDE){(void)mobiel_WAARDE;assert(gegevens->len==60);assert(((unsigned char*)gegevens->payload)[0]==0x42);Inkomend_AANTAL++;pbuf_free(gegevens);return ERR_OK;}
int main(void){
    struct netif mobiel_WAARDE;memset(&mobiel_WAARDE,0,sizeof(mobiel_WAARDE));mobiel_WAARDE.input=accepteren_verbinding;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Bereid_voor_bekabeld_net(&mobiel_WAARDE)==ERR_OK);assert(bekabeld_WAARDE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&mobiel_WAARDE);assert(netif_is_link_up(&mobiel_WAARDE));assert(bekabeld_WAARDE.속도==1000);
    bekabeld_WAARDE.생산=bekabeld_WAARDE.gebruiken_WAARDE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(e_mailen_datagram(&mobiel_WAARDE,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=bekabeld_WAARDE.생산;}
    assert(bekabeld_WAARDE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(bekabeld_WAARDE.e_mailen[0][0]==0x42&&bekabeld_WAARDE.e_mailen[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(bekabeld_WAARDE.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(e_mailen_datagram(&mobiel_WAARDE,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(bekabeld_WAARDE.ontvangen[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&mobiel_WAARDE);assert(Inkomend_AANTAL==1&&bekabeld_WAARDE.gebruiken_WAARDE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&mobiel_WAARDE);
    assert(bekabeld_WAARDE.gebruiken_WAARDE==0&&Inkomend_AANTAL==1&&bekabeld_WAARDE.Statistieken_WAARDE[4]==1);
    물리값[1]=0;timestamp_WAARDE+=1000;유선망살피기(&mobiel_WAARDE);assert(!netif_is_link_up(&mobiel_WAARDE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
