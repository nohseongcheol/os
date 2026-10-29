/* 가짜 MMIO/MDIO 장치로 حلقه_مقدار سرریز_مقدار·طول_مقدار·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ثبت_نام_مقدار[0x10000/4];
#define 유선저장기(آدرس) ثبت_نام_مقدار[(آدرس)/4]
#define JKOROS_GENET_TEST 1
#include "../شبکه_پشته/سیم_دار_شبکه.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t کلمات_متن=유선저장기(0xe14);
    if(물리작동&&(کلمات_متن&(1u<<29))){unsigned آدرس=(کلمات_متن>>21)&31,فهرست=(کلمات_متن>>16)&31;
        if(آدرس!=1)유선저장기(0xe14)=1<<28;
        else{if(((کلمات_متن>>26)&3)==1)물리값[فهرست]=کلمات_متن&65535;유선저장기(0xe14)=물리값[فهرست];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int تخته_ای_دستگاه_آدرس(unsigned char *آدرس){const unsigned char مقدار[]={2,1,2,3,4,5};memcpy(آدرس,مقدار,6);return 1;}
void netif_set_link_up(struct netif *دستگاه_مقدار){دستگاه_مقدار->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *دستگاه_مقدار){دستگاه_مقدار->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *دستگاه_مقدار,struct pbuf *전문,const ip4_addr_t *آدرس){(void)دستگاه_مقدار;(void)전문;(void)آدرس;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer لایه_فهرست,u16_t 수,pbuf_type 종류){
    (void)لایه_فهرست;(void)종류;struct pbuf *داده_ها=calloc(1,sizeof(*داده_ها)+수);assert(داده_ها);داده_ها->payload=داده_ها+1;داده_ها->len=داده_ها->tot_len=수;return داده_ها;
}
u8_t pbuf_free(struct pbuf *داده_ها){free(داده_ها);return 1;}
err_t pbuf_take(struct pbuf *داده_ها,const void *원본,u16_t 수){assert(수<=داده_ها->len);memcpy(داده_ها->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *داده_ها,void *مقصد_مقدار,u16_t 수,u16_t اجرا_2){assert(اجرا_2+수<=داده_ها->len);memcpy(مقصد_مقدار,(char*)داده_ها->payload+اجرا_2,수);return 수;}
static err_t پذیرش_اتصال(struct pbuf *داده_ها,struct netif *دستگاه_مقدار){(void)دستگاه_مقدار;assert(داده_ها->len==60);assert(((unsigned char*)داده_ها->payload)[0]==0x42);들어온수++;pbuf_free(داده_ها);return ERR_OK;}
int main(void){
    struct netif دستگاه_مقدار;memset(&دستگاه_مقدار,0,sizeof(دستگاه_مقدار));دستگاه_مقدار.input=پذیرش_اتصال;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(آماده_کردن_سیم_دار_شبکه(&دستگاه_مقدار)==ERR_OK);assert(سیم_دار_مقدار.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&دستگاه_مقدار);assert(netif_is_link_up(&دستگاه_مقدار));assert(سیم_دار_مقدار.속도==1000);
    سیم_دار_مقدار.생산=سیم_دار_مقدار.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&دستگاه_مقدار,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=سیم_دار_مقدار.생산;}
    assert(سیم_دار_مقدار.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(سیم_دار_مقدار.ارسال[0][0]==0x42&&سیم_دار_مقدار.ارسال[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(سیم_دار_مقدار.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&دستگاه_مقدار,전문)==ERR_MEM);pbuf_free(전문);
    memset(سیم_دار_مقدار.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&دستگاه_مقدار);assert(들어온수==1&&سیم_دار_مقدار.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&دستگاه_مقدار);
    assert(سیم_دار_مقدار.소비==0&&들어온수==1&&سیم_دار_مقدار.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&دستگاه_مقدار);assert(!netif_is_link_up(&دستگاه_مقدار));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
