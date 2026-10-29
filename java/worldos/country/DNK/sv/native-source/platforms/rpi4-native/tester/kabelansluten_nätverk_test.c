/* 가짜 MMIO/MDIO 장치로 Loop_värde spill_värde·längd_värde·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register[0x10000/4];
#define 유선저장기(Adress) register[(Adress)/4]
#define JKOROS_GENET_TEST 1
#include "../nätverk_Stack/kabelansluten_nätverk.c"
static uintptr_t tidsstämpel_värde;
static int 물리작동=1,실물=1,Inkommande_ANTAL;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Ord_SMS=유선저장기(0xe14);
    if(물리작동&&(Ord_SMS&(1u<<29))){unsigned Adress=(Ord_SMS>>21)&31,INDEX=(Ord_SMS>>16)&31;
        if(Adress!=1)유선저장기(0xe14)=1<<28;
        else{if(((Ord_SMS>>26)&3)==1)물리값[INDEX]=Ord_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return tidsstämpel_värde++;
}
int 보드실물(void){return 실물;}
int Tavla_absolut_adress(unsigned char *Adress){const unsigned char värde[]={2,1,2,3,4,5};memcpy(Adress,värde,6);return 1;}
void netif_set_link_up(struct netif *enhet_värde){enhet_värde->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *enhet_värde){enhet_värde->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *enhet_värde,struct pbuf *datagram,const ip4_addr_t *Adress){(void)enhet_värde;(void)datagram;(void)Adress;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer nivå_INDEX,u16_t nummer,pbuf_type variant_värde){
    (void)nivå_INDEX;(void)variant_värde;struct pbuf *data=calloc(1,sizeof(*data)+nummer);assert(data);data->payload=data+1;data->len=data->tot_len=nummer;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *원본,u16_t nummer){assert(nummer<=data->len);memcpy(data->payload,원본,nummer);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *mål_värde,u16_t nummer,u16_t Kör){assert(Kör+nummer<=data->len);memcpy(mål_värde,(char*)data->payload+Kör,nummer);return nummer;}
static err_t acceptera_kontakt(struct pbuf *data,struct netif *enhet_värde){(void)enhet_värde;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);Inkommande_ANTAL++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif enhet_värde;memset(&enhet_värde,0,sizeof(enhet_värde));enhet_värde.input=acceptera_kontakt;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Förbereda_kabelansluten_nätverk(&enhet_värde)==ERR_OK);assert(kabelansluten_värde.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&enhet_värde);assert(netif_is_link_up(&enhet_värde));assert(kabelansluten_värde.속도==1000);
    kabelansluten_värde.생산=kabelansluten_värde.använda_värde_84aa75c8=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(skicka_datagram(&enhet_värde,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=kabelansluten_värde.생산;}
    assert(kabelansluten_värde.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(kabelansluten_värde.skicka[0][0]==0x42&&kabelansluten_värde.skicka[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(kabelansluten_värde.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(skicka_datagram(&enhet_värde,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(kabelansluten_värde.få[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&enhet_värde);assert(Inkommande_ANTAL==1&&kabelansluten_värde.använda_värde_84aa75c8==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&enhet_värde);
    assert(kabelansluten_värde.använda_värde_84aa75c8==0&&Inkommande_ANTAL==1&&kabelansluten_värde.Statistik_värde[4]==1);
    물리값[1]=0;tidsstämpel_värde+=1000;유선망살피기(&enhet_värde);assert(!netif_is_link_up(&enhet_värde));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
