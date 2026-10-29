/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long Ευρετήριο, long 가, long 나, long 다, long 라) {
    register long δήλωση_μηδέν __asm__("x0")=가, 저장기일 __asm__("x1")=나;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=Ευρετήριο;
    __asm__ volatile("svc #0" : "+r"(δήλωση_μηδέν) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return δήλωση_μηδέν;
}
static int διάρκεια_τιμή(const char *Κείμενο) { int 수=0;while(Κείμενο[수])수++;return 수; }
static int Έξοδος(const char *Κείμενο) { int 수=διάρκεια_τιμή(Κείμενο);return 호출(64,1,(long)Κείμενο,수,0)==수; }
int main(int 인수수,char **Παράμετροι) {
    if(인수수!=2 || !Παράμετροι[0] || !Παράμετροι[1] || Παράμετροι[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Περιεχόμενο_τιμή[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Περιεχόμενο_τιμή,sizeof(Περιεχόμενο_τιμή)-1,0)!=sizeof(Περιεχόμενο_τιμή)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Περιεχόμενο_τιμή)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(Περιεχόμενο_τιμή)-1,0)!=sizeof(Περιεχόμενο_τιμή)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Περιεχόμενο_τιμή);순번++)if(Περιεχόμενο_τιμή[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long τιμή_ώρας[2];if(호출(113,1,(long)τιμή_ώρας,0,0) || τιμή_ώρας[1]<0 || τιμή_ώρας[1]>=1000000000)return 11;
    if(!Έξοδος("LINUX ARM64 ELF PASS\n") || !Έξοδος(Παράμετροι[1]) || !Έξοδος("\n"))return 12;
    return 0;
}
