/* 가짜 MMIO/MDIO 장치로 Loop_VALUE pretečenie_VALUE·dĺžka_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register_VALUE[0x10000/4];
#define 유선저장기(adresa) register_VALUE[(adresa)/4]
#define JKOROS_GENET_TEST 1
#include "../sieť_Vrstvy/drôtový_sieť.c"
static uintptr_t časová_pečiatka_VALUE;
static int 물리작동=1,실물=1,Prichádzajúci_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned adresa=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(adresa!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return časová_pečiatka_VALUE++;
}
int 보드실물(void){return 실물;}
int Panel_absolútna_adresa(unsigned char *adresa){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(adresa,VALUE,6);return 1;}
void netif_set_link_up(struct netif *telefón_VALUE){telefón_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *telefón_VALUE){telefón_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *telefón_VALUE,struct pbuf *datagram,const ip4_addr_t *adresa){(void)telefón_VALUE;(void)datagram;(void)adresa;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer vrstva_INDEX,u16_t 수,pbuf_type 종류){
    (void)vrstva_INDEX;(void)종류;struct pbuf *údaje=calloc(1,sizeof(*údaje)+수);assert(údaje);údaje->payload=údaje+1;údaje->len=údaje->tot_len=수;return údaje;
}
u8_t pbuf_free(struct pbuf *údaje){free(údaje);return 1;}
err_t pbuf_take(struct pbuf *údaje,const void *원본,u16_t 수){assert(수<=údaje->len);memcpy(údaje->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *údaje,void *cieľ_VALUE,u16_t 수,u16_t Spustiť_2){assert(Spustiť_2+수<=údaje->len);memcpy(cieľ_VALUE,(char*)údaje->payload+Spustiť_2,수);return 수;}
static err_t prijať_kontakt(struct pbuf *údaje,struct netif *telefón_VALUE){(void)telefón_VALUE;assert(údaje->len==60);assert(((unsigned char*)údaje->payload)[0]==0x42);Prichádzajúci_COUNT++;pbuf_free(údaje);return ERR_OK;}
int main(void){
    struct netif telefón_VALUE;memset(&telefón_VALUE,0,sizeof(telefón_VALUE));telefón_VALUE.input=prijať_kontakt;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Pripraviť_drôtový_sieť(&telefón_VALUE)==ERR_OK);assert(drôtový_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&telefón_VALUE);assert(netif_is_link_up(&telefón_VALUE));assert(drôtový_VALUE.속도==1000);
    drôtový_VALUE.생산=drôtový_VALUE.použiť_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(odoslať_datagram(&telefón_VALUE,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=drôtový_VALUE.생산;}
    assert(drôtový_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(drôtový_VALUE.odoslať[0][0]==0x42&&drôtový_VALUE.odoslať[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(drôtový_VALUE.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(odoslať_datagram(&telefón_VALUE,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(drôtový_VALUE.dostať[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&telefón_VALUE);assert(Prichádzajúci_COUNT==1&&drôtový_VALUE.použiť_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&telefón_VALUE);
    assert(drôtový_VALUE.použiť_VALUE==0&&Prichádzajúci_COUNT==1&&drôtový_VALUE.집계[4]==1);
    물리값[1]=0;časová_pečiatka_VALUE+=1000;유선망살피기(&telefón_VALUE);assert(!netif_is_link_up(&telefón_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
