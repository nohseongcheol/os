// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Skrá/스택/tilvísun/grein 경계를 keyra_skipun 중 검사한다. */
public final class 자바가상기계 {
    static int[] Skrá = new int[16384], skrá_heiti_SMS = new int[64];
    static int[] fasti_merki = new int[512], 상가 = new int[512], fasti_SECOND_VALUE = new int[512], strengur_tilvísun = new int[512];
    static int[] aðferð_heiti_SMS = new int[32], aðferð_TYPE = new int[32], aðferð_aðgangur = new int[32];
    static int[] aðferð_Opna = new int[32], aðferð_ljúka = new int[32], aðferð_bunki = new int[32], 함수지역 = new int[32];
    static int[] aðferð_frumbreyta_COUNT = new int[32], aðferð_frumbreyta_TYPE = new int[512], aðferð_skila = new int[32];
    static int[] 경계 = new int[16384];
    static int[] staðbundið_VALUE = new int[4096], staðbundið_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] ramma_aðferð = new int[32], ramma_staða = new int[32], ramma_bunki = new int[32];
    static int[] 힙 = new int[8192];
    static int Stærð, 읽기위치, fasti_COUNT, aðferð_COUNT, klasi_heiti, ramma_INDEX = -1, 힙끝 = 1, skila_TYPE;
    static boolean Villa;

    static void bilun_VALUE(String Word_SMS) {
        if (!Villa) { notandi.Skrift("JVM error: "); notandi.Skrift(Word_SMS); notandi.skrifa_stafur_VALUE(10); }
        Villa = true;
    }
    static boolean miðlaskrá(int Keyra_2, int lengd_VALUE) { return Keyra_2 >= 0 && lengd_VALUE >= 0 && Keyra_2 <= Stærð - lengd_VALUE; }
    static int bæti_VALUE() {
        if (!miðlaskrá(읽기위치, 1)) { bilun_VALUE("truncated class file"); return 0; }
        return Skrá[읽기위치++];
    }
    static int 짧은수() { return bæti_VALUE() << 8 | bæti_VALUE(); }
    static int heiltala() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lengd_VALUE) { if (!miðlaskrá(읽기위치, lengd_VALUE)) bilun_VALUE("invalid attribute size"); else 읽기위치 += lengd_VALUE; }
    static boolean athuga_fasti(int númer, int 종류) {
        if (númer <= 0 || númer >= fasti_COUNT || fasti_merki[númer] != 종류) { bilun_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Keyra_2, int lengd_VALUE, String Word_SMS) {
        if (!miðlaskrá(Keyra_2, lengd_VALUE) || lengd_VALUE != Word_SMS.length()) return false;
        for (int númer = 0; númer < lengd_VALUE; númer++) if (Skrá[Keyra_2 + númer] != Word_SMS.charAt(númer)) return false;
        return true;
    }
    static boolean Word_SMS(int fasti_VALUE, String Word_SMS) { return athuga_fasti(fasti_VALUE, 1) && 구간(상가[fasti_VALUE], fasti_SECOND_VALUE[fasti_VALUE], Word_SMS); }
    static boolean samsvörun_Word(int 가, int 나) {
        if (!athuga_fasti(가, 1) || !athuga_fasti(나, 1) || fasti_SECOND_VALUE[가] != fasti_SECOND_VALUE[나]) return false;
        for (int númer = 0; númer < fasti_SECOND_VALUE[가]; númer++) if (Skrá[상가[가] + númer] != Skrá[상가[나] + númer]) return false;
        return true;
    }
    static int klasi_heiti_SMS(int númer) { return athuga_fasti(númer, 7) && athuga_fasti(상가[númer], 1) ? 상가[númer] : 0; }
    static int tilvísun_heiti(int númer) { return athuga_fasti(númer, 12) && athuga_fasti(상가[númer], 1) ? 상가[númer] : 0; }
    static int tilvísun_TYPE(int númer) { return athuga_fasti(númer, 12) && athuga_fasti(fasti_SECOND_VALUE[númer], 1) ? fasti_SECOND_VALUE[númer] : 0; }
    static int 서술형(int 끝, boolean autt_TYPE) {
        if (읽기위치 >= 끝) { bilun_VALUE("invalid descriptor"); return 0; }
        int VALUE = bæti_VALUE();
        if (VALUE == 'V' && autt_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Keyra_2 = 읽기위치;
            while (읽기위치 < 끝 && Skrá[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Keyra_2) bilun_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        bilun_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int fall_VALUE) {
        int 이전 = 읽기위치, númer = aðferð_TYPE[fall_VALUE];
        if (!athuga_fasti(númer, 1)) return;
        읽기위치 = 상가[númer]; int 끝 = 읽기위치 + fasti_SECOND_VALUE[númer];
        if (bæti_VALUE() != '(') bilun_VALUE("invalid method descriptor");
        int vara_COUNT = 0;
        while (!Villa && 읽기위치 < 끝 && Skrá[읽기위치] != ')') {
            if (vara_COUNT == 16) { bilun_VALUE("too many method arguments"); break; }
            aðferð_frumbreyta_TYPE[fall_VALUE * 16 + vara_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bæti_VALUE() != ')') bilun_VALUE("invalid method descriptor");
        aðferð_skila[fall_VALUE] = 서술형(끝, true); aðferð_frumbreyta_COUNT[fall_VALUE] = vara_COUNT;
        if (읽기위치 != 끝) bilun_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int vara_COUNT = 짧은수();
        for (int númer = 0; númer < vara_COUNT && !Villa; númer++) { athuga_fasti(짧은수(), 1); 건너(heiltala()); }
    }
    static int skipun_lengd(int VALUE) {
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
        if (heiltala() != 0xcafebabe) bilun_VALUE("not a class file");
        int 부판 = 짧은수(), útgáfa_VALUE = 짧은수();
        if (útgáfa_VALUE < 45 || útgáfa_VALUE > 52 || 부판 != 0) bilun_VALUE("supported class versions: 45..52, minor 0");
        fasti_COUNT = 짧은수();
        if (fasti_COUNT < 1 || fasti_COUNT > 512) { bilun_VALUE("constant pool limit (511)"); return; }
        for (int númer = 1; númer < fasti_COUNT && !Villa; númer++) {
            int 종류 = bæti_VALUE(); fasti_merki[númer] = 종류;
            if (종류 == 1) { fasti_SECOND_VALUE[númer] = 짧은수(); 상가[númer] = 읽기위치; 건너(fasti_SECOND_VALUE[númer]); }
            else if (종류 == 3) 상가[númer] = heiltala();
            else if (종류 == 7 || 종류 == 8) 상가[númer] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[númer] = 짧은수(); fasti_SECOND_VALUE[númer] = 짧은수(); }
            else bilun_VALUE("unsupported constant type");
        }
        int leyfi_VALUE = 짧은수();
        if ((leyfi_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) bilun_VALUE("unsupported class flags");
        klasi_heiti = klasi_heiti_SMS(짧은수());
        if (!Word_SMS(klasi_heiti_SMS(짧은수()), "java/lang/Object")) bilun_VALUE("inheritance unsupported");
        if (짧은수() != 0) bilun_VALUE("interfaces unsupported");
        if (짧은수() != 0) bilun_VALUE("fields unsupported");
        aðferð_COUNT = 짧은수();
        if (aðferð_COUNT < 1 || aðferð_COUNT > 32) { bilun_VALUE("method count limit (32)"); return; }
        for (int númer = 0; númer < aðferð_COUNT && !Villa; númer++) {
            aðferð_aðgangur[númer] = 짧은수(); aðferð_heiti_SMS[númer] = 짧은수(); aðferð_TYPE[númer] = 짧은수();
            athuga_fasti(aðferð_heiti_SMS[númer], 1); 서술읽기(númer);
            if ((aðferð_aðgangur[númer] & (0x100 | 0x400 | 0x20)) != 0) bilun_VALUE("native, abstract and synchronized methods unsupported");
            if ((aðferð_aðgangur[númer] & 8) == 0 && !Word_SMS(aðferð_heiti_SMS[númer], "<init>")) bilun_VALUE("instance methods unsupported");
            if (Word_SMS(aðferð_heiti_SMS[númer], "<clinit>")) bilun_VALUE("class initializers unsupported");
            for (int myndavél_að_framan_VALUE = 0; myndavél_að_framan_VALUE < númer; myndavél_að_framan_VALUE++) if (samsvörun_Word(aðferð_heiti_SMS[myndavél_að_framan_VALUE], aðferð_heiti_SMS[númer]) && samsvörun_Word(aðferð_TYPE[myndavél_að_framan_VALUE], aðferð_TYPE[númer])) bilun_VALUE("duplicate method");
            int vara_COUNT = 짧은수();
            for (int eigind_VALUE = 0; eigind_VALUE < vara_COUNT && !Villa; eigind_VALUE++) {
                int Heiti = 짧은수(), lengd_VALUE = heiltala(), Keyra_2 = 읽기위치;
                if (!miðlaskrá(Keyra_2, lengd_VALUE)) { bilun_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Heiti, "Code")) {
                    if (aðferð_Opna[númer] != 0) bilun_VALUE("duplicate Code attribute");
                    aðferð_bunki[númer] = 짧은수(); 함수지역[númer] = 짧은수(); int CODE_lengd = heiltala();
                    if (aðferð_bunki[númer] > 128 || 함수지역[númer] > 128 || 함수지역[númer] < aðferð_frumbreyta_COUNT[númer]
                        || CODE_lengd < 1 || CODE_lengd > 8192) bilun_VALUE("method memory limits exceeded");
                    aðferð_Opna[númer] = 읽기위치; 건너(CODE_lengd); aðferð_ljúka[númer] = 읽기위치;
                    if (짧은수() != 0) bilun_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Keyra_2 + lengd_VALUE) bilun_VALUE("Code attribute size mismatch");
                } else 건너(lengd_VALUE);
            }
            if (aðferð_Opna[númer] == 0) bilun_VALUE("missing Code attribute");
            int rauf_færsla = aðferð_Opna[númer];
            while (rauf_færsla < aðferð_ljúka[númer] && !Villa) {
                int lengd_VALUE = skipun_lengd(Skrá[rauf_færsla]);
                if (lengd_VALUE == 0 || lengd_VALUE > aðferð_ljúka[númer] - rauf_færsla) { bilun_VALUE("unsupported or truncated bytecode"); break; }
                경계[rauf_færsla] = númer + 1; rauf_færsla += lengd_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 grein 목적지를 허용하지 않는다.
            rauf_færsla = aðferð_Opna[númer];
            while (rauf_færsla < aðferð_ljúka[númer] && !Villa) {
                int VALUE = Skrá[rauf_færsla];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int endastaður_VALUE = rauf_færsla + (short)(Skrá[rauf_færsla + 1] << 8 | Skrá[rauf_færsla + 2]);
                    if (endastaður_VALUE < aðferð_Opna[númer] || endastaður_VALUE >= aðferð_ljúka[númer] || 경계[endastaður_VALUE] != númer + 1) bilun_VALUE("invalid branch target");
                }
                rauf_færsla += skipun_lengd(VALUE);
            }
        }
        if (!Villa) 속성건너();
        if (읽기위치 != Stærð) bilun_VALUE("extra class file data");
    }
    static int úthluta_geymsla(int 종류, int lengd_VALUE) {
        if (lengd_VALUE < 0 || lengd_VALUE > 힙.length - 힙끝 - 2) { bilun_VALUE("object heap exhausted or negative array size"); return 0; }
        int tilvísun = 힙끝; 힙끝 += lengd_VALUE + 2; 힙[tilvísun] = 종류; 힙[tilvísun + 1] = lengd_VALUE;
        return tilvísun;
    }
    static boolean hlutur_VALUE(int tilvísun, int 종류) {
        if (tilvísun < 1 || tilvísun >= 힙끝 - 1 || 힙[tilvísun] != 종류) { bilun_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int fasti_SMS(int INDEX) {
        if (!athuga_fasti(INDEX, 1)) return 0;
        if (strengur_tilvísun[INDEX] != 0) return strengur_tilvísun[INDEX];
        int tilvísun = úthluta_geymsla(1, fasti_SECOND_VALUE[INDEX]); if (Villa) return 0;
        int 끝 = 상가[INDEX] + fasti_SECOND_VALUE[INDEX], númer = 상가[INDEX], lengd_VALUE = 0;
        while (númer < 끝 && !Villa) {
            int VALUE = Skrá[númer++];
            if (VALUE == 0) bilun_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && númer < 끝) {
                int Áfram_vara = Skrá[númer++];
                if ((Áfram_vara & 192) != 128) bilun_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Áfram_vara & 63;
                if (VALUE != 0 && VALUE < 128) bilun_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && númer + 1 < 끝) {
                int 가 = Skrá[númer++], 나 = Skrá[númer++];
                if ((가 & 192) != 128 || (나 & 192) != 128) bilun_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) bilun_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) bilun_VALUE("invalid modified UTF-8");
            힙[tilvísun + 2 + lengd_VALUE++] = VALUE;
        }
        힙[tilvísun + 1] = lengd_VALUE; strengur_tilvísun[INDEX] = tilvísun; return tilvísun;
    }
    static int hýsa_stafur(String VALUE) {
        int tilvísun = úthluta_geymsla(1, VALUE.length()); if (Villa) return 0;
        for (int númer = 0; númer < VALUE.length(); númer++) 힙[tilvísun + 2 + númer] = VALUE.charAt(númer);
        return tilvísun;
    }
    static void skrifa_SMS(int tilvísun) {
        if (tilvísun == 0) { notandi.Skrift("null"); return; }
        if (!hlutur_VALUE(tilvísun, 1)) return;
        for (int númer = 0; númer < 힙[tilvísun + 1]; númer++) notandi.skrifa_stafur_VALUE(힙[tilvísun + 2 + númer]);
    }
    static int tölustafur_stafur(int VALUE) {
        int tilvísun = úthluta_geymsla(1, 11); if (Villa) return 0;
        int lengd_VALUE = 0;
        if (VALUE < 0) 힙[tilvísun + 2 + lengd_VALUE++] = '-'; else VALUE = -VALUE;
        int staða_INDEX = 1000000000; boolean Keyra_2 = false;
        while (staða_INDEX != 0) {
            int númer = -(VALUE / staða_INDEX);
            if (númer != 0 || Keyra_2 || staða_INDEX == 1) { 힙[tilvísun + 2 + lengd_VALUE++] = '0' + númer; Keyra_2 = true; }
            VALUE %= staða_INDEX; staða_INDEX /= 10;
        }
        힙[tilvísun + 1] = lengd_VALUE; return tilvísun;
    }
    static int 정수해독(int tilvísun) {
        if (!hlutur_VALUE(tilvísun, 1)) return 0;
        int lengd_VALUE = 힙[tilvísun + 1], númer = 0, VALUE = 0; boolean 음수 = false;
        if (lengd_VALUE > 0 && (힙[tilvísun + 2] == '-' || 힙[tilvísun + 2] == '+')) { 음수 = 힙[tilvísun + 2] == '-'; númer++; }
        if (númer == lengd_VALUE) bilun_VALUE("NumberFormatException");
        for (; númer < lengd_VALUE && !Villa; númer++) {
            int tölustafur_VALUE = 힙[tilvísun + 2 + númer] - '0';
            if (tölustafur_VALUE < 0 || tölustafur_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && tölustafur_VALUE > (음수 ? 8 : 7)) bilun_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - tölustafur_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Villa) return;
        if (ramma_INDEX < 0 || ramma_bunki[ramma_INDEX] >= aðferð_bunki[ramma_aðferð[ramma_INDEX]]) { bilun_VALUE("operand stack overflow"); return; }
        int rauf_færsla = ramma_INDEX * 128 + ramma_bunki[ramma_INDEX]++; 스택값[rauf_færsla] = VALUE; 스택형[rauf_færsla] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Villa) return 0;
        if (ramma_INDEX < 0 || ramma_bunki[ramma_INDEX] < 1) { bilun_VALUE("operand stack underflow"); return 0; }
        int rauf_færsla = ramma_INDEX * 128 + --ramma_bunki[ramma_INDEX]; skila_TYPE = 스택형[rauf_færsla];
        if (TYPE_VALUE != 0 && skila_TYPE != TYPE_VALUE) bilun_VALUE("operand type mismatch");
        return 스택값[rauf_færsla];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[ramma_aðferð[ramma_INDEX]] || INDEX < 0 || staðbundið_TYPE[ramma_INDEX * 128 + INDEX] != TYPE_VALUE) { bilun_VALUE("invalid or uninitialized local"); return; }
        넣기(staðbundið_VALUE[ramma_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void skrifa_staðbundið(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[ramma_aðferð[ramma_INDEX]] || INDEX < 0) { bilun_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); staðbundið_VALUE[ramma_INDEX * 128 + INDEX] = VALUE; staðbundið_TYPE[ramma_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Staðsetning = ramma_staða[ramma_INDEX];
        if (Staðsetning < aðferð_Opna[ramma_aðferð[ramma_INDEX]] || Staðsetning >= aðferð_ljúka[ramma_aðferð[ramma_INDEX]]) { bilun_VALUE("instruction pointer out of range"); return 0; }
        ramma_staða[ramma_INDEX]++; return Skrá[Staðsetning];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void færa_VALUE(int Staðsetning) {
        int fall_VALUE = ramma_aðferð[ramma_INDEX];
        if (Staðsetning < aðferð_Opna[fall_VALUE] || Staðsetning >= aðferð_ljúka[fall_VALUE] || 경계[Staðsetning] != fall_VALUE + 1) bilun_VALUE("invalid branch target");
        else ramma_staða[ramma_INDEX] = Staðsetning;
    }
    static void 호출(int fall_VALUE) {
        if (ramma_INDEX == 31) { bilun_VALUE("call stack limit (32)"); return; }
        int Áfram_vara = ramma_INDEX + 1;
        for (int númer = 0; númer < 128; númer++) staðbundið_TYPE[Áfram_vara * 128 + númer] = 0;
        for (int númer = aðferð_frumbreyta_COUNT[fall_VALUE] - 1; númer >= 0; númer--) {
            staðbundið_VALUE[Áfram_vara * 128 + númer] = 빼기(aðferð_frumbreyta_TYPE[fall_VALUE * 16 + númer]); staðbundið_TYPE[Áfram_vara * 128 + númer] = aðferð_frumbreyta_TYPE[fall_VALUE * 16 + númer];
        }
        ramma_INDEX = Áfram_vara; ramma_aðferð[ramma_INDEX] = fall_VALUE; ramma_staða[ramma_INDEX] = aðferð_Opna[fall_VALUE]; ramma_bunki[ramma_INDEX] = 0;
    }
    static void skila_mæld_stærð(int TYPE_VALUE) {
        if (TYPE_VALUE != aðferð_skila[ramma_aðferð[ramma_INDEX]]) { bilun_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        ramma_INDEX--; if (ramma_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_skrá_heiti = new int[64];
    static void skrá_Stream_CALL(int eigandi_VALUE, int Heiti, int snið_VALUE, int Skipun) {
        boolean úttak = Word_SMS(eigandi_VALUE, "java/io/FileOutputStream");
        int 종류 = úttak ? 6 : 5;
        if (Skipun == 183 && Word_SMS(Heiti, "<init>")) {
            boolean 이어 = false;
            if (úttak && Word_SMS(snið_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(snið_VALUE, "(Ljava/lang/String;)V")) { bilun_VALUE("unsupported file stream constructor"); return; }
            int skrá_færsla_heiti = 빼기(2), Stream_VALUE = 빼기(2);
            if (!hlutur_VALUE(skrá_færsla_heiti, 1) || !hlutur_VALUE(Stream_VALUE, 종류) || Villa) return;
            if (힙[Stream_VALUE + 3] != 0) { bilun_VALUE("file stream already initialized"); return; }
            int lengd_VALUE = 힙[skrá_færsla_heiti + 1];
            if (lengd_VALUE < 1 || lengd_VALUE > 63) { bilun_VALUE("invalid file name length"); return; }
            for (int rauf_færsla = 0; rauf_færsla < lengd_VALUE; rauf_færsla++) {
                int VALUE = 힙[skrá_færsla_heiti + 2 + rauf_færsla];
                if (VALUE < 1 || VALUE > 127) { bilun_VALUE("file stream paths currently require ASCII"); return; }
                Stream_skrá_heiti[rauf_færsla] = VALUE;
            }
            Stream_skrá_heiti[lengd_VALUE] = 0;
            int 서술자 = notandi.파일서술자열기(Stream_skrá_heiti, úttak ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { bilun_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Skipun != 182) { bilun_VALUE("invalid file stream invocation"); return; }
        int Aðgerð = -1, VALUE = 0;
        if (Word_SMS(Heiti, "close") && Word_SMS(snið_VALUE, "()V")) Aðgerð = 0;
        if (!úttak && Word_SMS(Heiti, "read") && Word_SMS(snið_VALUE, "()I")) Aðgerð = 1;
        if (úttak && Word_SMS(Heiti, "write") && Word_SMS(snið_VALUE, "(I)V")) { Aðgerð = 2; VALUE = 빼기(1); }
        if (Aðgerð < 0) { bilun_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!hlutur_VALUE(Stream_VALUE, 종류) || Villa) return;
        if (힙[Stream_VALUE + 3] == 0) { bilun_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Aðgerð == 0) {
            if (서술자 >= 0 && notandi.파일서술자닫기(서술자) < 0) bilun_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { bilun_VALUE("IOException: stream closed"); return; }
        if (Aðgerð == 1) {
            int NIÐURSTAÐA = notandi.파일한바이트읽기(서술자);
            if (NIÐURSTAÐA < -1) bilun_VALUE("IOException: read failed"); else 넣기(NIÐURSTAÐA, 1);
        } else if (notandi.파일한바이트쓰기(서술자, VALUE) != 1) bilun_VALUE("IOException: write failed");
    }
    static void CALL_aðferð(int INDEX, int Skipun) {
        if (!athuga_fasti(INDEX, 10)) return;
        int eigandi_VALUE = klasi_heiti_SMS(상가[INDEX]), Heiti = tilvísun_heiti(fasti_SECOND_VALUE[INDEX]), snið_VALUE = tilvísun_TYPE(fasti_SECOND_VALUE[INDEX]);
        if (Villa) return;
        if (samsvörun_Word(eigandi_VALUE, klasi_heiti)) {
            if (Skipun != 184) { bilun_VALUE("only static user methods are supported"); return; }
            for (int númer = 0; númer < aðferð_COUNT; númer++) if (samsvörun_Word(Heiti, aðferð_heiti_SMS[númer]) && samsvörun_Word(snið_VALUE, aðferð_TYPE[númer])) {
                if ((aðferð_aðgangur[númer] & 8) == 0) bilun_VALUE("method is not static"); else 호출(númer);
                return;
            }
            bilun_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(eigandi_VALUE, "java/io/FileInputStream") || Word_SMS(eigandi_VALUE, "java/io/FileOutputStream")) {
            skrá_Stream_CALL(eigandi_VALUE, Heiti, snið_VALUE, Skipun); return;
        }
        if (Skipun == 184 && Word_SMS(eigandi_VALUE, "java/lang/Integer") && Word_SMS(Heiti, "parseInt") && Word_SMS(snið_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Skipun == 182 && Word_SMS(eigandi_VALUE, "java/io/PrintStream") && (Word_SMS(Heiti, "println") || Word_SMS(Heiti, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(snið_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(snið_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(snið_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(snið_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(snið_VALUE, "()V") || !Word_SMS(Heiti, "println")) bilun_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) bilun_VALUE("invalid PrintStream receiver");
            if (Villa) return;
            if (TYPE_VALUE == 1) 자바도구.skrifa_númer(VALUE);
            if (TYPE_VALUE == 2) notandi.Skrift(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) notandi.skrifa_stafur_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) skrifa_SMS(VALUE);
            if (Word_SMS(Heiti, "println")) notandi.skrifa_stafur_VALUE(10);
            return;
        }
        if (Skipun == 182 && Word_SMS(eigandi_VALUE, "java/lang/String")) {
            if (Word_SMS(Heiti, "length") && Word_SMS(snið_VALUE, "()I")) {
                int tilvísun = 빼기(2); if (hlutur_VALUE(tilvísun, 1)) 넣기(힙[tilvísun + 1], 1); return;
            }
            if (Word_SMS(Heiti, "charAt") && Word_SMS(snið_VALUE, "(I)C")) {
                int hnéletur_VALUE = 빼기(1), tilvísun = 빼기(2);
                if (hlutur_VALUE(tilvísun, 1)) {
                    if (hnéletur_VALUE < 0 || hnéletur_VALUE >= 힙[tilvísun + 1]) bilun_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[tilvísun + 2 + hnéletur_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(eigandi_VALUE, "java/lang/StringBuilder")) {
            if (Skipun == 183 && Word_SMS(Heiti, "<init>") && Word_SMS(snið_VALUE, "()V")) { hlutur_VALUE(빼기(2), 4); return; }
            if (Skipun == 182 && Word_SMS(Heiti, "toString") && Word_SMS(snið_VALUE, "()Ljava/lang/String;")) {
                int tilvísun = 빼기(2); if (hlutur_VALUE(tilvísun, 4)) 넣기(힙[tilvísun + 2] == 0 ? hýsa_stafur("") : 힙[tilvísun + 2], 2); return;
            }
            if (Skipun == 182 && Word_SMS(Heiti, "append")) {
                int Texti = 0;
                if (Word_SMS(snið_VALUE, "(I)Ljava/lang/StringBuilder;")) Texti = tölustafur_stafur(빼기(1));
                else if (Word_SMS(snið_VALUE, "(Z)Ljava/lang/StringBuilder;")) Texti = hýsa_stafur(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(snið_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Texti = úthluta_geymsla(1, 1); if (!Villa) 힙[Texti + 2] = VALUE & 65535;
                }
                else if (Word_SMS(snið_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Texti = 빼기(2); if (Texti == 0) Texti = hýsa_stafur("null"); }
                else { bilun_VALUE("unsupported StringBuilder append"); return; }
                int tilvísun = 빼기(2); if (!hlutur_VALUE(tilvísun, 4) || !hlutur_VALUE(Texti, 1)) return;
                int myndavél_að_framan_VALUE = 힙[tilvísun + 2], myndavél_að_framan_VALUE_lengd = myndavél_að_framan_VALUE == 0 ? 0 : 힙[myndavél_að_framan_VALUE + 1], TIL_BAKA_VALUE_lengd = 힙[Texti + 1];
                int 새글 = úthluta_geymsla(1, myndavél_að_framan_VALUE_lengd + TIL_BAKA_VALUE_lengd); if (Villa) return;
                for (int númer = 0; númer < myndavél_að_framan_VALUE_lengd; númer++) 힙[새글 + 2 + númer] = 힙[myndavél_að_framan_VALUE + 2 + númer];
                for (int númer = 0; númer < TIL_BAKA_VALUE_lengd; númer++) 힙[새글 + 2 + myndavél_að_framan_VALUE_lengd + númer] = 힙[Texti + 2 + númer];
                힙[tilvísun + 2] = 새글; 넣기(tilvísun, 2); return;
            }
        }
        bilun_VALUE("unsupported library method");
    }
    static int ARRAY_rauf(int tilvísun, int hnéletur_VALUE, int TYPE_VALUE) {
        if (!hlutur_VALUE(tilvísun, TYPE_VALUE)) return 0;
        if (hnéletur_VALUE < 0 || hnéletur_VALUE >= 힙[tilvísun + 1]) { bilun_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return tilvísun + 2 + hnéletur_VALUE;
    }
    static void keyra_skipun() {
        int 남음 = 500000;
        while (ramma_INDEX >= 0 && !Villa) {
            if (--남음 == 0) { bilun_VALUE("instruction limit (500000)"); break; }
            int Keyra_2 = ramma_staða[ramma_INDEX], VALUE = 명바();
            if (Villa) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int númer = VALUE == 18 ? 명바() : 명짧();
                if (númer <= 0 || númer >= fasti_COUNT) bilun_VALUE("invalid ldc constant");
                else if (fasti_merki[númer] == 3) 넣기(상가[númer], 1);
                else if (fasti_merki[númer] == 8) 넣기(fasti_SMS(상가[númer]), 2);
                else bilun_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { skrifa_staðbundið(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { skrifa_staðbundið(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { skrifa_staðbundið(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int hnéletur_VALUE = 빼기(1), tilvísun = 빼기(2), rauf_færsla = ARRAY_rauf(tilvísun, hnéletur_VALUE, VALUE == 46 ? 2 : 3);
                if (!Villa) 넣기(힙[rauf_færsla], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int vara_eining = 빼기(VALUE == 79 ? 1 : 2), hnéletur_VALUE = 빼기(1), tilvísun = 빼기(2), rauf_færsla = ARRAY_rauf(tilvísun, hnéletur_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && vara_eining != 0) hlutur_VALUE(vara_eining, 1);
                if (!Villa) 힙[rauf_færsla] = vara_eining; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = skila_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = skila_TYPE, 나 = 빼기(0), 나형 = skila_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), NIÐURSTAÐA = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { bilun_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) NIÐURSTAÐA = 가 + 나;
                if (VALUE == 100) NIÐURSTAÐA = 가 - 나;
                if (VALUE == 104) NIÐURSTAÐA = 가 * 나;
                if (VALUE == 108) NIÐURSTAÐA = 가 / 나;
                if (VALUE == 112) NIÐURSTAÐA = 가 % 나;
                if (VALUE == 120) NIÐURSTAÐA = 가 << 나;
                if (VALUE == 122) NIÐURSTAÐA = 가 >> 나;
                if (VALUE == 124) NIÐURSTAÐA = 가 >>> 나;
                if (VALUE == 126) NIÐURSTAÐA = 가 & 나;
                if (VALUE == 128) NIÐURSTAÐA = 가 | 나;
                if (VALUE == 130) NIÐURSTAÐA = 가 ^ 나;
                넣기(NIÐURSTAÐA, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int staðbundið_umfang = 명바(), 증분 = (byte)명바(); 지역읽기(staðbundið_umfang, 1); 넣기(빼기(1) + 증분, 1); skrifa_staðbundið(staðbundið_umfang, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int númer = 빼기(1); 넣기(VALUE == 145 ? (byte)númer : VALUE == 146 ? (char)númer : (short)númer, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int endastaður_VALUE = Keyra_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int númer = 빼기(1); 갈까 = VALUE == 153 ? númer == 0 : VALUE == 154 ? númer != 0 : VALUE == 155 ? númer < 0 : VALUE == 156 ? númer >= 0 : VALUE == 157 ? númer > 0 : númer <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int númer = 빼기(2); 갈까 = VALUE == 198 ? númer == 0 : númer != 0; }
                if (갈까) færa_VALUE(endastaður_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { skila_mæld_stærð(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int númer = 명짧(); if (!athuga_fasti(númer, 9)) continue;
                if (!Word_SMS(klasi_heiti_SMS(상가[númer]), "java/lang/System") || !Word_SMS(tilvísun_heiti(fasti_SECOND_VALUE[númer]), "out")
                    || !Word_SMS(tilvísun_TYPE(fasti_SECOND_VALUE[númer]), "Ljava/io/PrintStream;")) bilun_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_aðferð(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Heiti = klasi_heiti_SMS(명짧());
                if (Word_SMS(Heiti, "java/lang/StringBuilder")) 넣기(úthluta_geymsla(4, 1), 2);
                else if (Word_SMS(Heiti, "java/io/FileInputStream") || Word_SMS(Heiti, "java/io/FileOutputStream")) {
                    int tilvísun = úthluta_geymsla(Word_SMS(Heiti, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Villa) { 힙[tilvísun + 2] = -1; 넣기(tilvísun, 2); }
                } else bilun_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) bilun_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(klasi_heiti_SMS(명짧()), "java/lang/String")) bilun_VALUE("only String[] anewarray is supported");
                int lengd_VALUE = 빼기(1); 넣기(úthluta_geymsla(VALUE == 188 ? 2 : 3, lengd_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int tilvísun = 빼기(2);
                if (tilvísun < 1 || tilvísun >= 힙끝 - 1 || (힙[tilvísun] != 2 && 힙[tilvísun] != 3)) bilun_VALUE("null or invalid array");
                else 넣기(힙[tilvísun + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Heiti = klasi_heiti_SMS(명짧()), tilvísun = 빼기(2);
                if (!Word_SMS(Heiti, "java/lang/String")) bilun_VALUE("unsupported checkcast");
                else if (tilvísun != 0) hlutur_VALUE(tilvísun, 1);
                넣기(tilvísun, 2); continue;
            }
            bilun_VALUE("unsupported bytecode");
        }
    }
    public static int Keyra_2() {
        if (notandi.인수개수() == 1 && 자바도구.같음(notandi.Viðföng(0), "-version")) {
            notandi.Skrift("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (notandi.인수개수() < 1) { notandi.Skrift("Usage: java CLASS [ARGS]\n"); return 2; }
        int lengd_VALUE = 자바도구.Heiti(skrá_heiti_SMS, notandi.Viðföng(0));
        if (lengd_VALUE < 1 || lengd_VALUE > 57) { notandi.Skrift("java: invalid class name\n"); return 2; }
        skrá_heiti_SMS[lengd_VALUE] = '.'; skrá_heiti_SMS[lengd_VALUE + 1] = 'c'; skrá_heiti_SMS[lengd_VALUE + 2] = 'l'; skrá_heiti_SMS[lengd_VALUE + 3] = 'a'; skrá_heiti_SMS[lengd_VALUE + 4] = 's'; skrá_heiti_SMS[lengd_VALUE + 5] = 's';
        Stærð = notandi.파일읽기(skrá_heiti_SMS, Skrá);
        if (Stærð < 0) { notandi.Skrift("java: cannot read class: "); 자바도구.skrifa_númer(Stærð); notandi.skrifa_stafur_VALUE(10); return 1; }
        클래스읽기(); if (Villa) return 1;
        int stafur_heiti = fasti_SMS(klasi_heiti);
        if (!Villa && 힙[stafur_heiti + 1] != lengd_VALUE) bilun_VALUE("class name does not match file");
        for (int númer = 0; númer < lengd_VALUE && !Villa; númer++) if (힙[stafur_heiti + 2 + númer] != skrá_heiti_SMS[númer]) bilun_VALUE("class name does not match file");
        int færsla_P_VALUE = -1;
        for (int númer = 0; númer < aðferð_COUNT; númer++) if (Word_SMS(aðferð_heiti_SMS[númer], "main") && Word_SMS(aðferð_TYPE[númer], "([Ljava/lang/String;)V") && (aðferð_aðgangur[númer] & 9) == 9) færsla_P_VALUE = númer;
        if (færsla_P_VALUE < 0) bilun_VALUE("public static void main(String[] args) required");
        if (Villa) return 1;
        int Viðföng = úthluta_geymsla(3, notandi.인수개수() - 1);
        for (int númer = 1; númer < notandi.인수개수() && !Villa; númer++) 힙[Viðföng + 1 + númer] = hýsa_stafur(notandi.Viðföng(númer));
        ramma_INDEX = 0; ramma_aðferð[0] = færsla_P_VALUE; ramma_staða[0] = aðferð_Opna[færsla_P_VALUE]; staðbundið_VALUE[0] = Viðföng; staðbundið_TYPE[0] = 2;
        keyra_skipun(); return Villa ? 1 : 0;
    }
}
