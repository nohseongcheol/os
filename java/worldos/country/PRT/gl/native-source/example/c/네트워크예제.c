#include "예제규약.h"
#include <통신규약.h>
int main(int argumento_CONTAR,char **Argumentos) {
    if(argumento_CONTAR!=2)return Saída("사용법: ./네트워크 UDP창구번호\n");
    unsigned porto_VALOR=0;for(int 수=0;Argumentos[1][수];수++) {
        if(Argumentos[1][수]<'0'||Argumentos[1][수]>'9')return 2;
        porto_VALOR=porto_VALOR*10+Argumentos[1][수]-'0';if(porto_VALOR>65535)return 2;
    }
    if(!porto_VALOR)return 2;
    int extremo=crear_extremo(nube_Familia,전문통신,전문전송규약);if(extremo<0)return 3;
    struct 인터넷통신주소 ENDEREZO={0};ENDEREZO.ENDEREZO_Familia=nube_Familia;
    if(ligar_ENDEREZO(extremo,(struct 통신주소 *)&ENDEREZO,sizeof(ENDEREZO))<0)return 4;
    ENDEREZO.número_do_porto=망차례짧은수(porto_VALOR);ENDEREZO.enderezo_de_internet.ENDEREZO_VALOR=Rede_número_enteiro(0x0a000202);
    const char 전문[]="C UDP gl";
    if(자료전문보내기(extremo,전문,sizeof(전문)-1,0,(struct 통신주소 *)&ENDEREZO,sizeof(ENDEREZO))!=sizeof(전문)-1)return 5;
    char resposta[512];unsigned Executar_2=밀리초();int RECIBIDO_CONTAR;
    do {
        RECIBIDO_CONTAR=자료전문받기(extremo,resposta,sizeof(resposta),0,0,0);
        if(RECIBIDO_CONTAR<0&&número_de_erro!=다시시도오류)return 6;
    } while(RECIBIDO_CONTAR<0&&(unsigned)(밀리초()-Executar_2)<700);
    peche_Ficheiro(extremo);if(RECIBIDO_CONTAR!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECIBIDO_CONTAR;수++)if(전문[수]!=resposta[수])return 8;
    return Saída("C 네트워크 verificar: UDP gl\n");
}
