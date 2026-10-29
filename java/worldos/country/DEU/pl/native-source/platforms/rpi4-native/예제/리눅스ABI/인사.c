/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEKS, long 가, long SEKUNDA_operand, long 다, long 라) {
    register long rejestr_zero __asm__("x0")=가, 저장기일 __asm__("x1")=SEKUNDA_operand;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEKS;
    __asm__ volatile("svc #0" : "+r"(rejestr_zero) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return rejestr_zero;
}
static int długość_WARTOŚĆ(const char *tekst) { int identyfikator=0;while(tekst[identyfikator])identyfikator++;return identyfikator; }
static int pozycja_wyjścia(const char *tekst) { int identyfikator=długość_WARTOŚĆ(tekst);return 호출(64,1,(long)tekst,identyfikator,0)==identyfikator; }
int main(int argument_ILE_LICZB,char **argumenty) {
    if(argument_ILE_LICZB!=2 || !argumenty[0] || !argumenty[1] || argumenty[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char treść_WARTOŚĆ_cb0f2404[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)treść_WARTOŚĆ_cb0f2404,sizeof(treść_WARTOŚĆ_cb0f2404)-1,0)!=sizeof(treść_WARTOŚĆ_cb0f2404)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(treść_WARTOŚĆ_cb0f2404)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(treść_WARTOŚĆ_cb0f2404)-1,0)!=sizeof(treść_WARTOŚĆ_cb0f2404)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(treść_WARTOŚĆ_cb0f2404);순번++)if(treść_WARTOŚĆ_cb0f2404[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long wartość_czasu[2];if(호출(113,1,(long)wartość_czasu,0,0) || wartość_czasu[1]<0 || wartość_czasu[1]>=1000000000)return 11;
    if(!pozycja_wyjścia("LINUX ARM64 ELF PASS\n") || !pozycja_wyjścia(argumenty[1]) || !pozycja_wyjścia("\n"))return 12;
    return 0;
}
