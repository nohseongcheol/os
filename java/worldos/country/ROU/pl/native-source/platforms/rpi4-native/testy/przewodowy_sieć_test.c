/* 가짜 MMIO/MDIO 장치로 Loop_WARTOŚĆ przepełnienie_WARTOŚĆ·długość_WARTOŚĆ·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t rejestr[0x10000/4];
#define 유선저장기(Adres) rejestr[(Adres)/4]
#define JKOROS_GENET_TEST 1
#include "../sieć_Stos/przewodowy_sieć.c"
static uintptr_t znacznik_czasu_WARTOŚĆ;
static int 물리작동=1,실물=1,przychodzące_ILE_LICZB;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned Adres=(Word_SMS>>21)&31,INDEKS=(Word_SMS>>16)&31;
        if(Adres!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEKS]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEKS];}}
    return znacznik_czasu_WARTOŚĆ++;
}
int 보드실물(void){return 실물;}
int Tablica_adres_bezwzględny(unsigned char *Adres){const unsigned char WARTOŚĆ[]={2,1,2,3,4,5};memcpy(Adres,WARTOŚĆ,6);return 1;}
void netif_set_link_up(struct netif *urządzenie_WARTOŚĆ){urządzenie_WARTOŚĆ->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *urządzenie_WARTOŚĆ){urządzenie_WARTOŚĆ->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *urządzenie_WARTOŚĆ,struct pbuf *datagram,const ip4_addr_t *Adres){(void)urządzenie_WARTOŚĆ;(void)datagram;(void)Adres;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer warstwa_INDEKS,u16_t identyfikator,pbuf_type Rodzaj_WARTOŚĆ){
    (void)warstwa_INDEKS;(void)Rodzaj_WARTOŚĆ;struct pbuf *dane=calloc(1,sizeof(*dane)+identyfikator);assert(dane);dane->payload=dane+1;dane->len=dane->tot_len=identyfikator;return dane;
}
u8_t pbuf_free(struct pbuf *dane){free(dane);return 1;}
err_t pbuf_take(struct pbuf *dane,const void *원본,u16_t identyfikator){assert(identyfikator<=dane->len);memcpy(dane->payload,원본,identyfikator);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *dane,void *cel_WARTOŚĆ,u16_t identyfikator,u16_t Uruchom_2){assert(Uruchom_2+identyfikator<=dane->len);memcpy(cel_WARTOŚĆ,(char*)dane->payload+Uruchom_2,identyfikator);return identyfikator;}
static err_t akceptować_połączenie(struct pbuf *dane,struct netif *urządzenie_WARTOŚĆ){(void)urządzenie_WARTOŚĆ;assert(dane->len==60);assert(((unsigned char*)dane->payload)[0]==0x42);przychodzące_ILE_LICZB++;pbuf_free(dane);return ERR_OK;}
int main(void){
    struct netif urządzenie_WARTOŚĆ;memset(&urządzenie_WARTOŚĆ,0,sizeof(urządzenie_WARTOŚĆ));urządzenie_WARTOŚĆ.input=akceptować_połączenie;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Przygotuj_przewodowy_sieć(&urządzenie_WARTOŚĆ)==ERR_OK);assert(przewodowy_WARTOŚĆ.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&urządzenie_WARTOŚĆ);assert(netif_is_link_up(&urządzenie_WARTOŚĆ));assert(przewodowy_WARTOŚĆ.속도==1000);
    przewodowy_WARTOŚĆ.생산=przewodowy_WARTOŚĆ.zużycie_WARTOŚĆ=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(wysłać_datagram(&urządzenie_WARTOŚĆ,datagram)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=przewodowy_WARTOŚĆ.생산;}
    assert(przewodowy_WARTOŚĆ.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(przewodowy_WARTOŚĆ.wysłać[0][0]==0x42&&przewodowy_WARTOŚĆ.wysłać[0][59]==0);pbuf_free(datagram);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(przewodowy_WARTOŚĆ.생산-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(wysłać_datagram(&urządzenie_WARTOŚĆ,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(przewodowy_WARTOŚĆ.odbierać[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&urządzenie_WARTOŚĆ);assert(przychodzące_ILE_LICZB==1&&przewodowy_WARTOŚĆ.zużycie_WARTOŚĆ==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&urządzenie_WARTOŚĆ);
    assert(przewodowy_WARTOŚĆ.zużycie_WARTOŚĆ==0&&przychodzące_ILE_LICZB==1&&przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[4]==1);
    물리값[1]=0;znacznik_czasu_WARTOŚĆ+=1000;유선망살피기(&urządzenie_WARTOŚĆ);assert(!netif_is_link_up(&urządzenie_WARTOŚĆ));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
