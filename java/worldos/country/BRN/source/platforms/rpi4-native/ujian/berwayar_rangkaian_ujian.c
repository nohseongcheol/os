/* 가짜 MMIO/MDIO 장치로 Loop_VALUE limpahan_VALUE·kepanjangan_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t daftar[0x10000/4];
#define 유선저장기(e_mel) daftar[(e_mel)/4]
#define JKOROS_GENET_TEST 1
#include "../rangkaian_tindan/berwayar_rangkaian.c"
static uintptr_t cap_masa_VALUE;
static int 물리작동=1,실물=1,Masuk_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned e_mel=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(e_mel!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return cap_masa_VALUE++;
}
int 보드실물(void){return 실물;}
int Papan_mesin_e_mel(unsigned char *e_mel){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(e_mel,VALUE,6);return 1;}
void netif_set_link_up(struct netif *peranti_VALUE){peranti_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *peranti_VALUE){peranti_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *peranti_VALUE,struct pbuf *전문,const ip4_addr_t *e_mel){(void)peranti_VALUE;(void)전문;(void)e_mel;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer lapisan_INDEX,u16_t 수,pbuf_type 종류){
    (void)lapisan_INDEX;(void)종류;struct pbuf *data=calloc(1,sizeof(*data)+수);assert(data);data->payload=data+1;data->len=data->tot_len=수;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *원본,u16_t 수){assert(수<=data->len);memcpy(data->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *destinasi_VALUE,u16_t 수,u16_t Jalan){assert(Jalan+수<=data->len);memcpy(destinasi_VALUE,(char*)data->payload+Jalan,수);return 수;}
static err_t terima_hubungan(struct pbuf *data,struct netif *peranti_VALUE){(void)peranti_VALUE;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);Masuk_COUNT++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif peranti_VALUE;memset(&peranti_VALUE,0,sizeof(peranti_VALUE));peranti_VALUE.input=terima_hubungan;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Sediakan_berwayar_rangkaian(&peranti_VALUE)==ERR_OK);assert(berwayar_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&peranti_VALUE);assert(netif_is_link_up(&peranti_VALUE));assert(berwayar_VALUE.속도==1000);
    berwayar_VALUE.생산=berwayar_VALUE.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&peranti_VALUE,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=berwayar_VALUE.생산;}
    assert(berwayar_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(berwayar_VALUE.e_mel_9aee63bd[0][0]==0x42&&berwayar_VALUE.e_mel_9aee63bd[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(berwayar_VALUE.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&peranti_VALUE,전문)==ERR_MEM);pbuf_free(전문);
    memset(berwayar_VALUE.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&peranti_VALUE);assert(Masuk_COUNT==1&&berwayar_VALUE.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&peranti_VALUE);
    assert(berwayar_VALUE.소비==0&&Masuk_COUNT==1&&berwayar_VALUE.집계[4]==1);
    물리값[1]=0;cap_masa_VALUE+=1000;유선망살피기(&peranti_VALUE);assert(!netif_is_link_up(&peranti_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
