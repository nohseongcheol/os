// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Kartelë/스택/Referencë/degë 경계를 zbatoj_komandë 중 검사한다. */
public final class 자바가상기계 {
    static int[] Kartelë = new int[16 * 16384], 임시파일 = new int[16384], skedar_emër_SMS = new int[512];
    static int[] konstante_shenjë = new int[8192], 상가 = new int[8192], konstante_SECOND_VALUE = new int[8192], varg_Referencë = new int[8192];
    static int[] metoda_emër_SMS = new int[512], metoda_TYPE = new int[512], metoda_qasem = new int[512], metoda_pronari = new int[512];
    static int[] metoda_nis = new int[512], metoda_mbaroj = new int[512], metoda_Stivë = new int[512], 함수지역 = new int[512];
    static int[] metoda_argument_COUNT = new int[512], metoda_argument_TYPE = new int[8192], metoda_Kthe = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokal_VALUE = new int[16384], lokal_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] kuadër_metoda = new int[128], kuadër_pozicioni = new int[128], kuadër_Stivë = new int[128], kuadër_instruksion = new int[128], filloj_kuadër = new int[128];
    static int[] klasë_Përkufizim_emër = new int[16], klasë_Përkufizim_ndryshoj_përmasat = new int[16], 종부모 = new int[16], klasë_Përkufizim_status = new int[16], klasë_hapësirë_për_tekst_COUNT = new int[16], filloj_klasë_Përkufizim = new int[16];
    static int[] klasë_ndërfaqe = new int[16 * 16], klasë_ndërfaqe_COUNT = new int[16];
    static int[] hapësirë_për_tekst_emër = new int[512], hapësirë_për_tekst_TYPE = new int[512], hapësirë_për_tekst_pronari = new int[512], hapësirë_për_tekst_Lejet = new int[512], hapësirë_për_tekst_pozicioni = new int[512], hapësirë_për_tekst_të_dhëna = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_element = new int[32768], Store_numër_i_plotë = new int[256];
    static int Madhësi, 읽기위치, metoda_COUNT, klasë_emër, kuadër_INDEX = -1, 힙끝 = 1, Kthe_TYPE;
    static int klasë_Përkufizim_COUNT, hapësirë_për_tekst_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, afishim_COUNT, Koleksion_COUNT;
    static int 현재가닥, thread_COUNT = 1, futje_klasë_Përkufizim;
    static int[] thread_kuadër = new int[4], thread_status = new int[4], thread_objekt = new int[4], thread_objektiv = new int[4], 가닥대기 = new int[4];
    static boolean GABIM, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], klasë_thread = new int[16];

    static void dështim_VALUE(String Word_SMS) {
        if (GABIM) return;
        int kategori_kod = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) kategori_kod = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) kategori_kod = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) kategori_kod = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) kategori_kod = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) kategori_kod = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) kategori_kod = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) kategori_kod = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) kategori_kod = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) kategori_kod = 15;
        if (kategori_kod != 0 && kuadër_INDEX >= 0) { 예외던짐(kategori_kod, Word_SMS); return; }
        përdorues.Shkrimi("JVM error: "); përdorues.Shkrimi(Word_SMS); përdorues.shkruaj_karakter_VALUE(10); GABIM = true;
    }
    static boolean fragment(int Ekzekuto, int gjatësi_VALUE) {
        if (Ekzekuto < 0 || Ekzekuto >= Kartelë.length || gjatësi_VALUE < 0) return false;
        int klasë_Përkufizim = Ekzekuto / 16384;
        return Ekzekuto % 16384 <= klasë_Përkufizim_ndryshoj_përmasat[klasë_Përkufizim] && gjatësi_VALUE <= klasë_Përkufizim_ndryshoj_përmasat[klasë_Përkufizim] - Ekzekuto % 16384;
    }
    static int bajt_VALUE() {
        if (!fragment(읽기위치, 1)) { dështim_VALUE("truncated class file"); return 0; }
        return Kartelë[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int numër_i_plotë() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int gjatësi_VALUE) { if (!fragment(읽기위치, gjatësi_VALUE)) dështim_VALUE("invalid attribute size"); else 읽기위치 += gjatësi_VALUE; }
    static boolean çek_konstante(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstante_shenjë.length || konstante_shenjë[수] != 종류) { dështim_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Ekzekuto, int gjatësi_VALUE, String Word_SMS) {
        if (!fragment(Ekzekuto, gjatësi_VALUE)) return false;
        int 읽는자리 = Ekzekuto, 끝 = Ekzekuto + gjatësi_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int kodi_i_karakterit = Word_SMS.charAt(Loop_INDEX);
            if (kodi_i_karakterit > 0 && kodi_i_karakterit < 128) { if (읽는자리 >= 끝 || Kartelë[읽는자리++] != kodi_i_karakterit) return false; }
            else if (kodi_i_karakterit < 2048) {
                if (읽는자리 + 2 > 끝 || Kartelë[읽는자리++] != (192 | (kodi_i_karakterit >> 6)) || Kartelë[읽는자리++] != (128 | (kodi_i_karakterit & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Kartelë[읽는자리++] != (224 | (kodi_i_karakterit >> 12)) || Kartelë[읽는자리++] != (128 | ((kodi_i_karakterit >> 6) & 63)) || Kartelë[읽는자리++] != (128 | (kodi_i_karakterit & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstante_VALUE, String Word_SMS) { return çek_konstante(konstante_VALUE, 1) && 구간(상가[konstante_VALUE], konstante_SECOND_VALUE[konstante_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!çek_konstante(가, 1) || !çek_konstante(나, 1) || konstante_SECOND_VALUE[가] != konstante_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < konstante_SECOND_VALUE[가]; 수++) if (Kartelë[상가[가] + 수] != Kartelë[상가[나] + 수]) return false;
        return true;
    }
    static int klasë_emër_SMS(int 수) { return çek_konstante(수, 7) && çek_konstante(상가[수], 1) ? 상가[수] : 0; }
    static int Referencë_emër(int 수) { return çek_konstante(수, 12) && çek_konstante(상가[수], 1) ? 상가[수] : 0; }
    static int Referencë_TYPE(int 수) { return çek_konstante(수, 12) && çek_konstante(konstante_SECOND_VALUE[수], 1) ? konstante_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean bosh_TYPE) {
        if (읽기위치 >= 끝) { dështim_VALUE("invalid descriptor"); return 0; }
        int VALUE = bajt_VALUE();
        if (VALUE == 'V' && bosh_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Ekzekuto = 읽기위치;
            while (읽기위치 < 끝 && Kartelë[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Ekzekuto) dështim_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        dështim_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metoda_TYPE[FUNCTION_VALUE];
        if (!çek_konstante(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstante_SECOND_VALUE[수];
        if (bajt_VALUE() != '(') dështim_VALUE("invalid method descriptor");
        int njësi_COUNT = 0;
        while (!GABIM && 읽기위치 < 끝 && Kartelë[읽기위치] != ')') {
            if (njësi_COUNT == 16) { dështim_VALUE("too many method arguments"); break; }
            metoda_argument_TYPE[FUNCTION_VALUE * 16 + njësi_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_VALUE() != ')') dështim_VALUE("invalid method descriptor");
        metoda_Kthe[FUNCTION_VALUE] = 서술형(끝, true); metoda_argument_COUNT[FUNCTION_VALUE] = njësi_COUNT;
        if (읽기위치 != 끝) dështim_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metoda_pronari[kuadër_metoda[kuadër_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int njësi_COUNT = 짧은수();
        for (int 수 = 0; 수 < njësi_COUNT && !GABIM; 수++) { çek_konstante(상번호(), 1); 건너(numër_i_plotë()); }
    }
    static int komandë_gjatësi(int VALUE) {
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
    static int pozicioni_numër_i_plotë(int 읽는자리) {
        if (!fragment(읽는자리, 4)) { dështim_VALUE("truncated bytecode operand"); return 0; }
        return Kartelë[읽는자리] << 24 | Kartelë[읽는자리 + 1] << 16 | Kartelë[읽는자리 + 2] << 8 | Kartelë[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Ekzekuto, int 끝) {
        int VALUE = Kartelë[읽는자리], gjatësi_VALUE = komandë_gjatësi(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_pozicioni = 읽는자리 + 1;
            while ((BASE_pozicioni - Ekzekuto) % 4 != 0) BASE_pozicioni++;
            if (끝 - BASE_pozicioni < (VALUE == 170 ? 12 : 8)) return 0;
            int futje_COUNT = VALUE == 170 ? pozicioni_numër_i_plotë(BASE_pozicioni + 8) - pozicioni_numër_i_plotë(BASE_pozicioni + 4) + 1 : pozicioni_numër_i_plotë(BASE_pozicioni + 4);
            if (futje_COUNT < 0 || futje_COUNT > 2048) return 0;
            gjatësi_VALUE = BASE_pozicioni - 읽는자리 + (VALUE == 170 ? 12 + 4 * futje_COUNT : 8 + 8 * futje_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_të_dhëna = Kartelë[읽는자리 + 1]; gjatësi_VALUE = Word_të_dhëna == 132 ? 6 : (Word_të_dhëna == 21 || Word_të_dhëna == 25 || Word_të_dhëna == 54 || Word_të_dhëna == 58) ? 4 : 0;
        }
        return gjatësi_VALUE > 0 && gjatësi_VALUE <= 끝 - 읽는자리 ? gjatësi_VALUE : 0;
    }
    static void çek_vendmbërritje_VALUE(int vendmbërritje_VALUE, int FUNCTION_VALUE) {
        if (vendmbërritje_VALUE < metoda_nis[FUNCTION_VALUE] || vendmbërritje_VALUE >= metoda_mbaroj[FUNCTION_VALUE] || 경계[vendmbërritje_VALUE] != FUNCTION_VALUE + 1) dështim_VALUE("invalid branch target");
    }
    static void 클래스읽기(int klasë_Përkufizim) {
        현재읽는종 = klasë_Përkufizim; 읽기위치 = klasë_Përkufizim * 16384; Madhësi = 읽기위치 + klasë_Përkufizim_ndryshoj_përmasat[klasë_Përkufizim];
        if (numër_i_plotë() != 0xcafebabe) { dështim_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), version_VALUE = 짧은수();
        if (version_VALUE < 45 || version_VALUE > 52 || 부판 != 0) { dështim_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstante_COUNT = 짧은수(), BASE_pozicioni = klasë_Përkufizim * 512;
        if (konstante_COUNT < 1 || konstante_COUNT > 512) { dështim_VALUE("constant pool limit (511)"); return; }
        for (int futje_COUNT = 1; futje_COUNT < konstante_COUNT && !GABIM; futje_COUNT++) {
            int 수 = BASE_pozicioni + futje_COUNT, 종류 = bajt_VALUE(); konstante_shenjë[수] = 종류;
            if (종류 == 1) { konstante_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstante_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = numër_i_plotë();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstante_SECOND_VALUE[수] = 상번호(); }
            else dështim_VALUE("unsupported constant type");
        }
        int leje_VALUE = 짧은수();
        if ((leje_VALUE & (0x2000 | 0x4000)) != 0) dështim_VALUE("annotation/enum class unsupported");
        klasë_Përkufizim_emër[klasë_Përkufizim] = klasë_emër_SMS(상번호());
        종부모[klasë_Përkufizim] = klasë_emër_SMS(상번호());
        int ndërfaqe_COUNT = 짧은수(); if (ndërfaqe_COUNT > 16) { dështim_VALUE("interface count limit"); return; }
        klasë_ndërfaqe_COUNT[klasë_Përkufizim] = ndërfaqe_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < ndërfaqe_COUNT; Loop_INDEX++) klasë_ndërfaqe[klasë_Përkufizim * 16 + Loop_INDEX] = klasë_emër_SMS(상번호());
        int fushë_COUNT = 짧은수();
        if (fushë_COUNT > 512 - hapësirë_për_tekst_COUNT) { dështim_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < fushë_COUNT && !GABIM; Loop_INDEX++) {
            int skedar_INDEX = hapësirë_për_tekst_COUNT++; hapësirë_për_tekst_pronari[skedar_INDEX] = klasë_Përkufizim; hapësirë_për_tekst_Lejet[skedar_INDEX] = 짧은수(); hapësirë_për_tekst_emër[skedar_INDEX] = 상번호(); hapësirë_për_tekst_TYPE[skedar_INDEX] = 상번호();
            çek_konstante(hapësirë_për_tekst_emër[skedar_INDEX], 1); çek_konstante(hapësirë_për_tekst_TYPE[skedar_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[hapësirë_për_tekst_TYPE[skedar_INDEX]]; int kategori_kod = 서술형(읽기위치 + konstante_SECOND_VALUE[hapësirë_për_tekst_TYPE[skedar_INDEX]], false); 읽기위치 = 보존값;
            if ((hapësirë_për_tekst_Lejet[skedar_INDEX] & 8) == 0) hapësirë_për_tekst_pozicioni[skedar_INDEX] = klasë_hapësirë_për_tekst_COUNT[klasë_Përkufizim]++;
            int atribut_të_dhëna = 짧은수();
            for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < atribut_të_dhëna && !GABIM; bashkim_i_brendshëm_pozicioni++) {
                int emër_konstante = 상번호(), 유효길이 = numër_i_plotë();
                if (Word_SMS(emër_konstante, "ConstantValue") && 유효길이 == 2) {
                    int të_dhëna_VALUE = 상번호();
                    if (kategori_kod == 1 && çek_konstante(të_dhëna_VALUE, 3)) hapësirë_për_tekst_të_dhëna[skedar_INDEX] = 상가[të_dhëna_VALUE];
                    else if (kategori_kod == 2 && çek_konstante(të_dhëna_VALUE, 8)) hapësirë_për_tekst_të_dhëna[skedar_INDEX] = konstante_SMS(상가[të_dhëna_VALUE]);
                } else 건너(유효길이);
            }
        }
        int njësi_COUNT = 짧은수();
        if (njësi_COUNT > 512 - metoda_COUNT) { dështim_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < njësi_COUNT && !GABIM; Loop_INDEX++) {
            int 수 = metoda_COUNT++; metoda_pronari[수] = klasë_Përkufizim;
            metoda_qasem[수] = 짧은수(); metoda_emër_SMS[수] = 상번호(); metoda_TYPE[수] = 상번호();
            çek_konstante(metoda_emër_SMS[수], 1); 서술읽기(수);
            if ((metoda_qasem[수] & 8) == 0) {
                if (metoda_argument_COUNT[수] == 16) { dështim_VALUE("too many instance method arguments"); return; }
                for (int Krahasim_pozicioni = metoda_argument_COUNT[수]; Krahasim_pozicioni > 0; Krahasim_pozicioni--) metoda_argument_TYPE[수 * 16 + Krahasim_pozicioni] = metoda_argument_TYPE[수 * 16 + Krahasim_pozicioni - 1];
                metoda_argument_TYPE[수 * 16] = 2; metoda_argument_COUNT[수]++;
            }
            if ((metoda_qasem[수] & 0x100) != 0) dështim_VALUE("user native method unsupported");
            if (Word_SMS(metoda_emër_SMS[수], "<clinit>")) filloj_klasë_Përkufizim[klasë_Përkufizim] = 수 + 1;
            for (int e_përparme_VALUE = 0; e_përparme_VALUE < 수; e_përparme_VALUE++) if (metoda_pronari[e_përparme_VALUE] == klasë_Përkufizim && 같은말(metoda_emër_SMS[e_përparme_VALUE], metoda_emër_SMS[수]) && 같은말(metoda_TYPE[e_përparme_VALUE], metoda_TYPE[수])) dështim_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !GABIM; atribut_VALUE++) {
                int Emër = 상번호(), gjatësi_VALUE = numër_i_plotë(), Ekzekuto = 읽기위치;
                if (!fragment(Ekzekuto, gjatësi_VALUE)) { dështim_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Emër, "Code")) {
                    if (metoda_nis[수] != 0) dështim_VALUE("duplicate Code attribute");
                    metoda_Stivë[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_gjatësi = numër_i_plotë();
                    if (metoda_Stivë[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metoda_argument_COUNT[수]
                        || kod_gjatësi < 1 || kod_gjatësi > 8192) dështim_VALUE("method memory limits exceeded");
                    metoda_nis[수] = 읽기위치; 건너(kod_gjatësi); metoda_mbaroj[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { dështim_VALUE("exception table limit"); return; }
                    for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 잡는수; bashkim_i_brendshëm_pozicioni++) {
                        int gabim_Referencë = 잡기수++; 잡기함수[gabim_Referencë] = 수;
                        잡기시작[gabim_Referencë] = metoda_nis[수] + 짧은수(); 잡기끝[gabim_Referencë] = metoda_nis[수] + 짧은수();
                        잡기위치[gabim_Referencë] = metoda_nis[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[gabim_Referencë] = 부호값 == 0 ? 0 : klasë_emër_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Ekzekuto + gjatësi_VALUE) dështim_VALUE("Code attribute size mismatch");
                } else 건너(gjatësi_VALUE);
            }
            if ((metoda_qasem[수] & 0x400) != 0) continue;
            if (metoda_nis[수] == 0) dështim_VALUE("missing Code attribute");
            int hapësirë_për_tekst_futje = metoda_nis[수];
            while (hapësirë_për_tekst_futje < metoda_mbaroj[수] && !GABIM) {
                int gjatësi_VALUE = 길이읽기(hapësirë_për_tekst_futje, metoda_nis[수], metoda_mbaroj[수]);
                if (gjatësi_VALUE == 0) { dështim_VALUE("unsupported or truncated bytecode"); break; }
                경계[hapësirë_për_tekst_futje] = 수 + 1; hapësirë_për_tekst_futje += gjatësi_VALUE;
            }
            hapësirë_për_tekst_futje = metoda_nis[수];
            while (hapësirë_për_tekst_futje < metoda_mbaroj[수] && !GABIM) {
                int VALUE = Kartelë[hapësirë_për_tekst_futje];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) çek_vendmbërritje_VALUE(hapësirë_për_tekst_futje + (short)(Kartelë[hapësirë_për_tekst_futje + 1] << 8 | Kartelë[hapësirë_për_tekst_futje + 2]), 수);
                if (VALUE == 200) çek_vendmbërritje_VALUE(hapësirë_për_tekst_futje + pozicioni_numër_i_plotë(hapësirë_për_tekst_futje + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = hapësirë_për_tekst_futje + 1; while ((읽는자리 - metoda_nis[수]) % 4 != 0) 읽는자리++;
                    çek_vendmbërritje_VALUE(hapësirë_për_tekst_futje + pozicioni_numër_i_plotë(읽는자리), 수);
                    int futje_COUNT = VALUE == 170 ? pozicioni_numër_i_plotë(읽는자리 + 8) - pozicioni_numër_i_plotë(읽는자리 + 4) + 1 : pozicioni_numër_i_plotë(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < futje_COUNT; bashkim_i_brendshëm_pozicioni++) çek_vendmbërritje_VALUE(hapësirë_për_tekst_futje + pozicioni_numër_i_plotë(읽는자리 + bashkim_i_brendshëm_pozicioni * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                hapësirë_për_tekst_futje += 길이읽기(hapësirë_për_tekst_futje, metoda_nis[수], metoda_mbaroj[수]);
            }
            for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 잡기수; bashkim_i_brendshëm_pozicioni++) if (잡기함수[bashkim_i_brendshëm_pozicioni] == 수) {
                çek_vendmbërritje_VALUE(잡기시작[bashkim_i_brendshëm_pozicioni], 수); çek_vendmbërritje_VALUE(잡기위치[bashkim_i_brendshëm_pozicioni], 수);
                if (잡기끝[bashkim_i_brendshëm_pozicioni] != metoda_mbaroj[수]) çek_vendmbërritje_VALUE(잡기끝[bashkim_i_brendshëm_pozicioni], 수);
                if (잡기시작[bashkim_i_brendshëm_pozicioni] >= 잡기끝[bashkim_i_brendshëm_pozicioni]) dështim_VALUE("invalid exception range");
            }
        }
        if (!GABIM) 속성건너();
        if (읽기위치 != Madhësi) dështim_VALUE("extra class file data");
    }
    static int caktoj_hapësira_ruajtëse(int 종류, int gjatësi_VALUE) { return 새기억(종류, gjatësi_VALUE); }
    static boolean objekt_VALUE(int Referencë, int 종류) {
        if (!객체유효(Referencë)) return false;
        if (힙[Referencë] != 종류) { dështim_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstante_SMS(int INDEX) {
        if (!çek_konstante(INDEX, 1)) return 0;
        if (varg_Referencë[INDEX] != 0) return varg_Referencë[INDEX];
        int Referencë = caktoj_hapësira_ruajtëse(1, konstante_SECOND_VALUE[INDEX]); if (GABIM) return 0;
        int 끝 = 상가[INDEX] + konstante_SECOND_VALUE[INDEX], 수 = 상가[INDEX], gjatësi_VALUE = 0;
        while (수 < 끝 && !GABIM) {
            int VALUE = Kartelë[수++];
            if (VALUE == 0) dështim_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Tjetër_njësi = Kartelë[수++];
                if ((Tjetër_njësi & 192) != 128) dështim_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Tjetër_njësi & 63;
                if (VALUE != 0 && VALUE < 128) dështim_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Kartelë[수++], 나 = Kartelë[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) dështim_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) dështim_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) dështim_VALUE("invalid modified UTF-8");
            힙[Referencë + 2 + gjatësi_VALUE++] = VALUE;
        }
        힙[Referencë + 1] = gjatësi_VALUE; varg_Referencë[INDEX] = Referencë; return Referencë;
    }
    static int pritës_karakter(String VALUE) {
        int Referencë = caktoj_hapësira_ruajtëse(1, VALUE.length()); if (GABIM) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Referencë + 2 + 수] = VALUE.charAt(수);
        return Referencë;
    }
    static void shkruaj_SMS(int Referencë) {
        if (Referencë == 0) { përdorues.Shkrimi("null"); return; }
        if (!objekt_VALUE(Referencë, 1)) return;
        for (int 수 = 0; 수 < 힙[Referencë + 1]; 수++) përdorues.shkruaj_karakter_VALUE(힙[Referencë + 2 + 수]);
    }
    static int shifër_karakter(int VALUE) {
        int Referencë = caktoj_hapësira_ruajtëse(1, 11); if (GABIM) return 0;
        int gjatësi_VALUE = 0;
        if (VALUE < 0) 힙[Referencë + 2 + gjatësi_VALUE++] = '-'; else VALUE = -VALUE;
        int pozicioni_INDEX = 1000000000; boolean Ekzekuto = false;
        while (pozicioni_INDEX != 0) {
            int 수 = -(VALUE / pozicioni_INDEX);
            if (수 != 0 || Ekzekuto || pozicioni_INDEX == 1) { 힙[Referencë + 2 + gjatësi_VALUE++] = '0' + 수; Ekzekuto = true; }
            VALUE %= pozicioni_INDEX; pozicioni_INDEX /= 10;
        }
        힙[Referencë + 1] = gjatësi_VALUE; return Referencë;
    }
    static int 정수해독(int Referencë) {
        if (!objekt_VALUE(Referencë, 1)) return 0;
        int gjatësi_VALUE = 힙[Referencë + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (gjatësi_VALUE > 0 && (힙[Referencë + 2] == '-' || 힙[Referencë + 2] == '+')) { 음수 = 힙[Referencë + 2] == '-'; 수++; }
        if (수 == gjatësi_VALUE) dështim_VALUE("NumberFormatException");
        for (; 수 < gjatësi_VALUE && !GABIM; 수++) {
            int shifër_VALUE = 힙[Referencë + 2 + 수] - '0';
            if (shifër_VALUE < 0 || shifër_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && shifër_VALUE > (음수 ? 8 : 7)) dështim_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - shifër_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (GABIM) return;
        if (kuadër_INDEX < 0 || kuadër_Stivë[kuadër_INDEX] >= metoda_Stivë[kuadër_metoda[kuadër_INDEX]]) { dështim_VALUE("operand stack overflow"); return; }
        int hapësirë_për_tekst_futje = kuadër_INDEX * 128 + kuadër_Stivë[kuadër_INDEX]++; 스택값[hapësirë_për_tekst_futje] = VALUE; 스택형[hapësirë_për_tekst_futje] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (GABIM) return 0;
        if (kuadër_INDEX < 0 || kuadër_Stivë[kuadër_INDEX] < 1) { dështim_VALUE("operand stack underflow"); return 0; }
        int hapësirë_për_tekst_futje = kuadër_INDEX * 128 + --kuadër_Stivë[kuadër_INDEX]; Kthe_TYPE = 스택형[hapësirë_për_tekst_futje];
        if (TYPE_VALUE != 0 && Kthe_TYPE != TYPE_VALUE) dështim_VALUE("operand type mismatch");
        if (Kthe_TYPE == 2) mbroj_VALUE(스택값[hapësirë_për_tekst_futje]);
        return 스택값[hapësirë_për_tekst_futje];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kuadër_metoda[kuadër_INDEX]] || INDEX < 0 || lokal_TYPE[kuadër_INDEX * 128 + INDEX] != TYPE_VALUE) { dështim_VALUE("invalid or uninitialized local"); return; }
        넣기(lokal_VALUE[kuadër_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void shkruaj_lokal(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kuadër_metoda[kuadër_INDEX]] || INDEX < 0) { dështim_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokal_VALUE[kuadër_INDEX * 128 + INDEX] = VALUE; lokal_TYPE[kuadër_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Pozicioni = kuadër_pozicioni[kuadër_INDEX];
        if (Pozicioni < metoda_nis[kuadër_metoda[kuadër_INDEX]] || Pozicioni >= metoda_mbaroj[kuadër_metoda[kuadër_INDEX]]) { dështim_VALUE("instruction pointer out of range"); return 0; }
        kuadër_pozicioni[kuadër_INDEX]++; return Kartelë[Pozicioni];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void lëviz_VALUE(int Pozicioni) {
        int FUNCTION_VALUE = kuadër_metoda[kuadër_INDEX];
        if (Pozicioni < metoda_nis[FUNCTION_VALUE] || Pozicioni >= metoda_mbaroj[FUNCTION_VALUE] || 경계[Pozicioni] != FUNCTION_VALUE + 1) dështim_VALUE("invalid branch target");
        else kuadër_pozicioni[kuadër_INDEX] = Pozicioni;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kuadër_INDEX % 32 == 31) { dështim_VALUE("call stack limit (32)"); return; }
        int Tjetër_njësi = kuadër_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Tjetër_njësi * 128 + 수] = 0;
        for (int 수 = metoda_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Tjetër_njësi * 128 + 수] = 빼기(metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokal_TYPE[Tjetër_njësi * 128 + 수] = metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (GABIM) return;
        kuadër_INDEX = Tjetër_njësi; filloj_kuadër[kuadër_INDEX] = 0; kuadër_metoda[kuadër_INDEX] = FUNCTION_VALUE; kuadër_pozicioni[kuadër_INDEX] = metoda_nis[FUNCTION_VALUE]; kuadër_Stivë[kuadër_INDEX] = 0;
    }
    static void Kthe_llogaritje(int TYPE_VALUE) {
        if (TYPE_VALUE != metoda_Kthe[kuadër_metoda[kuadër_INDEX]]) { dështim_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (filloj_kuadër[kuadër_INDEX] != 0) klasë_Përkufizim_status[filloj_kuadër[kuadër_INDEX] - 1] = 2;
        if (틀잠금[kuadër_INDEX] != 0) { 잠금풀기(틀잠금[kuadër_INDEX]); 틀잠금[kuadër_INDEX] = 0; }
        kuadër_INDEX--; if (kuadër_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_skedar_emër = new int[64];
    static void skedar_Stream_CALL(int pronari_VALUE, int Emër, int format_VALUE, int Komanda) {
        boolean 출력 = Word_SMS(pronari_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Komanda == 183 && Word_SMS(Emër, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { dështim_VALUE("unsupported file stream constructor"); return; }
            int skedar_futje_emër = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objekt_VALUE(skedar_futje_emër, 1) || !objekt_VALUE(Stream_VALUE, 종류) || GABIM) return;
            if (힙[Stream_VALUE + 3] != 0) { dështim_VALUE("file stream already initialized"); return; }
            int gjatësi_VALUE = 힙[skedar_futje_emër + 1];
            if (gjatësi_VALUE < 1 || gjatësi_VALUE > 63) { dështim_VALUE("invalid file name length"); return; }
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < gjatësi_VALUE; hapësirë_për_tekst_futje++) {
                int VALUE = 힙[skedar_futje_emër + 2 + hapësirë_për_tekst_futje];
                if (VALUE < 1) { dështim_VALUE("invalid file stream path"); return; }
                Stream_skedar_emër[hapësirë_për_tekst_futje] = VALUE;
            }
            Stream_skedar_emër[gjatësi_VALUE] = 0;
            int 서술자 = përdorues.파일서술자열기(Stream_skedar_emër, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { dështim_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Komanda != 182) { dështim_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(Emër, "write") || !출력 && Word_SMS(Emër, "read"))
            && (Word_SMS(format_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean fragment_VALUE = Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int futje_COUNT = fragment_VALUE ? 빼기(1) : 0, 시작점 = fragment_VALUE ? 빼기(1) : 0, të_dhëna_ARRAY = 빼기(2), objekt_Referencë = 빼기(2);
            if (!objekt_VALUE(të_dhëna_ARRAY, 20) || !objekt_VALUE(objekt_Referencë, 종류)) return;
            if (!fragment_VALUE) futje_COUNT = 힙[të_dhëna_ARRAY + 1];
            if (시작점 < 0 || futje_COUNT < 0 || 시작점 > 힙[të_dhëna_ARRAY + 1] - futje_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objekt_Referencë + 3] == 0 || 힙[objekt_Referencë + 2] < 0) { dështim_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < futje_COUNT && !GABIM) {
                int 반환값 = 출력 ? përdorues.파일한바이트쓰기(힙[objekt_Referencë + 2], 힙[të_dhëna_ARRAY + 2 + 시작점 + 완료수]) : përdorues.파일한바이트읽기(힙[objekt_Referencë + 2]);
                if (반환값 < 0) { dështim_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[të_dhëna_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(futje_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_SMS(Emër, "flush") && Word_SMS(format_VALUE, "()V")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 종류) && 힙[objekt_Referencë + 2] < 0) dështim_VALUE("IOException: stream closed"); return; }
        int Veprim = -1, VALUE = 0;
        if (Word_SMS(Emër, "close") && Word_SMS(format_VALUE, "()V")) Veprim = 0;
        if (!출력 && Word_SMS(Emër, "read") && Word_SMS(format_VALUE, "()I")) Veprim = 1;
        if (출력 && Word_SMS(Emër, "write") && Word_SMS(format_VALUE, "(I)V")) { Veprim = 2; VALUE = 빼기(1); }
        if (Veprim < 0) { dështim_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objekt_VALUE(Stream_VALUE, 종류) || GABIM) return;
        if (힙[Stream_VALUE + 3] == 0) { dështim_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Veprim == 0) {
            if (서술자 >= 0 && përdorues.파일서술자닫기(서술자) < 0) dështim_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { dështim_VALUE("IOException: stream closed"); return; }
        if (Veprim == 1) {
            int llogaritje = përdorues.파일한바이트읽기(서술자);
            if (llogaritje < -1) dështim_VALUE("IOException: read failed"); else 넣기(llogaritje == 256 ? -1 : llogaritje, 1);
        } else if (përdorues.파일한바이트쓰기(서술자, VALUE) != 1) dështim_VALUE("IOException: write failed");
    }
    static void CALL_metoda(int INDEX, int Komanda) {
        if (INDEX <= 0 || INDEX >= konstante_shenjë.length || (konstante_shenjë[INDEX] != 10 && konstante_shenjë[INDEX] != 11)) { dështim_VALUE("invalid method reference"); return; }
        int pronari_VALUE = klasë_emër_SMS(상가[INDEX]), Emër = Referencë_emër(konstante_SECOND_VALUE[INDEX]), format_VALUE = Referencë_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (GABIM) return;
        if (기본호출(pronari_VALUE, Emër, format_VALUE, Komanda)) return;
        if (Word_SMS(pronari_VALUE, "java/io/FileInputStream") || Word_SMS(pronari_VALUE, "java/io/FileOutputStream")) {
            skedar_Stream_CALL(pronari_VALUE, Emër, format_VALUE, Komanda); return;
        }
        if (Komanda == 184 && Word_SMS(pronari_VALUE, "java/lang/Integer") && Word_SMS(Emër, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Komanda == 182 && Word_SMS(pronari_VALUE, "java/io/PrintStream") && (Word_SMS(Emër, "println") || Word_SMS(Emër, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(Emër, "println")) dështim_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) dështim_VALUE("invalid PrintStream receiver");
            if (GABIM) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) përdorues.Shkrimi(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) përdorues.shkruaj_karakter_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) shkruaj_SMS(VALUE);
            if (Word_SMS(Emër, "println")) përdorues.shkruaj_karakter_VALUE(10);
            return;
        }
        if (Komanda == 182 && Word_SMS(pronari_VALUE, "java/lang/String")) {
            if (Word_SMS(Emër, "length") && Word_SMS(format_VALUE, "()I")) {
                int Referencë = 빼기(2); if (objekt_VALUE(Referencë, 1)) 넣기(힙[Referencë + 1], 1); return;
            }
            if (Word_SMS(Emër, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int shkrim_i_poshtëm_VALUE = 빼기(1), Referencë = 빼기(2);
                if (objekt_VALUE(Referencë, 1)) {
                    if (shkrim_i_poshtëm_VALUE < 0 || shkrim_i_poshtëm_VALUE >= 힙[Referencë + 1]) dështim_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Referencë + 2 + shkrim_i_poshtëm_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(pronari_VALUE, "java/lang/StringBuilder")) {
            if (Komanda == 183 && Word_SMS(Emër, "<init>") && Word_SMS(format_VALUE, "()V")) { objekt_VALUE(빼기(2), 4); return; }
            if (Komanda == 182 && Word_SMS(Emër, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Referencë = 빼기(2); if (objekt_VALUE(Referencë, 4)) 넣기(힙[Referencë + 2] == 0 ? pritës_karakter("") : 힙[Referencë + 2], 2); return;
            }
            if (Komanda == 182 && Word_SMS(Emër, "append")) {
                int Teksti = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) Teksti = shifër_karakter(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) Teksti = pritës_karakter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Teksti = caktoj_hapësira_ruajtëse(1, 1); if (!GABIM) 힙[Teksti + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Teksti = 빼기(2); if (Teksti == 0) Teksti = pritës_karakter("null"); }
                else { dështim_VALUE("unsupported StringBuilder append"); return; }
                int Referencë = 빼기(2); if (!objekt_VALUE(Referencë, 4) || !objekt_VALUE(Teksti, 1)) return;
                int e_përparme_VALUE = 힙[Referencë + 2], e_përparme_VALUE_gjatësi = e_përparme_VALUE == 0 ? 0 : 힙[e_përparme_VALUE + 1], PAS_VALUE_gjatësi = 힙[Teksti + 1];
                int 새글 = caktoj_hapësira_ruajtëse(1, e_përparme_VALUE_gjatësi + PAS_VALUE_gjatësi); if (GABIM) return;
                for (int 수 = 0; 수 < e_përparme_VALUE_gjatësi; 수++) 힙[새글 + 2 + 수] = 힙[e_përparme_VALUE + 2 + 수];
                for (int 수 = 0; 수 < PAS_VALUE_gjatësi; 수++) 힙[새글 + 2 + e_përparme_VALUE_gjatësi + 수] = 힙[Teksti + 2 + 수];
                힙[Referencë + 2] = 새글; 넣기(Referencë, 2); return;
            }
        }
        int klasë_Përkufizim = FIND_klasë_Përkufizim(pronari_VALUE); if (klasë_Përkufizim < 0 || GABIM) return;
        int skedar_INDEX = FIND_metoda(klasë_Përkufizim, Emër, format_VALUE);
        if (skedar_INDEX < 0) {
            for (int kodi_i_karakterit = klasë_Përkufizim, futje_COUNT = 0; kodi_i_karakterit >= 0 && futje_COUNT < 16; futje_COUNT++, kodi_i_karakterit = 부모종(kodi_i_karakterit))
                if (Word_SMS(종부모[kodi_i_karakterit], "java/lang/Thread")) { 가닥호출(Emër, format_VALUE, Komanda); return; }
            dështim_VALUE("NoSuchMethodError"); return;
        }
        if (((metoda_qasem[skedar_INDEX] & 8) != 0) != (Komanda == 184)) { dështim_VALUE("method static/instance mismatch"); return; }
        if (Komanda == 184) { if (!filloj(metoda_pronari[skedar_INDEX], kuadër_instruksion[kuadër_INDEX])) return; }
        else {
            int 읽는자리 = kuadër_Stivë[kuadër_INDEX] - metoda_argument_COUNT[skedar_INDEX];
            if (읽는자리 < 0 || 스택형[kuadër_INDEX * 128 + 읽는자리] != 2) { dështim_VALUE("invalid method receiver"); return; }
            int objekt_Referencë = 스택값[kuadër_INDEX * 128 + 읽는자리];
            if (!객체유효(objekt_Referencë)) return;
            if (힙[objekt_Referencë] < 32 || !종포함(힙[objekt_Referencë] - 32, pronari_VALUE)) { dështim_VALUE("method receiver type mismatch"); return; }
            if (Komanda != 183) skedar_INDEX = FIND_metoda(힙[objekt_Referencë] - 32, Emër, format_VALUE);
        }
        if (skedar_INDEX < 0 || (metoda_qasem[skedar_INDEX] & 0x400) != 0) { dështim_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((metoda_qasem[skedar_INDEX] & 32) != 0) {
            if (Komanda == 184) { int kodi_i_karakterit = metoda_pronari[skedar_INDEX]; if (종잠금[kodi_i_karakterit] == 0) 종잠금[kodi_i_karakterit] = caktoj_hapësira_ruajtëse(8, 0); 잠금참조 = 종잠금[kodi_i_karakterit]; }
            else 잠금참조 = 스택값[kuadër_INDEX * 128 + kuadër_Stivë[kuadër_INDEX] - metoda_argument_COUNT[skedar_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!GABIM) kuadër_pozicioni[kuadër_INDEX] = kuadër_instruksion[kuadër_INDEX]; return; }
        }
        호출(skedar_INDEX); if (!GABIM) 틀잠금[kuadër_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Referencë, int të_dhëna_VALUE) {
        if (të_dhëna_VALUE == 0 || ARRAY_element[ARRAY_Referencë] == 0) return true;
        boolean 성공여부 = ARRAY_element[ARRAY_Referencë] == -1 ? (të_dhëna_VALUE > 0 && të_dhëna_VALUE < 힙끝 && 힙[të_dhëna_VALUE] == 1) : 맞는객체(të_dhëna_VALUE, ARRAY_element[ARRAY_Referencë]);
        if (!성공여부 && !GABIM) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_hapësirë_për_tekst(int Referencë, int shkrim_i_poshtëm_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(Referencë, TYPE_VALUE)) return 0;
        if (shkrim_i_poshtëm_VALUE < 0 || shkrim_i_poshtëm_VALUE >= 힙[Referencë + 1]) { dështim_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referencë + 2 + shkrim_i_poshtëm_VALUE;
    }
    static void zbatoj_komandë() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (GABIM) { if (던진객체 != 0) dorezë_përjashtim(); if (GABIM || kuadër_INDEX < 현재가닥 * 32) break; }
            if (kuadër_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_thread()) break; 조각 = 100; }
            if (kuadër_INDEX == 0 && klasë_Përkufizim_status[futje_klasë_Përkufizim] != 2 && !filloj(futje_klasë_Përkufizim, kuadër_pozicioni[kuadër_INDEX])) continue;
            if (kuadër_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (metoda_qasem[kuadër_metoda[kuadër_INDEX]] & 32) != 0 && 틀잠금[kuadër_INDEX] == 0) {
                int objekt_Referencë = thread_objektiv[현재가닥]; if (!잠금얻기(objekt_Referencë)) { if (GABIM) break; continue; } 틀잠금[kuadër_INDEX] = objekt_Referencë;
            }
            잠시수 = 0;
            if (--남음 == 0) { dështim_VALUE("instruction limit (500000)"); break; }
            int Ekzekuto = kuadër_pozicioni[kuadër_INDEX]; kuadër_instruksion[kuadër_INDEX] = Ekzekuto; int VALUE = 명바();
            if (GABIM) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metoda_pronari[kuadër_metoda[kuadër_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstante_shenjë.length) dështim_VALUE("invalid ldc constant");
                else if (konstante_shenjë[수] == 3) 넣기(상가[수], 1);
                else if (konstante_shenjë[수] == 8) 넣기(konstante_SMS(상가[수]), 2);
                else dështim_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { shkruaj_lokal(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { shkruaj_lokal(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { shkruaj_lokal(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int futje_pozicioni = 빼기(1), objekt_Referencë = 빼기(2), kategori_kod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekt_Referencë > 0 && objekt_Referencë < 힙끝 && 힙[objekt_Referencë] == 21) kategori_kod = 21;
                int 읽는자리 = ARRAY_hapësirë_për_tekst(objekt_Referencë, futje_pozicioni, kategori_kod); if (!GABIM) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int futje_Referencë = 빼기(VALUE == 83 ? 2 : 1), futje_pozicioni = 빼기(1), objekt_Referencë = 빼기(2), kategori_kod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekt_Referencë > 0 && objekt_Referencë < 힙끝 && 힙[objekt_Referencë] == 21) kategori_kod = 21;
                int 읽는자리 = ARRAY_hapësirë_për_tekst(objekt_Referencë, futje_pozicioni, kategori_kod);
                if (!GABIM && kategori_kod == 3 && !배열저장가능(objekt_Referencë, futje_Referencë)) continue;
                if (!GABIM) 힙[읽는자리] = kategori_kod == 20 ? (byte)futje_Referencë : kategori_kod == 21 ? futje_Referencë & 1 : kategori_kod == 22 ? (char)futje_Referencë : kategori_kod == 23 ? (short)futje_Referencë : futje_Referencë;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Stivë_instruksion(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), llogaritje = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { dështim_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) llogaritje = 가 + 나;
                if (VALUE == 100) llogaritje = 가 - 나;
                if (VALUE == 104) llogaritje = 가 * 나;
                if (VALUE == 108) llogaritje = 가 / 나;
                if (VALUE == 112) llogaritje = 가 % 나;
                if (VALUE == 120) llogaritje = 가 << 나;
                if (VALUE == 122) llogaritje = 가 >> 나;
                if (VALUE == 124) llogaritje = 가 >>> 나;
                if (VALUE == 126) llogaritje = 가 & 나;
                if (VALUE == 128) llogaritje = 가 | 나;
                if (VALUE == 130) llogaritje = 가 ^ 나;
                넣기(llogaritje, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokal_fushë = 명바(), 증분 = (byte)명바(); 지역읽기(lokal_fushë, 1); 넣기(빼기(1) + 증분, 1); shkruaj_lokal(lokal_fushë, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int vendmbërritje_VALUE = Ekzekuto + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) lëviz_VALUE(vendmbërritje_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { Kthe_llogaritje(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Ekzekuto); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { dështim_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metoda(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(klasë_emër_SMS(명상수()), Ekzekuto); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int kategori_kod = 3, përbërës = 0;
                if (VALUE == 188) { int 임시값 = 명바(); kategori_kod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else përbërës = klasë_emër_SMS(명상수());
                if (kategori_kod == 0) { dështim_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekt_Referencë = caktoj_hapësira_ruajtëse(kategori_kod, 유효길이); if (!GABIM) ARRAY_element[objekt_Referencë] = përbërës; 넣기(objekt_Referencë, 2); continue;
            }
            if (VALUE == 190) {
                int objekt_Referencë = 빼기(2);
                if (객체유효(objekt_Referencë)) { int Krahasim_pozicioni = 힙[objekt_Referencë]; if (Krahasim_pozicioni != 2 && Krahasim_pozicioni != 3 && (Krahasim_pozicioni < 20 || Krahasim_pozicioni > 23)) dështim_VALUE("not an array"); else 넣기(힙[objekt_Referencë + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekt_Referencë = 빼기(2); if (객체유효(objekt_Referencë)) { if (힙[objekt_Referencë] != 9) dështim_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekt_Referencë; GABIM = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int emër_konstante = klasë_emër_SMS(명상수()), objekt_Referencë = 빼기(2); boolean MATCH = 맞는객체(objekt_Referencë, emër_konstante);
                if (VALUE == 193) 넣기(objekt_Referencë != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !GABIM) dështim_VALUE("ClassCastException"); 넣기(objekt_Referencë, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Ekzekuto + 1, skedar_INDEX = kuadër_metoda[kuadër_INDEX], tast_Referencë = 빼기(1);
                while ((읽는자리 - metoda_nis[skedar_INDEX]) % 4 != 0) 읽는자리++;
                int objektiv_email = pozicioni_numër_i_plotë(읽는자리);
                if (VALUE == 170) { int 낮은값 = pozicioni_numër_i_plotë(읽는자리 + 4), 높은값 = pozicioni_numër_i_plotë(읽는자리 + 8); if (tast_Referencë >= 낮은값 && tast_Referencë <= 높은값) objektiv_email = pozicioni_numër_i_plotë(읽는자리 + 12 + (tast_Referencë - 낮은값) * 4); }
                else { int 총수 = pozicioni_numër_i_plotë(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (pozicioni_numër_i_plotë(읽는자리 + 8 + Loop_INDEX * 8) == tast_Referencë) objektiv_email = pozicioni_numër_i_plotë(읽는자리 + 12 + Loop_INDEX * 8); }
                lëviz_VALUE(Ekzekuto + objektiv_email); continue;
            }
            if (VALUE == 200) { lëviz_VALUE(Ekzekuto + pozicioni_numër_i_plotë(Ekzekuto + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekt_Referencë = 빼기(2);
                if (VALUE == 195) 잠금풀기(objekt_Referencë);
                else if (!잠금얻기(objekt_Referencë) && !GABIM) { 넣기(objekt_Referencë, 2); kuadër_pozicioni[kuadër_INDEX] = Ekzekuto; }
                continue;
            }
            if (VALUE == 196) {
                int komandë_kod = 명바(), futje_pozicioni = 명짧();
                if (komandë_kod == 21 || komandë_kod == 25) 지역읽기(futje_pozicioni, komandë_kod == 21 ? 1 : 2);
                else if (komandë_kod == 54 || komandë_kod == 58) shkruaj_lokal(futje_pozicioni, komandë_kod == 54 ? 1 : 2);
                else if (komandë_kod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(futje_pozicioni, 1); 넣기(빼기(1) + DELTA_VALUE, 1); shkruaj_lokal(futje_pozicioni, 1); }
                else dështim_VALUE("unsupported wide opcode");
                continue;
            }
            dështim_VALUE("unsupported bytecode");
        }
    }
    static int FIND_klasë_Përkufizim(int Emër) {
        for (int Loop_INDEX = 0; Loop_INDEX < klasë_Përkufizim_COUNT; Loop_INDEX++) if (klasë_Përkufizim_emër[Loop_INDEX] != 0 && 같은말(klasë_Përkufizim_emër[Loop_INDEX], Emër)) return Loop_INDEX;
        return ngarkoj_klasë_Përkufizim(konstante_SMS(Emër));
    }
    static int ngarkoj_klasë_Përkufizim(int emër_varg) {
        if (!objekt_VALUE(emër_varg, 1)) return -1;
        int gjatësi_VALUE = 힙[emër_varg + 1];
        if (gjatësi_VALUE < 1 || gjatësi_VALUE > 505 || klasë_Përkufizim_COUNT == 16) { dështim_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < gjatësi_VALUE; Loop_INDEX++) { int kodi_i_karakterit = 힙[emër_varg + 2 + Loop_INDEX]; skedar_emër_SMS[Loop_INDEX] = kodi_i_karakterit == '/' ? '.' : kodi_i_karakterit; }
        skedar_emër_SMS[gjatësi_VALUE] = '.'; skedar_emër_SMS[gjatësi_VALUE + 1] = 'c'; skedar_emër_SMS[gjatësi_VALUE + 2] = 'l'; skedar_emër_SMS[gjatësi_VALUE + 3] = 'a'; skedar_emër_SMS[gjatësi_VALUE + 4] = 's'; skedar_emër_SMS[gjatësi_VALUE + 5] = 's'; skedar_emër_SMS[gjatësi_VALUE + 6] = 0;
        int Madhësi = përdorues.파일읽기(skedar_emër_SMS, 임시파일);
        if (Madhësi < 0) { dështim_VALUE("ClassNotFoundException"); return -1; }
        int klasë_Përkufizim = klasë_Përkufizim_COUNT++; klasë_Përkufizim_ndryshoj_përmasat[klasë_Përkufizim] = Madhësi;
        for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) Kartelë[klasë_Përkufizim * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(klasë_Përkufizim); if (GABIM) return -1;
        int aktual_të_dhëna = konstante_SMS(klasë_Përkufizim_emër[klasë_Përkufizim]);
        if (!글같음(aktual_të_dhëna, emër_varg, true)) { dështim_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[klasë_Përkufizim];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_klasë_Përkufizim(부모);
            if (GABIM || 위 < 0) return -1;
            int 읽는자리 = 위, fazë_COUNT = 0;
            while (읽는자리 >= 0 && fazë_COUNT++ < 16) {
                if (읽는자리 == klasë_Përkufizim) { dështim_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = klasë_hapësirë_për_tekst_COUNT[위];
            for (int skedar_INDEX = 0; skedar_INDEX < hapësirë_për_tekst_COUNT; skedar_INDEX++) if (hapësirë_për_tekst_pronari[skedar_INDEX] == klasë_Përkufizim && (hapësirë_për_tekst_Lejet[skedar_INDEX] & 8) == 0) hapësirë_për_tekst_pozicioni[skedar_INDEX] += 시작변위;
            klasë_hapësirë_për_tekst_COUNT[klasë_Përkufizim] += 시작변위;
        }
        return klasë_Përkufizim;
    }
    static int 부모종(int klasë_Përkufizim) {
        int Emër = 종부모[klasë_Përkufizim];
        for (int Loop_INDEX = 0; Loop_INDEX < klasë_Përkufizim_COUNT; Loop_INDEX++) if (Emër != 0 && klasë_Përkufizim_emër[Loop_INDEX] != 0 && 같은말(klasë_Përkufizim_emër[Loop_INDEX], Emër)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metoda(int klasë_Përkufizim, int Emër, int format_VALUE) {
        for (int 깊이 = 0; klasë_Përkufizim >= 0 && 깊이 < 16; 깊이++, klasë_Përkufizim = 부모종(klasë_Përkufizim)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_COUNT; Loop_INDEX++) if (metoda_pronari[Loop_INDEX] == klasë_Përkufizim && 같은말(metoda_emër_SMS[Loop_INDEX], Emër) && 같은말(metoda_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int emër_metoda(int klasë_Përkufizim, String Emër, String format_VALUE) {
        for (int 깊이 = 0; klasë_Përkufizim >= 0 && 깊이 < 16; 깊이++, klasë_Përkufizim = 부모종(klasë_Përkufizim))
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_COUNT; Loop_INDEX++) if (metoda_pronari[Loop_INDEX] == klasë_Përkufizim && Word_SMS(metoda_emër_SMS[Loop_INDEX], Emër) && Word_SMS(metoda_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Emër) { return Kartelë[상가[Emër]] == 'L' || Kartelë[상가[Emër]] == '[' ? 2 : 1; }
    static boolean filloj(int klasë_Përkufizim, int komandë_nis) {
        if (klasë_Përkufizim < 0 || GABIM) return false;
        if (klasë_Përkufizim_status[klasë_Përkufizim] == 3) { dështim_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (klasë_Përkufizim_status[klasë_Përkufizim] == 1 && klasë_thread[klasë_Përkufizim] != 현재가닥) { kuadër_pozicioni[kuadër_INDEX] = komandë_nis; 바꿈요청 = true; return false; }
        if (klasë_Përkufizim_status[klasë_Përkufizim] != 0) return true;
        int 위 = 부모종(klasë_Përkufizim);
        if (위 >= 0 && !filloj(위, komandë_nis)) return false;
        klasë_Përkufizim_status[klasë_Përkufizim] = 1; klasë_thread[klasë_Përkufizim] = 현재가닥;
        if (filloj_klasë_Përkufizim[klasë_Përkufizim] != 0) {
            kuadër_pozicioni[kuadër_INDEX] = komandë_nis;
            호출(filloj_klasë_Përkufizim[klasë_Përkufizim] - 1); if (!GABIM) filloj_kuadër[kuadër_INDEX] = klasë_Përkufizim + 1;
            return false;
        }
        klasë_Përkufizim_status[klasë_Përkufizim] = 2; return true;
    }
    static void 필드호출(int INDEX, int Komanda, int Ekzekuto) {
        if (!çek_konstante(INDEX, 9)) return;
        int pronari_VALUE = klasë_emër_SMS(상가[INDEX]), Emër = Referencë_emër(konstante_SECOND_VALUE[INDEX]), format_VALUE = Referencë_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (Word_SMS(pronari_VALUE, "java/lang/System") && (Word_SMS(Emër, "out") || Word_SMS(Emër, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && Komanda == 178) { 넣기(-1, 2); return; }
        int klasë_Përkufizim = FIND_klasë_Përkufizim(pronari_VALUE); if (klasë_Përkufizim < 0 || GABIM) return;
        int 찾음 = -1;
        for (int 읽는자리 = klasë_Përkufizim, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int skedar_INDEX = 0; skedar_INDEX < hapësirë_për_tekst_COUNT; skedar_INDEX++) if (hapësirë_për_tekst_pronari[skedar_INDEX] == 읽는자리 && 같은말(hapësirë_për_tekst_emër[skedar_INDEX], Emër) && 같은말(hapësirë_për_tekst_TYPE[skedar_INDEX], format_VALUE)) 찾음 = skedar_INDEX;
        if (찾음 < 0) { dështim_VALUE("NoSuchFieldError"); return; }
        boolean statik_VALUE = Komanda == 178 || Komanda == 179;
        if (statik_VALUE != ((hapësirë_për_tekst_Lejet[찾음] & 8) != 0)) { dështim_VALUE("field static/instance mismatch"); return; }
        if (statik_VALUE && !filloj(hapësirë_për_tekst_pronari[찾음], Ekzekuto)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (Komanda == 179 || Komanda == 181) VALUE = 빼기(TYPE_VALUE);
        if (statik_VALUE) { if (Komanda == 178) 넣기(hapësirë_për_tekst_të_dhëna[찾음], TYPE_VALUE); else if (!GABIM) hapësirë_për_tekst_të_dhëna[찾음] = VALUE; return; }
        int objekt_Referencë = 빼기(2);
        if (!객체유효(objekt_Referencë)) return;
        if (힙[objekt_Referencë] < 32 || !종포함(힙[objekt_Referencë] - 32, pronari_VALUE)) { dështim_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekt_Referencë + 2 + hapësirë_për_tekst_pozicioni[찾음];
        if (Komanda == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!GABIM) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klasë_Përkufizim, int Emër) {
        for (int 중첩깊이 = 0; klasë_Përkufizim >= 0 && 중첩깊이 < 16; 중첩깊이++, klasë_Përkufizim = 부모종(klasë_Përkufizim)) {
            if (같은말(klasë_Përkufizim_emër[klasë_Përkufizim], Emër) || (종부모[klasë_Përkufizim] != 0 && 같은말(종부모[klasë_Përkufizim], Emër))) return true;
            for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < klasë_ndërfaqe_COUNT[klasë_Përkufizim]; bashkim_i_brendshëm_pozicioni++) if (같은말(klasë_ndërfaqe[klasë_Përkufizim * 16 + bashkim_i_brendshëm_pozicioni], Emër)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bajt_të_dhëna, boolean POZICIONI) {
        if (첫값 == bajt_të_dhëna) return true;
        if (첫값 <= 0 || bajt_të_dhëna <= 0 || 힙[첫값] != 1 || 힙[bajt_të_dhëna] != 1 || 힙[첫값 + 1] != 힙[bajt_të_dhëna + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int koordinata_x = 힙[첫값 + 2 + Loop_INDEX], Y_koordinatë = 힙[bajt_të_dhëna + 2 + Loop_INDEX];
            if (POZICIONI) { if (koordinata_x == '.') koordinata_x = '/'; if (Y_koordinatë == '.') Y_koordinatë = '/'; }
            if (koordinata_x != Y_koordinatë) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekt_Referencë) {
        if (objekt_Referencë == 0) { dështim_VALUE("NullPointerException"); return false; }
        if (objekt_Referencë < 1 || objekt_Referencë >= 힙끝 || 힙폭[objekt_Referencë] < 2 || 힙[objekt_Referencë] == 0) { dështim_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void mbroj_VALUE(int objekt_Referencë) {
        if (objekt_Referencë > 0 && objekt_Referencë < 힙끝 && 힙폭[objekt_Referencë] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_Referencë;
    }
    static void shfaq_VALUE(int objekt_Referencë) {
        if (objekt_Referencë > 0 && objekt_Referencë < 힙끝 && 힙폭[objekt_Referencë] >= 2 && 힙[objekt_Referencë] != 0 && 힙표시[objekt_Referencë] == 0) {
            힙표시[objekt_Referencë] = 1; 표시대기[afishim_COUNT++] = objekt_Referencë;
        }
    }
    static void 수거() {
        afishim_COUNT = 0; Koleksion_COUNT++;
        for (int çek_pozicioni = 1; çek_pozicioni < 힙끝; çek_pozicioni += 힙폭[çek_pozicioni]) 힙표시[çek_pozicioni] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < varg_Referencë.length; Loop_INDEX++) shfaq_VALUE(varg_Referencë[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < hapësirë_për_tekst_COUNT; Loop_INDEX++) if ((hapësirë_për_tekst_Lejet[Loop_INDEX] & 8) != 0 && 형종류(hapësirë_për_tekst_TYPE[Loop_INDEX]) == 2) shfaq_VALUE(hapësirë_për_tekst_të_dhëna[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < thread_COUNT; 임시값++) {
            shfaq_VALUE(thread_objekt[임시값]); shfaq_VALUE(thread_objektiv[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? kuadër_INDEX : thread_kuadër[임시값];
            for (int skedar_INDEX = 임시값 * 32; skedar_INDEX <= 꼭대기자리; skedar_INDEX++) {
                for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 함수지역[kuadër_metoda[skedar_INDEX]]; bashkim_i_brendshëm_pozicioni++) if (lokal_TYPE[skedar_INDEX * 128 + bashkim_i_brendshëm_pozicioni] == 2) shfaq_VALUE(lokal_VALUE[skedar_INDEX * 128 + bashkim_i_brendshëm_pozicioni]);
                for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < kuadër_Stivë[skedar_INDEX]; bashkim_i_brendshëm_pozicioni++) if (스택형[skedar_INDEX * 128 + bashkim_i_brendshëm_pozicioni] == 2) shfaq_VALUE(스택값[skedar_INDEX * 128 + bashkim_i_brendshëm_pozicioni]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) shfaq_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) shfaq_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_numër_i_plotë.length; Loop_INDEX++) shfaq_VALUE(Store_numër_i_plotë[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < klasë_Përkufizim_COUNT; Loop_INDEX++) shfaq_VALUE(종잠금[Loop_INDEX]);
        for (int çek_pozicioni = 1; çek_pozicioni < 힙끝; çek_pozicioni += 힙폭[çek_pozicioni]) if (잠금깊이[çek_pozicioni] > 0) shfaq_VALUE(çek_pozicioni);
        shfaq_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) shfaq_VALUE(잠시참조[Loop_INDEX]);
        while (afishim_COUNT > 0) {
            int objekt_Referencë = 표시대기[--afishim_COUNT], kategori_kod = 힙[objekt_Referencë];
            for (int Loop_INDEX = objekt_Referencë + 2; Loop_INDEX < objekt_Referencë + 힙폭[objekt_Referencë]; Loop_INDEX++) if (kategori_kod == 3 || kategori_kod == 4 || 힙참조[Loop_INDEX] != 0) shfaq_VALUE(힙[Loop_INDEX]);
        }
        for (int çek_pozicioni = 1; çek_pozicioni < 힙끝; çek_pozicioni += 힙폭[çek_pozicioni]) if (힙표시[çek_pozicioni] == 0) 힙[çek_pozicioni] = 0;
        for (int çek_pozicioni = 1; çek_pozicioni < 힙끝; çek_pozicioni += 힙폭[çek_pozicioni]) if (힙[çek_pozicioni] == 0) {
            while (çek_pozicioni + 힙폭[çek_pozicioni] < 힙끝 && 힙[çek_pozicioni + 힙폭[çek_pozicioni]] == 0) { int Tjetër_pozicioni = çek_pozicioni + 힙폭[çek_pozicioni]; 힙폭[çek_pozicioni] += 힙폭[Tjetër_pozicioni]; 힙폭[Tjetër_pozicioni] = 0; }
            if (çek_pozicioni + 힙폭[çek_pozicioni] == 힙끝) { 힙끝 = çek_pozicioni; break; }
        }
    }
    static int 새기억(int 종류, int gjatësi_VALUE) {
        if (gjatësi_VALUE < 0) { dështim_VALUE("NegativeArraySizeException"); return 0; }
        if (gjatësi_VALUE > 힙.length - 3) { dështim_VALUE("object heap exhausted"); return 0; }
        int 필요수 = gjatësi_VALUE + 2, objekt_Referencë = 0;
        if (필요수 <= 힙.length - 힙끝) { objekt_Referencë = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_Referencë = 읽는자리; break; }
            if (objekt_Referencë != 0) {
                int 남은길이 = 힙폭[objekt_Referencë] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_Referencë + 필요수] = 남은길이; 힙[objekt_Referencë + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objekt_Referencë = 힙끝; 힙끝 += 필요수; }
        }
        if (objekt_Referencë == 0) { dështim_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objekt_Referencë + Loop_INDEX] = 0; 힙참조[objekt_Referencë + Loop_INDEX] = 0; 힙폭[objekt_Referencë + Loop_INDEX] = 0; }
        ARRAY_element[objekt_Referencë] = 0;
        힙폭[objekt_Referencë] = 필요수; 힙[objekt_Referencë] = 종류; 힙[objekt_Referencë + 1] = gjatësi_VALUE; mbroj_VALUE(objekt_Referencë); return objekt_Referencë;
    }
    static int përjashtim_klasë(String emër_konstante) {
        if (자바도구.같음(emër_konstante, "java/lang/Throwable")) return 1;
        if (자바도구.같음(emër_konstante, "java/lang/Exception")) return 2;
        if (자바도구.같음(emër_konstante, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(emër_konstante, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(emër_konstante, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(emër_konstante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(emër_konstante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(emër_konstante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(emër_konstante, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(emër_konstante, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(emër_konstante, "java/io/IOException")) return 11;
        if (자바도구.같음(emër_konstante, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(emër_konstante, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(emër_konstante, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(emër_konstante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int përjashtim_konstante(int Emër) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Emër, përjashtim_emër(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String përjashtim_emër(int llogari_VALUE) {
        if (llogari_VALUE == 40) return "java/lang/InterruptedException";
        if (llogari_VALUE == 41) return "한국어/자체/대기중단예외";
        if (llogari_VALUE == 39) return "java/net/SocketException";
        if (llogari_VALUE == 20) return "한국어/자체/përjashtim";
        if (llogari_VALUE == 21) return "한국어/자체/실행예외";
        if (llogari_VALUE == 22) return "한국어/자체/I_O_përjashtim";
        if (llogari_VALUE == 23) return "한국어/자체/Prit_TIMEOUT_përjashtim";
        if (llogari_VALUE == 24) return "한국어/자체/email_LOOKUP_përjashtim";
        if (llogari_VALUE == 25) return "한국어/자체/파일없음예외";
        if (llogari_VALUE == 26) return "한국어/자체/통신예외";
        if (llogari_VALUE == 27) return "한국어/자체/i_pavlefshëm_argument_përjashtim";
        if (llogari_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (llogari_VALUE == 29) return "한국어/자체/범위예외";
        if (llogari_VALUE == 30) return "한국어/자체/배열범위예외";
        if (llogari_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (llogari_VALUE == 32) return "한국어/자체/NUL_Referencë_përjashtim";
        if (llogari_VALUE == 33) return "한국어/자체/산술예외";
        if (llogari_VALUE == 34) return "한국어/자체/status_përjashtim";
        if (llogari_VALUE == 35) return "한국어/자체/TYPE_Transmetim_përjashtim";
        if (llogari_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (llogari_VALUE == 37) return "한국어/자체/ARRAY_Store_dështim";
        if (llogari_VALUE == 38) return "한국어/자체/thread_status_përjashtim";
        if (llogari_VALUE == 1) return "java/lang/Throwable"; if (llogari_VALUE == 2) return "java/lang/Exception";
        if (llogari_VALUE == 3) return "java/lang/RuntimeException"; if (llogari_VALUE == 4) return "java/lang/ArithmeticException";
        if (llogari_VALUE == 5) return "java/lang/NullPointerException"; if (llogari_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (llogari_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (llogari_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (llogari_VALUE == 9) return "java/lang/IllegalArgumentException"; if (llogari_VALUE == 10) return "java/lang/NumberFormatException";
        if (llogari_VALUE == 11) return "java/io/IOException"; if (llogari_VALUE == 12) return "java/io/FileNotFoundException";
        if (llogari_VALUE == 17) return "java/lang/ArrayStoreException";
        if (llogari_VALUE == 18) return "java/net/UnknownHostException";
        if (llogari_VALUE == 19) return "java/net/SocketTimeoutException";
        if (llogari_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (llogari_VALUE == 13) return "java/lang/IllegalStateException"; if (llogari_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int llogari_VALUE) {
        if (llogari_VALUE == 40) return 2;
        if (llogari_VALUE == 41) return 40;
        if (llogari_VALUE == 39) return 11;
        if (llogari_VALUE == 1) return 0;
        if (llogari_VALUE == 2) return 1;
        if (llogari_VALUE == 3) return 2;
        if (llogari_VALUE == 4) return 3;
        if (llogari_VALUE == 5) return 3;
        if (llogari_VALUE == 6) return 3;
        if (llogari_VALUE == 7) return 6;
        if (llogari_VALUE == 8) return 6;
        if (llogari_VALUE == 9) return 3;
        if (llogari_VALUE == 10) return 9;
        if (llogari_VALUE == 11) return 2;
        if (llogari_VALUE == 12) return 11;
        if (llogari_VALUE == 13) return 3;
        if (llogari_VALUE == 14) return 3;
        if (llogari_VALUE == 15) return 3;
        if (llogari_VALUE == 16) return 9;
        if (llogari_VALUE == 17) return 3;
        if (llogari_VALUE == 18) return 11;
        if (llogari_VALUE == 19) return 11;
        if (llogari_VALUE == 20) return 2;
        if (llogari_VALUE == 21) return 3;
        if (llogari_VALUE == 22) return 11;
        if (llogari_VALUE == 23) return 22;
        if (llogari_VALUE == 24) return 22;
        if (llogari_VALUE == 25) return 22;
        if (llogari_VALUE == 26) return 22;
        if (llogari_VALUE == 27) return 9;
        if (llogari_VALUE == 28) return 27;
        if (llogari_VALUE == 29) return 6;
        if (llogari_VALUE == 30) return 29;
        if (llogari_VALUE == 31) return 29;
        if (llogari_VALUE == 32) return 5;
        if (llogari_VALUE == 33) return 4;
        if (llogari_VALUE == 34) return 13;
        if (llogari_VALUE == 35) return 14;
        if (llogari_VALUE == 36) return 15;
        if (llogari_VALUE == 37) return 17;
        if (llogari_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int aktual_VALUE, int 요구값) {
        for (int 깊이 = 0; aktual_VALUE != 0 && 깊이 < 16; 깊이++, aktual_VALUE = 예외부모(aktual_VALUE))
            if (aktual_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int llogari_VALUE, String LEXOMË_Referencë) {
        int objekt_Referencë = 새기억(9, 2); if (GABIM) return;
        힙[objekt_Referencë + 2] = llogari_VALUE; 힙[objekt_Referencë + 3] = pritës_karakter(LEXOMË_Referencë); 힙참조[objekt_Referencë + 3] = 1;
        던진객체 = objekt_Referencë; GABIM = true;
    }
    static boolean 맞는객체(int objekt_Referencë, int Emër) {
        if (objekt_Referencë == 0) return true;
        if (!객체유효(objekt_Referencë)) return false;
        int kategori_kod = 힙[objekt_Referencë];
        if (Word_SMS(Emër, "java/lang/Object")) return true;
        if (kategori_kod >= 32) return 종포함(kategori_kod - 32, Emër);
        if (kategori_kod == 9) { int objektiv_email = përjashtim_konstante(Emër); return objektiv_email != 0 && 예외포함(힙[objekt_Referencë + 2], objektiv_email); }
        if (kategori_kod == 1) return Word_SMS(Emër, "java/lang/String") || Word_SMS(Emër, "java/lang/CharSequence");
        if (kategori_kod == 4) return Word_SMS(Emër, "java/lang/StringBuilder") || Word_SMS(Emër, "java/lang/CharSequence");
        if (kategori_kod == 10) return Word_SMS(Emër, "java/util/ArrayList") || Word_SMS(Emër, "java/util/List");
        if (kategori_kod == 11) return Word_SMS(Emër, "java/util/HashMap") || Word_SMS(Emër, "java/util/Map");
        if (kategori_kod == 12) return Word_SMS(Emër, "java/lang/Integer") || Word_SMS(Emër, "java/lang/Number");
        if (kategori_kod >= 24 && kategori_kod <= 28 && 힙[objekt_Referencë + 13] != 0) return 한국어화면종(Emër) == kategori_kod || Word_SMS(Emër, "한국어/자체/화면구성요소");
        if (kategori_kod >= 24 && kategori_kod <= 28) return (한국어화면종(Emër) == 0 && 화면종(Emër) == kategori_kod) || Word_SMS(Emër, "java/awt/Component") || Word_SMS(Emër, "java/awt/Container") || Word_SMS(Emër, "javax/swing/JComponent");
        if (kategori_kod == 29) return Word_SMS(Emër, 힙[objekt_Referencë + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (kategori_kod == 30) return Word_SMS(Emër, "java/awt/FlowLayout") || Word_SMS(Emër, "java/awt/LayoutManager");
        if (kategori_kod == 17) return Word_SMS(Emër, "java/net/Socket");
        if (kategori_kod == 18) return Word_SMS(Emër, "java/net/ServerSocket");
        if (kategori_kod == 19) return Word_SMS(Emër, 힙[objekt_Referencë + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kategori_kod == 14) return Word_SMS(Emër, "java/net/InetAddress");
        if (kategori_kod == 15) return Word_SMS(Emër, "java/net/DatagramSocket");
        if (kategori_kod == 16) return Word_SMS(Emër, "java/net/DatagramPacket");
        if (kategori_kod == 13) return Word_SMS(Emër, 힙[objekt_Referencë + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (kategori_kod == 2) return Word_SMS(Emër, "[I"); if (kategori_kod == 20) return Word_SMS(Emër, "[B"); if (kategori_kod == 21) return Word_SMS(Emër, "[Z");
        if (kategori_kod == 22) return Word_SMS(Emër, "[C"); if (kategori_kod == 23) return Word_SMS(Emër, "[S");
        if (kategori_kod != 3) return false;
        if (Word_SMS(Emër, "[Ljava/lang/Object;")) return true;
        int përbërës = ARRAY_element[objekt_Referencë];
        if (përbërës == -1) return Word_SMS(Emër, "[Ljava/lang/String;") || Word_SMS(Emër, "[Ljava/lang/CharSequence;");
        if (përbërës == 0) return false;
        if (배열종비교(përbërës, Emër)) return true;
        if ((Word_SMS(përbërës, "java/lang/String") || Word_SMS(përbërës, "java/lang/StringBuilder")) && Word_SMS(Emër, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < klasë_Përkufizim_COUNT; Loop_INDEX++) if (같은말(klasë_Përkufizim_emër[Loop_INDEX], përbërës)) {
            for (int kodi_i_karakterit = Loop_INDEX, 중첩깊이 = 0; kodi_i_karakterit >= 0 && 중첩깊이 < 16; 중첩깊이++, kodi_i_karakterit = 부모종(kodi_i_karakterit)) {
                if (배열종비교(종부모[kodi_i_karakterit], Emër)) return true;
                for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < klasë_ndërfaqe_COUNT[kodi_i_karakterit]; bashkim_i_brendshëm_pozicioni++) if (배열종비교(klasë_ndërfaqe[kodi_i_karakterit * 16 + bashkim_i_brendshëm_pozicioni], Emër)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int emër_konstante, int 형식참조) {
        int çek_pozicioni = 상가[형식참조], futje_COUNT = konstante_SECOND_VALUE[형식참조];
        if (emër_konstante == 0 || futje_COUNT < 4 || Kartelë[çek_pozicioni] != '[' || Kartelë[çek_pozicioni + 1] != 'L' || Kartelë[çek_pozicioni + futje_COUNT - 1] != ';' || konstante_SECOND_VALUE[emër_konstante] != futje_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT - 3; Loop_INDEX++) if (Kartelë[상가[emër_konstante] + Loop_INDEX] != Kartelë[çek_pozicioni + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void dorezë_përjashtim() {
        if (던진객체 == 0) return;
        GABIM = false;
        while (kuadër_INDEX >= 현재가닥 * 32) {
            int skedar_INDEX = kuadër_metoda[kuadër_INDEX], 읽는자리 = kuadër_instruksion[kuadër_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == skedar_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kuadër_pozicioni[kuadër_INDEX] = 잡기위치[Loop_INDEX]; kuadër_Stivë[kuadër_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (filloj_kuadër[kuadër_INDEX] != 0) klasë_Përkufizim_status[filloj_kuadër[kuadër_INDEX] - 1] = 3;
            if (틀잠금[kuadër_INDEX] != 0) { 잠금풀기(틀잠금[kuadër_INDEX]); 틀잠금[kuadër_INDEX] = 0; }
            kuadër_INDEX--;
        }
        përdorues.Shkrimi("Uncaught ");
        if (힙[던진객체] == 9) { përdorues.Shkrimi(përjashtim_emër(힙[던진객체 + 2])); përdorues.Shkrimi(": "); shkruaj_SMS(힙[던진객체 + 3]); }
        else përdorues.Shkrimi("user exception");
        përdorues.shkruaj_karakter_VALUE(10); 던진객체 = 0; GABIM = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Stivë_instruksion(int komandë_kod) {
        int 첫값 = 빼기(0), 첫형식 = Kthe_TYPE;
        if (komandë_kod == 87) return;
        if (komandë_kod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bajt_të_dhëna = 빼기(0), SECOND_format = Kthe_TYPE;
        if (komandë_kod == 88) return;
        if (komandë_kod == 90) { 넣기(첫값, 첫형식); 넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komandë_kod == 92) { 넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식); 넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komandë_kod == 95) { 넣기(첫값, 첫형식); 넣기(bajt_të_dhëna, SECOND_format); return; }
        int kodi_i_karakterit = 빼기(0), 셋째형식 = Kthe_TYPE;
        if (komandë_kod == 91) { 넣기(첫값, 첫형식); 넣기(kodi_i_karakterit, 셋째형식); 넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (komandë_kod == 93) { 넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식); 넣기(kodi_i_karakterit, 셋째형식); 넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = Kthe_TYPE;
        넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kodi_i_karakterit, 셋째형식); 넣기(bajt_të_dhëna, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int emër_konstante, int 시작점) {
        int kategori_kod = 0, 유효길이 = 0, përjashtim_Referencë = përjashtim_konstante(emër_konstante);
        if (Word_SMS(emër_konstante, "java/lang/StringBuilder")) { kategori_kod = 4; 유효길이 = 1; }
        if (Word_SMS(emër_konstante, "java/io/FileInputStream")) { kategori_kod = 5; 유효길이 = 2; }
        if (Word_SMS(emër_konstante, "java/io/FileOutputStream")) { kategori_kod = 6; 유효길이 = 2; }
        if (përjashtim_Referencë != 0) { kategori_kod = 9; 유효길이 = 2; }
        if (Word_SMS(emër_konstante, "java/util/ArrayList")) { kategori_kod = 10; 유효길이 = 2; }
        if (Word_SMS(emër_konstante, "java/util/HashMap")) { kategori_kod = 11; 유효길이 = 2; }
        if (Word_SMS(emër_konstante, "java/lang/Integer")) { kategori_kod = 12; 유효길이 = 1; }
        if (Word_SMS(emër_konstante, "java/net/Socket")) { kategori_kod = 17; 유효길이 = 5; }
        if (Word_SMS(emër_konstante, "java/net/ServerSocket")) { kategori_kod = 18; 유효길이 = 5; }
        if (Word_SMS(emër_konstante, "java/net/DatagramSocket")) { kategori_kod = 15; 유효길이 = 3; }
        if (Word_SMS(emër_konstante, "java/net/DatagramPacket")) { kategori_kod = 16; 유효길이 = 4; }
        if (Word_SMS(emër_konstante, "java/lang/Thread") || Word_SMS(emër_konstante, "한국어/자체/작업가닥")) { kategori_kod = 13; 유효길이 = 2; }
        if (Word_SMS(emër_konstante, "java/lang/Object")) { kategori_kod = 8; }
        if (kategori_kod == 0 && 화면종(emër_konstante) != 0) { kategori_kod = 화면종(emër_konstante); 유효길이 = 12; }
        if (kategori_kod == 0) {
            int kodi_i_karakterit = FIND_klasë_Përkufizim(emër_konstante); if (kodi_i_karakterit < 0 || GABIM || !filloj(kodi_i_karakterit, 시작점)) return;
            kategori_kod = 32 + kodi_i_karakterit; 유효길이 = klasë_hapësirë_për_tekst_COUNT[kodi_i_karakterit];
        }
        int objekt_Referencë = caktoj_hapësira_ruajtëse(kategori_kod, 유효길이); if (GABIM) return;
        if (kategori_kod == 13 && Word_SMS(emër_konstante, "한국어/자체/작업가닥")) 힙[objekt_Referencë + 3] = 1;
        if (kategori_kod >= 24 && kategori_kod <= 28 && 한국어화면종(emër_konstante) != 0) 힙[objekt_Referencë + 13] = 1;
        if (kategori_kod == 5 || kategori_kod == 6 || kategori_kod == 15 || kategori_kod == 17 || kategori_kod == 18) 힙[objekt_Referencë + 2] = -1;
        if (kategori_kod == 9) 힙[objekt_Referencë + 2] = përjashtim_Referencë;
        넣기(objekt_Referencë, 2);
    }
    static boolean 값같음(int 첫값, int bajt_të_dhëna) {
        if (첫값 == bajt_të_dhëna) return true;
        if (첫값 == 0 || bajt_të_dhëna == 0 || 첫값 < 0 || bajt_të_dhëna < 0 || 첫값 >= 힙끝 || bajt_të_dhëna >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bajt_të_dhëna] == 1) return 글같음(첫값, bajt_të_dhëna, false);
        return 힙[첫값] == 12 && 힙[bajt_të_dhëna] == 12 && 힙[첫값 + 2] == 힙[bajt_të_dhëna + 2];
    }
    static int 글조각(int objekt_Referencë, int nis_pozicioni, int mbaroj_pozicioni) {
        if (!objekt_VALUE(objekt_Referencë, 1)) return 0;
        if (nis_pozicioni < 0 || mbaroj_pozicioni < nis_pozicioni || mbaroj_pozicioni > 힙[objekt_Referencë + 1]) { dështim_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = caktoj_hapësira_ruajtëse(1, mbaroj_pozicioni - nis_pozicioni); if (GABIM) return 0;
        for (int Loop_INDEX = nis_pozicioni; Loop_INDEX < mbaroj_pozicioni; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - nis_pozicioni] = 힙[objekt_Referencë + 2 + Loop_INDEX];
        return 반환값;
    }
    static int bashkim_SMS(int 첫값, int bajt_të_dhëna) {
        if (!objekt_VALUE(첫값, 1) || !objekt_VALUE(bajt_të_dhëna, 1)) return 0;
        int futje_COUNT = 힙[첫값 + 1], metoda_INDEX = 힙[bajt_të_dhëna + 1], 반환값 = caktoj_hapësira_ruajtëse(1, futje_COUNT + metoda_INDEX); if (GABIM) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metoda_INDEX; Loop_INDEX++) 힙[반환값 + 2 + futje_COUNT + Loop_INDEX] = 힙[bajt_të_dhëna + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int pronari, int emër_konstante, int 서술상수, int komandë_kod) {
        if (Word_SMS(pronari, "한국어/자체/실행인수") && komandë_kod == 184) {
            if (Word_SMS(emër_konstante, "njësi_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(përdorues.인수개수() - 1, 1); return true; }
            if (Word_SMS(emër_konstante, "Teksti") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= përdorues.인수개수() - 1) 예외던짐(29, "zbatoj_komandë Argumente 범위를 벗어났습니다");
                else 넣기(pritës_karakter(përdorues.Argumente(순번 + 1)), 2);
                return true;
            }
            dështim_VALUE("지원하지 않는 한국어 zbatoj_komandë Argumente 호출"); return true;
        }
        if (Word_SMS(pronari, "한국어/자체/작업가닥")) { Proces_thread(emër_konstante, 서술상수, komandë_kod, true); return true; }
        if (한국어화면소유(pronari)) { 한국어화면호출(pronari, emër_konstante, 서술상수, komandë_kod); return true; }
        if (화면소유(pronari)) { 화면호출(pronari, emër_konstante, 서술상수, komandë_kod); return true; }
        if (Word_SMS(pronari, "java/net/Socket") || Word_SMS(pronari, "java/net/ServerSocket") || Word_SMS(pronari, "java/io/InputStream") || Word_SMS(pronari, "java/io/OutputStream")) { 흐름호출(pronari, emër_konstante, 서술상수, komandë_kod); return true; }
        if (Word_SMS(pronari, "한국어/자체/bërthamë_VALUE") && komandë_kod == 184) {
            if (Word_SMS(emër_konstante, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(përdorues.화면너비(), 1); return true; }
            if (Word_SMS(emër_konstante, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(përdorues.화면높이(), 1); return true; }
            if (Word_SMS(emër_konstante, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(përdorues.밀리초(), 1); return true; }
            if (Word_SMS(emër_konstante, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(përdorues.그림대기(), 1); return true; }
            if (Word_SMS(emër_konstante, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinatë = 빼기(1), koordinata_x = 빼기(1); 넣기(përdorues.사각형(koordinata_x, Y_koordinatë, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(pronari, "java/net/InetAddress") || Word_SMS(pronari, "java/net/DatagramPacket") || Word_SMS(pronari, "java/net/DatagramSocket")) { 통신호출(pronari, emër_konstante, 서술상수, komandë_kod); return true; }
        if (Word_SMS(pronari, "java/lang/Thread")) { 가닥호출(emër_konstante, 서술상수, komandë_kod); return true; }
        if (Word_SMS(pronari, "java/lang/Object")) {
            if (Word_SMS(emër_konstante, "<init>") && Word_SMS(서술상수, "()V") && komandë_kod == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(emër_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_të_dhëna = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bajt_të_dhëna ? 1 : 0, 1); return true; }
        }
        if (përjashtim_konstante(pronari) != 0) {
            if (Word_SMS(emër_konstante, "<init>") && komandë_kod == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int kërkoj = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Referencë = 빼기(2);
                if (objekt_VALUE(objekt_Referencë, 9)) { 힙[objekt_Referencë + 3] = kërkoj; 힙참조[objekt_Referencë + 3] = 1; } return true;
            }
            if ((Word_SMS(emër_konstante, "getMessage") || Word_SMS(emër_konstante, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 9)) 넣기(힙[objekt_Referencë + 3], 2); return true; }
        }
        if (Word_SMS(pronari, "java/lang/String")) {
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int enkodim_emër = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_Referencë = 빼기(2);
                if (!objekt_VALUE(objekt_Referencë, 1)) return true;
                if (enkodim_emër != 0 && !글같음(enkodim_emër, pritës_karakter("UTF-8"), false) && !글같음(enkodim_emër, pritës_karakter("UTF8"), false) && !글같음(enkodim_emër, pritës_karakter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int futje_COUNT = 힙[objekt_Referencë + 1], 반환값 = caktoj_hapësira_ruajtëse(20, futje_COUNT * 3), 사용수 = 0; if (GABIM) return true;
                for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < futje_COUNT; bashkim_i_brendshëm_pozicioni++) {
                    int kodi_i_karakterit = 힙[objekt_Referencë + 2 + bashkim_i_brendshëm_pozicioni];
                    if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdbff && bashkim_i_brendshëm_pozicioni + 1 < futje_COUNT && 힙[objekt_Referencë + 3 + bashkim_i_brendshëm_pozicioni] >= 0xdc00 && 힙[objekt_Referencë + 3 + bashkim_i_brendshëm_pozicioni] <= 0xdfff) kodi_i_karakterit = 0x10000 + ((kodi_i_karakterit - 0xd800) << 10) + 힙[objekt_Referencë + 2 + ++bashkim_i_brendshëm_pozicioni] - 0xdc00;
                    else if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdfff) kodi_i_karakterit = '?';
                    if (kodi_i_karakterit < 128) 힙[반환값 + 2 + 사용수++] = kodi_i_karakterit;
                    else { int bajt_COUNT = kodi_i_karakterit < 2048 ? 2 : kodi_i_karakterit < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bajt_COUNT == 2 ? 192 : bajt_COUNT == 3 ? 224 : 240) | kodi_i_karakterit >> (6 * (bajt_COUNT - 1))); for (int Krahasim_pozicioni = bajt_COUNT - 1; Krahasim_pozicioni > 0; Krahasim_pozicioni--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kodi_i_karakterit >> (6 * (Krahasim_pozicioni - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(shifër_karakter(빼기(1)), 2); return true; }
            if (komandë_kod != 182) return false;
            if (Word_SMS(emër_konstante, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_të_dhëna = 빼기(2), 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(글같음(첫값, bajt_të_dhëna, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(emër_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(emër_konstante, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int mbaroj_pozicioni = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? mbaroj_pozicioni : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(emër_konstante, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bajt_të_dhëna = 빼기(2), 첫값 = 빼기(2); 넣기(bashkim_SMS(첫값, bajt_të_dhëna), 2); return true; }
            if (Word_SMS(emër_konstante, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALUE = 0; if (objekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_VALUE = hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_VALUE, 1); } return true; }
            if (Word_SMS(emër_konstante, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(pronari, "java/lang/Integer")) {
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int të_dhëna_VALUE = 빼기(1), objekt_Referencë = të_dhëna_VALUE >= -128 && të_dhëna_VALUE <= 127 ? Store_numër_i_plotë[të_dhëna_VALUE + 128] : 0; if (objekt_Referencë == 0) { objekt_Referencë = caktoj_hapësira_ruajtëse(12, 1); if (!GABIM) { 힙[objekt_Referencë + 2] = të_dhëna_VALUE; if (të_dhëna_VALUE >= -128 && të_dhëna_VALUE <= 127) Store_numër_i_plotë[të_dhëna_VALUE + 128] = objekt_Referencë; } } 넣기(objekt_Referencë, 2); return true; }
            if (komandë_kod == 183 && Word_SMS(emër_konstante, "<init>") && Word_SMS(서술상수, "(I)V")) { int të_dhëna_VALUE = 빼기(1), objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 12)) 힙[objekt_Referencë + 2] = të_dhëna_VALUE; return true; }
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "intValue") && Word_SMS(서술상수, "()I")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 12)) 넣기(힙[objekt_Referencë + 2], 1); return true; }
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(shifër_karakter(빼기(1)), 2); return true; }
        }
        if (Word_SMS(pronari, "java/lang/Math") && komandë_kod == 184) {
            if (Word_SMS(emër_konstante, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(emër_konstante, "min") || Word_SMS(emër_konstante, "max")) && Word_SMS(서술상수, "(II)I")) { int bajt_të_dhëna = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(emër_konstante, "min") ? (첫값 < bajt_të_dhëna ? 첫값 : bajt_të_dhëna) : (첫값 > bajt_të_dhëna ? 첫값 : bajt_të_dhëna), 1); return true; }
        }
        if (Word_SMS(pronari, "java/lang/System") && komandë_kod == 184) {
            if (Word_SMS(emër_konstante, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(emër_konstante, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int futje_COUNT = 빼기(1), vendmbërritje_VALUE_INDEX = 빼기(1), bajt_të_dhëna = 빼기(2), nis_pozicioni = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bajt_të_dhëna)) {
                    int kategori_kod = 힙[첫값];
                    if (힙[bajt_të_dhëna] != kategori_kod || (kategori_kod != 2 && kategori_kod != 3 && (kategori_kod < 20 || kategori_kod > 23))) dështim_VALUE("arraycopy type mismatch");
                    else if (futje_COUNT < 0 || nis_pozicioni < 0 || vendmbërritje_VALUE_INDEX < 0 || nis_pozicioni > 힙[첫값 + 1] - futje_COUNT || vendmbërritje_VALUE_INDEX > 힙[bajt_të_dhëna + 1] - futje_COUNT) dështim_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bajt_të_dhëna && vendmbërritje_VALUE_INDEX > nis_pozicioni) { for (int Loop_INDEX = futje_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bajt_të_dhëna + 2 + vendmbërritje_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + nis_pozicioni + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT && !GABIM; Loop_INDEX++) { int të_dhëna_VALUE = 힙[첫값 + 2 + nis_pozicioni + Loop_INDEX]; if (kategori_kod != 3 || 배열저장가능(bajt_të_dhëna, të_dhëna_VALUE)) 힙[bajt_të_dhëna + 2 + vendmbërritje_VALUE_INDEX + Loop_INDEX] = të_dhëna_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(pronari, "java/util/ArrayList") || Word_SMS(pronari, "java/util/List") || Word_SMS(pronari, "java/util/HashMap") || Word_SMS(pronari, "java/util/Map")) {
            모음호출(pronari, emër_konstante, 서술상수, komandë_kod); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_Referencë, int 필요수) {
        int 이전값 = 힙[objekt_Referencë + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Tjetër_pozicioni = 용량값 < 8 ? 8 : 용량값 * 2; if (Tjetër_pozicioni < 필요수) Tjetër_pozicioni = 필요수;
        int të_dhëna_ARRAY = caktoj_hapësira_ruajtëse(3, Tjetër_pozicioni); if (GABIM) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[të_dhëna_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objekt_Referencë + 2] = të_dhëna_ARRAY; 힙참조[objekt_Referencë + 2] = 1;
    }
    static void 모음호출(int pronari, int emër_konstante, int 서술상수, int komandë_kod) {
        boolean 대응참조 = Word_SMS(pronari, "java/util/HashMap") || Word_SMS(pronari, "java/util/Map"); int kategori_kod = 대응참조 ? 11 : 10;
        if (Word_SMS(emër_konstante, "<init>") && komandë_kod == 183 && Word_SMS(서술상수, "()V")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, kategori_kod)) 모음늘리기(objekt_Referencë, 8); return; }
        if (komandë_kod != 182 && komandë_kod != 185) { dështim_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(emër_konstante, "size") && Word_SMS(서술상수, "()I") || Word_SMS(emër_konstante, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, kategori_kod)) 넣기(Word_SMS(emër_konstante, "size") ? 힙[objekt_Referencë + 3] : 힙[objekt_Referencë + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(emër_konstante, "clear") && Word_SMS(서술상수, "()V")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, kategori_kod)) { int të_dhëna_ARRAY = 힙[objekt_Referencë + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[të_dhëna_ARRAY + 1]; Loop_INDEX++) 힙[të_dhëna_ARRAY + 2 + Loop_INDEX] = 0; 힙[objekt_Referencë + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(emër_konstante, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int të_dhëna_VALUE = 빼기(2), objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 10)) return;
            int futje_COUNT = 힙[objekt_Referencë + 3]; 모음늘리기(objekt_Referencë, futje_COUNT + 1); if (!GABIM) { 힙[힙[objekt_Referencë + 2] + 2 + futje_COUNT] = të_dhëna_VALUE; 힙[objekt_Referencë + 3] = futje_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(emër_konstante, "get") || Word_SMS(emër_konstante, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(emër_konstante, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(emër_konstante, "set"); int të_dhëna_VALUE = 지정여부 ? 빼기(2) : 0, futje_pozicioni = 빼기(1), objekt_Referencë = 빼기(2);
            if (!objekt_VALUE(objekt_Referencë, 10)) return;
            int futje_COUNT = 힙[objekt_Referencë + 3], të_dhëna_ARRAY = 힙[objekt_Referencë + 2];
            if (futje_pozicioni < 0 || futje_pozicioni >= futje_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[të_dhëna_ARRAY + 2 + futje_pozicioni];
            if (지정여부) 힙[të_dhëna_ARRAY + 2 + futje_pozicioni] = të_dhëna_VALUE;
            if (Word_SMS(emër_konstante, "remove")) { for (int Loop_INDEX = futje_pozicioni + 1; Loop_INDEX < futje_COUNT; Loop_INDEX++) 힙[të_dhëna_ARRAY + 1 + Loop_INDEX] = 힙[të_dhëna_ARRAY + 2 + Loop_INDEX]; 힙[të_dhëna_ARRAY + 1 + futje_COUNT] = 0; 힙[objekt_Referencë + 3] = futje_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(emër_konstante, "get") || Word_SMS(emër_konstante, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(emër_konstante, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(emër_konstante, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(emër_konstante, "put"), heq = Word_SMS(emër_konstante, "remove");
            int të_dhëna_VALUE = 넣기여부 ? 빼기(2) : 0, tast_Referencë = 빼기(2), objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 11)) return;
            int futje_COUNT = 힙[objekt_Referencë + 3], të_dhëna_ARRAY = 힙[objekt_Referencë + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) if (값같음(tast_Referencë, 힙[të_dhëna_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[të_dhëna_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_Referencë, (futje_COUNT + 1) * 2); të_dhëna_ARRAY = 힙[objekt_Referencë + 2]; 찾은여부 = futje_COUNT; if (!GABIM) 힙[objekt_Referencë + 3] = futje_COUNT + 1; }
                if (!GABIM) { 힙[të_dhëna_ARRAY + 2 + 2 * 찾은여부] = tast_Referencë; 힙[të_dhëna_ARRAY + 3 + 2 * 찾은여부] = të_dhëna_VALUE; }
            }
            if (heq && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < futje_COUNT; Loop_INDEX++) { 힙[të_dhëna_ARRAY + 2 * Loop_INDEX] = 힙[të_dhëna_ARRAY + 2 + 2 * Loop_INDEX]; 힙[të_dhëna_ARRAY + 1 + 2 * Loop_INDEX] = 힙[të_dhëna_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[të_dhëna_ARRAY + 2 * futje_COUNT] = 0; 힙[të_dhëna_ARRAY + 1 + 2 * futje_COUNT] = 0; 힙[objekt_Referencë + 3] = futje_COUNT - 1; }
            if (Word_SMS(emër_konstante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        dështim_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_Referencë) {
        if (!객체유효(objekt_Referencë)) return false;
        if (잠금깊이[objekt_Referencë] != 0 && 잠금주인[objekt_Referencë] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[objekt_Referencë] = 현재가닥 + 1; 잠금깊이[objekt_Referencë]++; return true;
    }
    static void 잠금풀기(int objekt_Referencë) {
        if (!객체유효(objekt_Referencë)) return;
        if (잠금깊이[objekt_Referencë] == 0 || 잠금주인[objekt_Referencë] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_Referencë] == 0) 잠금주인[objekt_Referencë] = 0;
    }
    static boolean SWITCH_thread() {
        thread_kuadër[현재가닥] = kuadër_INDEX;
        if (kuadër_INDEX < 현재가닥 * 32) thread_status[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < thread_COUNT; Loop_INDEX++) if (thread_status[Loop_INDEX] == 2 && thread_status[가닥대기[Loop_INDEX]] == 3) thread_status[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= thread_COUNT; Loop_INDEX++) {
            int Tjetër_pozicioni = (현재가닥 + Loop_INDEX) % thread_COUNT;
            if (thread_status[Tjetër_pozicioni] == 1) { 현재가닥 = Tjetër_pozicioni; kuadër_INDEX = thread_kuadër[Tjetër_pozicioni]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < thread_COUNT; Loop_INDEX++) if (thread_status[Loop_INDEX] != 3) { dështim_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int emër_konstante, int 서술상수, int komandë_kod) { Proces_thread(emër_konstante, 서술상수, komandë_kod, false); }
    static void Proces_thread(int emër_konstante, int 서술상수, int komandë_kod, boolean 한국어) {
        if (komandë_kod == 184 && Word_SMS(emër_konstante, 한국어 ? "YIELD_detyrë" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (komandë_kod == 184 && Word_SMS(emër_konstante, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(thread_objekt[현재가닥], 2); return; }
        if (komandë_kod == 183 && Word_SMS(emër_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int objektiv_email = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Referencë = 빼기(2);
            if (!객체유효(objekt_Referencë)) return;
            if (힙[objekt_Referencë] == 13) { 힙[objekt_Referencë + 2] = objektiv_email; 힙참조[objekt_Referencë + 2] = 1; }
            else if (objektiv_email != 0) dështim_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komandë_kod == 182 && (Word_SMS(emër_konstante, 한국어 ? "nis_detyrë" : "start") || Word_SMS(emër_konstante, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || komandë_kod == 182 && Word_SMS(emër_konstante, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekt_Referencë = 빼기(2); if (!객체유효(objekt_Referencë)) return;
            int llogari_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < thread_COUNT; Loop_INDEX++) if (thread_objekt[Loop_INDEX] == objekt_Referencë) llogari_VALUE = Loop_INDEX;
            if (Word_SMS(emër_konstante, 한국어 ? "살아있는가" : "isAlive")) { 넣기(llogari_VALUE >= 0 && thread_status[llogari_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(emër_konstante, 한국어 ? "기다리기" : "join")) { if (llogari_VALUE >= 0 && thread_status[llogari_VALUE] != 3) { 가닥대기[현재가닥] = llogari_VALUE; thread_status[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (llogari_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (thread_COUNT == 4) { dështim_VALUE("thread limit (4 including main)"); return; }
            int objektiv_email = 힙[objekt_Referencë] == 13 ? 힙[objekt_Referencë + 2] : objekt_Referencë;
            int skedar_INDEX = objektiv_email > 0 && 힙[objektiv_email] >= 32 ? emër_metoda(힙[objektiv_email] - 32, 한국어 ? "Kryej" : "run", "()V") : -1;
            if (objektiv_email != 0 && skedar_INDEX < 0) { dështim_VALUE("Runnable.run required"); return; }
            llogari_VALUE = thread_COUNT++; thread_objekt[llogari_VALUE] = objekt_Referencë; thread_objektiv[llogari_VALUE] = objektiv_email;
            int kuadër = llogari_VALUE * 32; thread_kuadër[llogari_VALUE] = skedar_INDEX < 0 ? kuadër - 1 : kuadër; thread_status[llogari_VALUE] = skedar_INDEX < 0 ? 3 : 1;
            if (skedar_INDEX >= 0) { kuadër_metoda[kuadër] = skedar_INDEX; kuadër_pozicioni[kuadër] = metoda_nis[skedar_INDEX]; lokal_VALUE[kuadër * 128] = objektiv_email; lokal_TYPE[kuadër * 128] = 2; }
            return;
        }
        dështim_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], email_SMS = new int[16];
    static int lokal_email() { return email_objekt(0x7f000001); }
    static int email_objekt(int VALUE) { int objekt_Referencë = caktoj_hapësira_ruajtëse(14, 1); if (!GABIM) 힙[objekt_Referencë + 2] = VALUE; return objekt_Referencë; }
    static int 주소해독(int objekt_Referencë) {
        if (objekt_Referencë == 0 || 글같음(objekt_Referencë, pritës_karakter("localhost"), false)) return 0x7f000001;
        if (!objekt_VALUE(objekt_Referencë, 1)) return 0;
        int të_dhëna_VALUE = 0, 총수 = 0, email_bajt = 0, 자릿수 = 0, futje_COUNT = 힙[objekt_Referencë + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= futje_COUNT; Loop_INDEX++) {
            int kodi_i_karakterit = Loop_INDEX == futje_COUNT ? '.' : 힙[objekt_Referencë + 2 + Loop_INDEX];
            if (kodi_i_karakterit == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } të_dhëna_VALUE = të_dhëna_VALUE << 8 | email_bajt; 총수++; email_bajt = 자릿수 = 0; }
            else { if (kodi_i_karakterit < '0' || kodi_i_karakterit > '9' || ++자릿수 > 3 || (email_bajt = email_bajt * 10 + kodi_i_karakterit - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return të_dhëna_VALUE;
    }
    static int email_karakter(int të_dhëna_VALUE) {
        int futje_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int email_bajt = të_dhëna_VALUE >>> 이동비트 & 255;
            if (email_bajt >= 100) email_SMS[futje_COUNT++] = '0' + email_bajt / 100;
            if (email_bajt >= 10) email_SMS[futje_COUNT++] = '0' + email_bajt / 10 % 10;
            email_SMS[futje_COUNT++] = '0' + email_bajt % 10; if (이동비트 != 0) email_SMS[futje_COUNT++] = '.';
        }
        int objekt_Referencë = caktoj_hapësira_ruajtëse(1, futje_COUNT); if (!GABIM) for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) 힙[objekt_Referencë + 2 + Loop_INDEX] = email_SMS[Loop_INDEX]; return objekt_Referencë;
    }
    static void 통신호출(int pronari, int emër_konstante, int 서술상수, int komandë_kod) {
        if (Word_SMS(pronari, "java/net/InetAddress")) {
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_email(), 2); return; }
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int të_dhëna_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !GABIM) 넣기(email_objekt(të_dhëna_VALUE), 2); return;
            }
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 14)) 넣기(email_karakter(힙[objekt_Referencë + 2]), 2); return; }
        }
        if (Word_SMS(pronari, "java/net/DatagramPacket")) {
            if (komandë_kod == 183 && Word_SMS(emër_konstante, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean vendmbërritje_VALUE_Referencë = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int numri_i_portës = vendmbërritje_VALUE_Referencë ? 빼기(1) : 0, email_Referencë = vendmbërritje_VALUE_Referencë ? 빼기(2) : 0;
                int futje_COUNT = 빼기(1), të_dhëna_ARRAY = 빼기(2), objekt_Referencë = 빼기(2);
                if (!objekt_VALUE(objekt_Referencë, 16) || !objekt_VALUE(të_dhëna_ARRAY, 20)) return;
                if (futje_COUNT < 0 || futje_COUNT > 힙[të_dhëna_ARRAY + 1] || numri_i_portës < 0 || numri_i_portës > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (email_Referencë != 0 && !objekt_VALUE(email_Referencë, 14)) return;
                힙[objekt_Referencë + 2] = të_dhëna_ARRAY; 힙참조[objekt_Referencë + 2] = 1; 힙[objekt_Referencë + 3] = futje_COUNT;
                힙[objekt_Referencë + 4] = email_Referencë; 힙참조[objekt_Referencë + 4] = 1; 힙[objekt_Referencë + 5] = numri_i_portës; return;
            }
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int futje_COUNT = 빼기(1), objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 16)) return;
                if (futje_COUNT < 0 || futje_COUNT > 힙[힙[objekt_Referencë + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objekt_Referencë + 3] = futje_COUNT; return;
            }
            if (komandë_kod == 182 && (Word_SMS(emër_konstante, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(emër_konstante, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(emër_konstante, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(emër_konstante, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 16)) return;
                int futje_pozicioni = Word_SMS(emër_konstante, "getData") ? 2 : Word_SMS(emër_konstante, "getLength") ? 3 : Word_SMS(emër_konstante, "getAddress") ? 4 : 5;
                넣기(힙[objekt_Referencë + futje_pozicioni], futje_pozicioni == 2 || futje_pozicioni == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(pronari, "java/net/DatagramSocket")) {
            if (komandë_kod == 183 && Word_SMS(emër_konstante, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int numri_i_portës = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 15)) return;
                if (numri_i_portës < 0 || numri_i_portës > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = përdorues.hap_rrjet(numri_i_portës); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objekt_Referencë + 2] = 열린파일번호; return;
            }
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Referencë + 3] = 밀리초값; return;
            }
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 15)) 넣기(힙[objekt_Referencë + 2] < 0 ? -1 : përdorues.rrjet_portë(힙[objekt_Referencë + 2]), 1); return; }
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 15)) 넣기(힙[objekt_Referencë + 2] < 0 ? 1 : 0, 1); return; }
            if (komandë_kod == 182 && Word_SMS(emër_konstante, "close") && Word_SMS(서술상수, "()V")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 15) && 힙[objekt_Referencë + 2] >= 0) { përdorues.파일서술자닫기(힙[objekt_Referencë + 2]); 힙[objekt_Referencë + 2] = -1; } return; }
            if (komandë_kod == 182 && (Word_SMS(emër_konstante, "send") || Word_SMS(emër_konstante, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paketë = 빼기(2), objekt_Referencë = 빼기(2); if (!objekt_VALUE(paketë, 16) || !objekt_VALUE(objekt_Referencë, 15)) return;
                int të_dhëna_ARRAY = 힙[paketë + 2], 유효길이 = 힙[paketë + 3], 열린파일번호 = 힙[objekt_Referencë + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(emër_konstante, "send")) {
                    if (!objekt_VALUE(힙[paketë + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[të_dhëna_ARRAY + 2 + Loop_INDEX];
                    if (përdorues.dërgoj_rrjet(열린파일번호, 힙[힙[paketë + 4] + 2], 힙[paketë + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int futje_COUNT = përdorues.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (futje_COUNT == -11) {
                        int 현재시각 = përdorues.밀리초();
                        if (힙[objekt_Referencë + 4] == 0) 힙[objekt_Referencë + 4] = 현재시각 + 1;
                        if (힙[objekt_Referencë + 3] > 0 && 현재시각 - (힙[objekt_Referencë + 4] - 1) >= 힙[objekt_Referencë + 3]) { 힙[objekt_Referencë + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_Referencë, 2); 넣기(paketë, 2); kuadër_pozicioni[kuadër_INDEX] = kuadër_instruksion[kuadër_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[objekt_Referencë + 4] = 0;
                    if (futje_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) 힙[të_dhëna_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paketë + 3] = futje_COUNT; 힙[paketë + 4] = email_objekt(통신임시[513]); 힙참조[paketë + 4] = 1; 힙[paketë + 5] = 통신임시[512];
                }
                return;
            }
        }
        dështim_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_Referencë) {
        int 현재시각 = përdorues.밀리초();
        if (힙[objekt_Referencë + 5] == 0) 힙[objekt_Referencë + 5] = 현재시각 + 1;
        if (힙[objekt_Referencë + 3] > 0 && 현재시각 - (힙[objekt_Referencë + 5] - 1) >= 힙[objekt_Referencë + 3]) { 힙[objekt_Referencë + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kuadër_pozicioni[kuadër_INDEX] = kuadër_instruksion[kuadër_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int pronari, int emër_konstante, int 서술상수, int komandë_kod) {
        boolean 수신쪽 = Word_SMS(pronari, "java/net/ServerSocket"), Stream = Word_SMS(pronari, "java/io/InputStream") || Word_SMS(pronari, "java/io/OutputStream");
        if (!Stream && komandë_kod == 183 && Word_SMS(emër_konstante, "<init>")) {
            boolean teknologjia_e_informacionit_bosh_status = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(teknologjia_e_informacionit_bosh_status || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { dështim_VALUE("unsupported socket constructor"); return; }
            int numri_i_portës = teknologjia_e_informacionit_bosh_status ? 0 : 빼기(1), email_Referencë = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_Referencë = 빼기(2);
            if (!objekt_VALUE(objekt_Referencë, 수신쪽 ? 18 : 17)) return;
            if (numri_i_portës < 0 || numri_i_portës > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VALUE(email_Referencë, 14)) return;
            int rrjet_email_df3458bb = 이름지정여부 ? 주소해독(email_Referencë) : 주소지정여부 ? 힙[email_Referencë + 2] : 0x7f000001;
            if (GABIM || 던진객체 != 0) return;
            int 열린파일번호 = përdorues.Stream_kontroll(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = teknologjia_e_informacionit_bosh_status ? 0 : 수신쪽 ? përdorues.Stream_kontroll(1, 열린파일번호, numri_i_portës) : përdorues.Lidh_Stream(열린파일번호, rrjet_email_df3458bb, numri_i_portës);
            if (처리값 < 0) { përdorues.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objekt_Referencë + 2] = 열린파일번호; 힙[objekt_Referencë + 4] = numri_i_portës; 힙[objekt_Referencë + 6] = teknologjia_e_informacionit_bosh_status ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(emër_konstante, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Referencë + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(emër_konstante, "close") && Word_SMS(서술상수, "()V")) { int objekt_Referencë = 빼기(2); if (objekt_VALUE(objekt_Referencë, 수신쪽 ? 18 : 17) && 힙[objekt_Referencë + 2] >= 0) { përdorues.파일서술자닫기(힙[objekt_Referencë + 2]); 힙[objekt_Referencë + 2] = -1; } return; }
        if (!Stream && (Word_SMS(emër_konstante, "getLocalPort") || Word_SMS(emër_konstante, "getPort") || Word_SMS(emër_konstante, "isClosed") || Word_SMS(emër_konstante, "isConnected"))) {
            int objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(emër_konstante, "isClosed") ? 힙[objekt_Referencë + 2] < 0 ? 1 : 0 : Word_SMS(emër_konstante, "isConnected") ? 힙[objekt_Referencë + 6] : Word_SMS(emër_konstante, "getPort") ? 힙[objekt_Referencë + 4] : 힙[objekt_Referencë + 2] < 0 ? -1 : përdorues.Stream_kontroll(4, 힙[objekt_Referencë + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(emër_konstante, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 18)) return; int 열린파일번호 = përdorues.Stream_kontroll(3, 힙[objekt_Referencë + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_Referencë)) 넣기(objekt_Referencë, 2); return; }
            힙[objekt_Referencë + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = caktoj_hapësira_ruajtëse(17, 5); if (GABIM) { përdorues.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = përdorues.Stream_kontroll(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(emër_konstante, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(emër_konstante, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 17)) return; if (힙[objekt_Referencë + 2] < 0 || 힙[objekt_Referencë + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = caktoj_hapësira_ruajtëse(19, 4); if (GABIM) return; 힙[반환값 + 2] = objekt_Referencë; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(emër_konstante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(emër_konstante, "read"), teknologjia_e_informacionit_shkruaj_operim = Word_SMS(emër_konstante, "write"), bllokoj = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), teknologjia_e_informacionit_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int futje_COUNT = teknologjia_e_informacionit_SUBARRAY ? 빼기(1) : 0, 시작변위 = teknologjia_e_informacionit_SUBARRAY ? 빼기(1) : 0, të_dhëna_ARRAY = bllokoj || teknologjia_e_informacionit_SUBARRAY ? 빼기(2) : 0;
            int të_dhëna_VALUE = teknologjia_e_informacionit_shkruaj_operim && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_Referencë = 빼기(2);
            if (!objekt_VALUE(objekt_Referencë, 19)) return; int 부모참조 = 힙[objekt_Referencë + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(emër_konstante, "close") && Word_SMS(서술상수, "()V")) { përdorues.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(emër_konstante, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !teknologjia_e_informacionit_shkruaj_operim) || 읽기여부 != (힙[objekt_Referencë + 3] == 0)) { dështim_VALUE("unsupported stream operation"); return; }
            if (bllokoj || teknologjia_e_informacionit_SUBARRAY) { if (!objekt_VALUE(të_dhëna_ARRAY, 20)) return; if (bllokoj) futje_COUNT = 힙[të_dhëna_ARRAY + 1]; if (시작변위 < 0 || futje_COUNT < 0 || 시작변위 > 힙[të_dhëna_ARRAY + 1] - futje_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else futje_COUNT = 1;
            if (futje_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = teknologjia_e_informacionit_shkruaj_operim ? 힙[objekt_Referencë + 4] : 0, 처리값 = 0;
            while (완료수 < futje_COUNT) {
                처리값 = 읽기여부 ? përdorues.파일한바이트읽기(열린파일번호) : përdorues.파일한바이트쓰기(열린파일번호, bllokoj || teknologjia_e_informacionit_SUBARRAY ? 힙[të_dhëna_ARRAY + 2 + 시작변위 + 완료수] : të_dhëna_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bllokoj || teknologjia_e_informacionit_SUBARRAY)) 힙[të_dhëna_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(bllokoj || teknologjia_e_informacionit_SUBARRAY)) break;
            }
            if (처리값 == -11 && (teknologjia_e_informacionit_shkruaj_operim || 완료수 == 0)) {
                힙[objekt_Referencë + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(objekt_Referencë, 2); if (bllokoj || teknologjia_e_informacionit_SUBARRAY) 넣기(të_dhëna_ARRAY, 2); if (teknologjia_e_informacionit_SUBARRAY) { 넣기(시작변위, 1); 넣기(futje_COUNT, 1); } if (teknologjia_e_informacionit_shkruaj_operim && !(bllokoj || teknologjia_e_informacionit_SUBARRAY)) 넣기(të_dhëna_VALUE, 1); } return;
            }
            힙[objekt_Referencë + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : bllokoj || teknologjia_e_informacionit_SUBARRAY ? 완료수 : 처리값, 1); return;
        }
        dështim_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int emër_konstante) {
        if (Word_SMS(emër_konstante, "한국어/자체/Dritare")) return 24;
        if (Word_SMS(emër_konstante, "한국어/자체/Etiketë")) return 26;
        if (Word_SMS(emër_konstante, "한국어/자체/Buton")) return 27;
        if (Word_SMS(emër_konstante, "한국어/자체/SMS_fushë")) return 28;
        if (Word_SMS(emër_konstante, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int emër_konstante) {
        return 한국어화면종(emër_konstante) != 0 || Word_SMS(emër_konstante, "한국어/자체/화면구성요소") || Word_SMS(emër_konstante, "한국어/자체/ngjarje_radhë");
    }
    static int 화면종(int emër_konstante) {
        int 한국어종 = 한국어화면종(emër_konstante); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(emër_konstante, "javax/swing/JFrame")) return 24;
        if (Word_SMS(emër_konstante, "javax/swing/JPanel")) return 25;
        if (Word_SMS(emër_konstante, "javax/swing/JLabel")) return 26;
        if (Word_SMS(emër_konstante, "javax/swing/JButton")) return 27;
        if (Word_SMS(emër_konstante, "javax/swing/JTextField")) return 28;
        if (Word_SMS(emër_konstante, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(emër_konstante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int emër_konstante) {
        return 화면종(emër_konstante) != 0 || Word_SMS(emër_konstante, "java/awt/Component") || Word_SMS(emër_konstante, "java/awt/Container") || Word_SMS(emër_konstante, "javax/swing/JComponent") || Word_SMS(emër_konstante, "javax/swing/AbstractButton") || Word_SMS(emër_konstante, "javax/swing/text/JTextComponent") || Word_SMS(emër_konstante, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekt_Referencë) { if (!객체유효(objekt_Referencë)) return false; if (힙[objekt_Referencë] < 24 || 힙[objekt_Referencë] > 28) { dështim_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekt_Referencë, int SMS_Referencë) {
        if (SMS_Referencë != 0 && !objekt_VALUE(SMS_Referencë, 1)) return;
        int futje_COUNT = SMS_Referencë == 0 ? 0 : 힙[SMS_Referencë + 1]; if (futje_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Referencë + 2 + Loop_INDEX];
        if (përdorues.화면글(힙[objekt_Referencë + 2], 화면글임시, futje_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objekt_Referencë + 3] = SMS_Referencë; 힙참조[objekt_Referencë + 3] = 1;
    }
    static int 화면문자읽기(int objekt_Referencë) {
        int llogari_VALUE = 힙[objekt_Referencë + 2], futje_COUNT = përdorues.화면연결(8, llogari_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (futje_COUNT < 0) { dështim_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) { int 부호값 = përdorues.화면연결(9, llogari_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = caktoj_hapësira_ruajtëse(1, 사용수); if (!GABIM) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 bërthamë_VALUE 화면 기능에 연결한다. Swing objekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int pronari, int emër_konstante, int 서술상수, int komandë_kod) {
        if (Word_SMS(pronari, "한국어/자체/ngjarje_radhë")) {
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int detyrë_veprim = 빼기(2); if (!객체유효(detyrë_veprim)) return;
                if (나중수 == 8) { dështim_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = detyrë_veprim; return;
            }
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            dështim_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(pronari, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!objekt_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(emër_konstante, "ngjarje_burim") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(emër_konstante, "komandë_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(emër_konstante, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else dështim_VALUE("지원하지 않는 한국어 Veprim 알림 호출"); return;
        }
        if (komandë_kod == 183 && Word_SMS(emër_konstante, "<init>")) {
            int 종류 = 한국어화면종(pronari), 받이 = 0, 가로 = 0, Vertikal_pozicioni = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (përdorues.화면너비() - 폭) / 2; Vertikal_pozicioni = (përdorues.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertikal_pozicioni = 빼기(1); 가로 = 빼기(1);
            } else { dështim_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int Teksti = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertikal_pozicioni < 0 || 폭 > përdorues.화면너비() - 가로 || 높이 > përdorues.화면높이() - Vertikal_pozicioni) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = përdorues.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { dështim_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikal_pozicioni; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            përdorues.화면연결(1, INDEX, 가로, Vertikal_pozicioni, 폭, 높이);
            if (종류 == 24) përdorues.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Teksti); return;
        }
        if (komandë_kod != 182) { dështim_VALUE("잘못된 한국어 화면 호출 Komanda"); return; }
        if (Word_SMS(emër_konstante, "shkruaj_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Teksti = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Teksti); return;
        }
        if (Word_SMS(emër_konstante, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(emër_konstante, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(emër_konstante, "shto_element") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int fëmijë_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(fëmijë_VALUE) || !화면객체(부모)) return;
            if (përdorues.화면연결(2, 힙[부모 + 2], 힙[fëmijë_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[fëmijë_VALUE + 11] = 부모; 힙참조[fëmijë_VALUE + 11] = 1; return;
        }
        if (Word_SMS(emër_konstante, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertikal_pozicioni = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (përdorues.화면연결(1, 힙[element_VALUE + 2], 가로, Vertikal_pozicioni, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikal_pozicioni; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(emër_konstante, "shfaq_dritare") || Word_SMS(emër_konstante, "Mbyll")) && Word_SMS(서술상수, "()V")) {
            boolean dukshmëri_VALUE = Word_SMS(emër_konstante, "shfaq_dritare"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (përdorues.화면연결(dukshmëri_VALUE ? 3 : 4, 힙[element_VALUE + 2], dukshmëri_VALUE ? 1 : 0, 0, 0, 0) < 0) { dështim_VALUE("화면은 ndërvepruese 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = dukshmëri_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(emër_konstante, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        dështim_VALUE("지원하지 않는 한국어 화면 metoda_VALUE");
    }
    static void 화면호출(int pronari, int emër_konstante, int 서술상수, int komandë_kod) {
        if (Word_SMS(pronari, "javax/swing/SwingUtilities")) {
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_Referencë = 빼기(2); if (!객체유효(objekt_Referencë)) return; if (나중수 == 8) { dështim_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_Referencë; return; }
            if (komandë_kod == 184 && Word_SMS(emër_konstante, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            dështim_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(pronari, "java/awt/event/ActionEvent")) {
            int objekt_Referencë = 빼기(2); if (!objekt_VALUE(objekt_Referencë, 29)) return;
            if (Word_SMS(emër_konstante, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objekt_Referencë + 2], 2);
            else if (Word_SMS(emër_konstante, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objekt_Referencë + 2]), 2);
            else if (Word_SMS(emër_konstante, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else dështim_VALUE("unsupported ActionEvent method"); return;
        }
        if (komandë_kod == 183 && Word_SMS(emër_konstante, "<init>")) {
            int COLUMNS = 0, SMS_Referencë = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Referencë = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Referencë = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { dështim_VALUE("unsupported Swing constructor"); return; }
            int objekt_Referencë = 빼기(2); if (!객체유효(objekt_Referencë)) return;
            if (힙[objekt_Referencë] == 30) { dështim_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekt_Referencë) || COLUMNS < 0) return;
            int llogari_VALUE = përdorues.화면연결(0, 힙[objekt_Referencë] - 23, 0, 0, 0, 0);
            if (llogari_VALUE < 1 || llogari_VALUE > 32) { dështim_VALUE("GUI widget slots exhausted"); return; }
            힙[objekt_Referencë + 2] = llogari_VALUE; 화면참조[llogari_VALUE - 1] = objekt_Referencë; 힙[objekt_Referencë + 5] = 힙[objekt_Referencë] == 24 ? 130 : 16; 힙[objekt_Referencë + 6] = 힙[objekt_Referencë] == 24 ? 110 : 16;
            힙[objekt_Referencë + 7] = 힙[objekt_Referencë] == 24 ? 380 : 220; 힙[objekt_Referencë + 8] = 힙[objekt_Referencë] == 24 ? 240 : 28; 힙[objekt_Referencë + 10] = 1;
            화면문자설정(objekt_Referencë, SMS_Referencë); return;
        }
        if (Word_SMS(emër_konstante, "setText") || Word_SMS(emër_konstante, "setTitle")) { int SMS_Referencë = 빼기(2), objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekt_Referencë, SMS_Referencë); return; }
        if (Word_SMS(emër_konstante, "getText") || Word_SMS(emër_konstante, "getTitle")) { int objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_Referencë), 2); return; }
        if (Word_SMS(emër_konstante, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë)) { 힙[objekt_Referencë + 4] = 수신참조; 힙참조[objekt_Referencë + 4] = 1; } return; }
        if (Word_SMS(emër_konstante, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë)) 넣기(objekt_Referencë, 2); return; }
        if (Word_SMS(emër_konstante, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Navigimi_Referencë = 빼기(2), objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë) && Navigimi_Referencë != 0) dështim_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(emër_konstante, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Navigimi_kusht = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Navigimi_kusht) 빼기(2);
            int fëmijë_Referencë = 빼기(2), objekt_Referencë = 빼기(2); if (!화면객체(fëmijë_Referencë) || !화면객체(objekt_Referencë)) return;
            if (përdorues.화면연결(2, 힙[objekt_Referencë + 2], 힙[fëmijë_Referencë + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[fëmijë_Referencë + 11] = objekt_Referencë; 힙참조[fëmijë_Referencë + 11] = 1; if (!Navigimi_kusht) 넣기(fëmijë_Referencë, 2); return;
        }
        if (Word_SMS(emër_konstante, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinatë = 빼기(1), koordinata_x = 빼기(1), objekt_Referencë = 빼기(2); if (!화면객체(objekt_Referencë)) return;
            if (përdorues.화면연결(1, 힙[objekt_Referencë + 2], koordinata_x, Y_koordinatë, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objekt_Referencë + 5] = koordinata_x; 힙[objekt_Referencë + 6] = Y_koordinatë; 힙[objekt_Referencë + 7] = 너비; 힙[objekt_Referencë + 8] = 높이; return;
        }
        if (Word_SMS(emër_konstante, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_Referencë = 빼기(2); if (!화면객체(objekt_Referencë)) return;
            if (përdorues.화면연결(1, 힙[objekt_Referencë + 2], 힙[objekt_Referencë + 5], 힙[objekt_Referencë + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objekt_Referencë + 7] = 너비; 힙[objekt_Referencë + 8] = 높이; } return;
        }
        if (Word_SMS(emër_konstante, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_Referencë = 빼기(2); if (!화면객체(objekt_Referencë)) return; if (상대배치 != 0) { dështim_VALUE("only screen centering supported"); return; } 힙[objekt_Referencë + 5] = (përdorues.화면너비() - 힙[objekt_Referencë + 7]) / 2; 힙[objekt_Referencë + 6] = (përdorues.화면높이() - 힙[objekt_Referencë + 8]) / 2; përdorues.화면연결(1, 힙[objekt_Referencë + 2], 힙[objekt_Referencë + 5], 힙[objekt_Referencë + 6], 힙[objekt_Referencë + 7], 힙[objekt_Referencë + 8]); return; }
        if (Word_SMS(emër_konstante, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int politikë = 빼기(1), objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë)) { if (politikë < 0 || politikë > 3) 예외던짐(9, "close policy"); else { 힙[objekt_Referencë + 10] = politikë; përdorues.화면연결(7, 힙[objekt_Referencë + 2], politikë, 0, 0, 0); } } return; }
        if (Word_SMS(emër_konstante, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int të_dhëna_VALUE = 빼기(1), objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë)) { int 처리값 = përdorues.화면연결(3, 힙[objekt_Referencë + 2], të_dhëna_VALUE, 0, 0, 0); if (처리값 < 0) dështim_VALUE("Swing requires a standalone interactive command"); else 힙[objekt_Referencë + 9] = të_dhëna_VALUE; } return; }
        if (Word_SMS(emër_konstante, "dispose") && Word_SMS(서술상수, "()V")) { int objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë)) { përdorues.화면연결(4, 힙[objekt_Referencë + 2], 0, 0, 0, 0); 힙[objekt_Referencë + 9] = 0; } return; }
        if (Word_SMS(emër_konstante, "repaint") || Word_SMS(emër_konstante, "validate")) { int objekt_Referencë = 빼기(2); if (!화면객체(objekt_Referencë) || !Word_SMS(서술상수, "()V")) return; përdorues.화면연결(1, 힙[objekt_Referencë + 2], 힙[objekt_Referencë + 5], 힙[objekt_Referencë + 6], 힙[objekt_Referencë + 7], 힙[objekt_Referencë + 8]); return; }
        if (Word_SMS(emër_konstante, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekt_Referencë = 빼기(2); if (화면객체(objekt_Referencë)) 넣기(힙[objekt_Referencë + 9], 1); return; }
        dështim_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int objektiv_email, int 사건번호, boolean 한국어) {
        if (objektiv_email < 1 || 힙[objektiv_email] < 32) { dështim_VALUE("Java event listener required"); return; }
        int skedar_INDEX = emër_metoda(힙[objektiv_email] - 32, 사건번호 == 0 ? (한국어 ? "Kryej" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (skedar_INDEX < 0) { dështim_VALUE("event callback missing"); return; }
        현재가닥 = 0; thread_COUNT = 1; kuadër_INDEX = 0; thread_status[0] = 1; kuadër_Stivë[0] = 0; 틀잠금[0] = filloj_kuadër[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokal_VALUE[Loop_INDEX] = lokal_TYPE[Loop_INDEX] = 0; }
        kuadër_metoda[0] = skedar_INDEX; kuadër_pozicioni[0] = metoda_nis[skedar_INDEX]; lokal_VALUE[0] = objektiv_email; lokal_TYPE[0] = 2;
        if (사건번호 != 0) { lokal_VALUE[1] = 사건번호; lokal_TYPE[1] = 2; }
        사건중 = true; zbatoj_komandë(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!GABIM) {
            if (나중수 > 0) { int objektiv_email = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(objektiv_email, 0, 한국어 != 0); continue; }
            if (përdorues.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = përdorues.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { dështim_VALUE("GUI event I/O failed"); return; }
            int llogari_VALUE = 사건번호 & 65535; if (llogari_VALUE < 1 || llogari_VALUE > 32) continue; int objekt_Referencë = 화면참조[llogari_VALUE - 1]; if (objekt_Referencë == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objekt_Referencë + 10] != 0) 힙[objekt_Referencë + 9] = 0;
                if (힙[objekt_Referencë + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) përdorues.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objekt_Referencë + 4] != 0) {
                int LEXOMË_Referencë = caktoj_hapësira_ruajtëse(29, 2); if (GABIM) return; 힙[LEXOMË_Referencë + 2] = objekt_Referencë; 힙[LEXOMË_Referencë + 3] = 힙[objekt_Referencë + 12]; 힙참조[LEXOMË_Referencë + 2] = 1; 사건실행(힙[objekt_Referencë + 4], LEXOMË_Referencë, 힙[objekt_Referencë + 12] != 0);
            }
        }
    }
    public static int Ekzekuto() {
        if (përdorues.인수개수() == 1 && 자바도구.같음(përdorues.Argumente(0), "-version")) {
            përdorues.Shkrimi("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (përdorues.인수개수() < 1) { përdorues.Shkrimi("Usage: java CLASS [ARGS]\n"); return 2; }
        futje_klasë_Përkufizim = ngarkoj_klasë_Përkufizim(pritës_karakter(përdorues.Argumente(0))); if (GABIM || futje_klasë_Përkufizim < 0) return 1;
        int futje_p_VALUE = emër_metoda(futje_klasë_Përkufizim, "Ekzekuto", "()V");
        boolean 한국어진입 = futje_p_VALUE >= 0 && (metoda_qasem[futje_p_VALUE] & 9) == 9;
        if (!한국어진입) futje_p_VALUE = emër_metoda(futje_klasë_Përkufizim, "main", "([Ljava/lang/String;)V");
        if (futje_p_VALUE < 0 || (metoda_qasem[futje_p_VALUE] & 9) != 9) dështim_VALUE("public static void Ekzekuto() or main(String[] args) required");
        if (GABIM) return 1;
        int Argumente = caktoj_hapësira_ruajtëse(3, përdorues.인수개수() - 1); ARRAY_element[Argumente] = -1;
        for (int 수 = 1; 수 < përdorues.인수개수() && !GABIM; 수++) 힙[Argumente + 1 + 수] = pritës_karakter(përdorues.Argumente(수));
        kuadër_INDEX = 0; kuadër_metoda[0] = futje_p_VALUE; kuadër_pozicioni[0] = metoda_nis[futje_p_VALUE]; lokal_VALUE[0] = 한국어진입 ? 0 : Argumente; lokal_TYPE[0] = 한국어진입 ? 0 : 2;
        thread_status[0] = 1; thread_objekt[0] = caktoj_hapësira_ruajtëse(13, 2);
        zbatoj_komandë(); if (!GABIM) 화면사건들(); return GABIM ? 1 : 0;
    }
}
