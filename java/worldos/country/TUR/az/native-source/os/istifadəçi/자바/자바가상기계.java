// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. FAYL/스택/İstinad/qol 경계를 icra_etmək_əmr 중 검사한다. */
public final class 자바가상기계 {
    static int[] FAYL = new int[16384], fayl_ad_SMS = new int[64];
    static int[] sabit_teq = new int[512], 상가 = new int[512], sabit_SECOND_VALUE = new int[512], sətir_İstinad = new int[512];
    static int[] metod_ad_SMS = new int[32], metod_TYPE = new int[32], metod_müraciət = new int[32];
    static int[] metod_Başla = new int[32], metod_bitirmək = new int[32], metod_Yığın = new int[32], 함수지역 = new int[32];
    static int[] metod_arqument_COUNT = new int[32], metod_arqument_TYPE = new int[512], metod_geri_qaytarmaq = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokal_VALUE = new int[4096], lokal_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] kadr_metod = new int[32], kadr_yerinə_qoymaq = new int[32], kadr_Yığın = new int[32];
    static int[] 힙 = new int[8192];
    static int Böyüklük, 읽기위치, sabit_COUNT, metod_COUNT, Sinif_ad, kadr_INDEX = -1, 힙끝 = 1, geri_qaytarmaq_TYPE;
    static boolean XƏTA;

    static void xəta_VALUE(String Söz_SMS) {
        if (!XƏTA) { istifadəçi.Yazma("JVM error: "); istifadəçi.Yazma(Söz_SMS); istifadəçi.yazmaq_simvol_VALUE(10); }
        XƏTA = true;
    }
    static boolean klip(int İcra_Et, int uzunluq_VALUE) { return İcra_Et >= 0 && uzunluq_VALUE >= 0 && İcra_Et <= Böyüklük - uzunluq_VALUE; }
    static int bayt_VALUE() {
        if (!klip(읽기위치, 1)) { xəta_VALUE("truncated class file"); return 0; }
        return FAYL[읽기위치++];
    }
    static int 짧은수() { return bayt_VALUE() << 8 | bayt_VALUE(); }
    static int tam_ədəd() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int uzunluq_VALUE) { if (!klip(읽기위치, uzunluq_VALUE)) xəta_VALUE("invalid attribute size"); else 읽기위치 += uzunluq_VALUE; }
    static boolean çek_sabit(int 수, int 종류) {
        if (수 <= 0 || 수 >= sabit_COUNT || sabit_teq[수] != 종류) { xəta_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int İcra_Et, int uzunluq_VALUE, String Söz_SMS) {
        if (!klip(İcra_Et, uzunluq_VALUE) || uzunluq_VALUE != Söz_SMS.length()) return false;
        for (int 수 = 0; 수 < uzunluq_VALUE; 수++) if (FAYL[İcra_Et + 수] != Söz_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !XƏTA; 수++) { çek_sabit(짧은수(), 1); 건너(tam_ədəd()); }
    }
    static int əmr_uzunluq(int VALUE) {
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
        if (tam_ədəd() != 0xcafebabe) xəta_VALUE("not a class file");
        int 부판 = 짧은수(), versiya_VALUE = 짧은수();
        if (versiya_VALUE < 45 || versiya_VALUE > 52 || 부판 != 0) xəta_VALUE("supported class versions: 45..52, minor 0");
        sabit_COUNT = 짧은수();
        if (sabit_COUNT < 1 || sabit_COUNT > 512) { xəta_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < sabit_COUNT && !XƏTA; 수++) {
            int 종류 = bayt_VALUE(); sabit_teq[수] = 종류;
            if (종류 == 1) { sabit_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(sabit_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = tam_ədəd();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); sabit_SECOND_VALUE[수] = 짧은수(); }
            else xəta_VALUE("unsupported constant type");
        }
        int icazə_VALUE = 짧은수();
        if ((icazə_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) xəta_VALUE("unsupported class flags");
        Sinif_ad = Sinif_ad_SMS(짧은수());
        if (!Söz_SMS(Sinif_ad_SMS(짧은수()), "java/lang/Object")) xəta_VALUE("inheritance unsupported");
        if (짧은수() != 0) xəta_VALUE("interfaces unsupported");
        if (짧은수() != 0) xəta_VALUE("fields unsupported");
        metod_COUNT = 짧은수();
        if (metod_COUNT < 1 || metod_COUNT > 32) { xəta_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metod_COUNT && !XƏTA; 수++) {
            metod_müraciət[수] = 짧은수(); metod_ad_SMS[수] = 짧은수(); metod_TYPE[수] = 짧은수();
            çek_sabit(metod_ad_SMS[수], 1); 서술읽기(수);
            if ((metod_müraciət[수] & (0x100 | 0x400 | 0x20)) != 0) xəta_VALUE("native, abstract and synchronized methods unsupported");
            if ((metod_müraciət[수] & 8) == 0 && !Söz_SMS(metod_ad_SMS[수], "<init>")) xəta_VALUE("instance methods unsupported");
            if (Söz_SMS(metod_ad_SMS[수], "<clinit>")) xəta_VALUE("class initializers unsupported");
            for (int ön_VALUE = 0; ön_VALUE < 수; ön_VALUE++) if (같은말(metod_ad_SMS[ön_VALUE], metod_ad_SMS[수]) && 같은말(metod_TYPE[ön_VALUE], metod_TYPE[수])) xəta_VALUE("duplicate method");
            int element_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < element_COUNT && !XƏTA; atribut_VALUE++) {
                int Ad = 짧은수(), uzunluq_VALUE = tam_ədəd(), İcra_Et = 읽기위치;
                if (!klip(İcra_Et, uzunluq_VALUE)) { xəta_VALUE("truncated method attribute"); break; }
                if (Söz_SMS(Ad, "Code")) {
                    if (metod_Başla[수] != 0) xəta_VALUE("duplicate Code attribute");
                    metod_Yığın[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_uzunluq = tam_ədəd();
                    if (metod_Yığın[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metod_arqument_COUNT[수]
                        || kod_uzunluq < 1 || kod_uzunluq > 8192) xəta_VALUE("method memory limits exceeded");
                    metod_Başla[수] = 읽기위치; 건너(kod_uzunluq); metod_bitirmək[수] = 읽기위치;
                    if (짧은수() != 0) xəta_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != İcra_Et + uzunluq_VALUE) xəta_VALUE("Code attribute size mismatch");
                } else 건너(uzunluq_VALUE);
            }
            if (metod_Başla[수] == 0) xəta_VALUE("missing Code attribute");
            int slot_daxiletmə = metod_Başla[수];
            while (slot_daxiletmə < metod_bitirmək[수] && !XƏTA) {
                int uzunluq_VALUE = əmr_uzunluq(FAYL[slot_daxiletmə]);
                if (uzunluq_VALUE == 0 || uzunluq_VALUE > metod_bitirmək[수] - slot_daxiletmə) { xəta_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_daxiletmə] = 수 + 1; slot_daxiletmə += uzunluq_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 qol 목적지를 허용하지 않는다.
            slot_daxiletmə = metod_Başla[수];
            while (slot_daxiletmə < metod_bitirmək[수] && !XƏTA) {
                int VALUE = FAYL[slot_daxiletmə];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int təyinat_VALUE_a0fbc067 = slot_daxiletmə + (short)(FAYL[slot_daxiletmə + 1] << 8 | FAYL[slot_daxiletmə + 2]);
                    if (təyinat_VALUE_a0fbc067 < metod_Başla[수] || təyinat_VALUE_a0fbc067 >= metod_bitirmək[수] || 경계[təyinat_VALUE_a0fbc067] != 수 + 1) xəta_VALUE("invalid branch target");
                }
                slot_daxiletmə += əmr_uzunluq(VALUE);
            }
        }
        if (!XƏTA) 속성건너();
        if (읽기위치 != Böyüklük) xəta_VALUE("extra class file data");
    }
    static int ayırmaq_Yaddaş(int 종류, int uzunluq_VALUE) {
        if (uzunluq_VALUE < 0 || uzunluq_VALUE > 힙.length - 힙끝 - 2) { xəta_VALUE("object heap exhausted or negative array size"); return 0; }
        int İstinad = 힙끝; 힙끝 += uzunluq_VALUE + 2; 힙[İstinad] = 종류; 힙[İstinad + 1] = uzunluq_VALUE;
        return İstinad;
    }
    static boolean obyekt_VALUE(int İstinad, int 종류) {
        if (İstinad < 1 || İstinad >= 힙끝 - 1 || 힙[İstinad] != 종류) { xəta_VALUE("null or invalid object reference"); return false; }
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
        if (kadr_INDEX == 31) { xəta_VALUE("call stack limit (32)"); return; }
        int Sonrakı_element = kadr_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Sonrakı_element * 128 + 수] = 0;
        for (int 수 = metod_arqument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Sonrakı_element * 128 + 수] = 빼기(metod_arqument_TYPE[FUNCTION_VALUE * 16 + 수]); lokal_TYPE[Sonrakı_element * 128 + 수] = metod_arqument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        kadr_INDEX = Sonrakı_element; kadr_metod[kadr_INDEX] = FUNCTION_VALUE; kadr_yerinə_qoymaq[kadr_INDEX] = metod_Başla[FUNCTION_VALUE]; kadr_Yığın[kadr_INDEX] = 0;
    }
    static void geri_qaytarmaq_ölçü(int TYPE_VALUE) {
        if (TYPE_VALUE != metod_geri_qaytarmaq[kadr_metod[kadr_INDEX]]) { xəta_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        kadr_INDEX--; if (kadr_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { xəta_VALUE("file stream paths currently require ASCII"); return; }
                axın_fayl_ad[slot_daxiletmə] = VALUE;
            }
            axın_fayl_ad[uzunluq_VALUE] = 0;
            int 서술자 = istifadəçi.파일서술자열기(axın_fayl_ad, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { xəta_VALUE("FileNotFoundException: file open failed"); return; }
            힙[axın_VALUE + 2] = 서술자; 힙[axın_VALUE + 3] = 1;
            return;
        }
        if (Əmr != 182) { xəta_VALUE("invalid file stream invocation"); return; }
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
            if (ölçü < -1) xəta_VALUE("IOException: read failed"); else 넣기(ölçü, 1);
        } else if (istifadəçi.파일한바이트쓰기(서술자, VALUE) != 1) xəta_VALUE("IOException: write failed");
    }
    static void CALL_metod(int INDEX, int Əmr) {
        if (!çek_sabit(INDEX, 10)) return;
        int sahib_VALUE = Sinif_ad_SMS(상가[INDEX]), Ad = İstinad_ad(sabit_SECOND_VALUE[INDEX]), format_VALUE = İstinad_TYPE(sabit_SECOND_VALUE[INDEX]);
        if (XƏTA) return;
        if (같은말(sahib_VALUE, Sinif_ad)) {
            if (Əmr != 184) { xəta_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metod_COUNT; 수++) if (같은말(Ad, metod_ad_SMS[수]) && 같은말(format_VALUE, metod_TYPE[수])) {
                if ((metod_müraciət[수] & 8) == 0) xəta_VALUE("method is not static"); else 호출(수);
                return;
            }
            xəta_VALUE("NoSuchMethodError"); return;
        }
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
        xəta_VALUE("unsupported library method");
    }
    static int ARRAY_slot(int İstinad, int aşağı_indeks_VALUE, int TYPE_VALUE) {
        if (!obyekt_VALUE(İstinad, TYPE_VALUE)) return 0;
        if (aşağı_indeks_VALUE < 0 || aşağı_indeks_VALUE >= 힙[İstinad + 1]) { xəta_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return İstinad + 2 + aşağı_indeks_VALUE;
    }
    static void icra_etmək_əmr() {
        int 남음 = 500000;
        while (kadr_INDEX >= 0 && !XƏTA) {
            if (--남음 == 0) { xəta_VALUE("instruction limit (500000)"); break; }
            int İcra_Et = kadr_yerinə_qoymaq[kadr_INDEX], VALUE = 명바();
            if (XƏTA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= sabit_COUNT) xəta_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int aşağı_indeks_VALUE = 빼기(1), İstinad = 빼기(2), slot_daxiletmə = ARRAY_slot(İstinad, aşağı_indeks_VALUE, VALUE == 46 ? 2 : 3);
                if (!XƏTA) 넣기(힙[slot_daxiletmə], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int element_element = 빼기(VALUE == 79 ? 1 : 2), aşağı_indeks_VALUE = 빼기(1), İstinad = 빼기(2), slot_daxiletmə = ARRAY_slot(İstinad, aşağı_indeks_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && element_element != 0) obyekt_VALUE(element_element, 1);
                if (!XƏTA) 힙[slot_daxiletmə] = element_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = geri_qaytarmaq_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = geri_qaytarmaq_TYPE, 나 = 빼기(0), 나형 = geri_qaytarmaq_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!çek_sabit(수, 9)) continue;
                if (!Söz_SMS(Sinif_ad_SMS(상가[수]), "java/lang/System") || !Söz_SMS(İstinad_ad(sabit_SECOND_VALUE[수]), "out")
                    || !Söz_SMS(İstinad_TYPE(sabit_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) xəta_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metod(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Ad = Sinif_ad_SMS(명짧());
                if (Söz_SMS(Ad, "java/lang/StringBuilder")) 넣기(ayırmaq_Yaddaş(4, 1), 2);
                else if (Söz_SMS(Ad, "java/io/FileInputStream") || Söz_SMS(Ad, "java/io/FileOutputStream")) {
                    int İstinad = ayırmaq_Yaddaş(Söz_SMS(Ad, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!XƏTA) { 힙[İstinad + 2] = -1; 넣기(İstinad, 2); }
                } else xəta_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) xəta_VALUE("only int[] newarray is supported"); }
                else if (!Söz_SMS(Sinif_ad_SMS(명짧()), "java/lang/String")) xəta_VALUE("only String[] anewarray is supported");
                int uzunluq_VALUE = 빼기(1); 넣기(ayırmaq_Yaddaş(VALUE == 188 ? 2 : 3, uzunluq_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int İstinad = 빼기(2);
                if (İstinad < 1 || İstinad >= 힙끝 - 1 || (힙[İstinad] != 2 && 힙[İstinad] != 3)) xəta_VALUE("null or invalid array");
                else 넣기(힙[İstinad + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Ad = Sinif_ad_SMS(명짧()), İstinad = 빼기(2);
                if (!Söz_SMS(Ad, "java/lang/String")) xəta_VALUE("unsupported checkcast");
                else if (İstinad != 0) obyekt_VALUE(İstinad, 1);
                넣기(İstinad, 2); continue;
            }
            xəta_VALUE("unsupported bytecode");
        }
    }
    public static int İcra_Et() {
        if (istifadəçi.인수개수() == 1 && 자바도구.같음(istifadəçi.인수(0), "-version")) {
            istifadəçi.Yazma("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (istifadəçi.인수개수() < 1) { istifadəçi.Yazma("Usage: java CLASS [ARGS]\n"); return 2; }
        int uzunluq_VALUE = 자바도구.Ad(fayl_ad_SMS, istifadəçi.인수(0));
        if (uzunluq_VALUE < 1 || uzunluq_VALUE > 57) { istifadəçi.Yazma("java: invalid class name\n"); return 2; }
        fayl_ad_SMS[uzunluq_VALUE] = '.'; fayl_ad_SMS[uzunluq_VALUE + 1] = 'c'; fayl_ad_SMS[uzunluq_VALUE + 2] = 'l'; fayl_ad_SMS[uzunluq_VALUE + 3] = 'a'; fayl_ad_SMS[uzunluq_VALUE + 4] = 's'; fayl_ad_SMS[uzunluq_VALUE + 5] = 's';
        Böyüklük = istifadəçi.파일읽기(fayl_ad_SMS, FAYL);
        if (Böyüklük < 0) { istifadəçi.Yazma("java: cannot read class: "); 자바도구.수쓰기(Böyüklük); istifadəçi.yazmaq_simvol_VALUE(10); return 1; }
        클래스읽기(); if (XƏTA) return 1;
        int simvol_ad = sabit_SMS(Sinif_ad);
        if (!XƏTA && 힙[simvol_ad + 1] != uzunluq_VALUE) xəta_VALUE("class name does not match file");
        for (int 수 = 0; 수 < uzunluq_VALUE && !XƏTA; 수++) if (힙[simvol_ad + 2 + 수] != fayl_ad_SMS[수]) xəta_VALUE("class name does not match file");
        int daxiletmə_p_VALUE = -1;
        for (int 수 = 0; 수 < metod_COUNT; 수++) if (Söz_SMS(metod_ad_SMS[수], "main") && Söz_SMS(metod_TYPE[수], "([Ljava/lang/String;)V") && (metod_müraciət[수] & 9) == 9) daxiletmə_p_VALUE = 수;
        if (daxiletmə_p_VALUE < 0) xəta_VALUE("public static void main(String[] args) required");
        if (XƏTA) return 1;
        int 인수 = ayırmaq_Yaddaş(3, istifadəçi.인수개수() - 1);
        for (int 수 = 1; 수 < istifadəçi.인수개수() && !XƏTA; 수++) 힙[인수 + 1 + 수] = host_simvol(istifadəçi.인수(수));
        kadr_INDEX = 0; kadr_metod[0] = daxiletmə_p_VALUE; kadr_yerinə_qoymaq[0] = metod_Başla[daxiletmə_p_VALUE]; lokal_VALUE[0] = 인수; lokal_TYPE[0] = 2;
        icra_etmək_əmr(); return XƏTA ? 1 : 0;
    }
}
