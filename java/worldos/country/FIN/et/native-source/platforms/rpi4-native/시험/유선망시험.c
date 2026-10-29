/* 가짜 MMIO/MDIO 장치로 Loop_VALUE ületäide_VALUE·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register_VALUE[0x10000/4];
#define 유선저장기(ADDRESS) register_VALUE[(ADDRESS)/4]
#define JKOROS_GENET_TEST 1
#include "../võrk_Virn/juhtmega_ühendatud_võrk.c"
static uintptr_t ajatempel_VALUE;
static int 물리작동=1,실물=1,Sissetulev_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned ADDRESS=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(ADDRESS!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return ajatempel_VALUE++;
}
int 보드실물(void){return 실물;}
int Tahvel_absoluutaadress(unsigned char *ADDRESS){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(ADDRESS,VALUE,6);return 1;}
void netif_set_link_up(struct netif *seade_VALUE){seade_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *seade_VALUE){seade_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *seade_VALUE,struct pbuf *datagramm,const ip4_addr_t *ADDRESS){(void)seade_VALUE;(void)datagramm;(void)ADDRESS;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer kiht_INDEX,u16_t number,pbuf_type 종류){
    (void)kiht_INDEX;(void)종류;struct pbuf *andmed=calloc(1,sizeof(*andmed)+number);assert(andmed);andmed->payload=andmed+1;andmed->len=andmed->tot_len=number;return andmed;
}
u8_t pbuf_free(struct pbuf *andmed){free(andmed);return 1;}
err_t pbuf_take(struct pbuf *andmed,const void *원본,u16_t number){assert(number<=andmed->len);memcpy(andmed->payload,원본,number);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *andmed,void *sihtkoht_VALUE,u16_t number,u16_t Käivita_2){assert(Käivita_2+number<=andmed->len);memcpy(sihtkoht_VALUE,(char*)andmed->payload+Käivita_2,number);return number;}
static err_t aktsepteerima_ühendus(struct pbuf *andmed,struct netif *seade_VALUE){(void)seade_VALUE;assert(andmed->len==60);assert(((unsigned char*)andmed->payload)[0]==0x42);Sissetulev_COUNT++;pbuf_free(andmed);return ERR_OK;}
int main(void){
    struct netif seade_VALUE;memset(&seade_VALUE,0,sizeof(seade_VALUE));seade_VALUE.input=aktsepteerima_ühendus;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Ettevalmistamine_juhtmega_ühendatud_võrk(&seade_VALUE)==ERR_OK);assert(juhtmega_ühendatud_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&seade_VALUE);assert(netif_is_link_up(&seade_VALUE));assert(juhtmega_ühendatud_VALUE.속도==1000);
    juhtmega_ühendatud_VALUE.생산=juhtmega_ühendatud_VALUE.tarbima_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagramm=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagramm->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(saatma_datagramm(&seade_VALUE,datagramm)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=juhtmega_ühendatud_VALUE.생산;}
    assert(juhtmega_ühendatud_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(juhtmega_ühendatud_VALUE.saatma[0][0]==0x42&&juhtmega_ühendatud_VALUE.saatma[0][59]==0);pbuf_free(datagramm);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(juhtmega_ühendatud_VALUE.생산-255)&65535;datagramm=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(saatma_datagramm(&seade_VALUE,datagramm)==ERR_MEM);pbuf_free(datagramm);
    memset(juhtmega_ühendatud_VALUE.saama[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&seade_VALUE);assert(Sissetulev_COUNT==1&&juhtmega_ühendatud_VALUE.tarbima_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&seade_VALUE);
    assert(juhtmega_ühendatud_VALUE.tarbima_VALUE==0&&Sissetulev_COUNT==1&&juhtmega_ühendatud_VALUE.집계[4]==1);
    물리값[1]=0;ajatempel_VALUE+=1000;유선망살피기(&seade_VALUE);assert(!netif_is_link_up(&seade_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
