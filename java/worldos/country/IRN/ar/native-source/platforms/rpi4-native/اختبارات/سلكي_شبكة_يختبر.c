/* 가짜 MMIO/MDIO 장치로 يكرر_قيمة تجاوز_قيمة·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t مسجل[0x10000/4];
#define 유선저장기(عنوان) مسجل[(عنوان)/4]
#define JKOROS_GENET_TEST 1
#include "../شبكة_رمز/سلكي_شبكة.c"
static uintptr_t طابع_زمني_قيمة;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t الكلمات_نص=유선저장기(0xe14);
    if(물리작동&&(الكلمات_نص&(1u<<29))){unsigned عنوان=(الكلمات_نص>>21)&31,فهرس=(الكلمات_نص>>16)&31;
        if(عنوان!=1)유선저장기(0xe14)=1<<28;
        else{if(((الكلمات_نص>>26)&3)==1)물리값[فهرس]=الكلمات_نص&65535;유선저장기(0xe14)=물리값[فهرس];}}
    return طابع_زمني_قيمة++;
}
int 보드실물(void){return 실물;}
int لوحة_عنوان_حقيقي(unsigned char *عنوان){const unsigned char قيمة[]={2,1,2,3,4,5};memcpy(عنوان,قيمة,6);return 1;}
void netif_set_link_up(struct netif *جهاز_قيمة){جهاز_قيمة->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *جهاز_قيمة){جهاز_قيمة->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *جهاز_قيمة,struct pbuf *رزمةمستقلة,const ip4_addr_t *عنوان){(void)جهاز_قيمة;(void)رزمةمستقلة;(void)عنوان;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer طبقة_فهرس,u16_t رقم,pbuf_type 종류){
    (void)طبقة_فهرس;(void)종류;struct pbuf *بيانات=calloc(1,sizeof(*بيانات)+رقم);assert(بيانات);بيانات->payload=بيانات+1;بيانات->len=بيانات->tot_len=رقم;return بيانات;
}
u8_t pbuf_free(struct pbuf *بيانات){free(بيانات);return 1;}
err_t pbuf_take(struct pbuf *بيانات,const void *원본,u16_t رقم){assert(رقم<=بيانات->len);memcpy(بيانات->payload,원본,رقم);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *بيانات,void *وجهة_قيمة,u16_t رقم,u16_t تشغيل){assert(تشغيل+رقم<=بيانات->len);memcpy(وجهة_قيمة,(char*)بيانات->payload+تشغيل,رقم);return رقم;}
static err_t قبول_صديق(struct pbuf *بيانات,struct netif *جهاز_قيمة){(void)جهاز_قيمة;assert(بيانات->len==60);assert(((unsigned char*)بيانات->payload)[0]==0x42);들어온수++;pbuf_free(بيانات);return ERR_OK;}
int main(void){
    struct netif جهاز_قيمة;memset(&جهاز_قيمة,0,sizeof(جهاز_قيمة));جهاز_قيمة.input=قبول_صديق;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(إعداد_سلكي_شبكة(&جهاز_قيمة)==ERR_OK);assert(سلكي_قيمة.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&جهاز_قيمة);assert(netif_is_link_up(&جهاز_قيمة));assert(سلكي_قيمة.속도==1000);
    سلكي_قيمة.생산=سلكي_قيمة.يستخدم_قيمة_84aa75c8=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *رزمةمستقلة=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(رزمةمستقلة->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(يرسل_مخطط_بيانات(&جهاز_قيمة,رزمةمستقلة)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=سلكي_قيمة.생산;}
    assert(سلكي_قيمة.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(سلكي_قيمة.يرسل[0][0]==0x42&&سلكي_قيمة.يرسل[0][59]==0);pbuf_free(رزمةمستقلة);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(سلكي_قيمة.생산-255)&65535;رزمةمستقلة=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(يرسل_مخطط_بيانات(&جهاز_قيمة,رزمةمستقلة)==ERR_MEM);pbuf_free(رزمةمستقلة);
    memset(سلكي_قيمة.يستلم[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&جهاز_قيمة);assert(들어온수==1&&سلكي_قيمة.يستخدم_قيمة_84aa75c8==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&جهاز_قيمة);
    assert(سلكي_قيمة.يستخدم_قيمة_84aa75c8==0&&들어온수==1&&سلكي_قيمة.집계[4]==1);
    물리값[1]=0;طابع_زمني_قيمة+=1000;유선망살피기(&جهاز_قيمة);assert(!netif_is_link_up(&جهاز_قيمة));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
