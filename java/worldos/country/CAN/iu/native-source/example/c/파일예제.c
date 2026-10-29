#include "예제규약.h"
int main(void) {
    const char titiqqat[]="C ini: iu 😀\n";
    int ini=matuirli_ini("c.txt",uqalimaarli_titirarli|없으면만들기|내용비우기,0600);
    if(ini<0)return 1;
    if(titiraq_ini_titiqqat(ini,titiqqat,sizeof(titiqqat)-1)!=sizeof(titiqqat)-1)return 2;
    if(qinirli_ini(ini,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int takininga_atuutilik=파일자료읽기(ini,읽은글,sizeof(읽은글)-1);
    matuli_ini(ini);
    if(takininga_atuutilik!=sizeof(titiqqat)-1)return 4;
    for(int 수=0;수<takininga_atuutilik;수++)if(titiqqat[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
