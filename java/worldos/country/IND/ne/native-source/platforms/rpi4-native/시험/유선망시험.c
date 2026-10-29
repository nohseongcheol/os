/* 가짜 MMIO/MDIO 장치로 लुप_मान ओभरफ्लो_मान·लम्बाइ_मान·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t दर्ता_मान[0x10000/4];
#define 유선저장기(ठेगाना) दर्ता_मान[(ठेगाना)/4]
#define JKOROS_GENET_TEST 1
#include "../सञ्जाल_चाङ/तार_सहितको_सञ्जाल.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t शब्द_पाठ=유선저장기(0xe14);
    if(물리작동&&(शब्द_पाठ&(1u<<29))){unsigned ठेगाना=(शब्द_पाठ>>21)&31,अनुक्रमणिका=(शब्द_पाठ>>16)&31;
        if(ठेगाना!=1)유선저장기(0xe14)=1<<28;
        else{if(((शब्द_पाठ>>26)&3)==1)물리값[अनुक्रमणिका]=शब्द_पाठ&65535;유선저장기(0xe14)=물리값[अनुक्रमणिका];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int बोर्ड_मेशिन_ठेगाना(unsigned char *ठेगाना){const unsigned char मान[]={2,1,2,3,4,5};memcpy(ठेगाना,मान,6);return 1;}
void netif_set_link_up(struct netif *मोबाइल_मान){मोबाइल_मान->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *मोबाइल_मान){मोबाइल_मान->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *मोबाइल_मान,struct pbuf *전문,const ip4_addr_t *ठेगाना){(void)मोबाइल_मान;(void)전문;(void)ठेगाना;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer तह_अनुक्रमणिका,u16_t 수,pbuf_type 종류){
    (void)तह_अनुक्रमणिका;(void)종류;struct pbuf *लगत=calloc(1,sizeof(*लगत)+수);assert(लगत);लगत->payload=लगत+1;लगत->len=लगत->tot_len=수;return लगत;
}
u8_t pbuf_free(struct pbuf *लगत){free(लगत);return 1;}
err_t pbuf_take(struct pbuf *लगत,const void *원본,u16_t 수){assert(수<=लगत->len);memcpy(लगत->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *लगत,void *गन्तव्य_मान,u16_t 수,u16_t चलाउनुहोस्){assert(चलाउनुहोस्+수<=लगत->len);memcpy(गन्तव्य_मान,(char*)लगत->payload+चलाउनुहोस्,수);return 수;}
static err_t स्वीकार्नुहोस्_जडान(struct pbuf *लगत,struct netif *मोबाइल_मान){(void)मोबाइल_मान;assert(लगत->len==60);assert(((unsigned char*)लगत->payload)[0]==0x42);들어온수++;pbuf_free(लगत);return ERR_OK;}
int main(void){
    struct netif मोबाइल_मान;memset(&मोबाइल_मान,0,sizeof(मोबाइल_मान));मोबाइल_मान.input=स्वीकार्नुहोस्_जडान;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(तयार_गर्नुहोस्_तार_सहितको_सञ्जाल(&मोबाइल_मान)==ERR_OK);assert(तार_सहितको_मान.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&मोबाइल_मान);assert(netif_is_link_up(&मोबाइल_मान));assert(तार_सहितको_मान.속도==1000);
    तार_सहितको_मान.생산=तार_सहितको_मान.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&मोबाइल_मान,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=तार_सहितको_मान.생산;}
    assert(तार_सहितको_मान.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(तार_सहितको_मान.पठाउनुहोस्[0][0]==0x42&&तार_सहितको_मान.पठाउनुहोस्[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(तार_सहितको_मान.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&मोबाइल_मान,전문)==ERR_MEM);pbuf_free(전문);
    memset(तार_सहितको_मान.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&मोबाइल_मान);assert(들어온수==1&&तार_सहितको_मान.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&मोबाइल_मान);
    assert(तार_सहितको_मान.소비==0&&들어온수==1&&तार_सहितको_मान.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&मोबाइल_मान);assert(!netif_is_link_up(&मोबाइल_मान));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
