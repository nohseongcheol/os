/* 가짜 MMIO/MDIO 장치로 Loop_VALUE прелевање_VALUE·должина_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t регистрирај_VALUE[0x10000/4];
#define 유선저장기(адреса) регистрирај_VALUE[(адреса)/4]
#define JKOROS_GENET_TEST 1
#include "../Мрежа_Купче/физички_поврзан_Мрежа.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,Дојдовен_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_СМС=유선저장기(0xe14);
    if(물리작동&&(Word_СМС&(1u<<29))){unsigned адреса=(Word_СМС>>21)&31,INDEX=(Word_СМС>>16)&31;
        if(адреса!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_СМС>>26)&3)==1)물리값[INDEX]=Word_СМС&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int табла_машина_адреса(unsigned char *адреса){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(адреса,VALUE,6);return 1;}
void netif_set_link_up(struct netif *уред_VALUE){уред_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *уред_VALUE){уред_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *уред_VALUE,struct pbuf *전문,const ip4_addr_t *адреса){(void)уред_VALUE;(void)전문;(void)адреса;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer слој_INDEX,u16_t 수,pbuf_type 종류){
    (void)слој_INDEX;(void)종류;struct pbuf *податоци=calloc(1,sizeof(*податоци)+수);assert(податоци);податоци->payload=податоци+1;податоци->len=податоци->tot_len=수;return податоци;
}
u8_t pbuf_free(struct pbuf *податоци){free(податоци);return 1;}
err_t pbuf_take(struct pbuf *податоци,const void *원본,u16_t 수){assert(수<=податоци->len);memcpy(податоци->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *податоци,void *одредиште_VALUE,u16_t 수,u16_t Изврши_2){assert(Изврши_2+수<=податоци->len);memcpy(одредиште_VALUE,(char*)податоци->payload+Изврши_2,수);return 수;}
static err_t прифати_врска(struct pbuf *податоци,struct netif *уред_VALUE){(void)уред_VALUE;assert(податоци->len==60);assert(((unsigned char*)податоци->payload)[0]==0x42);Дојдовен_COUNT++;pbuf_free(податоци);return ERR_OK;}
int main(void){
    struct netif уред_VALUE;memset(&уред_VALUE,0,sizeof(уред_VALUE));уред_VALUE.input=прифати_врска;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Подготви_физички_поврзан_Мрежа(&уред_VALUE)==ERR_OK);assert(физички_поврзан_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&уред_VALUE);assert(netif_is_link_up(&уред_VALUE));assert(физички_поврзан_VALUE.속도==1000);
    физички_поврзан_VALUE.생산=физички_поврзан_VALUE.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&уред_VALUE,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=физички_поврзан_VALUE.생산;}
    assert(физички_поврзан_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(физички_поврзан_VALUE.испрати[0][0]==0x42&&физички_поврзан_VALUE.испрати[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(физички_поврзан_VALUE.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&уред_VALUE,전문)==ERR_MEM);pbuf_free(전문);
    memset(физички_поврзан_VALUE.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&уред_VALUE);assert(Дојдовен_COUNT==1&&физички_поврзан_VALUE.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&уред_VALUE);
    assert(физички_поврзан_VALUE.소비==0&&Дојдовен_COUNT==1&&физички_поврзан_VALUE.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&уред_VALUE);assert(!netif_is_link_up(&уред_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
