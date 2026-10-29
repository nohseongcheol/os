// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fail/스택/Rujukan/cabang 경계를 laksanakan_perintah 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fail = new int[16384], nama_fail_SMS = new int[64];
    static int[] pemalar_tag = new int[512], 상가 = new int[512], pemalar_SECOND_VALUE = new int[512], rentetan_Rujukan = new int[512];
    static int[] kaedah_nama_SMS = new int[32], kaedah_TYPE = new int[32], kaedah_capai = new int[32];
    static int[] kaedah_Mula = new int[32], kaedah_tamat = new int[32], kaedah_tindan = new int[32], 함수지역 = new int[32];
    static int[] kaedah_argumen_COUNT = new int[32], kaedah_argumen_TYPE = new int[512], kaedah_kembalikan = new int[32];
    static int[] 경계 = new int[16384];
    static int[] setempat_VALUE = new int[4096], setempat_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] bingkai_kaedah = new int[32], bingkai_jawatan = new int[32], bingkai_tindan = new int[32];
    static int[] timbunan_VALUE = new int[8192];
    static int Saiz, 읽기위치, pemalar_COUNT, kaedah_COUNT, nama_kelas, bingkai_INDEX = -1, timbunan_tamat_jawatan = 1, kembalikan_TYPE;
    static boolean RALAT;

    static void kegagalan_VALUE(String Word_SMS) {
        if (!RALAT) { ruang_pengguna.Tulis("JVM error: "); ruang_pengguna.Tulis(Word_SMS); ruang_pengguna.tulis_aksara_VALUE(10); }
        RALAT = true;
    }
    static boolean klip(int Jalan, int kepanjangan_VALUE) { return Jalan >= 0 && kepanjangan_VALUE >= 0 && Jalan <= Saiz - kepanjangan_VALUE; }
    static int bait_VALUE() {
        if (!klip(읽기위치, 1)) { kegagalan_VALUE("truncated class file"); return 0; }
        return Fail[읽기위치++];
    }
    static int 짧은수() { return bait_VALUE() << 8 | bait_VALUE(); }
    static int integer() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int kepanjangan_VALUE) { if (!klip(읽기위치, kepanjangan_VALUE)) kegagalan_VALUE("invalid attribute size"); else 읽기위치 += kepanjangan_VALUE; }
    static boolean cek_pemalar(int 수, int 종류) {
        if (수 <= 0 || 수 >= pemalar_COUNT || pemalar_tag[수] != 종류) { kegagalan_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_julat(int Jalan, int kepanjangan_VALUE, String Word_SMS) {
        if (!klip(Jalan, kepanjangan_VALUE) || kepanjangan_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < kepanjangan_VALUE; 수++) if (Fail[Jalan + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int pemalar_VALUE, String Word_SMS) { return cek_pemalar(pemalar_VALUE, 1) && SMS_julat(상가[pemalar_VALUE], pemalar_SECOND_VALUE[pemalar_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!cek_pemalar(가, 1) || !cek_pemalar(나, 1) || pemalar_SECOND_VALUE[가] != pemalar_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < pemalar_SECOND_VALUE[가]; 수++) if (Fail[상가[가] + 수] != Fail[상가[나] + 수]) return false;
        return true;
    }
    static int nama_kelas_SMS(int 수) { return cek_pemalar(수, 7) && cek_pemalar(상가[수], 1) ? 상가[수] : 0; }
    static int Rujukan_nama(int 수) { return cek_pemalar(수, 12) && cek_pemalar(상가[수], 1) ? 상가[수] : 0; }
    static int jenis_rujukan(int 수) { return cek_pemalar(수, 12) && cek_pemalar(pemalar_SECOND_VALUE[수], 1) ? pemalar_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { kegagalan_VALUE("invalid descriptor"); return 0; }
        int VALUE = bait_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Jalan = 읽기위치;
            while (읽기위치 < 끝 && Fail[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Jalan) kegagalan_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        kegagalan_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int fungsi_VALUE) {
        int 이전 = 읽기위치, 수 = kaedah_TYPE[fungsi_VALUE];
        if (!cek_pemalar(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + pemalar_SECOND_VALUE[수];
        if (bait_VALUE() != '(') kegagalan_VALUE("invalid method descriptor");
        int item_COUNT = 0;
        while (!RALAT && 읽기위치 < 끝 && Fail[읽기위치] != ')') {
            if (item_COUNT == 16) { kegagalan_VALUE("too many method arguments"); break; }
            kaedah_argumen_TYPE[fungsi_VALUE * 16 + item_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bait_VALUE() != ')') kegagalan_VALUE("invalid method descriptor");
        kaedah_kembalikan[fungsi_VALUE] = 서술형(끝, true); kaedah_argumen_COUNT[fungsi_VALUE] = item_COUNT;
        if (읽기위치 != 끝) kegagalan_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void langkau_atribut() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !RALAT; 수++) { cek_pemalar(짧은수(), 1); 건너(integer()); }
    }
    static int perintah_kepanjangan(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE == 50
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE == 83 || VALUE == 87 || VALUE == 89 || VALUE == 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (integer() != 0xcafebabe) kegagalan_VALUE("not a class file");
        int 부판 = 짧은수(), versi_VALUE = 짧은수();
        if (versi_VALUE < 45 || versi_VALUE > 52 || 부판 != 0) kegagalan_VALUE("supported class versions: 45..52, minor 0");
        pemalar_COUNT = 짧은수();
        if (pemalar_COUNT < 1 || pemalar_COUNT > 512) { kegagalan_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < pemalar_COUNT && !RALAT; 수++) {
            int 종류 = bait_VALUE(); pemalar_tag[수] = 종류;
            if (종류 == 1) { pemalar_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(pemalar_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = integer();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); pemalar_SECOND_VALUE[수] = 짧은수(); }
            else kegagalan_VALUE("unsupported constant type");
        }
        int keizinan_VALUE = 짧은수();
        if ((keizinan_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) kegagalan_VALUE("unsupported class flags");
        nama_kelas = nama_kelas_SMS(짧은수());
        if (!Word_SMS(nama_kelas_SMS(짧은수()), "java/lang/Object")) kegagalan_VALUE("inheritance unsupported");
        if (짧은수() != 0) kegagalan_VALUE("interfaces unsupported");
        if (짧은수() != 0) kegagalan_VALUE("fields unsupported");
        kaedah_COUNT = 짧은수();
        if (kaedah_COUNT < 1 || kaedah_COUNT > 32) { kegagalan_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < kaedah_COUNT && !RALAT; 수++) {
            kaedah_capai[수] = 짧은수(); kaedah_nama_SMS[수] = 짧은수(); kaedah_TYPE[수] = 짧은수();
            cek_pemalar(kaedah_nama_SMS[수], 1); 서술읽기(수);
            if ((kaedah_capai[수] & (0x100 | 0x400 | 0x20)) != 0) kegagalan_VALUE("native, abstract and synchronized methods unsupported");
            if ((kaedah_capai[수] & 8) == 0 && !Word_SMS(kaedah_nama_SMS[수], "<init>")) kegagalan_VALUE("instance methods unsupported");
            if (Word_SMS(kaedah_nama_SMS[수], "<clinit>")) kegagalan_VALUE("class initializers unsupported");
            for (int hadapan_VALUE = 0; hadapan_VALUE < 수; hadapan_VALUE++) if (같은말(kaedah_nama_SMS[hadapan_VALUE], kaedah_nama_SMS[수]) && 같은말(kaedah_TYPE[hadapan_VALUE], kaedah_TYPE[수])) kegagalan_VALUE("duplicate method");
            int item_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < item_COUNT && !RALAT; atribut_VALUE++) {
                int Nama = 짧은수(), kepanjangan_VALUE = integer(), Jalan = 읽기위치;
                if (!klip(Jalan, kepanjangan_VALUE)) { kegagalan_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nama, "Code")) {
                    if (kaedah_Mula[수] != 0) kegagalan_VALUE("duplicate Code attribute");
                    kaedah_tindan[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_kepanjangan = integer();
                    if (kaedah_tindan[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < kaedah_argumen_COUNT[수]
                        || kod_kepanjangan < 1 || kod_kepanjangan > 8192) kegagalan_VALUE("method memory limits exceeded");
                    kaedah_Mula[수] = 읽기위치; 건너(kod_kepanjangan); kaedah_tamat[수] = 읽기위치;
                    if (짧은수() != 0) kegagalan_VALUE("exception handlers unsupported");
                    langkau_atribut();
                    if (읽기위치 != Jalan + kepanjangan_VALUE) kegagalan_VALUE("Code attribute size mismatch");
                } else 건너(kepanjangan_VALUE);
            }
            if (kaedah_Mula[수] == 0) kegagalan_VALUE("missing Code attribute");
            int 칸 = kaedah_Mula[수];
            while (칸 < kaedah_tamat[수] && !RALAT) {
                int kepanjangan_VALUE = perintah_kepanjangan(Fail[칸]);
                if (kepanjangan_VALUE == 0 || kepanjangan_VALUE > kaedah_tamat[수] - 칸) { kegagalan_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += kepanjangan_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 cabang 목적지를 허용하지 않는다.
            칸 = kaedah_Mula[수];
            while (칸 < kaedah_tamat[수] && !RALAT) {
                int VALUE = Fail[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int destinasi_VALUE = 칸 + (short)(Fail[칸 + 1] << 8 | Fail[칸 + 2]);
                    if (destinasi_VALUE < kaedah_Mula[수] || destinasi_VALUE >= kaedah_tamat[수] || 경계[destinasi_VALUE] != 수 + 1) kegagalan_VALUE("invalid branch target");
                }
                칸 += perintah_kepanjangan(VALUE);
            }
        }
        if (!RALAT) langkau_atribut();
        if (읽기위치 != Saiz) kegagalan_VALUE("extra class file data");
    }
    static int peruntuk_Storan(int 종류, int kepanjangan_VALUE) {
        if (kepanjangan_VALUE < 0 || kepanjangan_VALUE > timbunan_VALUE.length - timbunan_tamat_jawatan - 2) { kegagalan_VALUE("object heap exhausted or negative array size"); return 0; }
        int Rujukan = timbunan_tamat_jawatan; timbunan_tamat_jawatan += kepanjangan_VALUE + 2; timbunan_VALUE[Rujukan] = 종류; timbunan_VALUE[Rujukan + 1] = kepanjangan_VALUE;
        return Rujukan;
    }
    static boolean objek_VALUE(int Rujukan, int 종류) {
        if (Rujukan < 1 || Rujukan >= timbunan_tamat_jawatan - 1 || timbunan_VALUE[Rujukan] != 종류) { kegagalan_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int pemalar_SMS(int INDEX) {
        if (!cek_pemalar(INDEX, 1)) return 0;
        if (rentetan_Rujukan[INDEX] != 0) return rentetan_Rujukan[INDEX];
        int Rujukan = peruntuk_Storan(1, pemalar_SECOND_VALUE[INDEX]); if (RALAT) return 0;
        int 끝 = 상가[INDEX] + pemalar_SECOND_VALUE[INDEX], 수 = 상가[INDEX], kepanjangan_VALUE = 0;
        while (수 < 끝 && !RALAT) {
            int VALUE = Fail[수++];
            if (VALUE == 0) kegagalan_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Seterusnya_item = Fail[수++];
                if ((Seterusnya_item & 192) != 128) kegagalan_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Seterusnya_item & 63;
                if (VALUE != 0 && VALUE < 128) kegagalan_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Fail[수++], 나 = Fail[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) kegagalan_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) kegagalan_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) kegagalan_VALUE("invalid modified UTF-8");
            timbunan_VALUE[Rujukan + 2 + kepanjangan_VALUE++] = VALUE;
        }
        timbunan_VALUE[Rujukan + 1] = kepanjangan_VALUE; rentetan_Rujukan[INDEX] = Rujukan; return Rujukan;
    }
    static int hos_aksara(String VALUE) {
        int Rujukan = peruntuk_Storan(1, VALUE.length()); if (RALAT) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) timbunan_VALUE[Rujukan + 2 + 수] = VALUE.charAt(수);
        return Rujukan;
    }
    static void tulis_SMS(int Rujukan) {
        if (Rujukan == 0) { ruang_pengguna.Tulis("null"); return; }
        if (!objek_VALUE(Rujukan, 1)) return;
        for (int 수 = 0; 수 < timbunan_VALUE[Rujukan + 1]; 수++) ruang_pengguna.tulis_aksara_VALUE(timbunan_VALUE[Rujukan + 2 + 수]);
    }
    static int digit_aksara(int VALUE) {
        int Rujukan = peruntuk_Storan(1, 11); if (RALAT) return 0;
        int kepanjangan_VALUE = 0;
        if (VALUE < 0) timbunan_VALUE[Rujukan + 2 + kepanjangan_VALUE++] = '-'; else VALUE = -VALUE;
        int jawatan_INDEX = 1000000000; boolean Jalan = false;
        while (jawatan_INDEX != 0) {
            int 수 = -(VALUE / jawatan_INDEX);
            if (수 != 0 || Jalan || jawatan_INDEX == 1) { timbunan_VALUE[Rujukan + 2 + kepanjangan_VALUE++] = '0' + 수; Jalan = true; }
            VALUE %= jawatan_INDEX; jawatan_INDEX /= 10;
        }
        timbunan_VALUE[Rujukan + 1] = kepanjangan_VALUE; return Rujukan;
    }
    static int 정수해독(int Rujukan) {
        if (!objek_VALUE(Rujukan, 1)) return 0;
        int kepanjangan_VALUE = timbunan_VALUE[Rujukan + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (kepanjangan_VALUE > 0 && (timbunan_VALUE[Rujukan + 2] == '-' || timbunan_VALUE[Rujukan + 2] == '+')) { 음수 = timbunan_VALUE[Rujukan + 2] == '-'; 수++; }
        if (수 == kepanjangan_VALUE) kegagalan_VALUE("NumberFormatException");
        for (; 수 < kepanjangan_VALUE && !RALAT; 수++) {
            int digit_VALUE = timbunan_VALUE[Rujukan + 2 + 수] - '0';
            if (digit_VALUE < 0 || digit_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && digit_VALUE > (음수 ? 8 : 7)) kegagalan_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - digit_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (RALAT) return;
        if (bingkai_INDEX < 0 || bingkai_tindan[bingkai_INDEX] >= kaedah_tindan[bingkai_kaedah[bingkai_INDEX]]) { kegagalan_VALUE("operand stack overflow"); return; }
        int 칸 = bingkai_INDEX * 128 + bingkai_tindan[bingkai_INDEX]++; 스택값[칸] = VALUE; 스택형[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (RALAT) return 0;
        if (bingkai_INDEX < 0 || bingkai_tindan[bingkai_INDEX] < 1) { kegagalan_VALUE("operand stack underflow"); return 0; }
        int 칸 = bingkai_INDEX * 128 + --bingkai_tindan[bingkai_INDEX]; kembalikan_TYPE = 스택형[칸];
        if (TYPE_VALUE != 0 && kembalikan_TYPE != TYPE_VALUE) kegagalan_VALUE("operand type mismatch");
        return 스택값[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[bingkai_kaedah[bingkai_INDEX]] || INDEX < 0 || setempat_TYPE[bingkai_INDEX * 128 + INDEX] != TYPE_VALUE) { kegagalan_VALUE("invalid or uninitialized local"); return; }
        넣기(setempat_VALUE[bingkai_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void tulis_setempat(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[bingkai_kaedah[bingkai_INDEX]] || INDEX < 0) { kegagalan_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); setempat_VALUE[bingkai_INDEX * 128 + INDEX] = VALUE; setempat_TYPE[bingkai_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Kedudukan = bingkai_jawatan[bingkai_INDEX];
        if (Kedudukan < kaedah_Mula[bingkai_kaedah[bingkai_INDEX]] || Kedudukan >= kaedah_tamat[bingkai_kaedah[bingkai_INDEX]]) { kegagalan_VALUE("instruction pointer out of range"); return 0; }
        bingkai_jawatan[bingkai_INDEX]++; return Fail[Kedudukan];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void alih_VALUE(int Kedudukan) {
        int fungsi_VALUE = bingkai_kaedah[bingkai_INDEX];
        if (Kedudukan < kaedah_Mula[fungsi_VALUE] || Kedudukan >= kaedah_tamat[fungsi_VALUE] || 경계[Kedudukan] != fungsi_VALUE + 1) kegagalan_VALUE("invalid branch target");
        else bingkai_jawatan[bingkai_INDEX] = Kedudukan;
    }
    static void 호출(int fungsi_VALUE) {
        if (bingkai_INDEX == 31) { kegagalan_VALUE("call stack limit (32)"); return; }
        int Seterusnya_item = bingkai_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) setempat_TYPE[Seterusnya_item * 128 + 수] = 0;
        for (int 수 = kaedah_argumen_COUNT[fungsi_VALUE] - 1; 수 >= 0; 수--) {
            setempat_VALUE[Seterusnya_item * 128 + 수] = 빼기(kaedah_argumen_TYPE[fungsi_VALUE * 16 + 수]); setempat_TYPE[Seterusnya_item * 128 + 수] = kaedah_argumen_TYPE[fungsi_VALUE * 16 + 수];
        }
        bingkai_INDEX = Seterusnya_item; bingkai_kaedah[bingkai_INDEX] = fungsi_VALUE; bingkai_jawatan[bingkai_INDEX] = kaedah_Mula[fungsi_VALUE]; bingkai_tindan[bingkai_INDEX] = 0;
    }
    static void kembalikan_ukuran(int TYPE_VALUE) {
        if (TYPE_VALUE != kaedah_kembalikan[bingkai_kaedah[bingkai_INDEX]]) { kegagalan_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        bingkai_INDEX--; if (bingkai_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] strim_nama_fail = new int[64];
    static void fail_strim_CALL(int pemilik_VALUE, int Nama, int format_VALUE, int Perintah) {
        boolean 출력 = Word_SMS(pemilik_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Perintah == 183 && Word_SMS(Nama, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { kegagalan_VALUE("unsupported file stream constructor"); return; }
            int fail_pemasukan_nama = 빼기(2), strim_VALUE = 빼기(2);
            if (!objek_VALUE(fail_pemasukan_nama, 1) || !objek_VALUE(strim_VALUE, 종류) || RALAT) return;
            if (timbunan_VALUE[strim_VALUE + 3] != 0) { kegagalan_VALUE("file stream already initialized"); return; }
            int kepanjangan_VALUE = timbunan_VALUE[fail_pemasukan_nama + 1];
            if (kepanjangan_VALUE < 1 || kepanjangan_VALUE > 63) { kegagalan_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < kepanjangan_VALUE; 칸++) {
                int VALUE = timbunan_VALUE[fail_pemasukan_nama + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { kegagalan_VALUE("file stream paths currently require ASCII"); return; }
                strim_nama_fail[칸] = VALUE;
            }
            strim_nama_fail[kepanjangan_VALUE] = 0;
            int 서술자 = ruang_pengguna.파일서술자열기(strim_nama_fail, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kegagalan_VALUE("FileNotFoundException: file open failed"); return; }
            timbunan_VALUE[strim_VALUE + 2] = 서술자; timbunan_VALUE[strim_VALUE + 3] = 1;
            return;
        }
        if (Perintah != 182) { kegagalan_VALUE("invalid file stream invocation"); return; }
        int Aksi = -1, VALUE = 0;
        if (Word_SMS(Nama, "close") && Word_SMS(format_VALUE, "()V")) Aksi = 0;
        if (!출력 && Word_SMS(Nama, "read") && Word_SMS(format_VALUE, "()I")) Aksi = 1;
        if (출력 && Word_SMS(Nama, "write") && Word_SMS(format_VALUE, "(I)V")) { Aksi = 2; VALUE = 빼기(1); }
        if (Aksi < 0) { kegagalan_VALUE("unsupported file stream method"); return; }
        int strim_VALUE = 빼기(2);
        if (!objek_VALUE(strim_VALUE, 종류) || RALAT) return;
        if (timbunan_VALUE[strim_VALUE + 3] == 0) { kegagalan_VALUE("uninitialized file stream"); return; }
        int 서술자 = timbunan_VALUE[strim_VALUE + 2];
        if (Aksi == 0) {
            if (서술자 >= 0 && ruang_pengguna.파일서술자닫기(서술자) < 0) kegagalan_VALUE("IOException: close failed");
            timbunan_VALUE[strim_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { kegagalan_VALUE("IOException: stream closed"); return; }
        if (Aksi == 1) {
            int ukuran = ruang_pengguna.파일한바이트읽기(서술자);
            if (ukuran < -1) kegagalan_VALUE("IOException: read failed"); else 넣기(ukuran, 1);
        } else if (ruang_pengguna.파일한바이트쓰기(서술자, VALUE) != 1) kegagalan_VALUE("IOException: write failed");
    }
    static void CALL_kaedah(int INDEX, int Perintah) {
        if (!cek_pemalar(INDEX, 10)) return;
        int pemilik_VALUE = nama_kelas_SMS(상가[INDEX]), Nama = Rujukan_nama(pemalar_SECOND_VALUE[INDEX]), format_VALUE = jenis_rujukan(pemalar_SECOND_VALUE[INDEX]);
        if (RALAT) return;
        if (같은말(pemilik_VALUE, nama_kelas)) {
            if (Perintah != 184) { kegagalan_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < kaedah_COUNT; 수++) if (같은말(Nama, kaedah_nama_SMS[수]) && 같은말(format_VALUE, kaedah_TYPE[수])) {
                if ((kaedah_capai[수] & 8) == 0) kegagalan_VALUE("method is not static"); else 호출(수);
                return;
            }
            kegagalan_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(pemilik_VALUE, "java/io/FileInputStream") || Word_SMS(pemilik_VALUE, "java/io/FileOutputStream")) {
            fail_strim_CALL(pemilik_VALUE, Nama, format_VALUE, Perintah); return;
        }
        if (Perintah == 184 && Word_SMS(pemilik_VALUE, "java/lang/Integer") && Word_SMS(Nama, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Perintah == 182 && Word_SMS(pemilik_VALUE, "java/io/PrintStream") && (Word_SMS(Nama, "println") || Word_SMS(Nama, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(Nama, "println")) kegagalan_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) kegagalan_VALUE("invalid PrintStream receiver");
            if (RALAT) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) ruang_pengguna.Tulis(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) ruang_pengguna.tulis_aksara_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) tulis_SMS(VALUE);
            if (Word_SMS(Nama, "println")) ruang_pengguna.tulis_aksara_VALUE(10);
            return;
        }
        if (Perintah == 182 && Word_SMS(pemilik_VALUE, "java/lang/String")) {
            if (Word_SMS(Nama, "length") && Word_SMS(format_VALUE, "()I")) {
                int Rujukan = 빼기(2); if (objek_VALUE(Rujukan, 1)) 넣기(timbunan_VALUE[Rujukan + 1], 1); return;
            }
            if (Word_SMS(Nama, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int subskrip_VALUE = 빼기(1), Rujukan = 빼기(2);
                if (objek_VALUE(Rujukan, 1)) {
                    if (subskrip_VALUE < 0 || subskrip_VALUE >= timbunan_VALUE[Rujukan + 1]) kegagalan_VALUE("StringIndexOutOfBoundsException"); else 넣기(timbunan_VALUE[Rujukan + 2 + subskrip_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(pemilik_VALUE, "java/lang/StringBuilder")) {
            if (Perintah == 183 && Word_SMS(Nama, "<init>") && Word_SMS(format_VALUE, "()V")) { objek_VALUE(빼기(2), 4); return; }
            if (Perintah == 182 && Word_SMS(Nama, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Rujukan = 빼기(2); if (objek_VALUE(Rujukan, 4)) 넣기(timbunan_VALUE[Rujukan + 2] == 0 ? hos_aksara("") : timbunan_VALUE[Rujukan + 2], 2); return;
            }
            if (Perintah == 182 && Word_SMS(Nama, "append")) {
                int Teks = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) Teks = digit_aksara(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) Teks = hos_aksara(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Teks = peruntuk_Storan(1, 1); if (!RALAT) timbunan_VALUE[Teks + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Teks = 빼기(2); if (Teks == 0) Teks = hos_aksara("null"); }
                else { kegagalan_VALUE("unsupported StringBuilder append"); return; }
                int Rujukan = 빼기(2); if (!objek_VALUE(Rujukan, 4) || !objek_VALUE(Teks, 1)) return;
                int hadapan_VALUE = timbunan_VALUE[Rujukan + 2], hadapan_VALUE_kepanjangan = hadapan_VALUE == 0 ? 0 : timbunan_VALUE[hadapan_VALUE + 1], BACK_VALUE_kepanjangan = timbunan_VALUE[Teks + 1];
                int 새글 = peruntuk_Storan(1, hadapan_VALUE_kepanjangan + BACK_VALUE_kepanjangan); if (RALAT) return;
                for (int 수 = 0; 수 < hadapan_VALUE_kepanjangan; 수++) timbunan_VALUE[새글 + 2 + 수] = timbunan_VALUE[hadapan_VALUE + 2 + 수];
                for (int 수 = 0; 수 < BACK_VALUE_kepanjangan; 수++) timbunan_VALUE[새글 + 2 + hadapan_VALUE_kepanjangan + 수] = timbunan_VALUE[Teks + 2 + 수];
                timbunan_VALUE[Rujukan + 2] = 새글; 넣기(Rujukan, 2); return;
            }
        }
        kegagalan_VALUE("unsupported library method");
    }
    static int 배열칸(int Rujukan, int subskrip_VALUE, int TYPE_VALUE) {
        if (!objek_VALUE(Rujukan, TYPE_VALUE)) return 0;
        if (subskrip_VALUE < 0 || subskrip_VALUE >= timbunan_VALUE[Rujukan + 1]) { kegagalan_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Rujukan + 2 + subskrip_VALUE;
    }
    static void laksanakan_perintah() {
        int 남음 = 500000;
        while (bingkai_INDEX >= 0 && !RALAT) {
            if (--남음 == 0) { kegagalan_VALUE("instruction limit (500000)"); break; }
            int Jalan = bingkai_jawatan[bingkai_INDEX], VALUE = 명바();
            if (RALAT) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= pemalar_COUNT) kegagalan_VALUE("invalid ldc constant");
                else if (pemalar_tag[수] == 3) 넣기(상가[수], 1);
                else if (pemalar_tag[수] == 8) 넣기(pemalar_SMS(상가[수]), 2);
                else kegagalan_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { tulis_setempat(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { tulis_setempat(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { tulis_setempat(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int subskrip_VALUE = 빼기(1), Rujukan = 빼기(2), 칸 = 배열칸(Rujukan, subskrip_VALUE, VALUE == 46 ? 2 : 3);
                if (!RALAT) 넣기(timbunan_VALUE[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int item_unsur = 빼기(VALUE == 79 ? 1 : 2), subskrip_VALUE = 빼기(1), Rujukan = 빼기(2), 칸 = 배열칸(Rujukan, subskrip_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && item_unsur != 0) objek_VALUE(item_unsur, 1);
                if (!RALAT) timbunan_VALUE[칸] = item_unsur; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = kembalikan_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = kembalikan_TYPE, 나 = 빼기(0), 나형 = kembalikan_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), ukuran = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { kegagalan_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) ukuran = 가 + 나;
                if (VALUE == 100) ukuran = 가 - 나;
                if (VALUE == 104) ukuran = 가 * 나;
                if (VALUE == 108) ukuran = 가 / 나;
                if (VALUE == 112) ukuran = 가 % 나;
                if (VALUE == 120) ukuran = 가 << 나;
                if (VALUE == 122) ukuran = 가 >> 나;
                if (VALUE == 124) ukuran = 가 >>> 나;
                if (VALUE == 126) ukuran = 가 & 나;
                if (VALUE == 128) ukuran = 가 | 나;
                if (VALUE == 130) ukuran = 가 ^ 나;
                넣기(ukuran, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int setempat_Skop = 명바(), tokokan_langkah = (byte)명바(); 지역읽기(setempat_Skop, 1); 넣기(빼기(1) + tokokan_langkah, 1); tulis_setempat(setempat_Skop, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int destinasi_VALUE = Jalan + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) alih_VALUE(destinasi_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { kembalikan_ukuran(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!cek_pemalar(수, 9)) continue;
                if (!Word_SMS(nama_kelas_SMS(상가[수]), "java/lang/System") || !Word_SMS(Rujukan_nama(pemalar_SECOND_VALUE[수]), "out")
                    || !Word_SMS(jenis_rujukan(pemalar_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) kegagalan_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_kaedah(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Nama = nama_kelas_SMS(명짧());
                if (Word_SMS(Nama, "java/lang/StringBuilder")) 넣기(peruntuk_Storan(4, 1), 2);
                else if (Word_SMS(Nama, "java/io/FileInputStream") || Word_SMS(Nama, "java/io/FileOutputStream")) {
                    int Rujukan = peruntuk_Storan(Word_SMS(Nama, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!RALAT) { timbunan_VALUE[Rujukan + 2] = -1; 넣기(Rujukan, 2); }
                } else kegagalan_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) kegagalan_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(nama_kelas_SMS(명짧()), "java/lang/String")) kegagalan_VALUE("only String[] anewarray is supported");
                int kepanjangan_VALUE = 빼기(1); 넣기(peruntuk_Storan(VALUE == 188 ? 2 : 3, kepanjangan_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Rujukan = 빼기(2);
                if (Rujukan < 1 || Rujukan >= timbunan_tamat_jawatan - 1 || (timbunan_VALUE[Rujukan] != 2 && timbunan_VALUE[Rujukan] != 3)) kegagalan_VALUE("null or invalid array");
                else 넣기(timbunan_VALUE[Rujukan + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Nama = nama_kelas_SMS(명짧()), Rujukan = 빼기(2);
                if (!Word_SMS(Nama, "java/lang/String")) kegagalan_VALUE("unsupported checkcast");
                else if (Rujukan != 0) objek_VALUE(Rujukan, 1);
                넣기(Rujukan, 2); continue;
            }
            kegagalan_VALUE("unsupported bytecode");
        }
    }
    public static int Jalan() {
        if (ruang_pengguna.인수개수() == 1 && 자바도구.같음(ruang_pengguna.인수(0), "-version")) {
            ruang_pengguna.Tulis("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (ruang_pengguna.인수개수() < 1) { ruang_pengguna.Tulis("Usage: java CLASS [ARGS]\n"); return 2; }
        int kepanjangan_VALUE = 자바도구.Nama(nama_fail_SMS, ruang_pengguna.인수(0));
        if (kepanjangan_VALUE < 1 || kepanjangan_VALUE > 57) { ruang_pengguna.Tulis("java: invalid class name\n"); return 2; }
        nama_fail_SMS[kepanjangan_VALUE] = '.'; nama_fail_SMS[kepanjangan_VALUE + 1] = 'c'; nama_fail_SMS[kepanjangan_VALUE + 2] = 'l'; nama_fail_SMS[kepanjangan_VALUE + 3] = 'a'; nama_fail_SMS[kepanjangan_VALUE + 4] = 's'; nama_fail_SMS[kepanjangan_VALUE + 5] = 's';
        Saiz = ruang_pengguna.파일읽기(nama_fail_SMS, Fail);
        if (Saiz < 0) { ruang_pengguna.Tulis("java: cannot read class: "); 자바도구.수쓰기(Saiz); ruang_pengguna.tulis_aksara_VALUE(10); return 1; }
        클래스읽기(); if (RALAT) return 1;
        int aksara_nama = pemalar_SMS(nama_kelas);
        if (!RALAT && timbunan_VALUE[aksara_nama + 1] != kepanjangan_VALUE) kegagalan_VALUE("class name does not match file");
        for (int 수 = 0; 수 < kepanjangan_VALUE && !RALAT; 수++) if (timbunan_VALUE[aksara_nama + 2 + 수] != nama_fail_SMS[수]) kegagalan_VALUE("class name does not match file");
        int titik_permulaan_VALUE = -1;
        for (int 수 = 0; 수 < kaedah_COUNT; 수++) if (Word_SMS(kaedah_nama_SMS[수], "main") && Word_SMS(kaedah_TYPE[수], "([Ljava/lang/String;)V") && (kaedah_capai[수] & 9) == 9) titik_permulaan_VALUE = 수;
        if (titik_permulaan_VALUE < 0) kegagalan_VALUE("public static void main(String[] args) required");
        if (RALAT) return 1;
        int 인수 = peruntuk_Storan(3, ruang_pengguna.인수개수() - 1);
        for (int 수 = 1; 수 < ruang_pengguna.인수개수() && !RALAT; 수++) timbunan_VALUE[인수 + 1 + 수] = hos_aksara(ruang_pengguna.인수(수));
        bingkai_INDEX = 0; bingkai_kaedah[0] = titik_permulaan_VALUE; bingkai_jawatan[0] = kaedah_Mula[titik_permulaan_VALUE]; setempat_VALUE[0] = 인수; setempat_TYPE[0] = 2;
        laksanakan_perintah(); return RALAT ? 1 : 0;
    }
}
