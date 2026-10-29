/* 가짜 MMIO/MDIO 장치로 Loop_ÉRTÉK túlfolyás_ÉRTÉK·hossz_ÉRTÉK·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t jegyzék_ÉRTÉK[0x10000/4];
#define 유선저장기(CÍM) jegyzék_ÉRTÉK[(CÍM)/4]
#define JKOROS_GENET_TEST 1
#include "../hálózat_Sor/vezetékes_hálózat.c"
static uintptr_t timestamp_ÉRTÉK;
static int 물리작동=1,실물=1,Bejövő_DARAB;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t szó_SMS=유선저장기(0xe14);
    if(물리작동&&(szó_SMS&(1u<<29))){unsigned CÍM=(szó_SMS>>21)&31,INDEX=(szó_SMS>>16)&31;
        if(CÍM!=1)유선저장기(0xe14)=1<<28;
        else{if(((szó_SMS>>26)&3)==1)물리값[INDEX]=szó_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return timestamp_ÉRTÉK++;
}
int 보드실물(void){return 실물;}
int fal_valódi_cím(unsigned char *CÍM){const unsigned char ÉRTÉK[]={2,1,2,3,4,5};memcpy(CÍM,ÉRTÉK,6);return 1;}
void netif_set_link_up(struct netif *mobil_ÉRTÉK){mobil_ÉRTÉK->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *mobil_ÉRTÉK){mobil_ÉRTÉK->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *mobil_ÉRTÉK,struct pbuf *datagram,const ip4_addr_t *CÍM){(void)mobil_ÉRTÉK;(void)datagram;(void)CÍM;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer réteg_INDEX,u16_t szám,pbuf_type Altípus_ÉRTÉK){
    (void)réteg_INDEX;(void)Altípus_ÉRTÉK;struct pbuf *adat=calloc(1,sizeof(*adat)+szám);assert(adat);adat->payload=adat+1;adat->len=adat->tot_len=szám;return adat;
}
u8_t pbuf_free(struct pbuf *adat){free(adat);return 1;}
err_t pbuf_take(struct pbuf *adat,const void *원본,u16_t szám){assert(szám<=adat->len);memcpy(adat->payload,원본,szám);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *adat,void *cél_ÉRTÉK,u16_t szám,u16_t Futtatás){assert(Futtatás+szám<=adat->len);memcpy(cél_ÉRTÉK,(char*)adat->payload+Futtatás,szám);return szám;}
static err_t elfogad_ismerős(struct pbuf *adat,struct netif *mobil_ÉRTÉK){(void)mobil_ÉRTÉK;assert(adat->len==60);assert(((unsigned char*)adat->payload)[0]==0x42);Bejövő_DARAB++;pbuf_free(adat);return ERR_OK;}
int main(void){
    struct netif mobil_ÉRTÉK;memset(&mobil_ÉRTÉK,0,sizeof(mobil_ÉRTÉK));mobil_ÉRTÉK.input=elfogad_ismerős;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Előkészítés_vezetékes_hálózat(&mobil_ÉRTÉK)==ERR_OK);assert(vezetékes_ÉRTÉK.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&mobil_ÉRTÉK);assert(netif_is_link_up(&mobil_ÉRTÉK));assert(vezetékes_ÉRTÉK.속도==1000);
    vezetékes_ÉRTÉK.생산=vezetékes_ÉRTÉK.felhasznál_ÉRTÉK=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(küld_datagram(&mobil_ÉRTÉK,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=vezetékes_ÉRTÉK.생산;}
    assert(vezetékes_ÉRTÉK.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(vezetékes_ÉRTÉK.küld[0][0]==0x42&&vezetékes_ÉRTÉK.küld[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(vezetékes_ÉRTÉK.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(küld_datagram(&mobil_ÉRTÉK,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(vezetékes_ÉRTÉK.fogad[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&mobil_ÉRTÉK);assert(Bejövő_DARAB==1&&vezetékes_ÉRTÉK.felhasznál_ÉRTÉK==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&mobil_ÉRTÉK);
    assert(vezetékes_ÉRTÉK.felhasznál_ÉRTÉK==0&&Bejövő_DARAB==1&&vezetékes_ÉRTÉK.statisztika_ÉRTÉK[4]==1);
    물리값[1]=0;timestamp_ÉRTÉK+=1000;유선망살피기(&mobil_ÉRTÉK);assert(!netif_is_link_up(&mobil_ÉRTÉK));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
