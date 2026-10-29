/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEKS, long 가, long SEKUND_operand, long 다, long 라) {
    register long register_nul __asm__("x0")=가, 저장기일 __asm__("x1")=SEKUND_operand;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEKS;
    __asm__ volatile("svc #0" : "+r"(register_nul) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return register_nul;
}
static int varighed_VÆRDI(const char *Tekst) { int tal=0;while(Tekst[tal])tal++;return tal; }
static int Udgang(const char *Tekst) { int tal=varighed_VÆRDI(Tekst);return 호출(64,1,(long)Tekst,tal,0)==tal; }
int main(int argument_TÆL,char **Argumenter) {
    if(argument_TÆL!=2 || !Argumenter[0] || !Argumenter[1] || Argumenter[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Indhold_VÆRDI[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Indhold_VÆRDI,sizeof(Indhold_VÆRDI)-1,0)!=sizeof(Indhold_VÆRDI)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Indhold_VÆRDI)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(Indhold_VÆRDI)-1,0)!=sizeof(Indhold_VÆRDI)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Indhold_VÆRDI);순번++)if(Indhold_VÆRDI[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long TID_VÆRDI[2];if(호출(113,1,(long)TID_VÆRDI,0,0) || TID_VÆRDI[1]<0 || TID_VÆRDI[1]>=1000000000)return 11;
    if(!Udgang("LINUX ARM64 ELF PASS\n") || !Udgang(Argumenter[1]) || !Udgang("\n"))return 12;
    return 0;
}
