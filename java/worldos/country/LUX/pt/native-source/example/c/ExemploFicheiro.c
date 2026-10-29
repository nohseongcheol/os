#include "예제규약.h"
int main(void) {
    const char dados[]="C ficheiro: pt 😀\n";
    int ficheiro=abrir_Arquivo("c.txt",de_leitura_gravação|없으면만들기|cortar_Sumário,0600);
    if(ficheiro<0)return 1;
    if(gravar_Arquivo_dados(ficheiro,dados,sizeof(dados)-1)!=sizeof(dados)-1)return 2;
    if(busca_Arquivo(ficheiro,0,처음기준)!=0)return 3;
    char leitura_SMS_VALOR[128]={0};int duração_VALOR=leitura_Arquivo_dados(ficheiro,leitura_SMS_VALOR,sizeof(leitura_SMS_VALOR)-1);
    Close_Arquivo(ficheiro);
    if(duração_VALOR!=sizeof(dados)-1)return 4;
    for(int número=0;número<duração_VALOR;número++)if(dados[número]!=leitura_SMS_VALOR[número])return 5;
    return saídaTexto(leitura_SMS_VALOR);
}
