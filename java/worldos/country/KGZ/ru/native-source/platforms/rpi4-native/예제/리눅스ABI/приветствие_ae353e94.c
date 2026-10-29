/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long ИНДЕКС, long 가, long СЕКУНДЫ_операнд, long 다, long 라) {
    register long регистр_нуль __asm__("x0")=가, 저장기일 __asm__("x1")=СЕКУНДЫ_операнд;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=ИНДЕКС;
    __asm__ volatile("svc #0" : "+r"(регистр_нуль) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return регистр_нуль;
}
static int длина_ЗНАЧЕН(const char *текст) { int 수=0;while(текст[수])수++;return 수; }
static int текстовыйВывод(const char *текст) { int 수=длина_ЗНАЧЕН(текст);return 호출(64,1,(long)текст,수,0)==수; }
int main(int аргумент_СЧЁТ,char **аргументы) {
    if(аргумент_СЧЁТ!=2 || !аргументы[0] || !аргументы[1] || аргументы[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char контент_ЗНАЧЕН[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)контент_ЗНАЧЕН,sizeof(контент_ЗНАЧЕН)-1,0)!=sizeof(контент_ЗНАЧЕН)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char чтение_SMS_ЗНАЧЕН[sizeof(контент_ЗНАЧЕН)]={0};
    if(호출(63,문서,(long)чтение_SMS_ЗНАЧЕН,sizeof(контент_ЗНАЧЕН)-1,0)!=sizeof(контент_ЗНАЧЕН)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(контент_ЗНАЧЕН);순번++)if(контент_ЗНАЧЕН[순번]!=чтение_SMS_ЗНАЧЕН[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long значение_времени[2];if(호출(113,1,(long)значение_времени,0,0) || значение_времени[1]<0 || значение_времени[1]>=1000000000)return 11;
    if(!текстовыйВывод("LINUX ARM64 ELF PASS\n") || !текстовыйВывод(аргументы[1]) || !текстовыйВывод("\n"))return 12;
    return 0;
}
