#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "tinklas_eilė.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int išorinis[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_išorinis_lygiavertis_mazgas[8], riba_ADDRESS[8];
static int išorinis_numeris(int Failas_rodyklė) { return Failas_rodyklė>=32 && Failas_rodyklė<56 ? išorinis[Failas_rodyklė-32]-1 : -1; }
static int Įklijuoti_SMS(int Failas_rodyklė,int TYPE_sritis) {
    if(Failas_rodyklė<32||Failas_rodyklė>=56)return -9;int 이전=išorinis_numeris(Failas_rodyklė);if(이전>=0)return 이전;
    int prekė_COUNT=통신끝점만들기(TYPE_sritis);if(prekė_COUNT>=0)išorinis[Failas_rodyklė-32]=prekė_COUNT+1;return prekė_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t simbolio_kodas){return 되돌림전문만들기(첫째값,SECOND_VALUE,simbolio_kodas);}
int32_t 자바전문묶기(int32_t Failas_rodyklė,int32_t interneto_adresas,int32_t prievado_numeris){
    if(interneto_adresas==0x7f000001)return 되돌림전문묶기(Failas_rodyklė,interneto_adresas,prievado_numeris);
    if(interneto_adresas!=0&&interneto_adresas!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Failas_rodyklė,0,prievado_numeris);if(반환값<0)return 반환값;
    int prekė_COUNT=Įklijuoti_SMS(Failas_rodyklė,2);if(prekė_COUNT<0)return prekė_COUNT;반환값=NET_BIND(prekė_COUNT,망상태읽기(0,0),되돌림전문접속번호(Failas_rodyklė));if(!반환값)riba_ADDRESS[Failas_rodyklė-32]=interneto_adresas;return 반환값;
}
int32_t 자바전문보내기(int32_t Failas_rodyklė,int32_t interneto_adresas,int32_t prievado_numeris,int32_t Dydis){
    if(interneto_adresas==0x7f000001)return 되돌림전문보내기(Failas_rodyklė,interneto_adresas,prievado_numeris,Dydis);
    if(Dydis<0||Dydis>512)return -90;if(prievado_numeris<1||prievado_numeris>65535)return -22;
    if(되돌림전문접속번호(Failas_rodyklė)<0)return -9;
    if(되돌림전문주소(Failas_rodyklė)==0x7f000001)return -101;
    int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Failas_rodyklė)==0)반환값=되돌림전문묶기(Failas_rodyklė,0,0);if(반환값<0)return 반환값;prekė_COUNT=Įklijuoti_SMS(Failas_rodyklė,2);if(prekė_COUNT<0)return prekė_COUNT;반환값=NET_BIND(prekė_COUNT,망상태읽기(0,0),되돌림전문접속번호(Failas_rodyklė));if(반환값<0)return 반환값;}
    unsigned char duomenys[512];for(int 순번=0;순번<Dydis;순번++)duomenys[순번]=자바전문얻기(순번);return siųsti_paketų_kelio_schema(prekė_COUNT,duomenys,Dydis,interneto_adresas,prievado_numeris);
}
int32_t 자바전문받기(int32_t Failas_rodyklė,int32_t Dydis){
    int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT<0)return 되돌림전문받기(Failas_rodyklė,Dydis);if(Dydis<0||Dydis>512)return -22;
    int vietinis=되돌림전문받기(Failas_rodyklė,Dydis);if(vietinis!=-11){UDP_išorinis_lygiavertis_mazgas[Failas_rodyklė-32]=0;return vietinis;}
    unsigned char duomenys[512];int 반환값=gauti_paketų_kelio_schema(prekė_COUNT,duomenys,Dydis);if(반환값>=0)UDP_išorinis_lygiavertis_mazgas[Failas_rodyklė-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,duomenys[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Failas_rodyklė){int prekė_COUNT=išorinis_numeris(Failas_rodyklė);return prekė_COUNT<0?되돌림전문접속번호(Failas_rodyklė):(int32_t)tinklas_prievado_numeris(prekė_COUNT);}
int32_t 자바전문주소(int32_t Failas_rodyklė){return išorinis_numeris(Failas_rodyklė)<0?되돌림전문주소(Failas_rodyklė):riba_ADDRESS[Failas_rodyklė-32];}
int32_t 자바전문상대(int32_t Failas_rodyklė){int prekė_COUNT=išorinis_numeris(Failas_rodyklė);return prekė_COUNT<0||!UDP_išorinis_lygiavertis_mazgas[Failas_rodyklė-32]?되돌림전문상대(Failas_rodyklė):(int32_t)lygiavertis_mazgas_prievado_numeris(prekė_COUNT);}
int32_t 자바전문원격주소(int32_t Failas_rodyklė){int prekė_COUNT=išorinis_numeris(Failas_rodyklė);return prekė_COUNT<0||!UDP_išorinis_lygiavertis_mazgas[Failas_rodyklė-32]?0x7f000001:(int32_t)NET_lygiavertis_mazgas_ADDRESS(prekė_COUNT);}
int32_t 자바전문닫기(int32_t Failas_rodyklė){int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT>=0){Uždaryti_tinklas(prekė_COUNT);išorinis[Failas_rodyklė-32]=0;}if(Failas_rodyklė>=32&&Failas_rodyklė<40)UDP_išorinis_lygiavertis_mazgas[Failas_rodyklė-32]=riba_ADDRESS[Failas_rodyklė-32]=0;return 되돌림전문닫기(Failas_rodyklė);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Failas_rodyklė,int32_t interneto_adresas,int32_t prievado_numeris){
    if(interneto_adresas==0||interneto_adresas==0x7f000001){int 반환값=되돌림흐름묶기(Failas_rodyklė,interneto_adresas,prievado_numeris);if(!반환값)임의주소[Failas_rodyklė-32]=interneto_adresas==0;return 반환값;}
    if(interneto_adresas!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Failas_rodyklė,0,prievado_numeris);if(반환값<0)return 반환값;
    int prekė_COUNT=Įklijuoti_SMS(Failas_rodyklė,1);return prekė_COUNT<0?prekė_COUNT:NET_BIND(prekė_COUNT,interneto_adresas,되돌림흐름접속번호(Failas_rodyklė));
}
int32_t 자바흐름듣기(int32_t Failas_rodyklė,int32_t 연결대기한도){
    int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT<0){int 반환값=되돌림흐름듣기(Failas_rodyklė,연결대기한도);if(반환값<0||!임의주소[Failas_rodyklė-32])return 반환값;
        prekė_COUNT=Įklijuoti_SMS(Failas_rodyklė,1);if(prekė_COUNT<0)return prekė_COUNT;반환값=NET_BIND(prekė_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Failas_rodyklė));if(반환값<0)return 반환값;양쪽수신창구[Failas_rodyklė-32]=1;
    }return 연결대기한도<1?-22:NET_laukti(prekė_COUNT);
}
int32_t 자바흐름연결(int32_t Failas_rodyklė,int32_t interneto_adresas,int32_t prievado_numeris){
    if(interneto_adresas==0x7f000001 && išorinis_numeris(Failas_rodyklė)<0)return 되돌림흐름연결(Failas_rodyklė,interneto_adresas,prievado_numeris);
    if(되돌림흐름접속번호(Failas_rodyklė)<0)return -9;int prekė_COUNT=Įklijuoti_SMS(Failas_rodyklė,1);return prekė_COUNT<0?prekė_COUNT:NET_ryšys(prekė_COUNT,interneto_adresas,prievado_numeris);
}
int32_t 자바흐름연결받기(int32_t Failas_rodyklė){
    int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT<0)return 되돌림흐름연결받기(Failas_rodyklė);
    if(양쪽수신창구[Failas_rodyklė-32]){int vietinis=되돌림흐름연결받기(Failas_rodyklė);if(vietinis!=-11)return vietinis;}
    int lygiavertis_mazgas_VALUE=NET_priimti(prekė_COUNT);if(lygiavertis_mazgas_VALUE<0)return lygiavertis_mazgas_VALUE;
    int tikslas=되돌림흐름만들기();if(tikslas<0){Uždaryti_tinklas(lygiavertis_mazgas_VALUE);return tikslas;}išorinis[tikslas-32]=lygiavertis_mazgas_VALUE+1;return tikslas;
}
int32_t 자바흐름읽기(int32_t Failas_rodyklė,int32_t Dydis){
    int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT<0)return 되돌림흐름읽기(Failas_rodyklė,Dydis);if(Dydis<0||Dydis>512)return -22;
    unsigned char duomenys[512];int 반환값=통신읽기(prekė_COUNT,duomenys,Dydis);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,duomenys[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Failas_rodyklė,int32_t Dydis){
    int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT<0)return 되돌림흐름쓰기(Failas_rodyklė,Dydis);if(Dydis<0||Dydis>512)return -22;
    unsigned char duomenys[512];for(int 순번=0;순번<Dydis;순번++)duomenys[순번]=자바전문얻기(순번);return NET_rašymas(prekė_COUNT,duomenys,Dydis);
}
int32_t 자바흐름접속번호(int32_t Failas_rodyklė){int prekė_COUNT=išorinis_numeris(Failas_rodyklė);return prekė_COUNT<0?되돌림흐름접속번호(Failas_rodyklė):(int32_t)tinklas_prievado_numeris(prekė_COUNT);}
int32_t 자바흐름상대(int32_t Failas_rodyklė){int prekė_COUNT=išorinis_numeris(Failas_rodyklė);return prekė_COUNT<0?되돌림흐름상대(Failas_rodyklė):(int32_t)lygiavertis_mazgas_prievado_numeris(prekė_COUNT);}
int32_t 자바흐름주소(int32_t Failas_rodyklė){return išorinis_numeris(Failas_rodyklė)<0?0x7f000001:양쪽수신창구[Failas_rodyklė-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Failas_rodyklė){int prekė_COUNT=išorinis_numeris(Failas_rodyklė);if(prekė_COUNT>=0){Uždaryti_tinklas(prekė_COUNT);išorinis[Failas_rodyklė-32]=0;}if(Failas_rodyklė>=40&&Failas_rodyklė<56)임의주소[Failas_rodyklė-32]=양쪽수신창구[Failas_rodyklė-32]=0;return 되돌림흐름닫기(Failas_rodyklė);}
