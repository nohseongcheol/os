/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEX, long 가, long SEKUND_operand, long 다, long 라) {
    register long register_noll __asm__("x0")=가, 저장기일 __asm__("x1")=SEKUND_operand;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEX;
    __asm__ volatile("svc #0" : "+r"(register_noll) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return register_noll;
}
static int längd_värde(const char *text) { int nummer=0;while(text[nummer])nummer++;return nummer; }
static int utmatningsposition(const char *text) { int nummer=längd_värde(text);return 호출(64,1,(long)text,nummer,0)==nummer; }
int main(int argument_ANTAL,char **argument) {
    if(argument_ANTAL!=2 || !argument[0] || !argument[1] || argument[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Innehåll_värde[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Innehåll_värde,sizeof(Innehåll_värde)-1,0)!=sizeof(Innehåll_värde)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char läsa_SMS_värde[sizeof(Innehåll_värde)]={0};
    if(호출(63,문서,(long)läsa_SMS_värde,sizeof(Innehåll_värde)-1,0)!=sizeof(Innehåll_värde)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Innehåll_värde);순번++)if(Innehåll_värde[순번]!=läsa_SMS_värde[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long tid_värde[2];if(호출(113,1,(long)tid_värde,0,0) || tid_värde[1]<0 || tid_värde[1]>=1000000000)return 11;
    if(!utmatningsposition("LINUX ARM64 ELF PASS\n") || !utmatningsposition(argument[1]) || !utmatningsposition("\n"))return 12;
    return 0;
}
