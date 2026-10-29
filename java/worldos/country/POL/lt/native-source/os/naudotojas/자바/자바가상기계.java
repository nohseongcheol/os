// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Failas/operandas_eilė/nuoroda/šaka 경계를 Vykdyti_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Failas = new int[16384], failo_vardas_SMS = new int[64];
    static int[] konstanta_žyma = new int[512], 상가 = new int[512], konstanta_SECOND_VALUE = new int[512], eilutė_nuoroda = new int[512];
    static int[] metodas_pavadinimas_SMS = new int[32], metodas_TYPE = new int[32], metodas_prieiga = new int[32];
    static int[] metodas_Start = new int[32], metodas_baigti_pokalbį = new int[32], metodas_eilė = new int[32], 함수지역 = new int[32];
    static int[] metodas_argumentas_COUNT = new int[32], metodas_argumentas_TYPE = new int[512], metodas_grąžinti = new int[32];
    static int[] 경계 = new int[16384];
    static int[] vietinis_VALUE = new int[4096], vietinis_TYPE = new int[4096], operandas_eilė_VALUE = new int[4096], operandas_eilė_TYPE = new int[4096];
    static int[] kadras_metodas = new int[32], kadras_padėtis = new int[32], kadras_eilė = new int[32];
    static int[] 힙 = new int[8192];
    static int Dydis, 읽기위치, konstanta_COUNT, metodas_COUNT, klasės_pavadinimas, kadras_INDEX = -1, 힙끝 = 1, grąžinti_TYPE;
    static boolean KLAIDA;

    static void triktis_VALUE(String Word_SMS) {
        if (!KLAIDA) { naudotojas.Rašymas("JVM error: "); naudotojas.Rašymas(Word_SMS); naudotojas.rašymas_simbolis_VALUE(10); }
        KLAIDA = true;
    }
    static boolean klipas(int Paleisti, int 길이) { return Paleisti >= 0 && 길이 >= 0 && Paleisti <= Dydis - 길이; }
    static int baitas_VALUE() {
        if (!klipas(읽기위치, 1)) { triktis_VALUE("truncated class file"); return 0; }
        return Failas[읽기위치++];
    }
    static int 짧은수() { return baitas_VALUE() << 8 | baitas_VALUE(); }
    static int sveikasis_skaičius() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klipas(읽기위치, 길이)) triktis_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean čekis_konstanta(int numeris, int 종류) {
        if (numeris <= 0 || numeris >= konstanta_COUNT || konstanta_žyma[numeris] != 종류) { triktis_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_diapazonas(int Paleisti, int 길이, String Word_SMS) {
        if (!klipas(Paleisti, 길이) || 길이 != Word_SMS.length()) return false;
        for (int numeris = 0; numeris < 길이; numeris++) if (Failas[Paleisti + numeris] != Word_SMS.charAt(numeris)) return false;
        return true;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return čekis_konstanta(konstanta_VALUE, 1) && SMS_diapazonas(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operandas) {
        if (!čekis_konstanta(가, 1) || !čekis_konstanta(SECOND_operandas, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operandas]) return false;
        for (int numeris = 0; numeris < konstanta_SECOND_VALUE[가]; numeris++) if (Failas[상가[가] + numeris] != Failas[상가[SECOND_operandas] + numeris]) return false;
        return true;
    }
    static int klasės_pavadinimas_SMS(int numeris) { return čekis_konstanta(numeris, 7) && čekis_konstanta(상가[numeris], 1) ? 상가[numeris] : 0; }
    static int nuoroda_pavadinimas(int numeris) { return čekis_konstanta(numeris, 12) && čekis_konstanta(상가[numeris], 1) ? 상가[numeris] : 0; }
    static int nuoroda_TYPE(int numeris) { return čekis_konstanta(numeris, 12) && čekis_konstanta(konstanta_SECOND_VALUE[numeris], 1) ? konstanta_SECOND_VALUE[numeris] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { triktis_VALUE("invalid descriptor"); return 0; }
        int VALUE = baitas_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Paleisti = 읽기위치;
            while (읽기위치 < 끝 && Failas[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Paleisti) triktis_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        triktis_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, numeris = metodas_TYPE[FUNCTION_VALUE];
        if (!čekis_konstanta(numeris, 1)) return;
        읽기위치 = 상가[numeris]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[numeris];
        if (baitas_VALUE() != '(') triktis_VALUE("invalid method descriptor");
        int prekė_COUNT = 0;
        while (!KLAIDA && 읽기위치 < 끝 && Failas[읽기위치] != ')') {
            if (prekė_COUNT == 16) { triktis_VALUE("too many method arguments"); break; }
            metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + prekė_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || baitas_VALUE() != ')') triktis_VALUE("invalid method descriptor");
        metodas_grąžinti[FUNCTION_VALUE] = 서술형(끝, true); metodas_argumentas_COUNT[FUNCTION_VALUE] = prekė_COUNT;
        if (읽기위치 != 끝) triktis_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int prekė_COUNT = 짧은수();
        for (int numeris = 0; numeris < prekė_COUNT && !KLAIDA; numeris++) { čekis_konstanta(짧은수(), 1); 건너(sveikasis_skaičius()); }
    }
    static int 명령길이(int VALUE) {
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
        if (sveikasis_skaičius() != 0xcafebabe) triktis_VALUE("not a class file");
        int 부판 = 짧은수(), versija_VALUE = 짧은수();
        if (versija_VALUE < 45 || versija_VALUE > 52 || 부판 != 0) triktis_VALUE("supported class versions: 45..52, minor 0");
        konstanta_COUNT = 짧은수();
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { triktis_VALUE("constant pool limit (511)"); return; }
        for (int numeris = 1; numeris < konstanta_COUNT && !KLAIDA; numeris++) {
            int 종류 = baitas_VALUE(); konstanta_žyma[numeris] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[numeris] = 짧은수(); 상가[numeris] = 읽기위치; 건너(konstanta_SECOND_VALUE[numeris]); }
            else if (종류 == 3) 상가[numeris] = sveikasis_skaičius();
            else if (종류 == 7 || 종류 == 8) 상가[numeris] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[numeris] = 짧은수(); konstanta_SECOND_VALUE[numeris] = 짧은수(); }
            else triktis_VALUE("unsupported constant type");
        }
        int teisė_VALUE = 짧은수();
        if ((teisė_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) triktis_VALUE("unsupported class flags");
        klasės_pavadinimas = klasės_pavadinimas_SMS(짧은수());
        if (!Word_SMS(klasės_pavadinimas_SMS(짧은수()), "java/lang/Object")) triktis_VALUE("inheritance unsupported");
        if (짧은수() != 0) triktis_VALUE("interfaces unsupported");
        if (짧은수() != 0) triktis_VALUE("fields unsupported");
        metodas_COUNT = 짧은수();
        if (metodas_COUNT < 1 || metodas_COUNT > 32) { triktis_VALUE("method count limit (32)"); return; }
        for (int numeris = 0; numeris < metodas_COUNT && !KLAIDA; numeris++) {
            metodas_prieiga[numeris] = 짧은수(); metodas_pavadinimas_SMS[numeris] = 짧은수(); metodas_TYPE[numeris] = 짧은수();
            čekis_konstanta(metodas_pavadinimas_SMS[numeris], 1); 서술읽기(numeris);
            if ((metodas_prieiga[numeris] & (0x100 | 0x400 | 0x20)) != 0) triktis_VALUE("native, abstract and synchronized methods unsupported");
            if ((metodas_prieiga[numeris] & 8) == 0 && !Word_SMS(metodas_pavadinimas_SMS[numeris], "<init>")) triktis_VALUE("instance methods unsupported");
            if (Word_SMS(metodas_pavadinimas_SMS[numeris], "<clinit>")) triktis_VALUE("class initializers unsupported");
            for (int priekinis_VALUE = 0; priekinis_VALUE < numeris; priekinis_VALUE++) if (같은말(metodas_pavadinimas_SMS[priekinis_VALUE], metodas_pavadinimas_SMS[numeris]) && 같은말(metodas_TYPE[priekinis_VALUE], metodas_TYPE[numeris])) triktis_VALUE("duplicate method");
            int prekė_COUNT = 짧은수();
            for (int atributas_VALUE = 0; atributas_VALUE < prekė_COUNT && !KLAIDA; atributas_VALUE++) {
                int Pavadinimas_2 = 짧은수(), 길이 = sveikasis_skaičius(), Paleisti = 읽기위치;
                if (!klipas(Paleisti, 길이)) { triktis_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Pavadinimas_2, "Code")) {
                    if (metodas_Start[numeris] != 0) triktis_VALUE("duplicate Code attribute");
                    metodas_eilė[numeris] = 짧은수(); 함수지역[numeris] = 짧은수(); int 코드길이 = sveikasis_skaičius();
                    if (metodas_eilė[numeris] > 128 || 함수지역[numeris] > 128 || 함수지역[numeris] < metodas_argumentas_COUNT[numeris]
                        || 코드길이 < 1 || 코드길이 > 8192) triktis_VALUE("method memory limits exceeded");
                    metodas_Start[numeris] = 읽기위치; 건너(코드길이); metodas_baigti_pokalbį[numeris] = 읽기위치;
                    if (짧은수() != 0) triktis_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Paleisti + 길이) triktis_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if (metodas_Start[numeris] == 0) triktis_VALUE("missing Code attribute");
            int 칸 = metodas_Start[numeris];
            while (칸 < metodas_baigti_pokalbį[numeris] && !KLAIDA) {
                int 길이 = 명령길이(Failas[칸]);
                if (길이 == 0 || 길이 > metodas_baigti_pokalbį[numeris] - 칸) { triktis_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = numeris + 1; 칸 += 길이;
            }
            // 실행하지 않는 경로에도 잘못된 šaka 목적지를 허용하지 않는다.
            칸 = metodas_Start[numeris];
            while (칸 < metodas_baigti_pokalbį[numeris] && !KLAIDA) {
                int VALUE = Failas[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int vieta_VALUE = 칸 + (short)(Failas[칸 + 1] << 8 | Failas[칸 + 2]);
                    if (vieta_VALUE < metodas_Start[numeris] || vieta_VALUE >= metodas_baigti_pokalbį[numeris] || 경계[vieta_VALUE] != numeris + 1) triktis_VALUE("invalid branch target");
                }
                칸 += 명령길이(VALUE);
            }
        }
        if (!KLAIDA) 속성건너();
        if (읽기위치 != Dydis) triktis_VALUE("extra class file data");
    }
    static int priskirti_Saugykla(int 종류, int 길이) {
        if (길이 < 0 || 길이 > 힙.length - 힙끝 - 2) { triktis_VALUE("object heap exhausted or negative array size"); return 0; }
        int nuoroda = 힙끝; 힙끝 += 길이 + 2; 힙[nuoroda] = 종류; 힙[nuoroda + 1] = 길이;
        return nuoroda;
    }
    static boolean objektas_VALUE(int nuoroda, int 종류) {
        if (nuoroda < 1 || nuoroda >= 힙끝 - 1 || 힙[nuoroda] != 종류) { triktis_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!čekis_konstanta(INDEX, 1)) return 0;
        if (eilutė_nuoroda[INDEX] != 0) return eilutė_nuoroda[INDEX];
        int nuoroda = priskirti_Saugykla(1, konstanta_SECOND_VALUE[INDEX]); if (KLAIDA) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], numeris = 상가[INDEX], 길이 = 0;
        while (numeris < 끝 && !KLAIDA) {
            int VALUE = Failas[numeris++];
            if (VALUE == 0) triktis_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && numeris < 끝) {
                int toliau_prekė = Failas[numeris++];
                if ((toliau_prekė & 192) != 128) triktis_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | toliau_prekė & 63;
                if (VALUE != 0 && VALUE < 128) triktis_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && numeris + 1 < 끝) {
                int 가 = Failas[numeris++], SECOND_operandas = Failas[numeris++];
                if ((가 & 192) != 128 || (SECOND_operandas & 192) != 128) triktis_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operandas & 63;
                if (VALUE < 2048) triktis_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) triktis_VALUE("invalid modified UTF-8");
            힙[nuoroda + 2 + 길이++] = VALUE;
        }
        힙[nuoroda + 1] = 길이; eilutė_nuoroda[INDEX] = nuoroda; return nuoroda;
    }
    static int organizuoti_simbolis(String VALUE) {
        int nuoroda = priskirti_Saugykla(1, VALUE.length()); if (KLAIDA) return 0;
        for (int numeris = 0; numeris < VALUE.length(); numeris++) 힙[nuoroda + 2 + numeris] = VALUE.charAt(numeris);
        return nuoroda;
    }
    static void rašymas_SMS(int nuoroda) {
        if (nuoroda == 0) { naudotojas.Rašymas("null"); return; }
        if (!objektas_VALUE(nuoroda, 1)) return;
        for (int numeris = 0; numeris < 힙[nuoroda + 1]; numeris++) naudotojas.rašymas_simbolis_VALUE(힙[nuoroda + 2 + numeris]);
    }
    static int skaitmuo_simbolis(int VALUE) {
        int nuoroda = priskirti_Saugykla(1, 11); if (KLAIDA) return 0;
        int 길이 = 0;
        if (VALUE < 0) 힙[nuoroda + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int vietos_rodyklė = 1000000000; boolean Paleisti = false;
        while (vietos_rodyklė != 0) {
            int numeris = -(VALUE / vietos_rodyklė);
            if (numeris != 0 || Paleisti || vietos_rodyklė == 1) { 힙[nuoroda + 2 + 길이++] = '0' + numeris; Paleisti = true; }
            VALUE %= vietos_rodyklė; vietos_rodyklė /= 10;
        }
        힙[nuoroda + 1] = 길이; return nuoroda;
    }
    static int 정수해독(int nuoroda) {
        if (!objektas_VALUE(nuoroda, 1)) return 0;
        int 길이 = 힙[nuoroda + 1], numeris = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[nuoroda + 2] == '-' || 힙[nuoroda + 2] == '+')) { 음수 = 힙[nuoroda + 2] == '-'; numeris++; }
        if (numeris == 길이) triktis_VALUE("NumberFormatException");
        for (; numeris < 길이 && !KLAIDA; numeris++) {
            int skaitmuo_VALUE = 힙[nuoroda + 2 + numeris] - '0';
            if (skaitmuo_VALUE < 0 || skaitmuo_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && skaitmuo_VALUE > (음수 ? 8 : 7)) triktis_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - skaitmuo_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (KLAIDA) return;
        if (kadras_INDEX < 0 || kadras_eilė[kadras_INDEX] >= metodas_eilė[kadras_metodas[kadras_INDEX]]) { triktis_VALUE("operand stack overflow"); return; }
        int 칸 = kadras_INDEX * 128 + kadras_eilė[kadras_INDEX]++; operandas_eilė_VALUE[칸] = VALUE; operandas_eilė_TYPE[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (KLAIDA) return 0;
        if (kadras_INDEX < 0 || kadras_eilė[kadras_INDEX] < 1) { triktis_VALUE("operand stack underflow"); return 0; }
        int 칸 = kadras_INDEX * 128 + --kadras_eilė[kadras_INDEX]; grąžinti_TYPE = operandas_eilė_TYPE[칸];
        if (TYPE_VALUE != 0 && grąžinti_TYPE != TYPE_VALUE) triktis_VALUE("operand type mismatch");
        return operandas_eilė_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadras_metodas[kadras_INDEX]] || INDEX < 0 || vietinis_TYPE[kadras_INDEX * 128 + INDEX] != TYPE_VALUE) { triktis_VALUE("invalid or uninitialized local"); return; }
        넣기(vietinis_VALUE[kadras_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void rašymas_vietinis(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadras_metodas[kadras_INDEX]] || INDEX < 0) { triktis_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); vietinis_VALUE[kadras_INDEX * 128 + INDEX] = VALUE; vietinis_TYPE[kadras_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Pozicija = kadras_padėtis[kadras_INDEX];
        if (Pozicija < metodas_Start[kadras_metodas[kadras_INDEX]] || Pozicija >= metodas_baigti_pokalbį[kadras_metodas[kadras_INDEX]]) { triktis_VALUE("instruction pointer out of range"); return 0; }
        kadras_padėtis[kadras_INDEX]++; return Failas[Pozicija];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void judėti_VALUE(int Pozicija) {
        int FUNCTION_VALUE = kadras_metodas[kadras_INDEX];
        if (Pozicija < metodas_Start[FUNCTION_VALUE] || Pozicija >= metodas_baigti_pokalbį[FUNCTION_VALUE] || 경계[Pozicija] != FUNCTION_VALUE + 1) triktis_VALUE("invalid branch target");
        else kadras_padėtis[kadras_INDEX] = Pozicija;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadras_INDEX == 31) { triktis_VALUE("call stack limit (32)"); return; }
        int toliau_prekė = kadras_INDEX + 1;
        for (int numeris = 0; numeris < 128; numeris++) vietinis_TYPE[toliau_prekė * 128 + numeris] = 0;
        for (int numeris = metodas_argumentas_COUNT[FUNCTION_VALUE] - 1; numeris >= 0; numeris--) {
            vietinis_VALUE[toliau_prekė * 128 + numeris] = 빼기(metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + numeris]); vietinis_TYPE[toliau_prekė * 128 + numeris] = metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + numeris];
        }
        kadras_INDEX = toliau_prekė; kadras_metodas[kadras_INDEX] = FUNCTION_VALUE; kadras_padėtis[kadras_INDEX] = metodas_Start[FUNCTION_VALUE]; kadras_eilė[kadras_INDEX] = 0;
    }
    static void grąžinti_KR(int TYPE_VALUE) {
        if (TYPE_VALUE != metodas_grąžinti[kadras_metodas[kadras_INDEX]]) { triktis_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        kadras_INDEX--; if (kadras_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_failo_vardas = new int[64];
    static void Failas_Stream_CALL(int savininkas_VALUE, int Pavadinimas_2, int formatas_VALUE, int Komanda) {
        boolean Išvestis = Word_SMS(savininkas_VALUE, "java/io/FileOutputStream");
        int 종류 = Išvestis ? 6 : 5;
        if (Komanda == 183 && Word_SMS(Pavadinimas_2, "<init>")) {
            boolean 이어 = false;
            if (Išvestis && Word_SMS(formatas_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formatas_VALUE, "(Ljava/lang/String;)V")) { triktis_VALUE("unsupported file stream constructor"); return; }
            int Failas_įrašas_pavadinimas = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objektas_VALUE(Failas_įrašas_pavadinimas, 1) || !objektas_VALUE(Stream_VALUE, 종류) || KLAIDA) return;
            if (힙[Stream_VALUE + 3] != 0) { triktis_VALUE("file stream already initialized"); return; }
            int 길이 = 힙[Failas_įrašas_pavadinimas + 1];
            if (길이 < 1 || 길이 > 63) { triktis_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = 힙[Failas_įrašas_pavadinimas + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { triktis_VALUE("file stream paths currently require ASCII"); return; }
                Stream_failo_vardas[칸] = VALUE;
            }
            Stream_failo_vardas[길이] = 0;
            int 서술자 = naudotojas.파일서술자열기(Stream_failo_vardas, Išvestis ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { triktis_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Komanda != 182) { triktis_VALUE("invalid file stream invocation"); return; }
        int Veiksmas = -1, VALUE = 0;
        if (Word_SMS(Pavadinimas_2, "close") && Word_SMS(formatas_VALUE, "()V")) Veiksmas = 0;
        if (!Išvestis && Word_SMS(Pavadinimas_2, "read") && Word_SMS(formatas_VALUE, "()I")) Veiksmas = 1;
        if (Išvestis && Word_SMS(Pavadinimas_2, "write") && Word_SMS(formatas_VALUE, "(I)V")) { Veiksmas = 2; VALUE = 빼기(1); }
        if (Veiksmas < 0) { triktis_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objektas_VALUE(Stream_VALUE, 종류) || KLAIDA) return;
        if (힙[Stream_VALUE + 3] == 0) { triktis_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Veiksmas == 0) {
            if (서술자 >= 0 && naudotojas.파일서술자닫기(서술자) < 0) triktis_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { triktis_VALUE("IOException: stream closed"); return; }
        if (Veiksmas == 1) {
            int REZULTATAS = naudotojas.파일한바이트읽기(서술자);
            if (REZULTATAS < -1) triktis_VALUE("IOException: read failed"); else 넣기(REZULTATAS, 1);
        } else if (naudotojas.파일한바이트쓰기(서술자, VALUE) != 1) triktis_VALUE("IOException: write failed");
    }
    static void CALL_metodas(int INDEX, int Komanda) {
        if (!čekis_konstanta(INDEX, 10)) return;
        int savininkas_VALUE = klasės_pavadinimas_SMS(상가[INDEX]), Pavadinimas_2 = nuoroda_pavadinimas(konstanta_SECOND_VALUE[INDEX]), formatas_VALUE = nuoroda_TYPE(konstanta_SECOND_VALUE[INDEX]);
        if (KLAIDA) return;
        if (같은말(savininkas_VALUE, klasės_pavadinimas)) {
            if (Komanda != 184) { triktis_VALUE("only static user methods are supported"); return; }
            for (int numeris = 0; numeris < metodas_COUNT; numeris++) if (같은말(Pavadinimas_2, metodas_pavadinimas_SMS[numeris]) && 같은말(formatas_VALUE, metodas_TYPE[numeris])) {
                if ((metodas_prieiga[numeris] & 8) == 0) triktis_VALUE("method is not static"); else 호출(numeris);
                return;
            }
            triktis_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(savininkas_VALUE, "java/io/FileInputStream") || Word_SMS(savininkas_VALUE, "java/io/FileOutputStream")) {
            Failas_Stream_CALL(savininkas_VALUE, Pavadinimas_2, formatas_VALUE, Komanda); return;
        }
        if (Komanda == 184 && Word_SMS(savininkas_VALUE, "java/lang/Integer") && Word_SMS(Pavadinimas_2, "parseInt") && Word_SMS(formatas_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Komanda == 182 && Word_SMS(savininkas_VALUE, "java/io/PrintStream") && (Word_SMS(Pavadinimas_2, "println") || Word_SMS(Pavadinimas_2, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(formatas_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(formatas_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(formatas_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(formatas_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(formatas_VALUE, "()V") || !Word_SMS(Pavadinimas_2, "println")) triktis_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) triktis_VALUE("invalid PrintStream receiver");
            if (KLAIDA) return;
            if (TYPE_VALUE == 1) 자바도구.rašymas_numeris(VALUE);
            if (TYPE_VALUE == 2) naudotojas.Rašymas(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) naudotojas.rašymas_simbolis_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) rašymas_SMS(VALUE);
            if (Word_SMS(Pavadinimas_2, "println")) naudotojas.rašymas_simbolis_VALUE(10);
            return;
        }
        if (Komanda == 182 && Word_SMS(savininkas_VALUE, "java/lang/String")) {
            if (Word_SMS(Pavadinimas_2, "length") && Word_SMS(formatas_VALUE, "()I")) {
                int nuoroda = 빼기(2); if (objektas_VALUE(nuoroda, 1)) 넣기(힙[nuoroda + 1], 1); return;
            }
            if (Word_SMS(Pavadinimas_2, "charAt") && Word_SMS(formatas_VALUE, "(I)C")) {
                int apatinis_indeksas_VALUE = 빼기(1), nuoroda = 빼기(2);
                if (objektas_VALUE(nuoroda, 1)) {
                    if (apatinis_indeksas_VALUE < 0 || apatinis_indeksas_VALUE >= 힙[nuoroda + 1]) triktis_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[nuoroda + 2 + apatinis_indeksas_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(savininkas_VALUE, "java/lang/StringBuilder")) {
            if (Komanda == 183 && Word_SMS(Pavadinimas_2, "<init>") && Word_SMS(formatas_VALUE, "()V")) { objektas_VALUE(빼기(2), 4); return; }
            if (Komanda == 182 && Word_SMS(Pavadinimas_2, "toString") && Word_SMS(formatas_VALUE, "()Ljava/lang/String;")) {
                int nuoroda = 빼기(2); if (objektas_VALUE(nuoroda, 4)) 넣기(힙[nuoroda + 2] == 0 ? organizuoti_simbolis("") : 힙[nuoroda + 2], 2); return;
            }
            if (Komanda == 182 && Word_SMS(Pavadinimas_2, "append")) {
                int Tekstas = 0;
                if (Word_SMS(formatas_VALUE, "(I)Ljava/lang/StringBuilder;")) Tekstas = skaitmuo_simbolis(빼기(1));
                else if (Word_SMS(formatas_VALUE, "(Z)Ljava/lang/StringBuilder;")) Tekstas = organizuoti_simbolis(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formatas_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Tekstas = priskirti_Saugykla(1, 1); if (!KLAIDA) 힙[Tekstas + 2] = VALUE & 65535;
                }
                else if (Word_SMS(formatas_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekstas = 빼기(2); if (Tekstas == 0) Tekstas = organizuoti_simbolis("null"); }
                else { triktis_VALUE("unsupported StringBuilder append"); return; }
                int nuoroda = 빼기(2); if (!objektas_VALUE(nuoroda, 4) || !objektas_VALUE(Tekstas, 1)) return;
                int priekinis_VALUE = 힙[nuoroda + 2], 앞길이 = priekinis_VALUE == 0 ? 0 : 힙[priekinis_VALUE + 1], 뒤길이 = 힙[Tekstas + 1];
                int 새글 = priskirti_Saugykla(1, 앞길이 + 뒤길이); if (KLAIDA) return;
                for (int numeris = 0; numeris < 앞길이; numeris++) 힙[새글 + 2 + numeris] = 힙[priekinis_VALUE + 2 + numeris];
                for (int numeris = 0; numeris < 뒤길이; numeris++) 힙[새글 + 2 + 앞길이 + numeris] = 힙[Tekstas + 2 + numeris];
                힙[nuoroda + 2] = 새글; 넣기(nuoroda, 2); return;
            }
        }
        triktis_VALUE("unsupported library method");
    }
    static int 배열칸(int nuoroda, int apatinis_indeksas_VALUE, int TYPE_VALUE) {
        if (!objektas_VALUE(nuoroda, TYPE_VALUE)) return 0;
        if (apatinis_indeksas_VALUE < 0 || apatinis_indeksas_VALUE >= 힙[nuoroda + 1]) { triktis_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return nuoroda + 2 + apatinis_indeksas_VALUE;
    }
    static void Vykdyti_komanda() {
        int 남음 = 500000;
        while (kadras_INDEX >= 0 && !KLAIDA) {
            if (--남음 == 0) { triktis_VALUE("instruction limit (500000)"); break; }
            int Paleisti = kadras_padėtis[kadras_INDEX], VALUE = 명바();
            if (KLAIDA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int numeris = VALUE == 18 ? 명바() : 명짧();
                if (numeris <= 0 || numeris >= konstanta_COUNT) triktis_VALUE("invalid ldc constant");
                else if (konstanta_žyma[numeris] == 3) 넣기(상가[numeris], 1);
                else if (konstanta_žyma[numeris] == 8) 넣기(konstanta_SMS(상가[numeris]), 2);
                else triktis_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { rašymas_vietinis(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { rašymas_vietinis(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { rašymas_vietinis(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int apatinis_indeksas_VALUE = 빼기(1), nuoroda = 빼기(2), 칸 = 배열칸(nuoroda, apatinis_indeksas_VALUE, VALUE == 46 ? 2 : 3);
                if (!KLAIDA) 넣기(힙[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int prekė_elementas = 빼기(VALUE == 79 ? 1 : 2), apatinis_indeksas_VALUE = 빼기(1), nuoroda = 빼기(2), 칸 = 배열칸(nuoroda, apatinis_indeksas_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && prekė_elementas != 0) objektas_VALUE(prekė_elementas, 1);
                if (!KLAIDA) 힙[칸] = prekė_elementas; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = grąžinti_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = grąžinti_TYPE, SECOND_operandas = 빼기(0), SECOND_operandas_TYPE = grąžinti_TYPE; 넣기(가, 가형); 넣기(SECOND_operandas, SECOND_operandas_TYPE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operandas = 빼기(1), 가 = 빼기(1), REZULTATAS = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operandas == 0) { triktis_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) REZULTATAS = 가 + SECOND_operandas;
                if (VALUE == 100) REZULTATAS = 가 - SECOND_operandas;
                if (VALUE == 104) REZULTATAS = 가 * SECOND_operandas;
                if (VALUE == 108) REZULTATAS = 가 / SECOND_operandas;
                if (VALUE == 112) REZULTATAS = 가 % SECOND_operandas;
                if (VALUE == 120) REZULTATAS = 가 << SECOND_operandas;
                if (VALUE == 122) REZULTATAS = 가 >> SECOND_operandas;
                if (VALUE == 124) REZULTATAS = 가 >>> SECOND_operandas;
                if (VALUE == 126) REZULTATAS = 가 & SECOND_operandas;
                if (VALUE == 128) REZULTATAS = 가 | SECOND_operandas;
                if (VALUE == 130) REZULTATAS = 가 ^ SECOND_operandas;
                넣기(REZULTATAS, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int vietinis_Aprėptis = 명바(), padidinimas_veiksmas = (byte)명바(); 지역읽기(vietinis_Aprėptis, 1); 넣기(빼기(1) + padidinimas_veiksmas, 1); rašymas_vietinis(vietinis_Aprėptis, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int numeris = 빼기(1); 넣기(VALUE == 145 ? (byte)numeris : VALUE == 146 ? (char)numeris : (short)numeris, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int vieta_VALUE = Paleisti + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int numeris = 빼기(1); 갈까 = VALUE == 153 ? numeris == 0 : VALUE == 154 ? numeris != 0 : VALUE == 155 ? numeris < 0 : VALUE == 156 ? numeris >= 0 : VALUE == 157 ? numeris > 0 : numeris <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operandas = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operandas : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operandas : VALUE == 161 ? 가 < SECOND_operandas : VALUE == 162 ? 가 >= SECOND_operandas : VALUE == 163 ? 가 > SECOND_operandas : 가 <= SECOND_operandas;
                } else if (VALUE == 198 || VALUE == 199) { int numeris = 빼기(2); 갈까 = VALUE == 198 ? numeris == 0 : numeris != 0; }
                if (갈까) judėti_VALUE(vieta_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { grąžinti_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int numeris = 명짧(); if (!čekis_konstanta(numeris, 9)) continue;
                if (!Word_SMS(klasės_pavadinimas_SMS(상가[numeris]), "java/lang/System") || !Word_SMS(nuoroda_pavadinimas(konstanta_SECOND_VALUE[numeris]), "out")
                    || !Word_SMS(nuoroda_TYPE(konstanta_SECOND_VALUE[numeris]), "Ljava/io/PrintStream;")) triktis_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metodas(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Pavadinimas_2 = klasės_pavadinimas_SMS(명짧());
                if (Word_SMS(Pavadinimas_2, "java/lang/StringBuilder")) 넣기(priskirti_Saugykla(4, 1), 2);
                else if (Word_SMS(Pavadinimas_2, "java/io/FileInputStream") || Word_SMS(Pavadinimas_2, "java/io/FileOutputStream")) {
                    int nuoroda = priskirti_Saugykla(Word_SMS(Pavadinimas_2, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!KLAIDA) { 힙[nuoroda + 2] = -1; 넣기(nuoroda, 2); }
                } else triktis_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) triktis_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(klasės_pavadinimas_SMS(명짧()), "java/lang/String")) triktis_VALUE("only String[] anewarray is supported");
                int 길이 = 빼기(1); 넣기(priskirti_Saugykla(VALUE == 188 ? 2 : 3, 길이), 2); continue;
            }
            if (VALUE == 190) {
                int nuoroda = 빼기(2);
                if (nuoroda < 1 || nuoroda >= 힙끝 - 1 || (힙[nuoroda] != 2 && 힙[nuoroda] != 3)) triktis_VALUE("null or invalid array");
                else 넣기(힙[nuoroda + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Pavadinimas_2 = klasės_pavadinimas_SMS(명짧()), nuoroda = 빼기(2);
                if (!Word_SMS(Pavadinimas_2, "java/lang/String")) triktis_VALUE("unsupported checkcast");
                else if (nuoroda != 0) objektas_VALUE(nuoroda, 1);
                넣기(nuoroda, 2); continue;
            }
            triktis_VALUE("unsupported bytecode");
        }
    }
    public static int Paleisti() {
        if (naudotojas.인수개수() == 1 && 자바도구.같음(naudotojas.Argumentai(0), "-version")) {
            naudotojas.Rašymas("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (naudotojas.인수개수() < 1) { naudotojas.Rašymas("Usage: java CLASS [ARGS]\n"); return 2; }
        int 길이 = 자바도구.Pavadinimas_2(failo_vardas_SMS, naudotojas.Argumentai(0));
        if (길이 < 1 || 길이 > 57) { naudotojas.Rašymas("java: invalid class name\n"); return 2; }
        failo_vardas_SMS[길이] = '.'; failo_vardas_SMS[길이 + 1] = 'c'; failo_vardas_SMS[길이 + 2] = 'l'; failo_vardas_SMS[길이 + 3] = 'a'; failo_vardas_SMS[길이 + 4] = 's'; failo_vardas_SMS[길이 + 5] = 's';
        Dydis = naudotojas.파일읽기(failo_vardas_SMS, Failas);
        if (Dydis < 0) { naudotojas.Rašymas("java: cannot read class: "); 자바도구.rašymas_numeris(Dydis); naudotojas.rašymas_simbolis_VALUE(10); return 1; }
        클래스읽기(); if (KLAIDA) return 1;
        int simbolis_pavadinimas = konstanta_SMS(klasės_pavadinimas);
        if (!KLAIDA && 힙[simbolis_pavadinimas + 1] != 길이) triktis_VALUE("class name does not match file");
        for (int numeris = 0; numeris < 길이 && !KLAIDA; numeris++) if (힙[simbolis_pavadinimas + 2 + numeris] != failo_vardas_SMS[numeris]) triktis_VALUE("class name does not match file");
        int įrašas_p_VALUE = -1;
        for (int numeris = 0; numeris < metodas_COUNT; numeris++) if (Word_SMS(metodas_pavadinimas_SMS[numeris], "main") && Word_SMS(metodas_TYPE[numeris], "([Ljava/lang/String;)V") && (metodas_prieiga[numeris] & 9) == 9) įrašas_p_VALUE = numeris;
        if (įrašas_p_VALUE < 0) triktis_VALUE("public static void main(String[] args) required");
        if (KLAIDA) return 1;
        int Argumentai = priskirti_Saugykla(3, naudotojas.인수개수() - 1);
        for (int numeris = 1; numeris < naudotojas.인수개수() && !KLAIDA; numeris++) 힙[Argumentai + 1 + numeris] = organizuoti_simbolis(naudotojas.Argumentai(numeris));
        kadras_INDEX = 0; kadras_metodas[0] = įrašas_p_VALUE; kadras_padėtis[0] = metodas_Start[įrašas_p_VALUE]; vietinis_VALUE[0] = Argumentai; vietinis_TYPE[0] = 2;
        Vykdyti_komanda(); return KLAIDA ? 1 : 0;
    }
}
