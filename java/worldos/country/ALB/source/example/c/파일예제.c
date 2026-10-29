#include "예제규약.h"
int main(void) {
    const char të_dhëna[]="C Kartelë: Albanian 😀\n";
    int Kartelë=hap_skedar("c.txt",lexoj_shkruaj|없으면만들기|내용비우기,0600);
    if(Kartelë<0)return 1;
    if(shkruaj_skedar_të_dhëna(Kartelë,të_dhëna,sizeof(të_dhëna)-1)!=sizeof(të_dhëna)-1)return 2;
    if(kërko_skedar(Kartelë,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int gjatësi_VALUE=파일자료읽기(Kartelë,읽은글,sizeof(읽은글)-1);
    mbyll_skedar(Kartelë);
    if(gjatësi_VALUE!=sizeof(të_dhëna)-1)return 4;
    for(int 수=0;수<gjatësi_VALUE;수++)if(të_dhëna[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
