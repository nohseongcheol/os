#include "예제규약.h"
int main(void) {
    const char Tarin_bayani[]="C Fayil: ha 😀\n";
    int Fayil=buɗe_Fayil("c.txt",Rubutuwa_karantuwa|없으면만들기|내용비우기,0600);
    if(Fayil<0)return 1;
    if(Rubuta_Fayil_Tarin_bayani(Fayil,Tarin_bayani,sizeof(Tarin_bayani)-1)!=sizeof(Tarin_bayani)-1)return 2;
    if(binciko_Fayil(Fayil,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int Tsawo_Daraja=파일자료읽기(Fayil,읽은글,sizeof(읽은글)-1);
    Rufe_Fayil(Fayil);
    if(Tsawo_Daraja!=sizeof(Tarin_bayani)-1)return 4;
    for(int 수=0;수<Tsawo_Daraja;수++)if(Tarin_bayani[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
