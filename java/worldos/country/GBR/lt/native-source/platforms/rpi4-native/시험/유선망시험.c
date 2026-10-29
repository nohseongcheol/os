/* 가짜 MMIO/MDIO 장치로 Loop_VALUE perpilda_VALUE·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registras_VALUE[0x10000/4];
#define 유선저장기(ADDRESS) registras_VALUE[(ADDRESS)/4]
#define JKOROS_GENET_TEST 1
#include "../tinklas_eilė/laidinis_tinklas.c"
static uintptr_t laiko_žyma_VALUE;
static int 물리작동=1,실물=1,priimta_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned ADDRESS=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(ADDRESS!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return laiko_žyma_VALUE++;
}
int 보드실물(void){return 실물;}
int Lenta_absoliutusis_adresas(unsigned char *ADDRESS){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(ADDRESS,VALUE,6);return 1;}
void netif_set_link_up(struct netif *įrenginys_VALUE){įrenginys_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *įrenginys_VALUE){įrenginys_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *įrenginys_VALUE,struct pbuf *paketų_kelio_schema,const ip4_addr_t *ADDRESS){(void)įrenginys_VALUE;(void)paketų_kelio_schema;(void)ADDRESS;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer sluoksnis_INDEX,u16_t numeris,pbuf_type 종류){
    (void)sluoksnis_INDEX;(void)종류;struct pbuf *duomenys=calloc(1,sizeof(*duomenys)+numeris);assert(duomenys);duomenys->payload=duomenys+1;duomenys->len=duomenys->tot_len=numeris;return duomenys;
}
u8_t pbuf_free(struct pbuf *duomenys){free(duomenys);return 1;}
err_t pbuf_take(struct pbuf *duomenys,const void *원본,u16_t numeris){assert(numeris<=duomenys->len);memcpy(duomenys->payload,원본,numeris);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *duomenys,void *vieta_VALUE,u16_t numeris,u16_t Paleisti){assert(Paleisti+numeris<=duomenys->len);memcpy(vieta_VALUE,(char*)duomenys->payload+Paleisti,numeris);return numeris;}
static err_t priimti_ryšys(struct pbuf *duomenys,struct netif *įrenginys_VALUE){(void)įrenginys_VALUE;assert(duomenys->len==60);assert(((unsigned char*)duomenys->payload)[0]==0x42);priimta_COUNT++;pbuf_free(duomenys);return ERR_OK;}
int main(void){
    struct netif įrenginys_VALUE;memset(&įrenginys_VALUE,0,sizeof(įrenginys_VALUE));įrenginys_VALUE.input=priimti_ryšys;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Parengti_laidinis_tinklas(&įrenginys_VALUE)==ERR_OK);assert(laidinis_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&įrenginys_VALUE);assert(netif_is_link_up(&įrenginys_VALUE));assert(laidinis_VALUE.속도==1000);
    laidinis_VALUE.생산=laidinis_VALUE.vartoti_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *paketų_kelio_schema=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(paketų_kelio_schema->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(siųsti_paketų_kelio_schema(&įrenginys_VALUE,paketų_kelio_schema)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=laidinis_VALUE.생산;}
    assert(laidinis_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(laidinis_VALUE.siųsti[0][0]==0x42&&laidinis_VALUE.siųsti[0][59]==0);pbuf_free(paketų_kelio_schema);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(laidinis_VALUE.생산-255)&65535;paketų_kelio_schema=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(siųsti_paketų_kelio_schema(&įrenginys_VALUE,paketų_kelio_schema)==ERR_MEM);pbuf_free(paketų_kelio_schema);
    memset(laidinis_VALUE.gauti[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&įrenginys_VALUE);assert(priimta_COUNT==1&&laidinis_VALUE.vartoti_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&įrenginys_VALUE);
    assert(laidinis_VALUE.vartoti_VALUE==0&&priimta_COUNT==1&&laidinis_VALUE.집계[4]==1);
    물리값[1]=0;laiko_žyma_VALUE+=1000;유선망살피기(&įrenginys_VALUE);assert(!netif_is_link_up(&įrenginys_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
