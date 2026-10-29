/* 가짜 MMIO/MDIO 장치로 Loop_HODNOTA přetečení_HODNOTA·délka_HODNOTA·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registr[0x10000/4];
#define 유선저장기(Adresa) registr[(Adresa)/4]
#define JKOROS_GENET_TEST 1
#include "../síť_Štos/drátový_síť.c"
static uintptr_t timestamp_HODNOTA;
static int 물리작동=1,실물=1,Příchozí_POČET;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned Adresa=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(Adresa!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return timestamp_HODNOTA++;
}
int 보드실물(void){return 실물;}
int Panel_absolutní_adresa(unsigned char *Adresa){const unsigned char HODNOTA[]={2,1,2,3,4,5};memcpy(Adresa,HODNOTA,6);return 1;}
void netif_set_link_up(struct netif *mobilní_HODNOTA){mobilní_HODNOTA->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *mobilní_HODNOTA){mobilní_HODNOTA->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *mobilní_HODNOTA,struct pbuf *datagram,const ip4_addr_t *Adresa){(void)mobilní_HODNOTA;(void)datagram;(void)Adresa;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer vrstva_INDEX,u16_t číslo,pbuf_type Druh_HODNOTA){
    (void)vrstva_INDEX;(void)Druh_HODNOTA;struct pbuf *data=calloc(1,sizeof(*data)+číslo);assert(data);data->payload=data+1;data->len=data->tot_len=číslo;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *원본,u16_t číslo){assert(číslo<=data->len);memcpy(data->payload,원본,číslo);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *cíl_HODNOTA,u16_t číslo,u16_t Spustit_2){assert(Spustit_2+číslo<=data->len);memcpy(cíl_HODNOTA,(char*)data->payload+Spustit_2,číslo);return číslo;}
static err_t přijmout_kontakt(struct pbuf *data,struct netif *mobilní_HODNOTA){(void)mobilní_HODNOTA;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);Příchozí_POČET++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif mobilní_HODNOTA;memset(&mobilní_HODNOTA,0,sizeof(mobilní_HODNOTA));mobilní_HODNOTA.input=přijmout_kontakt;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Připravit_drátový_síť(&mobilní_HODNOTA)==ERR_OK);assert(drátový_HODNOTA.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&mobilní_HODNOTA);assert(netif_is_link_up(&mobilní_HODNOTA));assert(drátový_HODNOTA.속도==1000);
    drátový_HODNOTA.생산=drátový_HODNOTA.využívat_HODNOTA=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(poslat_datagram(&mobilní_HODNOTA,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=drátový_HODNOTA.생산;}
    assert(drátový_HODNOTA.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(drátový_HODNOTA.poslat[0][0]==0x42&&drátový_HODNOTA.poslat[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(drátový_HODNOTA.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(poslat_datagram(&mobilní_HODNOTA,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(drátový_HODNOTA.dostat[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&mobilní_HODNOTA);assert(Příchozí_POČET==1&&drátový_HODNOTA.využívat_HODNOTA==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&mobilní_HODNOTA);
    assert(drátový_HODNOTA.využívat_HODNOTA==0&&Příchozí_POČET==1&&drátový_HODNOTA.Statistika_HODNOTA[4]==1);
    물리값[1]=0;timestamp_HODNOTA+=1000;유선망살피기(&mobilní_HODNOTA);assert(!netif_is_link_up(&mobilní_HODNOTA));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
