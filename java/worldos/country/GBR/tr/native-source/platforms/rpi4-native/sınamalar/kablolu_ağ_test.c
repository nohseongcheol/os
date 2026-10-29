/* 가짜 MMIO/MDIO 장치로 Loop_değer Taşma_değer·süre_değer·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t yazmaç[0x10000/4];
#define 유선저장기(ADRES) yazmaç[(ADRES)/4]
#define JKOROS_GENET_TEST 1
#include "../ağ_Yığın/kablolu_ağ.c"
static uintptr_t zaman_damgası_değer;
static int 물리작동=1,실물=1,Gelen_BAĞ_DEĞ_SAY;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned ADRES=(Word_SMS>>21)&31,Dizin=(Word_SMS>>16)&31;
        if(ADRES!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[Dizin]=Word_SMS&65535;유선저장기(0xe14)=물리값[Dizin];}}
    return zaman_damgası_değer++;
}
int 보드실물(void){return 실물;}
int Pano_mutlak_adres(unsigned char *ADRES){const unsigned char değer[]={2,1,2,3,4,5};memcpy(ADRES,değer,6);return 1;}
void netif_set_link_up(struct netif *cihaz_değer){cihaz_değer->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *cihaz_değer){cihaz_değer->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *cihaz_değer,struct pbuf *veri_birimi,const ip4_addr_t *ADRES){(void)cihaz_değer;(void)veri_birimi;(void)ADRES;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer katman_Dizin,u16_t 수,pbuf_type Tip_değer){
    (void)katman_Dizin;(void)Tip_değer;struct pbuf *veri=calloc(1,sizeof(*veri)+수);assert(veri);veri->payload=veri+1;veri->len=veri->tot_len=수;return veri;
}
u8_t pbuf_free(struct pbuf *veri){free(veri);return 1;}
err_t pbuf_take(struct pbuf *veri,const void *원본,u16_t 수){assert(수<=veri->len);memcpy(veri->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *veri,void *hedef_değer,u16_t 수,u16_t çalıştır){assert(çalıştır+수<=veri->len);memcpy(hedef_değer,(char*)veri->payload+çalıştır,수);return 수;}
static err_t kabul_etmek_cxn(struct pbuf *veri,struct netif *cihaz_değer){(void)cihaz_değer;assert(veri->len==60);assert(((unsigned char*)veri->payload)[0]==0x42);Gelen_BAĞ_DEĞ_SAY++;pbuf_free(veri);return ERR_OK;}
int main(void){
    struct netif cihaz_değer;memset(&cihaz_değer,0,sizeof(cihaz_değer));cihaz_değer.input=kabul_etmek_cxn;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Hazırlan_kablolu_ağ(&cihaz_değer)==ERR_OK);assert(kablolu_değer.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&cihaz_değer);assert(netif_is_link_up(&cihaz_değer));assert(kablolu_değer.속도==1000);
    kablolu_değer.생산=kablolu_değer.tüketmek_değer=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *veri_birimi=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(veri_birimi->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(göndermek_veri_birimi(&cihaz_değer,veri_birimi)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=kablolu_değer.생산;}
    assert(kablolu_değer.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(kablolu_değer.göndermek[0][0]==0x42&&kablolu_değer.göndermek[0][59]==0);pbuf_free(veri_birimi);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(kablolu_değer.생산-255)&65535;veri_birimi=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(göndermek_veri_birimi(&cihaz_değer,veri_birimi)==ERR_MEM);pbuf_free(veri_birimi);
    memset(kablolu_değer.almak[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&cihaz_değer);assert(Gelen_BAĞ_DEĞ_SAY==1&&kablolu_değer.tüketmek_değer==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&cihaz_değer);
    assert(kablolu_değer.tüketmek_değer==0&&Gelen_BAĞ_DEĞ_SAY==1&&kablolu_değer.İstatistik_değer[4]==1);
    물리값[1]=0;zaman_damgası_değer+=1000;유선망살피기(&cihaz_değer);assert(!netif_is_link_up(&cihaz_değer));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
