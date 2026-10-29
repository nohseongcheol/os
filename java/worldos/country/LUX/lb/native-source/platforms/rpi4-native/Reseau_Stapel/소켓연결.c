#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Reseau_Stapel.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int Fichier_Handle) { return Fichier_Handle>=32 && Fichier_Handle<56 ? 외부연결[Fichier_Handle-32]-1 : -1; }
static int apechen_SMS(int Fichier_Handle,int TYPE_Kategorie) {
    if(Fichier_Handle<32||Fichier_Handle>=56)return -9;int 이전=외부번호(Fichier_Handle);if(이전>=0)return 이전;
    int Element_COUNT=통신끝점만들기(TYPE_Kategorie);if(Element_COUNT>=0)외부연결[Fichier_Handle-32]=Element_COUNT+1;return Element_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t Zeechecode){return 되돌림전문만들기(첫째값,SECOND_VALUE,Zeechecode);}
int32_t 자바전문묶기(int32_t Fichier_Handle,int32_t Internetsadress,int32_t 접속번호){
    if(Internetsadress==0x7f000001)return 되돌림전문묶기(Fichier_Handle,Internetsadress,접속번호);
    if(Internetsadress!=0&&Internetsadress!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Fichier_Handle,0,접속번호);if(반환값<0)return 반환값;
    int Element_COUNT=apechen_SMS(Fichier_Handle,2);if(Element_COUNT<0)return Element_COUNT;반환값=망주소묶기(Element_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fichier_Handle));if(!반환값)묶인주소[Fichier_Handle-32]=Internetsadress;return 반환값;
}
int32_t 자바전문보내기(int32_t Fichier_Handle,int32_t Internetsadress,int32_t 접속번호,int32_t d_Gréisst_veränneren){
    if(Internetsadress==0x7f000001)return 되돌림전문보내기(Fichier_Handle,Internetsadress,접속번호,d_Gréisst_veränneren);
    if(d_Gréisst_veränneren<0||d_Gréisst_veränneren>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(Fichier_Handle)<0)return -9;
    if(되돌림전문주소(Fichier_Handle)==0x7f000001)return -101;
    int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Fichier_Handle)==0)반환값=되돌림전문묶기(Fichier_Handle,0,0);if(반환값<0)return 반환값;Element_COUNT=apechen_SMS(Fichier_Handle,2);if(Element_COUNT<0)return Element_COUNT;반환값=망주소묶기(Element_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fichier_Handle));if(반환값<0)return 반환값;}
    unsigned char Daten[512];for(int 순번=0;순번<d_Gréisst_veränneren;순번++)Daten[순번]=자바전문얻기(순번);return 전문보내기(Element_COUNT,Daten,d_Gréisst_veränneren,Internetsadress,접속번호);
}
int32_t 자바전문받기(int32_t Fichier_Handle,int32_t d_Gréisst_veränneren){
    int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT<0)return 되돌림전문받기(Fichier_Handle,d_Gréisst_veränneren);if(d_Gréisst_veränneren<0||d_Gréisst_veränneren>512)return -22;
    int lokal=되돌림전문받기(Fichier_Handle,d_Gréisst_veränneren);if(lokal!=-11){전문외부상대[Fichier_Handle-32]=0;return lokal;}
    unsigned char Daten[512];int 반환값=전문받기(Element_COUNT,Daten,d_Gréisst_veränneren);if(반환값>=0)전문외부상대[Fichier_Handle-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,Daten[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Fichier_Handle){int Element_COUNT=외부번호(Fichier_Handle);return Element_COUNT<0?되돌림전문접속번호(Fichier_Handle):(int32_t)통신접속번호(Element_COUNT);}
int32_t 자바전문주소(int32_t Fichier_Handle){return 외부번호(Fichier_Handle)<0?되돌림전문주소(Fichier_Handle):묶인주소[Fichier_Handle-32];}
int32_t 자바전문상대(int32_t Fichier_Handle){int Element_COUNT=외부번호(Fichier_Handle);return Element_COUNT<0||!전문외부상대[Fichier_Handle-32]?되돌림전문상대(Fichier_Handle):(int32_t)상대접속번호(Element_COUNT);}
int32_t 자바전문원격주소(int32_t Fichier_Handle){int Element_COUNT=외부번호(Fichier_Handle);return Element_COUNT<0||!전문외부상대[Fichier_Handle-32]?0x7f000001:(int32_t)상대통신주소(Element_COUNT);}
int32_t 자바전문닫기(int32_t Fichier_Handle){int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT>=0){Clôture_Reseau(Element_COUNT);외부연결[Fichier_Handle-32]=0;}if(Fichier_Handle>=32&&Fichier_Handle<40)전문외부상대[Fichier_Handle-32]=묶인주소[Fichier_Handle-32]=0;return 되돌림전문닫기(Fichier_Handle);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Fichier_Handle,int32_t Internetsadress,int32_t 접속번호){
    if(Internetsadress==0||Internetsadress==0x7f000001){int 반환값=되돌림흐름묶기(Fichier_Handle,Internetsadress,접속번호);if(!반환값)임의주소[Fichier_Handle-32]=Internetsadress==0;return 반환값;}
    if(Internetsadress!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Fichier_Handle,0,접속번호);if(반환값<0)return 반환값;
    int Element_COUNT=apechen_SMS(Fichier_Handle,1);return Element_COUNT<0?Element_COUNT:망주소묶기(Element_COUNT,Internetsadress,되돌림흐름접속번호(Fichier_Handle));
}
int32_t 자바흐름듣기(int32_t Fichier_Handle,int32_t 연결대기한도){
    int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT<0){int 반환값=되돌림흐름듣기(Fichier_Handle,연결대기한도);if(반환값<0||!임의주소[Fichier_Handle-32])return 반환값;
        Element_COUNT=apechen_SMS(Fichier_Handle,1);if(Element_COUNT<0)return Element_COUNT;반환값=망주소묶기(Element_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Fichier_Handle));if(반환값<0)return 반환값;양쪽수신창구[Fichier_Handle-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(Element_COUNT);
}
int32_t 자바흐름연결(int32_t Fichier_Handle,int32_t Internetsadress,int32_t 접속번호){
    if(Internetsadress==0x7f000001 && 외부번호(Fichier_Handle)<0)return 되돌림흐름연결(Fichier_Handle,Internetsadress,접속번호);
    if(되돌림흐름접속번호(Fichier_Handle)<0)return -9;int Element_COUNT=apechen_SMS(Fichier_Handle,1);return Element_COUNT<0?Element_COUNT:망연결하기(Element_COUNT,Internetsadress,접속번호);
}
int32_t 자바흐름연결받기(int32_t Fichier_Handle){
    int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT<0)return 되돌림흐름연결받기(Fichier_Handle);
    if(양쪽수신창구[Fichier_Handle-32]){int lokal=되돌림흐름연결받기(Fichier_Handle);if(lokal!=-11)return lokal;}
    int Peer_VALUE=망연결받기(Element_COUNT);if(Peer_VALUE<0)return Peer_VALUE;
    int Zil=되돌림흐름만들기();if(Zil<0){Clôture_Reseau(Peer_VALUE);return Zil;}외부연결[Zil-32]=Peer_VALUE+1;return Zil;
}
int32_t 자바흐름읽기(int32_t Fichier_Handle,int32_t d_Gréisst_veränneren){
    int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT<0)return 되돌림흐름읽기(Fichier_Handle,d_Gréisst_veränneren);if(d_Gréisst_veränneren<0||d_Gréisst_veränneren>512)return -22;
    unsigned char Daten[512];int 반환값=통신읽기(Element_COUNT,Daten,d_Gréisst_veränneren);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,Daten[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Fichier_Handle,int32_t d_Gréisst_veränneren){
    int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT<0)return 되돌림흐름쓰기(Fichier_Handle,d_Gréisst_veränneren);if(d_Gréisst_veränneren<0||d_Gréisst_veränneren>512)return -22;
    unsigned char Daten[512];for(int 순번=0;순번<d_Gréisst_veränneren;순번++)Daten[순번]=자바전문얻기(순번);return 통신쓰기(Element_COUNT,Daten,d_Gréisst_veränneren);
}
int32_t 자바흐름접속번호(int32_t Fichier_Handle){int Element_COUNT=외부번호(Fichier_Handle);return Element_COUNT<0?되돌림흐름접속번호(Fichier_Handle):(int32_t)통신접속번호(Element_COUNT);}
int32_t 자바흐름상대(int32_t Fichier_Handle){int Element_COUNT=외부번호(Fichier_Handle);return Element_COUNT<0?되돌림흐름상대(Fichier_Handle):(int32_t)상대접속번호(Element_COUNT);}
int32_t 자바흐름주소(int32_t Fichier_Handle){return 외부번호(Fichier_Handle)<0?0x7f000001:양쪽수신창구[Fichier_Handle-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Fichier_Handle){int Element_COUNT=외부번호(Fichier_Handle);if(Element_COUNT>=0){Clôture_Reseau(Element_COUNT);외부연결[Fichier_Handle-32]=0;}if(Fichier_Handle>=40&&Fichier_Handle<56)임의주소[Fichier_Handle-32]=양쪽수신창구[Fichier_Handle-32]=0;return 되돌림흐름닫기(Fichier_Handle);}
