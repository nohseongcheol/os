/* 가짜 MMIO/MDIO 장치로 giáTrịVòngLặp giáTrịTràn·độDài·링크 전환을 검사한다. phầnCứngVậtLý 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t thanhGhi[0x10000/4];
#define cácThanhGhiHữuTuyến(địaChỉ) thanhGhi[(địaChỉ)/4]
#define JKOROS_GENET_TEST 1
#include "../NgănXếpMạng/mạngHữuTuyến.c"
static uintptr_t giáTrịDấuThờiGian;
static int thaoTácVậtLý=1,phầnCứngVậtLý=1,sốLượngĐiVào;
static unsigned short giáTrịVậtLý[32];
uintptr_t miliGiâyGọnBoMạch(void){
    uint32_t vănBảnTừ=cácThanhGhiHữuTuyến(0xe14);
    if(thaoTácVậtLý&&(vănBảnTừ&(1u<<29))){unsigned địaChỉ=(vănBảnTừ>>21)&31,sốHiệu=(vănBảnTừ>>16)&31;
        if(địaChỉ!=1)cácThanhGhiHữuTuyến(0xe14)=1<<28;
        else{if(((vănBảnTừ>>26)&3)==1)giáTrịVậtLý[sốHiệu]=vănBảnTừ&65535;cácThanhGhiHữuTuyến(0xe14)=giáTrịVậtLý[sốHiệu];}}
    return giáTrịDấuThờiGian++;
}
int phầnCứngVậtLýBoMạch(void){return phầnCứngVậtLý;}
int địaChỉMáyBoMạch(unsigned char *địaChỉ){const unsigned char giáTrị[]={2,1,2,3,4,5};memcpy(địaChỉ,giáTrị,6);return 1;}
void netif_set_link_up(struct netif *ThiếtBị){ThiếtBị->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ThiếtBị){ThiếtBị->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ThiếtBị,struct pbuf *điệnDữLiệu,const ip4_addr_t *địaChỉ){(void)ThiếtBị;(void)điệnDữLiệu;(void)địaChỉ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer chỉSốTầng,u16_t trịSố,pbuf_type giáTrịLoại){
    (void)chỉSốTầng;(void)giáTrịLoại;struct pbuf *DữLiệu=calloc(1,sizeof(*DữLiệu)+trịSố);assert(DữLiệu);DữLiệu->payload=DữLiệu+1;DữLiệu->len=DữLiệu->tot_len=trịSố;return DữLiệu;
}
u8_t pbuf_free(struct pbuf *DữLiệu){free(DữLiệu);return 1;}
err_t pbuf_take(struct pbuf *DữLiệu,const void *nguyênBản,u16_t trịSố){assert(trịSố<=DữLiệu->len);memcpy(DữLiệu->payload,nguyênBản,trịSố);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *DữLiệu,void *giáTrịĐích,u16_t trịSố,u16_t chạy){assert(chạy+trịSố<=DữLiệu->len);memcpy(giáTrịĐích,(char*)DữLiệu->payload+chạy,trịSố);return trịSố;}
static err_t chấpNhậnKếtNối(struct pbuf *DữLiệu,struct netif *ThiếtBị){(void)ThiếtBị;assert(DữLiệu->len==60);assert(((unsigned char*)DữLiệu->payload)[0]==0x42);sốLượngĐiVào++;pbuf_free(DữLiệu);return ERR_OK;}
int main(void){
    struct netif ThiếtBị;memset(&ThiếtBị,0,sizeof(ThiếtBị));ThiếtBị.input=chấpNhậnKếtNối;
    cácThanhGhiHữuTuyến(0)=6u<<24;giáTrịVậtLý[2]=0x600d;giáTrịVậtLý[1]=4;giáTrịVậtLý[25]=7<<8;
    phầnCứngVậtLý=0;assert(!cóThiếtBịHữuTuyến());phầnCứngVậtLý=1;assert(cóThiếtBịHữuTuyến());
    
    assert(chuẩnBịMạngHữuTuyến(&ThiếtBị)==ERR_OK);assert(giáTrịHữuTuyến.địaChỉVậtLý==1);
    assert(cácThanhGhiHữuTuyến(GENET_RX_DMA_CTRL)==0x20001&&cácThanhGhiHữuTuyến(GENET_TX_DMA_CTRL)==0x20001);
    assert(cácThanhGhiHữuTuyến(0x80c)==0x02010203&&cácThanhGhiHữuTuyến(0x810)==0x0405);
    xemXétMạngHữuTuyến(&ThiếtBị);assert(netif_is_link_up(&ThiếtBị));assert(giáTrịHữuTuyến.giáTrịTốcĐộ==1000);
    giáTrịHữuTuyến.giáTrịSảnSinh=giáTrịHữuTuyến.tiêuThụGiáTrị=65534;cácThanhGhiHữuTuyến(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *điệnDữLiệu=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(điệnDữLiệu->payload,0x42,40);
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<3;chỉSốThứBậc++){assert(gửiĐiệnDữLiệu(&ThiếtBị,điệnDữLiệu)==ERR_OK);cácThanhGhiHữuTuyến(GENET_TX_DMA_CONS_INDEX(16))=giáTrịHữuTuyến.giáTrịSảnSinh;}
    assert(giáTrịHữuTuyến.giáTrịSảnSinh==1);assert((cácThanhGhiHữuTuyến(0x4000)>>16)==60);assert(giáTrịHữuTuyến.gửi[0][0]==0x42&&giáTrịHữuTuyến.gửi[0][59]==0);pbuf_free(điệnDữLiệu);
    cácThanhGhiHữuTuyến(GENET_TX_DMA_CONS_INDEX(16))=(giáTrịHữuTuyến.giáTrịSảnSinh-255)&65535;điệnDữLiệu=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(gửiĐiệnDữLiệu(&ThiếtBị,điệnDữLiệu)==ERR_MEM);pbuf_free(điệnDữLiệu);
    memset(giáTrịHữuTuyến.nhận[254],0x42,64);cácThanhGhiHữuTuyến(0x2000+254*12)=(62<<16)|0x6000;cácThanhGhiHữuTuyến(GENET_RX_DMA_PROD_INDEX(16))=65535;
    xemXétMạngHữuTuyến(&ThiếtBị);assert(sốLượngĐiVào==1&&giáTrịHữuTuyến.tiêuThụGiáTrị==65535);
    cácThanhGhiHữuTuyến(0x2000+255*12)=(4095u<<16)|0x6000;cácThanhGhiHữuTuyến(GENET_RX_DMA_PROD_INDEX(16))=0;xemXétMạngHữuTuyến(&ThiếtBị);
    assert(giáTrịHữuTuyến.tiêuThụGiáTrị==0&&sốLượngĐiVào==1&&giáTrịHữuTuyến.giáTrịThốngKê[4]==1);
    giáTrịVậtLý[1]=0;giáTrịDấuThờiGian+=1000;xemXétMạngHữuTuyến(&ThiếtBị);assert(!netif_is_link_up(&ThiếtBị));
    thaoTácVậtLý=0;assert(chuyểnGiaoVậtLý(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
