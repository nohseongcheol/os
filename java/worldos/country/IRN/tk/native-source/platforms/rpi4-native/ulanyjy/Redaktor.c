/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Metin[편집용량],gaýtar_maglumat[편집용량],복사자료[편집용량],결과자료[1024];
static int dowamlylyk_baha,indeks_baha,맨위,왼쪽,변경됨,giriz,gaýtar_dowamlylyk,위쪽,gaýtar_Üýtgeşiklikler,되돌림있음,synp_dowamlylyk,사용량,열수=68,행수=19;
static char faýl_girizmeklik_at[64],buýruk[128],tap_girizmeklik[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned garaşýar_açar;
static int kömek_kategoriýa,ýagdaý_surat,ýagdaý_nobat;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void baýt_maglumat(unsigned nyşanyň_kody){if(ýagdaý_surat){if((nyşanyň_kody&192)!=128){ýagdaý_nobat+=nyşanyň_kody>=196?2:1;}if(ýagdaý_nobat>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=nyşanyň_kody;}
static void 글내보내기(const char *setir_maglumat){while(*setir_maglumat)baýt_maglumat((unsigned char)*setir_maglumat++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)baýt_maglumat(둘째값[--순번]);}
static void ýerini_üýtget_baha(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);baýt_maglumat(';');수치(열위치);baýt_maglumat('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(Metin[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<dowamlylyk_baha){자료위치++;while(자료위치<dowamlylyk_baha&&(Metin[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int Bitir(int 자료위치){while(자료위치>0&&Metin[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int tamamla_Süýşüriş(int 자료위치){while(자료위치<dowamlylyk_baha&&Metin[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned nyşanyň_kody){return nyşanyň_kody>=196?2:1;}
static int sütün(int 자료위치){int nyşanyň_kody=0;for(int 순번=Bitir(자료위치);순번<자료위치;순번=다음(순번))nyşanyň_kody+=Metin[순번]=='\t'?4-nyşanyň_kody%4:너비(Metin[순번]);return nyşanyň_kody;}
static void barlag_nokady(void){for(int 순번=0;순번<dowamlylyk_baha;순번++)gaýtar_maglumat[순번]=Metin[순번];gaýtar_dowamlylyk=dowamlylyk_baha;위쪽=indeks_baha;gaýtar_Üýtgeşiklikler=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){barlag_nokady();for(int 순번=도착위치;순번<dowamlylyk_baha;순번++)Metin[출발위치+순번-도착위치]=Metin[순번];dowamlylyk_baha-=도착위치-출발위치;indeks_baha=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *setir_maglumat,int 개수){if(개수>편집용량-dowamlylyk_baha){알림문="File full (16384 bytes)";return 0;}barlag_nokady();for(int 순번=dowamlylyk_baha-1;순번>=indeks_baha;순번--)Metin[순번+개수]=Metin[순번];for(int 순번=0;순번<개수;순번++)Metin[indeks_baha+순번]=setir_maglumat[순번];dowamlylyk_baha+=개수;indeks_baha+=개수;변경됨=1;return 1;}
static void Dik(int 차이){int 열위치=sütün(indeks_baha),자료위치=Bitir(indeks_baha);if(차이<0){if(!자료위치)return;자료위치=Bitir(자료위치-1);}else{자료위치=tamamla_Süýşüriş(자료위치);if(자료위치==dowamlylyk_baha)return;자료위치++;}int nyşanyň_kody=0;while(자료위치<dowamlylyk_baha&&Metin[자료위치]!='\n'&&nyşanyň_kody<열위치){nyşanyň_kody+=Metin[자료위치]=='\t'?4-nyşanyň_kody%4:너비(Metin[자료위치]);자료위치=다음(자료위치);}indeks_baha=자료위치;}
static void 화면그리기(void){
    if(indeks_baha>dowamlylyk_baha)indeks_baha=dowamlylyk_baha;if(맨위>indeks_baha)맨위=Bitir(indeks_baha);맨위=Bitir(맨위);
    int 행위치=0;for(int 순번=맨위;순번<indeks_baha;순번++)if(Metin[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=tamamla_Süýşüriş(맨위);if(맨위<dowamlylyk_baha)맨위++;행위치--;}
    int 열위치=sütün(indeks_baha);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        ýerini_üýtget_baha(반환값+1,1);글내보내기("\033[0m\033[2K");int nyşanyň_kody=0,그려진상태=0;
        if(자료위치>=dowamlylyk_baha&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<dowamlylyk_baha&&Metin[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=Metin[자료위치]=='\t'?4-nyşanyň_kody%4:너비(Metin[자료위치]);
            if(nyşanyň_kody>=왼쪽&&nyşanyň_kody-왼쪽+너비값<열수){
                if(Metin[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)baýt_maglumat(' ');}else if(Metin[자료위치]<32||Metin[자료위치]==127){baýt_maglumat('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)baýt_maglumat(Metin[안쪽순번]);그려진상태+=너비값;
            }nyşanyň_kody+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<dowamlylyk_baha)자료위치++;
    }
    ýerini_üýtget_baha(행수,1);글내보내기("\033[7m\033[2K");ýagdaý_surat=1;ýagdaý_nobat=0;글내보내기(giriz?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(faýl_girizmeklik_at[이름바이트수]&&이름바이트수<30)baýt_maglumat(faýl_girizmeklik_at[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int setir=1;for(int 순번=0;순번<indeks_baha;순번++)if(Metin[순번]=='\n')setir++;수치(setir);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)baýt_maglumat(알림문[개수++]);}
    ýagdaý_surat=0;글내보내기("\033[0m");ýerini_üýtget_baha(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(garaşýar_açar){int 셋째순번=garaşýar_açar;garaşýar_açar=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Ululyk=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Ululyk&65535)||행수!=(int)(Ululyk>>16)){
            열수=Ululyk&65535;행수=Ululyk>>16;화면그리기();
            if(kömek_kategoriýa){ýerini_üýtget_baha(행수,1);글내보내기("\033[0m\033[2K");baýt_maglumat(kömek_kategoriýa);글내보내기(buýruk);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){garaşýar_açar=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_baha(void){
    int faýl_ryçag=aç_faýl(faýl_girizmeklik_at,okalýan_ýazylýan|없으면만들기|내용비우기,0600);if(faýl_ryçag<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=ýaz_faýl_maglumat(faýl_ryçag,Metin,dowamlylyk_baha);ýap_faýl(faýl_ryçag);if(개수!=dowamlylyk_baha){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(tap_girizmeklik[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=dowamlylyk_baha;순번++){int 자료위치=(indeks_baha+순번)%(dowamlylyk_baha?dowamlylyk_baha:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<dowamlylyk_baha&&Metin[자료위치+안쪽순번]==(unsigned char)tap_girizmeklik[안쪽순번])안쪽순번++;if(안쪽순번==개수){indeks_baha=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int çagyryş(int kategoriýa_baha){
    int 개수=0;buýruk[0]=0;
    for(;;){ýerini_üýtget_baha(행수,1);글내보내기("\033[0m\033[2K");baýt_maglumat(kategoriýa_baha);글내보내기(buýruk);출력비우기();kömek_kategoriýa=kategoriýa_baha;int 셋째순번=누름값();kömek_kategoriýa=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)buýruk[개수]&192)==128)개수--;buýruk[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){buýruk[개수++]=셋째순번;buýruk[개수]=0;}
    }
    if(kategoriýa_baha=='/'){for(int 순번=0;순번<=개수;순번++)tap_girizmeklik[순번]=buýruk[순번];다음찾기();return 0;}
    if(같은지(buýruk,"q!"))return 1;
    if(같은지(buýruk,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(buýruk,"wq")||같은지(buýruk,"x"))return Store_baha();
    if(같은지(buýruk,"w")){Store_baha();return 0;}
    if(buýruk[0]=='w'&&buýruk[1]==' '){int 순번=2;while(buýruk[순번]==' ')순번++;int Ululyk=개수-순번;if(Ululyk<1||Ululyk>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Ululyk;안쪽순번++)faýl_girizmeklik_at[안쪽순번]=buýruk[순번+안쪽순번];faýl_girizmeklik_at[Ululyk]=0;Store_baha();return 0;}
    int setir=0;for(int 순번=0;순번<개수;순번++){if(buýruk[순번]<'0'||buýruk[순번]>'9'){setir=0;break;}setir=setir*10+buýruk[순번]-'0';if(setir>16384){setir=0;break;}}
    if(setir){indeks_baha=0;while(--setir&&indeks_baha<dowamlylyk_baha){indeks_baha=tamamla_Süýşüriş(indeks_baha);if(indeks_baha<dowamlylyk_baha)indeks_baha++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int başlat_ulanyjy_programma(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||ulanyjy_argument(0,faýl_girizmeklik_at,sizeof(faýl_girizmeklik_at))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int faýl_ryçag=aç_faýl(faýl_girizmeklik_at,diňe_okalýan_baha,0);
    if(faýl_ryçag>=0){int 개수=faýl_ölçegi_üýtget(faýl_ryçag);if(개수<0||개수>편집용량){ýap_faýl(faýl_ryçag);return 1;}dowamlylyk_baha=파일자료읽기(faýl_ryçag,Metin,개수);ýap_faýl(faýl_ryçag);if(dowamlylyk_baha!=개수)return 1;for(int 순번=0;순번<dowamlylyk_baha;순번++)if(!Metin[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Dik(-1);continue;}if(셋째순번==1002){Dik(1);continue;}if(셋째순번==1003){indeks_baha=다음(indeks_baha);continue;}if(셋째순번==1004){indeks_baha=이전항목(indeks_baha);continue;}
        if(셋째순번==1005){indeks_baha=Bitir(indeks_baha);continue;}if(셋째순번==1006){indeks_baha=tamamla_Süýşüriş(indeks_baha);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Dik(셋째순번==1008?-1:1);continue;}
        if(giriz){
            if(셋째순번==27||셋째순번==3){giriz=0;continue;}
            if(셋째순번==127||셋째순번==8){if(indeks_baha)바이트지우기(이전항목(indeks_baha),indeks_baha);continue;}
            if(셋째순번==1007){if(indeks_baha<dowamlylyk_baha)바이트지우기(indeks_baha,다음(indeks_baha));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int nyşanyň_kody=누름값();if(nyşanyň_kody<128||nyşanyň_kody>191){garaşýar_açar=nyşanyň_kody;유효함=0;break;}둘째값[순번]=nyşanyň_kody;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){indeks_baha=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_baha();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=Bitir(indeks_baha),둘째값=tamamla_Süýşüriş(indeks_baha);if(둘째값<dowamlylyk_baha)둘째값++;synp_dowamlylyk=둘째값-첫째값;for(int 순번=0;순번<synp_dowamlylyk;순번++)복사자료[순번]=Metin[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){giriz=1;continue;}if(셋째순번=='a'){if(indeks_baha<tamamla_Süýşüriş(indeks_baha))indeks_baha=다음(indeks_baha);giriz=1;continue;}
        if(셋째순번=='I'){indeks_baha=Bitir(indeks_baha);giriz=1;continue;}if(셋째순번=='A'){indeks_baha=tamamla_Süýşüriş(indeks_baha);giriz=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char setir_tamamla='\n';indeks_baha=셋째순번=='o'?tamamla_Süýşüriş(indeks_baha):Bitir(indeks_baha);if(덧붙이기(&setir_tamamla,1)){if(셋째순번=='O')indeks_baha--;giriz=1;}continue;}
        if(셋째순번=='h'){indeks_baha=이전항목(indeks_baha);continue;}if(셋째순번=='l'){indeks_baha=다음(indeks_baha);continue;}if(셋째순번=='j'){Dik(1);continue;}if(셋째순번=='k'){Dik(-1);continue;}
        if(셋째순번=='0'){indeks_baha=Bitir(indeks_baha);continue;}if(셋째순번=='$'){indeks_baha=tamamla_Süýşüriş(indeks_baha);continue;}if(셋째순번=='G'){indeks_baha=Bitir(dowamlylyk_baha);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(indeks_baha<dowamlylyk_baha)바이트지우기(indeks_baha,다음(indeks_baha));continue;}
        if(셋째순번=='p'&&synp_dowamlylyk){indeks_baha=tamamla_Süýşüriş(indeks_baha);if(indeks_baha<dowamlylyk_baha)indeks_baha++;덧붙이기(복사자료,synp_dowamlylyk);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=Metin[순번];Metin[순번]=gaýtar_maglumat[순번];gaýtar_maglumat[순번]=둘째값;}int 개수=dowamlylyk_baha;dowamlylyk_baha=gaýtar_dowamlylyk;gaýtar_dowamlylyk=개수;개수=indeks_baha;indeks_baha=위쪽;위쪽=개수;개수=변경됨;변경됨=gaýtar_Üýtgeşiklikler;gaýtar_Üýtgeşiklikler=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=çagyryş(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
