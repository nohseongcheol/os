/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 調用(long 編號, long 首位操作數, long 第二操作數, long 第三操作數, long 第四操作數) {
    register long 寄存器零 __asm__("x0")=首位操作數, 寄存器一 __asm__("x1")=第二操作數;
    register long 寄存器二 __asm__("x2")=第三操作數, 寄存器三 __asm__("x3")=第四操作數;
    register long 寄存器八 __asm__("x8")=編號;
    __asm__ volatile("svc #0" : "+r"(寄存器零) : "r"(寄存器一),"r"(寄存器二),"r"(寄存器三),"r"(寄存器八) : "memory","cc");
    return 寄存器零;
}
static int 長度(const char *文本) { int 數=0;while(文本[數])數++;return 數; }
static int 輸出(const char *文本) { int 數=長度(文本);return 調用(64,1,(long)文本,數,0)==數; }
int main(int 實際參數個數,char **實參) {
    if(實際參數個數!=2 || !實參[0] || !實參[1] || 實參[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 是否不支持=調用(6,99,0,0,0);
    if(是否不支持!=-38 && 是否不支持!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(調用(64,1,0x80000,1,0)!=-14)return 4;
    const char 內容值[]="LINUX ELF FILE IO\n";
    long 文檔集=調用(56,-100,(long)"linux.txt",578,0600);
    if(文檔集<0)return 5;
    if(調用(64,文檔集,(long)內容值,sizeof(內容值)-1,0)!=sizeof(內容值)-1)return 6;
    if(調用(62,文檔集,0,0,0)!=0)return 7;
    char 讀取文本值[sizeof(內容值)]={0};
    if(調用(63,文檔集,(long)讀取文本值,sizeof(內容值)-1,0)!=sizeof(內容值)-1)return 8;
    for(unsigned 序數索引=0;序數索引<sizeof(內容值);序數索引++)if(內容值[序數索引]!=讀取文本值[序數索引])return 9;
    if(調用(57,文檔集,0,0,0))return 10;
    long 時間值[2];if(調用(113,1,(long)時間值,0,0) || 時間值[1]<0 || 時間值[1]>=1000000000)return 11;
    if(!輸出("LINUX ARM64 ELF PASS\n") || !輸出(實參[1]) || !輸出("\n"))return 12;
    return 0;
}
