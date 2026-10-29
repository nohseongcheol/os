#include "예제규약.h"
int main(void) {
    const char dades[]="C Fitxer: Català 😀\n";
    int Fitxer=crear_arxiu("c.txt",lectura_escriptura|없으면만들기|내용비우기,0600);
    if(Fitxer<0)return 1;
    if(escriure_arxiu_dades(Fitxer,dades,sizeof(dades)-1)!=sizeof(dades)-1)return 2;
    if(cercar_arxiu(Fitxer,0,처음기준)!=0)return 3;
    char tancar_SMS_VALOR[128]={0};int durada_VALOR=tancar_arxiu_dades(Fitxer,tancar_SMS_VALOR,sizeof(tancar_SMS_VALOR)-1);
    Tanca_arxiu(Fitxer);
    if(durada_VALOR!=sizeof(dades)-1)return 4;
    for(int 수=0;수<durada_VALOR;수++)if(dades[수]!=tancar_SMS_VALOR[수])return 5;
    return Sortida(tancar_SMS_VALOR);
}
