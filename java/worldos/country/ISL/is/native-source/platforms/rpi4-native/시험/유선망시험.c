/* 가짜 MMIO/MDIO 장치로 Loop_VALUE yfirflæði_VALUE·lengd_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t skrá_VALUE[0x10000/4];
#define 유선저장기(slóð) skrá_VALUE[(slóð)/4]
#define JKOROS_GENET_TEST 1
#include "../Net_bunki/vírað_Net.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,Innhringing_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned slóð=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(slóð!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int bretti_vél_slóð(unsigned char *slóð){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(slóð,VALUE,6);return 1;}
void netif_set_link_up(struct netif *tæki_VALUE){tæki_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *tæki_VALUE){tæki_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *tæki_VALUE,struct pbuf *전문,const ip4_addr_t *slóð){(void)tæki_VALUE;(void)전문;(void)slóð;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer lag_INDEX,u16_t númer,pbuf_type 종류){
    (void)lag_INDEX;(void)종류;struct pbuf *gögn=calloc(1,sizeof(*gögn)+númer);assert(gögn);gögn->payload=gögn+1;gögn->len=gögn->tot_len=númer;return gögn;
}
u8_t pbuf_free(struct pbuf *gögn){free(gögn);return 1;}
err_t pbuf_take(struct pbuf *gögn,const void *원본,u16_t númer){assert(númer<=gögn->len);memcpy(gögn->payload,원본,númer);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *gögn,void *endastaður_VALUE,u16_t númer,u16_t Keyra_2){assert(Keyra_2+númer<=gögn->len);memcpy(endastaður_VALUE,(char*)gögn->payload+Keyra_2,númer);return númer;}
static err_t samþykkja_tenging(struct pbuf *gögn,struct netif *tæki_VALUE){(void)tæki_VALUE;assert(gögn->len==60);assert(((unsigned char*)gögn->payload)[0]==0x42);Innhringing_COUNT++;pbuf_free(gögn);return ERR_OK;}
int main(void){
    struct netif tæki_VALUE;memset(&tæki_VALUE,0,sizeof(tæki_VALUE));tæki_VALUE.input=samþykkja_tenging;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Undirbúa_vírað_Net(&tæki_VALUE)==ERR_OK);assert(vírað_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&tæki_VALUE);assert(netif_is_link_up(&tæki_VALUE));assert(vírað_VALUE.속도==1000);
    vírað_VALUE.생산=vírað_VALUE.nota_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&tæki_VALUE,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=vírað_VALUE.생산;}
    assert(vírað_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(vírað_VALUE.senda[0][0]==0x42&&vírað_VALUE.senda[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(vírað_VALUE.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&tæki_VALUE,전문)==ERR_MEM);pbuf_free(전문);
    memset(vírað_VALUE.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&tæki_VALUE);assert(Innhringing_COUNT==1&&vírað_VALUE.nota_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&tæki_VALUE);
    assert(vírað_VALUE.nota_VALUE==0&&Innhringing_COUNT==1&&vírað_VALUE.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&tæki_VALUE);assert(!netif_is_link_up(&tæki_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
