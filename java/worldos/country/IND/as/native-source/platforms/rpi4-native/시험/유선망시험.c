/* 가짜 MMIO/MDIO 장치로 লুপ_মান অ_ভাৰফ্ল_মান·দৈর্ঘ্য_মান·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t পঞ্জীয়ন_কৰক_মান[0x10000/4];
#define 유선저장기(ঠিকনা) পঞ্জীয়ন_কৰক_মান[(ঠিকনা)/4]
#define JKOROS_GENET_TEST 1
#include "../নেটৱৰ্ক_ষ্টেক/তাঁৰযুক্ত_নেটৱৰ্ক.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t 말=유선저장기(0xe14);
    if(물리작동&&(말&(1u<<29))){unsigned ঠিকনা=(말>>21)&31,ইনডেক্স=(말>>16)&31;
        if(ঠিকনা!=1)유선저장기(0xe14)=1<<28;
        else{if(((말>>26)&3)==1)물리값[ইনডেক্স]=말&65535;유선저장기(0xe14)=물리값[ইনডেক্স];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int ব_ৰ্ড_মেচিন_ঠিকনা(unsigned char *ঠিকনা){const unsigned char মান[]={2,1,2,3,4,5};memcpy(ঠিকনা,মান,6);return 1;}
void netif_set_link_up(struct netif *চেলফোন_মান){চেলফোন_মান->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *চেলফোন_মান){চেলফোন_মান->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *চেলফোন_মান,struct pbuf *전문,const ip4_addr_t *ঠিকনা){(void)চেলফোন_মান;(void)전문;(void)ঠিকনা;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer তৰপ_ইনডেক্স,u16_t 수,pbuf_type 종류){
    (void)তৰপ_ইনডেক্স;(void)종류;struct pbuf *ডাটা=calloc(1,sizeof(*ডাটা)+수);assert(ডাটা);ডাটা->payload=ডাটা+1;ডাটা->len=ডাটা->tot_len=수;return ডাটা;
}
u8_t pbuf_free(struct pbuf *ডাটা){free(ডাটা);return 1;}
err_t pbuf_take(struct pbuf *ডাটা,const void *원본,u16_t 수){assert(수<=ডাটা->len);memcpy(ডাটা->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ডাটা,void *গন্তব্য_স্থান_মান,u16_t 수,u16_t সঞ্চালন){assert(সঞ্চালন+수<=ডাটা->len);memcpy(গন্তব্য_স্থান_মান,(char*)ডাটা->payload+সঞ্চালন,수);return 수;}
static err_t গ্ৰহণ_সংযোগ(struct pbuf *ডাটা,struct netif *চেলফোন_মান){(void)চেলফোন_মান;assert(ডাটা->len==60);assert(((unsigned char*)ডাটা->payload)[0]==0x42);들어온수++;pbuf_free(ডাটা);return ERR_OK;}
int main(void){
    struct netif চেলফোন_মান;memset(&চেলফোন_মান,0,sizeof(চেলফোন_মান));চেলফোন_মান.input=গ্ৰহণ_সংযোগ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(প্ৰস্তুত_কৰক_তাঁৰযুক্ত_নেটৱৰ্ক(&চেলফোন_মান)==ERR_OK);assert(তাঁৰযুক্ত_মান.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&চেলফোন_মান);assert(netif_is_link_up(&চেলফোন_মান));assert(তাঁৰযুক্ত_মান.속도==1000);
    তাঁৰযুক্ত_মান.생산=তাঁৰযুক্ত_মান.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&চেলফোন_মান,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=তাঁৰযুক্ত_মান.생산;}
    assert(তাঁৰযুক্ত_মান.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(তাঁৰযুক্ত_মান.ই_মেইল_কৰক[0][0]==0x42&&তাঁৰযুক্ত_মান.ই_মেইল_কৰক[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(তাঁৰযুক্ত_মান.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&চেলফোন_মান,전문)==ERR_MEM);pbuf_free(전문);
    memset(তাঁৰযুক্ত_মান.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&চেলফোন_মান);assert(들어온수==1&&তাঁৰযুক্ত_মান.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&চেলফোন_মান);
    assert(তাঁৰযুক্ত_মান.소비==0&&들어온수==1&&তাঁৰযুক্ত_মান.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&চেলফোন_মান);assert(!netif_is_link_up(&চেলফোন_মান));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
