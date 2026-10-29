/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long فهرس, long 가, long 나, long 다, long 라) {
    register long سجل_صفر __asm__("x0")=가, 저장기일 __asm__("x1")=나;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=فهرس;
    __asm__ volatile("svc #0" : "+r"(سجل_صفر) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return سجل_صفر;
}
static int 길이(const char *نص) { int رقم=0;while(نص[رقم])رقم++;return رقم; }
static int مخرجات(const char *نص) { int رقم=길이(نص);return 호출(64,1,(long)نص,رقم,0)==رقم; }
int main(int 인수수,char **وسائط) {
    if(인수수!=2 || !وسائط[0] || !وسائط[1] || وسائط[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char محتوى_قيمة[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)محتوى_قيمة,sizeof(محتوى_قيمة)-1,0)!=sizeof(محتوى_قيمة)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char يقرأ_نص_قيمة[sizeof(محتوى_قيمة)]={0};
    if(호출(63,문서,(long)يقرأ_نص_قيمة,sizeof(محتوى_قيمة)-1,0)!=sizeof(محتوى_قيمة)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(محتوى_قيمة);순번++)if(محتوى_قيمة[순번]!=يقرأ_نص_قيمة[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long قيمة_الوقت[2];if(호출(113,1,(long)قيمة_الوقت,0,0) || قيمة_الوقت[1]<0 || قيمة_الوقت[1]>=1000000000)return 11;
    if(!مخرجات("LINUX ARM64 ELF PASS\n") || !مخرجات(وسائط[1]) || !مخرجات("\n"))return 12;
    return 0;
}
