/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],mèghasịa_datà[편집용량],복사자료[편집용량],결과자료[1024];
static int ogologo_valuu,indèks_valuu,맨위,왼쪽,변경됨,tibànye,mèghasịa_ogologo,위쪽,mèghasịa_Mgbanwe_gasi,되돌림있음,ṅomie_ogologo,사용량,열수=68,행수=19;
static char ọbọakwụkwọ_ndebà_akara_ahà[64],Ntiiwu[128],chọta_ndebà[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned ozi_ọnọdụ_ọtụgwo;
static int ènyèmaka_otu,ọnọdụ_foto,ọnọdụ_ọgbàrànchere;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void baịtị_datà(unsigned koòdù_nkeakàrà){if(ọnọdụ_foto){if((koòdù_nkeakàrà&192)!=128){ọnọdụ_ọgbàrànchere+=koòdù_nkeakàrà>=196?2:1;}if(ọnọdụ_ọgbàrànchere>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=koòdù_nkeakàrà;}
static void 글내보내기(const char *ùsòròokwū_datà){while(*ùsòròokwū_datà)baịtị_datà((unsigned char)*ùsòròokwū_datà++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)baịtị_datà(둘째값[--순번]);}
static void gàa_valuu(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);baịtị_datà(';');수치(열위치);baịtị_datà('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(SMS[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<ogologo_valuu){자료위치++;while(자료위치<ogologo_valuu&&(SMS[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int Bido(int 자료위치){while(자료위치>0&&SMS[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int mèdebe_Nnokwata(int 자료위치){while(자료위치<ogologo_valuu&&SMS[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned koòdù_nkeakàrà){return koòdù_nkeakàrà>=196?2:1;}
static int ọgbàràogō(int 자료위치){int koòdù_nkeakàrà=0;for(int 순번=Bido(자료위치);순번<자료위치;순번=다음(순번))koòdù_nkeakàrà+=SMS[순번]=='\t'?4-koòdù_nkeakàrà%4:너비(SMS[순번]);return koòdù_nkeakàrà;}
static void ebenlecha(void){for(int 순번=0;순번<ogologo_valuu;순번++)mèghasịa_datà[순번]=SMS[순번];mèghasịa_ogologo=ogologo_valuu;위쪽=indèks_valuu;mèghasịa_Mgbanwe_gasi=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){ebenlecha();for(int 순번=도착위치;순번<ogologo_valuu;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];ogologo_valuu-=도착위치-출발위치;indèks_valuu=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *ùsòròokwū_datà,int 개수){if(개수>편집용량-ogologo_valuu){알림문="File full (16384 bytes)";return 0;}ebenlecha();for(int 순번=ogologo_valuu-1;순번>=indèks_valuu;순번--)SMS[순번+개수]=SMS[순번];for(int 순번=0;순번<개수;순번++)SMS[indèks_valuu+순번]=ùsòròokwū_datà[순번];ogologo_valuu+=개수;indèks_valuu+=개수;변경됨=1;return 1;}
static void Ndepụta_Nkwụọtọ(int 차이){int 열위치=ọgbàràogō(indèks_valuu),자료위치=Bido(indèks_valuu);if(차이<0){if(!자료위치)return;자료위치=Bido(자료위치-1);}else{자료위치=mèdebe_Nnokwata(자료위치);if(자료위치==ogologo_valuu)return;자료위치++;}int koòdù_nkeakàrà=0;while(자료위치<ogologo_valuu&&SMS[자료위치]!='\n'&&koòdù_nkeakàrà<열위치){koòdù_nkeakàrà+=SMS[자료위치]=='\t'?4-koòdù_nkeakàrà%4:너비(SMS[자료위치]);자료위치=다음(자료위치);}indèks_valuu=자료위치;}
static void 화면그리기(void){
    if(indèks_valuu>ogologo_valuu)indèks_valuu=ogologo_valuu;if(맨위>indèks_valuu)맨위=Bido(indèks_valuu);맨위=Bido(맨위);
    int 행위치=0;for(int 순번=맨위;순번<indèks_valuu;순번++)if(SMS[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=mèdebe_Nnokwata(맨위);if(맨위<ogologo_valuu)맨위++;행위치--;}
    int 열위치=ọgbàràogō(indèks_valuu);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        gàa_valuu(반환값+1,1);글내보내기("\033[0m\033[2K");int koòdù_nkeakàrà=0,그려진상태=0;
        if(자료위치>=ogologo_valuu&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<ogologo_valuu&&SMS[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=SMS[자료위치]=='\t'?4-koòdù_nkeakàrà%4:너비(SMS[자료위치]);
            if(koòdù_nkeakàrà>=왼쪽&&koòdù_nkeakàrà-왼쪽+너비값<열수){
                if(SMS[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)baịtị_datà(' ');}else if(SMS[자료위치]<32||SMS[자료위치]==127){baịtị_datà('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)baịtị_datà(SMS[안쪽순번]);그려진상태+=너비값;
            }koòdù_nkeakàrà+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<ogologo_valuu)자료위치++;
    }
    gàa_valuu(행수,1);글내보내기("\033[7m\033[2K");ọnọdụ_foto=1;ọnọdụ_ọgbàrànchere=0;글내보내기(tibànye?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(ọbọakwụkwọ_ndebà_akara_ahà[이름바이트수]&&이름바이트수<30)baịtị_datà(ọbọakwụkwọ_ndebà_akara_ahà[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int ahịrī=1;for(int 순번=0;순번<indèks_valuu;순번++)if(SMS[순번]=='\n')ahịrī++;수치(ahịrī);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)baịtị_datà(알림문[개수++]);}
    ọnọdụ_foto=0;글내보내기("\033[0m");gàa_valuu(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(ozi_ọnọdụ_ọtụgwo){int 셋째순번=ozi_ọnọdụ_ọtụgwo;ozi_ọnọdụ_ọtụgwo=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Ụhara=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Ụhara&65535)||행수!=(int)(Ụhara>>16)){
            열수=Ụhara&65535;행수=Ụhara>>16;화면그리기();
            if(ènyèmaka_otu){gàa_valuu(행수,1);글내보내기("\033[0m\033[2K");baịtị_datà(ènyèmaka_otu);글내보내기(Ntiiwu);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){ozi_ọnọdụ_ọtụgwo=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_valuu(void){
    int ọbọakwụkwọ_ebenjìaka=mepee_ọbọakwụkwọ(ọbọakwụkwọ_ndebà_akara_ahà,gụọ_dèe|없으면만들기|내용비우기,0600);if(ọbọakwụkwọ_ebenjìaka<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=dee_ọbọakwụkwọ_datà(ọbọakwụkwọ_ebenjìaka,SMS,ogologo_valuu);mmechi_ọbọakwụkwọ(ọbọakwụkwọ_ebenjìaka);if(개수!=ogologo_valuu){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(chọta_ndebà[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=ogologo_valuu;순번++){int 자료위치=(indèks_valuu+순번)%(ogologo_valuu?ogologo_valuu:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<ogologo_valuu&&SMS[자료위치+안쪽순번]==(unsigned char)chọta_ndebà[안쪽순번])안쪽순번++;if(안쪽순번==개수){indèks_valuu=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int mkpalite(int otu_valuu_4b6d6445){
    int 개수=0;Ntiiwu[0]=0;
    for(;;){gàa_valuu(행수,1);글내보내기("\033[0m\033[2K");baịtị_datà(otu_valuu_4b6d6445);글내보내기(Ntiiwu);출력비우기();ènyèmaka_otu=otu_valuu_4b6d6445;int 셋째순번=누름값();ènyèmaka_otu=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Ntiiwu[개수]&192)==128)개수--;Ntiiwu[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Ntiiwu[개수++]=셋째순번;Ntiiwu[개수]=0;}
    }
    if(otu_valuu_4b6d6445=='/'){for(int 순번=0;순번<=개수;순번++)chọta_ndebà[순번]=Ntiiwu[순번];다음찾기();return 0;}
    if(같은지(Ntiiwu,"q!"))return 1;
    if(같은지(Ntiiwu,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Ntiiwu,"wq")||같은지(Ntiiwu,"x"))return Store_valuu();
    if(같은지(Ntiiwu,"w")){Store_valuu();return 0;}
    if(Ntiiwu[0]=='w'&&Ntiiwu[1]==' '){int 순번=2;while(Ntiiwu[순번]==' ')순번++;int Ụhara=개수-순번;if(Ụhara<1||Ụhara>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Ụhara;안쪽순번++)ọbọakwụkwọ_ndebà_akara_ahà[안쪽순번]=Ntiiwu[순번+안쪽순번];ọbọakwụkwọ_ndebà_akara_ahà[Ụhara]=0;Store_valuu();return 0;}
    int ahịrī=0;for(int 순번=0;순번<개수;순번++){if(Ntiiwu[순번]<'0'||Ntiiwu[순번]>'9'){ahịrī=0;break;}ahịrī=ahịrī*10+Ntiiwu[순번]-'0';if(ahịrī>16384){ahịrī=0;break;}}
    if(ahịrī){indèks_valuu=0;while(--ahịrī&&indèks_valuu<ogologo_valuu){indèks_valuu=mèdebe_Nnokwata(indèks_valuu);if(indèks_valuu<ogologo_valuu)indèks_valuu++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Mbido_òjìàrụ_app(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||òjìàrụ_agụment(0,ọbọakwụkwọ_ndebà_akara_ahà,sizeof(ọbọakwụkwọ_ndebà_akara_ahà))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int ọbọakwụkwọ_ebenjìaka=mepee_ọbọakwụkwọ(ọbọakwụkwọ_ndebà_akara_ahà,ọgụgụ_naanị_valuu,0);
    if(ọbọakwụkwọ_ebenjìaka>=0){int 개수=ọbọakwụkwọ_ụha(ọbọakwụkwọ_ebenjìaka);if(개수<0||개수>편집용량){mmechi_ọbọakwụkwọ(ọbọakwụkwọ_ebenjìaka);return 1;}ogologo_valuu=파일자료읽기(ọbọakwụkwọ_ebenjìaka,SMS,개수);mmechi_ọbọakwụkwọ(ọbọakwụkwọ_ebenjìaka);if(ogologo_valuu!=개수)return 1;for(int 순번=0;순번<ogologo_valuu;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Ndepụta_Nkwụọtọ(-1);continue;}if(셋째순번==1002){Ndepụta_Nkwụọtọ(1);continue;}if(셋째순번==1003){indèks_valuu=다음(indèks_valuu);continue;}if(셋째순번==1004){indèks_valuu=이전항목(indèks_valuu);continue;}
        if(셋째순번==1005){indèks_valuu=Bido(indèks_valuu);continue;}if(셋째순번==1006){indèks_valuu=mèdebe_Nnokwata(indèks_valuu);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Ndepụta_Nkwụọtọ(셋째순번==1008?-1:1);continue;}
        if(tibànye){
            if(셋째순번==27||셋째순번==3){tibànye=0;continue;}
            if(셋째순번==127||셋째순번==8){if(indèks_valuu)바이트지우기(이전항목(indèks_valuu),indèks_valuu);continue;}
            if(셋째순번==1007){if(indèks_valuu<ogologo_valuu)바이트지우기(indèks_valuu,다음(indèks_valuu));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int koòdù_nkeakàrà=누름값();if(koòdù_nkeakàrà<128||koòdù_nkeakàrà>191){ozi_ọnọdụ_ọtụgwo=koòdù_nkeakàrà;유효함=0;break;}둘째값[순번]=koòdù_nkeakàrà;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){indèks_valuu=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_valuu();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=Bido(indèks_valuu),둘째값=mèdebe_Nnokwata(indèks_valuu);if(둘째값<ogologo_valuu)둘째값++;ṅomie_ogologo=둘째값-첫째값;for(int 순번=0;순번<ṅomie_ogologo;순번++)복사자료[순번]=SMS[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){tibànye=1;continue;}if(셋째순번=='a'){if(indèks_valuu<mèdebe_Nnokwata(indèks_valuu))indèks_valuu=다음(indèks_valuu);tibànye=1;continue;}
        if(셋째순번=='I'){indèks_valuu=Bido(indèks_valuu);tibànye=1;continue;}if(셋째순번=='A'){indèks_valuu=mèdebe_Nnokwata(indèks_valuu);tibànye=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char ahịrī_mèdebe='\n';indèks_valuu=셋째순번=='o'?mèdebe_Nnokwata(indèks_valuu):Bido(indèks_valuu);if(덧붙이기(&ahịrī_mèdebe,1)){if(셋째순번=='O')indèks_valuu--;tibànye=1;}continue;}
        if(셋째순번=='h'){indèks_valuu=이전항목(indèks_valuu);continue;}if(셋째순번=='l'){indèks_valuu=다음(indèks_valuu);continue;}if(셋째순번=='j'){Ndepụta_Nkwụọtọ(1);continue;}if(셋째순번=='k'){Ndepụta_Nkwụọtọ(-1);continue;}
        if(셋째순번=='0'){indèks_valuu=Bido(indèks_valuu);continue;}if(셋째순번=='$'){indèks_valuu=mèdebe_Nnokwata(indèks_valuu);continue;}if(셋째순번=='G'){indèks_valuu=Bido(ogologo_valuu);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(indèks_valuu<ogologo_valuu)바이트지우기(indèks_valuu,다음(indèks_valuu));continue;}
        if(셋째순번=='p'&&ṅomie_ogologo){indèks_valuu=mèdebe_Nnokwata(indèks_valuu);if(indèks_valuu<ogologo_valuu)indèks_valuu++;덧붙이기(복사자료,ṅomie_ogologo);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=SMS[순번];SMS[순번]=mèghasịa_datà[순번];mèghasịa_datà[순번]=둘째값;}int 개수=ogologo_valuu;ogologo_valuu=mèghasịa_ogologo;mèghasịa_ogologo=개수;개수=indèks_valuu;indèks_valuu=위쪽;위쪽=개수;개수=변경됨;변경됨=mèghasịa_Mgbanwe_gasi;mèghasịa_Mgbanwe_gasi=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=mkpalite(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
