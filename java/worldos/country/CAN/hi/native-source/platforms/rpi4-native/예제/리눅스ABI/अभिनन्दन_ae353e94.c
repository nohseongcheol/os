/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long इंडेक्स, long 가, long 나, long 다, long 라) {
    register long रजिस्टर_शून्य __asm__("x0")=가, 저장기일 __asm__("x1")=나;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=इंडेक्स;
    __asm__ volatile("svc #0" : "+r"(रजिस्टर_शून्य) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return रजिस्टर_शून्य;
}
static int 길이(const char *पाठ) { int 수=0;while(पाठ[수])수++;return 수; }
static int निर्गम(const char *पाठ) { int 수=길이(पाठ);return 호출(64,1,(long)पाठ,수,0)==수; }
int main(int 인수수,char **तर्क) {
    if(인수수!=2 || !तर्क[0] || !तर्क[1] || तर्क[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char सामग्री_मान[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)सामग्री_मान,sizeof(सामग्री_मान)-1,0)!=sizeof(सामग्री_मान)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char पढें_पाठ_मान[sizeof(सामग्री_मान)]={0};
    if(호출(63,문서,(long)पढें_पाठ_मान,sizeof(सामग्री_मान)-1,0)!=sizeof(सामग्री_मान)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(सामग्री_मान);순번++)if(सामग्री_मान[순번]!=पढें_पाठ_मान[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long समय_उपयोगिता[2];if(호출(113,1,(long)समय_उपयोगिता,0,0) || समय_उपयोगिता[1]<0 || समय_उपयोगिता[1]>=1000000000)return 11;
    if(!निर्गम("LINUX ARM64 ELF PASS\n") || !निर्गम(तर्क[1]) || !निर्गम("\n"))return 12;
    return 0;
}
