// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Kartelë/스택/Referencë/degë 경계를 zbatoj_komandë 중 검사한다. */
public final class 자바가상기계 {
    static int[] Kartelë = new int[16384], skedar_emër_SMS = new int[64];
    static int[] konstante_shenjë = new int[512], 상가 = new int[512], konstante_SECOND_VALUE = new int[512], varg_Referencë = new int[512];
    static int[] metoda_emër_SMS = new int[32], metoda_TYPE = new int[32], metoda_qasem = new int[32];
    static int[] metoda_nis = new int[32], metoda_mbaroj = new int[32], metoda_Stivë = new int[32], 함수지역 = new int[32];
    static int[] metoda_argument_COUNT = new int[32], metoda_argument_TYPE = new int[512], metoda_Kthe = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lokal_VALUE = new int[4096], lokal_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] kuadër_metoda = new int[32], kuadër_pozicioni = new int[32], kuadër_Stivë = new int[32];
    static int[] 힙 = new int[8192];
    static int Madhësi, 읽기위치, konstante_COUNT, metoda_COUNT, klasë_emër, kuadër_INDEX = -1, 힙끝 = 1, Kthe_TYPE;
    static boolean GABIM;

    static void dështim_VALUE(String Word_SMS) {
        if (!GABIM) { përdorues.Shkrimi("JVM error: "); përdorues.Shkrimi(Word_SMS); përdorues.shkruaj_karakter_VALUE(10); }
        GABIM = true;
    }
    static boolean fragment(int Ekzekuto, int gjatësi_VALUE) { return Ekzekuto >= 0 && gjatësi_VALUE >= 0 && Ekzekuto <= Madhësi - gjatësi_VALUE; }
    static int bajt_VALUE() {
        if (!fragment(읽기위치, 1)) { dështim_VALUE("truncated class file"); return 0; }
        return Kartelë[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int numër_i_plotë() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int gjatësi_VALUE) { if (!fragment(읽기위치, gjatësi_VALUE)) dështim_VALUE("invalid attribute size"); else 읽기위치 += gjatësi_VALUE; }
    static boolean çek_konstante(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstante_COUNT || konstante_shenjë[수] != 종류) { dështim_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Ekzekuto, int gjatësi_VALUE, String Word_SMS) {
        if (!fragment(Ekzekuto, gjatësi_VALUE) || gjatësi_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < gjatësi_VALUE; 수++) if (Kartelë[Ekzekuto + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int njësi_COUNT = 짧은수();
        for (int 수 = 0; 수 < njësi_COUNT && !GABIM; 수++) { çek_konstante(짧은수(), 1); 건너(numër_i_plotë()); }
    }
    static int komandë_gjatësi(int VALUE) {
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
        if (numër_i_plotë() != 0xcafebabe) dështim_VALUE("not a class file");
        int 부판 = 짧은수(), version_VALUE = 짧은수();
        if (version_VALUE < 45 || version_VALUE > 52 || 부판 != 0) dështim_VALUE("supported class versions: 45..52, minor 0");
        konstante_COUNT = 짧은수();
        if (konstante_COUNT < 1 || konstante_COUNT > 512) { dështim_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konstante_COUNT && !GABIM; 수++) {
            int 종류 = bajt_VALUE(); konstante_shenjë[수] = 종류;
            if (종류 == 1) { konstante_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstante_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = numër_i_plotë();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konstante_SECOND_VALUE[수] = 짧은수(); }
            else dështim_VALUE("unsupported constant type");
        }
        int leje_VALUE = 짧은수();
        if ((leje_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) dështim_VALUE("unsupported class flags");
        klasë_emër = klasë_emër_SMS(짧은수());
        if (!Word_SMS(klasë_emër_SMS(짧은수()), "java/lang/Object")) dështim_VALUE("inheritance unsupported");
        if (짧은수() != 0) dështim_VALUE("interfaces unsupported");
        if (짧은수() != 0) dështim_VALUE("fields unsupported");
        metoda_COUNT = 짧은수();
        if (metoda_COUNT < 1 || metoda_COUNT > 32) { dështim_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metoda_COUNT && !GABIM; 수++) {
            metoda_qasem[수] = 짧은수(); metoda_emër_SMS[수] = 짧은수(); metoda_TYPE[수] = 짧은수();
            çek_konstante(metoda_emër_SMS[수], 1); 서술읽기(수);
            if ((metoda_qasem[수] & (0x100 | 0x400 | 0x20)) != 0) dështim_VALUE("native, abstract and synchronized methods unsupported");
            if ((metoda_qasem[수] & 8) == 0 && !Word_SMS(metoda_emër_SMS[수], "<init>")) dështim_VALUE("instance methods unsupported");
            if (Word_SMS(metoda_emër_SMS[수], "<clinit>")) dështim_VALUE("class initializers unsupported");
            for (int e_përparme_VALUE = 0; e_përparme_VALUE < 수; e_përparme_VALUE++) if (같은말(metoda_emër_SMS[e_përparme_VALUE], metoda_emër_SMS[수]) && 같은말(metoda_TYPE[e_përparme_VALUE], metoda_TYPE[수])) dështim_VALUE("duplicate method");
            int njësi_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < njësi_COUNT && !GABIM; atribut_VALUE++) {
                int Emër = 짧은수(), gjatësi_VALUE = numër_i_plotë(), Ekzekuto = 읽기위치;
                if (!fragment(Ekzekuto, gjatësi_VALUE)) { dështim_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Emër, "Code")) {
                    if (metoda_nis[수] != 0) dështim_VALUE("duplicate Code attribute");
                    metoda_Stivë[수] = 짧은수(); 함수지역[수] = 짧은수(); int kod_gjatësi = numër_i_plotë();
                    if (metoda_Stivë[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metoda_argument_COUNT[수]
                        || kod_gjatësi < 1 || kod_gjatësi > 8192) dështim_VALUE("method memory limits exceeded");
                    metoda_nis[수] = 읽기위치; 건너(kod_gjatësi); metoda_mbaroj[수] = 읽기위치;
                    if (짧은수() != 0) dështim_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Ekzekuto + gjatësi_VALUE) dështim_VALUE("Code attribute size mismatch");
                } else 건너(gjatësi_VALUE);
            }
            if (metoda_nis[수] == 0) dështim_VALUE("missing Code attribute");
            int hapësirë_për_tekst_futje = metoda_nis[수];
            while (hapësirë_për_tekst_futje < metoda_mbaroj[수] && !GABIM) {
                int gjatësi_VALUE = komandë_gjatësi(Kartelë[hapësirë_për_tekst_futje]);
                if (gjatësi_VALUE == 0 || gjatësi_VALUE > metoda_mbaroj[수] - hapësirë_për_tekst_futje) { dështim_VALUE("unsupported or truncated bytecode"); break; }
                경계[hapësirë_për_tekst_futje] = 수 + 1; hapësirë_për_tekst_futje += gjatësi_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 degë 목적지를 허용하지 않는다.
            hapësirë_për_tekst_futje = metoda_nis[수];
            while (hapësirë_për_tekst_futje < metoda_mbaroj[수] && !GABIM) {
                int VALUE = Kartelë[hapësirë_për_tekst_futje];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int vendmbërritje_VALUE = hapësirë_për_tekst_futje + (short)(Kartelë[hapësirë_për_tekst_futje + 1] << 8 | Kartelë[hapësirë_për_tekst_futje + 2]);
                    if (vendmbërritje_VALUE < metoda_nis[수] || vendmbërritje_VALUE >= metoda_mbaroj[수] || 경계[vendmbërritje_VALUE] != 수 + 1) dështim_VALUE("invalid branch target");
                }
                hapësirë_për_tekst_futje += komandë_gjatësi(VALUE);
            }
        }
        if (!GABIM) 속성건너();
        if (읽기위치 != Madhësi) dështim_VALUE("extra class file data");
    }
    static int caktoj_hapësira_ruajtëse(int 종류, int gjatësi_VALUE) {
        if (gjatësi_VALUE < 0 || gjatësi_VALUE > 힙.length - 힙끝 - 2) { dështim_VALUE("object heap exhausted or negative array size"); return 0; }
        int Referencë = 힙끝; 힙끝 += gjatësi_VALUE + 2; 힙[Referencë] = 종류; 힙[Referencë + 1] = gjatësi_VALUE;
        return Referencë;
    }
    static boolean objekt_VALUE(int Referencë, int 종류) {
        if (Referencë < 1 || Referencë >= 힙끝 - 1 || 힙[Referencë] != 종류) { dështim_VALUE("null or invalid object reference"); return false; }
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
        if (kuadër_INDEX == 31) { dështim_VALUE("call stack limit (32)"); return; }
        int Tjetër_njësi = kuadër_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Tjetër_njësi * 128 + 수] = 0;
        for (int 수 = metoda_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Tjetër_njësi * 128 + 수] = 빼기(metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokal_TYPE[Tjetër_njësi * 128 + 수] = metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        kuadër_INDEX = Tjetër_njësi; kuadër_metoda[kuadër_INDEX] = FUNCTION_VALUE; kuadër_pozicioni[kuadër_INDEX] = metoda_nis[FUNCTION_VALUE]; kuadër_Stivë[kuadër_INDEX] = 0;
    }
    static void Kthe_llogaritje(int TYPE_VALUE) {
        if (TYPE_VALUE != metoda_Kthe[kuadër_metoda[kuadër_INDEX]]) { dështim_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        kuadër_INDEX--; if (kuadër_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { dështim_VALUE("file stream paths currently require ASCII"); return; }
                Stream_skedar_emër[hapësirë_për_tekst_futje] = VALUE;
            }
            Stream_skedar_emër[gjatësi_VALUE] = 0;
            int 서술자 = përdorues.파일서술자열기(Stream_skedar_emër, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { dështim_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Komanda != 182) { dështim_VALUE("invalid file stream invocation"); return; }
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
            if (llogaritje < -1) dështim_VALUE("IOException: read failed"); else 넣기(llogaritje, 1);
        } else if (përdorues.파일한바이트쓰기(서술자, VALUE) != 1) dështim_VALUE("IOException: write failed");
    }
    static void CALL_metoda(int INDEX, int Komanda) {
        if (!çek_konstante(INDEX, 10)) return;
        int pronari_VALUE = klasë_emër_SMS(상가[INDEX]), Emër = Referencë_emër(konstante_SECOND_VALUE[INDEX]), format_VALUE = Referencë_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (GABIM) return;
        if (같은말(pronari_VALUE, klasë_emër)) {
            if (Komanda != 184) { dështim_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metoda_COUNT; 수++) if (같은말(Emër, metoda_emër_SMS[수]) && 같은말(format_VALUE, metoda_TYPE[수])) {
                if ((metoda_qasem[수] & 8) == 0) dështim_VALUE("method is not static"); else 호출(수);
                return;
            }
            dështim_VALUE("NoSuchMethodError"); return;
        }
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
        dështim_VALUE("unsupported library method");
    }
    static int ARRAY_hapësirë_për_tekst(int Referencë, int shkrim_i_poshtëm_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(Referencë, TYPE_VALUE)) return 0;
        if (shkrim_i_poshtëm_VALUE < 0 || shkrim_i_poshtëm_VALUE >= 힙[Referencë + 1]) { dështim_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referencë + 2 + shkrim_i_poshtëm_VALUE;
    }
    static void zbatoj_komandë() {
        int 남음 = 500000;
        while (kuadër_INDEX >= 0 && !GABIM) {
            if (--남음 == 0) { dështim_VALUE("instruction limit (500000)"); break; }
            int Ekzekuto = kuadër_pozicioni[kuadër_INDEX], VALUE = 명바();
            if (GABIM) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konstante_COUNT) dështim_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int shkrim_i_poshtëm_VALUE = 빼기(1), Referencë = 빼기(2), hapësirë_për_tekst_futje = ARRAY_hapësirë_për_tekst(Referencë, shkrim_i_poshtëm_VALUE, VALUE == 46 ? 2 : 3);
                if (!GABIM) 넣기(힙[hapësirë_për_tekst_futje], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int njësi_element = 빼기(VALUE == 79 ? 1 : 2), shkrim_i_poshtëm_VALUE = 빼기(1), Referencë = 빼기(2), hapësirë_për_tekst_futje = ARRAY_hapësirë_për_tekst(Referencë, shkrim_i_poshtëm_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && njësi_element != 0) objekt_VALUE(njësi_element, 1);
                if (!GABIM) 힙[hapësirë_për_tekst_futje] = njësi_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = Kthe_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = Kthe_TYPE, 나 = 빼기(0), 나형 = Kthe_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!çek_konstante(수, 9)) continue;
                if (!Word_SMS(klasë_emër_SMS(상가[수]), "java/lang/System") || !Word_SMS(Referencë_emër(konstante_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Referencë_TYPE(konstante_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) dështim_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metoda(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Emër = klasë_emër_SMS(명짧());
                if (Word_SMS(Emër, "java/lang/StringBuilder")) 넣기(caktoj_hapësira_ruajtëse(4, 1), 2);
                else if (Word_SMS(Emër, "java/io/FileInputStream") || Word_SMS(Emër, "java/io/FileOutputStream")) {
                    int Referencë = caktoj_hapësira_ruajtëse(Word_SMS(Emër, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!GABIM) { 힙[Referencë + 2] = -1; 넣기(Referencë, 2); }
                } else dështim_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) dështim_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(klasë_emër_SMS(명짧()), "java/lang/String")) dështim_VALUE("only String[] anewarray is supported");
                int gjatësi_VALUE = 빼기(1); 넣기(caktoj_hapësira_ruajtëse(VALUE == 188 ? 2 : 3, gjatësi_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Referencë = 빼기(2);
                if (Referencë < 1 || Referencë >= 힙끝 - 1 || (힙[Referencë] != 2 && 힙[Referencë] != 3)) dështim_VALUE("null or invalid array");
                else 넣기(힙[Referencë + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Emër = klasë_emër_SMS(명짧()), Referencë = 빼기(2);
                if (!Word_SMS(Emër, "java/lang/String")) dështim_VALUE("unsupported checkcast");
                else if (Referencë != 0) objekt_VALUE(Referencë, 1);
                넣기(Referencë, 2); continue;
            }
            dështim_VALUE("unsupported bytecode");
        }
    }
    public static int Ekzekuto() {
        if (përdorues.인수개수() == 1 && 자바도구.같음(përdorues.Argumente(0), "-version")) {
            përdorues.Shkrimi("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (përdorues.인수개수() < 1) { përdorues.Shkrimi("Usage: java CLASS [ARGS]\n"); return 2; }
        int gjatësi_VALUE = 자바도구.Emër(skedar_emër_SMS, përdorues.Argumente(0));
        if (gjatësi_VALUE < 1 || gjatësi_VALUE > 57) { përdorues.Shkrimi("java: invalid class name\n"); return 2; }
        skedar_emër_SMS[gjatësi_VALUE] = '.'; skedar_emër_SMS[gjatësi_VALUE + 1] = 'c'; skedar_emër_SMS[gjatësi_VALUE + 2] = 'l'; skedar_emër_SMS[gjatësi_VALUE + 3] = 'a'; skedar_emër_SMS[gjatësi_VALUE + 4] = 's'; skedar_emër_SMS[gjatësi_VALUE + 5] = 's';
        Madhësi = përdorues.파일읽기(skedar_emër_SMS, Kartelë);
        if (Madhësi < 0) { përdorues.Shkrimi("java: cannot read class: "); 자바도구.수쓰기(Madhësi); përdorues.shkruaj_karakter_VALUE(10); return 1; }
        클래스읽기(); if (GABIM) return 1;
        int karakter_emër = konstante_SMS(klasë_emër);
        if (!GABIM && 힙[karakter_emër + 1] != gjatësi_VALUE) dështim_VALUE("class name does not match file");
        for (int 수 = 0; 수 < gjatësi_VALUE && !GABIM; 수++) if (힙[karakter_emër + 2 + 수] != skedar_emër_SMS[수]) dështim_VALUE("class name does not match file");
        int futje_p_VALUE = -1;
        for (int 수 = 0; 수 < metoda_COUNT; 수++) if (Word_SMS(metoda_emër_SMS[수], "main") && Word_SMS(metoda_TYPE[수], "([Ljava/lang/String;)V") && (metoda_qasem[수] & 9) == 9) futje_p_VALUE = 수;
        if (futje_p_VALUE < 0) dështim_VALUE("public static void main(String[] args) required");
        if (GABIM) return 1;
        int Argumente = caktoj_hapësira_ruajtëse(3, përdorues.인수개수() - 1);
        for (int 수 = 1; 수 < përdorues.인수개수() && !GABIM; 수++) 힙[Argumente + 1 + 수] = pritës_karakter(përdorues.Argumente(수));
        kuadër_INDEX = 0; kuadër_metoda[0] = futje_p_VALUE; kuadër_pozicioni[0] = metoda_nis[futje_p_VALUE]; lokal_VALUE[0] = Argumente; lokal_TYPE[0] = 2;
        zbatoj_komandë(); return GABIM ? 1 : 0;
    }
}
