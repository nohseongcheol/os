#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "jaringan_tumpuk.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int eksternal[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_eksternal_serekan[8], batas_surel[8];
static int 외부번호(int file_handel) { return file_handel>=32 && file_handel<56 ? eksternal[file_handel-32]-1 : -1; }
static int tempel_SMS(int file_handel,int TYPE_area) {
    if(file_handel<32||file_handel>=56)return -9;int 이전=외부번호(file_handel);if(이전>=0)return 이전;
    int item_COUNT=통신끝점만들기(TYPE_area);if(item_COUNT>=0)eksternal[file_handel-32]=item_COUNT+1;return item_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t kode_karakter){return 되돌림전문만들기(첫째값,SECOND_VALUE,kode_karakter);}
int32_t 자바전문묶기(int32_t file_handel,int32_t Alamat_internet,int32_t nomor_port){
    if(Alamat_internet==0x7f000001)return 되돌림전문묶기(file_handel,Alamat_internet,nomor_port);
    if(Alamat_internet!=0&&Alamat_internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(file_handel,0,nomor_port);if(반환값<0)return 반환값;
    int item_COUNT=tempel_SMS(file_handel,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(file_handel));if(!반환값)batas_surel[file_handel-32]=Alamat_internet;return 반환값;
}
int32_t 자바전문보내기(int32_t file_handel,int32_t Alamat_internet,int32_t nomor_port,int32_t Ukuran){
    if(Alamat_internet==0x7f000001)return 되돌림전문보내기(file_handel,Alamat_internet,nomor_port,Ukuran);
    if(Ukuran<0||Ukuran>512)return -90;if(nomor_port<1||nomor_port>65535)return -22;
    if(되돌림전문접속번호(file_handel)<0)return -9;
    if(되돌림전문주소(file_handel)==0x7f000001)return -101;
    int item_COUNT=외부번호(file_handel);if(item_COUNT<0){int 반환값=0;if(되돌림전문접속번호(file_handel)==0)반환값=되돌림전문묶기(file_handel,0,0);if(반환값<0)return 반환값;item_COUNT=tempel_SMS(file_handel,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(file_handel));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Ukuran;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(item_COUNT,data,Ukuran,Alamat_internet,nomor_port);
}
int32_t 자바전문받기(int32_t file_handel,int32_t Ukuran){
    int item_COUNT=외부번호(file_handel);if(item_COUNT<0)return 되돌림전문받기(file_handel,Ukuran);if(Ukuran<0||Ukuran>512)return -22;
    int lokal=되돌림전문받기(file_handel,Ukuran);if(lokal!=-11){UDP_eksternal_serekan[file_handel-32]=0;return lokal;}
    unsigned char data[512];int 반환값=전문받기(item_COUNT,data,Ukuran);if(반환값>=0)UDP_eksternal_serekan[file_handel-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t file_handel){int item_COUNT=외부번호(file_handel);return item_COUNT<0?되돌림전문접속번호(file_handel):(int32_t)jaringan_nomor_port(item_COUNT);}
int32_t 자바전문주소(int32_t file_handel){return 외부번호(file_handel)<0?되돌림전문주소(file_handel):batas_surel[file_handel-32];}
int32_t 자바전문상대(int32_t file_handel){int item_COUNT=외부번호(file_handel);return item_COUNT<0||!UDP_eksternal_serekan[file_handel-32]?되돌림전문상대(file_handel):(int32_t)serekan_nomor_port(item_COUNT);}
int32_t 자바전문원격주소(int32_t file_handel){int item_COUNT=외부번호(file_handel);return item_COUNT<0||!UDP_eksternal_serekan[file_handel-32]?0x7f000001:(int32_t)상대통신주소(item_COUNT);}
int32_t 자바전문닫기(int32_t file_handel){int item_COUNT=외부번호(file_handel);if(item_COUNT>=0){Tutup_jaringan(item_COUNT);eksternal[file_handel-32]=0;}if(file_handel>=32&&file_handel<40)UDP_eksternal_serekan[file_handel-32]=batas_surel[file_handel-32]=0;return 되돌림전문닫기(file_handel);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t file_handel,int32_t Alamat_internet,int32_t nomor_port){
    if(Alamat_internet==0||Alamat_internet==0x7f000001){int 반환값=되돌림흐름묶기(file_handel,Alamat_internet,nomor_port);if(!반환값)임의주소[file_handel-32]=Alamat_internet==0;return 반환값;}
    if(Alamat_internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(file_handel,0,nomor_port);if(반환값<0)return 반환값;
    int item_COUNT=tempel_SMS(file_handel,1);return item_COUNT<0?item_COUNT:망주소묶기(item_COUNT,Alamat_internet,되돌림흐름접속번호(file_handel));
}
int32_t 자바흐름듣기(int32_t file_handel,int32_t 연결대기한도){
    int item_COUNT=외부번호(file_handel);if(item_COUNT<0){int 반환값=되돌림흐름듣기(file_handel,연결대기한도);if(반환값<0||!임의주소[file_handel-32])return 반환값;
        item_COUNT=tempel_SMS(file_handel,1);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림흐름접속번호(file_handel));if(반환값<0)return 반환값;양쪽수신창구[file_handel-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(item_COUNT);
}
int32_t 자바흐름연결(int32_t file_handel,int32_t Alamat_internet,int32_t nomor_port){
    if(Alamat_internet==0x7f000001 && 외부번호(file_handel)<0)return 되돌림흐름연결(file_handel,Alamat_internet,nomor_port);
    if(되돌림흐름접속번호(file_handel)<0)return -9;int item_COUNT=tempel_SMS(file_handel,1);return item_COUNT<0?item_COUNT:망연결하기(item_COUNT,Alamat_internet,nomor_port);
}
int32_t 자바흐름연결받기(int32_t file_handel){
    int item_COUNT=외부번호(file_handel);if(item_COUNT<0)return 되돌림흐름연결받기(file_handel);
    if(양쪽수신창구[file_handel-32]){int lokal=되돌림흐름연결받기(file_handel);if(lokal!=-11)return lokal;}
    int serekan_VALUE=망연결받기(item_COUNT);if(serekan_VALUE<0)return serekan_VALUE;
    int target=되돌림흐름만들기();if(target<0){Tutup_jaringan(serekan_VALUE);return target;}eksternal[target-32]=serekan_VALUE+1;return target;
}
int32_t 자바흐름읽기(int32_t file_handel,int32_t Ukuran){
    int item_COUNT=외부번호(file_handel);if(item_COUNT<0)return 되돌림흐름읽기(file_handel,Ukuran);if(Ukuran<0||Ukuran>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(item_COUNT,data,Ukuran);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t file_handel,int32_t Ukuran){
    int item_COUNT=외부번호(file_handel);if(item_COUNT<0)return 되돌림흐름쓰기(file_handel,Ukuran);if(Ukuran<0||Ukuran>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Ukuran;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(item_COUNT,data,Ukuran);
}
int32_t 자바흐름접속번호(int32_t file_handel){int item_COUNT=외부번호(file_handel);return item_COUNT<0?되돌림흐름접속번호(file_handel):(int32_t)jaringan_nomor_port(item_COUNT);}
int32_t 자바흐름상대(int32_t file_handel){int item_COUNT=외부번호(file_handel);return item_COUNT<0?되돌림흐름상대(file_handel):(int32_t)serekan_nomor_port(item_COUNT);}
int32_t 자바흐름주소(int32_t file_handel){return 외부번호(file_handel)<0?0x7f000001:양쪽수신창구[file_handel-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t file_handel){int item_COUNT=외부번호(file_handel);if(item_COUNT>=0){Tutup_jaringan(item_COUNT);eksternal[file_handel-32]=0;}if(file_handel>=40&&file_handel<56)임의주소[file_handel-32]=양쪽수신창구[file_handel-32]=0;return 되돌림흐름닫기(file_handel);}
