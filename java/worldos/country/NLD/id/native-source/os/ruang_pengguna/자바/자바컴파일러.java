// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java sumber_pohon -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] kodeSumber = new int[16384], keluaranTeks = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_posisi = new int[2048], token_panjang = new int[2048];
    static int[] konstanta_VALUE = new int[4096], konstanta_OFFSET = new int[512];
    static int[] 문자 = new int[512], nama_file_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int sumber_ukuran, token_COUNT, posisi, CODE_ukuran, konstanta_ukuran, konstanta_COUNT = 1, 출력크기, karakter_panjang;
    static boolean galat;
    static int Kelas_token, Kelas_konstanta, induk_konstanta, CODE_konstanta;
    static int[] metode_entri_nama = new int[32], metode_kembalikan = new int[32], metode_argumen_COUNT = new int[32];
    static int[] metode_argumen_nama = new int[512], metode_argumen_TYPE = new int[512];
    static int[] metode_isi = new int[32], metode_mengakhiri = new int[32], metode_CODE = new int[32];
    static int[] metode_panjang = new int[32], 함수지역 = new int[32], metode_nama_konstanta = new int[32], 함수서술 = new int[32];
    static int[] metode_akses = new int[32];
    static int metode_COUNT, saat_ini_metode, lokal_COUNT, 깊이, 식깊이;
    static int[] lokal_nama = new int[128], lokal_TYPE = new int[128], 지역깊이 = new int[128];

    static void kegagalan_VALUE(String 이유) {
        if (!galat) {
            ruang_pengguna.Tulis("javac error: "); ruang_pengguna.Tulis(이유);
            ruang_pengguna.Tulis(" at line ");
            int baris_masukan = 1, 끝 = posisi < token_COUNT ? token_posisi[posisi] : sumber_ukuran;
            for (int 수 = 0; 수 < 끝; 수++) if (kodeSumber[수] == 10) baris_masukan++;
            자바도구.수쓰기(baris_masukan); ruang_pengguna.tulis_karakter_VALUE(10);
        }
        galat = true;
    }
    static boolean karakter_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean angka_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= token_COUNT || SECOND_operand >= token_COUNT || token_panjang[가] != token_panjang[SECOND_operand]) return false;
        for (int 수 = 0; 수 < token_panjang[가]; 수++) if (kodeSumber[token_posisi[가] + 수] != kodeSumber[token_posisi[SECOND_operand] + 수]) return false;
        return true;
    }
    static boolean Kata_VALUE(int token_VALUE, String Kata_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_panjang[token_VALUE] != Kata_SMS.length()) return false;
        for (int 수 = 0; 수 < Kata_SMS.length(); 수++) if (kodeSumber[token_posisi[token_VALUE] + 수] != Kata_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return posisi < token_COUNT ? 토큰종류[posisi] : 0; }
    static boolean terima(int VALUE) { if (종류() != VALUE) return false; posisi++; return true; }
    static void persyaratan_VALUE(int VALUE) { if (!terima(VALUE)) kegagalan_VALUE("unexpected token"); }
    static boolean TAKE_Kata(String Kata_SMS) { if (!Kata_VALUE(posisi, Kata_SMS)) return false; posisi++; return true; }
    static void 말요구(String Kata_SMS) { if (!TAKE_Kata(Kata_SMS)) kegagalan_VALUE(Kata_SMS); }
    static int pengidentifikasi_VALUE() {
        int hasil = posisi;
        if (종류() != 256) kegagalan_VALUE("identifier required"); else posisi++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int jalankan = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - jalankan == token_panjang[hasil];
                for (int slot_entri = jalankan; 같음 && slot_entri < 수; slot_entri++) if (예약어.charAt(slot_entri) != kodeSumber[token_posisi[hasil] + slot_entri - jalankan]) 같음 = false;
                if (같음) kegagalan_VALUE("reserved word cannot be an identifier");
                jalankan = 수 + 1;
            }
        }
        return hasil;
    }
    static void potong_VALUE() {
        int 수 = 0;
        while (수 < sumber_ukuran && !galat) {
            int VALUE = kodeSumber[수], jalankan = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < sumber_ukuran && kodeSumber[수 + 1] == '/') {
                while (수 < sumber_ukuran && kodeSumber[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < sumber_ukuran && kodeSumber[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < sumber_ukuran && !(kodeSumber[수] == '*' && kodeSumber[수 + 1] == '/')) 수++;
                if (수 + 1 >= sumber_ukuran) { kegagalan_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (karakter_VALUE(VALUE)) { 종류 = 256; while (수 < sumber_ukuran && 문자이름규칙.이어진글자(kodeSumber[수])) 수++; }
            else if (angka_VALUE(VALUE)) { 종류 = 257; while (수 < sumber_ukuran && angka_VALUE(kodeSumber[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < sumber_ukuran && kodeSumber[수] != VALUE && kodeSumber[수] != 10 && kodeSumber[수] != 13) {
                    if (kodeSumber[수] == '\\') 수++;
                    수++;
                }
                if (수 >= sumber_ukuran || kodeSumber[수] != VALUE) { kegagalan_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < sumber_ukuran) {
                    int Berikutnya_item = kodeSumber[수];
                    if (VALUE == '=' && Berikutnya_item == '=') 종류 = 300;
                    if (VALUE == '!' && Berikutnya_item == '=') 종류 = 301;
                    if (VALUE == '<' && Berikutnya_item == '=') 종류 = 302;
                    if (VALUE == '>' && Berikutnya_item == '=') 종류 = 303;
                    if (VALUE == '&' && Berikutnya_item == '&') 종류 = 304;
                    if (VALUE == '|' && Berikutnya_item == '|') 종류 = 305;
                    if (VALUE == '+' && Berikutnya_item == '+') 종류 = 306;
                    if (VALUE == '-' && Berikutnya_item == '-') 종류 = 307;
                    if (VALUE == '+' && Berikutnya_item == '=') 종류 = 308;
                    if (VALUE == '-' && Berikutnya_item == '=') 종류 = 309;
                    if (VALUE == '*' && Berikutnya_item == '=') 종류 = 310;
                    if (VALUE == '/' && Berikutnya_item == '=') 종류 = 311;
                    if (VALUE == '%' && Berikutnya_item == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { kegagalan_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_posisi[token_COUNT] = jalankan; token_panjang[token_COUNT++] = 수 - jalankan;
        }
    }
    static void tulis_konstanta_byte(int VALUE) {
        if (konstanta_ukuran == konstanta_VALUE.length) { kegagalan_VALUE("constant pool too large"); return; }
        konstanta_VALUE[konstanta_ukuran++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { tulis_konstanta_byte(VALUE >> 8); tulis_konstanta_byte(VALUE); }
    static int daftar_konstanta(int jalankan) {
        for (int 수 = 1; 수 < konstanta_COUNT; 수++) {
            int depan_VALUE = konstanta_OFFSET[수], panjang_VALUE = (수 + 1 < konstanta_COUNT ? konstanta_OFFSET[수 + 1] : jalankan) - depan_VALUE;
            if (panjang_VALUE != konstanta_ukuran - jalankan) continue;
            boolean 같음 = true;
            for (int slot_entri = 0; slot_entri < panjang_VALUE; slot_entri++) if (konstanta_VALUE[depan_VALUE + slot_entri] != konstanta_VALUE[jalankan + slot_entri]) 같음 = false;
            if (같음) { konstanta_ukuran = jalankan; return 수; }
        }
        if (konstanta_COUNT == konstanta_OFFSET.length) { kegagalan_VALUE("too many constants"); return 0; }
        konstanta_OFFSET[konstanta_COUNT] = jalankan;
        return konstanta_COUNT++;
    }
    static void tambah_SMS(int VALUE) {
        if (karakter_panjang == 문자.length) { kegagalan_VALUE("text too long"); return; }
        문자[karakter_panjang++] = VALUE;
    }
    static void tambah_Kata(String Kata_SMS) { for (int 수 = 0; 수 < Kata_SMS.length(); 수++) tambah_SMS(Kata_SMS.charAt(수)); }
    static int karakter_konstanta() {
        int jalankan = konstanta_ukuran; tulis_konstanta_byte(1); 상짧(0);
        for (int 수 = 0; 수 < karakter_panjang; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) tulis_konstanta_byte(VALUE);
            else if (VALUE < 2048) { tulis_konstanta_byte(192 | VALUE >> 6); tulis_konstanta_byte(128 | VALUE & 63); }
            else { tulis_konstanta_byte(224 | VALUE >> 12); tulis_konstanta_byte(128 | VALUE >> 6 & 63); tulis_konstanta_byte(128 | VALUE & 63); }
        }
        if (galat) return 0;
        int panjang_VALUE = konstanta_ukuran - jalankan - 3;
        konstanta_VALUE[jalankan + 1] = panjang_VALUE >> 8; konstanta_VALUE[jalankan + 2] = panjang_VALUE & 255;
        return daftar_konstanta(jalankan);
    }
    static int Kata_konstanta(String Kata_SMS) { karakter_panjang = 0; tambah_Kata(Kata_SMS); return karakter_konstanta(); }
    static int token_konstanta(int token_VALUE) {
        karakter_panjang = 0;
        for (int 수 = 0; 수 < token_panjang[token_VALUE]; 수++) tambah_SMS(kodeSumber[token_posisi[token_VALUE] + 수]);
        return karakter_konstanta();
    }
    static int Referensi(int 종류, int 가, int SECOND_operand) {
        int jalankan = konstanta_ukuran; tulis_konstanta_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return daftar_konstanta(jalankan);
    }
    static int referensi_eksternal(int 종류, String pemilik_VALUE, String Nama_2, String 서술) {
        int pemilik_pengidentifikasi = Referensi(7, Kata_konstanta(pemilik_VALUE), 0);
        int nama_COUNT = Kata_konstanta(Nama_2), format_COUNT = Kata_konstanta(서술);
        return Referensi(종류, pemilik_pengidentifikasi, Referensi(12, nama_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_ukuran == CODE_VALUE.length) { kegagalan_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_ukuran++] = VALUE & 255;
    }
    static void perintah(int VALUE, int argumen) { 내보내기(VALUE); 내보내기(argumen >> 8); 내보내기(argumen); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int jalankan = konstanta_ukuran; tulis_konstanta_byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        perintah(19, daftar_konstanta(jalankan));
    }
    static int cabang(int perintah) { int hasil = CODE_ukuran; perintah(perintah, 0); return hasil; }
    static void link_VALUE(int cabang, int target_objek) {
        if (galat) return;
        int 거리 = target_objek - cabang;
        if (거리 < -32768 || 거리 > 32767 || cabang < 0 || cabang + 2 >= CODE_ukuran) { kegagalan_VALUE("invalid branch"); return; }
        CODE_VALUE[cabang + 1] = 거리 >> 8 & 255; CODE_VALUE[cabang + 2] = 거리 & 255;
    }
    static void Perbandingan_VALUE(int perintah) {
        int TRUE_VALUE = cabang(perintah); 내보내기(3); int 끝 = cabang(167);
        link_VALUE(TRUE_VALUE, CODE_ukuran); 내보내기(4); link_VALUE(끝, CODE_ukuran);
    }
    static int format_VALUE() {
        if (TAKE_Kata("void")) return 0;
        if (TAKE_Kata("int")) return 1;
        if (TAKE_Kata("boolean")) return 2;
        if (TAKE_Kata("char")) return 5;
        if (TAKE_Kata("FileInputStream")) return 6;
        if (TAKE_Kata("FileOutputStream")) return 7;
        if (TAKE_Kata("String")) { if (terima('[')) { persyaratan_VALUE(']'); return 4; } return 3; }
        kegagalan_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void tambah_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) tambah_SMS('V');
        if (TYPE_VALUE == 1) tambah_SMS('I');
        if (TYPE_VALUE == 2) tambah_SMS('Z');
        if (TYPE_VALUE == 3) tambah_Kata("Ljava/lang/String;");
        if (TYPE_VALUE == 4) tambah_Kata("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) tambah_SMS('C');
        if (TYPE_VALUE == 6) tambah_Kata("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) tambah_Kata("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklarasi_4f4f026b. pengecualian Proses_VALUE_entri 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Kata("Indonesia");
        if (한국어묶음) { persyaratan_VALUE('.'); 말요구("Asli"); persyaratan_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Kata("Exception") || TAKE_Kata("IOException"))) return;
        if (TAKE_Kata("pengecualian") || TAKE_Kata("실행예외") || TAKE_Kata("I_O_pengecualian") || TAKE_Kata("tunggu_TIMEOUT_pengecualian") || TAKE_Kata("surel_LOOKUP_pengecualian") || TAKE_Kata("파일없음예외") || TAKE_Kata("komunikasi_pengecualian") || TAKE_Kata("tidak_sahih_argumen_pengecualian") || TAKE_Kata("숫자형식예외") || TAKE_Kata("범위예외") || TAKE_Kata("배열범위예외") || TAKE_Kata("문자열범위예외") || TAKE_Kata("NULL_Referensi_pengecualian") || TAKE_Kata("산술예외") || TAKE_Kata("Status_pengecualian") || TAKE_Kata("TYPE_Transmisi_pengecualian") || TAKE_Kata("음수배열크기예외") || TAKE_Kata("ARRAY_Store_kegagalan") || TAKE_Kata("alur_Status_pengecualian") || TAKE_Kata("대기중단예외")) return;
        kegagalan_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Kata("import")) {
            if (Kata_VALUE(posisi, "Indonesia")) 예외이름읽기();
            else {
                말요구("java"); persyaratan_VALUE('.'); 말요구("io"); persyaratan_VALUE('.');
                if (!(TAKE_Kata("FileInputStream") || TAKE_Kata("FileOutputStream") || TAKE_Kata("IOException"))) kegagalan_VALUE("unsupported import");
            }
            persyaratan_VALUE(';');
        }
        TAKE_Kata("public"); TAKE_Kata("final"); 말요구("class"); Kelas_token = pengidentifikasi_VALUE();
        Kelas_konstanta = Referensi(7, token_konstanta(Kelas_token), 0);
        induk_konstanta = Referensi(7, Kata_konstanta("java/lang/Object"), 0); CODE_konstanta = Kata_konstanta("Code"); persyaratan_VALUE('{');
        while (!galat && 종류() != '}') {
            if (metode_COUNT == 32) { kegagalan_VALUE("too many methods"); break; }
            int akses_entri = TAKE_Kata("public") ? 1 : TAKE_Kata("private") ? 2 : 0; 말요구("static");
            int fungsi_VALUE = metode_COUNT++;
            metode_akses[fungsi_VALUE] = akses_entri | 8;
            metode_kembalikan[fungsi_VALUE] = format_VALUE(); metode_entri_nama[fungsi_VALUE] = pengidentifikasi_VALUE(); persyaratan_VALUE('(');
            for (int depan_VALUE = 0; depan_VALUE < fungsi_VALUE; depan_VALUE++) if (이름같음(metode_entri_nama[depan_VALUE], metode_entri_nama[fungsi_VALUE])) kegagalan_VALUE("duplicate method (overloading unsupported)");
            while (!galat && 종류() != ')') {
                int 수 = metode_argumen_COUNT[fungsi_VALUE];
                if (수 == 16) { kegagalan_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) kegagalan_VALUE("void parameter");
                metode_argumen_TYPE[fungsi_VALUE * 16 + 수] = TYPE_VALUE; metode_argumen_nama[fungsi_VALUE * 16 + 수] = pengidentifikasi_VALUE();
                metode_argumen_COUNT[fungsi_VALUE]++;
                if (!terima(',')) break;
            }
            persyaratan_VALUE(')');
            if (TAKE_Kata("throws")) {
                do { 예외이름읽기(); } while (!galat && terima(','));
            }
            metode_isi[fungsi_VALUE] = posisi; persyaratan_VALUE('{');
            int berlapis_VALUE = 1;
            while (posisi < token_COUNT && berlapis_VALUE > 0) {
                if (종류() == '{') berlapis_VALUE++;
                if (종류() == '}') berlapis_VALUE--;
                posisi++;
            }
            if (berlapis_VALUE != 0) kegagalan_VALUE("unclosed method body");
            metode_mengakhiri[fungsi_VALUE] = posisi;
            metode_nama_konstanta[fungsi_VALUE] = token_konstanta(metode_entri_nama[fungsi_VALUE]);
            karakter_panjang = 0; tambah_SMS('(');
            for (int 수 = 0; 수 < metode_argumen_COUNT[fungsi_VALUE]; 수++) tambah_format(metode_argumen_TYPE[fungsi_VALUE * 16 + 수]);
            tambah_SMS(')'); tambah_format(metode_kembalikan[fungsi_VALUE]); 함수서술[fungsi_VALUE] = karakter_konstanta();
        }
        persyaratan_VALUE('}'); if (posisi != token_COUNT) kegagalan_VALUE("extra input after class");
    }
    static int FIND_lokal(int Nama_2) {
        for (int 수 = lokal_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokal_nama[수], Nama_2)) return 수;
        kegagalan_VALUE("unknown variable"); return 0;
    }
    static int tambah_lokal(int Nama_2, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokal_nama[수], Nama_2)) kegagalan_VALUE("duplicate local variable");
        if (lokal_COUNT == 128) { kegagalan_VALUE("too many locals"); return 0; }
        lokal_nama[lokal_COUNT] = Nama_2; lokal_TYPE[lokal_COUNT] = TYPE_VALUE; 지역깊이[lokal_COUNT] = 깊이;
        return lokal_COUNT++;
    }
    static boolean bilangan_bulat_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void tulis_lokal(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void periksa_TYPE(int aktual_data, int 기대) { if (aktual_data != 기대 && !(aktual_data == 5 && 기대 == 1)) kegagalan_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        karakter_panjang = 0; int jalankan = token_posisi[token_VALUE] + 1, 끝 = token_posisi[token_VALUE] + token_panjang[token_VALUE] - 1;
        while (jalankan < 끝 && !galat) {
            int VALUE = kodeSumber[jalankan++];
            if (VALUE == '\\') {
                if (jalankan == 끝) { kegagalan_VALUE("invalid escape"); break; }
                VALUE = kodeSumber[jalankan++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') kegagalan_VALUE("unsupported escape");
            }
            tambah_SMS(VALUE);
        }
    }
    static int urai_bilangan_bulat(int token_VALUE, boolean 음수) {
        if (token_panjang[token_VALUE] > 1 && kodeSumber[token_posisi[token_VALUE]] == '0') kegagalan_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_panjang[token_VALUE]; 수++) {
            int angka_item = kodeSumber[token_posisi[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && angka_item > (음수 ? 8 : 7)) kegagalan_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - angka_item;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Kata("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { kegagalan_VALUE("only file streams supported by new in source"); return 0; }
            String pemilik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            perintah(187, Referensi(7, Kata_konstanta(pemilik_VALUE), 0)); 내보내기(89);
            persyaratan_VALUE('('); periksa_TYPE(ekspresi_VALUE(), 3); boolean 이어 = false;
            if (terima(',')) { if (TYPE_VALUE != 7) kegagalan_VALUE("input stream constructor arguments"); periksa_TYPE(ekspresi_VALUE(), 2); 이어 = true; }
            persyaratan_VALUE(')');
            perintah(183, referensi_eksternal(10, pemilik_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (terima('(')) { int TYPE_VALUE = ekspresi_VALUE(); persyaratan_VALUE(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(urai_bilangan_bulat(posisi++, false)); return 1; }
        if (종류() == 258) { 문자읽기(posisi++); perintah(19, Referensi(8, karakter_konstanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(posisi++); if (karakter_panjang != 1) kegagalan_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Kata("true")) { 내보내기(4); return 2; }
        if (TAKE_Kata("false")) { 내보내기(3); return 2; }
        if (TAKE_Kata("Indonesia")) {
            persyaratan_VALUE('.'); 말요구("Asli"); persyaratan_VALUE('.');
            String pemilik_VALUE = "", metode_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, hasil = 0;
            if (TAKE_Kata("keluaranTeks")) {
                pemilik_VALUE = "Indonesia/Asli/keluaranTeks"; persyaratan_VALUE('.');
                if (TAKE_Kata("tulis_baris")) { metode_VALUE = "tulis_baris"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Kata("Tulis")) { metode_VALUE = "Tulis"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Kata("수쓰기")) { metode_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else kegagalan_VALUE("unknown Korean output method");
            } else if (TAKE_Kata("문자")) {
                pemilik_VALUE = "Indonesia/Asli/문자"; persyaratan_VALUE('.'); 가 = 3;
                if (TAKE_Kata("panjang_VALUE")) { metode_VALUE = "panjang_VALUE"; 서술 = "(Ljava/lang/String;)I"; hasil = 1; }
                else if (TAKE_Kata("poin_kode_COUNT")) { metode_VALUE = "poin_kode_COUNT"; 서술 = "(Ljava/lang/String;)I"; hasil = 1; }
                else if (TAKE_Kata("urai_bilangan_bulat")) { metode_VALUE = "urai_bilangan_bulat"; 서술 = "(Ljava/lang/String;)I"; hasil = 1; }
                else if (TAKE_Kata("tulis_bilangan_bulat_VALUE")) { metode_VALUE = "tulis_bilangan_bulat_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; hasil = 3; }
                else if (TAKE_Kata("같음")) { metode_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; hasil = 2; }
                else if (TAKE_Kata("tempel_SMS")) { metode_VALUE = "tempel_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; hasil = 3; }
                else if (TAKE_Kata("potong_VALUE")) { metode_VALUE = "potong_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; hasil = 3; }
                else kegagalan_VALUE("unknown Korean text method");
            } else if (TAKE_Kata("berkas")) {
                pemilik_VALUE = "Indonesia/Asli/berkas"; persyaratan_VALUE('.'); 가 = 3;
                if (TAKE_Kata("Baca")) { metode_VALUE = "Baca"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; hasil = 3; }
                else if (TAKE_Kata("Tulis")) { metode_VALUE = "Tulis"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else kegagalan_VALUE("unknown Korean file method");
            } else if (TAKE_Kata("화면")) {
                pemilik_VALUE = "Indonesia/Asli/화면"; persyaratan_VALUE('.');
                if (TAKE_Kata("너비")) { metode_VALUE = "너비"; 서술 = "()I"; hasil = 1; }
                else if (TAKE_Kata("높이")) { metode_VALUE = "높이"; 서술 = "()I"; hasil = 1; }
                else if (TAKE_Kata("persegi")) { metode_VALUE = "persegi"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Kata("hapus_entri_c8dbc399")) { metode_VALUE = "hapus_entri_c8dbc399"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Kata("기다리기")) { metode_VALUE = "기다리기"; 서술 = "()V"; }
                else kegagalan_VALUE("unknown Korean framebuffer method");
            } else kegagalan_VALUE("unsupported Korean library class");
            persyaratan_VALUE('('); if (가 != 0) periksa_TYPE(ekspresi_VALUE(), 가);
            if (SECOND_operand != 0) { persyaratan_VALUE(','); periksa_TYPE(ekspresi_VALUE(), SECOND_operand); }
            if (다 != 0) { persyaratan_VALUE(','); periksa_TYPE(ekspresi_VALUE(), 다); }
            if (라 != 0) { persyaratan_VALUE(','); periksa_TYPE(ekspresi_VALUE(), 라); }
            if (마 != 0) { persyaratan_VALUE(','); periksa_TYPE(ekspresi_VALUE(), 마); }
            persyaratan_VALUE(')'); perintah(184, referensi_eksternal(10, pemilik_VALUE, metode_VALUE, 서술)); return hasil;
        }
        if (TAKE_Kata("Integer")) {
            persyaratan_VALUE('.'); 말요구("parseInt"); persyaratan_VALUE('('); periksa_TYPE(ekspresi_VALUE(), 3); persyaratan_VALUE(')');
            perintah(184, referensi_eksternal(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nama_2 = pengidentifikasi_VALUE();
        if (terima('(')) {
            int fungsi_VALUE = -1;
            for (int 수 = 0; 수 < metode_COUNT; 수++) if (이름같음(Nama_2, metode_entri_nama[수])) fungsi_VALUE = 수;
            if (fungsi_VALUE < 0) { kegagalan_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!galat && 종류() != ')') {
                if (수 >= metode_argumen_COUNT[fungsi_VALUE]) { kegagalan_VALUE("too many arguments"); break; }
                periksa_TYPE(ekspresi_VALUE(), metode_argumen_TYPE[fungsi_VALUE * 16 + 수++]); if (!terima(',')) break;
            }
            persyaratan_VALUE(')'); if (수 != metode_argumen_COUNT[fungsi_VALUE]) kegagalan_VALUE("argument count mismatch");
            perintah(184, Referensi(10, Kelas_konstanta, Referensi(12, metode_nama_konstanta[fungsi_VALUE], 함수서술[fungsi_VALUE])));
            return metode_kembalikan[fungsi_VALUE];
        }
        int lokal_Cakupan = FIND_lokal(Nama_2), TYPE_VALUE = lokal_TYPE[lokal_Cakupan]; 지역읽기(lokal_Cakupan);
        while (!galat) {
            if (terima('[')) { periksa_TYPE(TYPE_VALUE, 4); periksa_TYPE(ekspresi_VALUE(), 1); persyaratan_VALUE(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (terima('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String pemilik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Kata("close")) { persyaratan_VALUE('('); persyaratan_VALUE(')'); perintah(182, referensi_eksternal(10, pemilik_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Kata("read")) { persyaratan_VALUE('('); persyaratan_VALUE(')'); perintah(182, referensi_eksternal(10, pemilik_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Kata("write")) { persyaratan_VALUE('('); periksa_TYPE(ekspresi_VALUE(), 1); persyaratan_VALUE(')'); perintah(182, referensi_eksternal(10, pemilik_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { kegagalan_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { periksa_TYPE(TYPE_VALUE, 3); persyaratan_VALUE('('); persyaratan_VALUE(')'); perintah(182, referensi_eksternal(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { kegagalan_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (terima('!')) { periksa_TYPE(단항(), 2); Perbandingan_VALUE(153); TYPE_VALUE = 2; }
        else if (terima('-')) {
            if (종류() == 257) 수상수(urai_bilangan_bulat(posisi++, true));
            else { periksa_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (terima('+')) { periksa_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!galat && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int pengodean_VALUE = 종류(); posisi++; periksa_TYPE(TYPE_VALUE, 1); periksa_TYPE(단항(), 1);
            내보내기(pengodean_VALUE == '*' ? 104 : pengodean_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!galat && (종류() == '+' || 종류() == '-')) {
            int pengodean_VALUE = 종류(); posisi++; int 경계 = CODE_ukuran, BACK_VALUE_TYPE = 곱식();
            if (pengodean_VALUE == '+' && (TYPE_VALUE == 3 || BACK_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, BACK_VALUE_TYPE); TYPE_VALUE = 3; }
            else { periksa_TYPE(TYPE_VALUE, 1); periksa_TYPE(BACK_VALUE_TYPE, 1); 내보내기(pengodean_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) kegagalan_VALUE("unsupported concatenation type");
        return referensi_eksternal(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int depan_VALUE_TYPE, int BACK_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 buat 코드를 삽입한다.
        // RIGHT ekspresi_VALUE 내부의 serekan_VALUE cabang 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_ukuran;
        perintah(187, Referensi(7, Kata_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        perintah(183, referensi_eksternal(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); perintah(182, 붙임참조(depan_VALUE_TYPE));
        if (galat) return;
        int panjang_VALUE = CODE_ukuran - 끝;
        for (int 수 = 0; 수 < panjang_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + panjang_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < panjang_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        perintah(182, 붙임참조(BACK_VALUE_TYPE)); perintah(182, referensi_eksternal(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Perbandingan_ekspresi() {
        int TYPE_VALUE = 합식();
        while (!galat && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int pengodean_VALUE = 종류(); posisi++; periksa_TYPE(TYPE_VALUE, 1); periksa_TYPE(합식(), 1);
            Perbandingan_VALUE(pengodean_VALUE == '<' ? 161 : pengodean_VALUE == '>' ? 163 : pengodean_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Perbandingan_ekspresi();
        while (!galat && (종류() == 300 || 종류() == 301)) {
            int pengodean_VALUE = 종류(); posisi++; int BACK_VALUE_TYPE = Perbandingan_ekspresi();
            if (TYPE_VALUE == 0 || BACK_VALUE_TYPE == 0) kegagalan_VALUE("void expression");
            if (!(bilangan_bulat_TYPE(TYPE_VALUE) && bilangan_bulat_TYPE(BACK_VALUE_TYPE))) periksa_TYPE(BACK_VALUE_TYPE, TYPE_VALUE);
            Perbandingan_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (pengodean_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!galat && terima(304)) {
            periksa_TYPE(TYPE_VALUE, 2); int 가 = cabang(153); periksa_TYPE(동등식(), 2); int SECOND_operand = cabang(153);
            내보내기(4); int 끝 = cabang(167); link_VALUE(가, CODE_ukuran); link_VALUE(SECOND_operand, CODE_ukuran); 내보내기(3); link_VALUE(끝, CODE_ukuran); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int ekspresi_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!galat && terima(305)) {
            periksa_TYPE(TYPE_VALUE, 2); int 가 = cabang(154); periksa_TYPE(논리곱(), 2); int SECOND_operand = cabang(154);
            내보내기(3); int 끝 = cabang(167); link_VALUE(가, CODE_ukuran); link_VALUE(SECOND_operand, CODE_ukuran); 내보내기(4); link_VALUE(끝, CODE_ukuran); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void tugas_VALUE(boolean Perbolehkan_deklarasi) {
        if (Kata_VALUE(posisi, "int") || Kata_VALUE(posisi, "boolean") || Kata_VALUE(posisi, "String") || Kata_VALUE(posisi, "char")
            || Kata_VALUE(posisi, "FileInputStream") || Kata_VALUE(posisi, "FileOutputStream")) {
            if (!Perbolehkan_deklarasi) kegagalan_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), Nama_2 = pengidentifikasi_VALUE(); persyaratan_VALUE('='); periksa_TYPE(ekspresi_VALUE(), TYPE_VALUE);
            tulis_lokal(tambah_lokal(Nama_2, TYPE_VALUE)); return;
        }
        int Nama_2 = pengidentifikasi_VALUE(), lokal_Cakupan = FIND_lokal(Nama_2);
        if (terima('=')) { periksa_TYPE(ekspresi_VALUE(), lokal_TYPE[lokal_Cakupan]); tulis_lokal(lokal_Cakupan); }
        else if (종류() >= 308 && 종류() <= 312) {
            int pengodean_VALUE = 종류(); posisi++; 지역읽기(lokal_Cakupan); int 경계 = CODE_ukuran, BACK_VALUE_TYPE = ekspresi_VALUE();
            if (pengodean_VALUE == 308 && lokal_TYPE[lokal_Cakupan] == 3) 결합(경계, 3, BACK_VALUE_TYPE);
            else {
                periksa_TYPE(lokal_TYPE[lokal_Cakupan], 1); periksa_TYPE(BACK_VALUE_TYPE, 1);
                내보내기(pengodean_VALUE == 308 ? 96 : pengodean_VALUE == 309 ? 100 : pengodean_VALUE == 310 ? 104 : pengodean_VALUE == 311 ? 108 : 112);
                if (lokal_TYPE[lokal_Cakupan] == 5) 내보내기(146);
            }
            tulis_lokal(lokal_Cakupan);
        }
        else if (종류() == 306 || 종류() == 307) {
            periksa_TYPE(lokal_TYPE[lokal_Cakupan], 1); 내보내기(132); 내보내기(lokal_Cakupan); 내보내기(종류() == 306 ? 1 : 255); posisi++;
            if (lokal_TYPE[lokal_Cakupan] == 5) { 지역읽기(lokal_Cakupan); 내보내기(146); tulis_lokal(lokal_Cakupan); }
        } else kegagalan_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); persyaratan_VALUE('.'); 말요구("out"); persyaratan_VALUE('.');
        boolean 줄바꿈 = TAKE_Kata("println"); if (!줄바꿈) 말요구("print"); persyaratan_VALUE('(');
        perintah(178, referensi_eksternal(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean kosong_argumen = 종류() == ')';
        int TYPE_VALUE = kosong_argumen ? 0 : ekspresi_VALUE(); persyaratan_VALUE(')'); persyaratan_VALUE(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !kosong_argumen)) kegagalan_VALUE("unsupported print argument");
        perintah(182, referensi_eksternal(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean pernyataan_VALUE() {
        if (galat) return false;
        if (깊이 > 32) { kegagalan_VALUE("statement nesting too deep"); return false; }
        if (terima('{')) {
            깊이++; boolean kembalikan_KR = false;
            while (!galat && 종류() != '}') { if (kembalikan_KR) kegagalan_VALUE("unreachable statement"); kembalikan_KR = pernyataan_VALUE(); }
            persyaratan_VALUE('}'); for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return kembalikan_KR;
        }
        if (terima(';')) return false;
        if (TAKE_Kata("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : ekspresi_VALUE(); periksa_TYPE(TYPE_VALUE, metode_kembalikan[saat_ini_metode]); persyaratan_VALUE(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Kata("if")) {
            persyaratan_VALUE('('); periksa_TYPE(ekspresi_VALUE(), 2); persyaratan_VALUE(')'); int FALSE_VALUE = cabang(153);
            깊이++; boolean 가 = kontrol_pernyataan(); 깊이--;
            if (TAKE_Kata("else")) { int 끝 = cabang(167); link_VALUE(FALSE_VALUE, CODE_ukuran); 깊이++; boolean SECOND_operand = kontrol_pernyataan(); 깊이--; link_VALUE(끝, CODE_ukuran); return 가 && SECOND_operand; }
            link_VALUE(FALSE_VALUE, CODE_ukuran); return false;
        }
        if (TAKE_Kata("while")) {
            int jalankan = CODE_ukuran; persyaratan_VALUE('('); periksa_TYPE(ekspresi_VALUE(), 2); persyaratan_VALUE(')'); int 끝 = cabang(153);
            깊이++; kontrol_pernyataan(); 깊이--; link_VALUE(cabang(167), jalankan); link_VALUE(끝, CODE_ukuran); return false;
        }
        if (TAKE_Kata("for")) {
            깊이++; persyaratan_VALUE('('); if (종류() != ';') tugas_VALUE(true); persyaratan_VALUE(';');
            int kondisi = CODE_ukuran; if (종류() == ';') 내보내기(4); else periksa_TYPE(ekspresi_VALUE(), 2); persyaratan_VALUE(';');
            int 끝 = cabang(153), teks_isi = cabang(167), refresh = CODE_ukuran;
            if (종류() != ')') tugas_VALUE(false); persyaratan_VALUE(')'); link_VALUE(cabang(167), kondisi); link_VALUE(teks_isi, CODE_ukuran);
            kontrol_pernyataan(); link_VALUE(cabang(167), refresh); link_VALUE(끝, CODE_ukuran);
            for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Kata_VALUE(posisi, "System")) { 화면출력(); return false; }
        if (종류() == 256 && posisi + 1 < token_COUNT && (토큰종류[posisi + 1] == '(' || 토큰종류[posisi + 1] == '.')) {
            int TYPE_VALUE = ekspresi_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); persyaratan_VALUE(';'); return false;
        }
        tugas_VALUE(true); persyaratan_VALUE(';'); return false;
    }
    static boolean kontrol_pernyataan() {
        if (Kata_VALUE(posisi, "int") || Kata_VALUE(posisi, "boolean") || Kata_VALUE(posisi, "char") || Kata_VALUE(posisi, "String")
            || Kata_VALUE(posisi, "FileInputStream") || Kata_VALUE(posisi, "FileOutputStream")) kegagalan_VALUE("local declaration requires braces");
        return pernyataan_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == keluaranTeks.length) kegagalan_VALUE("class file too large"); else keluaranTeks[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void tulis_Kelas() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_COUNT);
        for (int 수 = 0; 수 < konstanta_ukuran; 수++) 출바(konstanta_VALUE[수]);
        출짧(0x21); 출짧(Kelas_konstanta); 출짧(induk_konstanta); 출짧(0); 출짧(0); 출짧(metode_COUNT);
        for (int 수 = 0; 수 < metode_COUNT; 수++) {
            출짧(metode_akses[수]); 출짧(metode_nama_konstanta[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_konstanta);
            출정(12 + metode_panjang[수]); 출짧(128); 출짧(함수지역[수]); 출정(metode_panjang[수]);
            for (int slot_entri = 0; slot_entri < metode_panjang[수]; slot_entri++) 출바(CODE_VALUE[metode_CODE[수] + slot_entri]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int jalankan() {
        if (ruang_pengguna.인수개수() == 1 && 자바도구.같음(ruang_pengguna.argumen(0), "-version")) {
            ruang_pengguna.Tulis("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (ruang_pengguna.인수개수() != 1) { ruang_pengguna.Tulis("Usage: javac FILE.java\n"); return 2; }
        int nama_ukuran = 자바도구.Nama_2(nama_file_SMS, ruang_pengguna.argumen(0));
        if (nama_ukuran < 6 || nama_ukuran > 62 || nama_file_SMS[nama_ukuran - 5] != '.' || nama_file_SMS[nama_ukuran - 4] != 'j'
            || nama_file_SMS[nama_ukuran - 3] != 'a' || nama_file_SMS[nama_ukuran - 2] != 'v' || nama_file_SMS[nama_ukuran - 1] != 'a') {
            ruang_pengguna.Tulis("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        sumber_ukuran = ruang_pengguna.파일읽기(nama_file_SMS, kodeSumber);
        if (sumber_ukuran < 0) { ruang_pengguna.Tulis("javac: cannot read source: "); 자바도구.수쓰기(sumber_ukuran); ruang_pengguna.tulis_karakter_VALUE(10); return 1; }
        sumber_ukuran = 자바도구.원문해독(kodeSumber, sumber_ukuran);
        if (sumber_ukuran < 0) { ruang_pengguna.Tulis("javac error: invalid UTF-8 source\n"); return 1; }
        potong_VALUE(); if (!galat) 선언읽기();
        if (!galat) {
            if (token_panjang[Kelas_token] != nama_ukuran - 5) kegagalan_VALUE("class name must match file name");
            for (int 수 = 0; 수 < nama_ukuran - 5; 수++) if (kodeSumber[token_posisi[Kelas_token] + 수] != nama_file_SMS[수]) kegagalan_VALUE("class name must match file name");
        }
        for (saat_ini_metode = 0; saat_ini_metode < metode_COUNT && !galat; saat_ini_metode++) {
            posisi = metode_isi[saat_ini_metode]; metode_CODE[saat_ini_metode] = CODE_ukuran; lokal_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metode_argumen_COUNT[saat_ini_metode]; 수++) tambah_lokal(metode_argumen_nama[saat_ini_metode * 16 + 수], metode_argumen_TYPE[saat_ini_metode * 16 + 수]);
            boolean kembalikan_KR = pernyataan_VALUE();
            if (!kembalikan_KR && metode_kembalikan[saat_ini_metode] != 0) kegagalan_VALUE("missing return");
            // cabang 뒤의 합류 지점은 반드시 aktual_data 명령이어야 한다 (버전 49 검증기).
            if (metode_kembalikan[saat_ini_metode] == 0) 내보내기(177);
            else { boolean bilangan_bulat = metode_kembalikan[saat_ini_metode] <= 2 || metode_kembalikan[saat_ini_metode] == 5; 내보내기(bilangan_bulat ? 3 : 1); 내보내기(bilangan_bulat ? 172 : 176); }
            if (posisi != metode_mengakhiri[saat_ini_metode]) kegagalan_VALUE("invalid method body");
            함수지역[saat_ini_metode] = lokal_COUNT; metode_panjang[saat_ini_metode] = CODE_ukuran - metode_CODE[saat_ini_metode];
        }
        if (galat) return 1;
        tulis_Kelas(); if (galat) return 1;
        nama_file_SMS[nama_ukuran - 4] = 'c'; nama_file_SMS[nama_ukuran - 3] = 'l'; nama_file_SMS[nama_ukuran - 2] = 'a';
        nama_file_SMS[nama_ukuran - 1] = 's'; nama_file_SMS[nama_ukuran] = 's'; nama_file_SMS[nama_ukuran + 1] = 0;
        int hasil = ruang_pengguna.tulis_file(nama_file_SMS, keluaranTeks, 출력크기);
        if (hasil < 0) { ruang_pengguna.Tulis("javac: cannot save class: "); 자바도구.수쓰기(hasil); ruang_pengguna.tulis_karakter_VALUE(10); return 1; }
        ruang_pengguna.Tulis("Compiled: "); for (int 수 = 0; nama_file_SMS[수] != 0; 수++) ruang_pengguna.tulis_karakter_VALUE(nama_file_SMS[수]);
        ruang_pengguna.Tulis(" (JVM class version 49)\n"); return 0;
    }
}
