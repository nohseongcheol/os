#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "verkko_Pino.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int ulkoinen[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_ulkoinen_vertaissolmu[8], raja_OSOITE[8];
static int ulkoinen_numero(int Tiedosto_kahva) { return Tiedosto_kahva>=32 && Tiedosto_kahva<56 ? ulkoinen[Tiedosto_kahva-32]-1 : -1; }
static int liitä_SMS_ea0cc186(int Tiedosto_kahva,int TYYPPI_alue) {
    if(Tiedosto_kahva<32||Tiedosto_kahva>=56)return -9;int Edellinen_kohde=ulkoinen_numero(Tiedosto_kahva);if(Edellinen_kohde>=0)return Edellinen_kohde;
    int kohde_LASKE=Luo_vastake_päätepiste(TYYPPI_alue);if(kohde_LASKE>=0)ulkoinen[Tiedosto_kahva-32]=kohde_LASKE+1;return kohde_LASKE;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEKUNNIT_ARVO,int32_t merkkikoodi){return 되돌림전문만들기(첫째값,SEKUNNIT_ARVO,merkkikoodi);}
int32_t 자바전문묶기(int32_t Tiedosto_kahva,int32_t Internet_osoite,int32_t portin_numero){
    if(Internet_osoite==0x7f000001)return 되돌림전문묶기(Tiedosto_kahva,Internet_osoite,portin_numero);
    if(Internet_osoite!=0&&Internet_osoite!=lukea_verkko_tila(0,0))return -99;
    int 반환값=되돌림전문묶기(Tiedosto_kahva,0,portin_numero);if(반환값<0)return 반환값;
    int kohde_LASKE=liitä_SMS_ea0cc186(Tiedosto_kahva,2);if(kohde_LASKE<0)return kohde_LASKE;반환값=NET_BIND(kohde_LASKE,lukea_verkko_tila(0,0),되돌림전문접속번호(Tiedosto_kahva));if(!반환값)raja_OSOITE[Tiedosto_kahva-32]=Internet_osoite;return 반환값;
}
int32_t 자바전문보내기(int32_t Tiedosto_kahva,int32_t Internet_osoite,int32_t portin_numero,int32_t Koko){
    if(Internet_osoite==0x7f000001)return 되돌림전문보내기(Tiedosto_kahva,Internet_osoite,portin_numero,Koko);
    if(Koko<0||Koko>512)return -90;if(portin_numero<1||portin_numero>65535)return -22;
    if(되돌림전문접속번호(Tiedosto_kahva)<0)return -9;
    if(되돌림전문주소(Tiedosto_kahva)==0x7f000001)return -101;
    int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE<0){int 반환값=0;if(되돌림전문접속번호(Tiedosto_kahva)==0)반환값=되돌림전문묶기(Tiedosto_kahva,0,0);if(반환값<0)return 반환값;kohde_LASKE=liitä_SMS_ea0cc186(Tiedosto_kahva,2);if(kohde_LASKE<0)return kohde_LASKE;반환값=NET_BIND(kohde_LASKE,lukea_verkko_tila(0,0),되돌림전문접속번호(Tiedosto_kahva));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Koko;순번++)data[순번]=자바전문얻기(순번);return lähettää_datagrammi(kohde_LASKE,data,Koko,Internet_osoite,portin_numero);
}
int32_t 자바전문받기(int32_t Tiedosto_kahva,int32_t Koko){
    int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE<0)return 되돌림전문받기(Tiedosto_kahva,Koko);if(Koko<0||Koko>512)return -22;
    int paikallinen=되돌림전문받기(Tiedosto_kahva,Koko);if(paikallinen!=-11){UDP_ulkoinen_vertaissolmu[Tiedosto_kahva-32]=0;return paikallinen;}
    unsigned char data[512];int 반환값=saada_datagrammi(kohde_LASKE,data,Koko);if(반환값>=0)UDP_ulkoinen_vertaissolmu[Tiedosto_kahva-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Tiedosto_kahva){int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);return kohde_LASKE<0?되돌림전문접속번호(Tiedosto_kahva):(int32_t)verkko_portin_numero(kohde_LASKE);}
int32_t 자바전문주소(int32_t Tiedosto_kahva){return ulkoinen_numero(Tiedosto_kahva)<0?되돌림전문주소(Tiedosto_kahva):raja_OSOITE[Tiedosto_kahva-32];}
int32_t 자바전문상대(int32_t Tiedosto_kahva){int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);return kohde_LASKE<0||!UDP_ulkoinen_vertaissolmu[Tiedosto_kahva-32]?되돌림전문상대(Tiedosto_kahva):(int32_t)vertaissolmu_portin_numero(kohde_LASKE);}
int32_t 자바전문원격주소(int32_t Tiedosto_kahva){int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);return kohde_LASKE<0||!UDP_ulkoinen_vertaissolmu[Tiedosto_kahva-32]?0x7f000001:(int32_t)NET_vertaissolmu_OSOITE(kohde_LASKE);}
int32_t 자바전문닫기(int32_t Tiedosto_kahva){int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE>=0){Sulje_verkko(kohde_LASKE);ulkoinen[Tiedosto_kahva-32]=0;}if(Tiedosto_kahva>=32&&Tiedosto_kahva<40)UDP_ulkoinen_vertaissolmu[Tiedosto_kahva-32]=raja_OSOITE[Tiedosto_kahva-32]=0;return 되돌림전문닫기(Tiedosto_kahva);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Tiedosto_kahva,int32_t Internet_osoite,int32_t portin_numero){
    if(Internet_osoite==0||Internet_osoite==0x7f000001){int 반환값=되돌림흐름묶기(Tiedosto_kahva,Internet_osoite,portin_numero);if(!반환값)임의주소[Tiedosto_kahva-32]=Internet_osoite==0;return 반환값;}
    if(Internet_osoite!=lukea_verkko_tila(0,0))return -99;int 반환값=되돌림흐름묶기(Tiedosto_kahva,0,portin_numero);if(반환값<0)return 반환값;
    int kohde_LASKE=liitä_SMS_ea0cc186(Tiedosto_kahva,1);return kohde_LASKE<0?kohde_LASKE:NET_BIND(kohde_LASKE,Internet_osoite,되돌림흐름접속번호(Tiedosto_kahva));
}
int32_t 자바흐름듣기(int32_t Tiedosto_kahva,int32_t keskeneräiset_työt){
    int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE<0){int 반환값=되돌림흐름듣기(Tiedosto_kahva,keskeneräiset_työt);if(반환값<0||!임의주소[Tiedosto_kahva-32])return 반환값;
        kohde_LASKE=liitä_SMS_ea0cc186(Tiedosto_kahva,1);if(kohde_LASKE<0)return kohde_LASKE;반환값=NET_BIND(kohde_LASKE,lukea_verkko_tila(0,0),되돌림흐름접속번호(Tiedosto_kahva));if(반환값<0)return 반환값;양쪽수신창구[Tiedosto_kahva-32]=1;
    }return keskeneräiset_työt<1?-22:NET_kuunnella(kohde_LASKE);
}
int32_t 자바흐름연결(int32_t Tiedosto_kahva,int32_t Internet_osoite,int32_t portin_numero){
    if(Internet_osoite==0x7f000001 && ulkoinen_numero(Tiedosto_kahva)<0)return 되돌림흐름연결(Tiedosto_kahva,Internet_osoite,portin_numero);
    if(되돌림흐름접속번호(Tiedosto_kahva)<0)return -9;int kohde_LASKE=liitä_SMS_ea0cc186(Tiedosto_kahva,1);return kohde_LASKE<0?kohde_LASKE:NET_YHDISTÄ(kohde_LASKE,Internet_osoite,portin_numero);
}
int32_t 자바흐름연결받기(int32_t Tiedosto_kahva){
    int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE<0)return 되돌림흐름연결받기(Tiedosto_kahva);
    if(양쪽수신창구[Tiedosto_kahva-32]){int paikallinen=되돌림흐름연결받기(Tiedosto_kahva);if(paikallinen!=-11)return paikallinen;}
    int vertaissolmu_ARVO=NET_hyväksyä(kohde_LASKE);if(vertaissolmu_ARVO<0)return vertaissolmu_ARVO;
    int tavoite=되돌림흐름만들기();if(tavoite<0){Sulje_verkko(vertaissolmu_ARVO);return tavoite;}ulkoinen[tavoite-32]=vertaissolmu_ARVO+1;return tavoite;
}
int32_t 자바흐름읽기(int32_t Tiedosto_kahva,int32_t Koko){
    int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE<0)return 되돌림흐름읽기(Tiedosto_kahva,Koko);if(Koko<0||Koko>512)return -22;
    unsigned char data[512];int 반환값=NET_lukea(kohde_LASKE,data,Koko);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Tiedosto_kahva,int32_t Koko){
    int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE<0)return 되돌림흐름쓰기(Tiedosto_kahva,Koko);if(Koko<0||Koko>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Koko;순번++)data[순번]=자바전문얻기(순번);return NET_kirjoitus(kohde_LASKE,data,Koko);
}
int32_t 자바흐름접속번호(int32_t Tiedosto_kahva){int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);return kohde_LASKE<0?되돌림흐름접속번호(Tiedosto_kahva):(int32_t)verkko_portin_numero(kohde_LASKE);}
int32_t 자바흐름상대(int32_t Tiedosto_kahva){int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);return kohde_LASKE<0?되돌림흐름상대(Tiedosto_kahva):(int32_t)vertaissolmu_portin_numero(kohde_LASKE);}
int32_t 자바흐름주소(int32_t Tiedosto_kahva){return ulkoinen_numero(Tiedosto_kahva)<0?0x7f000001:양쪽수신창구[Tiedosto_kahva-32]?0:lukea_verkko_tila(0,0);}
int32_t 자바흐름닫기(int32_t Tiedosto_kahva){int kohde_LASKE=ulkoinen_numero(Tiedosto_kahva);if(kohde_LASKE>=0){Sulje_verkko(kohde_LASKE);ulkoinen[Tiedosto_kahva-32]=0;}if(Tiedosto_kahva>=40&&Tiedosto_kahva<56)임의주소[Tiedosto_kahva-32]=양쪽수신창구[Tiedosto_kahva-32]=0;return 되돌림흐름닫기(Tiedosto_kahva);}
