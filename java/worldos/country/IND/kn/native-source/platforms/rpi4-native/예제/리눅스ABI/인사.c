/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long ಪದಸೂಚಿ, long 가, long 나, long 다, long 라) {
    register long 저장기영 __asm__("x0")=가, 저장기일 __asm__("x1")=나;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=ಪದಸೂಚಿ;
    __asm__ volatile("svc #0" : "+r"(저장기영) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return 저장기영;
}
static int ಉದ್ದ_ಮೌಲ್ಯ(const char *ಪಠ್ಯ) { int 수=0;while(ಪಠ್ಯ[수])수++;return 수; }
static int ಔಟ್_ಪುಟ್(const char *ಪಠ್ಯ) { int 수=ಉದ್ದ_ಮೌಲ್ಯ(ಪಠ್ಯ);return 호출(64,1,(long)ಪಠ್ಯ,수,0)==수; }
int main(int 인수수,char **인수) {
    if(인수수!=2 || !인수[0] || !인수[1] || 인수[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char ವಿಷಯ_ಮೌಲ್ಯ[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)ವಿಷಯ_ಮೌಲ್ಯ,sizeof(ವಿಷಯ_ಮೌಲ್ಯ)-1,0)!=sizeof(ವಿಷಯ_ಮೌಲ್ಯ)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(ವಿಷಯ_ಮೌಲ್ಯ)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(ವಿಷಯ_ಮೌಲ್ಯ)-1,0)!=sizeof(ವಿಷಯ_ಮೌಲ್ಯ)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(ವಿಷಯ_ಮೌಲ್ಯ);순번++)if(ವಿಷಯ_ಮೌಲ್ಯ[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long ಸಮಯ_ಮೌಲ್ಯ[2];if(호출(113,1,(long)ಸಮಯ_ಮೌಲ್ಯ,0,0) || ಸಮಯ_ಮೌಲ್ಯ[1]<0 || ಸಮಯ_ಮೌಲ್ಯ[1]>=1000000000)return 11;
    if(!ಔಟ್_ಪುಟ್("LINUX ARM64 ELF PASS\n") || !ಔಟ್_ಪುಟ್(인수[1]) || !ಔಟ್_ಪುಟ್("\n"))return 12;
    return 0;
}
