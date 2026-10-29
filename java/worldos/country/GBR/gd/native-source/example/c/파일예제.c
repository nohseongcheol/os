#include "예제규약.h"
int main(void) {
    const char dàta[]="C faidhle: gd 😀\n";
    int faidhle=fosgail_faidhle("c.txt",so_leughte_so_sgrìobhte|없으면만들기|내용비우기,0600);
    if(faidhle<0)return 1;
    if(sgrìobh_faidhle_dàta(faidhle,dàta,sizeof(dàta)-1)!=sizeof(dàta)-1)return 2;
    if(sir_faidhle(faidhle,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int faid_VALUE=파일자료읽기(faidhle,읽은글,sizeof(읽은글)-1);
    dùin_faidhle(faidhle);
    if(faid_VALUE!=sizeof(dàta)-1)return 4;
    for(int 수=0;수<faid_VALUE;수++)if(dàta[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
