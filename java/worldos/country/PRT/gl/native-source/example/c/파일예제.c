#include "예제규약.h"
int main(void) {
    const char datos[]="C Ficheiro: gl 😀\n";
    int Ficheiro=abrir_Ficheiro("c.txt",de_lectura_e_escrita|없으면만들기|내용비우기,0600);
    if(Ficheiro<0)return 1;
    if(escribir_Ficheiro_datos(Ficheiro,datos,sizeof(datos)-1)!=sizeof(datos)-1)return 2;
    if(buscar_Ficheiro(Ficheiro,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int duración_VALOR=파일자료읽기(Ficheiro,읽은글,sizeof(읽은글)-1);
    peche_Ficheiro(Ficheiro);
    if(duración_VALOR!=sizeof(datos)-1)return 4;
    for(int 수=0;수<duración_VALOR;수++)if(datos[수]!=읽은글[수])return 5;
    return Saída(읽은글);
}
