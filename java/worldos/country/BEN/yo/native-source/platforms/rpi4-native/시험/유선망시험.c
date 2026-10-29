/* 가짜 MMIO/MDIO 장치로 ṣetúnṣe_iye rékọjá_iye·gígùn_iye·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t forúkọsílẹ̀_iye[0x10000/4];
#define 유선저장기(àdírẹ́ẹ̀sì) forúkọsílẹ̀_iye[(àdírẹ́ẹ̀sì)/4]
#define JKOROS_GENET_TEST 1
#include "../Alásopọ̀_kójọ/aláfiwáyàsopọ̀_Alásopọ̀.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Ọ̀rọ̀_SMS=유선저장기(0xe14);
    if(물리작동&&(Ọ̀rọ̀_SMS&(1u<<29))){unsigned àdírẹ́ẹ̀sì=(Ọ̀rọ̀_SMS>>21)&31,wá_atọ̀ka_àkóónú=(Ọ̀rọ̀_SMS>>16)&31;
        if(àdírẹ́ẹ̀sì!=1)유선저장기(0xe14)=1<<28;
        else{if(((Ọ̀rọ̀_SMS>>26)&3)==1)물리값[wá_atọ̀ka_àkóónú]=Ọ̀rọ̀_SMS&65535;유선저장기(0xe14)=물리값[wá_atọ̀ka_àkóónú];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *àdírẹ́ẹ̀sì){const unsigned char iye[]={2,1,2,3,4,5};memcpy(àdírẹ́ẹ̀sì,iye,6);return 1;}
void netif_set_link_up(struct netif *ohun_èlò_iye){ohun_èlò_iye->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ohun_èlò_iye){ohun_èlò_iye->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ohun_èlò_iye,struct pbuf *전문,const ip4_addr_t *àdírẹ́ẹ̀sì){(void)ohun_èlò_iye;(void)전문;(void)àdírẹ́ẹ̀sì;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ìpele_wá_atọ̀ka_àkóónú,u16_t 수,pbuf_type 종류){
    (void)ìpele_wá_atọ̀ka_àkóónú;(void)종류;struct pbuf *détà=calloc(1,sizeof(*détà)+수);assert(détà);détà->payload=détà+1;détà->len=détà->tot_len=수;return détà;
}
u8_t pbuf_free(struct pbuf *détà){free(détà);return 1;}
err_t pbuf_take(struct pbuf *détà,const void *원본,u16_t 수){assert(수<=détà->len);memcpy(détà->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *détà,void *èbúté_iye,u16_t 수,u16_t Rọ́ọ̀nù){assert(Rọ́ọ̀nù+수<=détà->len);memcpy(èbúté_iye,(char*)détà->payload+Rọ́ọ̀nù,수);return 수;}
static err_t gbà_Ìsomọ́(struct pbuf *détà,struct netif *ohun_èlò_iye){(void)ohun_èlò_iye;assert(détà->len==60);assert(((unsigned char*)détà->payload)[0]==0x42);들어온수++;pbuf_free(détà);return ERR_OK;}
int main(void){
    struct netif ohun_èlò_iye;memset(&ohun_èlò_iye,0,sizeof(ohun_èlò_iye));ohun_èlò_iye.input=gbà_Ìsomọ́;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(gbaradì_aláfiwáyàsopọ̀_Alásopọ̀(&ohun_èlò_iye)==ERR_OK);assert(aláfiwáyàsopọ̀_iye.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ohun_èlò_iye);assert(netif_is_link_up(&ohun_èlò_iye));assert(aláfiwáyàsopọ̀_iye.속도==1000);
    aláfiwáyàsopọ̀_iye.생산=aláfiwáyàsopọ̀_iye.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ohun_èlò_iye,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=aláfiwáyàsopọ̀_iye.생산;}
    assert(aláfiwáyàsopọ̀_iye.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(aláfiwáyàsopọ̀_iye.í_meèlì[0][0]==0x42&&aláfiwáyàsopọ̀_iye.í_meèlì[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(aláfiwáyàsopọ̀_iye.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ohun_èlò_iye,전문)==ERR_MEM);pbuf_free(전문);
    memset(aláfiwáyàsopọ̀_iye.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ohun_èlò_iye);assert(들어온수==1&&aláfiwáyàsopọ̀_iye.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ohun_èlò_iye);
    assert(aláfiwáyàsopọ̀_iye.소비==0&&들어온수==1&&aláfiwáyàsopọ̀_iye.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ohun_èlò_iye);assert(!netif_is_link_up(&ohun_èlò_iye));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
