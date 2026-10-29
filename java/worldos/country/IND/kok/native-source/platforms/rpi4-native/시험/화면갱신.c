#include "../명명/기계연결이름.h"
#include "../यंत्र/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t बोर्ड_टर्मिनल(uintptr_t),बोर्ड_पिक्सॅल(uintptr_t,uintptr_t,uintptr_t);
extern void टर्मिनल_पॉयंटर(unsigned,int,int),टर्मिनल_बायट(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    बोर्ड_पॉयंटर(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=बोर्ड_रेखाटन_COUNT();बोर्ड_टर्मिनल(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(बोर्ड_रेखाटन_COUNT()==이전); /* 같은 화면을 다시 그려도 शो_मोल 메모리에 쓰지 않는다. */
}
static void बरोवचें_SMS(const char *SMS){while(*SMS)टर्मिनल_बायट((unsigned char)*SMS++);}
int main(void){
    बोर्ड_तयार_करचें_रेखाटन(&화면[0][0],1920,1080,sizeof(화면[0]));
    बोर्ड_टर्मिनल(300);बरोवचें_SMS("첫 창의 한글 डेटा\n");
    for(int INDEX=1;INDEX<4;INDEX++){बोर्ड_टर्मिनल(1);बोर्ड_टर्मिनल(100+INDEX);बरोवचें_SMS("겹친 창의 한글 डेटा\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,उबें_स्थिती=102,폭=568,높이=360;
    uint64_t हालोवचें_LOG=0;double 이동시간=0;
    for(int SEQUENCE_मोल=0;SEQUENCE_मोल<80;SEQUENCE_मोल++){
        टर्मिनल_पॉयंटर(1,가로+100,उबें_स्थिती+15);
        int 새가로=80+(SEQUENCE_मोल*37)%850,새세로=50+(SEQUENCE_मोल*13)%450;
        बोर्ड_पिक्सॅल(1900,1050,0x123456); /* परतून_ताजें_करचें 영역 밖의 उपेगकर्तो रेखाटन_मोल */
        uint64_t 이전=बोर्ड_रेखाटन_COUNT();clock_t चलोवप=clock();
        टर्मिनल_पॉयंटर(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-चलोवप)/CLOCKS_PER_SEC;
        हालोवचें_LOG+=बोर्ड_रेखाटन_COUNT()-이전;
        assert(बोर्ड_रेखाटन_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        बोर्ड_पिक्सॅल(1900,1050,0x302018);
        टर्मिनल_पॉयंटर(0,새가로+100,새세로+15);가로=새가로;उबें_स्थिती=새세로;
        전체와비교();
    }
    for(int SEQUENCE_मोल=0;SEQUENCE_मोल<40;SEQUENCE_मोल++){
        int 새폭=360+(SEQUENCE_मोल*29)%700,새높이=216+(SEQUENCE_मोल*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-उबें_स्थिती)새높이=1080-उबें_स्थिती;
        टर्मिनल_पॉयंटर(1,가로+폭-4,उबें_स्थिती+높이-4);
        टर्मिनल_पॉयंटर(1,가로+새폭-4,उबें_स्थिती+새높이-4);
        uint64_t 이전=बोर्ड_रेखाटन_COUNT();
        टर्मिनल_पॉयंटर(1,가로+새폭-4,उबें_स्थिती+새높이-4);
        assert(बोर्ड_रेखाटन_COUNT()==이전); /* 같은 좌표의 중복 प्रसंग */
        टर्मिनल_पॉयंटर(0,가로+새폭-4,उबें_स्थिती+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 प्रत्यक्ष_डेटा रेग 간격을 지킨다. */
    for(int रेग=0;रेग<1080;रेग++)for(int स्लॉट_प्रवेश=1920;स्लॉट_प्रवेश<1936;स्लॉट_प्रवेश++)assert(화면[रेग][स्लॉट_प्रवेश]==0);
    assert(!बोर्ड_Start_रेखाटन(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(हालोवचें_LOG/80));
    return 0;
}
