/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_kapasiti 16384
static unsigned char Teks[Editor_kapasiti],buat_asal_data[Editor_kapasiti],복사자료[Editor_kapasiti],ukuran_data[1024];
static int kepanjangan_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,Sisip,buat_asal_kepanjangan,위쪽,buat_asal_Perubahan,되돌림있음,tika_kepanjangan,사용량,COLUMNS=68,ROW_COUNT=19;
static char fail_pemasukan_nama[64],Perintah[128],Cari_pemasukan[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned belum_selesai_Kunci;
static int bantu_bidang,status_imej,status_baris;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)ukuran_data,사용량,0,0,0);사용량=0;}}
static void bait_data(unsigned titik_kod){if(status_imej){if((titik_kod&192)!=128){status_baris+=titik_kod>=196?2:1;}if(status_baris>=COLUMNS)return;}if(사용량==(int)sizeof(ukuran_data))출력비우기();ukuran_data[사용량++]=titik_kod;}
static void 글내보내기(const char *rentetan_data){while(*rentetan_data)bait_data((unsigned char)*rentetan_data++);}
static void 수치(unsigned item_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+item_COUNT%10;item_COUNT/=10;}while(item_COUNT);while(순번)bait_data(SECOND_VALUE[--순번]);}
static void alih_VALUE(int ROW_jawatan,int lajur_jawatan){글내보내기("\033[");수치(ROW_jawatan);bait_data(';');수치(lajur_jawatan);bait_data('H');}
static int 이전항목(int data_jawatan){if(data_jawatan){data_jawatan--;while(data_jawatan>0&&(Teks[data_jawatan]&192)==128)data_jawatan--;}return data_jawatan;}
static int Seterusnya_item(int data_jawatan){if(data_jawatan<kepanjangan_VALUE){data_jawatan++;while(data_jawatan<kepanjangan_VALUE&&(Teks[data_jawatan]&192)==128)data_jawatan++;}return data_jawatan;}
static int Jalan(int data_jawatan){while(data_jawatan>0&&Teks[data_jawatan-1]!='\n')data_jawatan--;return data_jawatan;}
static int tamat_Ofset(int data_jawatan){while(data_jawatan<kepanjangan_VALUE&&Teks[data_jawatan]!='\n')data_jawatan++;return data_jawatan;}
static int 너비(unsigned titik_kod){return titik_kod>=196?2:1;}
static int lajur(int data_jawatan){int titik_kod=0;for(int 순번=Jalan(data_jawatan);순번<data_jawatan;순번=Seterusnya_item(순번))titik_kod+=Teks[순번]=='\t'?4-titik_kod%4:너비(Teks[순번]);return titik_kod;}
static void titik_semak(void){for(int 순번=0;순번<kepanjangan_VALUE;순번++)buat_asal_data[순번]=Teks[순번];buat_asal_kepanjangan=kepanjangan_VALUE;위쪽=INDEX_VALUE;buat_asal_Perubahan=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){titik_semak();for(int 순번=도착위치;순번<kepanjangan_VALUE;순번++)Teks[출발위치+순번-도착위치]=Teks[순번];kepanjangan_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int Tambah_VALUE(const unsigned char *rentetan_data,int item_COUNT){if(item_COUNT>Editor_kapasiti-kepanjangan_VALUE){알림문="File full (16384 bytes)";return 0;}titik_semak();for(int 순번=kepanjangan_VALUE-1;순번>=INDEX_VALUE;순번--)Teks[순번+item_COUNT]=Teks[순번];for(int 순번=0;순번<item_COUNT;순번++)Teks[INDEX_VALUE+순번]=rentetan_data[순번];kepanjangan_VALUE+=item_COUNT;INDEX_VALUE+=item_COUNT;변경됨=1;return 1;}
static void Menegak(int 차이){int lajur_jawatan=lajur(INDEX_VALUE),data_jawatan=Jalan(INDEX_VALUE);if(차이<0){if(!data_jawatan)return;data_jawatan=Jalan(data_jawatan-1);}else{data_jawatan=tamat_Ofset(data_jawatan);if(data_jawatan==kepanjangan_VALUE)return;data_jawatan++;}int titik_kod=0;while(data_jawatan<kepanjangan_VALUE&&Teks[data_jawatan]!='\n'&&titik_kod<lajur_jawatan){titik_kod+=Teks[data_jawatan]=='\t'?4-titik_kod%4:너비(Teks[data_jawatan]);data_jawatan=Seterusnya_item(data_jawatan);}INDEX_VALUE=data_jawatan;}
static void 화면그리기(void){
    if(INDEX_VALUE>kepanjangan_VALUE)INDEX_VALUE=kepanjangan_VALUE;if(맨위>INDEX_VALUE)맨위=Jalan(INDEX_VALUE);맨위=Jalan(맨위);
    int ROW_jawatan=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Teks[순번]=='\n')ROW_jawatan++;
    while(ROW_jawatan>=ROW_COUNT-1){맨위=tamat_Ofset(맨위);if(맨위<kepanjangan_VALUE)맨위++;ROW_jawatan--;}
    int lajur_jawatan=lajur(INDEX_VALUE);if(lajur_jawatan<왼쪽)왼쪽=lajur_jawatan;if(lajur_jawatan-왼쪽>=COLUMNS-1)왼쪽=lajur_jawatan-COLUMNS+2;
    글내보내기("\033[?25l");int data_jawatan=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        alih_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int titik_kod=0,그려진상태=0;
        if(data_jawatan>=kepanjangan_VALUE&&반환값>ROW_jawatan){글내보내기("\033[90m~\033[0m");continue;}
        while(data_jawatan<kepanjangan_VALUE&&Teks[data_jawatan]!='\n'){
            int Seterusnya_Ofset=Seterusnya_item(data_jawatan),너비값=Teks[data_jawatan]=='\t'?4-titik_kod%4:너비(Teks[data_jawatan]);
            if(titik_kod>=왼쪽&&titik_kod-왼쪽+너비값<COLUMNS){
                if(Teks[data_jawatan]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bait_data(' ');}else if(Teks[data_jawatan]<32||Teks[data_jawatan]==127){bait_data('?');}else for(int 안쪽순번=data_jawatan;안쪽순번<Seterusnya_Ofset;안쪽순번++)bait_data(Teks[안쪽순번]);그려진상태+=너비값;
            }titik_kod+=너비값;data_jawatan=Seterusnya_Ofset;
        }
        (void)그려진상태;if(data_jawatan<kepanjangan_VALUE)data_jawatan++;
    }
    alih_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");status_imej=1;status_baris=0;글내보내기(Sisip?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fail_pemasukan_nama[이름바이트수]&&이름바이트수<30)bait_data(fail_pemasukan_nama[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int baris=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Teks[순번]=='\n')baris++;수치(baris);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int item_COUNT=0;글내보내기(" | ");while(알림문[item_COUNT]&&item_COUNT<20)bait_data(알림문[item_COUNT++]);}
    status_imej=0;글내보내기("\033[0m");alih_VALUE(ROW_jawatan+1,lajur_jawatan-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(belum_selesai_Kunci){int 셋째순번=belum_selesai_Kunci;belum_selesai_Kunci=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Saiz=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Saiz&65535)||ROW_COUNT!=(int)(Saiz>>16)){
            COLUMNS=Saiz&65535;ROW_COUNT=Saiz>>16;화면그리기();
            if(bantu_bidang){alih_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bait_data(bantu_bidang);글내보내기(Perintah);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){belum_selesai_Kunci=셋째순번;return 27;}
    int item_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){item_COUNT=item_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return item_COUNT==3?1007:item_COUNT==5?1008:item_COUNT==6?1009:item_COUNT==1?1005:item_COUNT==4?1006:27;return 27;}return 27;
}
static int stor_VALUE(void){
    int fail_pemegang=buka_fail(fail_pemasukan_nama,baca_tulis|없으면만들기|potong_TOC,0600);if(fail_pemegang<0){알림문="Cannot open for save";return 0;}
    intptr_t item_COUNT=tulis_fail_data(fail_pemegang,Teks,kepanjangan_VALUE);Tutup_fail(fail_pemegang);if(item_COUNT!=kepanjangan_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void Cari_Seterusnya(void){int item_COUNT=0;while(Cari_pemasukan[item_COUNT])item_COUNT++;if(!item_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=kepanjangan_VALUE;순번++){int data_jawatan=(INDEX_VALUE+순번)%(kepanjangan_VALUE?kepanjangan_VALUE:1),안쪽순번=0;while(안쪽순번<item_COUNT&&data_jawatan+안쪽순번<kepanjangan_VALUE&&Teks[data_jawatan+안쪽순번]==(unsigned char)Cari_pemasukan[안쪽순번])안쪽순번++;if(안쪽순번==item_COUNT){INDEX_VALUE=data_jawatan;알림문="Match";return;}}알림문="Pattern not found";}
static int prom(int bidang_VALUE){
    int item_COUNT=0;Perintah[0]=0;
    for(;;){alih_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bait_data(bidang_VALUE);글내보내기(Perintah);출력비우기();bantu_bidang=bidang_VALUE;int 셋째순번=누름값();bantu_bidang=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(item_COUNT){item_COUNT--;while(item_COUNT>0&&((unsigned char)Perintah[item_COUNT]&192)==128)item_COUNT--;Perintah[item_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&item_COUNT<120){Perintah[item_COUNT++]=셋째순번;Perintah[item_COUNT]=0;}
    }
    if(bidang_VALUE=='/'){for(int 순번=0;순번<=item_COUNT;순번++)Cari_pemasukan[순번]=Perintah[순번];Cari_Seterusnya();return 0;}
    if(같은지(Perintah,"q!"))return 1;
    if(같은지(Perintah,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Perintah,"wq")||같은지(Perintah,"x"))return stor_VALUE();
    if(같은지(Perintah,"w")){stor_VALUE();return 0;}
    if(Perintah[0]=='w'&&Perintah[1]==' '){int 순번=2;while(Perintah[순번]==' ')순번++;int Saiz=item_COUNT-순번;if(Saiz<1||Saiz>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Saiz;안쪽순번++)fail_pemasukan_nama[안쪽순번]=Perintah[순번+안쪽순번];fail_pemasukan_nama[Saiz]=0;stor_VALUE();return 0;}
    int baris=0;for(int 순번=0;순번<item_COUNT;순번++){if(Perintah[순번]<'0'||Perintah[순번]>'9'){baris=0;break;}baris=baris*10+Perintah[순번]-'0';if(baris>16384){baris=0;break;}}
    if(baris){INDEX_VALUE=0;while(--baris&&INDEX_VALUE<kepanjangan_VALUE){INDEX_VALUE=tamat_Ofset(INDEX_VALUE);if(INDEX_VALUE<kepanjangan_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Mula_pengguna_aplikasi(int 무시값){
    (void)무시값;if(pengguna_argumen_COUNT()!=1||pengguna_argumen(0,fail_pemasukan_nama,sizeof(fail_pemasukan_nama))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fail_pemegang=buka_fail(fail_pemasukan_nama,baca_sahaja_VALUE,0);
    if(fail_pemegang>=0){int item_COUNT=saiz_fail(fail_pemegang);if(item_COUNT<0||item_COUNT>Editor_kapasiti){Tutup_fail(fail_pemegang);return 1;}kepanjangan_VALUE=파일자료읽기(fail_pemegang,Teks,item_COUNT);Tutup_fail(fail_pemegang);if(kepanjangan_VALUE!=item_COUNT)return 1;for(int 순번=0;순번<kepanjangan_VALUE;순번++)if(!Teks[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,keluar_aplikasi=0;
    while(!keluar_aplikasi){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Menegak(-1);continue;}if(셋째순번==1002){Menegak(1);continue;}if(셋째순번==1003){INDEX_VALUE=Seterusnya_item(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Jalan(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=tamat_Ofset(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Menegak(셋째순번==1008?-1:1);continue;}
        if(Sisip){
            if(셋째순번==27||셋째순번==3){Sisip=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<kepanjangan_VALUE)바이트지우기(INDEX_VALUE,Seterusnya_item(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int item_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!item_COUNT){알림문="Invalid UTF-8";continue;}int sah=1;for(int 순번=1;순번<item_COUNT;순번++){int titik_kod=누름값();if(titik_kod<128||titik_kod>191){belum_selesai_Kunci=titik_kod;sah=0;break;}SECOND_VALUE[순번]=titik_kod;}
                if(sah)Tambah_VALUE(SECOND_VALUE,item_COUNT);
            }continue;
        }
        if(앞부분){int data_jawatan=앞부분;앞부분=0;if(data_jawatan=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(data_jawatan=='Z'&&셋째순번=='Z'){keluar_aplikasi=stor_VALUE();continue;}if((data_jawatan=='d'&&셋째순번=='d')||(data_jawatan=='y'&&셋째순번=='y')){int 첫째값=Jalan(INDEX_VALUE),SECOND_VALUE=tamat_Ofset(INDEX_VALUE);if(SECOND_VALUE<kepanjangan_VALUE)SECOND_VALUE++;tika_kepanjangan=SECOND_VALUE-첫째값;for(int 순번=0;순번<tika_kepanjangan;순번++)복사자료[순번]=Teks[첫째값+순번];if(data_jawatan=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Sisip=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<tamat_Ofset(INDEX_VALUE))INDEX_VALUE=Seterusnya_item(INDEX_VALUE);Sisip=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Jalan(INDEX_VALUE);Sisip=1;continue;}if(셋째순번=='A'){INDEX_VALUE=tamat_Ofset(INDEX_VALUE);Sisip=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char baris_tamat='\n';INDEX_VALUE=셋째순번=='o'?tamat_Ofset(INDEX_VALUE):Jalan(INDEX_VALUE);if(Tambah_VALUE(&baris_tamat,1)){if(셋째순번=='O')INDEX_VALUE--;Sisip=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Seterusnya_item(INDEX_VALUE);continue;}if(셋째순번=='j'){Menegak(1);continue;}if(셋째순번=='k'){Menegak(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Jalan(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=tamat_Ofset(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Jalan(kepanjangan_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<kepanjangan_VALUE)바이트지우기(INDEX_VALUE,Seterusnya_item(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&tika_kepanjangan){INDEX_VALUE=tamat_Ofset(INDEX_VALUE);if(INDEX_VALUE<kepanjangan_VALUE)INDEX_VALUE++;Tambah_VALUE(복사자료,tika_kepanjangan);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_kapasiti;순번++){unsigned char SECOND_VALUE=Teks[순번];Teks[순번]=buat_asal_data[순번];buat_asal_data[순번]=SECOND_VALUE;}int item_COUNT=kepanjangan_VALUE;kepanjangan_VALUE=buat_asal_kepanjangan;buat_asal_kepanjangan=item_COUNT;item_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=item_COUNT;item_COUNT=변경됨;변경됨=buat_asal_Perubahan;buat_asal_Perubahan=item_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){keluar_aplikasi=prom(셋째순번);continue;}if(셋째순번=='n'){Cari_Seterusnya();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
