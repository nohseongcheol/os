/* 가짜 MMIO/MDIO 장치로 लूप_मोल ओवरफ्लो_मोल·लांबाय_मोल·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t नोंदणी_मोल[0x10000/4];
#define 유선저장기(नामो) नोंदणी_मोल[(नामो)/4]
#define JKOROS_GENET_TEST 1
#include "../नॅटवर्क_स्टॅक/वायर्ड_नॅटवर्क.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned नामो=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(नामो!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int बोर्ड_यंत्र_नामो(unsigned char *नामो){const unsigned char मोल[]={2,1,2,3,4,5};memcpy(नामो,मोल,6);return 1;}
void netif_set_link_up(struct netif *मोबायल_मोल){मोबायल_मोल->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *मोबायल_मोल){मोबायल_मोल->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *मोबायल_मोल,struct pbuf *전문,const ip4_addr_t *नामो){(void)मोबायल_मोल;(void)전문;(void)नामो;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer थर_INDEX,u16_t 수,pbuf_type 종류){
    (void)थर_INDEX;(void)종류;struct pbuf *डेटा=calloc(1,sizeof(*डेटा)+수);assert(डेटा);डेटा->payload=डेटा+1;डेटा->len=डेटा->tot_len=수;return डेटा;
}
u8_t pbuf_free(struct pbuf *डेटा){free(डेटा);return 1;}
err_t pbuf_take(struct pbuf *डेटा,const void *원본,u16_t 수){assert(수<=डेटा->len);memcpy(डेटा->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *डेटा,void *नियुक्त_स्थान_मोल,u16_t 수,u16_t चलोवप){assert(चलोवप+수<=डेटा->len);memcpy(नियुक्त_स्थान_मोल,(char*)डेटा->payload+चलोवप,수);return 수;}
static err_t स्विकारचें_कनॅक्शन(struct pbuf *डेटा,struct netif *मोबायल_मोल){(void)मोबायल_मोल;assert(डेटा->len==60);assert(((unsigned char*)डेटा->payload)[0]==0x42);들어온수++;pbuf_free(डेटा);return ERR_OK;}
int main(void){
    struct netif मोबायल_मोल;memset(&मोबायल_मोल,0,sizeof(मोबायल_मोल));मोबायल_मोल.input=स्विकारचें_कनॅक्शन;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(तयार_करचें_वायर्ड_नॅटवर्क(&मोबायल_मोल)==ERR_OK);assert(वायर्ड_मोल.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&मोबायल_मोल);assert(netif_is_link_up(&मोबायल_मोल));assert(वायर्ड_मोल.속도==1000);
    वायर्ड_मोल.생산=वायर्ड_मोल.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&मोबायल_मोल,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=वायर्ड_मोल.생산;}
    assert(वायर्ड_मोल.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(वायर्ड_मोल.धाडचें[0][0]==0x42&&वायर्ड_मोल.धाडचें[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(वायर्ड_मोल.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&मोबायल_मोल,전문)==ERR_MEM);pbuf_free(전문);
    memset(वायर्ड_मोल.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&मोबायल_मोल);assert(들어온수==1&&वायर्ड_मोल.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&मोबायल_मोल);
    assert(वायर्ड_मोल.소비==0&&들어온수==1&&वायर्ड_मोल.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&मोबायल_मोल);assert(!netif_is_link_up(&मोबायल_मोल));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
