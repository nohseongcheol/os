/* 가짜 MMIO/MDIO 장치로 लूप_मान ओवरफ्लो_मान·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t रजिस्टर_मान[0x10000/4];
#define 유선저장기(पता) रजिस्टर_मान[(पता)/4]
#define JKOROS_GENET_TEST 1
#include "../नेटवर्क_स्टैक/वायर्ड_नेटवर्क.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t शब्द_पाठ=유선저장기(0xe14);
    if(물리작동&&(शब्द_पाठ&(1u<<29))){unsigned पता=(शब्द_पाठ>>21)&31,इंडेक्स=(शब्द_पाठ>>16)&31;
        if(पता!=1)유선저장기(0xe14)=1<<28;
        else{if(((शब्द_पाठ>>26)&3)==1)물리값[इंडेक्स]=शब्द_पाठ&65535;유선저장기(0xe14)=물리값[इंडेक्स];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int बोर्ड_वास्तविक_पता(unsigned char *पता){const unsigned char मान[]={2,1,2,3,4,5};memcpy(पता,मान,6);return 1;}
void netif_set_link_up(struct netif *उपकरण_मान){उपकरण_मान->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *उपकरण_मान){उपकरण_मान->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *उपकरण_मान,struct pbuf *स्वतंत्रसंदेश,const ip4_addr_t *पता){(void)उपकरण_मान;(void)स्वतंत्रसंदेश;(void)पता;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer लेयर_इंडेक्स,u16_t 수,pbuf_type 종류){
    (void)लेयर_इंडेक्स;(void)종류;struct pbuf *आँकड़े=calloc(1,sizeof(*आँकड़े)+수);assert(आँकड़े);आँकड़े->payload=आँकड़े+1;आँकड़े->len=आँकड़े->tot_len=수;return आँकड़े;
}
u8_t pbuf_free(struct pbuf *आँकड़े){free(आँकड़े);return 1;}
err_t pbuf_take(struct pbuf *आँकड़े,const void *원본,u16_t 수){assert(수<=आँकड़े->len);memcpy(आँकड़े->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *आँकड़े,void *गंतव्य_मान,u16_t 수,u16_t चलाएँ){assert(चलाएँ+수<=आँकड़े->len);memcpy(गंतव्य_मान,(char*)आँकड़े->payload+चलाएँ,수);return 수;}
static err_t स्वीकार_करें_कनेक्शन(struct pbuf *आँकड़े,struct netif *उपकरण_मान){(void)उपकरण_मान;assert(आँकड़े->len==60);assert(((unsigned char*)आँकड़े->payload)[0]==0x42);들어온수++;pbuf_free(आँकड़े);return ERR_OK;}
int main(void){
    struct netif उपकरण_मान;memset(&उपकरण_मान,0,sizeof(उपकरण_मान));उपकरण_मान.input=स्वीकार_करें_कनेक्शन;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(유선망준비(&उपकरण_मान)==ERR_OK);assert(वायर्ड_मान.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&उपकरण_मान);assert(netif_is_link_up(&उपकरण_मान));assert(वायर्ड_मान.속도==1000);
    वायर्ड_मान.생산=वायर्ड_मान.उपयोग_करें_मान=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *स्वतंत्रसंदेश=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(स्वतंत्रसंदेश->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&उपकरण_मान,स्वतंत्रसंदेश)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=वायर्ड_मान.생산;}
    assert(वायर्ड_मान.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(वायर्ड_मान.भेजें[0][0]==0x42&&वायर्ड_मान.भेजें[0][59]==0);pbuf_free(स्वतंत्रसंदेश);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(वायर्ड_मान.생산-255)&65535;स्वतंत्रसंदेश=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&उपकरण_मान,स्वतंत्रसंदेश)==ERR_MEM);pbuf_free(स्वतंत्रसंदेश);
    memset(वायर्ड_मान.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&उपकरण_मान);assert(들어온수==1&&वायर्ड_मान.उपयोग_करें_मान==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&उपकरण_मान);
    assert(वायर्ड_मान.उपयोग_करें_मान==0&&들어온수==1&&वायर्ड_मान.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&उपकरण_मान);assert(!netif_is_link_up(&उपकरण_मान));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
