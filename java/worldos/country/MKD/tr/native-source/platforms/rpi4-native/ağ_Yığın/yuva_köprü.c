#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "ağ_Yığın.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int dış[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_dış_eş[8], sınır_ADRES[8];
static int 외부번호(int dosya_tanıtıcısı) { return dosya_tanıtıcısı>=32 && dosya_tanıtıcısı<56 ? dış[dosya_tanıtıcısı-32]-1 : -1; }
static int yapıştırmak_SMS(int dosya_tanıtıcısı,int TÜR_alan) {
    if(dosya_tanıtıcısı<32||dosya_tanıtıcısı>=56)return -9;int Önceki_öğe=외부번호(dosya_tanıtıcısı);if(Önceki_öğe>=0)return Önceki_öğe;
    int öğe_BAĞ_DEĞ_SAY=açmak_yuva_uç_nokta(TÜR_alan);if(öğe_BAĞ_DEĞ_SAY>=0)dış[dosya_tanıtıcısı-32]=öğe_BAĞ_DEĞ_SAY+1;return öğe_BAĞ_DEĞ_SAY;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SANİYE_değer,int32_t kod_noktası){return 되돌림전문만들기(첫째값,SANİYE_değer,kod_noktası);}
int32_t 자바전문묶기(int32_t dosya_tanıtıcısı,int32_t İnternet_adresi,int32_t bağlantı_noktası_numarası){
    if(İnternet_adresi==0x7f000001)return 되돌림전문묶기(dosya_tanıtıcısı,İnternet_adresi,bağlantı_noktası_numarası);
    if(İnternet_adresi!=0&&İnternet_adresi!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(dosya_tanıtıcısı,0,bağlantı_noktası_numarası);if(반환값<0)return 반환값;
    int öğe_BAĞ_DEĞ_SAY=yapıştırmak_SMS(dosya_tanıtıcısı,2);if(öğe_BAĞ_DEĞ_SAY<0)return öğe_BAĞ_DEĞ_SAY;반환값=NET_BIND(öğe_BAĞ_DEĞ_SAY,망상태읽기(0,0),되돌림전문접속번호(dosya_tanıtıcısı));if(!반환값)sınır_ADRES[dosya_tanıtıcısı-32]=İnternet_adresi;return 반환값;
}
int32_t 자바전문보내기(int32_t dosya_tanıtıcısı,int32_t İnternet_adresi,int32_t bağlantı_noktası_numarası,int32_t Boyut){
    if(İnternet_adresi==0x7f000001)return 되돌림전문보내기(dosya_tanıtıcısı,İnternet_adresi,bağlantı_noktası_numarası,Boyut);
    if(Boyut<0||Boyut>512)return -90;if(bağlantı_noktası_numarası<1||bağlantı_noktası_numarası>65535)return -22;
    if(되돌림전문접속번호(dosya_tanıtıcısı)<0)return -9;
    if(되돌림전문주소(dosya_tanıtıcısı)==0x7f000001)return -101;
    int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0){int 반환값=0;if(되돌림전문접속번호(dosya_tanıtıcısı)==0)반환값=되돌림전문묶기(dosya_tanıtıcısı,0,0);if(반환값<0)return 반환값;öğe_BAĞ_DEĞ_SAY=yapıştırmak_SMS(dosya_tanıtıcısı,2);if(öğe_BAĞ_DEĞ_SAY<0)return öğe_BAĞ_DEĞ_SAY;반환값=NET_BIND(öğe_BAĞ_DEĞ_SAY,망상태읽기(0,0),되돌림전문접속번호(dosya_tanıtıcısı));if(반환값<0)return 반환값;}
    unsigned char veri[512];for(int 순번=0;순번<Boyut;순번++)veri[순번]=자바전문얻기(순번);return göndermek_veri_birimi(öğe_BAĞ_DEĞ_SAY,veri,Boyut,İnternet_adresi,bağlantı_noktası_numarası);
}
int32_t 자바전문받기(int32_t dosya_tanıtıcısı,int32_t Boyut){
    int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0)return 되돌림전문받기(dosya_tanıtıcısı,Boyut);if(Boyut<0||Boyut>512)return -22;
    int yerel=되돌림전문받기(dosya_tanıtıcısı,Boyut);if(yerel!=-11){UDP_dış_eş[dosya_tanıtıcısı-32]=0;return yerel;}
    unsigned char veri[512];int 반환값=almak_veri_birimi(öğe_BAĞ_DEĞ_SAY,veri,Boyut);if(반환값>=0)UDP_dış_eş[dosya_tanıtıcısı-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,veri[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t dosya_tanıtıcısı){int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);return öğe_BAĞ_DEĞ_SAY<0?되돌림전문접속번호(dosya_tanıtıcısı):(int32_t)ağ_bağlantı_noktası_numarası(öğe_BAĞ_DEĞ_SAY);}
int32_t 자바전문주소(int32_t dosya_tanıtıcısı){return 외부번호(dosya_tanıtıcısı)<0?되돌림전문주소(dosya_tanıtıcısı):sınır_ADRES[dosya_tanıtıcısı-32];}
int32_t 자바전문상대(int32_t dosya_tanıtıcısı){int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);return öğe_BAĞ_DEĞ_SAY<0||!UDP_dış_eş[dosya_tanıtıcısı-32]?되돌림전문상대(dosya_tanıtıcısı):(int32_t)eş_bağlantı_noktası_numarası(öğe_BAĞ_DEĞ_SAY);}
int32_t 자바전문원격주소(int32_t dosya_tanıtıcısı){int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);return öğe_BAĞ_DEĞ_SAY<0||!UDP_dış_eş[dosya_tanıtıcısı-32]?0x7f000001:(int32_t)NET_eş_ADRES(öğe_BAĞ_DEĞ_SAY);}
int32_t 자바전문닫기(int32_t dosya_tanıtıcısı){int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY>=0){Kapat_ağ(öğe_BAĞ_DEĞ_SAY);dış[dosya_tanıtıcısı-32]=0;}if(dosya_tanıtıcısı>=32&&dosya_tanıtıcısı<40)UDP_dış_eş[dosya_tanıtıcısı-32]=sınır_ADRES[dosya_tanıtıcısı-32]=0;return 되돌림전문닫기(dosya_tanıtıcısı);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t dosya_tanıtıcısı,int32_t İnternet_adresi,int32_t bağlantı_noktası_numarası){
    if(İnternet_adresi==0||İnternet_adresi==0x7f000001){int 반환값=되돌림흐름묶기(dosya_tanıtıcısı,İnternet_adresi,bağlantı_noktası_numarası);if(!반환값)임의주소[dosya_tanıtıcısı-32]=İnternet_adresi==0;return 반환값;}
    if(İnternet_adresi!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(dosya_tanıtıcısı,0,bağlantı_noktası_numarası);if(반환값<0)return 반환값;
    int öğe_BAĞ_DEĞ_SAY=yapıştırmak_SMS(dosya_tanıtıcısı,1);return öğe_BAĞ_DEĞ_SAY<0?öğe_BAĞ_DEĞ_SAY:NET_BIND(öğe_BAĞ_DEĞ_SAY,İnternet_adresi,되돌림흐름접속번호(dosya_tanıtıcısı));
}
int32_t 자바흐름듣기(int32_t dosya_tanıtıcısı,int32_t Kapsam){
    int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0){int 반환값=되돌림흐름듣기(dosya_tanıtıcısı,Kapsam);if(반환값<0||!임의주소[dosya_tanıtıcısı-32])return 반환값;
        öğe_BAĞ_DEĞ_SAY=yapıştırmak_SMS(dosya_tanıtıcısı,1);if(öğe_BAĞ_DEĞ_SAY<0)return öğe_BAĞ_DEĞ_SAY;반환값=NET_BIND(öğe_BAĞ_DEĞ_SAY,망상태읽기(0,0),되돌림흐름접속번호(dosya_tanıtıcısı));if(반환값<0)return 반환값;양쪽수신창구[dosya_tanıtıcısı-32]=1;
    }return Kapsam<1?-22:NET_dinlemek(öğe_BAĞ_DEĞ_SAY);
}
int32_t 자바흐름연결(int32_t dosya_tanıtıcısı,int32_t İnternet_adresi,int32_t bağlantı_noktası_numarası){
    if(İnternet_adresi==0x7f000001 && 외부번호(dosya_tanıtıcısı)<0)return 되돌림흐름연결(dosya_tanıtıcısı,İnternet_adresi,bağlantı_noktası_numarası);
    if(되돌림흐름접속번호(dosya_tanıtıcısı)<0)return -9;int öğe_BAĞ_DEĞ_SAY=yapıştırmak_SMS(dosya_tanıtıcısı,1);return öğe_BAĞ_DEĞ_SAY<0?öğe_BAĞ_DEĞ_SAY:NET_bağla(öğe_BAĞ_DEĞ_SAY,İnternet_adresi,bağlantı_noktası_numarası);
}
int32_t 자바흐름연결받기(int32_t dosya_tanıtıcısı){
    int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0)return 되돌림흐름연결받기(dosya_tanıtıcısı);
    if(양쪽수신창구[dosya_tanıtıcısı-32]){int yerel=되돌림흐름연결받기(dosya_tanıtıcısı);if(yerel!=-11)return yerel;}
    int eş_değer=NET_kabul_etmek(öğe_BAĞ_DEĞ_SAY);if(eş_değer<0)return eş_değer;
    int hedef=되돌림흐름만들기();if(hedef<0){Kapat_ağ(eş_değer);return hedef;}dış[hedef-32]=eş_değer+1;return hedef;
}
int32_t 자바흐름읽기(int32_t dosya_tanıtıcısı,int32_t Boyut){
    int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0)return 되돌림흐름읽기(dosya_tanıtıcısı,Boyut);if(Boyut<0||Boyut>512)return -22;
    unsigned char veri[512];int 반환값=통신읽기(öğe_BAĞ_DEĞ_SAY,veri,Boyut);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,veri[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t dosya_tanıtıcısı,int32_t Boyut){
    int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0)return 되돌림흐름쓰기(dosya_tanıtıcısı,Boyut);if(Boyut<0||Boyut>512)return -22;
    unsigned char veri[512];for(int 순번=0;순번<Boyut;순번++)veri[순번]=자바전문얻기(순번);return NET_yazma(öğe_BAĞ_DEĞ_SAY,veri,Boyut);
}
int32_t 자바흐름접속번호(int32_t dosya_tanıtıcısı){int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);return öğe_BAĞ_DEĞ_SAY<0?되돌림흐름접속번호(dosya_tanıtıcısı):(int32_t)ağ_bağlantı_noktası_numarası(öğe_BAĞ_DEĞ_SAY);}
int32_t 자바흐름상대(int32_t dosya_tanıtıcısı){int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);return öğe_BAĞ_DEĞ_SAY<0?되돌림흐름상대(dosya_tanıtıcısı):(int32_t)eş_bağlantı_noktası_numarası(öğe_BAĞ_DEĞ_SAY);}
int32_t 자바흐름주소(int32_t dosya_tanıtıcısı){return 외부번호(dosya_tanıtıcısı)<0?0x7f000001:양쪽수신창구[dosya_tanıtıcısı-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t dosya_tanıtıcısı){int öğe_BAĞ_DEĞ_SAY=외부번호(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY>=0){Kapat_ağ(öğe_BAĞ_DEĞ_SAY);dış[dosya_tanıtıcısı-32]=0;}if(dosya_tanıtıcısı>=40&&dosya_tanıtıcısı<56)임의주소[dosya_tanıtıcısı-32]=양쪽수신창구[dosya_tanıtıcısı-32]=0;return 되돌림흐름닫기(dosya_tanıtıcısı);}
