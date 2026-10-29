/* 가짜 MMIO/MDIO 장치로 لوپ_قدر اوور_فلو_قدر·لمبا_ئی_قدر·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t رجسٹر_کریں_قدر[0x10000/4];
#define 유선저장기(پتہ) رجسٹر_کریں_قدر[(پتہ)/4]
#define JKOROS_GENET_TEST 1
#include "../نیٹ_ورک_اسٹیک/بذریعہ_تار_نیٹ_ورک.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t الفاظ_متن=유선저장기(0xe14);
    if(물리작동&&(الفاظ_متن&(1u<<29))){unsigned پتہ=(الفاظ_متن>>21)&31,اشاریہ=(الفاظ_متن>>16)&31;
        if(پتہ!=1)유선저장기(0xe14)=1<<28;
        else{if(((الفاظ_متن>>26)&3)==1)물리값[اشاریہ]=الفاظ_متن&65535;유선저장기(0xe14)=물리값[اشاریہ];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int بورڈ_مشین_پتہ(unsigned char *پتہ){const unsigned char قدر[]={2,1,2,3,4,5};memcpy(پتہ,قدر,6);return 1;}
void netif_set_link_up(struct netif *آلہ_قدر){آلہ_قدر->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *آلہ_قدر){آلہ_قدر->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *آلہ_قدر,struct pbuf *전문,const ip4_addr_t *پتہ){(void)آلہ_قدر;(void)전문;(void)پتہ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer پرت_اشاریہ,u16_t 수,pbuf_type 종류){
    (void)پرت_اشاریہ;(void)종류;struct pbuf *کوائف=calloc(1,sizeof(*کوائف)+수);assert(کوائف);کوائف->payload=کوائف+1;کوائف->len=کوائف->tot_len=수;return کوائف;
}
u8_t pbuf_free(struct pbuf *کوائف){free(کوائف);return 1;}
err_t pbuf_take(struct pbuf *کوائف,const void *원본,u16_t 수){assert(수<=کوائف->len);memcpy(کوائف->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *کوائف,void *منزل_مقصود_قدر,u16_t 수,u16_t چلائیں){assert(چلائیں+수<=کوائف->len);memcpy(منزل_مقصود_قدر,(char*)کوائف->payload+چلائیں,수);return 수;}
static err_t قبول_کریں_رابطہ(struct pbuf *کوائف,struct netif *آلہ_قدر){(void)آلہ_قدر;assert(کوائف->len==60);assert(((unsigned char*)کوائف->payload)[0]==0x42);들어온수++;pbuf_free(کوائف);return ERR_OK;}
int main(void){
    struct netif آلہ_قدر;memset(&آلہ_قدر,0,sizeof(آلہ_قدر));آلہ_قدر.input=قبول_کریں_رابطہ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(تیار_کریں_بذریعہ_تار_نیٹ_ورک(&آلہ_قدر)==ERR_OK);assert(بذریعہ_تار_قدر.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&آلہ_قدر);assert(netif_is_link_up(&آلہ_قدر));assert(بذریعہ_تار_قدر.속도==1000);
    بذریعہ_تار_قدر.생산=بذریعہ_تار_قدر.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&آلہ_قدر,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=بذریعہ_تار_قدر.생산;}
    assert(بذریعہ_تار_قدر.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(بذریعہ_تار_قدر.بھیجیں[0][0]==0x42&&بذریعہ_تار_قدر.بھیجیں[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(بذریعہ_تار_قدر.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&آلہ_قدر,전문)==ERR_MEM);pbuf_free(전문);
    memset(بذریعہ_تار_قدر.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&آلہ_قدر);assert(들어온수==1&&بذریعہ_تار_قدر.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&آلہ_قدر);
    assert(بذریعہ_تار_قدر.소비==0&&들어온수==1&&بذریعہ_تار_قدر.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&آلہ_قدر);assert(!netif_is_link_up(&آلہ_قدر));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
