#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "rete_Pila.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int esterno[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_esterno_peer[8], limite_e_mail[8];
static int esterno_numero(int handle_di_file) { return handle_di_file>=32 && handle_di_file<56 ? esterno[handle_di_file-32]-1 : -1; }
static int incollare_SMS(int handle_di_file,int TIPO_area) {
    if(handle_di_file<32||handle_di_file>=56)return -9;int Indietro_articolo=esterno_numero(handle_di_file);if(Indietro_articolo>=0)return Indietro_articolo;
    int articolo_CONTA_NUMERI=Crea_socket_endpoint(TIPO_area);if(articolo_CONTA_NUMERI>=0)esterno[handle_di_file-32]=articolo_CONTA_NUMERI+1;return articolo_CONTA_NUMERI;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECONDO_VALORE,int32_t punto_di_codice){return 되돌림전문만들기(첫째값,SECONDO_VALORE,punto_di_codice);}
int32_t 자바전문묶기(int32_t handle_di_file,int32_t indirizzo_Internet,int32_t numero_di_porta){
    if(indirizzo_Internet==0x7f000001)return 되돌림전문묶기(handle_di_file,indirizzo_Internet,numero_di_porta);
    if(indirizzo_Internet!=0&&indirizzo_Internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(handle_di_file,0,numero_di_porta);if(반환값<0)return 반환값;
    int articolo_CONTA_NUMERI=incollare_SMS(handle_di_file,2);if(articolo_CONTA_NUMERI<0)return articolo_CONTA_NUMERI;반환값=NET_BIND(articolo_CONTA_NUMERI,망상태읽기(0,0),되돌림전문접속번호(handle_di_file));if(!반환값)limite_e_mail[handle_di_file-32]=indirizzo_Internet;return 반환값;
}
int32_t 자바전문보내기(int32_t handle_di_file,int32_t indirizzo_Internet,int32_t numero_di_porta,int32_t Dimensione){
    if(indirizzo_Internet==0x7f000001)return 되돌림전문보내기(handle_di_file,indirizzo_Internet,numero_di_porta,Dimensione);
    if(Dimensione<0||Dimensione>512)return -90;if(numero_di_porta<1||numero_di_porta>65535)return -22;
    if(되돌림전문접속번호(handle_di_file)<0)return -9;
    if(되돌림전문주소(handle_di_file)==0x7f000001)return -101;
    int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI<0){int 반환값=0;if(되돌림전문접속번호(handle_di_file)==0)반환값=되돌림전문묶기(handle_di_file,0,0);if(반환값<0)return 반환값;articolo_CONTA_NUMERI=incollare_SMS(handle_di_file,2);if(articolo_CONTA_NUMERI<0)return articolo_CONTA_NUMERI;반환값=NET_BIND(articolo_CONTA_NUMERI,망상태읽기(0,0),되돌림전문접속번호(handle_di_file));if(반환값<0)return 반환값;}
    unsigned char dati[512];for(int 순번=0;순번<Dimensione;순번++)dati[순번]=자바전문얻기(순번);return inviare_datagramma(articolo_CONTA_NUMERI,dati,Dimensione,indirizzo_Internet,numero_di_porta);
}
int32_t 자바전문받기(int32_t handle_di_file,int32_t Dimensione){
    int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI<0)return 되돌림전문받기(handle_di_file,Dimensione);if(Dimensione<0||Dimensione>512)return -22;
    int locale=되돌림전문받기(handle_di_file,Dimensione);if(locale!=-11){UDP_esterno_peer[handle_di_file-32]=0;return locale;}
    unsigned char dati[512];int 반환값=ricevere_datagramma(articolo_CONTA_NUMERI,dati,Dimensione);if(반환값>=0)UDP_esterno_peer[handle_di_file-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dati[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t handle_di_file){int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);return articolo_CONTA_NUMERI<0?되돌림전문접속번호(handle_di_file):(int32_t)rete_numero_di_porta(articolo_CONTA_NUMERI);}
int32_t 자바전문주소(int32_t handle_di_file){return esterno_numero(handle_di_file)<0?되돌림전문주소(handle_di_file):limite_e_mail[handle_di_file-32];}
int32_t 자바전문상대(int32_t handle_di_file){int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);return articolo_CONTA_NUMERI<0||!UDP_esterno_peer[handle_di_file-32]?되돌림전문상대(handle_di_file):(int32_t)peer_numero_di_porta(articolo_CONTA_NUMERI);}
int32_t 자바전문원격주소(int32_t handle_di_file){int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);return articolo_CONTA_NUMERI<0||!UDP_esterno_peer[handle_di_file-32]?0x7f000001:(int32_t)NET_peer_e_mail(articolo_CONTA_NUMERI);}
int32_t 자바전문닫기(int32_t handle_di_file){int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI>=0){Chiudi_rete(articolo_CONTA_NUMERI);esterno[handle_di_file-32]=0;}if(handle_di_file>=32&&handle_di_file<40)UDP_esterno_peer[handle_di_file-32]=limite_e_mail[handle_di_file-32]=0;return 되돌림전문닫기(handle_di_file);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t handle_di_file,int32_t indirizzo_Internet,int32_t numero_di_porta){
    if(indirizzo_Internet==0||indirizzo_Internet==0x7f000001){int 반환값=되돌림흐름묶기(handle_di_file,indirizzo_Internet,numero_di_porta);if(!반환값)임의주소[handle_di_file-32]=indirizzo_Internet==0;return 반환값;}
    if(indirizzo_Internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(handle_di_file,0,numero_di_porta);if(반환값<0)return 반환값;
    int articolo_CONTA_NUMERI=incollare_SMS(handle_di_file,1);return articolo_CONTA_NUMERI<0?articolo_CONTA_NUMERI:NET_BIND(articolo_CONTA_NUMERI,indirizzo_Internet,되돌림흐름접속번호(handle_di_file));
}
int32_t 자바흐름듣기(int32_t handle_di_file,int32_t backlog){
    int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI<0){int 반환값=되돌림흐름듣기(handle_di_file,backlog);if(반환값<0||!임의주소[handle_di_file-32])return 반환값;
        articolo_CONTA_NUMERI=incollare_SMS(handle_di_file,1);if(articolo_CONTA_NUMERI<0)return articolo_CONTA_NUMERI;반환값=NET_BIND(articolo_CONTA_NUMERI,망상태읽기(0,0),되돌림흐름접속번호(handle_di_file));if(반환값<0)return 반환값;양쪽수신창구[handle_di_file-32]=1;
    }return backlog<1?-22:NET_essere_in_ascolto(articolo_CONTA_NUMERI);
}
int32_t 자바흐름연결(int32_t handle_di_file,int32_t indirizzo_Internet,int32_t numero_di_porta){
    if(indirizzo_Internet==0x7f000001 && esterno_numero(handle_di_file)<0)return 되돌림흐름연결(handle_di_file,indirizzo_Internet,numero_di_porta);
    if(되돌림흐름접속번호(handle_di_file)<0)return -9;int articolo_CONTA_NUMERI=incollare_SMS(handle_di_file,1);return articolo_CONTA_NUMERI<0?articolo_CONTA_NUMERI:NET_CONNETTI(articolo_CONTA_NUMERI,indirizzo_Internet,numero_di_porta);
}
int32_t 자바흐름연결받기(int32_t handle_di_file){
    int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI<0)return 되돌림흐름연결받기(handle_di_file);
    if(양쪽수신창구[handle_di_file-32]){int locale=되돌림흐름연결받기(handle_di_file);if(locale!=-11)return locale;}
    int peer_VALORE=NET_accettare(articolo_CONTA_NUMERI);if(peer_VALORE<0)return peer_VALORE;
    int target=되돌림흐름만들기();if(target<0){Chiudi_rete(peer_VALORE);return target;}esterno[target-32]=peer_VALORE+1;return target;
}
int32_t 자바흐름읽기(int32_t handle_di_file,int32_t Dimensione){
    int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI<0)return 되돌림흐름읽기(handle_di_file,Dimensione);if(Dimensione<0||Dimensione>512)return -22;
    unsigned char dati[512];int 반환값=통신읽기(articolo_CONTA_NUMERI,dati,Dimensione);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dati[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t handle_di_file,int32_t Dimensione){
    int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI<0)return 되돌림흐름쓰기(handle_di_file,Dimensione);if(Dimensione<0||Dimensione>512)return -22;
    unsigned char dati[512];for(int 순번=0;순번<Dimensione;순번++)dati[순번]=자바전문얻기(순번);return NET_scrivere(articolo_CONTA_NUMERI,dati,Dimensione);
}
int32_t 자바흐름접속번호(int32_t handle_di_file){int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);return articolo_CONTA_NUMERI<0?되돌림흐름접속번호(handle_di_file):(int32_t)rete_numero_di_porta(articolo_CONTA_NUMERI);}
int32_t 자바흐름상대(int32_t handle_di_file){int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);return articolo_CONTA_NUMERI<0?되돌림흐름상대(handle_di_file):(int32_t)peer_numero_di_porta(articolo_CONTA_NUMERI);}
int32_t 자바흐름주소(int32_t handle_di_file){return esterno_numero(handle_di_file)<0?0x7f000001:양쪽수신창구[handle_di_file-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t handle_di_file){int articolo_CONTA_NUMERI=esterno_numero(handle_di_file);if(articolo_CONTA_NUMERI>=0){Chiudi_rete(articolo_CONTA_NUMERI);esterno[handle_di_file-32]=0;}if(handle_di_file>=40&&handle_di_file<56)임의주소[handle_di_file-32]=양쪽수신창구[handle_di_file-32]=0;return 되돌림흐름닫기(handle_di_file);}
