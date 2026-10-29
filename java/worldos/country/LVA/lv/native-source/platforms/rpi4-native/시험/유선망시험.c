/* 가짜 MMIO/MDIO 장치로 Loop_VALUE pārpilde_VALUE·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t reģistrs_VALUE[0x10000/4];
#define 유선저장기(adrese) reģistrs_VALUE[(adrese)/4]
#define JKOROS_GENET_TEST 1
#include "../tīkls_kopa/vadu_tīkls.c"
static uintptr_t timestamp_VALUE;
static int 물리작동=1,실물=1,Ienākošs_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned adrese=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(adrese!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return timestamp_VALUE++;
}
int 보드실물(void){return 실물;}
int Panelis_reālā_adrese(unsigned char *adrese){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(adrese,VALUE,6);return 1;}
void netif_set_link_up(struct netif *ierīce_VALUE){ierīce_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ierīce_VALUE){ierīce_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ierīce_VALUE,struct pbuf *datogramma,const ip4_addr_t *adrese){(void)ierīce_VALUE;(void)datogramma;(void)adrese;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer slānis_INDEX,u16_t numurs,pbuf_type 종류){
    (void)slānis_INDEX;(void)종류;struct pbuf *dati=calloc(1,sizeof(*dati)+numurs);assert(dati);dati->payload=dati+1;dati->len=dati->tot_len=numurs;return dati;
}
u8_t pbuf_free(struct pbuf *dati){free(dati);return 1;}
err_t pbuf_take(struct pbuf *dati,const void *원본,u16_t numurs){assert(numurs<=dati->len);memcpy(dati->payload,원본,numurs);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *dati,void *mērķis_VALUE,u16_t numurs,u16_t Palaist){assert(Palaist+numurs<=dati->len);memcpy(mērķis_VALUE,(char*)dati->payload+Palaist,numurs);return numurs;}
static err_t akceptēt_paziņa(struct pbuf *dati,struct netif *ierīce_VALUE){(void)ierīce_VALUE;assert(dati->len==60);assert(((unsigned char*)dati->payload)[0]==0x42);Ienākošs_COUNT++;pbuf_free(dati);return ERR_OK;}
int main(void){
    struct netif ierīce_VALUE;memset(&ierīce_VALUE,0,sizeof(ierīce_VALUE));ierīce_VALUE.input=akceptēt_paziņa;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Sagatavot_vadu_tīkls(&ierīce_VALUE)==ERR_OK);assert(vadu_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ierīce_VALUE);assert(netif_is_link_up(&ierīce_VALUE));assert(vadu_VALUE.속도==1000);
    vadu_VALUE.생산=vadu_VALUE.patērēt_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datogramma=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datogramma->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(sūtīt_datogramma(&ierīce_VALUE,datogramma)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=vadu_VALUE.생산;}
    assert(vadu_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(vadu_VALUE.sūtīt[0][0]==0x42&&vadu_VALUE.sūtīt[0][59]==0);pbuf_free(datogramma);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(vadu_VALUE.생산-255)&65535;datogramma=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(sūtīt_datogramma(&ierīce_VALUE,datogramma)==ERR_MEM);pbuf_free(datogramma);
    memset(vadu_VALUE.saņemt[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ierīce_VALUE);assert(Ienākošs_COUNT==1&&vadu_VALUE.patērēt_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ierīce_VALUE);
    assert(vadu_VALUE.patērēt_VALUE==0&&Ienākošs_COUNT==1&&vadu_VALUE.집계[4]==1);
    물리값[1]=0;timestamp_VALUE+=1000;유선망살피기(&ierīce_VALUE);assert(!netif_is_link_up(&ierīce_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
