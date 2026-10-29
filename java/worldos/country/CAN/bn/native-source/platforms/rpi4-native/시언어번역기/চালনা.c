#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char সনাক্তকারী_মান[16];uint16_t টাইপ_করুন_বিভাগ,মেশিন_টাইপ_করুন;uint32_t 판번호;uint64_t ভুক্তি_বিন্দু,অ্যাপ_হেডার_অফসেট,শাখা_হেডার_অফসেট;uint32_t বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস;uint16_t আকার,অ্যাপ_হেডার_আয়তন,프로그램머리개수,শাখা_হেডার_আয়তন,구역머리개수,শাখা_নাম_সারণি; } হেডার_মান;
typedef struct {uint32_t টাইপ_করুন_বিভাগ,বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস;uint64_t অফসেট_মান,ইমেইল,물리주소,파일영역크기,기억영역크기,맞춤;} অংশ_মান;
static unsigned char ছবি[16384];
static int প্রকাশ_করা_ভুক্তি(const char *নাম){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(হেডার_মান))return -1;
    হেডার_মান 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.টাইপ_করুন_বিভাগ!=2||실행머리.মেশিন_টাইপ_করুন!=183||실행머리.অ্যাপ_হেডার_আয়তন!=sizeof(অংশ_মান)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.অ্যাপ_হেডার_অফসেট>개수||실행머리.프로그램머리개수*sizeof(অংশ_মান)>개수-실행머리.অ্যাপ_হেডার_অফসেট)return -1;
    실행머리.অ্যাপ_হেডার_অফসেট=sizeof(실행머리);실행머리.শাখা_হেডার_অফসেট=실행머리.구역머리개수=실행머리.শাখা_হেডার_আয়তন=실행머리.শাখা_নাম_সারণি=0;memcpy(ছবি,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(অংশ_মান),পরবর্তী_দফা=4096;unsigned char পৃষ্ঠা_তালিকা[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        অংশ_মান ডাটা_পদ;হেডার_মান 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&ডাটা_পদ,원본자료+원본.অ্যাপ_হেডার_অফসেট+순번*sizeof(ডাটা_পদ),sizeof(ডাটা_পদ));
        if(ডাটা_পদ.অফসেট_মান>개수||ডাটা_পদ.파일영역크기>개수-ডাটা_পদ.অফসেট_মান||ডাটা_পদ.파일영역크기>ডাটা_পদ.기억영역크기)return -1;
        if(ডাটা_পদ.টাইপ_করুন_বিভাগ==1){
            if((ডাটা_পদ.বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস&~7u)||!(ডাটা_পদ.বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস&4)||(ডাটা_পদ.বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস&3)==3||ডাটা_পদ.ইমেইল<0x02000000||ডাটা_পদ.ইমেইল>0x02c00000||ডাটা_পদ.기억영역크기>0x02c00000-ডাটা_পদ.ইমেইল)return -1;
            if((ডাটা_পদ.বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস&1)&&실행머리.ভুক্তি_বিন্দু>=ডাটা_পদ.ইমেইল&&실행머리.ভুক্তি_বিন্দু-ডাটা_পদ.ইমেইল<ডাটা_পদ.파일영역크기&&!(실행머리.ভুক্তি_বিন্দু&3))진입점정상=1;
            size_t 선행값=ডাটা_পদ.ইমেইল&4095,바이트들=ডাটা_পদ.파일영역크기?선행값+ডাটা_পদ.파일영역크기:0;
            if(পরবর্তী_দফা>sizeof(ছবি)||바이트들>sizeof(ছবি)-পরবর্তী_দফা){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(পরবর্তী_দফা+바이트들),(unsigned)sizeof(ছবি));return -1;}
            if(바이트들)memcpy(ছবি+পরবর্তী_দফা+선행값,원본자료+ডাটা_পদ.অফসেট_মান,ডাটা_পদ.파일영역크기);
            ডাটা_পদ.ইমেইল-=선행값;ডাটা_পদ.물리주소=ডাটা_পদ.ইমেইল;ডাটা_পদ.기억영역크기+=선행값;ডাটা_পদ.파일영역크기=바이트들;ডাটা_পদ.অফসেট_মান=পরবর্তী_দফা;ডাটা_পদ.맞춤=4096;
            for(uint64_t পৃষ্ঠা_মান=ডাটা_পদ.ইমেইল;পৃষ্ঠা_মান<ডাটা_পদ.ইমেইল+ডাটা_পদ.기억영역크기;পৃষ্ঠা_মান+=4096){unsigned লুকআপ_সূচি=(পৃষ্ঠা_মান-0x02000000)/4096;if(লুকআপ_সূচি>=sizeof(পৃষ্ঠা_তালিকা)||পৃষ্ঠা_তালিকা[লুকআপ_সূচি]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}পৃষ্ঠা_তালিকা[লুকআপ_সূচি]=1;}
            পরবর্তী_দফা+=(바이트들+4095)&~(size_t)4095;
        }else if(ডাটা_পদ.টাইপ_করুন_বিভাগ==4){if(ডাটা_পদ.파일영역크기>4096-부가정보)return -1;memcpy(ছবি+부가정보,원본자료+ডাটা_পদ.অফসেট_মান,ডাটা_পদ.파일영역크기);ডাটা_পদ.অফসেট_মান=부가정보;부가정보+=ডাটা_পদ.파일영역크기;}
        else if(ডাটা_পদ.টাইপ_করুন_বিভাগ!=0&&ডাটা_পদ.টাইপ_করুন_বিভাগ!=6&&ডাটা_পদ.টাইপ_করুন_বিভাগ!=0x6474e551)return -1;
        memcpy(ছবি+실행머리.অ্যাপ_হেডার_অফসেট+순번*sizeof(ডাটা_পদ),&ডাটা_পদ,sizeof(ডাটা_পদ));
    }
    if(!진입점정상)return -1;
    intptr_t ফাইল_হাতল=사용자호출(3,(uintptr_t)নাম,577,0600,0,0,0);if(ফাইল_হাতল<0){printf("cc: cannot create output file, error %d\n",(int)ফাইল_হাতল);return -1;}
    intptr_t 쓴수=사용자호출(1,ফাইল_হাতল,(uintptr_t)ছবি,পরবর্তী_দফা,0,0,0);사용자호출(4,ফাইল_হাতল,0,0,0,0,0);return 쓴수==(intptr_t)পরবর্তী_দফা?0:-1;
}
int শুরু_ব্যবহারকারী_অ্যাপ(int পদ্ধতি_মোড){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(পদ্ধতি_মোড?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(পদ্ধতি_মোড?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*স্ট্রিং_ডাটা=tcc_new();if(!স্ট্রিং_ডাটা)return 1;
    tcc_undefine_symbol(স্ট্রিং_ডাটা,"__linux__");tcc_undefine_symbol(স্ট্রিং_ডাটা,"__linux");tcc_undefine_symbol(স্ট্রিং_ডাটা,"linux");
    tcc_undefine_symbol(স্ট্রিং_ডাটা,"__unix__");tcc_undefine_symbol(স্ট্রিং_ডাটা,"__unix");tcc_undefine_symbol(স্ট্রিং_ডাটা,"unix");
    tcc_undefine_symbol(স্ট্রিং_ডাটা,"__STDC_HOSTED__");tcc_define_symbol(স্ট্রিং_ডাটা,"__STDC_HOSTED__","0");tcc_define_symbol(স্ট্রিং_ডাটা,"__JKOROS__","1");
    tcc_set_options(স্ট্রিং_ডাটা,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(স্ট্রিং_ডাটা,"/sdk/include");
    int 반환값=tcc_set_output_type(স্ট্রিং_ডাটা,TCC_OUTPUT_EXE);
    if(!반환값){if(পদ্ধতি_মোড){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(স্ট্রিং_ডাটা,원본자료):-1;}else 반환값=tcc_add_file(স্ট্রিং_ডাটা,입력결과);}
    if(!반환값)반환값=tcc_add_file(স্ট্রিং_ডাটা,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(স্ট্রিং_ডাটা,"/sdk/lib/crt.o");
    if(!반환값&&পদ্ধতি_মোড)반환값=tcc_add_file(স্ট্রিং_ডাটা,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(স্ট্রিং_ডাটা,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(স্ট্রিং_ডাটা,"/@cc-output");
    if(!반환값)반환값=প্রকাশ_করা_ভুক্তি(출력결과);
    tcc_delete(স্ট্রিং_ডাটা);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(পদ্ধতি_মোড?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
