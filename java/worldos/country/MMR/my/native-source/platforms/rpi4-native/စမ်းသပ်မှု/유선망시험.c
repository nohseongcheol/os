/* 가짜 MMIO/MDIO 장치로 ထပ်ခါလည်ပတ်မှုတန်ဖိုး လျှံကျတန်ဖိုး·အလျား·링크 전환을 검사한다. ရုပ်ပိုင်းစက်ပစ္စည်း 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t အမြန်မှတ်ကွက်[0x10000/4];
#define 유선저장기(လိပ်စာ) အမြန်မှတ်ကွက်[(လိပ်စာ)/4]
#define JKOROS_GENET_TEST 1
#include "../ကွန်ရက်အလွှာစု/유선망.c"
static uintptr_t 시각;
static int ရုပ်ပိုင်းလုပ်ငန်း=1,ရုပ်ပိုင်းစက်ပစ္စည်း=1,들어온수;
static unsigned short ရုပ်ပိုင်းတန်ဖိုး[32];
uintptr_t 보드밀리초(void){
    uint32_t စကားလုံးစာသား=유선저장기(0xe14);
    if(ရုပ်ပိုင်းလုပ်ငန်း&&(စကားလုံးစာသား&(1u<<29))){unsigned လိပ်စာ=(စကားလုံးစာသား>>21)&31,နံပါတ်=(စကားလုံးစာသား>>16)&31;
        if(လိပ်စာ!=1)유선저장기(0xe14)=1<<28;
        else{if(((စကားလုံးစာသား>>26)&3)==1)ရုပ်ပိုင်းတန်ဖိုး[နံပါတ်]=စကားလုံးစာသား&65535;유선저장기(0xe14)=ရုပ်ပိုင်းတန်ဖိုး[နံပါတ်];}}
    return 시각++;
}
int ဆားကစ်ပြားရုပ်ပိုင်းစက်ပစ္စည်း(void){return ရုပ်ပိုင်းစက်ပစ္စည်း;}
int ဆားကစ်ပြားစက်လိပ်စာ(unsigned char *လိပ်စာ){const unsigned char တန်ဖိုး[]={2,1,2,3,4,5};memcpy(လိပ်စာ,တန်ဖိုး,6);return 1;}
void netif_set_link_up(struct netif *ကိရိယာ){ကိရိယာ->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ကိရိယာ){ကိရိယာ->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ကိရိယာ,struct pbuf *ဒေတာစာ,const ip4_addr_t *လိပ်စာ){(void)ကိရိယာ;(void)ဒေတာစာ;(void)လိပ်စာ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer အလွှာအညွှန်းကိန်း,u16_t ကိန်းတန်ဖိုး,pbuf_type အမျိုးအစားတန်ဖိုး){
    (void)အလွှာအညွှန်းကိန်း;(void)အမျိုးအစားတန်ဖိုး;struct pbuf *ဒေတာ=calloc(1,sizeof(*ဒေတာ)+ကိန်းတန်ဖိုး);assert(ဒေတာ);ဒေတာ->payload=ဒေတာ+1;ဒေတာ->len=ဒေတာ->tot_len=ကိန်းတန်ဖိုး;return ဒေတာ;
}
u8_t pbuf_free(struct pbuf *ဒေတာ){free(ဒေတာ);return 1;}
err_t pbuf_take(struct pbuf *ဒေတာ,const void *မူရင်း,u16_t ကိန်းတန်ဖိုး){assert(ကိန်းတန်ဖိုး<=ဒေတာ->len);memcpy(ဒေတာ->payload,မူရင်း,ကိန်းတန်ဖိုး);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ဒေတာ,void *ဦးတည်ရာတန်ဖိုး,u16_t ကိန်းတန်ဖိုး,u16_t လုပ်ဆောင်){assert(လုပ်ဆောင်+ကိန်းတန်ဖိုး<=ဒေတာ->len);memcpy(ဦးတည်ရာတန်ဖိုး,(char*)ဒေတာ->payload+လုပ်ဆောင်,ကိန်းတန်ဖိုး);return ကိန်းတန်ဖိုး;}
static err_t ချိတ်ဆက်မှုလက်ခံ(struct pbuf *ဒေတာ,struct netif *ကိရိယာ){(void)ကိရိယာ;assert(ဒေတာ->len==60);assert(((unsigned char*)ဒေတာ->payload)[0]==0x42);들어온수++;pbuf_free(ဒေတာ);return ERR_OK;}
int main(void){
    struct netif ကိရိယာ;memset(&ကိရိယာ,0,sizeof(ကိရိယာ));ကိရိယာ.input=ချိတ်ဆက်မှုလက်ခံ;
    유선저장기(0)=6u<<24;ရုပ်ပိုင်းတန်ဖိုး[2]=0x600d;ရုပ်ပိုင်းတန်ဖိုး[1]=4;ရုပ်ပိုင်းတန်ဖိုး[25]=7<<8;
    ရုပ်ပိုင်းစက်ပစ္စည်း=0;assert(!유선장치있음());ရုပ်ပိုင်းစက်ပစ္စည်း=1;assert(유선장치있음());
    
    assert(유선망준비(&ကိရိယာ)==ERR_OK);assert(유선.ရုပ်ပိုင်းလိပ်စာ==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ကိရိယာ);assert(netif_is_link_up(&ကိရိယာ));assert(유선.속도==1000);
    유선.생산=유선.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *ဒေတာစာ=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(ဒေတာစာ->payload,0x42,40);
    for(unsigned အစဉ်အမှတ်=0;အစဉ်အမှတ်<3;အစဉ်အမှတ်++){assert(ဒေတာစာပို့(&ကိရိယာ,ဒေတာစာ)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=유선.생산;}
    assert(유선.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(유선.ပို့[0][0]==0x42&&유선.ပို့[0][59]==0);pbuf_free(ဒေတာစာ);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(유선.생산-255)&65535;ဒေတာစာ=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(ဒေတာစာပို့(&ကိရိယာ,ဒေတာစာ)==ERR_MEM);pbuf_free(ဒေတာစာ);
    memset(유선.လက်ခံ[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ကိရိယာ);assert(들어온수==1&&유선.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ကိရိယာ);
    assert(유선.소비==0&&들어온수==1&&유선.집계[4]==1);
    ရုပ်ပိုင်းတန်ဖိုး[1]=0;시각+=1000;유선망살피기(&ကိရိယာ);assert(!netif_is_link_up(&ကိရိယာ));
    ရုပ်ပိုင်းလုပ်ငန်း=0;assert(ရုပ်ပိုင်းလွှဲပြောင်း(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
