#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Network_Stack.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int file_hawakán) { return file_hawakán>=32 && file_hawakán<56 ? 외부연결[file_hawakán-32]-1 : -1; }
static int I_paste_SMS(int file_hawakán,int TYPE_kategorya) {
    if(file_hawakán<32||file_hawakán>=56)return -9;int 이전=외부번호(file_hawakán);if(이전>=0)return 이전;
    int item_COUNT=통신끝점만들기(TYPE_kategorya);if(item_COUNT>=0)외부연결[file_hawakán-32]=item_COUNT+1;return item_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t character_code){return 되돌림전문만들기(첫째값,SECOND_VALUE,character_code);}
int32_t 자바전문묶기(int32_t file_hawakán,int32_t Internet_address,int32_t numero_ng_port){
    if(Internet_address==0x7f000001)return 되돌림전문묶기(file_hawakán,Internet_address,numero_ng_port);
    if(Internet_address!=0&&Internet_address!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(file_hawakán,0,numero_ng_port);if(반환값<0)return 반환값;
    int item_COUNT=I_paste_SMS(file_hawakán,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(file_hawakán));if(!반환값)묶인주소[file_hawakán-32]=Internet_address;return 반환값;
}
int32_t 자바전문보내기(int32_t file_hawakán,int32_t Internet_address,int32_t numero_ng_port,int32_t sukat_82232621){
    if(Internet_address==0x7f000001)return 되돌림전문보내기(file_hawakán,Internet_address,numero_ng_port,sukat_82232621);
    if(sukat_82232621<0||sukat_82232621>512)return -90;if(numero_ng_port<1||numero_ng_port>65535)return -22;
    if(되돌림전문접속번호(file_hawakán)<0)return -9;
    if(되돌림전문주소(file_hawakán)==0x7f000001)return -101;
    int item_COUNT=외부번호(file_hawakán);if(item_COUNT<0){int 반환값=0;if(되돌림전문접속번호(file_hawakán)==0)반환값=되돌림전문묶기(file_hawakán,0,0);if(반환값<0)return 반환값;item_COUNT=I_paste_SMS(file_hawakán,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(file_hawakán));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<sukat_82232621;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(item_COUNT,data,sukat_82232621,Internet_address,numero_ng_port);
}
int32_t 자바전문받기(int32_t file_hawakán,int32_t sukat_82232621){
    int item_COUNT=외부번호(file_hawakán);if(item_COUNT<0)return 되돌림전문받기(file_hawakán,sukat_82232621);if(sukat_82232621<0||sukat_82232621>512)return -22;
    int lokal=되돌림전문받기(file_hawakán,sukat_82232621);if(lokal!=-11){전문외부상대[file_hawakán-32]=0;return lokal;}
    unsigned char data[512];int 반환값=전문받기(item_COUNT,data,sukat_82232621);if(반환값>=0)전문외부상대[file_hawakán-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t file_hawakán){int item_COUNT=외부번호(file_hawakán);return item_COUNT<0?되돌림전문접속번호(file_hawakán):(int32_t)Network_numero_ng_port(item_COUNT);}
int32_t 자바전문주소(int32_t file_hawakán){return 외부번호(file_hawakán)<0?되돌림전문주소(file_hawakán):묶인주소[file_hawakán-32];}
int32_t 자바전문상대(int32_t file_hawakán){int item_COUNT=외부번호(file_hawakán);return item_COUNT<0||!전문외부상대[file_hawakán-32]?되돌림전문상대(file_hawakán):(int32_t)peer_numero_ng_port(item_COUNT);}
int32_t 자바전문원격주소(int32_t file_hawakán){int item_COUNT=외부번호(file_hawakán);return item_COUNT<0||!전문외부상대[file_hawakán-32]?0x7f000001:(int32_t)상대통신주소(item_COUNT);}
int32_t 자바전문닫기(int32_t file_hawakán){int item_COUNT=외부번호(file_hawakán);if(item_COUNT>=0){isara_Network(item_COUNT);외부연결[file_hawakán-32]=0;}if(file_hawakán>=32&&file_hawakán<40)전문외부상대[file_hawakán-32]=묶인주소[file_hawakán-32]=0;return 되돌림전문닫기(file_hawakán);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t file_hawakán,int32_t Internet_address,int32_t numero_ng_port){
    if(Internet_address==0||Internet_address==0x7f000001){int 반환값=되돌림흐름묶기(file_hawakán,Internet_address,numero_ng_port);if(!반환값)임의주소[file_hawakán-32]=Internet_address==0;return 반환값;}
    if(Internet_address!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(file_hawakán,0,numero_ng_port);if(반환값<0)return 반환값;
    int item_COUNT=I_paste_SMS(file_hawakán,1);return item_COUNT<0?item_COUNT:망주소묶기(item_COUNT,Internet_address,되돌림흐름접속번호(file_hawakán));
}
int32_t 자바흐름듣기(int32_t file_hawakán,int32_t 연결대기한도){
    int item_COUNT=외부번호(file_hawakán);if(item_COUNT<0){int 반환값=되돌림흐름듣기(file_hawakán,연결대기한도);if(반환값<0||!임의주소[file_hawakán-32])return 반환값;
        item_COUNT=I_paste_SMS(file_hawakán,1);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림흐름접속번호(file_hawakán));if(반환값<0)return 반환값;양쪽수신창구[file_hawakán-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(item_COUNT);
}
int32_t 자바흐름연결(int32_t file_hawakán,int32_t Internet_address,int32_t numero_ng_port){
    if(Internet_address==0x7f000001 && 외부번호(file_hawakán)<0)return 되돌림흐름연결(file_hawakán,Internet_address,numero_ng_port);
    if(되돌림흐름접속번호(file_hawakán)<0)return -9;int item_COUNT=I_paste_SMS(file_hawakán,1);return item_COUNT<0?item_COUNT:망연결하기(item_COUNT,Internet_address,numero_ng_port);
}
int32_t 자바흐름연결받기(int32_t file_hawakán){
    int item_COUNT=외부번호(file_hawakán);if(item_COUNT<0)return 되돌림흐름연결받기(file_hawakán);
    if(양쪽수신창구[file_hawakán-32]){int lokal=되돌림흐름연결받기(file_hawakán);if(lokal!=-11)return lokal;}
    int peer_VALUE=망연결받기(item_COUNT);if(peer_VALUE<0)return peer_VALUE;
    int layunin=되돌림흐름만들기();if(layunin<0){isara_Network(peer_VALUE);return layunin;}외부연결[layunin-32]=peer_VALUE+1;return layunin;
}
int32_t 자바흐름읽기(int32_t file_hawakán,int32_t sukat_82232621){
    int item_COUNT=외부번호(file_hawakán);if(item_COUNT<0)return 되돌림흐름읽기(file_hawakán,sukat_82232621);if(sukat_82232621<0||sukat_82232621>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(item_COUNT,data,sukat_82232621);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t file_hawakán,int32_t sukat_82232621){
    int item_COUNT=외부번호(file_hawakán);if(item_COUNT<0)return 되돌림흐름쓰기(file_hawakán,sukat_82232621);if(sukat_82232621<0||sukat_82232621>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<sukat_82232621;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(item_COUNT,data,sukat_82232621);
}
int32_t 자바흐름접속번호(int32_t file_hawakán){int item_COUNT=외부번호(file_hawakán);return item_COUNT<0?되돌림흐름접속번호(file_hawakán):(int32_t)Network_numero_ng_port(item_COUNT);}
int32_t 자바흐름상대(int32_t file_hawakán){int item_COUNT=외부번호(file_hawakán);return item_COUNT<0?되돌림흐름상대(file_hawakán):(int32_t)peer_numero_ng_port(item_COUNT);}
int32_t 자바흐름주소(int32_t file_hawakán){return 외부번호(file_hawakán)<0?0x7f000001:양쪽수신창구[file_hawakán-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t file_hawakán){int item_COUNT=외부번호(file_hawakán);if(item_COUNT>=0){isara_Network(item_COUNT);외부연결[file_hawakán-32]=0;}if(file_hawakán>=40&&file_hawakán<56)임의주소[file_hawakán-32]=양쪽수신창구[file_hawakán-32]=0;return 되돌림흐름닫기(file_hawakán);}
