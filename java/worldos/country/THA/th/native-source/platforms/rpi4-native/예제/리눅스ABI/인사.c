/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long ดัชนี, long 가, long 나, long 다, long 라) {
    register long ทะเบียน_ศูนย์ __asm__("x0")=가, 저장기일 __asm__("x1")=나;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=ดัชนี;
    __asm__ volatile("svc #0" : "+r"(ทะเบียน_ศูนย์) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return ทะเบียน_ศูนย์;
}
static int 길이(const char *ข้อความ) { int หมายเลข=0;while(ข้อความ[หมายเลข])หมายเลข++;return หมายเลข; }
static int ข้อความออก(const char *ข้อความ) { int หมายเลข=길이(ข้อความ);return 호출(64,1,(long)ข้อความ,หมายเลข,0)==หมายเลข; }
int main(int 인수수,char **อาร์กิวเมนต์) {
    if(인수수!=2 || !อาร์กิวเมนต์[0] || !อาร์กิวเมนต์[1] || อาร์กิวเมนต์[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char เนื้อหา_ค่า[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)เนื้อหา_ค่า,sizeof(เนื้อหา_ค่า)-1,0)!=sizeof(เนื้อหา_ค่า)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char 읽은글[sizeof(เนื้อหา_ค่า)]={0};
    if(호출(63,문서,(long)읽은글,sizeof(เนื้อหา_ค่า)-1,0)!=sizeof(เนื้อหา_ค่า)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(เนื้อหา_ค่า);순번++)if(เนื้อหา_ค่า[순번]!=읽은글[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long ค่าเวลา[2];if(호출(113,1,(long)ค่าเวลา,0,0) || ค่าเวลา[1]<0 || ค่าเวลา[1]>=1000000000)return 11;
    if(!ข้อความออก("LINUX ARM64 ELF PASS\n") || !ข้อความออก(อาร์กิวเมนต์[1]) || !ข้อความออก("\n"))return 12;
    return 0;
}
