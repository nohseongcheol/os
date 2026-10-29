#include "예제규약.h"
#include <통신규약.h>
int main(int argumen_COUNT,char **인수) {
    if(argumen_COUNT!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        port_VALUE=port_VALUE*10+인수[1][수]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int peserta=cipta_peserta(awan_Keluarga,전문통신,전문전송규약);if(peserta<0)return 3;
    struct 인터넷통신주소 e_mel={0};e_mel.e_mel_Keluarga=awan_Keluarga;
    if(ikat_e_mel(peserta,(struct 통신주소 *)&e_mel,sizeof(e_mel))<0)return 4;
    e_mel.nombor_port=망차례짧은수(port_VALUE);e_mel.alamat_Internet.e_mel_VALUE=rangkaian_integer(0x0a000202);
    const char 전문[]="C UDP Malay (macrolanguage)";
    if(자료전문보내기(peserta,전문,sizeof(전문)-1,0,(struct 통신주소 *)&e_mel,sizeof(e_mel))!=sizeof(전문)-1)return 5;
    char balas[512];unsigned Jalan=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(peserta,balas,sizeof(balas),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Jalan)<700);
    Tutup_fail(peserta);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=balas[수])return 8;
    return 출력("C 네트워크 tentu_sahkan: UDP Malay (macrolanguage)\n");
}
