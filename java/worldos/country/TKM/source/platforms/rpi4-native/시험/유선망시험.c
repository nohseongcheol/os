/* 가짜 MMIO/MDIO 장치로 sikl_baha gyrmalanma_baha·dowamlylyk_baha·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(salgy) 저장기[(salgy)/4]
#define JKOROS_GENET_TEST 1
#include "../Tor_Desse/simli_Tor.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Söz_SMS=유선저장기(0xe14);
    if(물리작동&&(Söz_SMS&(1u<<29))){unsigned salgy=(Söz_SMS>>21)&31,indeks=(Söz_SMS>>16)&31;
        if(salgy!=1)유선저장기(0xe14)=1<<28;
        else{if(((Söz_SMS>>26)&3)==1)물리값[indeks]=Söz_SMS&65535;유선저장기(0xe14)=물리값[indeks];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *salgy){const unsigned char baha[]={2,1,2,3,4,5};memcpy(salgy,baha,6);return 1;}
void netif_set_link_up(struct netif *enjam_baha){enjam_baha->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *enjam_baha){enjam_baha->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *enjam_baha,struct pbuf *전문,const ip4_addr_t *salgy){(void)enjam_baha;(void)전문;(void)salgy;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer dereje_indeks,u16_t 수,pbuf_type 종류){
    (void)dereje_indeks;(void)종류;struct pbuf *maglumat=calloc(1,sizeof(*maglumat)+수);assert(maglumat);maglumat->payload=maglumat+1;maglumat->len=maglumat->tot_len=수;return maglumat;
}
u8_t pbuf_free(struct pbuf *maglumat){free(maglumat);return 1;}
err_t pbuf_take(struct pbuf *maglumat,const void *원본,u16_t 수){assert(수<=maglumat->len);memcpy(maglumat->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *maglumat,void *barylmaly_ýer_baha,u16_t 수,u16_t Bitir){assert(Bitir+수<=maglumat->len);memcpy(barylmaly_ýer_baha,(char*)maglumat->payload+Bitir,수);return 수;}
static err_t kabul_et_birikme(struct pbuf *maglumat,struct netif *enjam_baha){(void)enjam_baha;assert(maglumat->len==60);assert(((unsigned char*)maglumat->payload)[0]==0x42);들어온수++;pbuf_free(maglumat);return ERR_OK;}
int main(void){
    struct netif enjam_baha;memset(&enjam_baha,0,sizeof(enjam_baha));enjam_baha.input=kabul_et_birikme;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Taýýarla_simli_Tor(&enjam_baha)==ERR_OK);assert(simli_baha.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&enjam_baha);assert(netif_is_link_up(&enjam_baha));assert(simli_baha.속도==1000);
    simli_baha.생산=simli_baha.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&enjam_baha,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=simli_baha.생산;}
    assert(simli_baha.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(simli_baha.iber[0][0]==0x42&&simli_baha.iber[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(simli_baha.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&enjam_baha,전문)==ERR_MEM);pbuf_free(전문);
    memset(simli_baha.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&enjam_baha);assert(들어온수==1&&simli_baha.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&enjam_baha);
    assert(simli_baha.소비==0&&들어온수==1&&simli_baha.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&enjam_baha);assert(!netif_is_link_up(&enjam_baha));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
