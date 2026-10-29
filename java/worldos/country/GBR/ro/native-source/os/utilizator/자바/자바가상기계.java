// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fișier/operand_Teanc/referință/ramură 경계를 executa_comandă 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fișier = new int[16384], nume_de_fișier_SMS = new int[64];
    static int[] constantă_eticheta = new int[512], 상가 = new int[512], constantă_SECOND_VALUE = new int[512], șir_referință = new int[512];
    static int[] metodă_nume_SMS = new int[32], metodă_Tip = new int[32], metodă_acces = new int[32];
    static int[] metodă_buta = new int[32], metodă_termina_un_apel = new int[32], metodă_Teanc = new int[32], 함수지역 = new int[32];
    static int[] metodă_argument_COUNT = new int[32], metodă_argument_Tip = new int[512], metodă_restitui = new int[32];
    static int[] 경계 = new int[16384];
    static int[] local_VALUE = new int[4096], local_Tip = new int[4096], operand_Teanc_VALUE = new int[4096], operand_Teanc_Tip = new int[4096];
    static int[] cadru_metodă = new int[32], cadru_poziție = new int[32], cadru_Teanc = new int[32];
    static int[] 힙 = new int[8192];
    static int Mărime, 읽기위치, constantă_COUNT, metodă_COUNT, nume_de_clasă, cadru_INDEX = -1, 힙끝 = 1, restitui_Tip;
    static boolean eroare;

    static void eroare_VALUE(String Word_SMS) {
        if (!eroare) { utilizator.Scriere("JVM error: "); utilizator.Scriere(Word_SMS); utilizator.scriere_caracter_VALUE(10); }
        eroare = true;
    }
    static boolean clip(int Pornește, int lungime_VALUE) { return Pornește >= 0 && lungime_VALUE >= 0 && Pornește <= Mărime - lungime_VALUE; }
    static int byte_VALUE() {
        if (!clip(읽기위치, 1)) { eroare_VALUE("truncated class file"); return 0; }
        return Fișier[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int întreg() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lungime_VALUE) { if (!clip(읽기위치, lungime_VALUE)) eroare_VALUE("invalid attribute size"); else 읽기위치 += lungime_VALUE; }
    static boolean verifica_constantă(int 수, int 종류) {
        if (수 <= 0 || 수 >= constantă_COUNT || constantă_eticheta[수] != 종류) { eroare_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_zonă(int Pornește, int lungime_VALUE, String Word_SMS) {
        if (!clip(Pornește, lungime_VALUE) || lungime_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < lungime_VALUE; 수++) if (Fișier[Pornește + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int constantă_VALUE, String Word_SMS) { return verifica_constantă(constantă_VALUE, 1) && SMS_zonă(상가[constantă_VALUE], constantă_SECOND_VALUE[constantă_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!verifica_constantă(가, 1) || !verifica_constantă(SECOND_operand, 1) || constantă_SECOND_VALUE[가] != constantă_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < constantă_SECOND_VALUE[가]; 수++) if (Fișier[상가[가] + 수] != Fișier[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int nume_de_clasă_SMS(int 수) { return verifica_constantă(수, 7) && verifica_constantă(상가[수], 1) ? 상가[수] : 0; }
    static int referință_nume(int 수) { return verifica_constantă(수, 12) && verifica_constantă(상가[수], 1) ? 상가[수] : 0; }
    static int referință_Tip(int 수) { return verifica_constantă(수, 12) && verifica_constantă(constantă_SECOND_VALUE[수], 1) ? constantă_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { eroare_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Pornește = 읽기위치;
            while (읽기위치 < 끝 && Fișier[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Pornește) eroare_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        eroare_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int funcție_VALUE) {
        int Anteriorul_element = 읽기위치, 수 = metodă_Tip[funcție_VALUE];
        if (!verifica_constantă(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + constantă_SECOND_VALUE[수];
        if (byte_VALUE() != '(') eroare_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!eroare && 읽기위치 < 끝 && Fișier[읽기위치] != ')') {
            if (element_COUNT == 16) { eroare_VALUE("too many method arguments"); break; }
            metodă_argument_Tip[funcție_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') eroare_VALUE("invalid method descriptor");
        metodă_restitui[funcție_VALUE] = 서술형(끝, true); metodă_argument_COUNT[funcție_VALUE] = element_COUNT;
        if (읽기위치 != 끝) eroare_VALUE("invalid method descriptor");
        읽기위치 = Anteriorul_element;
    }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !eroare; 수++) { verifica_constantă(짧은수(), 1); 건너(întreg()); }
    }
    static int comandă_lungime(int VALUE) {
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
        if (întreg() != 0xcafebabe) eroare_VALUE("not a class file");
        int 부판 = 짧은수(), versiune_VALUE = 짧은수();
        if (versiune_VALUE < 45 || versiune_VALUE > 52 || 부판 != 0) eroare_VALUE("supported class versions: 45..52, minor 0");
        constantă_COUNT = 짧은수();
        if (constantă_COUNT < 1 || constantă_COUNT > 512) { eroare_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < constantă_COUNT && !eroare; 수++) {
            int 종류 = byte_VALUE(); constantă_eticheta[수] = 종류;
            if (종류 == 1) { constantă_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(constantă_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = întreg();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); constantă_SECOND_VALUE[수] = 짧은수(); }
            else eroare_VALUE("unsupported constant type");
        }
        int permisiune_VALUE = 짧은수();
        if ((permisiune_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) eroare_VALUE("unsupported class flags");
        nume_de_clasă = nume_de_clasă_SMS(짧은수());
        if (!Word_SMS(nume_de_clasă_SMS(짧은수()), "java/lang/Object")) eroare_VALUE("inheritance unsupported");
        if (짧은수() != 0) eroare_VALUE("interfaces unsupported");
        if (짧은수() != 0) eroare_VALUE("fields unsupported");
        metodă_COUNT = 짧은수();
        if (metodă_COUNT < 1 || metodă_COUNT > 32) { eroare_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metodă_COUNT && !eroare; 수++) {
            metodă_acces[수] = 짧은수(); metodă_nume_SMS[수] = 짧은수(); metodă_Tip[수] = 짧은수();
            verifica_constantă(metodă_nume_SMS[수], 1); 서술읽기(수);
            if ((metodă_acces[수] & (0x100 | 0x400 | 0x20)) != 0) eroare_VALUE("native, abstract and synchronized methods unsupported");
            if ((metodă_acces[수] & 8) == 0 && !Word_SMS(metodă_nume_SMS[수], "<init>")) eroare_VALUE("instance methods unsupported");
            if (Word_SMS(metodă_nume_SMS[수], "<clinit>")) eroare_VALUE("class initializers unsupported");
            for (int frontală_VALUE = 0; frontală_VALUE < 수; frontală_VALUE++) if (같은말(metodă_nume_SMS[frontală_VALUE], metodă_nume_SMS[수]) && 같은말(metodă_Tip[frontală_VALUE], metodă_Tip[수])) eroare_VALUE("duplicate method");
            int element_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < element_COUNT && !eroare; atribut_VALUE++) {
                int Nume = 짧은수(), lungime_VALUE = întreg(), Pornește = 읽기위치;
                if (!clip(Pornește, lungime_VALUE)) { eroare_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nume, "Code")) {
                    if (metodă_buta[수] != 0) eroare_VALUE("duplicate Code attribute");
                    metodă_Teanc[수] = 짧은수(); 함수지역[수] = 짧은수(); int cod_lungime = întreg();
                    if (metodă_Teanc[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metodă_argument_COUNT[수]
                        || cod_lungime < 1 || cod_lungime > 8192) eroare_VALUE("method memory limits exceeded");
                    metodă_buta[수] = 읽기위치; 건너(cod_lungime); metodă_termina_un_apel[수] = 읽기위치;
                    if (짧은수() != 0) eroare_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Pornește + lungime_VALUE) eroare_VALUE("Code attribute size mismatch");
                } else 건너(lungime_VALUE);
            }
            if (metodă_buta[수] == 0) eroare_VALUE("missing Code attribute");
            int 칸 = metodă_buta[수];
            while (칸 < metodă_termina_un_apel[수] && !eroare) {
                int lungime_VALUE = comandă_lungime(Fișier[칸]);
                if (lungime_VALUE == 0 || lungime_VALUE > metodă_termina_un_apel[수] - 칸) { eroare_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += lungime_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 ramură 목적지를 허용하지 않는다.
            칸 = metodă_buta[수];
            while (칸 < metodă_termina_un_apel[수] && !eroare) {
                int VALUE = Fișier[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int destinație_VALUE = 칸 + (short)(Fișier[칸 + 1] << 8 | Fișier[칸 + 2]);
                    if (destinație_VALUE < metodă_buta[수] || destinație_VALUE >= metodă_termina_un_apel[수] || 경계[destinație_VALUE] != 수 + 1) eroare_VALUE("invalid branch target");
                }
                칸 += comandă_lungime(VALUE);
            }
        }
        if (!eroare) 속성건너();
        if (읽기위치 != Mărime) eroare_VALUE("extra class file data");
    }
    static int aloca_Stocare(int 종류, int lungime_VALUE) {
        if (lungime_VALUE < 0 || lungime_VALUE > 힙.length - 힙끝 - 2) { eroare_VALUE("object heap exhausted or negative array size"); return 0; }
        int referință = 힙끝; 힙끝 += lungime_VALUE + 2; 힙[referință] = 종류; 힙[referință + 1] = lungime_VALUE;
        return referință;
    }
    static boolean obiect_VALUE(int referință, int 종류) {
        if (referință < 1 || referință >= 힙끝 - 1 || 힙[referință] != 종류) { eroare_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int constantă_SMS(int INDEX) {
        if (!verifica_constantă(INDEX, 1)) return 0;
        if (șir_referință[INDEX] != 0) return șir_referință[INDEX];
        int referință = aloca_Stocare(1, constantă_SECOND_VALUE[INDEX]); if (eroare) return 0;
        int 끝 = 상가[INDEX] + constantă_SECOND_VALUE[INDEX], 수 = 상가[INDEX], lungime_VALUE = 0;
        while (수 < 끝 && !eroare) {
            int VALUE = Fișier[수++];
            if (VALUE == 0) eroare_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Următorul_element = Fișier[수++];
                if ((Următorul_element & 192) != 128) eroare_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Următorul_element & 63;
                if (VALUE != 0 && VALUE < 128) eroare_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Fișier[수++], SECOND_operand = Fișier[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) eroare_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) eroare_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) eroare_VALUE("invalid modified UTF-8");
            힙[referință + 2 + lungime_VALUE++] = VALUE;
        }
        힙[referință + 1] = lungime_VALUE; șir_referință[INDEX] = referință; return referință;
    }
    static int gazdă_caracter(String VALUE) {
        int referință = aloca_Stocare(1, VALUE.length()); if (eroare) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[referință + 2 + 수] = VALUE.charAt(수);
        return referință;
    }
    static void scriere_SMS(int referință) {
        if (referință == 0) { utilizator.Scriere("null"); return; }
        if (!obiect_VALUE(referință, 1)) return;
        for (int 수 = 0; 수 < 힙[referință + 1]; 수++) utilizator.scriere_caracter_VALUE(힙[referință + 2 + 수]);
    }
    static int cifră_caracter(int VALUE) {
        int referință = aloca_Stocare(1, 11); if (eroare) return 0;
        int lungime_VALUE = 0;
        if (VALUE < 0) 힙[referință + 2 + lungime_VALUE++] = '-'; else VALUE = -VALUE;
        int index_de_poziție = 1000000000; boolean Pornește = false;
        while (index_de_poziție != 0) {
            int 수 = -(VALUE / index_de_poziție);
            if (수 != 0 || Pornește || index_de_poziție == 1) { 힙[referință + 2 + lungime_VALUE++] = '0' + 수; Pornește = true; }
            VALUE %= index_de_poziție; index_de_poziție /= 10;
        }
        힙[referință + 1] = lungime_VALUE; return referință;
    }
    static int 정수해독(int referință) {
        if (!obiect_VALUE(referință, 1)) return 0;
        int lungime_VALUE = 힙[referință + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (lungime_VALUE > 0 && (힙[referință + 2] == '-' || 힙[referință + 2] == '+')) { 음수 = 힙[referință + 2] == '-'; 수++; }
        if (수 == lungime_VALUE) eroare_VALUE("NumberFormatException");
        for (; 수 < lungime_VALUE && !eroare; 수++) {
            int cifră_VALUE = 힙[referință + 2 + 수] - '0';
            if (cifră_VALUE < 0 || cifră_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && cifră_VALUE > (음수 ? 8 : 7)) eroare_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - cifră_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int Tip_VALUE) {
        if (eroare) return;
        if (cadru_INDEX < 0 || cadru_Teanc[cadru_INDEX] >= metodă_Teanc[cadru_metodă[cadru_INDEX]]) { eroare_VALUE("operand stack overflow"); return; }
        int 칸 = cadru_INDEX * 128 + cadru_Teanc[cadru_INDEX]++; operand_Teanc_VALUE[칸] = VALUE; operand_Teanc_Tip[칸] = Tip_VALUE;
    }
    static int 빼기(int Tip_VALUE) {
        if (eroare) return 0;
        if (cadru_INDEX < 0 || cadru_Teanc[cadru_INDEX] < 1) { eroare_VALUE("operand stack underflow"); return 0; }
        int 칸 = cadru_INDEX * 128 + --cadru_Teanc[cadru_INDEX]; restitui_Tip = operand_Teanc_Tip[칸];
        if (Tip_VALUE != 0 && restitui_Tip != Tip_VALUE) eroare_VALUE("operand type mismatch");
        return operand_Teanc_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[cadru_metodă[cadru_INDEX]] || INDEX < 0 || local_Tip[cadru_INDEX * 128 + INDEX] != Tip_VALUE) { eroare_VALUE("invalid or uninitialized local"); return; }
        넣기(local_VALUE[cadru_INDEX * 128 + INDEX], Tip_VALUE);
    }
    static void scriere_local(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[cadru_metodă[cadru_INDEX]] || INDEX < 0) { eroare_VALUE("local index out of range"); return; }
        int VALUE = 빼기(Tip_VALUE); local_VALUE[cadru_INDEX * 128 + INDEX] = VALUE; local_Tip[cadru_INDEX * 128 + INDEX] = Tip_VALUE;
    }
    static int 명바() {
        int Poziție = cadru_poziție[cadru_INDEX];
        if (Poziție < metodă_buta[cadru_metodă[cadru_INDEX]] || Poziție >= metodă_termina_un_apel[cadru_metodă[cadru_INDEX]]) { eroare_VALUE("instruction pointer out of range"); return 0; }
        cadru_poziție[cadru_INDEX]++; return Fișier[Poziție];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void muta_VALUE_83b651b8(int Poziție) {
        int funcție_VALUE = cadru_metodă[cadru_INDEX];
        if (Poziție < metodă_buta[funcție_VALUE] || Poziție >= metodă_termina_un_apel[funcție_VALUE] || 경계[Poziție] != funcție_VALUE + 1) eroare_VALUE("invalid branch target");
        else cadru_poziție[cadru_INDEX] = Poziție;
    }
    static void 호출(int funcție_VALUE) {
        if (cadru_INDEX == 31) { eroare_VALUE("call stack limit (32)"); return; }
        int Următorul_element = cadru_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) local_Tip[Următorul_element * 128 + 수] = 0;
        for (int 수 = metodă_argument_COUNT[funcție_VALUE] - 1; 수 >= 0; 수--) {
            local_VALUE[Următorul_element * 128 + 수] = 빼기(metodă_argument_Tip[funcție_VALUE * 16 + 수]); local_Tip[Următorul_element * 128 + 수] = metodă_argument_Tip[funcție_VALUE * 16 + 수];
        }
        cadru_INDEX = Următorul_element; cadru_metodă[cadru_INDEX] = funcție_VALUE; cadru_poziție[cadru_INDEX] = metodă_buta[funcție_VALUE]; cadru_Teanc[cadru_INDEX] = 0;
    }
    static void restitui_KR(int Tip_VALUE) {
        if (Tip_VALUE != metodă_restitui[cadru_metodă[cadru_INDEX]]) { eroare_VALUE("return type mismatch"); return; }
        int VALUE = Tip_VALUE == 0 ? 0 : 빼기(Tip_VALUE);
        cadru_INDEX--; if (cadru_INDEX >= 0 && Tip_VALUE != 0) 넣기(VALUE, Tip_VALUE);
    }
    static int[] flux_nume_de_fișier = new int[64];
    static void Fișier_flux_Apel(int proprietar_VALUE, int Nume, int format_VALUE, int Comandă) {
        boolean Rezultat = Word_SMS(proprietar_VALUE, "java/io/FileOutputStream");
        int 종류 = Rezultat ? 6 : 5;
        if (Comandă == 183 && Word_SMS(Nume, "<init>")) {
            boolean 이어 = false;
            if (Rezultat && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { eroare_VALUE("unsupported file stream constructor"); return; }
            int Fișier_intrare_nume = 빼기(2), flux_VALUE = 빼기(2);
            if (!obiect_VALUE(Fișier_intrare_nume, 1) || !obiect_VALUE(flux_VALUE, 종류) || eroare) return;
            if (힙[flux_VALUE + 3] != 0) { eroare_VALUE("file stream already initialized"); return; }
            int lungime_VALUE = 힙[Fișier_intrare_nume + 1];
            if (lungime_VALUE < 1 || lungime_VALUE > 63) { eroare_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < lungime_VALUE; 칸++) {
                int VALUE = 힙[Fișier_intrare_nume + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { eroare_VALUE("file stream paths currently require ASCII"); return; }
                flux_nume_de_fișier[칸] = VALUE;
            }
            flux_nume_de_fișier[lungime_VALUE] = 0;
            int 서술자 = utilizator.파일서술자열기(flux_nume_de_fișier, Rezultat ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { eroare_VALUE("FileNotFoundException: file open failed"); return; }
            힙[flux_VALUE + 2] = 서술자; 힙[flux_VALUE + 3] = 1;
            return;
        }
        if (Comandă != 182) { eroare_VALUE("invalid file stream invocation"); return; }
        int Acțiuni = -1, VALUE = 0;
        if (Word_SMS(Nume, "close") && Word_SMS(format_VALUE, "()V")) Acțiuni = 0;
        if (!Rezultat && Word_SMS(Nume, "read") && Word_SMS(format_VALUE, "()I")) Acțiuni = 1;
        if (Rezultat && Word_SMS(Nume, "write") && Word_SMS(format_VALUE, "(I)V")) { Acțiuni = 2; VALUE = 빼기(1); }
        if (Acțiuni < 0) { eroare_VALUE("unsupported file stream method"); return; }
        int flux_VALUE = 빼기(2);
        if (!obiect_VALUE(flux_VALUE, 종류) || eroare) return;
        if (힙[flux_VALUE + 3] == 0) { eroare_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[flux_VALUE + 2];
        if (Acțiuni == 0) {
            if (서술자 >= 0 && utilizator.파일서술자닫기(서술자) < 0) eroare_VALUE("IOException: close failed");
            힙[flux_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { eroare_VALUE("IOException: stream closed"); return; }
        if (Acțiuni == 1) {
            int KR = utilizator.파일한바이트읽기(서술자);
            if (KR < -1) eroare_VALUE("IOException: read failed"); else 넣기(KR, 1);
        } else if (utilizator.파일한바이트쓰기(서술자, VALUE) != 1) eroare_VALUE("IOException: write failed");
    }
    static void Apel_metodă(int INDEX, int Comandă) {
        if (!verifica_constantă(INDEX, 10)) return;
        int proprietar_VALUE = nume_de_clasă_SMS(상가[INDEX]), Nume = referință_nume(constantă_SECOND_VALUE[INDEX]), format_VALUE = referință_Tip(constantă_SECOND_VALUE[INDEX]);
        if (eroare) return;
        if (같은말(proprietar_VALUE, nume_de_clasă)) {
            if (Comandă != 184) { eroare_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metodă_COUNT; 수++) if (같은말(Nume, metodă_nume_SMS[수]) && 같은말(format_VALUE, metodă_Tip[수])) {
                if ((metodă_acces[수] & 8) == 0) eroare_VALUE("method is not static"); else 호출(수);
                return;
            }
            eroare_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(proprietar_VALUE, "java/io/FileInputStream") || Word_SMS(proprietar_VALUE, "java/io/FileOutputStream")) {
            Fișier_flux_Apel(proprietar_VALUE, Nume, format_VALUE, Comandă); return;
        }
        if (Comandă == 184 && Word_SMS(proprietar_VALUE, "java/lang/Integer") && Word_SMS(Nume, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Comandă == 182 && Word_SMS(proprietar_VALUE, "java/io/PrintStream") && (Word_SMS(Nume, "println") || Word_SMS(Nume, "print"))) {
            int Tip_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { Tip_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { Tip_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { Tip_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { Tip_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(Nume, "println")) eroare_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) eroare_VALUE("invalid PrintStream receiver");
            if (eroare) return;
            if (Tip_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (Tip_VALUE == 2) utilizator.Scriere(VALUE == 0 ? "false" : "true");
            if (Tip_VALUE == 3) utilizator.scriere_caracter_VALUE(VALUE & 65535);
            if (Tip_VALUE == 4) scriere_SMS(VALUE);
            if (Word_SMS(Nume, "println")) utilizator.scriere_caracter_VALUE(10);
            return;
        }
        if (Comandă == 182 && Word_SMS(proprietar_VALUE, "java/lang/String")) {
            if (Word_SMS(Nume, "length") && Word_SMS(format_VALUE, "()I")) {
                int referință = 빼기(2); if (obiect_VALUE(referință, 1)) 넣기(힙[referință + 1], 1); return;
            }
            if (Word_SMS(Nume, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int indice_VALUE = 빼기(1), referință = 빼기(2);
                if (obiect_VALUE(referință, 1)) {
                    if (indice_VALUE < 0 || indice_VALUE >= 힙[referință + 1]) eroare_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[referință + 2 + indice_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(proprietar_VALUE, "java/lang/StringBuilder")) {
            if (Comandă == 183 && Word_SMS(Nume, "<init>") && Word_SMS(format_VALUE, "()V")) { obiect_VALUE(빼기(2), 4); return; }
            if (Comandă == 182 && Word_SMS(Nume, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int referință = 빼기(2); if (obiect_VALUE(referință, 4)) 넣기(힙[referință + 2] == 0 ? gazdă_caracter("") : 힙[referință + 2], 2); return;
            }
            if (Comandă == 182 && Word_SMS(Nume, "append")) {
                int SMS = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = cifră_caracter(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = gazdă_caracter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = aloca_Stocare(1, 1); if (!eroare) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = gazdă_caracter("null"); }
                else { eroare_VALUE("unsupported StringBuilder append"); return; }
                int referință = 빼기(2); if (!obiect_VALUE(referință, 4) || !obiect_VALUE(SMS, 1)) return;
                int frontală_VALUE = 힙[referință + 2], frontală_VALUE_lungime = frontală_VALUE == 0 ? 0 : 힙[frontală_VALUE + 1], ÎNAPOI_VALUE_lungime = 힙[SMS + 1];
                int 새글 = aloca_Stocare(1, frontală_VALUE_lungime + ÎNAPOI_VALUE_lungime); if (eroare) return;
                for (int 수 = 0; 수 < frontală_VALUE_lungime; 수++) 힙[새글 + 2 + 수] = 힙[frontală_VALUE + 2 + 수];
                for (int 수 = 0; 수 < ÎNAPOI_VALUE_lungime; 수++) 힙[새글 + 2 + frontală_VALUE_lungime + 수] = 힙[SMS + 2 + 수];
                힙[referință + 2] = 새글; 넣기(referință, 2); return;
            }
        }
        eroare_VALUE("unsupported library method");
    }
    static int 배열칸(int referință, int indice_VALUE, int Tip_VALUE) {
        if (!obiect_VALUE(referință, Tip_VALUE)) return 0;
        if (indice_VALUE < 0 || indice_VALUE >= 힙[referință + 1]) { eroare_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return referință + 2 + indice_VALUE;
    }
    static void executa_comandă() {
        int 남음 = 500000;
        while (cadru_INDEX >= 0 && !eroare) {
            if (--남음 == 0) { eroare_VALUE("instruction limit (500000)"); break; }
            int Pornește = cadru_poziție[cadru_INDEX], VALUE = 명바();
            if (eroare) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= constantă_COUNT) eroare_VALUE("invalid ldc constant");
                else if (constantă_eticheta[수] == 3) 넣기(상가[수], 1);
                else if (constantă_eticheta[수] == 8) 넣기(constantă_SMS(상가[수]), 2);
                else eroare_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { scriere_local(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { scriere_local(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { scriere_local(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int indice_VALUE = 빼기(1), referință = 빼기(2), 칸 = 배열칸(referință, indice_VALUE, VALUE == 46 ? 2 : 3);
                if (!eroare) 넣기(힙[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int element_element = 빼기(VALUE == 79 ? 1 : 2), indice_VALUE = 빼기(1), referință = 빼기(2), 칸 = 배열칸(referință, indice_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && element_element != 0) obiect_VALUE(element_element, 1);
                if (!eroare) 힙[칸] = element_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), Tip_VALUE = restitui_Tip; 넣기(가, Tip_VALUE); 넣기(가, Tip_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = restitui_Tip, SECOND_operand = 빼기(0), SECOND_operand_Tip = restitui_Tip; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_Tip); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), KR = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { eroare_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) KR = 가 + SECOND_operand;
                if (VALUE == 100) KR = 가 - SECOND_operand;
                if (VALUE == 104) KR = 가 * SECOND_operand;
                if (VALUE == 108) KR = 가 / SECOND_operand;
                if (VALUE == 112) KR = 가 % SECOND_operand;
                if (VALUE == 120) KR = 가 << SECOND_operand;
                if (VALUE == 122) KR = 가 >> SECOND_operand;
                if (VALUE == 124) KR = 가 >>> SECOND_operand;
                if (VALUE == 126) KR = 가 & SECOND_operand;
                if (VALUE == 128) KR = 가 | SECOND_operand;
                if (VALUE == 130) KR = 가 ^ SECOND_operand;
                넣기(KR, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int local_gamă = 명바(), increment_pas = (byte)명바(); 지역읽기(local_gamă, 1); 넣기(빼기(1) + increment_pas, 1); scriere_local(local_gamă, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int destinație_VALUE = Pornește + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) muta_VALUE_83b651b8(destinație_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { restitui_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!verifica_constantă(수, 9)) continue;
                if (!Word_SMS(nume_de_clasă_SMS(상가[수]), "java/lang/System") || !Word_SMS(referință_nume(constantă_SECOND_VALUE[수]), "out")
                    || !Word_SMS(referință_Tip(constantă_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) eroare_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { Apel_metodă(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Nume = nume_de_clasă_SMS(명짧());
                if (Word_SMS(Nume, "java/lang/StringBuilder")) 넣기(aloca_Stocare(4, 1), 2);
                else if (Word_SMS(Nume, "java/io/FileInputStream") || Word_SMS(Nume, "java/io/FileOutputStream")) {
                    int referință = aloca_Stocare(Word_SMS(Nume, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!eroare) { 힙[referință + 2] = -1; 넣기(referință, 2); }
                } else eroare_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) eroare_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(nume_de_clasă_SMS(명짧()), "java/lang/String")) eroare_VALUE("only String[] anewarray is supported");
                int lungime_VALUE = 빼기(1); 넣기(aloca_Stocare(VALUE == 188 ? 2 : 3, lungime_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int referință = 빼기(2);
                if (referință < 1 || referință >= 힙끝 - 1 || (힙[referință] != 2 && 힙[referință] != 3)) eroare_VALUE("null or invalid array");
                else 넣기(힙[referință + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Nume = nume_de_clasă_SMS(명짧()), referință = 빼기(2);
                if (!Word_SMS(Nume, "java/lang/String")) eroare_VALUE("unsupported checkcast");
                else if (referință != 0) obiect_VALUE(referință, 1);
                넣기(referință, 2); continue;
            }
            eroare_VALUE("unsupported bytecode");
        }
    }
    public static int Pornește() {
        if (utilizator.인수개수() == 1 && 자바도구.같음(utilizator.Argumente(0), "-version")) {
            utilizator.Scriere("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (utilizator.인수개수() < 1) { utilizator.Scriere("Usage: java CLASS [ARGS]\n"); return 2; }
        int lungime_VALUE = 자바도구.Nume(nume_de_fișier_SMS, utilizator.Argumente(0));
        if (lungime_VALUE < 1 || lungime_VALUE > 57) { utilizator.Scriere("java: invalid class name\n"); return 2; }
        nume_de_fișier_SMS[lungime_VALUE] = '.'; nume_de_fișier_SMS[lungime_VALUE + 1] = 'c'; nume_de_fișier_SMS[lungime_VALUE + 2] = 'l'; nume_de_fișier_SMS[lungime_VALUE + 3] = 'a'; nume_de_fișier_SMS[lungime_VALUE + 4] = 's'; nume_de_fișier_SMS[lungime_VALUE + 5] = 's';
        Mărime = utilizator.파일읽기(nume_de_fișier_SMS, Fișier);
        if (Mărime < 0) { utilizator.Scriere("java: cannot read class: "); 자바도구.수쓰기(Mărime); utilizator.scriere_caracter_VALUE(10); return 1; }
        클래스읽기(); if (eroare) return 1;
        int caracter_nume = constantă_SMS(nume_de_clasă);
        if (!eroare && 힙[caracter_nume + 1] != lungime_VALUE) eroare_VALUE("class name does not match file");
        for (int 수 = 0; 수 < lungime_VALUE && !eroare; 수++) if (힙[caracter_nume + 2 + 수] != nume_de_fișier_SMS[수]) eroare_VALUE("class name does not match file");
        int intrare_p_VALUE = -1;
        for (int 수 = 0; 수 < metodă_COUNT; 수++) if (Word_SMS(metodă_nume_SMS[수], "main") && Word_SMS(metodă_Tip[수], "([Ljava/lang/String;)V") && (metodă_acces[수] & 9) == 9) intrare_p_VALUE = 수;
        if (intrare_p_VALUE < 0) eroare_VALUE("public static void main(String[] args) required");
        if (eroare) return 1;
        int Argumente = aloca_Stocare(3, utilizator.인수개수() - 1);
        for (int 수 = 1; 수 < utilizator.인수개수() && !eroare; 수++) 힙[Argumente + 1 + 수] = gazdă_caracter(utilizator.Argumente(수));
        cadru_INDEX = 0; cadru_metodă[0] = intrare_p_VALUE; cadru_poziție[0] = metodă_buta[intrare_p_VALUE]; local_VALUE[0] = Argumente; local_Tip[0] = 2;
        executa_comandă(); return eroare ? 1 : 0;
    }
}
