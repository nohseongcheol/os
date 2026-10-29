// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. berkas/operand_tumpuk/Referensi/cabang 경계를 Jalankan_perintah 중 검사한다. */
public final class 자바가상기계 {
    static int[] berkas = new int[16 * 16384], file_temporer = new int[16384], nama_file_SMS = new int[512];
    static int[] konstanta_tag = new int[8192], 상가 = new int[8192], konstanta_SECOND_VALUE = new int[8192], string_Referensi = new int[8192];
    static int[] metode_nama_SMS = new int[512], metode_TYPE = new int[512], metode_akses = new int[512], metode_pemilik = new int[512];
    static int[] metode_Mulai = new int[512], metode_mengakhiri = new int[512], metode_tumpuk = new int[512], 함수지역 = new int[512];
    static int[] metode_argumen_COUNT = new int[512], metode_argumen_TYPE = new int[8192], metode_kembalikan = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokal_VALUE = new int[16384], lokal_TYPE = new int[16384], operand_tumpuk_VALUE = new int[16384], operand_tumpuk_TYPE = new int[16384];
    static int[] bingkai_metode = new int[128], bingkai_posisi = new int[128], bingkai_tumpuk = new int[128], bingkai_instruksi = new int[128], berinisial_bingkai = new int[128];
    static int[] Kelas_Definisi_nama = new int[16], Kelas_Definisi_ukuran = new int[16], Kelas_Definisi_induk = new int[16], Kelas_Definisi_Status = new int[16], Kelas_slot_COUNT = new int[16], berinisial_Kelas_Definisi = new int[16];
    static int[] Kelas_antarmuka = new int[16 * 16], Kelas_antarmuka_COUNT = new int[16];
    static int[] slot_nama = new int[512], slot_TYPE = new int[512], slot_pemilik = new int[512], slot_Izin = new int[512], slot_posisi = new int[512], slot_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], barisan_elemen = new int[32768], Store_bilangan_bulat = new int[256];
    static int Ukuran, 읽기위치, metode_COUNT, nama_kelas, bingkai_INDEX = -1, 힙끝 = 1, kembalikan_TYPE;
    static int Kelas_Definisi_COUNT, slot_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, tampilan_COUNT, Koleksi_COUNT;
    static int saat_ini_alur, alur_COUNT = 1, entri_Kelas_Definisi;
    static int[] alur_bingkai = new int[4], alur_Status = new int[4], alur_objek = new int[4], alur_target = new int[4], 가닥대기 = new int[4];
    static boolean galat, ubah_permintaan;
    static int[] kunci_pemilik = new int[32768], 잠금깊이 = new int[32768], bingkai_kunci = new int[128], Kelas_kunci = new int[16], Kelas_alur = new int[16];

    static void kegagalan_VALUE(String Kata_SMS) {
        if (galat) return;
        int area_CODE = 0;
        if (자바도구.같음(Kata_SMS, "ArithmeticException: / by zero")) area_CODE = 4;
        if (자바도구.같음(Kata_SMS, "NullPointerException") || 자바도구.같음(Kata_SMS, "null or invalid array")) area_CODE = 5;
        if (자바도구.같음(Kata_SMS, "ArrayIndexOutOfBoundsException")) area_CODE = 7;
        if (자바도구.같음(Kata_SMS, "StringIndexOutOfBoundsException")) area_CODE = 8;
        if (자바도구.같음(Kata_SMS, "NumberFormatException")) area_CODE = 10;
        if (자바도구.같음(Kata_SMS, "FileNotFoundException: file open failed")) area_CODE = 12;
        if (자바도구.같음(Kata_SMS, "IOException: stream closed") || 자바도구.같음(Kata_SMS, "IOException: read failed") || 자바도구.같음(Kata_SMS, "IOException: write failed")) area_CODE = 11;
        if (자바도구.같음(Kata_SMS, "ClassCastException")) area_CODE = 14;
        if (자바도구.같음(Kata_SMS, "NegativeArraySizeException")) area_CODE = 15;
        if (area_CODE != 0 && bingkai_INDEX >= 0) { 예외던짐(area_CODE, Kata_SMS); return; }
        ruang_pengguna.Tulis("JVM error: "); ruang_pengguna.Tulis(Kata_SMS); ruang_pengguna.tulis_karakter_VALUE(10); galat = true;
    }
    static boolean klip(int jalankan, int panjang_VALUE) {
        if (jalankan < 0 || jalankan >= berkas.length || panjang_VALUE < 0) return false;
        int Kelas_Definisi = jalankan / 16384;
        return jalankan % 16384 <= Kelas_Definisi_ukuran[Kelas_Definisi] && panjang_VALUE <= Kelas_Definisi_ukuran[Kelas_Definisi] - jalankan % 16384;
    }
    static int byte_VALUE() {
        if (!klip(읽기위치, 1)) { kegagalan_VALUE("truncated class file"); return 0; }
        return berkas[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int bilangan_bulat() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int panjang_VALUE) { if (!klip(읽기위치, panjang_VALUE)) kegagalan_VALUE("invalid attribute size"); else 읽기위치 += panjang_VALUE; }
    static boolean cek_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_tag.length || konstanta_tag[수] != 종류) { kegagalan_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_rentang(int jalankan, int panjang_VALUE, String Kata_SMS) {
        if (!klip(jalankan, panjang_VALUE)) return false;
        int 읽는자리 = jalankan, 끝 = jalankan + panjang_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Kata_SMS.length(); Loop_INDEX++) {
            int kode_karakter = Kata_SMS.charAt(Loop_INDEX);
            if (kode_karakter > 0 && kode_karakter < 128) { if (읽는자리 >= 끝 || berkas[읽는자리++] != kode_karakter) return false; }
            else if (kode_karakter < 2048) {
                if (읽는자리 + 2 > 끝 || berkas[읽는자리++] != (192 | (kode_karakter >> 6)) || berkas[읽는자리++] != (128 | (kode_karakter & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || berkas[읽는자리++] != (224 | (kode_karakter >> 12)) || berkas[읽는자리++] != (128 | ((kode_karakter >> 6) & 63)) || berkas[읽는자리++] != (128 | (kode_karakter & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Kata_SMS(int konstanta_VALUE, String Kata_SMS) { return cek_konstanta(konstanta_VALUE, 1) && SMS_rentang(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Kata_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!cek_konstanta(가, 1) || !cek_konstanta(SECOND_operand, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < konstanta_SECOND_VALUE[가]; 수++) if (berkas[상가[가] + 수] != berkas[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int nama_kelas_SMS(int 수) { return cek_konstanta(수, 7) && cek_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Referensi_nama(int 수) { return cek_konstanta(수, 12) && cek_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Referensi_TYPE(int 수) { return cek_konstanta(수, 12) && cek_konstanta(konstanta_SECOND_VALUE[수], 1) ? konstanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean kosong_TYPE) {
        if (읽기위치 >= 끝) { kegagalan_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && kosong_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int jalankan = 읽기위치;
            while (읽기위치 < 끝 && berkas[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == jalankan) kegagalan_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        kegagalan_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int fungsi_VALUE) {
        int 이전 = 읽기위치, 수 = metode_TYPE[fungsi_VALUE];
        if (!cek_konstanta(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[수];
        if (byte_VALUE() != '(') kegagalan_VALUE("invalid method descriptor");
        int item_COUNT = 0;
        while (!galat && 읽기위치 < 끝 && berkas[읽기위치] != ')') {
            if (item_COUNT == 16) { kegagalan_VALUE("too many method arguments"); break; }
            metode_argumen_TYPE[fungsi_VALUE * 16 + item_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') kegagalan_VALUE("invalid method descriptor");
        metode_kembalikan[fungsi_VALUE] = 서술형(끝, true); metode_argumen_COUNT[fungsi_VALUE] = item_COUNT;
        if (읽기위치 != 끝) kegagalan_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metode_pemilik[bingkai_metode[bingkai_INDEX]] * 512 + 명짧(); }
    static void lompati_atribut() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !galat; 수++) { cek_konstanta(상번호(), 1); 건너(bilangan_bulat()); }
    }
    static int perintah_panjang(int VALUE) {
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
    static int posisi_bilangan_bulat(int 읽는자리) {
        if (!klip(읽는자리, 4)) { kegagalan_VALUE("truncated bytecode operand"); return 0; }
        return berkas[읽는자리] << 24 | berkas[읽는자리 + 1] << 16 | berkas[읽는자리 + 2] << 8 | berkas[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int jalankan, int 끝) {
        int VALUE = berkas[읽는자리], panjang_VALUE = perintah_panjang(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_posisi = 읽는자리 + 1;
            while ((BASE_posisi - jalankan) % 4 != 0) BASE_posisi++;
            if (끝 - BASE_posisi < (VALUE == 170 ? 12 : 8)) return 0;
            int entri_COUNT = VALUE == 170 ? posisi_bilangan_bulat(BASE_posisi + 8) - posisi_bilangan_bulat(BASE_posisi + 4) + 1 : posisi_bilangan_bulat(BASE_posisi + 4);
            if (entri_COUNT < 0 || entri_COUNT > 2048) return 0;
            panjang_VALUE = BASE_posisi - 읽는자리 + (VALUE == 170 ? 12 + 4 * entri_COUNT : 8 + 8 * entri_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Kata_data = berkas[읽는자리 + 1]; panjang_VALUE = Kata_data == 132 ? 6 : (Kata_data == 21 || Kata_data == 25 || Kata_data == 54 || Kata_data == 58) ? 4 : 0;
        }
        return panjang_VALUE > 0 && panjang_VALUE <= 끝 - 읽는자리 ? panjang_VALUE : 0;
    }
    static void cek_tujuan_VALUE(int tujuan_VALUE, int fungsi_VALUE) {
        if (tujuan_VALUE < metode_Mulai[fungsi_VALUE] || tujuan_VALUE >= metode_mengakhiri[fungsi_VALUE] || 경계[tujuan_VALUE] != fungsi_VALUE + 1) kegagalan_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Kelas_Definisi) {
        현재읽는종 = Kelas_Definisi; 읽기위치 = Kelas_Definisi * 16384; Ukuran = 읽기위치 + Kelas_Definisi_ukuran[Kelas_Definisi];
        if (bilangan_bulat() != 0xcafebabe) { kegagalan_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versi_VALUE = 짧은수();
        if (versi_VALUE < 45 || versi_VALUE > 52 || 부판 != 0) { kegagalan_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstanta_COUNT = 짧은수(), BASE_posisi = Kelas_Definisi * 512;
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { kegagalan_VALUE("constant pool limit (511)"); return; }
        for (int entri_COUNT = 1; entri_COUNT < konstanta_COUNT && !galat; entri_COUNT++) {
            int 수 = BASE_posisi + entri_COUNT, 종류 = byte_VALUE(); konstanta_tag[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = bilangan_bulat();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstanta_SECOND_VALUE[수] = 상번호(); }
            else kegagalan_VALUE("unsupported constant type");
        }
        int izin_VALUE = 짧은수();
        if ((izin_VALUE & (0x2000 | 0x4000)) != 0) kegagalan_VALUE("annotation/enum class unsupported");
        Kelas_Definisi_nama[Kelas_Definisi] = nama_kelas_SMS(상번호());
        Kelas_Definisi_induk[Kelas_Definisi] = nama_kelas_SMS(상번호());
        int antarmuka_COUNT = 짧은수(); if (antarmuka_COUNT > 16) { kegagalan_VALUE("interface count limit"); return; }
        Kelas_antarmuka_COUNT[Kelas_Definisi] = antarmuka_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < antarmuka_COUNT; Loop_INDEX++) Kelas_antarmuka[Kelas_Definisi * 16 + Loop_INDEX] = nama_kelas_SMS(상번호());
        int bidang_COUNT = 짧은수();
        if (bidang_COUNT > 512 - slot_COUNT) { kegagalan_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < bidang_COUNT && !galat; Loop_INDEX++) {
            int file_INDEX = slot_COUNT++; slot_pemilik[file_INDEX] = Kelas_Definisi; slot_Izin[file_INDEX] = 짧은수(); slot_nama[file_INDEX] = 상번호(); slot_TYPE[file_INDEX] = 상번호();
            cek_konstanta(slot_nama[file_INDEX], 1); cek_konstanta(slot_TYPE[file_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[slot_TYPE[file_INDEX]]; int area_CODE = 서술형(읽기위치 + konstanta_SECOND_VALUE[slot_TYPE[file_INDEX]], false); 읽기위치 = 보존값;
            if ((slot_Izin[file_INDEX] & 8) == 0) slot_posisi[file_INDEX] = Kelas_slot_COUNT[Kelas_Definisi]++;
            int atribut_data = 짧은수();
            for (int dalam_posisi = 0; dalam_posisi < atribut_data && !galat; dalam_posisi++) {
                int nama_konstanta = 상번호(), 유효길이 = bilangan_bulat();
                if (Kata_SMS(nama_konstanta, "ConstantValue") && 유효길이 == 2) {
                    int data_VALUE = 상번호();
                    if (area_CODE == 1 && cek_konstanta(data_VALUE, 3)) slot_data[file_INDEX] = 상가[data_VALUE];
                    else if (area_CODE == 2 && cek_konstanta(data_VALUE, 8)) slot_data[file_INDEX] = konstanta_SMS(상가[data_VALUE]);
                } else 건너(유효길이);
            }
        }
        int item_COUNT = 짧은수();
        if (item_COUNT > 512 - metode_COUNT) { kegagalan_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < item_COUNT && !galat; Loop_INDEX++) {
            int 수 = metode_COUNT++; metode_pemilik[수] = Kelas_Definisi;
            metode_akses[수] = 짧은수(); metode_nama_SMS[수] = 상번호(); metode_TYPE[수] = 상번호();
            cek_konstanta(metode_nama_SMS[수], 1); 서술읽기(수);
            if ((metode_akses[수] & 8) == 0) {
                if (metode_argumen_COUNT[수] == 16) { kegagalan_VALUE("too many instance method arguments"); return; }
                for (int Perbandingan_posisi = metode_argumen_COUNT[수]; Perbandingan_posisi > 0; Perbandingan_posisi--) metode_argumen_TYPE[수 * 16 + Perbandingan_posisi] = metode_argumen_TYPE[수 * 16 + Perbandingan_posisi - 1];
                metode_argumen_TYPE[수 * 16] = 2; metode_argumen_COUNT[수]++;
            }
            if ((metode_akses[수] & 0x100) != 0) kegagalan_VALUE("user native method unsupported");
            if (Kata_SMS(metode_nama_SMS[수], "<clinit>")) berinisial_Kelas_Definisi[Kelas_Definisi] = 수 + 1;
            for (int depan_VALUE = 0; depan_VALUE < 수; depan_VALUE++) if (metode_pemilik[depan_VALUE] == Kelas_Definisi && 같은말(metode_nama_SMS[depan_VALUE], metode_nama_SMS[수]) && 같은말(metode_TYPE[depan_VALUE], metode_TYPE[수])) kegagalan_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int nilai_atribut = 0; nilai_atribut < atribut_COUNT && !galat; nilai_atribut++) {
                int Nama_2 = 상번호(), panjang_VALUE = bilangan_bulat(), jalankan = 읽기위치;
                if (!klip(jalankan, panjang_VALUE)) { kegagalan_VALUE("truncated method attribute"); break; }
                if (Kata_SMS(Nama_2, "Code")) {
                    if (metode_Mulai[수] != 0) kegagalan_VALUE("duplicate Code attribute");
                    metode_tumpuk[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_panjang = bilangan_bulat();
                    if (metode_tumpuk[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metode_argumen_COUNT[수]
                        || CODE_panjang < 1 || CODE_panjang > 8192) kegagalan_VALUE("method memory limits exceeded");
                    metode_Mulai[수] = 읽기위치; 건너(CODE_panjang); metode_mengakhiri[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { kegagalan_VALUE("exception table limit"); return; }
                    for (int dalam_posisi = 0; dalam_posisi < 잡는수; dalam_posisi++) {
                        int kesalahan_Referensi = 잡기수++; 잡기함수[kesalahan_Referensi] = 수;
                        잡기시작[kesalahan_Referensi] = metode_Mulai[수] + 짧은수(); 잡기끝[kesalahan_Referensi] = metode_Mulai[수] + 짧은수();
                        잡기위치[kesalahan_Referensi] = metode_Mulai[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[kesalahan_Referensi] = 부호값 == 0 ? 0 : nama_kelas_SMS(부호값);
                    }
                    lompati_atribut();
                    if (읽기위치 != jalankan + panjang_VALUE) kegagalan_VALUE("Code attribute size mismatch");
                } else 건너(panjang_VALUE);
            }
            if ((metode_akses[수] & 0x400) != 0) continue;
            if (metode_Mulai[수] == 0) kegagalan_VALUE("missing Code attribute");
            int slot_entri = metode_Mulai[수];
            while (slot_entri < metode_mengakhiri[수] && !galat) {
                int panjang_VALUE = 길이읽기(slot_entri, metode_Mulai[수], metode_mengakhiri[수]);
                if (panjang_VALUE == 0) { kegagalan_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_entri] = 수 + 1; slot_entri += panjang_VALUE;
            }
            slot_entri = metode_Mulai[수];
            while (slot_entri < metode_mengakhiri[수] && !galat) {
                int VALUE = berkas[slot_entri];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) cek_tujuan_VALUE(slot_entri + (short)(berkas[slot_entri + 1] << 8 | berkas[slot_entri + 2]), 수);
                if (VALUE == 200) cek_tujuan_VALUE(slot_entri + posisi_bilangan_bulat(slot_entri + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = slot_entri + 1; while ((읽는자리 - metode_Mulai[수]) % 4 != 0) 읽는자리++;
                    cek_tujuan_VALUE(slot_entri + posisi_bilangan_bulat(읽는자리), 수);
                    int entri_COUNT = VALUE == 170 ? posisi_bilangan_bulat(읽는자리 + 8) - posisi_bilangan_bulat(읽는자리 + 4) + 1 : posisi_bilangan_bulat(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int dalam_posisi = 0; dalam_posisi < entri_COUNT; dalam_posisi++) cek_tujuan_VALUE(slot_entri + posisi_bilangan_bulat(읽는자리 + dalam_posisi * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                slot_entri += 길이읽기(slot_entri, metode_Mulai[수], metode_mengakhiri[수]);
            }
            for (int dalam_posisi = 0; dalam_posisi < 잡기수; dalam_posisi++) if (잡기함수[dalam_posisi] == 수) {
                cek_tujuan_VALUE(잡기시작[dalam_posisi], 수); cek_tujuan_VALUE(잡기위치[dalam_posisi], 수);
                if (잡기끝[dalam_posisi] != metode_mengakhiri[수]) cek_tujuan_VALUE(잡기끝[dalam_posisi], 수);
                if (잡기시작[dalam_posisi] >= 잡기끝[dalam_posisi]) kegagalan_VALUE("invalid exception range");
            }
        }
        if (!galat) lompati_atribut();
        if (읽기위치 != Ukuran) kegagalan_VALUE("extra class file data");
    }
    static int alokasi_Storage(int 종류, int panjang_VALUE) { return 새기억(종류, panjang_VALUE); }
    static boolean objek_VALUE(int Referensi, int 종류) {
        if (!객체유효(Referensi)) return false;
        if (힙[Referensi] != 종류) { kegagalan_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!cek_konstanta(INDEX, 1)) return 0;
        if (string_Referensi[INDEX] != 0) return string_Referensi[INDEX];
        int Referensi = alokasi_Storage(1, konstanta_SECOND_VALUE[INDEX]); if (galat) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], panjang_VALUE = 0;
        while (수 < 끝 && !galat) {
            int VALUE = berkas[수++];
            if (VALUE == 0) kegagalan_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Berikutnya_item = berkas[수++];
                if ((Berikutnya_item & 192) != 128) kegagalan_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Berikutnya_item & 63;
                if (VALUE != 0 && VALUE < 128) kegagalan_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = berkas[수++], SECOND_operand = berkas[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) kegagalan_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) kegagalan_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) kegagalan_VALUE("invalid modified UTF-8");
            힙[Referensi + 2 + panjang_VALUE++] = VALUE;
        }
        힙[Referensi + 1] = panjang_VALUE; string_Referensi[INDEX] = Referensi; return Referensi;
    }
    static int host_karakter(String VALUE) {
        int Referensi = alokasi_Storage(1, VALUE.length()); if (galat) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Referensi + 2 + 수] = VALUE.charAt(수);
        return Referensi;
    }
    static void tulis_SMS(int Referensi) {
        if (Referensi == 0) { ruang_pengguna.Tulis("null"); return; }
        if (!objek_VALUE(Referensi, 1)) return;
        for (int 수 = 0; 수 < 힙[Referensi + 1]; 수++) ruang_pengguna.tulis_karakter_VALUE(힙[Referensi + 2 + 수]);
    }
    static int angka_karakter(int VALUE) {
        int Referensi = alokasi_Storage(1, 11); if (galat) return 0;
        int panjang_VALUE = 0;
        if (VALUE < 0) 힙[Referensi + 2 + panjang_VALUE++] = '-'; else VALUE = -VALUE;
        int posisi_INDEX = 1000000000; boolean jalankan = false;
        while (posisi_INDEX != 0) {
            int 수 = -(VALUE / posisi_INDEX);
            if (수 != 0 || jalankan || posisi_INDEX == 1) { 힙[Referensi + 2 + panjang_VALUE++] = '0' + 수; jalankan = true; }
            VALUE %= posisi_INDEX; posisi_INDEX /= 10;
        }
        힙[Referensi + 1] = panjang_VALUE; return Referensi;
    }
    static int 정수해독(int Referensi) {
        if (!objek_VALUE(Referensi, 1)) return 0;
        int panjang_VALUE = 힙[Referensi + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (panjang_VALUE > 0 && (힙[Referensi + 2] == '-' || 힙[Referensi + 2] == '+')) { 음수 = 힙[Referensi + 2] == '-'; 수++; }
        if (수 == panjang_VALUE) kegagalan_VALUE("NumberFormatException");
        for (; 수 < panjang_VALUE && !galat; 수++) {
            int angka_VALUE = 힙[Referensi + 2 + 수] - '0';
            if (angka_VALUE < 0 || angka_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && angka_VALUE > (음수 ? 8 : 7)) kegagalan_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - angka_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (galat) return;
        if (bingkai_INDEX < 0 || bingkai_tumpuk[bingkai_INDEX] >= metode_tumpuk[bingkai_metode[bingkai_INDEX]]) { kegagalan_VALUE("operand stack overflow"); return; }
        int slot_entri = bingkai_INDEX * 128 + bingkai_tumpuk[bingkai_INDEX]++; operand_tumpuk_VALUE[slot_entri] = VALUE; operand_tumpuk_TYPE[slot_entri] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (galat) return 0;
        if (bingkai_INDEX < 0 || bingkai_tumpuk[bingkai_INDEX] < 1) { kegagalan_VALUE("operand stack underflow"); return 0; }
        int slot_entri = bingkai_INDEX * 128 + --bingkai_tumpuk[bingkai_INDEX]; kembalikan_TYPE = operand_tumpuk_TYPE[slot_entri];
        if (TYPE_VALUE != 0 && kembalikan_TYPE != TYPE_VALUE) kegagalan_VALUE("operand type mismatch");
        if (kembalikan_TYPE == 2) amankan_VALUE(operand_tumpuk_VALUE[slot_entri]);
        return operand_tumpuk_VALUE[slot_entri];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[bingkai_metode[bingkai_INDEX]] || INDEX < 0 || lokal_TYPE[bingkai_INDEX * 128 + INDEX] != TYPE_VALUE) { kegagalan_VALUE("invalid or uninitialized local"); return; }
        넣기(lokal_VALUE[bingkai_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void tulis_lokal(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[bingkai_metode[bingkai_INDEX]] || INDEX < 0) { kegagalan_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokal_VALUE[bingkai_INDEX * 128 + INDEX] = VALUE; lokal_TYPE[bingkai_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int posisi = bingkai_posisi[bingkai_INDEX];
        if (posisi < metode_Mulai[bingkai_metode[bingkai_INDEX]] || posisi >= metode_mengakhiri[bingkai_metode[bingkai_INDEX]]) { kegagalan_VALUE("instruction pointer out of range"); return 0; }
        bingkai_posisi[bingkai_INDEX]++; return berkas[posisi];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void gerak_VALUE(int posisi) {
        int fungsi_VALUE = bingkai_metode[bingkai_INDEX];
        if (posisi < metode_Mulai[fungsi_VALUE] || posisi >= metode_mengakhiri[fungsi_VALUE] || 경계[posisi] != fungsi_VALUE + 1) kegagalan_VALUE("invalid branch target");
        else bingkai_posisi[bingkai_INDEX] = posisi;
    }
    static void 호출(int fungsi_VALUE) {
        if (bingkai_INDEX % 32 == 31) { kegagalan_VALUE("call stack limit (32)"); return; }
        int Berikutnya_item = bingkai_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Berikutnya_item * 128 + 수] = 0;
        for (int 수 = metode_argumen_COUNT[fungsi_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Berikutnya_item * 128 + 수] = 빼기(metode_argumen_TYPE[fungsi_VALUE * 16 + 수]); lokal_TYPE[Berikutnya_item * 128 + 수] = metode_argumen_TYPE[fungsi_VALUE * 16 + 수];
        }
        if (galat) return;
        bingkai_INDEX = Berikutnya_item; berinisial_bingkai[bingkai_INDEX] = 0; bingkai_metode[bingkai_INDEX] = fungsi_VALUE; bingkai_posisi[bingkai_INDEX] = metode_Mulai[fungsi_VALUE]; bingkai_tumpuk[bingkai_INDEX] = 0;
    }
    static void kembalikan_KR(int TYPE_VALUE) {
        if (TYPE_VALUE != metode_kembalikan[bingkai_metode[bingkai_INDEX]]) { kegagalan_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (berinisial_bingkai[bingkai_INDEX] != 0) Kelas_Definisi_Status[berinisial_bingkai[bingkai_INDEX] - 1] = 2;
        if (bingkai_kunci[bingkai_INDEX] != 0) { lepas_kunci(bingkai_kunci[bingkai_INDEX]); bingkai_kunci[bingkai_INDEX] = 0; }
        bingkai_INDEX--; if (bingkai_INDEX >= saat_ini_alur * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_nama_file = new int[64];
    static void file_Stream_CALL(int pemilik_VALUE, int Nama_2, int format_VALUE, int perintah) {
        boolean keluaranTeks = Kata_SMS(pemilik_VALUE, "java/io/FileOutputStream");
        int 종류 = keluaranTeks ? 6 : 5;
        if (perintah == 183 && Kata_SMS(Nama_2, "<init>")) {
            boolean 이어 = false;
            if (keluaranTeks && Kata_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Kata_SMS(format_VALUE, "(Ljava/lang/String;)V")) { kegagalan_VALUE("unsupported file stream constructor"); return; }
            int file_entri_nama = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objek_VALUE(file_entri_nama, 1) || !objek_VALUE(Stream_VALUE, 종류) || galat) return;
            if (힙[Stream_VALUE + 3] != 0) { kegagalan_VALUE("file stream already initialized"); return; }
            int panjang_VALUE = 힙[file_entri_nama + 1];
            if (panjang_VALUE < 1 || panjang_VALUE > 63) { kegagalan_VALUE("invalid file name length"); return; }
            for (int slot_entri = 0; slot_entri < panjang_VALUE; slot_entri++) {
                int VALUE = 힙[file_entri_nama + 2 + slot_entri];
                if (VALUE < 1) { kegagalan_VALUE("invalid file stream path"); return; }
                Stream_nama_file[slot_entri] = VALUE;
            }
            Stream_nama_file[panjang_VALUE] = 0;
            int 서술자 = ruang_pengguna.파일서술자열기(Stream_nama_file, keluaranTeks ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kegagalan_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (perintah != 182) { kegagalan_VALUE("invalid file stream invocation"); return; }
        if ((keluaranTeks && Kata_SMS(Nama_2, "write") || !keluaranTeks && Kata_SMS(Nama_2, "read"))
            && (Kata_SMS(format_VALUE, keluaranTeks ? "([B)V" : "([B)I") || Kata_SMS(format_VALUE, keluaranTeks ? "([BII)V" : "([BII)I"))) {
            boolean klip_VALUE = Kata_SMS(format_VALUE, keluaranTeks ? "([BII)V" : "([BII)I");
            int entri_COUNT = klip_VALUE ? 빼기(1) : 0, 시작점 = klip_VALUE ? 빼기(1) : 0, data_ARRAY = 빼기(2), objek_Referensi = 빼기(2);
            if (!objek_VALUE(data_ARRAY, 20) || !objek_VALUE(objek_Referensi, 종류)) return;
            if (!klip_VALUE) entri_COUNT = 힙[data_ARRAY + 1];
            if (시작점 < 0 || entri_COUNT < 0 || 시작점 > 힙[data_ARRAY + 1] - entri_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objek_Referensi + 3] == 0 || 힙[objek_Referensi + 2] < 0) { kegagalan_VALUE("IOException: stream closed"); return; }
            int Selesai_COUNT = 0;
            while (Selesai_COUNT < entri_COUNT && !galat) {
                int 반환값 = keluaranTeks ? ruang_pengguna.파일한바이트쓰기(힙[objek_Referensi + 2], 힙[data_ARRAY + 2 + 시작점 + Selesai_COUNT]) : ruang_pengguna.파일한바이트읽기(힙[objek_Referensi + 2]);
                if (반환값 < 0) { kegagalan_VALUE(keluaranTeks ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!keluaranTeks && 반환값 == 256) break;
                if (!keluaranTeks) 힙[data_ARRAY + 2 + 시작점 + Selesai_COUNT] = (byte)반환값;
                Selesai_COUNT++;
            }
            if (!keluaranTeks) 넣기(entri_COUNT != 0 && Selesai_COUNT == 0 ? -1 : Selesai_COUNT, 1);
            return;
        }
        if (keluaranTeks && Kata_SMS(Nama_2, "flush") && Kata_SMS(format_VALUE, "()V")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 종류) && 힙[objek_Referensi + 2] < 0) kegagalan_VALUE("IOException: stream closed"); return; }
        int Aksi = -1, VALUE = 0;
        if (Kata_SMS(Nama_2, "close") && Kata_SMS(format_VALUE, "()V")) Aksi = 0;
        if (!keluaranTeks && Kata_SMS(Nama_2, "read") && Kata_SMS(format_VALUE, "()I")) Aksi = 1;
        if (keluaranTeks && Kata_SMS(Nama_2, "write") && Kata_SMS(format_VALUE, "(I)V")) { Aksi = 2; VALUE = 빼기(1); }
        if (Aksi < 0) { kegagalan_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objek_VALUE(Stream_VALUE, 종류) || galat) return;
        if (힙[Stream_VALUE + 3] == 0) { kegagalan_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Aksi == 0) {
            if (서술자 >= 0 && ruang_pengguna.파일서술자닫기(서술자) < 0) kegagalan_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { kegagalan_VALUE("IOException: stream closed"); return; }
        if (Aksi == 1) {
            int hasil = ruang_pengguna.파일한바이트읽기(서술자);
            if (hasil < -1) kegagalan_VALUE("IOException: read failed"); else 넣기(hasil == 256 ? -1 : hasil, 1);
        } else if (ruang_pengguna.파일한바이트쓰기(서술자, VALUE) != 1) kegagalan_VALUE("IOException: write failed");
    }
    static void CALL_metode(int INDEX, int perintah) {
        if (INDEX <= 0 || INDEX >= konstanta_tag.length || (konstanta_tag[INDEX] != 10 && konstanta_tag[INDEX] != 11)) { kegagalan_VALUE("invalid method reference"); return; }
        int pemilik_VALUE = nama_kelas_SMS(상가[INDEX]), Nama_2 = Referensi_nama(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Referensi_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (galat) return;
        if (기본호출(pemilik_VALUE, Nama_2, format_VALUE, perintah)) return;
        if (Kata_SMS(pemilik_VALUE, "java/io/FileInputStream") || Kata_SMS(pemilik_VALUE, "java/io/FileOutputStream")) {
            file_Stream_CALL(pemilik_VALUE, Nama_2, format_VALUE, perintah); return;
        }
        if (perintah == 184 && Kata_SMS(pemilik_VALUE, "java/lang/Integer") && Kata_SMS(Nama_2, "parseInt") && Kata_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (perintah == 182 && Kata_SMS(pemilik_VALUE, "java/io/PrintStream") && (Kata_SMS(Nama_2, "println") || Kata_SMS(Nama_2, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Kata_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Kata_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Kata_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Kata_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Kata_SMS(format_VALUE, "()V") || !Kata_SMS(Nama_2, "println")) kegagalan_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) kegagalan_VALUE("invalid PrintStream receiver");
            if (galat) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) ruang_pengguna.Tulis(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) ruang_pengguna.tulis_karakter_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) tulis_SMS(VALUE);
            if (Kata_SMS(Nama_2, "println")) ruang_pengguna.tulis_karakter_VALUE(10);
            return;
        }
        if (perintah == 182 && Kata_SMS(pemilik_VALUE, "java/lang/String")) {
            if (Kata_SMS(Nama_2, "length") && Kata_SMS(format_VALUE, "()I")) {
                int Referensi = 빼기(2); if (objek_VALUE(Referensi, 1)) 넣기(힙[Referensi + 1], 1); return;
            }
            if (Kata_SMS(Nama_2, "charAt") && Kata_SMS(format_VALUE, "(I)C")) {
                int subskrip_VALUE = 빼기(1), Referensi = 빼기(2);
                if (objek_VALUE(Referensi, 1)) {
                    if (subskrip_VALUE < 0 || subskrip_VALUE >= 힙[Referensi + 1]) kegagalan_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Referensi + 2 + subskrip_VALUE], 1);
                }
                return;
            }
        }
        if (Kata_SMS(pemilik_VALUE, "java/lang/StringBuilder")) {
            if (perintah == 183 && Kata_SMS(Nama_2, "<init>") && Kata_SMS(format_VALUE, "()V")) { objek_VALUE(빼기(2), 4); return; }
            if (perintah == 182 && Kata_SMS(Nama_2, "toString") && Kata_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Referensi = 빼기(2); if (objek_VALUE(Referensi, 4)) 넣기(힙[Referensi + 2] == 0 ? host_karakter("") : 힙[Referensi + 2], 2); return;
            }
            if (perintah == 182 && Kata_SMS(Nama_2, "append")) {
                int teks = 0;
                if (Kata_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) teks = angka_karakter(빼기(1));
                else if (Kata_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) teks = host_karakter(빼기(1) == 0 ? "false" : "true");
                else if (Kata_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); teks = alokasi_Storage(1, 1); if (!galat) 힙[teks + 2] = VALUE & 65535;
                }
                else if (Kata_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { teks = 빼기(2); if (teks == 0) teks = host_karakter("null"); }
                else { kegagalan_VALUE("unsupported StringBuilder append"); return; }
                int Referensi = 빼기(2); if (!objek_VALUE(Referensi, 4) || !objek_VALUE(teks, 1)) return;
                int depan_VALUE = 힙[Referensi + 2], depan_VALUE_panjang = depan_VALUE == 0 ? 0 : 힙[depan_VALUE + 1], BACK_VALUE_panjang = 힙[teks + 1];
                int 새글 = alokasi_Storage(1, depan_VALUE_panjang + BACK_VALUE_panjang); if (galat) return;
                for (int 수 = 0; 수 < depan_VALUE_panjang; 수++) 힙[새글 + 2 + 수] = 힙[depan_VALUE + 2 + 수];
                for (int 수 = 0; 수 < BACK_VALUE_panjang; 수++) 힙[새글 + 2 + depan_VALUE_panjang + 수] = 힙[teks + 2 + 수];
                힙[Referensi + 2] = 새글; 넣기(Referensi, 2); return;
            }
        }
        int Kelas_Definisi = FIND_Kelas_Definisi(pemilik_VALUE); if (Kelas_Definisi < 0 || galat) return;
        int file_INDEX = FIND_metode(Kelas_Definisi, Nama_2, format_VALUE);
        if (file_INDEX < 0) {
            for (int kode_karakter = Kelas_Definisi, entri_COUNT = 0; kode_karakter >= 0 && entri_COUNT < 16; entri_COUNT++, kode_karakter = induk_Kelas(kode_karakter))
                if (Kata_SMS(Kelas_Definisi_induk[kode_karakter], "java/lang/Thread")) { 가닥호출(Nama_2, format_VALUE, perintah); return; }
            kegagalan_VALUE("NoSuchMethodError"); return;
        }
        if (((metode_akses[file_INDEX] & 8) != 0) != (perintah == 184)) { kegagalan_VALUE("method static/instance mismatch"); return; }
        if (perintah == 184) { if (!inisialisasi(metode_pemilik[file_INDEX], bingkai_instruksi[bingkai_INDEX])) return; }
        else {
            int 읽는자리 = bingkai_tumpuk[bingkai_INDEX] - metode_argumen_COUNT[file_INDEX];
            if (읽는자리 < 0 || operand_tumpuk_TYPE[bingkai_INDEX * 128 + 읽는자리] != 2) { kegagalan_VALUE("invalid method receiver"); return; }
            int objek_Referensi = operand_tumpuk_VALUE[bingkai_INDEX * 128 + 읽는자리];
            if (!객체유효(objek_Referensi)) return;
            if (힙[objek_Referensi] < 32 || !종포함(힙[objek_Referensi] - 32, pemilik_VALUE)) { kegagalan_VALUE("method receiver type mismatch"); return; }
            if (perintah != 183) file_INDEX = FIND_metode(힙[objek_Referensi] - 32, Nama_2, format_VALUE);
        }
        if (file_INDEX < 0 || (metode_akses[file_INDEX] & 0x400) != 0) { kegagalan_VALUE("AbstractMethodError"); return; }
        int kunci_Referensi = 0;
        if ((metode_akses[file_INDEX] & 32) != 0) {
            if (perintah == 184) { int kode_karakter = metode_pemilik[file_INDEX]; if (Kelas_kunci[kode_karakter] == 0) Kelas_kunci[kode_karakter] = alokasi_Storage(8, 0); kunci_Referensi = Kelas_kunci[kode_karakter]; }
            else kunci_Referensi = operand_tumpuk_VALUE[bingkai_INDEX * 128 + bingkai_tumpuk[bingkai_INDEX] - metode_argumen_COUNT[file_INDEX]];
            if (!잠금얻기(kunci_Referensi)) { if (!galat) bingkai_posisi[bingkai_INDEX] = bingkai_instruksi[bingkai_INDEX]; return; }
        }
        호출(file_INDEX); if (!galat) bingkai_kunci[bingkai_INDEX] = kunci_Referensi;
    }
    static boolean 배열저장가능(int ARRAY_Referensi, int data_VALUE) {
        if (data_VALUE == 0 || barisan_elemen[ARRAY_Referensi] == 0) return true;
        boolean 성공여부 = barisan_elemen[ARRAY_Referensi] == -1 ? (data_VALUE > 0 && data_VALUE < 힙끝 && 힙[data_VALUE] == 1) : 맞는객체(data_VALUE, barisan_elemen[ARRAY_Referensi]);
        if (!성공여부 && !galat) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_slot(int Referensi, int subskrip_VALUE, int TYPE_VALUE) {
        if (!objek_VALUE(Referensi, TYPE_VALUE)) return 0;
        if (subskrip_VALUE < 0 || subskrip_VALUE >= 힙[Referensi + 1]) { kegagalan_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referensi + 2 + subskrip_VALUE;
    }
    static void Jalankan_perintah() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (galat) { if (던진객체 != 0) handel_pengecualian(); if (galat || bingkai_INDEX < saat_ini_alur * 32) break; }
            if (bingkai_INDEX < saat_ini_alur * 32 || ubah_permintaan || --조각 == 0) { if (!SWITCH_alur()) break; 조각 = 100; }
            if (bingkai_INDEX == 0 && Kelas_Definisi_Status[entri_Kelas_Definisi] != 2 && !inisialisasi(entri_Kelas_Definisi, bingkai_posisi[bingkai_INDEX])) continue;
            if (bingkai_INDEX == saat_ini_alur * 32 && saat_ini_alur != 0 && (metode_akses[bingkai_metode[bingkai_INDEX]] & 32) != 0 && bingkai_kunci[bingkai_INDEX] == 0) {
                int objek_Referensi = alur_target[saat_ini_alur]; if (!잠금얻기(objek_Referensi)) { if (galat) break; continue; } bingkai_kunci[bingkai_INDEX] = objek_Referensi;
            }
            잠시수 = 0;
            if (--남음 == 0) { kegagalan_VALUE("instruction limit (500000)"); break; }
            int jalankan = bingkai_posisi[bingkai_INDEX]; bingkai_instruksi[bingkai_INDEX] = jalankan; int VALUE = 명바();
            if (galat) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metode_pemilik[bingkai_metode[bingkai_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstanta_tag.length) kegagalan_VALUE("invalid ldc constant");
                else if (konstanta_tag[수] == 3) 넣기(상가[수], 1);
                else if (konstanta_tag[수] == 8) 넣기(konstanta_SMS(상가[수]), 2);
                else kegagalan_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { tulis_lokal(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { tulis_lokal(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { tulis_lokal(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int entri_posisi = 빼기(1), objek_Referensi = 빼기(2), area_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objek_Referensi > 0 && objek_Referensi < 힙끝 && 힙[objek_Referensi] == 21) area_CODE = 21;
                int 읽는자리 = ARRAY_slot(objek_Referensi, entri_posisi, area_CODE); if (!galat) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int entri_Referensi = 빼기(VALUE == 83 ? 2 : 1), entri_posisi = 빼기(1), objek_Referensi = 빼기(2), area_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objek_Referensi > 0 && objek_Referensi < 힙끝 && 힙[objek_Referensi] == 21) area_CODE = 21;
                int 읽는자리 = ARRAY_slot(objek_Referensi, entri_posisi, area_CODE);
                if (!galat && area_CODE == 3 && !배열저장가능(objek_Referensi, entri_Referensi)) continue;
                if (!galat) 힙[읽는자리] = area_CODE == 20 ? (byte)entri_Referensi : area_CODE == 21 ? entri_Referensi & 1 : area_CODE == 22 ? (char)entri_Referensi : area_CODE == 23 ? (short)entri_Referensi : entri_Referensi;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { tumpuk_instruksi(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), hasil = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { kegagalan_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) hasil = 가 + SECOND_operand;
                if (VALUE == 100) hasil = 가 - SECOND_operand;
                if (VALUE == 104) hasil = 가 * SECOND_operand;
                if (VALUE == 108) hasil = 가 / SECOND_operand;
                if (VALUE == 112) hasil = 가 % SECOND_operand;
                if (VALUE == 120) hasil = 가 << SECOND_operand;
                if (VALUE == 122) hasil = 가 >> SECOND_operand;
                if (VALUE == 124) hasil = 가 >>> SECOND_operand;
                if (VALUE == 126) hasil = 가 & SECOND_operand;
                if (VALUE == 128) hasil = 가 | SECOND_operand;
                if (VALUE == 130) hasil = 가 ^ SECOND_operand;
                넣기(hasil, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokal_Cakupan = 명바(), tahapan_langkah = (byte)명바(); 지역읽기(lokal_Cakupan, 1); 넣기(빼기(1) + tahapan_langkah, 1); tulis_lokal(lokal_Cakupan, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int tujuan_VALUE = jalankan + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) gerak_VALUE(tujuan_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { kembalikan_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, jalankan); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int total_COUNT = 명바(); if (total_COUNT == 0 || 명바() != 0) { kegagalan_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metode(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(nama_kelas_SMS(명상수()), jalankan); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int area_CODE = 3, komponen = 0;
                if (VALUE == 188) { int 임시값 = 명바(); area_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponen = nama_kelas_SMS(명상수());
                if (area_CODE == 0) { kegagalan_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objek_Referensi = alokasi_Storage(area_CODE, 유효길이); if (!galat) barisan_elemen[objek_Referensi] = komponen; 넣기(objek_Referensi, 2); continue;
            }
            if (VALUE == 190) {
                int objek_Referensi = 빼기(2);
                if (객체유효(objek_Referensi)) { int Perbandingan_posisi = 힙[objek_Referensi]; if (Perbandingan_posisi != 2 && Perbandingan_posisi != 3 && (Perbandingan_posisi < 20 || Perbandingan_posisi > 23)) kegagalan_VALUE("not an array"); else 넣기(힙[objek_Referensi + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objek_Referensi = 빼기(2); if (객체유효(objek_Referensi)) { if (힙[objek_Referensi] != 9) kegagalan_VALUE("athrow requires supported Throwable"); else { 던진객체 = objek_Referensi; galat = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int nama_konstanta = nama_kelas_SMS(명상수()), objek_Referensi = 빼기(2); boolean MATCH = 맞는객체(objek_Referensi, nama_konstanta);
                if (VALUE == 193) 넣기(objek_Referensi != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !galat) kegagalan_VALUE("ClassCastException"); 넣기(objek_Referensi, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = jalankan + 1, file_INDEX = bingkai_metode[bingkai_INDEX], Kunci_Referensi = 빼기(1);
                while ((읽는자리 - metode_Mulai[file_INDEX]) % 4 != 0) 읽는자리++;
                int target_surel = posisi_bilangan_bulat(읽는자리);
                if (VALUE == 170) { int 낮은값 = posisi_bilangan_bulat(읽는자리 + 4), 높은값 = posisi_bilangan_bulat(읽는자리 + 8); if (Kunci_Referensi >= 낮은값 && Kunci_Referensi <= 높은값) target_surel = posisi_bilangan_bulat(읽는자리 + 12 + (Kunci_Referensi - 낮은값) * 4); }
                else { int total_COUNT = posisi_bilangan_bulat(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < total_COUNT; Loop_INDEX++) if (posisi_bilangan_bulat(읽는자리 + 8 + Loop_INDEX * 8) == Kunci_Referensi) target_surel = posisi_bilangan_bulat(읽는자리 + 12 + Loop_INDEX * 8); }
                gerak_VALUE(jalankan + target_surel); continue;
            }
            if (VALUE == 200) { gerak_VALUE(jalankan + posisi_bilangan_bulat(jalankan + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objek_Referensi = 빼기(2);
                if (VALUE == 195) lepas_kunci(objek_Referensi);
                else if (!잠금얻기(objek_Referensi) && !galat) { 넣기(objek_Referensi, 2); bingkai_posisi[bingkai_INDEX] = jalankan; }
                continue;
            }
            if (VALUE == 196) {
                int perintah_CODE = 명바(), entri_posisi = 명짧();
                if (perintah_CODE == 21 || perintah_CODE == 25) 지역읽기(entri_posisi, perintah_CODE == 21 ? 1 : 2);
                else if (perintah_CODE == 54 || perintah_CODE == 58) tulis_lokal(entri_posisi, perintah_CODE == 54 ? 1 : 2);
                else if (perintah_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(entri_posisi, 1); 넣기(빼기(1) + DELTA_VALUE, 1); tulis_lokal(entri_posisi, 1); }
                else kegagalan_VALUE("unsupported wide opcode");
                continue;
            }
            kegagalan_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Kelas_Definisi(int Nama_2) {
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Definisi_COUNT; Loop_INDEX++) if (Kelas_Definisi_nama[Loop_INDEX] != 0 && 같은말(Kelas_Definisi_nama[Loop_INDEX], Nama_2)) return Loop_INDEX;
        return muat_Kelas_Definisi(konstanta_SMS(Nama_2));
    }
    static int muat_Kelas_Definisi(int nama_string) {
        if (!objek_VALUE(nama_string, 1)) return -1;
        int panjang_VALUE = 힙[nama_string + 1];
        if (panjang_VALUE < 1 || panjang_VALUE > 505 || Kelas_Definisi_COUNT == 16) { kegagalan_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < panjang_VALUE; Loop_INDEX++) { int kode_karakter = 힙[nama_string + 2 + Loop_INDEX]; nama_file_SMS[Loop_INDEX] = kode_karakter == '/' ? '.' : kode_karakter; }
        nama_file_SMS[panjang_VALUE] = '.'; nama_file_SMS[panjang_VALUE + 1] = 'c'; nama_file_SMS[panjang_VALUE + 2] = 'l'; nama_file_SMS[panjang_VALUE + 3] = 'a'; nama_file_SMS[panjang_VALUE + 4] = 's'; nama_file_SMS[panjang_VALUE + 5] = 's'; nama_file_SMS[panjang_VALUE + 6] = 0;
        int Ukuran = ruang_pengguna.파일읽기(nama_file_SMS, file_temporer);
        if (Ukuran < 0) { kegagalan_VALUE("ClassNotFoundException"); return -1; }
        int Kelas_Definisi = Kelas_Definisi_COUNT++; Kelas_Definisi_ukuran[Kelas_Definisi] = Ukuran;
        for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) berkas[Kelas_Definisi * 16384 + Loop_INDEX] = file_temporer[Loop_INDEX];
        클래스읽기(Kelas_Definisi); if (galat) return -1;
        int aktual_data = konstanta_SMS(Kelas_Definisi_nama[Kelas_Definisi]);
        if (!teks_sama(aktual_data, nama_string, true)) { kegagalan_VALUE("class name does not match file"); return -1; }
        int induk_VALUE = Kelas_Definisi_induk[Kelas_Definisi];
        if (induk_VALUE != 0 && !Kata_SMS(induk_VALUE, "java/lang/Object") && !Kata_SMS(induk_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 coba_lagi_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Kelas_Definisi(induk_VALUE);
            if (galat || 위 < 0) return -1;
            int 읽는자리 = 위, tahap_COUNT = 0;
            while (읽는자리 >= 0 && tahap_COUNT++ < 16) {
                if (읽는자리 == Kelas_Definisi) { kegagalan_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = induk_Kelas(읽는자리);
            }
            int 시작변위 = Kelas_slot_COUNT[위];
            for (int file_INDEX = 0; file_INDEX < slot_COUNT; file_INDEX++) if (slot_pemilik[file_INDEX] == Kelas_Definisi && (slot_Izin[file_INDEX] & 8) == 0) slot_posisi[file_INDEX] += 시작변위;
            Kelas_slot_COUNT[Kelas_Definisi] += 시작변위;
        }
        return Kelas_Definisi;
    }
    static int induk_Kelas(int Kelas_Definisi) {
        int Nama_2 = Kelas_Definisi_induk[Kelas_Definisi];
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Definisi_COUNT; Loop_INDEX++) if (Nama_2 != 0 && Kelas_Definisi_nama[Loop_INDEX] != 0 && 같은말(Kelas_Definisi_nama[Loop_INDEX], Nama_2)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metode(int Kelas_Definisi, int Nama_2, int format_VALUE) {
        for (int 깊이 = 0; Kelas_Definisi >= 0 && 깊이 < 16; 깊이++, Kelas_Definisi = induk_Kelas(Kelas_Definisi)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metode_COUNT; Loop_INDEX++) if (metode_pemilik[Loop_INDEX] == Kelas_Definisi && 같은말(metode_nama_SMS[Loop_INDEX], Nama_2) && 같은말(metode_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int nama_metode(int Kelas_Definisi, String Nama_2, String format_VALUE) {
        for (int 깊이 = 0; Kelas_Definisi >= 0 && 깊이 < 16; 깊이++, Kelas_Definisi = induk_Kelas(Kelas_Definisi))
            for (int Loop_INDEX = 0; Loop_INDEX < metode_COUNT; Loop_INDEX++) if (metode_pemilik[Loop_INDEX] == Kelas_Definisi && Kata_SMS(metode_nama_SMS[Loop_INDEX], Nama_2) && Kata_SMS(metode_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Nama_2) { return berkas[상가[Nama_2]] == 'L' || berkas[상가[Nama_2]] == '[' ? 2 : 1; }
    static boolean inisialisasi(int Kelas_Definisi, int perintah_Mulai) {
        if (Kelas_Definisi < 0 || galat) return false;
        if (Kelas_Definisi_Status[Kelas_Definisi] == 3) { kegagalan_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Kelas_Definisi_Status[Kelas_Definisi] == 1 && Kelas_alur[Kelas_Definisi] != saat_ini_alur) { bingkai_posisi[bingkai_INDEX] = perintah_Mulai; ubah_permintaan = true; return false; }
        if (Kelas_Definisi_Status[Kelas_Definisi] != 0) return true;
        int 위 = induk_Kelas(Kelas_Definisi);
        if (위 >= 0 && !inisialisasi(위, perintah_Mulai)) return false;
        Kelas_Definisi_Status[Kelas_Definisi] = 1; Kelas_alur[Kelas_Definisi] = saat_ini_alur;
        if (berinisial_Kelas_Definisi[Kelas_Definisi] != 0) {
            bingkai_posisi[bingkai_INDEX] = perintah_Mulai;
            호출(berinisial_Kelas_Definisi[Kelas_Definisi] - 1); if (!galat) berinisial_bingkai[bingkai_INDEX] = Kelas_Definisi + 1;
            return false;
        }
        Kelas_Definisi_Status[Kelas_Definisi] = 2; return true;
    }
    static void 필드호출(int INDEX, int perintah, int jalankan) {
        if (!cek_konstanta(INDEX, 9)) return;
        int pemilik_VALUE = nama_kelas_SMS(상가[INDEX]), Nama_2 = Referensi_nama(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Referensi_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (Kata_SMS(pemilik_VALUE, "java/lang/System") && (Kata_SMS(Nama_2, "out") || Kata_SMS(Nama_2, "err")) && Kata_SMS(format_VALUE, "Ljava/io/PrintStream;") && perintah == 178) { 넣기(-1, 2); return; }
        int Kelas_Definisi = FIND_Kelas_Definisi(pemilik_VALUE); if (Kelas_Definisi < 0 || galat) return;
        int 찾음 = -1;
        for (int 읽는자리 = Kelas_Definisi, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = induk_Kelas(읽는자리))
            for (int file_INDEX = 0; file_INDEX < slot_COUNT; file_INDEX++) if (slot_pemilik[file_INDEX] == 읽는자리 && 같은말(slot_nama[file_INDEX], Nama_2) && 같은말(slot_TYPE[file_INDEX], format_VALUE)) 찾음 = file_INDEX;
        if (찾음 < 0) { kegagalan_VALUE("NoSuchFieldError"); return; }
        boolean statik_VALUE = perintah == 178 || perintah == 179;
        if (statik_VALUE != ((slot_Izin[찾음] & 8) != 0)) { kegagalan_VALUE("field static/instance mismatch"); return; }
        if (statik_VALUE && !inisialisasi(slot_pemilik[찾음], jalankan)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (perintah == 179 || perintah == 181) VALUE = 빼기(TYPE_VALUE);
        if (statik_VALUE) { if (perintah == 178) 넣기(slot_data[찾음], TYPE_VALUE); else if (!galat) slot_data[찾음] = VALUE; return; }
        int objek_Referensi = 빼기(2);
        if (!객체유효(objek_Referensi)) return;
        if (힙[objek_Referensi] < 32 || !종포함(힙[objek_Referensi] - 32, pemilik_VALUE)) { kegagalan_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objek_Referensi + 2 + slot_posisi[찾음];
        if (perintah == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!galat) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Kelas_Definisi, int Nama_2) {
        for (int 중첩깊이 = 0; Kelas_Definisi >= 0 && 중첩깊이 < 16; 중첩깊이++, Kelas_Definisi = induk_Kelas(Kelas_Definisi)) {
            if (같은말(Kelas_Definisi_nama[Kelas_Definisi], Nama_2) || (Kelas_Definisi_induk[Kelas_Definisi] != 0 && 같은말(Kelas_Definisi_induk[Kelas_Definisi], Nama_2))) return true;
            for (int dalam_posisi = 0; dalam_posisi < Kelas_antarmuka_COUNT[Kelas_Definisi]; dalam_posisi++) if (같은말(Kelas_antarmuka[Kelas_Definisi * 16 + dalam_posisi], Nama_2)) return true;
        }
        return false;
    }
    static boolean teks_sama(int 첫값, int byte_data, boolean jalur) {
        if (첫값 == byte_data) return true;
        if (첫값 <= 0 || byte_data <= 0 || 힙[첫값] != 1 || 힙[byte_data] != 1 || 힙[첫값 + 1] != 힙[byte_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int koordinat_x = 힙[첫값 + 2 + Loop_INDEX], Y_koordinat = 힙[byte_data + 2 + Loop_INDEX];
            if (jalur) { if (koordinat_x == '.') koordinat_x = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (koordinat_x != Y_koordinat) return false;
        }
        return true;
    }
    static boolean 객체유효(int objek_Referensi) {
        if (objek_Referensi == 0) { kegagalan_VALUE("NullPointerException"); return false; }
        if (objek_Referensi < 1 || objek_Referensi >= 힙끝 || 힙폭[objek_Referensi] < 2 || 힙[objek_Referensi] == 0) { kegagalan_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void amankan_VALUE(int objek_Referensi) {
        if (objek_Referensi > 0 && objek_Referensi < 힙끝 && 힙폭[objek_Referensi] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objek_Referensi;
    }
    static void show_VALUE(int objek_Referensi) {
        if (objek_Referensi > 0 && objek_Referensi < 힙끝 && 힙폭[objek_Referensi] >= 2 && 힙[objek_Referensi] != 0 && 힙표시[objek_Referensi] == 0) {
            힙표시[objek_Referensi] = 1; 표시대기[tampilan_COUNT++] = objek_Referensi;
        }
    }
    static void 수거() {
        tampilan_COUNT = 0; Koleksi_COUNT++;
        for (int cek_posisi = 1; cek_posisi < 힙끝; cek_posisi += 힙폭[cek_posisi]) 힙표시[cek_posisi] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < string_Referensi.length; Loop_INDEX++) show_VALUE(string_Referensi[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < slot_COUNT; Loop_INDEX++) if ((slot_Izin[Loop_INDEX] & 8) != 0 && 형종류(slot_TYPE[Loop_INDEX]) == 2) show_VALUE(slot_data[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < alur_COUNT; 임시값++) {
            show_VALUE(alur_objek[임시값]); show_VALUE(alur_target[임시값]);
            int 꼭대기자리 = 임시값 == saat_ini_alur ? bingkai_INDEX : alur_bingkai[임시값];
            for (int file_INDEX = 임시값 * 32; file_INDEX <= 꼭대기자리; file_INDEX++) {
                for (int dalam_posisi = 0; dalam_posisi < 함수지역[bingkai_metode[file_INDEX]]; dalam_posisi++) if (lokal_TYPE[file_INDEX * 128 + dalam_posisi] == 2) show_VALUE(lokal_VALUE[file_INDEX * 128 + dalam_posisi]);
                for (int dalam_posisi = 0; dalam_posisi < bingkai_tumpuk[file_INDEX]; dalam_posisi++) if (operand_tumpuk_TYPE[file_INDEX * 128 + dalam_posisi] == 2) show_VALUE(operand_tumpuk_VALUE[file_INDEX * 128 + dalam_posisi]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) show_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) show_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_bilangan_bulat.length; Loop_INDEX++) show_VALUE(Store_bilangan_bulat[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Definisi_COUNT; Loop_INDEX++) show_VALUE(Kelas_kunci[Loop_INDEX]);
        for (int cek_posisi = 1; cek_posisi < 힙끝; cek_posisi += 힙폭[cek_posisi]) if (잠금깊이[cek_posisi] > 0) show_VALUE(cek_posisi);
        show_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) show_VALUE(잠시참조[Loop_INDEX]);
        while (tampilan_COUNT > 0) {
            int objek_Referensi = 표시대기[--tampilan_COUNT], area_CODE = 힙[objek_Referensi];
            for (int Loop_INDEX = objek_Referensi + 2; Loop_INDEX < objek_Referensi + 힙폭[objek_Referensi]; Loop_INDEX++) if (area_CODE == 3 || area_CODE == 4 || 힙참조[Loop_INDEX] != 0) show_VALUE(힙[Loop_INDEX]);
        }
        for (int cek_posisi = 1; cek_posisi < 힙끝; cek_posisi += 힙폭[cek_posisi]) if (힙표시[cek_posisi] == 0) 힙[cek_posisi] = 0;
        for (int cek_posisi = 1; cek_posisi < 힙끝; cek_posisi += 힙폭[cek_posisi]) if (힙[cek_posisi] == 0) {
            while (cek_posisi + 힙폭[cek_posisi] < 힙끝 && 힙[cek_posisi + 힙폭[cek_posisi]] == 0) { int Berikutnya_posisi = cek_posisi + 힙폭[cek_posisi]; 힙폭[cek_posisi] += 힙폭[Berikutnya_posisi]; 힙폭[Berikutnya_posisi] = 0; }
            if (cek_posisi + 힙폭[cek_posisi] == 힙끝) { 힙끝 = cek_posisi; break; }
        }
    }
    static int 새기억(int 종류, int panjang_VALUE) {
        if (panjang_VALUE < 0) { kegagalan_VALUE("NegativeArraySizeException"); return 0; }
        if (panjang_VALUE > 힙.length - 3) { kegagalan_VALUE("object heap exhausted"); return 0; }
        int 필요수 = panjang_VALUE + 2, objek_Referensi = 0;
        if (필요수 <= 힙.length - 힙끝) { objek_Referensi = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objek_Referensi = 읽는자리; break; }
            if (objek_Referensi != 0) {
                int 남은길이 = 힙폭[objek_Referensi] - 필요수;
                if (남은길이 >= 2) { 힙폭[objek_Referensi + 필요수] = 남은길이; 힙[objek_Referensi + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objek_Referensi = 힙끝; 힙끝 += 필요수; }
        }
        if (objek_Referensi == 0) { kegagalan_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objek_Referensi + Loop_INDEX] = 0; 힙참조[objek_Referensi + Loop_INDEX] = 0; 힙폭[objek_Referensi + Loop_INDEX] = 0; }
        barisan_elemen[objek_Referensi] = 0;
        힙폭[objek_Referensi] = 필요수; 힙[objek_Referensi] = 종류; 힙[objek_Referensi + 1] = panjang_VALUE; amankan_VALUE(objek_Referensi); return objek_Referensi;
    }
    static int pengecualian_Kelas(String nama_konstanta) {
        if (자바도구.같음(nama_konstanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nama_konstanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(nama_konstanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nama_konstanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nama_konstanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nama_konstanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nama_konstanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nama_konstanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nama_konstanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nama_konstanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nama_konstanta, "java/io/IOException")) return 11;
        if (자바도구.같음(nama_konstanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nama_konstanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nama_konstanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nama_konstanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int pengecualian_konstanta(int Nama_2) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Kata_SMS(Nama_2, pengecualian_nama(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String pengecualian_nama(int akun_VALUE) {
        if (akun_VALUE == 40) return "java/lang/InterruptedException";
        if (akun_VALUE == 41) return "Indonesia/Asli/대기중단예외";
        if (akun_VALUE == 39) return "java/net/SocketException";
        if (akun_VALUE == 20) return "Indonesia/Asli/pengecualian";
        if (akun_VALUE == 21) return "Indonesia/Asli/실행예외";
        if (akun_VALUE == 22) return "Indonesia/Asli/I_O_pengecualian";
        if (akun_VALUE == 23) return "Indonesia/Asli/tunggu_TIMEOUT_pengecualian";
        if (akun_VALUE == 24) return "Indonesia/Asli/surel_LOOKUP_pengecualian";
        if (akun_VALUE == 25) return "Indonesia/Asli/파일없음예외";
        if (akun_VALUE == 26) return "Indonesia/Asli/komunikasi_pengecualian";
        if (akun_VALUE == 27) return "Indonesia/Asli/tidak_sahih_argumen_pengecualian";
        if (akun_VALUE == 28) return "Indonesia/Asli/숫자형식예외";
        if (akun_VALUE == 29) return "Indonesia/Asli/범위예외";
        if (akun_VALUE == 30) return "Indonesia/Asli/배열범위예외";
        if (akun_VALUE == 31) return "Indonesia/Asli/문자열범위예외";
        if (akun_VALUE == 32) return "Indonesia/Asli/NULL_Referensi_pengecualian";
        if (akun_VALUE == 33) return "Indonesia/Asli/산술예외";
        if (akun_VALUE == 34) return "Indonesia/Asli/Status_pengecualian";
        if (akun_VALUE == 35) return "Indonesia/Asli/TYPE_Transmisi_pengecualian";
        if (akun_VALUE == 36) return "Indonesia/Asli/음수배열크기예외";
        if (akun_VALUE == 37) return "Indonesia/Asli/ARRAY_Store_kegagalan";
        if (akun_VALUE == 38) return "Indonesia/Asli/alur_Status_pengecualian";
        if (akun_VALUE == 1) return "java/lang/Throwable"; if (akun_VALUE == 2) return "java/lang/Exception";
        if (akun_VALUE == 3) return "java/lang/RuntimeException"; if (akun_VALUE == 4) return "java/lang/ArithmeticException";
        if (akun_VALUE == 5) return "java/lang/NullPointerException"; if (akun_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (akun_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (akun_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (akun_VALUE == 9) return "java/lang/IllegalArgumentException"; if (akun_VALUE == 10) return "java/lang/NumberFormatException";
        if (akun_VALUE == 11) return "java/io/IOException"; if (akun_VALUE == 12) return "java/io/FileNotFoundException";
        if (akun_VALUE == 17) return "java/lang/ArrayStoreException";
        if (akun_VALUE == 18) return "java/net/UnknownHostException";
        if (akun_VALUE == 19) return "java/net/SocketTimeoutException";
        if (akun_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (akun_VALUE == 13) return "java/lang/IllegalStateException"; if (akun_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int pengecualian_induk(int akun_VALUE) {
        if (akun_VALUE == 40) return 2;
        if (akun_VALUE == 41) return 40;
        if (akun_VALUE == 39) return 11;
        if (akun_VALUE == 1) return 0;
        if (akun_VALUE == 2) return 1;
        if (akun_VALUE == 3) return 2;
        if (akun_VALUE == 4) return 3;
        if (akun_VALUE == 5) return 3;
        if (akun_VALUE == 6) return 3;
        if (akun_VALUE == 7) return 6;
        if (akun_VALUE == 8) return 6;
        if (akun_VALUE == 9) return 3;
        if (akun_VALUE == 10) return 9;
        if (akun_VALUE == 11) return 2;
        if (akun_VALUE == 12) return 11;
        if (akun_VALUE == 13) return 3;
        if (akun_VALUE == 14) return 3;
        if (akun_VALUE == 15) return 3;
        if (akun_VALUE == 16) return 9;
        if (akun_VALUE == 17) return 3;
        if (akun_VALUE == 18) return 11;
        if (akun_VALUE == 19) return 11;
        if (akun_VALUE == 20) return 2;
        if (akun_VALUE == 21) return 3;
        if (akun_VALUE == 22) return 11;
        if (akun_VALUE == 23) return 22;
        if (akun_VALUE == 24) return 22;
        if (akun_VALUE == 25) return 22;
        if (akun_VALUE == 26) return 22;
        if (akun_VALUE == 27) return 9;
        if (akun_VALUE == 28) return 27;
        if (akun_VALUE == 29) return 6;
        if (akun_VALUE == 30) return 29;
        if (akun_VALUE == 31) return 29;
        if (akun_VALUE == 32) return 5;
        if (akun_VALUE == 33) return 4;
        if (akun_VALUE == 34) return 13;
        if (akun_VALUE == 35) return 14;
        if (akun_VALUE == 36) return 15;
        if (akun_VALUE == 37) return 17;
        if (akun_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int nilai_aktual, int 요구값) {
        for (int 깊이 = 0; nilai_aktual != 0 && 깊이 < 16; 깊이++, nilai_aktual = pengecualian_induk(nilai_aktual))
            if (nilai_aktual == 요구값) return true;
        return false;
    }
    static void 예외던짐(int akun_VALUE, String baca_saya_Referensi) {
        int objek_Referensi = 새기억(9, 2); if (galat) return;
        힙[objek_Referensi + 2] = akun_VALUE; 힙[objek_Referensi + 3] = host_karakter(baca_saya_Referensi); 힙참조[objek_Referensi + 3] = 1;
        던진객체 = objek_Referensi; galat = true;
    }
    static boolean 맞는객체(int objek_Referensi, int Nama_2) {
        if (objek_Referensi == 0) return true;
        if (!객체유효(objek_Referensi)) return false;
        int area_CODE = 힙[objek_Referensi];
        if (Kata_SMS(Nama_2, "java/lang/Object")) return true;
        if (area_CODE >= 32) return 종포함(area_CODE - 32, Nama_2);
        if (area_CODE == 9) { int target_surel = pengecualian_konstanta(Nama_2); return target_surel != 0 && 예외포함(힙[objek_Referensi + 2], target_surel); }
        if (area_CODE == 1) return Kata_SMS(Nama_2, "java/lang/String") || Kata_SMS(Nama_2, "java/lang/CharSequence");
        if (area_CODE == 4) return Kata_SMS(Nama_2, "java/lang/StringBuilder") || Kata_SMS(Nama_2, "java/lang/CharSequence");
        if (area_CODE == 10) return Kata_SMS(Nama_2, "java/util/ArrayList") || Kata_SMS(Nama_2, "java/util/List");
        if (area_CODE == 11) return Kata_SMS(Nama_2, "java/util/HashMap") || Kata_SMS(Nama_2, "java/util/Map");
        if (area_CODE == 12) return Kata_SMS(Nama_2, "java/lang/Integer") || Kata_SMS(Nama_2, "java/lang/Number");
        if (area_CODE >= 24 && area_CODE <= 28 && 힙[objek_Referensi + 13] != 0) return 한국어화면종(Nama_2) == area_CODE || Kata_SMS(Nama_2, "Indonesia/Asli/화면구성요소");
        if (area_CODE >= 24 && area_CODE <= 28) return (한국어화면종(Nama_2) == 0 && 화면종(Nama_2) == area_CODE) || Kata_SMS(Nama_2, "java/awt/Component") || Kata_SMS(Nama_2, "java/awt/Container") || Kata_SMS(Nama_2, "javax/swing/JComponent");
        if (area_CODE == 29) return Kata_SMS(Nama_2, 힙[objek_Referensi + 3] != 0 ? "Indonesia/Asli/동작알림" : "java/awt/event/ActionEvent");
        if (area_CODE == 30) return Kata_SMS(Nama_2, "java/awt/FlowLayout") || Kata_SMS(Nama_2, "java/awt/LayoutManager");
        if (area_CODE == 17) return Kata_SMS(Nama_2, "java/net/Socket");
        if (area_CODE == 18) return Kata_SMS(Nama_2, "java/net/ServerSocket");
        if (area_CODE == 19) return Kata_SMS(Nama_2, 힙[objek_Referensi + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (area_CODE == 14) return Kata_SMS(Nama_2, "java/net/InetAddress");
        if (area_CODE == 15) return Kata_SMS(Nama_2, "java/net/DatagramSocket");
        if (area_CODE == 16) return Kata_SMS(Nama_2, "java/net/DatagramPacket");
        if (area_CODE == 13) return Kata_SMS(Nama_2, 힙[objek_Referensi + 3] != 0 ? "Indonesia/Asli/tugasLatar" : "java/lang/Thread");
        if (area_CODE == 2) return Kata_SMS(Nama_2, "[I"); if (area_CODE == 20) return Kata_SMS(Nama_2, "[B"); if (area_CODE == 21) return Kata_SMS(Nama_2, "[Z");
        if (area_CODE == 22) return Kata_SMS(Nama_2, "[C"); if (area_CODE == 23) return Kata_SMS(Nama_2, "[S");
        if (area_CODE != 3) return false;
        if (Kata_SMS(Nama_2, "[Ljava/lang/Object;")) return true;
        int komponen = barisan_elemen[objek_Referensi];
        if (komponen == -1) return Kata_SMS(Nama_2, "[Ljava/lang/String;") || Kata_SMS(Nama_2, "[Ljava/lang/CharSequence;");
        if (komponen == 0) return false;
        if (배열종비교(komponen, Nama_2)) return true;
        if ((Kata_SMS(komponen, "java/lang/String") || Kata_SMS(komponen, "java/lang/StringBuilder")) && Kata_SMS(Nama_2, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Kelas_Definisi_COUNT; Loop_INDEX++) if (같은말(Kelas_Definisi_nama[Loop_INDEX], komponen)) {
            for (int kode_karakter = Loop_INDEX, 중첩깊이 = 0; kode_karakter >= 0 && 중첩깊이 < 16; 중첩깊이++, kode_karakter = induk_Kelas(kode_karakter)) {
                if (배열종비교(Kelas_Definisi_induk[kode_karakter], Nama_2)) return true;
                for (int dalam_posisi = 0; dalam_posisi < Kelas_antarmuka_COUNT[kode_karakter]; dalam_posisi++) if (배열종비교(Kelas_antarmuka[kode_karakter * 16 + dalam_posisi], Nama_2)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nama_konstanta, int 형식참조) {
        int cek_posisi = 상가[형식참조], entri_COUNT = konstanta_SECOND_VALUE[형식참조];
        if (nama_konstanta == 0 || entri_COUNT < 4 || berkas[cek_posisi] != '[' || berkas[cek_posisi + 1] != 'L' || berkas[cek_posisi + entri_COUNT - 1] != ';' || konstanta_SECOND_VALUE[nama_konstanta] != entri_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT - 3; Loop_INDEX++) if (berkas[상가[nama_konstanta] + Loop_INDEX] != berkas[cek_posisi + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void handel_pengecualian() {
        if (던진객체 == 0) return;
        galat = false;
        while (bingkai_INDEX >= saat_ini_alur * 32) {
            int file_INDEX = bingkai_metode[bingkai_INDEX], 읽는자리 = bingkai_instruksi[bingkai_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == file_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                bingkai_posisi[bingkai_INDEX] = 잡기위치[Loop_INDEX]; bingkai_tumpuk[bingkai_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (berinisial_bingkai[bingkai_INDEX] != 0) Kelas_Definisi_Status[berinisial_bingkai[bingkai_INDEX] - 1] = 3;
            if (bingkai_kunci[bingkai_INDEX] != 0) { lepas_kunci(bingkai_kunci[bingkai_INDEX]); bingkai_kunci[bingkai_INDEX] = 0; }
            bingkai_INDEX--;
        }
        ruang_pengguna.Tulis("Uncaught ");
        if (힙[던진객체] == 9) { ruang_pengguna.Tulis(pengecualian_nama(힙[던진객체 + 2])); ruang_pengguna.Tulis(": "); tulis_SMS(힙[던진객체 + 3]); }
        else ruang_pengguna.Tulis("user exception");
        ruang_pengguna.tulis_karakter_VALUE(10); 던진객체 = 0; galat = true;
    }
    // 이 JVM의 operand_tumpuk 항목은 saat_ini_item category-1(int/reference)만 허용한다.
    static void tumpuk_instruksi(int perintah_CODE) {
        int 첫값 = 빼기(0), 첫형식 = kembalikan_TYPE;
        if (perintah_CODE == 87) return;
        if (perintah_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_data = 빼기(0), SECOND_format = kembalikan_TYPE;
        if (perintah_CODE == 88) return;
        if (perintah_CODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (perintah_CODE == 92) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (perintah_CODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); return; }
        int kode_karakter = 빼기(0), 셋째형식 = kembalikan_TYPE;
        if (perintah_CODE == 91) { 넣기(첫값, 첫형식); 넣기(kode_karakter, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (perintah_CODE == 93) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(kode_karakter, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        int berikutnya_VALUE = 빼기(0), 넷째형식 = kembalikan_TYPE;
        넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(berikutnya_VALUE, 넷째형식); 넣기(kode_karakter, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nama_konstanta, int 시작점) {
        int area_CODE = 0, 유효길이 = 0, pengecualian_Referensi = pengecualian_konstanta(nama_konstanta);
        if (Kata_SMS(nama_konstanta, "java/lang/StringBuilder")) { area_CODE = 4; 유효길이 = 1; }
        if (Kata_SMS(nama_konstanta, "java/io/FileInputStream")) { area_CODE = 5; 유효길이 = 2; }
        if (Kata_SMS(nama_konstanta, "java/io/FileOutputStream")) { area_CODE = 6; 유효길이 = 2; }
        if (pengecualian_Referensi != 0) { area_CODE = 9; 유효길이 = 2; }
        if (Kata_SMS(nama_konstanta, "java/util/ArrayList")) { area_CODE = 10; 유효길이 = 2; }
        if (Kata_SMS(nama_konstanta, "java/util/HashMap")) { area_CODE = 11; 유효길이 = 2; }
        if (Kata_SMS(nama_konstanta, "java/lang/Integer")) { area_CODE = 12; 유효길이 = 1; }
        if (Kata_SMS(nama_konstanta, "java/net/Socket")) { area_CODE = 17; 유효길이 = 5; }
        if (Kata_SMS(nama_konstanta, "java/net/ServerSocket")) { area_CODE = 18; 유효길이 = 5; }
        if (Kata_SMS(nama_konstanta, "java/net/DatagramSocket")) { area_CODE = 15; 유효길이 = 3; }
        if (Kata_SMS(nama_konstanta, "java/net/DatagramPacket")) { area_CODE = 16; 유효길이 = 4; }
        if (Kata_SMS(nama_konstanta, "java/lang/Thread") || Kata_SMS(nama_konstanta, "Indonesia/Asli/tugasLatar")) { area_CODE = 13; 유효길이 = 2; }
        if (Kata_SMS(nama_konstanta, "java/lang/Object")) { area_CODE = 8; }
        if (area_CODE == 0 && 화면종(nama_konstanta) != 0) { area_CODE = 화면종(nama_konstanta); 유효길이 = 12; }
        if (area_CODE == 0) {
            int kode_karakter = FIND_Kelas_Definisi(nama_konstanta); if (kode_karakter < 0 || galat || !inisialisasi(kode_karakter, 시작점)) return;
            area_CODE = 32 + kode_karakter; 유효길이 = Kelas_slot_COUNT[kode_karakter];
        }
        int objek_Referensi = alokasi_Storage(area_CODE, 유효길이); if (galat) return;
        if (area_CODE == 13 && Kata_SMS(nama_konstanta, "Indonesia/Asli/tugasLatar")) 힙[objek_Referensi + 3] = 1;
        if (area_CODE >= 24 && area_CODE <= 28 && 한국어화면종(nama_konstanta) != 0) 힙[objek_Referensi + 13] = 1;
        if (area_CODE == 5 || area_CODE == 6 || area_CODE == 15 || area_CODE == 17 || area_CODE == 18) 힙[objek_Referensi + 2] = -1;
        if (area_CODE == 9) 힙[objek_Referensi + 2] = pengecualian_Referensi;
        넣기(objek_Referensi, 2);
    }
    static boolean 값같음(int 첫값, int byte_data) {
        if (첫값 == byte_data) return true;
        if (첫값 == 0 || byte_data == 0 || 첫값 < 0 || byte_data < 0 || 첫값 >= 힙끝 || byte_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_data] == 1) return teks_sama(첫값, byte_data, false);
        return 힙[첫값] == 12 && 힙[byte_data] == 12 && 힙[첫값 + 2] == 힙[byte_data + 2];
    }
    static int 글조각(int objek_Referensi, int Mulai_posisi, int mengakhiri_posisi) {
        if (!objek_VALUE(objek_Referensi, 1)) return 0;
        if (Mulai_posisi < 0 || mengakhiri_posisi < Mulai_posisi || mengakhiri_posisi > 힙[objek_Referensi + 1]) { kegagalan_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = alokasi_Storage(1, mengakhiri_posisi - Mulai_posisi); if (galat) return 0;
        for (int Loop_INDEX = Mulai_posisi; Loop_INDEX < mengakhiri_posisi; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Mulai_posisi] = 힙[objek_Referensi + 2 + Loop_INDEX];
        return 반환값;
    }
    static int gabung_SMS(int 첫값, int byte_data) {
        if (!objek_VALUE(첫값, 1) || !objek_VALUE(byte_data, 1)) return 0;
        int entri_COUNT = 힙[첫값 + 1], metode_INDEX = 힙[byte_data + 1], 반환값 = alokasi_Storage(1, entri_COUNT + metode_INDEX); if (galat) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metode_INDEX; Loop_INDEX++) 힙[반환값 + 2 + entri_COUNT + Loop_INDEX] = 힙[byte_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int pemilik, int nama_konstanta, int 서술상수, int perintah_CODE) {
        if (Kata_SMS(pemilik, "Indonesia/Asli/실행인수") && perintah_CODE == 184) {
            if (Kata_SMS(nama_konstanta, "item_COUNT") && Kata_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.인수개수() - 1, 1); return true; }
            if (Kata_SMS(nama_konstanta, "teks") && Kata_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= ruang_pengguna.인수개수() - 1) 예외던짐(29, "Jalankan_perintah argumen 범위를 벗어났습니다");
                else 넣기(host_karakter(ruang_pengguna.argumen(순번 + 1)), 2);
                return true;
            }
            kegagalan_VALUE("지원하지 않는 Indonesia Jalankan_perintah argumen 호출"); return true;
        }
        if (Kata_SMS(pemilik, "Indonesia/Asli/tugasLatar")) { Proses_alur(nama_konstanta, 서술상수, perintah_CODE, true); return true; }
        if (한국어화면소유(pemilik)) { 한국어화면호출(pemilik, nama_konstanta, 서술상수, perintah_CODE); return true; }
        if (화면소유(pemilik)) { 화면호출(pemilik, nama_konstanta, 서술상수, perintah_CODE); return true; }
        if (Kata_SMS(pemilik, "java/net/Socket") || Kata_SMS(pemilik, "java/net/ServerSocket") || Kata_SMS(pemilik, "java/io/InputStream") || Kata_SMS(pemilik, "java/io/OutputStream")) { 흐름호출(pemilik, nama_konstanta, 서술상수, perintah_CODE); return true; }
        if (Kata_SMS(pemilik, "Indonesia/Asli/kernel_VALUE") && perintah_CODE == 184) {
            if (Kata_SMS(nama_konstanta, "화면너비") && Kata_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.화면너비(), 1); return true; }
            if (Kata_SMS(nama_konstanta, "화면높이") && Kata_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.화면높이(), 1); return true; }
            if (Kata_SMS(nama_konstanta, "밀리초") && Kata_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.밀리초(), 1); return true; }
            if (Kata_SMS(nama_konstanta, "그림대기") && Kata_SMS(서술상수, "()I")) { 넣기(ruang_pengguna.그림대기(), 1); return true; }
            if (Kata_SMS(nama_konstanta, "persegi") && Kata_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), koordinat_x = 빼기(1); 넣기(ruang_pengguna.persegi(koordinat_x, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Kata_SMS(pemilik, "java/net/InetAddress") || Kata_SMS(pemilik, "java/net/DatagramPacket") || Kata_SMS(pemilik, "java/net/DatagramSocket")) { 통신호출(pemilik, nama_konstanta, 서술상수, perintah_CODE); return true; }
        if (Kata_SMS(pemilik, "java/lang/Thread")) { 가닥호출(nama_konstanta, 서술상수, perintah_CODE); return true; }
        if (Kata_SMS(pemilik, "java/lang/Object")) {
            if (Kata_SMS(nama_konstanta, "<init>") && Kata_SMS(서술상수, "()V") && perintah_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Kata_SMS(nama_konstanta, "equals") && Kata_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_data ? 1 : 0, 1); return true; }
        }
        if (pengecualian_konstanta(pemilik) != 0) {
            if (Kata_SMS(nama_konstanta, "<init>") && perintah_CODE == 183 && (Kata_SMS(서술상수, "()V") || Kata_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int minta = Kata_SMS(서술상수, "()V") ? 0 : 빼기(2), objek_Referensi = 빼기(2);
                if (objek_VALUE(objek_Referensi, 9)) { 힙[objek_Referensi + 3] = minta; 힙참조[objek_Referensi + 3] = 1; } return true;
            }
            if ((Kata_SMS(nama_konstanta, "getMessage") || Kata_SMS(nama_konstanta, "설명")) && Kata_SMS(서술상수, "()Ljava/lang/String;")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 9)) 넣기(힙[objek_Referensi + 3], 2); return true; }
        }
        if (Kata_SMS(pemilik, "java/lang/String")) {
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "getBytes") && (Kata_SMS(서술상수, "()[B") || Kata_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int pengodean_nama = Kata_SMS(서술상수, "()[B") ? 0 : 빼기(2), objek_Referensi = 빼기(2);
                if (!objek_VALUE(objek_Referensi, 1)) return true;
                if (pengodean_nama != 0 && !teks_sama(pengodean_nama, host_karakter("UTF-8"), false) && !teks_sama(pengodean_nama, host_karakter("UTF8"), false) && !teks_sama(pengodean_nama, host_karakter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int entri_COUNT = 힙[objek_Referensi + 1], 반환값 = alokasi_Storage(20, entri_COUNT * 3), 사용수 = 0; if (galat) return true;
                for (int dalam_posisi = 0; dalam_posisi < entri_COUNT; dalam_posisi++) {
                    int kode_karakter = 힙[objek_Referensi + 2 + dalam_posisi];
                    if (kode_karakter >= 0xd800 && kode_karakter <= 0xdbff && dalam_posisi + 1 < entri_COUNT && 힙[objek_Referensi + 3 + dalam_posisi] >= 0xdc00 && 힙[objek_Referensi + 3 + dalam_posisi] <= 0xdfff) kode_karakter = 0x10000 + ((kode_karakter - 0xd800) << 10) + 힙[objek_Referensi + 2 + ++dalam_posisi] - 0xdc00;
                    else if (kode_karakter >= 0xd800 && kode_karakter <= 0xdfff) kode_karakter = '?';
                    if (kode_karakter < 128) 힙[반환값 + 2 + 사용수++] = kode_karakter;
                    else { int byte_COUNT = kode_karakter < 2048 ? 2 : kode_karakter < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_COUNT == 2 ? 192 : byte_COUNT == 3 ? 224 : 240) | kode_karakter >> (6 * (byte_COUNT - 1))); for (int Perbandingan_posisi = byte_COUNT - 1; Perbandingan_posisi > 0; Perbandingan_posisi--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kode_karakter >> (6 * (Perbandingan_posisi - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "valueOf") && Kata_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(angka_karakter(빼기(1)), 2); return true; }
            if (perintah_CODE != 182) return false;
            if (Kata_SMS(nama_konstanta, "equals") && Kata_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(teks_sama(첫값, byte_data, false) ? 1 : 0, 1); return true; }
            if (Kata_SMS(nama_konstanta, "isEmpty") && Kata_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Kata_SMS(nama_konstanta, "substring") && (Kata_SMS(서술상수, "(I)Ljava/lang/String;") || Kata_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Kata_SMS(서술상수, "(II)Ljava/lang/String;"); int mengakhiri_posisi = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objek_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? mengakhiri_posisi : 힙[첫값 + 1]), 2); return true;
            }
            if (Kata_SMS(nama_konstanta, "concat") && Kata_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_data = 빼기(2), 첫값 = 빼기(2); 넣기(gabung_SMS(첫값, byte_data), 2); return true; }
            if (Kata_SMS(nama_konstanta, "hashCode") && Kata_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALUE = 0; if (objek_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_VALUE = hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_VALUE, 1); } return true; }
            if (Kata_SMS(nama_konstanta, "toString") && Kata_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objek_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Kata_SMS(pemilik, "java/lang/Integer")) {
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "valueOf") && Kata_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VALUE = 빼기(1), objek_Referensi = data_VALUE >= -128 && data_VALUE <= 127 ? Store_bilangan_bulat[data_VALUE + 128] : 0; if (objek_Referensi == 0) { objek_Referensi = alokasi_Storage(12, 1); if (!galat) { 힙[objek_Referensi + 2] = data_VALUE; if (data_VALUE >= -128 && data_VALUE <= 127) Store_bilangan_bulat[data_VALUE + 128] = objek_Referensi; } } 넣기(objek_Referensi, 2); return true; }
            if (perintah_CODE == 183 && Kata_SMS(nama_konstanta, "<init>") && Kata_SMS(서술상수, "(I)V")) { int data_VALUE = 빼기(1), objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 12)) 힙[objek_Referensi + 2] = data_VALUE; return true; }
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "intValue") && Kata_SMS(서술상수, "()I")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 12)) 넣기(힙[objek_Referensi + 2], 1); return true; }
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "toString") && Kata_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(angka_karakter(빼기(1)), 2); return true; }
        }
        if (Kata_SMS(pemilik, "java/lang/Math") && perintah_CODE == 184) {
            if (Kata_SMS(nama_konstanta, "abs") && Kata_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Kata_SMS(nama_konstanta, "min") || Kata_SMS(nama_konstanta, "max")) && Kata_SMS(서술상수, "(II)I")) { int byte_data = 빼기(1), 첫값 = 빼기(1); 넣기(Kata_SMS(nama_konstanta, "min") ? (첫값 < byte_data ? 첫값 : byte_data) : (첫값 > byte_data ? 첫값 : byte_data), 1); return true; }
        }
        if (Kata_SMS(pemilik, "java/lang/System") && perintah_CODE == 184) {
            if (Kata_SMS(nama_konstanta, "gc") && Kata_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Kata_SMS(nama_konstanta, "arraycopy") && Kata_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int entri_COUNT = 빼기(1), tujuan_VALUE_INDEX = 빼기(1), byte_data = 빼기(2), Mulai_posisi = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_data)) {
                    int area_CODE = 힙[첫값];
                    if (힙[byte_data] != area_CODE || (area_CODE != 2 && area_CODE != 3 && (area_CODE < 20 || area_CODE > 23))) kegagalan_VALUE("arraycopy type mismatch");
                    else if (entri_COUNT < 0 || Mulai_posisi < 0 || tujuan_VALUE_INDEX < 0 || Mulai_posisi > 힙[첫값 + 1] - entri_COUNT || tujuan_VALUE_INDEX > 힙[byte_data + 1] - entri_COUNT) kegagalan_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_data && tujuan_VALUE_INDEX > Mulai_posisi) { for (int Loop_INDEX = entri_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[byte_data + 2 + tujuan_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Mulai_posisi + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT && !galat; Loop_INDEX++) { int data_VALUE = 힙[첫값 + 2 + Mulai_posisi + Loop_INDEX]; if (area_CODE != 3 || 배열저장가능(byte_data, data_VALUE)) 힙[byte_data + 2 + tujuan_VALUE_INDEX + Loop_INDEX] = data_VALUE; } }
                }
                return true;
            }
        }
        if (Kata_SMS(pemilik, "java/util/ArrayList") || Kata_SMS(pemilik, "java/util/List") || Kata_SMS(pemilik, "java/util/HashMap") || Kata_SMS(pemilik, "java/util/Map")) {
            모음호출(pemilik, nama_konstanta, 서술상수, perintah_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objek_Referensi, int 필요수) {
        int 이전값 = 힙[objek_Referensi + 2], kapasitas_data = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (kapasitas_data >= 필요수) return;
        int Berikutnya_posisi = kapasitas_data < 8 ? 8 : kapasitas_data * 2; if (Berikutnya_posisi < 필요수) Berikutnya_posisi = 필요수;
        int data_ARRAY = alokasi_Storage(3, Berikutnya_posisi); if (galat) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapasitas_data; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objek_Referensi + 2] = data_ARRAY; 힙참조[objek_Referensi + 2] = 1;
    }
    static void 모음호출(int pemilik, int nama_konstanta, int 서술상수, int perintah_CODE) {
        boolean 대응참조 = Kata_SMS(pemilik, "java/util/HashMap") || Kata_SMS(pemilik, "java/util/Map"); int area_CODE = 대응참조 ? 11 : 10;
        if (Kata_SMS(nama_konstanta, "<init>") && perintah_CODE == 183 && Kata_SMS(서술상수, "()V")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, area_CODE)) 모음늘리기(objek_Referensi, 8); return; }
        if (perintah_CODE != 182 && perintah_CODE != 185) { kegagalan_VALUE("invalid collection invocation"); return; }
        if (Kata_SMS(nama_konstanta, "size") && Kata_SMS(서술상수, "()I") || Kata_SMS(nama_konstanta, "isEmpty") && Kata_SMS(서술상수, "()Z")) {
            int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, area_CODE)) 넣기(Kata_SMS(nama_konstanta, "size") ? 힙[objek_Referensi + 3] : 힙[objek_Referensi + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Kata_SMS(nama_konstanta, "clear") && Kata_SMS(서술상수, "()V")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, area_CODE)) { int data_ARRAY = 힙[objek_Referensi + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[data_ARRAY + 1]; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 0; 힙[objek_Referensi + 3] = 0; } return; }
        if (!대응참조 && Kata_SMS(nama_konstanta, "add") && Kata_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VALUE = 빼기(2), objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 10)) return;
            int entri_COUNT = 힙[objek_Referensi + 3]; 모음늘리기(objek_Referensi, entri_COUNT + 1); if (!galat) { 힙[힙[objek_Referensi + 2] + 2 + entri_COUNT] = data_VALUE; 힙[objek_Referensi + 3] = entri_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Kata_SMS(nama_konstanta, "get") || Kata_SMS(nama_konstanta, "remove")) && Kata_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Kata_SMS(nama_konstanta, "set") && Kata_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean teknologi_informasi_ditetapkan = Kata_SMS(nama_konstanta, "set"); int data_VALUE = teknologi_informasi_ditetapkan ? 빼기(2) : 0, entri_posisi = 빼기(1), objek_Referensi = 빼기(2);
            if (!objek_VALUE(objek_Referensi, 10)) return;
            int entri_COUNT = 힙[objek_Referensi + 3], data_ARRAY = 힙[objek_Referensi + 2];
            if (entri_posisi < 0 || entri_posisi >= entri_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_ARRAY + 2 + entri_posisi];
            if (teknologi_informasi_ditetapkan) 힙[data_ARRAY + 2 + entri_posisi] = data_VALUE;
            if (Kata_SMS(nama_konstanta, "remove")) { for (int Loop_INDEX = entri_posisi + 1; Loop_INDEX < entri_COUNT; Loop_INDEX++) 힙[data_ARRAY + 1 + Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX]; 힙[data_ARRAY + 1 + entri_COUNT] = 0; 힙[objek_Referensi + 3] = entri_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Kata_SMS(nama_konstanta, "get") || Kata_SMS(nama_konstanta, "remove")) && Kata_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Kata_SMS(nama_konstanta, "put") && Kata_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Kata_SMS(nama_konstanta, "containsKey") && Kata_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Kata_SMS(nama_konstanta, "put"), hapus = Kata_SMS(nama_konstanta, "remove");
            int data_VALUE = 넣기여부 ? 빼기(2) : 0, Kunci_Referensi = 빼기(2), objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 11)) return;
            int entri_COUNT = 힙[objek_Referensi + 3], data_ARRAY = 힙[objek_Referensi + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) if (값같음(Kunci_Referensi, 힙[data_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objek_Referensi, (entri_COUNT + 1) * 2); data_ARRAY = 힙[objek_Referensi + 2]; 찾은여부 = entri_COUNT; if (!galat) 힙[objek_Referensi + 3] = entri_COUNT + 1; }
                if (!galat) { 힙[data_ARRAY + 2 + 2 * 찾은여부] = Kunci_Referensi; 힙[data_ARRAY + 3 + 2 * 찾은여부] = data_VALUE; }
            }
            if (hapus && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < entri_COUNT; Loop_INDEX++) { 힙[data_ARRAY + 2 * Loop_INDEX] = 힙[data_ARRAY + 2 + 2 * Loop_INDEX]; 힙[data_ARRAY + 1 + 2 * Loop_INDEX] = 힙[data_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[data_ARRAY + 2 * entri_COUNT] = 0; 힙[data_ARRAY + 1 + 2 * entri_COUNT] = 0; 힙[objek_Referensi + 3] = entri_COUNT - 1; }
            if (Kata_SMS(nama_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        kegagalan_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objek_Referensi) {
        if (!객체유효(objek_Referensi)) return false;
        if (잠금깊이[objek_Referensi] != 0 && kunci_pemilik[objek_Referensi] != saat_ini_alur + 1) { ubah_permintaan = true; return false; }
        kunci_pemilik[objek_Referensi] = saat_ini_alur + 1; 잠금깊이[objek_Referensi]++; return true;
    }
    static void lepas_kunci(int objek_Referensi) {
        if (!객체유효(objek_Referensi)) return;
        if (잠금깊이[objek_Referensi] == 0 || kunci_pemilik[objek_Referensi] != saat_ini_alur + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objek_Referensi] == 0) kunci_pemilik[objek_Referensi] = 0;
    }
    static boolean SWITCH_alur() {
        alur_bingkai[saat_ini_alur] = bingkai_INDEX;
        if (bingkai_INDEX < saat_ini_alur * 32) alur_Status[saat_ini_alur] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < alur_COUNT; Loop_INDEX++) if (alur_Status[Loop_INDEX] == 2 && alur_Status[가닥대기[Loop_INDEX]] == 3) alur_Status[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= alur_COUNT; Loop_INDEX++) {
            int Berikutnya_posisi = (saat_ini_alur + Loop_INDEX) % alur_COUNT;
            if (alur_Status[Berikutnya_posisi] == 1) { saat_ini_alur = Berikutnya_posisi; bingkai_INDEX = alur_bingkai[Berikutnya_posisi]; ubah_permintaan = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < alur_COUNT; Loop_INDEX++) if (alur_Status[Loop_INDEX] != 3) { kegagalan_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nama_konstanta, int 서술상수, int perintah_CODE) { Proses_alur(nama_konstanta, 서술상수, perintah_CODE, false); }
    static void Proses_alur(int nama_konstanta, int 서술상수, int perintah_CODE, boolean Indonesia) {
        if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, Indonesia ? "YIELD_tugas" : "yield") && Kata_SMS(서술상수, "()V")) { ubah_permintaan = true; return; }
        if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "currentThread") && Kata_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(alur_objek[saat_ini_alur], 2); return; }
        if (perintah_CODE == 183 && Kata_SMS(nama_konstanta, "<init>") && (Kata_SMS(서술상수, "()V") || Kata_SMS(서술상수, Indonesia ? "(LIndonesia/Asli/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int target_surel = Kata_SMS(서술상수, "()V") ? 0 : 빼기(2), objek_Referensi = 빼기(2);
            if (!객체유효(objek_Referensi)) return;
            if (힙[objek_Referensi] == 13) { 힙[objek_Referensi + 2] = target_surel; 힙참조[objek_Referensi + 2] = 1; }
            else if (target_surel != 0) kegagalan_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (perintah_CODE == 182 && (Kata_SMS(nama_konstanta, Indonesia ? "Mulai_tugas" : "start") || Kata_SMS(nama_konstanta, Indonesia ? "기다리기" : "join")) && Kata_SMS(서술상수, "()V") || perintah_CODE == 182 && Kata_SMS(nama_konstanta, Indonesia ? "살아있는가" : "isAlive") && Kata_SMS(서술상수, "()Z")) {
            int objek_Referensi = 빼기(2); if (!객체유효(objek_Referensi)) return;
            int akun_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < alur_COUNT; Loop_INDEX++) if (alur_objek[Loop_INDEX] == objek_Referensi) akun_VALUE = Loop_INDEX;
            if (Kata_SMS(nama_konstanta, Indonesia ? "살아있는가" : "isAlive")) { 넣기(akun_VALUE >= 0 && alur_Status[akun_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Kata_SMS(nama_konstanta, Indonesia ? "기다리기" : "join")) { if (akun_VALUE >= 0 && alur_Status[akun_VALUE] != 3) { 가닥대기[saat_ini_alur] = akun_VALUE; alur_Status[saat_ini_alur] = 2; ubah_permintaan = true; } return; }
            if (akun_VALUE >= 0) { 예외던짐(Indonesia ? 38 : 16, "thread already started"); return; }
            if (alur_COUNT == 4) { kegagalan_VALUE("thread limit (4 including main)"); return; }
            int target_surel = 힙[objek_Referensi] == 13 ? 힙[objek_Referensi + 2] : objek_Referensi;
            int file_INDEX = target_surel > 0 && 힙[target_surel] >= 32 ? nama_metode(힙[target_surel] - 32, Indonesia ? "Eksekusi" : "run", "()V") : -1;
            if (target_surel != 0 && file_INDEX < 0) { kegagalan_VALUE("Runnable.run required"); return; }
            akun_VALUE = alur_COUNT++; alur_objek[akun_VALUE] = objek_Referensi; alur_target[akun_VALUE] = target_surel;
            int bingkai = akun_VALUE * 32; alur_bingkai[akun_VALUE] = file_INDEX < 0 ? bingkai - 1 : bingkai; alur_Status[akun_VALUE] = file_INDEX < 0 ? 3 : 1;
            if (file_INDEX >= 0) { bingkai_metode[bingkai] = file_INDEX; bingkai_posisi[bingkai] = metode_Mulai[file_INDEX]; lokal_VALUE[bingkai * 128] = target_surel; lokal_TYPE[bingkai * 128] = 2; }
            return;
        }
        kegagalan_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], surel_SMS = new int[16];
    static int lokal_surel() { return surel_objek(0x7f000001); }
    static int surel_objek(int VALUE) { int objek_Referensi = alokasi_Storage(14, 1); if (!galat) 힙[objek_Referensi + 2] = VALUE; return objek_Referensi; }
    static int 주소해독(int objek_Referensi) {
        if (objek_Referensi == 0 || teks_sama(objek_Referensi, host_karakter("localhost"), false)) return 0x7f000001;
        if (!objek_VALUE(objek_Referensi, 1)) return 0;
        int data_VALUE = 0, total_COUNT = 0, surel_byte = 0, 자릿수 = 0, entri_COUNT = 힙[objek_Referensi + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= entri_COUNT; Loop_INDEX++) {
            int kode_karakter = Loop_INDEX == entri_COUNT ? '.' : 힙[objek_Referensi + 2 + Loop_INDEX];
            if (kode_karakter == '.') { if (자릿수 == 0 || total_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VALUE = data_VALUE << 8 | surel_byte; total_COUNT++; surel_byte = 자릿수 = 0; }
            else { if (kode_karakter < '0' || kode_karakter > '9' || ++자릿수 > 3 || (surel_byte = surel_byte * 10 + kode_karakter - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (total_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VALUE;
    }
    static int surel_karakter(int data_VALUE) {
        int entri_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int surel_byte = data_VALUE >>> 이동비트 & 255;
            if (surel_byte >= 100) surel_SMS[entri_COUNT++] = '0' + surel_byte / 100;
            if (surel_byte >= 10) surel_SMS[entri_COUNT++] = '0' + surel_byte / 10 % 10;
            surel_SMS[entri_COUNT++] = '0' + surel_byte % 10; if (이동비트 != 0) surel_SMS[entri_COUNT++] = '.';
        }
        int objek_Referensi = alokasi_Storage(1, entri_COUNT); if (!galat) for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) 힙[objek_Referensi + 2 + Loop_INDEX] = surel_SMS[Loop_INDEX]; return objek_Referensi;
    }
    static void 통신호출(int pemilik, int nama_konstanta, int 서술상수, int perintah_CODE) {
        if (Kata_SMS(pemilik, "java/net/InetAddress")) {
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "getLoopbackAddress") && Kata_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_surel(), 2); return; }
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "getByName") && Kata_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !galat) 넣기(surel_objek(data_VALUE), 2); return;
            }
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "getHostAddress") && Kata_SMS(서술상수, "()Ljava/lang/String;")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 14)) 넣기(surel_karakter(힙[objek_Referensi + 2]), 2); return; }
        }
        if (Kata_SMS(pemilik, "java/net/DatagramPacket")) {
            if (perintah_CODE == 183 && Kata_SMS(nama_konstanta, "<init>") && (Kata_SMS(서술상수, "([BI)V") || Kata_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean tujuan_VALUE_Referensi = Kata_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int nomor_port = tujuan_VALUE_Referensi ? 빼기(1) : 0, surel_Referensi = tujuan_VALUE_Referensi ? 빼기(2) : 0;
                int entri_COUNT = 빼기(1), data_ARRAY = 빼기(2), objek_Referensi = 빼기(2);
                if (!objek_VALUE(objek_Referensi, 16) || !objek_VALUE(data_ARRAY, 20)) return;
                if (entri_COUNT < 0 || entri_COUNT > 힙[data_ARRAY + 1] || nomor_port < 0 || nomor_port > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (surel_Referensi != 0 && !objek_VALUE(surel_Referensi, 14)) return;
                힙[objek_Referensi + 2] = data_ARRAY; 힙참조[objek_Referensi + 2] = 1; 힙[objek_Referensi + 3] = entri_COUNT;
                힙[objek_Referensi + 4] = surel_Referensi; 힙참조[objek_Referensi + 4] = 1; 힙[objek_Referensi + 5] = nomor_port; return;
            }
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "setLength") && Kata_SMS(서술상수, "(I)V")) {
                int entri_COUNT = 빼기(1), objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 16)) return;
                if (entri_COUNT < 0 || entri_COUNT > 힙[힙[objek_Referensi + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objek_Referensi + 3] = entri_COUNT; return;
            }
            if (perintah_CODE == 182 && (Kata_SMS(nama_konstanta, "getData") && Kata_SMS(서술상수, "()[B") || Kata_SMS(nama_konstanta, "getLength") && Kata_SMS(서술상수, "()I") || Kata_SMS(nama_konstanta, "getAddress") && Kata_SMS(서술상수, "()Ljava/net/InetAddress;") || Kata_SMS(nama_konstanta, "getPort") && Kata_SMS(서술상수, "()I"))) {
                int objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 16)) return;
                int entri_posisi = Kata_SMS(nama_konstanta, "getData") ? 2 : Kata_SMS(nama_konstanta, "getLength") ? 3 : Kata_SMS(nama_konstanta, "getAddress") ? 4 : 5;
                넣기(힙[objek_Referensi + entri_posisi], entri_posisi == 2 || entri_posisi == 4 ? 2 : 1); return;
            }
        }
        if (Kata_SMS(pemilik, "java/net/DatagramSocket")) {
            if (perintah_CODE == 183 && Kata_SMS(nama_konstanta, "<init>") && (Kata_SMS(서술상수, "()V") || Kata_SMS(서술상수, "(I)V"))) {
                int nomor_port = Kata_SMS(서술상수, "()V") ? 0 : 빼기(1), objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 15)) return;
                if (nomor_port < 0 || nomor_port > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = ruang_pengguna.buat_jaringan(nomor_port); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objek_Referensi + 2] = 열린파일번호; return;
            }
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "setSoTimeout") && Kata_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objek_Referensi + 3] = 밀리초값; return;
            }
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "getLocalPort") && Kata_SMS(서술상수, "()I")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 15)) 넣기(힙[objek_Referensi + 2] < 0 ? -1 : ruang_pengguna.jaringan_port(힙[objek_Referensi + 2]), 1); return; }
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "isClosed") && Kata_SMS(서술상수, "()Z")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 15)) 넣기(힙[objek_Referensi + 2] < 0 ? 1 : 0, 1); return; }
            if (perintah_CODE == 182 && Kata_SMS(nama_konstanta, "close") && Kata_SMS(서술상수, "()V")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, 15) && 힙[objek_Referensi + 2] >= 0) { ruang_pengguna.파일서술자닫기(힙[objek_Referensi + 2]); 힙[objek_Referensi + 2] = -1; } return; }
            if (perintah_CODE == 182 && (Kata_SMS(nama_konstanta, "send") || Kata_SMS(nama_konstanta, "receive")) && Kata_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket_5cd5338b = 빼기(2), objek_Referensi = 빼기(2); if (!objek_VALUE(paket_5cd5338b, 16) || !objek_VALUE(objek_Referensi, 15)) return;
                int data_ARRAY = 힙[paket_5cd5338b + 2], 유효길이 = 힙[paket_5cd5338b + 3], 열린파일번호 = 힙[objek_Referensi + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Kata_SMS(nama_konstanta, "send")) {
                    if (!objek_VALUE(힙[paket_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX];
                    if (ruang_pengguna.kirim_jaringan(열린파일번호, 힙[힙[paket_5cd5338b + 4] + 2], 힙[paket_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int entri_COUNT = ruang_pengguna.terima_jaringan(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (entri_COUNT == -11) {
                        int saat_ini_TIME = ruang_pengguna.밀리초();
                        if (힙[objek_Referensi + 4] == 0) 힙[objek_Referensi + 4] = saat_ini_TIME + 1;
                        if (힙[objek_Referensi + 3] > 0 && saat_ini_TIME - (힙[objek_Referensi + 4] - 1) >= 힙[objek_Referensi + 3]) { 힙[objek_Referensi + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objek_Referensi, 2); 넣기(paket_5cd5338b, 2); bingkai_posisi[bingkai_INDEX] = bingkai_instruksi[bingkai_INDEX]; ubah_permintaan = true; return;
                    }
                    힙[objek_Referensi + 4] = 0;
                    if (entri_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paket_5cd5338b + 3] = entri_COUNT; 힙[paket_5cd5338b + 4] = surel_objek(통신임시[513]); 힙참조[paket_5cd5338b + 4] = 1; 힙[paket_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        kegagalan_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objek_Referensi) {
        int saat_ini_TIME = ruang_pengguna.밀리초();
        if (힙[objek_Referensi + 5] == 0) 힙[objek_Referensi + 5] = saat_ini_TIME + 1;
        if (힙[objek_Referensi + 3] > 0 && saat_ini_TIME - (힙[objek_Referensi + 5] - 1) >= 힙[objek_Referensi + 3]) { 힙[objek_Referensi + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        bingkai_posisi[bingkai_INDEX] = bingkai_instruksi[bingkai_INDEX]; ubah_permintaan = true; return true;
    }
    static void 흐름호출(int pemilik, int nama_konstanta, int 서술상수, int perintah_CODE) {
        boolean terima_halaman = Kata_SMS(pemilik, "java/net/ServerSocket"), Stream = Kata_SMS(pemilik, "java/io/InputStream") || Kata_SMS(pemilik, "java/io/OutputStream");
        if (!Stream && perintah_CODE == 183 && Kata_SMS(nama_konstanta, "<init>")) {
            boolean teknologi_informasi_kosong_Status = Kata_SMS(서술상수, "()V"), 이름지정여부 = Kata_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Kata_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(teknologi_informasi_kosong_Status || terima_halaman && Kata_SMS(서술상수, "(I)V") || !terima_halaman && (이름지정여부 || 주소지정여부))) { kegagalan_VALUE("unsupported socket constructor"); return; }
            int nomor_port = teknologi_informasi_kosong_Status ? 0 : 빼기(1), surel_Referensi = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objek_Referensi = 빼기(2);
            if (!objek_VALUE(objek_Referensi, terima_halaman ? 18 : 17)) return;
            if (nomor_port < 0 || nomor_port > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objek_VALUE(surel_Referensi, 14)) return;
            int jaringan_surel = 이름지정여부 ? 주소해독(surel_Referensi) : 주소지정여부 ? 힙[surel_Referensi + 2] : 0x7f000001;
            if (galat || 던진객체 != 0) return;
            int 열린파일번호 = ruang_pengguna.Stream_kontrol(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = teknologi_informasi_kosong_Status ? 0 : terima_halaman ? ruang_pengguna.Stream_kontrol(1, 열린파일번호, nomor_port) : ruang_pengguna.CONNECT_Stream(열린파일번호, jaringan_surel, nomor_port);
            if (처리값 < 0) { ruang_pengguna.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objek_Referensi + 2] = 열린파일번호; 힙[objek_Referensi + 4] = nomor_port; 힙[objek_Referensi + 6] = teknologi_informasi_kosong_Status ? 0 : 1; return;
        }
        if (!Stream && Kata_SMS(nama_konstanta, "setSoTimeout") && Kata_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, terima_halaman ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objek_Referensi + 3] = 밀리초값; return; }
        if (!Stream && Kata_SMS(nama_konstanta, "close") && Kata_SMS(서술상수, "()V")) { int objek_Referensi = 빼기(2); if (objek_VALUE(objek_Referensi, terima_halaman ? 18 : 17) && 힙[objek_Referensi + 2] >= 0) { ruang_pengguna.파일서술자닫기(힙[objek_Referensi + 2]); 힙[objek_Referensi + 2] = -1; } return; }
        if (!Stream && (Kata_SMS(nama_konstanta, "getLocalPort") || Kata_SMS(nama_konstanta, "getPort") || Kata_SMS(nama_konstanta, "isClosed") || Kata_SMS(nama_konstanta, "isConnected"))) {
            int objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, terima_halaman ? 18 : 17)) return;
            넣기(Kata_SMS(nama_konstanta, "isClosed") ? 힙[objek_Referensi + 2] < 0 ? 1 : 0 : Kata_SMS(nama_konstanta, "isConnected") ? 힙[objek_Referensi + 6] : Kata_SMS(nama_konstanta, "getPort") ? 힙[objek_Referensi + 4] : 힙[objek_Referensi + 2] < 0 ? -1 : ruang_pengguna.Stream_kontrol(4, 힙[objek_Referensi + 2], 0), 1); return;
        }
        if (terima_halaman && Kata_SMS(nama_konstanta, "accept") && Kata_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 18)) return; int 열린파일번호 = ruang_pengguna.Stream_kontrol(3, 힙[objek_Referensi + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objek_Referensi)) 넣기(objek_Referensi, 2); return; }
            힙[objek_Referensi + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = alokasi_Storage(17, 5); if (galat) { ruang_pengguna.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = ruang_pengguna.Stream_kontrol(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!terima_halaman && !Stream && ((Kata_SMS(nama_konstanta, "getInputStream") && Kata_SMS(서술상수, "()Ljava/io/InputStream;")) || (Kata_SMS(nama_konstanta, "getOutputStream") && Kata_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 17)) return; if (힙[objek_Referensi + 2] < 0 || 힙[objek_Referensi + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = alokasi_Storage(19, 4); if (galat) return; 힙[반환값 + 2] = objek_Referensi; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Kata_SMS(nama_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Kata_SMS(nama_konstanta, "read"), teknologi_informasi_tulis_bedah = Kata_SMS(nama_konstanta, "write"), blok = Kata_SMS(서술상수, "([B)I") || Kata_SMS(서술상수, "([B)V"), teknologi_informasi_SUBARRAY = Kata_SMS(서술상수, "([BII)I") || Kata_SMS(서술상수, "([BII)V");
            int entri_COUNT = teknologi_informasi_SUBARRAY ? 빼기(1) : 0, 시작변위 = teknologi_informasi_SUBARRAY ? 빼기(1) : 0, data_ARRAY = blok || teknologi_informasi_SUBARRAY ? 빼기(2) : 0;
            int data_VALUE = teknologi_informasi_tulis_bedah && Kata_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objek_Referensi = 빼기(2);
            if (!objek_VALUE(objek_Referensi, 19)) return; int induk_Referensi = 힙[objek_Referensi + 2], 열린파일번호 = 힙[induk_Referensi + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Kata_SMS(nama_konstanta, "close") && Kata_SMS(서술상수, "()V")) { ruang_pengguna.파일서술자닫기(열린파일번호); 힙[induk_Referensi + 2] = -1; return; }
            if (Kata_SMS(nama_konstanta, "flush") && Kata_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !teknologi_informasi_tulis_bedah) || 읽기여부 != (힙[objek_Referensi + 3] == 0)) { kegagalan_VALUE("unsupported stream operation"); return; }
            if (blok || teknologi_informasi_SUBARRAY) { if (!objek_VALUE(data_ARRAY, 20)) return; if (blok) entri_COUNT = 힙[data_ARRAY + 1]; if (시작변위 < 0 || entri_COUNT < 0 || 시작변위 > 힙[data_ARRAY + 1] - entri_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else entri_COUNT = 1;
            if (entri_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Selesai_COUNT = teknologi_informasi_tulis_bedah ? 힙[objek_Referensi + 4] : 0, 처리값 = 0;
            while (Selesai_COUNT < entri_COUNT) {
                처리값 = 읽기여부 ? ruang_pengguna.파일한바이트읽기(열린파일번호) : ruang_pengguna.파일한바이트쓰기(열린파일번호, blok || teknologi_informasi_SUBARRAY ? 힙[data_ARRAY + 2 + 시작변위 + Selesai_COUNT] : data_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || teknologi_informasi_SUBARRAY)) 힙[data_ARRAY + 2 + 시작변위 + Selesai_COUNT] = (byte)처리값;
                Selesai_COUNT++; if (읽기여부 && !(blok || teknologi_informasi_SUBARRAY)) break;
            }
            if (처리값 == -11 && (teknologi_informasi_tulis_bedah || Selesai_COUNT == 0)) {
                힙[objek_Referensi + 4] = Selesai_COUNT;
                if (흐름대기(induk_Referensi)) { 넣기(objek_Referensi, 2); if (blok || teknologi_informasi_SUBARRAY) 넣기(data_ARRAY, 2); if (teknologi_informasi_SUBARRAY) { 넣기(시작변위, 1); 넣기(entri_COUNT, 1); } if (teknologi_informasi_tulis_bedah && !(blok || teknologi_informasi_SUBARRAY)) 넣기(data_VALUE, 1); } return;
            }
            힙[objek_Referensi + 4] = 0; 힙[induk_Referensi + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Selesai_COUNT == 0 && 처리값 == 256 ? -1 : blok || teknologi_informasi_SUBARRAY ? Selesai_COUNT : 처리값, 1); return;
        }
        kegagalan_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nama_konstanta) {
        if (Kata_SMS(nama_konstanta, "Indonesia/Asli/Jendela")) return 24;
        if (Kata_SMS(nama_konstanta, "Indonesia/Asli/Nama")) return 26;
        if (Kata_SMS(nama_konstanta, "Indonesia/Asli/tombol")) return 27;
        if (Kata_SMS(nama_konstanta, "Indonesia/Asli/bidang_teks")) return 28;
        if (Kata_SMS(nama_konstanta, "Indonesia/Asli/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nama_konstanta) {
        return 한국어화면종(nama_konstanta) != 0 || Kata_SMS(nama_konstanta, "Indonesia/Asli/화면구성요소") || Kata_SMS(nama_konstanta, "Indonesia/Asli/acara_antrean");
    }
    static int 화면종(int nama_konstanta) {
        int 한국어종 = 한국어화면종(nama_konstanta); if (한국어종 != 0) return 한국어종;
        if (Kata_SMS(nama_konstanta, "javax/swing/JFrame")) return 24;
        if (Kata_SMS(nama_konstanta, "javax/swing/JPanel")) return 25;
        if (Kata_SMS(nama_konstanta, "javax/swing/JLabel")) return 26;
        if (Kata_SMS(nama_konstanta, "javax/swing/JButton")) return 27;
        if (Kata_SMS(nama_konstanta, "javax/swing/JTextField")) return 28;
        if (Kata_SMS(nama_konstanta, "java/awt/event/ActionEvent")) return 29;
        if (Kata_SMS(nama_konstanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nama_konstanta) {
        return 화면종(nama_konstanta) != 0 || Kata_SMS(nama_konstanta, "java/awt/Component") || Kata_SMS(nama_konstanta, "java/awt/Container") || Kata_SMS(nama_konstanta, "javax/swing/JComponent") || Kata_SMS(nama_konstanta, "javax/swing/AbstractButton") || Kata_SMS(nama_konstanta, "javax/swing/text/JTextComponent") || Kata_SMS(nama_konstanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objek_Referensi) { if (!객체유효(objek_Referensi)) return false; if (힙[objek_Referensi] < 24 || 힙[objek_Referensi] > 28) { kegagalan_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objek_Referensi, int SMS_Referensi) {
        if (SMS_Referensi != 0 && !objek_VALUE(SMS_Referensi, 1)) return;
        int entri_COUNT = SMS_Referensi == 0 ? 0 : 힙[SMS_Referensi + 1]; if (entri_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Referensi + 2 + Loop_INDEX];
        if (ruang_pengguna.화면글(힙[objek_Referensi + 2], 화면글임시, entri_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objek_Referensi + 3] = SMS_Referensi; 힙참조[objek_Referensi + 3] = 1;
    }
    static int 화면문자읽기(int objek_Referensi) {
        int akun_VALUE = 힙[objek_Referensi + 2], entri_COUNT = ruang_pengguna.화면연결(8, akun_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (entri_COUNT < 0) { kegagalan_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) { int 부호값 = ruang_pengguna.화면연결(9, akun_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = alokasi_Storage(1, 사용수); if (!galat) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Indonesia 객체를 직접 만들고 kernel_VALUE 화면 기능에 연결한다. Swing objek_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int pemilik, int nama_konstanta, int 서술상수, int perintah_CODE) {
        if (Kata_SMS(pemilik, "Indonesia/Asli/acara_antrean")) {
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "나중에실행") && Kata_SMS(서술상수, "(LIndonesia/Asli/실행할일;)V")) {
                int tugas_Tugas = 빼기(2); if (!객체유효(tugas_Tugas)) return;
                if (나중수 == 8) { kegagalan_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tugas_Tugas; return;
            }
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "사건처리중인가") && Kata_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kegagalan_VALUE("지원하지 않는 Indonesia 화면 일정 호출"); return;
        }
        if (Kata_SMS(pemilik, "Indonesia/Asli/동작알림")) {
            int 알림 = 빼기(2); if (!objek_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Kata_SMS(nama_konstanta, "sumber_kejadian") && Kata_SMS(서술상수, "()LIndonesia/Asli/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Kata_SMS(nama_konstanta, "perintah_SMS") && Kata_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Kata_SMS(nama_konstanta, "INDEX") && Kata_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kegagalan_VALUE("지원하지 않는 Indonesia Aksi 알림 호출"); return;
        }
        if (perintah_CODE == 183 && Kata_SMS(nama_konstanta, "<init>")) {
            int 종류 = 한국어화면종(pemilik), 받이 = 0, 가로 = 0, Vertikal_posisi = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Kata_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (ruang_pengguna.화면너비() - 폭) / 2; Vertikal_posisi = (ruang_pengguna.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Kata_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Kata_SMS(서술상수, "(Ljava/lang/String;IIIILIndonesia/Asli/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertikal_posisi = 빼기(1); 가로 = 빼기(1);
            } else { kegagalan_VALUE("지원하지 않는 Indonesia 화면 생성자"); return; }
            int teks = 빼기(2), elemen_VALUE = 빼기(2); if (!화면객체(elemen_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertikal_posisi < 0 || 폭 > ruang_pengguna.화면너비() - 가로 || 높이 > ruang_pengguna.화면높이() - Vertikal_posisi) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = ruang_pengguna.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { kegagalan_VALUE("화면 elemen_VALUE 자리가 가득 찼습니다"); return; }
            힙[elemen_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = elemen_VALUE;
            힙[elemen_VALUE + 5] = 가로; 힙[elemen_VALUE + 6] = Vertikal_posisi; 힙[elemen_VALUE + 7] = 폭; 힙[elemen_VALUE + 8] = 높이; 힙[elemen_VALUE + 10] = 2;
            힙[elemen_VALUE + 4] = 받이; 힙참조[elemen_VALUE + 4] = 1; 힙[elemen_VALUE + 12] = 1;
            ruang_pengguna.화면연결(1, INDEX, 가로, Vertikal_posisi, 폭, 높이);
            if (종류 == 24) ruang_pengguna.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(elemen_VALUE, teks); return;
        }
        if (perintah_CODE != 182) { kegagalan_VALUE("잘못된 Indonesia 화면 호출 perintah"); return; }
        if (Kata_SMS(nama_konstanta, "tulis_SMS") && Kata_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int teks = 빼기(2), elemen_VALUE = 빼기(2); if (화면객체(elemen_VALUE)) 화면문자설정(elemen_VALUE, teks); return;
        }
        if (Kata_SMS(nama_konstanta, "글읽기") && Kata_SMS(서술상수, "()Ljava/lang/String;")) {
            int elemen_VALUE = 빼기(2); if (화면객체(elemen_VALUE)) 넣기(화면문자읽기(elemen_VALUE), 2); return;
        }
        if (Kata_SMS(nama_konstanta, "동작맡기기") && Kata_SMS(서술상수, "(LIndonesia/Asli/동작받이;)V")) {
            int 받이 = 빼기(2), elemen_VALUE = 빼기(2);
            if (화면객체(elemen_VALUE)) { 힙[elemen_VALUE + 4] = 받이; 힙참조[elemen_VALUE + 4] = 1; 힙[elemen_VALUE + 12] = 1; } return;
        }
        if (Kata_SMS(nama_konstanta, "tambah_elemen") && Kata_SMS(서술상수, "(LIndonesia/Asli/화면구성요소;)V")) {
            int turunan_VALUE = 빼기(2), induk_VALUE = 빼기(2); if (!화면객체(turunan_VALUE) || !화면객체(induk_VALUE)) return;
            if (ruang_pengguna.화면연결(2, 힙[induk_VALUE + 2], 힙[turunan_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[turunan_VALUE + 11] = induk_VALUE; 힙참조[turunan_VALUE + 11] = 1; return;
        }
        if (Kata_SMS(nama_konstanta, "자리정하기") && Kata_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertikal_posisi = 빼기(1), 가로 = 빼기(1), elemen_VALUE = 빼기(2); if (!화면객체(elemen_VALUE)) return;
            if (ruang_pengguna.화면연결(1, 힙[elemen_VALUE + 2], 가로, Vertikal_posisi, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elemen_VALUE + 5] = 가로; 힙[elemen_VALUE + 6] = Vertikal_posisi; 힙[elemen_VALUE + 7] = 폭; 힙[elemen_VALUE + 8] = 높이; return;
        }
        if ((Kata_SMS(nama_konstanta, "show_jendela") || Kata_SMS(nama_konstanta, "Tutup")) && Kata_SMS(서술상수, "()V")) {
            boolean visibilitas_VALUE = Kata_SMS(nama_konstanta, "show_jendela"); int elemen_VALUE = 빼기(2); if (!화면객체(elemen_VALUE)) return;
            if (ruang_pengguna.화면연결(visibilitas_VALUE ? 3 : 4, 힙[elemen_VALUE + 2], visibilitas_VALUE ? 1 : 0, 0, 0, 0) < 0) { kegagalan_VALUE("화면은 interaktif 명령에서 실행해야 합니다"); return; }
            힙[elemen_VALUE + 9] = visibilitas_VALUE ? 1 : 0; return;
        }
        if (Kata_SMS(nama_konstanta, "보이는가") && Kata_SMS(서술상수, "()Z")) { int elemen_VALUE = 빼기(2); if (화면객체(elemen_VALUE)) 넣기(힙[elemen_VALUE + 9], 1); return; }
        kegagalan_VALUE("지원하지 않는 Indonesia 화면 metode_VALUE");
    }
    static void 화면호출(int pemilik, int nama_konstanta, int 서술상수, int perintah_CODE) {
        if (Kata_SMS(pemilik, "javax/swing/SwingUtilities")) {
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "invokeLater") && Kata_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objek_Referensi = 빼기(2); if (!객체유효(objek_Referensi)) return; if (나중수 == 8) { kegagalan_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objek_Referensi; return; }
            if (perintah_CODE == 184 && Kata_SMS(nama_konstanta, "isEventDispatchThread") && Kata_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kegagalan_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Kata_SMS(pemilik, "java/awt/event/ActionEvent")) {
            int objek_Referensi = 빼기(2); if (!objek_VALUE(objek_Referensi, 29)) return;
            if (Kata_SMS(nama_konstanta, "getSource") && Kata_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objek_Referensi + 2], 2);
            else if (Kata_SMS(nama_konstanta, "getActionCommand") && Kata_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objek_Referensi + 2]), 2);
            else if (Kata_SMS(nama_konstanta, "getID") && Kata_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kegagalan_VALUE("unsupported ActionEvent method"); return;
        }
        if (perintah_CODE == 183 && Kata_SMS(nama_konstanta, "<init>")) {
            int COLUMNS = 0, SMS_Referensi = 0;
            if (Kata_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Kata_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Referensi = 빼기(2); }
            else if (Kata_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Referensi = 빼기(2);
            else if (Kata_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Kata_SMS(서술상수, "()V")) { kegagalan_VALUE("unsupported Swing constructor"); return; }
            int objek_Referensi = 빼기(2); if (!객체유효(objek_Referensi)) return;
            if (힙[objek_Referensi] == 30) { kegagalan_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objek_Referensi) || COLUMNS < 0) return;
            int akun_VALUE = ruang_pengguna.화면연결(0, 힙[objek_Referensi] - 23, 0, 0, 0, 0);
            if (akun_VALUE < 1 || akun_VALUE > 32) { kegagalan_VALUE("GUI widget slots exhausted"); return; }
            힙[objek_Referensi + 2] = akun_VALUE; 화면참조[akun_VALUE - 1] = objek_Referensi; 힙[objek_Referensi + 5] = 힙[objek_Referensi] == 24 ? 130 : 16; 힙[objek_Referensi + 6] = 힙[objek_Referensi] == 24 ? 110 : 16;
            힙[objek_Referensi + 7] = 힙[objek_Referensi] == 24 ? 380 : 220; 힙[objek_Referensi + 8] = 힙[objek_Referensi] == 24 ? 240 : 28; 힙[objek_Referensi + 10] = 1;
            화면문자설정(objek_Referensi, SMS_Referensi); return;
        }
        if (Kata_SMS(nama_konstanta, "setText") || Kata_SMS(nama_konstanta, "setTitle")) { int SMS_Referensi = 빼기(2), objek_Referensi = 빼기(2); if (화면객체(objek_Referensi) && Kata_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objek_Referensi, SMS_Referensi); return; }
        if (Kata_SMS(nama_konstanta, "getText") || Kata_SMS(nama_konstanta, "getTitle")) { int objek_Referensi = 빼기(2); if (화면객체(objek_Referensi) && Kata_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objek_Referensi), 2); return; }
        if (Kata_SMS(nama_konstanta, "addActionListener") && Kata_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int terima_Referensi = 빼기(2), objek_Referensi = 빼기(2); if (화면객체(objek_Referensi)) { 힙[objek_Referensi + 4] = terima_Referensi; 힙참조[objek_Referensi + 4] = 1; } return; }
        if (Kata_SMS(nama_konstanta, "getContentPane") && Kata_SMS(서술상수, "()Ljava/awt/Container;")) { int objek_Referensi = 빼기(2); if (화면객체(objek_Referensi)) 넣기(objek_Referensi, 2); return; }
        if (Kata_SMS(nama_konstanta, "setLayout") && Kata_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Navigasi_Referensi = 빼기(2), objek_Referensi = 빼기(2); if (화면객체(objek_Referensi) && Navigasi_Referensi != 0) kegagalan_VALUE("only absolute layout (null) is supported"); return; }
        if (Kata_SMS(nama_konstanta, "add") && (Kata_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Kata_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Navigasi_kondisi = Kata_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Navigasi_kondisi) 빼기(2);
            int turunan_Referensi = 빼기(2), objek_Referensi = 빼기(2); if (!화면객체(turunan_Referensi) || !화면객체(objek_Referensi)) return;
            if (ruang_pengguna.화면연결(2, 힙[objek_Referensi + 2], 힙[turunan_Referensi + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[turunan_Referensi + 11] = objek_Referensi; 힙참조[turunan_Referensi + 11] = 1; if (!Navigasi_kondisi) 넣기(turunan_Referensi, 2); return;
        }
        if (Kata_SMS(nama_konstanta, "setBounds") && Kata_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), koordinat_x = 빼기(1), objek_Referensi = 빼기(2); if (!화면객체(objek_Referensi)) return;
            if (ruang_pengguna.화면연결(1, 힙[objek_Referensi + 2], koordinat_x, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objek_Referensi + 5] = koordinat_x; 힙[objek_Referensi + 6] = Y_koordinat; 힙[objek_Referensi + 7] = 너비; 힙[objek_Referensi + 8] = 높이; return;
        }
        if (Kata_SMS(nama_konstanta, "setSize") && Kata_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objek_Referensi = 빼기(2); if (!화면객체(objek_Referensi)) return;
            if (ruang_pengguna.화면연결(1, 힙[objek_Referensi + 2], 힙[objek_Referensi + 5], 힙[objek_Referensi + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objek_Referensi + 7] = 너비; 힙[objek_Referensi + 8] = 높이; } return;
        }
        if (Kata_SMS(nama_konstanta, "setLocationRelativeTo") && Kata_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objek_Referensi = 빼기(2); if (!화면객체(objek_Referensi)) return; if (상대배치 != 0) { kegagalan_VALUE("only screen centering supported"); return; } 힙[objek_Referensi + 5] = (ruang_pengguna.화면너비() - 힙[objek_Referensi + 7]) / 2; 힙[objek_Referensi + 6] = (ruang_pengguna.화면높이() - 힙[objek_Referensi + 8]) / 2; ruang_pengguna.화면연결(1, 힙[objek_Referensi + 2], 힙[objek_Referensi + 5], 힙[objek_Referensi + 6], 힙[objek_Referensi + 7], 힙[objek_Referensi + 8]); return; }
        if (Kata_SMS(nama_konstanta, "setDefaultCloseOperation") && Kata_SMS(서술상수, "(I)V")) { int Policy = 빼기(1), objek_Referensi = 빼기(2); if (화면객체(objek_Referensi)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { 힙[objek_Referensi + 10] = Policy; ruang_pengguna.화면연결(7, 힙[objek_Referensi + 2], Policy, 0, 0, 0); } } return; }
        if (Kata_SMS(nama_konstanta, "setVisible") && Kata_SMS(서술상수, "(Z)V")) { int data_VALUE = 빼기(1), objek_Referensi = 빼기(2); if (화면객체(objek_Referensi)) { int 처리값 = ruang_pengguna.화면연결(3, 힙[objek_Referensi + 2], data_VALUE, 0, 0, 0); if (처리값 < 0) kegagalan_VALUE("Swing requires a standalone interactive command"); else 힙[objek_Referensi + 9] = data_VALUE; } return; }
        if (Kata_SMS(nama_konstanta, "dispose") && Kata_SMS(서술상수, "()V")) { int objek_Referensi = 빼기(2); if (화면객체(objek_Referensi)) { ruang_pengguna.화면연결(4, 힙[objek_Referensi + 2], 0, 0, 0, 0); 힙[objek_Referensi + 9] = 0; } return; }
        if (Kata_SMS(nama_konstanta, "repaint") || Kata_SMS(nama_konstanta, "validate")) { int objek_Referensi = 빼기(2); if (!화면객체(objek_Referensi) || !Kata_SMS(서술상수, "()V")) return; ruang_pengguna.화면연결(1, 힙[objek_Referensi + 2], 힙[objek_Referensi + 5], 힙[objek_Referensi + 6], 힙[objek_Referensi + 7], 힙[objek_Referensi + 8]); return; }
        if (Kata_SMS(nama_konstanta, "isVisible") && Kata_SMS(서술상수, "()Z")) { int objek_Referensi = 빼기(2); if (화면객체(objek_Referensi)) 넣기(힙[objek_Referensi + 9], 1); return; }
        kegagalan_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int target_surel, int 사건번호, boolean Indonesia) {
        if (target_surel < 1 || 힙[target_surel] < 32) { kegagalan_VALUE("Java event listener required"); return; }
        int file_INDEX = nama_metode(힙[target_surel] - 32, 사건번호 == 0 ? (Indonesia ? "Eksekusi" : "run") : (Indonesia ? "terima_Tugas" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Indonesia ? "(LIndonesia/Asli/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (file_INDEX < 0) { kegagalan_VALUE("event callback missing"); return; }
        saat_ini_alur = 0; alur_COUNT = 1; bingkai_INDEX = 0; alur_Status[0] = 1; bingkai_tumpuk[0] = 0; bingkai_kunci[0] = berinisial_bingkai[0] = 0; ubah_permintaan = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokal_VALUE[Loop_INDEX] = lokal_TYPE[Loop_INDEX] = 0; }
        bingkai_metode[0] = file_INDEX; bingkai_posisi[0] = metode_Mulai[file_INDEX]; lokal_VALUE[0] = target_surel; lokal_TYPE[0] = 2;
        if (사건번호 != 0) { lokal_VALUE[1] = 사건번호; lokal_TYPE[1] = 2; }
        사건중 = true; Jalankan_perintah(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!galat) {
            if (나중수 > 0) { int target_surel = 나중실행[0], Indonesia = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(target_surel, 0, Indonesia != 0); continue; }
            if (ruang_pengguna.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = ruang_pengguna.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { kegagalan_VALUE("GUI event I/O failed"); return; }
            int akun_VALUE = 사건번호 & 65535; if (akun_VALUE < 1 || akun_VALUE > 32) continue; int objek_Referensi = 화면참조[akun_VALUE - 1]; if (objek_Referensi == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objek_Referensi + 10] != 0) 힙[objek_Referensi + 9] = 0;
                if (힙[objek_Referensi + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) ruang_pengguna.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objek_Referensi + 4] != 0) {
                int baca_saya_Referensi = alokasi_Storage(29, 2); if (galat) return; 힙[baca_saya_Referensi + 2] = objek_Referensi; 힙[baca_saya_Referensi + 3] = 힙[objek_Referensi + 12]; 힙참조[baca_saya_Referensi + 2] = 1; 사건실행(힙[objek_Referensi + 4], baca_saya_Referensi, 힙[objek_Referensi + 12] != 0);
            }
        }
    }
    public static int jalankan() {
        if (ruang_pengguna.인수개수() == 1 && 자바도구.같음(ruang_pengguna.argumen(0), "-version")) {
            ruang_pengguna.Tulis("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (ruang_pengguna.인수개수() < 1) { ruang_pengguna.Tulis("Usage: java CLASS [ARGS]\n"); return 2; }
        entri_Kelas_Definisi = muat_Kelas_Definisi(host_karakter(ruang_pengguna.argumen(0))); if (galat || entri_Kelas_Definisi < 0) return 1;
        int entri_p_VALUE = nama_metode(entri_Kelas_Definisi, "jalankan", "()V");
        boolean 한국어진입 = entri_p_VALUE >= 0 && (metode_akses[entri_p_VALUE] & 9) == 9;
        if (!한국어진입) entri_p_VALUE = nama_metode(entri_Kelas_Definisi, "main", "([Ljava/lang/String;)V");
        if (entri_p_VALUE < 0 || (metode_akses[entri_p_VALUE] & 9) != 9) kegagalan_VALUE("public static void jalankan() or main(String[] args) required");
        if (galat) return 1;
        int argumen = alokasi_Storage(3, ruang_pengguna.인수개수() - 1); barisan_elemen[argumen] = -1;
        for (int 수 = 1; 수 < ruang_pengguna.인수개수() && !galat; 수++) 힙[argumen + 1 + 수] = host_karakter(ruang_pengguna.argumen(수));
        bingkai_INDEX = 0; bingkai_metode[0] = entri_p_VALUE; bingkai_posisi[0] = metode_Mulai[entri_p_VALUE]; lokal_VALUE[0] = 한국어진입 ? 0 : argumen; lokal_TYPE[0] = 한국어진입 ? 0 : 2;
        alur_Status[0] = 1; alur_objek[0] = alokasi_Storage(13, 2);
        Jalankan_perintah(); if (!galat) 화면사건들(); return galat ? 1 : 0;
    }
}
