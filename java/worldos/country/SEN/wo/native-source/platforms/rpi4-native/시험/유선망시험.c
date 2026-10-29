/* 가짜 MMIO/MDIO 장치로 wërngël_xëyma luëppe_xëyma·diir_xëyma·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t bindu_xëyma[0x10000/4];
#define 유선저장기(dëkkuwaay) bindu_xëyma[(dëkkuwaay)/4]
#define JKOROS_GENET_TEST 1
#include "../mbaal_Tegalo/tënku_mbaal.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned dëkkuwaay=(Word_SMS>>21)&31,àlluwa_tur=(Word_SMS>>16)&31;
        if(dëkkuwaay!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[àlluwa_tur]=Word_SMS&65535;유선저장기(0xe14)=물리값[àlluwa_tur];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *dëkkuwaay){const unsigned char xëyma[]={2,1,2,3,4,5};memcpy(dëkkuwaay,xëyma,6);return 1;}
void netif_set_link_up(struct netif *toftal_xëyma){toftal_xëyma->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *toftal_xëyma){toftal_xëyma->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *toftal_xëyma,struct pbuf *전문,const ip4_addr_t *dëkkuwaay){(void)toftal_xëyma;(void)전문;(void)dëkkuwaay;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer déggoob_wet_àlluwa_tur,u16_t 수,pbuf_type 종류){
    (void)déggoob_wet_àlluwa_tur;(void)종류;struct pbuf *mbir=calloc(1,sizeof(*mbir)+수);assert(mbir);mbir->payload=mbir+1;mbir->len=mbir->tot_len=수;return mbir;
}
u8_t pbuf_free(struct pbuf *mbir){free(mbir);return 1;}
err_t pbuf_take(struct pbuf *mbir,const void *원본,u16_t 수){assert(수<=mbir->len);memcpy(mbir->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *mbir,void *jëmmukaay_xëyma,u16_t 수,u16_t daw){assert(daw+수<=mbir->len);memcpy(jëmmukaay_xëyma,(char*)mbir->payload+daw,수);return 수;}
static err_t nangu_jokkalóo(struct pbuf *mbir,struct netif *toftal_xëyma){(void)toftal_xëyma;assert(mbir->len==60);assert(((unsigned char*)mbir->payload)[0]==0x42);들어온수++;pbuf_free(mbir);return ERR_OK;}
int main(void){
    struct netif toftal_xëyma;memset(&toftal_xëyma,0,sizeof(toftal_xëyma));toftal_xëyma.input=nangu_jokkalóo;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(jël_matuwaay_tënku_mbaal(&toftal_xëyma)==ERR_OK);assert(tënku_xëyma.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&toftal_xëyma);assert(netif_is_link_up(&toftal_xëyma));assert(tënku_xëyma.속도==1000);
    tënku_xëyma.생산=tënku_xëyma.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&toftal_xëyma,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=tënku_xëyma.생산;}
    assert(tënku_xëyma.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(tënku_xëyma.Yónnee[0][0]==0x42&&tënku_xëyma.Yónnee[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(tënku_xëyma.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&toftal_xëyma,전문)==ERR_MEM);pbuf_free(전문);
    memset(tënku_xëyma.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&toftal_xëyma);assert(들어온수==1&&tënku_xëyma.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&toftal_xëyma);
    assert(tënku_xëyma.소비==0&&들어온수==1&&tënku_xëyma.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&toftal_xëyma);assert(!netif_is_link_up(&toftal_xëyma));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
