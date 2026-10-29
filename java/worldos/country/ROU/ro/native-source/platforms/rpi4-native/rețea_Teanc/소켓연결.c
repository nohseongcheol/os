#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "rețea_Teanc.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_extern_pereche[8], limită_adresa[8];
static int 외부번호(int Fișier_handle) { return Fișier_handle>=32 && Fișier_handle<56 ? 외부연결[Fișier_handle-32]-1 : -1; }
static int lipi_SMS(int Fișier_handle,int Tip_zonă) {
    if(Fișier_handle<32||Fișier_handle>=56)return -9;int Anteriorul_element=외부번호(Fișier_handle);if(Anteriorul_element>=0)return Anteriorul_element;
    int element_COUNT=통신끝점만들기(Tip_zonă);if(element_COUNT>=0)외부연결[Fișier_handle-32]=element_COUNT+1;return element_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t cod_caracter){return 되돌림전문만들기(첫째값,SECOND_VALUE,cod_caracter);}
int32_t 자바전문묶기(int32_t Fișier_handle,int32_t adresă_internet,int32_t număr_port){
    if(adresă_internet==0x7f000001)return 되돌림전문묶기(Fișier_handle,adresă_internet,număr_port);
    if(adresă_internet!=0&&adresă_internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Fișier_handle,0,număr_port);if(반환값<0)return 반환값;
    int element_COUNT=lipi_SMS(Fișier_handle,2);if(element_COUNT<0)return element_COUNT;반환값=NET_BIND(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fișier_handle));if(!반환값)limită_adresa[Fișier_handle-32]=adresă_internet;return 반환값;
}
int32_t 자바전문보내기(int32_t Fișier_handle,int32_t adresă_internet,int32_t număr_port,int32_t Mărime){
    if(adresă_internet==0x7f000001)return 되돌림전문보내기(Fișier_handle,adresă_internet,număr_port,Mărime);
    if(Mărime<0||Mărime>512)return -90;if(număr_port<1||număr_port>65535)return -22;
    if(되돌림전문접속번호(Fișier_handle)<0)return -9;
    if(되돌림전문주소(Fișier_handle)==0x7f000001)return -101;
    int element_COUNT=외부번호(Fișier_handle);if(element_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Fișier_handle)==0)반환값=되돌림전문묶기(Fișier_handle,0,0);if(반환값<0)return 반환값;element_COUNT=lipi_SMS(Fișier_handle,2);if(element_COUNT<0)return element_COUNT;반환값=NET_BIND(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fișier_handle));if(반환값<0)return 반환값;}
    unsigned char date[512];for(int 순번=0;순번<Mărime;순번++)date[순번]=자바전문얻기(순번);return trimite_diagramă_informații(element_COUNT,date,Mărime,adresă_internet,număr_port);
}
int32_t 자바전문받기(int32_t Fișier_handle,int32_t Mărime){
    int element_COUNT=외부번호(Fișier_handle);if(element_COUNT<0)return 되돌림전문받기(Fișier_handle,Mărime);if(Mărime<0||Mărime>512)return -22;
    int local=되돌림전문받기(Fișier_handle,Mărime);if(local!=-11){UDP_extern_pereche[Fișier_handle-32]=0;return local;}
    unsigned char date[512];int 반환값=primi_diagramă_informații(element_COUNT,date,Mărime);if(반환값>=0)UDP_extern_pereche[Fișier_handle-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,date[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Fișier_handle){int element_COUNT=외부번호(Fișier_handle);return element_COUNT<0?되돌림전문접속번호(Fișier_handle):(int32_t)rețea_număr_port(element_COUNT);}
int32_t 자바전문주소(int32_t Fișier_handle){return 외부번호(Fișier_handle)<0?되돌림전문주소(Fișier_handle):limită_adresa[Fișier_handle-32];}
int32_t 자바전문상대(int32_t Fișier_handle){int element_COUNT=외부번호(Fișier_handle);return element_COUNT<0||!UDP_extern_pereche[Fișier_handle-32]?되돌림전문상대(Fișier_handle):(int32_t)pereche_număr_port(element_COUNT);}
int32_t 자바전문원격주소(int32_t Fișier_handle){int element_COUNT=외부번호(Fișier_handle);return element_COUNT<0||!UDP_extern_pereche[Fișier_handle-32]?0x7f000001:(int32_t)NET_pereche_adresa(element_COUNT);}
int32_t 자바전문닫기(int32_t Fișier_handle){int element_COUNT=외부번호(Fișier_handle);if(element_COUNT>=0){închide_rețea(element_COUNT);외부연결[Fișier_handle-32]=0;}if(Fișier_handle>=32&&Fișier_handle<40)UDP_extern_pereche[Fișier_handle-32]=limită_adresa[Fișier_handle-32]=0;return 되돌림전문닫기(Fișier_handle);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Fișier_handle,int32_t adresă_internet,int32_t număr_port){
    if(adresă_internet==0||adresă_internet==0x7f000001){int 반환값=되돌림흐름묶기(Fișier_handle,adresă_internet,număr_port);if(!반환값)임의주소[Fișier_handle-32]=adresă_internet==0;return 반환값;}
    if(adresă_internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Fișier_handle,0,număr_port);if(반환값<0)return 반환값;
    int element_COUNT=lipi_SMS(Fișier_handle,1);return element_COUNT<0?element_COUNT:NET_BIND(element_COUNT,adresă_internet,되돌림흐름접속번호(Fișier_handle));
}
int32_t 자바흐름듣기(int32_t Fișier_handle,int32_t 연결대기한도){
    int element_COUNT=외부번호(Fișier_handle);if(element_COUNT<0){int 반환값=되돌림흐름듣기(Fișier_handle,연결대기한도);if(반환값<0||!임의주소[Fișier_handle-32])return 반환값;
        element_COUNT=lipi_SMS(Fișier_handle,1);if(element_COUNT<0)return element_COUNT;반환값=NET_BIND(element_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Fișier_handle));if(반환값<0)return 반환값;양쪽수신창구[Fișier_handle-32]=1;
    }return 연결대기한도<1?-22:NET_asculta(element_COUNT);
}
int32_t 자바흐름연결(int32_t Fișier_handle,int32_t adresă_internet,int32_t număr_port){
    if(adresă_internet==0x7f000001 && 외부번호(Fișier_handle)<0)return 되돌림흐름연결(Fișier_handle,adresă_internet,număr_port);
    if(되돌림흐름접속번호(Fișier_handle)<0)return -9;int element_COUNT=lipi_SMS(Fișier_handle,1);return element_COUNT<0?element_COUNT:NET_conecta(element_COUNT,adresă_internet,număr_port);
}
int32_t 자바흐름연결받기(int32_t Fișier_handle){
    int element_COUNT=외부번호(Fișier_handle);if(element_COUNT<0)return 되돌림흐름연결받기(Fișier_handle);
    if(양쪽수신창구[Fișier_handle-32]){int local=되돌림흐름연결받기(Fișier_handle);if(local!=-11)return local;}
    int pereche_VALUE=NET_accepta(element_COUNT);if(pereche_VALUE<0)return pereche_VALUE;
    int țintă=되돌림흐름만들기();if(țintă<0){închide_rețea(pereche_VALUE);return țintă;}외부연결[țintă-32]=pereche_VALUE+1;return țintă;
}
int32_t 자바흐름읽기(int32_t Fișier_handle,int32_t Mărime){
    int element_COUNT=외부번호(Fișier_handle);if(element_COUNT<0)return 되돌림흐름읽기(Fișier_handle,Mărime);if(Mărime<0||Mărime>512)return -22;
    unsigned char date[512];int 반환값=통신읽기(element_COUNT,date,Mărime);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,date[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Fișier_handle,int32_t Mărime){
    int element_COUNT=외부번호(Fișier_handle);if(element_COUNT<0)return 되돌림흐름쓰기(Fișier_handle,Mărime);if(Mărime<0||Mărime>512)return -22;
    unsigned char date[512];for(int 순번=0;순번<Mărime;순번++)date[순번]=자바전문얻기(순번);return NET_scriere(element_COUNT,date,Mărime);
}
int32_t 자바흐름접속번호(int32_t Fișier_handle){int element_COUNT=외부번호(Fișier_handle);return element_COUNT<0?되돌림흐름접속번호(Fișier_handle):(int32_t)rețea_număr_port(element_COUNT);}
int32_t 자바흐름상대(int32_t Fișier_handle){int element_COUNT=외부번호(Fișier_handle);return element_COUNT<0?되돌림흐름상대(Fișier_handle):(int32_t)pereche_număr_port(element_COUNT);}
int32_t 자바흐름주소(int32_t Fișier_handle){return 외부번호(Fișier_handle)<0?0x7f000001:양쪽수신창구[Fișier_handle-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Fișier_handle){int element_COUNT=외부번호(Fișier_handle);if(element_COUNT>=0){închide_rețea(element_COUNT);외부연결[Fișier_handle-32]=0;}if(Fișier_handle>=40&&Fișier_handle<56)임의주소[Fișier_handle-32]=양쪽수신창구[Fișier_handle-32]=0;return 되돌림흐름닫기(Fișier_handle);}
