/* 가짜 MMIO/MDIO 장치로 օղակում_արժեք չափերի_գերազանցում_արժեք·տեւողություն_արժեք·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t գրանցվել_արժեք[0x10000/4];
#define 유선저장기(հասցե) գրանցվել_արժեք[(հասցե)/4]
#define JKOROS_GENET_TEST 1
#include "../Ցանց_Շեղջ/լարային_Ցանց.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Բառ_Գրվածք=유선저장기(0xe14);
    if(물리작동&&(Բառ_Գրվածք&(1u<<29))){unsigned հասցե=(Բառ_Գրվածք>>21)&31,դասիչ=(Բառ_Գրվածք>>16)&31;
        if(հասցե!=1)유선저장기(0xe14)=1<<28;
        else{if(((Բառ_Գրվածք>>26)&3)==1)물리값[դասիչ]=Բառ_Գրվածք&65535;유선저장기(0xe14)=물리값[դասիչ];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int տախտակ_մեքենա_հասցե(unsigned char *հասցե){const unsigned char արժեք[]={2,1,2,3,4,5};memcpy(հասցե,արժեք,6);return 1;}
void netif_set_link_up(struct netif *սարք_արժեք){սարք_արժեք->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *սարք_արժեք){սարք_արժեք->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *սարք_արժեք,struct pbuf *전문,const ip4_addr_t *հասցե){(void)սարք_արժեք;(void)전문;(void)հասցե;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer շերտ_դասիչ,u16_t 수,pbuf_type 종류){
    (void)շերտ_դասիչ;(void)종류;struct pbuf *տվյալ=calloc(1,sizeof(*տվյալ)+수);assert(տվյալ);տվյալ->payload=տվյալ+1;տվյալ->len=տվյալ->tot_len=수;return տվյալ;
}
u8_t pbuf_free(struct pbuf *տվյալ){free(տվյալ);return 1;}
err_t pbuf_take(struct pbuf *տվյալ,const void *원본,u16_t 수){assert(수<=տվյալ->len);memcpy(տվյալ->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *տվյալ,void *նպատակակետ_արժեք,u16_t 수,u16_t Գործարկել){assert(Գործարկել+수<=տվյալ->len);memcpy(նպատակակետ_արժեք,(char*)տվյալ->payload+Գործարկել,수);return 수;}
static err_t ընդունել_կապ(struct pbuf *տվյալ,struct netif *սարք_արժեք){(void)սարք_արժեք;assert(տվյալ->len==60);assert(((unsigned char*)տվյալ->payload)[0]==0x42);들어온수++;pbuf_free(տվյալ);return ERR_OK;}
int main(void){
    struct netif սարք_արժեք;memset(&սարք_արժեք,0,sizeof(սարք_արժեք));սարք_արժեք.input=ընդունել_կապ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Պատրաստել_լարային_Ցանց(&սարք_արժեք)==ERR_OK);assert(լարային_արժեք.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&սարք_արժեք);assert(netif_is_link_up(&սարք_արժեք));assert(լարային_արժեք.속도==1000);
    լարային_արժեք.생산=լարային_արժեք.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&սարք_արժեք,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=լարային_արժեք.생산;}
    assert(լարային_արժեք.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(լարային_արժեք.ուղարկել[0][0]==0x42&&լարային_արժեք.ուղարկել[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(լարային_արժեք.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&սարք_արժեք,전문)==ERR_MEM);pbuf_free(전문);
    memset(լարային_արժեք.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&սարք_արժեք);assert(들어온수==1&&լարային_արժեք.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&սարք_արժեք);
    assert(լարային_արժեք.소비==0&&들어온수==1&&լարային_արժեք.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&սարք_արժեք);assert(!netif_is_link_up(&սարք_արժեք));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
