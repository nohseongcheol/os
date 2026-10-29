/* 가짜 MMIO/MDIO 장치로 Loop_ЗНАЧЕН переполнение_ЗНАЧЕН·длина_ЗНАЧЕН·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t регистр[0x10000/4];
#define 유선저장기(АДРЕС) регистр[(АДРЕС)/4]
#define JKOROS_GENET_TEST 1
#include "../сеть_стек/проводной_сеть.c"
static uintptr_t метка_времени_ЗНАЧЕН;
static int 물리작동=1,실물=1,Входящий_СЧЁТ;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned АДРЕС=(Word_SMS>>21)&31,ИНДЕКС=(Word_SMS>>16)&31;
        if(АДРЕС!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[ИНДЕКС]=Word_SMS&65535;유선저장기(0xe14)=물리값[ИНДЕКС];}}
    return метка_времени_ЗНАЧЕН++;
}
int 보드실물(void){return 실물;}
int Доска_абсолютный_адрес(unsigned char *АДРЕС){const unsigned char ЗНАЧЕН[]={2,1,2,3,4,5};memcpy(АДРЕС,ЗНАЧЕН,6);return 1;}
void netif_set_link_up(struct netif *устройство_ЗНАЧЕН){устройство_ЗНАЧЕН->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *устройство_ЗНАЧЕН){устройство_ЗНАЧЕН->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *устройство_ЗНАЧЕН,struct pbuf *датаграмма,const ip4_addr_t *АДРЕС){(void)устройство_ЗНАЧЕН;(void)датаграмма;(void)АДРЕС;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer слой_ИНДЕКС,u16_t 수,pbuf_type Вид_ЗНАЧЕН){
    (void)слой_ИНДЕКС;(void)Вид_ЗНАЧЕН;struct pbuf *данные=calloc(1,sizeof(*данные)+수);assert(данные);данные->payload=данные+1;данные->len=данные->tot_len=수;return данные;
}
u8_t pbuf_free(struct pbuf *данные){free(данные);return 1;}
err_t pbuf_take(struct pbuf *данные,const void *원본,u16_t 수){assert(수<=данные->len);memcpy(данные->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *данные,void *цель_ЗНАЧЕН,u16_t 수,u16_t запустить){assert(запустить+수<=данные->len);memcpy(цель_ЗНАЧЕН,(char*)данные->payload+запустить,수);return 수;}
static err_t принять_контакт(struct pbuf *данные,struct netif *устройство_ЗНАЧЕН){(void)устройство_ЗНАЧЕН;assert(данные->len==60);assert(((unsigned char*)данные->payload)[0]==0x42);Входящий_СЧЁТ++;pbuf_free(данные);return ERR_OK;}
int main(void){
    struct netif устройство_ЗНАЧЕН;memset(&устройство_ЗНАЧЕН,0,sizeof(устройство_ЗНАЧЕН));устройство_ЗНАЧЕН.input=принять_контакт;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Подготовить_проводной_сеть(&устройство_ЗНАЧЕН)==ERR_OK);assert(проводной_ЗНАЧЕН.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&устройство_ЗНАЧЕН);assert(netif_is_link_up(&устройство_ЗНАЧЕН));assert(проводной_ЗНАЧЕН.속도==1000);
    проводной_ЗНАЧЕН.생산=проводной_ЗНАЧЕН.потребление_ЗНАЧЕН=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *датаграмма=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(датаграмма->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(написать_датаграмма(&устройство_ЗНАЧЕН,датаграмма)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=проводной_ЗНАЧЕН.생산;}
    assert(проводной_ЗНАЧЕН.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(проводной_ЗНАЧЕН.написать[0][0]==0x42&&проводной_ЗНАЧЕН.написать[0][59]==0);pbuf_free(датаграмма);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(проводной_ЗНАЧЕН.생산-255)&65535;датаграмма=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(написать_датаграмма(&устройство_ЗНАЧЕН,датаграмма)==ERR_MEM);pbuf_free(датаграмма);
    memset(проводной_ЗНАЧЕН.получить[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&устройство_ЗНАЧЕН);assert(Входящий_СЧЁТ==1&&проводной_ЗНАЧЕН.потребление_ЗНАЧЕН==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&устройство_ЗНАЧЕН);
    assert(проводной_ЗНАЧЕН.потребление_ЗНАЧЕН==0&&Входящий_СЧЁТ==1&&проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[4]==1);
    물리값[1]=0;метка_времени_ЗНАЧЕН+=1000;유선망살피기(&устройство_ЗНАЧЕН);assert(!netif_is_link_up(&устройство_ЗНАЧЕН));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
