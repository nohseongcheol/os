/* 가짜 MMIO/MDIO 장치로 ደጋግም_ዋጋ ፍሳስ_ዋጋ·ንውሓት_ዋጋ·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(ኣድራሻ) 저장기[(ኣድራሻ)/4]
#define JKOROS_GENET_TEST 1
#include "../ማሕበራዊ_ኔትወርክ_ድርደራ/유선망.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t ናይ_ቃል_ጸወታ_ጽሑፍ=유선저장기(0xe14);
    if(물리작동&&(ናይ_ቃል_ጸወታ_ጽሑፍ&(1u<<29))){unsigned ኣድራሻ=(ናይ_ቃል_ጸወታ_ጽሑፍ>>21)&31,መሐበሪ=(ናይ_ቃል_ጸወታ_ጽሑፍ>>16)&31;
        if(ኣድራሻ!=1)유선저장기(0xe14)=1<<28;
        else{if(((ናይ_ቃል_ጸወታ_ጽሑፍ>>26)&3)==1)물리값[መሐበሪ]=ናይ_ቃል_ጸወታ_ጽሑፍ&65535;유선저장기(0xe14)=물리값[መሐበሪ];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *ኣድራሻ){const unsigned char ዋጋ[]={2,1,2,3,4,5};memcpy(ኣድራሻ,ዋጋ,6);return 1;}
void netif_set_link_up(struct netif *መሳርሒ_ዋጋ){መሳርሒ_ዋጋ->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *መሳርሒ_ዋጋ){መሳርሒ_ዋጋ->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *መሳርሒ_ዋጋ,struct pbuf *전문,const ip4_addr_t *ኣድራሻ){(void)መሳርሒ_ዋጋ;(void)전문;(void)ኣድራሻ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ንጻፍ_መሐበሪ,u16_t 수,pbuf_type 종류){
    (void)ንጻፍ_መሐበሪ;(void)종류;struct pbuf *ሓበሬታ=calloc(1,sizeof(*ሓበሬታ)+수);assert(ሓበሬታ);ሓበሬታ->payload=ሓበሬታ+1;ሓበሬታ->len=ሓበሬታ->tot_len=수;return ሓበሬታ;
}
u8_t pbuf_free(struct pbuf *ሓበሬታ){free(ሓበሬታ);return 1;}
err_t pbuf_take(struct pbuf *ሓበሬታ,const void *원본,u16_t 수){assert(수<=ሓበሬታ->len);memcpy(ሓበሬታ->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ሓበሬታ,void *መዓልቦ_ዋጋ,u16_t 수,u16_t ኣኺድ){assert(ኣኺድ+수<=ሓበሬታ->len);memcpy(መዓልቦ_ዋጋ,(char*)ሓበሬታ->payload+ኣኺድ,수);return 수;}
static err_t ተቐበል_ርክብ(struct pbuf *ሓበሬታ,struct netif *መሳርሒ_ዋጋ){(void)መሳርሒ_ዋጋ;assert(ሓበሬታ->len==60);assert(((unsigned char*)ሓበሬታ->payload)[0]==0x42);들어온수++;pbuf_free(ሓበሬታ);return ERR_OK;}
int main(void){
    struct netif መሳርሒ_ዋጋ;memset(&መሳርሒ_ዋጋ,0,sizeof(መሳርሒ_ዋጋ));መሳርሒ_ዋጋ.input=ተቐበል_ርክብ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(유선망준비(&መሳርሒ_ዋጋ)==ERR_OK);assert(유선.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&መሳርሒ_ዋጋ);assert(netif_is_link_up(&መሳርሒ_ዋጋ));assert(유선.속도==1000);
    유선.생산=유선.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&መሳርሒ_ዋጋ,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=유선.생산;}
    assert(유선.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(유선.ለኣኽ[0][0]==0x42&&유선.ለኣኽ[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(유선.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&መሳርሒ_ዋጋ,전문)==ERR_MEM);pbuf_free(전문);
    memset(유선.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&መሳርሒ_ዋጋ);assert(들어온수==1&&유선.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&መሳርሒ_ዋጋ);
    assert(유선.소비==0&&들어온수==1&&유선.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&መሳርሒ_ዋጋ);assert(!netif_is_link_up(&መሳርሒ_ዋጋ));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
