/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long INDEX, long 가, long SECOND_operand, long 다, long 라) {
    register long register_null __asm__("x0")=가, 저장기일 __asm__("x1")=SECOND_operand;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=INDEX;
    __asm__ volatile("svc #0" : "+r"(register_null) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return register_null;
}
static int 길이(const char *Tekst) { int number=0;while(Tekst[number])number++;return number; }
static int Väljund(const char *Tekst) { int number=길이(Tekst);return 호출(64,1,(long)Tekst,number,0)==number; }
int main(int argument_COUNT,char **Argumendid) {
    if(argument_COUNT!=2 || !Argumendid[0] || !Argumendid[1] || Argumendid[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Sisu_VALUE[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Sisu_VALUE,sizeof(Sisu_VALUE)-1,0)!=sizeof(Sisu_VALUE)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Sisu_VALUE)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(Sisu_VALUE)-1,0)!=sizeof(Sisu_VALUE)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Sisu_VALUE);순번++)if(Sisu_VALUE[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long Aeg_VALUE[2];if(호출(113,1,(long)Aeg_VALUE,0,0) || Aeg_VALUE[1]<0 || Aeg_VALUE[1]>=1000000000)return 11;
    if(!Väljund("LINUX ARM64 ELF PASS\n") || !Väljund(Argumendid[1]) || !Väljund("\n"))return 12;
    return 0;
}
