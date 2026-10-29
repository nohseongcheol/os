#include "../명명/기계연결이름.h"
#include "통신망.h"
#include "lwip/dns.h"
#include "../원격/암호기반.h"
static int 조회상태=-2;
static uint32_t 조회주소;
static uintptr_t 조회차례;
uint32_t 통신난수(void){uint32_t 값=0;원격난수((unsigned char*)&값,sizeof(값));return 값;}
static void 이름받음(const char *이름,const ip_addr_t *주소,void *차례){
    (void)이름;if((uintptr_t)차례!=조회차례)return;
    조회주소=주소?lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(주소))):0;
    조회상태=주소?0:-2;
}
int 이름서버설정(uint32_t 주소){
    if(!주소||(주소>>24)==127||(주소>>28)>=14)return -22;
    if(조회상태==-11)return -16;
    ip_addr_t 값;ip_addr_set_ip4_u32(&값,lwip_htonl(주소));dns_setserver(0,&값);return 0;
}
void 이름조회준비(void){이름서버설정(IP_CONFIG_DNS);}
int 이름조회시작(const unsigned char *자료,unsigned 길이){
    if(조회상태==-11)return -16;
    if(!자료||!길이||길이>253)return -22;
    char 이름[254];unsigned 칸=0;
    for(unsigned 자리=0;자리<길이;자리++){
        unsigned 글=자료[자리];if(글=='.'){if(!칸||이름[자리-1]=='-')return -22;칸=0;}
        else {if(!((글>='a'&&글<='z')||(글>='A'&&글<='Z')||(글>='0'&&글<='9')||글=='-')||(!칸&&글=='-')||++칸>63)return -22;}
        이름[자리]=(char)글;
    }
    if(!칸||이름[길이-1]=='-')return -22;이름[길이]=0;
    uint32_t 난수;if(원격난수((unsigned char*)&난수,sizeof(난수)))return -5;
    조회차례++;조회주소=0;조회상태=-11;ip_addr_t 주소;
    err_t 결과=dns_gethostbyname(이름,&주소,이름받음,(void*)조회차례);
    if(결과==ERR_OK){조회주소=lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&주소)));조회상태=0;}
    else if(결과!=ERR_INPROGRESS)조회상태=-5;
    return 조회상태;
}
uint32_t 이름조회읽기(unsigned 항목){if(항목==0)return 조회상태;if(항목==1)return 조회주소;if(항목==2)return lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(dns_getserver(0))));if(항목==3){조회차례++;조회상태=-110;조회주소=0;}return 0;}
