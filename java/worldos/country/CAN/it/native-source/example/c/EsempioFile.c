#include "예제규약.h"
int main(void) {
    const char dati[]="C file: it 😀\n";
    int file=aperto_File("c.txt",in_lettura_scrittura|없으면만들기|tagliare_Sommario,0600);
    if(file<0)return 1;
    if(scrivere_File_dati(file,dati,sizeof(dati)-1)!=sizeof(dati)-1)return 2;
    if(cercare_File(file,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int durata_VALORE=파일자료읽기(file,읽은글,sizeof(읽은글)-1);
    Chiudi_File(file);
    if(durata_VALORE!=sizeof(dati)-1)return 4;
    for(int numero=0;numero<durata_VALORE;numero++)if(dati[numero]!=읽은글[numero])return 5;
    return uscitaTesto(읽은글);
}
