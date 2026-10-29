#include "예제규약.h"
#include <통신규약.h>
int main(int arg_ZENBATU,char **Argumentuak) {
    if(arg_ZENBATU!=2)return Irteera("사용법: ./네트워크 UDP창구번호\n");
    unsigned ataka_balio=0;for(int 수=0;Argumentuak[1][수];수++) {
        if(Argumentuak[1][수]<'0'||Argumentuak[1][수]>'9')return 2;
        ataka_balio=ataka_balio*10+Argumentuak[1][수]-'0';if(ataka_balio>65535)return 2;
    }
    if(!ataka_balio)return 2;
    int amaiera_puntu=sortu_amaiera_puntu(hodei_sorta,전문통신,전문전송규약);if(amaiera_puntu<0)return 3;
    struct 인터넷통신주소 helbide={0};helbide.helbide_sorta=hodei_sorta;
    if(lotu_helbide(amaiera_puntu,(struct 통신주소 *)&helbide,sizeof(helbide))<0)return 4;
    helbide.ataka_zenbaki=망차례짧은수(ataka_balio);helbide.Internet_helbide.helbide_balio=sare_osoko_zenbaki(0x0a000202);
    const char 전문[]="C UDP eu";
    if(자료전문보내기(amaiera_puntu,전문,sizeof(전문)-1,0,(struct 통신주소 *)&helbide,sizeof(helbide))!=sizeof(전문)-1)return 5;
    char erantzun[512];unsigned Exekutatu_2=밀리초();int RECEIVED_ZENBATU;
    do {
        RECEIVED_ZENBATU=자료전문받기(amaiera_puntu,erantzun,sizeof(erantzun),0,0,0);
        if(RECEIVED_ZENBATU<0&&errorearen_zenbaki!=다시시도오류)return 6;
    } while(RECEIVED_ZENBATU<0&&(unsigned)(밀리초()-Exekutatu_2)<700);
    itxi_fitxategi(amaiera_puntu);if(RECEIVED_ZENBATU!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_ZENBATU;수++)if(전문[수]!=erantzun[수])return 8;
    return Irteera("C 네트워크 egiaztatu: UDP eu\n");
}
