/* 가짜 MMIO/MDIO 장치로 ループ値 桁あふれ値·長さ·링크 전환을 검사한다. 物理機器 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 値レジスタ[0x10000/4];
#define 結線済みレジスタ群(番地) 値レジスタ[(番地)/4]
#define JKOROS_GENET_TEST 1
#include "../通信網/結線済み通信網.c"
static uintptr_t 時刻印値;
static int 物理操作=1,物理機器=1,到来個数;
static unsigned short 物理値[32];
uintptr_t 基板経過ミリ秒(void){
    uint32_t 語本文=結線済みレジスタ群(0xe14);
    if(物理操作&&(語本文&(1u<<29))){unsigned 番地=(語本文>>21)&31,番号=(語本文>>16)&31;
        if(番地!=1)結線済みレジスタ群(0xe14)=1<<28;
        else{if(((語本文>>26)&3)==1)物理値[番号]=語本文&65535;結線済みレジスタ群(0xe14)=物理値[番号];}}
    return 時刻印値++;
}
int 基板物理機器(void){return 物理機器;}
int 基板機械番地(unsigned char *番地){const unsigned char 値[]={2,1,2,3,4,5};memcpy(番地,値,6);return 1;}
void netif_set_link_up(struct netif *装置){装置->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *装置){装置->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *装置,struct pbuf *データグラム,const ip4_addr_t *番地){(void)装置;(void)データグラム;(void)番地;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer 階層添字,u16_t 数,pbuf_type 種別値){
    (void)階層添字;(void)種別値;struct pbuf *データ=calloc(1,sizeof(*データ)+数);assert(データ);データ->payload=データ+1;データ->len=データ->tot_len=数;return データ;
}
u8_t pbuf_free(struct pbuf *データ){free(データ);return 1;}
err_t pbuf_take(struct pbuf *データ,const void *原本,u16_t 数){assert(数<=データ->len);memcpy(データ->payload,原本,数);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *データ,void *宛先値,u16_t 数,u16_t 起動処理){assert(起動処理+数<=データ->len);memcpy(宛先値,(char*)データ->payload+起動処理,数);return 数;}
static err_t 接続状態受理(struct pbuf *データ,struct netif *装置){(void)装置;assert(データ->len==60);assert(((unsigned char*)データ->payload)[0]==0x42);到来個数++;pbuf_free(データ);return ERR_OK;}
int main(void){
    struct netif 装置;memset(&装置,0,sizeof(装置));装置.input=接続状態受理;
    結線済みレジスタ群(0)=6u<<24;物理値[2]=0x600d;物理値[1]=4;物理値[25]=7<<8;
    物理機器=0;assert(!保有結線済み装置());物理機器=1;assert(保有結線済み装置());
    
    assert(結線済み通信網用意(&装置)==ERR_OK);assert(結線済み値.物理番地==1);
    assert(結線済みレジスタ群(GENET_RX_DMA_CTRL)==0x20001&&結線済みレジスタ群(GENET_TX_DMA_CTRL)==0x20001);
    assert(結線済みレジスタ群(0x80c)==0x02010203&&結線済みレジスタ群(0x810)==0x0405);
    結線済み通信網調査(&装置);assert(netif_is_link_up(&装置));assert(結線済み値.速度値==1000);
    結線済み値.生成処理値=結線済み値.値消費=65534;結線済みレジスタ群(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *データグラム=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(データグラム->payload,0x42,40);
    for(unsigned 序数添字=0;序数添字<3;序数添字++){assert(データグラム送信(&装置,データグラム)==ERR_OK);結線済みレジスタ群(GENET_TX_DMA_CONS_INDEX(16))=結線済み値.生成処理値;}
    assert(結線済み値.生成処理値==1);assert((結線済みレジスタ群(0x4000)>>16)==60);assert(結線済み値.送信[0][0]==0x42&&結線済み値.送信[0][59]==0);pbuf_free(データグラム);
    結線済みレジスタ群(GENET_TX_DMA_CONS_INDEX(16))=(結線済み値.生成処理値-255)&65535;データグラム=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(データグラム送信(&装置,データグラム)==ERR_MEM);pbuf_free(データグラム);
    memset(結線済み値.受取[254],0x42,64);結線済みレジスタ群(0x2000+254*12)=(62<<16)|0x6000;結線済みレジスタ群(GENET_RX_DMA_PROD_INDEX(16))=65535;
    結線済み通信網調査(&装置);assert(到来個数==1&&結線済み値.値消費==65535);
    結線済みレジスタ群(0x2000+255*12)=(4095u<<16)|0x6000;結線済みレジスタ群(GENET_RX_DMA_PROD_INDEX(16))=0;結線済み通信網調査(&装置);
    assert(結線済み値.値消費==0&&到来個数==1&&結線済み値.統計値[4]==1);
    物理値[1]=0;時刻印値+=1000;結線済み通信網調査(&装置);assert(!netif_is_link_up(&装置));
    物理操作=0;assert(物理転送(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
