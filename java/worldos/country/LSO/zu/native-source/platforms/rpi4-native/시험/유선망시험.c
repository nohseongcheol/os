/* 가짜 MMIO/MDIO 장치로 iluphu_inani ukukapaka_inani·ubude_inani·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t bhalisa_inani[0x10000/4];
#define 유선저장기(ikheli) bhalisa_inani[(ikheli)/4]
#define JKOROS_GENET_TEST 1
#include "../iNethiwekhi_Isitaki/kunezintambo_iNethiwekhi.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Amagama_I_SMS=유선저장기(0xe14);
    if(물리작동&&(Amagama_I_SMS&(1u<<29))){unsigned ikheli=(Amagama_I_SMS>>21)&31,thola_inkomba=(Amagama_I_SMS>>16)&31;
        if(ikheli!=1)유선저장기(0xe14)=1<<28;
        else{if(((Amagama_I_SMS>>26)&3)==1)물리값[thola_inkomba]=Amagama_I_SMS&65535;유선저장기(0xe14)=물리값[thola_inkomba];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *ikheli){const unsigned char inani[]={2,1,2,3,4,5};memcpy(ikheli,inani,6);return 1;}
void netif_set_link_up(struct netif *idivayisi_inani){idivayisi_inani->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *idivayisi_inani){idivayisi_inani->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *idivayisi_inani,struct pbuf *전문,const ip4_addr_t *ikheli){(void)idivayisi_inani;(void)전문;(void)ikheli;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ugqinsi_thola_inkomba,u16_t 수,pbuf_type 종류){
    (void)ugqinsi_thola_inkomba;(void)종류;struct pbuf *imininingwane=calloc(1,sizeof(*imininingwane)+수);assert(imininingwane);imininingwane->payload=imininingwane+1;imininingwane->len=imininingwane->tot_len=수;return imininingwane;
}
u8_t pbuf_free(struct pbuf *imininingwane){free(imininingwane);return 1;}
err_t pbuf_take(struct pbuf *imininingwane,const void *원본,u16_t 수){assert(수<=imininingwane->len);memcpy(imininingwane->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *imininingwane,void *isikhumulo_inani,u16_t 수,u16_t Sebenzisa){assert(Sebenzisa+수<=imininingwane->len);memcpy(isikhumulo_inani,(char*)imininingwane->payload+Sebenzisa,수);return 수;}
static err_t yamukela_uxhumano(struct pbuf *imininingwane,struct netif *idivayisi_inani){(void)idivayisi_inani;assert(imininingwane->len==60);assert(((unsigned char*)imininingwane->payload)[0]==0x42);들어온수++;pbuf_free(imininingwane);return ERR_OK;}
int main(void){
    struct netif idivayisi_inani;memset(&idivayisi_inani,0,sizeof(idivayisi_inani));idivayisi_inani.input=yamukela_uxhumano;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Hlela_kunezintambo_iNethiwekhi(&idivayisi_inani)==ERR_OK);assert(kunezintambo_inani.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&idivayisi_inani);assert(netif_is_link_up(&idivayisi_inani));assert(kunezintambo_inani.속도==1000);
    kunezintambo_inani.생산=kunezintambo_inani.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&idivayisi_inani,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=kunezintambo_inani.생산;}
    assert(kunezintambo_inani.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(kunezintambo_inani.Thumela[0][0]==0x42&&kunezintambo_inani.Thumela[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(kunezintambo_inani.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&idivayisi_inani,전문)==ERR_MEM);pbuf_free(전문);
    memset(kunezintambo_inani.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&idivayisi_inani);assert(들어온수==1&&kunezintambo_inani.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&idivayisi_inani);
    assert(kunezintambo_inani.소비==0&&들어온수==1&&kunezintambo_inani.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&idivayisi_inani);assert(!netif_is_link_up(&idivayisi_inani));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
