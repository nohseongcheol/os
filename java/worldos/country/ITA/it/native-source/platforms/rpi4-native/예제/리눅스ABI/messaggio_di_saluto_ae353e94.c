/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDICE, long 가, long SECONDO_operando, long 다, long 라) {
    register long registro_zero __asm__("x0")=가, 저장기일 __asm__("x1")=SECONDO_operando;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDICE;
    __asm__ volatile("svc #0" : "+r"(registro_zero) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return registro_zero;
}
static int durata_VALORE(const char *testo) { int numero=0;while(testo[numero])numero++;return numero; }
static int uscitaTesto(const char *testo) { int numero=durata_VALORE(testo);return 호출(64,1,(long)testo,numero,0)==numero; }
int main(int argomento_CONTA_NUMERI,char **argomenti) {
    if(argomento_CONTA_NUMERI!=2 || !argomenti[0] || !argomenti[1] || argomenti[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Contenuto_VALORE[]="LINUX ELF FILE IO\n";
    long Guides=호출(56,-100,(long)"linux.txt",578,0600);
    if(Guides<0)return 5;
    if(호출(64,Guides,(long)Contenuto_VALORE,sizeof(Contenuto_VALORE)-1,0)!=sizeof(Contenuto_VALORE)-1)return 6;
    if(호출(62,Guides,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Contenuto_VALORE)]={0};
    if(호출(63,Guides,(long)읽은글,sizeof(Contenuto_VALORE)-1,0)!=sizeof(Contenuto_VALORE)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Contenuto_VALORE);순번++)if(Contenuto_VALORE[순번]!=읽은글[순번])return 9;
    if(호출(57,Guides,0,0,0))return 10;
    long valore[2];if(호출(113,1,(long)valore,0,0) || valore[1]<0 || valore[1]>=1000000000)return 11;
    if(!uscitaTesto("LINUX ARM64 ELF PASS\n") || !uscitaTesto(argomenti[1]) || !uscitaTesto("\n"))return 12;
    return 0;
}
