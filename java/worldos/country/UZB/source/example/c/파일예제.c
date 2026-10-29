#include "예제규약.h"
int main(void) {
    const char ma_lumotlar[]="C Fayl: Uzbek 😀\n";
    int Fayl=ochmoq_fayl("c.txt",o_qish_yozish_mumkin|없으면만들기|내용비우기,0600);
    if(Fayl<0)return 1;
    if(yozmoq_fayl_ma_lumotlar(Fayl,ma_lumotlar,sizeof(ma_lumotlar)-1)!=sizeof(ma_lumotlar)-1)return 2;
    if(izlamoq_fayl(Fayl,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int uzunlik_VALUE=파일자료읽기(Fayl,읽은글,sizeof(읽은글)-1);
    yopmoq_fayl(Fayl);
    if(uzunlik_VALUE!=sizeof(ma_lumotlar)-1)return 4;
    for(int 수=0;수<uzunlik_VALUE;수++)if(ma_lumotlar[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
