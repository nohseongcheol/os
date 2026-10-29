/* 가짜 MMIO/MDIO 장치로 цикл_маани ашыра_толтуруу_маани·узундук_маани·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(дарек) 저장기[(дарек)/4]
#define JKOROS_GENET_TEST 1
#include "../Желе_стек/зымдуу_Желе.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Сөз_СМС=유선저장기(0xe14);
    if(물리작동&&(Сөз_СМС&(1u<<29))){unsigned дарек=(Сөз_СМС>>21)&31,индекс=(Сөз_СМС>>16)&31;
        if(дарек!=1)유선저장기(0xe14)=1<<28;
        else{if(((Сөз_СМС>>26)&3)==1)물리값[индекс]=Сөз_СМС&65535;유선저장기(0xe14)=물리값[индекс];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *дарек){const unsigned char маани[]={2,1,2,3,4,5};memcpy(дарек,маани,6);return 1;}
void netif_set_link_up(struct netif *түзмөк_маани){түзмөк_маани->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *түзмөк_маани){түзмөк_маани->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *түзмөк_маани,struct pbuf *전문,const ip4_addr_t *дарек){(void)түзмөк_маани;(void)전문;(void)дарек;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer катмар_индекс,u16_t 수,pbuf_type 종류){
    (void)катмар_индекс;(void)종류;struct pbuf *берилмелер=calloc(1,sizeof(*берилмелер)+수);assert(берилмелер);берилмелер->payload=берилмелер+1;берилмелер->len=берилмелер->tot_len=수;return берилмелер;
}
u8_t pbuf_free(struct pbuf *берилмелер){free(берилмелер);return 1;}
err_t pbuf_take(struct pbuf *берилмелер,const void *원본,u16_t 수){assert(수<=берилмелер->len);memcpy(берилмелер->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *берилмелер,void *көздөө_жайы_маани,u16_t 수,u16_t Жүргүзүү){assert(Жүргүзүү+수<=берилмелер->len);memcpy(көздөө_жайы_маани,(char*)берилмелер->payload+Жүргүзүү,수);return 수;}
static err_t кабыл_алуу_туташуу(struct pbuf *берилмелер,struct netif *түзмөк_маани){(void)түзмөк_маани;assert(берилмелер->len==60);assert(((unsigned char*)берилмелер->payload)[0]==0x42);들어온수++;pbuf_free(берилмелер);return ERR_OK;}
int main(void){
    struct netif түзмөк_маани;memset(&түзмөк_маани,0,sizeof(түзмөк_маани));түзмөк_маани.input=кабыл_алуу_туташуу;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Даярдоо_зымдуу_Желе(&түзмөк_маани)==ERR_OK);assert(зымдуу_маани.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&түзмөк_маани);assert(netif_is_link_up(&түзмөк_маани));assert(зымдуу_маани.속도==1000);
    зымдуу_маани.생산=зымдуу_маани.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&түзмөк_маани,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=зымдуу_маани.생산;}
    assert(зымдуу_маани.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(зымдуу_маани.жөнөтүү[0][0]==0x42&&зымдуу_маани.жөнөтүү[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(зымдуу_маани.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&түзмөк_маани,전문)==ERR_MEM);pbuf_free(전문);
    memset(зымдуу_маани.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&түзмөк_маани);assert(들어온수==1&&зымдуу_маани.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&түзмөк_маани);
    assert(зымдуу_маани.소비==0&&들어온수==1&&зымдуу_маани.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&түзмөк_маани);assert(!netif_is_link_up(&түзмөк_маани));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
