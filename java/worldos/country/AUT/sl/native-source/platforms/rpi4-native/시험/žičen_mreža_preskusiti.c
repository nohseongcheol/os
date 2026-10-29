/* 가짜 MMIO/MDIO 장치로 Loop_VALUE presežek_VALUE·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register_VALUE[0x10000/4];
#define 유선저장기(naslov) register_VALUE[(naslov)/4]
#define JKOROS_GENET_TEST 1
#include "../mreža_Sklad/žičen_mreža.c"
static uintptr_t timestamp_VALUE;
static int 물리작동=1,실물=1,Dohoden_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned naslov=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(naslov!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return timestamp_VALUE++;
}
int 보드실물(void){return 실물;}
int Tabla_absolutni_naslov(unsigned char *naslov){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(naslov,VALUE,6);return 1;}
void netif_set_link_up(struct netif *naprava_VALUE){naprava_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *naprava_VALUE){naprava_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *naprava_VALUE,struct pbuf *datagram,const ip4_addr_t *naslov){(void)naprava_VALUE;(void)datagram;(void)naslov;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer sloj_INDEX,u16_t 수,pbuf_type 종류){
    (void)sloj_INDEX;(void)종류;struct pbuf *podatki=calloc(1,sizeof(*podatki)+수);assert(podatki);podatki->payload=podatki+1;podatki->len=podatki->tot_len=수;return podatki;
}
u8_t pbuf_free(struct pbuf *podatki){free(podatki);return 1;}
err_t pbuf_take(struct pbuf *podatki,const void *원본,u16_t 수){assert(수<=podatki->len);memcpy(podatki->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *podatki,void *cilj_VALUE,u16_t 수,u16_t Zaženi){assert(Zaženi+수<=podatki->len);memcpy(cilj_VALUE,(char*)podatki->payload+Zaženi,수);return 수;}
static err_t sprejeti_povezava(struct pbuf *podatki,struct netif *naprava_VALUE){(void)naprava_VALUE;assert(podatki->len==60);assert(((unsigned char*)podatki->payload)[0]==0x42);Dohoden_COUNT++;pbuf_free(podatki);return ERR_OK;}
int main(void){
    struct netif naprava_VALUE;memset(&naprava_VALUE,0,sizeof(naprava_VALUE));naprava_VALUE.input=sprejeti_povezava;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Pripravi_žičen_mreža(&naprava_VALUE)==ERR_OK);assert(žičen_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&naprava_VALUE);assert(netif_is_link_up(&naprava_VALUE));assert(žičen_VALUE.속도==1000);
    žičen_VALUE.생산=žičen_VALUE.porabiti_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(poslati_datagram(&naprava_VALUE,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=žičen_VALUE.생산;}
    assert(žičen_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(žičen_VALUE.poslati[0][0]==0x42&&žičen_VALUE.poslati[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(žičen_VALUE.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(poslati_datagram(&naprava_VALUE,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(žičen_VALUE.sprejeti_sprejemati_prejeti_prejemati[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&naprava_VALUE);assert(Dohoden_COUNT==1&&žičen_VALUE.porabiti_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&naprava_VALUE);
    assert(žičen_VALUE.porabiti_VALUE==0&&Dohoden_COUNT==1&&žičen_VALUE.집계[4]==1);
    물리값[1]=0;timestamp_VALUE+=1000;유선망살피기(&naprava_VALUE);assert(!netif_is_link_up(&naprava_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
