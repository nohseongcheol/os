/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long અનુક્રમણિકા, long 가, long 나, long 다, long 라) {
    register long 저장기영 __asm__("x0")=가, 저장기일 __asm__("x1")=나;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=અનુક્રમણિકા;
    __asm__ volatile("svc #0" : "+r"(저장기영) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return 저장기영;
}
static int લંબાઈ_મૂલ્ય(const char *લખાણ) { int 수=0;while(લખાણ[수])수++;return 수; }
static int આઉટપુટ(const char *લખાણ) { int 수=લંબાઈ_મૂલ્ય(લખાણ);return 호출(64,1,(long)લખાણ,수,0)==수; }
int main(int 인수수,char **દલીલો) {
    if(인수수!=2 || !દલીલો[0] || !દલીલો[1] || દલીલો[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char સામગ્રી_મૂલ્ય[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)સામગ્રી_મૂલ્ય,sizeof(સામગ્રી_મૂલ્ય)-1,0)!=sizeof(સામગ્રી_મૂલ્ય)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(સામગ્રી_મૂલ્ય)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(સામગ્રી_મૂલ્ય)-1,0)!=sizeof(સામગ્રી_મૂલ્ય)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(સામગ્રી_મૂલ્ય);순번++)if(સામગ્રી_મૂલ્ય[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long સમય_મૂલ્ય[2];if(호출(113,1,(long)સમય_મૂલ્ય,0,0) || સમય_મૂલ્ય[1]<0 || સમય_મૂલ્ય[1]>=1000000000)return 11;
    if(!આઉટપુટ("LINUX ARM64 ELF PASS\n") || !આઉટપુટ(દલીલો[1]) || !આઉટપુટ("\n"))return 12;
    return 0;
}
