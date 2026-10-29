/* 가짜 MMIO/MDIO 장치로 Loop_VALOR 넘침·duración_VALOR·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t rexistrarse_VALOR[0x10000/4];
#define 유선저장기(ENDEREZO) rexistrarse_VALOR[(ENDEREZO)/4]
#define JKOROS_GENET_TEST 1
#include "../Rede_Montón/con_fíos_Rede.c"
static uintptr_t marca_de_hora_VALOR;
static int 물리작동=1,실물=1,Entrante_CONTAR;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned ENDEREZO=(Word_SMS>>21)&31,ÍNDICE=(Word_SMS>>16)&31;
        if(ENDEREZO!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[ÍNDICE]=Word_SMS&65535;유선저장기(0xe14)=물리값[ÍNDICE];}}
    return marca_de_hora_VALOR++;
}
int 보드실물(void){return 실물;}
int Panel_máquina_ENDEREZO(unsigned char *ENDEREZO){const unsigned char VALOR[]={2,1,2,3,4,5};memcpy(ENDEREZO,VALOR,6);return 1;}
void netif_set_link_up(struct netif *dispositivo_VALOR){dispositivo_VALOR->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *dispositivo_VALOR){dispositivo_VALOR->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *dispositivo_VALOR,struct pbuf *전문,const ip4_addr_t *ENDEREZO){(void)dispositivo_VALOR;(void)전문;(void)ENDEREZO;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer capa_ÍNDICE,u16_t 수,pbuf_type 종류){
    (void)capa_ÍNDICE;(void)종류;struct pbuf *datos=calloc(1,sizeof(*datos)+수);assert(datos);datos->payload=datos+1;datos->len=datos->tot_len=수;return datos;
}
u8_t pbuf_free(struct pbuf *datos){free(datos);return 1;}
err_t pbuf_take(struct pbuf *datos,const void *원본,u16_t 수){assert(수<=datos->len);memcpy(datos->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *datos,void *destino_VALOR,u16_t 수,u16_t Executar_2){assert(Executar_2+수<=datos->len);memcpy(destino_VALOR,(char*)datos->payload+Executar_2,수);return 수;}
static err_t aceptar_conexión(struct pbuf *datos,struct netif *dispositivo_VALOR){(void)dispositivo_VALOR;assert(datos->len==60);assert(((unsigned char*)datos->payload)[0]==0x42);Entrante_CONTAR++;pbuf_free(datos);return ERR_OK;}
int main(void){
    struct netif dispositivo_VALOR;memset(&dispositivo_VALOR,0,sizeof(dispositivo_VALOR));dispositivo_VALOR.input=aceptar_conexión;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(유선망준비(&dispositivo_VALOR)==ERR_OK);assert(con_fíos_VALOR.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&dispositivo_VALOR);assert(netif_is_link_up(&dispositivo_VALOR));assert(con_fíos_VALOR.속도==1000);
    con_fíos_VALOR.생산=con_fíos_VALOR.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&dispositivo_VALOR,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=con_fíos_VALOR.생산;}
    assert(con_fíos_VALOR.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(con_fíos_VALOR.enviar[0][0]==0x42&&con_fíos_VALOR.enviar[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(con_fíos_VALOR.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&dispositivo_VALOR,전문)==ERR_MEM);pbuf_free(전문);
    memset(con_fíos_VALOR.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&dispositivo_VALOR);assert(Entrante_CONTAR==1&&con_fíos_VALOR.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&dispositivo_VALOR);
    assert(con_fíos_VALOR.소비==0&&Entrante_CONTAR==1&&con_fíos_VALOR.집계[4]==1);
    물리값[1]=0;marca_de_hora_VALOR+=1000;유선망살피기(&dispositivo_VALOR);assert(!netif_is_link_up(&dispositivo_VALOR));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
