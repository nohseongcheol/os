/* 가짜 MMIO/MDIO 장치로 цикл_значення_201e2521 надлишок_значення·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t регістр[0x10000/4];
#define 유선저장기(Адреса) регістр[(Адреса)/4]
#define JKOROS_GENET_TEST 1
#include "../мережа_Стіс/проводовий_мережа.c"
static uintptr_t позначка_часу_значення;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Ігри_в_слова_Текст=유선저장기(0xe14);
    if(물리작동&&(Ігри_в_слова_Текст&(1u<<29))){unsigned Адреса=(Ігри_в_слова_Текст>>21)&31,індекс=(Ігри_в_слова_Текст>>16)&31;
        if(Адреса!=1)유선저장기(0xe14)=1<<28;
        else{if(((Ігри_в_слова_Текст>>26)&3)==1)물리값[індекс]=Ігри_в_слова_Текст&65535;유선저장기(0xe14)=물리값[індекс];}}
    return позначка_часу_значення++;
}
int 보드실물(void){return 실물;}
int Дошка_дійсна_адреса(unsigned char *Адреса){const unsigned char значення[]={2,1,2,3,4,5};memcpy(Адреса,значення,6);return 1;}
void netif_set_link_up(struct netif *пристрій_значення){пристрій_значення->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *пристрій_значення){пристрій_значення->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *пристрій_значення,struct pbuf *дейтаграма,const ip4_addr_t *Адреса){(void)пристрій_значення;(void)дейтаграма;(void)Адреса;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer шар_індекс,u16_t 수,pbuf_type 종류){
    (void)шар_індекс;(void)종류;struct pbuf *дані=calloc(1,sizeof(*дані)+수);assert(дані);дані->payload=дані+1;дані->len=дані->tot_len=수;return дані;
}
u8_t pbuf_free(struct pbuf *дані){free(дані);return 1;}
err_t pbuf_take(struct pbuf *дані,const void *원본,u16_t 수){assert(수<=дані->len);memcpy(дані->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *дані,void *місце_значення,u16_t 수,u16_t запустити){assert(запустити+수<=дані->len);memcpy(місце_значення,(char*)дані->payload+запустити,수);return 수;}
static err_t приймати_зв_язок(struct pbuf *дані,struct netif *пристрій_значення){(void)пристрій_значення;assert(дані->len==60);assert(((unsigned char*)дані->payload)[0]==0x42);들어온수++;pbuf_free(дані);return ERR_OK;}
int main(void){
    struct netif пристрій_значення;memset(&пристрій_значення,0,sizeof(пристрій_значення));пристрій_значення.input=приймати_зв_язок;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Готувати_проводовий_мережа(&пристрій_значення)==ERR_OK);assert(проводовий_значення.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&пристрій_значення);assert(netif_is_link_up(&пристрій_значення));assert(проводовий_значення.속도==1000);
    проводовий_значення.생산=проводовий_значення.використовувати_значення=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *дейтаграма=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(дейтаграма->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(надсилати_дейтаграма(&пристрій_значення,дейтаграма)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=проводовий_значення.생산;}
    assert(проводовий_значення.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(проводовий_значення.надсилати[0][0]==0x42&&проводовий_значення.надсилати[0][59]==0);pbuf_free(дейтаграма);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(проводовий_значення.생산-255)&65535;дейтаграма=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(надсилати_дейтаграма(&пристрій_значення,дейтаграма)==ERR_MEM);pbuf_free(дейтаграма);
    memset(проводовий_значення.отримувати[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&пристрій_значення);assert(들어온수==1&&проводовий_значення.використовувати_значення==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&пристрій_значення);
    assert(проводовий_значення.використовувати_значення==0&&들어온수==1&&проводовий_значення.집계[4]==1);
    물리값[1]=0;позначка_часу_значення+=1000;유선망살피기(&пристрій_значення);assert(!netif_is_link_up(&пристрій_значення));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
