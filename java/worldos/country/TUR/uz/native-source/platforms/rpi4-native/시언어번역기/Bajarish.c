#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VALUE[16];uint16_t TYPE_toifa,기계유형;uint32_t 판번호;uint64_t kiritish_nuqta,ilova_Sarlavha_OFFSET,bo_lim_Sarlavha_OFFSET;uint32_t tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati;uint16_t Hajmi,ilova_Sarlavha_o_lcham,ilova_Sarlavha_COUNT,bo_lim_Sarlavha_o_lcham,bo_lim_Sarlavha_COUNT,bo_lim_nom_jadval; } Sarlavha_VALUE;
typedef struct {uint32_t TYPE_toifa,tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati;uint64_t OFFSET_VALUE,manzil,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char rasm[16384];
static int joylash_kiritish(const char *Nomi){
    size_t element_COUNT;const unsigned char*원본자료=시언어출력(&element_COUNT);if(element_COUNT<sizeof(Sarlavha_VALUE))return -1;
    Sarlavha_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_toifa!=2||실행머리.기계유형!=183||실행머리.ilova_Sarlavha_o_lcham!=sizeof(segment_VALUE)||!실행머리.ilova_Sarlavha_COUNT||실행머리.ilova_Sarlavha_COUNT>16||실행머리.ilova_Sarlavha_OFFSET>element_COUNT||실행머리.ilova_Sarlavha_COUNT*sizeof(segment_VALUE)>element_COUNT-실행머리.ilova_Sarlavha_OFFSET)return -1;
    실행머리.ilova_Sarlavha_OFFSET=sizeof(실행머리);실행머리.bo_lim_Sarlavha_OFFSET=실행머리.bo_lim_Sarlavha_COUNT=실행머리.bo_lim_Sarlavha_o_lcham=실행머리.bo_lim_nom_jadval=0;memcpy(rasm,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.ilova_Sarlavha_COUNT*sizeof(segment_VALUE),Keyingi_element=4096;unsigned char sahifa_Ro_yxat[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.ilova_Sarlavha_COUNT;순번++){
        segment_VALUE ma_lumotlar_holat;Sarlavha_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&ma_lumotlar_holat,원본자료+원본.ilova_Sarlavha_OFFSET+순번*sizeof(ma_lumotlar_holat),sizeof(ma_lumotlar_holat));
        if(ma_lumotlar_holat.OFFSET_VALUE>element_COUNT||ma_lumotlar_holat.파일영역크기>element_COUNT-ma_lumotlar_holat.OFFSET_VALUE||ma_lumotlar_holat.파일영역크기>ma_lumotlar_holat.기억영역크기)return -1;
        if(ma_lumotlar_holat.TYPE_toifa==1){
            if((ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&~7u)||!(ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&4)||(ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&3)==3||ma_lumotlar_holat.manzil<0x02000000||ma_lumotlar_holat.manzil>0x02c00000||ma_lumotlar_holat.기억영역크기>0x02c00000-ma_lumotlar_holat.manzil)return -1;
            if((ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&1)&&실행머리.kiritish_nuqta>=ma_lumotlar_holat.manzil&&실행머리.kiritish_nuqta-ma_lumotlar_holat.manzil<ma_lumotlar_holat.파일영역크기&&!(실행머리.kiritish_nuqta&3))진입점정상=1;
            size_t 선행값=ma_lumotlar_holat.manzil&4095,바이트들=ma_lumotlar_holat.파일영역크기?선행값+ma_lumotlar_holat.파일영역크기:0;
            if(Keyingi_element>sizeof(rasm)||바이트들>sizeof(rasm)-Keyingi_element){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Keyingi_element+바이트들),(unsigned)sizeof(rasm));return -1;}
            if(바이트들)memcpy(rasm+Keyingi_element+선행값,원본자료+ma_lumotlar_holat.OFFSET_VALUE,ma_lumotlar_holat.파일영역크기);
            ma_lumotlar_holat.manzil-=선행값;ma_lumotlar_holat.물리주소=ma_lumotlar_holat.manzil;ma_lumotlar_holat.기억영역크기+=선행값;ma_lumotlar_holat.파일영역크기=바이트들;ma_lumotlar_holat.OFFSET_VALUE=Keyingi_element;ma_lumotlar_holat.맞춤=4096;
            for(uint64_t sahifa_VALUE=ma_lumotlar_holat.manzil;sahifa_VALUE<ma_lumotlar_holat.manzil+ma_lumotlar_holat.기억영역크기;sahifa_VALUE+=4096){unsigned LOOKUP_INDEX=(sahifa_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(sahifa_Ro_yxat)||sahifa_Ro_yxat[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}sahifa_Ro_yxat[LOOKUP_INDEX]=1;}
            Keyingi_element+=(바이트들+4095)&~(size_t)4095;
        }else if(ma_lumotlar_holat.TYPE_toifa==4){if(ma_lumotlar_holat.파일영역크기>4096-부가정보)return -1;memcpy(rasm+부가정보,원본자료+ma_lumotlar_holat.OFFSET_VALUE,ma_lumotlar_holat.파일영역크기);ma_lumotlar_holat.OFFSET_VALUE=부가정보;부가정보+=ma_lumotlar_holat.파일영역크기;}
        else if(ma_lumotlar_holat.TYPE_toifa!=0&&ma_lumotlar_holat.TYPE_toifa!=6&&ma_lumotlar_holat.TYPE_toifa!=0x6474e551)return -1;
        memcpy(rasm+실행머리.ilova_Sarlavha_OFFSET+순번*sizeof(ma_lumotlar_holat),&ma_lumotlar_holat,sizeof(ma_lumotlar_holat));
    }
    if(!진입점정상)return -1;
    intptr_t fayl_deskriptor=사용자호출(3,(uintptr_t)Nomi,577,0600,0,0,0);if(fayl_deskriptor<0){printf("cc: cannot create output file, error %d\n",(int)fayl_deskriptor);return -1;}
    intptr_t 쓴수=사용자호출(1,fayl_deskriptor,(uintptr_t)rasm,Keyingi_element,0,0,0);사용자호출(4,fayl_deskriptor,0,0,0,0,0);return 쓴수==(intptr_t)Keyingi_element?0:-1;
}
int Start_foydalanuvchi_ilova(int uslub_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(uslub_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(uslub_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*satr_ma_lumotlar=tcc_new();if(!satr_ma_lumotlar)return 1;
    tcc_undefine_symbol(satr_ma_lumotlar,"__linux__");tcc_undefine_symbol(satr_ma_lumotlar,"__linux");tcc_undefine_symbol(satr_ma_lumotlar,"linux");
    tcc_undefine_symbol(satr_ma_lumotlar,"__unix__");tcc_undefine_symbol(satr_ma_lumotlar,"__unix");tcc_undefine_symbol(satr_ma_lumotlar,"unix");
    tcc_undefine_symbol(satr_ma_lumotlar,"__STDC_HOSTED__");tcc_define_symbol(satr_ma_lumotlar,"__STDC_HOSTED__","0");tcc_define_symbol(satr_ma_lumotlar,"__JKOROS__","1");
    tcc_set_options(satr_ma_lumotlar,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(satr_ma_lumotlar,"/sdk/include");
    int 반환값=tcc_set_output_type(satr_ma_lumotlar,TCC_OUTPUT_EXE);
    if(!반환값){if(uslub_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(satr_ma_lumotlar,원본자료):-1;}else 반환값=tcc_add_file(satr_ma_lumotlar,입력결과);}
    if(!반환값)반환값=tcc_add_file(satr_ma_lumotlar,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(satr_ma_lumotlar,"/sdk/lib/crt.o");
    if(!반환값&&uslub_MODE)반환값=tcc_add_file(satr_ma_lumotlar,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(satr_ma_lumotlar,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(satr_ma_lumotlar,"/@cc-output");
    if(!반환값)반환값=joylash_kiritish(출력결과);
    tcc_delete(satr_ma_lumotlar);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(uslub_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
