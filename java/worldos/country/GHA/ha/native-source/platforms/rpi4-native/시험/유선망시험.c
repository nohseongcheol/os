/* 가짜 MMIO/MDIO 장치로 Warware_Daraja Mamayar_bayanai_Daraja·Tsawo_Daraja·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(imel) 저장기[(imel)/4]
#define JKOROS_GENET_TEST 1
#include "../Hanyar_sadarwa_tara/Hade_da_waya_Hanyar_sadarwa.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Microsoft_Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Microsoft_Word_SMS&(1u<<29))){unsigned imel=(Microsoft_Word_SMS>>21)&31,Indes=(Microsoft_Word_SMS>>16)&31;
        if(imel!=1)유선저장기(0xe14)=1<<28;
        else{if(((Microsoft_Word_SMS>>26)&3)==1)물리값[Indes]=Microsoft_Word_SMS&65535;유선저장기(0xe14)=물리값[Indes];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *imel){const unsigned char Daraja[]={2,1,2,3,4,5};memcpy(imel,Daraja,6);return 1;}
void netif_set_link_up(struct netif *na_ura_Daraja){na_ura_Daraja->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *na_ura_Daraja){na_ura_Daraja->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *na_ura_Daraja,struct pbuf *전문,const ip4_addr_t *imel){(void)na_ura_Daraja;(void)전문;(void)imel;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer Tsarkiya_Indes,u16_t 수,pbuf_type 종류){
    (void)Tsarkiya_Indes;(void)종류;struct pbuf *Tarin_bayani=calloc(1,sizeof(*Tarin_bayani)+수);assert(Tarin_bayani);Tarin_bayani->payload=Tarin_bayani+1;Tarin_bayani->len=Tarin_bayani->tot_len=수;return Tarin_bayani;
}
u8_t pbuf_free(struct pbuf *Tarin_bayani){free(Tarin_bayani);return 1;}
err_t pbuf_take(struct pbuf *Tarin_bayani,const void *원본,u16_t 수){assert(수<=Tarin_bayani->len);memcpy(Tarin_bayani->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *Tarin_bayani,void *Zangon_ƙarshe_Daraja,u16_t 수,u16_t Tafiyar_da){assert(Tafiyar_da+수<=Tarin_bayani->len);memcpy(Zangon_ƙarshe_Daraja,(char*)Tarin_bayani->payload+Tafiyar_da,수);return 수;}
static err_t 받음(struct pbuf *Tarin_bayani,struct netif *na_ura_Daraja){(void)na_ura_Daraja;assert(Tarin_bayani->len==60);assert(((unsigned char*)Tarin_bayani->payload)[0]==0x42);들어온수++;pbuf_free(Tarin_bayani);return ERR_OK;}
int main(void){
    struct netif na_ura_Daraja;memset(&na_ura_Daraja,0,sizeof(na_ura_Daraja));na_ura_Daraja.input=받음;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Shirya_Hade_da_waya_Hanyar_sadarwa(&na_ura_Daraja)==ERR_OK);assert(Hade_da_waya_Daraja.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&na_ura_Daraja);assert(netif_is_link_up(&na_ura_Daraja));assert(Hade_da_waya_Daraja.속도==1000);
    Hade_da_waya_Daraja.생산=Hade_da_waya_Daraja.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&na_ura_Daraja,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=Hade_da_waya_Daraja.생산;}
    assert(Hade_da_waya_Daraja.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(Hade_da_waya_Daraja.Aika[0][0]==0x42&&Hade_da_waya_Daraja.Aika[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(Hade_da_waya_Daraja.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&na_ura_Daraja,전문)==ERR_MEM);pbuf_free(전문);
    memset(Hade_da_waya_Daraja.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&na_ura_Daraja);assert(들어온수==1&&Hade_da_waya_Daraja.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&na_ura_Daraja);
    assert(Hade_da_waya_Daraja.소비==0&&들어온수==1&&Hade_da_waya_Daraja.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&na_ura_Daraja);assert(!netif_is_link_up(&na_ura_Daraja));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
