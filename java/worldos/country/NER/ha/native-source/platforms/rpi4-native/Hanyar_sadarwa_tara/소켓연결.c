#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Hanyar_sadarwa_tara.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int Fayil_Mariki) { return Fayil_Mariki>=32 && Fayil_Mariki<56 ? 외부연결[Fayil_Mariki-32]-1 : -1; }
static int manna_SMS(int Fayil_Mariki,int rubuta_ɓangare) {
    if(Fayil_Mariki<32||Fayil_Mariki>=56)return -9;int 이전=외부번호(Fayil_Mariki);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(rubuta_ɓangare);if(개수>=0)외부연결[Fayil_Mariki-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t Lambar_sirrin_harafi){return 되돌림전문만들기(첫째값,둘째값,Lambar_sirrin_harafi);}
int32_t 자바전문묶기(int32_t Fayil_Mariki,int32_t Adireshin_yanar_gizo,int32_t lambar_kafa){
    if(Adireshin_yanar_gizo==0x7f000001)return 되돌림전문묶기(Fayil_Mariki,Adireshin_yanar_gizo,lambar_kafa);
    if(Adireshin_yanar_gizo!=0&&Adireshin_yanar_gizo!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Fayil_Mariki,0,lambar_kafa);if(반환값<0)return 반환값;
    int 개수=manna_SMS(Fayil_Mariki,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(Fayil_Mariki));if(!반환값)묶인주소[Fayil_Mariki-32]=Adireshin_yanar_gizo;return 반환값;
}
int32_t 자바전문보내기(int32_t Fayil_Mariki,int32_t Adireshin_yanar_gizo,int32_t lambar_kafa,int32_t Girma){
    if(Adireshin_yanar_gizo==0x7f000001)return 되돌림전문보내기(Fayil_Mariki,Adireshin_yanar_gizo,lambar_kafa,Girma);
    if(Girma<0||Girma>512)return -90;if(lambar_kafa<1||lambar_kafa>65535)return -22;
    if(되돌림전문접속번호(Fayil_Mariki)<0)return -9;
    if(되돌림전문주소(Fayil_Mariki)==0x7f000001)return -101;
    int 개수=외부번호(Fayil_Mariki);if(개수<0){int 반환값=0;if(되돌림전문접속번호(Fayil_Mariki)==0)반환값=되돌림전문묶기(Fayil_Mariki,0,0);if(반환값<0)return 반환값;개수=manna_SMS(Fayil_Mariki,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(Fayil_Mariki));if(반환값<0)return 반환값;}
    unsigned char Tarin_bayani[512];for(int 순번=0;순번<Girma;순번++)Tarin_bayani[순번]=자바전문얻기(순번);return 전문보내기(개수,Tarin_bayani,Girma,Adireshin_yanar_gizo,lambar_kafa);
}
int32_t 자바전문받기(int32_t Fayil_Mariki,int32_t Girma){
    int 개수=외부번호(Fayil_Mariki);if(개수<0)return 되돌림전문받기(Fayil_Mariki,Girma);if(Girma<0||Girma>512)return -22;
    int na_gida=되돌림전문받기(Fayil_Mariki,Girma);if(na_gida!=-11){전문외부상대[Fayil_Mariki-32]=0;return na_gida;}
    unsigned char Tarin_bayani[512];int 반환값=전문받기(개수,Tarin_bayani,Girma);if(반환값>=0)전문외부상대[Fayil_Mariki-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,Tarin_bayani[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Fayil_Mariki){int 개수=외부번호(Fayil_Mariki);return 개수<0?되돌림전문접속번호(Fayil_Mariki):(int32_t)Hanyar_sadarwa_lambar_kafa(개수);}
int32_t 자바전문주소(int32_t Fayil_Mariki){return 외부번호(Fayil_Mariki)<0?되돌림전문주소(Fayil_Mariki):묶인주소[Fayil_Mariki-32];}
int32_t 자바전문상대(int32_t Fayil_Mariki){int 개수=외부번호(Fayil_Mariki);return 개수<0||!전문외부상대[Fayil_Mariki-32]?되돌림전문상대(Fayil_Mariki):(int32_t)Fiya_lambar_kafa(개수);}
int32_t 자바전문원격주소(int32_t Fayil_Mariki){int 개수=외부번호(Fayil_Mariki);return 개수<0||!전문외부상대[Fayil_Mariki-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t Fayil_Mariki){int 개수=외부번호(Fayil_Mariki);if(개수>=0){Rufe_Hanyar_sadarwa(개수);외부연결[Fayil_Mariki-32]=0;}if(Fayil_Mariki>=32&&Fayil_Mariki<40)전문외부상대[Fayil_Mariki-32]=묶인주소[Fayil_Mariki-32]=0;return 되돌림전문닫기(Fayil_Mariki);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Fayil_Mariki,int32_t Adireshin_yanar_gizo,int32_t lambar_kafa){
    if(Adireshin_yanar_gizo==0||Adireshin_yanar_gizo==0x7f000001){int 반환값=되돌림흐름묶기(Fayil_Mariki,Adireshin_yanar_gizo,lambar_kafa);if(!반환값)임의주소[Fayil_Mariki-32]=Adireshin_yanar_gizo==0;return 반환값;}
    if(Adireshin_yanar_gizo!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Fayil_Mariki,0,lambar_kafa);if(반환값<0)return 반환값;
    int 개수=manna_SMS(Fayil_Mariki,1);return 개수<0?개수:망주소묶기(개수,Adireshin_yanar_gizo,되돌림흐름접속번호(Fayil_Mariki));
}
int32_t 자바흐름듣기(int32_t Fayil_Mariki,int32_t 연결대기한도){
    int 개수=외부번호(Fayil_Mariki);if(개수<0){int 반환값=되돌림흐름듣기(Fayil_Mariki,연결대기한도);if(반환값<0||!임의주소[Fayil_Mariki-32])return 반환값;
        개수=manna_SMS(Fayil_Mariki,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(Fayil_Mariki));if(반환값<0)return 반환값;양쪽수신창구[Fayil_Mariki-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t Fayil_Mariki,int32_t Adireshin_yanar_gizo,int32_t lambar_kafa){
    if(Adireshin_yanar_gizo==0x7f000001 && 외부번호(Fayil_Mariki)<0)return 되돌림흐름연결(Fayil_Mariki,Adireshin_yanar_gizo,lambar_kafa);
    if(되돌림흐름접속번호(Fayil_Mariki)<0)return -9;int 개수=manna_SMS(Fayil_Mariki,1);return 개수<0?개수:망연결하기(개수,Adireshin_yanar_gizo,lambar_kafa);
}
int32_t 자바흐름연결받기(int32_t Fayil_Mariki){
    int 개수=외부번호(Fayil_Mariki);if(개수<0)return 되돌림흐름연결받기(Fayil_Mariki);
    if(양쪽수신창구[Fayil_Mariki-32]){int na_gida=되돌림흐름연결받기(Fayil_Mariki);if(na_gida!=-11)return na_gida;}
    int Fiya_Daraja=망연결받기(개수);if(Fiya_Daraja<0)return Fiya_Daraja;
    int tageti=되돌림흐름만들기();if(tageti<0){Rufe_Hanyar_sadarwa(Fiya_Daraja);return tageti;}외부연결[tageti-32]=Fiya_Daraja+1;return tageti;
}
int32_t 자바흐름읽기(int32_t Fayil_Mariki,int32_t Girma){
    int 개수=외부번호(Fayil_Mariki);if(개수<0)return 되돌림흐름읽기(Fayil_Mariki,Girma);if(Girma<0||Girma>512)return -22;
    unsigned char Tarin_bayani[512];int 반환값=통신읽기(개수,Tarin_bayani,Girma);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,Tarin_bayani[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Fayil_Mariki,int32_t Girma){
    int 개수=외부번호(Fayil_Mariki);if(개수<0)return 되돌림흐름쓰기(Fayil_Mariki,Girma);if(Girma<0||Girma>512)return -22;
    unsigned char Tarin_bayani[512];for(int 순번=0;순번<Girma;순번++)Tarin_bayani[순번]=자바전문얻기(순번);return 통신쓰기(개수,Tarin_bayani,Girma);
}
int32_t 자바흐름접속번호(int32_t Fayil_Mariki){int 개수=외부번호(Fayil_Mariki);return 개수<0?되돌림흐름접속번호(Fayil_Mariki):(int32_t)Hanyar_sadarwa_lambar_kafa(개수);}
int32_t 자바흐름상대(int32_t Fayil_Mariki){int 개수=외부번호(Fayil_Mariki);return 개수<0?되돌림흐름상대(Fayil_Mariki):(int32_t)Fiya_lambar_kafa(개수);}
int32_t 자바흐름주소(int32_t Fayil_Mariki){return 외부번호(Fayil_Mariki)<0?0x7f000001:양쪽수신창구[Fayil_Mariki-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Fayil_Mariki){int 개수=외부번호(Fayil_Mariki);if(개수>=0){Rufe_Hanyar_sadarwa(개수);외부연결[Fayil_Mariki-32]=0;}if(Fayil_Mariki>=40&&Fayil_Mariki<56)임의주소[Fayil_Mariki-32]=양쪽수신창구[Fayil_Mariki-32]=0;return 되돌림흐름닫기(Fayil_Mariki);}
