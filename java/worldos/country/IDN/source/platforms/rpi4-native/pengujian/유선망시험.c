/* 가짜 MMIO/MDIO 장치로 Loop_VALUE luapan_VALUE·panjang_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t register[0x10000/4];
#define 유선저장기(surel) register[(surel)/4]
#define JKOROS_GENET_TEST 1
#include "../jaringan_tumpuk/terkabel_jaringan.c"
static uintptr_t stempel_waktu_VALUE;
static int 물리작동=1,실물=1,Masuk_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Kata_SMS=유선저장기(0xe14);
    if(물리작동&&(Kata_SMS&(1u<<29))){unsigned surel=(Kata_SMS>>21)&31,INDEX=(Kata_SMS>>16)&31;
        if(surel!=1)유선저장기(0xe14)=1<<28;
        else{if(((Kata_SMS>>26)&3)==1)물리값[INDEX]=Kata_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return stempel_waktu_VALUE++;
}
int 보드실물(void){return 실물;}
int Papan_mesin_surel(unsigned char *surel){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(surel,VALUE,6);return 1;}
void netif_set_link_up(struct netif *Ponsel_VALUE){Ponsel_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *Ponsel_VALUE){Ponsel_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *Ponsel_VALUE,struct pbuf *전문,const ip4_addr_t *surel){(void)Ponsel_VALUE;(void)전문;(void)surel;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer lapisan_INDEX,u16_t 수,pbuf_type 종류){
    (void)lapisan_INDEX;(void)종류;struct pbuf *data=calloc(1,sizeof(*data)+수);assert(data);data->payload=data+1;data->len=data->tot_len=수;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *원본,u16_t 수){assert(수<=data->len);memcpy(data->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *tujuan_VALUE,u16_t 수,u16_t jalankan){assert(jalankan+수<=data->len);memcpy(tujuan_VALUE,(char*)data->payload+jalankan,수);return 수;}
static err_t terima_koneksi(struct pbuf *data,struct netif *Ponsel_VALUE){(void)Ponsel_VALUE;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);Masuk_COUNT++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif Ponsel_VALUE;memset(&Ponsel_VALUE,0,sizeof(Ponsel_VALUE));Ponsel_VALUE.input=terima_koneksi;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Siapkan_terkabel_jaringan(&Ponsel_VALUE)==ERR_OK);assert(terkabel_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&Ponsel_VALUE);assert(netif_is_link_up(&Ponsel_VALUE));assert(terkabel_VALUE.속도==1000);
    terkabel_VALUE.생산=terkabel_VALUE.konsumsi_VALUE=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&Ponsel_VALUE,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=terkabel_VALUE.생산;}
    assert(terkabel_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(terkabel_VALUE.kirim[0][0]==0x42&&terkabel_VALUE.kirim[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(terkabel_VALUE.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&Ponsel_VALUE,전문)==ERR_MEM);pbuf_free(전문);
    memset(terkabel_VALUE.terima[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&Ponsel_VALUE);assert(Masuk_COUNT==1&&terkabel_VALUE.konsumsi_VALUE==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&Ponsel_VALUE);
    assert(terkabel_VALUE.konsumsi_VALUE==0&&Masuk_COUNT==1&&terkabel_VALUE.집계[4]==1);
    물리값[1]=0;stempel_waktu_VALUE+=1000;유선망살피기(&Ponsel_VALUE);assert(!netif_is_link_up(&Ponsel_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
