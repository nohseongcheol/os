/* 가짜 MMIO/MDIO 장치로 lupu_Boleng penologo_Boleng·boleele_Boleng·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t kwadisa_Boleng[0x10000/4];
#define 유선저장기(aterese) kwadisa_Boleng[(aterese)/4]
#define JKOROS_GENET_TEST 1
#include "../Neteweke_kokoanyodinepe/golagantsweng_ka_megala_Neteweke.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Lefoko_SMS=유선저장기(0xe14);
    if(물리작동&&(Lefoko_SMS&(1u<<29))){unsigned aterese=(Lefoko_SMS>>21)&31,tshupane=(Lefoko_SMS>>16)&31;
        if(aterese!=1)유선저장기(0xe14)=1<<28;
        else{if(((Lefoko_SMS>>26)&3)==1)물리값[tshupane]=Lefoko_SMS&65535;유선저장기(0xe14)=물리값[tshupane];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *aterese){const unsigned char Boleng[]={2,1,2,3,4,5};memcpy(aterese,Boleng,6);return 1;}
void netif_set_link_up(struct netif *mobaele_Boleng){mobaele_Boleng->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *mobaele_Boleng){mobaele_Boleng->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *mobaele_Boleng,struct pbuf *전문,const ip4_addr_t *aterese){(void)mobaele_Boleng;(void)전문;(void)aterese;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer boalo_tshupane,u16_t 수,pbuf_type 종류){
    (void)boalo_tshupane;(void)종류;struct pbuf *tshedimosetso=calloc(1,sizeof(*tshedimosetso)+수);assert(tshedimosetso);tshedimosetso->payload=tshedimosetso+1;tshedimosetso->len=tshedimosetso->tot_len=수;return tshedimosetso;
}
u8_t pbuf_free(struct pbuf *tshedimosetso){free(tshedimosetso);return 1;}
err_t pbuf_take(struct pbuf *tshedimosetso,const void *원본,u16_t 수){assert(수<=tshedimosetso->len);memcpy(tshedimosetso->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *tshedimosetso,void *bogorogelo_Boleng,u16_t 수,u16_t dirisa){assert(dirisa+수<=tshedimosetso->len);memcpy(bogorogelo_Boleng,(char*)tshedimosetso->payload+dirisa,수);return 수;}
static err_t amogela_Kgolagano(struct pbuf *tshedimosetso,struct netif *mobaele_Boleng){(void)mobaele_Boleng;assert(tshedimosetso->len==60);assert(((unsigned char*)tshedimosetso->payload)[0]==0x42);들어온수++;pbuf_free(tshedimosetso);return ERR_OK;}
int main(void){
    struct netif mobaele_Boleng;memset(&mobaele_Boleng,0,sizeof(mobaele_Boleng));mobaele_Boleng.input=amogela_Kgolagano;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Baakanya_golagantsweng_ka_megala_Neteweke(&mobaele_Boleng)==ERR_OK);assert(golagantsweng_ka_megala_Boleng.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&mobaele_Boleng);assert(netif_is_link_up(&mobaele_Boleng));assert(golagantsweng_ka_megala_Boleng.속도==1000);
    golagantsweng_ka_megala_Boleng.생산=golagantsweng_ka_megala_Boleng.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&mobaele_Boleng,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=golagantsweng_ka_megala_Boleng.생산;}
    assert(golagantsweng_ka_megala_Boleng.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(golagantsweng_ka_megala_Boleng.romela[0][0]==0x42&&golagantsweng_ka_megala_Boleng.romela[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(golagantsweng_ka_megala_Boleng.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&mobaele_Boleng,전문)==ERR_MEM);pbuf_free(전문);
    memset(golagantsweng_ka_megala_Boleng.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&mobaele_Boleng);assert(들어온수==1&&golagantsweng_ka_megala_Boleng.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&mobaele_Boleng);
    assert(golagantsweng_ka_megala_Boleng.소비==0&&들어온수==1&&golagantsweng_ka_megala_Boleng.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&mobaele_Boleng);assert(!netif_is_link_up(&mobaele_Boleng));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
