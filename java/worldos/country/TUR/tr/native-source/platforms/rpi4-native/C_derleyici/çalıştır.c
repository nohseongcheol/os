#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_çıktı(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char tanımlayıcı_değer[16];uint16_t TÜR_alan,makine_TÜR;uint32_t sürüm_numarası;uint64_t giriş_noktası,program_Başlık_Ofset,bölüm_üst_bilgisi_Ofset;uint32_t Yapılandırma_BITS;uint16_t Boyut,program_Başlık_boyutlandırmak,program_Başlık_BAĞ_DEĞ_SAY,bölüm_üst_bilgisi_boyutlandırmak,bölüm_üst_bilgisi_BAĞ_DEĞ_SAY,bölüm_ad_tablo; } Başlık_değer;
typedef struct {uint32_t TÜR_alan,Yapılandırma_BITS;uint64_t Ofset_değer,ADRES,물리주소,파일영역크기,기억영역크기,hizalamak_sınır;} segment_değer;
static unsigned char RESİM[16384];
static int yayımlamak_girdi(const char *İsim){
    size_t öğe_BAĞ_DEĞ_SAY;const unsigned char*원본자료=C_çıktı(&öğe_BAĞ_DEĞ_SAY);if(öğe_BAĞ_DEĞ_SAY<sizeof(Başlık_değer))return -1;
    Başlık_değer yürütülebilir_Başlık;memcpy(&yürütülebilir_Başlık,원본자료,sizeof(yürütülebilir_Başlık));
    if(yürütülebilir_Başlık.TÜR_alan!=2||yürütülebilir_Başlık.makine_TÜR!=183||yürütülebilir_Başlık.program_Başlık_boyutlandırmak!=sizeof(segment_değer)||!yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY||yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY>16||yürütülebilir_Başlık.program_Başlık_Ofset>öğe_BAĞ_DEĞ_SAY||yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY*sizeof(segment_değer)>öğe_BAĞ_DEĞ_SAY-yürütülebilir_Başlık.program_Başlık_Ofset)return -1;
    yürütülebilir_Başlık.program_Başlık_Ofset=sizeof(yürütülebilir_Başlık);yürütülebilir_Başlık.bölüm_üst_bilgisi_Ofset=yürütülebilir_Başlık.bölüm_üst_bilgisi_BAĞ_DEĞ_SAY=yürütülebilir_Başlık.bölüm_üst_bilgisi_boyutlandırmak=yürütülebilir_Başlık.bölüm_ad_tablo=0;memcpy(RESİM,&yürütülebilir_Başlık,sizeof(yürütülebilir_Başlık));
    size_t 부가정보=sizeof(yürütülebilir_Başlık)+yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY*sizeof(segment_değer),Sonraki_öğe=4096;unsigned char sayfa_Liste[3072]={0};int geçerli_giriş_noktası=0;
    for(unsigned 순번=0;순번<yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY;순번++){
        segment_değer veri_konum;Başlık_değer 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&veri_konum,원본자료+원본.program_Başlık_Ofset+순번*sizeof(veri_konum),sizeof(veri_konum));
        if(veri_konum.Ofset_değer>öğe_BAĞ_DEĞ_SAY||veri_konum.파일영역크기>öğe_BAĞ_DEĞ_SAY-veri_konum.Ofset_değer||veri_konum.파일영역크기>veri_konum.기억영역크기)return -1;
        if(veri_konum.TÜR_alan==1){
            if((veri_konum.Yapılandırma_BITS&~7u)||!(veri_konum.Yapılandırma_BITS&4)||(veri_konum.Yapılandırma_BITS&3)==3||veri_konum.ADRES<0x02000000||veri_konum.ADRES>0x02c00000||veri_konum.기억영역크기>0x02c00000-veri_konum.ADRES)return -1;
            if((veri_konum.Yapılandırma_BITS&1)&&yürütülebilir_Başlık.giriş_noktası>=veri_konum.ADRES&&yürütülebilir_Başlık.giriş_noktası-veri_konum.ADRES<veri_konum.파일영역크기&&!(yürütülebilir_Başlık.giriş_noktası&3))geçerli_giriş_noktası=1;
            size_t 선행값=veri_konum.ADRES&4095,바이트들=veri_konum.파일영역크기?선행값+veri_konum.파일영역크기:0;
            if(Sonraki_öğe>sizeof(RESİM)||바이트들>sizeof(RESİM)-Sonraki_öğe){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Sonraki_öğe+바이트들),(unsigned)sizeof(RESİM));return -1;}
            if(바이트들)memcpy(RESİM+Sonraki_öğe+선행값,원본자료+veri_konum.Ofset_değer,veri_konum.파일영역크기);
            veri_konum.ADRES-=선행값;veri_konum.물리주소=veri_konum.ADRES;veri_konum.기억영역크기+=선행값;veri_konum.파일영역크기=바이트들;veri_konum.Ofset_değer=Sonraki_öğe;veri_konum.hizalamak_sınır=4096;
            for(uint64_t sayfa_değer=veri_konum.ADRES;sayfa_değer<veri_konum.ADRES+veri_konum.기억영역크기;sayfa_değer+=4096){unsigned ARA_Dizin=(sayfa_değer-0x02000000)/4096;if(ARA_Dizin>=sizeof(sayfa_Liste)||sayfa_Liste[ARA_Dizin]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}sayfa_Liste[ARA_Dizin]=1;}
            Sonraki_öğe+=(바이트들+4095)&~(size_t)4095;
        }else if(veri_konum.TÜR_alan==4){if(veri_konum.파일영역크기>4096-부가정보)return -1;memcpy(RESİM+부가정보,원본자료+veri_konum.Ofset_değer,veri_konum.파일영역크기);veri_konum.Ofset_değer=부가정보;부가정보+=veri_konum.파일영역크기;}
        else if(veri_konum.TÜR_alan!=0&&veri_konum.TÜR_alan!=6&&veri_konum.TÜR_alan!=0x6474e551)return -1;
        memcpy(RESİM+yürütülebilir_Başlık.program_Başlık_Ofset+순번*sizeof(veri_konum),&veri_konum,sizeof(veri_konum));
    }
    if(!geçerli_giriş_noktası)return -1;
    intptr_t dosya_tanıtıcısı=사용자호출(3,(uintptr_t)İsim,577,0600,0,0,0);if(dosya_tanıtıcısı<0){printf("cc: cannot create output file, error %d\n",(int)dosya_tanıtıcısı);return -1;}
    intptr_t 쓴수=사용자호출(1,dosya_tanıtıcısı,(uintptr_t)RESİM,Sonraki_öğe,0,0,0);사용자호출(4,dosya_tanıtıcısı,0,0,0,0,0);return 쓴수==(intptr_t)Sonraki_öğe?0:-1;
}
int Start_kullanıcı_program(int metot_mod){
    char artış[256],선택항목[256],çıktı[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metot_mod?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)artış,sizeof(artış),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(artış,"--version")||!strcmp(artış,"-version"))){printf(metot_mod?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)çıktı,sizeof(çıktı),0,0,0)<0)return 2;}
    if(!strcmp(artış,çıktı)){printf("cc: input and output must differ\n");return 2;}
    TCCState*dize_veri=tcc_new();if(!dize_veri)return 1;
    tcc_undefine_symbol(dize_veri,"__linux__");tcc_undefine_symbol(dize_veri,"__linux");tcc_undefine_symbol(dize_veri,"linux");
    tcc_undefine_symbol(dize_veri,"__unix__");tcc_undefine_symbol(dize_veri,"__unix");tcc_undefine_symbol(dize_veri,"unix");
    tcc_undefine_symbol(dize_veri,"__STDC_HOSTED__");tcc_define_symbol(dize_veri,"__STDC_HOSTED__","0");tcc_define_symbol(dize_veri,"__JKOROS__","1");
    tcc_set_options(dize_veri,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(dize_veri,"/sdk/include");
    int 반환값=tcc_set_output_type(dize_veri,TCC_OUTPUT_EXE);
    if(!반환값){if(metot_mod){const char*원본자료=자바미리번역원문(artış);반환값=원본자료?tcc_compile_string(dize_veri,원본자료):-1;}else 반환값=tcc_add_file(dize_veri,artış);}
    if(!반환값)반환값=tcc_add_file(dize_veri,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(dize_veri,"/sdk/lib/crt.o");
    if(!반환값&&metot_mod)반환값=tcc_add_file(dize_veri,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(dize_veri,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(dize_veri,"/@cc-output");
    if(!반환값)반환값=yayımlamak_girdi(çıktı);
    tcc_delete(dize_veri);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metot_mod?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",çıktı);return 0;
}
