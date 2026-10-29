#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char танигч_утга[16];uint16_t бичих_ангилал,компьютер_бичих;uint32_t 판번호;uint64_t оролт_цэг,програм_Толгой_Оффсет,хэсэг_Толгой_Оффсет;uint32_t 설정비트;uint16_t Хэмжээ,програм_Толгой_хэмжээ,프로그램머리개수,хэсэг_Толгой_хэмжээ,구역머리개수,хэсэг_нэр_хүснэгт; } Толгой_утга;
typedef struct {uint32_t бичих_ангилал,설정비트;uint64_t Оффсет_утга,хаяг,물리주소,파일영역크기,기억영역크기,맞춤;} сегмент_утга;
static unsigned char зураг[16384];
static int нийтлэх_оролт(const char *Нэр){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(Толгой_утга))return -1;
    Толгой_утга 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.бичих_ангилал!=2||실행머리.компьютер_бичих!=183||실행머리.програм_Толгой_хэмжээ!=sizeof(сегмент_утга)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.програм_Толгой_Оффсет>개수||실행머리.프로그램머리개수*sizeof(сегмент_утга)>개수-실행머리.програм_Толгой_Оффсет)return -1;
    실행머리.програм_Толгой_Оффсет=sizeof(실행머리);실행머리.хэсэг_Толгой_Оффсет=실행머리.구역머리개수=실행머리.хэсэг_Толгой_хэмжээ=실행머리.хэсэг_нэр_хүснэгт=0;memcpy(зураг,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(сегмент_утга),다음=4096;unsigned char хуудас_Жагсаалт[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        сегмент_утга 자료위치;Толгой_утга 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.програм_Толгой_Оффсет+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Оффсет_утга>개수||자료위치.파일영역크기>개수-자료위치.Оффсет_утга||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.бичих_ангилал==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.хаяг<0x02000000||자료위치.хаяг>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.хаяг)return -1;
            if((자료위치.설정비트&1)&&실행머리.оролт_цэг>=자료위치.хаяг&&실행머리.оролт_цэг-자료위치.хаяг<자료위치.파일영역크기&&!(실행머리.оролт_цэг&3))진입점정상=1;
            size_t 선행값=자료위치.хаяг&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(зураг)||바이트들>sizeof(зураг)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(зураг));return -1;}
            if(바이트들)memcpy(зураг+다음+선행값,원본자료+자료위치.Оффсет_утга,자료위치.파일영역크기);
            자료위치.хаяг-=선행값;자료위치.물리주소=자료위치.хаяг;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Оффсет_утга=다음;자료위치.맞춤=4096;
            for(uint64_t хуудас_утга=자료위치.хаяг;хуудас_утга<자료위치.хаяг+자료위치.기억영역크기;хуудас_утга+=4096){unsigned 색인=(хуудас_утга-0x02000000)/4096;if(색인>=sizeof(хуудас_Жагсаалт)||хуудас_Жагсаалт[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}хуудас_Жагсаалт[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.бичих_ангилал==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(зураг+부가정보,원본자료+자료위치.Оффсет_утга,자료위치.파일영역크기);자료위치.Оффсет_утга=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.бичих_ангилал!=0&&자료위치.бичих_ангилал!=6&&자료위치.бичих_ангилал!=0x6474e551)return -1;
        memcpy(зураг+실행머리.програм_Толгой_Оффсет+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t файл_барих=사용자호출(3,(uintptr_t)Нэр,577,0600,0,0,0);if(файл_барих<0){printf("cc: cannot create output file, error %d\n",(int)файл_барих);return -1;}
    intptr_t 쓴수=사용자호출(1,файл_барих,(uintptr_t)зураг,다음,0,0,0);사용자호출(4,файл_барих,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Эхлэл_хэрэглэгч_програм(int арга_горим){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(арга_горим?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(арга_горим?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*мөр_өгөгдөл=tcc_new();if(!мөр_өгөгдөл)return 1;
    tcc_undefine_symbol(мөр_өгөгдөл,"__linux__");tcc_undefine_symbol(мөр_өгөгдөл,"__linux");tcc_undefine_symbol(мөр_өгөгдөл,"linux");
    tcc_undefine_symbol(мөр_өгөгдөл,"__unix__");tcc_undefine_symbol(мөр_өгөгдөл,"__unix");tcc_undefine_symbol(мөр_өгөгдөл,"unix");
    tcc_undefine_symbol(мөр_өгөгдөл,"__STDC_HOSTED__");tcc_define_symbol(мөр_өгөгдөл,"__STDC_HOSTED__","0");tcc_define_symbol(мөр_өгөгдөл,"__JKOROS__","1");
    tcc_set_options(мөр_өгөгдөл,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(мөр_өгөгдөл,"/sdk/include");
    int 반환값=tcc_set_output_type(мөр_өгөгдөл,TCC_OUTPUT_EXE);
    if(!반환값){if(арга_горим){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(мөр_өгөгдөл,원본자료):-1;}else 반환값=tcc_add_file(мөр_өгөгдөл,입력결과);}
    if(!반환값)반환값=tcc_add_file(мөр_өгөгдөл,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(мөр_өгөгдөл,"/sdk/lib/crt.o");
    if(!반환값&&арга_горим)반환값=tcc_add_file(мөр_өгөгдөл,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(мөр_өгөгдөл,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(мөр_өгөгдөл,"/@cc-output");
    if(!반환값)반환값=нийтлэх_оролт(출력결과);
    tcc_delete(мөр_өгөгдөл);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(арга_горим?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
