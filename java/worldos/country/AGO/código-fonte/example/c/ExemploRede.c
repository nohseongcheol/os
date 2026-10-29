#include "예제규약.h"
#include <rede_ABI.h>
int main(int argumento_CONT_NÚM,char **argumentos) {
    if(argumento_CONT_NÚM!=2)return saídaTexto("사용법: ./네트워크 UDP창구번호\n");
    unsigned porta_VALOR=0;for(int número=0;argumentos[1][número];número++) {
        if(argumentos[1][número]<'0'||argumentos[1][número]>'9')return 2;
        porta_VALOR=porta_VALOR*10+argumentos[1][número]-'0';if(porta_VALOR>65535)return 2;
    }
    if(!porta_VALOR)return 2;
    int empresa=Criar_empresa(malha_Família,datagrama_soquete,datagrama_protocolo);if(empresa<0)return 3;
    struct malha_soquete_email Endereço={0};Endereço.email_Família=malha_Família;
    if(BIND_email(empresa,(struct soquete_email *)&Endereço,sizeof(Endereço))<0)return 4;
    Endereço.número_da_porta=망차례짧은수(porta_VALOR);Endereço.endereço_na_Internet.email_VALOR=rede_inteiro(0x0a000202);
    const char datagrama[]="C UDP Português";
    if(enviar_datagrama_dados(empresa,datagrama,sizeof(datagrama)-1,0,(struct soquete_email *)&Endereço,sizeof(Endereço))!=sizeof(datagrama)-1)return 5;
    char resposta[512];unsigned iniciar=밀리초();int RECEBER_CONT_NÚM;
    do {
        RECEBER_CONT_NÚM=receber_datagrama_dados(empresa,resposta,sizeof(resposta),0,0,0);
        if(RECEBER_CONT_NÚM<0&&número_do_erro!=다시시도오류)return 6;
    } while(RECEBER_CONT_NÚM<0&&(unsigned)(밀리초()-iniciar)<700);
    Close_Arquivo(empresa);if(RECEBER_CONT_NÚM!=sizeof(datagrama)-1)return 7;
    for(int número=0;número<RECEBER_CONT_NÚM;número++)if(datagrama[número]!=resposta[número])return 8;
    return saídaTexto("C 네트워크 verificar: UDP Português\n");
}
