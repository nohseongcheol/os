#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char መለያ_እሴት_5b7b8b77[16];uint16_t ተይብ_ምድብ,ማሽን_ተይብ;uint32_t 판번호;uint64_t ምዝግብ_ቦታ,ፕሮግራም_ርእስ_ዝንፍ,ክፍል_ርእስ_ዝንፍ;uint32_t ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት;uint16_t መጠን,ፕሮግራም_ርእስ_መጠን_ቀይር,프로그램머리개수,ክፍል_ርእስ_መጠን_ቀይር,구역머리개수,ክፍል_ስም_ሰንጠረዥ; } ርእስ_እሴት;
typedef struct {uint32_t ተይብ_ምድብ,ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት;uint64_t ዝንፍ_እሴት,አድራሻ,물리주소,파일영역크기,기억영역크기,맞춤;} ምድብ_እሴት_32e9301f;
static unsigned char ምስል[16384];
static int አትም_ምዝግብ(const char *ስም){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(ርእስ_እሴት))return -1;
    ርእስ_እሴት 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.ተይብ_ምድብ!=2||실행머리.ማሽን_ተይብ!=183||실행머리.ፕሮግራም_ርእስ_መጠን_ቀይር!=sizeof(ምድብ_እሴት_32e9301f)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.ፕሮግራም_ርእስ_ዝንፍ>개수||실행머리.프로그램머리개수*sizeof(ምድብ_እሴት_32e9301f)>개수-실행머리.ፕሮግራም_ርእስ_ዝንፍ)return -1;
    실행머리.ፕሮግራም_ርእስ_ዝንፍ=sizeof(실행머리);실행머리.ክፍል_ርእስ_ዝንፍ=실행머리.구역머리개수=실행머리.ክፍል_ርእስ_መጠን_ቀይር=실행머리.ክፍል_ስም_ሰንጠረዥ=0;memcpy(ምስል,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(ምድብ_እሴት_32e9301f),ቀጣይ_ንጥል_ነገር=4096;unsigned char ገጽ_ዝርዝር[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        ምድብ_እሴት_32e9301f ውሂብ_በቦታ_አስቀመጠ;ርእስ_እሴት 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&ውሂብ_በቦታ_አስቀመጠ,원본자료+원본.ፕሮግራም_ርእስ_ዝንፍ+순번*sizeof(ውሂብ_በቦታ_አስቀመጠ),sizeof(ውሂብ_በቦታ_አስቀመጠ));
        if(ውሂብ_በቦታ_አስቀመጠ.ዝንፍ_እሴት>개수||ውሂብ_በቦታ_አስቀመጠ.파일영역크기>개수-ውሂብ_በቦታ_አስቀመጠ.ዝንፍ_እሴት||ውሂብ_በቦታ_አስቀመጠ.파일영역크기>ውሂብ_በቦታ_አስቀመጠ.기억영역크기)return -1;
        if(ውሂብ_በቦታ_አስቀመጠ.ተይብ_ምድብ==1){
            if((ውሂብ_በቦታ_አስቀመጠ.ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት&~7u)||!(ውሂብ_በቦታ_አስቀመጠ.ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት&4)||(ውሂብ_በቦታ_አስቀመጠ.ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት&3)==3||ውሂብ_በቦታ_አስቀመጠ.አድራሻ<0x02000000||ውሂብ_በቦታ_አስቀመጠ.አድራሻ>0x02c00000||ውሂብ_በቦታ_አስቀመጠ.기억영역크기>0x02c00000-ውሂብ_በቦታ_አስቀመጠ.አድራሻ)return -1;
            if((ውሂብ_በቦታ_አስቀመጠ.ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት&1)&&실행머리.ምዝግብ_ቦታ>=ውሂብ_በቦታ_አስቀመጠ.አድራሻ&&실행머리.ምዝግብ_ቦታ-ውሂብ_በቦታ_አስቀመጠ.አድራሻ<ውሂብ_በቦታ_አስቀመጠ.파일영역크기&&!(실행머리.ምዝግብ_ቦታ&3))진입점정상=1;
            size_t 선행값=ውሂብ_በቦታ_አስቀመጠ.አድራሻ&4095,바이트들=ውሂብ_በቦታ_አስቀመጠ.파일영역크기?선행값+ውሂብ_በቦታ_አስቀመጠ.파일영역크기:0;
            if(ቀጣይ_ንጥል_ነገር>sizeof(ምስል)||바이트들>sizeof(ምስል)-ቀጣይ_ንጥል_ነገር){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(ቀጣይ_ንጥል_ነገር+바이트들),(unsigned)sizeof(ምስል));return -1;}
            if(바이트들)memcpy(ምስል+ቀጣይ_ንጥል_ነገር+선행값,원본자료+ውሂብ_በቦታ_አስቀመጠ.ዝንፍ_እሴት,ውሂብ_በቦታ_አስቀመጠ.파일영역크기);
            ውሂብ_በቦታ_አስቀመጠ.አድራሻ-=선행값;ውሂብ_በቦታ_አስቀመጠ.물리주소=ውሂብ_በቦታ_አስቀመጠ.አድራሻ;ውሂብ_በቦታ_አስቀመጠ.기억영역크기+=선행값;ውሂብ_በቦታ_አስቀመጠ.파일영역크기=바이트들;ውሂብ_በቦታ_አስቀመጠ.ዝንፍ_እሴት=ቀጣይ_ንጥል_ነገር;ውሂብ_በቦታ_አስቀመጠ.맞춤=4096;
            for(uint64_t ገጽ_እሴት=ውሂብ_በቦታ_አስቀመጠ.አድራሻ;ገጽ_እሴት<ውሂብ_በቦታ_አስቀመጠ.አድራሻ+ውሂብ_በቦታ_አስቀመጠ.기억영역크기;ገጽ_እሴት+=4096){unsigned ፍለጋ_መረጃ_ጠቆመ=(ገጽ_እሴት-0x02000000)/4096;if(ፍለጋ_መረጃ_ጠቆመ>=sizeof(ገጽ_ዝርዝር)||ገጽ_ዝርዝር[ፍለጋ_መረጃ_ጠቆመ]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ገጽ_ዝርዝር[ፍለጋ_መረጃ_ጠቆመ]=1;}
            ቀጣይ_ንጥል_ነገር+=(바이트들+4095)&~(size_t)4095;
        }else if(ውሂብ_በቦታ_አስቀመጠ.ተይብ_ምድብ==4){if(ውሂብ_በቦታ_አስቀመጠ.파일영역크기>4096-부가정보)return -1;memcpy(ምስል+부가정보,원본자료+ውሂብ_በቦታ_አስቀመጠ.ዝንፍ_እሴት,ውሂብ_በቦታ_አስቀመጠ.파일영역크기);ውሂብ_በቦታ_አስቀመጠ.ዝንፍ_እሴት=부가정보;부가정보+=ውሂብ_በቦታ_አስቀመጠ.파일영역크기;}
        else if(ውሂብ_በቦታ_አስቀመጠ.ተይብ_ምድብ!=0&&ውሂብ_በቦታ_አስቀመጠ.ተይብ_ምድብ!=6&&ውሂብ_በቦታ_አስቀመጠ.ተይብ_ምድብ!=0x6474e551)return -1;
        memcpy(ምስል+실행머리.ፕሮግራም_ርእስ_ዝንፍ+순번*sizeof(ውሂብ_በቦታ_አስቀመጠ),&ውሂብ_በቦታ_አስቀመጠ,sizeof(ውሂብ_በቦታ_አስቀመጠ));
    }
    if(!진입점정상)return -1;
    intptr_t ፋይል_እጀታ=사용자호출(3,(uintptr_t)ስም,577,0600,0,0,0);if(ፋይል_እጀታ<0){printf("cc: cannot create output file, error %d\n",(int)ፋይል_እጀታ);return -1;}
    intptr_t 쓴수=사용자호출(1,ፋይል_እጀታ,(uintptr_t)ምስል,ቀጣይ_ንጥል_ነገር,0,0,0);사용자호출(4,ፋይል_እጀታ,0,0,0,0,0);return 쓴수==(intptr_t)ቀጣይ_ንጥል_ነገር?0:-1;
}
int ጀምር_ተጠቃሚ_ፕሮግራም(int ስልት_ሁነታ){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(ስልት_ሁነታ?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(ስልት_ሁነታ?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*ኅብረቁምፊ_ውሂብ=tcc_new();if(!ኅብረቁምፊ_ውሂብ)return 1;
    tcc_undefine_symbol(ኅብረቁምፊ_ውሂብ,"__linux__");tcc_undefine_symbol(ኅብረቁምፊ_ውሂብ,"__linux");tcc_undefine_symbol(ኅብረቁምፊ_ውሂብ,"linux");
    tcc_undefine_symbol(ኅብረቁምፊ_ውሂብ,"__unix__");tcc_undefine_symbol(ኅብረቁምፊ_ውሂብ,"__unix");tcc_undefine_symbol(ኅብረቁምፊ_ውሂብ,"unix");
    tcc_undefine_symbol(ኅብረቁምፊ_ውሂብ,"__STDC_HOSTED__");tcc_define_symbol(ኅብረቁምፊ_ውሂብ,"__STDC_HOSTED__","0");tcc_define_symbol(ኅብረቁምፊ_ውሂብ,"__JKOROS__","1");
    tcc_set_options(ኅብረቁምፊ_ውሂብ,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(ኅብረቁምፊ_ውሂብ,"/sdk/include");
    int 반환값=tcc_set_output_type(ኅብረቁምፊ_ውሂብ,TCC_OUTPUT_EXE);
    if(!반환값){if(ስልት_ሁነታ){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(ኅብረቁምፊ_ውሂብ,원본자료):-1;}else 반환값=tcc_add_file(ኅብረቁምፊ_ውሂብ,입력결과);}
    if(!반환값)반환값=tcc_add_file(ኅብረቁምፊ_ውሂብ,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(ኅብረቁምፊ_ውሂብ,"/sdk/lib/crt.o");
    if(!반환값&&ስልት_ሁነታ)반환값=tcc_add_file(ኅብረቁምፊ_ውሂብ,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(ኅብረቁምፊ_ውሂብ,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(ኅብረቁምፊ_ውሂብ,"/@cc-output");
    if(!반환값)반환값=አትም_ምዝግብ(출력결과);
    tcc_delete(ኅብረቁምፊ_ውሂብ);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(ስልት_ሁነታ?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
