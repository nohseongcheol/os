/* 가짜 MMIO/MDIO 장치로 valorBucle valorDesbordamiento·longitud·링크 전환을 검사한다. equipoFísicoFísico 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registroProcesador[0x10000/4];
#define registrosCableado(dirección) registroProcesador[(dirección)/4]
#define JKOROS_GENET_TEST 1
#include "../PilaRed/redCableado.c"
static uintptr_t valorMarcaTiempo;
static int operaciónFísico=1,equipoFísicoFísico=1,númeroElementosEntrando;
static unsigned short valorFísico[32];
uintptr_t milisegundosTranscurridosPlaca(void){
    uint32_t textoPalabra=registrosCableado(0xe14);
    if(operaciónFísico&&(textoPalabra&(1u<<29))){unsigned dirección=(textoPalabra>>21)&31,número=(textoPalabra>>16)&31;
        if(dirección!=1)registrosCableado(0xe14)=1<<28;
        else{if(((textoPalabra>>26)&3)==1)valorFísico[número]=textoPalabra&65535;registrosCableado(0xe14)=valorFísico[número];}}
    return valorMarcaTiempo++;
}
int equipoFísicoFísicoPlaca(void){return equipoFísicoFísico;}
int direcciónMáquinaPlaca(unsigned char *dirección){const unsigned char valor[]={2,1,2,3,4,5};memcpy(dirección,valor,6);return 1;}
void netif_set_link_up(struct netif *Dispositivo){Dispositivo->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *Dispositivo){Dispositivo->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *Dispositivo,struct pbuf *datagrama,const ip4_addr_t *dirección){(void)Dispositivo;(void)datagrama;(void)dirección;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer índiceCapa,u16_t númeroValor,pbuf_type valorClaseTipo){
    (void)índiceCapa;(void)valorClaseTipo;struct pbuf *Datos=calloc(1,sizeof(*Datos)+númeroValor);assert(Datos);Datos->payload=Datos+1;Datos->len=Datos->tot_len=númeroValor;return Datos;
}
u8_t pbuf_free(struct pbuf *Datos){free(Datos);return 1;}
err_t pbuf_take(struct pbuf *Datos,const void *original,u16_t númeroValor){assert(númeroValor<=Datos->len);memcpy(Datos->payload,original,númeroValor);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *Datos,void *valorDestino,u16_t númeroValor,u16_t ponerEnMarcha){assert(ponerEnMarcha+númeroValor<=Datos->len);memcpy(valorDestino,(char*)Datos->payload+ponerEnMarcha,númeroValor);return númeroValor;}
static err_t aceptarConexión(struct pbuf *Datos,struct netif *Dispositivo){(void)Dispositivo;assert(Datos->len==60);assert(((unsigned char*)Datos->payload)[0]==0x42);númeroElementosEntrando++;pbuf_free(Datos);return ERR_OK;}
int main(void){
    struct netif Dispositivo;memset(&Dispositivo,0,sizeof(Dispositivo));Dispositivo.input=aceptarConexión;
    registrosCableado(0)=6u<<24;valorFísico[2]=0x600d;valorFísico[1]=4;valorFísico[25]=7<<8;
    equipoFísicoFísico=0;assert(!tieneDispositivoCableado());equipoFísicoFísico=1;assert(tieneDispositivoCableado());
    
    assert(prepararRedCableado(&Dispositivo)==ERR_OK);assert(valorCableado.direcciónFísico==1);
    assert(registrosCableado(GENET_RX_DMA_CTRL)==0x20001&&registrosCableado(GENET_TX_DMA_CTRL)==0x20001);
    assert(registrosCableado(0x80c)==0x02010203&&registrosCableado(0x810)==0x0405);
    inspeccionarRedCableado(&Dispositivo);assert(netif_is_link_up(&Dispositivo));assert(valorCableado.valorVelocidad==1000);
    valorCableado.valorProducir=valorCableado.consumirValor=65534;registrosCableado(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagrama=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagrama->payload,0x42,40);
    for(unsigned índiceOrdinal=0;índiceOrdinal<3;índiceOrdinal++){assert(enviarDatagrama(&Dispositivo,datagrama)==ERR_OK);registrosCableado(GENET_TX_DMA_CONS_INDEX(16))=valorCableado.valorProducir;}
    assert(valorCableado.valorProducir==1);assert((registrosCableado(0x4000)>>16)==60);assert(valorCableado.enviar[0][0]==0x42&&valorCableado.enviar[0][59]==0);pbuf_free(datagrama);
    registrosCableado(GENET_TX_DMA_CONS_INDEX(16))=(valorCableado.valorProducir-255)&65535;datagrama=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(enviarDatagrama(&Dispositivo,datagrama)==ERR_MEM);pbuf_free(datagrama);
    memset(valorCableado.recibir[254],0x42,64);registrosCableado(0x2000+254*12)=(62<<16)|0x6000;registrosCableado(GENET_RX_DMA_PROD_INDEX(16))=65535;
    inspeccionarRedCableado(&Dispositivo);assert(númeroElementosEntrando==1&&valorCableado.consumirValor==65535);
    registrosCableado(0x2000+255*12)=(4095u<<16)|0x6000;registrosCableado(GENET_RX_DMA_PROD_INDEX(16))=0;inspeccionarRedCableado(&Dispositivo);
    assert(valorCableado.consumirValor==0&&númeroElementosEntrando==1&&valorCableado.valorEstadísticas[4]==1);
    valorFísico[1]=0;valorMarcaTiempo+=1000;inspeccionarRedCableado(&Dispositivo);assert(!netif_is_link_up(&Dispositivo));
    operaciónFísico=0;assert(transferenciaFísico(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
