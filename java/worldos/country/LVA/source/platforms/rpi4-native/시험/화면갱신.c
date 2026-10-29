#include "../명명/기계연결이름.h"
#include "../mašīna/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Panelis_Terminālis(uintptr_t),Panelis_attēla_elements(uintptr_t,uintptr_t,uintptr_t);
extern void Terminālis_rādītājs(unsigned,int,int),Terminālis_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Salīdzinājums_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Panelis_rādītājs(0,0,0);memcpy(Salīdzinājums_IMAGE,화면,sizeof(화면));
    uint64_t 이전=Panelis_zīmējums_COUNT();Panelis_Terminālis(3);
    assert(memcmp(Salīdzinājums_IMAGE,화면,sizeof(화면))==0);
    assert(Panelis_zīmējums_COUNT()==이전); /* 같은 화면을 mēģināt_vēlreiz_VALUE 그려도 rādīt_VALUE 메모리에 쓰지 않는다. */
}
static void rakstīšana_SMS(const char *Teksts){while(*Teksts)Terminālis_byte((unsigned char)*Teksts++);}
int main(void){
    Panelis_Sagatavot_zīmējums(&화면[0][0],1920,1080,sizeof(화면[0]));
    Panelis_Terminālis(300);rakstīšana_SMS("첫 창의 한글 dati\n");
    for(int INDEX=1;INDEX<4;INDEX++){Panelis_Terminālis(1);Panelis_Terminālis(100+INDEX);rakstīšana_SMS("겹친 창의 한글 dati\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,vertikāle_amats=102,폭=568,높이=360;
    uint64_t pārvietot_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminālis_rādītājs(1,가로+100,vertikāle_amats+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Panelis_attēla_elements(1900,1050,0x123456); /* atsvaidzināt reģions_VALUE 밖의 lietotājs zīmējums_VALUE */
        uint64_t 이전=Panelis_zīmējums_COUNT();clock_t Palaist=clock();
        Terminālis_rādītājs(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Palaist)/CLOCKS_PER_SEC;
        pārvietot_LOG+=Panelis_zīmējums_COUNT()-이전;
        assert(Panelis_zīmējums_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Panelis_attēla_elements(1900,1050,0x302018);
        Terminālis_rādītājs(0,새가로+100,새세로+15);가로=새가로;vertikāle_amats=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-vertikāle_amats)새높이=1080-vertikāle_amats;
        Terminālis_rādītājs(1,가로+폭-4,vertikāle_amats+높이-4);
        Terminālis_rādītājs(1,가로+새폭-4,vertikāle_amats+새높이-4);
        uint64_t 이전=Panelis_zīmējums_COUNT();
        Terminālis_rādītājs(1,가로+새폭-4,vertikāle_amats+새높이-4);
        assert(Panelis_zīmējums_COUNT()==이전); /* 같은 좌표의 중복 Notikums */
        Terminālis_rādītājs(0,가로+새폭-4,vertikāle_amats+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 faktisks_dati Līniju 간격을 지킨다. */
    for(int Līniju=0;Līniju<1080;Līniju++)for(int 칸=1920;칸<1936;칸++)assert(화면[Līniju][칸]==0);
    assert(!Panelis_Sākt_zīmējums(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(pārvietot_LOG/80));
    return 0;
}
