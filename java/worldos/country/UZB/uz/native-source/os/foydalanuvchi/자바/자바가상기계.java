// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fayl/스택/Ma_lumotnomalar/shox 경계를 bajarmoq_buyruq 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fayl = new int[16384], fayl_nom_SMS = new int[64];
    static int[] konstanta_teg = new int[512], 상가 = new int[512], konstanta_SECOND_VALUE = new int[512], satr_Ma_lumotnomalar = new int[512];
    static int[] uslub_nom_SMS = new int[32], uslub_TYPE = new int[32], uslub_kirish_huquqi = new int[32];
    static int[] uslub_Start = new int[32], uslub_to_xtatmoq = new int[32], uslub_Stack = new int[32], 함수지역 = new int[32];
    static int[] uslub_dalil_COUNT = new int[32], uslub_dalil_TYPE = new int[512], uslub_qaytarish = new int[32];
    static int[] 경계 = new int[16384];
    static int[] mahalliy_VALUE = new int[4096], mahalliy_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] kadr_uslub = new int[32], kadr_holat = new int[32], kadr_Stack = new int[32];
    static int[] 힙 = new int[8192];
    static int Hajmi, 읽기위치, konstanta_COUNT, uslub_COUNT, Sinf_nom, kadr_INDEX = -1, 힙끝 = 1, qaytarish_TYPE;
    static boolean Xato;

    static void to_xtab_qolish_VALUE(String Word_SMS) {
        if (!Xato) { foydalanuvchi.Yozish("JVM error: "); foydalanuvchi.Yozish(Word_SMS); foydalanuvchi.yozmoq_belgi_VALUE(10); }
        Xato = true;
    }
    static boolean klip(int Bajarish, int uzunlik_VALUE) { return Bajarish >= 0 && uzunlik_VALUE >= 0 && Bajarish <= Hajmi - uzunlik_VALUE; }
    static int bayt_VALUE() {
        if (!klip(읽기위치, 1)) { to_xtab_qolish_VALUE("truncated class file"); return 0; }
        return Fayl[읽기위치++];
    }
    static int 짧은수() { return bayt_VALUE() << 8 | bayt_VALUE(); }
    static int butun_son() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int uzunlik_VALUE) { if (!klip(읽기위치, uzunlik_VALUE)) to_xtab_qolish_VALUE("invalid attribute size"); else 읽기위치 += uzunlik_VALUE; }
    static boolean chek_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_COUNT || konstanta_teg[수] != 종류) { to_xtab_qolish_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Bajarish, int uzunlik_VALUE, String Word_SMS) {
        if (!klip(Bajarish, uzunlik_VALUE) || uzunlik_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < uzunlik_VALUE; 수++) if (Fayl[Bajarish + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !Xato; 수++) { chek_konstanta(짧은수(), 1); 건너(butun_son()); }
    }
    static int buyruq_uzunlik(int VALUE) {
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
        if (butun_son() != 0xcafebabe) to_xtab_qolish_VALUE("not a class file");
        int 부판 = 짧은수(), versiya_VALUE = 짧은수();
        if (versiya_VALUE < 45 || versiya_VALUE > 52 || 부판 != 0) to_xtab_qolish_VALUE("supported class versions: 45..52, minor 0");
        konstanta_COUNT = 짧은수();
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { to_xtab_qolish_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstanta_COUNT && !Xato; 수++) {
            int 종류 = bayt_VALUE(); konstanta_teg[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = butun_son();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstanta_SECOND_VALUE[수] = 짧은수(); }
            else to_xtab_qolish_VALUE("unsupported constant type");
        }
        int ruxsat_VALUE_a9fa0dfa = 짧은수();
        if ((ruxsat_VALUE_a9fa0dfa & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) to_xtab_qolish_VALUE("unsupported class flags");
        Sinf_nom = Sinf_nom_SMS(짧은수());
        if (!Word_SMS(Sinf_nom_SMS(짧은수()), "java/lang/Object")) to_xtab_qolish_VALUE("inheritance unsupported");
        if (짧은수() != 0) to_xtab_qolish_VALUE("interfaces unsupported");
        if (짧은수() != 0) to_xtab_qolish_VALUE("fields unsupported");
        uslub_COUNT = 짧은수();
        if (uslub_COUNT < 1 || uslub_COUNT > 32) { to_xtab_qolish_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < uslub_COUNT && !Xato; 수++) {
            uslub_kirish_huquqi[수] = 짧은수(); uslub_nom_SMS[수] = 짧은수(); uslub_TYPE[수] = 짧은수();
            chek_konstanta(uslub_nom_SMS[수], 1); 서술읽기(수);
            if ((uslub_kirish_huquqi[수] & (0x100 | 0x400 | 0x20)) != 0) to_xtab_qolish_VALUE("native, abstract and synchronized methods unsupported");
            if ((uslub_kirish_huquqi[수] & 8) == 0 && !Word_SMS(uslub_nom_SMS[수], "<init>")) to_xtab_qolish_VALUE("instance methods unsupported");
            if (Word_SMS(uslub_nom_SMS[수], "<clinit>")) to_xtab_qolish_VALUE("class initializers unsupported");
            for (int old_kamera_VALUE = 0; old_kamera_VALUE < 수; old_kamera_VALUE++) if (같은말(uslub_nom_SMS[old_kamera_VALUE], uslub_nom_SMS[수]) && 같은말(uslub_TYPE[old_kamera_VALUE], uslub_TYPE[수])) to_xtab_qolish_VALUE("duplicate method");
            int element_COUNT = 짧은수();
            for (int xususiyat_VALUE = 0; xususiyat_VALUE < element_COUNT && !Xato; xususiyat_VALUE++) {
                int Nomi = 짧은수(), uzunlik_VALUE = butun_son(), Bajarish = 읽기위치;
                if (!klip(Bajarish, uzunlik_VALUE)) { to_xtab_qolish_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nomi, "Code")) {
                    if (uslub_Start[수] != 0) to_xtab_qolish_VALUE("duplicate Code attribute");
                    uslub_Stack[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_uzunlik = butun_son();
                    if (uslub_Stack[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < uslub_dalil_COUNT[수]
                        || kod_uzunlik < 1 || kod_uzunlik > 8192) to_xtab_qolish_VALUE("method memory limits exceeded");
                    uslub_Start[수] = 읽기위치; 건너(kod_uzunlik); uslub_to_xtatmoq[수] = 읽기위치;
                    if (짧은수() != 0) to_xtab_qolish_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Bajarish + uzunlik_VALUE) to_xtab_qolish_VALUE("Code attribute size mismatch");
                } else 건너(uzunlik_VALUE);
            }
            if (uslub_Start[수] == 0) to_xtab_qolish_VALUE("missing Code attribute");
            int in_kiritish = uslub_Start[수];
            while (in_kiritish < uslub_to_xtatmoq[수] && !Xato) {
                int uzunlik_VALUE = buyruq_uzunlik(Fayl[in_kiritish]);
                if (uzunlik_VALUE == 0 || uzunlik_VALUE > uslub_to_xtatmoq[수] - in_kiritish) { to_xtab_qolish_VALUE("unsupported or truncated bytecode"); break; }
                경계[in_kiritish] = 수 + 1; in_kiritish += uzunlik_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 shox 목적지를 허용하지 않는다.
            in_kiritish = uslub_Start[수];
            while (in_kiritish < uslub_to_xtatmoq[수] && !Xato) {
                int VALUE = Fayl[in_kiritish];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int ko_chirish_joyi_VALUE = in_kiritish + (short)(Fayl[in_kiritish + 1] << 8 | Fayl[in_kiritish + 2]);
                    if (ko_chirish_joyi_VALUE < uslub_Start[수] || ko_chirish_joyi_VALUE >= uslub_to_xtatmoq[수] || 경계[ko_chirish_joyi_VALUE] != 수 + 1) to_xtab_qolish_VALUE("invalid branch target");
                }
                in_kiritish += buyruq_uzunlik(VALUE);
            }
        }
        if (!Xato) 속성건너();
        if (읽기위치 != Hajmi) to_xtab_qolish_VALUE("extra class file data");
    }
    static int joylashtirmoq_Xotira(int 종류, int uzunlik_VALUE) {
        if (uzunlik_VALUE < 0 || uzunlik_VALUE > 힙.length - 힙끝 - 2) { to_xtab_qolish_VALUE("object heap exhausted or negative array size"); return 0; }
        int Ma_lumotnomalar = 힙끝; 힙끝 += uzunlik_VALUE + 2; 힙[Ma_lumotnomalar] = 종류; 힙[Ma_lumotnomalar + 1] = uzunlik_VALUE;
        return Ma_lumotnomalar;
    }
    static boolean obyekt_VALUE(int Ma_lumotnomalar, int 종류) {
        if (Ma_lumotnomalar < 1 || Ma_lumotnomalar >= 힙끝 - 1 || 힙[Ma_lumotnomalar] != 종류) { to_xtab_qolish_VALUE("null or invalid object reference"); return false; }
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
        if (kadr_INDEX == 31) { to_xtab_qolish_VALUE("call stack limit (32)"); return; }
        int Keyingi_element = kadr_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) mahalliy_TYPE[Keyingi_element * 128 + 수] = 0;
        for (int 수 = uslub_dalil_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            mahalliy_VALUE[Keyingi_element * 128 + 수] = 빼기(uslub_dalil_TYPE[FUNCTION_VALUE * 16 + 수]); mahalliy_TYPE[Keyingi_element * 128 + 수] = uslub_dalil_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        kadr_INDEX = Keyingi_element; kadr_uslub[kadr_INDEX] = FUNCTION_VALUE; kadr_holat[kadr_INDEX] = uslub_Start[FUNCTION_VALUE]; kadr_Stack[kadr_INDEX] = 0;
    }
    static void qaytarish_o_lchov(int TYPE_VALUE) {
        if (TYPE_VALUE != uslub_qaytarish[kadr_uslub[kadr_INDEX]]) { to_xtab_qolish_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        kadr_INDEX--; if (kadr_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { to_xtab_qolish_VALUE("file stream paths currently require ASCII"); return; }
                oqim_fayl_nom[in_kiritish] = VALUE;
            }
            oqim_fayl_nom[uzunlik_VALUE] = 0;
            int 서술자 = foydalanuvchi.파일서술자열기(oqim_fayl_nom, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { to_xtab_qolish_VALUE("FileNotFoundException: file open failed"); return; }
            힙[oqim_VALUE + 2] = 서술자; 힙[oqim_VALUE + 3] = 1;
            return;
        }
        if (Buyruq != 182) { to_xtab_qolish_VALUE("invalid file stream invocation"); return; }
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
            if (o_lchov < -1) to_xtab_qolish_VALUE("IOException: read failed"); else 넣기(o_lchov, 1);
        } else if (foydalanuvchi.파일한바이트쓰기(서술자, VALUE) != 1) to_xtab_qolish_VALUE("IOException: write failed");
    }
    static void CALL_uslub(int INDEX, int Buyruq) {
        if (!chek_konstanta(INDEX, 10)) return;
        int egasi_VALUE = Sinf_nom_SMS(상가[INDEX]), Nomi = Ma_lumotnomalar_nom(konstanta_SECOND_VALUE[INDEX]), format_VALUE = Ma_lumotnomalar_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (Xato) return;
        if (같은말(egasi_VALUE, Sinf_nom)) {
            if (Buyruq != 184) { to_xtab_qolish_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < uslub_COUNT; 수++) if (같은말(Nomi, uslub_nom_SMS[수]) && 같은말(format_VALUE, uslub_TYPE[수])) {
                if ((uslub_kirish_huquqi[수] & 8) == 0) to_xtab_qolish_VALUE("method is not static"); else 호출(수);
                return;
            }
            to_xtab_qolish_VALUE("NoSuchMethodError"); return;
        }
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
        to_xtab_qolish_VALUE("unsupported library method");
    }
    static int ARRAY_in(int Ma_lumotnomalar, int satr_osti_VALUE, int TYPE_VALUE) {
        if (!obyekt_VALUE(Ma_lumotnomalar, TYPE_VALUE)) return 0;
        if (satr_osti_VALUE < 0 || satr_osti_VALUE >= 힙[Ma_lumotnomalar + 1]) { to_xtab_qolish_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Ma_lumotnomalar + 2 + satr_osti_VALUE;
    }
    static void bajarmoq_buyruq() {
        int 남음 = 500000;
        while (kadr_INDEX >= 0 && !Xato) {
            if (--남음 == 0) { to_xtab_qolish_VALUE("instruction limit (500000)"); break; }
            int Bajarish = kadr_holat[kadr_INDEX], VALUE = 명바();
            if (Xato) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstanta_COUNT) to_xtab_qolish_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int satr_osti_VALUE = 빼기(1), Ma_lumotnomalar = 빼기(2), in_kiritish = ARRAY_in(Ma_lumotnomalar, satr_osti_VALUE, VALUE == 46 ? 2 : 3);
                if (!Xato) 넣기(힙[in_kiritish], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int element_element = 빼기(VALUE == 79 ? 1 : 2), satr_osti_VALUE = 빼기(1), Ma_lumotnomalar = 빼기(2), in_kiritish = ARRAY_in(Ma_lumotnomalar, satr_osti_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && element_element != 0) obyekt_VALUE(element_element, 1);
                if (!Xato) 힙[in_kiritish] = element_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = qaytarish_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = qaytarish_TYPE, 나 = 빼기(0), 나형 = qaytarish_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!chek_konstanta(수, 9)) continue;
                if (!Word_SMS(Sinf_nom_SMS(상가[수]), "java/lang/System") || !Word_SMS(Ma_lumotnomalar_nom(konstanta_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Ma_lumotnomalar_TYPE(konstanta_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) to_xtab_qolish_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_uslub(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Nomi = Sinf_nom_SMS(명짧());
                if (Word_SMS(Nomi, "java/lang/StringBuilder")) 넣기(joylashtirmoq_Xotira(4, 1), 2);
                else if (Word_SMS(Nomi, "java/io/FileInputStream") || Word_SMS(Nomi, "java/io/FileOutputStream")) {
                    int Ma_lumotnomalar = joylashtirmoq_Xotira(Word_SMS(Nomi, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Xato) { 힙[Ma_lumotnomalar + 2] = -1; 넣기(Ma_lumotnomalar, 2); }
                } else to_xtab_qolish_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) to_xtab_qolish_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(Sinf_nom_SMS(명짧()), "java/lang/String")) to_xtab_qolish_VALUE("only String[] anewarray is supported");
                int uzunlik_VALUE = 빼기(1); 넣기(joylashtirmoq_Xotira(VALUE == 188 ? 2 : 3, uzunlik_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Ma_lumotnomalar = 빼기(2);
                if (Ma_lumotnomalar < 1 || Ma_lumotnomalar >= 힙끝 - 1 || (힙[Ma_lumotnomalar] != 2 && 힙[Ma_lumotnomalar] != 3)) to_xtab_qolish_VALUE("null or invalid array");
                else 넣기(힙[Ma_lumotnomalar + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Nomi = Sinf_nom_SMS(명짧()), Ma_lumotnomalar = 빼기(2);
                if (!Word_SMS(Nomi, "java/lang/String")) to_xtab_qolish_VALUE("unsupported checkcast");
                else if (Ma_lumotnomalar != 0) obyekt_VALUE(Ma_lumotnomalar, 1);
                넣기(Ma_lumotnomalar, 2); continue;
            }
            to_xtab_qolish_VALUE("unsupported bytecode");
        }
    }
    public static int Bajarish() {
        if (foydalanuvchi.인수개수() == 1 && 자바도구.같음(foydalanuvchi.인수(0), "-version")) {
            foydalanuvchi.Yozish("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (foydalanuvchi.인수개수() < 1) { foydalanuvchi.Yozish("Usage: java CLASS [ARGS]\n"); return 2; }
        int uzunlik_VALUE = 자바도구.Nomi(fayl_nom_SMS, foydalanuvchi.인수(0));
        if (uzunlik_VALUE < 1 || uzunlik_VALUE > 57) { foydalanuvchi.Yozish("java: invalid class name\n"); return 2; }
        fayl_nom_SMS[uzunlik_VALUE] = '.'; fayl_nom_SMS[uzunlik_VALUE + 1] = 'c'; fayl_nom_SMS[uzunlik_VALUE + 2] = 'l'; fayl_nom_SMS[uzunlik_VALUE + 3] = 'a'; fayl_nom_SMS[uzunlik_VALUE + 4] = 's'; fayl_nom_SMS[uzunlik_VALUE + 5] = 's';
        Hajmi = foydalanuvchi.파일읽기(fayl_nom_SMS, Fayl);
        if (Hajmi < 0) { foydalanuvchi.Yozish("java: cannot read class: "); 자바도구.수쓰기(Hajmi); foydalanuvchi.yozmoq_belgi_VALUE(10); return 1; }
        클래스읽기(); if (Xato) return 1;
        int belgi_nom = konstanta_SMS(Sinf_nom);
        if (!Xato && 힙[belgi_nom + 1] != uzunlik_VALUE) to_xtab_qolish_VALUE("class name does not match file");
        for (int 수 = 0; 수 < uzunlik_VALUE && !Xato; 수++) if (힙[belgi_nom + 2 + 수] != fayl_nom_SMS[수]) to_xtab_qolish_VALUE("class name does not match file");
        int kiritish_nuqta_VALUE = -1;
        for (int 수 = 0; 수 < uslub_COUNT; 수++) if (Word_SMS(uslub_nom_SMS[수], "main") && Word_SMS(uslub_TYPE[수], "([Ljava/lang/String;)V") && (uslub_kirish_huquqi[수] & 9) == 9) kiritish_nuqta_VALUE = 수;
        if (kiritish_nuqta_VALUE < 0) to_xtab_qolish_VALUE("public static void main(String[] args) required");
        if (Xato) return 1;
        int 인수 = joylashtirmoq_Xotira(3, foydalanuvchi.인수개수() - 1);
        for (int 수 = 1; 수 < foydalanuvchi.인수개수() && !Xato; 수++) 힙[인수 + 1 + 수] = tashkilotchi_belgi(foydalanuvchi.인수(수));
        kadr_INDEX = 0; kadr_uslub[0] = kiritish_nuqta_VALUE; kadr_holat[0] = uslub_Start[kiritish_nuqta_VALUE]; mahalliy_VALUE[0] = 인수; mahalliy_TYPE[0] = 2;
        bajarmoq_buyruq(); return Xato ? 1 : 0;
    }
}
