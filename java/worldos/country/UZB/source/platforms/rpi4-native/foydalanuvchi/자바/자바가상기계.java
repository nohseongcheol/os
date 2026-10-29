// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fayl/스택/Ma_lumotnomalar/shox 경계를 bajarmoq_buyruq 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fayl = new int[16 * 16384], 임시파일 = new int[16384], fayl_nom_SMS = new int[512];
    static int[] konstanta_teg = new int[8192], 상가 = new int[8192], konstanta_SECOND_VALUE = new int[8192], satr_Ma_lumotnomalar = new int[8192];
    static int[] uslub_nom_SMS = new int[512], uslub_TYPE = new int[512], uslub_kirish_huquqi = new int[512], uslub_egasi = new int[512];
    static int[] uslub_Start = new int[512], uslub_to_xtatmoq = new int[512], uslub_Stack = new int[512], 함수지역 = new int[512];
    static int[] uslub_dalil_COUNT = new int[512], uslub_dalil_TYPE = new int[8192], uslub_qaytarish = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] mahalliy_VALUE = new int[16384], mahalliy_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] kadr_uslub = new int[128], kadr_holat = new int[128], kadr_Stack = new int[128], kadr_qo_llanma = new int[128], ishga_tushirmoq_kadr = new int[128];
    static int[] Sinf_Izoh_nom = new int[16], Sinf_Izoh_o_lcham = new int[16], 종부모 = new int[16], Sinf_Izoh_holat = new int[16], Sinf_in_COUNT = new int[16], ishga_tushirmoq_Sinf_Izoh = new int[16];
    static int[] Sinf_interfeys = new int[16 * 16], Sinf_interfeys_COUNT = new int[16];
    static int[] in_nom = new int[512], in_TYPE = new int[512], in_egasi = new int[512], in_Ruxsatlar = new int[512], in_holat = new int[512], in_ma_lumotlar = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_element = new int[32768], Store_butun_son = new int[256];
    static int Hajmi, 읽기위치, uslub_COUNT, Sinf_nom, kadr_INDEX = -1, 힙끝 = 1, qaytarish_TYPE;
    static int Sinf_Izoh_COUNT, in_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, ekran_COUNT, To_plam_COUNT;
    static int 현재가닥, oqim_COUNT = 1, kiritish_Sinf_Izoh;
    static int[] oqim_kadr = new int[4], oqim_holat = new int[4], oqim_obyekt = new int[4], oqim_maqsad = new int[4], 가닥대기 = new int[4];
    static boolean Xato, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], Sinf_oqim = new int[16];

    static void to_xtab_qolish_VALUE(String Word_SMS) {
        if (Xato) return;
        int toifa_kod = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) toifa_kod = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) toifa_kod = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) toifa_kod = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) toifa_kod = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) toifa_kod = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) toifa_kod = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) toifa_kod = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) toifa_kod = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) toifa_kod = 15;
        if (toifa_kod != 0 && kadr_INDEX >= 0) { 예외던짐(toifa_kod, Word_SMS); return; }
        foydalanuvchi.Yozish("JVM error: "); foydalanuvchi.Yozish(Word_SMS); foydalanuvchi.yozmoq_belgi_VALUE(10); Xato = true;
    }
    static boolean klip(int Bajarish, int uzunlik_VALUE) {
        if (Bajarish < 0 || Bajarish >= Fayl.length || uzunlik_VALUE < 0) return false;
        int Sinf_Izoh = Bajarish / 16384;
        return Bajarish % 16384 <= Sinf_Izoh_o_lcham[Sinf_Izoh] && uzunlik_VALUE <= Sinf_Izoh_o_lcham[Sinf_Izoh] - Bajarish % 16384;
    }
    static int bayt_VALUE() {
        if (!klip(읽기위치, 1)) { to_xtab_qolish_VALUE("truncated class file"); return 0; }
        return Fayl[읽기위치++];
    }
    static int 짧은수() { return bayt_VALUE() << 8 | bayt_VALUE(); }
    static int butun_son() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int uzunlik_VALUE) { if (!klip(읽기위치, uzunlik_VALUE)) to_xtab_qolish_VALUE("invalid attribute size"); else 읽기위치 += uzunlik_VALUE; }
    static boolean chek_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_teg.length || konstanta_teg[수] != 종류) { to_xtab_qolish_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Bajarish, int uzunlik_VALUE, String Word_SMS) {
        if (!klip(Bajarish, uzunlik_VALUE)) return false;
        int 읽는자리 = Bajarish, 끝 = Bajarish + uzunlik_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int belgi_kodi = Word_SMS.charAt(Loop_INDEX);
            if (belgi_kodi > 0 && belgi_kodi < 128) { if (읽는자리 >= 끝 || Fayl[읽는자리++] != belgi_kodi) return false; }
            else if (belgi_kodi < 2048) {
                if (읽는자리 + 2 > 끝 || Fayl[읽는자리++] != (192 | (belgi_kodi >> 6)) || Fayl[읽는자리++] != (128 | (belgi_kodi & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fayl[읽는자리++] != (224 | (belgi_kodi >> 12)) || Fayl[읽는자리++] != (128 | ((belgi_kodi >> 6) & 63)) || Fayl[읽는자리++] != (128 | (belgi_kodi & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return chek_konstanta(konstanta_VALUE, 1) && 구간(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!chek_konstanta(가, 1) || !chek_konstanta(나, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < konstanta_SECOND_VALUE[가]; 수++) if (Fayl[상가[가] + 수] != Fayl[상가[나] + 수]) return false;
        return true;
    }
    static int Sinf_nom_SMS(int 수) { return chek_konstanta(수, 7) && chek_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Ma_lumotnomalar_nom(int 수) { return chek_konstanta(수, 12) && chek_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Ma_lumotnomalar_TYPE(int 수) { return chek_konstanta(수, 12) && chek_konstanta(konstanta_SECOND_VALUE[수], 1) ? konstanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean bo_sh_TYPE) {
        if (읽기위치 >= 끝) { to_xtab_qolish_VALUE("invalid descriptor"); return 0; }
        int VALUE = bayt_VALUE();
        if (VALUE == 'V' && bo_sh_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Bajarish = 읽기위치;
            while (읽기위치 < 끝 && Fayl[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Bajarish) to_xtab_qolish_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        to_xtab_qolish_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = uslub_TYPE[FUNCTION_VALUE];
        if (!chek_konstanta(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[수];
        if (bayt_VALUE() != '(') to_xtab_qolish_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!Xato && 읽기위치 < 끝 && Fayl[읽기위치] != ')') {
            if (element_COUNT == 16) { to_xtab_qolish_VALUE("too many method arguments"); break; }
            uslub_dalil_TYPE[FUNCTION_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bayt_VALUE() != ')') to_xtab_qolish_VALUE("invalid method descriptor");
        uslub_qaytarish[FUNCTION_VALUE] = 서술형(끝, true); uslub_dalil_COUNT[FUNCTION_VALUE] = element_COUNT;
        if (읽기위치 != 끝) to_xtab_qolish_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return uslub_egasi[kadr_uslub[kadr_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !Xato; 수++) { chek_konstanta(상번호(), 1); 건너(butun_son()); }
    }
    static int buyruq_uzunlik(int VALUE) {
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
    static int holat_butun_son(int 읽는자리) {
        if (!klip(읽는자리, 4)) { to_xtab_qolish_VALUE("truncated bytecode operand"); return 0; }
        return Fayl[읽는자리] << 24 | Fayl[읽는자리 + 1] << 16 | Fayl[읽는자리 + 2] << 8 | Fayl[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Bajarish, int 끝) {
        int VALUE = Fayl[읽는자리], uzunlik_VALUE = buyruq_uzunlik(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_holat = 읽는자리 + 1;
            while ((BASE_holat - Bajarish) % 4 != 0) BASE_holat++;
            if (끝 - BASE_holat < (VALUE == 170 ? 12 : 8)) return 0;
            int kiritish_COUNT = VALUE == 170 ? holat_butun_son(BASE_holat + 8) - holat_butun_son(BASE_holat + 4) + 1 : holat_butun_son(BASE_holat + 4);
            if (kiritish_COUNT < 0 || kiritish_COUNT > 2048) return 0;
            uzunlik_VALUE = BASE_holat - 읽는자리 + (VALUE == 170 ? 12 + 4 * kiritish_COUNT : 8 + 8 * kiritish_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_ma_lumotlar = Fayl[읽는자리 + 1]; uzunlik_VALUE = Word_ma_lumotlar == 132 ? 6 : (Word_ma_lumotlar == 21 || Word_ma_lumotlar == 25 || Word_ma_lumotlar == 54 || Word_ma_lumotlar == 58) ? 4 : 0;
        }
        return uzunlik_VALUE > 0 && uzunlik_VALUE <= 끝 - 읽는자리 ? uzunlik_VALUE : 0;
    }
    static void chek_ko_chirish_joyi_VALUE(int ko_chirish_joyi_VALUE, int FUNCTION_VALUE) {
        if (ko_chirish_joyi_VALUE < uslub_Start[FUNCTION_VALUE] || ko_chirish_joyi_VALUE >= uslub_to_xtatmoq[FUNCTION_VALUE] || 경계[ko_chirish_joyi_VALUE] != FUNCTION_VALUE + 1) to_xtab_qolish_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Sinf_Izoh) {
        현재읽는종 = Sinf_Izoh; 읽기위치 = Sinf_Izoh * 16384; Hajmi = 읽기위치 + Sinf_Izoh_o_lcham[Sinf_Izoh];
        if (butun_son() != 0xcafebabe) { to_xtab_qolish_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versiya_VALUE = 짧은수();
        if (versiya_VALUE < 45 || versiya_VALUE > 52 || 부판 != 0) { to_xtab_qolish_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstanta_COUNT = 짧은수(), BASE_holat = Sinf_Izoh * 512;
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { to_xtab_qolish_VALUE("constant pool limit (511)"); return; }
        for (int kiritish_COUNT = 1; kiritish_COUNT < konstanta_COUNT && !Xato; kiritish_COUNT++) {
            int 수 = BASE_holat + kiritish_COUNT, 종류 = bayt_VALUE(); konstanta_teg[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = butun_son();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstanta_SECOND_VALUE[수] = 상번호(); }
            else to_xtab_qolish_VALUE("unsupported constant type");
        }
        int ruxsat_VALUE_a9fa0dfa = 짧은수();
        if ((ruxsat_VALUE_a9fa0dfa & (0x2000 | 0x4000)) != 0) to_xtab_qolish_VALUE("annotation/enum class unsupported");
        Sinf_Izoh_nom[Sinf_Izoh] = Sinf_nom_SMS(상번호());
        종부모[Sinf_Izoh] = Sinf_nom_SMS(상번호());
        int interfeys_COUNT = 짧은수(); if (interfeys_COUNT > 16) { to_xtab_qolish_VALUE("interface count limit"); return; }
        Sinf_interfeys_COUNT[Sinf_Izoh] = interfeys_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interfeys_COUNT; Loop_INDEX++) Sinf_interfeys[Sinf_Izoh * 16 + Loop_INDEX] = Sinf_nom_SMS(상번호());
        int ma_lumotlar_maydoni_COUNT = 짧은수();
        if (ma_lumotlar_maydoni_COUNT > 512 - in_COUNT) { to_xtab_qolish_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < ma_lumotlar_maydoni_COUNT && !Xato; Loop_INDEX++) {
            int fayl_INDEX = in_COUNT++; in_egasi[fayl_INDEX] = Sinf_Izoh; in_Ruxsatlar[fayl_INDEX] = 짧은수(); in_nom[fayl_INDEX] = 상번호(); in_TYPE[fayl_INDEX] = 상번호();
            chek_konstanta(in_nom[fayl_INDEX], 1); chek_konstanta(in_TYPE[fayl_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[in_TYPE[fayl_INDEX]]; int toifa_kod = 서술형(읽기위치 + konstanta_SECOND_VALUE[in_TYPE[fayl_INDEX]], false); 읽기위치 = 보존값;
            if ((in_Ruxsatlar[fayl_INDEX] & 8) == 0) in_holat[fayl_INDEX] = Sinf_in_COUNT[Sinf_Izoh]++;
            int xususiyat_ma_lumotlar = 짧은수();
            for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < xususiyat_ma_lumotlar && !Xato; ichki_qo_shilish_holat++) {
                int nom_konstanta = 상번호(), 유효길이 = butun_son();
                if (Word_SMS(nom_konstanta, "ConstantValue") && 유효길이 == 2) {
                    int ma_lumotlar_VALUE = 상번호();
                    if (toifa_kod == 1 && chek_konstanta(ma_lumotlar_VALUE, 3)) in_ma_lumotlar[fayl_INDEX] = 상가[ma_lumotlar_VALUE];
                    else if (toifa_kod == 2 && chek_konstanta(ma_lumotlar_VALUE, 8)) in_ma_lumotlar[fayl_INDEX] = konstanta_SMS(상가[ma_lumotlar_VALUE]);
                } else 건너(유효길이);
            }
        }
        int element_COUNT = 짧은수();
        if (element_COUNT > 512 - uslub_COUNT) { to_xtab_qolish_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < element_COUNT && !Xato; Loop_INDEX++) {
            int 수 = uslub_COUNT++; uslub_egasi[수] = Sinf_Izoh;
            uslub_kirish_huquqi[수] = 짧은수(); uslub_nom_SMS[수] = 상번호(); uslub_TYPE[수] = 상번호();
            chek_konstanta(uslub_nom_SMS[수], 1); 서술읽기(수);
            if ((uslub_kirish_huquqi[수] & 8) == 0) {
                if (uslub_dalil_COUNT[수] == 16) { to_xtab_qolish_VALUE("too many instance method arguments"); return; }
                for (int Taqqoslama_holat = uslub_dalil_COUNT[수]; Taqqoslama_holat > 0; Taqqoslama_holat--) uslub_dalil_TYPE[수 * 16 + Taqqoslama_holat] = uslub_dalil_TYPE[수 * 16 + Taqqoslama_holat - 1];
                uslub_dalil_TYPE[수 * 16] = 2; uslub_dalil_COUNT[수]++;
            }
            if ((uslub_kirish_huquqi[수] & 0x100) != 0) to_xtab_qolish_VALUE("user native method unsupported");
            if (Word_SMS(uslub_nom_SMS[수], "<clinit>")) ishga_tushirmoq_Sinf_Izoh[Sinf_Izoh] = 수 + 1;
            for (int old_kamera_VALUE = 0; old_kamera_VALUE < 수; old_kamera_VALUE++) if (uslub_egasi[old_kamera_VALUE] == Sinf_Izoh && 같은말(uslub_nom_SMS[old_kamera_VALUE], uslub_nom_SMS[수]) && 같은말(uslub_TYPE[old_kamera_VALUE], uslub_TYPE[수])) to_xtab_qolish_VALUE("duplicate method");
            int xususiyat_COUNT = 짧은수();
            for (int xususiyat_VALUE = 0; xususiyat_VALUE < xususiyat_COUNT && !Xato; xususiyat_VALUE++) {
                int Nomi = 상번호(), uzunlik_VALUE = butun_son(), Bajarish = 읽기위치;
                if (!klip(Bajarish, uzunlik_VALUE)) { to_xtab_qolish_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nomi, "Code")) {
                    if (uslub_Start[수] != 0) to_xtab_qolish_VALUE("duplicate Code attribute");
                    uslub_Stack[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_uzunlik = butun_son();
                    if (uslub_Stack[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < uslub_dalil_COUNT[수]
                        || kod_uzunlik < 1 || kod_uzunlik > 8192) to_xtab_qolish_VALUE("method memory limits exceeded");
                    uslub_Start[수] = 읽기위치; 건너(kod_uzunlik); uslub_to_xtatmoq[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { to_xtab_qolish_VALUE("exception table limit"); return; }
                    for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 잡는수; ichki_qo_shilish_holat++) {
                        int xato_Ma_lumotnomalar = 잡기수++; 잡기함수[xato_Ma_lumotnomalar] = 수;
                        잡기시작[xato_Ma_lumotnomalar] = uslub_Start[수] + 짧은수(); 잡기끝[xato_Ma_lumotnomalar] = uslub_Start[수] + 짧은수();
                        잡기위치[xato_Ma_lumotnomalar] = uslub_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[xato_Ma_lumotnomalar] = 부호값 == 0 ? 0 : Sinf_nom_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Bajarish + uzunlik_VALUE) to_xtab_qolish_VALUE("Code attribute size mismatch");
                } else 건너(uzunlik_VALUE);
            }
            if ((uslub_kirish_huquqi[수] & 0x400) != 0) continue;
            if (uslub_Start[수] == 0) to_xtab_qolish_VALUE("missing Code attribute");
            int in_kiritish = uslub_Start[수];
            while (in_kiritish < uslub_to_xtatmoq[수] && !Xato) {
                int uzunlik_VALUE = 길이읽기(in_kiritish, uslub_Start[수], uslub_to_xtatmoq[수]);
                if (uzunlik_VALUE == 0) { to_xtab_qolish_VALUE("unsupported or truncated bytecode"); break; }
                경계[in_kiritish] = 수 + 1; in_kiritish += uzunlik_VALUE;
            }
            in_kiritish = uslub_Start[수];
            while (in_kiritish < uslub_to_xtatmoq[수] && !Xato) {
                int VALUE = Fayl[in_kiritish];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) chek_ko_chirish_joyi_VALUE(in_kiritish + (short)(Fayl[in_kiritish + 1] << 8 | Fayl[in_kiritish + 2]), 수);
                if (VALUE == 200) chek_ko_chirish_joyi_VALUE(in_kiritish + holat_butun_son(in_kiritish + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = in_kiritish + 1; while ((읽는자리 - uslub_Start[수]) % 4 != 0) 읽는자리++;
                    chek_ko_chirish_joyi_VALUE(in_kiritish + holat_butun_son(읽는자리), 수);
                    int kiritish_COUNT = VALUE == 170 ? holat_butun_son(읽는자리 + 8) - holat_butun_son(읽는자리 + 4) + 1 : holat_butun_son(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < kiritish_COUNT; ichki_qo_shilish_holat++) chek_ko_chirish_joyi_VALUE(in_kiritish + holat_butun_son(읽는자리 + ichki_qo_shilish_holat * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                in_kiritish += 길이읽기(in_kiritish, uslub_Start[수], uslub_to_xtatmoq[수]);
            }
            for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 잡기수; ichki_qo_shilish_holat++) if (잡기함수[ichki_qo_shilish_holat] == 수) {
                chek_ko_chirish_joyi_VALUE(잡기시작[ichki_qo_shilish_holat], 수); chek_ko_chirish_joyi_VALUE(잡기위치[ichki_qo_shilish_holat], 수);
                if (잡기끝[ichki_qo_shilish_holat] != uslub_to_xtatmoq[수]) chek_ko_chirish_joyi_VALUE(잡기끝[ichki_qo_shilish_holat], 수);
                if (잡기시작[ichki_qo_shilish_holat] >= 잡기끝[ichki_qo_shilish_holat]) to_xtab_qolish_VALUE("invalid exception range");
            }
        }
        if (!Xato) 속성건너();
        if (읽기위치 != Hajmi) to_xtab_qolish_VALUE("extra class file data");
    }
    static int joylashtirmoq_Xotira(int 종류, int uzunlik_VALUE) { return 새기억(종류, uzunlik_VALUE); }
    static boolean obyekt_VALUE(int Ma_lumotnomalar, int 종류) {
        if (!객체유효(Ma_lumotnomalar)) return false;
        if (힙[Ma_lumotnomalar] != 종류) { to_xtab_qolish_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!chek_konstanta(INDEX, 1)) return 0;
        if (satr_Ma_lumotnomalar[INDEX] != 0) return satr_Ma_lumotnomalar[INDEX];
        int Ma_lumotnomalar = joylashtirmoq_Xotira(1, konstanta_SECOND_VALUE[INDEX]); if (Xato) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], uzunlik_VALUE = 0;
        while (수 < 끝 && !Xato) {
            int VALUE = Fayl[수++];
            if (VALUE == 0) to_xtab_qolish_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Keyingi_element = Fayl[수++];
                if ((Keyingi_element & 192) != 128) to_xtab_qolish_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Keyingi_element & 63;
                if (VALUE != 0 && VALUE < 128) to_xtab_qolish_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Fayl[수++], 나 = Fayl[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) to_xtab_qolish_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) to_xtab_qolish_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) to_xtab_qolish_VALUE("invalid modified UTF-8");
            힙[Ma_lumotnomalar + 2 + uzunlik_VALUE++] = VALUE;
        }
        힙[Ma_lumotnomalar + 1] = uzunlik_VALUE; satr_Ma_lumotnomalar[INDEX] = Ma_lumotnomalar; return Ma_lumotnomalar;
    }
    static int tashkilotchi_belgi(String VALUE) {
        int Ma_lumotnomalar = joylashtirmoq_Xotira(1, VALUE.length()); if (Xato) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Ma_lumotnomalar + 2 + 수] = VALUE.charAt(수);
        return Ma_lumotnomalar;
    }
    static void yozmoq_SMS(int Ma_lumotnomalar) {
        if (Ma_lumotnomalar == 0) { foydalanuvchi.Yozish("null"); return; }
        if (!obyekt_VALUE(Ma_lumotnomalar, 1)) return;
        for (int 수 = 0; 수 < 힙[Ma_lumotnomalar + 1]; 수++) foydalanuvchi.yozmoq_belgi_VALUE(힙[Ma_lumotnomalar + 2 + 수]);
    }
    static int raqam_belgi(int VALUE) {
        int Ma_lumotnomalar = joylashtirmoq_Xotira(1, 11); if (Xato) return 0;
        int uzunlik_VALUE = 0;
        if (VALUE < 0) 힙[Ma_lumotnomalar + 2 + uzunlik_VALUE++] = '-'; else VALUE = -VALUE;
        int holat_INDEX = 1000000000; boolean Bajarish = false;
        while (holat_INDEX != 0) {
            int 수 = -(VALUE / holat_INDEX);
            if (수 != 0 || Bajarish || holat_INDEX == 1) { 힙[Ma_lumotnomalar + 2 + uzunlik_VALUE++] = '0' + 수; Bajarish = true; }
            VALUE %= holat_INDEX; holat_INDEX /= 10;
        }
        힙[Ma_lumotnomalar + 1] = uzunlik_VALUE; return Ma_lumotnomalar;
    }
    static int 정수해독(int Ma_lumotnomalar) {
        if (!obyekt_VALUE(Ma_lumotnomalar, 1)) return 0;
        int uzunlik_VALUE = 힙[Ma_lumotnomalar + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (uzunlik_VALUE > 0 && (힙[Ma_lumotnomalar + 2] == '-' || 힙[Ma_lumotnomalar + 2] == '+')) { 음수 = 힙[Ma_lumotnomalar + 2] == '-'; 수++; }
        if (수 == uzunlik_VALUE) to_xtab_qolish_VALUE("NumberFormatException");
        for (; 수 < uzunlik_VALUE && !Xato; 수++) {
            int raqam_VALUE = 힙[Ma_lumotnomalar + 2 + 수] - '0';
            if (raqam_VALUE < 0 || raqam_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && raqam_VALUE > (음수 ? 8 : 7)) to_xtab_qolish_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - raqam_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Xato) return;
        if (kadr_INDEX < 0 || kadr_Stack[kadr_INDEX] >= uslub_Stack[kadr_uslub[kadr_INDEX]]) { to_xtab_qolish_VALUE("operand stack overflow"); return; }
        int in_kiritish = kadr_INDEX * 128 + kadr_Stack[kadr_INDEX]++; 스택값[in_kiritish] = VALUE; 스택형[in_kiritish] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Xato) return 0;
        if (kadr_INDEX < 0 || kadr_Stack[kadr_INDEX] < 1) { to_xtab_qolish_VALUE("operand stack underflow"); return 0; }
        int in_kiritish = kadr_INDEX * 128 + --kadr_Stack[kadr_INDEX]; qaytarish_TYPE = 스택형[in_kiritish];
        if (TYPE_VALUE != 0 && qaytarish_TYPE != TYPE_VALUE) to_xtab_qolish_VALUE("operand type mismatch");
        if (qaytarish_TYPE == 2) himoya_qilmoq_VALUE(스택값[in_kiritish]);
        return 스택값[in_kiritish];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadr_uslub[kadr_INDEX]] || INDEX < 0 || mahalliy_TYPE[kadr_INDEX * 128 + INDEX] != TYPE_VALUE) { to_xtab_qolish_VALUE("invalid or uninitialized local"); return; }
        넣기(mahalliy_VALUE[kadr_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void yozmoq_mahalliy(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadr_uslub[kadr_INDEX]] || INDEX < 0) { to_xtab_qolish_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); mahalliy_VALUE[kadr_INDEX * 128 + INDEX] = VALUE; mahalliy_TYPE[kadr_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Holati = kadr_holat[kadr_INDEX];
        if (Holati < uslub_Start[kadr_uslub[kadr_INDEX]] || Holati >= uslub_to_xtatmoq[kadr_uslub[kadr_INDEX]]) { to_xtab_qolish_VALUE("instruction pointer out of range"); return 0; }
        kadr_holat[kadr_INDEX]++; return Fayl[Holati];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void ko_chirmoq_VALUE(int Holati) {
        int FUNCTION_VALUE = kadr_uslub[kadr_INDEX];
        if (Holati < uslub_Start[FUNCTION_VALUE] || Holati >= uslub_to_xtatmoq[FUNCTION_VALUE] || 경계[Holati] != FUNCTION_VALUE + 1) to_xtab_qolish_VALUE("invalid branch target");
        else kadr_holat[kadr_INDEX] = Holati;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadr_INDEX % 32 == 31) { to_xtab_qolish_VALUE("call stack limit (32)"); return; }
        int Keyingi_element = kadr_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) mahalliy_TYPE[Keyingi_element * 128 + 수] = 0;
        for (int 수 = uslub_dalil_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            mahalliy_VALUE[Keyingi_element * 128 + 수] = 빼기(uslub_dalil_TYPE[FUNCTION_VALUE * 16 + 수]); mahalliy_TYPE[Keyingi_element * 128 + 수] = uslub_dalil_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (Xato) return;
        kadr_INDEX = Keyingi_element; ishga_tushirmoq_kadr[kadr_INDEX] = 0; kadr_uslub[kadr_INDEX] = FUNCTION_VALUE; kadr_holat[kadr_INDEX] = uslub_Start[FUNCTION_VALUE]; kadr_Stack[kadr_INDEX] = 0;
    }
    static void qaytarish_o_lchov(int TYPE_VALUE) {
        if (TYPE_VALUE != uslub_qaytarish[kadr_uslub[kadr_INDEX]]) { to_xtab_qolish_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (ishga_tushirmoq_kadr[kadr_INDEX] != 0) Sinf_Izoh_holat[ishga_tushirmoq_kadr[kadr_INDEX] - 1] = 2;
        if (틀잠금[kadr_INDEX] != 0) { 잠금풀기(틀잠금[kadr_INDEX]); 틀잠금[kadr_INDEX] = 0; }
        kadr_INDEX--; if (kadr_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] oqim_fayl_nom = new int[64];
    static void fayl_oqim_CALL(int egasi_VALUE, int Nomi, int format_VALUE, int Buyruq) {
        boolean 출력 = Word_SMS(egasi_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Buyruq == 183 && Word_SMS(Nomi, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { to_xtab_qolish_VALUE("unsupported file stream constructor"); return; }
            int fayl_kiritish_nom = 빼기(2), oqim_VALUE = 빼기(2);
            if (!obyekt_VALUE(fayl_kiritish_nom, 1) || !obyekt_VALUE(oqim_VALUE, 종류) || Xato) return;
            if (힙[oqim_VALUE + 3] != 0) { to_xtab_qolish_VALUE("file stream already initialized"); return; }
            int uzunlik_VALUE = 힙[fayl_kiritish_nom + 1];
            if (uzunlik_VALUE < 1 || uzunlik_VALUE > 63) { to_xtab_qolish_VALUE("invalid file name length"); return; }
            for (int in_kiritish = 0; in_kiritish < uzunlik_VALUE; in_kiritish++) {
                int VALUE = 힙[fayl_kiritish_nom + 2 + in_kiritish];
                if (VALUE < 1) { to_xtab_qolish_VALUE("invalid file stream path"); return; }
                oqim_fayl_nom[in_kiritish] = VALUE;
            }
            oqim_fayl_nom[uzunlik_VALUE] = 0;
            int 서술자 = foydalanuvchi.파일서술자열기(oqim_fayl_nom, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { to_xtab_qolish_VALUE("FileNotFoundException: file open failed"); return; }
            힙[oqim_VALUE + 2] = 서술자; 힙[oqim_VALUE + 3] = 1;
            return;
        }
        if (Buyruq != 182) { to_xtab_qolish_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(Nomi, "write") || !출력 && Word_SMS(Nomi, "read"))
            && (Word_SMS(format_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean klip_VALUE = Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int kiritish_COUNT = klip_VALUE ? 빼기(1) : 0, 시작점 = klip_VALUE ? 빼기(1) : 0, ma_lumotlar_ARRAY = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2);
            if (!obyekt_VALUE(ma_lumotlar_ARRAY, 20) || !obyekt_VALUE(obyekt_Ma_lumotnomalar, 종류)) return;
            if (!klip_VALUE) kiritish_COUNT = 힙[ma_lumotlar_ARRAY + 1];
            if (시작점 < 0 || kiritish_COUNT < 0 || 시작점 > 힙[ma_lumotlar_ARRAY + 1] - kiritish_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[obyekt_Ma_lumotnomalar + 3] == 0 || 힙[obyekt_Ma_lumotnomalar + 2] < 0) { to_xtab_qolish_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < kiritish_COUNT && !Xato) {
                int 반환값 = 출력 ? foydalanuvchi.파일한바이트쓰기(힙[obyekt_Ma_lumotnomalar + 2], 힙[ma_lumotlar_ARRAY + 2 + 시작점 + 완료수]) : foydalanuvchi.파일한바이트읽기(힙[obyekt_Ma_lumotnomalar + 2]);
                if (반환값 < 0) { to_xtab_qolish_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[ma_lumotlar_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(kiritish_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_SMS(Nomi, "flush") && Word_SMS(format_VALUE, "()V")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 종류) && 힙[obyekt_Ma_lumotnomalar + 2] < 0) to_xtab_qolish_VALUE("IOException: stream closed"); return; }
        int Amal = -1, VALUE = 0;
        if (Word_SMS(Nomi, "close") && Word_SMS(format_VALUE, "()V")) Amal = 0;
        if (!출력 && Word_SMS(Nomi, "read") && Word_SMS(format_VALUE, "()I")) Amal = 1;
        if (출력 && Word_SMS(Nomi, "write") && Word_SMS(format_VALUE, "(I)V")) { Amal = 2; VALUE = 빼기(1); }
        if (Amal < 0) { to_xtab_qolish_VALUE("unsupported file stream method"); return; }
        int oqim_VALUE = 빼기(2);
        if (!obyekt_VALUE(oqim_VALUE, 종류) || Xato) return;
        if (힙[oqim_VALUE + 3] == 0) { to_xtab_qolish_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[oqim_VALUE + 2];
        if (Amal == 0) {
            if (서술자 >= 0 && foydalanuvchi.파일서술자닫기(서술자) < 0) to_xtab_qolish_VALUE("IOException: close failed");
            힙[oqim_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { to_xtab_qolish_VALUE("IOException: stream closed"); return; }
        if (Amal == 1) {
            int o_lchov = foydalanuvchi.파일한바이트읽기(서술자);
            if (o_lchov < -1) to_xtab_qolish_VALUE("IOException: read failed"); else 넣기(o_lchov == 256 ? -1 : o_lchov, 1);
        } else if (foydalanuvchi.파일한바이트쓰기(서술자, VALUE) != 1) to_xtab_qolish_VALUE("IOException: write failed");
    }
    static void CALL_uslub(int INDEX, int Buyruq) {
        if (INDEX <= 0 || INDEX >= konstanta_teg.length || (konstanta_teg[INDEX] != 10 && konstanta_teg[INDEX] != 11)) { to_xtab_qolish_VALUE("invalid method reference"); return; }
        int egasi_VALUE = Sinf_nom_SMS(상가[INDEX]), Nomi = Ma_lumotnomalar_nom(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Ma_lumotnomalar_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (Xato) return;
        if (기본호출(egasi_VALUE, Nomi, format_VALUE, Buyruq)) return;
        if (Word_SMS(egasi_VALUE, "java/io/FileInputStream") || Word_SMS(egasi_VALUE, "java/io/FileOutputStream")) {
            fayl_oqim_CALL(egasi_VALUE, Nomi, format_VALUE, Buyruq); return;
        }
        if (Buyruq == 184 && Word_SMS(egasi_VALUE, "java/lang/Integer") && Word_SMS(Nomi, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Buyruq == 182 && Word_SMS(egasi_VALUE, "java/io/PrintStream") && (Word_SMS(Nomi, "println") || Word_SMS(Nomi, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(Nomi, "println")) to_xtab_qolish_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) to_xtab_qolish_VALUE("invalid PrintStream receiver");
            if (Xato) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) foydalanuvchi.Yozish(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) foydalanuvchi.yozmoq_belgi_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) yozmoq_SMS(VALUE);
            if (Word_SMS(Nomi, "println")) foydalanuvchi.yozmoq_belgi_VALUE(10);
            return;
        }
        if (Buyruq == 182 && Word_SMS(egasi_VALUE, "java/lang/String")) {
            if (Word_SMS(Nomi, "length") && Word_SMS(format_VALUE, "()I")) {
                int Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(Ma_lumotnomalar, 1)) 넣기(힙[Ma_lumotnomalar + 1], 1); return;
            }
            if (Word_SMS(Nomi, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int satr_osti_VALUE = 빼기(1), Ma_lumotnomalar = 빼기(2);
                if (obyekt_VALUE(Ma_lumotnomalar, 1)) {
                    if (satr_osti_VALUE < 0 || satr_osti_VALUE >= 힙[Ma_lumotnomalar + 1]) to_xtab_qolish_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Ma_lumotnomalar + 2 + satr_osti_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(egasi_VALUE, "java/lang/StringBuilder")) {
            if (Buyruq == 183 && Word_SMS(Nomi, "<init>") && Word_SMS(format_VALUE, "()V")) { obyekt_VALUE(빼기(2), 4); return; }
            if (Buyruq == 182 && Word_SMS(Nomi, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(Ma_lumotnomalar, 4)) 넣기(힙[Ma_lumotnomalar + 2] == 0 ? tashkilotchi_belgi("") : 힙[Ma_lumotnomalar + 2], 2); return;
            }
            if (Buyruq == 182 && Word_SMS(Nomi, "append")) {
                int Matn = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) Matn = raqam_belgi(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) Matn = tashkilotchi_belgi(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Matn = joylashtirmoq_Xotira(1, 1); if (!Xato) 힙[Matn + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Matn = 빼기(2); if (Matn == 0) Matn = tashkilotchi_belgi("null"); }
                else { to_xtab_qolish_VALUE("unsupported StringBuilder append"); return; }
                int Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(Ma_lumotnomalar, 4) || !obyekt_VALUE(Matn, 1)) return;
                int old_kamera_VALUE = 힙[Ma_lumotnomalar + 2], old_kamera_VALUE_uzunlik = old_kamera_VALUE == 0 ? 0 : 힙[old_kamera_VALUE + 1], Orqaga_VALUE_uzunlik = 힙[Matn + 1];
                int 새글 = joylashtirmoq_Xotira(1, old_kamera_VALUE_uzunlik + Orqaga_VALUE_uzunlik); if (Xato) return;
                for (int 수 = 0; 수 < old_kamera_VALUE_uzunlik; 수++) 힙[새글 + 2 + 수] = 힙[old_kamera_VALUE + 2 + 수];
                for (int 수 = 0; 수 < Orqaga_VALUE_uzunlik; 수++) 힙[새글 + 2 + old_kamera_VALUE_uzunlik + 수] = 힙[Matn + 2 + 수];
                힙[Ma_lumotnomalar + 2] = 새글; 넣기(Ma_lumotnomalar, 2); return;
            }
        }
        int Sinf_Izoh = FIND_Sinf_Izoh(egasi_VALUE); if (Sinf_Izoh < 0 || Xato) return;
        int fayl_INDEX = FIND_uslub(Sinf_Izoh, Nomi, format_VALUE);
        if (fayl_INDEX < 0) {
            for (int belgi_kodi = Sinf_Izoh, kiritish_COUNT = 0; belgi_kodi >= 0 && kiritish_COUNT < 16; kiritish_COUNT++, belgi_kodi = 부모종(belgi_kodi))
                if (Word_SMS(종부모[belgi_kodi], "java/lang/Thread")) { 가닥호출(Nomi, format_VALUE, Buyruq); return; }
            to_xtab_qolish_VALUE("NoSuchMethodError"); return;
        }
        if (((uslub_kirish_huquqi[fayl_INDEX] & 8) != 0) != (Buyruq == 184)) { to_xtab_qolish_VALUE("method static/instance mismatch"); return; }
        if (Buyruq == 184) { if (!ishga_tushirmoq(uslub_egasi[fayl_INDEX], kadr_qo_llanma[kadr_INDEX])) return; }
        else {
            int 읽는자리 = kadr_Stack[kadr_INDEX] - uslub_dalil_COUNT[fayl_INDEX];
            if (읽는자리 < 0 || 스택형[kadr_INDEX * 128 + 읽는자리] != 2) { to_xtab_qolish_VALUE("invalid method receiver"); return; }
            int obyekt_Ma_lumotnomalar = 스택값[kadr_INDEX * 128 + 읽는자리];
            if (!객체유효(obyekt_Ma_lumotnomalar)) return;
            if (힙[obyekt_Ma_lumotnomalar] < 32 || !종포함(힙[obyekt_Ma_lumotnomalar] - 32, egasi_VALUE)) { to_xtab_qolish_VALUE("method receiver type mismatch"); return; }
            if (Buyruq != 183) fayl_INDEX = FIND_uslub(힙[obyekt_Ma_lumotnomalar] - 32, Nomi, format_VALUE);
        }
        if (fayl_INDEX < 0 || (uslub_kirish_huquqi[fayl_INDEX] & 0x400) != 0) { to_xtab_qolish_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((uslub_kirish_huquqi[fayl_INDEX] & 32) != 0) {
            if (Buyruq == 184) { int belgi_kodi = uslub_egasi[fayl_INDEX]; if (종잠금[belgi_kodi] == 0) 종잠금[belgi_kodi] = joylashtirmoq_Xotira(8, 0); 잠금참조 = 종잠금[belgi_kodi]; }
            else 잠금참조 = 스택값[kadr_INDEX * 128 + kadr_Stack[kadr_INDEX] - uslub_dalil_COUNT[fayl_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!Xato) kadr_holat[kadr_INDEX] = kadr_qo_llanma[kadr_INDEX]; return; }
        }
        호출(fayl_INDEX); if (!Xato) 틀잠금[kadr_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Ma_lumotnomalar, int ma_lumotlar_VALUE) {
        if (ma_lumotlar_VALUE == 0 || ARRAY_element[ARRAY_Ma_lumotnomalar] == 0) return true;
        boolean 성공여부 = ARRAY_element[ARRAY_Ma_lumotnomalar] == -1 ? (ma_lumotlar_VALUE > 0 && ma_lumotlar_VALUE < 힙끝 && 힙[ma_lumotlar_VALUE] == 1) : 맞는객체(ma_lumotlar_VALUE, ARRAY_element[ARRAY_Ma_lumotnomalar]);
        if (!성공여부 && !Xato) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_in(int Ma_lumotnomalar, int satr_osti_VALUE, int TYPE_VALUE) {
        if (!obyekt_VALUE(Ma_lumotnomalar, TYPE_VALUE)) return 0;
        if (satr_osti_VALUE < 0 || satr_osti_VALUE >= 힙[Ma_lumotnomalar + 1]) { to_xtab_qolish_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Ma_lumotnomalar + 2 + satr_osti_VALUE;
    }
    static void bajarmoq_buyruq() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Xato) { if (던진객체 != 0) deskriptor_istisno(); if (Xato || kadr_INDEX < 현재가닥 * 32) break; }
            if (kadr_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_oqim()) break; 조각 = 100; }
            if (kadr_INDEX == 0 && Sinf_Izoh_holat[kiritish_Sinf_Izoh] != 2 && !ishga_tushirmoq(kiritish_Sinf_Izoh, kadr_holat[kadr_INDEX])) continue;
            if (kadr_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (uslub_kirish_huquqi[kadr_uslub[kadr_INDEX]] & 32) != 0 && 틀잠금[kadr_INDEX] == 0) {
                int obyekt_Ma_lumotnomalar = oqim_maqsad[현재가닥]; if (!잠금얻기(obyekt_Ma_lumotnomalar)) { if (Xato) break; continue; } 틀잠금[kadr_INDEX] = obyekt_Ma_lumotnomalar;
            }
            잠시수 = 0;
            if (--남음 == 0) { to_xtab_qolish_VALUE("instruction limit (500000)"); break; }
            int Bajarish = kadr_holat[kadr_INDEX]; kadr_qo_llanma[kadr_INDEX] = Bajarish; int VALUE = 명바();
            if (Xato) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = uslub_egasi[kadr_uslub[kadr_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstanta_teg.length) to_xtab_qolish_VALUE("invalid ldc constant");
                else if (konstanta_teg[수] == 3) 넣기(상가[수], 1);
                else if (konstanta_teg[수] == 8) 넣기(konstanta_SMS(상가[수]), 2);
                else to_xtab_qolish_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { yozmoq_mahalliy(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { yozmoq_mahalliy(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { yozmoq_mahalliy(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int kiritish_holat = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2), toifa_kod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && obyekt_Ma_lumotnomalar > 0 && obyekt_Ma_lumotnomalar < 힙끝 && 힙[obyekt_Ma_lumotnomalar] == 21) toifa_kod = 21;
                int 읽는자리 = ARRAY_in(obyekt_Ma_lumotnomalar, kiritish_holat, toifa_kod); if (!Xato) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int kiritish_Ma_lumotnomalar = 빼기(VALUE == 83 ? 2 : 1), kiritish_holat = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2), toifa_kod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && obyekt_Ma_lumotnomalar > 0 && obyekt_Ma_lumotnomalar < 힙끝 && 힙[obyekt_Ma_lumotnomalar] == 21) toifa_kod = 21;
                int 읽는자리 = ARRAY_in(obyekt_Ma_lumotnomalar, kiritish_holat, toifa_kod);
                if (!Xato && toifa_kod == 3 && !배열저장가능(obyekt_Ma_lumotnomalar, kiritish_Ma_lumotnomalar)) continue;
                if (!Xato) 힙[읽는자리] = toifa_kod == 20 ? (byte)kiritish_Ma_lumotnomalar : toifa_kod == 21 ? kiritish_Ma_lumotnomalar & 1 : toifa_kod == 22 ? (char)kiritish_Ma_lumotnomalar : toifa_kod == 23 ? (short)kiritish_Ma_lumotnomalar : kiritish_Ma_lumotnomalar;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Stack_qo_llanma(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), o_lchov = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { to_xtab_qolish_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) o_lchov = 가 + 나;
                if (VALUE == 100) o_lchov = 가 - 나;
                if (VALUE == 104) o_lchov = 가 * 나;
                if (VALUE == 108) o_lchov = 가 / 나;
                if (VALUE == 112) o_lchov = 가 % 나;
                if (VALUE == 120) o_lchov = 가 << 나;
                if (VALUE == 122) o_lchov = 가 >> 나;
                if (VALUE == 124) o_lchov = 가 >>> 나;
                if (VALUE == 126) o_lchov = 가 & 나;
                if (VALUE == 128) o_lchov = 가 | 나;
                if (VALUE == 130) o_lchov = 가 ^ 나;
                넣기(o_lchov, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int mahalliy_soha = 명바(), 증분 = (byte)명바(); 지역읽기(mahalliy_soha, 1); 넣기(빼기(1) + 증분, 1); yozmoq_mahalliy(mahalliy_soha, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int ko_chirish_joyi_VALUE = Bajarish + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) ko_chirmoq_VALUE(ko_chirish_joyi_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { qaytarish_o_lchov(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Bajarish); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { to_xtab_qolish_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_uslub(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(Sinf_nom_SMS(명상수()), Bajarish); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int toifa_kod = 3, tarkibiy_qism = 0;
                if (VALUE == 188) { int 임시값 = 명바(); toifa_kod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else tarkibiy_qism = Sinf_nom_SMS(명상수());
                if (toifa_kod == 0) { to_xtab_qolish_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), obyekt_Ma_lumotnomalar = joylashtirmoq_Xotira(toifa_kod, 유효길이); if (!Xato) ARRAY_element[obyekt_Ma_lumotnomalar] = tarkibiy_qism; 넣기(obyekt_Ma_lumotnomalar, 2); continue;
            }
            if (VALUE == 190) {
                int obyekt_Ma_lumotnomalar = 빼기(2);
                if (객체유효(obyekt_Ma_lumotnomalar)) { int Taqqoslama_holat = 힙[obyekt_Ma_lumotnomalar]; if (Taqqoslama_holat != 2 && Taqqoslama_holat != 3 && (Taqqoslama_holat < 20 || Taqqoslama_holat > 23)) to_xtab_qolish_VALUE("not an array"); else 넣기(힙[obyekt_Ma_lumotnomalar + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int obyekt_Ma_lumotnomalar = 빼기(2); if (객체유효(obyekt_Ma_lumotnomalar)) { if (힙[obyekt_Ma_lumotnomalar] != 9) to_xtab_qolish_VALUE("athrow requires supported Throwable"); else { 던진객체 = obyekt_Ma_lumotnomalar; Xato = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int nom_konstanta = Sinf_nom_SMS(명상수()), obyekt_Ma_lumotnomalar = 빼기(2); boolean MATCH = 맞는객체(obyekt_Ma_lumotnomalar, nom_konstanta);
                if (VALUE == 193) 넣기(obyekt_Ma_lumotnomalar != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Xato) to_xtab_qolish_VALUE("ClassCastException"); 넣기(obyekt_Ma_lumotnomalar, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Bajarish + 1, fayl_INDEX = kadr_uslub[kadr_INDEX], Kalit_Ma_lumotnomalar = 빼기(1);
                while ((읽는자리 - uslub_Start[fayl_INDEX]) % 4 != 0) 읽는자리++;
                int maqsad_manzil = holat_butun_son(읽는자리);
                if (VALUE == 170) { int 낮은값 = holat_butun_son(읽는자리 + 4), 높은값 = holat_butun_son(읽는자리 + 8); if (Kalit_Ma_lumotnomalar >= 낮은값 && Kalit_Ma_lumotnomalar <= 높은값) maqsad_manzil = holat_butun_son(읽는자리 + 12 + (Kalit_Ma_lumotnomalar - 낮은값) * 4); }
                else { int 총수 = holat_butun_son(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (holat_butun_son(읽는자리 + 8 + Loop_INDEX * 8) == Kalit_Ma_lumotnomalar) maqsad_manzil = holat_butun_son(읽는자리 + 12 + Loop_INDEX * 8); }
                ko_chirmoq_VALUE(Bajarish + maqsad_manzil); continue;
            }
            if (VALUE == 200) { ko_chirmoq_VALUE(Bajarish + holat_butun_son(Bajarish + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int obyekt_Ma_lumotnomalar = 빼기(2);
                if (VALUE == 195) 잠금풀기(obyekt_Ma_lumotnomalar);
                else if (!잠금얻기(obyekt_Ma_lumotnomalar) && !Xato) { 넣기(obyekt_Ma_lumotnomalar, 2); kadr_holat[kadr_INDEX] = Bajarish; }
                continue;
            }
            if (VALUE == 196) {
                int buyruq_kod = 명바(), kiritish_holat = 명짧();
                if (buyruq_kod == 21 || buyruq_kod == 25) 지역읽기(kiritish_holat, buyruq_kod == 21 ? 1 : 2);
                else if (buyruq_kod == 54 || buyruq_kod == 58) yozmoq_mahalliy(kiritish_holat, buyruq_kod == 54 ? 1 : 2);
                else if (buyruq_kod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(kiritish_holat, 1); 넣기(빼기(1) + DELTA_VALUE, 1); yozmoq_mahalliy(kiritish_holat, 1); }
                else to_xtab_qolish_VALUE("unsupported wide opcode");
                continue;
            }
            to_xtab_qolish_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Sinf_Izoh(int Nomi) {
        for (int Loop_INDEX = 0; Loop_INDEX < Sinf_Izoh_COUNT; Loop_INDEX++) if (Sinf_Izoh_nom[Loop_INDEX] != 0 && 같은말(Sinf_Izoh_nom[Loop_INDEX], Nomi)) return Loop_INDEX;
        return yuklamoq_Sinf_Izoh(konstanta_SMS(Nomi));
    }
    static int yuklamoq_Sinf_Izoh(int nom_satr) {
        if (!obyekt_VALUE(nom_satr, 1)) return -1;
        int uzunlik_VALUE = 힙[nom_satr + 1];
        if (uzunlik_VALUE < 1 || uzunlik_VALUE > 505 || Sinf_Izoh_COUNT == 16) { to_xtab_qolish_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < uzunlik_VALUE; Loop_INDEX++) { int belgi_kodi = 힙[nom_satr + 2 + Loop_INDEX]; fayl_nom_SMS[Loop_INDEX] = belgi_kodi == '/' ? '.' : belgi_kodi; }
        fayl_nom_SMS[uzunlik_VALUE] = '.'; fayl_nom_SMS[uzunlik_VALUE + 1] = 'c'; fayl_nom_SMS[uzunlik_VALUE + 2] = 'l'; fayl_nom_SMS[uzunlik_VALUE + 3] = 'a'; fayl_nom_SMS[uzunlik_VALUE + 4] = 's'; fayl_nom_SMS[uzunlik_VALUE + 5] = 's'; fayl_nom_SMS[uzunlik_VALUE + 6] = 0;
        int Hajmi = foydalanuvchi.파일읽기(fayl_nom_SMS, 임시파일);
        if (Hajmi < 0) { to_xtab_qolish_VALUE("ClassNotFoundException"); return -1; }
        int Sinf_Izoh = Sinf_Izoh_COUNT++; Sinf_Izoh_o_lcham[Sinf_Izoh] = Hajmi;
        for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) Fayl[Sinf_Izoh * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(Sinf_Izoh); if (Xato) return -1;
        int real_ma_lumotlar = konstanta_SMS(Sinf_Izoh_nom[Sinf_Izoh]);
        if (!글같음(real_ma_lumotlar, nom_satr, true)) { to_xtab_qolish_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[Sinf_Izoh];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Sinf_Izoh(부모);
            if (Xato || 위 < 0) return -1;
            int 읽는자리 = 위, bosqich_COUNT = 0;
            while (읽는자리 >= 0 && bosqich_COUNT++ < 16) {
                if (읽는자리 == Sinf_Izoh) { to_xtab_qolish_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = Sinf_in_COUNT[위];
            for (int fayl_INDEX = 0; fayl_INDEX < in_COUNT; fayl_INDEX++) if (in_egasi[fayl_INDEX] == Sinf_Izoh && (in_Ruxsatlar[fayl_INDEX] & 8) == 0) in_holat[fayl_INDEX] += 시작변위;
            Sinf_in_COUNT[Sinf_Izoh] += 시작변위;
        }
        return Sinf_Izoh;
    }
    static int 부모종(int Sinf_Izoh) {
        int Nomi = 종부모[Sinf_Izoh];
        for (int Loop_INDEX = 0; Loop_INDEX < Sinf_Izoh_COUNT; Loop_INDEX++) if (Nomi != 0 && Sinf_Izoh_nom[Loop_INDEX] != 0 && 같은말(Sinf_Izoh_nom[Loop_INDEX], Nomi)) return Loop_INDEX;
        return -1;
    }
    static int FIND_uslub(int Sinf_Izoh, int Nomi, int format_VALUE) {
        for (int 깊이 = 0; Sinf_Izoh >= 0 && 깊이 < 16; 깊이++, Sinf_Izoh = 부모종(Sinf_Izoh)) {
            for (int Loop_INDEX = 0; Loop_INDEX < uslub_COUNT; Loop_INDEX++) if (uslub_egasi[Loop_INDEX] == Sinf_Izoh && 같은말(uslub_nom_SMS[Loop_INDEX], Nomi) && 같은말(uslub_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int nom_uslub(int Sinf_Izoh, String Nomi, String format_VALUE) {
        for (int 깊이 = 0; Sinf_Izoh >= 0 && 깊이 < 16; 깊이++, Sinf_Izoh = 부모종(Sinf_Izoh))
            for (int Loop_INDEX = 0; Loop_INDEX < uslub_COUNT; Loop_INDEX++) if (uslub_egasi[Loop_INDEX] == Sinf_Izoh && Word_SMS(uslub_nom_SMS[Loop_INDEX], Nomi) && Word_SMS(uslub_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Nomi) { return Fayl[상가[Nomi]] == 'L' || Fayl[상가[Nomi]] == '[' ? 2 : 1; }
    static boolean ishga_tushirmoq(int Sinf_Izoh, int buyruq_Start) {
        if (Sinf_Izoh < 0 || Xato) return false;
        if (Sinf_Izoh_holat[Sinf_Izoh] == 3) { to_xtab_qolish_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Sinf_Izoh_holat[Sinf_Izoh] == 1 && Sinf_oqim[Sinf_Izoh] != 현재가닥) { kadr_holat[kadr_INDEX] = buyruq_Start; 바꿈요청 = true; return false; }
        if (Sinf_Izoh_holat[Sinf_Izoh] != 0) return true;
        int 위 = 부모종(Sinf_Izoh);
        if (위 >= 0 && !ishga_tushirmoq(위, buyruq_Start)) return false;
        Sinf_Izoh_holat[Sinf_Izoh] = 1; Sinf_oqim[Sinf_Izoh] = 현재가닥;
        if (ishga_tushirmoq_Sinf_Izoh[Sinf_Izoh] != 0) {
            kadr_holat[kadr_INDEX] = buyruq_Start;
            호출(ishga_tushirmoq_Sinf_Izoh[Sinf_Izoh] - 1); if (!Xato) ishga_tushirmoq_kadr[kadr_INDEX] = Sinf_Izoh + 1;
            return false;
        }
        Sinf_Izoh_holat[Sinf_Izoh] = 2; return true;
    }
    static void 필드호출(int INDEX, int Buyruq, int Bajarish) {
        if (!chek_konstanta(INDEX, 9)) return;
        int egasi_VALUE = Sinf_nom_SMS(상가[INDEX]), Nomi = Ma_lumotnomalar_nom(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Ma_lumotnomalar_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (Word_SMS(egasi_VALUE, "java/lang/System") && (Word_SMS(Nomi, "out") || Word_SMS(Nomi, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && Buyruq == 178) { 넣기(-1, 2); return; }
        int Sinf_Izoh = FIND_Sinf_Izoh(egasi_VALUE); if (Sinf_Izoh < 0 || Xato) return;
        int 찾음 = -1;
        for (int 읽는자리 = Sinf_Izoh, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int fayl_INDEX = 0; fayl_INDEX < in_COUNT; fayl_INDEX++) if (in_egasi[fayl_INDEX] == 읽는자리 && 같은말(in_nom[fayl_INDEX], Nomi) && 같은말(in_TYPE[fayl_INDEX], format_VALUE)) 찾음 = fayl_INDEX;
        if (찾음 < 0) { to_xtab_qolish_VALUE("NoSuchFieldError"); return; }
        boolean statik_VALUE = Buyruq == 178 || Buyruq == 179;
        if (statik_VALUE != ((in_Ruxsatlar[찾음] & 8) != 0)) { to_xtab_qolish_VALUE("field static/instance mismatch"); return; }
        if (statik_VALUE && !ishga_tushirmoq(in_egasi[찾음], Bajarish)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (Buyruq == 179 || Buyruq == 181) VALUE = 빼기(TYPE_VALUE);
        if (statik_VALUE) { if (Buyruq == 178) 넣기(in_ma_lumotlar[찾음], TYPE_VALUE); else if (!Xato) in_ma_lumotlar[찾음] = VALUE; return; }
        int obyekt_Ma_lumotnomalar = 빼기(2);
        if (!객체유효(obyekt_Ma_lumotnomalar)) return;
        if (힙[obyekt_Ma_lumotnomalar] < 32 || !종포함(힙[obyekt_Ma_lumotnomalar] - 32, egasi_VALUE)) { to_xtab_qolish_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = obyekt_Ma_lumotnomalar + 2 + in_holat[찾음];
        if (Buyruq == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!Xato) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Sinf_Izoh, int Nomi) {
        for (int 중첩깊이 = 0; Sinf_Izoh >= 0 && 중첩깊이 < 16; 중첩깊이++, Sinf_Izoh = 부모종(Sinf_Izoh)) {
            if (같은말(Sinf_Izoh_nom[Sinf_Izoh], Nomi) || (종부모[Sinf_Izoh] != 0 && 같은말(종부모[Sinf_Izoh], Nomi))) return true;
            for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < Sinf_interfeys_COUNT[Sinf_Izoh]; ichki_qo_shilish_holat++) if (같은말(Sinf_interfeys[Sinf_Izoh * 16 + ichki_qo_shilish_holat], Nomi)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bayt_ma_lumotlar, boolean yo_l) {
        if (첫값 == bayt_ma_lumotlar) return true;
        if (첫값 <= 0 || bayt_ma_lumotlar <= 0 || 힙[첫값] != 1 || 힙[bayt_ma_lumotlar] != 1 || 힙[첫값 + 1] != 힙[bayt_ma_lumotlar + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int x_koordinata = 힙[첫값 + 2 + Loop_INDEX], Y_tugmasi_koordinat = 힙[bayt_ma_lumotlar + 2 + Loop_INDEX];
            if (yo_l) { if (x_koordinata == '.') x_koordinata = '/'; if (Y_tugmasi_koordinat == '.') Y_tugmasi_koordinat = '/'; }
            if (x_koordinata != Y_tugmasi_koordinat) return false;
        }
        return true;
    }
    static boolean 객체유효(int obyekt_Ma_lumotnomalar) {
        if (obyekt_Ma_lumotnomalar == 0) { to_xtab_qolish_VALUE("NullPointerException"); return false; }
        if (obyekt_Ma_lumotnomalar < 1 || obyekt_Ma_lumotnomalar >= 힙끝 || 힙폭[obyekt_Ma_lumotnomalar] < 2 || 힙[obyekt_Ma_lumotnomalar] == 0) { to_xtab_qolish_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void himoya_qilmoq_VALUE(int obyekt_Ma_lumotnomalar) {
        if (obyekt_Ma_lumotnomalar > 0 && obyekt_Ma_lumotnomalar < 힙끝 && 힙폭[obyekt_Ma_lumotnomalar] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = obyekt_Ma_lumotnomalar;
    }
    static void ko_rsatmoq_VALUE(int obyekt_Ma_lumotnomalar) {
        if (obyekt_Ma_lumotnomalar > 0 && obyekt_Ma_lumotnomalar < 힙끝 && 힙폭[obyekt_Ma_lumotnomalar] >= 2 && 힙[obyekt_Ma_lumotnomalar] != 0 && 힙표시[obyekt_Ma_lumotnomalar] == 0) {
            힙표시[obyekt_Ma_lumotnomalar] = 1; 표시대기[ekran_COUNT++] = obyekt_Ma_lumotnomalar;
        }
    }
    static void 수거() {
        ekran_COUNT = 0; To_plam_COUNT++;
        for (int chek_holat = 1; chek_holat < 힙끝; chek_holat += 힙폭[chek_holat]) 힙표시[chek_holat] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < satr_Ma_lumotnomalar.length; Loop_INDEX++) ko_rsatmoq_VALUE(satr_Ma_lumotnomalar[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < in_COUNT; Loop_INDEX++) if ((in_Ruxsatlar[Loop_INDEX] & 8) != 0 && 형종류(in_TYPE[Loop_INDEX]) == 2) ko_rsatmoq_VALUE(in_ma_lumotlar[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < oqim_COUNT; 임시값++) {
            ko_rsatmoq_VALUE(oqim_obyekt[임시값]); ko_rsatmoq_VALUE(oqim_maqsad[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? kadr_INDEX : oqim_kadr[임시값];
            for (int fayl_INDEX = 임시값 * 32; fayl_INDEX <= 꼭대기자리; fayl_INDEX++) {
                for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 함수지역[kadr_uslub[fayl_INDEX]]; ichki_qo_shilish_holat++) if (mahalliy_TYPE[fayl_INDEX * 128 + ichki_qo_shilish_holat] == 2) ko_rsatmoq_VALUE(mahalliy_VALUE[fayl_INDEX * 128 + ichki_qo_shilish_holat]);
                for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < kadr_Stack[fayl_INDEX]; ichki_qo_shilish_holat++) if (스택형[fayl_INDEX * 128 + ichki_qo_shilish_holat] == 2) ko_rsatmoq_VALUE(스택값[fayl_INDEX * 128 + ichki_qo_shilish_holat]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) ko_rsatmoq_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) ko_rsatmoq_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_butun_son.length; Loop_INDEX++) ko_rsatmoq_VALUE(Store_butun_son[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Sinf_Izoh_COUNT; Loop_INDEX++) ko_rsatmoq_VALUE(종잠금[Loop_INDEX]);
        for (int chek_holat = 1; chek_holat < 힙끝; chek_holat += 힙폭[chek_holat]) if (잠금깊이[chek_holat] > 0) ko_rsatmoq_VALUE(chek_holat);
        ko_rsatmoq_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) ko_rsatmoq_VALUE(잠시참조[Loop_INDEX]);
        while (ekran_COUNT > 0) {
            int obyekt_Ma_lumotnomalar = 표시대기[--ekran_COUNT], toifa_kod = 힙[obyekt_Ma_lumotnomalar];
            for (int Loop_INDEX = obyekt_Ma_lumotnomalar + 2; Loop_INDEX < obyekt_Ma_lumotnomalar + 힙폭[obyekt_Ma_lumotnomalar]; Loop_INDEX++) if (toifa_kod == 3 || toifa_kod == 4 || 힙참조[Loop_INDEX] != 0) ko_rsatmoq_VALUE(힙[Loop_INDEX]);
        }
        for (int chek_holat = 1; chek_holat < 힙끝; chek_holat += 힙폭[chek_holat]) if (힙표시[chek_holat] == 0) 힙[chek_holat] = 0;
        for (int chek_holat = 1; chek_holat < 힙끝; chek_holat += 힙폭[chek_holat]) if (힙[chek_holat] == 0) {
            while (chek_holat + 힙폭[chek_holat] < 힙끝 && 힙[chek_holat + 힙폭[chek_holat]] == 0) { int Keyingi_holat = chek_holat + 힙폭[chek_holat]; 힙폭[chek_holat] += 힙폭[Keyingi_holat]; 힙폭[Keyingi_holat] = 0; }
            if (chek_holat + 힙폭[chek_holat] == 힙끝) { 힙끝 = chek_holat; break; }
        }
    }
    static int 새기억(int 종류, int uzunlik_VALUE) {
        if (uzunlik_VALUE < 0) { to_xtab_qolish_VALUE("NegativeArraySizeException"); return 0; }
        if (uzunlik_VALUE > 힙.length - 3) { to_xtab_qolish_VALUE("object heap exhausted"); return 0; }
        int 필요수 = uzunlik_VALUE + 2, obyekt_Ma_lumotnomalar = 0;
        if (필요수 <= 힙.length - 힙끝) { obyekt_Ma_lumotnomalar = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { obyekt_Ma_lumotnomalar = 읽는자리; break; }
            if (obyekt_Ma_lumotnomalar != 0) {
                int 남은길이 = 힙폭[obyekt_Ma_lumotnomalar] - 필요수;
                if (남은길이 >= 2) { 힙폭[obyekt_Ma_lumotnomalar + 필요수] = 남은길이; 힙[obyekt_Ma_lumotnomalar + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { obyekt_Ma_lumotnomalar = 힙끝; 힙끝 += 필요수; }
        }
        if (obyekt_Ma_lumotnomalar == 0) { to_xtab_qolish_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[obyekt_Ma_lumotnomalar + Loop_INDEX] = 0; 힙참조[obyekt_Ma_lumotnomalar + Loop_INDEX] = 0; 힙폭[obyekt_Ma_lumotnomalar + Loop_INDEX] = 0; }
        ARRAY_element[obyekt_Ma_lumotnomalar] = 0;
        힙폭[obyekt_Ma_lumotnomalar] = 필요수; 힙[obyekt_Ma_lumotnomalar] = 종류; 힙[obyekt_Ma_lumotnomalar + 1] = uzunlik_VALUE; himoya_qilmoq_VALUE(obyekt_Ma_lumotnomalar); return obyekt_Ma_lumotnomalar;
    }
    static int istisno_Sinf(String nom_konstanta) {
        if (자바도구.같음(nom_konstanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nom_konstanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(nom_konstanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nom_konstanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nom_konstanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nom_konstanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nom_konstanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nom_konstanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nom_konstanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nom_konstanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nom_konstanta, "java/io/IOException")) return 11;
        if (자바도구.같음(nom_konstanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nom_konstanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nom_konstanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nom_konstanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int istisno_konstanta(int Nomi) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Nomi, istisno_nom(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String istisno_nom(int Guvohnoma_VALUE) {
        if (Guvohnoma_VALUE == 40) return "java/lang/InterruptedException";
        if (Guvohnoma_VALUE == 41) return "한국어/자체/대기중단예외";
        if (Guvohnoma_VALUE == 39) return "java/net/SocketException";
        if (Guvohnoma_VALUE == 20) return "한국어/자체/istisno";
        if (Guvohnoma_VALUE == 21) return "한국어/자체/실행예외";
        if (Guvohnoma_VALUE == 22) return "한국어/자체/I_O_istisno";
        if (Guvohnoma_VALUE == 23) return "한국어/자체/bir_daqiqa_TANAFFUS_istisno";
        if (Guvohnoma_VALUE == 24) return "한국어/자체/manzil_LOOKUP_istisno";
        if (Guvohnoma_VALUE == 25) return "한국어/자체/파일없음예외";
        if (Guvohnoma_VALUE == 26) return "한국어/자체/통신예외";
        if (Guvohnoma_VALUE == 27) return "한국어/자체/xato_dalil_istisno";
        if (Guvohnoma_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (Guvohnoma_VALUE == 29) return "한국어/자체/범위예외";
        if (Guvohnoma_VALUE == 30) return "한국어/자체/배열범위예외";
        if (Guvohnoma_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (Guvohnoma_VALUE == 32) return "한국어/자체/nul_Ma_lumotnomalar_istisno";
        if (Guvohnoma_VALUE == 33) return "한국어/자체/산술예외";
        if (Guvohnoma_VALUE == 34) return "한국어/자체/holat_istisno";
        if (Guvohnoma_VALUE == 35) return "한국어/자체/TYPE_uzatish_istisno";
        if (Guvohnoma_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (Guvohnoma_VALUE == 37) return "한국어/자체/ARRAY_Store_to_xtab_qolish";
        if (Guvohnoma_VALUE == 38) return "한국어/자체/oqim_holat_istisno";
        if (Guvohnoma_VALUE == 1) return "java/lang/Throwable"; if (Guvohnoma_VALUE == 2) return "java/lang/Exception";
        if (Guvohnoma_VALUE == 3) return "java/lang/RuntimeException"; if (Guvohnoma_VALUE == 4) return "java/lang/ArithmeticException";
        if (Guvohnoma_VALUE == 5) return "java/lang/NullPointerException"; if (Guvohnoma_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (Guvohnoma_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (Guvohnoma_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (Guvohnoma_VALUE == 9) return "java/lang/IllegalArgumentException"; if (Guvohnoma_VALUE == 10) return "java/lang/NumberFormatException";
        if (Guvohnoma_VALUE == 11) return "java/io/IOException"; if (Guvohnoma_VALUE == 12) return "java/io/FileNotFoundException";
        if (Guvohnoma_VALUE == 17) return "java/lang/ArrayStoreException";
        if (Guvohnoma_VALUE == 18) return "java/net/UnknownHostException";
        if (Guvohnoma_VALUE == 19) return "java/net/SocketTimeoutException";
        if (Guvohnoma_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (Guvohnoma_VALUE == 13) return "java/lang/IllegalStateException"; if (Guvohnoma_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int Guvohnoma_VALUE) {
        if (Guvohnoma_VALUE == 40) return 2;
        if (Guvohnoma_VALUE == 41) return 40;
        if (Guvohnoma_VALUE == 39) return 11;
        if (Guvohnoma_VALUE == 1) return 0;
        if (Guvohnoma_VALUE == 2) return 1;
        if (Guvohnoma_VALUE == 3) return 2;
        if (Guvohnoma_VALUE == 4) return 3;
        if (Guvohnoma_VALUE == 5) return 3;
        if (Guvohnoma_VALUE == 6) return 3;
        if (Guvohnoma_VALUE == 7) return 6;
        if (Guvohnoma_VALUE == 8) return 6;
        if (Guvohnoma_VALUE == 9) return 3;
        if (Guvohnoma_VALUE == 10) return 9;
        if (Guvohnoma_VALUE == 11) return 2;
        if (Guvohnoma_VALUE == 12) return 11;
        if (Guvohnoma_VALUE == 13) return 3;
        if (Guvohnoma_VALUE == 14) return 3;
        if (Guvohnoma_VALUE == 15) return 3;
        if (Guvohnoma_VALUE == 16) return 9;
        if (Guvohnoma_VALUE == 17) return 3;
        if (Guvohnoma_VALUE == 18) return 11;
        if (Guvohnoma_VALUE == 19) return 11;
        if (Guvohnoma_VALUE == 20) return 2;
        if (Guvohnoma_VALUE == 21) return 3;
        if (Guvohnoma_VALUE == 22) return 11;
        if (Guvohnoma_VALUE == 23) return 22;
        if (Guvohnoma_VALUE == 24) return 22;
        if (Guvohnoma_VALUE == 25) return 22;
        if (Guvohnoma_VALUE == 26) return 22;
        if (Guvohnoma_VALUE == 27) return 9;
        if (Guvohnoma_VALUE == 28) return 27;
        if (Guvohnoma_VALUE == 29) return 6;
        if (Guvohnoma_VALUE == 30) return 29;
        if (Guvohnoma_VALUE == 31) return 29;
        if (Guvohnoma_VALUE == 32) return 5;
        if (Guvohnoma_VALUE == 33) return 4;
        if (Guvohnoma_VALUE == 34) return 13;
        if (Guvohnoma_VALUE == 35) return 14;
        if (Guvohnoma_VALUE == 36) return 15;
        if (Guvohnoma_VALUE == 37) return 17;
        if (Guvohnoma_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int real_VALUE, int 요구값) {
        for (int 깊이 = 0; real_VALUE != 0 && 깊이 < 16; 깊이++, real_VALUE = 예외부모(real_VALUE))
            if (real_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int Guvohnoma_VALUE, String ma_lumot_fayli_Ma_lumotnomalar) {
        int obyekt_Ma_lumotnomalar = 새기억(9, 2); if (Xato) return;
        힙[obyekt_Ma_lumotnomalar + 2] = Guvohnoma_VALUE; 힙[obyekt_Ma_lumotnomalar + 3] = tashkilotchi_belgi(ma_lumot_fayli_Ma_lumotnomalar); 힙참조[obyekt_Ma_lumotnomalar + 3] = 1;
        던진객체 = obyekt_Ma_lumotnomalar; Xato = true;
    }
    static boolean 맞는객체(int obyekt_Ma_lumotnomalar, int Nomi) {
        if (obyekt_Ma_lumotnomalar == 0) return true;
        if (!객체유효(obyekt_Ma_lumotnomalar)) return false;
        int toifa_kod = 힙[obyekt_Ma_lumotnomalar];
        if (Word_SMS(Nomi, "java/lang/Object")) return true;
        if (toifa_kod >= 32) return 종포함(toifa_kod - 32, Nomi);
        if (toifa_kod == 9) { int maqsad_manzil = istisno_konstanta(Nomi); return maqsad_manzil != 0 && 예외포함(힙[obyekt_Ma_lumotnomalar + 2], maqsad_manzil); }
        if (toifa_kod == 1) return Word_SMS(Nomi, "java/lang/String") || Word_SMS(Nomi, "java/lang/CharSequence");
        if (toifa_kod == 4) return Word_SMS(Nomi, "java/lang/StringBuilder") || Word_SMS(Nomi, "java/lang/CharSequence");
        if (toifa_kod == 10) return Word_SMS(Nomi, "java/util/ArrayList") || Word_SMS(Nomi, "java/util/List");
        if (toifa_kod == 11) return Word_SMS(Nomi, "java/util/HashMap") || Word_SMS(Nomi, "java/util/Map");
        if (toifa_kod == 12) return Word_SMS(Nomi, "java/lang/Integer") || Word_SMS(Nomi, "java/lang/Number");
        if (toifa_kod >= 24 && toifa_kod <= 28 && 힙[obyekt_Ma_lumotnomalar + 13] != 0) return 한국어화면종(Nomi) == toifa_kod || Word_SMS(Nomi, "한국어/자체/화면구성요소");
        if (toifa_kod >= 24 && toifa_kod <= 28) return (한국어화면종(Nomi) == 0 && 화면종(Nomi) == toifa_kod) || Word_SMS(Nomi, "java/awt/Component") || Word_SMS(Nomi, "java/awt/Container") || Word_SMS(Nomi, "javax/swing/JComponent");
        if (toifa_kod == 29) return Word_SMS(Nomi, 힙[obyekt_Ma_lumotnomalar + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (toifa_kod == 30) return Word_SMS(Nomi, "java/awt/FlowLayout") || Word_SMS(Nomi, "java/awt/LayoutManager");
        if (toifa_kod == 17) return Word_SMS(Nomi, "java/net/Socket");
        if (toifa_kod == 18) return Word_SMS(Nomi, "java/net/ServerSocket");
        if (toifa_kod == 19) return Word_SMS(Nomi, 힙[obyekt_Ma_lumotnomalar + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (toifa_kod == 14) return Word_SMS(Nomi, "java/net/InetAddress");
        if (toifa_kod == 15) return Word_SMS(Nomi, "java/net/DatagramSocket");
        if (toifa_kod == 16) return Word_SMS(Nomi, "java/net/DatagramPacket");
        if (toifa_kod == 13) return Word_SMS(Nomi, 힙[obyekt_Ma_lumotnomalar + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (toifa_kod == 2) return Word_SMS(Nomi, "[I"); if (toifa_kod == 20) return Word_SMS(Nomi, "[B"); if (toifa_kod == 21) return Word_SMS(Nomi, "[Z");
        if (toifa_kod == 22) return Word_SMS(Nomi, "[C"); if (toifa_kod == 23) return Word_SMS(Nomi, "[S");
        if (toifa_kod != 3) return false;
        if (Word_SMS(Nomi, "[Ljava/lang/Object;")) return true;
        int tarkibiy_qism = ARRAY_element[obyekt_Ma_lumotnomalar];
        if (tarkibiy_qism == -1) return Word_SMS(Nomi, "[Ljava/lang/String;") || Word_SMS(Nomi, "[Ljava/lang/CharSequence;");
        if (tarkibiy_qism == 0) return false;
        if (배열종비교(tarkibiy_qism, Nomi)) return true;
        if ((Word_SMS(tarkibiy_qism, "java/lang/String") || Word_SMS(tarkibiy_qism, "java/lang/StringBuilder")) && Word_SMS(Nomi, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Sinf_Izoh_COUNT; Loop_INDEX++) if (같은말(Sinf_Izoh_nom[Loop_INDEX], tarkibiy_qism)) {
            for (int belgi_kodi = Loop_INDEX, 중첩깊이 = 0; belgi_kodi >= 0 && 중첩깊이 < 16; 중첩깊이++, belgi_kodi = 부모종(belgi_kodi)) {
                if (배열종비교(종부모[belgi_kodi], Nomi)) return true;
                for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < Sinf_interfeys_COUNT[belgi_kodi]; ichki_qo_shilish_holat++) if (배열종비교(Sinf_interfeys[belgi_kodi * 16 + ichki_qo_shilish_holat], Nomi)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nom_konstanta, int 형식참조) {
        int chek_holat = 상가[형식참조], kiritish_COUNT = konstanta_SECOND_VALUE[형식참조];
        if (nom_konstanta == 0 || kiritish_COUNT < 4 || Fayl[chek_holat] != '[' || Fayl[chek_holat + 1] != 'L' || Fayl[chek_holat + kiritish_COUNT - 1] != ';' || konstanta_SECOND_VALUE[nom_konstanta] != kiritish_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT - 3; Loop_INDEX++) if (Fayl[상가[nom_konstanta] + Loop_INDEX] != Fayl[chek_holat + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void deskriptor_istisno() {
        if (던진객체 == 0) return;
        Xato = false;
        while (kadr_INDEX >= 현재가닥 * 32) {
            int fayl_INDEX = kadr_uslub[kadr_INDEX], 읽는자리 = kadr_qo_llanma[kadr_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == fayl_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                kadr_holat[kadr_INDEX] = 잡기위치[Loop_INDEX]; kadr_Stack[kadr_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (ishga_tushirmoq_kadr[kadr_INDEX] != 0) Sinf_Izoh_holat[ishga_tushirmoq_kadr[kadr_INDEX] - 1] = 3;
            if (틀잠금[kadr_INDEX] != 0) { 잠금풀기(틀잠금[kadr_INDEX]); 틀잠금[kadr_INDEX] = 0; }
            kadr_INDEX--;
        }
        foydalanuvchi.Yozish("Uncaught ");
        if (힙[던진객체] == 9) { foydalanuvchi.Yozish(istisno_nom(힙[던진객체 + 2])); foydalanuvchi.Yozish(": "); yozmoq_SMS(힙[던진객체 + 3]); }
        else foydalanuvchi.Yozish("user exception");
        foydalanuvchi.yozmoq_belgi_VALUE(10); 던진객체 = 0; Xato = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Stack_qo_llanma(int buyruq_kod) {
        int 첫값 = 빼기(0), 첫형식 = qaytarish_TYPE;
        if (buyruq_kod == 87) return;
        if (buyruq_kod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bayt_ma_lumotlar = 빼기(0), SECOND_format = qaytarish_TYPE;
        if (buyruq_kod == 88) return;
        if (buyruq_kod == 90) { 넣기(첫값, 첫형식); 넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (buyruq_kod == 92) { 넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식); 넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (buyruq_kod == 95) { 넣기(첫값, 첫형식); 넣기(bayt_ma_lumotlar, SECOND_format); return; }
        int belgi_kodi = 빼기(0), 셋째형식 = qaytarish_TYPE;
        if (buyruq_kod == 91) { 넣기(첫값, 첫형식); 넣기(belgi_kodi, 셋째형식); 넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (buyruq_kod == 93) { 넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식); 넣기(belgi_kodi, 셋째형식); 넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = qaytarish_TYPE;
        넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(belgi_kodi, 셋째형식); 넣기(bayt_ma_lumotlar, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nom_konstanta, int 시작점) {
        int toifa_kod = 0, 유효길이 = 0, istisno_Ma_lumotnomalar = istisno_konstanta(nom_konstanta);
        if (Word_SMS(nom_konstanta, "java/lang/StringBuilder")) { toifa_kod = 4; 유효길이 = 1; }
        if (Word_SMS(nom_konstanta, "java/io/FileInputStream")) { toifa_kod = 5; 유효길이 = 2; }
        if (Word_SMS(nom_konstanta, "java/io/FileOutputStream")) { toifa_kod = 6; 유효길이 = 2; }
        if (istisno_Ma_lumotnomalar != 0) { toifa_kod = 9; 유효길이 = 2; }
        if (Word_SMS(nom_konstanta, "java/util/ArrayList")) { toifa_kod = 10; 유효길이 = 2; }
        if (Word_SMS(nom_konstanta, "java/util/HashMap")) { toifa_kod = 11; 유효길이 = 2; }
        if (Word_SMS(nom_konstanta, "java/lang/Integer")) { toifa_kod = 12; 유효길이 = 1; }
        if (Word_SMS(nom_konstanta, "java/net/Socket")) { toifa_kod = 17; 유효길이 = 5; }
        if (Word_SMS(nom_konstanta, "java/net/ServerSocket")) { toifa_kod = 18; 유효길이 = 5; }
        if (Word_SMS(nom_konstanta, "java/net/DatagramSocket")) { toifa_kod = 15; 유효길이 = 3; }
        if (Word_SMS(nom_konstanta, "java/net/DatagramPacket")) { toifa_kod = 16; 유효길이 = 4; }
        if (Word_SMS(nom_konstanta, "java/lang/Thread") || Word_SMS(nom_konstanta, "한국어/자체/작업가닥")) { toifa_kod = 13; 유효길이 = 2; }
        if (Word_SMS(nom_konstanta, "java/lang/Object")) { toifa_kod = 8; }
        if (toifa_kod == 0 && 화면종(nom_konstanta) != 0) { toifa_kod = 화면종(nom_konstanta); 유효길이 = 12; }
        if (toifa_kod == 0) {
            int belgi_kodi = FIND_Sinf_Izoh(nom_konstanta); if (belgi_kodi < 0 || Xato || !ishga_tushirmoq(belgi_kodi, 시작점)) return;
            toifa_kod = 32 + belgi_kodi; 유효길이 = Sinf_in_COUNT[belgi_kodi];
        }
        int obyekt_Ma_lumotnomalar = joylashtirmoq_Xotira(toifa_kod, 유효길이); if (Xato) return;
        if (toifa_kod == 13 && Word_SMS(nom_konstanta, "한국어/자체/작업가닥")) 힙[obyekt_Ma_lumotnomalar + 3] = 1;
        if (toifa_kod >= 24 && toifa_kod <= 28 && 한국어화면종(nom_konstanta) != 0) 힙[obyekt_Ma_lumotnomalar + 13] = 1;
        if (toifa_kod == 5 || toifa_kod == 6 || toifa_kod == 15 || toifa_kod == 17 || toifa_kod == 18) 힙[obyekt_Ma_lumotnomalar + 2] = -1;
        if (toifa_kod == 9) 힙[obyekt_Ma_lumotnomalar + 2] = istisno_Ma_lumotnomalar;
        넣기(obyekt_Ma_lumotnomalar, 2);
    }
    static boolean 값같음(int 첫값, int bayt_ma_lumotlar) {
        if (첫값 == bayt_ma_lumotlar) return true;
        if (첫값 == 0 || bayt_ma_lumotlar == 0 || 첫값 < 0 || bayt_ma_lumotlar < 0 || 첫값 >= 힙끝 || bayt_ma_lumotlar >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bayt_ma_lumotlar] == 1) return 글같음(첫값, bayt_ma_lumotlar, false);
        return 힙[첫값] == 12 && 힙[bayt_ma_lumotlar] == 12 && 힙[첫값 + 2] == 힙[bayt_ma_lumotlar + 2];
    }
    static int 글조각(int obyekt_Ma_lumotnomalar, int Start_holat, int to_xtatmoq_holat) {
        if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 1)) return 0;
        if (Start_holat < 0 || to_xtatmoq_holat < Start_holat || to_xtatmoq_holat > 힙[obyekt_Ma_lumotnomalar + 1]) { to_xtab_qolish_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = joylashtirmoq_Xotira(1, to_xtatmoq_holat - Start_holat); if (Xato) return 0;
        for (int Loop_INDEX = Start_holat; Loop_INDEX < to_xtatmoq_holat; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Start_holat] = 힙[obyekt_Ma_lumotnomalar + 2 + Loop_INDEX];
        return 반환값;
    }
    static int bog_lanish_SMS(int 첫값, int bayt_ma_lumotlar) {
        if (!obyekt_VALUE(첫값, 1) || !obyekt_VALUE(bayt_ma_lumotlar, 1)) return 0;
        int kiritish_COUNT = 힙[첫값 + 1], uslub_INDEX = 힙[bayt_ma_lumotlar + 1], 반환값 = joylashtirmoq_Xotira(1, kiritish_COUNT + uslub_INDEX); if (Xato) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < uslub_INDEX; Loop_INDEX++) 힙[반환값 + 2 + kiritish_COUNT + Loop_INDEX] = 힙[bayt_ma_lumotlar + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int egasi, int nom_konstanta, int 서술상수, int buyruq_kod) {
        if (Word_SMS(egasi, "한국어/자체/실행인수") && buyruq_kod == 184) {
            if (Word_SMS(nom_konstanta, "element_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(foydalanuvchi.인수개수() - 1, 1); return true; }
            if (Word_SMS(nom_konstanta, "Matn") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= foydalanuvchi.인수개수() - 1) 예외던짐(29, "bajarmoq_buyruq 인수 범위를 벗어났습니다");
                else 넣기(tashkilotchi_belgi(foydalanuvchi.인수(순번 + 1)), 2);
                return true;
            }
            to_xtab_qolish_VALUE("지원하지 않는 한국어 bajarmoq_buyruq 인수 호출"); return true;
        }
        if (Word_SMS(egasi, "한국어/자체/작업가닥")) { Jarayon_oqim(nom_konstanta, 서술상수, buyruq_kod, true); return true; }
        if (한국어화면소유(egasi)) { 한국어화면호출(egasi, nom_konstanta, 서술상수, buyruq_kod); return true; }
        if (화면소유(egasi)) { 화면호출(egasi, nom_konstanta, 서술상수, buyruq_kod); return true; }
        if (Word_SMS(egasi, "java/net/Socket") || Word_SMS(egasi, "java/net/ServerSocket") || Word_SMS(egasi, "java/io/InputStream") || Word_SMS(egasi, "java/io/OutputStream")) { 흐름호출(egasi, nom_konstanta, 서술상수, buyruq_kod); return true; }
        if (Word_SMS(egasi, "한국어/자체/o_zak_VALUE") && buyruq_kod == 184) {
            if (Word_SMS(nom_konstanta, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(foydalanuvchi.화면너비(), 1); return true; }
            if (Word_SMS(nom_konstanta, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(foydalanuvchi.화면높이(), 1); return true; }
            if (Word_SMS(nom_konstanta, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(foydalanuvchi.밀리초(), 1); return true; }
            if (Word_SMS(nom_konstanta, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(foydalanuvchi.그림대기(), 1); return true; }
            if (Word_SMS(nom_konstanta, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_tugmasi_koordinat = 빼기(1), x_koordinata = 빼기(1); 넣기(foydalanuvchi.사각형(x_koordinata, Y_tugmasi_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(egasi, "java/net/InetAddress") || Word_SMS(egasi, "java/net/DatagramPacket") || Word_SMS(egasi, "java/net/DatagramSocket")) { 통신호출(egasi, nom_konstanta, 서술상수, buyruq_kod); return true; }
        if (Word_SMS(egasi, "java/lang/Thread")) { 가닥호출(nom_konstanta, 서술상수, buyruq_kod); return true; }
        if (Word_SMS(egasi, "java/lang/Object")) {
            if (Word_SMS(nom_konstanta, "<init>") && Word_SMS(서술상수, "()V") && buyruq_kod == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(nom_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayt_ma_lumotlar = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bayt_ma_lumotlar ? 1 : 0, 1); return true; }
        }
        if (istisno_konstanta(egasi) != 0) {
            if (Word_SMS(nom_konstanta, "<init>") && buyruq_kod == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int so_rov = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2);
                if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 9)) { 힙[obyekt_Ma_lumotnomalar + 3] = so_rov; 힙참조[obyekt_Ma_lumotnomalar + 3] = 1; } return true;
            }
            if ((Word_SMS(nom_konstanta, "getMessage") || Word_SMS(nom_konstanta, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 9)) 넣기(힙[obyekt_Ma_lumotnomalar + 3], 2); return true; }
        }
        if (Word_SMS(egasi, "java/lang/String")) {
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodlash_nom = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2);
                if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 1)) return true;
                if (kodlash_nom != 0 && !글같음(kodlash_nom, tashkilotchi_belgi("UTF-8"), false) && !글같음(kodlash_nom, tashkilotchi_belgi("UTF8"), false) && !글같음(kodlash_nom, tashkilotchi_belgi("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int kiritish_COUNT = 힙[obyekt_Ma_lumotnomalar + 1], 반환값 = joylashtirmoq_Xotira(20, kiritish_COUNT * 3), 사용수 = 0; if (Xato) return true;
                for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < kiritish_COUNT; ichki_qo_shilish_holat++) {
                    int belgi_kodi = 힙[obyekt_Ma_lumotnomalar + 2 + ichki_qo_shilish_holat];
                    if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdbff && ichki_qo_shilish_holat + 1 < kiritish_COUNT && 힙[obyekt_Ma_lumotnomalar + 3 + ichki_qo_shilish_holat] >= 0xdc00 && 힙[obyekt_Ma_lumotnomalar + 3 + ichki_qo_shilish_holat] <= 0xdfff) belgi_kodi = 0x10000 + ((belgi_kodi - 0xd800) << 10) + 힙[obyekt_Ma_lumotnomalar + 2 + ++ichki_qo_shilish_holat] - 0xdc00;
                    else if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdfff) belgi_kodi = '?';
                    if (belgi_kodi < 128) 힙[반환값 + 2 + 사용수++] = belgi_kodi;
                    else { int bayt_COUNT = belgi_kodi < 2048 ? 2 : belgi_kodi < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((bayt_COUNT == 2 ? 192 : bayt_COUNT == 3 ? 224 : 240) | belgi_kodi >> (6 * (bayt_COUNT - 1))); for (int Taqqoslama_holat = bayt_COUNT - 1; Taqqoslama_holat > 0; Taqqoslama_holat--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | belgi_kodi >> (6 * (Taqqoslama_holat - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(raqam_belgi(빼기(1)), 2); return true; }
            if (buyruq_kod != 182) return false;
            if (Word_SMS(nom_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayt_ma_lumotlar = 빼기(2), 첫값 = 빼기(2); if (obyekt_VALUE(첫값, 1)) 넣기(글같음(첫값, bayt_ma_lumotlar, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nom_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (obyekt_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nom_konstanta, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int to_xtatmoq_holat = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (obyekt_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? to_xtatmoq_holat : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nom_konstanta, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bayt_ma_lumotlar = 빼기(2), 첫값 = 빼기(2); 넣기(bog_lanish_SMS(첫값, bayt_ma_lumotlar), 2); return true; }
            if (Word_SMS(nom_konstanta, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), tasodifiy_ma_lumot_VALUE = 0; if (obyekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) tasodifiy_ma_lumot_VALUE = tasodifiy_ma_lumot_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(tasodifiy_ma_lumot_VALUE, 1); } return true; }
            if (Word_SMS(nom_konstanta, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (obyekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(egasi, "java/lang/Integer")) {
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int ma_lumotlar_VALUE = 빼기(1), obyekt_Ma_lumotnomalar = ma_lumotlar_VALUE >= -128 && ma_lumotlar_VALUE <= 127 ? Store_butun_son[ma_lumotlar_VALUE + 128] : 0; if (obyekt_Ma_lumotnomalar == 0) { obyekt_Ma_lumotnomalar = joylashtirmoq_Xotira(12, 1); if (!Xato) { 힙[obyekt_Ma_lumotnomalar + 2] = ma_lumotlar_VALUE; if (ma_lumotlar_VALUE >= -128 && ma_lumotlar_VALUE <= 127) Store_butun_son[ma_lumotlar_VALUE + 128] = obyekt_Ma_lumotnomalar; } } 넣기(obyekt_Ma_lumotnomalar, 2); return true; }
            if (buyruq_kod == 183 && Word_SMS(nom_konstanta, "<init>") && Word_SMS(서술상수, "(I)V")) { int ma_lumotlar_VALUE = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 12)) 힙[obyekt_Ma_lumotnomalar + 2] = ma_lumotlar_VALUE; return true; }
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "intValue") && Word_SMS(서술상수, "()I")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 12)) 넣기(힙[obyekt_Ma_lumotnomalar + 2], 1); return true; }
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(raqam_belgi(빼기(1)), 2); return true; }
        }
        if (Word_SMS(egasi, "java/lang/Math") && buyruq_kod == 184) {
            if (Word_SMS(nom_konstanta, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nom_konstanta, "min") || Word_SMS(nom_konstanta, "max")) && Word_SMS(서술상수, "(II)I")) { int bayt_ma_lumotlar = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nom_konstanta, "min") ? (첫값 < bayt_ma_lumotlar ? 첫값 : bayt_ma_lumotlar) : (첫값 > bayt_ma_lumotlar ? 첫값 : bayt_ma_lumotlar), 1); return true; }
        }
        if (Word_SMS(egasi, "java/lang/System") && buyruq_kod == 184) {
            if (Word_SMS(nom_konstanta, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(nom_konstanta, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int kiritish_COUNT = 빼기(1), ko_chirish_joyi_VALUE_INDEX = 빼기(1), bayt_ma_lumotlar = 빼기(2), Start_holat = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bayt_ma_lumotlar)) {
                    int toifa_kod = 힙[첫값];
                    if (힙[bayt_ma_lumotlar] != toifa_kod || (toifa_kod != 2 && toifa_kod != 3 && (toifa_kod < 20 || toifa_kod > 23))) to_xtab_qolish_VALUE("arraycopy type mismatch");
                    else if (kiritish_COUNT < 0 || Start_holat < 0 || ko_chirish_joyi_VALUE_INDEX < 0 || Start_holat > 힙[첫값 + 1] - kiritish_COUNT || ko_chirish_joyi_VALUE_INDEX > 힙[bayt_ma_lumotlar + 1] - kiritish_COUNT) to_xtab_qolish_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bayt_ma_lumotlar && ko_chirish_joyi_VALUE_INDEX > Start_holat) { for (int Loop_INDEX = kiritish_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[bayt_ma_lumotlar + 2 + ko_chirish_joyi_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Start_holat + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT && !Xato; Loop_INDEX++) { int ma_lumotlar_VALUE = 힙[첫값 + 2 + Start_holat + Loop_INDEX]; if (toifa_kod != 3 || 배열저장가능(bayt_ma_lumotlar, ma_lumotlar_VALUE)) 힙[bayt_ma_lumotlar + 2 + ko_chirish_joyi_VALUE_INDEX + Loop_INDEX] = ma_lumotlar_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(egasi, "java/util/ArrayList") || Word_SMS(egasi, "java/util/List") || Word_SMS(egasi, "java/util/HashMap") || Word_SMS(egasi, "java/util/Map")) {
            모음호출(egasi, nom_konstanta, 서술상수, buyruq_kod); return true;
        }
        return false;
    }
    static void 모음늘리기(int obyekt_Ma_lumotnomalar, int 필요수) {
        int 이전값 = 힙[obyekt_Ma_lumotnomalar + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Keyingi_holat = 용량값 < 8 ? 8 : 용량값 * 2; if (Keyingi_holat < 필요수) Keyingi_holat = 필요수;
        int ma_lumotlar_ARRAY = joylashtirmoq_Xotira(3, Keyingi_holat); if (Xato) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[ma_lumotlar_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[obyekt_Ma_lumotnomalar + 2] = ma_lumotlar_ARRAY; 힙참조[obyekt_Ma_lumotnomalar + 2] = 1;
    }
    static void 모음호출(int egasi, int nom_konstanta, int 서술상수, int buyruq_kod) {
        boolean 대응참조 = Word_SMS(egasi, "java/util/HashMap") || Word_SMS(egasi, "java/util/Map"); int toifa_kod = 대응참조 ? 11 : 10;
        if (Word_SMS(nom_konstanta, "<init>") && buyruq_kod == 183 && Word_SMS(서술상수, "()V")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, toifa_kod)) 모음늘리기(obyekt_Ma_lumotnomalar, 8); return; }
        if (buyruq_kod != 182 && buyruq_kod != 185) { to_xtab_qolish_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(nom_konstanta, "size") && Word_SMS(서술상수, "()I") || Word_SMS(nom_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, toifa_kod)) 넣기(Word_SMS(nom_konstanta, "size") ? 힙[obyekt_Ma_lumotnomalar + 3] : 힙[obyekt_Ma_lumotnomalar + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nom_konstanta, "clear") && Word_SMS(서술상수, "()V")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, toifa_kod)) { int ma_lumotlar_ARRAY = 힙[obyekt_Ma_lumotnomalar + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[ma_lumotlar_ARRAY + 1]; Loop_INDEX++) 힙[ma_lumotlar_ARRAY + 2 + Loop_INDEX] = 0; 힙[obyekt_Ma_lumotnomalar + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nom_konstanta, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int ma_lumotlar_VALUE = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 10)) return;
            int kiritish_COUNT = 힙[obyekt_Ma_lumotnomalar + 3]; 모음늘리기(obyekt_Ma_lumotnomalar, kiritish_COUNT + 1); if (!Xato) { 힙[힙[obyekt_Ma_lumotnomalar + 2] + 2 + kiritish_COUNT] = ma_lumotlar_VALUE; 힙[obyekt_Ma_lumotnomalar + 3] = kiritish_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nom_konstanta, "get") || Word_SMS(nom_konstanta, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nom_konstanta, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(nom_konstanta, "set"); int ma_lumotlar_VALUE = 지정여부 ? 빼기(2) : 0, kiritish_holat = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2);
            if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 10)) return;
            int kiritish_COUNT = 힙[obyekt_Ma_lumotnomalar + 3], ma_lumotlar_ARRAY = 힙[obyekt_Ma_lumotnomalar + 2];
            if (kiritish_holat < 0 || kiritish_holat >= kiritish_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[ma_lumotlar_ARRAY + 2 + kiritish_holat];
            if (지정여부) 힙[ma_lumotlar_ARRAY + 2 + kiritish_holat] = ma_lumotlar_VALUE;
            if (Word_SMS(nom_konstanta, "remove")) { for (int Loop_INDEX = kiritish_holat + 1; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) 힙[ma_lumotlar_ARRAY + 1 + Loop_INDEX] = 힙[ma_lumotlar_ARRAY + 2 + Loop_INDEX]; 힙[ma_lumotlar_ARRAY + 1 + kiritish_COUNT] = 0; 힙[obyekt_Ma_lumotnomalar + 3] = kiritish_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(nom_konstanta, "get") || Word_SMS(nom_konstanta, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nom_konstanta, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nom_konstanta, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nom_konstanta, "put"), olib_tashlamoq = Word_SMS(nom_konstanta, "remove");
            int ma_lumotlar_VALUE = 넣기여부 ? 빼기(2) : 0, Kalit_Ma_lumotnomalar = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 11)) return;
            int kiritish_COUNT = 힙[obyekt_Ma_lumotnomalar + 3], ma_lumotlar_ARRAY = 힙[obyekt_Ma_lumotnomalar + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) if (값같음(Kalit_Ma_lumotnomalar, 힙[ma_lumotlar_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[ma_lumotlar_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(obyekt_Ma_lumotnomalar, (kiritish_COUNT + 1) * 2); ma_lumotlar_ARRAY = 힙[obyekt_Ma_lumotnomalar + 2]; 찾은여부 = kiritish_COUNT; if (!Xato) 힙[obyekt_Ma_lumotnomalar + 3] = kiritish_COUNT + 1; }
                if (!Xato) { 힙[ma_lumotlar_ARRAY + 2 + 2 * 찾은여부] = Kalit_Ma_lumotnomalar; 힙[ma_lumotlar_ARRAY + 3 + 2 * 찾은여부] = ma_lumotlar_VALUE; }
            }
            if (olib_tashlamoq && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) { 힙[ma_lumotlar_ARRAY + 2 * Loop_INDEX] = 힙[ma_lumotlar_ARRAY + 2 + 2 * Loop_INDEX]; 힙[ma_lumotlar_ARRAY + 1 + 2 * Loop_INDEX] = 힙[ma_lumotlar_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[ma_lumotlar_ARRAY + 2 * kiritish_COUNT] = 0; 힙[ma_lumotlar_ARRAY + 1 + 2 * kiritish_COUNT] = 0; 힙[obyekt_Ma_lumotnomalar + 3] = kiritish_COUNT - 1; }
            if (Word_SMS(nom_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        to_xtab_qolish_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int obyekt_Ma_lumotnomalar) {
        if (!객체유효(obyekt_Ma_lumotnomalar)) return false;
        if (잠금깊이[obyekt_Ma_lumotnomalar] != 0 && 잠금주인[obyekt_Ma_lumotnomalar] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[obyekt_Ma_lumotnomalar] = 현재가닥 + 1; 잠금깊이[obyekt_Ma_lumotnomalar]++; return true;
    }
    static void 잠금풀기(int obyekt_Ma_lumotnomalar) {
        if (!객체유효(obyekt_Ma_lumotnomalar)) return;
        if (잠금깊이[obyekt_Ma_lumotnomalar] == 0 || 잠금주인[obyekt_Ma_lumotnomalar] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[obyekt_Ma_lumotnomalar] == 0) 잠금주인[obyekt_Ma_lumotnomalar] = 0;
    }
    static boolean SWITCH_oqim() {
        oqim_kadr[현재가닥] = kadr_INDEX;
        if (kadr_INDEX < 현재가닥 * 32) oqim_holat[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < oqim_COUNT; Loop_INDEX++) if (oqim_holat[Loop_INDEX] == 2 && oqim_holat[가닥대기[Loop_INDEX]] == 3) oqim_holat[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= oqim_COUNT; Loop_INDEX++) {
            int Keyingi_holat = (현재가닥 + Loop_INDEX) % oqim_COUNT;
            if (oqim_holat[Keyingi_holat] == 1) { 현재가닥 = Keyingi_holat; kadr_INDEX = oqim_kadr[Keyingi_holat]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < oqim_COUNT; Loop_INDEX++) if (oqim_holat[Loop_INDEX] != 3) { to_xtab_qolish_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nom_konstanta, int 서술상수, int buyruq_kod) { Jarayon_oqim(nom_konstanta, 서술상수, buyruq_kod, false); }
    static void Jarayon_oqim(int nom_konstanta, int 서술상수, int buyruq_kod, boolean 한국어) {
        if (buyruq_kod == 184 && Word_SMS(nom_konstanta, 한국어 ? "YIELD_vazifa" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(oqim_obyekt[현재가닥], 2); return; }
        if (buyruq_kod == 183 && Word_SMS(nom_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int maqsad_manzil = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2);
            if (!객체유효(obyekt_Ma_lumotnomalar)) return;
            if (힙[obyekt_Ma_lumotnomalar] == 13) { 힙[obyekt_Ma_lumotnomalar + 2] = maqsad_manzil; 힙참조[obyekt_Ma_lumotnomalar + 2] = 1; }
            else if (maqsad_manzil != 0) to_xtab_qolish_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (buyruq_kod == 182 && (Word_SMS(nom_konstanta, 한국어 ? "Start_vazifa" : "start") || Word_SMS(nom_konstanta, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || buyruq_kod == 182 && Word_SMS(nom_konstanta, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int obyekt_Ma_lumotnomalar = 빼기(2); if (!객체유효(obyekt_Ma_lumotnomalar)) return;
            int Guvohnoma_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < oqim_COUNT; Loop_INDEX++) if (oqim_obyekt[Loop_INDEX] == obyekt_Ma_lumotnomalar) Guvohnoma_VALUE = Loop_INDEX;
            if (Word_SMS(nom_konstanta, 한국어 ? "살아있는가" : "isAlive")) { 넣기(Guvohnoma_VALUE >= 0 && oqim_holat[Guvohnoma_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nom_konstanta, 한국어 ? "기다리기" : "join")) { if (Guvohnoma_VALUE >= 0 && oqim_holat[Guvohnoma_VALUE] != 3) { 가닥대기[현재가닥] = Guvohnoma_VALUE; oqim_holat[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (Guvohnoma_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (oqim_COUNT == 4) { to_xtab_qolish_VALUE("thread limit (4 including main)"); return; }
            int maqsad_manzil = 힙[obyekt_Ma_lumotnomalar] == 13 ? 힙[obyekt_Ma_lumotnomalar + 2] : obyekt_Ma_lumotnomalar;
            int fayl_INDEX = maqsad_manzil > 0 && 힙[maqsad_manzil] >= 32 ? nom_uslub(힙[maqsad_manzil] - 32, 한국어 ? "Ishga_tushirish" : "run", "()V") : -1;
            if (maqsad_manzil != 0 && fayl_INDEX < 0) { to_xtab_qolish_VALUE("Runnable.run required"); return; }
            Guvohnoma_VALUE = oqim_COUNT++; oqim_obyekt[Guvohnoma_VALUE] = obyekt_Ma_lumotnomalar; oqim_maqsad[Guvohnoma_VALUE] = maqsad_manzil;
            int kadr = Guvohnoma_VALUE * 32; oqim_kadr[Guvohnoma_VALUE] = fayl_INDEX < 0 ? kadr - 1 : kadr; oqim_holat[Guvohnoma_VALUE] = fayl_INDEX < 0 ? 3 : 1;
            if (fayl_INDEX >= 0) { kadr_uslub[kadr] = fayl_INDEX; kadr_holat[kadr] = uslub_Start[fayl_INDEX]; mahalliy_VALUE[kadr * 128] = maqsad_manzil; mahalliy_TYPE[kadr * 128] = 2; }
            return;
        }
        to_xtab_qolish_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], manzil_SMS = new int[16];
    static int mahalliy_manzil() { return manzil_obyekt(0x7f000001); }
    static int manzil_obyekt(int VALUE) { int obyekt_Ma_lumotnomalar = joylashtirmoq_Xotira(14, 1); if (!Xato) 힙[obyekt_Ma_lumotnomalar + 2] = VALUE; return obyekt_Ma_lumotnomalar; }
    static int 주소해독(int obyekt_Ma_lumotnomalar) {
        if (obyekt_Ma_lumotnomalar == 0 || 글같음(obyekt_Ma_lumotnomalar, tashkilotchi_belgi("localhost"), false)) return 0x7f000001;
        if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 1)) return 0;
        int ma_lumotlar_VALUE = 0, 총수 = 0, manzil_bayt = 0, 자릿수 = 0, kiritish_COUNT = 힙[obyekt_Ma_lumotnomalar + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= kiritish_COUNT; Loop_INDEX++) {
            int belgi_kodi = Loop_INDEX == kiritish_COUNT ? '.' : 힙[obyekt_Ma_lumotnomalar + 2 + Loop_INDEX];
            if (belgi_kodi == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } ma_lumotlar_VALUE = ma_lumotlar_VALUE << 8 | manzil_bayt; 총수++; manzil_bayt = 자릿수 = 0; }
            else { if (belgi_kodi < '0' || belgi_kodi > '9' || ++자릿수 > 3 || (manzil_bayt = manzil_bayt * 10 + belgi_kodi - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return ma_lumotlar_VALUE;
    }
    static int manzil_belgi(int ma_lumotlar_VALUE) {
        int kiritish_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int manzil_bayt = ma_lumotlar_VALUE >>> 이동비트 & 255;
            if (manzil_bayt >= 100) manzil_SMS[kiritish_COUNT++] = '0' + manzil_bayt / 100;
            if (manzil_bayt >= 10) manzil_SMS[kiritish_COUNT++] = '0' + manzil_bayt / 10 % 10;
            manzil_SMS[kiritish_COUNT++] = '0' + manzil_bayt % 10; if (이동비트 != 0) manzil_SMS[kiritish_COUNT++] = '.';
        }
        int obyekt_Ma_lumotnomalar = joylashtirmoq_Xotira(1, kiritish_COUNT); if (!Xato) for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) 힙[obyekt_Ma_lumotnomalar + 2 + Loop_INDEX] = manzil_SMS[Loop_INDEX]; return obyekt_Ma_lumotnomalar;
    }
    static void 통신호출(int egasi, int nom_konstanta, int 서술상수, int buyruq_kod) {
        if (Word_SMS(egasi, "java/net/InetAddress")) {
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(mahalliy_manzil(), 2); return; }
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int ma_lumotlar_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Xato) 넣기(manzil_obyekt(ma_lumotlar_VALUE), 2); return;
            }
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 14)) 넣기(manzil_belgi(힙[obyekt_Ma_lumotnomalar + 2]), 2); return; }
        }
        if (Word_SMS(egasi, "java/net/DatagramPacket")) {
            if (buyruq_kod == 183 && Word_SMS(nom_konstanta, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean ko_chirish_joyi_VALUE_Ma_lumotnomalar = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = ko_chirish_joyi_VALUE_Ma_lumotnomalar ? 빼기(1) : 0, manzil_Ma_lumotnomalar = ko_chirish_joyi_VALUE_Ma_lumotnomalar ? 빼기(2) : 0;
                int kiritish_COUNT = 빼기(1), ma_lumotlar_ARRAY = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2);
                if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 16) || !obyekt_VALUE(ma_lumotlar_ARRAY, 20)) return;
                if (kiritish_COUNT < 0 || kiritish_COUNT > 힙[ma_lumotlar_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (manzil_Ma_lumotnomalar != 0 && !obyekt_VALUE(manzil_Ma_lumotnomalar, 14)) return;
                힙[obyekt_Ma_lumotnomalar + 2] = ma_lumotlar_ARRAY; 힙참조[obyekt_Ma_lumotnomalar + 2] = 1; 힙[obyekt_Ma_lumotnomalar + 3] = kiritish_COUNT;
                힙[obyekt_Ma_lumotnomalar + 4] = manzil_Ma_lumotnomalar; 힙참조[obyekt_Ma_lumotnomalar + 4] = 1; 힙[obyekt_Ma_lumotnomalar + 5] = 접속번호; return;
            }
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int kiritish_COUNT = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 16)) return;
                if (kiritish_COUNT < 0 || kiritish_COUNT > 힙[힙[obyekt_Ma_lumotnomalar + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[obyekt_Ma_lumotnomalar + 3] = kiritish_COUNT; return;
            }
            if (buyruq_kod == 182 && (Word_SMS(nom_konstanta, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(nom_konstanta, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(nom_konstanta, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(nom_konstanta, "getPort") && Word_SMS(서술상수, "()I"))) {
                int obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 16)) return;
                int kiritish_holat = Word_SMS(nom_konstanta, "getData") ? 2 : Word_SMS(nom_konstanta, "getLength") ? 3 : Word_SMS(nom_konstanta, "getAddress") ? 4 : 5;
                넣기(힙[obyekt_Ma_lumotnomalar + kiritish_holat], kiritish_holat == 2 || kiritish_holat == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(egasi, "java/net/DatagramSocket")) {
            if (buyruq_kod == 183 && Word_SMS(nom_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = foydalanuvchi.ochmoq_Tarmoq(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[obyekt_Ma_lumotnomalar + 2] = 열린파일번호; return;
            }
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obyekt_Ma_lumotnomalar + 3] = 밀리초값; return;
            }
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "getLocalPort") && Word_SMS(서술상수, "()I")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 15)) 넣기(힙[obyekt_Ma_lumotnomalar + 2] < 0 ? -1 : foydalanuvchi.Tarmoq_port(힙[obyekt_Ma_lumotnomalar + 2]), 1); return; }
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "isClosed") && Word_SMS(서술상수, "()Z")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 15)) 넣기(힙[obyekt_Ma_lumotnomalar + 2] < 0 ? 1 : 0, 1); return; }
            if (buyruq_kod == 182 && Word_SMS(nom_konstanta, "close") && Word_SMS(서술상수, "()V")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 15) && 힙[obyekt_Ma_lumotnomalar + 2] >= 0) { foydalanuvchi.파일서술자닫기(힙[obyekt_Ma_lumotnomalar + 2]); 힙[obyekt_Ma_lumotnomalar + 2] = -1; } return; }
            if (buyruq_kod == 182 && (Word_SMS(nom_konstanta, "send") || Word_SMS(nom_konstanta, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(전문참조, 16) || !obyekt_VALUE(obyekt_Ma_lumotnomalar, 15)) return;
                int ma_lumotlar_ARRAY = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[obyekt_Ma_lumotnomalar + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nom_konstanta, "send")) {
                    if (!obyekt_VALUE(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[ma_lumotlar_ARRAY + 2 + Loop_INDEX];
                    if (foydalanuvchi.yuborish_Tarmoq(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int kiritish_COUNT = foydalanuvchi.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (kiritish_COUNT == -11) {
                        int 현재시각 = foydalanuvchi.밀리초();
                        if (힙[obyekt_Ma_lumotnomalar + 4] == 0) 힙[obyekt_Ma_lumotnomalar + 4] = 현재시각 + 1;
                        if (힙[obyekt_Ma_lumotnomalar + 3] > 0 && 현재시각 - (힙[obyekt_Ma_lumotnomalar + 4] - 1) >= 힙[obyekt_Ma_lumotnomalar + 3]) { 힙[obyekt_Ma_lumotnomalar + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(obyekt_Ma_lumotnomalar, 2); 넣기(전문참조, 2); kadr_holat[kadr_INDEX] = kadr_qo_llanma[kadr_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[obyekt_Ma_lumotnomalar + 4] = 0;
                    if (kiritish_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) 힙[ma_lumotlar_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[전문참조 + 3] = kiritish_COUNT; 힙[전문참조 + 4] = manzil_obyekt(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        to_xtab_qolish_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int obyekt_Ma_lumotnomalar) {
        int 현재시각 = foydalanuvchi.밀리초();
        if (힙[obyekt_Ma_lumotnomalar + 5] == 0) 힙[obyekt_Ma_lumotnomalar + 5] = 현재시각 + 1;
        if (힙[obyekt_Ma_lumotnomalar + 3] > 0 && 현재시각 - (힙[obyekt_Ma_lumotnomalar + 5] - 1) >= 힙[obyekt_Ma_lumotnomalar + 3]) { 힙[obyekt_Ma_lumotnomalar + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadr_holat[kadr_INDEX] = kadr_qo_llanma[kadr_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int egasi, int nom_konstanta, int 서술상수, int buyruq_kod) {
        boolean 수신쪽 = Word_SMS(egasi, "java/net/ServerSocket"), oqim = Word_SMS(egasi, "java/io/InputStream") || Word_SMS(egasi, "java/io/OutputStream");
        if (!oqim && buyruq_kod == 183 && Word_SMS(nom_konstanta, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { to_xtab_qolish_VALUE("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), manzil_Ma_lumotnomalar = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, obyekt_Ma_lumotnomalar = 빼기(2);
            if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !obyekt_VALUE(manzil_Ma_lumotnomalar, 14)) return;
            int Tarmoq_manzil = 이름지정여부 ? 주소해독(manzil_Ma_lumotnomalar) : 주소지정여부 ? 힙[manzil_Ma_lumotnomalar + 2] : 0x7f000001;
            if (Xato || 던진객체 != 0) return;
            int 열린파일번호 = foydalanuvchi.oqim_boshqaruv(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? foydalanuvchi.oqim_boshqaruv(1, 열린파일번호, 접속번호) : foydalanuvchi.ulash_oqim(열린파일번호, Tarmoq_manzil, 접속번호);
            if (처리값 < 0) { foydalanuvchi.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[obyekt_Ma_lumotnomalar + 2] = 열린파일번호; 힙[obyekt_Ma_lumotnomalar + 4] = 접속번호; 힙[obyekt_Ma_lumotnomalar + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!oqim && Word_SMS(nom_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obyekt_Ma_lumotnomalar + 3] = 밀리초값; return; }
        if (!oqim && Word_SMS(nom_konstanta, "close") && Word_SMS(서술상수, "()V")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (obyekt_VALUE(obyekt_Ma_lumotnomalar, 수신쪽 ? 18 : 17) && 힙[obyekt_Ma_lumotnomalar + 2] >= 0) { foydalanuvchi.파일서술자닫기(힙[obyekt_Ma_lumotnomalar + 2]); 힙[obyekt_Ma_lumotnomalar + 2] = -1; } return; }
        if (!oqim && (Word_SMS(nom_konstanta, "getLocalPort") || Word_SMS(nom_konstanta, "getPort") || Word_SMS(nom_konstanta, "isClosed") || Word_SMS(nom_konstanta, "isConnected"))) {
            int obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(nom_konstanta, "isClosed") ? 힙[obyekt_Ma_lumotnomalar + 2] < 0 ? 1 : 0 : Word_SMS(nom_konstanta, "isConnected") ? 힙[obyekt_Ma_lumotnomalar + 6] : Word_SMS(nom_konstanta, "getPort") ? 힙[obyekt_Ma_lumotnomalar + 4] : 힙[obyekt_Ma_lumotnomalar + 2] < 0 ? -1 : foydalanuvchi.oqim_boshqaruv(4, 힙[obyekt_Ma_lumotnomalar + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(nom_konstanta, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 18)) return; int 열린파일번호 = foydalanuvchi.oqim_boshqaruv(3, 힙[obyekt_Ma_lumotnomalar + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(obyekt_Ma_lumotnomalar)) 넣기(obyekt_Ma_lumotnomalar, 2); return; }
            힙[obyekt_Ma_lumotnomalar + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = joylashtirmoq_Xotira(17, 5); if (Xato) { foydalanuvchi.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = foydalanuvchi.oqim_boshqaruv(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !oqim && ((Word_SMS(nom_konstanta, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(nom_konstanta, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 17)) return; if (힙[obyekt_Ma_lumotnomalar + 2] < 0 || 힙[obyekt_Ma_lumotnomalar + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = joylashtirmoq_Xotira(19, 4); if (Xato) return; 힙[반환값 + 2] = obyekt_Ma_lumotnomalar; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(nom_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (oqim) {
            boolean 읽기여부 = Word_SMS(nom_konstanta, "read"), 쓰기여부 = Word_SMS(nom_konstanta, "write"), bloklash = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), 부분배열여부 = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int kiritish_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, ma_lumotlar_ARRAY = bloklash || 부분배열여부 ? 빼기(2) : 0;
            int ma_lumotlar_VALUE = 쓰기여부 && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, obyekt_Ma_lumotnomalar = 빼기(2);
            if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 19)) return; int 부모참조 = 힙[obyekt_Ma_lumotnomalar + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nom_konstanta, "close") && Word_SMS(서술상수, "()V")) { foydalanuvchi.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(nom_konstanta, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[obyekt_Ma_lumotnomalar + 3] == 0)) { to_xtab_qolish_VALUE("unsupported stream operation"); return; }
            if (bloklash || 부분배열여부) { if (!obyekt_VALUE(ma_lumotlar_ARRAY, 20)) return; if (bloklash) kiritish_COUNT = 힙[ma_lumotlar_ARRAY + 1]; if (시작변위 < 0 || kiritish_COUNT < 0 || 시작변위 > 힙[ma_lumotlar_ARRAY + 1] - kiritish_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else kiritish_COUNT = 1;
            if (kiritish_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[obyekt_Ma_lumotnomalar + 4] : 0, 처리값 = 0;
            while (완료수 < kiritish_COUNT) {
                처리값 = 읽기여부 ? foydalanuvchi.파일한바이트읽기(열린파일번호) : foydalanuvchi.파일한바이트쓰기(열린파일번호, bloklash || 부분배열여부 ? 힙[ma_lumotlar_ARRAY + 2 + 시작변위 + 완료수] : ma_lumotlar_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bloklash || 부분배열여부)) 힙[ma_lumotlar_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(bloklash || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[obyekt_Ma_lumotnomalar + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(obyekt_Ma_lumotnomalar, 2); if (bloklash || 부분배열여부) 넣기(ma_lumotlar_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(kiritish_COUNT, 1); } if (쓰기여부 && !(bloklash || 부분배열여부)) 넣기(ma_lumotlar_VALUE, 1); } return;
            }
            힙[obyekt_Ma_lumotnomalar + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : bloklash || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        to_xtab_qolish_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nom_konstanta) {
        if (Word_SMS(nom_konstanta, "한국어/자체/oyna")) return 24;
        if (Word_SMS(nom_konstanta, "한국어/자체/Yorliq")) return 26;
        if (Word_SMS(nom_konstanta, "한국어/자체/tugma")) return 27;
        if (Word_SMS(nom_konstanta, "한국어/자체/SMS_ma_lumotlar_maydoni")) return 28;
        if (Word_SMS(nom_konstanta, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nom_konstanta) {
        return 한국어화면종(nom_konstanta) != 0 || Word_SMS(nom_konstanta, "한국어/자체/화면구성요소") || Word_SMS(nom_konstanta, "한국어/자체/hodisa_navbat");
    }
    static int 화면종(int nom_konstanta) {
        int 한국어종 = 한국어화면종(nom_konstanta); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nom_konstanta, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nom_konstanta, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nom_konstanta, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nom_konstanta, "javax/swing/JButton")) return 27;
        if (Word_SMS(nom_konstanta, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nom_konstanta, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nom_konstanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nom_konstanta) {
        return 화면종(nom_konstanta) != 0 || Word_SMS(nom_konstanta, "java/awt/Component") || Word_SMS(nom_konstanta, "java/awt/Container") || Word_SMS(nom_konstanta, "javax/swing/JComponent") || Word_SMS(nom_konstanta, "javax/swing/AbstractButton") || Word_SMS(nom_konstanta, "javax/swing/text/JTextComponent") || Word_SMS(nom_konstanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int obyekt_Ma_lumotnomalar) { if (!객체유효(obyekt_Ma_lumotnomalar)) return false; if (힙[obyekt_Ma_lumotnomalar] < 24 || 힙[obyekt_Ma_lumotnomalar] > 28) { to_xtab_qolish_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int obyekt_Ma_lumotnomalar, int SMS_Ma_lumotnomalar) {
        if (SMS_Ma_lumotnomalar != 0 && !obyekt_VALUE(SMS_Ma_lumotnomalar, 1)) return;
        int kiritish_COUNT = SMS_Ma_lumotnomalar == 0 ? 0 : 힙[SMS_Ma_lumotnomalar + 1]; if (kiritish_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Ma_lumotnomalar + 2 + Loop_INDEX];
        if (foydalanuvchi.화면글(힙[obyekt_Ma_lumotnomalar + 2], 화면글임시, kiritish_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[obyekt_Ma_lumotnomalar + 3] = SMS_Ma_lumotnomalar; 힙참조[obyekt_Ma_lumotnomalar + 3] = 1;
    }
    static int 화면문자읽기(int obyekt_Ma_lumotnomalar) {
        int Guvohnoma_VALUE = 힙[obyekt_Ma_lumotnomalar + 2], kiritish_COUNT = foydalanuvchi.화면연결(8, Guvohnoma_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (kiritish_COUNT < 0) { to_xtab_qolish_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) { int 부호값 = foydalanuvchi.화면연결(9, Guvohnoma_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = joylashtirmoq_Xotira(1, 사용수); if (!Xato) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 o_zak_VALUE 화면 기능에 연결한다. Swing obyekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int egasi, int nom_konstanta, int 서술상수, int buyruq_kod) {
        if (Word_SMS(egasi, "한국어/자체/hodisa_navbat")) {
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int vazifa_harakat = 빼기(2); if (!객체유효(vazifa_harakat)) return;
                if (나중수 == 8) { to_xtab_qolish_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = vazifa_harakat; return;
            }
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            to_xtab_qolish_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(egasi, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!obyekt_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(nom_konstanta, "hodisa_manba") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(nom_konstanta, "buyruq_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(nom_konstanta, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else to_xtab_qolish_VALUE("지원하지 않는 한국어 Amal 알림 호출"); return;
        }
        if (buyruq_kod == 183 && Word_SMS(nom_konstanta, "<init>")) {
            int 종류 = 한국어화면종(egasi), 받이 = 0, 가로 = 0, Vertikal_holat = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (foydalanuvchi.화면너비() - 폭) / 2; Vertikal_holat = (foydalanuvchi.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertikal_holat = 빼기(1); 가로 = 빼기(1);
            } else { to_xtab_qolish_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int Matn = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertikal_holat < 0 || 폭 > foydalanuvchi.화면너비() - 가로 || 높이 > foydalanuvchi.화면높이() - Vertikal_holat) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = foydalanuvchi.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { to_xtab_qolish_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikal_holat; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            foydalanuvchi.화면연결(1, INDEX, 가로, Vertikal_holat, 폭, 높이);
            if (종류 == 24) foydalanuvchi.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Matn); return;
        }
        if (buyruq_kod != 182) { to_xtab_qolish_VALUE("잘못된 한국어 화면 호출 Buyruq"); return; }
        if (Word_SMS(nom_konstanta, "yozmoq_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Matn = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Matn); return;
        }
        if (Word_SMS(nom_konstanta, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(nom_konstanta, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(nom_konstanta, "qo_shmoq_element") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int farzand_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(farzand_VALUE) || !화면객체(부모)) return;
            if (foydalanuvchi.화면연결(2, 힙[부모 + 2], 힙[farzand_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[farzand_VALUE + 11] = 부모; 힙참조[farzand_VALUE + 11] = 1; return;
        }
        if (Word_SMS(nom_konstanta, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertikal_holat = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (foydalanuvchi.화면연결(1, 힙[element_VALUE + 2], 가로, Vertikal_holat, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikal_holat; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(nom_konstanta, "ko_rsatmoq_oyna") || Word_SMS(nom_konstanta, "Yopish")) && Word_SMS(서술상수, "()V")) {
            boolean ko_rinish_VALUE_83f79b03 = Word_SMS(nom_konstanta, "ko_rsatmoq_oyna"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (foydalanuvchi.화면연결(ko_rinish_VALUE_83f79b03 ? 3 : 4, 힙[element_VALUE + 2], ko_rinish_VALUE_83f79b03 ? 1 : 0, 0, 0, 0) < 0) { to_xtab_qolish_VALUE("화면은 o_zaro_faol 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = ko_rinish_VALUE_83f79b03 ? 1 : 0; return;
        }
        if (Word_SMS(nom_konstanta, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        to_xtab_qolish_VALUE("지원하지 않는 한국어 화면 uslub_VALUE");
    }
    static void 화면호출(int egasi, int nom_konstanta, int 서술상수, int buyruq_kod) {
        if (Word_SMS(egasi, "javax/swing/SwingUtilities")) {
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (!객체유효(obyekt_Ma_lumotnomalar)) return; if (나중수 == 8) { to_xtab_qolish_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = obyekt_Ma_lumotnomalar; return; }
            if (buyruq_kod == 184 && Word_SMS(nom_konstanta, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            to_xtab_qolish_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(egasi, "java/awt/event/ActionEvent")) {
            int obyekt_Ma_lumotnomalar = 빼기(2); if (!obyekt_VALUE(obyekt_Ma_lumotnomalar, 29)) return;
            if (Word_SMS(nom_konstanta, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[obyekt_Ma_lumotnomalar + 2], 2);
            else if (Word_SMS(nom_konstanta, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[obyekt_Ma_lumotnomalar + 2]), 2);
            else if (Word_SMS(nom_konstanta, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else to_xtab_qolish_VALUE("unsupported ActionEvent method"); return;
        }
        if (buyruq_kod == 183 && Word_SMS(nom_konstanta, "<init>")) {
            int COLUMNS = 0, SMS_Ma_lumotnomalar = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Ma_lumotnomalar = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Ma_lumotnomalar = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { to_xtab_qolish_VALUE("unsupported Swing constructor"); return; }
            int obyekt_Ma_lumotnomalar = 빼기(2); if (!객체유효(obyekt_Ma_lumotnomalar)) return;
            if (힙[obyekt_Ma_lumotnomalar] == 30) { to_xtab_qolish_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(obyekt_Ma_lumotnomalar) || COLUMNS < 0) return;
            int Guvohnoma_VALUE = foydalanuvchi.화면연결(0, 힙[obyekt_Ma_lumotnomalar] - 23, 0, 0, 0, 0);
            if (Guvohnoma_VALUE < 1 || Guvohnoma_VALUE > 32) { to_xtab_qolish_VALUE("GUI widget slots exhausted"); return; }
            힙[obyekt_Ma_lumotnomalar + 2] = Guvohnoma_VALUE; 화면참조[Guvohnoma_VALUE - 1] = obyekt_Ma_lumotnomalar; 힙[obyekt_Ma_lumotnomalar + 5] = 힙[obyekt_Ma_lumotnomalar] == 24 ? 130 : 16; 힙[obyekt_Ma_lumotnomalar + 6] = 힙[obyekt_Ma_lumotnomalar] == 24 ? 110 : 16;
            힙[obyekt_Ma_lumotnomalar + 7] = 힙[obyekt_Ma_lumotnomalar] == 24 ? 380 : 220; 힙[obyekt_Ma_lumotnomalar + 8] = 힙[obyekt_Ma_lumotnomalar] == 24 ? 240 : 28; 힙[obyekt_Ma_lumotnomalar + 10] = 1;
            화면문자설정(obyekt_Ma_lumotnomalar, SMS_Ma_lumotnomalar); return;
        }
        if (Word_SMS(nom_konstanta, "setText") || Word_SMS(nom_konstanta, "setTitle")) { int SMS_Ma_lumotnomalar = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(obyekt_Ma_lumotnomalar, SMS_Ma_lumotnomalar); return; }
        if (Word_SMS(nom_konstanta, "getText") || Word_SMS(nom_konstanta, "getTitle")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(obyekt_Ma_lumotnomalar), 2); return; }
        if (Word_SMS(nom_konstanta, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar)) { 힙[obyekt_Ma_lumotnomalar + 4] = 수신참조; 힙참조[obyekt_Ma_lumotnomalar + 4] = 1; } return; }
        if (Word_SMS(nom_konstanta, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar)) 넣기(obyekt_Ma_lumotnomalar, 2); return; }
        if (Word_SMS(nom_konstanta, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Maket_Ma_lumotnomalar = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar) && Maket_Ma_lumotnomalar != 0) to_xtab_qolish_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nom_konstanta, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Maket_holat = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Maket_holat) 빼기(2);
            int farzand_Ma_lumotnomalar = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (!화면객체(farzand_Ma_lumotnomalar) || !화면객체(obyekt_Ma_lumotnomalar)) return;
            if (foydalanuvchi.화면연결(2, 힙[obyekt_Ma_lumotnomalar + 2], 힙[farzand_Ma_lumotnomalar + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[farzand_Ma_lumotnomalar + 11] = obyekt_Ma_lumotnomalar; 힙참조[farzand_Ma_lumotnomalar + 11] = 1; if (!Maket_holat) 넣기(farzand_Ma_lumotnomalar, 2); return;
        }
        if (Word_SMS(nom_konstanta, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_tugmasi_koordinat = 빼기(1), x_koordinata = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (!화면객체(obyekt_Ma_lumotnomalar)) return;
            if (foydalanuvchi.화면연결(1, 힙[obyekt_Ma_lumotnomalar + 2], x_koordinata, Y_tugmasi_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[obyekt_Ma_lumotnomalar + 5] = x_koordinata; 힙[obyekt_Ma_lumotnomalar + 6] = Y_tugmasi_koordinat; 힙[obyekt_Ma_lumotnomalar + 7] = 너비; 힙[obyekt_Ma_lumotnomalar + 8] = 높이; return;
        }
        if (Word_SMS(nom_konstanta, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (!화면객체(obyekt_Ma_lumotnomalar)) return;
            if (foydalanuvchi.화면연결(1, 힙[obyekt_Ma_lumotnomalar + 2], 힙[obyekt_Ma_lumotnomalar + 5], 힙[obyekt_Ma_lumotnomalar + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[obyekt_Ma_lumotnomalar + 7] = 너비; 힙[obyekt_Ma_lumotnomalar + 8] = 높이; } return;
        }
        if (Word_SMS(nom_konstanta, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), obyekt_Ma_lumotnomalar = 빼기(2); if (!화면객체(obyekt_Ma_lumotnomalar)) return; if (상대배치 != 0) { to_xtab_qolish_VALUE("only screen centering supported"); return; } 힙[obyekt_Ma_lumotnomalar + 5] = (foydalanuvchi.화면너비() - 힙[obyekt_Ma_lumotnomalar + 7]) / 2; 힙[obyekt_Ma_lumotnomalar + 6] = (foydalanuvchi.화면높이() - 힙[obyekt_Ma_lumotnomalar + 8]) / 2; foydalanuvchi.화면연결(1, 힙[obyekt_Ma_lumotnomalar + 2], 힙[obyekt_Ma_lumotnomalar + 5], 힙[obyekt_Ma_lumotnomalar + 6], 힙[obyekt_Ma_lumotnomalar + 7], 힙[obyekt_Ma_lumotnomalar + 8]); return; }
        if (Word_SMS(nom_konstanta, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int siyosat = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar)) { if (siyosat < 0 || siyosat > 3) 예외던짐(9, "close policy"); else { 힙[obyekt_Ma_lumotnomalar + 10] = siyosat; foydalanuvchi.화면연결(7, 힙[obyekt_Ma_lumotnomalar + 2], siyosat, 0, 0, 0); } } return; }
        if (Word_SMS(nom_konstanta, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int ma_lumotlar_VALUE = 빼기(1), obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar)) { int 처리값 = foydalanuvchi.화면연결(3, 힙[obyekt_Ma_lumotnomalar + 2], ma_lumotlar_VALUE, 0, 0, 0); if (처리값 < 0) to_xtab_qolish_VALUE("Swing requires a standalone interactive command"); else 힙[obyekt_Ma_lumotnomalar + 9] = ma_lumotlar_VALUE; } return; }
        if (Word_SMS(nom_konstanta, "dispose") && Word_SMS(서술상수, "()V")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar)) { foydalanuvchi.화면연결(4, 힙[obyekt_Ma_lumotnomalar + 2], 0, 0, 0, 0); 힙[obyekt_Ma_lumotnomalar + 9] = 0; } return; }
        if (Word_SMS(nom_konstanta, "repaint") || Word_SMS(nom_konstanta, "validate")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (!화면객체(obyekt_Ma_lumotnomalar) || !Word_SMS(서술상수, "()V")) return; foydalanuvchi.화면연결(1, 힙[obyekt_Ma_lumotnomalar + 2], 힙[obyekt_Ma_lumotnomalar + 5], 힙[obyekt_Ma_lumotnomalar + 6], 힙[obyekt_Ma_lumotnomalar + 7], 힙[obyekt_Ma_lumotnomalar + 8]); return; }
        if (Word_SMS(nom_konstanta, "isVisible") && Word_SMS(서술상수, "()Z")) { int obyekt_Ma_lumotnomalar = 빼기(2); if (화면객체(obyekt_Ma_lumotnomalar)) 넣기(힙[obyekt_Ma_lumotnomalar + 9], 1); return; }
        to_xtab_qolish_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int maqsad_manzil, int 사건번호, boolean 한국어) {
        if (maqsad_manzil < 1 || 힙[maqsad_manzil] < 32) { to_xtab_qolish_VALUE("Java event listener required"); return; }
        int fayl_INDEX = nom_uslub(힙[maqsad_manzil] - 32, 사건번호 == 0 ? (한국어 ? "Ishga_tushirish" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fayl_INDEX < 0) { to_xtab_qolish_VALUE("event callback missing"); return; }
        현재가닥 = 0; oqim_COUNT = 1; kadr_INDEX = 0; oqim_holat[0] = 1; kadr_Stack[0] = 0; 틀잠금[0] = ishga_tushirmoq_kadr[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { mahalliy_VALUE[Loop_INDEX] = mahalliy_TYPE[Loop_INDEX] = 0; }
        kadr_uslub[0] = fayl_INDEX; kadr_holat[0] = uslub_Start[fayl_INDEX]; mahalliy_VALUE[0] = maqsad_manzil; mahalliy_TYPE[0] = 2;
        if (사건번호 != 0) { mahalliy_VALUE[1] = 사건번호; mahalliy_TYPE[1] = 2; }
        사건중 = true; bajarmoq_buyruq(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Xato) {
            if (나중수 > 0) { int maqsad_manzil = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(maqsad_manzil, 0, 한국어 != 0); continue; }
            if (foydalanuvchi.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = foydalanuvchi.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { to_xtab_qolish_VALUE("GUI event I/O failed"); return; }
            int Guvohnoma_VALUE = 사건번호 & 65535; if (Guvohnoma_VALUE < 1 || Guvohnoma_VALUE > 32) continue; int obyekt_Ma_lumotnomalar = 화면참조[Guvohnoma_VALUE - 1]; if (obyekt_Ma_lumotnomalar == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[obyekt_Ma_lumotnomalar + 10] != 0) 힙[obyekt_Ma_lumotnomalar + 9] = 0;
                if (힙[obyekt_Ma_lumotnomalar + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) foydalanuvchi.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[obyekt_Ma_lumotnomalar + 4] != 0) {
                int ma_lumot_fayli_Ma_lumotnomalar = joylashtirmoq_Xotira(29, 2); if (Xato) return; 힙[ma_lumot_fayli_Ma_lumotnomalar + 2] = obyekt_Ma_lumotnomalar; 힙[ma_lumot_fayli_Ma_lumotnomalar + 3] = 힙[obyekt_Ma_lumotnomalar + 12]; 힙참조[ma_lumot_fayli_Ma_lumotnomalar + 2] = 1; 사건실행(힙[obyekt_Ma_lumotnomalar + 4], ma_lumot_fayli_Ma_lumotnomalar, 힙[obyekt_Ma_lumotnomalar + 12] != 0);
            }
        }
    }
    public static int Bajarish() {
        if (foydalanuvchi.인수개수() == 1 && 자바도구.같음(foydalanuvchi.인수(0), "-version")) {
            foydalanuvchi.Yozish("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (foydalanuvchi.인수개수() < 1) { foydalanuvchi.Yozish("Usage: java CLASS [ARGS]\n"); return 2; }
        kiritish_Sinf_Izoh = yuklamoq_Sinf_Izoh(tashkilotchi_belgi(foydalanuvchi.인수(0))); if (Xato || kiritish_Sinf_Izoh < 0) return 1;
        int kiritish_nuqta_VALUE = nom_uslub(kiritish_Sinf_Izoh, "Bajarish", "()V");
        boolean 한국어진입 = kiritish_nuqta_VALUE >= 0 && (uslub_kirish_huquqi[kiritish_nuqta_VALUE] & 9) == 9;
        if (!한국어진입) kiritish_nuqta_VALUE = nom_uslub(kiritish_Sinf_Izoh, "main", "([Ljava/lang/String;)V");
        if (kiritish_nuqta_VALUE < 0 || (uslub_kirish_huquqi[kiritish_nuqta_VALUE] & 9) != 9) to_xtab_qolish_VALUE("public static void Bajarish() or main(String[] args) required");
        if (Xato) return 1;
        int 인수 = joylashtirmoq_Xotira(3, foydalanuvchi.인수개수() - 1); ARRAY_element[인수] = -1;
        for (int 수 = 1; 수 < foydalanuvchi.인수개수() && !Xato; 수++) 힙[인수 + 1 + 수] = tashkilotchi_belgi(foydalanuvchi.인수(수));
        kadr_INDEX = 0; kadr_uslub[0] = kiritish_nuqta_VALUE; kadr_holat[0] = uslub_Start[kiritish_nuqta_VALUE]; mahalliy_VALUE[0] = 한국어진입 ? 0 : 인수; mahalliy_TYPE[0] = 한국어진입 ? 0 : 2;
        oqim_holat[0] = 1; oqim_obyekt[0] = joylashtirmoq_Xotira(13, 2);
        bajarmoq_buyruq(); if (!Xato) 화면사건들(); return Xato ? 1 : 0;
    }
}
