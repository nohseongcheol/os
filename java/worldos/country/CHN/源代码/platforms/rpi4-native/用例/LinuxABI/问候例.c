/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 调用(long 编号, long 首位操作数, long 第二操作数, long 第三操作数, long 第四操作数) {
    register long 寄存器零 __asm__("x0")=首位操作数, 寄存器一 __asm__("x1")=第二操作数;
    register long 寄存器二 __asm__("x2")=第三操作数, 寄存器三 __asm__("x3")=第四操作数;
    register long 寄存器八 __asm__("x8")=编号;
    __asm__ volatile("svc #0" : "+r"(寄存器零) : "r"(寄存器一),"r"(寄存器二),"r"(寄存器三),"r"(寄存器八) : "memory","cc");
    return 寄存器零;
}
static int 长度(const char *文本) { int 数=0;while(文本[数])数++;return 数; }
static int 输出(const char *文本) { int 数=长度(文本);return 调用(64,1,(long)文本,数,0)==数; }
int main(int 参数个数,char **实参) {
    if(参数个数!=2 || !实参[0] || !实参[1] || 实参[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 是否不支持=调用(6,99,0,0,0);
    if(是否不支持!=-38 && 是否不支持!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(调用(64,1,0x80000,1,0)!=-14)return 4;
    const char 内容值[]="LINUX ELF FILE IO\n";
    long 文档集=调用(56,-100,(long)"linux.txt",578,0600);
    if(文档集<0)return 5;
    if(调用(64,文档集,(long)内容值,sizeof(内容值)-1,0)!=sizeof(内容值)-1)return 6;
    if(调用(62,文档集,0,0,0)!=0)return 7;
    char 读取文本值[sizeof(内容值)]={0};
    if(调用(63,文档集,(long)读取文本值,sizeof(内容值)-1,0)!=sizeof(内容值)-1)return 8;
    for(unsigned 序数索引=0;序数索引<sizeof(内容值);序数索引++)if(内容值[序数索引]!=读取文本值[序数索引])return 9;
    if(调用(57,文档集,0,0,0))return 10;
    long 时间值[2];if(调用(113,1,(long)时间值,0,0) || 时间值[1]<0 || 时间值[1]>=1000000000)return 11;
    if(!输出("LINUX ARM64 ELF PASS\n") || !输出(实参[1]) || !输出("\n"))return 12;
    return 0;
}
