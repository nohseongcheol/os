/* 가짜 MMIO/MDIO 장치로 цикъл_стойност Препълване_стойност·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t регистър_стойност[0x10000/4];
#define 유선저장기(адрес) регистър_стойност[(адрес)/4]
#define JKOROS_GENET_TEST 1
#include "../мрежа_стек/кабелен_мрежа.c"
static uintptr_t времево_клеймо_стойност;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Игри_с_думи_Текст=유선저장기(0xe14);
    if(물리작동&&(Игри_с_думи_Текст&(1u<<29))){unsigned адрес=(Игри_с_думи_Текст>>21)&31,индекс=(Игри_с_думи_Текст>>16)&31;
        if(адрес!=1)유선저장기(0xe14)=1<<28;
        else{if(((Игри_с_думи_Текст>>26)&3)==1)물리값[индекс]=Игри_с_думи_Текст&65535;유선저장기(0xe14)=물리값[индекс];}}
    return времево_клеймо_стойност++;
}
int 보드실물(void){return 실물;}
int Табло_реален_адрес(unsigned char *адрес){const unsigned char стойност[]={2,1,2,3,4,5};memcpy(адрес,стойност,6);return 1;}
void netif_set_link_up(struct netif *устройство_стойност){устройство_стойност->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *устройство_стойност){устройство_стойност->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *устройство_стойност,struct pbuf *дейтаграма,const ip4_addr_t *адрес){(void)устройство_стойност;(void)дейтаграма;(void)адрес;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer слой_индекс,u16_t 수,pbuf_type 종류){
    (void)слой_индекс;(void)종류;struct pbuf *данни=calloc(1,sizeof(*данни)+수);assert(данни);данни->payload=данни+1;данни->len=данни->tot_len=수;return данни;
}
u8_t pbuf_free(struct pbuf *данни){free(данни);return 1;}
err_t pbuf_take(struct pbuf *данни,const void *원본,u16_t 수){assert(수<=данни->len);memcpy(данни->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *данни,void *местоназначение_стойност,u16_t 수,u16_t Стартиране){assert(Стартиране+수<=данни->len);memcpy(местоназначение_стойност,(char*)данни->payload+Стартиране,수);return 수;}
static err_t приемам_връзка(struct pbuf *данни,struct netif *устройство_стойност){(void)устройство_стойност;assert(данни->len==60);assert(((unsigned char*)данни->payload)[0]==0x42);들어온수++;pbuf_free(данни);return ERR_OK;}
int main(void){
    struct netif устройство_стойност;memset(&устройство_стойност,0,sizeof(устройство_стойност));устройство_стойност.input=приемам_връзка;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Подготвяне_кабелен_мрежа(&устройство_стойност)==ERR_OK);assert(кабелен_стойност.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&устройство_стойност);assert(netif_is_link_up(&устройство_стойност));assert(кабелен_стойност.속도==1000);
    кабелен_стойност.생산=кабелен_стойност.използвам_стойност_84aa75c8=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *дейтаграма=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(дейтаграма->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(изпращам_дейтаграма(&устройство_стойност,дейтаграма)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=кабелен_стойност.생산;}
    assert(кабелен_стойност.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(кабелен_стойност.изпращам[0][0]==0x42&&кабелен_стойност.изпращам[0][59]==0);pbuf_free(дейтаграма);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(кабелен_стойност.생산-255)&65535;дейтаграма=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(изпращам_дейтаграма(&устройство_стойност,дейтаграма)==ERR_MEM);pbuf_free(дейтаграма);
    memset(кабелен_стойност.получавам[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&устройство_стойност);assert(들어온수==1&&кабелен_стойност.използвам_стойност_84aa75c8==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&устройство_стойност);
    assert(кабелен_стойност.използвам_стойност_84aa75c8==0&&들어온수==1&&кабелен_стойност.집계[4]==1);
    물리값[1]=0;времево_клеймо_стойност+=1000;유선망살피기(&устройство_стойност);assert(!netif_is_link_up(&устройство_стойност));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
