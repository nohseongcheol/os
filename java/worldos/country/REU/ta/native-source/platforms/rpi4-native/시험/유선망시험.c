/* 가짜 MMIO/MDIO 장치로 சுழற்சி_மதிப்பு வழிதல்_மதிப்பு·நீளம்_மதிப்பு·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t பதிவு_செய்_மதிப்பு[0x10000/4];
#define 유선저장기(முகவரி) பதிவு_செய்_மதிப்பு[(முகவரி)/4]
#define JKOROS_GENET_TEST 1
#include "../பிணையம்_அடுக்கு_49fba3da/கம்பியிலான_பிணையம்.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t சொல்_உரை=유선저장기(0xe14);
    if(물리작동&&(சொல்_உரை&(1u<<29))){unsigned முகவரி=(சொல்_உரை>>21)&31,அடைவு=(சொல்_உரை>>16)&31;
        if(முகவரி!=1)유선저장기(0xe14)=1<<28;
        else{if(((சொல்_உரை>>26)&3)==1)물리값[அடைவு]=சொல்_உரை&65535;유선저장기(0xe14)=물리값[அடைவு];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int போர்டு_இயந்திரம்_முகவரி(unsigned char *முகவரி){const unsigned char மதிப்பு[]={2,1,2,3,4,5};memcpy(முகவரி,மதிப்பு,6);return 1;}
void netif_set_link_up(struct netif *சாதனம்_மதிப்பு){சாதனம்_மதிப்பு->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *சாதனம்_மதிப்பு){சாதனம்_மதிப்பு->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *சாதனம்_மதிப்பு,struct pbuf *전문,const ip4_addr_t *முகவரி){(void)சாதனம்_மதிப்பு;(void)전문;(void)முகவரி;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer அடுக்கு_அடைவு,u16_t 수,pbuf_type 종류){
    (void)அடுக்கு_அடைவு;(void)종류;struct pbuf *தரவு=calloc(1,sizeof(*தரவு)+수);assert(தரவு);தரவு->payload=தரவு+1;தரவு->len=தரவு->tot_len=수;return தரவு;
}
u8_t pbuf_free(struct pbuf *தரவு){free(தரவு);return 1;}
err_t pbuf_take(struct pbuf *தரவு,const void *원본,u16_t 수){assert(수<=தரவு->len);memcpy(தரவு->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *தரவு,void *இலக்கு_மதிப்பு,u16_t 수,u16_t செயல்படுத்துக){assert(செயல்படுத்துக+수<=தரவு->len);memcpy(இலக்கு_மதிப்பு,(char*)தரவு->payload+செயல்படுத்துக,수);return 수;}
static err_t ஏற்றுக்கொள்_இணைப்பு(struct pbuf *தரவு,struct netif *சாதனம்_மதிப்பு){(void)சாதனம்_மதிப்பு;assert(தரவு->len==60);assert(((unsigned char*)தரவு->payload)[0]==0x42);들어온수++;pbuf_free(தரவு);return ERR_OK;}
int main(void){
    struct netif சாதனம்_மதிப்பு;memset(&சாதனம்_மதிப்பு,0,sizeof(சாதனம்_மதிப்பு));சாதனம்_மதிப்பு.input=ஏற்றுக்கொள்_இணைப்பு;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(தயார்படுத்த_கம்பியிலான_பிணையம்(&சாதனம்_மதிப்பு)==ERR_OK);assert(கம்பியிலான_மதிப்பு.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&சாதனம்_மதிப்பு);assert(netif_is_link_up(&சாதனம்_மதிப்பு));assert(கம்பியிலான_மதிப்பு.속도==1000);
    கம்பியிலான_மதிப்பு.생산=கம்பியிலான_மதிப்பு.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&சாதனம்_மதிப்பு,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=கம்பியிலான_மதிப்பு.생산;}
    assert(கம்பியிலான_மதிப்பு.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(கம்பியிலான_மதிப்பு.அனுப்பு[0][0]==0x42&&கம்பியிலான_மதிப்பு.அனுப்பு[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(கம்பியிலான_மதிப்பு.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&சாதனம்_மதிப்பு,전문)==ERR_MEM);pbuf_free(전문);
    memset(கம்பியிலான_மதிப்பு.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&சாதனம்_மதிப்பு);assert(들어온수==1&&கம்பியிலான_மதிப்பு.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&சாதனம்_மதிப்பு);
    assert(கம்பியிலான_மதிப்பு.소비==0&&들어온수==1&&கம்பியிலான_மதிப்பு.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&சாதனம்_மதிப்பு);assert(!netif_is_link_up(&சாதனம்_மதிப்பு));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
