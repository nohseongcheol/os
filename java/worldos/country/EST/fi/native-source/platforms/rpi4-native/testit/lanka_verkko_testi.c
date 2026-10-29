/* 가짜 MMIO/MDIO 장치로 Loop_ARVO ylivuoto_ARVO·kesto_ARVO·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t rekisteri[0x10000/4];
#define 유선저장기(OSOITE) rekisteri[(OSOITE)/4]
#define JKOROS_GENET_TEST 1
#include "../verkko_Pino/lanka_verkko.c"
static uintptr_t aikaleima_ARVO;
static int 물리작동=1,실물=1,Vastattu_LASKE;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned OSOITE=(Word_SMS>>21)&31,INDEKSI=(Word_SMS>>16)&31;
        if(OSOITE!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEKSI]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEKSI];}}
    return aikaleima_ARVO++;
}
int 보드실물(void){return 실물;}
int Taulu_absoluuttinen_osoite(unsigned char *OSOITE){const unsigned char ARVO[]={2,1,2,3,4,5};memcpy(OSOITE,ARVO,6);return 1;}
void netif_set_link_up(struct netif *laite_ARVO){laite_ARVO->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *laite_ARVO){laite_ARVO->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *laite_ARVO,struct pbuf *datagrammi,const ip4_addr_t *OSOITE){(void)laite_ARVO;(void)datagrammi;(void)OSOITE;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer kerros_INDEKSI,u16_t numero,pbuf_type 종류){
    (void)kerros_INDEKSI;(void)종류;struct pbuf *data=calloc(1,sizeof(*data)+numero);assert(data);data->payload=data+1;data->len=data->tot_len=numero;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *원본,u16_t numero){assert(numero<=data->len);memcpy(data->payload,원본,numero);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *kohde_ARVO,u16_t numero,u16_t Suorita_2){assert(Suorita_2+numero<=data->len);memcpy(kohde_ARVO,(char*)data->payload+Suorita_2,numero);return numero;}
static err_t hyväksyä_yhteys(struct pbuf *data,struct netif *laite_ARVO){(void)laite_ARVO;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);Vastattu_LASKE++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif laite_ARVO;memset(&laite_ARVO,0,sizeof(laite_ARVO));laite_ARVO.input=hyväksyä_yhteys;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Valmistele_lanka_verkko(&laite_ARVO)==ERR_OK);assert(lanka_ARVO.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&laite_ARVO);assert(netif_is_link_up(&laite_ARVO));assert(lanka_ARVO.속도==1000);
    lanka_ARVO.생산=lanka_ARVO.käyttää_ARVO=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagrammi=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagrammi->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(lähettää_datagrammi(&laite_ARVO,datagrammi)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=lanka_ARVO.생산;}
    assert(lanka_ARVO.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(lanka_ARVO.lähettää[0][0]==0x42&&lanka_ARVO.lähettää[0][59]==0);pbuf_free(datagrammi);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(lanka_ARVO.생산-255)&65535;datagrammi=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(lähettää_datagrammi(&laite_ARVO,datagrammi)==ERR_MEM);pbuf_free(datagrammi);
    memset(lanka_ARVO.saada[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&laite_ARVO);assert(Vastattu_LASKE==1&&lanka_ARVO.käyttää_ARVO==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&laite_ARVO);
    assert(lanka_ARVO.käyttää_ARVO==0&&Vastattu_LASKE==1&&lanka_ARVO.Tilastotiedot_ARVO[4]==1);
    물리값[1]=0;aikaleima_ARVO+=1000;유선망살피기(&laite_ARVO);assert(!netif_is_link_up(&laite_ARVO));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
