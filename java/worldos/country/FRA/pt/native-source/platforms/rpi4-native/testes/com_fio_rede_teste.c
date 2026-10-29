/* 가짜 MMIO/MDIO 장치로 Loop_VALOR estouro_VALOR·duração_VALOR·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registo[0x10000/4];
#define 유선저장기(Endereço) registo[(Endereço)/4]
#define JKOROS_GENET_TEST 1
#include "../rede_pilha/com_fio_rede.c"
static uintptr_t carimbo_de_data_hora_VALOR;
static int 물리작동=1,실물=1,recebida_CONT_NÚM;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned Endereço=(Word_SMS>>21)&31,ÍNDICE=(Word_SMS>>16)&31;
        if(Endereço!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[ÍNDICE]=Word_SMS&65535;유선저장기(0xe14)=물리값[ÍNDICE];}}
    return carimbo_de_data_hora_VALOR++;
}
int 보드실물(void){return 실물;}
int Quadro_endereço_real(unsigned char *Endereço){const unsigned char VALOR[]={2,1,2,3,4,5};memcpy(Endereço,VALOR,6);return 1;}
void netif_set_link_up(struct netif *celular_VALOR){celular_VALOR->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *celular_VALOR){celular_VALOR->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *celular_VALOR,struct pbuf *datagrama,const ip4_addr_t *Endereço){(void)celular_VALOR;(void)datagrama;(void)Endereço;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer camada_ÍNDICE,u16_t número,pbuf_type Tipo_VALOR){
    (void)camada_ÍNDICE;(void)Tipo_VALOR;struct pbuf *dados=calloc(1,sizeof(*dados)+número);assert(dados);dados->payload=dados+1;dados->len=dados->tot_len=número;return dados;
}
u8_t pbuf_free(struct pbuf *dados){free(dados);return 1;}
err_t pbuf_take(struct pbuf *dados,const void *원본,u16_t número){assert(número<=dados->len);memcpy(dados->payload,원본,número);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *dados,void *destino_VALOR,u16_t número,u16_t iniciar){assert(iniciar+número<=dados->len);memcpy(destino_VALOR,(char*)dados->payload+iniciar,número);return número;}
static err_t aceitar_conexão(struct pbuf *dados,struct netif *celular_VALOR){(void)celular_VALOR;assert(dados->len==60);assert(((unsigned char*)dados->payload)[0]==0x42);recebida_CONT_NÚM++;pbuf_free(dados);return ERR_OK;}
int main(void){
    struct netif celular_VALOR;memset(&celular_VALOR,0,sizeof(celular_VALOR));celular_VALOR.input=aceitar_conexão;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Preparar_com_fio_rede(&celular_VALOR)==ERR_OK);assert(com_fio_VALOR.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&celular_VALOR);assert(netif_is_link_up(&celular_VALOR));assert(com_fio_VALOR.속도==1000);
    com_fio_VALOR.생산=com_fio_VALOR.consumir_VALOR=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagrama=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagrama->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(enviar_datagrama(&celular_VALOR,datagrama)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=com_fio_VALOR.생산;}
    assert(com_fio_VALOR.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(com_fio_VALOR.enviar[0][0]==0x42&&com_fio_VALOR.enviar[0][59]==0);pbuf_free(datagrama);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(com_fio_VALOR.생산-255)&65535;datagrama=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(enviar_datagrama(&celular_VALOR,datagrama)==ERR_MEM);pbuf_free(datagrama);
    memset(com_fio_VALOR.receber[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&celular_VALOR);assert(recebida_CONT_NÚM==1&&com_fio_VALOR.consumir_VALOR==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&celular_VALOR);
    assert(com_fio_VALOR.consumir_VALOR==0&&recebida_CONT_NÚM==1&&com_fio_VALOR.Estatísticas_VALOR[4]==1);
    물리값[1]=0;carimbo_de_data_hora_VALOR+=1000;유선망살피기(&celular_VALOR);assert(!netif_is_link_up(&celular_VALOR));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
