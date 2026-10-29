/* 가짜 MMIO/MDIO 장치로 Loop_uara waipuke_uara·roa_uara·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t rēhita_uara[0x10000/4];
#define 유선저장기(ADDRESS) rēhita_uara[(ADDRESS)/4]
#define JKOROS_GENET_TEST 1
#include "../whatunga_Huinga/whaiaho_whatunga.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_TEXT=유선저장기(0xe14);
    if(물리작동&&(Word_TEXT&(1u<<29))){unsigned ADDRESS=(Word_TEXT>>21)&31,INDEX=(Word_TEXT>>16)&31;
        if(ADDRESS!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_TEXT>>26)&3)==1)물리값[INDEX]=Word_TEXT&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int papa_mīhini_ADDRESS(unsigned char *ADDRESS){const unsigned char uara[]={2,1,2,3,4,5};memcpy(ADDRESS,uara,6);return 1;}
void netif_set_link_up(struct netif *pūkoro_uara){pūkoro_uara->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *pūkoro_uara){pūkoro_uara->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *pūkoro_uara,struct pbuf *전문,const ip4_addr_t *ADDRESS){(void)pūkoro_uara;(void)전문;(void)ADDRESS;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer apa_INDEX,u16_t 수,pbuf_type 종류){
    (void)apa_INDEX;(void)종류;struct pbuf *raraunga=calloc(1,sizeof(*raraunga)+수);assert(raraunga);raraunga->payload=raraunga+1;raraunga->len=raraunga->tot_len=수;return raraunga;
}
u8_t pbuf_free(struct pbuf *raraunga){free(raraunga);return 1;}
err_t pbuf_take(struct pbuf *raraunga,const void *원본,u16_t 수){assert(수<=raraunga->len);memcpy(raraunga->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *raraunga,void *ūnga_uara,u16_t 수,u16_t whakahaere){assert(whakahaere+수<=raraunga->len);memcpy(ūnga_uara,(char*)raraunga->payload+whakahaere,수);return 수;}
static err_t whakaae_hononga(struct pbuf *raraunga,struct netif *pūkoro_uara){(void)pūkoro_uara;assert(raraunga->len==60);assert(((unsigned char*)raraunga->payload)[0]==0x42);들어온수++;pbuf_free(raraunga);return ERR_OK;}
int main(void){
    struct netif pūkoro_uara;memset(&pūkoro_uara,0,sizeof(pūkoro_uara));pūkoro_uara.input=whakaae_hononga;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Whakarite_whaiaho_whatunga(&pūkoro_uara)==ERR_OK);assert(whaiaho_uara.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&pūkoro_uara);assert(netif_is_link_up(&pūkoro_uara));assert(whaiaho_uara.속도==1000);
    whaiaho_uara.생산=whaiaho_uara.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&pūkoro_uara,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=whaiaho_uara.생산;}
    assert(whaiaho_uara.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(whaiaho_uara.tuku[0][0]==0x42&&whaiaho_uara.tuku[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(whaiaho_uara.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&pūkoro_uara,전문)==ERR_MEM);pbuf_free(전문);
    memset(whaiaho_uara.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&pūkoro_uara);assert(들어온수==1&&whaiaho_uara.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&pūkoro_uara);
    assert(whaiaho_uara.소비==0&&들어온수==1&&whaiaho_uara.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&pūkoro_uara);assert(!netif_is_link_up(&pūkoro_uara));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
