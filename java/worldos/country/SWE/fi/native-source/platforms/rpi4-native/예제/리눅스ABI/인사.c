/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEKSI, long 가, long SEKUNNIT_operandi, long 다, long 라) {
    register long rekisteri_nolla __asm__("x0")=가, 저장기일 __asm__("x1")=SEKUNNIT_operandi;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEKSI;
    __asm__ volatile("svc #0" : "+r"(rekisteri_nolla) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return rekisteri_nolla;
}
static int kesto_ARVO(const char *teksti) { int numero=0;while(teksti[numero])numero++;return numero; }
static int tulostuspaikka(const char *teksti) { int numero=kesto_ARVO(teksti);return 호출(64,1,(long)teksti,numero,0)==numero; }
int main(int argumentti_LASKE,char **argumentit) {
    if(argumentti_LASKE!=2 || !argumentit[0] || !argumentit[1] || argumentit[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Sisältö_ARVO[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Sisältö_ARVO,sizeof(Sisältö_ARVO)-1,0)!=sizeof(Sisältö_ARVO)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char lukea_SMS_ARVO[sizeof(Sisältö_ARVO)]={0};
    if(호출(63,문서,(long)lukea_SMS_ARVO,sizeof(Sisältö_ARVO)-1,0)!=sizeof(Sisältö_ARVO)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Sisältö_ARVO);순번++)if(Sisältö_ARVO[순번]!=lukea_SMS_ARVO[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long AIKA_ARVO[2];if(호출(113,1,(long)AIKA_ARVO,0,0) || AIKA_ARVO[1]<0 || AIKA_ARVO[1]>=1000000000)return 11;
    if(!tulostuspaikka("LINUX ARM64 ELF PASS\n") || !tulostuspaikka(argumentit[1]) || !tulostuspaikka("\n"))return 12;
    return 0;
}
