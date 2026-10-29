/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define editore_ahalmen 16384
static unsigned char Testua[editore_ahalmen],desegin_datuak[editore_ahalmen],복사자료[editore_ahalmen],neurria_datuak[1024];
static int luzera_balio,INDIZE_balio,맨위,왼쪽,변경됨,Txertatu,desegin_luzera,위쪽,desegin_Aldaketak,되돌림있음,kopiatu_luzera,사용량,ZUTABEAK=68,ERRENKADA_ZENBATU=19;
static char fitxategi_sarrera_izen[64],Komandoa[128],Bilatu_sarrera[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned zain_gako;
static int laguntza_Kategoria,Egoera_irudi,Egoera_ilara;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)neurria_datuak,사용량,0,0,0);사용량=0;}}
static void byte_datuak(unsigned karaktere_kode){if(Egoera_irudi){if((karaktere_kode&192)!=128){Egoera_ilara+=karaktere_kode>=196?2:1;}if(Egoera_ilara>=ZUTABEAK)return;}if(사용량==(int)sizeof(neurria_datuak))출력비우기();neurria_datuak[사용량++]=karaktere_kode;}
static void 글내보내기(const char *kate_datuak){while(*kate_datuak)byte_datuak((unsigned char)*kate_datuak++);}
static void 수치(unsigned elementu_ZENBATU){char SEGUNDOA_balio[12];int 순번=0;do{SEGUNDOA_balio[순번++]='0'+elementu_ZENBATU%10;elementu_ZENBATU/=10;}while(elementu_ZENBATU);while(순번)byte_datuak(SEGUNDOA_balio[--순번]);}
static void eraman_balio(int ERRENKADA_kargu,int zutabe_kargu){글내보내기("\033[");수치(ERRENKADA_kargu);byte_datuak(';');수치(zutabe_kargu);byte_datuak('H');}
static int 이전항목(int datuak_kargu){if(datuak_kargu){datuak_kargu--;while(datuak_kargu>0&&(Testua[datuak_kargu]&192)==128)datuak_kargu--;}return datuak_kargu;}
static int Hurrengoa_elementu(int datuak_kargu){if(datuak_kargu<luzera_balio){datuak_kargu++;while(datuak_kargu<luzera_balio&&(Testua[datuak_kargu]&192)==128)datuak_kargu++;}return datuak_kargu;}
static int Exekutatu_2(int datuak_kargu){while(datuak_kargu>0&&Testua[datuak_kargu-1]!='\n')datuak_kargu--;return datuak_kargu;}
static int amaitu_Geruzak(int datuak_kargu){while(datuak_kargu<luzera_balio&&Testua[datuak_kargu]!='\n')datuak_kargu++;return datuak_kargu;}
static int 너비(unsigned karaktere_kode){return karaktere_kode>=196?2:1;}
static int zutabe(int datuak_kargu){int karaktere_kode=0;for(int 순번=Exekutatu_2(datuak_kargu);순번<datuak_kargu;순번=Hurrengoa_elementu(순번))karaktere_kode+=Testua[순번]=='\t'?4-karaktere_kode%4:너비(Testua[순번]);return karaktere_kode;}
static void kontrol_puntu(void){for(int 순번=0;순번<luzera_balio;순번++)desegin_datuak[순번]=Testua[순번];desegin_luzera=luzera_balio;위쪽=INDIZE_balio;desegin_Aldaketak=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrol_puntu();for(int 순번=도착위치;순번<luzera_balio;순번++)Testua[출발위치+순번-도착위치]=Testua[순번];luzera_balio-=도착위치-출발위치;INDIZE_balio=출발위치;변경됨=1;}
static int Erantsi_balio(const unsigned char *kate_datuak,int elementu_ZENBATU){if(elementu_ZENBATU>editore_ahalmen-luzera_balio){알림문="File full (16384 bytes)";return 0;}kontrol_puntu();for(int 순번=luzera_balio-1;순번>=INDIZE_balio;순번--)Testua[순번+elementu_ZENBATU]=Testua[순번];for(int 순번=0;순번<elementu_ZENBATU;순번++)Testua[INDIZE_balio+순번]=kate_datuak[순번];luzera_balio+=elementu_ZENBATU;INDIZE_balio+=elementu_ZENBATU;변경됨=1;return 1;}
static void Bertikala(int 차이){int zutabe_kargu=zutabe(INDIZE_balio),datuak_kargu=Exekutatu_2(INDIZE_balio);if(차이<0){if(!datuak_kargu)return;datuak_kargu=Exekutatu_2(datuak_kargu-1);}else{datuak_kargu=amaitu_Geruzak(datuak_kargu);if(datuak_kargu==luzera_balio)return;datuak_kargu++;}int karaktere_kode=0;while(datuak_kargu<luzera_balio&&Testua[datuak_kargu]!='\n'&&karaktere_kode<zutabe_kargu){karaktere_kode+=Testua[datuak_kargu]=='\t'?4-karaktere_kode%4:너비(Testua[datuak_kargu]);datuak_kargu=Hurrengoa_elementu(datuak_kargu);}INDIZE_balio=datuak_kargu;}
static void 화면그리기(void){
    if(INDIZE_balio>luzera_balio)INDIZE_balio=luzera_balio;if(맨위>INDIZE_balio)맨위=Exekutatu_2(INDIZE_balio);맨위=Exekutatu_2(맨위);
    int ERRENKADA_kargu=0;for(int 순번=맨위;순번<INDIZE_balio;순번++)if(Testua[순번]=='\n')ERRENKADA_kargu++;
    while(ERRENKADA_kargu>=ERRENKADA_ZENBATU-1){맨위=amaitu_Geruzak(맨위);if(맨위<luzera_balio)맨위++;ERRENKADA_kargu--;}
    int zutabe_kargu=zutabe(INDIZE_balio);if(zutabe_kargu<왼쪽)왼쪽=zutabe_kargu;if(zutabe_kargu-왼쪽>=ZUTABEAK-1)왼쪽=zutabe_kargu-ZUTABEAK+2;
    글내보내기("\033[?25l");int datuak_kargu=맨위;
    for(int 반환값=0;반환값<ERRENKADA_ZENBATU-1;반환값++){
        eraman_balio(반환값+1,1);글내보내기("\033[0m\033[2K");int karaktere_kode=0,그려진상태=0;
        if(datuak_kargu>=luzera_balio&&반환값>ERRENKADA_kargu){글내보내기("\033[90m~\033[0m");continue;}
        while(datuak_kargu<luzera_balio&&Testua[datuak_kargu]!='\n'){
            int Hurrengoa_Geruzak=Hurrengoa_elementu(datuak_kargu),너비값=Testua[datuak_kargu]=='\t'?4-karaktere_kode%4:너비(Testua[datuak_kargu]);
            if(karaktere_kode>=왼쪽&&karaktere_kode-왼쪽+너비값<ZUTABEAK){
                if(Testua[datuak_kargu]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_datuak(' ');}else if(Testua[datuak_kargu]<32||Testua[datuak_kargu]==127){byte_datuak('?');}else for(int 안쪽순번=datuak_kargu;안쪽순번<Hurrengoa_Geruzak;안쪽순번++)byte_datuak(Testua[안쪽순번]);그려진상태+=너비값;
            }karaktere_kode+=너비값;datuak_kargu=Hurrengoa_Geruzak;
        }
        (void)그려진상태;if(datuak_kargu<luzera_balio)datuak_kargu++;
    }
    eraman_balio(ERRENKADA_ZENBATU,1);글내보내기("\033[7m\033[2K");Egoera_irudi=1;Egoera_ilara=0;글내보내기(Txertatu?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fitxategi_sarrera_izen[이름바이트수]&&이름바이트수<30)byte_datuak(fitxategi_sarrera_izen[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Marra=1;for(int 순번=0;순번<INDIZE_balio;순번++)if(Testua[순번]=='\n')Marra++;수치(Marra);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int elementu_ZENBATU=0;글내보내기(" | ");while(알림문[elementu_ZENBATU]&&elementu_ZENBATU<20)byte_datuak(알림문[elementu_ZENBATU++]);}
    Egoera_irudi=0;글내보내기("\033[0m");eraman_balio(ERRENKADA_kargu+1,zutabe_kargu-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(zain_gako){int 셋째순번=zain_gako;zain_gako=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Tamaina=사용자호출(16,3,0,0,0,0,0);
        if(ZUTABEAK!=(int)(Tamaina&65535)||ERRENKADA_ZENBATU!=(int)(Tamaina>>16)){
            ZUTABEAK=Tamaina&65535;ERRENKADA_ZENBATU=Tamaina>>16;화면그리기();
            if(laguntza_Kategoria){eraman_balio(ERRENKADA_ZENBATU,1);글내보내기("\033[0m\033[2K");byte_datuak(laguntza_Kategoria);글내보내기(Komandoa);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){zain_gako=셋째순번;return 27;}
    int elementu_ZENBATU=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){elementu_ZENBATU=elementu_ZENBATU*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return elementu_ZENBATU==3?1007:elementu_ZENBATU==5?1008:elementu_ZENBATU==6?1009:elementu_ZENBATU==1?1005:elementu_ZENBATU==4?1006:27;return 27;}return 27;
}
static int Store_balio(void){
    int fitxategi_helduleku=ireki_fitxategi(fitxategi_sarrera_izen,irakurri_idatzi|없으면만들기|내용비우기,0600);if(fitxategi_helduleku<0){알림문="Cannot open for save";return 0;}
    intptr_t elementu_ZENBATU=idatzi_fitxategi_datuak(fitxategi_helduleku,Testua,luzera_balio);itxi_fitxategi(fitxategi_helduleku);if(elementu_ZENBATU!=luzera_balio){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEGUNDOA_balio){while(*첫째값&&*첫째값==*SEGUNDOA_balio){첫째값++;SEGUNDOA_balio++;}return *첫째값==*SEGUNDOA_balio;}
static void Bilatu_Hurrengoa(void){int elementu_ZENBATU=0;while(Bilatu_sarrera[elementu_ZENBATU])elementu_ZENBATU++;if(!elementu_ZENBATU){알림문="No search pattern";return;}for(int 순번=1;순번<=luzera_balio;순번++){int datuak_kargu=(INDIZE_balio+순번)%(luzera_balio?luzera_balio:1),안쪽순번=0;while(안쪽순번<elementu_ZENBATU&&datuak_kargu+안쪽순번<luzera_balio&&Testua[datuak_kargu+안쪽순번]==(unsigned char)Bilatu_sarrera[안쪽순번])안쪽순번++;if(안쪽순번==elementu_ZENBATU){INDIZE_balio=datuak_kargu;알림문="Match";return;}}알림문="Pattern not found";}
static int eskatu(int Kategoria_balio){
    int elementu_ZENBATU=0;Komandoa[0]=0;
    for(;;){eraman_balio(ERRENKADA_ZENBATU,1);글내보내기("\033[0m\033[2K");byte_datuak(Kategoria_balio);글내보내기(Komandoa);출력비우기();laguntza_Kategoria=Kategoria_balio;int 셋째순번=누름값();laguntza_Kategoria=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(elementu_ZENBATU){elementu_ZENBATU--;while(elementu_ZENBATU>0&&((unsigned char)Komandoa[elementu_ZENBATU]&192)==128)elementu_ZENBATU--;Komandoa[elementu_ZENBATU]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&elementu_ZENBATU<120){Komandoa[elementu_ZENBATU++]=셋째순번;Komandoa[elementu_ZENBATU]=0;}
    }
    if(Kategoria_balio=='/'){for(int 순번=0;순번<=elementu_ZENBATU;순번++)Bilatu_sarrera[순번]=Komandoa[순번];Bilatu_Hurrengoa();return 0;}
    if(같은지(Komandoa,"q!"))return 1;
    if(같은지(Komandoa,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Komandoa,"wq")||같은지(Komandoa,"x"))return Store_balio();
    if(같은지(Komandoa,"w")){Store_balio();return 0;}
    if(Komandoa[0]=='w'&&Komandoa[1]==' '){int 순번=2;while(Komandoa[순번]==' ')순번++;int Tamaina=elementu_ZENBATU-순번;if(Tamaina<1||Tamaina>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Tamaina;안쪽순번++)fitxategi_sarrera_izen[안쪽순번]=Komandoa[순번+안쪽순번];fitxategi_sarrera_izen[Tamaina]=0;Store_balio();return 0;}
    int Marra=0;for(int 순번=0;순번<elementu_ZENBATU;순번++){if(Komandoa[순번]<'0'||Komandoa[순번]>'9'){Marra=0;break;}Marra=Marra*10+Komandoa[순번]-'0';if(Marra>16384){Marra=0;break;}}
    if(Marra){INDIZE_balio=0;while(--Marra&&INDIZE_balio<luzera_balio){INDIZE_balio=amaitu_Geruzak(INDIZE_balio);if(INDIZE_balio<luzera_balio)INDIZE_balio++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int HASI_erabiltzaile_aplik(int 무시값){
    (void)무시값;if(erabiltzaile_arg_ZENBATU()!=1||erabiltzaile_arg(0,fitxategi_sarrera_izen,sizeof(fitxategi_sarrera_izen))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fitxategi_helduleku=ireki_fitxategi(fitxategi_sarrera_izen,irakurtzeko_soilik_balio,0);
    if(fitxategi_helduleku>=0){int elementu_ZENBATU=파일크기(fitxategi_helduleku);if(elementu_ZENBATU<0||elementu_ZENBATU>editore_ahalmen){itxi_fitxategi(fitxategi_helduleku);return 1;}luzera_balio=파일자료읽기(fitxategi_helduleku,Testua,elementu_ZENBATU);itxi_fitxategi(fitxategi_helduleku);if(luzera_balio!=elementu_ZENBATU)return 1;for(int 순번=0;순번<luzera_balio;순번++)if(!Testua[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(errorearen_zenbaki!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}ZUTABEAK=흐린색&65535;ERRENKADA_ZENBATU=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,irten_aplik_55b3a1cd=0;
    while(!irten_aplik_55b3a1cd){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Bertikala(-1);continue;}if(셋째순번==1002){Bertikala(1);continue;}if(셋째순번==1003){INDIZE_balio=Hurrengoa_elementu(INDIZE_balio);continue;}if(셋째순번==1004){INDIZE_balio=이전항목(INDIZE_balio);continue;}
        if(셋째순번==1005){INDIZE_balio=Exekutatu_2(INDIZE_balio);continue;}if(셋째순번==1006){INDIZE_balio=amaitu_Geruzak(INDIZE_balio);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ERRENKADA_ZENBATU-2;순번++)Bertikala(셋째순번==1008?-1:1);continue;}
        if(Txertatu){
            if(셋째순번==27||셋째순번==3){Txertatu=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDIZE_balio)바이트지우기(이전항목(INDIZE_balio),INDIZE_balio);continue;}
            if(셋째순번==1007){if(INDIZE_balio<luzera_balio)바이트지우기(INDIZE_balio,Hurrengoa_elementu(INDIZE_balio));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEGUNDOA_balio[4];SEGUNDOA_balio[0]=셋째순번;int elementu_ZENBATU=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!elementu_ZENBATU){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<elementu_ZENBATU;순번++){int karaktere_kode=누름값();if(karaktere_kode<128||karaktere_kode>191){zain_gako=karaktere_kode;유효함=0;break;}SEGUNDOA_balio[순번]=karaktere_kode;}
                if(유효함)Erantsi_balio(SEGUNDOA_balio,elementu_ZENBATU);
            }continue;
        }
        if(앞부분){int datuak_kargu=앞부분;앞부분=0;if(datuak_kargu=='g'&&셋째순번=='g'){INDIZE_balio=0;continue;}if(datuak_kargu=='Z'&&셋째순번=='Z'){irten_aplik_55b3a1cd=Store_balio();continue;}if((datuak_kargu=='d'&&셋째순번=='d')||(datuak_kargu=='y'&&셋째순번=='y')){int 첫째값=Exekutatu_2(INDIZE_balio),SEGUNDOA_balio=amaitu_Geruzak(INDIZE_balio);if(SEGUNDOA_balio<luzera_balio)SEGUNDOA_balio++;kopiatu_luzera=SEGUNDOA_balio-첫째값;for(int 순번=0;순번<kopiatu_luzera;순번++)복사자료[순번]=Testua[첫째값+순번];if(datuak_kargu=='d')바이트지우기(첫째값,SEGUNDOA_balio);continue;}}
        if(셋째순번=='i'){Txertatu=1;continue;}if(셋째순번=='a'){if(INDIZE_balio<amaitu_Geruzak(INDIZE_balio))INDIZE_balio=Hurrengoa_elementu(INDIZE_balio);Txertatu=1;continue;}
        if(셋째순번=='I'){INDIZE_balio=Exekutatu_2(INDIZE_balio);Txertatu=1;continue;}if(셋째순번=='A'){INDIZE_balio=amaitu_Geruzak(INDIZE_balio);Txertatu=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char lerro_amaitu='\n';INDIZE_balio=셋째순번=='o'?amaitu_Geruzak(INDIZE_balio):Exekutatu_2(INDIZE_balio);if(Erantsi_balio(&lerro_amaitu,1)){if(셋째순번=='O')INDIZE_balio--;Txertatu=1;}continue;}
        if(셋째순번=='h'){INDIZE_balio=이전항목(INDIZE_balio);continue;}if(셋째순번=='l'){INDIZE_balio=Hurrengoa_elementu(INDIZE_balio);continue;}if(셋째순번=='j'){Bertikala(1);continue;}if(셋째순번=='k'){Bertikala(-1);continue;}
        if(셋째순번=='0'){INDIZE_balio=Exekutatu_2(INDIZE_balio);continue;}if(셋째순번=='$'){INDIZE_balio=amaitu_Geruzak(INDIZE_balio);continue;}if(셋째순번=='G'){INDIZE_balio=Exekutatu_2(luzera_balio);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDIZE_balio<luzera_balio)바이트지우기(INDIZE_balio,Hurrengoa_elementu(INDIZE_balio));continue;}
        if(셋째순번=='p'&&kopiatu_luzera){INDIZE_balio=amaitu_Geruzak(INDIZE_balio);if(INDIZE_balio<luzera_balio)INDIZE_balio++;Erantsi_balio(복사자료,kopiatu_luzera);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<editore_ahalmen;순번++){unsigned char SEGUNDOA_balio=Testua[순번];Testua[순번]=desegin_datuak[순번];desegin_datuak[순번]=SEGUNDOA_balio;}int elementu_ZENBATU=luzera_balio;luzera_balio=desegin_luzera;desegin_luzera=elementu_ZENBATU;elementu_ZENBATU=INDIZE_balio;INDIZE_balio=위쪽;위쪽=elementu_ZENBATU;elementu_ZENBATU=변경됨;변경됨=desegin_Aldaketak;desegin_Aldaketak=elementu_ZENBATU;continue;}
        if(셋째순번==':'||셋째순번=='/'){irten_aplik_55b3a1cd=eskatu(셋째순번);continue;}if(셋째순번=='n'){Bilatu_Hurrengoa();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
