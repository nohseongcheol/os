/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long індекс, long 가, long 나, long 다, long 라) {
    register long реєстр_нуль __asm__("x0")=가, 저장기일 __asm__("x1")=나;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=індекс;
    __asm__ volatile("svc #0" : "+r"(реєстр_нуль) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return реєстр_нуль;
}
static int 길이(const char *текст) { int 수=0;while(текст[수])수++;return 수; }
static int Вивід(const char *текст) { int 수=길이(текст);return 호출(64,1,(long)текст,수,0)==수; }
int main(int 인수수,char **аргументи) {
    if(인수수!=2 || !аргументи[0] || !аргументи[1] || аргументи[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Вміст_значення[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Вміст_значення,sizeof(Вміст_значення)-1,0)!=sizeof(Вміст_значення)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(Вміст_значення)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(Вміст_значення)-1,0)!=sizeof(Вміст_значення)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Вміст_значення);순번++)if(Вміст_значення[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long час_значення[2];if(호출(113,1,(long)час_значення,0,0) || час_значення[1]<0 || час_значення[1]>=1000000000)return 11;
    if(!Вивід("LINUX ARM64 ELF PASS\n") || !Вивід(аргументи[1]) || !Вивід("\n"))return 12;
    return 0;
}
