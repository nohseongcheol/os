/* 가짜 MMIO/MDIO 장치로 Loop_balio 넘침·luzera_balio·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t izena_eman_balio[0x10000/4];
#define 유선저장기(helbide) izena_eman_balio[(helbide)/4]
#define JKOROS_GENET_TEST 1
#include "../sare_pila/haridun_sare.c"
static uintptr_t denbora_zigilu_balio;
static int 물리작동=1,실물=1,Sarrerakoa_ZENBATU;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned helbide=(Word_SMS>>21)&31,INDIZE=(Word_SMS>>16)&31;
        if(helbide!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDIZE]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDIZE];}}
    return denbora_zigilu_balio++;
}
int 보드실물(void){return 실물;}
int arbel_gailu_helbide(unsigned char *helbide){const unsigned char balio[]={2,1,2,3,4,5};memcpy(helbide,balio,6);return 1;}
void netif_set_link_up(struct netif *gailu_balio){gailu_balio->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *gailu_balio){gailu_balio->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *gailu_balio,struct pbuf *전문,const ip4_addr_t *helbide){(void)gailu_balio;(void)전문;(void)helbide;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer maila_INDIZE,u16_t 수,pbuf_type 종류){
    (void)maila_INDIZE;(void)종류;struct pbuf *datuak=calloc(1,sizeof(*datuak)+수);assert(datuak);datuak->payload=datuak+1;datuak->len=datuak->tot_len=수;return datuak;
}
u8_t pbuf_free(struct pbuf *datuak){free(datuak);return 1;}
err_t pbuf_take(struct pbuf *datuak,const void *원본,u16_t 수){assert(수<=datuak->len);memcpy(datuak->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *datuak,void *helburu_balio_a0fbc067,u16_t 수,u16_t Exekutatu_2){assert(Exekutatu_2+수<=datuak->len);memcpy(helburu_balio_a0fbc067,(char*)datuak->payload+Exekutatu_2,수);return 수;}
static err_t onartu_konexio(struct pbuf *datuak,struct netif *gailu_balio){(void)gailu_balio;assert(datuak->len==60);assert(((unsigned char*)datuak->payload)[0]==0x42);Sarrerakoa_ZENBATU++;pbuf_free(datuak);return ERR_OK;}
int main(void){
    struct netif gailu_balio;memset(&gailu_balio,0,sizeof(gailu_balio));gailu_balio.input=onartu_konexio;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(유선망준비(&gailu_balio)==ERR_OK);assert(haridun_balio.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&gailu_balio);assert(netif_is_link_up(&gailu_balio));assert(haridun_balio.속도==1000);
    haridun_balio.생산=haridun_balio.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&gailu_balio,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=haridun_balio.생산;}
    assert(haridun_balio.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(haridun_balio.bidali[0][0]==0x42&&haridun_balio.bidali[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(haridun_balio.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&gailu_balio,전문)==ERR_MEM);pbuf_free(전문);
    memset(haridun_balio.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&gailu_balio);assert(Sarrerakoa_ZENBATU==1&&haridun_balio.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&gailu_balio);
    assert(haridun_balio.소비==0&&Sarrerakoa_ZENBATU==1&&haridun_balio.집계[4]==1);
    물리값[1]=0;denbora_zigilu_balio+=1000;유선망살피기(&gailu_balio);assert(!netif_is_link_up(&gailu_balio));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
