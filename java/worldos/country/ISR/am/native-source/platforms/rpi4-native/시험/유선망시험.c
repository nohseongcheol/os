/* 가짜 MMIO/MDIO 장치로 ድግግሞሽ_እሴት መትረፍ_እሴት·ርዝመት_እሴት·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t መዝግብ_እሴት[0x10000/4];
#define 유선저장기(አድራሻ) መዝግብ_እሴት[(አድራሻ)/4]
#define JKOROS_GENET_TEST 1
#include "../መረብ_ክምር/ባለሽቦ_መረብ.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t ቃል_ጽሁፍ=유선저장기(0xe14);
    if(물리작동&&(ቃል_ጽሁፍ&(1u<<29))){unsigned አድራሻ=(ቃል_ጽሁፍ>>21)&31,መረጃ_ጠቆመ=(ቃል_ጽሁፍ>>16)&31;
        if(አድራሻ!=1)유선저장기(0xe14)=1<<28;
        else{if(((ቃል_ጽሁፍ>>26)&3)==1)물리값[መረጃ_ጠቆመ]=ቃል_ጽሁፍ&65535;유선저장기(0xe14)=물리값[መረጃ_ጠቆመ];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int ቦርድ_ማሽን_አድራሻ(unsigned char *አድራሻ){const unsigned char እሴት[]={2,1,2,3,4,5};memcpy(አድራሻ,እሴት,6);return 1;}
void netif_set_link_up(struct netif *መሳሪያ_እሴት){መሳሪያ_እሴት->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *መሳሪያ_እሴት){መሳሪያ_እሴት->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *መሳሪያ_እሴት,struct pbuf *전문,const ip4_addr_t *አድራሻ){(void)መሳሪያ_እሴት;(void)전문;(void)አድራሻ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ንብርብር_መረጃ_ጠቆመ,u16_t 수,pbuf_type 종류){
    (void)ንብርብር_መረጃ_ጠቆመ;(void)종류;struct pbuf *ውሂብ=calloc(1,sizeof(*ውሂብ)+수);assert(ውሂብ);ውሂብ->payload=ውሂብ+1;ውሂብ->len=ውሂብ->tot_len=수;return ውሂብ;
}
u8_t pbuf_free(struct pbuf *ውሂብ){free(ውሂብ);return 1;}
err_t pbuf_take(struct pbuf *ውሂብ,const void *원본,u16_t 수){assert(수<=ውሂብ->len);memcpy(ውሂብ->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ውሂብ,void *መድረሻ_እሴት,u16_t 수,u16_t ማስኬጃ){assert(ማስኬጃ+수<=ውሂብ->len);memcpy(መድረሻ_እሴት,(char*)ውሂብ->payload+ማስኬጃ,수);return 수;}
static err_t ተቀበል_ግንኙነት(struct pbuf *ውሂብ,struct netif *መሳሪያ_እሴት){(void)መሳሪያ_እሴት;assert(ውሂብ->len==60);assert(((unsigned char*)ውሂብ->payload)[0]==0x42);들어온수++;pbuf_free(ውሂብ);return ERR_OK;}
int main(void){
    struct netif መሳሪያ_እሴት;memset(&መሳሪያ_እሴት,0,sizeof(መሳሪያ_እሴት));መሳሪያ_እሴት.input=ተቀበል_ግንኙነት;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(አዘጋጅ_ባለሽቦ_መረብ(&መሳሪያ_እሴት)==ERR_OK);assert(ባለሽቦ_እሴት.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&መሳሪያ_እሴት);assert(netif_is_link_up(&መሳሪያ_እሴት));assert(ባለሽቦ_እሴት.속도==1000);
    ባለሽቦ_እሴት.생산=ባለሽቦ_እሴት.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&መሳሪያ_እሴት,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ባለሽቦ_እሴት.생산;}
    assert(ባለሽቦ_እሴት.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ባለሽቦ_እሴት.ላክ[0][0]==0x42&&ባለሽቦ_እሴት.ላክ[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ባለሽቦ_እሴት.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&መሳሪያ_እሴት,전문)==ERR_MEM);pbuf_free(전문);
    memset(ባለሽቦ_እሴት.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&መሳሪያ_እሴት);assert(들어온수==1&&ባለሽቦ_እሴት.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&መሳሪያ_እሴት);
    assert(ባለሽቦ_እሴት.소비==0&&들어온수==1&&ባለሽቦ_እሴት.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&መሳሪያ_እሴት);assert(!netif_is_link_up(&መሳሪያ_እሴት));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
