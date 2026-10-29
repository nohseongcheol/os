/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEX, long 가, long SEKUNDA_operand, long 다, long 라) {
    register long registr_nula __asm__("x0")=가, 저장기일 __asm__("x1")=SEKUNDA_operand;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEX;
    __asm__ volatile("svc #0" : "+r"(registr_nula) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return registr_nula;
}
static int délka_HODNOTA(const char *text) { int číslo=0;while(text[číslo])číslo++;return číslo; }
static int výstupní_pozice(const char *text) { int číslo=délka_HODNOTA(text);return 호출(64,1,(long)text,číslo,0)==číslo; }
int main(int argument_POČET,char **argumenty) {
    if(argument_POČET!=2 || !argumenty[0] || !argumenty[1] || argumenty[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Obsah_HODNOTA[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Obsah_HODNOTA,sizeof(Obsah_HODNOTA)-1,0)!=sizeof(Obsah_HODNOTA)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Obsah_HODNOTA)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(Obsah_HODNOTA)-1,0)!=sizeof(Obsah_HODNOTA)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Obsah_HODNOTA);순번++)if(Obsah_HODNOTA[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long časová_hodnota[2];if(호출(113,1,(long)časová_hodnota,0,0) || časová_hodnota[1]<0 || časová_hodnota[1]>=1000000000)return 11;
    if(!výstupní_pozice("LINUX ARM64 ELF PASS\n") || !výstupní_pozice(argumenty[1]) || !výstupní_pozice("\n"))return 12;
    return 0;
}
