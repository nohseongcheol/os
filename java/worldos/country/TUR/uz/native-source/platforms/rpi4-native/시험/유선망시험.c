/* 가짜 MMIO/MDIO 장치로 Loop_VALUE to_lib_ketish_VALUE·uzunlik_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(manzil) 저장기[(manzil)/4]
#define JKOROS_GENET_TEST 1
#include "../Tarmoq_Stack/o_tkazish_Tarmoq.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,Kirish_qo_ng_irog_i_COUNT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned manzil=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(manzil!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *manzil){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(manzil,VALUE,6);return 1;}
void netif_set_link_up(struct netif *qurilma_VALUE){qurilma_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *qurilma_VALUE){qurilma_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *qurilma_VALUE,struct pbuf *전문,const ip4_addr_t *manzil){(void)qurilma_VALUE;(void)전문;(void)manzil;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer qatlam_INDEX,u16_t 수,pbuf_type 종류){
    (void)qatlam_INDEX;(void)종류;struct pbuf *ma_lumotlar=calloc(1,sizeof(*ma_lumotlar)+수);assert(ma_lumotlar);ma_lumotlar->payload=ma_lumotlar+1;ma_lumotlar->len=ma_lumotlar->tot_len=수;return ma_lumotlar;
}
u8_t pbuf_free(struct pbuf *ma_lumotlar){free(ma_lumotlar);return 1;}
err_t pbuf_take(struct pbuf *ma_lumotlar,const void *원본,u16_t 수){assert(수<=ma_lumotlar->len);memcpy(ma_lumotlar->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ma_lumotlar,void *ko_chirish_joyi_VALUE,u16_t 수,u16_t Bajarish){assert(Bajarish+수<=ma_lumotlar->len);memcpy(ko_chirish_joyi_VALUE,(char*)ma_lumotlar->payload+Bajarish,수);return 수;}
static err_t qabul_qilish_aloqa(struct pbuf *ma_lumotlar,struct netif *qurilma_VALUE){(void)qurilma_VALUE;assert(ma_lumotlar->len==60);assert(((unsigned char*)ma_lumotlar->payload)[0]==0x42);Kirish_qo_ng_irog_i_COUNT++;pbuf_free(ma_lumotlar);return ERR_OK;}
int main(void){
    struct netif qurilma_VALUE;memset(&qurilma_VALUE,0,sizeof(qurilma_VALUE));qurilma_VALUE.input=qabul_qilish_aloqa;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Tayyorlamoq_o_tkazish_Tarmoq(&qurilma_VALUE)==ERR_OK);assert(o_tkazish_VALUE.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&qurilma_VALUE);assert(netif_is_link_up(&qurilma_VALUE));assert(o_tkazish_VALUE.속도==1000);
    o_tkazish_VALUE.생산=o_tkazish_VALUE.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&qurilma_VALUE,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=o_tkazish_VALUE.생산;}
    assert(o_tkazish_VALUE.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(o_tkazish_VALUE.yuborish[0][0]==0x42&&o_tkazish_VALUE.yuborish[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(o_tkazish_VALUE.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&qurilma_VALUE,전문)==ERR_MEM);pbuf_free(전문);
    memset(o_tkazish_VALUE.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&qurilma_VALUE);assert(Kirish_qo_ng_irog_i_COUNT==1&&o_tkazish_VALUE.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&qurilma_VALUE);
    assert(o_tkazish_VALUE.소비==0&&Kirish_qo_ng_irog_i_COUNT==1&&o_tkazish_VALUE.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&qurilma_VALUE);assert(!netif_is_link_up(&qurilma_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
