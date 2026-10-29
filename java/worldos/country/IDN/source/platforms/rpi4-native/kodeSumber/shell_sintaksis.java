// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktif shell 문법. 파이프는 순차 Jalankan_perintah, 환경은 같은 셸에서 공유한다. */
public final class shell_sintaksis {
    static int[] kodeSumber = new int[4 * 4096], 종류 = new int[4 * 128], jalankan = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabel_nama = new int[16 * 32], variabel_data = new int[16 * 256], 이름길이 = new int[16], VALUE_panjang = new int[16];
    static int[] skrip_VALUE = new int[4 * 16384];
    static int Status_VALUE, 깊이, 쓴수;
    static boolean 연결중, skrip_mengakhiri, ekstensi_kesalahan;
    static boolean nama_karakter(int kode_karakter) { return kode_karakter >= 'a' && kode_karakter <= 'z' || kode_karakter >= 'A' && kode_karakter <= 'Z' || kode_karakter == '_' || kode_karakter >= 128; }
    static boolean 이름뒤(int kode_karakter) { return nama_karakter(kode_karakter) || kode_karakter >= '0' && kode_karakter <= '9'; }
    static void galat(String teks) { Papan.입출력전환(0); 단말.Tulis("perintah urai_VALUE: "); 단말.Tulis(teks); 단말.문자(10); Status_VALUE = 2; }
    static int Baca(int entri_COUNT, int 중첩깊이) {
        int saat_ini_INDEX = 0, total_COUNT = 0, BASE_posisi = 중첩깊이 * 4096, karakter_khusus = 중첩깊이 * 128;
        while (saat_ini_INDEX < entri_COUNT) {
            while (saat_ini_INDEX < entri_COUNT && (kodeSumber[BASE_posisi + saat_ini_INDEX] == 32 || kodeSumber[BASE_posisi + saat_ini_INDEX] == 9)) saat_ini_INDEX++;
            if (saat_ini_INDEX == entri_COUNT || kodeSumber[BASE_posisi + saat_ini_INDEX] == '#') break;
            if (total_COUNT == 128) { galat("낱말이 너무 많습니다"); return -1; }
            int Mulai_posisi = saat_ini_INDEX, kode_karakter = kodeSumber[BASE_posisi + saat_ini_INDEX], 자료종류 = 0;
            if (kode_karakter == ';') { 자료종류 = 1; saat_ini_INDEX++; }
            else if (kode_karakter == '&') { if (saat_ini_INDEX + 1 >= entri_COUNT || kodeSumber[BASE_posisi + saat_ini_INDEX + 1] != '&') { galat("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; saat_ini_INDEX += 2; }
            else if (kode_karakter == '|') { saat_ini_INDEX++; 자료종류 = saat_ini_INDEX < entri_COUNT && kodeSumber[BASE_posisi + saat_ini_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) saat_ini_INDEX++; }
            else if (kode_karakter == '>') { saat_ini_INDEX++; 자료종류 = saat_ini_INDEX < entri_COUNT && kodeSumber[BASE_posisi + saat_ini_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) saat_ini_INDEX++; }
            else if (kode_karakter == '<') { 자료종류 = 7; saat_ini_INDEX++; }
            else {
                int Kutipan = 0;
                while (saat_ini_INDEX < entri_COUNT) {
                    kode_karakter = kodeSumber[BASE_posisi + saat_ini_INDEX];
                    if (kode_karakter == '`' && Kutipan != 39 || kode_karakter == '$' && Kutipan != 39 && saat_ini_INDEX + 1 < entri_COUNT && kodeSumber[BASE_posisi + saat_ini_INDEX + 1] == '(') { galat("perintah hasil 치환은 지원하지 않습니다"); return -1; }
                    if (kode_karakter == '\\' && Kutipan != 39) { if (++saat_ini_INDEX == entri_COUNT) { galat("baris_masukan 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } saat_ini_INDEX++; continue; }
                    if (kode_karakter == Kutipan) { Kutipan = 0; saat_ini_INDEX++; continue; }
                    if (Kutipan == 0 && (kode_karakter == 39 || kode_karakter == 34)) { Kutipan = kode_karakter; saat_ini_INDEX++; continue; }
                    if (Kutipan == 0 && (kode_karakter == 32 || kode_karakter == 9 || kode_karakter == ';' || kode_karakter == '&' || kode_karakter == '|' || kode_karakter == '<' || kode_karakter == '>')) break;
                    saat_ini_INDEX++;
                }
                if (Kutipan != 0) { galat("따옴표가 닫히지 않았습니다"); return -1; }
                if (saat_ini_INDEX < entri_COUNT && (kodeSumber[BASE_posisi + saat_ini_INDEX] == '>' || kodeSumber[BASE_posisi + saat_ini_INDEX] == '<')) {
                    boolean 수치 = saat_ini_INDEX > Mulai_posisi;
                    for (int Loop_INDEX = Mulai_posisi; Loop_INDEX < saat_ini_INDEX; Loop_INDEX++) if (kodeSumber[BASE_posisi + Loop_INDEX] < '0' || kodeSumber[BASE_posisi + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { galat("번호를 지정한 berkas 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[karakter_khusus + total_COUNT] = 자료종류; jalankan[karakter_khusus + total_COUNT] = Mulai_posisi; 끝[karakter_khusus + total_COUNT] = saat_ini_INDEX; total_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < total_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[karakter_khusus + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == total_COUNT || 종류[karakter_khusus + Loop_INDEX] != 0) { galat("I_O 전환에 berkas 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == total_COUNT - 1 && 임시값 != 1) { galat("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (total_COUNT > 0 && !낱말 && 종류[karakter_khusus + total_COUNT - 1] != 1) { galat("명령이 빠졌습니다"); return -1; }
        return total_COUNT;
    }
    static boolean rentang_SMS(int[] data_ARRAY, int lokal_Mulai, int entri_COUNT, String karakter_posisi) {
        if (entri_COUNT != karakter_posisi.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) if (data_ARRAY[lokal_Mulai + Loop_INDEX] != karakter_posisi.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_data) {
        if (쓴수 >= PenafsirPerintah.token_VALUE.length) { if (!ekstensi_kesalahan) galat("변수를 펼친 명령이 너무 깁니다"); ekstensi_kesalahan = true; return; }
        PenafsirPerintah.token_VALUE[쓴수++] = byte_data;
    }
    static void variabel_VALUE(int[] data_ARRAY, int Mulai_posisi, int entri_COUNT) {
        if (rentang_SMS(data_ARRAY, Mulai_posisi, entri_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < BerkasMemori.saat_ini_panjang; Loop_INDEX++) 넣기(BerkasMemori.saat_ini_item[Loop_INDEX]); return; }
        if (rentang_SMS(data_ARRAY, Mulai_posisi, entri_COUNT, "HOME")) { 넣기('/'); return; }
        if (rentang_SMS(data_ARRAY, Mulai_posisi, entri_COUNT, "?")) {
            int data_VALUE = Status_VALUE, angka = 100; boolean 시작여부 = false;
            while (angka > 0) { int berikutnya_VALUE = data_VALUE / angka; if (berikutnya_VALUE != 0 || 시작여부 || angka == 1) { 넣기('0' + berikutnya_VALUE); 시작여부 = true; } data_VALUE %= angka; angka /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == entri_COUNT) {
            boolean MATCH = true; for (int dalam_posisi = 0; dalam_posisi < entri_COUNT; dalam_posisi++) if (variabel_nama[Loop_INDEX * 32 + dalam_posisi] != data_ARRAY[Mulai_posisi + dalam_posisi]) MATCH = false;
            if (MATCH) { for (int dalam_posisi = 0; dalam_posisi < VALUE_panjang[Loop_INDEX]; dalam_posisi++) 넣기(variabel_data[Loop_INDEX * 256 + dalam_posisi]); return; }
        }
    }
    static boolean Kata_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = jalankan[중첩깊이 * 128 + 낱말번호], mengakhiri_posisi = 끝[중첩깊이 * 128 + 낱말번호], BASE_posisi = 중첩깊이 * 4096, Kutipan = 0;
        if (읽는자리 < mengakhiri_posisi && kodeSumber[BASE_posisi + 읽는자리] == '~' && (읽는자리 + 1 == mengakhiri_posisi || kodeSumber[BASE_posisi + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < mengakhiri_posisi) {
            int kode_karakter = kodeSumber[BASE_posisi + 읽는자리++];
            if (kode_karakter == Kutipan) { Kutipan = 0; continue; }
            if (Kutipan == 0 && (kode_karakter == 39 || kode_karakter == 34)) { Kutipan = kode_karakter; continue; }
            if (kode_karakter == '\\' && Kutipan != 39) { int Berikutnya_posisi = kodeSumber[BASE_posisi + 읽는자리++]; if (Kutipan == 34 && Berikutnya_posisi != '$' && Berikutnya_posisi != '"' && Berikutnya_posisi != '\\') 넣기('\\'); 넣기(Berikutnya_posisi); continue; }
            if (kode_karakter == '$' && Kutipan != 39 && 읽는자리 < mengakhiri_posisi) {
                boolean 중괄호자리 = kodeSumber[BASE_posisi + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < mengakhiri_posisi && kodeSumber[BASE_posisi + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < mengakhiri_posisi && 이름뒤(kodeSumber[BASE_posisi + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == mengakhiri_posisi || kodeSumber[BASE_posisi + 읽는자리] != '}')) { galat("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabel_VALUE(kodeSumber, BASE_posisi + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kode_karakter);
        }
        return !ekstensi_kesalahan;
    }
    static int lingkungan_Pengaturan(int argumen_INDEX, boolean hapus) {
        int lokal_Mulai = PenafsirPerintah.시작점[argumen_INDEX], mengakhiri_posisi = lokal_Mulai + PenafsirPerintah.panjang_VALUE[argumen_INDEX], 같음자리 = lokal_Mulai;
        while (같음자리 < mengakhiri_posisi && PenafsirPerintah.token_VALUE[같음자리] != '=') 같음자리++;
        int entri_COUNT = 같음자리 - lokal_Mulai;
        if (entri_COUNT < 1 || entri_COUNT > 31 || !nama_karakter(PenafsirPerintah.token_VALUE[lokal_Mulai]) || !hapus && 같음자리 == mengakhiri_posisi || mengakhiri_posisi - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokal_Mulai; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(PenafsirPerintah.token_VALUE[Loop_INDEX])) return 2;
        if (rentang_SMS(PenafsirPerintah.token_VALUE, lokal_Mulai, entri_COUNT, "PWD") || rentang_SMS(PenafsirPerintah.token_VALUE, lokal_Mulai, entri_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, teknologi_informasi_kosong_Status = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) teknologi_informasi_kosong_Status = Loop_INDEX;
            if (이름길이[Loop_INDEX] != entri_COUNT) continue;
            boolean MATCH = true; for (int dalam_posisi = 0; dalam_posisi < entri_COUNT; dalam_posisi++) if (variabel_nama[Loop_INDEX * 32 + dalam_posisi] != PenafsirPerintah.token_VALUE[lokal_Mulai + dalam_posisi]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (hapus) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = teknologi_informasi_kosong_Status; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = entri_COUNT; VALUE_panjang[찾은여부] = mengakhiri_posisi - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) variabel_nama[찾은여부 * 32 + Loop_INDEX] = PenafsirPerintah.token_VALUE[lokal_Mulai + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < mengakhiri_posisi; Loop_INDEX++) variabel_data[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = PenafsirPerintah.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void show_lingkungan() {
        단말.Tulis("HOME=/\nPWD="); BerkasMemori.saat_ini_tulis(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int dalam_posisi = 0; dalam_posisi < 이름길이[Loop_INDEX]; dalam_posisi++) Papan.직렬쓰기(variabel_nama[Loop_INDEX * 32 + dalam_posisi]); 단말.문자('=');
            for (int dalam_posisi = 0; dalam_posisi < VALUE_panjang[Loop_INDEX]; dalam_posisi++) Papan.직렬쓰기(variabel_data[Loop_INDEX * 256 + dalam_posisi]); 단말.문자(10);
        }
    }
    static void Jalankan_perintah(int[] data_ARRAY, int 시작변위, int entri_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || entri_COUNT > 4096) { galat("perintah 파일의 berlapis_VALUE 또는 baris_masukan panjang_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) kodeSumber[중첩깊이 * 4096 + Loop_INDEX] = data_ARRAY[시작변위 + Loop_INDEX];
        int total_COUNT = Baca(entri_COUNT, 중첩깊이); if (total_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < total_COUNT) {
            int grup_mengakhiri = 읽는자리;
            while (grup_mengakhiri < total_COUNT && (종류[중첩깊이 * 128 + grup_mengakhiri] == 0 || 종류[중첩깊이 * 128 + grup_mengakhiri] >= 4)) grup_mengakhiri++;
            boolean Jalankan = 조건성립 == 1 || 조건성립 == 2 && Status_VALUE == 0 || 조건성립 == 3 && Status_VALUE != 0;
            if (Jalankan) {
                boolean 이전자리 = false;
                while (읽는자리 < grup_mengakhiri) {
                    int Berikutnya_posisi = 읽는자리; while (Berikutnya_posisi < grup_mengakhiri && 종류[중첩깊이 * 128 + Berikutnya_posisi] != 4) Berikutnya_posisi++;
                    boolean CONNECT_Stream = Berikutnya_posisi < grup_mengakhiri; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    PenafsirPerintah.token_COUNT = 0; 쓴수 = 0; ekstensi_kesalahan = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Berikutnya_posisi; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { galat("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { galat("keluaranTeks 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (PenafsirPerintah.token_COUNT == 32) { galat("인수가 너무 많습니다"); return; }
                        int argumen_INDEX = PenafsirPerintah.token_COUNT++; PenafsirPerintah.시작점[argumen_INDEX] = 쓴수;
                        if (!Kata_VALUE(Loop_INDEX, 중첩깊이)) return;
                        PenafsirPerintah.panjang_VALUE[argumen_INDEX] = 쓴수 - PenafsirPerintah.시작점[argumen_INDEX];
                    }
                    연결중 = 이전자리 || CONNECT_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (PenafsirPerintah.같음(0, "vi") || PenafsirPerintah.같음(0, "edit") || PenafsirPerintah.같음(0, "load") || PenafsirPerintah.같음(0, "gui") || PenafsirPerintah.같음(0, "terminal") || PenafsirPerintah.같음(0, "sh") || PenafsirPerintah.같음(0, "source"))) { galat("interaktif 명령과 perintah 파일은 I_O 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.jalankan(이전자리, CONNECT_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int entri_posisi = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (entri_posisi < 0) continue;
                        int Mulai_posisi = 쓴수; if (!Kata_VALUE(entri_posisi, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = BerkasMemori.jalur_Mulai(쓴수 - Mulai_posisi);
                        for (int dalam_posisi = Mulai_posisi; 처리값 >= 0 && dalam_posisi < 쓴수; dalam_posisi++) 처리값 = BerkasMemori.jalur_byte(dalam_posisi - Mulai_posisi, PenafsirPerintah.token_VALUE[dalam_posisi]);
                        if (처리값 >= 0) 처리값 = BerkasMemori.Buka(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); PenafsirPerintah.galat(처리값); Status_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.file_input = 처리값; else 셸입출력.file_output = 처리값;
                    }
                    셸입출력.Perbolehkan_interaktif = 중첩깊이 == 0 && 읽는자리 == 0 && Berikutnya_posisi == total_COUNT;
                    깊이 = 중첩깊이; PenafsirPerintah.hasil = 0; Papan.입출력전환(1);
                    PenafsirPerintah.perintah();
                    Papan.terminal(3);
                    int 반환값 = PenafsirPerintah.hasil, Stream_kesalahan = 셸입출력.kegagalan_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Status_VALUE = Stream_kesalahan < 0 ? 1 : 반환값;
                    if (Stream_kesalahan < 0) { PenafsirPerintah.galat(Stream_kesalahan); return; }
                    if (skrip_mengakhiri || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Berikutnya_posisi + 1;
                }
            }
            if (grup_mengakhiri < total_COUNT) 조건성립 = 종류[중첩깊이 * 128 + grup_mengakhiri];
            읽는자리 = grup_mengakhiri + 1;
        }
    }
    static void Jalankan_file() {
        if (PenafsirPerintah.token_COUNT != 2 || 깊이 >= 3) { PenafsirPerintah.hasil = 2; 단말.Tulis("사용법: sh berkas (berlapis_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = PenafsirPerintah.jalur(1); if (처리값 >= 0) 처리값 = BerkasMemori.Buka(0);
        if (처리값 < 0) { PenafsirPerintah.galat(처리값); return; }
        int entri_COUNT = 0, byte_data;
        while ((byte_data = BerkasMemori.Baca(처리값)) != 256 && byte_data >= 0 && entri_COUNT < 16384) skrip_VALUE[중첩깊이 * 16384 + entri_COUNT++] = byte_data;
        BerkasMemori.Tutup(처리값); Papan.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < entri_COUNT && !skrip_mengakhiri;) {
            int mengakhiri_posisi = 읽는자리; while (mengakhiri_posisi < entri_COUNT && skrip_VALUE[중첩깊이 * 16384 + mengakhiri_posisi] != 10) mengakhiri_posisi++;
            int 유효길이 = mengakhiri_posisi - 읽는자리; if (유효길이 > 0 && skrip_VALUE[중첩깊이 * 16384 + mengakhiri_posisi - 1] == 13) 유효길이--;
            Jalankan_perintah(skrip_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = mengakhiri_posisi + 1;
        }
        PenafsirPerintah.hasil = Status_VALUE; skrip_mengakhiri = false; 깊이 = 중첩깊이 - 1;
    }
}
