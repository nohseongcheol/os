// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. fajl/스택/Referenza/fergħa 경계를 eżegwixxa_kmand 중 검사한다. */
public final class 자바가상기계 {
    static int[] fajl = new int[16384], fajl_isem_SMS = new int[64];
    static int[] valur_fiss_tag = new int[512], 상가 = new int[512], valur_fiss_SECOND_VALUE = new int[512], string_Referenza = new int[512];
    static int[] metodu_isem_SMS = new int[32], metodu_TYPE = new int[32], metodu_aċċess = new int[32];
    static int[] metodu_Bidu = new int[32], metodu_ttermina = new int[32], metodu_Munzell = new int[32], 함수지역 = new int[32];
    static int[] metodu_argument_COUNT = new int[32], metodu_argument_TYPE = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokali_VALUE = new int[4096], lokali_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] frejm_metodu = new int[32], frejm_pożizzjoni = new int[32], frejm_Munzell = new int[32];
    static int[] 힙 = new int[8192];
    static int daqqas, 읽기위치, valur_fiss_COUNT, metodu_COUNT, klassi_isem, frejm_INDEX = -1, 힙끝 = 1, 반환형;
    static boolean żball;

    static void żball_VALUE(String Word_SMS) {
        if (!żball) { utent.kiteb("JVM error: "); utent.kiteb(Word_SMS); utent.kiteb_karattru_VALUE(10); }
        żball = true;
    }
    static boolean klipp(int serje, int tul_VALUE) { return serje >= 0 && tul_VALUE >= 0 && serje <= daqqas - tul_VALUE; }
    static int byte_VALUE() {
        if (!klipp(읽기위치, 1)) { żball_VALUE("truncated class file"); return 0; }
        return fajl[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int numru_sħiħ() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int tul_VALUE) { if (!klipp(읽기위치, tul_VALUE)) żball_VALUE("invalid attribute size"); else 읽기위치 += tul_VALUE; }
    static boolean ċekk_valur_fiss(int 수, int 종류) {
        if (수 <= 0 || 수 >= valur_fiss_COUNT || valur_fiss_tag[수] != 종류) { żball_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int serje, int tul_VALUE, String Word_SMS) {
        if (!klipp(serje, tul_VALUE) || tul_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < tul_VALUE; 수++) if (fajl[serje + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int valur_fiss_VALUE, String Word_SMS) { return ċekk_valur_fiss(valur_fiss_VALUE, 1) && 구간(상가[valur_fiss_VALUE], valur_fiss_SECOND_VALUE[valur_fiss_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!ċekk_valur_fiss(가, 1) || !ċekk_valur_fiss(나, 1) || valur_fiss_SECOND_VALUE[가] != valur_fiss_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < valur_fiss_SECOND_VALUE[가]; 수++) if (fajl[상가[가] + 수] != fajl[상가[나] + 수]) return false;
        return true;
    }
    static int klassi_isem_SMS(int 수) { return ċekk_valur_fiss(수, 7) && ċekk_valur_fiss(상가[수], 1) ? 상가[수] : 0; }
    static int Referenza_isem(int 수) { return ċekk_valur_fiss(수, 12) && ċekk_valur_fiss(상가[수], 1) ? 상가[수] : 0; }
    static int Referenza_TYPE(int 수) { return ċekk_valur_fiss(수, 12) && ċekk_valur_fiss(valur_fiss_SECOND_VALUE[수], 1) ? valur_fiss_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean vojt_TYPE) {
        if (읽기위치 >= 끝) { żball_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && vojt_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int serje = 읽기위치;
            while (읽기위치 < 끝 && fajl[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == serje) żball_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        żball_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metodu_TYPE[FUNCTION_VALUE];
        if (!ċekk_valur_fiss(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + valur_fiss_SECOND_VALUE[수];
        if (byte_VALUE() != '(') żball_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!żball && 읽기위치 < 끝 && fajl[읽기위치] != ')') {
            if (element_COUNT == 16) { żball_VALUE("too many method arguments"); break; }
            metodu_argument_TYPE[FUNCTION_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') żball_VALUE("invalid method descriptor");
        함수반환[FUNCTION_VALUE] = 서술형(끝, true); metodu_argument_COUNT[FUNCTION_VALUE] = element_COUNT;
        if (읽기위치 != 끝) żball_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !żball; 수++) { ċekk_valur_fiss(짧은수(), 1); 건너(numru_sħiħ()); }
    }
    static int kmand_tul(int VALUE) {
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
        if (numru_sħiħ() != 0xcafebabe) żball_VALUE("not a class file");
        int 부판 = 짧은수(), verżjoni_VALUE = 짧은수();
        if (verżjoni_VALUE < 45 || verżjoni_VALUE > 52 || 부판 != 0) żball_VALUE("supported class versions: 45..52, minor 0");
        valur_fiss_COUNT = 짧은수();
        if (valur_fiss_COUNT < 1 || valur_fiss_COUNT > 512) { żball_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < valur_fiss_COUNT && !żball; 수++) {
            int 종류 = byte_VALUE(); valur_fiss_tag[수] = 종류;
            if (종류 == 1) { valur_fiss_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(valur_fiss_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = numru_sħiħ();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); valur_fiss_SECOND_VALUE[수] = 짧은수(); }
            else żball_VALUE("unsupported constant type");
        }
        int permess_VALUE = 짧은수();
        if ((permess_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) żball_VALUE("unsupported class flags");
        klassi_isem = klassi_isem_SMS(짧은수());
        if (!Word_SMS(klassi_isem_SMS(짧은수()), "java/lang/Object")) żball_VALUE("inheritance unsupported");
        if (짧은수() != 0) żball_VALUE("interfaces unsupported");
        if (짧은수() != 0) żball_VALUE("fields unsupported");
        metodu_COUNT = 짧은수();
        if (metodu_COUNT < 1 || metodu_COUNT > 32) { żball_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metodu_COUNT && !żball; 수++) {
            metodu_aċċess[수] = 짧은수(); metodu_isem_SMS[수] = 짧은수(); metodu_TYPE[수] = 짧은수();
            ċekk_valur_fiss(metodu_isem_SMS[수], 1); 서술읽기(수);
            if ((metodu_aċċess[수] & (0x100 | 0x400 | 0x20)) != 0) żball_VALUE("native, abstract and synchronized methods unsupported");
            if ((metodu_aċċess[수] & 8) == 0 && !Word_SMS(metodu_isem_SMS[수], "<init>")) żball_VALUE("instance methods unsupported");
            if (Word_SMS(metodu_isem_SMS[수], "<clinit>")) żball_VALUE("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(metodu_isem_SMS[앞], metodu_isem_SMS[수]) && 같은말(metodu_TYPE[앞], metodu_TYPE[수])) żball_VALUE("duplicate method");
            int element_COUNT = 짧은수();
            for (int attribut_VALUE = 0; attribut_VALUE < element_COUNT && !żball; attribut_VALUE++) {
                int isem = 짧은수(), tul_VALUE = numru_sħiħ(), serje = 읽기위치;
                if (!klipp(serje, tul_VALUE)) { żball_VALUE("truncated method attribute"); break; }
                if (Word_SMS(isem, "Code")) {
                    if (metodu_Bidu[수] != 0) żball_VALUE("duplicate Code attribute");
                    metodu_Munzell[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_tul = numru_sħiħ();
                    if (metodu_Munzell[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metodu_argument_COUNT[수]
                        || CODE_tul < 1 || CODE_tul > 8192) żball_VALUE("method memory limits exceeded");
                    metodu_Bidu[수] = 읽기위치; 건너(CODE_tul); metodu_ttermina[수] = 읽기위치;
                    if (짧은수() != 0) żball_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != serje + tul_VALUE) żball_VALUE("Code attribute size mismatch");
                } else 건너(tul_VALUE);
            }
            if (metodu_Bidu[수] == 0) żball_VALUE("missing Code attribute");
            int slott_entrata = metodu_Bidu[수];
            while (slott_entrata < metodu_ttermina[수] && !żball) {
                int tul_VALUE = kmand_tul(fajl[slott_entrata]);
                if (tul_VALUE == 0 || tul_VALUE > metodu_ttermina[수] - slott_entrata) { żball_VALUE("unsupported or truncated bytecode"); break; }
                경계[slott_entrata] = 수 + 1; slott_entrata += tul_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 fergħa 목적지를 허용하지 않는다.
            slott_entrata = metodu_Bidu[수];
            while (slott_entrata < metodu_ttermina[수] && !żball) {
                int VALUE = fajl[slott_entrata];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int destinazzjoni_VALUE = slott_entrata + (short)(fajl[slott_entrata + 1] << 8 | fajl[slott_entrata + 2]);
                    if (destinazzjoni_VALUE < metodu_Bidu[수] || destinazzjoni_VALUE >= metodu_ttermina[수] || 경계[destinazzjoni_VALUE] != 수 + 1) żball_VALUE("invalid branch target");
                }
                slott_entrata += kmand_tul(VALUE);
            }
        }
        if (!żball) 속성건너();
        if (읽기위치 != daqqas) żball_VALUE("extra class file data");
    }
    static int alloka_Ħażna(int 종류, int tul_VALUE) {
        if (tul_VALUE < 0 || tul_VALUE > 힙.length - 힙끝 - 2) { żball_VALUE("object heap exhausted or negative array size"); return 0; }
        int Referenza = 힙끝; 힙끝 += tul_VALUE + 2; 힙[Referenza] = 종류; 힙[Referenza + 1] = tul_VALUE;
        return Referenza;
    }
    static boolean oġġett_VALUE(int Referenza, int 종류) {
        if (Referenza < 1 || Referenza >= 힙끝 - 1 || 힙[Referenza] != 종류) { żball_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int valur_fiss_SMS(int INDEX) {
        if (!ċekk_valur_fiss(INDEX, 1)) return 0;
        if (string_Referenza[INDEX] != 0) return string_Referenza[INDEX];
        int Referenza = alloka_Ħażna(1, valur_fiss_SECOND_VALUE[INDEX]); if (żball) return 0;
        int 끝 = 상가[INDEX] + valur_fiss_SECOND_VALUE[INDEX], 수 = 상가[INDEX], tul_VALUE = 0;
        while (수 < 끝 && !żball) {
            int VALUE = fajl[수++];
            if (VALUE == 0) żball_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Li_Jmiss_element = fajl[수++];
                if ((Li_Jmiss_element & 192) != 128) żball_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Li_Jmiss_element & 63;
                if (VALUE != 0 && VALUE < 128) żball_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = fajl[수++], 나 = fajl[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) żball_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) żball_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) żball_VALUE("invalid modified UTF-8");
            힙[Referenza + 2 + tul_VALUE++] = VALUE;
        }
        힙[Referenza + 1] = tul_VALUE; string_Referenza[INDEX] = Referenza; return Referenza;
    }
    static int host_karattru(String VALUE) {
        int Referenza = alloka_Ħażna(1, VALUE.length()); if (żball) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Referenza + 2 + 수] = VALUE.charAt(수);
        return Referenza;
    }
    static void kiteb_SMS(int Referenza) {
        if (Referenza == 0) { utent.kiteb("null"); return; }
        if (!oġġett_VALUE(Referenza, 1)) return;
        for (int 수 = 0; 수 < 힙[Referenza + 1]; 수++) utent.kiteb_karattru_VALUE(힙[Referenza + 2 + 수]);
    }
    static int ċifra_karattru(int VALUE) {
        int Referenza = alloka_Ħażna(1, 11); if (żball) return 0;
        int tul_VALUE = 0;
        if (VALUE < 0) 힙[Referenza + 2 + tul_VALUE++] = '-'; else VALUE = -VALUE;
        int pożizzjoni_INDEX = 1000000000; boolean serje = false;
        while (pożizzjoni_INDEX != 0) {
            int 수 = -(VALUE / pożizzjoni_INDEX);
            if (수 != 0 || serje || pożizzjoni_INDEX == 1) { 힙[Referenza + 2 + tul_VALUE++] = '0' + 수; serje = true; }
            VALUE %= pożizzjoni_INDEX; pożizzjoni_INDEX /= 10;
        }
        힙[Referenza + 1] = tul_VALUE; return Referenza;
    }
    static int 정수해독(int Referenza) {
        if (!oġġett_VALUE(Referenza, 1)) return 0;
        int tul_VALUE = 힙[Referenza + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (tul_VALUE > 0 && (힙[Referenza + 2] == '-' || 힙[Referenza + 2] == '+')) { 음수 = 힙[Referenza + 2] == '-'; 수++; }
        if (수 == tul_VALUE) żball_VALUE("NumberFormatException");
        for (; 수 < tul_VALUE && !żball; 수++) {
            int ċifra_VALUE = 힙[Referenza + 2 + 수] - '0';
            if (ċifra_VALUE < 0 || ċifra_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && ċifra_VALUE > (음수 ? 8 : 7)) żball_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - ċifra_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (żball) return;
        if (frejm_INDEX < 0 || frejm_Munzell[frejm_INDEX] >= metodu_Munzell[frejm_metodu[frejm_INDEX]]) { żball_VALUE("operand stack overflow"); return; }
        int slott_entrata = frejm_INDEX * 128 + frejm_Munzell[frejm_INDEX]++; 스택값[slott_entrata] = VALUE; 스택형[slott_entrata] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (żball) return 0;
        if (frejm_INDEX < 0 || frejm_Munzell[frejm_INDEX] < 1) { żball_VALUE("operand stack underflow"); return 0; }
        int slott_entrata = frejm_INDEX * 128 + --frejm_Munzell[frejm_INDEX]; 반환형 = 스택형[slott_entrata];
        if (TYPE_VALUE != 0 && 반환형 != TYPE_VALUE) żball_VALUE("operand type mismatch");
        return 스택값[slott_entrata];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frejm_metodu[frejm_INDEX]] || INDEX < 0 || lokali_TYPE[frejm_INDEX * 128 + INDEX] != TYPE_VALUE) { żball_VALUE("invalid or uninitialized local"); return; }
        넣기(lokali_VALUE[frejm_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void kiteb_lokali(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frejm_metodu[frejm_INDEX]] || INDEX < 0) { żball_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokali_VALUE[frejm_INDEX * 128 + INDEX] = VALUE; lokali_TYPE[frejm_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int pożizzjoni = frejm_pożizzjoni[frejm_INDEX];
        if (pożizzjoni < metodu_Bidu[frejm_metodu[frejm_INDEX]] || pożizzjoni >= metodu_ttermina[frejm_metodu[frejm_INDEX]]) { żball_VALUE("instruction pointer out of range"); return 0; }
        frejm_pożizzjoni[frejm_INDEX]++; return fajl[pożizzjoni];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void mexxi_VALUE(int pożizzjoni) {
        int FUNCTION_VALUE = frejm_metodu[frejm_INDEX];
        if (pożizzjoni < metodu_Bidu[FUNCTION_VALUE] || pożizzjoni >= metodu_ttermina[FUNCTION_VALUE] || 경계[pożizzjoni] != FUNCTION_VALUE + 1) żball_VALUE("invalid branch target");
        else frejm_pożizzjoni[frejm_INDEX] = pożizzjoni;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (frejm_INDEX == 31) { żball_VALUE("call stack limit (32)"); return; }
        int Li_Jmiss_element = frejm_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokali_TYPE[Li_Jmiss_element * 128 + 수] = 0;
        for (int 수 = metodu_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokali_VALUE[Li_Jmiss_element * 128 + 수] = 빼기(metodu_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokali_TYPE[Li_Jmiss_element * 128 + 수] = metodu_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        frejm_INDEX = Li_Jmiss_element; frejm_metodu[frejm_INDEX] = FUNCTION_VALUE; frejm_pożizzjoni[frejm_INDEX] = metodu_Bidu[FUNCTION_VALUE]; frejm_Munzell[frejm_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[frejm_metodu[frejm_INDEX]]) { żball_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        frejm_INDEX--; if (frejm_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_fajl_isem = new int[64];
    static void fajl_Stream_CALL(int propjetarju_VALUE, int isem, int format_VALUE, int kmand) {
        boolean 출력 = Word_SMS(propjetarju_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (kmand == 183 && Word_SMS(isem, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { żball_VALUE("unsupported file stream constructor"); return; }
            int fajl_entrata_isem = 빼기(2), Stream_VALUE = 빼기(2);
            if (!oġġett_VALUE(fajl_entrata_isem, 1) || !oġġett_VALUE(Stream_VALUE, 종류) || żball) return;
            if (힙[Stream_VALUE + 3] != 0) { żball_VALUE("file stream already initialized"); return; }
            int tul_VALUE = 힙[fajl_entrata_isem + 1];
            if (tul_VALUE < 1 || tul_VALUE > 63) { żball_VALUE("invalid file name length"); return; }
            for (int slott_entrata = 0; slott_entrata < tul_VALUE; slott_entrata++) {
                int VALUE = 힙[fajl_entrata_isem + 2 + slott_entrata];
                if (VALUE < 1 || VALUE > 127) { żball_VALUE("file stream paths currently require ASCII"); return; }
                Stream_fajl_isem[slott_entrata] = VALUE;
            }
            Stream_fajl_isem[tul_VALUE] = 0;
            int 서술자 = utent.파일서술자열기(Stream_fajl_isem, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { żball_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (kmand != 182) { żball_VALUE("invalid file stream invocation"); return; }
        int azzjoni = -1, VALUE = 0;
        if (Word_SMS(isem, "close") && Word_SMS(format_VALUE, "()V")) azzjoni = 0;
        if (!출력 && Word_SMS(isem, "read") && Word_SMS(format_VALUE, "()I")) azzjoni = 1;
        if (출력 && Word_SMS(isem, "write") && Word_SMS(format_VALUE, "(I)V")) { azzjoni = 2; VALUE = 빼기(1); }
        if (azzjoni < 0) { żball_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!oġġett_VALUE(Stream_VALUE, 종류) || żball) return;
        if (힙[Stream_VALUE + 3] == 0) { żball_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (azzjoni == 0) {
            if (서술자 >= 0 && utent.파일서술자닫기(서술자) < 0) żball_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { żball_VALUE("IOException: stream closed"); return; }
        if (azzjoni == 1) {
            int miżura = utent.파일한바이트읽기(서술자);
            if (miżura < -1) żball_VALUE("IOException: read failed"); else 넣기(miżura, 1);
        } else if (utent.파일한바이트쓰기(서술자, VALUE) != 1) żball_VALUE("IOException: write failed");
    }
    static void CALL_metodu(int INDEX, int kmand) {
        if (!ċekk_valur_fiss(INDEX, 10)) return;
        int propjetarju_VALUE = klassi_isem_SMS(상가[INDEX]), isem = Referenza_isem(valur_fiss_SECOND_VALUE[INDEX]), format_VALUE = Referenza_TYPE(valur_fiss_SECOND_VALUE[INDEX]);
        if (żball) return;
        if (같은말(propjetarju_VALUE, klassi_isem)) {
            if (kmand != 184) { żball_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metodu_COUNT; 수++) if (같은말(isem, metodu_isem_SMS[수]) && 같은말(format_VALUE, metodu_TYPE[수])) {
                if ((metodu_aċċess[수] & 8) == 0) żball_VALUE("method is not static"); else 호출(수);
                return;
            }
            żball_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(propjetarju_VALUE, "java/io/FileInputStream") || Word_SMS(propjetarju_VALUE, "java/io/FileOutputStream")) {
            fajl_Stream_CALL(propjetarju_VALUE, isem, format_VALUE, kmand); return;
        }
        if (kmand == 184 && Word_SMS(propjetarju_VALUE, "java/lang/Integer") && Word_SMS(isem, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (kmand == 182 && Word_SMS(propjetarju_VALUE, "java/io/PrintStream") && (Word_SMS(isem, "println") || Word_SMS(isem, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(isem, "println")) żball_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) żball_VALUE("invalid PrintStream receiver");
            if (żball) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) utent.kiteb(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) utent.kiteb_karattru_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) kiteb_SMS(VALUE);
            if (Word_SMS(isem, "println")) utent.kiteb_karattru_VALUE(10);
            return;
        }
        if (kmand == 182 && Word_SMS(propjetarju_VALUE, "java/lang/String")) {
            if (Word_SMS(isem, "length") && Word_SMS(format_VALUE, "()I")) {
                int Referenza = 빼기(2); if (oġġett_VALUE(Referenza, 1)) 넣기(힙[Referenza + 1], 1); return;
            }
            if (Word_SMS(isem, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int subscript_VALUE = 빼기(1), Referenza = 빼기(2);
                if (oġġett_VALUE(Referenza, 1)) {
                    if (subscript_VALUE < 0 || subscript_VALUE >= 힙[Referenza + 1]) żball_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Referenza + 2 + subscript_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(propjetarju_VALUE, "java/lang/StringBuilder")) {
            if (kmand == 183 && Word_SMS(isem, "<init>") && Word_SMS(format_VALUE, "()V")) { oġġett_VALUE(빼기(2), 4); return; }
            if (kmand == 182 && Word_SMS(isem, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Referenza = 빼기(2); if (oġġett_VALUE(Referenza, 4)) 넣기(힙[Referenza + 2] == 0 ? host_karattru("") : 힙[Referenza + 2], 2); return;
            }
            if (kmand == 182 && Word_SMS(isem, "append")) {
                int SMS = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = ċifra_karattru(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = host_karattru(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = alloka_Ħażna(1, 1); if (!żball) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = host_karattru("null"); }
                else { żball_VALUE("unsupported StringBuilder append"); return; }
                int Referenza = 빼기(2); if (!oġġett_VALUE(Referenza, 4) || !oġġett_VALUE(SMS, 1)) return;
                int 앞 = 힙[Referenza + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Lura_VALUE_tul = 힙[SMS + 1];
                int 새글 = alloka_Ħażna(1, 앞길이 + Lura_VALUE_tul); if (żball) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Lura_VALUE_tul; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[Referenza + 2] = 새글; 넣기(Referenza, 2); return;
            }
        }
        żball_VALUE("unsupported library method");
    }
    static int ARRAY_slott(int Referenza, int subscript_VALUE, int TYPE_VALUE) {
        if (!oġġett_VALUE(Referenza, TYPE_VALUE)) return 0;
        if (subscript_VALUE < 0 || subscript_VALUE >= 힙[Referenza + 1]) { żball_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referenza + 2 + subscript_VALUE;
    }
    static void eżegwixxa_kmand() {
        int 남음 = 500000;
        while (frejm_INDEX >= 0 && !żball) {
            if (--남음 == 0) { żball_VALUE("instruction limit (500000)"); break; }
            int serje = frejm_pożizzjoni[frejm_INDEX], VALUE = 명바();
            if (żball) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= valur_fiss_COUNT) żball_VALUE("invalid ldc constant");
                else if (valur_fiss_tag[수] == 3) 넣기(상가[수], 1);
                else if (valur_fiss_tag[수] == 8) 넣기(valur_fiss_SMS(상가[수]), 2);
                else żball_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { kiteb_lokali(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { kiteb_lokali(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { kiteb_lokali(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int subscript_VALUE = 빼기(1), Referenza = 빼기(2), slott_entrata = ARRAY_slott(Referenza, subscript_VALUE, VALUE == 46 ? 2 : 3);
                if (!żball) 넣기(힙[slott_entrata], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int element_element = 빼기(VALUE == 79 ? 1 : 2), subscript_VALUE = 빼기(1), Referenza = 빼기(2), slott_entrata = ARRAY_slott(Referenza, subscript_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && element_element != 0) oġġett_VALUE(element_element, 1);
                if (!żball) 힙[slott_entrata] = element_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = 반환형; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), miżura = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { żball_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) miżura = 가 + 나;
                if (VALUE == 100) miżura = 가 - 나;
                if (VALUE == 104) miżura = 가 * 나;
                if (VALUE == 108) miżura = 가 / 나;
                if (VALUE == 112) miżura = 가 % 나;
                if (VALUE == 120) miżura = 가 << 나;
                if (VALUE == 122) miżura = 가 >> 나;
                if (VALUE == 124) miżura = 가 >>> 나;
                if (VALUE == 126) miżura = 가 & 나;
                if (VALUE == 128) miżura = 가 | 나;
                if (VALUE == 130) miżura = 가 ^ 나;
                넣기(miżura, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokali_ambitu = 명바(), 증분 = (byte)명바(); 지역읽기(lokali_ambitu, 1); 넣기(빼기(1) + 증분, 1); kiteb_lokali(lokali_ambitu, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int destinazzjoni_VALUE = serje + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) mexxi_VALUE(destinazzjoni_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { 반환(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!ċekk_valur_fiss(수, 9)) continue;
                if (!Word_SMS(klassi_isem_SMS(상가[수]), "java/lang/System") || !Word_SMS(Referenza_isem(valur_fiss_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Referenza_TYPE(valur_fiss_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) żball_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metodu(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int isem = klassi_isem_SMS(명짧());
                if (Word_SMS(isem, "java/lang/StringBuilder")) 넣기(alloka_Ħażna(4, 1), 2);
                else if (Word_SMS(isem, "java/io/FileInputStream") || Word_SMS(isem, "java/io/FileOutputStream")) {
                    int Referenza = alloka_Ħażna(Word_SMS(isem, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!żball) { 힙[Referenza + 2] = -1; 넣기(Referenza, 2); }
                } else żball_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) żball_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(klassi_isem_SMS(명짧()), "java/lang/String")) żball_VALUE("only String[] anewarray is supported");
                int tul_VALUE = 빼기(1); 넣기(alloka_Ħażna(VALUE == 188 ? 2 : 3, tul_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Referenza = 빼기(2);
                if (Referenza < 1 || Referenza >= 힙끝 - 1 || (힙[Referenza] != 2 && 힙[Referenza] != 3)) żball_VALUE("null or invalid array");
                else 넣기(힙[Referenza + 1], 1); continue;
            }
            if (VALUE == 192) {
                int isem = klassi_isem_SMS(명짧()), Referenza = 빼기(2);
                if (!Word_SMS(isem, "java/lang/String")) żball_VALUE("unsupported checkcast");
                else if (Referenza != 0) oġġett_VALUE(Referenza, 1);
                넣기(Referenza, 2); continue;
            }
            żball_VALUE("unsupported bytecode");
        }
    }
    public static int serje() {
        if (utent.인수개수() == 1 && 자바도구.같음(utent.인수(0), "-version")) {
            utent.kiteb("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (utent.인수개수() < 1) { utent.kiteb("Usage: java CLASS [ARGS]\n"); return 2; }
        int tul_VALUE = 자바도구.isem(fajl_isem_SMS, utent.인수(0));
        if (tul_VALUE < 1 || tul_VALUE > 57) { utent.kiteb("java: invalid class name\n"); return 2; }
        fajl_isem_SMS[tul_VALUE] = '.'; fajl_isem_SMS[tul_VALUE + 1] = 'c'; fajl_isem_SMS[tul_VALUE + 2] = 'l'; fajl_isem_SMS[tul_VALUE + 3] = 'a'; fajl_isem_SMS[tul_VALUE + 4] = 's'; fajl_isem_SMS[tul_VALUE + 5] = 's';
        daqqas = utent.파일읽기(fajl_isem_SMS, fajl);
        if (daqqas < 0) { utent.kiteb("java: cannot read class: "); 자바도구.수쓰기(daqqas); utent.kiteb_karattru_VALUE(10); return 1; }
        클래스읽기(); if (żball) return 1;
        int karattru_isem = valur_fiss_SMS(klassi_isem);
        if (!żball && 힙[karattru_isem + 1] != tul_VALUE) żball_VALUE("class name does not match file");
        for (int 수 = 0; 수 < tul_VALUE && !żball; 수++) if (힙[karattru_isem + 2 + 수] != fajl_isem_SMS[수]) żball_VALUE("class name does not match file");
        int entrata_punt_VALUE = -1;
        for (int 수 = 0; 수 < metodu_COUNT; 수++) if (Word_SMS(metodu_isem_SMS[수], "main") && Word_SMS(metodu_TYPE[수], "([Ljava/lang/String;)V") && (metodu_aċċess[수] & 9) == 9) entrata_punt_VALUE = 수;
        if (entrata_punt_VALUE < 0) żball_VALUE("public static void main(String[] args) required");
        if (żball) return 1;
        int 인수 = alloka_Ħażna(3, utent.인수개수() - 1);
        for (int 수 = 1; 수 < utent.인수개수() && !żball; 수++) 힙[인수 + 1 + 수] = host_karattru(utent.인수(수));
        frejm_INDEX = 0; frejm_metodu[0] = entrata_punt_VALUE; frejm_pożizzjoni[0] = metodu_Bidu[entrata_punt_VALUE]; lokali_VALUE[0] = 인수; lokali_TYPE[0] = 2;
        eżegwixxa_kmand(); return żball ? 1 : 0;
    }
}
