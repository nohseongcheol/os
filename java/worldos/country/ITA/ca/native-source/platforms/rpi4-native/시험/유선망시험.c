/* 가짜 MMIO/MDIO 장치로 Loop_VALOR sobreeiximent_VALOR·durada_VALOR·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registrar_se_VALOR[0x10000/4];
#define 유선저장기(Adreça) registrar_se_VALOR[(Adreça)/4]
#define JKOROS_GENET_TEST 1
#include "../xarxa_Pila/per_cable_xarxa.c"
static uintptr_t data_i_hora_VALOR;
static int 물리작동=1,실물=1,Entrant_COMPT;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned Adreça=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(Adreça!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return data_i_hora_VALOR++;
}
int 보드실물(void){return 실물;}
int Tauler_màquina_ADREÇA(unsigned char *Adreça){const unsigned char VALOR[]={2,1,2,3,4,5};memcpy(Adreça,VALOR,6);return 1;}
void netif_set_link_up(struct netif *dispositiu_VALOR){dispositiu_VALOR->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *dispositiu_VALOR){dispositiu_VALOR->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *dispositiu_VALOR,struct pbuf *전문,const ip4_addr_t *Adreça){(void)dispositiu_VALOR;(void)전문;(void)Adreça;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer capa_INDEX,u16_t 수,pbuf_type 종류){
    (void)capa_INDEX;(void)종류;struct pbuf *dades=calloc(1,sizeof(*dades)+수);assert(dades);dades->payload=dades+1;dades->len=dades->tot_len=수;return dades;
}
u8_t pbuf_free(struct pbuf *dades){free(dades);return 1;}
err_t pbuf_take(struct pbuf *dades,const void *원본,u16_t 수){assert(수<=dades->len);memcpy(dades->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *dades,void *destinació_VALOR,u16_t 수,u16_t Executa_2){assert(Executa_2+수<=dades->len);memcpy(destinació_VALOR,(char*)dades->payload+Executa_2,수);return 수;}
static err_t acceptar_connexió(struct pbuf *dades,struct netif *dispositiu_VALOR){(void)dispositiu_VALOR;assert(dades->len==60);assert(((unsigned char*)dades->payload)[0]==0x42);Entrant_COMPT++;pbuf_free(dades);return ERR_OK;}
int main(void){
    struct netif dispositiu_VALOR;memset(&dispositiu_VALOR,0,sizeof(dispositiu_VALOR));dispositiu_VALOR.input=acceptar_connexió;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Prepara_per_cable_xarxa(&dispositiu_VALOR)==ERR_OK);assert(per_cable_VALOR.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&dispositiu_VALOR);assert(netif_is_link_up(&dispositiu_VALOR));assert(per_cable_VALOR.속도==1000);
    per_cable_VALOR.생산=per_cable_VALOR.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&dispositiu_VALOR,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=per_cable_VALOR.생산;}
    assert(per_cable_VALOR.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(per_cable_VALOR.enviar[0][0]==0x42&&per_cable_VALOR.enviar[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(per_cable_VALOR.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&dispositiu_VALOR,전문)==ERR_MEM);pbuf_free(전문);
    memset(per_cable_VALOR.rebre[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&dispositiu_VALOR);assert(Entrant_COMPT==1&&per_cable_VALOR.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&dispositiu_VALOR);
    assert(per_cable_VALOR.소비==0&&Entrant_COMPT==1&&per_cable_VALOR.집계[4]==1);
    물리값[1]=0;data_i_hora_VALOR+=1000;유선망살피기(&dispositiu_VALOR);assert(!netif_is_link_up(&dispositiu_VALOR));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
