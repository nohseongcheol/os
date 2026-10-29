#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Netwọọkụ_ikpo.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int ọbọakwụkwọ_ebenjìaka) { return ọbọakwụkwọ_ebenjìaka>=32 && ọbọakwụkwọ_ebenjìaka<56 ? 외부연결[ọbọakwụkwọ_ebenjìaka-32]-1 : -1; }
static int nyàpanye_SMS(int ọbọakwụkwọ_ebenjìaka,int pinye_otu) {
    if(ọbọakwụkwọ_ebenjìaka<32||ọbọakwụkwọ_ebenjìaka>=56)return -9;int 이전=외부번호(ọbọakwụkwọ_ebenjìaka);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(pinye_otu);if(개수>=0)외부연결[ọbọakwụkwọ_ebenjìaka-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t koòdù_nkeakàrà){return 되돌림전문만들기(첫째값,둘째값,koòdù_nkeakàrà);}
int32_t 자바전문묶기(int32_t ọbọakwụkwọ_ebenjìaka,int32_t adreesi_ịntaneèt,int32_t 접속번호){
    if(adreesi_ịntaneèt==0x7f000001)return 되돌림전문묶기(ọbọakwụkwọ_ebenjìaka,adreesi_ịntaneèt,접속번호);
    if(adreesi_ịntaneèt!=0&&adreesi_ịntaneèt!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(ọbọakwụkwọ_ebenjìaka,0,접속번호);if(반환값<0)return 반환값;
    int 개수=nyàpanye_SMS(ọbọakwụkwọ_ebenjìaka,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(ọbọakwụkwọ_ebenjìaka));if(!반환값)묶인주소[ọbọakwụkwọ_ebenjìaka-32]=adreesi_ịntaneèt;return 반환값;
}
int32_t 자바전문보내기(int32_t ọbọakwụkwọ_ebenjìaka,int32_t adreesi_ịntaneèt,int32_t 접속번호,int32_t Ụhara){
    if(adreesi_ịntaneèt==0x7f000001)return 되돌림전문보내기(ọbọakwụkwọ_ebenjìaka,adreesi_ịntaneèt,접속번호,Ụhara);
    if(Ụhara<0||Ụhara>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(ọbọakwụkwọ_ebenjìaka)<0)return -9;
    if(되돌림전문주소(ọbọakwụkwọ_ebenjìaka)==0x7f000001)return -101;
    int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수<0){int 반환값=0;if(되돌림전문접속번호(ọbọakwụkwọ_ebenjìaka)==0)반환값=되돌림전문묶기(ọbọakwụkwọ_ebenjìaka,0,0);if(반환값<0)return 반환값;개수=nyàpanye_SMS(ọbọakwụkwọ_ebenjìaka,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(ọbọakwụkwọ_ebenjìaka));if(반환값<0)return 반환값;}
    unsigned char datà[512];for(int 순번=0;순번<Ụhara;순번++)datà[순번]=자바전문얻기(순번);return 전문보내기(개수,datà,Ụhara,adreesi_ịntaneèt,접속번호);
}
int32_t 자바전문받기(int32_t ọbọakwụkwọ_ebenjìaka,int32_t Ụhara){
    int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수<0)return 되돌림전문받기(ọbọakwụkwọ_ebenjìaka,Ụhara);if(Ụhara<0||Ụhara>512)return -22;
    int otù_ebe=되돌림전문받기(ọbọakwụkwọ_ebenjìaka,Ụhara);if(otù_ebe!=-11){전문외부상대[ọbọakwụkwọ_ebenjìaka-32]=0;return otù_ebe;}
    unsigned char datà[512];int 반환값=전문받기(개수,datà,Ụhara);if(반환값>=0)전문외부상대[ọbọakwụkwọ_ebenjìaka-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,datà[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t ọbọakwụkwọ_ebenjìaka){int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);return 개수<0?되돌림전문접속번호(ọbọakwụkwọ_ebenjìaka):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t ọbọakwụkwọ_ebenjìaka){return 외부번호(ọbọakwụkwọ_ebenjìaka)<0?되돌림전문주소(ọbọakwụkwọ_ebenjìaka):묶인주소[ọbọakwụkwọ_ebenjìaka-32];}
int32_t 자바전문상대(int32_t ọbọakwụkwọ_ebenjìaka){int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);return 개수<0||!전문외부상대[ọbọakwụkwọ_ebenjìaka-32]?되돌림전문상대(ọbọakwụkwọ_ebenjìaka):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t ọbọakwụkwọ_ebenjìaka){int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);return 개수<0||!전문외부상대[ọbọakwụkwọ_ebenjìaka-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t ọbọakwụkwọ_ebenjìaka){int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수>=0){mmechi_Netwọọkụ(개수);외부연결[ọbọakwụkwọ_ebenjìaka-32]=0;}if(ọbọakwụkwọ_ebenjìaka>=32&&ọbọakwụkwọ_ebenjìaka<40)전문외부상대[ọbọakwụkwọ_ebenjìaka-32]=묶인주소[ọbọakwụkwọ_ebenjìaka-32]=0;return 되돌림전문닫기(ọbọakwụkwọ_ebenjìaka);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t ọbọakwụkwọ_ebenjìaka,int32_t adreesi_ịntaneèt,int32_t 접속번호){
    if(adreesi_ịntaneèt==0||adreesi_ịntaneèt==0x7f000001){int 반환값=되돌림흐름묶기(ọbọakwụkwọ_ebenjìaka,adreesi_ịntaneèt,접속번호);if(!반환값)임의주소[ọbọakwụkwọ_ebenjìaka-32]=adreesi_ịntaneèt==0;return 반환값;}
    if(adreesi_ịntaneèt!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(ọbọakwụkwọ_ebenjìaka,0,접속번호);if(반환값<0)return 반환값;
    int 개수=nyàpanye_SMS(ọbọakwụkwọ_ebenjìaka,1);return 개수<0?개수:망주소묶기(개수,adreesi_ịntaneèt,되돌림흐름접속번호(ọbọakwụkwọ_ebenjìaka));
}
int32_t 자바흐름듣기(int32_t ọbọakwụkwọ_ebenjìaka,int32_t 연결대기한도){
    int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수<0){int 반환값=되돌림흐름듣기(ọbọakwụkwọ_ebenjìaka,연결대기한도);if(반환값<0||!임의주소[ọbọakwụkwọ_ebenjìaka-32])return 반환값;
        개수=nyàpanye_SMS(ọbọakwụkwọ_ebenjìaka,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(ọbọakwụkwọ_ebenjìaka));if(반환값<0)return 반환값;양쪽수신창구[ọbọakwụkwọ_ebenjìaka-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t ọbọakwụkwọ_ebenjìaka,int32_t adreesi_ịntaneèt,int32_t 접속번호){
    if(adreesi_ịntaneèt==0x7f000001 && 외부번호(ọbọakwụkwọ_ebenjìaka)<0)return 되돌림흐름연결(ọbọakwụkwọ_ebenjìaka,adreesi_ịntaneèt,접속번호);
    if(되돌림흐름접속번호(ọbọakwụkwọ_ebenjìaka)<0)return -9;int 개수=nyàpanye_SMS(ọbọakwụkwọ_ebenjìaka,1);return 개수<0?개수:망연결하기(개수,adreesi_ịntaneèt,접속번호);
}
int32_t 자바흐름연결받기(int32_t ọbọakwụkwọ_ebenjìaka){
    int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수<0)return 되돌림흐름연결받기(ọbọakwụkwọ_ebenjìaka);
    if(양쪽수신창구[ọbọakwụkwọ_ebenjìaka-32]){int otù_ebe=되돌림흐름연결받기(ọbọakwụkwọ_ebenjìaka);if(otù_ebe!=-11)return otù_ebe;}
    int ibè_valuu=망연결받기(개수);if(ibè_valuu<0)return ibè_valuu;
    int ebenlereanya=되돌림흐름만들기();if(ebenlereanya<0){mmechi_Netwọọkụ(ibè_valuu);return ebenlereanya;}외부연결[ebenlereanya-32]=ibè_valuu+1;return ebenlereanya;
}
int32_t 자바흐름읽기(int32_t ọbọakwụkwọ_ebenjìaka,int32_t Ụhara){
    int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수<0)return 되돌림흐름읽기(ọbọakwụkwọ_ebenjìaka,Ụhara);if(Ụhara<0||Ụhara>512)return -22;
    unsigned char datà[512];int 반환값=통신읽기(개수,datà,Ụhara);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,datà[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t ọbọakwụkwọ_ebenjìaka,int32_t Ụhara){
    int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수<0)return 되돌림흐름쓰기(ọbọakwụkwọ_ebenjìaka,Ụhara);if(Ụhara<0||Ụhara>512)return -22;
    unsigned char datà[512];for(int 순번=0;순번<Ụhara;순번++)datà[순번]=자바전문얻기(순번);return 통신쓰기(개수,datà,Ụhara);
}
int32_t 자바흐름접속번호(int32_t ọbọakwụkwọ_ebenjìaka){int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);return 개수<0?되돌림흐름접속번호(ọbọakwụkwọ_ebenjìaka):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t ọbọakwụkwọ_ebenjìaka){int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);return 개수<0?되돌림흐름상대(ọbọakwụkwọ_ebenjìaka):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t ọbọakwụkwọ_ebenjìaka){return 외부번호(ọbọakwụkwọ_ebenjìaka)<0?0x7f000001:양쪽수신창구[ọbọakwụkwọ_ebenjìaka-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t ọbọakwụkwọ_ebenjìaka){int 개수=외부번호(ọbọakwụkwọ_ebenjìaka);if(개수>=0){mmechi_Netwọọkụ(개수);외부연결[ọbọakwụkwọ_ebenjìaka-32]=0;}if(ọbọakwụkwọ_ebenjìaka>=40&&ọbọakwụkwọ_ebenjìaka<56)임의주소[ọbọakwụkwọ_ebenjìaka-32]=양쪽수신창구[ọbọakwụkwọ_ebenjìaka-32]=0;return 되돌림흐름닫기(ọbọakwụkwọ_ebenjìaka);}
