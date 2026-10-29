#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Şəbəkə_Yığın.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int fayl_tutacaq) { return fayl_tutacaq>=32 && fayl_tutacaq<56 ? 외부연결[fayl_tutacaq-32]-1 : -1; }
static int əlavə_etmək_SMS(int fayl_tutacaq,int TYPE_sahə) {
    if(fayl_tutacaq<32||fayl_tutacaq>=56)return -9;int 이전=외부번호(fayl_tutacaq);if(이전>=0)return 이전;
    int element_COUNT=통신끝점만들기(TYPE_sahə);if(element_COUNT>=0)외부연결[fayl_tutacaq-32]=element_COUNT+1;return element_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t simvol_kodu){return 되돌림전문만들기(첫째값,SECOND_VALUE,simvol_kodu);}
int32_t 자바전문묶기(int32_t fayl_tutacaq,int32_t İnternet_ünvanı,int32_t 접속번호){
    if(İnternet_ünvanı==0x7f000001)return 되돌림전문묶기(fayl_tutacaq,İnternet_ünvanı,접속번호);
    if(İnternet_ünvanı!=0&&İnternet_ünvanı!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fayl_tutacaq,0,접속번호);if(반환값<0)return 반환값;
    int element_COUNT=əlavə_etmək_SMS(fayl_tutacaq,2);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(fayl_tutacaq));if(!반환값)묶인주소[fayl_tutacaq-32]=İnternet_ünvanı;return 반환값;
}
int32_t 자바전문보내기(int32_t fayl_tutacaq,int32_t İnternet_ünvanı,int32_t 접속번호,int32_t Böyüklük){
    if(İnternet_ünvanı==0x7f000001)return 되돌림전문보내기(fayl_tutacaq,İnternet_ünvanı,접속번호,Böyüklük);
    if(Böyüklük<0||Böyüklük>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(fayl_tutacaq)<0)return -9;
    if(되돌림전문주소(fayl_tutacaq)==0x7f000001)return -101;
    int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT<0){int 반환값=0;if(되돌림전문접속번호(fayl_tutacaq)==0)반환값=되돌림전문묶기(fayl_tutacaq,0,0);if(반환값<0)return 반환값;element_COUNT=əlavə_etmək_SMS(fayl_tutacaq,2);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(fayl_tutacaq));if(반환값<0)return 반환값;}
    unsigned char verilənlər[512];for(int 순번=0;순번<Böyüklük;순번++)verilənlər[순번]=자바전문얻기(순번);return 전문보내기(element_COUNT,verilənlər,Böyüklük,İnternet_ünvanı,접속번호);
}
int32_t 자바전문받기(int32_t fayl_tutacaq,int32_t Böyüklük){
    int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT<0)return 되돌림전문받기(fayl_tutacaq,Böyüklük);if(Böyüklük<0||Böyüklük>512)return -22;
    int lokal=되돌림전문받기(fayl_tutacaq,Böyüklük);if(lokal!=-11){전문외부상대[fayl_tutacaq-32]=0;return lokal;}
    unsigned char verilənlər[512];int 반환값=전문받기(element_COUNT,verilənlər,Böyüklük);if(반환값>=0)전문외부상대[fayl_tutacaq-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,verilənlər[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fayl_tutacaq){int element_COUNT=외부번호(fayl_tutacaq);return element_COUNT<0?되돌림전문접속번호(fayl_tutacaq):(int32_t)통신접속번호(element_COUNT);}
int32_t 자바전문주소(int32_t fayl_tutacaq){return 외부번호(fayl_tutacaq)<0?되돌림전문주소(fayl_tutacaq):묶인주소[fayl_tutacaq-32];}
int32_t 자바전문상대(int32_t fayl_tutacaq){int element_COUNT=외부번호(fayl_tutacaq);return element_COUNT<0||!전문외부상대[fayl_tutacaq-32]?되돌림전문상대(fayl_tutacaq):(int32_t)상대접속번호(element_COUNT);}
int32_t 자바전문원격주소(int32_t fayl_tutacaq){int element_COUNT=외부번호(fayl_tutacaq);return element_COUNT<0||!전문외부상대[fayl_tutacaq-32]?0x7f000001:(int32_t)상대통신주소(element_COUNT);}
int32_t 자바전문닫기(int32_t fayl_tutacaq){int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT>=0){bağlamaq_Şəbəkə(element_COUNT);외부연결[fayl_tutacaq-32]=0;}if(fayl_tutacaq>=32&&fayl_tutacaq<40)전문외부상대[fayl_tutacaq-32]=묶인주소[fayl_tutacaq-32]=0;return 되돌림전문닫기(fayl_tutacaq);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fayl_tutacaq,int32_t İnternet_ünvanı,int32_t 접속번호){
    if(İnternet_ünvanı==0||İnternet_ünvanı==0x7f000001){int 반환값=되돌림흐름묶기(fayl_tutacaq,İnternet_ünvanı,접속번호);if(!반환값)임의주소[fayl_tutacaq-32]=İnternet_ünvanı==0;return 반환값;}
    if(İnternet_ünvanı!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fayl_tutacaq,0,접속번호);if(반환값<0)return 반환값;
    int element_COUNT=əlavə_etmək_SMS(fayl_tutacaq,1);return element_COUNT<0?element_COUNT:망주소묶기(element_COUNT,İnternet_ünvanı,되돌림흐름접속번호(fayl_tutacaq));
}
int32_t 자바흐름듣기(int32_t fayl_tutacaq,int32_t 연결대기한도){
    int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT<0){int 반환값=되돌림흐름듣기(fayl_tutacaq,연결대기한도);if(반환값<0||!임의주소[fayl_tutacaq-32])return 반환값;
        element_COUNT=əlavə_etmək_SMS(fayl_tutacaq,1);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림흐름접속번호(fayl_tutacaq));if(반환값<0)return 반환값;양쪽수신창구[fayl_tutacaq-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(element_COUNT);
}
int32_t 자바흐름연결(int32_t fayl_tutacaq,int32_t İnternet_ünvanı,int32_t 접속번호){
    if(İnternet_ünvanı==0x7f000001 && 외부번호(fayl_tutacaq)<0)return 되돌림흐름연결(fayl_tutacaq,İnternet_ünvanı,접속번호);
    if(되돌림흐름접속번호(fayl_tutacaq)<0)return -9;int element_COUNT=əlavə_etmək_SMS(fayl_tutacaq,1);return element_COUNT<0?element_COUNT:망연결하기(element_COUNT,İnternet_ünvanı,접속번호);
}
int32_t 자바흐름연결받기(int32_t fayl_tutacaq){
    int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT<0)return 되돌림흐름연결받기(fayl_tutacaq);
    if(양쪽수신창구[fayl_tutacaq-32]){int lokal=되돌림흐름연결받기(fayl_tutacaq);if(lokal!=-11)return lokal;}
    int eynisəviyyəli_VALUE=망연결받기(element_COUNT);if(eynisəviyyəli_VALUE<0)return eynisəviyyəli_VALUE;
    int hədəf=되돌림흐름만들기();if(hədəf<0){bağlamaq_Şəbəkə(eynisəviyyəli_VALUE);return hədəf;}외부연결[hədəf-32]=eynisəviyyəli_VALUE+1;return hədəf;
}
int32_t 자바흐름읽기(int32_t fayl_tutacaq,int32_t Böyüklük){
    int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT<0)return 되돌림흐름읽기(fayl_tutacaq,Böyüklük);if(Böyüklük<0||Böyüklük>512)return -22;
    unsigned char verilənlər[512];int 반환값=통신읽기(element_COUNT,verilənlər,Böyüklük);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,verilənlər[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fayl_tutacaq,int32_t Böyüklük){
    int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT<0)return 되돌림흐름쓰기(fayl_tutacaq,Böyüklük);if(Böyüklük<0||Böyüklük>512)return -22;
    unsigned char verilənlər[512];for(int 순번=0;순번<Böyüklük;순번++)verilənlər[순번]=자바전문얻기(순번);return 통신쓰기(element_COUNT,verilənlər,Böyüklük);
}
int32_t 자바흐름접속번호(int32_t fayl_tutacaq){int element_COUNT=외부번호(fayl_tutacaq);return element_COUNT<0?되돌림흐름접속번호(fayl_tutacaq):(int32_t)통신접속번호(element_COUNT);}
int32_t 자바흐름상대(int32_t fayl_tutacaq){int element_COUNT=외부번호(fayl_tutacaq);return element_COUNT<0?되돌림흐름상대(fayl_tutacaq):(int32_t)상대접속번호(element_COUNT);}
int32_t 자바흐름주소(int32_t fayl_tutacaq){return 외부번호(fayl_tutacaq)<0?0x7f000001:양쪽수신창구[fayl_tutacaq-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fayl_tutacaq){int element_COUNT=외부번호(fayl_tutacaq);if(element_COUNT>=0){bağlamaq_Şəbəkə(element_COUNT);외부연결[fayl_tutacaq-32]=0;}if(fayl_tutacaq>=40&&fayl_tutacaq<56)임의주소[fayl_tutacaq-32]=양쪽수신창구[fayl_tutacaq-32]=0;return 되돌림흐름닫기(fayl_tutacaq);}
