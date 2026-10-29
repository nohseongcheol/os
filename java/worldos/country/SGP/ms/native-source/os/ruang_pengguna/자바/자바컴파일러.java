// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java sumber_pepohon -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] SUMBER = new int[16384], 출력 = new int[16384], kod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_jawatan = new int[2048], token_kepanjangan = new int[2048];
    static int[] pemalar_VALUE = new int[4096], pemalar_Ofset = new int[512];
    static int[] 문자 = new int[512], nama_fail_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int sumber_saiz, token_COUNT, Kedudukan, kod_saiz, pemalar_saiz, pemalar_COUNT = 1, 출력크기, aksara_kepanjangan;
    static boolean RALAT;
    static int Kelas_token, Kelas_pemalar, 부모상수, kod_pemalar;
    static int[] kaedah_pemasukan_nama = new int[32], kaedah_kembalikan = new int[32], kaedah_argumen_COUNT = new int[32];
    static int[] kaedah_argumen_nama = new int[512], kaedah_argumen_TYPE = new int[512];
    static int[] kaedah_isi = new int[32], kaedah_tamat = new int[32], kaedah_kod = new int[32];
    static int[] kaedah_kepanjangan = new int[32], 함수지역 = new int[32], kaedah_nama_pemalar = new int[32], 함수서술 = new int[32];
    static int[] kaedah_capai = new int[32];
    static int kaedah_COUNT, 현재함수, setempat_COUNT, 깊이, 식깊이;
    static int[] setempat_nama = new int[128], setempat_TYPE = new int[128], 지역깊이 = new int[128];

    static void kegagalan_VALUE(String 이유) {
        if (!RALAT) {
            ruang_pengguna.Tulis("javac error: "); ruang_pengguna.Tulis(이유);
            ruang_pengguna.Tulis(" at line ");
            int baris = 1, 끝 = Kedudukan < token_COUNT ? token_jawatan[Kedudukan] : sumber_saiz;
            for (int 수 = 0; 수 < 끝; 수++) if (SUMBER[수] == 10) baris++;
            자바도구.수쓰기(baris); ruang_pengguna.tulis_aksara_VALUE(10);
        }
        RALAT = true;
    }
    static boolean aksara_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean digit_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= token_COUNT || 나 >= token_COUNT || token_kepanjangan[가] != token_kepanjangan[나]) return false;
        for (int 수 = 0; 수 < token_kepanjangan[가]; 수++) if (SUMBER[token_jawatan[가] + 수] != SUMBER[token_jawatan[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_kepanjangan[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (SUMBER[token_jawatan[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Kedudukan < token_COUNT ? 토큰종류[Kedudukan] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Kedudukan++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) kegagalan_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Kedudukan, Word_SMS)) return false; Kedudukan++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) kegagalan_VALUE(Word_SMS); }
    static int 식별자() {
        int ukuran = Kedudukan;
        if (종류() != 256) kegagalan_VALUE("identifier required"); else Kedudukan++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Jalan = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Jalan == token_kepanjangan[ukuran];
                for (int 칸 = Jalan; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != SUMBER[token_jawatan[ukuran] + 칸 - Jalan]) 같음 = false;
                if (같음) kegagalan_VALUE("reserved word cannot be an identifier");
                Jalan = 수 + 1;
            }
        }
        return ukuran;
    }
    static void potong_VALUE() {
        int 수 = 0;
        while (수 < sumber_saiz && !RALAT) {
            int VALUE = SUMBER[수], Jalan = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < sumber_saiz && SUMBER[수 + 1] == '/') {
                while (수 < sumber_saiz && SUMBER[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < sumber_saiz && SUMBER[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < sumber_saiz && !(SUMBER[수] == '*' && SUMBER[수 + 1] == '/')) 수++;
                if (수 + 1 >= sumber_saiz) { kegagalan_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (aksara_VALUE(VALUE)) { 종류 = 256; while (수 < sumber_saiz && 문자이름규칙.이어진글자(SUMBER[수])) 수++; }
            else if (digit_VALUE(VALUE)) { 종류 = 257; while (수 < sumber_saiz && digit_VALUE(SUMBER[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < sumber_saiz && SUMBER[수] != VALUE && SUMBER[수] != 10 && SUMBER[수] != 13) {
                    if (SUMBER[수] == '\\') 수++;
                    수++;
                }
                if (수 >= sumber_saiz || SUMBER[수] != VALUE) { kegagalan_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < sumber_saiz) {
                    int Seterusnya_item = SUMBER[수];
                    if (VALUE == '=' && Seterusnya_item == '=') 종류 = 300;
                    if (VALUE == '!' && Seterusnya_item == '=') 종류 = 301;
                    if (VALUE == '<' && Seterusnya_item == '=') 종류 = 302;
                    if (VALUE == '>' && Seterusnya_item == '=') 종류 = 303;
                    if (VALUE == '&' && Seterusnya_item == '&') 종류 = 304;
                    if (VALUE == '|' && Seterusnya_item == '|') 종류 = 305;
                    if (VALUE == '+' && Seterusnya_item == '+') 종류 = 306;
                    if (VALUE == '-' && Seterusnya_item == '-') 종류 = 307;
                    if (VALUE == '+' && Seterusnya_item == '=') 종류 = 308;
                    if (VALUE == '-' && Seterusnya_item == '=') 종류 = 309;
                    if (VALUE == '*' && Seterusnya_item == '=') 종류 = 310;
                    if (VALUE == '/' && Seterusnya_item == '=') 종류 = 311;
                    if (VALUE == '%' && Seterusnya_item == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { kegagalan_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_jawatan[token_COUNT] = Jalan; token_kepanjangan[token_COUNT++] = 수 - Jalan;
        }
    }
    static void tulis_pemalar_bait(int VALUE) {
        if (pemalar_saiz == pemalar_VALUE.length) { kegagalan_VALUE("constant pool too large"); return; }
        pemalar_VALUE[pemalar_saiz++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { tulis_pemalar_bait(VALUE >> 8); tulis_pemalar_bait(VALUE); }
    static int daftar_pemalar(int Jalan) {
        for (int 수 = 1; 수 < pemalar_COUNT; 수++) {
            int hadapan_VALUE = pemalar_Ofset[수], kepanjangan_VALUE = (수 + 1 < pemalar_COUNT ? pemalar_Ofset[수 + 1] : Jalan) - hadapan_VALUE;
            if (kepanjangan_VALUE != pemalar_saiz - Jalan) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < kepanjangan_VALUE; 칸++) if (pemalar_VALUE[hadapan_VALUE + 칸] != pemalar_VALUE[Jalan + 칸]) 같음 = false;
            if (같음) { pemalar_saiz = Jalan; return 수; }
        }
        if (pemalar_COUNT == pemalar_Ofset.length) { kegagalan_VALUE("too many constants"); return 0; }
        pemalar_Ofset[pemalar_COUNT] = Jalan;
        return pemalar_COUNT++;
    }
    static void Tambah_SMS(int VALUE) {
        if (aksara_kepanjangan == 문자.length) { kegagalan_VALUE("text too long"); return; }
        문자[aksara_kepanjangan++] = VALUE;
    }
    static void Tambah_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) Tambah_SMS(Word_SMS.charAt(수)); }
    static int aksara_pemalar() {
        int Jalan = pemalar_saiz; tulis_pemalar_bait(1); 상짧(0);
        for (int 수 = 0; 수 < aksara_kepanjangan; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) tulis_pemalar_bait(VALUE);
            else if (VALUE < 2048) { tulis_pemalar_bait(192 | VALUE >> 6); tulis_pemalar_bait(128 | VALUE & 63); }
            else { tulis_pemalar_bait(224 | VALUE >> 12); tulis_pemalar_bait(128 | VALUE >> 6 & 63); tulis_pemalar_bait(128 | VALUE & 63); }
        }
        if (RALAT) return 0;
        int kepanjangan_VALUE = pemalar_saiz - Jalan - 3;
        pemalar_VALUE[Jalan + 1] = kepanjangan_VALUE >> 8; pemalar_VALUE[Jalan + 2] = kepanjangan_VALUE & 255;
        return daftar_pemalar(Jalan);
    }
    static int Word_pemalar(String Word_SMS) { aksara_kepanjangan = 0; Tambah_Word(Word_SMS); return aksara_pemalar(); }
    static int token_pemalar(int token_VALUE) {
        aksara_kepanjangan = 0;
        for (int 수 = 0; 수 < token_kepanjangan[token_VALUE]; 수++) Tambah_SMS(SUMBER[token_jawatan[token_VALUE] + 수]);
        return aksara_pemalar();
    }
    static int Rujukan(int 종류, int 가, int 나) {
        int Jalan = pemalar_saiz; tulis_pemalar_bait(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return daftar_pemalar(Jalan);
    }
    static int rujukan_luaran(int 종류, String pemilik_VALUE, String Nama, String 서술) {
        int 주인 = Rujukan(7, Word_pemalar(pemilik_VALUE), 0);
        int nama_COUNT = Word_pemalar(Nama), format_COUNT = Word_pemalar(서술);
        return Rujukan(종류, 주인, Rujukan(12, nama_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kod_saiz == kod_VALUE.length) { kegagalan_VALUE("bytecode too large"); return; }
        kod_VALUE[kod_saiz++] = VALUE & 255;
    }
    static void Perintah(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Jalan = pemalar_saiz; tulis_pemalar_bait(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Perintah(19, daftar_pemalar(Jalan));
    }
    static int cabang(int Perintah) { int ukuran = kod_saiz; Perintah(Perintah, 0); return ukuran; }
    static void paut_VALUE(int cabang, int sasaran_objek) {
        if (RALAT) return;
        int 거리 = sasaran_objek - cabang;
        if (거리 < -32768 || 거리 > 32767 || cabang < 0 || cabang + 2 >= kod_saiz) { kegagalan_VALUE("invalid branch"); return; }
        kod_VALUE[cabang + 1] = 거리 >> 8 & 255; kod_VALUE[cabang + 2] = 거리 & 255;
    }
    static void Perbandingan_VALUE(int Perintah) {
        int TRUE_VALUE = cabang(Perintah); 내보내기(3); int 끝 = cabang(167);
        paut_VALUE(TRUE_VALUE, kod_saiz); 내보내기(4); paut_VALUE(끝, kod_saiz);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        kegagalan_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void tambah_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) Tambah_SMS('V');
        if (TYPE_VALUE == 1) Tambah_SMS('I');
        if (TYPE_VALUE == 2) Tambah_SMS('Z');
        if (TYPE_VALUE == 3) Tambah_Word("Ljava/lang/String;");
        if (TYPE_VALUE == 4) Tambah_Word("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) Tambah_SMS('C');
        if (TYPE_VALUE == 6) Tambah_Word("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) Tambah_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws pengisytiharan_4f4f026b. pengecualian Proses_VALUE_pemasukan 본문은 hos javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Melayu");
        if (한국어묶음) { 요구('.'); 말요구("Asli"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("pengecualian") || TAKE_Word("실행예외") || TAKE_Word("I_O_pengecualian") || TAKE_Word("tunggu_TIMEOUT_pengecualian") || TAKE_Word("e_mel_Carian_pengecualian") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("tak_sah_argumen_pengecualian") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("rujukan_nol_pengecualian") || TAKE_Word("산술예외") || TAKE_Word("status_pengecualian") || TAKE_Word("TYPE_siar_pengecualian") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_stor_kegagalan") || TAKE_Word("urutan_status_pengecualian") || TAKE_Word("대기중단예외")) return;
        kegagalan_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Kedudukan, "Melayu")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) kegagalan_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Kelas_token = 식별자();
        Kelas_pemalar = Rujukan(7, token_pemalar(Kelas_token), 0);
        부모상수 = Rujukan(7, Word_pemalar("java/lang/Object"), 0); kod_pemalar = Word_pemalar("Code"); 요구('{');
        while (!RALAT && 종류() != '}') {
            if (kaedah_COUNT == 32) { kegagalan_VALUE("too many methods"); break; }
            int capai_pemasukan = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int fungsi_VALUE = kaedah_COUNT++;
            kaedah_capai[fungsi_VALUE] = capai_pemasukan | 8;
            kaedah_kembalikan[fungsi_VALUE] = format_VALUE(); kaedah_pemasukan_nama[fungsi_VALUE] = 식별자(); 요구('(');
            for (int hadapan_VALUE = 0; hadapan_VALUE < fungsi_VALUE; hadapan_VALUE++) if (이름같음(kaedah_pemasukan_nama[hadapan_VALUE], kaedah_pemasukan_nama[fungsi_VALUE])) kegagalan_VALUE("duplicate method (overloading unsupported)");
            while (!RALAT && 종류() != ')') {
                int 수 = kaedah_argumen_COUNT[fungsi_VALUE];
                if (수 == 16) { kegagalan_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) kegagalan_VALUE("void parameter");
                kaedah_argumen_TYPE[fungsi_VALUE * 16 + 수] = TYPE_VALUE; kaedah_argumen_nama[fungsi_VALUE * 16 + 수] = 식별자();
                kaedah_argumen_COUNT[fungsi_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!RALAT && 받기(','));
            }
            kaedah_isi[fungsi_VALUE] = Kedudukan; 요구('{');
            int penyarangan_VALUE = 1;
            while (Kedudukan < token_COUNT && penyarangan_VALUE > 0) {
                if (종류() == '{') penyarangan_VALUE++;
                if (종류() == '}') penyarangan_VALUE--;
                Kedudukan++;
            }
            if (penyarangan_VALUE != 0) kegagalan_VALUE("unclosed method body");
            kaedah_tamat[fungsi_VALUE] = Kedudukan;
            kaedah_nama_pemalar[fungsi_VALUE] = token_pemalar(kaedah_pemasukan_nama[fungsi_VALUE]);
            aksara_kepanjangan = 0; Tambah_SMS('(');
            for (int 수 = 0; 수 < kaedah_argumen_COUNT[fungsi_VALUE]; 수++) tambah_format(kaedah_argumen_TYPE[fungsi_VALUE * 16 + 수]);
            Tambah_SMS(')'); tambah_format(kaedah_kembalikan[fungsi_VALUE]); 함수서술[fungsi_VALUE] = aksara_pemalar();
        }
        요구('}'); if (Kedudukan != token_COUNT) kegagalan_VALUE("extra input after class");
    }
    static int Cari_setempat(int Nama) {
        for (int 수 = setempat_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(setempat_nama[수], Nama)) return 수;
        kegagalan_VALUE("unknown variable"); return 0;
    }
    static int tambah_setempat(int Nama, int TYPE_VALUE) {
        for (int 수 = 0; 수 < setempat_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(setempat_nama[수], Nama)) kegagalan_VALUE("duplicate local variable");
        if (setempat_COUNT == 128) { kegagalan_VALUE("too many locals"); return 0; }
        setempat_nama[setempat_COUNT] = Nama; setempat_TYPE[setempat_COUNT] = TYPE_VALUE; 지역깊이[setempat_COUNT] = 깊이;
        return setempat_COUNT++;
    }
    static boolean integer_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(setempat_TYPE[수] <= 2 || setempat_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void tulis_setempat(int 수) { 내보내기(setempat_TYPE[수] <= 2 || setempat_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void tentu_sahkan_TYPE(int sebenar_data, int 기대) { if (sebenar_data != 기대 && !(sebenar_data == 5 && 기대 == 1)) kegagalan_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        aksara_kepanjangan = 0; int Jalan = token_jawatan[token_VALUE] + 1, 끝 = token_jawatan[token_VALUE] + token_kepanjangan[token_VALUE] - 1;
        while (Jalan < 끝 && !RALAT) {
            int VALUE = SUMBER[Jalan++];
            if (VALUE == '\\') {
                if (Jalan == 끝) { kegagalan_VALUE("invalid escape"); break; }
                VALUE = SUMBER[Jalan++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') kegagalan_VALUE("unsupported escape");
            }
            Tambah_SMS(VALUE);
        }
    }
    static int hurai_integer(int token_VALUE, boolean 음수) {
        if (token_kepanjangan[token_VALUE] > 1 && SUMBER[token_jawatan[token_VALUE]] == '0') kegagalan_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_kepanjangan[token_VALUE]; 수++) {
            int digit_item = SUMBER[token_jawatan[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && digit_item > (음수 ? 8 : 7)) kegagalan_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - digit_item;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { kegagalan_VALUE("only file streams supported by new in source"); return 0; }
            String pemilik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Perintah(187, Rujukan(7, Word_pemalar(pemilik_VALUE), 0)); 내보내기(89);
            요구('('); tentu_sahkan_TYPE(ungkapan_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) kegagalan_VALUE("input stream constructor arguments"); tentu_sahkan_TYPE(ungkapan_VALUE(), 2); 이어 = true; }
            요구(')');
            Perintah(183, rujukan_luaran(10, pemilik_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = ungkapan_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(hurai_integer(Kedudukan++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Kedudukan++); Perintah(19, Rujukan(8, aksara_pemalar(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Kedudukan++); if (aksara_kepanjangan != 1) kegagalan_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Melayu")) {
            요구('.'); 말요구("Asli"); 요구('.');
            String pemilik_VALUE = "", kaedah_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, ukuran = 0;
            if (TAKE_Word("출력")) {
                pemilik_VALUE = "Melayu/Asli/출력"; 요구('.');
                if (TAKE_Word("tulis_baris")) { kaedah_VALUE = "tulis_baris"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Tulis")) { kaedah_VALUE = "Tulis"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { kaedah_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else kegagalan_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                pemilik_VALUE = "Melayu/Asli/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("kepanjangan_VALUE")) { kaedah_VALUE = "kepanjangan_VALUE"; 서술 = "(Ljava/lang/String;)I"; ukuran = 1; }
                else if (TAKE_Word("titik_kod_COUNT")) { kaedah_VALUE = "titik_kod_COUNT"; 서술 = "(Ljava/lang/String;)I"; ukuran = 1; }
                else if (TAKE_Word("hurai_integer")) { kaedah_VALUE = "hurai_integer"; 서술 = "(Ljava/lang/String;)I"; ukuran = 1; }
                else if (TAKE_Word("tulis_integer_VALUE")) { kaedah_VALUE = "tulis_integer_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; ukuran = 3; }
                else if (TAKE_Word("같음")) { kaedah_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; ukuran = 2; }
                else if (TAKE_Word("tampal_SMS")) { kaedah_VALUE = "tampal_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; ukuran = 3; }
                else if (TAKE_Word("potong_VALUE")) { kaedah_VALUE = "potong_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; ukuran = 3; }
                else kegagalan_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fail")) {
                pemilik_VALUE = "Melayu/Asli/Fail"; 요구('.'); 가 = 3;
                if (TAKE_Word("Baca")) { kaedah_VALUE = "Baca"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; ukuran = 3; }
                else if (TAKE_Word("Tulis")) { kaedah_VALUE = "Tulis"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else kegagalan_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                pemilik_VALUE = "Melayu/Asli/화면"; 요구('.');
                if (TAKE_Word("너비")) { kaedah_VALUE = "너비"; 서술 = "()I"; ukuran = 1; }
                else if (TAKE_Word("높이")) { kaedah_VALUE = "높이"; 서술 = "()I"; ukuran = 1; }
                else if (TAKE_Word("segi_empat_tepat")) { kaedah_VALUE = "segi_empat_tepat"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("padam_pemasukan")) { kaedah_VALUE = "padam_pemasukan"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { kaedah_VALUE = "기다리기"; 서술 = "()V"; }
                else kegagalan_VALUE("unknown Korean framebuffer method");
            } else kegagalan_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) tentu_sahkan_TYPE(ungkapan_VALUE(), 가);
            if (나 != 0) { 요구(','); tentu_sahkan_TYPE(ungkapan_VALUE(), 나); }
            if (다 != 0) { 요구(','); tentu_sahkan_TYPE(ungkapan_VALUE(), 다); }
            if (라 != 0) { 요구(','); tentu_sahkan_TYPE(ungkapan_VALUE(), 라); }
            if (마 != 0) { 요구(','); tentu_sahkan_TYPE(ungkapan_VALUE(), 마); }
            요구(')'); Perintah(184, rujukan_luaran(10, pemilik_VALUE, kaedah_VALUE, 서술)); return ukuran;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); tentu_sahkan_TYPE(ungkapan_VALUE(), 3); 요구(')');
            Perintah(184, rujukan_luaran(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nama = 식별자();
        if (받기('(')) {
            int fungsi_VALUE = -1;
            for (int 수 = 0; 수 < kaedah_COUNT; 수++) if (이름같음(Nama, kaedah_pemasukan_nama[수])) fungsi_VALUE = 수;
            if (fungsi_VALUE < 0) { kegagalan_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!RALAT && 종류() != ')') {
                if (수 >= kaedah_argumen_COUNT[fungsi_VALUE]) { kegagalan_VALUE("too many arguments"); break; }
                tentu_sahkan_TYPE(ungkapan_VALUE(), kaedah_argumen_TYPE[fungsi_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != kaedah_argumen_COUNT[fungsi_VALUE]) kegagalan_VALUE("argument count mismatch");
            Perintah(184, Rujukan(10, Kelas_pemalar, Rujukan(12, kaedah_nama_pemalar[fungsi_VALUE], 함수서술[fungsi_VALUE])));
            return kaedah_kembalikan[fungsi_VALUE];
        }
        int setempat_Skop = Cari_setempat(Nama), TYPE_VALUE = setempat_TYPE[setempat_Skop]; 지역읽기(setempat_Skop);
        while (!RALAT) {
            if (받기('[')) { tentu_sahkan_TYPE(TYPE_VALUE, 4); tentu_sahkan_TYPE(ungkapan_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String pemilik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Perintah(182, rujukan_luaran(10, pemilik_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Perintah(182, rujukan_luaran(10, pemilik_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); tentu_sahkan_TYPE(ungkapan_VALUE(), 1); 요구(')'); Perintah(182, rujukan_luaran(10, pemilik_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { kegagalan_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { tentu_sahkan_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Perintah(182, rujukan_luaran(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { kegagalan_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { tentu_sahkan_TYPE(단항(), 2); Perbandingan_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(hurai_integer(Kedudukan++, true));
            else { tentu_sahkan_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { tentu_sahkan_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!RALAT && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int pengekodan_VALUE = 종류(); Kedudukan++; tentu_sahkan_TYPE(TYPE_VALUE, 1); tentu_sahkan_TYPE(단항(), 1);
            내보내기(pengekodan_VALUE == '*' ? 104 : pengekodan_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!RALAT && (종류() == '+' || 종류() == '-')) {
            int pengekodan_VALUE = 종류(); Kedudukan++; int 경계 = kod_saiz, BACK_jenis_nilai = 곱식();
            if (pengekodan_VALUE == '+' && (TYPE_VALUE == 3 || BACK_jenis_nilai == 3)) { 결합(경계, TYPE_VALUE, BACK_jenis_nilai); TYPE_VALUE = 3; }
            else { tentu_sahkan_TYPE(TYPE_VALUE, 1); tentu_sahkan_TYPE(BACK_jenis_nilai, 1); 내보내기(pengekodan_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) kegagalan_VALUE("unsupported concatenation type");
        return rujukan_luaran(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int hadapan_jenis_nilai, int BACK_jenis_nilai) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kod_VALUE 앞에 jana 코드를 삽입한다.
        // RIGHT ungkapan_VALUE 내부의 rakan_VALUE cabang 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kod_saiz;
        Perintah(187, Rujukan(7, Word_pemalar("java/lang/StringBuilder"), 0)); 내보내기(89);
        Perintah(183, rujukan_luaran(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Perintah(182, 붙임참조(hadapan_jenis_nilai));
        if (RALAT) return;
        int kepanjangan_VALUE = kod_saiz - 끝;
        for (int 수 = 0; 수 < kepanjangan_VALUE; 수++) 삽입코드[수] = kod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kod_VALUE[수 + kepanjangan_VALUE] = kod_VALUE[수];
        for (int 수 = 0; 수 < kepanjangan_VALUE; 수++) kod_VALUE[경계 + 수] = 삽입코드[수];
        Perintah(182, 붙임참조(BACK_jenis_nilai)); Perintah(182, rujukan_luaran(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Perbandingan_ungkapan() {
        int TYPE_VALUE = 합식();
        while (!RALAT && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int pengekodan_VALUE = 종류(); Kedudukan++; tentu_sahkan_TYPE(TYPE_VALUE, 1); tentu_sahkan_TYPE(합식(), 1);
            Perbandingan_VALUE(pengekodan_VALUE == '<' ? 161 : pengekodan_VALUE == '>' ? 163 : pengekodan_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Perbandingan_ungkapan();
        while (!RALAT && (종류() == 300 || 종류() == 301)) {
            int pengekodan_VALUE = 종류(); Kedudukan++; int BACK_jenis_nilai = Perbandingan_ungkapan();
            if (TYPE_VALUE == 0 || BACK_jenis_nilai == 0) kegagalan_VALUE("void expression");
            if (!(integer_TYPE(TYPE_VALUE) && integer_TYPE(BACK_jenis_nilai))) tentu_sahkan_TYPE(BACK_jenis_nilai, TYPE_VALUE);
            Perbandingan_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (pengekodan_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!RALAT && 받기(304)) {
            tentu_sahkan_TYPE(TYPE_VALUE, 2); int 가 = cabang(153); tentu_sahkan_TYPE(동등식(), 2); int 나 = cabang(153);
            내보내기(4); int 끝 = cabang(167); paut_VALUE(가, kod_saiz); paut_VALUE(나, kod_saiz); 내보내기(3); paut_VALUE(끝, kod_saiz); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int ungkapan_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!RALAT && 받기(305)) {
            tentu_sahkan_TYPE(TYPE_VALUE, 2); int 가 = cabang(154); tentu_sahkan_TYPE(논리곱(), 2); int 나 = cabang(154);
            내보내기(3); int 끝 = cabang(167); paut_VALUE(가, kod_saiz); paut_VALUE(나, kod_saiz); 내보내기(4); paut_VALUE(끝, kod_saiz); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void tugasan_VALUE(boolean Izin_pengisytiharan) {
        if (Word_VALUE(Kedudukan, "int") || Word_VALUE(Kedudukan, "boolean") || Word_VALUE(Kedudukan, "String") || Word_VALUE(Kedudukan, "char")
            || Word_VALUE(Kedudukan, "FileInputStream") || Word_VALUE(Kedudukan, "FileOutputStream")) {
            if (!Izin_pengisytiharan) kegagalan_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), Nama = 식별자(); 요구('='); tentu_sahkan_TYPE(ungkapan_VALUE(), TYPE_VALUE);
            tulis_setempat(tambah_setempat(Nama, TYPE_VALUE)); return;
        }
        int Nama = 식별자(), setempat_Skop = Cari_setempat(Nama);
        if (받기('=')) { tentu_sahkan_TYPE(ungkapan_VALUE(), setempat_TYPE[setempat_Skop]); tulis_setempat(setempat_Skop); }
        else if (종류() >= 308 && 종류() <= 312) {
            int pengekodan_VALUE = 종류(); Kedudukan++; 지역읽기(setempat_Skop); int 경계 = kod_saiz, BACK_jenis_nilai = ungkapan_VALUE();
            if (pengekodan_VALUE == 308 && setempat_TYPE[setempat_Skop] == 3) 결합(경계, 3, BACK_jenis_nilai);
            else {
                tentu_sahkan_TYPE(setempat_TYPE[setempat_Skop], 1); tentu_sahkan_TYPE(BACK_jenis_nilai, 1);
                내보내기(pengekodan_VALUE == 308 ? 96 : pengekodan_VALUE == 309 ? 100 : pengekodan_VALUE == 310 ? 104 : pengekodan_VALUE == 311 ? 108 : 112);
                if (setempat_TYPE[setempat_Skop] == 5) 내보내기(146);
            }
            tulis_setempat(setempat_Skop);
        }
        else if (종류() == 306 || 종류() == 307) {
            tentu_sahkan_TYPE(setempat_TYPE[setempat_Skop], 1); 내보내기(132); 내보내기(setempat_Skop); 내보내기(종류() == 306 ? 1 : 255); Kedudukan++;
            if (setempat_TYPE[setempat_Skop] == 5) { 지역읽기(setempat_Skop); 내보내기(146); tulis_setempat(setempat_Skop); }
        } else kegagalan_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Perintah(178, rujukan_luaran(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int TYPE_VALUE = 빈인수 ? 0 : ungkapan_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !빈인수)) kegagalan_VALUE("unsupported print argument");
        Perintah(182, rujukan_luaran(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean kenyataan_VALUE() {
        if (RALAT) return false;
        if (깊이 > 32) { kegagalan_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean kembalikan_ukuran = false;
            while (!RALAT && 종류() != '}') { if (kembalikan_ukuran) kegagalan_VALUE("unreachable statement"); kembalikan_ukuran = kenyataan_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < setempat_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return kembalikan_ukuran;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : ungkapan_VALUE(); tentu_sahkan_TYPE(TYPE_VALUE, kaedah_kembalikan[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); tentu_sahkan_TYPE(ungkapan_VALUE(), 2); 요구(')'); int FALSE_VALUE = cabang(153);
            깊이++; boolean 가 = kawalan_kenyataan(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = cabang(167); paut_VALUE(FALSE_VALUE, kod_saiz); 깊이++; boolean 나 = kawalan_kenyataan(); 깊이--; paut_VALUE(끝, kod_saiz); return 가 && 나; }
            paut_VALUE(FALSE_VALUE, kod_saiz); return false;
        }
        if (TAKE_Word("while")) {
            int Jalan = kod_saiz; 요구('('); tentu_sahkan_TYPE(ungkapan_VALUE(), 2); 요구(')'); int 끝 = cabang(153);
            깊이++; kawalan_kenyataan(); 깊이--; paut_VALUE(cabang(167), Jalan); paut_VALUE(끝, kod_saiz); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') tugasan_VALUE(true); 요구(';');
            int syarat = kod_saiz; if (종류() == ';') 내보내기(4); else tentu_sahkan_TYPE(ungkapan_VALUE(), 2); 요구(';');
            int 끝 = cabang(153), teks_jasad = cabang(167), segar_semula = kod_saiz;
            if (종류() != ')') tugasan_VALUE(false); 요구(')'); paut_VALUE(cabang(167), syarat); paut_VALUE(teks_jasad, kod_saiz);
            kawalan_kenyataan(); paut_VALUE(cabang(167), segar_semula); paut_VALUE(끝, kod_saiz);
            for (int 수 = 0; 수 < setempat_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Kedudukan, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Kedudukan + 1 < token_COUNT && (토큰종류[Kedudukan + 1] == '(' || 토큰종류[Kedudukan + 1] == '.')) {
            int TYPE_VALUE = ungkapan_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        tugasan_VALUE(true); 요구(';'); return false;
    }
    static boolean kawalan_kenyataan() {
        if (Word_VALUE(Kedudukan, "int") || Word_VALUE(Kedudukan, "boolean") || Word_VALUE(Kedudukan, "char") || Word_VALUE(Kedudukan, "String")
            || Word_VALUE(Kedudukan, "FileInputStream") || Word_VALUE(Kedudukan, "FileOutputStream")) kegagalan_VALUE("local declaration requires braces");
        return kenyataan_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) kegagalan_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void tulis_Kelas() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(pemalar_COUNT);
        for (int 수 = 0; 수 < pemalar_saiz; 수++) 출바(pemalar_VALUE[수]);
        출짧(0x21); 출짧(Kelas_pemalar); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(kaedah_COUNT);
        for (int 수 = 0; 수 < kaedah_COUNT; 수++) {
            출짧(kaedah_capai[수]); 출짧(kaedah_nama_pemalar[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kod_pemalar);
            출정(12 + kaedah_kepanjangan[수]); 출짧(128); 출짧(함수지역[수]); 출정(kaedah_kepanjangan[수]);
            for (int 칸 = 0; 칸 < kaedah_kepanjangan[수]; 칸++) 출바(kod_VALUE[kaedah_kod[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Jalan() {
        if (ruang_pengguna.인수개수() == 1 && 자바도구.같음(ruang_pengguna.인수(0), "-version")) {
            ruang_pengguna.Tulis("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (ruang_pengguna.인수개수() != 1) { ruang_pengguna.Tulis("Usage: javac FILE.java\n"); return 2; }
        int nama_saiz = 자바도구.Nama(nama_fail_SMS, ruang_pengguna.인수(0));
        if (nama_saiz < 6 || nama_saiz > 62 || nama_fail_SMS[nama_saiz - 5] != '.' || nama_fail_SMS[nama_saiz - 4] != 'j'
            || nama_fail_SMS[nama_saiz - 3] != 'a' || nama_fail_SMS[nama_saiz - 2] != 'v' || nama_fail_SMS[nama_saiz - 1] != 'a') {
            ruang_pengguna.Tulis("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        sumber_saiz = ruang_pengguna.파일읽기(nama_fail_SMS, SUMBER);
        if (sumber_saiz < 0) { ruang_pengguna.Tulis("javac: cannot read source: "); 자바도구.수쓰기(sumber_saiz); ruang_pengguna.tulis_aksara_VALUE(10); return 1; }
        sumber_saiz = 자바도구.원문해독(SUMBER, sumber_saiz);
        if (sumber_saiz < 0) { ruang_pengguna.Tulis("javac error: invalid UTF-8 source\n"); return 1; }
        potong_VALUE(); if (!RALAT) 선언읽기();
        if (!RALAT) {
            if (token_kepanjangan[Kelas_token] != nama_saiz - 5) kegagalan_VALUE("class name must match file name");
            for (int 수 = 0; 수 < nama_saiz - 5; 수++) if (SUMBER[token_jawatan[Kelas_token] + 수] != nama_fail_SMS[수]) kegagalan_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < kaedah_COUNT && !RALAT; 현재함수++) {
            Kedudukan = kaedah_isi[현재함수]; kaedah_kod[현재함수] = kod_saiz; setempat_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < kaedah_argumen_COUNT[현재함수]; 수++) tambah_setempat(kaedah_argumen_nama[현재함수 * 16 + 수], kaedah_argumen_TYPE[현재함수 * 16 + 수]);
            boolean kembalikan_ukuran = kenyataan_VALUE();
            if (!kembalikan_ukuran && kaedah_kembalikan[현재함수] != 0) kegagalan_VALUE("missing return");
            // cabang 뒤의 합류 지점은 반드시 sebenar_data 명령이어야 한다 (버전 49 검증기).
            if (kaedah_kembalikan[현재함수] == 0) 내보내기(177);
            else { boolean integer = kaedah_kembalikan[현재함수] <= 2 || kaedah_kembalikan[현재함수] == 5; 내보내기(integer ? 3 : 1); 내보내기(integer ? 172 : 176); }
            if (Kedudukan != kaedah_tamat[현재함수]) kegagalan_VALUE("invalid method body");
            함수지역[현재함수] = setempat_COUNT; kaedah_kepanjangan[현재함수] = kod_saiz - kaedah_kod[현재함수];
        }
        if (RALAT) return 1;
        tulis_Kelas(); if (RALAT) return 1;
        nama_fail_SMS[nama_saiz - 4] = 'c'; nama_fail_SMS[nama_saiz - 3] = 'l'; nama_fail_SMS[nama_saiz - 2] = 'a';
        nama_fail_SMS[nama_saiz - 1] = 's'; nama_fail_SMS[nama_saiz] = 's'; nama_fail_SMS[nama_saiz + 1] = 0;
        int ukuran = ruang_pengguna.tulis_fail(nama_fail_SMS, 출력, 출력크기);
        if (ukuran < 0) { ruang_pengguna.Tulis("javac: cannot save class: "); 자바도구.수쓰기(ukuran); ruang_pengguna.tulis_aksara_VALUE(10); return 1; }
        ruang_pengguna.Tulis("Compiled: "); for (int 수 = 0; nama_fail_SMS[수] != 0; 수++) ruang_pengguna.tulis_aksara_VALUE(nama_fail_SMS[수]);
        ruang_pengguna.Tulis(" (JVM class version 49)\n"); return 0;
    }
}
