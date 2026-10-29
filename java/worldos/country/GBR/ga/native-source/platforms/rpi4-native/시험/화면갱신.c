#include "../명명/기계연결이름.h"
#include "../meaisín/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t clár_Teirminéal(uintptr_t),clár_picteilín(uintptr_t,uintptr_t,uintptr_t);
extern void Teirminéal_pointeoir(unsigned,int,int),Teirminéal_beart(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    clár_pointeoir(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=clár_líníocht_COUNT();clár_Teirminéal(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(clár_líníocht_COUNT()==이전); /* 같은 화면을 다시 그려도 seó_VALUE 메모리에 쓰지 않는다. */
}
static void scríobh_SMS(const char *Téacs){while(*Téacs)Teirminéal_beart((unsigned char)*Téacs++);}
int main(void){
    clár_Ullmhaigh_líníocht(&화면[0][0],1920,1080,sizeof(화면[0]));
    clár_Teirminéal(300);scríobh_SMS("첫 창의 한글 sonraí\n");
    for(int INDEX=1;INDEX<4;INDEX++){clár_Teirminéal(1);clár_Teirminéal(100+INDEX);scríobh_SMS("겹친 창의 한글 sonraí\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Ingearach_suíomh=102,폭=568,높이=360;
    uint64_t bog_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Teirminéal_pointeoir(1,가로+100,Ingearach_suíomh+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        clár_picteilín(1900,1050,0x123456); /* athnuaigh 영역 밖의 úsáideoir líníocht_VALUE */
        uint64_t 이전=clár_líníocht_COUNT();clock_t Rith_2=clock();
        Teirminéal_pointeoir(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Rith_2)/CLOCKS_PER_SEC;
        bog_LOG+=clár_líníocht_COUNT()-이전;
        assert(clár_líníocht_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        clár_picteilín(1900,1050,0x302018);
        Teirminéal_pointeoir(0,새가로+100,새세로+15);가로=새가로;Ingearach_suíomh=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Ingearach_suíomh)새높이=1080-Ingearach_suíomh;
        Teirminéal_pointeoir(1,가로+폭-4,Ingearach_suíomh+높이-4);
        Teirminéal_pointeoir(1,가로+새폭-4,Ingearach_suíomh+새높이-4);
        uint64_t 이전=clár_líníocht_COUNT();
        Teirminéal_pointeoir(1,가로+새폭-4,Ingearach_suíomh+새높이-4);
        assert(clár_líníocht_COUNT()==이전); /* 같은 좌표의 중복 ócáid */
        Teirminéal_pointeoir(0,가로+새폭-4,Ingearach_suíomh+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 iarbhír_sonraí Líne 간격을 지킨다. */
    for(int Líne=0;Líne<1080;Líne++)for(int spás_iontráil=1920;spás_iontráil<1936;spás_iontráil++)assert(화면[Líne][spás_iontráil]==0);
    assert(!clár_Start_líníocht(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(bog_LOG/80));
    return 0;
}
