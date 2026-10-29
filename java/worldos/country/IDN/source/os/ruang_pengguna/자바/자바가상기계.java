// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. berkas/operand_tumpuk/Referensi/cabang 경계를 Jalankan_perintah 중 검사한다. */
public final class 자바가상기계 {
    static int[] berkas = new int[16384], nama_file_SMS = new int[64];
    static int[] konstanta_tag = new int[512], 상가 = new int[512], konstanta_SECOND_VALUE = new int[512], string_Referensi = new int[512];
    static int[] metode_nama_SMS = new int[32], metode_TYPE = new int[32], metode_akses = new int[32];
    static int[] metode_Mulai = new int[32], metode_mengakhiri = new int[32], metode_tumpuk = new int[32], 함수지역 = new int[32];
    static int[] metode_argumen_COUNT = new int[32], metode_argumen_TYPE = new int[512], metode_kembalikan = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokal_VALUE = new int[4096], lokal_TYPE = new int[4096], operand_tumpuk_VALUE = new int[4096], operand_tumpuk_TYPE = new int[4096];
    static int[] bingkai_metode = new int[32], bingkai_posisi = new int[32], bingkai_tumpuk = new int[32];
    static int[] 힙 = new int[8192];
    static int Ukuran, 읽기위치, konstanta_COUNT, metode_COUNT, nama_kelas, bingkai_INDEX = -1, 힙끝 = 1, kembalikan_TYPE;
    static boolean galat;

    static void kegagalan_VALUE(String Kata_SMS) {
        if (!galat) { ruang_pengguna.Tulis("JVM error: "); ruang_pengguna.Tulis(Kata_SMS); ruang_pengguna.tulis_karakter_VALUE(10); }
        galat = true;
    }
    static boolean klip(int jalankan, int panjang_VALUE) { return jalankan >= 0 && panjang_VALUE >= 0 && jalankan <= Ukuran - panjang_VALUE; }
    static int byte_VALUE() {
        if (!klip(읽기위치, 1)) { kegagalan_VALUE("truncated class file"); return 0; }
        return berkas[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int bilangan_bulat() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int panjang_VALUE) { if (!klip(읽기위치, panjang_VALUE)) kegagalan_VALUE("invalid attribute size"); else 읽기위치 += panjang_VALUE; }
    static boolean cek_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_COUNT || konstanta_tag[수] != 종류) { kegagalan_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_rentang(int jalankan, int panjang_VALUE, String Kata_SMS) {
        if (!klip(jalankan, panjang_VALUE) || panjang_VALUE != Kata_SMS.length()) return false;
        for (int 수 = 0; 수 < panjang_VALUE; 수++) if (berkas[jalankan + 수] != Kata_SMS.charAt(수)) return false;
        return true;
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
    static void lompati_atribut() {
        int item_COUNT = 짧은수();
        for (int 수 = 0; 수 < item_COUNT && !galat; 수++) { cek_konstanta(짧은수(), 1); 건너(bilangan_bulat()); }
    }
    static int perintah_panjang(int VALUE) {
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
        if (bilangan_bulat() != 0xcafebabe) kegagalan_VALUE("not a class file");
        int 부판 = 짧은수(), versi_VALUE = 짧은수();
        if (versi_VALUE < 45 || versi_VALUE > 52 || 부판 != 0) kegagalan_VALUE("supported class versions: 45..52, minor 0");
        konstanta_COUNT = 짧은수();
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { kegagalan_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstanta_COUNT && !galat; 수++) {
            int 종류 = byte_VALUE(); konstanta_tag[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = bilangan_bulat();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstanta_SECOND_VALUE[수] = 짧은수(); }
            else kegagalan_VALUE("unsupported constant type");
        }
        int izin_VALUE = 짧은수();
        if ((izin_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) kegagalan_VALUE("unsupported class flags");
        nama_kelas = nama_kelas_SMS(짧은수());
        if (!Kata_SMS(nama_kelas_SMS(짧은수()), "java/lang/Object")) kegagalan_VALUE("inheritance unsupported");
        if (짧은수() != 0) kegagalan_VALUE("interfaces unsupported");
        if (짧은수() != 0) kegagalan_VALUE("fields unsupported");
        metode_COUNT = 짧은수();
        if (metode_COUNT < 1 || metode_COUNT > 32) { kegagalan_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metode_COUNT && !galat; 수++) {
            metode_akses[수] = 짧은수(); metode_nama_SMS[수] = 짧은수(); metode_TYPE[수] = 짧은수();
            cek_konstanta(metode_nama_SMS[수], 1); 서술읽기(수);
            if ((metode_akses[수] & (0x100 | 0x400 | 0x20)) != 0) kegagalan_VALUE("native, abstract and synchronized methods unsupported");
            if ((metode_akses[수] & 8) == 0 && !Kata_SMS(metode_nama_SMS[수], "<init>")) kegagalan_VALUE("instance methods unsupported");
            if (Kata_SMS(metode_nama_SMS[수], "<clinit>")) kegagalan_VALUE("class initializers unsupported");
            for (int depan_VALUE = 0; depan_VALUE < 수; depan_VALUE++) if (같은말(metode_nama_SMS[depan_VALUE], metode_nama_SMS[수]) && 같은말(metode_TYPE[depan_VALUE], metode_TYPE[수])) kegagalan_VALUE("duplicate method");
            int item_COUNT = 짧은수();
            for (int nilai_atribut = 0; nilai_atribut < item_COUNT && !galat; nilai_atribut++) {
                int Nama_2 = 짧은수(), panjang_VALUE = bilangan_bulat(), jalankan = 읽기위치;
                if (!klip(jalankan, panjang_VALUE)) { kegagalan_VALUE("truncated method attribute"); break; }
                if (Kata_SMS(Nama_2, "Code")) {
                    if (metode_Mulai[수] != 0) kegagalan_VALUE("duplicate Code attribute");
                    metode_tumpuk[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_panjang = bilangan_bulat();
                    if (metode_tumpuk[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metode_argumen_COUNT[수]
                        || CODE_panjang < 1 || CODE_panjang > 8192) kegagalan_VALUE("method memory limits exceeded");
                    metode_Mulai[수] = 읽기위치; 건너(CODE_panjang); metode_mengakhiri[수] = 읽기위치;
                    if (짧은수() != 0) kegagalan_VALUE("exception handlers unsupported");
                    lompati_atribut();
                    if (읽기위치 != jalankan + panjang_VALUE) kegagalan_VALUE("Code attribute size mismatch");
                } else 건너(panjang_VALUE);
            }
            if (metode_Mulai[수] == 0) kegagalan_VALUE("missing Code attribute");
            int slot_entri = metode_Mulai[수];
            while (slot_entri < metode_mengakhiri[수] && !galat) {
                int panjang_VALUE = perintah_panjang(berkas[slot_entri]);
                if (panjang_VALUE == 0 || panjang_VALUE > metode_mengakhiri[수] - slot_entri) { kegagalan_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_entri] = 수 + 1; slot_entri += panjang_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 cabang 목적지를 허용하지 않는다.
            slot_entri = metode_Mulai[수];
            while (slot_entri < metode_mengakhiri[수] && !galat) {
                int VALUE = berkas[slot_entri];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int tujuan_VALUE = slot_entri + (short)(berkas[slot_entri + 1] << 8 | berkas[slot_entri + 2]);
                    if (tujuan_VALUE < metode_Mulai[수] || tujuan_VALUE >= metode_mengakhiri[수] || 경계[tujuan_VALUE] != 수 + 1) kegagalan_VALUE("invalid branch target");
                }
                slot_entri += perintah_panjang(VALUE);
            }
        }
        if (!galat) lompati_atribut();
        if (읽기위치 != Ukuran) kegagalan_VALUE("extra class file data");
    }
    static int alokasi_Storage(int 종류, int panjang_VALUE) {
        if (panjang_VALUE < 0 || panjang_VALUE > 힙.length - 힙끝 - 2) { kegagalan_VALUE("object heap exhausted or negative array size"); return 0; }
        int Referensi = 힙끝; 힙끝 += panjang_VALUE + 2; 힙[Referensi] = 종류; 힙[Referensi + 1] = panjang_VALUE;
        return Referensi;
    }
    static boolean objek_VALUE(int Referensi, int 종류) {
        if (Referensi < 1 || Referensi >= 힙끝 - 1 || 힙[Referensi] != 종류) { kegagalan_VALUE("null or invalid object reference"); return false; }
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
        if (bingkai_INDEX == 31) { kegagalan_VALUE("call stack limit (32)"); return; }
        int Berikutnya_item = bingkai_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Berikutnya_item * 128 + 수] = 0;
        for (int 수 = metode_argumen_COUNT[fungsi_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Berikutnya_item * 128 + 수] = 빼기(metode_argumen_TYPE[fungsi_VALUE * 16 + 수]); lokal_TYPE[Berikutnya_item * 128 + 수] = metode_argumen_TYPE[fungsi_VALUE * 16 + 수];
        }
        bingkai_INDEX = Berikutnya_item; bingkai_metode[bingkai_INDEX] = fungsi_VALUE; bingkai_posisi[bingkai_INDEX] = metode_Mulai[fungsi_VALUE]; bingkai_tumpuk[bingkai_INDEX] = 0;
    }
    static void kembalikan_KR(int TYPE_VALUE) {
        if (TYPE_VALUE != metode_kembalikan[bingkai_metode[bingkai_INDEX]]) { kegagalan_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        bingkai_INDEX--; if (bingkai_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { kegagalan_VALUE("file stream paths currently require ASCII"); return; }
                Stream_nama_file[slot_entri] = VALUE;
            }
            Stream_nama_file[panjang_VALUE] = 0;
            int 서술자 = ruang_pengguna.파일서술자열기(Stream_nama_file, keluaranTeks ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kegagalan_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (perintah != 182) { kegagalan_VALUE("invalid file stream invocation"); return; }
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
            if (hasil < -1) kegagalan_VALUE("IOException: read failed"); else 넣기(hasil, 1);
        } else if (ruang_pengguna.파일한바이트쓰기(서술자, VALUE) != 1) kegagalan_VALUE("IOException: write failed");
    }
    static void CALL_metode(int INDEX, int perintah) {
        if (!cek_konstanta(INDEX, 10)) return;
        int pemilik_VALUE = nama_kelas_SMS(상가[INDEX]), Nama_2 = Referensi_nama(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Referensi_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (galat) return;
        if (같은말(pemilik_VALUE, nama_kelas)) {
            if (perintah != 184) { kegagalan_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metode_COUNT; 수++) if (같은말(Nama_2, metode_nama_SMS[수]) && 같은말(format_VALUE, metode_TYPE[수])) {
                if ((metode_akses[수] & 8) == 0) kegagalan_VALUE("method is not static"); else 호출(수);
                return;
            }
            kegagalan_VALUE("NoSuchMethodError"); return;
        }
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
        kegagalan_VALUE("unsupported library method");
    }
    static int ARRAY_slot(int Referensi, int subskrip_VALUE, int TYPE_VALUE) {
        if (!objek_VALUE(Referensi, TYPE_VALUE)) return 0;
        if (subskrip_VALUE < 0 || subskrip_VALUE >= 힙[Referensi + 1]) { kegagalan_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referensi + 2 + subskrip_VALUE;
    }
    static void Jalankan_perintah() {
        int 남음 = 500000;
        while (bingkai_INDEX >= 0 && !galat) {
            if (--남음 == 0) { kegagalan_VALUE("instruction limit (500000)"); break; }
            int jalankan = bingkai_posisi[bingkai_INDEX], VALUE = 명바();
            if (galat) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstanta_COUNT) kegagalan_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int subskrip_VALUE = 빼기(1), Referensi = 빼기(2), slot_entri = ARRAY_slot(Referensi, subskrip_VALUE, VALUE == 46 ? 2 : 3);
                if (!galat) 넣기(힙[slot_entri], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int item_elemen = 빼기(VALUE == 79 ? 1 : 2), subskrip_VALUE = 빼기(1), Referensi = 빼기(2), slot_entri = ARRAY_slot(Referensi, subskrip_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && item_elemen != 0) objek_VALUE(item_elemen, 1);
                if (!galat) 힙[slot_entri] = item_elemen; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = kembalikan_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = kembalikan_TYPE, SECOND_operand = 빼기(0), SECOND_operand_TYPE = kembalikan_TYPE; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_TYPE); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!cek_konstanta(수, 9)) continue;
                if (!Kata_SMS(nama_kelas_SMS(상가[수]), "java/lang/System") || !Kata_SMS(Referensi_nama(konstanta_SECOND_VALUE[수]), "out")
                    || !Kata_SMS(Referensi_TYPE(konstanta_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) kegagalan_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metode(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Nama_2 = nama_kelas_SMS(명짧());
                if (Kata_SMS(Nama_2, "java/lang/StringBuilder")) 넣기(alokasi_Storage(4, 1), 2);
                else if (Kata_SMS(Nama_2, "java/io/FileInputStream") || Kata_SMS(Nama_2, "java/io/FileOutputStream")) {
                    int Referensi = alokasi_Storage(Kata_SMS(Nama_2, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!galat) { 힙[Referensi + 2] = -1; 넣기(Referensi, 2); }
                } else kegagalan_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) kegagalan_VALUE("only int[] newarray is supported"); }
                else if (!Kata_SMS(nama_kelas_SMS(명짧()), "java/lang/String")) kegagalan_VALUE("only String[] anewarray is supported");
                int panjang_VALUE = 빼기(1); 넣기(alokasi_Storage(VALUE == 188 ? 2 : 3, panjang_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Referensi = 빼기(2);
                if (Referensi < 1 || Referensi >= 힙끝 - 1 || (힙[Referensi] != 2 && 힙[Referensi] != 3)) kegagalan_VALUE("null or invalid array");
                else 넣기(힙[Referensi + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Nama_2 = nama_kelas_SMS(명짧()), Referensi = 빼기(2);
                if (!Kata_SMS(Nama_2, "java/lang/String")) kegagalan_VALUE("unsupported checkcast");
                else if (Referensi != 0) objek_VALUE(Referensi, 1);
                넣기(Referensi, 2); continue;
            }
            kegagalan_VALUE("unsupported bytecode");
        }
    }
    public static int jalankan() {
        if (ruang_pengguna.인수개수() == 1 && 자바도구.같음(ruang_pengguna.argumen(0), "-version")) {
            ruang_pengguna.Tulis("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (ruang_pengguna.인수개수() < 1) { ruang_pengguna.Tulis("Usage: java CLASS [ARGS]\n"); return 2; }
        int panjang_VALUE = 자바도구.Nama_2(nama_file_SMS, ruang_pengguna.argumen(0));
        if (panjang_VALUE < 1 || panjang_VALUE > 57) { ruang_pengguna.Tulis("java: invalid class name\n"); return 2; }
        nama_file_SMS[panjang_VALUE] = '.'; nama_file_SMS[panjang_VALUE + 1] = 'c'; nama_file_SMS[panjang_VALUE + 2] = 'l'; nama_file_SMS[panjang_VALUE + 3] = 'a'; nama_file_SMS[panjang_VALUE + 4] = 's'; nama_file_SMS[panjang_VALUE + 5] = 's';
        Ukuran = ruang_pengguna.파일읽기(nama_file_SMS, berkas);
        if (Ukuran < 0) { ruang_pengguna.Tulis("java: cannot read class: "); 자바도구.수쓰기(Ukuran); ruang_pengguna.tulis_karakter_VALUE(10); return 1; }
        클래스읽기(); if (galat) return 1;
        int karakter_nama = konstanta_SMS(nama_kelas);
        if (!galat && 힙[karakter_nama + 1] != panjang_VALUE) kegagalan_VALUE("class name does not match file");
        for (int 수 = 0; 수 < panjang_VALUE && !galat; 수++) if (힙[karakter_nama + 2 + 수] != nama_file_SMS[수]) kegagalan_VALUE("class name does not match file");
        int entri_p_VALUE = -1;
        for (int 수 = 0; 수 < metode_COUNT; 수++) if (Kata_SMS(metode_nama_SMS[수], "main") && Kata_SMS(metode_TYPE[수], "([Ljava/lang/String;)V") && (metode_akses[수] & 9) == 9) entri_p_VALUE = 수;
        if (entri_p_VALUE < 0) kegagalan_VALUE("public static void main(String[] args) required");
        if (galat) return 1;
        int argumen = alokasi_Storage(3, ruang_pengguna.인수개수() - 1);
        for (int 수 = 1; 수 < ruang_pengguna.인수개수() && !galat; 수++) 힙[argumen + 1 + 수] = host_karakter(ruang_pengguna.argumen(수));
        bingkai_INDEX = 0; bingkai_metode[0] = entri_p_VALUE; bingkai_posisi[0] = metode_Mulai[entri_p_VALUE]; lokal_VALUE[0] = argumen; lokal_TYPE[0] = 2;
        Jalankan_perintah(); return galat ? 1 : 0;
    }
}
