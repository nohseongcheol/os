/* 가짜 MMIO/MDIO 장치로 петља_вриједност прелијевање_вриједност·дужина_вриједност·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(адреса) 저장기[(адреса)/4]
#define JKOROS_GENET_TEST 1
#include "../통신망/ожичен_Мрежа.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t 말=유선저장기(0xe14);
    if(물리작동&&(말&(1u<<29))){unsigned адреса=(말>>21)&31,индекс=(말>>16)&31;
        if(адреса!=1)유선저장기(0xe14)=1<<28;
        else{if(((말>>26)&3)==1)물리값[индекс]=말&65535;유선저장기(0xe14)=물리값[индекс];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *адреса){const unsigned char вриједност[]={2,1,2,3,4,5};memcpy(адреса,вриједност,6);return 1;}
void netif_set_link_up(struct netif *уређај_вриједност){уређај_вриједност->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *уређај_вриједност){уређај_вриједност->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *уређај_вриједност,struct pbuf *전문,const ip4_addr_t *адреса){(void)уређај_вриједност;(void)전문;(void)адреса;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer слој_индекс,u16_t 수,pbuf_type 종류){
    (void)слој_индекс;(void)종류;struct pbuf *подаци=calloc(1,sizeof(*подаци)+수);assert(подаци);подаци->payload=подаци+1;подаци->len=подаци->tot_len=수;return подаци;
}
u8_t pbuf_free(struct pbuf *подаци){free(подаци);return 1;}
err_t pbuf_take(struct pbuf *подаци,const void *원본,u16_t 수){assert(수<=подаци->len);memcpy(подаци->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *подаци,void *одредиште_вриједност,u16_t 수,u16_t 시작){assert(시작+수<=подаци->len);memcpy(одредиште_вриједност,(char*)подаци->payload+시작,수);return 수;}
static err_t 받음(struct pbuf *подаци,struct netif *уређај_вриједност){(void)уређај_вриједност;assert(подаци->len==60);assert(((unsigned char*)подаци->payload)[0]==0x42);들어온수++;pbuf_free(подаци);return ERR_OK;}
int main(void){
    struct netif уређај_вриједност;memset(&уређај_вриједност,0,sizeof(уређај_вриједност));уређај_вриједност.input=받음;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Припремити_ожичен_Мрежа(&уређај_вриједност)==ERR_OK);assert(ожичен_вриједност.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&уређај_вриједност);assert(netif_is_link_up(&уређај_вриједност));assert(ожичен_вриједност.속도==1000);
    ожичен_вриједност.생산=ожичен_вриједност.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&уређај_вриједност,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ожичен_вриједност.생산;}
    assert(ожичен_вриједност.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ожичен_вриједност.послати[0][0]==0x42&&ожичен_вриједност.послати[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ожичен_вриједност.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&уређај_вриједност,전문)==ERR_MEM);pbuf_free(전문);
    memset(ожичен_вриједност.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&уређај_вриједност);assert(들어온수==1&&ожичен_вриједност.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&уређај_вриједност);
    assert(ожичен_вриједност.소비==0&&들어온수==1&&ожичен_вриједност.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&уређај_вриједност);assert(!netif_is_link_up(&уређај_вриједност));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
