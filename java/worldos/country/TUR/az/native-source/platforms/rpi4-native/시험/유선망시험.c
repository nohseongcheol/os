/* 가짜 MMIO/MDIO 장치로 Loop_VALUE dolub_daşma_VALUE·uzunluq_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t qeydiyyatdan_keçmək_VALUE[0x10000/4];
#define 유선저장기(ünvan) qeydiyyatdan_keçmək_VALUE[(ünvan)/4]
#define JKOROS_GENET_TEST 1
#include "../Şəbəkə_Yığın/naqilli_Şəbəkə.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,Daxil_olan_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Söz_SMS=유선저장기(0xe14);
    if(물리작동&&(Söz_SMS&(1u<<29))){unsigned ünvan=(Söz_SMS>>21)&31,INDEX=(Söz_SMS>>16)&31;
        if(ünvan!=1)유선저장기(0xe14)=1<<28;
        else{if(((Söz_SMS>>26)&3)==1)물리값[INDEX]=Söz_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int lövhə_maşın_ünvan(unsigned char *ünvan){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(ünvan,VALUE,6);return 1;}
void netif_set_link_up(struct netif *cihaz_VALUE){cihaz_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *cihaz_VALUE){cihaz_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *cihaz_VALUE,struct pbuf *전문,const ip4_addr_t *ünvan){(void)cihaz_VALUE;(void)전문;(void)ünvan;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer lay_INDEX,u16_t 수,pbuf_type 종류){
    (void)lay_INDEX;(void)종류;struct pbuf *verilənlər=calloc(1,sizeof(*verilənlər)+수);assert(verilənlər);verilənlər->payload=verilənlər+1;verilənlər->len=verilənlər->tot_len=수;return verilənlər;
}
u8_t pbuf_free(struct pbuf *verilənlər){free(verilənlər);return 1;}
err_t pbuf_take(struct pbuf *verilənlər,const void *원본,u16_t 수){assert(수<=verilənlər->len);memcpy(verilənlər->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *verilənlər,void *təyinat_VALUE_a0fbc067,u16_t 수,u16_t İcra_Et){assert(İcra_Et+수<=verilənlər->len);memcpy(təyinat_VALUE_a0fbc067,(char*)verilənlər->payload+İcra_Et,수);return 수;}
static err_t qəbul_et_qoşulma(struct pbuf *verilənlər,struct netif *cihaz_VALUE){(void)cihaz_VALUE;assert(verilənlər->len==60);assert(((unsigned char*)verilənlər->payload)[0]==0x42);Daxil_olan_COUNT++;pbuf_free(verilənlər);return ERR_OK;}
int main(void){
    struct netif cihaz_VALUE;memset(&cihaz_VALUE,0,sizeof(cihaz_VALUE));cihaz_VALUE.input=qəbul_et_qoşulma;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Hazırla_naqilli_Şəbəkə(&cihaz_VALUE)==ERR_OK);assert(naqilli_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&cihaz_VALUE);assert(netif_is_link_up(&cihaz_VALUE));assert(naqilli_VALUE.속도==1000);
    naqilli_VALUE.생산=naqilli_VALUE.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&cihaz_VALUE,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=naqilli_VALUE.생산;}
    assert(naqilli_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(naqilli_VALUE.göndərmək[0][0]==0x42&&naqilli_VALUE.göndərmək[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(naqilli_VALUE.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&cihaz_VALUE,전문)==ERR_MEM);pbuf_free(전문);
    memset(naqilli_VALUE.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&cihaz_VALUE);assert(Daxil_olan_COUNT==1&&naqilli_VALUE.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&cihaz_VALUE);
    assert(naqilli_VALUE.소비==0&&Daxil_olan_COUNT==1&&naqilli_VALUE.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&cihaz_VALUE);assert(!netif_is_link_up(&cihaz_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
