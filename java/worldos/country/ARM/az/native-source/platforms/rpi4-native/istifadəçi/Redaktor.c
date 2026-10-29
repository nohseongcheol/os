/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Mətn[편집용량],qaytarmaq_verilənlər[편집용량],복사자료[편집용량],ölçü_verilənlər[1024];
static int uzunluq_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,əlavə_etmək,qaytarmaq_uzunluq,위쪽,qaytarmaq_Dəyişikliklər,되돌림있음,nümunə_uzunluq,사용량,COLUMNS=68,ROW_COUNT=19;
static char fayl_daxiletmə_ad[64],Əmr[128],FIND_daxiletmə[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned gözləyir_Açar;
static int kömək_sahə,vəziyyət_IMAGE,vəziyyət_növbə;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)ölçü_verilənlər,사용량,0,0,0);사용량=0;}}
static void bayt_verilənlər(unsigned simvol_kodu){if(vəziyyət_IMAGE){if((simvol_kodu&192)!=128){vəziyyət_növbə+=simvol_kodu>=196?2:1;}if(vəziyyət_növbə>=COLUMNS)return;}if(사용량==(int)sizeof(ölçü_verilənlər))출력비우기();ölçü_verilənlər[사용량++]=simvol_kodu;}
static void 글내보내기(const char *sətir_verilənlər){while(*sətir_verilənlər)bayt_verilənlər((unsigned char)*sətir_verilənlər++);}
static void 수치(unsigned element_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+element_COUNT%10;element_COUNT/=10;}while(element_COUNT);while(순번)bayt_verilənlər(SECOND_VALUE[--순번]);}
static void hərəkət_etdir_VALUE(int ROW_yerinə_qoymaq,int sütun_yerinə_qoymaq){글내보내기("\033[");수치(ROW_yerinə_qoymaq);bayt_verilənlər(';');수치(sütun_yerinə_qoymaq);bayt_verilənlər('H');}
static int 이전항목(int verilənlər_yerinə_qoymaq){if(verilənlər_yerinə_qoymaq){verilənlər_yerinə_qoymaq--;while(verilənlər_yerinə_qoymaq>0&&(Mətn[verilənlər_yerinə_qoymaq]&192)==128)verilənlər_yerinə_qoymaq--;}return verilənlər_yerinə_qoymaq;}
static int Sonrakı_element(int verilənlər_yerinə_qoymaq){if(verilənlər_yerinə_qoymaq<uzunluq_VALUE){verilənlər_yerinə_qoymaq++;while(verilənlər_yerinə_qoymaq<uzunluq_VALUE&&(Mətn[verilənlər_yerinə_qoymaq]&192)==128)verilənlər_yerinə_qoymaq++;}return verilənlər_yerinə_qoymaq;}
static int İcra_Et(int verilənlər_yerinə_qoymaq){while(verilənlər_yerinə_qoymaq>0&&Mətn[verilənlər_yerinə_qoymaq-1]!='\n')verilənlər_yerinə_qoymaq--;return verilənlər_yerinə_qoymaq;}
static int bitirmək_OFFSET(int verilənlər_yerinə_qoymaq){while(verilənlər_yerinə_qoymaq<uzunluq_VALUE&&Mətn[verilənlər_yerinə_qoymaq]!='\n')verilənlər_yerinə_qoymaq++;return verilənlər_yerinə_qoymaq;}
static int 너비(unsigned simvol_kodu){return simvol_kodu>=196?2:1;}
static int sütun(int verilənlər_yerinə_qoymaq){int simvol_kodu=0;for(int 순번=İcra_Et(verilənlər_yerinə_qoymaq);순번<verilənlər_yerinə_qoymaq;순번=Sonrakı_element(순번))simvol_kodu+=Mətn[순번]=='\t'?4-simvol_kodu%4:너비(Mətn[순번]);return simvol_kodu;}
static void nəzarət_nöqtəsi(void){for(int 순번=0;순번<uzunluq_VALUE;순번++)qaytarmaq_verilənlər[순번]=Mətn[순번];qaytarmaq_uzunluq=uzunluq_VALUE;위쪽=INDEX_VALUE;qaytarmaq_Dəyişikliklər=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){nəzarət_nöqtəsi();for(int 순번=도착위치;순번<uzunluq_VALUE;순번++)Mətn[출발위치+순번-도착위치]=Mətn[순번];uzunluq_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *sətir_verilənlər,int element_COUNT){if(element_COUNT>편집용량-uzunluq_VALUE){알림문="File full (16384 bytes)";return 0;}nəzarət_nöqtəsi();for(int 순번=uzunluq_VALUE-1;순번>=INDEX_VALUE;순번--)Mətn[순번+element_COUNT]=Mətn[순번];for(int 순번=0;순번<element_COUNT;순번++)Mətn[INDEX_VALUE+순번]=sətir_verilənlər[순번];uzunluq_VALUE+=element_COUNT;INDEX_VALUE+=element_COUNT;변경됨=1;return 1;}
static void Şaquli(int 차이){int sütun_yerinə_qoymaq=sütun(INDEX_VALUE),verilənlər_yerinə_qoymaq=İcra_Et(INDEX_VALUE);if(차이<0){if(!verilənlər_yerinə_qoymaq)return;verilənlər_yerinə_qoymaq=İcra_Et(verilənlər_yerinə_qoymaq-1);}else{verilənlər_yerinə_qoymaq=bitirmək_OFFSET(verilənlər_yerinə_qoymaq);if(verilənlər_yerinə_qoymaq==uzunluq_VALUE)return;verilənlər_yerinə_qoymaq++;}int simvol_kodu=0;while(verilənlər_yerinə_qoymaq<uzunluq_VALUE&&Mətn[verilənlər_yerinə_qoymaq]!='\n'&&simvol_kodu<sütun_yerinə_qoymaq){simvol_kodu+=Mətn[verilənlər_yerinə_qoymaq]=='\t'?4-simvol_kodu%4:너비(Mətn[verilənlər_yerinə_qoymaq]);verilənlər_yerinə_qoymaq=Sonrakı_element(verilənlər_yerinə_qoymaq);}INDEX_VALUE=verilənlər_yerinə_qoymaq;}
static void 화면그리기(void){
    if(INDEX_VALUE>uzunluq_VALUE)INDEX_VALUE=uzunluq_VALUE;if(맨위>INDEX_VALUE)맨위=İcra_Et(INDEX_VALUE);맨위=İcra_Et(맨위);
    int ROW_yerinə_qoymaq=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Mətn[순번]=='\n')ROW_yerinə_qoymaq++;
    while(ROW_yerinə_qoymaq>=ROW_COUNT-1){맨위=bitirmək_OFFSET(맨위);if(맨위<uzunluq_VALUE)맨위++;ROW_yerinə_qoymaq--;}
    int sütun_yerinə_qoymaq=sütun(INDEX_VALUE);if(sütun_yerinə_qoymaq<왼쪽)왼쪽=sütun_yerinə_qoymaq;if(sütun_yerinə_qoymaq-왼쪽>=COLUMNS-1)왼쪽=sütun_yerinə_qoymaq-COLUMNS+2;
    글내보내기("\033[?25l");int verilənlər_yerinə_qoymaq=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        hərəkət_etdir_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int simvol_kodu=0,그려진상태=0;
        if(verilənlər_yerinə_qoymaq>=uzunluq_VALUE&&반환값>ROW_yerinə_qoymaq){글내보내기("\033[90m~\033[0m");continue;}
        while(verilənlər_yerinə_qoymaq<uzunluq_VALUE&&Mətn[verilənlər_yerinə_qoymaq]!='\n'){
            int Sonrakı_OFFSET=Sonrakı_element(verilənlər_yerinə_qoymaq),너비값=Mətn[verilənlər_yerinə_qoymaq]=='\t'?4-simvol_kodu%4:너비(Mətn[verilənlər_yerinə_qoymaq]);
            if(simvol_kodu>=왼쪽&&simvol_kodu-왼쪽+너비값<COLUMNS){
                if(Mətn[verilənlər_yerinə_qoymaq]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bayt_verilənlər(' ');}else if(Mətn[verilənlər_yerinə_qoymaq]<32||Mətn[verilənlər_yerinə_qoymaq]==127){bayt_verilənlər('?');}else for(int 안쪽순번=verilənlər_yerinə_qoymaq;안쪽순번<Sonrakı_OFFSET;안쪽순번++)bayt_verilənlər(Mətn[안쪽순번]);그려진상태+=너비값;
            }simvol_kodu+=너비값;verilənlər_yerinə_qoymaq=Sonrakı_OFFSET;
        }
        (void)그려진상태;if(verilənlər_yerinə_qoymaq<uzunluq_VALUE)verilənlər_yerinə_qoymaq++;
    }
    hərəkət_etdir_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");vəziyyət_IMAGE=1;vəziyyət_növbə=0;글내보내기(əlavə_etmək?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fayl_daxiletmə_ad[이름바이트수]&&이름바이트수<30)bayt_verilənlər(fayl_daxiletmə_ad[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Giriş=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Mətn[순번]=='\n')Giriş++;수치(Giriş);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int element_COUNT=0;글내보내기(" | ");while(알림문[element_COUNT]&&element_COUNT<20)bayt_verilənlər(알림문[element_COUNT++]);}
    vəziyyət_IMAGE=0;글내보내기("\033[0m");hərəkət_etdir_VALUE(ROW_yerinə_qoymaq+1,sütun_yerinə_qoymaq-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(gözləyir_Açar){int 셋째순번=gözləyir_Açar;gözləyir_Açar=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Böyüklük=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Böyüklük&65535)||ROW_COUNT!=(int)(Böyüklük>>16)){
            COLUMNS=Böyüklük&65535;ROW_COUNT=Böyüklük>>16;화면그리기();
            if(kömək_sahə){hərəkət_etdir_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bayt_verilənlər(kömək_sahə);글내보내기(Əmr);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){gözləyir_Açar=셋째순번;return 27;}
    int element_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){element_COUNT=element_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return element_COUNT==3?1007:element_COUNT==5?1008:element_COUNT==6?1009:element_COUNT==1?1005:element_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int fayl_tutacaq=açmaq_fayl(fayl_daxiletmə_ad,oxunan_yazılan|없으면만들기|내용비우기,0600);if(fayl_tutacaq<0){알림문="Cannot open for save";return 0;}
    intptr_t element_COUNT=yazmaq_fayl_verilənlər(fayl_tutacaq,Mətn,uzunluq_VALUE);bağlamaq_fayl(fayl_tutacaq);if(element_COUNT!=uzunluq_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Sonrakı(void){int element_COUNT=0;while(FIND_daxiletmə[element_COUNT])element_COUNT++;if(!element_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=uzunluq_VALUE;순번++){int verilənlər_yerinə_qoymaq=(INDEX_VALUE+순번)%(uzunluq_VALUE?uzunluq_VALUE:1),안쪽순번=0;while(안쪽순번<element_COUNT&&verilənlər_yerinə_qoymaq+안쪽순번<uzunluq_VALUE&&Mətn[verilənlər_yerinə_qoymaq+안쪽순번]==(unsigned char)FIND_daxiletmə[안쪽순번])안쪽순번++;if(안쪽순번==element_COUNT){INDEX_VALUE=verilənlər_yerinə_qoymaq;알림문="Match";return;}}알림문="Pattern not found";}
static int dəvət(int sahə_VALUE){
    int element_COUNT=0;Əmr[0]=0;
    for(;;){hərəkət_etdir_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bayt_verilənlər(sahə_VALUE);글내보내기(Əmr);출력비우기();kömək_sahə=sahə_VALUE;int 셋째순번=누름값();kömək_sahə=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(element_COUNT){element_COUNT--;while(element_COUNT>0&&((unsigned char)Əmr[element_COUNT]&192)==128)element_COUNT--;Əmr[element_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&element_COUNT<120){Əmr[element_COUNT++]=셋째순번;Əmr[element_COUNT]=0;}
    }
    if(sahə_VALUE=='/'){for(int 순번=0;순번<=element_COUNT;순번++)FIND_daxiletmə[순번]=Əmr[순번];FIND_Sonrakı();return 0;}
    if(같은지(Əmr,"q!"))return 1;
    if(같은지(Əmr,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Əmr,"wq")||같은지(Əmr,"x"))return Store_VALUE();
    if(같은지(Əmr,"w")){Store_VALUE();return 0;}
    if(Əmr[0]=='w'&&Əmr[1]==' '){int 순번=2;while(Əmr[순번]==' ')순번++;int Böyüklük=element_COUNT-순번;if(Böyüklük<1||Böyüklük>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Böyüklük;안쪽순번++)fayl_daxiletmə_ad[안쪽순번]=Əmr[순번+안쪽순번];fayl_daxiletmə_ad[Böyüklük]=0;Store_VALUE();return 0;}
    int Giriş=0;for(int 순번=0;순번<element_COUNT;순번++){if(Əmr[순번]<'0'||Əmr[순번]>'9'){Giriş=0;break;}Giriş=Giriş*10+Əmr[순번]-'0';if(Giriş>16384){Giriş=0;break;}}
    if(Giriş){INDEX_VALUE=0;while(--Giriş&&INDEX_VALUE<uzunluq_VALUE){INDEX_VALUE=bitirmək_OFFSET(INDEX_VALUE);if(INDEX_VALUE<uzunluq_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Başla_istifadəçi_proqram(int 무시값){
    (void)무시값;if(istifadəçi_arqument_COUNT()!=1||istifadəçi_arqument(0,fayl_daxiletmə_ad,sizeof(fayl_daxiletmə_ad))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fayl_tutacaq=açmaq_fayl(fayl_daxiletmə_ad,yalnız_oxunan_VALUE,0);
    if(fayl_tutacaq>=0){int element_COUNT=fayl_ölçünü_dəyişmək(fayl_tutacaq);if(element_COUNT<0||element_COUNT>편집용량){bağlamaq_fayl(fayl_tutacaq);return 1;}uzunluq_VALUE=파일자료읽기(fayl_tutacaq,Mətn,element_COUNT);bağlamaq_fayl(fayl_tutacaq);if(uzunluq_VALUE!=element_COUNT)return 1;for(int 순번=0;순번<uzunluq_VALUE;순번++)if(!Mətn[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,çıxış_proqram=0;
    while(!çıxış_proqram){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Şaquli(-1);continue;}if(셋째순번==1002){Şaquli(1);continue;}if(셋째순번==1003){INDEX_VALUE=Sonrakı_element(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=İcra_Et(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=bitirmək_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Şaquli(셋째순번==1008?-1:1);continue;}
        if(əlavə_etmək){
            if(셋째순번==27||셋째순번==3){əlavə_etmək=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<uzunluq_VALUE)바이트지우기(INDEX_VALUE,Sonrakı_element(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int element_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!element_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<element_COUNT;순번++){int simvol_kodu=누름값();if(simvol_kodu<128||simvol_kodu>191){gözləyir_Açar=simvol_kodu;유효함=0;break;}SECOND_VALUE[순번]=simvol_kodu;}
                if(유효함)덧붙이기(SECOND_VALUE,element_COUNT);
            }continue;
        }
        if(앞부분){int verilənlər_yerinə_qoymaq=앞부분;앞부분=0;if(verilənlər_yerinə_qoymaq=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(verilənlər_yerinə_qoymaq=='Z'&&셋째순번=='Z'){çıxış_proqram=Store_VALUE();continue;}if((verilənlər_yerinə_qoymaq=='d'&&셋째순번=='d')||(verilənlər_yerinə_qoymaq=='y'&&셋째순번=='y')){int 첫째값=İcra_Et(INDEX_VALUE),SECOND_VALUE=bitirmək_OFFSET(INDEX_VALUE);if(SECOND_VALUE<uzunluq_VALUE)SECOND_VALUE++;nümunə_uzunluq=SECOND_VALUE-첫째값;for(int 순번=0;순번<nümunə_uzunluq;순번++)복사자료[순번]=Mətn[첫째값+순번];if(verilənlər_yerinə_qoymaq=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){əlavə_etmək=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<bitirmək_OFFSET(INDEX_VALUE))INDEX_VALUE=Sonrakı_element(INDEX_VALUE);əlavə_etmək=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=İcra_Et(INDEX_VALUE);əlavə_etmək=1;continue;}if(셋째순번=='A'){INDEX_VALUE=bitirmək_OFFSET(INDEX_VALUE);əlavə_etmək=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char xətt_bitirmək='\n';INDEX_VALUE=셋째순번=='o'?bitirmək_OFFSET(INDEX_VALUE):İcra_Et(INDEX_VALUE);if(덧붙이기(&xətt_bitirmək,1)){if(셋째순번=='O')INDEX_VALUE--;əlavə_etmək=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Sonrakı_element(INDEX_VALUE);continue;}if(셋째순번=='j'){Şaquli(1);continue;}if(셋째순번=='k'){Şaquli(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=İcra_Et(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=bitirmək_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=İcra_Et(uzunluq_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<uzunluq_VALUE)바이트지우기(INDEX_VALUE,Sonrakı_element(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&nümunə_uzunluq){INDEX_VALUE=bitirmək_OFFSET(INDEX_VALUE);if(INDEX_VALUE<uzunluq_VALUE)INDEX_VALUE++;덧붙이기(복사자료,nümunə_uzunluq);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Mətn[순번];Mətn[순번]=qaytarmaq_verilənlər[순번];qaytarmaq_verilənlər[순번]=SECOND_VALUE;}int element_COUNT=uzunluq_VALUE;uzunluq_VALUE=qaytarmaq_uzunluq;qaytarmaq_uzunluq=element_COUNT;element_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=element_COUNT;element_COUNT=변경됨;변경됨=qaytarmaq_Dəyişikliklər;qaytarmaq_Dəyişikliklər=element_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){çıxış_proqram=dəvət(셋째순번);continue;}if(셋째순번=='n'){FIND_Sonrakı();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
