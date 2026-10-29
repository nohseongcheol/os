/* 가짜 MMIO/MDIO 장치로 ଲୁପ୍_ମୂଲ୍ୟ ଅଧିକ୍ରମଣ_ମୂଲ୍ୟ·ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ମୂଲ୍ୟ[0x10000/4];
#define 유선저장기(ଠିକଣା) ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ମୂଲ୍ୟ[(ଠିକଣା)/4]
#define JKOROS_GENET_TEST 1
#include "../ନେଟ୍_ୱାର୍କ୍_ଗଦା/ତାରଯୁକ୍ତ_ନେଟ୍_ୱାର୍କ୍.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t 말=유선저장기(0xe14);
    if(물리작동&&(말&(1u<<29))){unsigned ଠିକଣା=(말>>21)&31,ଅନୁକ୍ରମଣିକା=(말>>16)&31;
        if(ଠିକଣା!=1)유선저장기(0xe14)=1<<28;
        else{if(((말>>26)&3)==1)물리값[ଅନୁକ୍ରମଣିକା]=말&65535;유선저장기(0xe14)=물리값[ଅନୁକ୍ରମଣିକା];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int ବୋର୍ଡ୍_ମେସିନ୍_ଠିକଣା(unsigned char *ଠିକଣା){const unsigned char ମୂଲ୍ୟ[]={2,1,2,3,4,5};memcpy(ଠିକଣା,ମୂଲ୍ୟ,6);return 1;}
void netif_set_link_up(struct netif *ଡିଭାଇସ_ମୂଲ୍ୟ){ଡିଭାଇସ_ମୂଲ୍ୟ->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ଡିଭାଇସ_ମୂଲ୍ୟ){ଡିଭାଇସ_ମୂଲ୍ୟ->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ଡିଭାଇସ_ମୂଲ୍ୟ,struct pbuf *전문,const ip4_addr_t *ଠିକଣା){(void)ଡିଭାଇସ_ମୂଲ୍ୟ;(void)전문;(void)ଠିକଣା;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ସ୍ତର_ଅନୁକ୍ରମଣିକା,u16_t 수,pbuf_type 종류){
    (void)ସ୍ତର_ଅନୁକ୍ରମଣିକା;(void)종류;struct pbuf *ଡାଟା=calloc(1,sizeof(*ଡାଟା)+수);assert(ଡାଟା);ଡାଟା->payload=ଡାଟା+1;ଡାଟା->len=ଡାଟା->tot_len=수;return ଡାଟା;
}
u8_t pbuf_free(struct pbuf *ଡାଟା){free(ଡାଟା);return 1;}
err_t pbuf_take(struct pbuf *ଡାଟା,const void *원본,u16_t 수){assert(수<=ଡାଟା->len);memcpy(ଡାଟା->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ଡାଟା,void *ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ,u16_t 수,u16_t ଚଳାନ୍ତୁ){assert(ଚଳାନ୍ତୁ+수<=ଡାଟା->len);memcpy(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ,(char*)ଡାଟା->payload+ଚଳାନ୍ତୁ,수);return 수;}
static err_t ସ୍ୱୀକାର_କରିବା_ସଂଯୋଗ(struct pbuf *ଡାଟା,struct netif *ଡିଭାଇସ_ମୂଲ୍ୟ){(void)ଡିଭାଇସ_ମୂଲ୍ୟ;assert(ଡାଟା->len==60);assert(((unsigned char*)ଡାଟା->payload)[0]==0x42);들어온수++;pbuf_free(ଡାଟା);return ERR_OK;}
int main(void){
    struct netif ଡିଭାଇସ_ମୂଲ୍ୟ;memset(&ଡିଭାଇସ_ମୂଲ୍ୟ,0,sizeof(ଡିଭାଇସ_ମୂଲ୍ୟ));ଡିଭାଇସ_ମୂଲ୍ୟ.input=ସ୍ୱୀକାର_କରିବା_ସଂଯୋଗ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(ପ୍ରସ୍ତୁତ_ତାରଯୁକ୍ତ_ନେଟ୍_ୱାର୍କ୍(&ଡିଭାଇସ_ମୂଲ୍ୟ)==ERR_OK);assert(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ଡିଭାଇସ_ମୂଲ୍ୟ);assert(netif_is_link_up(&ଡିଭାଇସ_ମୂଲ୍ୟ));assert(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.속도==1000);
    ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산=ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ଡିଭାଇସ_ମୂଲ୍ୟ,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산;}
    assert(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ପଠାନ୍ତୁ[0][0]==0x42&&ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ପଠାନ୍ତୁ[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ଡିଭାଇସ_ମୂଲ୍ୟ,전문)==ERR_MEM);pbuf_free(전문);
    memset(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ଡିଭାଇସ_ମୂଲ୍ୟ);assert(들어온수==1&&ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ଡିଭାଇସ_ମୂଲ୍ୟ);
    assert(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.소비==0&&들어온수==1&&ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ଡିଭାଇସ_ମୂଲ୍ୟ);assert(!netif_is_link_up(&ଡିଭାଇସ_ମୂଲ୍ୟ));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
