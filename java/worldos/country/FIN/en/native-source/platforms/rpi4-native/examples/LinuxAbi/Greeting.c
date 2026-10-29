/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long invoke(long index, long firstOperand, long secondOperand, long thirdOperand, long fourthOperand) {
    register long registerZero __asm__("x0")=firstOperand, registerOne __asm__("x1")=secondOperand;
    register long registerTwo __asm__("x2")=thirdOperand, registerThree __asm__("x3")=fourthOperand;
    register long registerEight __asm__("x8")=index;
    __asm__ volatile("svc #0" : "+r"(registerZero) : "r"(registerOne),"r"(registerTwo),"r"(registerThree),"r"(registerEight) : "memory","cc");
    return registerZero;
}
static int lengthValue(const char *text) { int number=0;while(text[number])number++;return number; }
static int Output(const char *text) { int number=lengthValue(text);return invoke(64,1,(long)text,number,0)==number; }
int main(int argumentCount,char **arguments) {
    if(argumentCount!=2 || !arguments[0] || !arguments[1] || arguments[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long isUnsupported=invoke(6,99,0,0,0);
    if(isUnsupported!=-38 && isUnsupported!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(invoke(64,1,0x80000,1,0)!=-14)return 4;
    const char contentValue[]="LINUX ELF FILE IO\n";
    long guides=invoke(56,-100,(long)"linux.txt",578,0600);
    if(guides<0)return 5;
    if(invoke(64,guides,(long)contentValue,sizeof(contentValue)-1,0)!=sizeof(contentValue)-1)return 6;
    if(invoke(62,guides,0,0,0)!=0)return 7;
    char readTextValue[sizeof(contentValue)]={0};
    if(invoke(63,guides,(long)readTextValue,sizeof(contentValue)-1,0)!=sizeof(contentValue)-1)return 8;
    for(unsigned ordinalIndex=0;ordinalIndex<sizeof(contentValue);ordinalIndex++)if(contentValue[ordinalIndex]!=readTextValue[ordinalIndex])return 9;
    if(invoke(57,guides,0,0,0))return 10;
    long timeValue[2];if(invoke(113,1,(long)timeValue,0,0) || timeValue[1]<0 || timeValue[1]>=1000000000)return 11;
    if(!Output("LINUX ARM64 ELF PASS\n") || !Output(arguments[1]) || !Output("\n"))return 12;
    return 0;
}
