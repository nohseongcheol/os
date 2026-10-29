/* 가짜 MMIO/MDIO 장치로 循環值 溢出值·長度·링크 전환을 검사한다. 物理硬件 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 寄存器值[0x10000/4];
#define 有線寄存器集(地址) 寄存器值[(地址)/4]
#define JKOROS_GENET_TEST 1
#include "../通信網絡/有線網路.c"
static uintptr_t 時間戳值;
static int 物理操作=1,物理硬件=1,傳入個數;
static unsigned short 物理值[32];
uintptr_t 板經過毫秒(void){
    uint32_t 機器字文本=有線寄存器集(0xe14);
    if(物理操作&&(機器字文本&(1u<<29))){unsigned 地址=(機器字文本>>21)&31,編號=(機器字文本>>16)&31;
        if(地址!=1)有線寄存器集(0xe14)=1<<28;
        else{if(((機器字文本>>26)&3)==1)物理值[編號]=機器字文本&65535;有線寄存器集(0xe14)=物理值[編號];}}
    return 時間戳值++;
}
int 板物理硬件(void){return 物理硬件;}
int 板計算機地址(unsigned char *地址){const unsigned char 值[]={2,1,2,3,4,5};memcpy(地址,值,6);return 1;}
void netif_set_link_up(struct netif *設備){設備->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *設備){設備->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *設備,struct pbuf *數據報,const ip4_addr_t *地址){(void)設備;(void)數據報;(void)地址;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer 層索引,u16_t 數,pbuf_type 種類值){
    (void)層索引;(void)種類值;struct pbuf *資料=calloc(1,sizeof(*資料)+數);assert(資料);資料->payload=資料+1;資料->len=資料->tot_len=數;return 資料;
}
u8_t pbuf_free(struct pbuf *資料){free(資料);return 1;}
err_t pbuf_take(struct pbuf *資料,const void *原始,u16_t 數){assert(數<=資料->len);memcpy(資料->payload,原始,數);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *資料,void *目的地址值,u16_t 數,u16_t 運行){assert(運行+數<=資料->len);memcpy(目的地址值,(char*)資料->payload+運行,數);return 數;}
static err_t 接受連接狀態(struct pbuf *資料,struct netif *設備){(void)設備;assert(資料->len==60);assert(((unsigned char*)資料->payload)[0]==0x42);傳入個數++;pbuf_free(資料);return ERR_OK;}
int main(void){
    struct netif 設備;memset(&設備,0,sizeof(設備));設備.input=接受連接狀態;
    有線寄存器集(0)=6u<<24;物理值[2]=0x600d;物理值[1]=4;物理值[25]=7<<8;
    物理硬件=0;assert(!擁有有線設備());物理硬件=1;assert(擁有有線設備());
    
    assert(準備有線網路(&設備)==ERR_OK);assert(有線值.物理地址==1);
    assert(有線寄存器集(GENET_RX_DMA_CTRL)==0x20001&&有線寄存器集(GENET_TX_DMA_CTRL)==0x20001);
    assert(有線寄存器集(0x80c)==0x02010203&&有線寄存器集(0x810)==0x0405);
    審查有線網路(&設備);assert(netif_is_link_up(&設備));assert(有線值.速度值==1000);
    有線值.產生值=有線值.消耗值=65534;有線寄存器集(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *數據報=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(數據報->payload,0x42,40);
    for(unsigned 序數索引=0;序數索引<3;序數索引++){assert(發送數據報(&設備,數據報)==ERR_OK);有線寄存器集(GENET_TX_DMA_CONS_INDEX(16))=有線值.產生值;}
    assert(有線值.產生值==1);assert((有線寄存器集(0x4000)>>16)==60);assert(有線值.發送[0][0]==0x42&&有線值.發送[0][59]==0);pbuf_free(數據報);
    有線寄存器集(GENET_TX_DMA_CONS_INDEX(16))=(有線值.產生值-255)&65535;數據報=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(發送數據報(&設備,數據報)==ERR_MEM);pbuf_free(數據報);
    memset(有線值.接收[254],0x42,64);有線寄存器集(0x2000+254*12)=(62<<16)|0x6000;有線寄存器集(GENET_RX_DMA_PROD_INDEX(16))=65535;
    審查有線網路(&設備);assert(傳入個數==1&&有線值.消耗值==65535);
    有線寄存器集(0x2000+255*12)=(4095u<<16)|0x6000;有線寄存器集(GENET_RX_DMA_PROD_INDEX(16))=0;審查有線網路(&設備);
    assert(有線值.消耗值==0&&傳入個數==1&&有線值.統計值[4]==1);
    物理值[1]=0;時間戳值+=1000;審查有線網路(&設備);assert(!netif_is_link_up(&設備));
    物理操作=0;assert(物理傳送(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
