/* 가짜 MMIO/MDIO 장치로 লুপ_মান উপচানো_মান·দৈর্ঘ্য_মান·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t নিবন্ধন_করুন_মান[0x10000/4];
#define 유선저장기(ইমেইল) নিবন্ধন_করুন_মান[(ইমেইল)/4]
#define JKOROS_GENET_TEST 1
#include "../নেটওয়ার্ক_গাদা/ওয়্যার্ড_নেটওয়ার্ক.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t শব্দ_পাঠ=유선저장기(0xe14);
    if(물리작동&&(শব্দ_পাঠ&(1u<<29))){unsigned ইমেইল=(শব্দ_পাঠ>>21)&31,সূচি=(শব্দ_পাঠ>>16)&31;
        if(ইমেইল!=1)유선저장기(0xe14)=1<<28;
        else{if(((শব্দ_পাঠ>>26)&3)==1)물리값[সূচি]=শব্দ_পাঠ&65535;유선저장기(0xe14)=물리값[সূচি];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int বোর্ড_মেশিন_ইমেইল(unsigned char *ইমেইল){const unsigned char মান[]={2,1,2,3,4,5};memcpy(ইমেইল,মান,6);return 1;}
void netif_set_link_up(struct netif *ডিভাইস_মান){ডিভাইস_মান->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ডিভাইস_মান){ডিভাইস_মান->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ডিভাইস_মান,struct pbuf *전문,const ip4_addr_t *ইমেইল){(void)ডিভাইস_মান;(void)전문;(void)ইমেইল;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer স্তর_সূচি,u16_t 수,pbuf_type 종류){
    (void)স্তর_সূচি;(void)종류;struct pbuf *ডাটা=calloc(1,sizeof(*ডাটা)+수);assert(ডাটা);ডাটা->payload=ডাটা+1;ডাটা->len=ডাটা->tot_len=수;return ডাটা;
}
u8_t pbuf_free(struct pbuf *ডাটা){free(ডাটা);return 1;}
err_t pbuf_take(struct pbuf *ডাটা,const void *원본,u16_t 수){assert(수<=ডাটা->len);memcpy(ডাটা->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ডাটা,void *গন্তব্য_মান,u16_t 수,u16_t চালনা){assert(চালনা+수<=ডাটা->len);memcpy(গন্তব্য_মান,(char*)ডাটা->payload+চালনা,수);return 수;}
static err_t স্বীকার_করুন_সংযোগ(struct pbuf *ডাটা,struct netif *ডিভাইস_মান){(void)ডিভাইস_মান;assert(ডাটা->len==60);assert(((unsigned char*)ডাটা->payload)[0]==0x42);들어온수++;pbuf_free(ডাটা);return ERR_OK;}
int main(void){
    struct netif ডিভাইস_মান;memset(&ডিভাইস_মান,0,sizeof(ডিভাইস_মান));ডিভাইস_মান.input=স্বীকার_করুন_সংযোগ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(প্রস্তুত_করুন_ওয়্যার্ড_নেটওয়ার্ক(&ডিভাইস_মান)==ERR_OK);assert(ওয়্যার্ড_মান.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ডিভাইস_মান);assert(netif_is_link_up(&ডিভাইস_মান));assert(ওয়্যার্ড_মান.속도==1000);
    ওয়্যার্ড_মান.생산=ওয়্যার্ড_মান.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ডিভাইস_মান,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ওয়্যার্ড_মান.생산;}
    assert(ওয়্যার্ড_মান.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ওয়্যার্ড_মান.পাঠান[0][0]==0x42&&ওয়্যার্ড_মান.পাঠান[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ওয়্যার্ড_মান.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ডিভাইস_মান,전문)==ERR_MEM);pbuf_free(전문);
    memset(ওয়্যার্ড_মান.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ডিভাইস_মান);assert(들어온수==1&&ওয়্যার্ড_মান.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ডিভাইস_মান);
    assert(ওয়্যার্ড_মান.소비==0&&들어온수==1&&ওয়্যার্ড_মান.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ডিভাইস_মান);assert(!netif_is_link_up(&ডিভাইস_মান));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
