// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktif cangkerang 문법. 파이프는 순차 laksanakan_perintah, 환경은 같은 셸에서 공유한다. */
public final class cangkerang_sintaks {
    static int[] SUMBER = new int[4 * 4096], 종류 = new int[4 * 128], Jalan = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] pemboleh_ubah_nama = new int[16 * 32], pemboleh_ubah_data = new int[16 * 256], 이름길이 = new int[16], VALUE_kepanjangan = new int[16];
    static int[] skrip_VALUE = new int[4 * 16384];
    static int status_VALUE, 깊이, 쓴수;
    static boolean 연결중, skrip_tamat, sambungan_ralat;
    static boolean nama_aksara(int titik_kod) { return titik_kod >= 'a' && titik_kod <= 'z' || titik_kod >= 'A' && titik_kod <= 'Z' || titik_kod == '_' || titik_kod >= 128; }
    static boolean 이름뒤(int titik_kod) { return nama_aksara(titik_kod) || titik_kod >= '0' && titik_kod <= '9'; }
    static void RALAT(String Teks) { Papan.입출력전환(0); 단말.Tulis("Perintah hurai_VALUE: "); 단말.Tulis(Teks); 단말.문자(10); status_VALUE = 2; }
    static int Baca(int pemasukan_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_jawatan = 중첩깊이 * 4096, 특수문자 = 중첩깊이 * 128;
        while (현재자리 < pemasukan_COUNT) {
            while (현재자리 < pemasukan_COUNT && (SUMBER[BASE_jawatan + 현재자리] == 32 || SUMBER[BASE_jawatan + 현재자리] == 9)) 현재자리++;
            if (현재자리 == pemasukan_COUNT || SUMBER[BASE_jawatan + 현재자리] == '#') break;
            if (총수 == 128) { RALAT("낱말이 너무 많습니다"); return -1; }
            int Mula_jawatan = 현재자리, titik_kod = SUMBER[BASE_jawatan + 현재자리], 자료종류 = 0;
            if (titik_kod == ';') { 자료종류 = 1; 현재자리++; }
            else if (titik_kod == '&') { if (현재자리 + 1 >= pemasukan_COUNT || SUMBER[BASE_jawatan + 현재자리 + 1] != '&') { RALAT("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (titik_kod == '|') { 현재자리++; 자료종류 = 현재자리 < pemasukan_COUNT && SUMBER[BASE_jawatan + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (titik_kod == '>') { 현재자리++; 자료종류 = 현재자리 < pemasukan_COUNT && SUMBER[BASE_jawatan + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (titik_kod == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Petikan = 0;
                while (현재자리 < pemasukan_COUNT) {
                    titik_kod = SUMBER[BASE_jawatan + 현재자리];
                    if (titik_kod == '`' && Petikan != 39 || titik_kod == '$' && Petikan != 39 && 현재자리 + 1 < pemasukan_COUNT && SUMBER[BASE_jawatan + 현재자리 + 1] == '(') { RALAT("Perintah ukuran 치환은 지원하지 않습니다"); return -1; }
                    if (titik_kod == '\\' && Petikan != 39) { if (++현재자리 == pemasukan_COUNT) { RALAT("baris 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (titik_kod == Petikan) { Petikan = 0; 현재자리++; continue; }
                    if (Petikan == 0 && (titik_kod == 39 || titik_kod == 34)) { Petikan = titik_kod; 현재자리++; continue; }
                    if (Petikan == 0 && (titik_kod == 32 || titik_kod == 9 || titik_kod == ';' || titik_kod == '&' || titik_kod == '|' || titik_kod == '<' || titik_kod == '>')) break;
                    현재자리++;
                }
                if (Petikan != 0) { RALAT("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < pemasukan_COUNT && (SUMBER[BASE_jawatan + 현재자리] == '>' || SUMBER[BASE_jawatan + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Mula_jawatan;
                    for (int Loop_INDEX = Mula_jawatan; Loop_INDEX < 현재자리; Loop_INDEX++) if (SUMBER[BASE_jawatan + Loop_INDEX] < '0' || SUMBER[BASE_jawatan + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { RALAT("번호를 지정한 Fail 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[특수문자 + 총수] = 자료종류; Jalan[특수문자 + 총수] = Mula_jawatan; 끝[특수문자 + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[특수문자 + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[특수문자 + Loop_INDEX] != 0) { RALAT("I_O 전환에 Fail 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { RALAT("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[특수문자 + 총수 - 1] != 1) { RALAT("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean julat_SMS(int[] data_ARRAY, int setempat_Mula, int pemasukan_COUNT, String aksara_jawatan) {
        if (pemasukan_COUNT != aksara_jawatan.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) if (data_ARRAY[setempat_Mula + Loop_INDEX] != aksara_jawatan.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bait_data) {
        if (쓴수 >= pentafsir_perintah.token_VALUE.length) { if (!sambungan_ralat) RALAT("변수를 펼친 명령이 너무 깁니다"); sambungan_ralat = true; return; }
        pentafsir_perintah.token_VALUE[쓴수++] = bait_data;
    }
    static void pemboleh_ubah_VALUE(int[] data_ARRAY, int Mula_jawatan, int pemasukan_COUNT) {
        if (julat_SMS(data_ARRAY, Mula_jawatan, pemasukan_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memori_Fail.현재길이; Loop_INDEX++) 넣기(Memori_Fail.현재[Loop_INDEX]); return; }
        if (julat_SMS(data_ARRAY, Mula_jawatan, pemasukan_COUNT, "HOME")) { 넣기('/'); return; }
        if (julat_SMS(data_ARRAY, Mula_jawatan, pemasukan_COUNT, "?")) {
            int data_VALUE = status_VALUE, digit = 100; boolean 시작여부 = false;
            while (digit > 0) { int 뒷값 = data_VALUE / digit; if (뒷값 != 0 || 시작여부 || digit == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VALUE %= digit; digit /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == pemasukan_COUNT) {
            boolean MATCH = true; for (int dalaman_jawatan = 0; dalaman_jawatan < pemasukan_COUNT; dalaman_jawatan++) if (pemboleh_ubah_nama[Loop_INDEX * 32 + dalaman_jawatan] != data_ARRAY[Mula_jawatan + dalaman_jawatan]) MATCH = false;
            if (MATCH) { for (int dalaman_jawatan = 0; dalaman_jawatan < VALUE_kepanjangan[Loop_INDEX]; dalaman_jawatan++) 넣기(pemboleh_ubah_data[Loop_INDEX * 256 + dalaman_jawatan]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Jalan[중첩깊이 * 128 + 낱말번호], tamat_jawatan = 끝[중첩깊이 * 128 + 낱말번호], BASE_jawatan = 중첩깊이 * 4096, Petikan = 0;
        if (읽는자리 < tamat_jawatan && SUMBER[BASE_jawatan + 읽는자리] == '~' && (읽는자리 + 1 == tamat_jawatan || SUMBER[BASE_jawatan + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < tamat_jawatan) {
            int titik_kod = SUMBER[BASE_jawatan + 읽는자리++];
            if (titik_kod == Petikan) { Petikan = 0; continue; }
            if (Petikan == 0 && (titik_kod == 39 || titik_kod == 34)) { Petikan = titik_kod; continue; }
            if (titik_kod == '\\' && Petikan != 39) { int Seterusnya_jawatan = SUMBER[BASE_jawatan + 읽는자리++]; if (Petikan == 34 && Seterusnya_jawatan != '$' && Seterusnya_jawatan != '"' && Seterusnya_jawatan != '\\') 넣기('\\'); 넣기(Seterusnya_jawatan); continue; }
            if (titik_kod == '$' && Petikan != 39 && 읽는자리 < tamat_jawatan) {
                boolean 중괄호자리 = SUMBER[BASE_jawatan + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < tamat_jawatan && SUMBER[BASE_jawatan + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < tamat_jawatan && 이름뒤(SUMBER[BASE_jawatan + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == tamat_jawatan || SUMBER[BASE_jawatan + 읽는자리] != '}')) { RALAT("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                pemboleh_ubah_VALUE(SUMBER, BASE_jawatan + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(titik_kod);
        }
        return !sambungan_ralat;
    }
    static int persekitaran_Seting(int argumen_INDEX, boolean alih_keluar) {
        int setempat_Mula = pentafsir_perintah.시작점[argumen_INDEX], tamat_jawatan = setempat_Mula + pentafsir_perintah.kepanjangan_VALUE[argumen_INDEX], 같음자리 = setempat_Mula;
        while (같음자리 < tamat_jawatan && pentafsir_perintah.token_VALUE[같음자리] != '=') 같음자리++;
        int pemasukan_COUNT = 같음자리 - setempat_Mula;
        if (pemasukan_COUNT < 1 || pemasukan_COUNT > 31 || !nama_aksara(pentafsir_perintah.token_VALUE[setempat_Mula]) || !alih_keluar && 같음자리 == tamat_jawatan || tamat_jawatan - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = setempat_Mula; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(pentafsir_perintah.token_VALUE[Loop_INDEX])) return 2;
        if (julat_SMS(pentafsir_perintah.token_VALUE, setempat_Mula, pemasukan_COUNT, "PWD") || julat_SMS(pentafsir_perintah.token_VALUE, setempat_Mula, pemasukan_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != pemasukan_COUNT) continue;
            boolean MATCH = true; for (int dalaman_jawatan = 0; dalaman_jawatan < pemasukan_COUNT; dalaman_jawatan++) if (pemboleh_ubah_nama[Loop_INDEX * 32 + dalaman_jawatan] != pentafsir_perintah.token_VALUE[setempat_Mula + dalaman_jawatan]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (alih_keluar) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = pemasukan_COUNT; VALUE_kepanjangan[찾은여부] = tamat_jawatan - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) pemboleh_ubah_nama[찾은여부 * 32 + Loop_INDEX] = pentafsir_perintah.token_VALUE[setempat_Mula + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < tamat_jawatan; Loop_INDEX++) pemboleh_ubah_data[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = pentafsir_perintah.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void tayang_persekitaran() {
        단말.Tulis("HOME=/\nPWD="); Memori_Fail.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int dalaman_jawatan = 0; dalaman_jawatan < 이름길이[Loop_INDEX]; dalaman_jawatan++) Papan.직렬쓰기(pemboleh_ubah_nama[Loop_INDEX * 32 + dalaman_jawatan]); 단말.문자('=');
            for (int dalaman_jawatan = 0; dalaman_jawatan < VALUE_kepanjangan[Loop_INDEX]; dalaman_jawatan++) Papan.직렬쓰기(pemboleh_ubah_data[Loop_INDEX * 256 + dalaman_jawatan]); 단말.문자(10);
        }
    }
    static void laksanakan_perintah(int[] data_ARRAY, int 시작변위, int pemasukan_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || pemasukan_COUNT > 4096) { RALAT("Perintah 파일의 penyarangan_VALUE 또는 baris kepanjangan_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) SUMBER[중첩깊이 * 4096 + Loop_INDEX] = data_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = Baca(pemasukan_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Kumpulan_tamat = 읽는자리;
            while (Kumpulan_tamat < 총수 && (종류[중첩깊이 * 128 + Kumpulan_tamat] == 0 || 종류[중첩깊이 * 128 + Kumpulan_tamat] >= 4)) Kumpulan_tamat++;
            boolean laksanakan = 조건성립 == 1 || 조건성립 == 2 && status_VALUE == 0 || 조건성립 == 3 && status_VALUE != 0;
            if (laksanakan) {
                boolean 이전자리 = false;
                while (읽는자리 < Kumpulan_tamat) {
                    int Seterusnya_jawatan = 읽는자리; while (Seterusnya_jawatan < Kumpulan_tamat && 종류[중첩깊이 * 128 + Seterusnya_jawatan] != 4) Seterusnya_jawatan++;
                    boolean CONNECT_strim = Seterusnya_jawatan < Kumpulan_tamat; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    pentafsir_perintah.token_COUNT = 0; 쓴수 = 0; sambungan_ralat = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Seterusnya_jawatan; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { RALAT("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { RALAT("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (pentafsir_perintah.token_COUNT == 32) { RALAT("인수가 너무 많습니다"); return; }
                        int argumen_INDEX = pentafsir_perintah.token_COUNT++; pentafsir_perintah.시작점[argumen_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        pentafsir_perintah.kepanjangan_VALUE[argumen_INDEX] = 쓴수 - pentafsir_perintah.시작점[argumen_INDEX];
                    }
                    연결중 = 이전자리 || CONNECT_strim || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (pentafsir_perintah.같음(0, "vi") || pentafsir_perintah.같음(0, "edit") || pentafsir_perintah.같음(0, "load") || pentafsir_perintah.같음(0, "gui") || pentafsir_perintah.같음(0, "terminal") || pentafsir_perintah.같음(0, "sh") || pentafsir_perintah.같음(0, "source"))) { RALAT("interaktif 명령과 Perintah 파일은 I_O 전환이나 strim_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Jalan(이전자리, CONNECT_strim);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int pemasukan_jawatan = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (pemasukan_jawatan < 0) continue;
                        int Mula_jawatan = 쓴수; if (!Word_VALUE(pemasukan_jawatan, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memori_Fail.laluan_Mula(쓴수 - Mula_jawatan);
                        for (int dalaman_jawatan = Mula_jawatan; 처리값 >= 0 && dalaman_jawatan < 쓴수; dalaman_jawatan++) 처리값 = Memori_Fail.laluan_bait(dalaman_jawatan - Mula_jawatan, pentafsir_perintah.token_VALUE[dalaman_jawatan]);
                        if (처리값 >= 0) 처리값 = Memori_Fail.Buka(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); pentafsir_perintah.RALAT(처리값); status_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.fail_input = 처리값; else 셸입출력.출력파일 = 처리값;
                    }
                    셸입출력.Izin_interaktif = 중첩깊이 == 0 && 읽는자리 == 0 && Seterusnya_jawatan == 총수;
                    깊이 = 중첩깊이; pentafsir_perintah.ukuran = 0; Papan.입출력전환(1);
                    pentafsir_perintah.Perintah();
                    Papan.Terminal(3);
                    int 반환값 = pentafsir_perintah.ukuran, strim_ralat = 셸입출력.kegagalan_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    status_VALUE = strim_ralat < 0 ? 1 : 반환값;
                    if (strim_ralat < 0) { pentafsir_perintah.RALAT(strim_ralat); return; }
                    if (skrip_tamat || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Seterusnya_jawatan + 1;
                }
            }
            if (Kumpulan_tamat < 총수) 조건성립 = 종류[중첩깊이 * 128 + Kumpulan_tamat];
            읽는자리 = Kumpulan_tamat + 1;
        }
    }
    static void laksanakan_fail() {
        if (pentafsir_perintah.token_COUNT != 2 || 깊이 >= 3) { pentafsir_perintah.ukuran = 2; 단말.Tulis("사용법: sh Fail (penyarangan_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = pentafsir_perintah.LALUAN(1); if (처리값 >= 0) 처리값 = Memori_Fail.Buka(0);
        if (처리값 < 0) { pentafsir_perintah.RALAT(처리값); return; }
        int pemasukan_COUNT = 0, bait_data;
        while ((bait_data = Memori_Fail.Baca(처리값)) != 256 && bait_data >= 0 && pemasukan_COUNT < 16384) skrip_VALUE[중첩깊이 * 16384 + pemasukan_COUNT++] = bait_data;
        Memori_Fail.Tutup(처리값); Papan.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < pemasukan_COUNT && !skrip_tamat;) {
            int tamat_jawatan = 읽는자리; while (tamat_jawatan < pemasukan_COUNT && skrip_VALUE[중첩깊이 * 16384 + tamat_jawatan] != 10) tamat_jawatan++;
            int sah_kepanjangan = tamat_jawatan - 읽는자리; if (sah_kepanjangan > 0 && skrip_VALUE[중첩깊이 * 16384 + tamat_jawatan - 1] == 13) sah_kepanjangan--;
            laksanakan_perintah(skrip_VALUE, 중첩깊이 * 16384 + 읽는자리, sah_kepanjangan, 중첩깊이); 읽는자리 = tamat_jawatan + 1;
        }
        pentafsir_perintah.ukuran = status_VALUE; skrip_tamat = false; 깊이 = 중첩깊이 - 1;
    }
}
