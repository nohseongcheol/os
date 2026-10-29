/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEX, long 가, long SECOND_operand, long 다, long 라) {
    register long registar_nula __asm__("x0")=가, 저장기일 __asm__("x1")=SECOND_operand;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEX;
    __asm__ volatile("svc #0" : "+r"(registar_nula) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return registar_nula;
}
static int 길이(const char *Tekst) { int 수=0;while(Tekst[수])수++;return 수; }
static int Izlaz(const char *Tekst) { int 수=길이(Tekst);return 호출(64,1,(long)Tekst,수,0)==수; }
int main(int argument_COUNT,char **Argumenti) {
    if(argument_COUNT!=2 || !Argumenti[0] || !Argumenti[1] || Argumenti[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Sadržaj_VALUE[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Sadržaj_VALUE,sizeof(Sadržaj_VALUE)-1,0)!=sizeof(Sadržaj_VALUE)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Sadržaj_VALUE)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(Sadržaj_VALUE)-1,0)!=sizeof(Sadržaj_VALUE)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Sadržaj_VALUE);순번++)if(Sadržaj_VALUE[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long TIME_VALUE[2];if(호출(113,1,(long)TIME_VALUE,0,0) || TIME_VALUE[1]<0 || TIME_VALUE[1]>=1000000000)return 11;
    if(!Izlaz("LINUX ARM64 ELF PASS\n") || !Izlaz(Argumenti[1]) || !Izlaz("\n"))return 12;
    return 0;
}
