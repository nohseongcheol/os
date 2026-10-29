#include "예제규약.h"
#include <통신규약.h>
int main(int arg_COMPT,char **인수) {
    if(arg_COMPT!=2)return Sortida("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALOR=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        port_VALOR=port_VALOR*10+인수[1][수]-'0';if(port_VALOR>65535)return 2;
    }
    if(!port_VALOR)return 2;
    int extrem=Crear_extrem(núvol_Família,전문통신,전문전송규약);if(extrem<0)return 3;
    struct 인터넷통신주소 Adreça={0};Adreça.ADREÇA_Família=núvol_Família;
    if(enllaçar_ADREÇA(extrem,(struct 통신주소 *)&Adreça,sizeof(Adreça))<0)return 4;
    Adreça.número_de_port=망차례짧은수(port_VALOR);Adreça.adreça_d_Internet.ADREÇA_VALOR=망차례정수(0x0a000202);
    const char 전문[]="C UDP ca";
    if(자료전문보내기(extrem,전문,sizeof(전문)-1,0,(struct 통신주소 *)&Adreça,sizeof(Adreça))!=sizeof(전문)-1)return 5;
    char resposta[512];unsigned Executa_2=밀리초();int CANTIDAD_RECIBIDA_COMPT;
    do {
        CANTIDAD_RECIBIDA_COMPT=자료전문받기(extrem,resposta,sizeof(resposta),0,0,0);
        if(CANTIDAD_RECIBIDA_COMPT<0&&número_d_error!=다시시도오류)return 6;
    } while(CANTIDAD_RECIBIDA_COMPT<0&&(unsigned)(밀리초()-Executa_2)<700);
    Tanca_arxiu(extrem);if(CANTIDAD_RECIBIDA_COMPT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<CANTIDAD_RECIBIDA_COMPT;수++)if(전문[수]!=resposta[수])return 8;
    return Sortida("C 네트워크 verificar: UDP ca\n");
}
