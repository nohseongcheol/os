/* 가짜 MMIO/MDIO 장치로 Loop_VERDI overløp_VERDI·lengde_VERDI·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register_VERDI[0x10000/4];
#define 유선저장기(e_post) register_VERDI[(e_post)/4]
#define JKOROS_GENET_TEST 1
#include "../nettverk_stakk/kabelbasert_nettverk.c"
static uintptr_t timestamp_VERDI;
static int 물리작동=1,실물=1,Innkommende_ANTALL;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t ord_SMS=유선저장기(0xe14);
    if(물리작동&&(ord_SMS&(1u<<29))){unsigned e_post=(ord_SMS>>21)&31,INDEKS=(ord_SMS>>16)&31;
        if(e_post!=1)유선저장기(0xe14)=1<<28;
        else{if(((ord_SMS>>26)&3)==1)물리값[INDEKS]=ord_SMS&65535;유선저장기(0xe14)=물리값[INDEKS];}}
    return timestamp_VERDI++;
}
int 보드실물(void){return 실물;}
int Tavle_absolutt_adresse(unsigned char *e_post){const unsigned char VERDI[]={2,1,2,3,4,5};memcpy(e_post,VERDI,6);return 1;}
void netif_set_link_up(struct netif *enhet_VERDI){enhet_VERDI->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *enhet_VERDI){enhet_VERDI->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *enhet_VERDI,struct pbuf *datagram,const ip4_addr_t *e_post){(void)enhet_VERDI;(void)datagram;(void)e_post;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer lag_INDEKS,u16_t nummer,pbuf_type 종류){
    (void)lag_INDEKS;(void)종류;struct pbuf *data=calloc(1,sizeof(*data)+nummer);assert(data);data->payload=data+1;data->len=data->tot_len=nummer;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *원본,u16_t nummer){assert(nummer<=data->len);memcpy(data->payload,원본,nummer);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *mål_VERDI,u16_t nummer,u16_t Kjør_2){assert(Kjør_2+nummer<=data->len);memcpy(mål_VERDI,(char*)data->payload+Kjør_2,nummer);return nummer;}
static err_t godta_kontakt(struct pbuf *data,struct netif *enhet_VERDI){(void)enhet_VERDI;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);Innkommende_ANTALL++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif enhet_VERDI;memset(&enhet_VERDI,0,sizeof(enhet_VERDI));enhet_VERDI.input=godta_kontakt;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Forbered_kabelbasert_nettverk(&enhet_VERDI)==ERR_OK);assert(kabelbasert_VERDI.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&enhet_VERDI);assert(netif_is_link_up(&enhet_VERDI));assert(kabelbasert_VERDI.속도==1000);
    kabelbasert_VERDI.생산=kabelbasert_VERDI.bruke_VERDI=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(sende_datagram(&enhet_VERDI,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=kabelbasert_VERDI.생산;}
    assert(kabelbasert_VERDI.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(kabelbasert_VERDI.sende[0][0]==0x42&&kabelbasert_VERDI.sende[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(kabelbasert_VERDI.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(sende_datagram(&enhet_VERDI,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(kabelbasert_VERDI.motta[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&enhet_VERDI);assert(Innkommende_ANTALL==1&&kabelbasert_VERDI.bruke_VERDI==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&enhet_VERDI);
    assert(kabelbasert_VERDI.bruke_VERDI==0&&Innkommende_ANTALL==1&&kabelbasert_VERDI.statistikk_VERDI[4]==1);
    물리값[1]=0;timestamp_VERDI+=1000;유선망살피기(&enhet_VERDI);assert(!netif_is_link_up(&enhet_VERDI));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
