// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. FAYL/스택/İstinad/qol 경계를 icra_etmək_əmr 중 검사한다. */
public final class 자바가상기계 {
    static int[] FAYL = new int[16 * 16384], 임시파일 = new int[16384], fayl_ad_SMS = new int[512];
    static int[] sabit_teq = new int[8192], 상가 = new int[8192], sabit_SECOND_VALUE = new int[8192], sətir_İstinad = new int[8192];
    static int[] metod_ad_SMS = new int[512], metod_TYPE = new int[512], metod_müraciət = new int[512], metod_sahib = new int[512];
    static int[] metod_Başla = new int[512], metod_bitirmək = new int[512], metod_Yığın = new int[512], 함수지역 = new int[512];
    static int[] metod_arqument_COUNT = new int[512], metod_arqument_TYPE = new int[8192], metod_geri_qaytarmaq = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokal_VALUE = new int[16384], lokal_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] kadr_metod = new int[128], kadr_yerinə_qoymaq = new int[128], kadr_Yığın = new int[128], kadr_təlimat = new int[128], ilkin_qiymət_vermək_kadr = new int[128];
    static int[] Sinif_Tərif_ad = new int[16], Sinif_Tərif_ölçünü_dəyişmək = new int[16], 종부모 = new int[16], Sinif_Tərif_vəziyyət = new int[16], Sinif_slot_COUNT = new int[16], ilkin_qiymət_vermək_Sinif_Tərif = new int[16];
    static int[] Sinif_interfeys = new int[16 * 16], Sinif_interfeys_COUNT = new int[16];
    static int[] slot_ad = new int[512], slot_TYPE = new int[512], slot_sahib = new int[512], slot_icazələr = new int[512], slot_yerinə_qoymaq = new int[512], slot_verilənlər = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_element = new int[32768], Store_tam_ədəd = new int[256];
    static int Böyüklük, 읽기위치, metod_COUNT, Sinif_ad, kadr_INDEX = -1, 힙끝 = 1, geri_qaytarmaq_TYPE;
    static int Sinif_Tərif_COUNT, slot_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, displey_COUNT, toplu_COUNT;
    static int 현재가닥, axın_COUNT = 1, daxiletmə_Sinif_Tərif;
    static int[] axın_kadr = new int[4], axın_vəziyyət = new int[4], axın_obyekt = new int[4], axın_hədəf = new int[4], 가닥대기 = new int[4];
    static boolean XƏTA, dəyişdirmək_HTTP_sorğusu;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], Sinif_axın = new int[16];

    static void xəta_VALUE(String Söz_SMS) {
        if (XƏTA) return;
        int sahə_kod = 0;
        if (자바도구.같음(Söz_SMS, "ArithmeticException: / by zero")) sahə_kod = 4;
        if (자바도구.같음(Söz_SMS, "NullPointerException") || 자바도구.같음(Söz_SMS, "null or invalid array")) sahə_kod = 5;
        if (자바도구.같음(Söz_SMS, "ArrayIndexOutOfBoundsException")) sahə_kod = 7;
        if (자바도구.같음(Söz_SMS, "StringIndexOutOfBoundsException")) sahə_kod = 8;
        if (자바도구.같음(Söz_SMS, "NumberFormatException")) sahə_kod = 10;
        if (자바도구.같음(Söz_SMS, "FileNotFoundException: file open failed")) sahə_kod = 12;
        if (자바도구.같음(Söz_SMS, "IOException: stream closed") || 자바도구.같음(Söz_SMS, "IOException: read failed") || 자바도구.같음(Söz_SMS, "IOException: write failed")) sahə_kod = 11;
        if (자바도구.같음(Söz_SMS, "ClassCastException")) sahə_kod = 14;
        if (자바도구.같음(Söz_SMS, "NegativeArraySizeException")) sahə_kod = 15;
        if (sahə_kod != 0 && kadr_INDEX >= 0) { 예외던짐(sahə_kod, Söz_SMS); return; }
        istifadəçi.Yazma("JVM error: "); istifadəçi.Yazma(Söz_SMS); istifadəçi.yazmaq_simvol_VALUE(10); XƏTA = true;
    }
    static boolean klip(int İcra_Et, int uzunluq_VALUE) {
        if (İcra_Et < 0 || İcra_Et >= FAYL.length || uzunluq_VALUE < 0) return false;
        int Sinif_Tərif = İcra_Et / 16384;
        return İcra_Et % 16384 <= Sinif_Tərif_ölçünü_dəyişmək[Sinif_Tərif] && uzunluq_VALUE <= Sinif_Tərif_ölçünü_dəyişmək[Sinif_Tərif] - İcra_Et % 16384;
    }
    static int bayt_VALUE() {
        if (!klip(읽기위치, 1)) { xəta_VALUE("truncated class file"); return 0; }
        return FAYL[읽기위치++];
    }
    static int 짧은수() { return bayt_VALUE() << 8 | bayt_VALUE(); }
    static int tam_ədəd() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int uzunluq_VALUE) { if (!klip(읽기위치, uzunluq_VALUE)) xəta_VALUE("invalid attribute size"); else 읽기위치 += uzunluq_VALUE; }
    static boolean çek_sabit(int 수, int 종류) {
        if (수 <= 0 || 수 >= sabit_teq.length || sabit_teq[수] != 종류) { xəta_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int İcra_Et, int uzunluq_VALUE, String Söz_SMS) {
        if (!klip(İcra_Et, uzunluq_VALUE)) return false;
        int 읽는자리 = İcra_Et, 끝 = İcra_Et + uzunluq_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Söz_SMS.length(); Loop_INDEX++) {
            int simvol_kodu = Söz_SMS.charAt(Loop_INDEX);
            if (simvol_kodu > 0 && simvol_kodu < 128) { if (읽는자리 >= 끝 || FAYL[읽는자리++] != simvol_kodu) return false; }
            else if (simvol_kodu < 2048) {
                if (읽는자리 + 2 > 끝 || FAYL[읽는자리++] != (192 | (simvol_kodu >> 6)) || FAYL[읽는자리++] != (128 | (simvol_kodu & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || FAYL[읽는자리++] != (224 | (simvol_kodu >> 12)) || FAYL[읽는자리++] != (128 | ((simvol_kodu >> 6) & 63)) || FAYL[읽는자리++] != (128 | (simvol_kodu & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Söz_SMS(int sabit_VALUE, String Söz_SMS) { return çek_sabit(sabit_VALUE, 1) && 구간(상가[sabit_VALUE], sabit_SECOND_VALUE[sabit_VALUE], Söz_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!çek_sabit(가, 1) || !çek_sabit(나, 1) || sabit_SECOND_VALUE[가] != sabit_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < sabit_SECOND_VALUE[가]; 수++) if (FAYL[상가[가] + 수] != FAYL[상가[나] + 수]) return false;
        return true;
    }
    static int Sinif_ad_SMS(int 수) { return çek_sabit(수, 7) && çek_sabit(상가[수], 1) ? 상가[수] : 0; }
    static int İstinad_ad(int 수) { return çek_sabit(수, 12) && çek_sabit(상가[수], 1) ? 상가[수] : 0; }
    static int İstinad_TYPE(int 수) { return çek_sabit(수, 12) && çek_sabit(sabit_SECOND_VALUE[수], 1) ? sabit_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean boş_TYPE) {
        if (읽기위치 >= 끝) { xəta_VALUE("invalid descriptor"); return 0; }
        int VALUE = bayt_VALUE();
        if (VALUE == 'V' && boş_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int İcra_Et = 읽기위치;
            while (읽기위치 < 끝 && FAYL[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == İcra_Et) xəta_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        xəta_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metod_TYPE[FUNCTION_VALUE];
        if (!çek_sabit(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + sabit_SECOND_VALUE[수];
        if (bayt_VALUE() != '(') xəta_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!XƏTA && 읽기위치 < 끝 && FAYL[읽기위치] != ')') {
            if (element_COUNT == 16) { xəta_VALUE("too many method arguments"); break; }
            metod_arqument_TYPE[FUNCTION_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bayt_VALUE() != ')') xəta_VALUE("invalid method descriptor");
        metod_geri_qaytarmaq[FUNCTION_VALUE] = 서술형(끝, true); metod_arqument_COUNT[FUNCTION_VALUE] = element_COUNT;
        if (읽기위치 != 끝) xəta_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metod_sahib[kadr_metod[kadr_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !XƏTA; 수++) { çek_sabit(상번호(), 1); 건너(tam_ədəd()); }
    }
    static int əmr_uzunluq(int VALUE) {
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
    static int yerinə_qoymaq_tam_ədəd(int 읽는자리) {
        if (!klip(읽는자리, 4)) { xəta_VALUE("truncated bytecode operand"); return 0; }
        return FAYL[읽는자리] << 24 | FAYL[읽는자리 + 1] << 16 | FAYL[읽는자리 + 2] << 8 | FAYL[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int İcra_Et, int 끝) {
        int VALUE = FAYL[읽는자리], uzunluq_VALUE = əmr_uzunluq(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_yerinə_qoymaq = 읽는자리 + 1;
            while ((BASE_yerinə_qoymaq - İcra_Et) % 4 != 0) BASE_yerinə_qoymaq++;
            if (끝 - BASE_yerinə_qoymaq < (VALUE == 170 ? 12 : 8)) return 0;
            int daxiletmə_COUNT = VALUE == 170 ? yerinə_qoymaq_tam_ədəd(BASE_yerinə_qoymaq + 8) - yerinə_qoymaq_tam_ədəd(BASE_yerinə_qoymaq + 4) + 1 : yerinə_qoymaq_tam_ədəd(BASE_yerinə_qoymaq + 4);
            if (daxiletmə_COUNT < 0 || daxiletmə_COUNT > 2048) return 0;
            uzunluq_VALUE = BASE_yerinə_qoymaq - 읽는자리 + (VALUE == 170 ? 12 + 4 * daxiletmə_COUNT : 8 + 8 * daxiletmə_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Söz_verilənlər = FAYL[읽는자리 + 1]; uzunluq_VALUE = Söz_verilənlər == 132 ? 6 : (Söz_verilənlər == 21 || Söz_verilənlər == 25 || Söz_verilənlər == 54 || Söz_verilənlər == 58) ? 4 : 0;
        }
        return uzunluq_VALUE > 0 && uzunluq_VALUE <= 끝 - 읽는자리 ? uzunluq_VALUE : 0;
    }
    static void çek_təyinat_VALUE(int təyinat_VALUE_a0fbc067, int FUNCTION_VALUE) {
        if (təyinat_VALUE_a0fbc067 < metod_Başla[FUNCTION_VALUE] || təyinat_VALUE_a0fbc067 >= metod_bitirmək[FUNCTION_VALUE] || 경계[təyinat_VALUE_a0fbc067] != FUNCTION_VALUE + 1) xəta_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Sinif_Tərif) {
        현재읽는종 = Sinif_Tərif; 읽기위치 = Sinif_Tərif * 16384; Böyüklük = 읽기위치 + Sinif_Tərif_ölçünü_dəyişmək[Sinif_Tərif];
        if (tam_ədəd() != 0xcafebabe) { xəta_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versiya_VALUE = 짧은수();
        if (versiya_VALUE < 45 || versiya_VALUE > 52 || 부판 != 0) { xəta_VALUE("supported class versions: 45..52, minor 0"); return; }
        int sabit_COUNT = 짧은수(), BASE_yerinə_qoymaq = Sinif_Tərif * 512;
        if (sabit_COUNT < 1 || sabit_COUNT > 512) { xəta_VALUE("constant pool limit (511)"); return; }
        for (int daxiletmə_COUNT = 1; daxiletmə_COUNT < sabit_COUNT && !XƏTA; daxiletmə_COUNT++) {
            int 수 = BASE_yerinə_qoymaq + daxiletmə_COUNT, 종류 = bayt_VALUE(); sabit_teq[수] = 종류;
            if (종류 == 1) { sabit_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(sabit_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = tam_ədəd();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); sabit_SECOND_VALUE[수] = 상번호(); }
            else xəta_VALUE("unsupported constant type");
        }
        int icazə_VALUE = 짧은수();
        if ((icazə_VALUE & (0x2000 | 0x4000)) != 0) xəta_VALUE("annotation/enum class unsupported");
        Sinif_Tərif_ad[Sinif_Tərif] = Sinif_ad_SMS(상번호());
        종부모[Sinif_Tərif] = Sinif_ad_SMS(상번호());
        int interfeys_COUNT = 짧은수(); if (interfeys_COUNT > 16) { xəta_VALUE("interface count limit"); return; }
        Sinif_interfeys_COUNT[Sinif_Tərif] = interfeys_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interfeys_COUNT; Loop_INDEX++) Sinif_interfeys[Sinif_Tərif * 16 + Loop_INDEX] = Sinif_ad_SMS(상번호());
        int sahə_COUNT = 짧은수();
        if (sahə_COUNT > 512 - slot_COUNT) { xəta_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < sahə_COUNT && !XƏTA; Loop_INDEX++) {
            int fayl_INDEX = slot_COUNT++; slot_sahib[fayl_INDEX] = Sinif_Tərif; slot_icazələr[fayl_INDEX] = 짧은수(); slot_ad[fayl_INDEX] = 상번호(); slot_TYPE[fayl_INDEX] = 상번호();
            çek_sabit(slot_ad[fayl_INDEX], 1); çek_sabit(slot_TYPE[fayl_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[slot_TYPE[fayl_INDEX]]; int sahə_kod = 서술형(읽기위치 + sabit_SECOND_VALUE[slot_TYPE[fayl_INDEX]], false); 읽기위치 = 보존값;
            if ((slot_icazələr[fayl_INDEX] & 8) == 0) slot_yerinə_qoymaq[fayl_INDEX] = Sinif_slot_COUNT[Sinif_Tərif]++;
            int atribut_verilənlər = 짧은수();
            for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < atribut_verilənlər && !XƏTA; daxili_qoşulma_yerinə_qoymaq++) {
                int ad_sabit = 상번호(), 유효길이 = tam_ədəd();
                if (Söz_SMS(ad_sabit, "ConstantValue") && 유효길이 == 2) {
                    int verilənlər_VALUE = 상번호();
                    if (sahə_kod == 1 && çek_sabit(verilənlər_VALUE, 3)) slot_verilənlər[fayl_INDEX] = 상가[verilənlər_VALUE];
                    else if (sahə_kod == 2 && çek_sabit(verilənlər_VALUE, 8)) slot_verilənlər[fayl_INDEX] = sabit_SMS(상가[verilənlər_VALUE]);
                } else 건너(유효길이);
            }
        }
        int element_COUNT = 짧은수();
        if (element_COUNT > 512 - metod_COUNT) { xəta_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < element_COUNT && !XƏTA; Loop_INDEX++) {
            int 수 = metod_COUNT++; metod_sahib[수] = Sinif_Tərif;
            metod_müraciət[수] = 짧은수(); metod_ad_SMS[수] = 상번호(); metod_TYPE[수] = 상번호();
            çek_sabit(metod_ad_SMS[수], 1); 서술읽기(수);
            if ((metod_müraciət[수] & 8) == 0) {
                if (metod_arqument_COUNT[수] == 16) { xəta_VALUE("too many instance method arguments"); return; }
                for (int Müqayisə_yerinə_qoymaq = metod_arqument_COUNT[수]; Müqayisə_yerinə_qoymaq > 0; Müqayisə_yerinə_qoymaq--) metod_arqument_TYPE[수 * 16 + Müqayisə_yerinə_qoymaq] = metod_arqument_TYPE[수 * 16 + Müqayisə_yerinə_qoymaq - 1];
                metod_arqument_TYPE[수 * 16] = 2; metod_arqument_COUNT[수]++;
            }
            if ((metod_müraciət[수] & 0x100) != 0) xəta_VALUE("user native method unsupported");
            if (Söz_SMS(metod_ad_SMS[수], "<clinit>")) ilkin_qiymət_vermək_Sinif_Tərif[Sinif_Tərif] = 수 + 1;
            for (int ön_VALUE = 0; ön_VALUE < 수; ön_VALUE++) if (metod_sahib[ön_VALUE] == Sinif_Tərif && 같은말(metod_ad_SMS[ön_VALUE], metod_ad_SMS[수]) && 같은말(metod_TYPE[ön_VALUE], metod_TYPE[수])) xəta_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !XƏTA; atribut_VALUE++) {
                int Ad = 상번호(), uzunluq_VALUE = tam_ədəd(), İcra_Et = 읽기위치;
                if (!klip(İcra_Et, uzunluq_VALUE)) { xəta_VALUE("truncated method attribute"); break; }
                if (Söz_SMS(Ad, "Code")) {
                    if (metod_Başla[수] != 0) xəta_VALUE("duplicate Code attribute");
                    metod_Yığın[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_uzunluq = tam_ədəd();
                    if (metod_Yığın[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metod_arqument_COUNT[수]
                        || kod_uzunluq < 1 || kod_uzunluq > 8192) xəta_VALUE("method memory limits exceeded");
                    metod_Başla[수] = 읽기위치; 건너(kod_uzunluq); metod_bitirmək[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { xəta_VALUE("exception table limit"); return; }
                    for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 잡는수; daxili_qoşulma_yerinə_qoymaq++) {
                        int səhv_İstinad = 잡기수++; 잡기함수[səhv_İstinad] = 수;
                        잡기시작[səhv_İstinad] = metod_Başla[수] + 짧은수(); 잡기끝[səhv_İstinad] = metod_Başla[수] + 짧은수();
                        잡기위치[səhv_İstinad] = metod_Başla[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[səhv_İstinad] = 부호값 == 0 ? 0 : Sinif_ad_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != İcra_Et + uzunluq_VALUE) xəta_VALUE("Code attribute size mismatch");
                } else 건너(uzunluq_VALUE);
            }
            if ((metod_müraciət[수] & 0x400) != 0) continue;
            if (metod_Başla[수] == 0) xəta_VALUE("missing Code attribute");
            int slot_daxiletmə = metod_Başla[수];
            while (slot_daxiletmə < metod_bitirmək[수] && !XƏTA) {
                int uzunluq_VALUE = 길이읽기(slot_daxiletmə, metod_Başla[수], metod_bitirmək[수]);
                if (uzunluq_VALUE == 0) { xəta_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_daxiletmə] = 수 + 1; slot_daxiletmə += uzunluq_VALUE;
            }
            slot_daxiletmə = metod_Başla[수];
            while (slot_daxiletmə < metod_bitirmək[수] && !XƏTA) {
                int VALUE = FAYL[slot_daxiletmə];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) çek_təyinat_VALUE(slot_daxiletmə + (short)(FAYL[slot_daxiletmə + 1] << 8 | FAYL[slot_daxiletmə + 2]), 수);
                if (VALUE == 200) çek_təyinat_VALUE(slot_daxiletmə + yerinə_qoymaq_tam_ədəd(slot_daxiletmə + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = slot_daxiletmə + 1; while ((읽는자리 - metod_Başla[수]) % 4 != 0) 읽는자리++;
                    çek_təyinat_VALUE(slot_daxiletmə + yerinə_qoymaq_tam_ədəd(읽는자리), 수);
                    int daxiletmə_COUNT = VALUE == 170 ? yerinə_qoymaq_tam_ədəd(읽는자리 + 8) - yerinə_qoymaq_tam_ədəd(읽는자리 + 4) + 1 : yerinə_qoymaq_tam_ədəd(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < daxiletmə_COUNT; daxili_qoşulma_yerinə_qoymaq++) çek_təyinat_VALUE(slot_daxiletmə + yerinə_qoymaq_tam_ədəd(읽는자리 + daxili_qoşulma_yerinə_qoymaq * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                slot_daxiletmə += 길이읽기(slot_daxiletmə, metod_Başla[수], metod_bitirmək[수]);
            }
            for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 잡기수; daxili_qoşulma_yerinə_qoymaq++) if (잡기함수[daxili_qoşulma_yerinə_qoymaq] == 수) {
                çek_təyinat_VALUE(잡기시작[daxili_qoşulma_yerinə_qoymaq], 수); çek_təyinat_VALUE(잡기위치[daxili_qoşulma_yerinə_qoymaq], 수);
                if (잡기끝[daxili_qoşulma_yerinə_qoymaq] != metod_bitirmək[수]) çek_təyinat_VALUE(잡기끝[daxili_qoşulma_yerinə_qoymaq], 수);
                if (잡기시작[daxili_qoşulma_yerinə_qoymaq] >= 잡기끝[daxili_qoşulma_yerinə_qoymaq]) xəta_VALUE("invalid exception range");
            }
        }
        if (!XƏTA) 속성건너();
        if (읽기위치 != Böyüklük) xəta_VALUE("extra class file data");
    }
    static int ayırmaq_Yaddaş(int 종류, int uzunluq_VALUE) { return 새기억(종류, uzunluq_VALUE); }
    static boolean obyekt_VALUE(int İstinad, int 종류) {
        if (!객체유효(İstinad)) return false;
        if (힙[İstinad] != 종류) { xəta_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int sabit_SMS(int INDEX) {
        if (!çek_sabit(INDEX, 1)) return 0;
        if (sətir_İstinad[INDEX] != 0) return sətir_İstinad[INDEX];
        int İstinad = ayırmaq_Yaddaş(1, sabit_SECOND_VALUE[INDEX]); if (XƏTA) return 0;
        int 끝 = 상가[INDEX] + sabit_SECOND_VALUE[INDEX], 수 = 상가[INDEX], uzunluq_VALUE = 0;
        while (수 < 끝 && !XƏTA) {
            int VALUE = FAYL[수++];
            if (VALUE == 0) xəta_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Sonrakı_element = FAYL[수++];
                if ((Sonrakı_element & 192) != 128) xəta_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Sonrakı_element & 63;
                if (VALUE != 0 && VALUE < 128) xəta_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = FAYL[수++], 나 = FAYL[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) xəta_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) xəta_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) xəta_VALUE("invalid modified UTF-8");
            힙[İstinad + 2 + uzunluq_VALUE++] = VALUE;
        }
        힙[İstinad + 1] = uzunluq_VALUE; sətir_İstinad[INDEX] = İstinad; return İstinad;
    }
    static int host_simvol(String VALUE) {
        int İstinad = ayırmaq_Yaddaş(1, VALUE.length()); if (XƏTA) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[İstinad + 2 + 수] = VALUE.charAt(수);
        return İstinad;
    }
    static void yazmaq_SMS(int İstinad) {
        if (İstinad == 0) { istifadəçi.Yazma("null"); return; }
        if (!obyekt_VALUE(İstinad, 1)) return;
        for (int 수 = 0; 수 < 힙[İstinad + 1]; 수++) istifadəçi.yazmaq_simvol_VALUE(힙[İstinad + 2 + 수]);
    }
    static int rəqəm_simvol(int VALUE) {
        int İstinad = ayırmaq_Yaddaş(1, 11); if (XƏTA) return 0;
        int uzunluq_VALUE = 0;
        if (VALUE < 0) 힙[İstinad + 2 + uzunluq_VALUE++] = '-'; else VALUE = -VALUE;
        int yerinə_qoymaq_INDEX = 1000000000; boolean İcra_Et = false;
        while (yerinə_qoymaq_INDEX != 0) {
            int 수 = -(VALUE / yerinə_qoymaq_INDEX);
            if (수 != 0 || İcra_Et || yerinə_qoymaq_INDEX == 1) { 힙[İstinad + 2 + uzunluq_VALUE++] = '0' + 수; İcra_Et = true; }
            VALUE %= yerinə_qoymaq_INDEX; yerinə_qoymaq_INDEX /= 10;
        }
        힙[İstinad + 1] = uzunluq_VALUE; return İstinad;
    }
    static int 정수해독(int İstinad) {
        if (!obyekt_VALUE(İstinad, 1)) return 0;
        int uzunluq_VALUE = 힙[İstinad + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (uzunluq_VALUE > 0 && (힙[İstinad + 2] == '-' || 힙[İstinad + 2] == '+')) { 음수 = 힙[İstinad + 2] == '-'; 수++; }
        if (수 == uzunluq_VALUE) xəta_VALUE("NumberFormatException");
        for (; 수 < uzunluq_VALUE && !XƏTA; 수++) {
            int rəqəm_VALUE = 힙[İstinad + 2 + 수] - '0';
            if (rəqəm_VALUE < 0 || rəqəm_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && rəqəm_VALUE > (음수 ? 8 : 7)) xəta_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - rəqəm_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (XƏTA) return;
        if (kadr_INDEX < 0 || kadr_Yığın[kadr_INDEX] >= metod_Yığın[kadr_metod[kadr_INDEX]]) { xəta_VALUE("operand stack overflow"); return; }
        int slot_daxiletmə = kadr_INDEX * 128 + kadr_Yığın[kadr_INDEX]++; 스택값[slot_daxiletmə] = VALUE; 스택형[slot_daxiletmə] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (XƏTA) return 0;
        if (kadr_INDEX < 0 || kadr_Yığın[kadr_INDEX] < 1) { xəta_VALUE("operand stack underflow"); return 0; }
        int slot_daxiletmə = kadr_INDEX * 128 + --kadr_Yığın[kadr_INDEX]; geri_qaytarmaq_TYPE = 스택형[slot_daxiletmə];
        if (TYPE_VALUE != 0 && geri_qaytarmaq_TYPE != TYPE_VALUE) xəta_VALUE("operand type mismatch");
        if (geri_qaytarmaq_TYPE == 2) qorumaq_VALUE(스택값[slot_daxiletmə]);
        return 스택값[slot_daxiletmə];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadr_metod[kadr_INDEX]] || INDEX < 0 || lokal_TYPE[kadr_INDEX * 128 + INDEX] != TYPE_VALUE) { xəta_VALUE("invalid or uninitialized local"); return; }
        넣기(lokal_VALUE[kadr_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void yazmaq_lokal(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadr_metod[kadr_INDEX]] || INDEX < 0) { xəta_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokal_VALUE[kadr_INDEX * 128 + INDEX] = VALUE; lokal_TYPE[kadr_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int yerinə_qoymaq = kadr_yerinə_qoymaq[kadr_INDEX];
        if (yerinə_qoymaq < metod_Başla[kadr_metod[kadr_INDEX]] || yerinə_qoymaq >= metod_bitirmək[kadr_metod[kadr_INDEX]]) { xəta_VALUE("instruction pointer out of range"); return 0; }
        kadr_yerinə_qoymaq[kadr_INDEX]++; return FAYL[yerinə_qoymaq];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void hərəkət_etdir_VALUE(int yerinə_qoymaq) {
        int FUNCTION_VALUE = kadr_metod[kadr_INDEX];
        if (yerinə_qoymaq < metod_Başla[FUNCTION_VALUE] || yerinə_qoymaq >= metod_bitirmək[FUNCTION_VALUE] || 경계[yerinə_qoymaq] != FUNCTION_VALUE + 1) xəta_VALUE("invalid branch target");
        else kadr_yerinə_qoymaq[kadr_INDEX] = yerinə_qoymaq;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadr_INDEX % 32 == 31) { xəta_VALUE("call stack limit (32)"); return; }
        int Sonrakı_element = kadr_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Sonrakı_element * 128 + 수] = 0;
        for (int 수 = metod_arqument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Sonrakı_element * 128 + 수] = 빼기(metod_arqument_TYPE[FUNCTION_VALUE * 16 + 수]); lokal_TYPE[Sonrakı_element * 128 + 수] = metod_arqument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (XƏTA) return;
        kadr_INDEX = Sonrakı_element; ilkin_qiymət_vermək_kadr[kadr_INDEX] = 0; kadr_metod[kadr_INDEX] = FUNCTION_VALUE; kadr_yerinə_qoymaq[kadr_INDEX] = metod_Başla[FUNCTION_VALUE]; kadr_Yığın[kadr_INDEX] = 0;
    }
    static void geri_qaytarmaq_ölçü(int TYPE_VALUE) {
        if (TYPE_VALUE != metod_geri_qaytarmaq[kadr_metod[kadr_INDEX]]) { xəta_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (ilkin_qiymət_vermək_kadr[kadr_INDEX] != 0) Sinif_Tərif_vəziyyət[ilkin_qiymət_vermək_kadr[kadr_INDEX] - 1] = 2;
        if (틀잠금[kadr_INDEX] != 0) { 잠금풀기(틀잠금[kadr_INDEX]); 틀잠금[kadr_INDEX] = 0; }
        kadr_INDEX--; if (kadr_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] axın_fayl_ad = new int[64];
    static void fayl_axın_CALL(int sahib_VALUE, int Ad, int format_VALUE, int Əmr) {
        boolean 출력 = Söz_SMS(sahib_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Əmr == 183 && Söz_SMS(Ad, "<init>")) {
            boolean 이어 = false;
            if (출력 && Söz_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Söz_SMS(format_VALUE, "(Ljava/lang/String;)V")) { xəta_VALUE("unsupported file stream constructor"); return; }
            int fayl_daxiletmə_ad = 빼기(2), axın_VALUE = 빼기(2);
            if (!obyekt_VALUE(fayl_daxiletmə_ad, 1) || !obyekt_VALUE(axın_VALUE, 종류) || XƏTA) return;
            if (힙[axın_VALUE + 3] != 0) { xəta_VALUE("file stream already initialized"); return; }
            int uzunluq_VALUE = 힙[fayl_daxiletmə_ad + 1];
            if (uzunluq_VALUE < 1 || uzunluq_VALUE > 63) { xəta_VALUE("invalid file name length"); return; }
            for (int slot_daxiletmə = 0; slot_daxiletmə < uzunluq_VALUE; slot_daxiletmə++) {
                int VALUE = 힙[fayl_daxiletmə_ad + 2 + slot_daxiletmə];
                if (VALUE < 1) { xəta_VALUE("invalid file stream path"); return; }
                axın_fayl_ad[slot_daxiletmə] = VALUE;
            }
            axın_fayl_ad[uzunluq_VALUE] = 0;
            int 서술자 = istifadəçi.파일서술자열기(axın_fayl_ad, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { xəta_VALUE("FileNotFoundException: file open failed"); return; }
            힙[axın_VALUE + 2] = 서술자; 힙[axın_VALUE + 3] = 1;
            return;
        }
        if (Əmr != 182) { xəta_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Söz_SMS(Ad, "write") || !출력 && Söz_SMS(Ad, "read"))
            && (Söz_SMS(format_VALUE, 출력 ? "([B)V" : "([B)I") || Söz_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean klip_VALUE = Söz_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int daxiletmə_COUNT = klip_VALUE ? 빼기(1) : 0, 시작점 = klip_VALUE ? 빼기(1) : 0, verilənlər_ARRAY = 빼기(2), obyekt_İstinad = 빼기(2);
            if (!obyekt_VALUE(verilənlər_ARRAY, 20) || !obyekt_VALUE(obyekt_İstinad, 종류)) return;
            if (!klip_VALUE) daxiletmə_COUNT = 힙[verilənlər_ARRAY + 1];
            if (시작점 < 0 || daxiletmə_COUNT < 0 || 시작점 > 힙[verilənlər_ARRAY + 1] - daxiletmə_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[obyekt_İstinad + 3] == 0 || 힙[obyekt_İstinad + 2] < 0) { xəta_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < daxiletmə_COUNT && !XƏTA) {
                int 반환값 = 출력 ? istifadəçi.파일한바이트쓰기(힙[obyekt_İstinad + 2], 힙[verilənlər_ARRAY + 2 + 시작점 + 완료수]) : istifadəçi.파일한바이트읽기(힙[obyekt_İstinad + 2]);
                if (반환값 < 0) { xəta_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[verilənlər_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(daxiletmə_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Söz_SMS(Ad, "flush") && Söz_SMS(format_VALUE, "()V")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 종류) && 힙[obyekt_İstinad + 2] < 0) xəta_VALUE("IOException: stream closed"); return; }
        int Gedişat = -1, VALUE = 0;
        if (Söz_SMS(Ad, "close") && Söz_SMS(format_VALUE, "()V")) Gedişat = 0;
        if (!출력 && Söz_SMS(Ad, "read") && Söz_SMS(format_VALUE, "()I")) Gedişat = 1;
        if (출력 && Söz_SMS(Ad, "write") && Söz_SMS(format_VALUE, "(I)V")) { Gedişat = 2; VALUE = 빼기(1); }
        if (Gedişat < 0) { xəta_VALUE("unsupported file stream method"); return; }
        int axın_VALUE = 빼기(2);
        if (!obyekt_VALUE(axın_VALUE, 종류) || XƏTA) return;
        if (힙[axın_VALUE + 3] == 0) { xəta_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[axın_VALUE + 2];
        if (Gedişat == 0) {
            if (서술자 >= 0 && istifadəçi.파일서술자닫기(서술자) < 0) xəta_VALUE("IOException: close failed");
            힙[axın_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { xəta_VALUE("IOException: stream closed"); return; }
        if (Gedişat == 1) {
            int ölçü = istifadəçi.파일한바이트읽기(서술자);
            if (ölçü < -1) xəta_VALUE("IOException: read failed"); else 넣기(ölçü == 256 ? -1 : ölçü, 1);
        } else if (istifadəçi.파일한바이트쓰기(서술자, VALUE) != 1) xəta_VALUE("IOException: write failed");
    }
    static void CALL_metod(int INDEX, int Əmr) {
        if (INDEX <= 0 || INDEX >= sabit_teq.length || (sabit_teq[INDEX] != 10 && sabit_teq[INDEX] != 11)) { xəta_VALUE("invalid method reference"); return; }
        int sahib_VALUE = Sinif_ad_SMS(상가[INDEX]), Ad = İstinad_ad(sabit_SECOND_VALUE[INDEX]), format_VALUE = İstinad_TYPE(sabit_SECOND_VALUE[INDEX]);
        if (XƏTA) return;
        if (기본호출(sahib_VALUE, Ad, format_VALUE, Əmr)) return;
        if (Söz_SMS(sahib_VALUE, "java/io/FileInputStream") || Söz_SMS(sahib_VALUE, "java/io/FileOutputStream")) {
            fayl_axın_CALL(sahib_VALUE, Ad, format_VALUE, Əmr); return;
        }
        if (Əmr == 184 && Söz_SMS(sahib_VALUE, "java/lang/Integer") && Söz_SMS(Ad, "parseInt") && Söz_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Əmr == 182 && Söz_SMS(sahib_VALUE, "java/io/PrintStream") && (Söz_SMS(Ad, "println") || Söz_SMS(Ad, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Söz_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Söz_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Söz_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Söz_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Söz_SMS(format_VALUE, "()V") || !Söz_SMS(Ad, "println")) xəta_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) xəta_VALUE("invalid PrintStream receiver");
            if (XƏTA) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) istifadəçi.Yazma(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) istifadəçi.yazmaq_simvol_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) yazmaq_SMS(VALUE);
            if (Söz_SMS(Ad, "println")) istifadəçi.yazmaq_simvol_VALUE(10);
            return;
        }
        if (Əmr == 182 && Söz_SMS(sahib_VALUE, "java/lang/String")) {
            if (Söz_SMS(Ad, "length") && Söz_SMS(format_VALUE, "()I")) {
                int İstinad = 빼기(2); if (obyekt_VALUE(İstinad, 1)) 넣기(힙[İstinad + 1], 1); return;
            }
            if (Söz_SMS(Ad, "charAt") && Söz_SMS(format_VALUE, "(I)C")) {
                int aşağı_indeks_VALUE = 빼기(1), İstinad = 빼기(2);
                if (obyekt_VALUE(İstinad, 1)) {
                    if (aşağı_indeks_VALUE < 0 || aşağı_indeks_VALUE >= 힙[İstinad + 1]) xəta_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[İstinad + 2 + aşağı_indeks_VALUE], 1);
                }
                return;
            }
        }
        if (Söz_SMS(sahib_VALUE, "java/lang/StringBuilder")) {
            if (Əmr == 183 && Söz_SMS(Ad, "<init>") && Söz_SMS(format_VALUE, "()V")) { obyekt_VALUE(빼기(2), 4); return; }
            if (Əmr == 182 && Söz_SMS(Ad, "toString") && Söz_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int İstinad = 빼기(2); if (obyekt_VALUE(İstinad, 4)) 넣기(힙[İstinad + 2] == 0 ? host_simvol("") : 힙[İstinad + 2], 2); return;
            }
            if (Əmr == 182 && Söz_SMS(Ad, "append")) {
                int Mətn = 0;
                if (Söz_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) Mətn = rəqəm_simvol(빼기(1));
                else if (Söz_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) Mətn = host_simvol(빼기(1) == 0 ? "false" : "true");
                else if (Söz_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Mətn = ayırmaq_Yaddaş(1, 1); if (!XƏTA) 힙[Mətn + 2] = VALUE & 65535;
                }
                else if (Söz_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Mətn = 빼기(2); if (Mətn == 0) Mətn = host_simvol("null"); }
                else { xəta_VALUE("unsupported StringBuilder append"); return; }
                int İstinad = 빼기(2); if (!obyekt_VALUE(İstinad, 4) || !obyekt_VALUE(Mətn, 1)) return;
                int ön_VALUE = 힙[İstinad + 2], ön_VALUE_uzunluq = ön_VALUE == 0 ? 0 : 힙[ön_VALUE + 1], GERİ_VALUE_uzunluq = 힙[Mətn + 1];
                int 새글 = ayırmaq_Yaddaş(1, ön_VALUE_uzunluq + GERİ_VALUE_uzunluq); if (XƏTA) return;
                for (int 수 = 0; 수 < ön_VALUE_uzunluq; 수++) 힙[새글 + 2 + 수] = 힙[ön_VALUE + 2 + 수];
                for (int 수 = 0; 수 < GERİ_VALUE_uzunluq; 수++) 힙[새글 + 2 + ön_VALUE_uzunluq + 수] = 힙[Mətn + 2 + 수];
                힙[İstinad + 2] = 새글; 넣기(İstinad, 2); return;
            }
        }
        int Sinif_Tərif = FIND_Sinif_Tərif(sahib_VALUE); if (Sinif_Tərif < 0 || XƏTA) return;
        int fayl_INDEX = FIND_metod(Sinif_Tərif, Ad, format_VALUE);
        if (fayl_INDEX < 0) {
            for (int simvol_kodu = Sinif_Tərif, daxiletmə_COUNT = 0; simvol_kodu >= 0 && daxiletmə_COUNT < 16; daxiletmə_COUNT++, simvol_kodu = 부모종(simvol_kodu))
                if (Söz_SMS(종부모[simvol_kodu], "java/lang/Thread")) { 가닥호출(Ad, format_VALUE, Əmr); return; }
            xəta_VALUE("NoSuchMethodError"); return;
        }
        if (((metod_müraciət[fayl_INDEX] & 8) != 0) != (Əmr == 184)) { xəta_VALUE("method static/instance mismatch"); return; }
        if (Əmr == 184) { if (!ilkin_qiymət_vermək(metod_sahib[fayl_INDEX], kadr_təlimat[kadr_INDEX])) return; }
        else {
            int 읽는자리 = kadr_Yığın[kadr_INDEX] - metod_arqument_COUNT[fayl_INDEX];
            if (읽는자리 < 0 || 스택형[kadr_INDEX * 128 + 읽는자리] != 2) { xəta_VALUE("invalid method receiver"); return; }
            int obyekt_İstinad = 스택값[kadr_INDEX * 128 + 읽는자리];
            if (!객체유효(obyekt_İstinad)) return;
            if (힙[obyekt_İstinad] < 32 || !종포함(힙[obyekt_İstinad] - 32, sahib_VALUE)) { xəta_VALUE("method receiver type mismatch"); return; }
            if (Əmr != 183) fayl_INDEX = FIND_metod(힙[obyekt_İstinad] - 32, Ad, format_VALUE);
        }
        if (fayl_INDEX < 0 || (metod_müraciət[fayl_INDEX] & 0x400) != 0) { xəta_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((metod_müraciət[fayl_INDEX] & 32) != 0) {
            if (Əmr == 184) { int simvol_kodu = metod_sahib[fayl_INDEX]; if (종잠금[simvol_kodu] == 0) 종잠금[simvol_kodu] = ayırmaq_Yaddaş(8, 0); 잠금참조 = 종잠금[simvol_kodu]; }
            else 잠금참조 = 스택값[kadr_INDEX * 128 + kadr_Yığın[kadr_INDEX] - metod_arqument_COUNT[fayl_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!XƏTA) kadr_yerinə_qoymaq[kadr_INDEX] = kadr_təlimat[kadr_INDEX]; return; }
        }
        호출(fayl_INDEX); if (!XƏTA) 틀잠금[kadr_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_İstinad, int verilənlər_VALUE) {
        if (verilənlər_VALUE == 0 || ARRAY_element[ARRAY_İstinad] == 0) return true;
        boolean 성공여부 = ARRAY_element[ARRAY_İstinad] == -1 ? (verilənlər_VALUE > 0 && verilənlər_VALUE < 힙끝 && 힙[verilənlər_VALUE] == 1) : 맞는객체(verilənlər_VALUE, ARRAY_element[ARRAY_İstinad]);
        if (!성공여부 && !XƏTA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_slot(int İstinad, int aşağı_indeks_VALUE, int TYPE_VALUE) {
        if (!obyekt_VALUE(İstinad, TYPE_VALUE)) return 0;
        if (aşağı_indeks_VALUE < 0 || aşağı_indeks_VALUE >= 힙[İstinad + 1]) { xəta_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return İstinad + 2 + aşağı_indeks_VALUE;
    }
    static void icra_etmək_əmr() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (XƏTA) { if (던진객체 != 0) tutacaq_istisna(); if (XƏTA || kadr_INDEX < 현재가닥 * 32) break; }
            if (kadr_INDEX < 현재가닥 * 32 || dəyişdirmək_HTTP_sorğusu || --조각 == 0) { if (!SWITCH_axın()) break; 조각 = 100; }
            if (kadr_INDEX == 0 && Sinif_Tərif_vəziyyət[daxiletmə_Sinif_Tərif] != 2 && !ilkin_qiymət_vermək(daxiletmə_Sinif_Tərif, kadr_yerinə_qoymaq[kadr_INDEX])) continue;
            if (kadr_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (metod_müraciət[kadr_metod[kadr_INDEX]] & 32) != 0 && 틀잠금[kadr_INDEX] == 0) {
                int obyekt_İstinad = axın_hədəf[현재가닥]; if (!잠금얻기(obyekt_İstinad)) { if (XƏTA) break; continue; } 틀잠금[kadr_INDEX] = obyekt_İstinad;
            }
            잠시수 = 0;
            if (--남음 == 0) { xəta_VALUE("instruction limit (500000)"); break; }
            int İcra_Et = kadr_yerinə_qoymaq[kadr_INDEX]; kadr_təlimat[kadr_INDEX] = İcra_Et; int VALUE = 명바();
            if (XƏTA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metod_sahib[kadr_metod[kadr_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= sabit_teq.length) xəta_VALUE("invalid ldc constant");
                else if (sabit_teq[수] == 3) 넣기(상가[수], 1);
                else if (sabit_teq[수] == 8) 넣기(sabit_SMS(상가[수]), 2);
                else xəta_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { yazmaq_lokal(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { yazmaq_lokal(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { yazmaq_lokal(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int daxiletmə_yerinə_qoymaq = 빼기(1), obyekt_İstinad = 빼기(2), sahə_kod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && obyekt_İstinad > 0 && obyekt_İstinad < 힙끝 && 힙[obyekt_İstinad] == 21) sahə_kod = 21;
                int 읽는자리 = ARRAY_slot(obyekt_İstinad, daxiletmə_yerinə_qoymaq, sahə_kod); if (!XƏTA) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int daxiletmə_İstinad = 빼기(VALUE == 83 ? 2 : 1), daxiletmə_yerinə_qoymaq = 빼기(1), obyekt_İstinad = 빼기(2), sahə_kod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && obyekt_İstinad > 0 && obyekt_İstinad < 힙끝 && 힙[obyekt_İstinad] == 21) sahə_kod = 21;
                int 읽는자리 = ARRAY_slot(obyekt_İstinad, daxiletmə_yerinə_qoymaq, sahə_kod);
                if (!XƏTA && sahə_kod == 3 && !배열저장가능(obyekt_İstinad, daxiletmə_İstinad)) continue;
                if (!XƏTA) 힙[읽는자리] = sahə_kod == 20 ? (byte)daxiletmə_İstinad : sahə_kod == 21 ? daxiletmə_İstinad & 1 : sahə_kod == 22 ? (char)daxiletmə_İstinad : sahə_kod == 23 ? (short)daxiletmə_İstinad : daxiletmə_İstinad;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Yığın_təlimat(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), ölçü = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { xəta_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) ölçü = 가 + 나;
                if (VALUE == 100) ölçü = 가 - 나;
                if (VALUE == 104) ölçü = 가 * 나;
                if (VALUE == 108) ölçü = 가 / 나;
                if (VALUE == 112) ölçü = 가 % 나;
                if (VALUE == 120) ölçü = 가 << 나;
                if (VALUE == 122) ölçü = 가 >> 나;
                if (VALUE == 124) ölçü = 가 >>> 나;
                if (VALUE == 126) ölçü = 가 & 나;
                if (VALUE == 128) ölçü = 가 | 나;
                if (VALUE == 130) ölçü = 가 ^ 나;
                넣기(ölçü, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokal_miqyas = 명바(), 증분 = (byte)명바(); 지역읽기(lokal_miqyas, 1); 넣기(빼기(1) + 증분, 1); yazmaq_lokal(lokal_miqyas, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int təyinat_VALUE_a0fbc067 = İcra_Et + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) hərəkət_etdir_VALUE(təyinat_VALUE_a0fbc067); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { geri_qaytarmaq_ölçü(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, İcra_Et); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { xəta_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metod(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(Sinif_ad_SMS(명상수()), İcra_Et); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int sahə_kod = 3, komponent = 0;
                if (VALUE == 188) { int 임시값 = 명바(); sahə_kod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = Sinif_ad_SMS(명상수());
                if (sahə_kod == 0) { xəta_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), obyekt_İstinad = ayırmaq_Yaddaş(sahə_kod, 유효길이); if (!XƏTA) ARRAY_element[obyekt_İstinad] = komponent; 넣기(obyekt_İstinad, 2); continue;
            }
            if (VALUE == 190) {
                int obyekt_İstinad = 빼기(2);
                if (객체유효(obyekt_İstinad)) { int Müqayisə_yerinə_qoymaq = 힙[obyekt_İstinad]; if (Müqayisə_yerinə_qoymaq != 2 && Müqayisə_yerinə_qoymaq != 3 && (Müqayisə_yerinə_qoymaq < 20 || Müqayisə_yerinə_qoymaq > 23)) xəta_VALUE("not an array"); else 넣기(힙[obyekt_İstinad + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int obyekt_İstinad = 빼기(2); if (객체유효(obyekt_İstinad)) { if (힙[obyekt_İstinad] != 9) xəta_VALUE("athrow requires supported Throwable"); else { 던진객체 = obyekt_İstinad; XƏTA = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int ad_sabit = Sinif_ad_SMS(명상수()), obyekt_İstinad = 빼기(2); boolean MATCH = 맞는객체(obyekt_İstinad, ad_sabit);
                if (VALUE == 193) 넣기(obyekt_İstinad != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !XƏTA) xəta_VALUE("ClassCastException"); 넣기(obyekt_İstinad, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = İcra_Et + 1, fayl_INDEX = kadr_metod[kadr_INDEX], Açar_İstinad = 빼기(1);
                while ((읽는자리 - metod_Başla[fayl_INDEX]) % 4 != 0) 읽는자리++;
                int hədəf_ünvan = yerinə_qoymaq_tam_ədəd(읽는자리);
                if (VALUE == 170) { int 낮은값 = yerinə_qoymaq_tam_ədəd(읽는자리 + 4), 높은값 = yerinə_qoymaq_tam_ədəd(읽는자리 + 8); if (Açar_İstinad >= 낮은값 && Açar_İstinad <= 높은값) hədəf_ünvan = yerinə_qoymaq_tam_ədəd(읽는자리 + 12 + (Açar_İstinad - 낮은값) * 4); }
                else { int 총수 = yerinə_qoymaq_tam_ədəd(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (yerinə_qoymaq_tam_ədəd(읽는자리 + 8 + Loop_INDEX * 8) == Açar_İstinad) hədəf_ünvan = yerinə_qoymaq_tam_ədəd(읽는자리 + 12 + Loop_INDEX * 8); }
                hərəkət_etdir_VALUE(İcra_Et + hədəf_ünvan); continue;
            }
            if (VALUE == 200) { hərəkət_etdir_VALUE(İcra_Et + yerinə_qoymaq_tam_ədəd(İcra_Et + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int obyekt_İstinad = 빼기(2);
                if (VALUE == 195) 잠금풀기(obyekt_İstinad);
                else if (!잠금얻기(obyekt_İstinad) && !XƏTA) { 넣기(obyekt_İstinad, 2); kadr_yerinə_qoymaq[kadr_INDEX] = İcra_Et; }
                continue;
            }
            if (VALUE == 196) {
                int əmr_kod = 명바(), daxiletmə_yerinə_qoymaq = 명짧();
                if (əmr_kod == 21 || əmr_kod == 25) 지역읽기(daxiletmə_yerinə_qoymaq, əmr_kod == 21 ? 1 : 2);
                else if (əmr_kod == 54 || əmr_kod == 58) yazmaq_lokal(daxiletmə_yerinə_qoymaq, əmr_kod == 54 ? 1 : 2);
                else if (əmr_kod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(daxiletmə_yerinə_qoymaq, 1); 넣기(빼기(1) + DELTA_VALUE, 1); yazmaq_lokal(daxiletmə_yerinə_qoymaq, 1); }
                else xəta_VALUE("unsupported wide opcode");
                continue;
            }
            xəta_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Sinif_Tərif(int Ad) {
        for (int Loop_INDEX = 0; Loop_INDEX < Sinif_Tərif_COUNT; Loop_INDEX++) if (Sinif_Tərif_ad[Loop_INDEX] != 0 && 같은말(Sinif_Tərif_ad[Loop_INDEX], Ad)) return Loop_INDEX;
        return yüklə_Sinif_Tərif(sabit_SMS(Ad));
    }
    static int yüklə_Sinif_Tərif(int ad_sətir) {
        if (!obyekt_VALUE(ad_sətir, 1)) return -1;
        int uzunluq_VALUE = 힙[ad_sətir + 1];
        if (uzunluq_VALUE < 1 || uzunluq_VALUE > 505 || Sinif_Tərif_COUNT == 16) { xəta_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < uzunluq_VALUE; Loop_INDEX++) { int simvol_kodu = 힙[ad_sətir + 2 + Loop_INDEX]; fayl_ad_SMS[Loop_INDEX] = simvol_kodu == '/' ? '.' : simvol_kodu; }
        fayl_ad_SMS[uzunluq_VALUE] = '.'; fayl_ad_SMS[uzunluq_VALUE + 1] = 'c'; fayl_ad_SMS[uzunluq_VALUE + 2] = 'l'; fayl_ad_SMS[uzunluq_VALUE + 3] = 'a'; fayl_ad_SMS[uzunluq_VALUE + 4] = 's'; fayl_ad_SMS[uzunluq_VALUE + 5] = 's'; fayl_ad_SMS[uzunluq_VALUE + 6] = 0;
        int Böyüklük = istifadəçi.파일읽기(fayl_ad_SMS, 임시파일);
        if (Böyüklük < 0) { xəta_VALUE("ClassNotFoundException"); return -1; }
        int Sinif_Tərif = Sinif_Tərif_COUNT++; Sinif_Tərif_ölçünü_dəyişmək[Sinif_Tərif] = Böyüklük;
        for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) FAYL[Sinif_Tərif * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(Sinif_Tərif); if (XƏTA) return -1;
        int faktiki_verilənlər = sabit_SMS(Sinif_Tərif_ad[Sinif_Tərif]);
        if (!글같음(faktiki_verilənlər, ad_sətir, true)) { xəta_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[Sinif_Tərif];
        if (부모 != 0 && !Söz_SMS(부모, "java/lang/Object") && !Söz_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Sinif_Tərif(부모);
            if (XƏTA || 위 < 0) return -1;
            int 읽는자리 = 위, səhnə_COUNT = 0;
            while (읽는자리 >= 0 && səhnə_COUNT++ < 16) {
                if (읽는자리 == Sinif_Tərif) { xəta_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = Sinif_slot_COUNT[위];
            for (int fayl_INDEX = 0; fayl_INDEX < slot_COUNT; fayl_INDEX++) if (slot_sahib[fayl_INDEX] == Sinif_Tərif && (slot_icazələr[fayl_INDEX] & 8) == 0) slot_yerinə_qoymaq[fayl_INDEX] += 시작변위;
            Sinif_slot_COUNT[Sinif_Tərif] += 시작변위;
        }
        return Sinif_Tərif;
    }
    static int 부모종(int Sinif_Tərif) {
        int Ad = 종부모[Sinif_Tərif];
        for (int Loop_INDEX = 0; Loop_INDEX < Sinif_Tərif_COUNT; Loop_INDEX++) if (Ad != 0 && Sinif_Tərif_ad[Loop_INDEX] != 0 && 같은말(Sinif_Tərif_ad[Loop_INDEX], Ad)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metod(int Sinif_Tərif, int Ad, int format_VALUE) {
        for (int 깊이 = 0; Sinif_Tərif >= 0 && 깊이 < 16; 깊이++, Sinif_Tərif = 부모종(Sinif_Tərif)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metod_COUNT; Loop_INDEX++) if (metod_sahib[Loop_INDEX] == Sinif_Tərif && 같은말(metod_ad_SMS[Loop_INDEX], Ad) && 같은말(metod_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int ad_metod(int Sinif_Tərif, String Ad, String format_VALUE) {
        for (int 깊이 = 0; Sinif_Tərif >= 0 && 깊이 < 16; 깊이++, Sinif_Tərif = 부모종(Sinif_Tərif))
            for (int Loop_INDEX = 0; Loop_INDEX < metod_COUNT; Loop_INDEX++) if (metod_sahib[Loop_INDEX] == Sinif_Tərif && Söz_SMS(metod_ad_SMS[Loop_INDEX], Ad) && Söz_SMS(metod_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Ad) { return FAYL[상가[Ad]] == 'L' || FAYL[상가[Ad]] == '[' ? 2 : 1; }
    static boolean ilkin_qiymət_vermək(int Sinif_Tərif, int əmr_Başla) {
        if (Sinif_Tərif < 0 || XƏTA) return false;
        if (Sinif_Tərif_vəziyyət[Sinif_Tərif] == 3) { xəta_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Sinif_Tərif_vəziyyət[Sinif_Tərif] == 1 && Sinif_axın[Sinif_Tərif] != 현재가닥) { kadr_yerinə_qoymaq[kadr_INDEX] = əmr_Başla; dəyişdirmək_HTTP_sorğusu = true; return false; }
        if (Sinif_Tərif_vəziyyət[Sinif_Tərif] != 0) return true;
        int 위 = 부모종(Sinif_Tərif);
        if (위 >= 0 && !ilkin_qiymət_vermək(위, əmr_Başla)) return false;
        Sinif_Tərif_vəziyyət[Sinif_Tərif] = 1; Sinif_axın[Sinif_Tərif] = 현재가닥;
        if (ilkin_qiymət_vermək_Sinif_Tərif[Sinif_Tərif] != 0) {
            kadr_yerinə_qoymaq[kadr_INDEX] = əmr_Başla;
            호출(ilkin_qiymət_vermək_Sinif_Tərif[Sinif_Tərif] - 1); if (!XƏTA) ilkin_qiymət_vermək_kadr[kadr_INDEX] = Sinif_Tərif + 1;
            return false;
        }
        Sinif_Tərif_vəziyyət[Sinif_Tərif] = 2; return true;
    }
    static void 필드호출(int INDEX, int Əmr, int İcra_Et) {
        if (!çek_sabit(INDEX, 9)) return;
        int sahib_VALUE = Sinif_ad_SMS(상가[INDEX]), Ad = İstinad_ad(sabit_SECOND_VALUE[INDEX]), format_VALUE = İstinad_TYPE(sabit_SECOND_VALUE[INDEX]);
        if (Söz_SMS(sahib_VALUE, "java/lang/System") && (Söz_SMS(Ad, "out") || Söz_SMS(Ad, "err")) && Söz_SMS(format_VALUE, "Ljava/io/PrintStream;") && Əmr == 178) { 넣기(-1, 2); return; }
        int Sinif_Tərif = FIND_Sinif_Tərif(sahib_VALUE); if (Sinif_Tərif < 0 || XƏTA) return;
        int 찾음 = -1;
        for (int 읽는자리 = Sinif_Tərif, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int fayl_INDEX = 0; fayl_INDEX < slot_COUNT; fayl_INDEX++) if (slot_sahib[fayl_INDEX] == 읽는자리 && 같은말(slot_ad[fayl_INDEX], Ad) && 같은말(slot_TYPE[fayl_INDEX], format_VALUE)) 찾음 = fayl_INDEX;
        if (찾음 < 0) { xəta_VALUE("NoSuchFieldError"); return; }
        boolean statik_VALUE = Əmr == 178 || Əmr == 179;
        if (statik_VALUE != ((slot_icazələr[찾음] & 8) != 0)) { xəta_VALUE("field static/instance mismatch"); return; }
        if (statik_VALUE && !ilkin_qiymət_vermək(slot_sahib[찾음], İcra_Et)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (Əmr == 179 || Əmr == 181) VALUE = 빼기(TYPE_VALUE);
        if (statik_VALUE) { if (Əmr == 178) 넣기(slot_verilənlər[찾음], TYPE_VALUE); else if (!XƏTA) slot_verilənlər[찾음] = VALUE; return; }
        int obyekt_İstinad = 빼기(2);
        if (!객체유효(obyekt_İstinad)) return;
        if (힙[obyekt_İstinad] < 32 || !종포함(힙[obyekt_İstinad] - 32, sahib_VALUE)) { xəta_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = obyekt_İstinad + 2 + slot_yerinə_qoymaq[찾음];
        if (Əmr == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!XƏTA) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Sinif_Tərif, int Ad) {
        for (int 중첩깊이 = 0; Sinif_Tərif >= 0 && 중첩깊이 < 16; 중첩깊이++, Sinif_Tərif = 부모종(Sinif_Tərif)) {
            if (같은말(Sinif_Tərif_ad[Sinif_Tərif], Ad) || (종부모[Sinif_Tərif] != 0 && 같은말(종부모[Sinif_Tərif], Ad))) return true;
            for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < Sinif_interfeys_COUNT[Sinif_Tərif]; daxili_qoşulma_yerinə_qoymaq++) if (같은말(Sinif_interfeys[Sinif_Tərif * 16 + daxili_qoşulma_yerinə_qoymaq], Ad)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bayt_verilənlər, boolean Cığır) {
        if (첫값 == bayt_verilənlər) return true;
        if (첫값 <= 0 || bayt_verilənlər <= 0 || 힙[첫값] != 1 || 힙[bayt_verilənlər] != 1 || 힙[첫값 + 1] != 힙[bayt_verilənlər + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int x_koordinatı = 힙[첫값 + 2 + Loop_INDEX], Y_koordinat = 힙[bayt_verilənlər + 2 + Loop_INDEX];
            if (Cığır) { if (x_koordinatı == '.') x_koordinatı = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (x_koordinatı != Y_koordinat) return false;
        }
        return true;
    }
    static boolean 객체유효(int obyekt_İstinad) {
        if (obyekt_İstinad == 0) { xəta_VALUE("NullPointerException"); return false; }
        if (obyekt_İstinad < 1 || obyekt_İstinad >= 힙끝 || 힙폭[obyekt_İstinad] < 2 || 힙[obyekt_İstinad] == 0) { xəta_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void qorumaq_VALUE(int obyekt_İstinad) {
        if (obyekt_İstinad > 0 && obyekt_İstinad < 힙끝 && 힙폭[obyekt_İstinad] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = obyekt_İstinad;
    }
    static void göstərmək_VALUE(int obyekt_İstinad) {
        if (obyekt_İstinad > 0 && obyekt_İstinad < 힙끝 && 힙폭[obyekt_İstinad] >= 2 && 힙[obyekt_İstinad] != 0 && 힙표시[obyekt_İstinad] == 0) {
            힙표시[obyekt_İstinad] = 1; 표시대기[displey_COUNT++] = obyekt_İstinad;
        }
    }
    static void 수거() {
        displey_COUNT = 0; toplu_COUNT++;
        for (int çek_yerinə_qoymaq = 1; çek_yerinə_qoymaq < 힙끝; çek_yerinə_qoymaq += 힙폭[çek_yerinə_qoymaq]) 힙표시[çek_yerinə_qoymaq] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < sətir_İstinad.length; Loop_INDEX++) göstərmək_VALUE(sətir_İstinad[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < slot_COUNT; Loop_INDEX++) if ((slot_icazələr[Loop_INDEX] & 8) != 0 && 형종류(slot_TYPE[Loop_INDEX]) == 2) göstərmək_VALUE(slot_verilənlər[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < axın_COUNT; 임시값++) {
            göstərmək_VALUE(axın_obyekt[임시값]); göstərmək_VALUE(axın_hədəf[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? kadr_INDEX : axın_kadr[임시값];
            for (int fayl_INDEX = 임시값 * 32; fayl_INDEX <= 꼭대기자리; fayl_INDEX++) {
                for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 함수지역[kadr_metod[fayl_INDEX]]; daxili_qoşulma_yerinə_qoymaq++) if (lokal_TYPE[fayl_INDEX * 128 + daxili_qoşulma_yerinə_qoymaq] == 2) göstərmək_VALUE(lokal_VALUE[fayl_INDEX * 128 + daxili_qoşulma_yerinə_qoymaq]);
                for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < kadr_Yığın[fayl_INDEX]; daxili_qoşulma_yerinə_qoymaq++) if (스택형[fayl_INDEX * 128 + daxili_qoşulma_yerinə_qoymaq] == 2) göstərmək_VALUE(스택값[fayl_INDEX * 128 + daxili_qoşulma_yerinə_qoymaq]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) göstərmək_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) göstərmək_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_tam_ədəd.length; Loop_INDEX++) göstərmək_VALUE(Store_tam_ədəd[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Sinif_Tərif_COUNT; Loop_INDEX++) göstərmək_VALUE(종잠금[Loop_INDEX]);
        for (int çek_yerinə_qoymaq = 1; çek_yerinə_qoymaq < 힙끝; çek_yerinə_qoymaq += 힙폭[çek_yerinə_qoymaq]) if (잠금깊이[çek_yerinə_qoymaq] > 0) göstərmək_VALUE(çek_yerinə_qoymaq);
        göstərmək_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) göstərmək_VALUE(잠시참조[Loop_INDEX]);
        while (displey_COUNT > 0) {
            int obyekt_İstinad = 표시대기[--displey_COUNT], sahə_kod = 힙[obyekt_İstinad];
            for (int Loop_INDEX = obyekt_İstinad + 2; Loop_INDEX < obyekt_İstinad + 힙폭[obyekt_İstinad]; Loop_INDEX++) if (sahə_kod == 3 || sahə_kod == 4 || 힙참조[Loop_INDEX] != 0) göstərmək_VALUE(힙[Loop_INDEX]);
        }
        for (int çek_yerinə_qoymaq = 1; çek_yerinə_qoymaq < 힙끝; çek_yerinə_qoymaq += 힙폭[çek_yerinə_qoymaq]) if (힙표시[çek_yerinə_qoymaq] == 0) 힙[çek_yerinə_qoymaq] = 0;
        for (int çek_yerinə_qoymaq = 1; çek_yerinə_qoymaq < 힙끝; çek_yerinə_qoymaq += 힙폭[çek_yerinə_qoymaq]) if (힙[çek_yerinə_qoymaq] == 0) {
            while (çek_yerinə_qoymaq + 힙폭[çek_yerinə_qoymaq] < 힙끝 && 힙[çek_yerinə_qoymaq + 힙폭[çek_yerinə_qoymaq]] == 0) { int Sonrakı_yerinə_qoymaq = çek_yerinə_qoymaq + 힙폭[çek_yerinə_qoymaq]; 힙폭[çek_yerinə_qoymaq] += 힙폭[Sonrakı_yerinə_qoymaq]; 힙폭[Sonrakı_yerinə_qoymaq] = 0; }
            if (çek_yerinə_qoymaq + 힙폭[çek_yerinə_qoymaq] == 힙끝) { 힙끝 = çek_yerinə_qoymaq; break; }
        }
    }
    static int 새기억(int 종류, int uzunluq_VALUE) {
        if (uzunluq_VALUE < 0) { xəta_VALUE("NegativeArraySizeException"); return 0; }
        if (uzunluq_VALUE > 힙.length - 3) { xəta_VALUE("object heap exhausted"); return 0; }
        int 필요수 = uzunluq_VALUE + 2, obyekt_İstinad = 0;
        if (필요수 <= 힙.length - 힙끝) { obyekt_İstinad = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { obyekt_İstinad = 읽는자리; break; }
            if (obyekt_İstinad != 0) {
                int 남은길이 = 힙폭[obyekt_İstinad] - 필요수;
                if (남은길이 >= 2) { 힙폭[obyekt_İstinad + 필요수] = 남은길이; 힙[obyekt_İstinad + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { obyekt_İstinad = 힙끝; 힙끝 += 필요수; }
        }
        if (obyekt_İstinad == 0) { xəta_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[obyekt_İstinad + Loop_INDEX] = 0; 힙참조[obyekt_İstinad + Loop_INDEX] = 0; 힙폭[obyekt_İstinad + Loop_INDEX] = 0; }
        ARRAY_element[obyekt_İstinad] = 0;
        힙폭[obyekt_İstinad] = 필요수; 힙[obyekt_İstinad] = 종류; 힙[obyekt_İstinad + 1] = uzunluq_VALUE; qorumaq_VALUE(obyekt_İstinad); return obyekt_İstinad;
    }
    static int istisna_Sinif(String ad_sabit) {
        if (자바도구.같음(ad_sabit, "java/lang/Throwable")) return 1;
        if (자바도구.같음(ad_sabit, "java/lang/Exception")) return 2;
        if (자바도구.같음(ad_sabit, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(ad_sabit, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(ad_sabit, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(ad_sabit, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(ad_sabit, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(ad_sabit, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(ad_sabit, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(ad_sabit, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(ad_sabit, "java/io/IOException")) return 11;
        if (자바도구.같음(ad_sabit, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(ad_sabit, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(ad_sabit, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(ad_sabit, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int istisna_sabit(int Ad) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Söz_SMS(Ad, istisna_ad(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String istisna_ad(int hesab_VALUE) {
        if (hesab_VALUE == 40) return "java/lang/InterruptedException";
        if (hesab_VALUE == 41) return "한국어/자체/대기중단예외";
        if (hesab_VALUE == 39) return "java/net/SocketException";
        if (hesab_VALUE == 20) return "한국어/자체/istisna";
        if (hesab_VALUE == 21) return "한국어/자체/실행예외";
        if (hesab_VALUE == 22) return "한국어/자체/giriş_çıxış_istisna";
        if (hesab_VALUE == 23) return "한국어/자체/gözlə_FASİLƏ_istisna";
        if (hesab_VALUE == 24) return "한국어/자체/ünvan_LOOKUP_istisna";
        if (hesab_VALUE == 25) return "한국어/자체/파일없음예외";
        if (hesab_VALUE == 26) return "한국어/자체/통신예외";
        if (hesab_VALUE == 27) return "한국어/자체/yanlış_arqument_istisna";
        if (hesab_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (hesab_VALUE == 29) return "한국어/자체/범위예외";
        if (hesab_VALUE == 30) return "한국어/자체/배열범위예외";
        if (hesab_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (hesab_VALUE == 32) return "한국어/자체/NULL_İstinad_istisna";
        if (hesab_VALUE == 33) return "한국어/자체/산술예외";
        if (hesab_VALUE == 34) return "한국어/자체/vəziyyət_istisna";
        if (hesab_VALUE == 35) return "한국어/자체/TYPE_Yayım_istisna";
        if (hesab_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (hesab_VALUE == 37) return "한국어/자체/ARRAY_Store_xəta";
        if (hesab_VALUE == 38) return "한국어/자체/axın_vəziyyət_istisna";
        if (hesab_VALUE == 1) return "java/lang/Throwable"; if (hesab_VALUE == 2) return "java/lang/Exception";
        if (hesab_VALUE == 3) return "java/lang/RuntimeException"; if (hesab_VALUE == 4) return "java/lang/ArithmeticException";
        if (hesab_VALUE == 5) return "java/lang/NullPointerException"; if (hesab_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (hesab_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (hesab_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (hesab_VALUE == 9) return "java/lang/IllegalArgumentException"; if (hesab_VALUE == 10) return "java/lang/NumberFormatException";
        if (hesab_VALUE == 11) return "java/io/IOException"; if (hesab_VALUE == 12) return "java/io/FileNotFoundException";
        if (hesab_VALUE == 17) return "java/lang/ArrayStoreException";
        if (hesab_VALUE == 18) return "java/net/UnknownHostException";
        if (hesab_VALUE == 19) return "java/net/SocketTimeoutException";
        if (hesab_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (hesab_VALUE == 13) return "java/lang/IllegalStateException"; if (hesab_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int hesab_VALUE) {
        if (hesab_VALUE == 40) return 2;
        if (hesab_VALUE == 41) return 40;
        if (hesab_VALUE == 39) return 11;
        if (hesab_VALUE == 1) return 0;
        if (hesab_VALUE == 2) return 1;
        if (hesab_VALUE == 3) return 2;
        if (hesab_VALUE == 4) return 3;
        if (hesab_VALUE == 5) return 3;
        if (hesab_VALUE == 6) return 3;
        if (hesab_VALUE == 7) return 6;
        if (hesab_VALUE == 8) return 6;
        if (hesab_VALUE == 9) return 3;
        if (hesab_VALUE == 10) return 9;
        if (hesab_VALUE == 11) return 2;
        if (hesab_VALUE == 12) return 11;
        if (hesab_VALUE == 13) return 3;
        if (hesab_VALUE == 14) return 3;
        if (hesab_VALUE == 15) return 3;
        if (hesab_VALUE == 16) return 9;
        if (hesab_VALUE == 17) return 3;
        if (hesab_VALUE == 18) return 11;
        if (hesab_VALUE == 19) return 11;
        if (hesab_VALUE == 20) return 2;
        if (hesab_VALUE == 21) return 3;
        if (hesab_VALUE == 22) return 11;
        if (hesab_VALUE == 23) return 22;
        if (hesab_VALUE == 24) return 22;
        if (hesab_VALUE == 25) return 22;
        if (hesab_VALUE == 26) return 22;
        if (hesab_VALUE == 27) return 9;
        if (hesab_VALUE == 28) return 27;
        if (hesab_VALUE == 29) return 6;
        if (hesab_VALUE == 30) return 29;
        if (hesab_VALUE == 31) return 29;
        if (hesab_VALUE == 32) return 5;
        if (hesab_VALUE == 33) return 4;
        if (hesab_VALUE == 34) return 13;
        if (hesab_VALUE == 35) return 14;
        if (hesab_VALUE == 36) return 15;
        if (hesab_VALUE == 37) return 17;
        if (hesab_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int faktiki_VALUE, int 요구값) {
        for (int 깊이 = 0; faktiki_VALUE != 0 && 깊이 < 16; 깊이++, faktiki_VALUE = 예외부모(faktiki_VALUE))
            if (faktiki_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int hesab_VALUE, String OXUMƏNİ_İstinad) {
        int obyekt_İstinad = 새기억(9, 2); if (XƏTA) return;
        힙[obyekt_İstinad + 2] = hesab_VALUE; 힙[obyekt_İstinad + 3] = host_simvol(OXUMƏNİ_İstinad); 힙참조[obyekt_İstinad + 3] = 1;
        던진객체 = obyekt_İstinad; XƏTA = true;
    }
    static boolean 맞는객체(int obyekt_İstinad, int Ad) {
        if (obyekt_İstinad == 0) return true;
        if (!객체유효(obyekt_İstinad)) return false;
        int sahə_kod = 힙[obyekt_İstinad];
        if (Söz_SMS(Ad, "java/lang/Object")) return true;
        if (sahə_kod >= 32) return 종포함(sahə_kod - 32, Ad);
        if (sahə_kod == 9) { int hədəf_ünvan = istisna_sabit(Ad); return hədəf_ünvan != 0 && 예외포함(힙[obyekt_İstinad + 2], hədəf_ünvan); }
        if (sahə_kod == 1) return Söz_SMS(Ad, "java/lang/String") || Söz_SMS(Ad, "java/lang/CharSequence");
        if (sahə_kod == 4) return Söz_SMS(Ad, "java/lang/StringBuilder") || Söz_SMS(Ad, "java/lang/CharSequence");
        if (sahə_kod == 10) return Söz_SMS(Ad, "java/util/ArrayList") || Söz_SMS(Ad, "java/util/List");
        if (sahə_kod == 11) return Söz_SMS(Ad, "java/util/HashMap") || Söz_SMS(Ad, "java/util/Map");
        if (sahə_kod == 12) return Söz_SMS(Ad, "java/lang/Integer") || Söz_SMS(Ad, "java/lang/Number");
        if (sahə_kod >= 24 && sahə_kod <= 28 && 힙[obyekt_İstinad + 13] != 0) return 한국어화면종(Ad) == sahə_kod || Söz_SMS(Ad, "한국어/자체/화면구성요소");
        if (sahə_kod >= 24 && sahə_kod <= 28) return (한국어화면종(Ad) == 0 && 화면종(Ad) == sahə_kod) || Söz_SMS(Ad, "java/awt/Component") || Söz_SMS(Ad, "java/awt/Container") || Söz_SMS(Ad, "javax/swing/JComponent");
        if (sahə_kod == 29) return Söz_SMS(Ad, 힙[obyekt_İstinad + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (sahə_kod == 30) return Söz_SMS(Ad, "java/awt/FlowLayout") || Söz_SMS(Ad, "java/awt/LayoutManager");
        if (sahə_kod == 17) return Söz_SMS(Ad, "java/net/Socket");
        if (sahə_kod == 18) return Söz_SMS(Ad, "java/net/ServerSocket");
        if (sahə_kod == 19) return Söz_SMS(Ad, 힙[obyekt_İstinad + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (sahə_kod == 14) return Söz_SMS(Ad, "java/net/InetAddress");
        if (sahə_kod == 15) return Söz_SMS(Ad, "java/net/DatagramSocket");
        if (sahə_kod == 16) return Söz_SMS(Ad, "java/net/DatagramPacket");
        if (sahə_kod == 13) return Söz_SMS(Ad, 힙[obyekt_İstinad + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (sahə_kod == 2) return Söz_SMS(Ad, "[I"); if (sahə_kod == 20) return Söz_SMS(Ad, "[B"); if (sahə_kod == 21) return Söz_SMS(Ad, "[Z");
        if (sahə_kod == 22) return Söz_SMS(Ad, "[C"); if (sahə_kod == 23) return Söz_SMS(Ad, "[S");
        if (sahə_kod != 3) return false;
        if (Söz_SMS(Ad, "[Ljava/lang/Object;")) return true;
        int komponent = ARRAY_element[obyekt_İstinad];
        if (komponent == -1) return Söz_SMS(Ad, "[Ljava/lang/String;") || Söz_SMS(Ad, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Ad)) return true;
        if ((Söz_SMS(komponent, "java/lang/String") || Söz_SMS(komponent, "java/lang/StringBuilder")) && Söz_SMS(Ad, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Sinif_Tərif_COUNT; Loop_INDEX++) if (같은말(Sinif_Tərif_ad[Loop_INDEX], komponent)) {
            for (int simvol_kodu = Loop_INDEX, 중첩깊이 = 0; simvol_kodu >= 0 && 중첩깊이 < 16; 중첩깊이++, simvol_kodu = 부모종(simvol_kodu)) {
                if (배열종비교(종부모[simvol_kodu], Ad)) return true;
                for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < Sinif_interfeys_COUNT[simvol_kodu]; daxili_qoşulma_yerinə_qoymaq++) if (배열종비교(Sinif_interfeys[simvol_kodu * 16 + daxili_qoşulma_yerinə_qoymaq], Ad)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int ad_sabit, int 형식참조) {
        int çek_yerinə_qoymaq = 상가[형식참조], daxiletmə_COUNT = sabit_SECOND_VALUE[형식참조];
        if (ad_sabit == 0 || daxiletmə_COUNT < 4 || FAYL[çek_yerinə_qoymaq] != '[' || FAYL[çek_yerinə_qoymaq + 1] != 'L' || FAYL[çek_yerinə_qoymaq + daxiletmə_COUNT - 1] != ';' || sabit_SECOND_VALUE[ad_sabit] != daxiletmə_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT - 3; Loop_INDEX++) if (FAYL[상가[ad_sabit] + Loop_INDEX] != FAYL[çek_yerinə_qoymaq + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void tutacaq_istisna() {
        if (던진객체 == 0) return;
        XƏTA = false;
        while (kadr_INDEX >= 현재가닥 * 32) {
            int fayl_INDEX = kadr_metod[kadr_INDEX], 읽는자리 = kadr_təlimat[kadr_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == fayl_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kadr_yerinə_qoymaq[kadr_INDEX] = 잡기위치[Loop_INDEX]; kadr_Yığın[kadr_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (ilkin_qiymət_vermək_kadr[kadr_INDEX] != 0) Sinif_Tərif_vəziyyət[ilkin_qiymət_vermək_kadr[kadr_INDEX] - 1] = 3;
            if (틀잠금[kadr_INDEX] != 0) { 잠금풀기(틀잠금[kadr_INDEX]); 틀잠금[kadr_INDEX] = 0; }
            kadr_INDEX--;
        }
        istifadəçi.Yazma("Uncaught ");
        if (힙[던진객체] == 9) { istifadəçi.Yazma(istisna_ad(힙[던진객체 + 2])); istifadəçi.Yazma(": "); yazmaq_SMS(힙[던진객체 + 3]); }
        else istifadəçi.Yazma("user exception");
        istifadəçi.yazmaq_simvol_VALUE(10); 던진객체 = 0; XƏTA = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Yığın_təlimat(int əmr_kod) {
        int 첫값 = 빼기(0), 첫형식 = geri_qaytarmaq_TYPE;
        if (əmr_kod == 87) return;
        if (əmr_kod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bayt_verilənlər = 빼기(0), SECOND_format = geri_qaytarmaq_TYPE;
        if (əmr_kod == 88) return;
        if (əmr_kod == 90) { 넣기(첫값, 첫형식); 넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (əmr_kod == 92) { 넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식); 넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (əmr_kod == 95) { 넣기(첫값, 첫형식); 넣기(bayt_verilənlər, SECOND_format); return; }
        int simvol_kodu = 빼기(0), 셋째형식 = geri_qaytarmaq_TYPE;
        if (əmr_kod == 91) { 넣기(첫값, 첫형식); 넣기(simvol_kodu, 셋째형식); 넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (əmr_kod == 93) { 넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식); 넣기(simvol_kodu, 셋째형식); 넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = geri_qaytarmaq_TYPE;
        넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(simvol_kodu, 셋째형식); 넣기(bayt_verilənlər, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int ad_sabit, int 시작점) {
        int sahə_kod = 0, 유효길이 = 0, istisna_İstinad = istisna_sabit(ad_sabit);
        if (Söz_SMS(ad_sabit, "java/lang/StringBuilder")) { sahə_kod = 4; 유효길이 = 1; }
        if (Söz_SMS(ad_sabit, "java/io/FileInputStream")) { sahə_kod = 5; 유효길이 = 2; }
        if (Söz_SMS(ad_sabit, "java/io/FileOutputStream")) { sahə_kod = 6; 유효길이 = 2; }
        if (istisna_İstinad != 0) { sahə_kod = 9; 유효길이 = 2; }
        if (Söz_SMS(ad_sabit, "java/util/ArrayList")) { sahə_kod = 10; 유효길이 = 2; }
        if (Söz_SMS(ad_sabit, "java/util/HashMap")) { sahə_kod = 11; 유효길이 = 2; }
        if (Söz_SMS(ad_sabit, "java/lang/Integer")) { sahə_kod = 12; 유효길이 = 1; }
        if (Söz_SMS(ad_sabit, "java/net/Socket")) { sahə_kod = 17; 유효길이 = 5; }
        if (Söz_SMS(ad_sabit, "java/net/ServerSocket")) { sahə_kod = 18; 유효길이 = 5; }
        if (Söz_SMS(ad_sabit, "java/net/DatagramSocket")) { sahə_kod = 15; 유효길이 = 3; }
        if (Söz_SMS(ad_sabit, "java/net/DatagramPacket")) { sahə_kod = 16; 유효길이 = 4; }
        if (Söz_SMS(ad_sabit, "java/lang/Thread") || Söz_SMS(ad_sabit, "한국어/자체/작업가닥")) { sahə_kod = 13; 유효길이 = 2; }
        if (Söz_SMS(ad_sabit, "java/lang/Object")) { sahə_kod = 8; }
        if (sahə_kod == 0 && 화면종(ad_sabit) != 0) { sahə_kod = 화면종(ad_sabit); 유효길이 = 12; }
        if (sahə_kod == 0) {
            int simvol_kodu = FIND_Sinif_Tərif(ad_sabit); if (simvol_kodu < 0 || XƏTA || !ilkin_qiymət_vermək(simvol_kodu, 시작점)) return;
            sahə_kod = 32 + simvol_kodu; 유효길이 = Sinif_slot_COUNT[simvol_kodu];
        }
        int obyekt_İstinad = ayırmaq_Yaddaş(sahə_kod, 유효길이); if (XƏTA) return;
        if (sahə_kod == 13 && Söz_SMS(ad_sabit, "한국어/자체/작업가닥")) 힙[obyekt_İstinad + 3] = 1;
        if (sahə_kod >= 24 && sahə_kod <= 28 && 한국어화면종(ad_sabit) != 0) 힙[obyekt_İstinad + 13] = 1;
        if (sahə_kod == 5 || sahə_kod == 6 || sahə_kod == 15 || sahə_kod == 17 || sahə_kod == 18) 힙[obyekt_İstinad + 2] = -1;
        if (sahə_kod == 9) 힙[obyekt_İstinad + 2] = istisna_İstinad;
        넣기(obyekt_İstinad, 2);
    }
    static boolean 값같음(int 첫값, int bayt_verilənlər) {
        if (첫값 == bayt_verilənlər) return true;
        if (첫값 == 0 || bayt_verilənlər == 0 || 첫값 < 0 || bayt_verilənlər < 0 || 첫값 >= 힙끝 || bayt_verilənlər >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bayt_verilənlər] == 1) return 글같음(첫값, bayt_verilənlər, false);
        return 힙[첫값] == 12 && 힙[bayt_verilənlər] == 12 && 힙[첫값 + 2] == 힙[bayt_verilənlər + 2];
    }
    static int 글조각(int obyekt_İstinad, int Başla_yerinə_qoymaq, int bitirmək_yerinə_qoymaq) {
        if (!obyekt_VALUE(obyekt_İstinad, 1)) return 0;
        if (Başla_yerinə_qoymaq < 0 || bitirmək_yerinə_qoymaq < Başla_yerinə_qoymaq || bitirmək_yerinə_qoymaq > 힙[obyekt_İstinad + 1]) { xəta_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = ayırmaq_Yaddaş(1, bitirmək_yerinə_qoymaq - Başla_yerinə_qoymaq); if (XƏTA) return 0;
        for (int Loop_INDEX = Başla_yerinə_qoymaq; Loop_INDEX < bitirmək_yerinə_qoymaq; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Başla_yerinə_qoymaq] = 힙[obyekt_İstinad + 2 + Loop_INDEX];
        return 반환값;
    }
    static int qoşul_SMS(int 첫값, int bayt_verilənlər) {
        if (!obyekt_VALUE(첫값, 1) || !obyekt_VALUE(bayt_verilənlər, 1)) return 0;
        int daxiletmə_COUNT = 힙[첫값 + 1], metod_INDEX = 힙[bayt_verilənlər + 1], 반환값 = ayırmaq_Yaddaş(1, daxiletmə_COUNT + metod_INDEX); if (XƏTA) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metod_INDEX; Loop_INDEX++) 힙[반환값 + 2 + daxiletmə_COUNT + Loop_INDEX] = 힙[bayt_verilənlər + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int sahib, int ad_sabit, int 서술상수, int əmr_kod) {
        if (Söz_SMS(sahib, "한국어/자체/실행인수") && əmr_kod == 184) {
            if (Söz_SMS(ad_sabit, "element_COUNT") && Söz_SMS(서술상수, "()I")) { 넣기(istifadəçi.인수개수() - 1, 1); return true; }
            if (Söz_SMS(ad_sabit, "Mətn") && Söz_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= istifadəçi.인수개수() - 1) 예외던짐(29, "icra_etmək_əmr 인수 범위를 벗어났습니다");
                else 넣기(host_simvol(istifadəçi.인수(순번 + 1)), 2);
                return true;
            }
            xəta_VALUE("지원하지 않는 한국어 icra_etmək_əmr 인수 호출"); return true;
        }
        if (Söz_SMS(sahib, "한국어/자체/작업가닥")) { Proses_axın(ad_sabit, 서술상수, əmr_kod, true); return true; }
        if (한국어화면소유(sahib)) { 한국어화면호출(sahib, ad_sabit, 서술상수, əmr_kod); return true; }
        if (화면소유(sahib)) { 화면호출(sahib, ad_sabit, 서술상수, əmr_kod); return true; }
        if (Söz_SMS(sahib, "java/net/Socket") || Söz_SMS(sahib, "java/net/ServerSocket") || Söz_SMS(sahib, "java/io/InputStream") || Söz_SMS(sahib, "java/io/OutputStream")) { 흐름호출(sahib, ad_sabit, 서술상수, əmr_kod); return true; }
        if (Söz_SMS(sahib, "한국어/자체/nüvə_VALUE") && əmr_kod == 184) {
            if (Söz_SMS(ad_sabit, "화면너비") && Söz_SMS(서술상수, "()I")) { 넣기(istifadəçi.화면너비(), 1); return true; }
            if (Söz_SMS(ad_sabit, "화면높이") && Söz_SMS(서술상수, "()I")) { 넣기(istifadəçi.화면높이(), 1); return true; }
            if (Söz_SMS(ad_sabit, "밀리초") && Söz_SMS(서술상수, "()I")) { 넣기(istifadəçi.밀리초(), 1); return true; }
            if (Söz_SMS(ad_sabit, "그림대기") && Söz_SMS(서술상수, "()I")) { 넣기(istifadəçi.그림대기(), 1); return true; }
            if (Söz_SMS(ad_sabit, "사각형") && Söz_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinatı = 빼기(1); 넣기(istifadəçi.사각형(x_koordinatı, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Söz_SMS(sahib, "java/net/InetAddress") || Söz_SMS(sahib, "java/net/DatagramPacket") || Söz_SMS(sahib, "java/net/DatagramSocket")) { 통신호출(sahib, ad_sabit, 서술상수, əmr_kod); return true; }
        if (Söz_SMS(sahib, "java/lang/Thread")) { 가닥호출(ad_sabit, 서술상수, əmr_kod); return true; }
        if (Söz_SMS(sahib, "java/lang/Object")) {
            if (Söz_SMS(ad_sabit, "<init>") && Söz_SMS(서술상수, "()V") && əmr_kod == 183) { 객체유효(빼기(2)); return true; }
            if (Söz_SMS(ad_sabit, "equals") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayt_verilənlər = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bayt_verilənlər ? 1 : 0, 1); return true; }
        }
        if (istisna_sabit(sahib) != 0) {
            if (Söz_SMS(ad_sabit, "<init>") && əmr_kod == 183 && (Söz_SMS(서술상수, "()V") || Söz_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int dəvət = Söz_SMS(서술상수, "()V") ? 0 : 빼기(2), obyekt_İstinad = 빼기(2);
                if (obyekt_VALUE(obyekt_İstinad, 9)) { 힙[obyekt_İstinad + 3] = dəvət; 힙참조[obyekt_İstinad + 3] = 1; } return true;
            }
            if ((Söz_SMS(ad_sabit, "getMessage") || Söz_SMS(ad_sabit, "설명")) && Söz_SMS(서술상수, "()Ljava/lang/String;")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 9)) 넣기(힙[obyekt_İstinad + 3], 2); return true; }
        }
        if (Söz_SMS(sahib, "java/lang/String")) {
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "getBytes") && (Söz_SMS(서술상수, "()[B") || Söz_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodlaşdırma_ad = Söz_SMS(서술상수, "()[B") ? 0 : 빼기(2), obyekt_İstinad = 빼기(2);
                if (!obyekt_VALUE(obyekt_İstinad, 1)) return true;
                if (kodlaşdırma_ad != 0 && !글같음(kodlaşdırma_ad, host_simvol("UTF-8"), false) && !글같음(kodlaşdırma_ad, host_simvol("UTF8"), false) && !글같음(kodlaşdırma_ad, host_simvol("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int daxiletmə_COUNT = 힙[obyekt_İstinad + 1], 반환값 = ayırmaq_Yaddaş(20, daxiletmə_COUNT * 3), 사용수 = 0; if (XƏTA) return true;
                for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < daxiletmə_COUNT; daxili_qoşulma_yerinə_qoymaq++) {
                    int simvol_kodu = 힙[obyekt_İstinad + 2 + daxili_qoşulma_yerinə_qoymaq];
                    if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdbff && daxili_qoşulma_yerinə_qoymaq + 1 < daxiletmə_COUNT && 힙[obyekt_İstinad + 3 + daxili_qoşulma_yerinə_qoymaq] >= 0xdc00 && 힙[obyekt_İstinad + 3 + daxili_qoşulma_yerinə_qoymaq] <= 0xdfff) simvol_kodu = 0x10000 + ((simvol_kodu - 0xd800) << 10) + 힙[obyekt_İstinad + 2 + ++daxili_qoşulma_yerinə_qoymaq] - 0xdc00;
                    else if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdfff) simvol_kodu = '?';
                    if (simvol_kodu < 128) 힙[반환값 + 2 + 사용수++] = simvol_kodu;
                    else { int bayt_COUNT = simvol_kodu < 2048 ? 2 : simvol_kodu < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bayt_COUNT == 2 ? 192 : bayt_COUNT == 3 ? 224 : 240) | simvol_kodu >> (6 * (bayt_COUNT - 1))); for (int Müqayisə_yerinə_qoymaq = bayt_COUNT - 1; Müqayisə_yerinə_qoymaq > 0; Müqayisə_yerinə_qoymaq--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | simvol_kodu >> (6 * (Müqayisə_yerinə_qoymaq - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "valueOf") && Söz_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(rəqəm_simvol(빼기(1)), 2); return true; }
            if (əmr_kod != 182) return false;
            if (Söz_SMS(ad_sabit, "equals") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayt_verilənlər = 빼기(2), 첫값 = 빼기(2); if (obyekt_VALUE(첫값, 1)) 넣기(글같음(첫값, bayt_verilənlər, false) ? 1 : 0, 1); return true; }
            if (Söz_SMS(ad_sabit, "isEmpty") && Söz_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (obyekt_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Söz_SMS(ad_sabit, "substring") && (Söz_SMS(서술상수, "(I)Ljava/lang/String;") || Söz_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Söz_SMS(서술상수, "(II)Ljava/lang/String;"); int bitirmək_yerinə_qoymaq = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (obyekt_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? bitirmək_yerinə_qoymaq : 힙[첫값 + 1]), 2); return true;
            }
            if (Söz_SMS(ad_sabit, "concat") && Söz_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bayt_verilənlər = 빼기(2), 첫값 = 빼기(2); 넣기(qoşul_SMS(첫값, bayt_verilənlər), 2); return true; }
            if (Söz_SMS(ad_sabit, "hashCode") && Söz_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), heş_VALUE = 0; if (obyekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) heş_VALUE = heş_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(heş_VALUE, 1); } return true; }
            if (Söz_SMS(ad_sabit, "toString") && Söz_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (obyekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Söz_SMS(sahib, "java/lang/Integer")) {
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "valueOf") && Söz_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int verilənlər_VALUE = 빼기(1), obyekt_İstinad = verilənlər_VALUE >= -128 && verilənlər_VALUE <= 127 ? Store_tam_ədəd[verilənlər_VALUE + 128] : 0; if (obyekt_İstinad == 0) { obyekt_İstinad = ayırmaq_Yaddaş(12, 1); if (!XƏTA) { 힙[obyekt_İstinad + 2] = verilənlər_VALUE; if (verilənlər_VALUE >= -128 && verilənlər_VALUE <= 127) Store_tam_ədəd[verilənlər_VALUE + 128] = obyekt_İstinad; } } 넣기(obyekt_İstinad, 2); return true; }
            if (əmr_kod == 183 && Söz_SMS(ad_sabit, "<init>") && Söz_SMS(서술상수, "(I)V")) { int verilənlər_VALUE = 빼기(1), obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 12)) 힙[obyekt_İstinad + 2] = verilənlər_VALUE; return true; }
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "intValue") && Söz_SMS(서술상수, "()I")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 12)) 넣기(힙[obyekt_İstinad + 2], 1); return true; }
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "toString") && Söz_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(rəqəm_simvol(빼기(1)), 2); return true; }
        }
        if (Söz_SMS(sahib, "java/lang/Math") && əmr_kod == 184) {
            if (Söz_SMS(ad_sabit, "abs") && Söz_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Söz_SMS(ad_sabit, "min") || Söz_SMS(ad_sabit, "max")) && Söz_SMS(서술상수, "(II)I")) { int bayt_verilənlər = 빼기(1), 첫값 = 빼기(1); 넣기(Söz_SMS(ad_sabit, "min") ? (첫값 < bayt_verilənlər ? 첫값 : bayt_verilənlər) : (첫값 > bayt_verilənlər ? 첫값 : bayt_verilənlər), 1); return true; }
        }
        if (Söz_SMS(sahib, "java/lang/System") && əmr_kod == 184) {
            if (Söz_SMS(ad_sabit, "gc") && Söz_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Söz_SMS(ad_sabit, "arraycopy") && Söz_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int daxiletmə_COUNT = 빼기(1), təyinat_VALUE_INDEX = 빼기(1), bayt_verilənlər = 빼기(2), Başla_yerinə_qoymaq = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bayt_verilənlər)) {
                    int sahə_kod = 힙[첫값];
                    if (힙[bayt_verilənlər] != sahə_kod || (sahə_kod != 2 && sahə_kod != 3 && (sahə_kod < 20 || sahə_kod > 23))) xəta_VALUE("arraycopy type mismatch");
                    else if (daxiletmə_COUNT < 0 || Başla_yerinə_qoymaq < 0 || təyinat_VALUE_INDEX < 0 || Başla_yerinə_qoymaq > 힙[첫값 + 1] - daxiletmə_COUNT || təyinat_VALUE_INDEX > 힙[bayt_verilənlər + 1] - daxiletmə_COUNT) xəta_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bayt_verilənlər && təyinat_VALUE_INDEX > Başla_yerinə_qoymaq) { for (int Loop_INDEX = daxiletmə_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bayt_verilənlər + 2 + təyinat_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Başla_yerinə_qoymaq + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT && !XƏTA; Loop_INDEX++) { int verilənlər_VALUE = 힙[첫값 + 2 + Başla_yerinə_qoymaq + Loop_INDEX]; if (sahə_kod != 3 || 배열저장가능(bayt_verilənlər, verilənlər_VALUE)) 힙[bayt_verilənlər + 2 + təyinat_VALUE_INDEX + Loop_INDEX] = verilənlər_VALUE; } }
                }
                return true;
            }
        }
        if (Söz_SMS(sahib, "java/util/ArrayList") || Söz_SMS(sahib, "java/util/List") || Söz_SMS(sahib, "java/util/HashMap") || Söz_SMS(sahib, "java/util/Map")) {
            모음호출(sahib, ad_sabit, 서술상수, əmr_kod); return true;
        }
        return false;
    }
    static void 모음늘리기(int obyekt_İstinad, int 필요수) {
        int 이전값 = 힙[obyekt_İstinad + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Sonrakı_yerinə_qoymaq = 용량값 < 8 ? 8 : 용량값 * 2; if (Sonrakı_yerinə_qoymaq < 필요수) Sonrakı_yerinə_qoymaq = 필요수;
        int verilənlər_ARRAY = ayırmaq_Yaddaş(3, Sonrakı_yerinə_qoymaq); if (XƏTA) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[verilənlər_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[obyekt_İstinad + 2] = verilənlər_ARRAY; 힙참조[obyekt_İstinad + 2] = 1;
    }
    static void 모음호출(int sahib, int ad_sabit, int 서술상수, int əmr_kod) {
        boolean 대응참조 = Söz_SMS(sahib, "java/util/HashMap") || Söz_SMS(sahib, "java/util/Map"); int sahə_kod = 대응참조 ? 11 : 10;
        if (Söz_SMS(ad_sabit, "<init>") && əmr_kod == 183 && Söz_SMS(서술상수, "()V")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, sahə_kod)) 모음늘리기(obyekt_İstinad, 8); return; }
        if (əmr_kod != 182 && əmr_kod != 185) { xəta_VALUE("invalid collection invocation"); return; }
        if (Söz_SMS(ad_sabit, "size") && Söz_SMS(서술상수, "()I") || Söz_SMS(ad_sabit, "isEmpty") && Söz_SMS(서술상수, "()Z")) {
            int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, sahə_kod)) 넣기(Söz_SMS(ad_sabit, "size") ? 힙[obyekt_İstinad + 3] : 힙[obyekt_İstinad + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Söz_SMS(ad_sabit, "clear") && Söz_SMS(서술상수, "()V")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, sahə_kod)) { int verilənlər_ARRAY = 힙[obyekt_İstinad + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[verilənlər_ARRAY + 1]; Loop_INDEX++) 힙[verilənlər_ARRAY + 2 + Loop_INDEX] = 0; 힙[obyekt_İstinad + 3] = 0; } return; }
        if (!대응참조 && Söz_SMS(ad_sabit, "add") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int verilənlər_VALUE = 빼기(2), obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 10)) return;
            int daxiletmə_COUNT = 힙[obyekt_İstinad + 3]; 모음늘리기(obyekt_İstinad, daxiletmə_COUNT + 1); if (!XƏTA) { 힙[힙[obyekt_İstinad + 2] + 2 + daxiletmə_COUNT] = verilənlər_VALUE; 힙[obyekt_İstinad + 3] = daxiletmə_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Söz_SMS(ad_sabit, "get") || Söz_SMS(ad_sabit, "remove")) && Söz_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Söz_SMS(ad_sabit, "set") && Söz_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Söz_SMS(ad_sabit, "set"); int verilənlər_VALUE = 지정여부 ? 빼기(2) : 0, daxiletmə_yerinə_qoymaq = 빼기(1), obyekt_İstinad = 빼기(2);
            if (!obyekt_VALUE(obyekt_İstinad, 10)) return;
            int daxiletmə_COUNT = 힙[obyekt_İstinad + 3], verilənlər_ARRAY = 힙[obyekt_İstinad + 2];
            if (daxiletmə_yerinə_qoymaq < 0 || daxiletmə_yerinə_qoymaq >= daxiletmə_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[verilənlər_ARRAY + 2 + daxiletmə_yerinə_qoymaq];
            if (지정여부) 힙[verilənlər_ARRAY + 2 + daxiletmə_yerinə_qoymaq] = verilənlər_VALUE;
            if (Söz_SMS(ad_sabit, "remove")) { for (int Loop_INDEX = daxiletmə_yerinə_qoymaq + 1; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) 힙[verilənlər_ARRAY + 1 + Loop_INDEX] = 힙[verilənlər_ARRAY + 2 + Loop_INDEX]; 힙[verilənlər_ARRAY + 1 + daxiletmə_COUNT] = 0; 힙[obyekt_İstinad + 3] = daxiletmə_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Söz_SMS(ad_sabit, "get") || Söz_SMS(ad_sabit, "remove")) && Söz_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Söz_SMS(ad_sabit, "put") && Söz_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Söz_SMS(ad_sabit, "containsKey") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Söz_SMS(ad_sabit, "put"), silmək = Söz_SMS(ad_sabit, "remove");
            int verilənlər_VALUE = 넣기여부 ? 빼기(2) : 0, Açar_İstinad = 빼기(2), obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 11)) return;
            int daxiletmə_COUNT = 힙[obyekt_İstinad + 3], verilənlər_ARRAY = 힙[obyekt_İstinad + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) if (값같음(Açar_İstinad, 힙[verilənlər_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[verilənlər_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(obyekt_İstinad, (daxiletmə_COUNT + 1) * 2); verilənlər_ARRAY = 힙[obyekt_İstinad + 2]; 찾은여부 = daxiletmə_COUNT; if (!XƏTA) 힙[obyekt_İstinad + 3] = daxiletmə_COUNT + 1; }
                if (!XƏTA) { 힙[verilənlər_ARRAY + 2 + 2 * 찾은여부] = Açar_İstinad; 힙[verilənlər_ARRAY + 3 + 2 * 찾은여부] = verilənlər_VALUE; }
            }
            if (silmək && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) { 힙[verilənlər_ARRAY + 2 * Loop_INDEX] = 힙[verilənlər_ARRAY + 2 + 2 * Loop_INDEX]; 힙[verilənlər_ARRAY + 1 + 2 * Loop_INDEX] = 힙[verilənlər_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[verilənlər_ARRAY + 2 * daxiletmə_COUNT] = 0; 힙[verilənlər_ARRAY + 1 + 2 * daxiletmə_COUNT] = 0; 힙[obyekt_İstinad + 3] = daxiletmə_COUNT - 1; }
            if (Söz_SMS(ad_sabit, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        xəta_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int obyekt_İstinad) {
        if (!객체유효(obyekt_İstinad)) return false;
        if (잠금깊이[obyekt_İstinad] != 0 && 잠금주인[obyekt_İstinad] != 현재가닥 + 1) { dəyişdirmək_HTTP_sorğusu = true; return false; }
        잠금주인[obyekt_İstinad] = 현재가닥 + 1; 잠금깊이[obyekt_İstinad]++; return true;
    }
    static void 잠금풀기(int obyekt_İstinad) {
        if (!객체유효(obyekt_İstinad)) return;
        if (잠금깊이[obyekt_İstinad] == 0 || 잠금주인[obyekt_İstinad] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[obyekt_İstinad] == 0) 잠금주인[obyekt_İstinad] = 0;
    }
    static boolean SWITCH_axın() {
        axın_kadr[현재가닥] = kadr_INDEX;
        if (kadr_INDEX < 현재가닥 * 32) axın_vəziyyət[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < axın_COUNT; Loop_INDEX++) if (axın_vəziyyət[Loop_INDEX] == 2 && axın_vəziyyət[가닥대기[Loop_INDEX]] == 3) axın_vəziyyət[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= axın_COUNT; Loop_INDEX++) {
            int Sonrakı_yerinə_qoymaq = (현재가닥 + Loop_INDEX) % axın_COUNT;
            if (axın_vəziyyət[Sonrakı_yerinə_qoymaq] == 1) { 현재가닥 = Sonrakı_yerinə_qoymaq; kadr_INDEX = axın_kadr[Sonrakı_yerinə_qoymaq]; dəyişdirmək_HTTP_sorğusu = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < axın_COUNT; Loop_INDEX++) if (axın_vəziyyət[Loop_INDEX] != 3) { xəta_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int ad_sabit, int 서술상수, int əmr_kod) { Proses_axın(ad_sabit, 서술상수, əmr_kod, false); }
    static void Proses_axın(int ad_sabit, int 서술상수, int əmr_kod, boolean 한국어) {
        if (əmr_kod == 184 && Söz_SMS(ad_sabit, 한국어 ? "YIELD_tapşırıq" : "yield") && Söz_SMS(서술상수, "()V")) { dəyişdirmək_HTTP_sorğusu = true; return; }
        if (əmr_kod == 184 && Söz_SMS(ad_sabit, "currentThread") && Söz_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(axın_obyekt[현재가닥], 2); return; }
        if (əmr_kod == 183 && Söz_SMS(ad_sabit, "<init>") && (Söz_SMS(서술상수, "()V") || Söz_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int hədəf_ünvan = Söz_SMS(서술상수, "()V") ? 0 : 빼기(2), obyekt_İstinad = 빼기(2);
            if (!객체유효(obyekt_İstinad)) return;
            if (힙[obyekt_İstinad] == 13) { 힙[obyekt_İstinad + 2] = hədəf_ünvan; 힙참조[obyekt_İstinad + 2] = 1; }
            else if (hədəf_ünvan != 0) xəta_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (əmr_kod == 182 && (Söz_SMS(ad_sabit, 한국어 ? "Başla_tapşırıq" : "start") || Söz_SMS(ad_sabit, 한국어 ? "기다리기" : "join")) && Söz_SMS(서술상수, "()V") || əmr_kod == 182 && Söz_SMS(ad_sabit, 한국어 ? "살아있는가" : "isAlive") && Söz_SMS(서술상수, "()Z")) {
            int obyekt_İstinad = 빼기(2); if (!객체유효(obyekt_İstinad)) return;
            int hesab_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < axın_COUNT; Loop_INDEX++) if (axın_obyekt[Loop_INDEX] == obyekt_İstinad) hesab_VALUE = Loop_INDEX;
            if (Söz_SMS(ad_sabit, 한국어 ? "살아있는가" : "isAlive")) { 넣기(hesab_VALUE >= 0 && axın_vəziyyət[hesab_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Söz_SMS(ad_sabit, 한국어 ? "기다리기" : "join")) { if (hesab_VALUE >= 0 && axın_vəziyyət[hesab_VALUE] != 3) { 가닥대기[현재가닥] = hesab_VALUE; axın_vəziyyət[현재가닥] = 2; dəyişdirmək_HTTP_sorğusu = true; } return; }
            if (hesab_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (axın_COUNT == 4) { xəta_VALUE("thread limit (4 including main)"); return; }
            int hədəf_ünvan = 힙[obyekt_İstinad] == 13 ? 힙[obyekt_İstinad + 2] : obyekt_İstinad;
            int fayl_INDEX = hədəf_ünvan > 0 && 힙[hədəf_ünvan] >= 32 ? ad_metod(힙[hədəf_ünvan] - 32, 한국어 ? "icra_etmək_tapşırıq" : "run", "()V") : -1;
            if (hədəf_ünvan != 0 && fayl_INDEX < 0) { xəta_VALUE("Runnable.run required"); return; }
            hesab_VALUE = axın_COUNT++; axın_obyekt[hesab_VALUE] = obyekt_İstinad; axın_hədəf[hesab_VALUE] = hədəf_ünvan;
            int kadr = hesab_VALUE * 32; axın_kadr[hesab_VALUE] = fayl_INDEX < 0 ? kadr - 1 : kadr; axın_vəziyyət[hesab_VALUE] = fayl_INDEX < 0 ? 3 : 1;
            if (fayl_INDEX >= 0) { kadr_metod[kadr] = fayl_INDEX; kadr_yerinə_qoymaq[kadr] = metod_Başla[fayl_INDEX]; lokal_VALUE[kadr * 128] = hədəf_ünvan; lokal_TYPE[kadr * 128] = 2; }
            return;
        }
        xəta_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ünvan_SMS = new int[16];
    static int lokal_ünvan() { return ünvan_obyekt(0x7f000001); }
    static int ünvan_obyekt(int VALUE) { int obyekt_İstinad = ayırmaq_Yaddaş(14, 1); if (!XƏTA) 힙[obyekt_İstinad + 2] = VALUE; return obyekt_İstinad; }
    static int 주소해독(int obyekt_İstinad) {
        if (obyekt_İstinad == 0 || 글같음(obyekt_İstinad, host_simvol("localhost"), false)) return 0x7f000001;
        if (!obyekt_VALUE(obyekt_İstinad, 1)) return 0;
        int verilənlər_VALUE = 0, 총수 = 0, ünvan_bayt = 0, 자릿수 = 0, daxiletmə_COUNT = 힙[obyekt_İstinad + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= daxiletmə_COUNT; Loop_INDEX++) {
            int simvol_kodu = Loop_INDEX == daxiletmə_COUNT ? '.' : 힙[obyekt_İstinad + 2 + Loop_INDEX];
            if (simvol_kodu == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } verilənlər_VALUE = verilənlər_VALUE << 8 | ünvan_bayt; 총수++; ünvan_bayt = 자릿수 = 0; }
            else { if (simvol_kodu < '0' || simvol_kodu > '9' || ++자릿수 > 3 || (ünvan_bayt = ünvan_bayt * 10 + simvol_kodu - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return verilənlər_VALUE;
    }
    static int ünvan_simvol(int verilənlər_VALUE) {
        int daxiletmə_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ünvan_bayt = verilənlər_VALUE >>> 이동비트 & 255;
            if (ünvan_bayt >= 100) ünvan_SMS[daxiletmə_COUNT++] = '0' + ünvan_bayt / 100;
            if (ünvan_bayt >= 10) ünvan_SMS[daxiletmə_COUNT++] = '0' + ünvan_bayt / 10 % 10;
            ünvan_SMS[daxiletmə_COUNT++] = '0' + ünvan_bayt % 10; if (이동비트 != 0) ünvan_SMS[daxiletmə_COUNT++] = '.';
        }
        int obyekt_İstinad = ayırmaq_Yaddaş(1, daxiletmə_COUNT); if (!XƏTA) for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) 힙[obyekt_İstinad + 2 + Loop_INDEX] = ünvan_SMS[Loop_INDEX]; return obyekt_İstinad;
    }
    static void 통신호출(int sahib, int ad_sabit, int 서술상수, int əmr_kod) {
        if (Söz_SMS(sahib, "java/net/InetAddress")) {
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "getLoopbackAddress") && Söz_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_ünvan(), 2); return; }
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "getByName") && Söz_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int verilənlər_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !XƏTA) 넣기(ünvan_obyekt(verilənlər_VALUE), 2); return;
            }
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "getHostAddress") && Söz_SMS(서술상수, "()Ljava/lang/String;")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 14)) 넣기(ünvan_simvol(힙[obyekt_İstinad + 2]), 2); return; }
        }
        if (Söz_SMS(sahib, "java/net/DatagramPacket")) {
            if (əmr_kod == 183 && Söz_SMS(ad_sabit, "<init>") && (Söz_SMS(서술상수, "([BI)V") || Söz_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean təyinat_VALUE_İstinad = Söz_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = təyinat_VALUE_İstinad ? 빼기(1) : 0, ünvan_İstinad = təyinat_VALUE_İstinad ? 빼기(2) : 0;
                int daxiletmə_COUNT = 빼기(1), verilənlər_ARRAY = 빼기(2), obyekt_İstinad = 빼기(2);
                if (!obyekt_VALUE(obyekt_İstinad, 16) || !obyekt_VALUE(verilənlər_ARRAY, 20)) return;
                if (daxiletmə_COUNT < 0 || daxiletmə_COUNT > 힙[verilənlər_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ünvan_İstinad != 0 && !obyekt_VALUE(ünvan_İstinad, 14)) return;
                힙[obyekt_İstinad + 2] = verilənlər_ARRAY; 힙참조[obyekt_İstinad + 2] = 1; 힙[obyekt_İstinad + 3] = daxiletmə_COUNT;
                힙[obyekt_İstinad + 4] = ünvan_İstinad; 힙참조[obyekt_İstinad + 4] = 1; 힙[obyekt_İstinad + 5] = 접속번호; return;
            }
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "setLength") && Söz_SMS(서술상수, "(I)V")) {
                int daxiletmə_COUNT = 빼기(1), obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 16)) return;
                if (daxiletmə_COUNT < 0 || daxiletmə_COUNT > 힙[힙[obyekt_İstinad + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[obyekt_İstinad + 3] = daxiletmə_COUNT; return;
            }
            if (əmr_kod == 182 && (Söz_SMS(ad_sabit, "getData") && Söz_SMS(서술상수, "()[B") || Söz_SMS(ad_sabit, "getLength") && Söz_SMS(서술상수, "()I") || Söz_SMS(ad_sabit, "getAddress") && Söz_SMS(서술상수, "()Ljava/net/InetAddress;") || Söz_SMS(ad_sabit, "getPort") && Söz_SMS(서술상수, "()I"))) {
                int obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 16)) return;
                int daxiletmə_yerinə_qoymaq = Söz_SMS(ad_sabit, "getData") ? 2 : Söz_SMS(ad_sabit, "getLength") ? 3 : Söz_SMS(ad_sabit, "getAddress") ? 4 : 5;
                넣기(힙[obyekt_İstinad + daxiletmə_yerinə_qoymaq], daxiletmə_yerinə_qoymaq == 2 || daxiletmə_yerinə_qoymaq == 4 ? 2 : 1); return;
            }
        }
        if (Söz_SMS(sahib, "java/net/DatagramSocket")) {
            if (əmr_kod == 183 && Söz_SMS(ad_sabit, "<init>") && (Söz_SMS(서술상수, "()V") || Söz_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Söz_SMS(서술상수, "()V") ? 0 : 빼기(1), obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = istifadəçi.açmaq_Şəbəkə(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[obyekt_İstinad + 2] = 열린파일번호; return;
            }
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "setSoTimeout") && Söz_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obyekt_İstinad + 3] = 밀리초값; return;
            }
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "getLocalPort") && Söz_SMS(서술상수, "()I")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 15)) 넣기(힙[obyekt_İstinad + 2] < 0 ? -1 : istifadəçi.Şəbəkə_port(힙[obyekt_İstinad + 2]), 1); return; }
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "isClosed") && Söz_SMS(서술상수, "()Z")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 15)) 넣기(힙[obyekt_İstinad + 2] < 0 ? 1 : 0, 1); return; }
            if (əmr_kod == 182 && Söz_SMS(ad_sabit, "close") && Söz_SMS(서술상수, "()V")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 15) && 힙[obyekt_İstinad + 2] >= 0) { istifadəçi.파일서술자닫기(힙[obyekt_İstinad + 2]); 힙[obyekt_İstinad + 2] = -1; } return; }
            if (əmr_kod == 182 && (Söz_SMS(ad_sabit, "send") || Söz_SMS(ad_sabit, "receive")) && Söz_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket_5cd5338b = 빼기(2), obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(paket_5cd5338b, 16) || !obyekt_VALUE(obyekt_İstinad, 15)) return;
                int verilənlər_ARRAY = 힙[paket_5cd5338b + 2], 유효길이 = 힙[paket_5cd5338b + 3], 열린파일번호 = 힙[obyekt_İstinad + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Söz_SMS(ad_sabit, "send")) {
                    if (!obyekt_VALUE(힙[paket_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[verilənlər_ARRAY + 2 + Loop_INDEX];
                    if (istifadəçi.göndərmək_Şəbəkə(열린파일번호, 힙[힙[paket_5cd5338b + 4] + 2], 힙[paket_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int daxiletmə_COUNT = istifadəçi.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (daxiletmə_COUNT == -11) {
                        int 현재시각 = istifadəçi.밀리초();
                        if (힙[obyekt_İstinad + 4] == 0) 힙[obyekt_İstinad + 4] = 현재시각 + 1;
                        if (힙[obyekt_İstinad + 3] > 0 && 현재시각 - (힙[obyekt_İstinad + 4] - 1) >= 힙[obyekt_İstinad + 3]) { 힙[obyekt_İstinad + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(obyekt_İstinad, 2); 넣기(paket_5cd5338b, 2); kadr_yerinə_qoymaq[kadr_INDEX] = kadr_təlimat[kadr_INDEX]; dəyişdirmək_HTTP_sorğusu = true; return;
                    }
                    힙[obyekt_İstinad + 4] = 0;
                    if (daxiletmə_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) 힙[verilənlər_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[paket_5cd5338b + 3] = daxiletmə_COUNT; 힙[paket_5cd5338b + 4] = ünvan_obyekt(통신임시[513]); 힙참조[paket_5cd5338b + 4] = 1; 힙[paket_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        xəta_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int obyekt_İstinad) {
        int 현재시각 = istifadəçi.밀리초();
        if (힙[obyekt_İstinad + 5] == 0) 힙[obyekt_İstinad + 5] = 현재시각 + 1;
        if (힙[obyekt_İstinad + 3] > 0 && 현재시각 - (힙[obyekt_İstinad + 5] - 1) >= 힙[obyekt_İstinad + 3]) { 힙[obyekt_İstinad + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadr_yerinə_qoymaq[kadr_INDEX] = kadr_təlimat[kadr_INDEX]; dəyişdirmək_HTTP_sorğusu = true; return true;
    }
    static void 흐름호출(int sahib, int ad_sabit, int 서술상수, int əmr_kod) {
        boolean 수신쪽 = Söz_SMS(sahib, "java/net/ServerSocket"), axın = Söz_SMS(sahib, "java/io/InputStream") || Söz_SMS(sahib, "java/io/OutputStream");
        if (!axın && əmr_kod == 183 && Söz_SMS(ad_sabit, "<init>")) {
            boolean 빈여부 = Söz_SMS(서술상수, "()V"), 이름지정여부 = Söz_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Söz_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Söz_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { xəta_VALUE("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), ünvan_İstinad = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, obyekt_İstinad = 빼기(2);
            if (!obyekt_VALUE(obyekt_İstinad, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !obyekt_VALUE(ünvan_İstinad, 14)) return;
            int Şəbəkə_ünvan = 이름지정여부 ? 주소해독(ünvan_İstinad) : 주소지정여부 ? 힙[ünvan_İstinad + 2] : 0x7f000001;
            if (XƏTA || 던진객체 != 0) return;
            int 열린파일번호 = istifadəçi.axın_nəzarət(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? istifadəçi.axın_nəzarət(1, 열린파일번호, 접속번호) : istifadəçi.QOŞUN_axın(열린파일번호, Şəbəkə_ünvan, 접속번호);
            if (처리값 < 0) { istifadəçi.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[obyekt_İstinad + 2] = 열린파일번호; 힙[obyekt_İstinad + 4] = 접속번호; 힙[obyekt_İstinad + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!axın && Söz_SMS(ad_sabit, "setSoTimeout") && Söz_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obyekt_İstinad + 3] = 밀리초값; return; }
        if (!axın && Söz_SMS(ad_sabit, "close") && Söz_SMS(서술상수, "()V")) { int obyekt_İstinad = 빼기(2); if (obyekt_VALUE(obyekt_İstinad, 수신쪽 ? 18 : 17) && 힙[obyekt_İstinad + 2] >= 0) { istifadəçi.파일서술자닫기(힙[obyekt_İstinad + 2]); 힙[obyekt_İstinad + 2] = -1; } return; }
        if (!axın && (Söz_SMS(ad_sabit, "getLocalPort") || Söz_SMS(ad_sabit, "getPort") || Söz_SMS(ad_sabit, "isClosed") || Söz_SMS(ad_sabit, "isConnected"))) {
            int obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 수신쪽 ? 18 : 17)) return;
            넣기(Söz_SMS(ad_sabit, "isClosed") ? 힙[obyekt_İstinad + 2] < 0 ? 1 : 0 : Söz_SMS(ad_sabit, "isConnected") ? 힙[obyekt_İstinad + 6] : Söz_SMS(ad_sabit, "getPort") ? 힙[obyekt_İstinad + 4] : 힙[obyekt_İstinad + 2] < 0 ? -1 : istifadəçi.axın_nəzarət(4, 힙[obyekt_İstinad + 2], 0), 1); return;
        }
        if (수신쪽 && Söz_SMS(ad_sabit, "accept") && Söz_SMS(서술상수, "()Ljava/net/Socket;")) {
            int obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 18)) return; int 열린파일번호 = istifadəçi.axın_nəzarət(3, 힙[obyekt_İstinad + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(obyekt_İstinad)) 넣기(obyekt_İstinad, 2); return; }
            힙[obyekt_İstinad + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = ayırmaq_Yaddaş(17, 5); if (XƏTA) { istifadəçi.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = istifadəçi.axın_nəzarət(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !axın && ((Söz_SMS(ad_sabit, "getInputStream") && Söz_SMS(서술상수, "()Ljava/io/InputStream;")) || (Söz_SMS(ad_sabit, "getOutputStream") && Söz_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 17)) return; if (힙[obyekt_İstinad + 2] < 0 || 힙[obyekt_İstinad + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = ayırmaq_Yaddaş(19, 4); if (XƏTA) return; 힙[반환값 + 2] = obyekt_İstinad; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Söz_SMS(ad_sabit, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (axın) {
            boolean 읽기여부 = Söz_SMS(ad_sabit, "read"), 쓰기여부 = Söz_SMS(ad_sabit, "write"), blokla = Söz_SMS(서술상수, "([B)I") || Söz_SMS(서술상수, "([B)V"), 부분배열여부 = Söz_SMS(서술상수, "([BII)I") || Söz_SMS(서술상수, "([BII)V");
            int daxiletmə_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, verilənlər_ARRAY = blokla || 부분배열여부 ? 빼기(2) : 0;
            int verilənlər_VALUE = 쓰기여부 && Söz_SMS(서술상수, "(I)V") ? 빼기(1) : 0, obyekt_İstinad = 빼기(2);
            if (!obyekt_VALUE(obyekt_İstinad, 19)) return; int 부모참조 = 힙[obyekt_İstinad + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Söz_SMS(ad_sabit, "close") && Söz_SMS(서술상수, "()V")) { istifadəçi.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Söz_SMS(ad_sabit, "flush") && Söz_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[obyekt_İstinad + 3] == 0)) { xəta_VALUE("unsupported stream operation"); return; }
            if (blokla || 부분배열여부) { if (!obyekt_VALUE(verilənlər_ARRAY, 20)) return; if (blokla) daxiletmə_COUNT = 힙[verilənlər_ARRAY + 1]; if (시작변위 < 0 || daxiletmə_COUNT < 0 || 시작변위 > 힙[verilənlər_ARRAY + 1] - daxiletmə_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else daxiletmə_COUNT = 1;
            if (daxiletmə_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[obyekt_İstinad + 4] : 0, 처리값 = 0;
            while (완료수 < daxiletmə_COUNT) {
                처리값 = 읽기여부 ? istifadəçi.파일한바이트읽기(열린파일번호) : istifadəçi.파일한바이트쓰기(열린파일번호, blokla || 부분배열여부 ? 힙[verilənlər_ARRAY + 2 + 시작변위 + 완료수] : verilənlər_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blokla || 부분배열여부)) 힙[verilənlər_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(blokla || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[obyekt_İstinad + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(obyekt_İstinad, 2); if (blokla || 부분배열여부) 넣기(verilənlər_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(daxiletmə_COUNT, 1); } if (쓰기여부 && !(blokla || 부분배열여부)) 넣기(verilənlər_VALUE, 1); } return;
            }
            힙[obyekt_İstinad + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : blokla || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        xəta_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int ad_sabit) {
        if (Söz_SMS(ad_sabit, "한국어/자체/pəncərə")) return 24;
        if (Söz_SMS(ad_sabit, "한국어/자체/Etiket")) return 26;
        if (Söz_SMS(ad_sabit, "한국어/자체/düymə")) return 27;
        if (Söz_SMS(ad_sabit, "한국어/자체/SMS_sahə")) return 28;
        if (Söz_SMS(ad_sabit, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int ad_sabit) {
        return 한국어화면종(ad_sabit) != 0 || Söz_SMS(ad_sabit, "한국어/자체/화면구성요소") || Söz_SMS(ad_sabit, "한국어/자체/hadisə_növbə");
    }
    static int 화면종(int ad_sabit) {
        int 한국어종 = 한국어화면종(ad_sabit); if (한국어종 != 0) return 한국어종;
        if (Söz_SMS(ad_sabit, "javax/swing/JFrame")) return 24;
        if (Söz_SMS(ad_sabit, "javax/swing/JPanel")) return 25;
        if (Söz_SMS(ad_sabit, "javax/swing/JLabel")) return 26;
        if (Söz_SMS(ad_sabit, "javax/swing/JButton")) return 27;
        if (Söz_SMS(ad_sabit, "javax/swing/JTextField")) return 28;
        if (Söz_SMS(ad_sabit, "java/awt/event/ActionEvent")) return 29;
        if (Söz_SMS(ad_sabit, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int ad_sabit) {
        return 화면종(ad_sabit) != 0 || Söz_SMS(ad_sabit, "java/awt/Component") || Söz_SMS(ad_sabit, "java/awt/Container") || Söz_SMS(ad_sabit, "javax/swing/JComponent") || Söz_SMS(ad_sabit, "javax/swing/AbstractButton") || Söz_SMS(ad_sabit, "javax/swing/text/JTextComponent") || Söz_SMS(ad_sabit, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int obyekt_İstinad) { if (!객체유효(obyekt_İstinad)) return false; if (힙[obyekt_İstinad] < 24 || 힙[obyekt_İstinad] > 28) { xəta_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int obyekt_İstinad, int SMS_İstinad) {
        if (SMS_İstinad != 0 && !obyekt_VALUE(SMS_İstinad, 1)) return;
        int daxiletmə_COUNT = SMS_İstinad == 0 ? 0 : 힙[SMS_İstinad + 1]; if (daxiletmə_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_İstinad + 2 + Loop_INDEX];
        if (istifadəçi.화면글(힙[obyekt_İstinad + 2], 화면글임시, daxiletmə_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[obyekt_İstinad + 3] = SMS_İstinad; 힙참조[obyekt_İstinad + 3] = 1;
    }
    static int 화면문자읽기(int obyekt_İstinad) {
        int hesab_VALUE = 힙[obyekt_İstinad + 2], daxiletmə_COUNT = istifadəçi.화면연결(8, hesab_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (daxiletmə_COUNT < 0) { xəta_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) { int 부호값 = istifadəçi.화면연결(9, hesab_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = ayırmaq_Yaddaş(1, 사용수); if (!XƏTA) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 nüvə_VALUE 화면 기능에 연결한다. Swing obyekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int sahib, int ad_sabit, int 서술상수, int əmr_kod) {
        if (Söz_SMS(sahib, "한국어/자체/hadisə_növbə")) {
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "나중에실행") && Söz_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int tapşırıq_aktiv = 빼기(2); if (!객체유효(tapşırıq_aktiv)) return;
                if (나중수 == 8) { xəta_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tapşırıq_aktiv; return;
            }
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "사건처리중인가") && Söz_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            xəta_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Söz_SMS(sahib, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!obyekt_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Söz_SMS(ad_sabit, "hadisə_mənbə") && Söz_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Söz_SMS(ad_sabit, "əmr_SMS") && Söz_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Söz_SMS(ad_sabit, "INDEX") && Söz_SMS(서술상수, "()I")) 넣기(1001, 1);
            else xəta_VALUE("지원하지 않는 한국어 Gedişat 알림 호출"); return;
        }
        if (əmr_kod == 183 && Söz_SMS(ad_sabit, "<init>")) {
            int 종류 = 한국어화면종(sahib), 받이 = 0, 가로 = 0, Şaquli_yerinə_qoymaq = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Söz_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (istifadəçi.화면너비() - 폭) / 2; Şaquli_yerinə_qoymaq = (istifadəçi.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Söz_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Söz_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Şaquli_yerinə_qoymaq = 빼기(1); 가로 = 빼기(1);
            } else { xəta_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int Mətn = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Şaquli_yerinə_qoymaq < 0 || 폭 > istifadəçi.화면너비() - 가로 || 높이 > istifadəçi.화면높이() - Şaquli_yerinə_qoymaq) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = istifadəçi.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { xəta_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Şaquli_yerinə_qoymaq; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            istifadəçi.화면연결(1, INDEX, 가로, Şaquli_yerinə_qoymaq, 폭, 높이);
            if (종류 == 24) istifadəçi.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Mətn); return;
        }
        if (əmr_kod != 182) { xəta_VALUE("잘못된 한국어 화면 호출 Əmr"); return; }
        if (Söz_SMS(ad_sabit, "yazmaq_SMS") && Söz_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Mətn = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Mətn); return;
        }
        if (Söz_SMS(ad_sabit, "글읽기") && Söz_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Söz_SMS(ad_sabit, "동작맡기기") && Söz_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Söz_SMS(ad_sabit, "əlavə_etmək_element") && Söz_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int uşaq_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(uşaq_VALUE) || !화면객체(부모)) return;
            if (istifadəçi.화면연결(2, 힙[부모 + 2], 힙[uşaq_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[uşaq_VALUE + 11] = 부모; 힙참조[uşaq_VALUE + 11] = 1; return;
        }
        if (Söz_SMS(ad_sabit, "자리정하기") && Söz_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Şaquli_yerinə_qoymaq = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (istifadəçi.화면연결(1, 힙[element_VALUE + 2], 가로, Şaquli_yerinə_qoymaq, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Şaquli_yerinə_qoymaq; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Söz_SMS(ad_sabit, "göstərmək_pəncərə") || Söz_SMS(ad_sabit, "Bağla")) && Söz_SMS(서술상수, "()V")) {
            boolean görünmə_VALUE = Söz_SMS(ad_sabit, "göstərmək_pəncərə"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (istifadəçi.화면연결(görünmə_VALUE ? 3 : 4, 힙[element_VALUE + 2], görünmə_VALUE ? 1 : 0, 0, 0, 0) < 0) { xəta_VALUE("화면은 interaktiv 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = görünmə_VALUE ? 1 : 0; return;
        }
        if (Söz_SMS(ad_sabit, "보이는가") && Söz_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        xəta_VALUE("지원하지 않는 한국어 화면 metod_VALUE");
    }
    static void 화면호출(int sahib, int ad_sabit, int 서술상수, int əmr_kod) {
        if (Söz_SMS(sahib, "javax/swing/SwingUtilities")) {
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "invokeLater") && Söz_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int obyekt_İstinad = 빼기(2); if (!객체유효(obyekt_İstinad)) return; if (나중수 == 8) { xəta_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = obyekt_İstinad; return; }
            if (əmr_kod == 184 && Söz_SMS(ad_sabit, "isEventDispatchThread") && Söz_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            xəta_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Söz_SMS(sahib, "java/awt/event/ActionEvent")) {
            int obyekt_İstinad = 빼기(2); if (!obyekt_VALUE(obyekt_İstinad, 29)) return;
            if (Söz_SMS(ad_sabit, "getSource") && Söz_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[obyekt_İstinad + 2], 2);
            else if (Söz_SMS(ad_sabit, "getActionCommand") && Söz_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[obyekt_İstinad + 2]), 2);
            else if (Söz_SMS(ad_sabit, "getID") && Söz_SMS(서술상수, "()I")) 넣기(1001, 1);
            else xəta_VALUE("unsupported ActionEvent method"); return;
        }
        if (əmr_kod == 183 && Söz_SMS(ad_sabit, "<init>")) {
            int COLUMNS = 0, SMS_İstinad = 0;
            if (Söz_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Söz_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_İstinad = 빼기(2); }
            else if (Söz_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_İstinad = 빼기(2);
            else if (Söz_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Söz_SMS(서술상수, "()V")) { xəta_VALUE("unsupported Swing constructor"); return; }
            int obyekt_İstinad = 빼기(2); if (!객체유효(obyekt_İstinad)) return;
            if (힙[obyekt_İstinad] == 30) { xəta_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(obyekt_İstinad) || COLUMNS < 0) return;
            int hesab_VALUE = istifadəçi.화면연결(0, 힙[obyekt_İstinad] - 23, 0, 0, 0, 0);
            if (hesab_VALUE < 1 || hesab_VALUE > 32) { xəta_VALUE("GUI widget slots exhausted"); return; }
            힙[obyekt_İstinad + 2] = hesab_VALUE; 화면참조[hesab_VALUE - 1] = obyekt_İstinad; 힙[obyekt_İstinad + 5] = 힙[obyekt_İstinad] == 24 ? 130 : 16; 힙[obyekt_İstinad + 6] = 힙[obyekt_İstinad] == 24 ? 110 : 16;
            힙[obyekt_İstinad + 7] = 힙[obyekt_İstinad] == 24 ? 380 : 220; 힙[obyekt_İstinad + 8] = 힙[obyekt_İstinad] == 24 ? 240 : 28; 힙[obyekt_İstinad + 10] = 1;
            화면문자설정(obyekt_İstinad, SMS_İstinad); return;
        }
        if (Söz_SMS(ad_sabit, "setText") || Söz_SMS(ad_sabit, "setTitle")) { int SMS_İstinad = 빼기(2), obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad) && Söz_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(obyekt_İstinad, SMS_İstinad); return; }
        if (Söz_SMS(ad_sabit, "getText") || Söz_SMS(ad_sabit, "getTitle")) { int obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad) && Söz_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(obyekt_İstinad), 2); return; }
        if (Söz_SMS(ad_sabit, "addActionListener") && Söz_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad)) { 힙[obyekt_İstinad + 4] = 수신참조; 힙참조[obyekt_İstinad + 4] = 1; } return; }
        if (Söz_SMS(ad_sabit, "getContentPane") && Söz_SMS(서술상수, "()Ljava/awt/Container;")) { int obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad)) 넣기(obyekt_İstinad, 2); return; }
        if (Söz_SMS(ad_sabit, "setLayout") && Söz_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Düzüm_İstinad = 빼기(2), obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad) && Düzüm_İstinad != 0) xəta_VALUE("only absolute layout (null) is supported"); return; }
        if (Söz_SMS(ad_sabit, "add") && (Söz_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Söz_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Düzüm_şərt = Söz_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Düzüm_şərt) 빼기(2);
            int uşaq_İstinad = 빼기(2), obyekt_İstinad = 빼기(2); if (!화면객체(uşaq_İstinad) || !화면객체(obyekt_İstinad)) return;
            if (istifadəçi.화면연결(2, 힙[obyekt_İstinad + 2], 힙[uşaq_İstinad + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[uşaq_İstinad + 11] = obyekt_İstinad; 힙참조[uşaq_İstinad + 11] = 1; if (!Düzüm_şərt) 넣기(uşaq_İstinad, 2); return;
        }
        if (Söz_SMS(ad_sabit, "setBounds") && Söz_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinatı = 빼기(1), obyekt_İstinad = 빼기(2); if (!화면객체(obyekt_İstinad)) return;
            if (istifadəçi.화면연결(1, 힙[obyekt_İstinad + 2], x_koordinatı, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[obyekt_İstinad + 5] = x_koordinatı; 힙[obyekt_İstinad + 6] = Y_koordinat; 힙[obyekt_İstinad + 7] = 너비; 힙[obyekt_İstinad + 8] = 높이; return;
        }
        if (Söz_SMS(ad_sabit, "setSize") && Söz_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), obyekt_İstinad = 빼기(2); if (!화면객체(obyekt_İstinad)) return;
            if (istifadəçi.화면연결(1, 힙[obyekt_İstinad + 2], 힙[obyekt_İstinad + 5], 힙[obyekt_İstinad + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[obyekt_İstinad + 7] = 너비; 힙[obyekt_İstinad + 8] = 높이; } return;
        }
        if (Söz_SMS(ad_sabit, "setLocationRelativeTo") && Söz_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), obyekt_İstinad = 빼기(2); if (!화면객체(obyekt_İstinad)) return; if (상대배치 != 0) { xəta_VALUE("only screen centering supported"); return; } 힙[obyekt_İstinad + 5] = (istifadəçi.화면너비() - 힙[obyekt_İstinad + 7]) / 2; 힙[obyekt_İstinad + 6] = (istifadəçi.화면높이() - 힙[obyekt_İstinad + 8]) / 2; istifadəçi.화면연결(1, 힙[obyekt_İstinad + 2], 힙[obyekt_İstinad + 5], 힙[obyekt_İstinad + 6], 힙[obyekt_İstinad + 7], 힙[obyekt_İstinad + 8]); return; }
        if (Söz_SMS(ad_sabit, "setDefaultCloseOperation") && Söz_SMS(서술상수, "(I)V")) { int siyasət = 빼기(1), obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad)) { if (siyasət < 0 || siyasət > 3) 예외던짐(9, "close policy"); else { 힙[obyekt_İstinad + 10] = siyasət; istifadəçi.화면연결(7, 힙[obyekt_İstinad + 2], siyasət, 0, 0, 0); } } return; }
        if (Söz_SMS(ad_sabit, "setVisible") && Söz_SMS(서술상수, "(Z)V")) { int verilənlər_VALUE = 빼기(1), obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad)) { int 처리값 = istifadəçi.화면연결(3, 힙[obyekt_İstinad + 2], verilənlər_VALUE, 0, 0, 0); if (처리값 < 0) xəta_VALUE("Swing requires a standalone interactive command"); else 힙[obyekt_İstinad + 9] = verilənlər_VALUE; } return; }
        if (Söz_SMS(ad_sabit, "dispose") && Söz_SMS(서술상수, "()V")) { int obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad)) { istifadəçi.화면연결(4, 힙[obyekt_İstinad + 2], 0, 0, 0, 0); 힙[obyekt_İstinad + 9] = 0; } return; }
        if (Söz_SMS(ad_sabit, "repaint") || Söz_SMS(ad_sabit, "validate")) { int obyekt_İstinad = 빼기(2); if (!화면객체(obyekt_İstinad) || !Söz_SMS(서술상수, "()V")) return; istifadəçi.화면연결(1, 힙[obyekt_İstinad + 2], 힙[obyekt_İstinad + 5], 힙[obyekt_İstinad + 6], 힙[obyekt_İstinad + 7], 힙[obyekt_İstinad + 8]); return; }
        if (Söz_SMS(ad_sabit, "isVisible") && Söz_SMS(서술상수, "()Z")) { int obyekt_İstinad = 빼기(2); if (화면객체(obyekt_İstinad)) 넣기(힙[obyekt_İstinad + 9], 1); return; }
        xəta_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int hədəf_ünvan, int 사건번호, boolean 한국어) {
        if (hədəf_ünvan < 1 || 힙[hədəf_ünvan] < 32) { xəta_VALUE("Java event listener required"); return; }
        int fayl_INDEX = ad_metod(힙[hədəf_ünvan] - 32, 사건번호 == 0 ? (한국어 ? "icra_etmək_tapşırıq" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fayl_INDEX < 0) { xəta_VALUE("event callback missing"); return; }
        현재가닥 = 0; axın_COUNT = 1; kadr_INDEX = 0; axın_vəziyyət[0] = 1; kadr_Yığın[0] = 0; 틀잠금[0] = ilkin_qiymət_vermək_kadr[0] = 0; dəyişdirmək_HTTP_sorğusu = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokal_VALUE[Loop_INDEX] = lokal_TYPE[Loop_INDEX] = 0; }
        kadr_metod[0] = fayl_INDEX; kadr_yerinə_qoymaq[0] = metod_Başla[fayl_INDEX]; lokal_VALUE[0] = hədəf_ünvan; lokal_TYPE[0] = 2;
        if (사건번호 != 0) { lokal_VALUE[1] = 사건번호; lokal_TYPE[1] = 2; }
        사건중 = true; icra_etmək_əmr(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!XƏTA) {
            if (나중수 > 0) { int hədəf_ünvan = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(hədəf_ünvan, 0, 한국어 != 0); continue; }
            if (istifadəçi.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = istifadəçi.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { xəta_VALUE("GUI event I/O failed"); return; }
            int hesab_VALUE = 사건번호 & 65535; if (hesab_VALUE < 1 || hesab_VALUE > 32) continue; int obyekt_İstinad = 화면참조[hesab_VALUE - 1]; if (obyekt_İstinad == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[obyekt_İstinad + 10] != 0) 힙[obyekt_İstinad + 9] = 0;
                if (힙[obyekt_İstinad + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) istifadəçi.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[obyekt_İstinad + 4] != 0) {
                int OXUMƏNİ_İstinad = ayırmaq_Yaddaş(29, 2); if (XƏTA) return; 힙[OXUMƏNİ_İstinad + 2] = obyekt_İstinad; 힙[OXUMƏNİ_İstinad + 3] = 힙[obyekt_İstinad + 12]; 힙참조[OXUMƏNİ_İstinad + 2] = 1; 사건실행(힙[obyekt_İstinad + 4], OXUMƏNİ_İstinad, 힙[obyekt_İstinad + 12] != 0);
            }
        }
    }
    public static int İcra_Et() {
        if (istifadəçi.인수개수() == 1 && 자바도구.같음(istifadəçi.인수(0), "-version")) {
            istifadəçi.Yazma("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (istifadəçi.인수개수() < 1) { istifadəçi.Yazma("Usage: java CLASS [ARGS]\n"); return 2; }
        daxiletmə_Sinif_Tərif = yüklə_Sinif_Tərif(host_simvol(istifadəçi.인수(0))); if (XƏTA || daxiletmə_Sinif_Tərif < 0) return 1;
        int daxiletmə_p_VALUE = ad_metod(daxiletmə_Sinif_Tərif, "İcra_Et", "()V");
        boolean 한국어진입 = daxiletmə_p_VALUE >= 0 && (metod_müraciət[daxiletmə_p_VALUE] & 9) == 9;
        if (!한국어진입) daxiletmə_p_VALUE = ad_metod(daxiletmə_Sinif_Tərif, "main", "([Ljava/lang/String;)V");
        if (daxiletmə_p_VALUE < 0 || (metod_müraciət[daxiletmə_p_VALUE] & 9) != 9) xəta_VALUE("public static void İcra_Et() or main(String[] args) required");
        if (XƏTA) return 1;
        int 인수 = ayırmaq_Yaddaş(3, istifadəçi.인수개수() - 1); ARRAY_element[인수] = -1;
        for (int 수 = 1; 수 < istifadəçi.인수개수() && !XƏTA; 수++) 힙[인수 + 1 + 수] = host_simvol(istifadəçi.인수(수));
        kadr_INDEX = 0; kadr_metod[0] = daxiletmə_p_VALUE; kadr_yerinə_qoymaq[0] = metod_Başla[daxiletmə_p_VALUE]; lokal_VALUE[0] = 한국어진입 ? 0 : 인수; lokal_TYPE[0] = 한국어진입 ? 0 : 2;
        axın_vəziyyət[0] = 1; axın_obyekt[0] = ayırmaq_Yaddaş(13, 2);
        icra_etmək_əmr(); if (!XƏTA) 화면사건들(); return XƏTA ? 1 : 0;
    }
}
