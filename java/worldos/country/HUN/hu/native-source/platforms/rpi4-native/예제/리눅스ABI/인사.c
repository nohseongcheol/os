/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEX, long 가, long MPERC_operandus, long 다, long 라) {
    register long jegyzék_nulla __asm__("x0")=가, 저장기일 __asm__("x1")=MPERC_operandus;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEX;
    __asm__ volatile("svc #0" : "+r"(jegyzék_nulla) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return jegyzék_nulla;
}
static int hossz_ÉRTÉK(const char *Szöveg) { int szám=0;while(Szöveg[szám])szám++;return szám; }
static int Kimenet(const char *Szöveg) { int szám=hossz_ÉRTÉK(Szöveg);return 호출(64,1,(long)Szöveg,szám,0)==szám; }
int main(int argumentum_DARAB,char **Argumentumok) {
    if(argumentum_DARAB!=2 || !Argumentumok[0] || !Argumentumok[1] || Argumentumok[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Tartalom_ÉRTÉK[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Tartalom_ÉRTÉK,sizeof(Tartalom_ÉRTÉK)-1,0)!=sizeof(Tartalom_ÉRTÉK)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Tartalom_ÉRTÉK)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(Tartalom_ÉRTÉK)-1,0)!=sizeof(Tartalom_ÉRTÉK)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Tartalom_ÉRTÉK);순번++)if(Tartalom_ÉRTÉK[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long IDŐ_ÉRTÉK[2];if(호출(113,1,(long)IDŐ_ÉRTÉK,0,0) || IDŐ_ÉRTÉK[1]<0 || IDŐ_ÉRTÉK[1]>=1000000000)return 11;
    if(!Kimenet("LINUX ARM64 ELF PASS\n") || !Kimenet(Argumentumok[1]) || !Kimenet("\n"))return 12;
    return 0;
}
