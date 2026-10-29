/* 가짜 MMIO/MDIO 장치로 کړۍ_ارزښت 넘침·اوږدوالى_ارزښت·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(پته) 저장기[(پته)/4]
#define JKOROS_GENET_TEST 1
#include "../통신망/سیم_پیوسته_شوی_جال.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t 말=유선저장기(0xe14);
    if(물리작동&&(말&(1u<<29))){unsigned پته=(말>>21)&31,لړیال=(말>>16)&31;
        if(پته!=1)유선저장기(0xe14)=1<<28;
        else{if(((말>>26)&3)==1)물리값[لړیال]=말&65535;유선저장기(0xe14)=물리값[لړیال];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *پته){const unsigned char ارزښت[]={2,1,2,3,4,5};memcpy(پته,ارزښت,6);return 1;}
void netif_set_link_up(struct netif *وزله_ارزښت){وزله_ارزښت->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *وزله_ارزښت){وزله_ارزښت->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *وزله_ارزښت,struct pbuf *전문,const ip4_addr_t *پته){(void)وزله_ارزښت;(void)전문;(void)پته;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer لهر_لړیال,u16_t 수,pbuf_type 종류){
    (void)لهر_لړیال;(void)종류;struct pbuf *اومتوک=calloc(1,sizeof(*اومتوک)+수);assert(اومتوک);اومتوک->payload=اومتوک+1;اومتوک->len=اومتوک->tot_len=수;return اومتوک;
}
u8_t pbuf_free(struct pbuf *اومتوک){free(اومتوک);return 1;}
err_t pbuf_take(struct pbuf *اومتوک,const void *원본,u16_t 수){assert(수<=اومتوک->len);memcpy(اومتوک->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *اومتوک,void *موخه_ارزښت,u16_t 수,u16_t ځغلول){assert(ځغلول+수<=اومتوک->len);memcpy(موخه_ارزښت,(char*)اومتوک->payload+ځغلول,수);return 수;}
static err_t 받음(struct pbuf *اومتوک,struct netif *وزله_ارزښت){(void)وزله_ارزښت;assert(اومتوک->len==60);assert(((unsigned char*)اومتوک->payload)[0]==0x42);들어온수++;pbuf_free(اومتوک);return ERR_OK;}
int main(void){
    struct netif وزله_ارزښت;memset(&وزله_ارزښت,0,sizeof(وزله_ارزښت));وزله_ارزښت.input=받음;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(유선망준비(&وزله_ارزښت)==ERR_OK);assert(سیم_پیوسته_شوی_ارزښت.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&وزله_ارزښت);assert(netif_is_link_up(&وزله_ارزښت));assert(سیم_پیوسته_شوی_ارزښت.속도==1000);
    سیم_پیوسته_شوی_ارزښت.생산=سیم_پیوسته_شوی_ارزښت.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&وزله_ارزښت,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=سیم_پیوسته_شوی_ارزښت.생산;}
    assert(سیم_پیوسته_شوی_ارزښت.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(سیم_پیوسته_شوی_ارزښت.استول[0][0]==0x42&&سیم_پیوسته_شوی_ارزښت.استول[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(سیم_پیوسته_شوی_ارزښت.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&وزله_ارزښت,전문)==ERR_MEM);pbuf_free(전문);
    memset(سیم_پیوسته_شوی_ارزښت.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&وزله_ارزښت);assert(들어온수==1&&سیم_پیوسته_شوی_ارزښت.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&وزله_ارزښت);
    assert(سیم_پیوسته_شوی_ارزښت.소비==0&&들어온수==1&&سیم_پیوسته_شوی_ارزښت.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&وزله_ارزښت);assert(!netif_is_link_up(&وزله_ارزښت));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
