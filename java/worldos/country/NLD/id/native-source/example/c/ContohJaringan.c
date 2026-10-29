#include "예제규약.h"
#include <통신규약.h>
int main(int argumen_COUNT,char **argumen) {
    if(argumen_COUNT!=2)return keluaranTeks("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int 수=0;argumen[1][수];수++) {
        if(argumen[1][수]<'0'||argumen[1][수]>'9')return 2;
        port_VALUE=port_VALUE*10+argumen[1][수]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int peserta=Buat_peserta(cloud_famili,전문통신,전문전송규약);if(peserta<0)return 3;
    struct 인터넷통신주소 surel={0};surel.surel_famili=cloud_famili;
    if(ikat_surel(peserta,(struct 통신주소 *)&surel,sizeof(surel))<0)return 4;
    surel.nomor_port=망차례짧은수(port_VALUE);surel.Alamat_internet.surel_VALUE=jaringan_bilangan_bulat(0x0a000202);
    const char 전문[]="C UDP id";
    if(자료전문보내기(peserta,전문,sizeof(전문)-1,0,(struct 통신주소 *)&surel,sizeof(surel))!=sizeof(전문)-1)return 5;
    char balas[512];unsigned jalankan=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(peserta,balas,sizeof(balas),0,0,0);
        if(RECEIVED_COUNT<0&&nomor_kesalahan!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-jalankan)<700);
    Tutup_file(peserta);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=balas[수])return 8;
    return keluaranTeks("C 네트워크 periksa: UDP id\n");
}
