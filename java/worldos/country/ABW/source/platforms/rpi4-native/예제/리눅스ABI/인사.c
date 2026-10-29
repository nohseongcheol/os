/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEX, long 가, long SECONDE_operand, long 다, long 라) {
    register long register_nul __asm__("x0")=가, 저장기일 __asm__("x1")=SECONDE_operand;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEX;
    __asm__ volatile("svc #0" : "+r"(register_nul) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return register_nul;
}
static int tijdsduur_WAARDE(const char *tekst) { int nummer=0;while(tekst[nummer])nummer++;return nummer; }
static int tekstuitvoer(const char *tekst) { int nummer=tijdsduur_WAARDE(tekst);return 호출(64,1,(long)tekst,nummer,0)==nummer; }
int main(int argument_AANTAL,char **argumenten) {
    if(argument_AANTAL!=2 || !argumenten[0] || !argumenten[1] || argumenten[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Inhoud_WAARDE[]="LINUX ELF FILE IO\n";
    long Guides=호출(56,-100,(long)"linux.txt",578,0600);
    if(Guides<0)return 5;
    if(호출(64,Guides,(long)Inhoud_WAARDE,sizeof(Inhoud_WAARDE)-1,0)!=sizeof(Inhoud_WAARDE)-1)return 6;
    if(호출(62,Guides,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Inhoud_WAARDE)]={0};
    if(호출(63,Guides,(long)읽은글,sizeof(Inhoud_WAARDE)-1,0)!=sizeof(Inhoud_WAARDE)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Inhoud_WAARDE);순번++)if(Inhoud_WAARDE[순번]!=읽은글[순번])return 9;
    if(호출(57,Guides,0,0,0))return 10;
    long TIJD_WAARDE[2];if(호출(113,1,(long)TIJD_WAARDE,0,0) || TIJD_WAARDE[1]<0 || TIJD_WAARDE[1]>=1000000000)return 11;
    if(!tekstuitvoer("LINUX ARM64 ELF PASS\n") || !tekstuitvoer(argumenten[1]) || !tekstuitvoer("\n"))return 12;
    return 0;
}
