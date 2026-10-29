/* 가짜 MMIO/MDIO 장치로 Loop_VALUE preljev_VALUE·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registar_VALUE[0x10000/4];
#define 유선저장기(adresa) registar_VALUE[(adresa)/4]
#define JKOROS_GENET_TEST 1
#include "../mreža_hrpa/ožičen_mreža.c"
static uintptr_t podaci_vremenske_oznake_VALUE;
static int 물리작동=1,실물=1,Dolazni_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned adresa=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(adresa!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return podaci_vremenske_oznake_VALUE++;
}
int 보드실물(void){return 실물;}
int pano_apsolutna_adresa(unsigned char *adresa){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(adresa,VALUE,6);return 1;}
void netif_set_link_up(struct netif *uređaj_VALUE){uređaj_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *uređaj_VALUE){uređaj_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *uređaj_VALUE,struct pbuf *datogram,const ip4_addr_t *adresa){(void)uređaj_VALUE;(void)datogram;(void)adresa;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer sloj_INDEX,u16_t 수,pbuf_type 종류){
    (void)sloj_INDEX;(void)종류;struct pbuf *podaci=calloc(1,sizeof(*podaci)+수);assert(podaci);podaci->payload=podaci+1;podaci->len=podaci->tot_len=수;return podaci;
}
u8_t pbuf_free(struct pbuf *podaci){free(podaci);return 1;}
err_t pbuf_take(struct pbuf *podaci,const void *원본,u16_t 수){assert(수<=podaci->len);memcpy(podaci->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *podaci,void *odredište_VALUE,u16_t 수,u16_t Pokreni){assert(Pokreni+수<=podaci->len);memcpy(odredište_VALUE,(char*)podaci->payload+Pokreni,수);return 수;}
static err_t prihvatiti_veza(struct pbuf *podaci,struct netif *uređaj_VALUE){(void)uređaj_VALUE;assert(podaci->len==60);assert(((unsigned char*)podaci->payload)[0]==0x42);Dolazni_COUNT++;pbuf_free(podaci);return ERR_OK;}
int main(void){
    struct netif uređaj_VALUE;memset(&uređaj_VALUE,0,sizeof(uređaj_VALUE));uređaj_VALUE.input=prihvatiti_veza;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Pripremi_ožičen_mreža(&uređaj_VALUE)==ERR_OK);assert(ožičen_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&uređaj_VALUE);assert(netif_is_link_up(&uređaj_VALUE));assert(ožičen_VALUE.속도==1000);
    ožičen_VALUE.생산=ožičen_VALUE.potrošiti_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datogram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datogram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(slati_datogram(&uređaj_VALUE,datogram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ožičen_VALUE.생산;}
    assert(ožičen_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ožičen_VALUE.slati[0][0]==0x42&&ožičen_VALUE.slati[0][59]==0);pbuf_free(datogram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ožičen_VALUE.생산-255)&65535;datogram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(slati_datogram(&uređaj_VALUE,datogram)==ERR_MEM);pbuf_free(datogram);
    memset(ožičen_VALUE.primiti[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&uređaj_VALUE);assert(Dolazni_COUNT==1&&ožičen_VALUE.potrošiti_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&uređaj_VALUE);
    assert(ožičen_VALUE.potrošiti_VALUE==0&&Dolazni_COUNT==1&&ožičen_VALUE.집계[4]==1);
    물리값[1]=0;podaci_vremenske_oznake_VALUE+=1000;유선망살피기(&uređaj_VALUE);assert(!netif_is_link_up(&uređaj_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
