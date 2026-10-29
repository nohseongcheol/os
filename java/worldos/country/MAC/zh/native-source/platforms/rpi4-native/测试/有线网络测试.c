/* 가짜 MMIO/MDIO 장치로 循环值 溢出值·长度·링크 전환을 검사한다. 物理硬件 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 寄存器值[0x10000/4];
#define 有线寄存器集(地址) 寄存器值[(地址)/4]
#define JKOROS_GENET_TEST 1
#include "../通信网络/有线网络.c"
static uintptr_t 时间戳值;
static int 物理操作=1,物理硬件=1,传入个数;
static unsigned short 物理值[32];
uintptr_t 板经过毫秒(void){
    uint32_t 机器字文本=有线寄存器集(0xe14);
    if(物理操作&&(机器字文本&(1u<<29))){unsigned 地址=(机器字文本>>21)&31,编号=(机器字文本>>16)&31;
        if(地址!=1)有线寄存器集(0xe14)=1<<28;
        else{if(((机器字文本>>26)&3)==1)物理值[编号]=机器字文本&65535;有线寄存器集(0xe14)=物理值[编号];}}
    return 时间戳值++;
}
int 板物理硬件(void){return 物理硬件;}
int 板计算机地址(unsigned char *地址){const unsigned char 值[]={2,1,2,3,4,5};memcpy(地址,值,6);return 1;}
void netif_set_link_up(struct netif *设备){设备->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *设备){设备->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *设备,struct pbuf *数据报,const ip4_addr_t *地址){(void)设备;(void)数据报;(void)地址;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer 层索引,u16_t 数,pbuf_type 种类值){
    (void)层索引;(void)种类值;struct pbuf *数据=calloc(1,sizeof(*数据)+数);assert(数据);数据->payload=数据+1;数据->len=数据->tot_len=数;return 数据;
}
u8_t pbuf_free(struct pbuf *数据){free(数据);return 1;}
err_t pbuf_take(struct pbuf *数据,const void *原始,u16_t 数){assert(数<=数据->len);memcpy(数据->payload,原始,数);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *数据,void *目的地址值,u16_t 数,u16_t 运行){assert(运行+数<=数据->len);memcpy(目的地址值,(char*)数据->payload+运行,数);return 数;}
static err_t 接受连接状态(struct pbuf *数据,struct netif *设备){(void)设备;assert(数据->len==60);assert(((unsigned char*)数据->payload)[0]==0x42);传入个数++;pbuf_free(数据);return ERR_OK;}
int main(void){
    struct netif 设备;memset(&设备,0,sizeof(设备));设备.input=接受连接状态;
    有线寄存器集(0)=6u<<24;物理值[2]=0x600d;物理值[1]=4;物理值[25]=7<<8;
    物理硬件=0;assert(!拥有有线设备());物理硬件=1;assert(拥有有线设备());
    
    assert(准备有线网络(&设备)==ERR_OK);assert(有线值.物理地址==1);
    assert(有线寄存器集(GENET_RX_DMA_CTRL)==0x20001&&有线寄存器集(GENET_TX_DMA_CTRL)==0x20001);
    assert(有线寄存器集(0x80c)==0x02010203&&有线寄存器集(0x810)==0x0405);
    审查有线网络(&设备);assert(netif_is_link_up(&设备));assert(有线值.速度值==1000);
    有线值.产生值=有线值.消耗值=65534;有线寄存器集(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *数据报=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(数据报->payload,0x42,40);
    for(unsigned 序数索引=0;序数索引<3;序数索引++){assert(发送数据报(&设备,数据报)==ERR_OK);有线寄存器集(GENET_TX_DMA_CONS_INDEX(16))=有线值.产生值;}
    assert(有线值.产生值==1);assert((有线寄存器集(0x4000)>>16)==60);assert(有线值.发送[0][0]==0x42&&有线值.发送[0][59]==0);pbuf_free(数据报);
    有线寄存器集(GENET_TX_DMA_CONS_INDEX(16))=(有线值.产生值-255)&65535;数据报=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(发送数据报(&设备,数据报)==ERR_MEM);pbuf_free(数据报);
    memset(有线值.接收[254],0x42,64);有线寄存器集(0x2000+254*12)=(62<<16)|0x6000;有线寄存器集(GENET_RX_DMA_PROD_INDEX(16))=65535;
    审查有线网络(&设备);assert(传入个数==1&&有线值.消耗值==65535);
    有线寄存器集(0x2000+255*12)=(4095u<<16)|0x6000;有线寄存器集(GENET_RX_DMA_PROD_INDEX(16))=0;审查有线网络(&设备);
    assert(有线值.消耗值==0&&传入个数==1&&有线值.统计值[4]==1);
    物理值[1]=0;时间戳值+=1000;审查有线网络(&设备);assert(!netif_is_link_up(&设备));
    物理操作=0;assert(物理传送(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
