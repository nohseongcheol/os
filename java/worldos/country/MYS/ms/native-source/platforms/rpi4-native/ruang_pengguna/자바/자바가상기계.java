// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fail/스택/Rujukan/cabang 경계를 laksanakan_perintah 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fail = new int[16 * 16384], 임시파일 = new int[16384], nama_fail_SMS = new int[512];
    static int[] pemalar_tag = new int[8192], 상가 = new int[8192], pemalar_SECOND_VALUE = new int[8192], rentetan_Rujukan = new int[8192];
    static int[] kaedah_nama_SMS = new int[512], kaedah_TYPE = new int[512], kaedah_capai = new int[512], kaedah_pemilik = new int[512];
    static int[] kaedah_Mula = new int[512], kaedah_tamat = new int[512], kaedah_tindan = new int[512], 함수지역 = new int[512];
    static int[] kaedah_argumen_COUNT = new int[512], kaedah_argumen_TYPE = new int[8192], kaedah_kembalikan = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] setempat_VALUE = new int[16384], setempat_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] bingkai_kaedah = new int[128], bingkai_jawatan = new int[128], bingkai_tindan = new int[128], bingkai_suruhan = new int[128], mengasal_bingkai = new int[128];
    static int[] Kelas_Takrif_nama = new int[16], Kelas_Takrif_saiz = new int[16], 종부모 = new int[16], Kelas_Takrif_status = new int[16], 종칸수 = new int[16], mengasal_Kelas_Takrif = new int[16];
    static int[] Kelas_antara_muka = new int[16 * 16], Kelas_antara_muka_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] timbunan_VALUE = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], timbunan_Rujukan = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_unsur = new int[32768], stor_integer = new int[256];
    static int Saiz, 읽기위치, kaedah_COUNT, nama_kelas, bingkai_INDEX = -1, timbunan_tamat_jawatan = 1, kembalikan_TYPE;
    static int Kelas_Takrif_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, papar_COUNT, Koleksi_COUNT;
    static int 현재가닥, urutan_COUNT = 1, pemasukan_Kelas_Takrif;
    static int[] urutan_bingkai = new int[4], urutan_status = new int[4], urutan_objek = new int[4], urutan_sasaran = new int[4], 가닥대기 = new int[4];
    static boolean RALAT, ubah_permintaan;
    static int[] kunci_pemilik = new int[32768], 잠금깊이 = new int[32768], bingkai_kunci = new int[128], Kelas_kunci = new int[16], Kelas_urutan = new int[16];

    static void kegagalan_VALUE(String Word_SMS) {
        if (RALAT) return;
        int bidang_kod = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) bidang_kod = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) bidang_kod = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) bidang_kod = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) bidang_kod = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) bidang_kod = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) bidang_kod = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) bidang_kod = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) bidang_kod = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) bidang_kod = 15;
        if (bidang_kod != 0 && bingkai_INDEX >= 0) { 예외던짐(bidang_kod, Word_SMS); return; }
        ruang_pengguna.Tulis("JVM error: "); ruang_pengguna.Tulis(Word_SMS); ruang_pengguna.tulis_aksara_VALUE(10); RALAT = true;
    }
    static boolean klip(int Jalan, int kepanjangan_VALUE) {
        if (Jalan < 0 || Jalan >= Fail.length || kepanjangan_VALUE < 0) return false;
        int Kelas_Takrif = Jalan / 16384;
        return Jalan % 16384 <= Kelas_Takrif_saiz[Kelas_Takrif] && kepanjangan_VALUE <= Kelas_Takrif_saiz[Kelas_Takrif] - Jalan % 16384;
    }
    static int bait_VALUE() {
        if (!klip(읽기위치, 1)) { kegagalan_VALUE("truncated class file"); return 0; }
        return Fail[읽기위치++];
    }
    static int 짧은수() { return bait_VALUE() << 8 | bait_VALUE(); }
    static int integer() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int kepanjangan_VALUE) { if (!klip(읽기위치, kepanjangan_VALUE)) kegagalan_VALUE("invalid attribute size"); else 읽기위치 += kepanjangan_VALUE; }
    static boolean cek_pemalar(int 수, int 종류) {
        if (수 <= 0 || 수 >= pemalar_tag.length || pemalar_tag[수] != 종류) { kegagalan_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_julat(int Jalan, int kepanjangan_VALUE, String Word_SMS) {
        if (!klip(Jalan, kepanjangan_VALUE)) return false;
        int 읽는자리 = Jalan, 끝 = Jalan + kepanjangan_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int titik_kod = Word_SMS.charAt(Loop_INDEX);
            if (titik_kod > 0 && titik_kod < 128) { if (읽는자리 >= 끝 || Fail[읽는자리++] != titik_kod) return false; }
            else if (titik_kod < 2048) {
                if (읽는자리 + 2 > 끝 || Fail[읽는자리++] != (192 | (titik_kod >> 6)) || Fail[읽는자리++] != (128 | (titik_kod & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fail[읽는자리++] != (224 | (titik_kod >> 12)) || Fail[읽는자리++] != (128 | ((titik_kod >> 6) & 63)) || Fail[읽는자리++] != (128 | (titik_kod & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return kaedah_pemilik[bingkai_kaedah[bingkai_INDEX]] * 512 + 명짧(); }
    static void langkau_atribut() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !RALAT; 수++) { cek_pemalar(상번호(), 1); 건너(integer()); }
    }
    static int perintah_kepanjangan(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 193 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE == 185 || VALUE == 200) return 5;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE >= 50 && VALUE <= 53
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE >= 83 && VALUE <= 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190 || VALUE == 191
            || VALUE == 194 || VALUE == 195) return 1;
        return 0;
    }
    static int jawatan_integer(int 읽는자리) {
        if (!klip(읽는자리, 4)) { kegagalan_VALUE("truncated bytecode operand"); return 0; }
        return Fail[읽는자리] << 24 | Fail[읽는자리 + 1] << 16 | Fail[읽는자리 + 2] << 8 | Fail[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Jalan, int 끝) {
        int VALUE = Fail[읽는자리], kepanjangan_VALUE = perintah_kepanjangan(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_jawatan = 읽는자리 + 1;
            while ((BASE_jawatan - Jalan) % 4 != 0) BASE_jawatan++;
            if (끝 - BASE_jawatan < (VALUE == 170 ? 12 : 8)) return 0;
            int pemasukan_COUNT = VALUE == 170 ? jawatan_integer(BASE_jawatan + 8) - jawatan_integer(BASE_jawatan + 4) + 1 : jawatan_integer(BASE_jawatan + 4);
            if (pemasukan_COUNT < 0 || pemasukan_COUNT > 2048) return 0;
            kepanjangan_VALUE = BASE_jawatan - 읽는자리 + (VALUE == 170 ? 12 + 4 * pemasukan_COUNT : 8 + 8 * pemasukan_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_data = Fail[읽는자리 + 1]; kepanjangan_VALUE = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return kepanjangan_VALUE > 0 && kepanjangan_VALUE <= 끝 - 읽는자리 ? kepanjangan_VALUE : 0;
    }
    static void cek_destinasi_VALUE(int destinasi_VALUE, int fungsi_VALUE) {
        if (destinasi_VALUE < kaedah_Mula[fungsi_VALUE] || destinasi_VALUE >= kaedah_tamat[fungsi_VALUE] || 경계[destinasi_VALUE] != fungsi_VALUE + 1) kegagalan_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Kelas_Takrif) {
        현재읽는종 = Kelas_Takrif; 읽기위치 = Kelas_Takrif * 16384; Saiz = 읽기위치 + Kelas_Takrif_saiz[Kelas_Takrif];
        if (integer() != 0xcafebabe) { kegagalan_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versi_VALUE = 짧은수();
        if (versi_VALUE < 45 || versi_VALUE > 52 || 부판 != 0) { kegagalan_VALUE("supported class versions: 45..52, minor 0"); return; }
        int pemalar_COUNT = 짧은수(), BASE_jawatan = Kelas_Takrif * 512;
        if (pemalar_COUNT < 1 || pemalar_COUNT > 512) { kegagalan_VALUE("constant pool limit (511)"); return; }
        for (int pemasukan_COUNT = 1; pemasukan_COUNT < pemalar_COUNT && !RALAT; pemasukan_COUNT++) {
            int 수 = BASE_jawatan + pemasukan_COUNT, 종류 = bait_VALUE(); pemalar_tag[수] = 종류;
            if (종류 == 1) { pemalar_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(pemalar_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = integer();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); pemalar_SECOND_VALUE[수] = 상번호(); }
            else kegagalan_VALUE("unsupported constant type");
        }
        int keizinan_VALUE = 짧은수();
        if ((keizinan_VALUE & (0x2000 | 0x4000)) != 0) kegagalan_VALUE("annotation/enum class unsupported");
        Kelas_Takrif_nama[Kelas_Takrif] = nama_kelas_SMS(상번호());
        종부모[Kelas_Takrif] = nama_kelas_SMS(상번호());
        int antara_muka_COUNT = 짧은수(); if (antara_muka_COUNT > 16) { kegagalan_VALUE("interface count limit"); return; }
        Kelas_antara_muka_COUNT[Kelas_Takrif] = antara_muka_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < antara_muka_COUNT; Loop_INDEX++) Kelas_antara_muka[Kelas_Takrif * 16 + Loop_INDEX] = nama_kelas_SMS(상번호());
        int medan_COUNT = 짧은수();
        if (medan_COUNT > 512 - 칸수) { kegagalan_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < medan_COUNT && !RALAT; Loop_INDEX++) {
            int fail_INDEX = 칸수++; 칸주인[fail_INDEX] = Kelas_Takrif; 칸권한[fail_INDEX] = 짧은수(); 칸이름[fail_INDEX] = 상번호(); 칸형[fail_INDEX] = 상번호();
            cek_pemalar(칸이름[fail_INDEX], 1); cek_pemalar(칸형[fail_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[fail_INDEX]]; int bidang_kod = 서술형(읽기위치 + pemalar_SECOND_VALUE[칸형[fail_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[fail_INDEX] & 8) == 0) 칸위치[fail_INDEX] = 종칸수[Kelas_Takrif]++;
            int atribut_data = 짧은수();
            for (int dalaman_jawatan = 0; dalaman_jawatan < atribut_data && !RALAT; dalaman_jawatan++) {
                int nama_pemalar = 상번호(), sah_kepanjangan = integer();
                if (Word_SMS(nama_pemalar, "ConstantValue") && sah_kepanjangan == 2) {
                    int data_VALUE = 상번호();
                    if (bidang_kod == 1 && cek_pemalar(data_VALUE, 3)) 칸값[fail_INDEX] = 상가[data_VALUE];
                    else if (bidang_kod == 2 && cek_pemalar(data_VALUE, 8)) 칸값[fail_INDEX] = pemalar_SMS(상가[data_VALUE]);
                } else 건너(sah_kepanjangan);
            }
        }
        int item_COUNT = 짧은수();
        if (item_COUNT > 512 - kaedah_COUNT) { kegagalan_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < item_COUNT && !RALAT; Loop_INDEX++) {
            int 수 = kaedah_COUNT++; kaedah_pemilik[수] = Kelas_Takrif;
            kaedah_capai[수] = 짧은수(); kaedah_nama_SMS[수] = 상번호(); kaedah_TYPE[수] = 상번호();
            cek_pemalar(kaedah_nama_SMS[수], 1); 서술읽기(수);
            if ((kaedah_capai[수] & 8) == 0) {
                if (kaedah_argumen_COUNT[수] == 16) { kegagalan_VALUE("too many instance method arguments"); return; }
                for (int Perbandingan_jawatan = kaedah_argumen_COUNT[수]; Perbandingan_jawatan > 0; Perbandingan_jawatan--) kaedah_argumen_TYPE[수 * 16 + Perbandingan_jawatan] = kaedah_argumen_TYPE[수 * 16 + Perbandingan_jawatan - 1];
                kaedah_argumen_TYPE[수 * 16] = 2; kaedah_argumen_COUNT[수]++;
            }
            if ((kaedah_capai[수] & 0x100) != 0) kegagalan_VALUE("user native method unsupported");
            if (Word_SMS(kaedah_nama_SMS[수], "<clinit>")) mengasal_Kelas_Takrif[Kelas_Takrif] = 수 + 1;
            for (int hadapan_VALUE = 0; hadapan_VALUE < 수; hadapan_VALUE++) if (kaedah_pemilik[hadapan_VALUE] == Kelas_Takrif && 같은말(kaedah_nama_SMS[hadapan_VALUE], kaedah_nama_SMS[수]) && 같은말(kaedah_TYPE[hadapan_VALUE], kaedah_TYPE[수])) kegagalan_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !RALAT; atribut_VALUE++) {
                int Nama = 상번호(), kepanjangan_VALUE = integer(), Jalan = 읽기위치;
                if (!klip(Jalan, kepanjangan_VALUE)) { kegagalan_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nama, "Code")) {
                    if (kaedah_Mula[수] != 0) kegagalan_VALUE("duplicate Code attribute");
                    kaedah_tindan[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_kepanjangan = integer();
                    if (kaedah_tindan[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < kaedah_argumen_COUNT[수]
                        || kod_kepanjangan < 1 || kod_kepanjangan > 8192) kegagalan_VALUE("method memory limits exceeded");
                    kaedah_Mula[수] = 읽기위치; 건너(kod_kepanjangan); kaedah_tamat[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { kegagalan_VALUE("exception table limit"); return; }
                    for (int dalaman_jawatan = 0; dalaman_jawatan < 잡는수; dalaman_jawatan++) {
                        int ralat_Rujukan = 잡기수++; 잡기함수[ralat_Rujukan] = 수;
                        잡기시작[ralat_Rujukan] = kaedah_Mula[수] + 짧은수(); 잡기끝[ralat_Rujukan] = kaedah_Mula[수] + 짧은수();
                        잡기위치[ralat_Rujukan] = kaedah_Mula[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[ralat_Rujukan] = 부호값 == 0 ? 0 : nama_kelas_SMS(부호값);
                    }
                    langkau_atribut();
                    if (읽기위치 != Jalan + kepanjangan_VALUE) kegagalan_VALUE("Code attribute size mismatch");
                } else 건너(kepanjangan_VALUE);
            }
            if ((kaedah_capai[수] & 0x400) != 0) continue;
            if (kaedah_Mula[수] == 0) kegagalan_VALUE("missing Code attribute");
            int 칸 = kaedah_Mula[수];
            while (칸 < kaedah_tamat[수] && !RALAT) {
                int kepanjangan_VALUE = 길이읽기(칸, kaedah_Mula[수], kaedah_tamat[수]);
                if (kepanjangan_VALUE == 0) { kegagalan_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += kepanjangan_VALUE;
            }
            칸 = kaedah_Mula[수];
            while (칸 < kaedah_tamat[수] && !RALAT) {
                int VALUE = Fail[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) cek_destinasi_VALUE(칸 + (short)(Fail[칸 + 1] << 8 | Fail[칸 + 2]), 수);
                if (VALUE == 200) cek_destinasi_VALUE(칸 + jawatan_integer(칸 + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - kaedah_Mula[수]) % 4 != 0) 읽는자리++;
                    cek_destinasi_VALUE(칸 + jawatan_integer(읽는자리), 수);
                    int pemasukan_COUNT = VALUE == 170 ? jawatan_integer(읽는자리 + 8) - jawatan_integer(읽는자리 + 4) + 1 : jawatan_integer(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int dalaman_jawatan = 0; dalaman_jawatan < pemasukan_COUNT; dalaman_jawatan++) cek_destinasi_VALUE(칸 + jawatan_integer(읽는자리 + dalaman_jawatan * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, kaedah_Mula[수], kaedah_tamat[수]);
            }
            for (int dalaman_jawatan = 0; dalaman_jawatan < 잡기수; dalaman_jawatan++) if (잡기함수[dalaman_jawatan] == 수) {
                cek_destinasi_VALUE(잡기시작[dalaman_jawatan], 수); cek_destinasi_VALUE(잡기위치[dalaman_jawatan], 수);
                if (잡기끝[dalaman_jawatan] != kaedah_tamat[수]) cek_destinasi_VALUE(잡기끝[dalaman_jawatan], 수);
                if (잡기시작[dalaman_jawatan] >= 잡기끝[dalaman_jawatan]) kegagalan_VALUE("invalid exception range");
            }
        }
        if (!RALAT) langkau_atribut();
        if (읽기위치 != Saiz) kegagalan_VALUE("extra class file data");
    }
    static int peruntuk_Storan(int 종류, int kepanjangan_VALUE) { return 새기억(종류, kepanjangan_VALUE); }
    static boolean objek_VALUE(int Rujukan, int 종류) {
        if (!teknologi_maklumat_sah_objek(Rujukan)) return false;
        if (timbunan_VALUE[Rujukan] != 종류) { kegagalan_VALUE("object type mismatch"); return false; }
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
        if (kembalikan_TYPE == 2) lindung_VALUE(스택값[칸]);
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
        if (bingkai_INDEX % 32 == 31) { kegagalan_VALUE("call stack limit (32)"); return; }
        int Seterusnya_item = bingkai_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) setempat_TYPE[Seterusnya_item * 128 + 수] = 0;
        for (int 수 = kaedah_argumen_COUNT[fungsi_VALUE] - 1; 수 >= 0; 수--) {
            setempat_VALUE[Seterusnya_item * 128 + 수] = 빼기(kaedah_argumen_TYPE[fungsi_VALUE * 16 + 수]); setempat_TYPE[Seterusnya_item * 128 + 수] = kaedah_argumen_TYPE[fungsi_VALUE * 16 + 수];
        }
        if (RALAT) return;
        bingkai_INDEX = Seterusnya_item; mengasal_bingkai[bingkai_INDEX] = 0; bingkai_kaedah[bingkai_INDEX] = fungsi_VALUE; bingkai_jawatan[bingkai_INDEX] = kaedah_Mula[fungsi_VALUE]; bingkai_tindan[bingkai_INDEX] = 0;
    }
    static void kembalikan_ukuran(int TYPE_VALUE) {
        if (TYPE_VALUE != kaedah_kembalikan[bingkai_kaedah[bingkai_INDEX]]) { kegagalan_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (mengasal_bingkai[bingkai_INDEX] != 0) Kelas_Takrif_status[mengasal_bingkai[bingkai_INDEX] - 1] = 2;
        if (bingkai_kunci[bingkai_INDEX] != 0) { keluaran_kunci(bingkai_kunci[bingkai_INDEX]); bingkai_kunci[bingkai_INDEX] = 0; }
        bingkai_INDEX--; if (bingkai_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1) { kegagalan_VALUE("invalid file stream path"); return; }
                strim_nama_fail[칸] = VALUE;
            }
            strim_nama_fail[kepanjangan_VALUE] = 0;
            int 서술자 = ruang_pengguna.파일서술자열기(strim_nama_fail, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kegagalan_VALUE("FileNotFoundException: file open failed"); return; }
            timbunan_VALUE[strim_VALUE + 2] = 서술자; timbunan_VALUE[strim_VALUE + 3] = 1;
            return;
        }
        if (Perintah != 182) { kegagalan_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(Nama, "write") || !출력 && Word_SMS(Nama, "read"))
            && (Word_SMS(format_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean klip_VALUE = Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int pemasukan_COUNT = klip_VALUE ? 빼기(1) : 0, 시작점 = klip_VALUE ? 빼기(1) : 0, data_ARRAY = 빼기(2), objek_Rujukan = 빼기(2);
            if (!objek_VALUE(data_ARRAY, 20) || !objek_VALUE(objek_Rujukan, 종류)) return;
            if (!klip_VALUE) pemasukan_COUNT = timbunan_VALUE[data_ARRAY + 1];
            if (시작점 < 0 || pemasukan_COUNT < 0 || 시작점 > timbunan_VALUE[data_ARRAY + 1] - pemasukan_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (timbunan_VALUE[objek_Rujukan + 3] == 0 || timbunan_VALUE[objek_Rujukan + 2] < 0) { kegagalan_VALUE("IOException: stream closed"); return; }
            int Selesai_COUNT = 0;
            while (Selesai_COUNT < pemasukan_COUNT && !RALAT) {
                int 반환값 = 출력 ? ruang_pengguna.파일한바이트쓰기(timbunan_VALUE[objek_Rujukan + 2], timbunan_VALUE[data_ARRAY + 2 + 시작점 + Selesai_COUNT]) : ruang_pengguna.파일한바이트읽기(timbunan_VALUE[objek_Rujukan + 2]);
                if (반환값 < 0) { kegagalan_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) timbunan_VALUE[data_ARRAY + 2 + 시작점 + Selesai_COUNT] = (byte)반환값;
                Selesai_COUNT++;
            }
            if (!출력) 넣기(pemasukan_COUNT != 0 && Selesai_COUNT == 0 ? -1 : Selesai_COUNT, 1);
            return;
        }
        if (출력 && Word_SMS(Nama, "flush") && Word_SMS(format_VALUE, "()V")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 종류) && timbunan_VALUE[objek_Rujukan + 2] < 0) kegagalan_VALUE("IOException: stream closed"); return; }
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
            if (ukuran < -1) kegagalan_VALUE("IOException: read failed"); else 넣기(ukuran == 256 ? -1 : ukuran, 1);
        } else if (ruang_pengguna.파일한바이트쓰기(서술자, VALUE) != 1) kegagalan_VALUE("IOException: write failed");
    }
    static void CALL_kaedah(int INDEX, int Perintah) {
        if (INDEX <= 0 || INDEX >= pemalar_tag.length || (pemalar_tag[INDEX] != 10 && pemalar_tag[INDEX] != 11)) { kegagalan_VALUE("invalid method reference"); return; }
        int pemilik_VALUE = nama_kelas_SMS(상가[INDEX]), Nama = Rujukan_nama(pemalar_SECOND_VALUE[INDEX]), format_VALUE = jenis_rujukan(pemalar_SECOND_VALUE[INDEX]);
        if (RALAT) return;
        if (기본호출(pemilik_VALUE, Nama, format_VALUE, Perintah)) return;
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
        int Kelas_Takrif = Cari_Kelas_Takrif(pemilik_VALUE); if (Kelas_Takrif < 0 || RALAT) return;
        int fail_INDEX = Cari_kaedah(Kelas_Takrif, Nama, format_VALUE);
        if (fail_INDEX < 0) {
            for (int titik_kod = Kelas_Takrif, pemasukan_COUNT = 0; titik_kod >= 0 && pemasukan_COUNT < 16; pemasukan_COUNT++, titik_kod = 부모종(titik_kod))
                if (Word_SMS(종부모[titik_kod], "java/lang/Thread")) { 가닥호출(Nama, format_VALUE, Perintah); return; }
            kegagalan_VALUE("NoSuchMethodError"); return;
        }
        if (((kaedah_capai[fail_INDEX] & 8) != 0) != (Perintah == 184)) { kegagalan_VALUE("method static/instance mismatch"); return; }
        if (Perintah == 184) { if (!mengasal(kaedah_pemilik[fail_INDEX], bingkai_suruhan[bingkai_INDEX])) return; }
        else {
            int 읽는자리 = bingkai_tindan[bingkai_INDEX] - kaedah_argumen_COUNT[fail_INDEX];
            if (읽는자리 < 0 || 스택형[bingkai_INDEX * 128 + 읽는자리] != 2) { kegagalan_VALUE("invalid method receiver"); return; }
            int objek_Rujukan = 스택값[bingkai_INDEX * 128 + 읽는자리];
            if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return;
            if (timbunan_VALUE[objek_Rujukan] < 32 || !종포함(timbunan_VALUE[objek_Rujukan] - 32, pemilik_VALUE)) { kegagalan_VALUE("method receiver type mismatch"); return; }
            if (Perintah != 183) fail_INDEX = Cari_kaedah(timbunan_VALUE[objek_Rujukan] - 32, Nama, format_VALUE);
        }
        if (fail_INDEX < 0 || (kaedah_capai[fail_INDEX] & 0x400) != 0) { kegagalan_VALUE("AbstractMethodError"); return; }
        int kunci_Rujukan = 0;
        if ((kaedah_capai[fail_INDEX] & 32) != 0) {
            if (Perintah == 184) { int titik_kod = kaedah_pemilik[fail_INDEX]; if (Kelas_kunci[titik_kod] == 0) Kelas_kunci[titik_kod] = peruntuk_Storan(8, 0); kunci_Rujukan = Kelas_kunci[titik_kod]; }
            else kunci_Rujukan = 스택값[bingkai_INDEX * 128 + bingkai_tindan[bingkai_INDEX] - kaedah_argumen_COUNT[fail_INDEX]];
            if (!잠금얻기(kunci_Rujukan)) { if (!RALAT) bingkai_jawatan[bingkai_INDEX] = bingkai_suruhan[bingkai_INDEX]; return; }
        }
        호출(fail_INDEX); if (!RALAT) bingkai_kunci[bingkai_INDEX] = kunci_Rujukan;
    }
    static boolean 배열저장가능(int ARRAY_Rujukan, int data_VALUE) {
        if (data_VALUE == 0 || ARRAY_unsur[ARRAY_Rujukan] == 0) return true;
        boolean 성공여부 = ARRAY_unsur[ARRAY_Rujukan] == -1 ? (data_VALUE > 0 && data_VALUE < timbunan_tamat_jawatan && timbunan_VALUE[data_VALUE] == 1) : 맞는객체(data_VALUE, ARRAY_unsur[ARRAY_Rujukan]);
        if (!성공여부 && !RALAT) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int Rujukan, int subskrip_VALUE, int TYPE_VALUE) {
        if (!objek_VALUE(Rujukan, TYPE_VALUE)) return 0;
        if (subskrip_VALUE < 0 || subskrip_VALUE >= timbunan_VALUE[Rujukan + 1]) { kegagalan_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Rujukan + 2 + subskrip_VALUE;
    }
    static void laksanakan_perintah() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (RALAT) { if (던진객체 != 0) pemegang_pengecualian(); if (RALAT || bingkai_INDEX < 현재가닥 * 32) break; }
            if (bingkai_INDEX < 현재가닥 * 32 || ubah_permintaan || --조각 == 0) { if (!tukar_urutan()) break; 조각 = 100; }
            if (bingkai_INDEX == 0 && Kelas_Takrif_status[pemasukan_Kelas_Takrif] != 2 && !mengasal(pemasukan_Kelas_Takrif, bingkai_jawatan[bingkai_INDEX])) continue;
            if (bingkai_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (kaedah_capai[bingkai_kaedah[bingkai_INDEX]] & 32) != 0 && bingkai_kunci[bingkai_INDEX] == 0) {
                int objek_Rujukan = urutan_sasaran[현재가닥]; if (!잠금얻기(objek_Rujukan)) { if (RALAT) break; continue; } bingkai_kunci[bingkai_INDEX] = objek_Rujukan;
            }
            잠시수 = 0;
            if (--남음 == 0) { kegagalan_VALUE("instruction limit (500000)"); break; }
            int Jalan = bingkai_jawatan[bingkai_INDEX]; bingkai_suruhan[bingkai_INDEX] = Jalan; int VALUE = 명바();
            if (RALAT) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = kaedah_pemilik[bingkai_kaedah[bingkai_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= pemalar_tag.length) kegagalan_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int pemasukan_jawatan = 빼기(1), objek_Rujukan = 빼기(2), bidang_kod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objek_Rujukan > 0 && objek_Rujukan < timbunan_tamat_jawatan && timbunan_VALUE[objek_Rujukan] == 21) bidang_kod = 21;
                int 읽는자리 = 배열칸(objek_Rujukan, pemasukan_jawatan, bidang_kod); if (!RALAT) 넣기(timbunan_VALUE[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int pemasukan_Rujukan = 빼기(VALUE == 83 ? 2 : 1), pemasukan_jawatan = 빼기(1), objek_Rujukan = 빼기(2), bidang_kod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objek_Rujukan > 0 && objek_Rujukan < timbunan_tamat_jawatan && timbunan_VALUE[objek_Rujukan] == 21) bidang_kod = 21;
                int 읽는자리 = 배열칸(objek_Rujukan, pemasukan_jawatan, bidang_kod);
                if (!RALAT && bidang_kod == 3 && !배열저장가능(objek_Rujukan, pemasukan_Rujukan)) continue;
                if (!RALAT) timbunan_VALUE[읽는자리] = bidang_kod == 20 ? (byte)pemasukan_Rujukan : bidang_kod == 21 ? pemasukan_Rujukan & 1 : bidang_kod == 22 ? (char)pemasukan_Rujukan : bidang_kod == 23 ? (short)pemasukan_Rujukan : pemasukan_Rujukan;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { tindan_suruhan(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Jalan); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { kegagalan_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_kaedah(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(nama_kelas_SMS(명상수()), Jalan); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int bidang_kod = 3, komponen = 0;
                if (VALUE == 188) { int 임시값 = 명바(); bidang_kod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponen = nama_kelas_SMS(명상수());
                if (bidang_kod == 0) { kegagalan_VALUE("unsupported primitive array type"); continue; }
                int sah_kepanjangan = 빼기(1), objek_Rujukan = peruntuk_Storan(bidang_kod, sah_kepanjangan); if (!RALAT) ARRAY_unsur[objek_Rujukan] = komponen; 넣기(objek_Rujukan, 2); continue;
            }
            if (VALUE == 190) {
                int objek_Rujukan = 빼기(2);
                if (teknologi_maklumat_sah_objek(objek_Rujukan)) { int Perbandingan_jawatan = timbunan_VALUE[objek_Rujukan]; if (Perbandingan_jawatan != 2 && Perbandingan_jawatan != 3 && (Perbandingan_jawatan < 20 || Perbandingan_jawatan > 23)) kegagalan_VALUE("not an array"); else 넣기(timbunan_VALUE[objek_Rujukan + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objek_Rujukan = 빼기(2); if (teknologi_maklumat_sah_objek(objek_Rujukan)) { if (timbunan_VALUE[objek_Rujukan] != 9) kegagalan_VALUE("athrow requires supported Throwable"); else { 던진객체 = objek_Rujukan; RALAT = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int nama_pemalar = nama_kelas_SMS(명상수()), objek_Rujukan = 빼기(2); boolean MATCH = 맞는객체(objek_Rujukan, nama_pemalar);
                if (VALUE == 193) 넣기(objek_Rujukan != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !RALAT) kegagalan_VALUE("ClassCastException"); 넣기(objek_Rujukan, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Jalan + 1, fail_INDEX = bingkai_kaedah[bingkai_INDEX], Kunci_Rujukan = 빼기(1);
                while ((읽는자리 - kaedah_Mula[fail_INDEX]) % 4 != 0) 읽는자리++;
                int sasaran_e_mel = jawatan_integer(읽는자리);
                if (VALUE == 170) { int 낮은값 = jawatan_integer(읽는자리 + 4), 높은값 = jawatan_integer(읽는자리 + 8); if (Kunci_Rujukan >= 낮은값 && Kunci_Rujukan <= 높은값) sasaran_e_mel = jawatan_integer(읽는자리 + 12 + (Kunci_Rujukan - 낮은값) * 4); }
                else { int 총수 = jawatan_integer(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (jawatan_integer(읽는자리 + 8 + Loop_INDEX * 8) == Kunci_Rujukan) sasaran_e_mel = jawatan_integer(읽는자리 + 12 + Loop_INDEX * 8); }
                alih_VALUE(Jalan + sasaran_e_mel); continue;
            }
            if (VALUE == 200) { alih_VALUE(Jalan + jawatan_integer(Jalan + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objek_Rujukan = 빼기(2);
                if (VALUE == 195) keluaran_kunci(objek_Rujukan);
                else if (!잠금얻기(objek_Rujukan) && !RALAT) { 넣기(objek_Rujukan, 2); bingkai_jawatan[bingkai_INDEX] = Jalan; }
                continue;
            }
            if (VALUE == 196) {
                int perintah_kod = 명바(), pemasukan_jawatan = 명짧();
                if (perintah_kod == 21 || perintah_kod == 25) 지역읽기(pemasukan_jawatan, perintah_kod == 21 ? 1 : 2);
                else if (perintah_kod == 54 || perintah_kod == 58) tulis_setempat(pemasukan_jawatan, perintah_kod == 54 ? 1 : 2);
                else if (perintah_kod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(pemasukan_jawatan, 1); 넣기(빼기(1) + DELTA_VALUE, 1); tulis_setempat(pemasukan_jawatan, 1); }
                else kegagalan_VALUE("unsupported wide opcode");
                continue;
            }
            kegagalan_VALUE("unsupported bytecode");
        }
    }
    static int Cari_Kelas_Takrif(int Nama) {
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Takrif_COUNT; Loop_INDEX++) if (Kelas_Takrif_nama[Loop_INDEX] != 0 && 같은말(Kelas_Takrif_nama[Loop_INDEX], Nama)) return Loop_INDEX;
        return muat_Kelas_Takrif(pemalar_SMS(Nama));
    }
    static int muat_Kelas_Takrif(int nama_rentetan) {
        if (!objek_VALUE(nama_rentetan, 1)) return -1;
        int kepanjangan_VALUE = timbunan_VALUE[nama_rentetan + 1];
        if (kepanjangan_VALUE < 1 || kepanjangan_VALUE > 505 || Kelas_Takrif_COUNT == 16) { kegagalan_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < kepanjangan_VALUE; Loop_INDEX++) { int titik_kod = timbunan_VALUE[nama_rentetan + 2 + Loop_INDEX]; nama_fail_SMS[Loop_INDEX] = titik_kod == '/' ? '.' : titik_kod; }
        nama_fail_SMS[kepanjangan_VALUE] = '.'; nama_fail_SMS[kepanjangan_VALUE + 1] = 'c'; nama_fail_SMS[kepanjangan_VALUE + 2] = 'l'; nama_fail_SMS[kepanjangan_VALUE + 3] = 'a'; nama_fail_SMS[kepanjangan_VALUE + 4] = 's'; nama_fail_SMS[kepanjangan_VALUE + 5] = 's'; nama_fail_SMS[kepanjangan_VALUE + 6] = 0;
        int Saiz = ruang_pengguna.파일읽기(nama_fail_SMS, 임시파일);
        if (Saiz < 0) { kegagalan_VALUE("ClassNotFoundException"); return -1; }
        int Kelas_Takrif = Kelas_Takrif_COUNT++; Kelas_Takrif_saiz[Kelas_Takrif] = Saiz;
        for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) Fail[Kelas_Takrif * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(Kelas_Takrif); if (RALAT) return -1;
        int sebenar_data = pemalar_SMS(Kelas_Takrif_nama[Kelas_Takrif]);
        if (!teks_sama(sebenar_data, nama_rentetan, true)) { kegagalan_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[Kelas_Takrif];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = Cari_Kelas_Takrif(부모);
            if (RALAT || 위 < 0) return -1;
            int 읽는자리 = 위, pentas_COUNT = 0;
            while (읽는자리 >= 0 && pentas_COUNT++ < 16) {
                if (읽는자리 == Kelas_Takrif) { kegagalan_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int fail_INDEX = 0; fail_INDEX < 칸수; fail_INDEX++) if (칸주인[fail_INDEX] == Kelas_Takrif && (칸권한[fail_INDEX] & 8) == 0) 칸위치[fail_INDEX] += 시작변위;
            종칸수[Kelas_Takrif] += 시작변위;
        }
        return Kelas_Takrif;
    }
    static int 부모종(int Kelas_Takrif) {
        int Nama = 종부모[Kelas_Takrif];
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Takrif_COUNT; Loop_INDEX++) if (Nama != 0 && Kelas_Takrif_nama[Loop_INDEX] != 0 && 같은말(Kelas_Takrif_nama[Loop_INDEX], Nama)) return Loop_INDEX;
        return -1;
    }
    static int Cari_kaedah(int Kelas_Takrif, int Nama, int format_VALUE) {
        for (int 깊이 = 0; Kelas_Takrif >= 0 && 깊이 < 16; 깊이++, Kelas_Takrif = 부모종(Kelas_Takrif)) {
            for (int Loop_INDEX = 0; Loop_INDEX < kaedah_COUNT; Loop_INDEX++) if (kaedah_pemilik[Loop_INDEX] == Kelas_Takrif && 같은말(kaedah_nama_SMS[Loop_INDEX], Nama) && 같은말(kaedah_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int nama_kaedah(int Kelas_Takrif, String Nama, String format_VALUE) {
        for (int 깊이 = 0; Kelas_Takrif >= 0 && 깊이 < 16; 깊이++, Kelas_Takrif = 부모종(Kelas_Takrif))
            for (int Loop_INDEX = 0; Loop_INDEX < kaedah_COUNT; Loop_INDEX++) if (kaedah_pemilik[Loop_INDEX] == Kelas_Takrif && Word_SMS(kaedah_nama_SMS[Loop_INDEX], Nama) && Word_SMS(kaedah_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Nama) { return Fail[상가[Nama]] == 'L' || Fail[상가[Nama]] == '[' ? 2 : 1; }
    static boolean mengasal(int Kelas_Takrif, int perintah_Mula) {
        if (Kelas_Takrif < 0 || RALAT) return false;
        if (Kelas_Takrif_status[Kelas_Takrif] == 3) { kegagalan_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Kelas_Takrif_status[Kelas_Takrif] == 1 && Kelas_urutan[Kelas_Takrif] != 현재가닥) { bingkai_jawatan[bingkai_INDEX] = perintah_Mula; ubah_permintaan = true; return false; }
        if (Kelas_Takrif_status[Kelas_Takrif] != 0) return true;
        int 위 = 부모종(Kelas_Takrif);
        if (위 >= 0 && !mengasal(위, perintah_Mula)) return false;
        Kelas_Takrif_status[Kelas_Takrif] = 1; Kelas_urutan[Kelas_Takrif] = 현재가닥;
        if (mengasal_Kelas_Takrif[Kelas_Takrif] != 0) {
            bingkai_jawatan[bingkai_INDEX] = perintah_Mula;
            호출(mengasal_Kelas_Takrif[Kelas_Takrif] - 1); if (!RALAT) mengasal_bingkai[bingkai_INDEX] = Kelas_Takrif + 1;
            return false;
        }
        Kelas_Takrif_status[Kelas_Takrif] = 2; return true;
    }
    static void 필드호출(int INDEX, int Perintah, int Jalan) {
        if (!cek_pemalar(INDEX, 9)) return;
        int pemilik_VALUE = nama_kelas_SMS(상가[INDEX]), Nama = Rujukan_nama(pemalar_SECOND_VALUE[INDEX]), format_VALUE = jenis_rujukan(pemalar_SECOND_VALUE[INDEX]);
        if (Word_SMS(pemilik_VALUE, "java/lang/System") && (Word_SMS(Nama, "out") || Word_SMS(Nama, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && Perintah == 178) { 넣기(-1, 2); return; }
        int Kelas_Takrif = Cari_Kelas_Takrif(pemilik_VALUE); if (Kelas_Takrif < 0 || RALAT) return;
        int 찾음 = -1;
        for (int 읽는자리 = Kelas_Takrif, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int fail_INDEX = 0; fail_INDEX < 칸수; fail_INDEX++) if (칸주인[fail_INDEX] == 읽는자리 && 같은말(칸이름[fail_INDEX], Nama) && 같은말(칸형[fail_INDEX], format_VALUE)) 찾음 = fail_INDEX;
        if (찾음 < 0) { kegagalan_VALUE("NoSuchFieldError"); return; }
        boolean statik_VALUE = Perintah == 178 || Perintah == 179;
        if (statik_VALUE != ((칸권한[찾음] & 8) != 0)) { kegagalan_VALUE("field static/instance mismatch"); return; }
        if (statik_VALUE && !mengasal(칸주인[찾음], Jalan)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (Perintah == 179 || Perintah == 181) VALUE = 빼기(TYPE_VALUE);
        if (statik_VALUE) { if (Perintah == 178) 넣기(칸값[찾음], TYPE_VALUE); else if (!RALAT) 칸값[찾음] = VALUE; return; }
        int objek_Rujukan = 빼기(2);
        if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return;
        if (timbunan_VALUE[objek_Rujukan] < 32 || !종포함(timbunan_VALUE[objek_Rujukan] - 32, pemilik_VALUE)) { kegagalan_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objek_Rujukan + 2 + 칸위치[찾음];
        if (Perintah == 180) 넣기(timbunan_VALUE[보관칸], TYPE_VALUE);
        else if (!RALAT) { timbunan_VALUE[보관칸] = VALUE; timbunan_Rujukan[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Kelas_Takrif, int Nama) {
        for (int 중첩깊이 = 0; Kelas_Takrif >= 0 && 중첩깊이 < 16; 중첩깊이++, Kelas_Takrif = 부모종(Kelas_Takrif)) {
            if (같은말(Kelas_Takrif_nama[Kelas_Takrif], Nama) || (종부모[Kelas_Takrif] != 0 && 같은말(종부모[Kelas_Takrif], Nama))) return true;
            for (int dalaman_jawatan = 0; dalaman_jawatan < Kelas_antara_muka_COUNT[Kelas_Takrif]; dalaman_jawatan++) if (같은말(Kelas_antara_muka[Kelas_Takrif * 16 + dalaman_jawatan], Nama)) return true;
        }
        return false;
    }
    static boolean teks_sama(int 첫값, int bait_data, boolean LALUAN) {
        if (첫값 == bait_data) return true;
        if (첫값 <= 0 || bait_data <= 0 || timbunan_VALUE[첫값] != 1 || timbunan_VALUE[bait_data] != 1 || timbunan_VALUE[첫값 + 1] != timbunan_VALUE[bait_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < timbunan_VALUE[첫값 + 1]; Loop_INDEX++) {
            int koordinat_x = timbunan_VALUE[첫값 + 2 + Loop_INDEX], Y_koordinat = timbunan_VALUE[bait_data + 2 + Loop_INDEX];
            if (LALUAN) { if (koordinat_x == '.') koordinat_x = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (koordinat_x != Y_koordinat) return false;
        }
        return true;
    }
    static boolean teknologi_maklumat_sah_objek(int objek_Rujukan) {
        if (objek_Rujukan == 0) { kegagalan_VALUE("NullPointerException"); return false; }
        if (objek_Rujukan < 1 || objek_Rujukan >= timbunan_tamat_jawatan || 힙폭[objek_Rujukan] < 2 || timbunan_VALUE[objek_Rujukan] == 0) { kegagalan_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void lindung_VALUE(int objek_Rujukan) {
        if (objek_Rujukan > 0 && objek_Rujukan < timbunan_tamat_jawatan && 힙폭[objek_Rujukan] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objek_Rujukan;
    }
    static void tayang_VALUE(int objek_Rujukan) {
        if (objek_Rujukan > 0 && objek_Rujukan < timbunan_tamat_jawatan && 힙폭[objek_Rujukan] >= 2 && timbunan_VALUE[objek_Rujukan] != 0 && 힙표시[objek_Rujukan] == 0) {
            힙표시[objek_Rujukan] = 1; 표시대기[papar_COUNT++] = objek_Rujukan;
        }
    }
    static void 수거() {
        papar_COUNT = 0; Koleksi_COUNT++;
        for (int cek_jawatan = 1; cek_jawatan < timbunan_tamat_jawatan; cek_jawatan += 힙폭[cek_jawatan]) 힙표시[cek_jawatan] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < rentetan_Rujukan.length; Loop_INDEX++) tayang_VALUE(rentetan_Rujukan[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) tayang_VALUE(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < urutan_COUNT; 임시값++) {
            tayang_VALUE(urutan_objek[임시값]); tayang_VALUE(urutan_sasaran[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? bingkai_INDEX : urutan_bingkai[임시값];
            for (int fail_INDEX = 임시값 * 32; fail_INDEX <= 꼭대기자리; fail_INDEX++) {
                for (int dalaman_jawatan = 0; dalaman_jawatan < 함수지역[bingkai_kaedah[fail_INDEX]]; dalaman_jawatan++) if (setempat_TYPE[fail_INDEX * 128 + dalaman_jawatan] == 2) tayang_VALUE(setempat_VALUE[fail_INDEX * 128 + dalaman_jawatan]);
                for (int dalaman_jawatan = 0; dalaman_jawatan < bingkai_tindan[fail_INDEX]; dalaman_jawatan++) if (스택형[fail_INDEX * 128 + dalaman_jawatan] == 2) tayang_VALUE(스택값[fail_INDEX * 128 + dalaman_jawatan]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) tayang_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) tayang_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < stor_integer.length; Loop_INDEX++) tayang_VALUE(stor_integer[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Takrif_COUNT; Loop_INDEX++) tayang_VALUE(Kelas_kunci[Loop_INDEX]);
        for (int cek_jawatan = 1; cek_jawatan < timbunan_tamat_jawatan; cek_jawatan += 힙폭[cek_jawatan]) if (잠금깊이[cek_jawatan] > 0) tayang_VALUE(cek_jawatan);
        tayang_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) tayang_VALUE(잠시참조[Loop_INDEX]);
        while (papar_COUNT > 0) {
            int objek_Rujukan = 표시대기[--papar_COUNT], bidang_kod = timbunan_VALUE[objek_Rujukan];
            for (int Loop_INDEX = objek_Rujukan + 2; Loop_INDEX < objek_Rujukan + 힙폭[objek_Rujukan]; Loop_INDEX++) if (bidang_kod == 3 || bidang_kod == 4 || timbunan_Rujukan[Loop_INDEX] != 0) tayang_VALUE(timbunan_VALUE[Loop_INDEX]);
        }
        for (int cek_jawatan = 1; cek_jawatan < timbunan_tamat_jawatan; cek_jawatan += 힙폭[cek_jawatan]) if (힙표시[cek_jawatan] == 0) timbunan_VALUE[cek_jawatan] = 0;
        for (int cek_jawatan = 1; cek_jawatan < timbunan_tamat_jawatan; cek_jawatan += 힙폭[cek_jawatan]) if (timbunan_VALUE[cek_jawatan] == 0) {
            while (cek_jawatan + 힙폭[cek_jawatan] < timbunan_tamat_jawatan && timbunan_VALUE[cek_jawatan + 힙폭[cek_jawatan]] == 0) { int Seterusnya_jawatan = cek_jawatan + 힙폭[cek_jawatan]; 힙폭[cek_jawatan] += 힙폭[Seterusnya_jawatan]; 힙폭[Seterusnya_jawatan] = 0; }
            if (cek_jawatan + 힙폭[cek_jawatan] == timbunan_tamat_jawatan) { timbunan_tamat_jawatan = cek_jawatan; break; }
        }
    }
    static int 새기억(int 종류, int kepanjangan_VALUE) {
        if (kepanjangan_VALUE < 0) { kegagalan_VALUE("NegativeArraySizeException"); return 0; }
        if (kepanjangan_VALUE > timbunan_VALUE.length - 3) { kegagalan_VALUE("object heap exhausted"); return 0; }
        int 필요수 = kepanjangan_VALUE + 2, objek_Rujukan = 0;
        if (필요수 <= timbunan_VALUE.length - timbunan_tamat_jawatan) { objek_Rujukan = timbunan_tamat_jawatan; timbunan_tamat_jawatan += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < timbunan_tamat_jawatan; 읽는자리 += 힙폭[읽는자리]) if (timbunan_VALUE[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objek_Rujukan = 읽는자리; break; }
            if (objek_Rujukan != 0) {
                int 남은길이 = 힙폭[objek_Rujukan] - 필요수;
                if (남은길이 >= 2) { 힙폭[objek_Rujukan + 필요수] = 남은길이; timbunan_VALUE[objek_Rujukan + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= timbunan_VALUE.length - timbunan_tamat_jawatan) { objek_Rujukan = timbunan_tamat_jawatan; timbunan_tamat_jawatan += 필요수; }
        }
        if (objek_Rujukan == 0) { kegagalan_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { timbunan_VALUE[objek_Rujukan + Loop_INDEX] = 0; timbunan_Rujukan[objek_Rujukan + Loop_INDEX] = 0; 힙폭[objek_Rujukan + Loop_INDEX] = 0; }
        ARRAY_unsur[objek_Rujukan] = 0;
        힙폭[objek_Rujukan] = 필요수; timbunan_VALUE[objek_Rujukan] = 종류; timbunan_VALUE[objek_Rujukan + 1] = kepanjangan_VALUE; lindung_VALUE(objek_Rujukan); return objek_Rujukan;
    }
    static int pengecualian_Kelas(String nama_pemalar) {
        if (자바도구.같음(nama_pemalar, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nama_pemalar, "java/lang/Exception")) return 2;
        if (자바도구.같음(nama_pemalar, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nama_pemalar, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nama_pemalar, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nama_pemalar, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nama_pemalar, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nama_pemalar, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nama_pemalar, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nama_pemalar, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nama_pemalar, "java/io/IOException")) return 11;
        if (자바도구.같음(nama_pemalar, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nama_pemalar, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nama_pemalar, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nama_pemalar, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int pengecualian_pemalar(int Nama) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Nama, pengecualian_nama(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String pengecualian_nama(int akaun_VALUE) {
        if (akaun_VALUE == 40) return "java/lang/InterruptedException";
        if (akaun_VALUE == 41) return "Melayu/Asli/대기중단예외";
        if (akaun_VALUE == 39) return "java/net/SocketException";
        if (akaun_VALUE == 20) return "Melayu/Asli/pengecualian";
        if (akaun_VALUE == 21) return "Melayu/Asli/실행예외";
        if (akaun_VALUE == 22) return "Melayu/Asli/I_O_pengecualian";
        if (akaun_VALUE == 23) return "Melayu/Asli/tunggu_TIMEOUT_pengecualian";
        if (akaun_VALUE == 24) return "Melayu/Asli/e_mel_Carian_pengecualian";
        if (akaun_VALUE == 25) return "Melayu/Asli/파일없음예외";
        if (akaun_VALUE == 26) return "Melayu/Asli/통신예외";
        if (akaun_VALUE == 27) return "Melayu/Asli/tak_sah_argumen_pengecualian";
        if (akaun_VALUE == 28) return "Melayu/Asli/숫자형식예외";
        if (akaun_VALUE == 29) return "Melayu/Asli/범위예외";
        if (akaun_VALUE == 30) return "Melayu/Asli/배열범위예외";
        if (akaun_VALUE == 31) return "Melayu/Asli/문자열범위예외";
        if (akaun_VALUE == 32) return "Melayu/Asli/rujukan_nol_pengecualian";
        if (akaun_VALUE == 33) return "Melayu/Asli/산술예외";
        if (akaun_VALUE == 34) return "Melayu/Asli/status_pengecualian";
        if (akaun_VALUE == 35) return "Melayu/Asli/TYPE_siar_pengecualian";
        if (akaun_VALUE == 36) return "Melayu/Asli/음수배열크기예외";
        if (akaun_VALUE == 37) return "Melayu/Asli/ARRAY_stor_kegagalan";
        if (akaun_VALUE == 38) return "Melayu/Asli/urutan_status_pengecualian";
        if (akaun_VALUE == 1) return "java/lang/Throwable"; if (akaun_VALUE == 2) return "java/lang/Exception";
        if (akaun_VALUE == 3) return "java/lang/RuntimeException"; if (akaun_VALUE == 4) return "java/lang/ArithmeticException";
        if (akaun_VALUE == 5) return "java/lang/NullPointerException"; if (akaun_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (akaun_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (akaun_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (akaun_VALUE == 9) return "java/lang/IllegalArgumentException"; if (akaun_VALUE == 10) return "java/lang/NumberFormatException";
        if (akaun_VALUE == 11) return "java/io/IOException"; if (akaun_VALUE == 12) return "java/io/FileNotFoundException";
        if (akaun_VALUE == 17) return "java/lang/ArrayStoreException";
        if (akaun_VALUE == 18) return "java/net/UnknownHostException";
        if (akaun_VALUE == 19) return "java/net/SocketTimeoutException";
        if (akaun_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (akaun_VALUE == 13) return "java/lang/IllegalStateException"; if (akaun_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int akaun_VALUE) {
        if (akaun_VALUE == 40) return 2;
        if (akaun_VALUE == 41) return 40;
        if (akaun_VALUE == 39) return 11;
        if (akaun_VALUE == 1) return 0;
        if (akaun_VALUE == 2) return 1;
        if (akaun_VALUE == 3) return 2;
        if (akaun_VALUE == 4) return 3;
        if (akaun_VALUE == 5) return 3;
        if (akaun_VALUE == 6) return 3;
        if (akaun_VALUE == 7) return 6;
        if (akaun_VALUE == 8) return 6;
        if (akaun_VALUE == 9) return 3;
        if (akaun_VALUE == 10) return 9;
        if (akaun_VALUE == 11) return 2;
        if (akaun_VALUE == 12) return 11;
        if (akaun_VALUE == 13) return 3;
        if (akaun_VALUE == 14) return 3;
        if (akaun_VALUE == 15) return 3;
        if (akaun_VALUE == 16) return 9;
        if (akaun_VALUE == 17) return 3;
        if (akaun_VALUE == 18) return 11;
        if (akaun_VALUE == 19) return 11;
        if (akaun_VALUE == 20) return 2;
        if (akaun_VALUE == 21) return 3;
        if (akaun_VALUE == 22) return 11;
        if (akaun_VALUE == 23) return 22;
        if (akaun_VALUE == 24) return 22;
        if (akaun_VALUE == 25) return 22;
        if (akaun_VALUE == 26) return 22;
        if (akaun_VALUE == 27) return 9;
        if (akaun_VALUE == 28) return 27;
        if (akaun_VALUE == 29) return 6;
        if (akaun_VALUE == 30) return 29;
        if (akaun_VALUE == 31) return 29;
        if (akaun_VALUE == 32) return 5;
        if (akaun_VALUE == 33) return 4;
        if (akaun_VALUE == 34) return 13;
        if (akaun_VALUE == 35) return 14;
        if (akaun_VALUE == 36) return 15;
        if (akaun_VALUE == 37) return 17;
        if (akaun_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int nilai_sebenar, int 요구값) {
        for (int 깊이 = 0; nilai_sebenar != 0 && 깊이 < 16; 깊이++, nilai_sebenar = 예외부모(nilai_sebenar))
            if (nilai_sebenar == 요구값) return true;
        return false;
    }
    static void 예외던짐(int akaun_VALUE, String README_Rujukan) {
        int objek_Rujukan = 새기억(9, 2); if (RALAT) return;
        timbunan_VALUE[objek_Rujukan + 2] = akaun_VALUE; timbunan_VALUE[objek_Rujukan + 3] = hos_aksara(README_Rujukan); timbunan_Rujukan[objek_Rujukan + 3] = 1;
        던진객체 = objek_Rujukan; RALAT = true;
    }
    static boolean 맞는객체(int objek_Rujukan, int Nama) {
        if (objek_Rujukan == 0) return true;
        if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return false;
        int bidang_kod = timbunan_VALUE[objek_Rujukan];
        if (Word_SMS(Nama, "java/lang/Object")) return true;
        if (bidang_kod >= 32) return 종포함(bidang_kod - 32, Nama);
        if (bidang_kod == 9) { int sasaran_e_mel = pengecualian_pemalar(Nama); return sasaran_e_mel != 0 && 예외포함(timbunan_VALUE[objek_Rujukan + 2], sasaran_e_mel); }
        if (bidang_kod == 1) return Word_SMS(Nama, "java/lang/String") || Word_SMS(Nama, "java/lang/CharSequence");
        if (bidang_kod == 4) return Word_SMS(Nama, "java/lang/StringBuilder") || Word_SMS(Nama, "java/lang/CharSequence");
        if (bidang_kod == 10) return Word_SMS(Nama, "java/util/ArrayList") || Word_SMS(Nama, "java/util/List");
        if (bidang_kod == 11) return Word_SMS(Nama, "java/util/HashMap") || Word_SMS(Nama, "java/util/Map");
        if (bidang_kod == 12) return Word_SMS(Nama, "java/lang/Integer") || Word_SMS(Nama, "java/lang/Number");
        if (bidang_kod >= 24 && bidang_kod <= 28 && timbunan_VALUE[objek_Rujukan + 13] != 0) return 한국어화면종(Nama) == bidang_kod || Word_SMS(Nama, "Melayu/Asli/화면구성요소");
        if (bidang_kod >= 24 && bidang_kod <= 28) return (한국어화면종(Nama) == 0 && 화면종(Nama) == bidang_kod) || Word_SMS(Nama, "java/awt/Component") || Word_SMS(Nama, "java/awt/Container") || Word_SMS(Nama, "javax/swing/JComponent");
        if (bidang_kod == 29) return Word_SMS(Nama, timbunan_VALUE[objek_Rujukan + 3] != 0 ? "Melayu/Asli/동작알림" : "java/awt/event/ActionEvent");
        if (bidang_kod == 30) return Word_SMS(Nama, "java/awt/FlowLayout") || Word_SMS(Nama, "java/awt/LayoutManager");
        if (bidang_kod == 17) return Word_SMS(Nama, "java/net/Socket");
        if (bidang_kod == 18) return Word_SMS(Nama, "java/net/ServerSocket");
        if (bidang_kod == 19) return Word_SMS(Nama, timbunan_VALUE[objek_Rujukan + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (bidang_kod == 14) return Word_SMS(Nama, "java/net/InetAddress");
        if (bidang_kod == 15) return Word_SMS(Nama, "java/net/DatagramSocket");
        if (bidang_kod == 16) return Word_SMS(Nama, "java/net/DatagramPacket");
        if (bidang_kod == 13) return Word_SMS(Nama, timbunan_VALUE[objek_Rujukan + 3] != 0 ? "Melayu/Asli/작업가닥" : "java/lang/Thread");
        if (bidang_kod == 2) return Word_SMS(Nama, "[I"); if (bidang_kod == 20) return Word_SMS(Nama, "[B"); if (bidang_kod == 21) return Word_SMS(Nama, "[Z");
        if (bidang_kod == 22) return Word_SMS(Nama, "[C"); if (bidang_kod == 23) return Word_SMS(Nama, "[S");
        if (bidang_kod != 3) return false;
        if (Word_SMS(Nama, "[Ljava/lang/Object;")) return true;
        int komponen = ARRAY_unsur[objek_Rujukan];
        if (komponen == -1) return Word_SMS(Nama, "[Ljava/lang/String;") || Word_SMS(Nama, "[Ljava/lang/CharSequence;");
        if (komponen == 0) return false;
        if (배열종비교(komponen, Nama)) return true;
        if ((Word_SMS(komponen, "java/lang/String") || Word_SMS(komponen, "java/lang/StringBuilder")) && Word_SMS(Nama, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Takrif_COUNT; Loop_INDEX++) if (같은말(Kelas_Takrif_nama[Loop_INDEX], komponen)) {
            for (int titik_kod = Loop_INDEX, 중첩깊이 = 0; titik_kod >= 0 && 중첩깊이 < 16; 중첩깊이++, titik_kod = 부모종(titik_kod)) {
                if (배열종비교(종부모[titik_kod], Nama)) return true;
                for (int dalaman_jawatan = 0; dalaman_jawatan < Kelas_antara_muka_COUNT[titik_kod]; dalaman_jawatan++) if (배열종비교(Kelas_antara_muka[titik_kod * 16 + dalaman_jawatan], Nama)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nama_pemalar, int 형식참조) {
        int cek_jawatan = 상가[형식참조], pemasukan_COUNT = pemalar_SECOND_VALUE[형식참조];
        if (nama_pemalar == 0 || pemasukan_COUNT < 4 || Fail[cek_jawatan] != '[' || Fail[cek_jawatan + 1] != 'L' || Fail[cek_jawatan + pemasukan_COUNT - 1] != ';' || pemalar_SECOND_VALUE[nama_pemalar] != pemasukan_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT - 3; Loop_INDEX++) if (Fail[상가[nama_pemalar] + Loop_INDEX] != Fail[cek_jawatan + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void pemegang_pengecualian() {
        if (던진객체 == 0) return;
        RALAT = false;
        while (bingkai_INDEX >= 현재가닥 * 32) {
            int fail_INDEX = bingkai_kaedah[bingkai_INDEX], 읽는자리 = bingkai_suruhan[bingkai_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == fail_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                bingkai_jawatan[bingkai_INDEX] = 잡기위치[Loop_INDEX]; bingkai_tindan[bingkai_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (mengasal_bingkai[bingkai_INDEX] != 0) Kelas_Takrif_status[mengasal_bingkai[bingkai_INDEX] - 1] = 3;
            if (bingkai_kunci[bingkai_INDEX] != 0) { keluaran_kunci(bingkai_kunci[bingkai_INDEX]); bingkai_kunci[bingkai_INDEX] = 0; }
            bingkai_INDEX--;
        }
        ruang_pengguna.Tulis("Uncaught ");
        if (timbunan_VALUE[던진객체] == 9) { ruang_pengguna.Tulis(pengecualian_nama(timbunan_VALUE[던진객체 + 2])); ruang_pengguna.Tulis(": "); tulis_SMS(timbunan_VALUE[던진객체 + 3]); }
        else ruang_pengguna.Tulis("user exception");
        ruang_pengguna.tulis_aksara_VALUE(10); 던진객체 = 0; RALAT = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void tindan_suruhan(int perintah_kod) {
        int 첫값 = 빼기(0), 첫형식 = kembalikan_TYPE;
        if (perintah_kod == 87) return;
        if (perintah_kod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bait_data = 빼기(0), SECOND_format = kembalikan_TYPE;
        if (perintah_kod == 88) return;
        if (perintah_kod == 90) { 넣기(첫값, 첫형식); 넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (perintah_kod == 92) { 넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (perintah_kod == 95) { 넣기(첫값, 첫형식); 넣기(bait_data, SECOND_format); return; }
        int titik_kod = 빼기(0), 셋째형식 = kembalikan_TYPE;
        if (perintah_kod == 91) { 넣기(첫값, 첫형식); 넣기(titik_kod, 셋째형식); 넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (perintah_kod == 93) { 넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(titik_kod, 셋째형식); 넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = kembalikan_TYPE;
        넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(titik_kod, 셋째형식); 넣기(bait_data, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nama_pemalar, int 시작점) {
        int bidang_kod = 0, sah_kepanjangan = 0, pengecualian_Rujukan = pengecualian_pemalar(nama_pemalar);
        if (Word_SMS(nama_pemalar, "java/lang/StringBuilder")) { bidang_kod = 4; sah_kepanjangan = 1; }
        if (Word_SMS(nama_pemalar, "java/io/FileInputStream")) { bidang_kod = 5; sah_kepanjangan = 2; }
        if (Word_SMS(nama_pemalar, "java/io/FileOutputStream")) { bidang_kod = 6; sah_kepanjangan = 2; }
        if (pengecualian_Rujukan != 0) { bidang_kod = 9; sah_kepanjangan = 2; }
        if (Word_SMS(nama_pemalar, "java/util/ArrayList")) { bidang_kod = 10; sah_kepanjangan = 2; }
        if (Word_SMS(nama_pemalar, "java/util/HashMap")) { bidang_kod = 11; sah_kepanjangan = 2; }
        if (Word_SMS(nama_pemalar, "java/lang/Integer")) { bidang_kod = 12; sah_kepanjangan = 1; }
        if (Word_SMS(nama_pemalar, "java/net/Socket")) { bidang_kod = 17; sah_kepanjangan = 5; }
        if (Word_SMS(nama_pemalar, "java/net/ServerSocket")) { bidang_kod = 18; sah_kepanjangan = 5; }
        if (Word_SMS(nama_pemalar, "java/net/DatagramSocket")) { bidang_kod = 15; sah_kepanjangan = 3; }
        if (Word_SMS(nama_pemalar, "java/net/DatagramPacket")) { bidang_kod = 16; sah_kepanjangan = 4; }
        if (Word_SMS(nama_pemalar, "java/lang/Thread") || Word_SMS(nama_pemalar, "Melayu/Asli/작업가닥")) { bidang_kod = 13; sah_kepanjangan = 2; }
        if (Word_SMS(nama_pemalar, "java/lang/Object")) { bidang_kod = 8; }
        if (bidang_kod == 0 && 화면종(nama_pemalar) != 0) { bidang_kod = 화면종(nama_pemalar); sah_kepanjangan = 12; }
        if (bidang_kod == 0) {
            int titik_kod = Cari_Kelas_Takrif(nama_pemalar); if (titik_kod < 0 || RALAT || !mengasal(titik_kod, 시작점)) return;
            bidang_kod = 32 + titik_kod; sah_kepanjangan = 종칸수[titik_kod];
        }
        int objek_Rujukan = peruntuk_Storan(bidang_kod, sah_kepanjangan); if (RALAT) return;
        if (bidang_kod == 13 && Word_SMS(nama_pemalar, "Melayu/Asli/작업가닥")) timbunan_VALUE[objek_Rujukan + 3] = 1;
        if (bidang_kod >= 24 && bidang_kod <= 28 && 한국어화면종(nama_pemalar) != 0) timbunan_VALUE[objek_Rujukan + 13] = 1;
        if (bidang_kod == 5 || bidang_kod == 6 || bidang_kod == 15 || bidang_kod == 17 || bidang_kod == 18) timbunan_VALUE[objek_Rujukan + 2] = -1;
        if (bidang_kod == 9) timbunan_VALUE[objek_Rujukan + 2] = pengecualian_Rujukan;
        넣기(objek_Rujukan, 2);
    }
    static boolean 값같음(int 첫값, int bait_data) {
        if (첫값 == bait_data) return true;
        if (첫값 == 0 || bait_data == 0 || 첫값 < 0 || bait_data < 0 || 첫값 >= timbunan_tamat_jawatan || bait_data >= timbunan_tamat_jawatan) return false;
        if (timbunan_VALUE[첫값] == 1 && timbunan_VALUE[bait_data] == 1) return teks_sama(첫값, bait_data, false);
        return timbunan_VALUE[첫값] == 12 && timbunan_VALUE[bait_data] == 12 && timbunan_VALUE[첫값 + 2] == timbunan_VALUE[bait_data + 2];
    }
    static int 글조각(int objek_Rujukan, int Mula_jawatan, int tamat_jawatan) {
        if (!objek_VALUE(objek_Rujukan, 1)) return 0;
        if (Mula_jawatan < 0 || tamat_jawatan < Mula_jawatan || tamat_jawatan > timbunan_VALUE[objek_Rujukan + 1]) { kegagalan_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = peruntuk_Storan(1, tamat_jawatan - Mula_jawatan); if (RALAT) return 0;
        for (int Loop_INDEX = Mula_jawatan; Loop_INDEX < tamat_jawatan; Loop_INDEX++) timbunan_VALUE[반환값 + 2 + Loop_INDEX - Mula_jawatan] = timbunan_VALUE[objek_Rujukan + 2 + Loop_INDEX];
        return 반환값;
    }
    static int cantum_SMS(int 첫값, int bait_data) {
        if (!objek_VALUE(첫값, 1) || !objek_VALUE(bait_data, 1)) return 0;
        int pemasukan_COUNT = timbunan_VALUE[첫값 + 1], kaedah_INDEX = timbunan_VALUE[bait_data + 1], 반환값 = peruntuk_Storan(1, pemasukan_COUNT + kaedah_INDEX); if (RALAT) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) timbunan_VALUE[반환값 + 2 + Loop_INDEX] = timbunan_VALUE[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < kaedah_INDEX; Loop_INDEX++) timbunan_VALUE[반환값 + 2 + pemasukan_COUNT + Loop_INDEX] = timbunan_VALUE[bait_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int pemilik, int nama_pemalar, int 서술상수, int perintah_kod) {
        if (Word_SMS(pemilik, "Melayu/Asli/실행인수") && perintah_kod == 184) {
            if (Word_SMS(nama_pemalar, "item_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.인수개수() - 1, 1); return true; }
            if (Word_SMS(nama_pemalar, "Teks") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= ruang_pengguna.인수개수() - 1) 예외던짐(29, "laksanakan_perintah 인수 범위를 벗어났습니다");
                else 넣기(hos_aksara(ruang_pengguna.인수(순번 + 1)), 2);
                return true;
            }
            kegagalan_VALUE("지원하지 않는 Melayu laksanakan_perintah 인수 호출"); return true;
        }
        if (Word_SMS(pemilik, "Melayu/Asli/작업가닥")) { Proses_urutan(nama_pemalar, 서술상수, perintah_kod, true); return true; }
        if (한국어화면소유(pemilik)) { 한국어화면호출(pemilik, nama_pemalar, 서술상수, perintah_kod); return true; }
        if (화면소유(pemilik)) { 화면호출(pemilik, nama_pemalar, 서술상수, perintah_kod); return true; }
        if (Word_SMS(pemilik, "java/net/Socket") || Word_SMS(pemilik, "java/net/ServerSocket") || Word_SMS(pemilik, "java/io/InputStream") || Word_SMS(pemilik, "java/io/OutputStream")) { 흐름호출(pemilik, nama_pemalar, 서술상수, perintah_kod); return true; }
        if (Word_SMS(pemilik, "Melayu/Asli/kernel_VALUE") && perintah_kod == 184) {
            if (Word_SMS(nama_pemalar, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.화면너비(), 1); return true; }
            if (Word_SMS(nama_pemalar, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.화면높이(), 1); return true; }
            if (Word_SMS(nama_pemalar, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.밀리초(), 1); return true; }
            if (Word_SMS(nama_pemalar, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.그림대기(), 1); return true; }
            if (Word_SMS(nama_pemalar, "segi_empat_tepat") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), koordinat_x = 빼기(1); 넣기(ruang_pengguna.segi_empat_tepat(koordinat_x, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(pemilik, "java/net/InetAddress") || Word_SMS(pemilik, "java/net/DatagramPacket") || Word_SMS(pemilik, "java/net/DatagramSocket")) { 통신호출(pemilik, nama_pemalar, 서술상수, perintah_kod); return true; }
        if (Word_SMS(pemilik, "java/lang/Thread")) { 가닥호출(nama_pemalar, 서술상수, perintah_kod); return true; }
        if (Word_SMS(pemilik, "java/lang/Object")) {
            if (Word_SMS(nama_pemalar, "<init>") && Word_SMS(서술상수, "()V") && perintah_kod == 183) { teknologi_maklumat_sah_objek(빼기(2)); return true; }
            if (Word_SMS(nama_pemalar, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bait_data = 빼기(2), 첫값 = 빼기(2); if (teknologi_maklumat_sah_objek(첫값)) 넣기(첫값 == bait_data ? 1 : 0, 1); return true; }
        }
        if (pengecualian_pemalar(pemilik) != 0) {
            if (Word_SMS(nama_pemalar, "<init>") && perintah_kod == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int prom = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objek_Rujukan = 빼기(2);
                if (objek_VALUE(objek_Rujukan, 9)) { timbunan_VALUE[objek_Rujukan + 3] = prom; timbunan_Rujukan[objek_Rujukan + 3] = 1; } return true;
            }
            if ((Word_SMS(nama_pemalar, "getMessage") || Word_SMS(nama_pemalar, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 9)) 넣기(timbunan_VALUE[objek_Rujukan + 3], 2); return true; }
        }
        if (Word_SMS(pemilik, "java/lang/String")) {
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int pengekodan_nama = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objek_Rujukan = 빼기(2);
                if (!objek_VALUE(objek_Rujukan, 1)) return true;
                if (pengekodan_nama != 0 && !teks_sama(pengekodan_nama, hos_aksara("UTF-8"), false) && !teks_sama(pengekodan_nama, hos_aksara("UTF8"), false) && !teks_sama(pengekodan_nama, hos_aksara("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int pemasukan_COUNT = timbunan_VALUE[objek_Rujukan + 1], 반환값 = peruntuk_Storan(20, pemasukan_COUNT * 3), 사용수 = 0; if (RALAT) return true;
                for (int dalaman_jawatan = 0; dalaman_jawatan < pemasukan_COUNT; dalaman_jawatan++) {
                    int titik_kod = timbunan_VALUE[objek_Rujukan + 2 + dalaman_jawatan];
                    if (titik_kod >= 0xd800 && titik_kod <= 0xdbff && dalaman_jawatan + 1 < pemasukan_COUNT && timbunan_VALUE[objek_Rujukan + 3 + dalaman_jawatan] >= 0xdc00 && timbunan_VALUE[objek_Rujukan + 3 + dalaman_jawatan] <= 0xdfff) titik_kod = 0x10000 + ((titik_kod - 0xd800) << 10) + timbunan_VALUE[objek_Rujukan + 2 + ++dalaman_jawatan] - 0xdc00;
                    else if (titik_kod >= 0xd800 && titik_kod <= 0xdfff) titik_kod = '?';
                    if (titik_kod < 128) timbunan_VALUE[반환값 + 2 + 사용수++] = titik_kod;
                    else { int bait_COUNT = titik_kod < 2048 ? 2 : titik_kod < 65536 ? 3 : 4; timbunan_VALUE[반환값 + 2 + 사용수++] = (byte)((bait_COUNT == 2 ? 192 : bait_COUNT == 3 ? 224 : 240) | titik_kod >> (6 * (bait_COUNT - 1))); for (int Perbandingan_jawatan = bait_COUNT - 1; Perbandingan_jawatan > 0; Perbandingan_jawatan--) timbunan_VALUE[반환값 + 2 + 사용수++] = (byte)(128 | titik_kod >> (6 * (Perbandingan_jawatan - 1)) & 63); }
                }
                timbunan_VALUE[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digit_aksara(빼기(1)), 2); return true; }
            if (perintah_kod != 182) return false;
            if (Word_SMS(nama_pemalar, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bait_data = 빼기(2), 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(teks_sama(첫값, bait_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nama_pemalar, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(timbunan_VALUE[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nama_pemalar, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int tamat_jawatan = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objek_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? tamat_jawatan : timbunan_VALUE[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nama_pemalar, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bait_data = 빼기(2), 첫값 = 빼기(2); 넣기(cantum_SMS(첫값, bait_data), 2); return true; }
            if (Word_SMS(nama_pemalar, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), cincangan_VALUE = 0; if (objek_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < timbunan_VALUE[첫값 + 1]; Loop_INDEX++) cincangan_VALUE = cincangan_VALUE * 31 + timbunan_VALUE[첫값 + 2 + Loop_INDEX]; 넣기(cincangan_VALUE, 1); } return true; }
            if (Word_SMS(nama_pemalar, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(pemilik, "java/lang/Integer")) {
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VALUE = 빼기(1), objek_Rujukan = data_VALUE >= -128 && data_VALUE <= 127 ? stor_integer[data_VALUE + 128] : 0; if (objek_Rujukan == 0) { objek_Rujukan = peruntuk_Storan(12, 1); if (!RALAT) { timbunan_VALUE[objek_Rujukan + 2] = data_VALUE; if (data_VALUE >= -128 && data_VALUE <= 127) stor_integer[data_VALUE + 128] = objek_Rujukan; } } 넣기(objek_Rujukan, 2); return true; }
            if (perintah_kod == 183 && Word_SMS(nama_pemalar, "<init>") && Word_SMS(서술상수, "(I)V")) { int data_VALUE = 빼기(1), objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 12)) timbunan_VALUE[objek_Rujukan + 2] = data_VALUE; return true; }
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "intValue") && Word_SMS(서술상수, "()I")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 12)) 넣기(timbunan_VALUE[objek_Rujukan + 2], 1); return true; }
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digit_aksara(빼기(1)), 2); return true; }
        }
        if (Word_SMS(pemilik, "java/lang/Math") && perintah_kod == 184) {
            if (Word_SMS(nama_pemalar, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nama_pemalar, "min") || Word_SMS(nama_pemalar, "max")) && Word_SMS(서술상수, "(II)I")) { int bait_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nama_pemalar, "min") ? (첫값 < bait_data ? 첫값 : bait_data) : (첫값 > bait_data ? 첫값 : bait_data), 1); return true; }
        }
        if (Word_SMS(pemilik, "java/lang/System") && perintah_kod == 184) {
            if (Word_SMS(nama_pemalar, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(nama_pemalar, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int pemasukan_COUNT = 빼기(1), destinasi_VALUE_INDEX = 빼기(1), bait_data = 빼기(2), Mula_jawatan = 빼기(1), 첫값 = 빼기(2);
                if (teknologi_maklumat_sah_objek(첫값) && teknologi_maklumat_sah_objek(bait_data)) {
                    int bidang_kod = timbunan_VALUE[첫값];
                    if (timbunan_VALUE[bait_data] != bidang_kod || (bidang_kod != 2 && bidang_kod != 3 && (bidang_kod < 20 || bidang_kod > 23))) kegagalan_VALUE("arraycopy type mismatch");
                    else if (pemasukan_COUNT < 0 || Mula_jawatan < 0 || destinasi_VALUE_INDEX < 0 || Mula_jawatan > timbunan_VALUE[첫값 + 1] - pemasukan_COUNT || destinasi_VALUE_INDEX > timbunan_VALUE[bait_data + 1] - pemasukan_COUNT) kegagalan_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bait_data && destinasi_VALUE_INDEX > Mula_jawatan) { for (int Loop_INDEX = pemasukan_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) timbunan_VALUE[bait_data + 2 + destinasi_VALUE_INDEX + Loop_INDEX] = timbunan_VALUE[첫값 + 2 + Mula_jawatan + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT && !RALAT; Loop_INDEX++) { int data_VALUE = timbunan_VALUE[첫값 + 2 + Mula_jawatan + Loop_INDEX]; if (bidang_kod != 3 || 배열저장가능(bait_data, data_VALUE)) timbunan_VALUE[bait_data + 2 + destinasi_VALUE_INDEX + Loop_INDEX] = data_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(pemilik, "java/util/ArrayList") || Word_SMS(pemilik, "java/util/List") || Word_SMS(pemilik, "java/util/HashMap") || Word_SMS(pemilik, "java/util/Map")) {
            모음호출(pemilik, nama_pemalar, 서술상수, perintah_kod); return true;
        }
        return false;
    }
    static void 모음늘리기(int objek_Rujukan, int 필요수) {
        int 이전값 = timbunan_VALUE[objek_Rujukan + 2], kapasiti_data = 이전값 == 0 ? 0 : timbunan_VALUE[이전값 + 1];
        if (kapasiti_data >= 필요수) return;
        int Seterusnya_jawatan = kapasiti_data < 8 ? 8 : kapasiti_data * 2; if (Seterusnya_jawatan < 필요수) Seterusnya_jawatan = 필요수;
        int data_ARRAY = peruntuk_Storan(3, Seterusnya_jawatan); if (RALAT) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapasiti_data; Loop_INDEX++) timbunan_VALUE[data_ARRAY + 2 + Loop_INDEX] = timbunan_VALUE[이전값 + 2 + Loop_INDEX];
        timbunan_VALUE[objek_Rujukan + 2] = data_ARRAY; timbunan_Rujukan[objek_Rujukan + 2] = 1;
    }
    static void 모음호출(int pemilik, int nama_pemalar, int 서술상수, int perintah_kod) {
        boolean 대응참조 = Word_SMS(pemilik, "java/util/HashMap") || Word_SMS(pemilik, "java/util/Map"); int bidang_kod = 대응참조 ? 11 : 10;
        if (Word_SMS(nama_pemalar, "<init>") && perintah_kod == 183 && Word_SMS(서술상수, "()V")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, bidang_kod)) 모음늘리기(objek_Rujukan, 8); return; }
        if (perintah_kod != 182 && perintah_kod != 185) { kegagalan_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(nama_pemalar, "size") && Word_SMS(서술상수, "()I") || Word_SMS(nama_pemalar, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, bidang_kod)) 넣기(Word_SMS(nama_pemalar, "size") ? timbunan_VALUE[objek_Rujukan + 3] : timbunan_VALUE[objek_Rujukan + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nama_pemalar, "clear") && Word_SMS(서술상수, "()V")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, bidang_kod)) { int data_ARRAY = timbunan_VALUE[objek_Rujukan + 2]; for (int Loop_INDEX = 0; Loop_INDEX < timbunan_VALUE[data_ARRAY + 1]; Loop_INDEX++) timbunan_VALUE[data_ARRAY + 2 + Loop_INDEX] = 0; timbunan_VALUE[objek_Rujukan + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nama_pemalar, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VALUE = 빼기(2), objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 10)) return;
            int pemasukan_COUNT = timbunan_VALUE[objek_Rujukan + 3]; 모음늘리기(objek_Rujukan, pemasukan_COUNT + 1); if (!RALAT) { timbunan_VALUE[timbunan_VALUE[objek_Rujukan + 2] + 2 + pemasukan_COUNT] = data_VALUE; timbunan_VALUE[objek_Rujukan + 3] = pemasukan_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nama_pemalar, "get") || Word_SMS(nama_pemalar, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nama_pemalar, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean teknologi_maklumat_Diuntukkan = Word_SMS(nama_pemalar, "set"); int data_VALUE = teknologi_maklumat_Diuntukkan ? 빼기(2) : 0, pemasukan_jawatan = 빼기(1), objek_Rujukan = 빼기(2);
            if (!objek_VALUE(objek_Rujukan, 10)) return;
            int pemasukan_COUNT = timbunan_VALUE[objek_Rujukan + 3], data_ARRAY = timbunan_VALUE[objek_Rujukan + 2];
            if (pemasukan_jawatan < 0 || pemasukan_jawatan >= pemasukan_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = timbunan_VALUE[data_ARRAY + 2 + pemasukan_jawatan];
            if (teknologi_maklumat_Diuntukkan) timbunan_VALUE[data_ARRAY + 2 + pemasukan_jawatan] = data_VALUE;
            if (Word_SMS(nama_pemalar, "remove")) { for (int Loop_INDEX = pemasukan_jawatan + 1; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) timbunan_VALUE[data_ARRAY + 1 + Loop_INDEX] = timbunan_VALUE[data_ARRAY + 2 + Loop_INDEX]; timbunan_VALUE[data_ARRAY + 1 + pemasukan_COUNT] = 0; timbunan_VALUE[objek_Rujukan + 3] = pemasukan_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(nama_pemalar, "get") || Word_SMS(nama_pemalar, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nama_pemalar, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nama_pemalar, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nama_pemalar, "put"), alih_keluar = Word_SMS(nama_pemalar, "remove");
            int data_VALUE = 넣기여부 ? 빼기(2) : 0, Kunci_Rujukan = 빼기(2), objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 11)) return;
            int pemasukan_COUNT = timbunan_VALUE[objek_Rujukan + 3], data_ARRAY = timbunan_VALUE[objek_Rujukan + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) if (값같음(Kunci_Rujukan, timbunan_VALUE[data_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : timbunan_VALUE[data_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objek_Rujukan, (pemasukan_COUNT + 1) * 2); data_ARRAY = timbunan_VALUE[objek_Rujukan + 2]; 찾은여부 = pemasukan_COUNT; if (!RALAT) timbunan_VALUE[objek_Rujukan + 3] = pemasukan_COUNT + 1; }
                if (!RALAT) { timbunan_VALUE[data_ARRAY + 2 + 2 * 찾은여부] = Kunci_Rujukan; timbunan_VALUE[data_ARRAY + 3 + 2 * 찾은여부] = data_VALUE; }
            }
            if (alih_keluar && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) { timbunan_VALUE[data_ARRAY + 2 * Loop_INDEX] = timbunan_VALUE[data_ARRAY + 2 + 2 * Loop_INDEX]; timbunan_VALUE[data_ARRAY + 1 + 2 * Loop_INDEX] = timbunan_VALUE[data_ARRAY + 3 + 2 * Loop_INDEX]; } timbunan_VALUE[data_ARRAY + 2 * pemasukan_COUNT] = 0; timbunan_VALUE[data_ARRAY + 1 + 2 * pemasukan_COUNT] = 0; timbunan_VALUE[objek_Rujukan + 3] = pemasukan_COUNT - 1; }
            if (Word_SMS(nama_pemalar, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        kegagalan_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objek_Rujukan) {
        if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return false;
        if (잠금깊이[objek_Rujukan] != 0 && kunci_pemilik[objek_Rujukan] != 현재가닥 + 1) { ubah_permintaan = true; return false; }
        kunci_pemilik[objek_Rujukan] = 현재가닥 + 1; 잠금깊이[objek_Rujukan]++; return true;
    }
    static void keluaran_kunci(int objek_Rujukan) {
        if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return;
        if (잠금깊이[objek_Rujukan] == 0 || kunci_pemilik[objek_Rujukan] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objek_Rujukan] == 0) kunci_pemilik[objek_Rujukan] = 0;
    }
    static boolean tukar_urutan() {
        urutan_bingkai[현재가닥] = bingkai_INDEX;
        if (bingkai_INDEX < 현재가닥 * 32) urutan_status[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < urutan_COUNT; Loop_INDEX++) if (urutan_status[Loop_INDEX] == 2 && urutan_status[가닥대기[Loop_INDEX]] == 3) urutan_status[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= urutan_COUNT; Loop_INDEX++) {
            int Seterusnya_jawatan = (현재가닥 + Loop_INDEX) % urutan_COUNT;
            if (urutan_status[Seterusnya_jawatan] == 1) { 현재가닥 = Seterusnya_jawatan; bingkai_INDEX = urutan_bingkai[Seterusnya_jawatan]; ubah_permintaan = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < urutan_COUNT; Loop_INDEX++) if (urutan_status[Loop_INDEX] != 3) { kegagalan_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nama_pemalar, int 서술상수, int perintah_kod) { Proses_urutan(nama_pemalar, 서술상수, perintah_kod, false); }
    static void Proses_urutan(int nama_pemalar, int 서술상수, int perintah_kod, boolean Melayu) {
        if (perintah_kod == 184 && Word_SMS(nama_pemalar, Melayu ? "YIELD_tugas" : "yield") && Word_SMS(서술상수, "()V")) { ubah_permintaan = true; return; }
        if (perintah_kod == 184 && Word_SMS(nama_pemalar, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(urutan_objek[현재가닥], 2); return; }
        if (perintah_kod == 183 && Word_SMS(nama_pemalar, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Melayu ? "(LMelayu/Asli/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int sasaran_e_mel = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objek_Rujukan = 빼기(2);
            if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return;
            if (timbunan_VALUE[objek_Rujukan] == 13) { timbunan_VALUE[objek_Rujukan + 2] = sasaran_e_mel; timbunan_Rujukan[objek_Rujukan + 2] = 1; }
            else if (sasaran_e_mel != 0) kegagalan_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (perintah_kod == 182 && (Word_SMS(nama_pemalar, Melayu ? "Mula_tugas" : "start") || Word_SMS(nama_pemalar, Melayu ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || perintah_kod == 182 && Word_SMS(nama_pemalar, Melayu ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objek_Rujukan = 빼기(2); if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return;
            int akaun_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < urutan_COUNT; Loop_INDEX++) if (urutan_objek[Loop_INDEX] == objek_Rujukan) akaun_VALUE = Loop_INDEX;
            if (Word_SMS(nama_pemalar, Melayu ? "살아있는가" : "isAlive")) { 넣기(akaun_VALUE >= 0 && urutan_status[akaun_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nama_pemalar, Melayu ? "기다리기" : "join")) { if (akaun_VALUE >= 0 && urutan_status[akaun_VALUE] != 3) { 가닥대기[현재가닥] = akaun_VALUE; urutan_status[현재가닥] = 2; ubah_permintaan = true; } return; }
            if (akaun_VALUE >= 0) { 예외던짐(Melayu ? 38 : 16, "thread already started"); return; }
            if (urutan_COUNT == 4) { kegagalan_VALUE("thread limit (4 including main)"); return; }
            int sasaran_e_mel = timbunan_VALUE[objek_Rujukan] == 13 ? timbunan_VALUE[objek_Rujukan + 2] : objek_Rujukan;
            int fail_INDEX = sasaran_e_mel > 0 && timbunan_VALUE[sasaran_e_mel] >= 32 ? nama_kaedah(timbunan_VALUE[sasaran_e_mel] - 32, Melayu ? "Lakukan" : "run", "()V") : -1;
            if (sasaran_e_mel != 0 && fail_INDEX < 0) { kegagalan_VALUE("Runnable.run required"); return; }
            akaun_VALUE = urutan_COUNT++; urutan_objek[akaun_VALUE] = objek_Rujukan; urutan_sasaran[akaun_VALUE] = sasaran_e_mel;
            int bingkai = akaun_VALUE * 32; urutan_bingkai[akaun_VALUE] = fail_INDEX < 0 ? bingkai - 1 : bingkai; urutan_status[akaun_VALUE] = fail_INDEX < 0 ? 3 : 1;
            if (fail_INDEX >= 0) { bingkai_kaedah[bingkai] = fail_INDEX; bingkai_jawatan[bingkai] = kaedah_Mula[fail_INDEX]; setempat_VALUE[bingkai * 128] = sasaran_e_mel; setempat_TYPE[bingkai * 128] = 2; }
            return;
        }
        kegagalan_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], e_mel_SMS = new int[16];
    static int setempat_e_mel() { return e_mel_objek(0x7f000001); }
    static int e_mel_objek(int VALUE) { int objek_Rujukan = peruntuk_Storan(14, 1); if (!RALAT) timbunan_VALUE[objek_Rujukan + 2] = VALUE; return objek_Rujukan; }
    static int 주소해독(int objek_Rujukan) {
        if (objek_Rujukan == 0 || teks_sama(objek_Rujukan, hos_aksara("localhost"), false)) return 0x7f000001;
        if (!objek_VALUE(objek_Rujukan, 1)) return 0;
        int data_VALUE = 0, 총수 = 0, e_mel_bait = 0, 자릿수 = 0, pemasukan_COUNT = timbunan_VALUE[objek_Rujukan + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= pemasukan_COUNT; Loop_INDEX++) {
            int titik_kod = Loop_INDEX == pemasukan_COUNT ? '.' : timbunan_VALUE[objek_Rujukan + 2 + Loop_INDEX];
            if (titik_kod == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VALUE = data_VALUE << 8 | e_mel_bait; 총수++; e_mel_bait = 자릿수 = 0; }
            else { if (titik_kod < '0' || titik_kod > '9' || ++자릿수 > 3 || (e_mel_bait = e_mel_bait * 10 + titik_kod - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VALUE;
    }
    static int e_mel_aksara(int data_VALUE) {
        int pemasukan_COUNT = 0;
        for (int anjak = 24; anjak >= 0; anjak -= 8) {
            int e_mel_bait = data_VALUE >>> anjak & 255;
            if (e_mel_bait >= 100) e_mel_SMS[pemasukan_COUNT++] = '0' + e_mel_bait / 100;
            if (e_mel_bait >= 10) e_mel_SMS[pemasukan_COUNT++] = '0' + e_mel_bait / 10 % 10;
            e_mel_SMS[pemasukan_COUNT++] = '0' + e_mel_bait % 10; if (anjak != 0) e_mel_SMS[pemasukan_COUNT++] = '.';
        }
        int objek_Rujukan = peruntuk_Storan(1, pemasukan_COUNT); if (!RALAT) for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) timbunan_VALUE[objek_Rujukan + 2 + Loop_INDEX] = e_mel_SMS[Loop_INDEX]; return objek_Rujukan;
    }
    static void 통신호출(int pemilik, int nama_pemalar, int 서술상수, int perintah_kod) {
        if (Word_SMS(pemilik, "java/net/InetAddress")) {
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(setempat_e_mel(), 2); return; }
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !RALAT) 넣기(e_mel_objek(data_VALUE), 2); return;
            }
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 14)) 넣기(e_mel_aksara(timbunan_VALUE[objek_Rujukan + 2]), 2); return; }
        }
        if (Word_SMS(pemilik, "java/net/DatagramPacket")) {
            if (perintah_kod == 183 && Word_SMS(nama_pemalar, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean destinasi_VALUE_Rujukan = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int nombor_port = destinasi_VALUE_Rujukan ? 빼기(1) : 0, e_mel_Rujukan = destinasi_VALUE_Rujukan ? 빼기(2) : 0;
                int pemasukan_COUNT = 빼기(1), data_ARRAY = 빼기(2), objek_Rujukan = 빼기(2);
                if (!objek_VALUE(objek_Rujukan, 16) || !objek_VALUE(data_ARRAY, 20)) return;
                if (pemasukan_COUNT < 0 || pemasukan_COUNT > timbunan_VALUE[data_ARRAY + 1] || nombor_port < 0 || nombor_port > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (e_mel_Rujukan != 0 && !objek_VALUE(e_mel_Rujukan, 14)) return;
                timbunan_VALUE[objek_Rujukan + 2] = data_ARRAY; timbunan_Rujukan[objek_Rujukan + 2] = 1; timbunan_VALUE[objek_Rujukan + 3] = pemasukan_COUNT;
                timbunan_VALUE[objek_Rujukan + 4] = e_mel_Rujukan; timbunan_Rujukan[objek_Rujukan + 4] = 1; timbunan_VALUE[objek_Rujukan + 5] = nombor_port; return;
            }
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int pemasukan_COUNT = 빼기(1), objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 16)) return;
                if (pemasukan_COUNT < 0 || pemasukan_COUNT > timbunan_VALUE[timbunan_VALUE[objek_Rujukan + 2] + 1]) 예외던짐(9, "invalid datagram length"); else timbunan_VALUE[objek_Rujukan + 3] = pemasukan_COUNT; return;
            }
            if (perintah_kod == 182 && (Word_SMS(nama_pemalar, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(nama_pemalar, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(nama_pemalar, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(nama_pemalar, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 16)) return;
                int pemasukan_jawatan = Word_SMS(nama_pemalar, "getData") ? 2 : Word_SMS(nama_pemalar, "getLength") ? 3 : Word_SMS(nama_pemalar, "getAddress") ? 4 : 5;
                넣기(timbunan_VALUE[objek_Rujukan + pemasukan_jawatan], pemasukan_jawatan == 2 || pemasukan_jawatan == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(pemilik, "java/net/DatagramSocket")) {
            if (perintah_kod == 183 && Word_SMS(nama_pemalar, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int nombor_port = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 15)) return;
                if (nombor_port < 0 || nombor_port > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = ruang_pengguna.buka_rangkaian(nombor_port); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else timbunan_VALUE[objek_Rujukan + 2] = 열린파일번호; return;
            }
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else timbunan_VALUE[objek_Rujukan + 3] = 밀리초값; return;
            }
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 15)) 넣기(timbunan_VALUE[objek_Rujukan + 2] < 0 ? -1 : ruang_pengguna.rangkaian_port(timbunan_VALUE[objek_Rujukan + 2]), 1); return; }
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "isClosed") && Word_SMS(서술상수, "()Z")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 15)) 넣기(timbunan_VALUE[objek_Rujukan + 2] < 0 ? 1 : 0, 1); return; }
            if (perintah_kod == 182 && Word_SMS(nama_pemalar, "close") && Word_SMS(서술상수, "()V")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 15) && timbunan_VALUE[objek_Rujukan + 2] >= 0) { ruang_pengguna.파일서술자닫기(timbunan_VALUE[objek_Rujukan + 2]); timbunan_VALUE[objek_Rujukan + 2] = -1; } return; }
            if (perintah_kod == 182 && (Word_SMS(nama_pemalar, "send") || Word_SMS(nama_pemalar, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), objek_Rujukan = 빼기(2); if (!objek_VALUE(paket, 16) || !objek_VALUE(objek_Rujukan, 15)) return;
                int data_ARRAY = timbunan_VALUE[paket + 2], sah_kepanjangan = timbunan_VALUE[paket + 3], 열린파일번호 = timbunan_VALUE[objek_Rujukan + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nama_pemalar, "send")) {
                    if (!objek_VALUE(timbunan_VALUE[paket + 4], 14)) return;
                    if (sah_kepanjangan > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < sah_kepanjangan; Loop_INDEX++) 통신임시[Loop_INDEX] = timbunan_VALUE[data_ARRAY + 2 + Loop_INDEX];
                    if (ruang_pengguna.e_mel_rangkaian(열린파일번호, timbunan_VALUE[timbunan_VALUE[paket + 4] + 2], timbunan_VALUE[paket + 5], 통신임시, sah_kepanjangan) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int pemasukan_COUNT = ruang_pengguna.통신받기(열린파일번호, 통신임시, sah_kepanjangan > 512 ? 512 : sah_kepanjangan);
                    if (pemasukan_COUNT == -11) {
                        int 현재시각 = ruang_pengguna.밀리초();
                        if (timbunan_VALUE[objek_Rujukan + 4] == 0) timbunan_VALUE[objek_Rujukan + 4] = 현재시각 + 1;
                        if (timbunan_VALUE[objek_Rujukan + 3] > 0 && 현재시각 - (timbunan_VALUE[objek_Rujukan + 4] - 1) >= timbunan_VALUE[objek_Rujukan + 3]) { timbunan_VALUE[objek_Rujukan + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objek_Rujukan, 2); 넣기(paket, 2); bingkai_jawatan[bingkai_INDEX] = bingkai_suruhan[bingkai_INDEX]; ubah_permintaan = true; return;
                    }
                    timbunan_VALUE[objek_Rujukan + 4] = 0;
                    if (pemasukan_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) timbunan_VALUE[data_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    timbunan_VALUE[paket + 3] = pemasukan_COUNT; timbunan_VALUE[paket + 4] = e_mel_objek(통신임시[513]); timbunan_Rujukan[paket + 4] = 1; timbunan_VALUE[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        kegagalan_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objek_Rujukan) {
        int 현재시각 = ruang_pengguna.밀리초();
        if (timbunan_VALUE[objek_Rujukan + 5] == 0) timbunan_VALUE[objek_Rujukan + 5] = 현재시각 + 1;
        if (timbunan_VALUE[objek_Rujukan + 3] > 0 && 현재시각 - (timbunan_VALUE[objek_Rujukan + 5] - 1) >= timbunan_VALUE[objek_Rujukan + 3]) { timbunan_VALUE[objek_Rujukan + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        bingkai_jawatan[bingkai_INDEX] = bingkai_suruhan[bingkai_INDEX]; ubah_permintaan = true; return true;
    }
    static void 흐름호출(int pemilik, int nama_pemalar, int 서술상수, int perintah_kod) {
        boolean 수신쪽 = Word_SMS(pemilik, "java/net/ServerSocket"), strim = Word_SMS(pemilik, "java/io/InputStream") || Word_SMS(pemilik, "java/io/OutputStream");
        if (!strim && perintah_kod == 183 && Word_SMS(nama_pemalar, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { kegagalan_VALUE("unsupported socket constructor"); return; }
            int nombor_port = 빈여부 ? 0 : 빼기(1), e_mel_Rujukan = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objek_Rujukan = 빼기(2);
            if (!objek_VALUE(objek_Rujukan, 수신쪽 ? 18 : 17)) return;
            if (nombor_port < 0 || nombor_port > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objek_VALUE(e_mel_Rujukan, 14)) return;
            int rangkaian_e_mel_df3458bb = 이름지정여부 ? 주소해독(e_mel_Rujukan) : 주소지정여부 ? timbunan_VALUE[e_mel_Rujukan + 2] : 0x7f000001;
            if (RALAT || 던진객체 != 0) return;
            int 열린파일번호 = ruang_pengguna.strim_kawalan(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? ruang_pengguna.strim_kawalan(1, 열린파일번호, nombor_port) : ruang_pengguna.CONNECT_strim(열린파일번호, rangkaian_e_mel_df3458bb, nombor_port);
            if (처리값 < 0) { ruang_pengguna.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            timbunan_VALUE[objek_Rujukan + 2] = 열린파일번호; timbunan_VALUE[objek_Rujukan + 4] = nombor_port; timbunan_VALUE[objek_Rujukan + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!strim && Word_SMS(nama_pemalar, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else timbunan_VALUE[objek_Rujukan + 3] = 밀리초값; return; }
        if (!strim && Word_SMS(nama_pemalar, "close") && Word_SMS(서술상수, "()V")) { int objek_Rujukan = 빼기(2); if (objek_VALUE(objek_Rujukan, 수신쪽 ? 18 : 17) && timbunan_VALUE[objek_Rujukan + 2] >= 0) { ruang_pengguna.파일서술자닫기(timbunan_VALUE[objek_Rujukan + 2]); timbunan_VALUE[objek_Rujukan + 2] = -1; } return; }
        if (!strim && (Word_SMS(nama_pemalar, "getLocalPort") || Word_SMS(nama_pemalar, "getPort") || Word_SMS(nama_pemalar, "isClosed") || Word_SMS(nama_pemalar, "isConnected"))) {
            int objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(nama_pemalar, "isClosed") ? timbunan_VALUE[objek_Rujukan + 2] < 0 ? 1 : 0 : Word_SMS(nama_pemalar, "isConnected") ? timbunan_VALUE[objek_Rujukan + 6] : Word_SMS(nama_pemalar, "getPort") ? timbunan_VALUE[objek_Rujukan + 4] : timbunan_VALUE[objek_Rujukan + 2] < 0 ? -1 : ruang_pengguna.strim_kawalan(4, timbunan_VALUE[objek_Rujukan + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(nama_pemalar, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 18)) return; int 열린파일번호 = ruang_pengguna.strim_kawalan(3, timbunan_VALUE[objek_Rujukan + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objek_Rujukan)) 넣기(objek_Rujukan, 2); return; }
            timbunan_VALUE[objek_Rujukan + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = peruntuk_Storan(17, 5); if (RALAT) { ruang_pengguna.파일서술자닫기(열린파일번호); return; } timbunan_VALUE[반환값 + 2] = 열린파일번호; timbunan_VALUE[반환값 + 4] = ruang_pengguna.strim_kawalan(5, 열린파일번호, 0); timbunan_VALUE[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !strim && ((Word_SMS(nama_pemalar, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(nama_pemalar, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 17)) return; if (timbunan_VALUE[objek_Rujukan + 2] < 0 || timbunan_VALUE[objek_Rujukan + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = peruntuk_Storan(19, 4); if (RALAT) return; timbunan_VALUE[반환값 + 2] = objek_Rujukan; timbunan_Rujukan[반환값 + 2] = 1; timbunan_VALUE[반환값 + 3] = Word_SMS(nama_pemalar, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (strim) {
            boolean 읽기여부 = Word_SMS(nama_pemalar, "read"), teknologi_maklumat_tulis_operasi = Word_SMS(nama_pemalar, "write"), blok = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), teknologi_maklumat_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int pemasukan_COUNT = teknologi_maklumat_SUBARRAY ? 빼기(1) : 0, 시작변위 = teknologi_maklumat_SUBARRAY ? 빼기(1) : 0, data_ARRAY = blok || teknologi_maklumat_SUBARRAY ? 빼기(2) : 0;
            int data_VALUE = teknologi_maklumat_tulis_operasi && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objek_Rujukan = 빼기(2);
            if (!objek_VALUE(objek_Rujukan, 19)) return; int 부모참조 = timbunan_VALUE[objek_Rujukan + 2], 열린파일번호 = timbunan_VALUE[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nama_pemalar, "close") && Word_SMS(서술상수, "()V")) { ruang_pengguna.파일서술자닫기(열린파일번호); timbunan_VALUE[부모참조 + 2] = -1; return; }
            if (Word_SMS(nama_pemalar, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !teknologi_maklumat_tulis_operasi) || 읽기여부 != (timbunan_VALUE[objek_Rujukan + 3] == 0)) { kegagalan_VALUE("unsupported stream operation"); return; }
            if (blok || teknologi_maklumat_SUBARRAY) { if (!objek_VALUE(data_ARRAY, 20)) return; if (blok) pemasukan_COUNT = timbunan_VALUE[data_ARRAY + 1]; if (시작변위 < 0 || pemasukan_COUNT < 0 || 시작변위 > timbunan_VALUE[data_ARRAY + 1] - pemasukan_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else pemasukan_COUNT = 1;
            if (pemasukan_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Selesai_COUNT = teknologi_maklumat_tulis_operasi ? timbunan_VALUE[objek_Rujukan + 4] : 0, 처리값 = 0;
            while (Selesai_COUNT < pemasukan_COUNT) {
                처리값 = 읽기여부 ? ruang_pengguna.파일한바이트읽기(열린파일번호) : ruang_pengguna.파일한바이트쓰기(열린파일번호, blok || teknologi_maklumat_SUBARRAY ? timbunan_VALUE[data_ARRAY + 2 + 시작변위 + Selesai_COUNT] : data_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || teknologi_maklumat_SUBARRAY)) timbunan_VALUE[data_ARRAY + 2 + 시작변위 + Selesai_COUNT] = (byte)처리값;
                Selesai_COUNT++; if (읽기여부 && !(blok || teknologi_maklumat_SUBARRAY)) break;
            }
            if (처리값 == -11 && (teknologi_maklumat_tulis_operasi || Selesai_COUNT == 0)) {
                timbunan_VALUE[objek_Rujukan + 4] = Selesai_COUNT;
                if (흐름대기(부모참조)) { 넣기(objek_Rujukan, 2); if (blok || teknologi_maklumat_SUBARRAY) 넣기(data_ARRAY, 2); if (teknologi_maklumat_SUBARRAY) { 넣기(시작변위, 1); 넣기(pemasukan_COUNT, 1); } if (teknologi_maklumat_tulis_operasi && !(blok || teknologi_maklumat_SUBARRAY)) 넣기(data_VALUE, 1); } return;
            }
            timbunan_VALUE[objek_Rujukan + 4] = 0; timbunan_VALUE[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Selesai_COUNT == 0 && 처리값 == 256 ? -1 : blok || teknologi_maklumat_SUBARRAY ? Selesai_COUNT : 처리값, 1); return;
        }
        kegagalan_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nama_pemalar) {
        if (Word_SMS(nama_pemalar, "Melayu/Asli/Tetingkap")) return 24;
        if (Word_SMS(nama_pemalar, "Melayu/Asli/label")) return 26;
        if (Word_SMS(nama_pemalar, "Melayu/Asli/Butang")) return 27;
        if (Word_SMS(nama_pemalar, "Melayu/Asli/medan_teks")) return 28;
        if (Word_SMS(nama_pemalar, "Melayu/Asli/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nama_pemalar) {
        return 한국어화면종(nama_pemalar) != 0 || Word_SMS(nama_pemalar, "Melayu/Asli/화면구성요소") || Word_SMS(nama_pemalar, "Melayu/Asli/acara_baris");
    }
    static int 화면종(int nama_pemalar) {
        int 한국어종 = 한국어화면종(nama_pemalar); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nama_pemalar, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nama_pemalar, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nama_pemalar, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nama_pemalar, "javax/swing/JButton")) return 27;
        if (Word_SMS(nama_pemalar, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nama_pemalar, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nama_pemalar, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nama_pemalar) {
        return 화면종(nama_pemalar) != 0 || Word_SMS(nama_pemalar, "java/awt/Component") || Word_SMS(nama_pemalar, "java/awt/Container") || Word_SMS(nama_pemalar, "javax/swing/JComponent") || Word_SMS(nama_pemalar, "javax/swing/AbstractButton") || Word_SMS(nama_pemalar, "javax/swing/text/JTextComponent") || Word_SMS(nama_pemalar, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objek_Rujukan) { if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return false; if (timbunan_VALUE[objek_Rujukan] < 24 || timbunan_VALUE[objek_Rujukan] > 28) { kegagalan_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objek_Rujukan, int SMS_Rujukan) {
        if (SMS_Rujukan != 0 && !objek_VALUE(SMS_Rujukan, 1)) return;
        int pemasukan_COUNT = SMS_Rujukan == 0 ? 0 : timbunan_VALUE[SMS_Rujukan + 1]; if (pemasukan_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = timbunan_VALUE[SMS_Rujukan + 2 + Loop_INDEX];
        if (ruang_pengguna.화면글(timbunan_VALUE[objek_Rujukan + 2], 화면글임시, pemasukan_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        timbunan_VALUE[objek_Rujukan + 3] = SMS_Rujukan; timbunan_Rujukan[objek_Rujukan + 3] = 1;
    }
    static int 화면문자읽기(int objek_Rujukan) {
        int akaun_VALUE = timbunan_VALUE[objek_Rujukan + 2], pemasukan_COUNT = ruang_pengguna.화면연결(8, akaun_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (pemasukan_COUNT < 0) { kegagalan_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) { int 부호값 = ruang_pengguna.화면연결(9, akaun_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = peruntuk_Storan(1, 사용수); if (!RALAT) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) timbunan_VALUE[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Melayu 객체를 직접 만들고 kernel_VALUE 화면 기능에 연결한다. Swing objek_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int pemilik, int nama_pemalar, int 서술상수, int perintah_kod) {
        if (Word_SMS(pemilik, "Melayu/Asli/acara_baris")) {
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "나중에실행") && Word_SMS(서술상수, "(LMelayu/Asli/실행할일;)V")) {
                int tugas_cadangan = 빼기(2); if (!teknologi_maklumat_sah_objek(tugas_cadangan)) return;
                if (나중수 == 8) { kegagalan_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tugas_cadangan; return;
            }
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kegagalan_VALUE("지원하지 않는 Melayu 화면 일정 호출"); return;
        }
        if (Word_SMS(pemilik, "Melayu/Asli/동작알림")) {
            int 알림 = 빼기(2); if (!objek_VALUE(알림, 29) || timbunan_VALUE[알림 + 3] == 0) return;
            if (Word_SMS(nama_pemalar, "sumber_peristiwa") && Word_SMS(서술상수, "()LMelayu/Asli/화면구성요소;")) 넣기(timbunan_VALUE[알림 + 2], 2);
            else if (Word_SMS(nama_pemalar, "perintah_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(timbunan_VALUE[알림 + 2]), 2);
            else if (Word_SMS(nama_pemalar, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kegagalan_VALUE("지원하지 않는 Melayu Aksi 알림 호출"); return;
        }
        if (perintah_kod == 183 && Word_SMS(nama_pemalar, "<init>")) {
            int 종류 = 한국어화면종(pemilik), 받이 = 0, 가로 = 0, Menegak_jawatan = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (ruang_pengguna.화면너비() - 폭) / 2; Menegak_jawatan = (ruang_pengguna.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILMelayu/Asli/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Menegak_jawatan = 빼기(1); 가로 = 빼기(1);
            } else { kegagalan_VALUE("지원하지 않는 Melayu 화면 생성자"); return; }
            int Teks = 빼기(2), unsur_VALUE = 빼기(2); if (!화면객체(unsur_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Menegak_jawatan < 0 || 폭 > ruang_pengguna.화면너비() - 가로 || 높이 > ruang_pengguna.화면높이() - Menegak_jawatan) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = ruang_pengguna.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { kegagalan_VALUE("화면 unsur_VALUE 자리가 가득 찼습니다"); return; }
            timbunan_VALUE[unsur_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = unsur_VALUE;
            timbunan_VALUE[unsur_VALUE + 5] = 가로; timbunan_VALUE[unsur_VALUE + 6] = Menegak_jawatan; timbunan_VALUE[unsur_VALUE + 7] = 폭; timbunan_VALUE[unsur_VALUE + 8] = 높이; timbunan_VALUE[unsur_VALUE + 10] = 2;
            timbunan_VALUE[unsur_VALUE + 4] = 받이; timbunan_Rujukan[unsur_VALUE + 4] = 1; timbunan_VALUE[unsur_VALUE + 12] = 1;
            ruang_pengguna.화면연결(1, INDEX, 가로, Menegak_jawatan, 폭, 높이);
            if (종류 == 24) ruang_pengguna.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(unsur_VALUE, Teks); return;
        }
        if (perintah_kod != 182) { kegagalan_VALUE("잘못된 Melayu 화면 호출 Perintah"); return; }
        if (Word_SMS(nama_pemalar, "tulis_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Teks = 빼기(2), unsur_VALUE = 빼기(2); if (화면객체(unsur_VALUE)) 화면문자설정(unsur_VALUE, Teks); return;
        }
        if (Word_SMS(nama_pemalar, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int unsur_VALUE = 빼기(2); if (화면객체(unsur_VALUE)) 넣기(화면문자읽기(unsur_VALUE), 2); return;
        }
        if (Word_SMS(nama_pemalar, "동작맡기기") && Word_SMS(서술상수, "(LMelayu/Asli/동작받이;)V")) {
            int 받이 = 빼기(2), unsur_VALUE = 빼기(2);
            if (화면객체(unsur_VALUE)) { timbunan_VALUE[unsur_VALUE + 4] = 받이; timbunan_Rujukan[unsur_VALUE + 4] = 1; timbunan_VALUE[unsur_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(nama_pemalar, "tambah_unsur") && Word_SMS(서술상수, "(LMelayu/Asli/화면구성요소;)V")) {
            int anak_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(anak_VALUE) || !화면객체(부모)) return;
            if (ruang_pengguna.화면연결(2, timbunan_VALUE[부모 + 2], timbunan_VALUE[anak_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            timbunan_VALUE[anak_VALUE + 11] = 부모; timbunan_Rujukan[anak_VALUE + 11] = 1; return;
        }
        if (Word_SMS(nama_pemalar, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Menegak_jawatan = 빼기(1), 가로 = 빼기(1), unsur_VALUE = 빼기(2); if (!화면객체(unsur_VALUE)) return;
            if (ruang_pengguna.화면연결(1, timbunan_VALUE[unsur_VALUE + 2], 가로, Menegak_jawatan, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            timbunan_VALUE[unsur_VALUE + 5] = 가로; timbunan_VALUE[unsur_VALUE + 6] = Menegak_jawatan; timbunan_VALUE[unsur_VALUE + 7] = 폭; timbunan_VALUE[unsur_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(nama_pemalar, "tayang_tetingkap") || Word_SMS(nama_pemalar, "Tutup")) && Word_SMS(서술상수, "()V")) {
            boolean kebolehlihatan_VALUE = Word_SMS(nama_pemalar, "tayang_tetingkap"); int unsur_VALUE = 빼기(2); if (!화면객체(unsur_VALUE)) return;
            if (ruang_pengguna.화면연결(kebolehlihatan_VALUE ? 3 : 4, timbunan_VALUE[unsur_VALUE + 2], kebolehlihatan_VALUE ? 1 : 0, 0, 0, 0) < 0) { kegagalan_VALUE("화면은 interaktif 명령에서 실행해야 합니다"); return; }
            timbunan_VALUE[unsur_VALUE + 9] = kebolehlihatan_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(nama_pemalar, "보이는가") && Word_SMS(서술상수, "()Z")) { int unsur_VALUE = 빼기(2); if (화면객체(unsur_VALUE)) 넣기(timbunan_VALUE[unsur_VALUE + 9], 1); return; }
        kegagalan_VALUE("지원하지 않는 Melayu 화면 kaedah_VALUE");
    }
    static void 화면호출(int pemilik, int nama_pemalar, int 서술상수, int perintah_kod) {
        if (Word_SMS(pemilik, "javax/swing/SwingUtilities")) {
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objek_Rujukan = 빼기(2); if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return; if (나중수 == 8) { kegagalan_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objek_Rujukan; return; }
            if (perintah_kod == 184 && Word_SMS(nama_pemalar, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kegagalan_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(pemilik, "java/awt/event/ActionEvent")) {
            int objek_Rujukan = 빼기(2); if (!objek_VALUE(objek_Rujukan, 29)) return;
            if (Word_SMS(nama_pemalar, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(timbunan_VALUE[objek_Rujukan + 2], 2);
            else if (Word_SMS(nama_pemalar, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(timbunan_VALUE[objek_Rujukan + 2]), 2);
            else if (Word_SMS(nama_pemalar, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kegagalan_VALUE("unsupported ActionEvent method"); return;
        }
        if (perintah_kod == 183 && Word_SMS(nama_pemalar, "<init>")) {
            int COLUMNS = 0, SMS_Rujukan = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Rujukan = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Rujukan = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { kegagalan_VALUE("unsupported Swing constructor"); return; }
            int objek_Rujukan = 빼기(2); if (!teknologi_maklumat_sah_objek(objek_Rujukan)) return;
            if (timbunan_VALUE[objek_Rujukan] == 30) { kegagalan_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objek_Rujukan) || COLUMNS < 0) return;
            int akaun_VALUE = ruang_pengguna.화면연결(0, timbunan_VALUE[objek_Rujukan] - 23, 0, 0, 0, 0);
            if (akaun_VALUE < 1 || akaun_VALUE > 32) { kegagalan_VALUE("GUI widget slots exhausted"); return; }
            timbunan_VALUE[objek_Rujukan + 2] = akaun_VALUE; 화면참조[akaun_VALUE - 1] = objek_Rujukan; timbunan_VALUE[objek_Rujukan + 5] = timbunan_VALUE[objek_Rujukan] == 24 ? 130 : 16; timbunan_VALUE[objek_Rujukan + 6] = timbunan_VALUE[objek_Rujukan] == 24 ? 110 : 16;
            timbunan_VALUE[objek_Rujukan + 7] = timbunan_VALUE[objek_Rujukan] == 24 ? 380 : 220; timbunan_VALUE[objek_Rujukan + 8] = timbunan_VALUE[objek_Rujukan] == 24 ? 240 : 28; timbunan_VALUE[objek_Rujukan + 10] = 1;
            화면문자설정(objek_Rujukan, SMS_Rujukan); return;
        }
        if (Word_SMS(nama_pemalar, "setText") || Word_SMS(nama_pemalar, "setTitle")) { int SMS_Rujukan = 빼기(2), objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objek_Rujukan, SMS_Rujukan); return; }
        if (Word_SMS(nama_pemalar, "getText") || Word_SMS(nama_pemalar, "getTitle")) { int objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objek_Rujukan), 2); return; }
        if (Word_SMS(nama_pemalar, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan)) { timbunan_VALUE[objek_Rujukan + 4] = 수신참조; timbunan_Rujukan[objek_Rujukan + 4] = 1; } return; }
        if (Word_SMS(nama_pemalar, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan)) 넣기(objek_Rujukan, 2); return; }
        if (Word_SMS(nama_pemalar, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Navigasi_Rujukan = 빼기(2), objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan) && Navigasi_Rujukan != 0) kegagalan_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nama_pemalar, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Navigasi_syarat = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Navigasi_syarat) 빼기(2);
            int anak_Rujukan = 빼기(2), objek_Rujukan = 빼기(2); if (!화면객체(anak_Rujukan) || !화면객체(objek_Rujukan)) return;
            if (ruang_pengguna.화면연결(2, timbunan_VALUE[objek_Rujukan + 2], timbunan_VALUE[anak_Rujukan + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            timbunan_VALUE[anak_Rujukan + 11] = objek_Rujukan; timbunan_Rujukan[anak_Rujukan + 11] = 1; if (!Navigasi_syarat) 넣기(anak_Rujukan, 2); return;
        }
        if (Word_SMS(nama_pemalar, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), koordinat_x = 빼기(1), objek_Rujukan = 빼기(2); if (!화면객체(objek_Rujukan)) return;
            if (ruang_pengguna.화면연결(1, timbunan_VALUE[objek_Rujukan + 2], koordinat_x, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            timbunan_VALUE[objek_Rujukan + 5] = koordinat_x; timbunan_VALUE[objek_Rujukan + 6] = Y_koordinat; timbunan_VALUE[objek_Rujukan + 7] = 너비; timbunan_VALUE[objek_Rujukan + 8] = 높이; return;
        }
        if (Word_SMS(nama_pemalar, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objek_Rujukan = 빼기(2); if (!화면객체(objek_Rujukan)) return;
            if (ruang_pengguna.화면연결(1, timbunan_VALUE[objek_Rujukan + 2], timbunan_VALUE[objek_Rujukan + 5], timbunan_VALUE[objek_Rujukan + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { timbunan_VALUE[objek_Rujukan + 7] = 너비; timbunan_VALUE[objek_Rujukan + 8] = 높이; } return;
        }
        if (Word_SMS(nama_pemalar, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objek_Rujukan = 빼기(2); if (!화면객체(objek_Rujukan)) return; if (상대배치 != 0) { kegagalan_VALUE("only screen centering supported"); return; } timbunan_VALUE[objek_Rujukan + 5] = (ruang_pengguna.화면너비() - timbunan_VALUE[objek_Rujukan + 7]) / 2; timbunan_VALUE[objek_Rujukan + 6] = (ruang_pengguna.화면높이() - timbunan_VALUE[objek_Rujukan + 8]) / 2; ruang_pengguna.화면연결(1, timbunan_VALUE[objek_Rujukan + 2], timbunan_VALUE[objek_Rujukan + 5], timbunan_VALUE[objek_Rujukan + 6], timbunan_VALUE[objek_Rujukan + 7], timbunan_VALUE[objek_Rujukan + 8]); return; }
        if (Word_SMS(nama_pemalar, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int dasar = 빼기(1), objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan)) { if (dasar < 0 || dasar > 3) 예외던짐(9, "close policy"); else { timbunan_VALUE[objek_Rujukan + 10] = dasar; ruang_pengguna.화면연결(7, timbunan_VALUE[objek_Rujukan + 2], dasar, 0, 0, 0); } } return; }
        if (Word_SMS(nama_pemalar, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int data_VALUE = 빼기(1), objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan)) { int 처리값 = ruang_pengguna.화면연결(3, timbunan_VALUE[objek_Rujukan + 2], data_VALUE, 0, 0, 0); if (처리값 < 0) kegagalan_VALUE("Swing requires a standalone interactive command"); else timbunan_VALUE[objek_Rujukan + 9] = data_VALUE; } return; }
        if (Word_SMS(nama_pemalar, "dispose") && Word_SMS(서술상수, "()V")) { int objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan)) { ruang_pengguna.화면연결(4, timbunan_VALUE[objek_Rujukan + 2], 0, 0, 0, 0); timbunan_VALUE[objek_Rujukan + 9] = 0; } return; }
        if (Word_SMS(nama_pemalar, "repaint") || Word_SMS(nama_pemalar, "validate")) { int objek_Rujukan = 빼기(2); if (!화면객체(objek_Rujukan) || !Word_SMS(서술상수, "()V")) return; ruang_pengguna.화면연결(1, timbunan_VALUE[objek_Rujukan + 2], timbunan_VALUE[objek_Rujukan + 5], timbunan_VALUE[objek_Rujukan + 6], timbunan_VALUE[objek_Rujukan + 7], timbunan_VALUE[objek_Rujukan + 8]); return; }
        if (Word_SMS(nama_pemalar, "isVisible") && Word_SMS(서술상수, "()Z")) { int objek_Rujukan = 빼기(2); if (화면객체(objek_Rujukan)) 넣기(timbunan_VALUE[objek_Rujukan + 9], 1); return; }
        kegagalan_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int sasaran_e_mel, int 사건번호, boolean Melayu) {
        if (sasaran_e_mel < 1 || timbunan_VALUE[sasaran_e_mel] < 32) { kegagalan_VALUE("Java event listener required"); return; }
        int fail_INDEX = nama_kaedah(timbunan_VALUE[sasaran_e_mel] - 32, 사건번호 == 0 ? (Melayu ? "Lakukan" : "run") : (Melayu ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Melayu ? "(LMelayu/Asli/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fail_INDEX < 0) { kegagalan_VALUE("event callback missing"); return; }
        현재가닥 = 0; urutan_COUNT = 1; bingkai_INDEX = 0; urutan_status[0] = 1; bingkai_tindan[0] = 0; bingkai_kunci[0] = mengasal_bingkai[0] = 0; ubah_permintaan = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { setempat_VALUE[Loop_INDEX] = setempat_TYPE[Loop_INDEX] = 0; }
        bingkai_kaedah[0] = fail_INDEX; bingkai_jawatan[0] = kaedah_Mula[fail_INDEX]; setempat_VALUE[0] = sasaran_e_mel; setempat_TYPE[0] = 2;
        if (사건번호 != 0) { setempat_VALUE[1] = 사건번호; setempat_TYPE[1] = 2; }
        사건중 = true; laksanakan_perintah(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!RALAT) {
            if (나중수 > 0) { int sasaran_e_mel = 나중실행[0], Melayu = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(sasaran_e_mel, 0, Melayu != 0); continue; }
            if (ruang_pengguna.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = ruang_pengguna.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { kegagalan_VALUE("GUI event I/O failed"); return; }
            int akaun_VALUE = 사건번호 & 65535; if (akaun_VALUE < 1 || akaun_VALUE > 32) continue; int objek_Rujukan = 화면참조[akaun_VALUE - 1]; if (objek_Rujukan == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (timbunan_VALUE[objek_Rujukan + 10] != 0) timbunan_VALUE[objek_Rujukan + 9] = 0;
                if (timbunan_VALUE[objek_Rujukan + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && timbunan_VALUE[화면참조[Loop_INDEX]] == 24) ruang_pengguna.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (timbunan_VALUE[objek_Rujukan + 4] != 0) {
                int README_Rujukan = peruntuk_Storan(29, 2); if (RALAT) return; timbunan_VALUE[README_Rujukan + 2] = objek_Rujukan; timbunan_VALUE[README_Rujukan + 3] = timbunan_VALUE[objek_Rujukan + 12]; timbunan_Rujukan[README_Rujukan + 2] = 1; 사건실행(timbunan_VALUE[objek_Rujukan + 4], README_Rujukan, timbunan_VALUE[objek_Rujukan + 12] != 0);
            }
        }
    }
    public static int Jalan() {
        if (ruang_pengguna.인수개수() == 1 && 자바도구.같음(ruang_pengguna.인수(0), "-version")) {
            ruang_pengguna.Tulis("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (ruang_pengguna.인수개수() < 1) { ruang_pengguna.Tulis("Usage: java CLASS [ARGS]\n"); return 2; }
        pemasukan_Kelas_Takrif = muat_Kelas_Takrif(hos_aksara(ruang_pengguna.인수(0))); if (RALAT || pemasukan_Kelas_Takrif < 0) return 1;
        int titik_permulaan_VALUE = nama_kaedah(pemasukan_Kelas_Takrif, "Jalan", "()V");
        boolean 한국어진입 = titik_permulaan_VALUE >= 0 && (kaedah_capai[titik_permulaan_VALUE] & 9) == 9;
        if (!한국어진입) titik_permulaan_VALUE = nama_kaedah(pemasukan_Kelas_Takrif, "main", "([Ljava/lang/String;)V");
        if (titik_permulaan_VALUE < 0 || (kaedah_capai[titik_permulaan_VALUE] & 9) != 9) kegagalan_VALUE("public static void Jalan() or main(String[] args) required");
        if (RALAT) return 1;
        int 인수 = peruntuk_Storan(3, ruang_pengguna.인수개수() - 1); ARRAY_unsur[인수] = -1;
        for (int 수 = 1; 수 < ruang_pengguna.인수개수() && !RALAT; 수++) timbunan_VALUE[인수 + 1 + 수] = hos_aksara(ruang_pengguna.인수(수));
        bingkai_INDEX = 0; bingkai_kaedah[0] = titik_permulaan_VALUE; bingkai_jawatan[0] = kaedah_Mula[titik_permulaan_VALUE]; setempat_VALUE[0] = 한국어진입 ? 0 : 인수; setempat_TYPE[0] = 한국어진입 ? 0 : 2;
        urutan_status[0] = 1; urutan_objek[0] = peruntuk_Storan(13, 2);
        laksanakan_perintah(); if (!RALAT) 화면사건들(); return RALAT ? 1 : 0;
    }
}
