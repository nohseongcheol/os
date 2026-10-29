/* 가짜 MMIO/MDIO 장치로 ലൂപ്_മൂല്യം കവിഞ്ഞ്_പോകല്_മൂല്യം·ദൈര്_ഘ്യം_മൂല്യം·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t രജിസ്_റ്റർ_ചെയ്യുക_മൂല്യം[0x10000/4];
#define 유선저장기(ഇമെയിൽ) രജിസ്_റ്റർ_ചെയ്യുക_മൂല്യം[(ഇമെയിൽ)/4]
#define JKOROS_GENET_TEST 1
#include "../നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക/പരസ്പരബന്ധിതമായ_നെറ്റ്_വർക്ക്.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t വാക്ക്_ലിഖിതം=유선저장기(0xe14);
    if(물리작동&&(വാക്ക്_ലിഖിതം&(1u<<29))){unsigned ഇമെയിൽ=(വാക്ക്_ലിഖിതം>>21)&31,സൂചിക=(വാക്ക്_ലിഖിതം>>16)&31;
        if(ഇമെയിൽ!=1)유선저장기(0xe14)=1<<28;
        else{if(((വാക്ക്_ലിഖിതം>>26)&3)==1)물리값[സൂചിക]=വാക്ക്_ലിഖിതം&65535;유선저장기(0xe14)=물리값[സൂചിക];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int ബോർഡ്_മെഷീൻ_ഇമെയിൽ(unsigned char *ഇമെയിൽ){const unsigned char മൂല്യം[]={2,1,2,3,4,5};memcpy(ഇമെയിൽ,മൂല്യം,6);return 1;}
void netif_set_link_up(struct netif *മൊബൈൽ_മൂല്യം){മൊബൈൽ_മൂല്യം->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *മൊബൈൽ_മൂല്യം){മൊബൈൽ_മൂല്യം->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *മൊബൈൽ_മൂല്യം,struct pbuf *전문,const ip4_addr_t *ഇമെയിൽ){(void)മൊബൈൽ_മൂല്യം;(void)전문;(void)ഇമെയിൽ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ലെയര്_സൂചിക,u16_t 수,pbuf_type 종류){
    (void)ലെയര്_സൂചിക;(void)종류;struct pbuf *ഡാറ്റാ=calloc(1,sizeof(*ഡാറ്റാ)+수);assert(ഡാറ്റാ);ഡാറ്റാ->payload=ഡാറ്റാ+1;ഡാറ്റാ->len=ഡാറ്റാ->tot_len=수;return ഡാറ്റാ;
}
u8_t pbuf_free(struct pbuf *ഡാറ്റാ){free(ഡാറ്റാ);return 1;}
err_t pbuf_take(struct pbuf *ഡാറ്റാ,const void *원본,u16_t 수){assert(수<=ഡാറ്റാ->len);memcpy(ഡാറ്റാ->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ഡാറ്റാ,void *ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം,u16_t 수,u16_t നടപ്പിലാക്കുക){assert(നടപ്പിലാക്കുക+수<=ഡാറ്റാ->len);memcpy(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം,(char*)ഡാറ്റാ->payload+നടപ്പിലാക്കുക,수);return 수;}
static err_t സ്വീകരിക്കുക_കണക്ഷൻ(struct pbuf *ഡാറ്റാ,struct netif *മൊബൈൽ_മൂല്യം){(void)മൊബൈൽ_മൂല്യം;assert(ഡാറ്റാ->len==60);assert(((unsigned char*)ഡാറ്റാ->payload)[0]==0x42);들어온수++;pbuf_free(ഡാറ്റാ);return ERR_OK;}
int main(void){
    struct netif മൊബൈൽ_മൂല്യം;memset(&മൊബൈൽ_മൂല്യം,0,sizeof(മൊബൈൽ_മൂല്യം));മൊബൈൽ_മൂല്യം.input=സ്വീകരിക്കുക_കണക്ഷൻ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(തയ്യാറാക്കുക_പരസ്പരബന്ധിതമായ_നെറ്റ്_വർക്ക്(&മൊബൈൽ_മൂല്യം)==ERR_OK);assert(പരസ്പരബന്ധിതമായ_മൂല്യം.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&മൊബൈൽ_മൂല്യം);assert(netif_is_link_up(&മൊബൈൽ_മൂല്യം));assert(പരസ്പരബന്ധിതമായ_മൂല്യം.속도==1000);
    പരസ്പരബന്ധിതമായ_മൂല്യം.생산=പരസ്പരബന്ധിതമായ_മൂല്യം.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&മൊബൈൽ_മൂല്യം,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=പരസ്പരബന്ധിതമായ_മൂല്യം.생산;}
    assert(പരസ്പരബന്ധിതമായ_മൂല്യം.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(പരസ്പരബന്ധിതമായ_മൂല്യം.അയയ്ക്കുക[0][0]==0x42&&പരസ്പരബന്ധിതമായ_മൂല്യം.അയയ്ക്കുക[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(പരസ്പരബന്ധിതമായ_മൂല്യം.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&മൊബൈൽ_മൂല്യം,전문)==ERR_MEM);pbuf_free(전문);
    memset(പരസ്പരബന്ധിതമായ_മൂല്യം.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&മൊബൈൽ_മൂല്യം);assert(들어온수==1&&പരസ്പരബന്ധിതമായ_മൂല്യം.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&മൊബൈൽ_മൂല്യം);
    assert(പരസ്പരബന്ധിതമായ_മൂല്യം.소비==0&&들어온수==1&&പരസ്പരബന്ധിതമായ_മൂല്യം.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&മൊബൈൽ_മൂല്യം);assert(!netif_is_link_up(&മൊബൈൽ_മൂല്യം));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
