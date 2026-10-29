#include "예제규약.h"
#include <rete_ABI.h>
int main(int argomento_CONTA_NUMERI,char **argomenti) {
    if(argomento_CONTA_NUMERI!=2)return uscitaTesto("사용법: ./네트워크 UDP창구번호\n");
    unsigned porta_VALORE=0;for(int numero=0;argomenti[1][numero];numero++) {
        if(argomenti[1][numero]<'0'||argomenti[1][numero]>'9')return 2;
        porta_VALORE=porta_VALORE*10+argomenti[1][numero]-'0';if(porta_VALORE>65535)return 2;
    }
    if(!porta_VALORE)return 2;
    int endpoint=Crea_endpoint(cloud_serie,socket_di_datagramma,datagramma_protocollo);if(endpoint<0)return 3;
    struct cloud_socket_e_mail e_mail={0};e_mail.e_mail_serie=cloud_serie;
    if(BIND_e_mail(endpoint,(struct socket_e_mail *)&e_mail,sizeof(e_mail))<0)return 4;
    e_mail.numero_di_porta=망차례짧은수(porta_VALORE);e_mail.indirizzo_Internet.e_mail_VALORE=rete_intero(0x0a000202);
    const char datagramma[]="C UDP Italiano";
    if(inviare_datagramma_dati(endpoint,datagramma,sizeof(datagramma)-1,0,(struct socket_e_mail *)&e_mail,sizeof(e_mail))!=sizeof(datagramma)-1)return 5;
    char replica[512];unsigned avvia=밀리초();int RICEV_SCAD_CONTA_NUMERI;
    do {
        RICEV_SCAD_CONTA_NUMERI=ricevere_datagramma_dati(endpoint,replica,sizeof(replica),0,0,0);
        if(RICEV_SCAD_CONTA_NUMERI<0&&numero_errore!=다시시도오류)return 6;
    } while(RICEV_SCAD_CONTA_NUMERI<0&&(unsigned)(밀리초()-avvia)<700);
    Chiudi_File(endpoint);if(RICEV_SCAD_CONTA_NUMERI!=sizeof(datagramma)-1)return 7;
    for(int numero=0;numero<RICEV_SCAD_CONTA_NUMERI;numero++)if(datagramma[numero]!=replica[numero])return 8;
    return uscitaTesto("C 네트워크 verificare: UDP Italiano\n");
}
