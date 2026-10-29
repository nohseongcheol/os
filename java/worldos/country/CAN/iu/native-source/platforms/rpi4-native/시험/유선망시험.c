/* 가짜 MMIO/MDIO 장치로 piliqqittaajuq_atuutilik tatattuq_atuutilik·takininga_atuutilik·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(turaarut) 저장기[(turaarut)/4]
#define JKOROS_GENET_TEST 1
#include "../통신망/nukillautilik_Kasuqatigiitsimajut.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t 말=유선저장기(0xe14);
    if(물리작동&&(말&(1u<<29))){unsigned turaarut=(말>>21)&31,nalunaiqsimavik=(말>>16)&31;
        if(turaarut!=1)유선저장기(0xe14)=1<<28;
        else{if(((말>>26)&3)==1)물리값[nalunaiqsimavik]=말&65535;유선저장기(0xe14)=물리값[nalunaiqsimavik];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *turaarut){const unsigned char atuutilik[]={2,1,2,3,4,5};memcpy(turaarut,atuutilik,6);return 1;}
void netif_set_link_up(struct netif *sunakkutaaq_atuutilik){sunakkutaaq_atuutilik->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *sunakkutaaq_atuutilik){sunakkutaaq_atuutilik->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *sunakkutaaq_atuutilik,struct pbuf *전문,const ip4_addr_t *turaarut){(void)sunakkutaaq_atuutilik;(void)전문;(void)turaarut;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer qaliriit_nalunaiqsimavik,u16_t 수,pbuf_type 종류){
    (void)qaliriit_nalunaiqsimavik;(void)종류;struct pbuf *titiqqat=calloc(1,sizeof(*titiqqat)+수);assert(titiqqat);titiqqat->payload=titiqqat+1;titiqqat->len=titiqqat->tot_len=수;return titiqqat;
}
u8_t pbuf_free(struct pbuf *titiqqat){free(titiqqat);return 1;}
err_t pbuf_take(struct pbuf *titiqqat,const void *원본,u16_t 수){assert(수<=titiqqat->len);memcpy(titiqqat->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *titiqqat,void *namunngarvik_atuutilik,u16_t 수,u16_t 시작){assert(시작+수<=titiqqat->len);memcpy(namunngarvik_atuutilik,(char*)titiqqat->payload+시작,수);return 수;}
static err_t 받음(struct pbuf *titiqqat,struct netif *sunakkutaaq_atuutilik){(void)sunakkutaaq_atuutilik;assert(titiqqat->len==60);assert(((unsigned char*)titiqqat->payload)[0]==0x42);들어온수++;pbuf_free(titiqqat);return ERR_OK;}
int main(void){
    struct netif sunakkutaaq_atuutilik;memset(&sunakkutaaq_atuutilik,0,sizeof(sunakkutaaq_atuutilik));sunakkutaaq_atuutilik.input=받음;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Parnalli_nukillautilik_Kasuqatigiitsimajut(&sunakkutaaq_atuutilik)==ERR_OK);assert(nukillautilik_atuutilik.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&sunakkutaaq_atuutilik);assert(netif_is_link_up(&sunakkutaaq_atuutilik));assert(nukillautilik_atuutilik.속도==1000);
    nukillautilik_atuutilik.생산=nukillautilik_atuutilik.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&sunakkutaaq_atuutilik,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=nukillautilik_atuutilik.생산;}
    assert(nukillautilik_atuutilik.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(nukillautilik_atuutilik.nassiutili[0][0]==0x42&&nukillautilik_atuutilik.nassiutili[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(nukillautilik_atuutilik.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&sunakkutaaq_atuutilik,전문)==ERR_MEM);pbuf_free(전문);
    memset(nukillautilik_atuutilik.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&sunakkutaaq_atuutilik);assert(들어온수==1&&nukillautilik_atuutilik.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&sunakkutaaq_atuutilik);
    assert(nukillautilik_atuutilik.소비==0&&들어온수==1&&nukillautilik_atuutilik.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&sunakkutaaq_atuutilik);assert(!netif_is_link_up(&sunakkutaaq_atuutilik));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
