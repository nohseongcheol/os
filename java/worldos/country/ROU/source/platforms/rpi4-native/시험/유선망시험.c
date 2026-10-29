/* 가짜 MMIO/MDIO 장치로 Loop_VALUE depășire_VALUE·lungime_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registru_VALUE[0x10000/4];
#define 유선저장기(adresa) registru_VALUE[(adresa)/4]
#define JKOROS_GENET_TEST 1
#include "../rețea_Teanc/cu_fir_rețea.c"
static uintptr_t marcă_de_timp_VALUE;
static int 물리작동=1,실물=1,Primit_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned adresa=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(adresa!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return marcă_de_timp_VALUE++;
}
int 보드실물(void){return 실물;}
int Avizier_adresă_reală(unsigned char *adresa){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(adresa,VALUE,6);return 1;}
void netif_set_link_up(struct netif *mobil_VALUE){mobil_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *mobil_VALUE){mobil_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *mobil_VALUE,struct pbuf *diagramă_informații,const ip4_addr_t *adresa){(void)mobil_VALUE;(void)diagramă_informații;(void)adresa;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer strat_INDEX,u16_t 수,pbuf_type 종류){
    (void)strat_INDEX;(void)종류;struct pbuf *date=calloc(1,sizeof(*date)+수);assert(date);date->payload=date+1;date->len=date->tot_len=수;return date;
}
u8_t pbuf_free(struct pbuf *date){free(date);return 1;}
err_t pbuf_take(struct pbuf *date,const void *원본,u16_t 수){assert(수<=date->len);memcpy(date->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *date,void *destinație_VALUE,u16_t 수,u16_t Pornește){assert(Pornește+수<=date->len);memcpy(destinație_VALUE,(char*)date->payload+Pornește,수);return 수;}
static err_t accepta_conexiune(struct pbuf *date,struct netif *mobil_VALUE){(void)mobil_VALUE;assert(date->len==60);assert(((unsigned char*)date->payload)[0]==0x42);Primit_COUNT++;pbuf_free(date);return ERR_OK;}
int main(void){
    struct netif mobil_VALUE;memset(&mobil_VALUE,0,sizeof(mobil_VALUE));mobil_VALUE.input=accepta_conexiune;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Pregătiți_cu_fir_rețea(&mobil_VALUE)==ERR_OK);assert(cu_fir_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&mobil_VALUE);assert(netif_is_link_up(&mobil_VALUE));assert(cu_fir_VALUE.속도==1000);
    cu_fir_VALUE.생산=cu_fir_VALUE.consum_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *diagramă_informații=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(diagramă_informații->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(trimite_diagramă_informații(&mobil_VALUE,diagramă_informații)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=cu_fir_VALUE.생산;}
    assert(cu_fir_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(cu_fir_VALUE.trimite[0][0]==0x42&&cu_fir_VALUE.trimite[0][59]==0);pbuf_free(diagramă_informații);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(cu_fir_VALUE.생산-255)&65535;diagramă_informații=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(trimite_diagramă_informații(&mobil_VALUE,diagramă_informații)==ERR_MEM);pbuf_free(diagramă_informații);
    memset(cu_fir_VALUE.primi[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&mobil_VALUE);assert(Primit_COUNT==1&&cu_fir_VALUE.consum_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&mobil_VALUE);
    assert(cu_fir_VALUE.consum_VALUE==0&&Primit_COUNT==1&&cu_fir_VALUE.Statistică_VALUE[4]==1);
    물리값[1]=0;marcă_de_timp_VALUE+=1000;유선망살피기(&mobil_VALUE);assert(!netif_is_link_up(&mobil_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
