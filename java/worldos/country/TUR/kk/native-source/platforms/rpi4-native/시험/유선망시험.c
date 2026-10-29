/* 가짜 MMIO/MDIO 장치로 тұйық_мән толып_кету_мән·ұзындық_мән·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t тіркеу_мән[0x10000/4];
#define 유선저장기(мекенжай) тіркеу_мән[(мекенжай)/4]
#define JKOROS_GENET_TEST 1
#include "../желі_Бума/сымды_желі.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Сөз_Мәтін=유선저장기(0xe14);
    if(물리작동&&(Сөз_Мәтін&(1u<<29))){unsigned мекенжай=(Сөз_Мәтін>>21)&31,индекс=(Сөз_Мәтін>>16)&31;
        if(мекенжай!=1)유선저장기(0xe14)=1<<28;
        else{if(((Сөз_Мәтін>>26)&3)==1)물리값[индекс]=Сөз_Мәтін&65535;유선저장기(0xe14)=물리값[индекс];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int Тақта_нақпа_нақ_мекенжай(unsigned char *мекенжай){const unsigned char мән[]={2,1,2,3,4,5};memcpy(мекенжай,мән,6);return 1;}
void netif_set_link_up(struct netif *құрылғы_мән){құрылғы_мән->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *құрылғы_мән){құрылғы_мән->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *құрылғы_мән,struct pbuf *전문,const ip4_addr_t *мекенжай){(void)құрылғы_мән;(void)전문;(void)мекенжай;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer қабат_индекс,u16_t 수,pbuf_type 종류){
    (void)қабат_индекс;(void)종류;struct pbuf *деректер=calloc(1,sizeof(*деректер)+수);assert(деректер);деректер->payload=деректер+1;деректер->len=деректер->tot_len=수;return деректер;
}
u8_t pbuf_free(struct pbuf *деректер){free(деректер);return 1;}
err_t pbuf_take(struct pbuf *деректер,const void *원본,u16_t 수){assert(수<=деректер->len);memcpy(деректер->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *деректер,void *тағайындау_мән,u16_t 수,u16_t Орындау_2){assert(Орындау_2+수<=деректер->len);memcpy(тағайындау_мән,(char*)деректер->payload+Орындау_2,수);return 수;}
static err_t қабылдау_қосылым(struct pbuf *деректер,struct netif *құрылғы_мән){(void)құрылғы_мән;assert(деректер->len==60);assert(((unsigned char*)деректер->payload)[0]==0x42);들어온수++;pbuf_free(деректер);return ERR_OK;}
int main(void){
    struct netif құрылғы_мән;memset(&құрылғы_мән,0,sizeof(құрылғы_мән));құрылғы_мән.input=қабылдау_қосылым;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Дайындау_сымды_желі(&құрылғы_мән)==ERR_OK);assert(сымды_мән.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&құрылғы_мән);assert(netif_is_link_up(&құрылғы_мән));assert(сымды_мән.속도==1000);
    сымды_мән.생산=сымды_мән.пайдалану_мән=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&құрылғы_мән,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=сымды_мән.생산;}
    assert(сымды_мән.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(сымды_мән.жіберу[0][0]==0x42&&сымды_мән.жіберу[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(сымды_мән.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&құрылғы_мән,전문)==ERR_MEM);pbuf_free(전문);
    memset(сымды_мән.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&құрылғы_мән);assert(들어온수==1&&сымды_мән.пайдалану_мән==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&құрылғы_мән);
    assert(сымды_мән.пайдалану_мән==0&&들어온수==1&&сымды_мән.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&құрылғы_мән);assert(!netif_is_link_up(&құрылғы_мән));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
