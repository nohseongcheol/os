/* 가짜 MMIO/MDIO 장치로 Loop_VÆRDI overløb_VÆRDI·varighed_VÆRDI·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register_VÆRDI[0x10000/4];
#define 유선저장기(mail) register_VÆRDI[(mail)/4]
#define JKOROS_GENET_TEST 1
#include "../netværk_Stak/traditionel_netværk.c"
static uintptr_t timestamp_VÆRDI;
static int 물리작동=1,실물=1,Indgående_TÆL;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Ord_sms=유선저장기(0xe14);
    if(물리작동&&(Ord_sms&(1u<<29))){unsigned mail=(Ord_sms>>21)&31,INDEKS=(Ord_sms>>16)&31;
        if(mail!=1)유선저장기(0xe14)=1<<28;
        else{if(((Ord_sms>>26)&3)==1)물리값[INDEKS]=Ord_sms&65535;유선저장기(0xe14)=물리값[INDEKS];}}
    return timestamp_VÆRDI++;
}
int 보드실물(void){return 실물;}
int Tavle_absolut_adresse(unsigned char *mail){const unsigned char VÆRDI[]={2,1,2,3,4,5};memcpy(mail,VÆRDI,6);return 1;}
void netif_set_link_up(struct netif *enhed_VÆRDI){enhed_VÆRDI->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *enhed_VÆRDI){enhed_VÆRDI->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *enhed_VÆRDI,struct pbuf *datagram,const ip4_addr_t *mail){(void)enhed_VÆRDI;(void)datagram;(void)mail;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer lag_INDEKS,u16_t tal,pbuf_type 종류){
    (void)lag_INDEKS;(void)종류;struct pbuf *data=calloc(1,sizeof(*data)+tal);assert(data);data->payload=data+1;data->len=data->tot_len=tal;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *원본,u16_t tal){assert(tal<=data->len);memcpy(data->payload,원본,tal);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *destination_VÆRDI,u16_t tal,u16_t Kør_2){assert(Kør_2+tal<=data->len);memcpy(destination_VÆRDI,(char*)data->payload+Kør_2,tal);return tal;}
static err_t acceptere_forbindelse(struct pbuf *data,struct netif *enhed_VÆRDI){(void)enhed_VÆRDI;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);Indgående_TÆL++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif enhed_VÆRDI;memset(&enhed_VÆRDI,0,sizeof(enhed_VÆRDI));enhed_VÆRDI.input=acceptere_forbindelse;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Tilrettelæg_traditionel_netværk(&enhed_VÆRDI)==ERR_OK);assert(traditionel_VÆRDI.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&enhed_VÆRDI);assert(netif_is_link_up(&enhed_VÆRDI));assert(traditionel_VÆRDI.속도==1000);
    traditionel_VÆRDI.생산=traditionel_VÆRDI.bruge_VÆRDI=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(maile_datagram(&enhed_VÆRDI,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=traditionel_VÆRDI.생산;}
    assert(traditionel_VÆRDI.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(traditionel_VÆRDI.maile[0][0]==0x42&&traditionel_VÆRDI.maile[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(traditionel_VÆRDI.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(maile_datagram(&enhed_VÆRDI,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(traditionel_VÆRDI.modtage[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&enhed_VÆRDI);assert(Indgående_TÆL==1&&traditionel_VÆRDI.bruge_VÆRDI==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&enhed_VÆRDI);
    assert(traditionel_VÆRDI.bruge_VÆRDI==0&&Indgående_TÆL==1&&traditionel_VÆRDI.Statistik_VÆRDI[4]==1);
    물리값[1]=0;timestamp_VÆRDI+=1000;유선망살피기(&enhed_VÆRDI);assert(!netif_is_link_up(&enhed_VÆRDI));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
