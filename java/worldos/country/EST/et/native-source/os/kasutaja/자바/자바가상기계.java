// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fail/operand_Virn/viide/haru 경계를 Täida_käsk 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fail = new int[16384], failinimi_SMS = new int[64];
    static int[] konstant_silt = new int[512], 상가 = new int[512], konstant_SECOND_VALUE = new int[512], string_viide = new int[512];
    static int[] meetod_nimetus_SMS = new int[32], meetod_TYPE = new int[32], meetod_pöördus = new int[32];
    static int[] meetod_START = new int[32], meetod_lõpeta_kõne = new int[32], meetod_Virn = new int[32], 함수지역 = new int[32];
    static int[] meetod_argument_COUNT = new int[32], meetod_argument_TYPE = new int[512], meetod_tagasi_saatma = new int[32];
    static int[] 경계 = new int[16384];
    static int[] kohalik_VALUE = new int[4096], kohalik_TYPE = new int[4096], operand_Virn_VALUE = new int[4096], operand_Virn_TYPE = new int[4096];
    static int[] raam_meetod = new int[32], raam_ametikoht = new int[32], raam_Virn = new int[32];
    static int[] 힙 = new int[8192];
    static int Suurus, 읽기위치, konstant_COUNT, meetod_COUNT, klassinimi, raam_INDEX = -1, 힙끝 = 1, tagasi_saatma_TYPE;
    static boolean VIGA;

    static void tõrge_VALUE(String Word_SMS) {
        if (!VIGA) { kasutaja.Kirjutamine("JVM error: "); kasutaja.Kirjutamine(Word_SMS); kasutaja.kirjutamine_märk_VALUE(10); }
        VIGA = true;
    }
    static boolean klipp(int Käivita_2, int 길이) { return Käivita_2 >= 0 && 길이 >= 0 && Käivita_2 <= Suurus - 길이; }
    static int bait_VALUE() {
        if (!klipp(읽기위치, 1)) { tõrge_VALUE("truncated class file"); return 0; }
        return Fail[읽기위치++];
    }
    static int 짧은수() { return bait_VALUE() << 8 | bait_VALUE(); }
    static int täisarv() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klipp(읽기위치, 길이)) tõrge_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean tšekk_konstant(int number, int 종류) {
        if (number <= 0 || number >= konstant_COUNT || konstant_silt[number] != 종류) { tõrge_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_vahemik(int Käivita_2, int 길이, String Word_SMS) {
        if (!klipp(Käivita_2, 길이) || 길이 != Word_SMS.length()) return false;
        for (int number = 0; number < 길이; number++) if (Fail[Käivita_2 + number] != Word_SMS.charAt(number)) return false;
        return true;
    }
    static boolean Word_SMS(int konstant_VALUE, String Word_SMS) { return tšekk_konstant(konstant_VALUE, 1) && SMS_vahemik(상가[konstant_VALUE], konstant_SECOND_VALUE[konstant_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!tšekk_konstant(가, 1) || !tšekk_konstant(SECOND_operand, 1) || konstant_SECOND_VALUE[가] != konstant_SECOND_VALUE[SECOND_operand]) return false;
        for (int number = 0; number < konstant_SECOND_VALUE[가]; number++) if (Fail[상가[가] + number] != Fail[상가[SECOND_operand] + number]) return false;
        return true;
    }
    static int klassinimi_SMS(int number) { return tšekk_konstant(number, 7) && tšekk_konstant(상가[number], 1) ? 상가[number] : 0; }
    static int viide_nimetus(int number) { return tšekk_konstant(number, 12) && tšekk_konstant(상가[number], 1) ? 상가[number] : 0; }
    static int viide_TYPE(int number) { return tšekk_konstant(number, 12) && tšekk_konstant(konstant_SECOND_VALUE[number], 1) ? konstant_SECOND_VALUE[number] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { tõrge_VALUE("invalid descriptor"); return 0; }
        int VALUE = bait_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Käivita_2 = 읽기위치;
            while (읽기위치 < 끝 && Fail[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Käivita_2) tõrge_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        tõrge_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, number = meetod_TYPE[FUNCTION_VALUE];
        if (!tšekk_konstant(number, 1)) return;
        읽기위치 = 상가[number]; int 끝 = 읽기위치 + konstant_SECOND_VALUE[number];
        if (bait_VALUE() != '(') tõrge_VALUE("invalid method descriptor");
        int kaup_COUNT = 0;
        while (!VIGA && 읽기위치 < 끝 && Fail[읽기위치] != ')') {
            if (kaup_COUNT == 16) { tõrge_VALUE("too many method arguments"); break; }
            meetod_argument_TYPE[FUNCTION_VALUE * 16 + kaup_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bait_VALUE() != ')') tõrge_VALUE("invalid method descriptor");
        meetod_tagasi_saatma[FUNCTION_VALUE] = 서술형(끝, true); meetod_argument_COUNT[FUNCTION_VALUE] = kaup_COUNT;
        if (읽기위치 != 끝) tõrge_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int kaup_COUNT = 짧은수();
        for (int number = 0; number < kaup_COUNT && !VIGA; number++) { tšekk_konstant(짧은수(), 1); 건너(täisarv()); }
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
        if (täisarv() != 0xcafebabe) tõrge_VALUE("not a class file");
        int 부판 = 짧은수(), versioon_VALUE = 짧은수();
        if (versioon_VALUE < 45 || versioon_VALUE > 52 || 부판 != 0) tõrge_VALUE("supported class versions: 45..52, minor 0");
        konstant_COUNT = 짧은수();
        if (konstant_COUNT < 1 || konstant_COUNT > 512) { tõrge_VALUE("constant pool limit (511)"); return; }
        for (int number = 1; number < konstant_COUNT && !VIGA; number++) {
            int 종류 = bait_VALUE(); konstant_silt[number] = 종류;
            if (종류 == 1) { konstant_SECOND_VALUE[number] = 짧은수(); 상가[number] = 읽기위치; 건너(konstant_SECOND_VALUE[number]); }
            else if (종류 == 3) 상가[number] = täisarv();
            else if (종류 == 7 || 종류 == 8) 상가[number] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[number] = 짧은수(); konstant_SECOND_VALUE[number] = 짧은수(); }
            else tõrge_VALUE("unsupported constant type");
        }
        int luba_VALUE = 짧은수();
        if ((luba_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) tõrge_VALUE("unsupported class flags");
        klassinimi = klassinimi_SMS(짧은수());
        if (!Word_SMS(klassinimi_SMS(짧은수()), "java/lang/Object")) tõrge_VALUE("inheritance unsupported");
        if (짧은수() != 0) tõrge_VALUE("interfaces unsupported");
        if (짧은수() != 0) tõrge_VALUE("fields unsupported");
        meetod_COUNT = 짧은수();
        if (meetod_COUNT < 1 || meetod_COUNT > 32) { tõrge_VALUE("method count limit (32)"); return; }
        for (int number = 0; number < meetod_COUNT && !VIGA; number++) {
            meetod_pöördus[number] = 짧은수(); meetod_nimetus_SMS[number] = 짧은수(); meetod_TYPE[number] = 짧은수();
            tšekk_konstant(meetod_nimetus_SMS[number], 1); 서술읽기(number);
            if ((meetod_pöördus[number] & (0x100 | 0x400 | 0x20)) != 0) tõrge_VALUE("native, abstract and synchronized methods unsupported");
            if ((meetod_pöördus[number] & 8) == 0 && !Word_SMS(meetod_nimetus_SMS[number], "<init>")) tõrge_VALUE("instance methods unsupported");
            if (Word_SMS(meetod_nimetus_SMS[number], "<clinit>")) tõrge_VALUE("class initializers unsupported");
            for (int esikaamera_VALUE = 0; esikaamera_VALUE < number; esikaamera_VALUE++) if (같은말(meetod_nimetus_SMS[esikaamera_VALUE], meetod_nimetus_SMS[number]) && 같은말(meetod_TYPE[esikaamera_VALUE], meetod_TYPE[number])) tõrge_VALUE("duplicate method");
            int kaup_COUNT = 짧은수();
            for (int atribuut_VALUE = 0; atribuut_VALUE < kaup_COUNT && !VIGA; atribuut_VALUE++) {
                int Nimi_2 = 짧은수(), 길이 = täisarv(), Käivita_2 = 읽기위치;
                if (!klipp(Käivita_2, 길이)) { tõrge_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nimi_2, "Code")) {
                    if (meetod_START[number] != 0) tõrge_VALUE("duplicate Code attribute");
                    meetod_Virn[number] = 짧은수(); 함수지역[number] = 짧은수(); int 코드길이 = täisarv();
                    if (meetod_Virn[number] > 128 || 함수지역[number] > 128 || 함수지역[number] < meetod_argument_COUNT[number]
                        || 코드길이 < 1 || 코드길이 > 8192) tõrge_VALUE("method memory limits exceeded");
                    meetod_START[number] = 읽기위치; 건너(코드길이); meetod_lõpeta_kõne[number] = 읽기위치;
                    if (짧은수() != 0) tõrge_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Käivita_2 + 길이) tõrge_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if (meetod_START[number] == 0) tõrge_VALUE("missing Code attribute");
            int 칸 = meetod_START[number];
            while (칸 < meetod_lõpeta_kõne[number] && !VIGA) {
                int 길이 = 명령길이(Fail[칸]);
                if (길이 == 0 || 길이 > meetod_lõpeta_kõne[number] - 칸) { tõrge_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = number + 1; 칸 += 길이;
            }
            // 실행하지 않는 경로에도 잘못된 haru 목적지를 허용하지 않는다.
            칸 = meetod_START[number];
            while (칸 < meetod_lõpeta_kõne[number] && !VIGA) {
                int VALUE = Fail[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int sihtkoht_VALUE = 칸 + (short)(Fail[칸 + 1] << 8 | Fail[칸 + 2]);
                    if (sihtkoht_VALUE < meetod_START[number] || sihtkoht_VALUE >= meetod_lõpeta_kõne[number] || 경계[sihtkoht_VALUE] != number + 1) tõrge_VALUE("invalid branch target");
                }
                칸 += 명령길이(VALUE);
            }
        }
        if (!VIGA) 속성건너();
        if (읽기위치 != Suurus) tõrge_VALUE("extra class file data");
    }
    static int lisama_salvesti(int 종류, int 길이) {
        if (길이 < 0 || 길이 > 힙.length - 힙끝 - 2) { tõrge_VALUE("object heap exhausted or negative array size"); return 0; }
        int viide = 힙끝; 힙끝 += 길이 + 2; 힙[viide] = 종류; 힙[viide + 1] = 길이;
        return viide;
    }
    static boolean objekt_VALUE(int viide, int 종류) {
        if (viide < 1 || viide >= 힙끝 - 1 || 힙[viide] != 종류) { tõrge_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstant_SMS(int INDEX) {
        if (!tšekk_konstant(INDEX, 1)) return 0;
        if (string_viide[INDEX] != 0) return string_viide[INDEX];
        int viide = lisama_salvesti(1, konstant_SECOND_VALUE[INDEX]); if (VIGA) return 0;
        int 끝 = 상가[INDEX] + konstant_SECOND_VALUE[INDEX], number = 상가[INDEX], 길이 = 0;
        while (number < 끝 && !VIGA) {
            int VALUE = Fail[number++];
            if (VALUE == 0) tõrge_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && number < 끝) {
                int Edasi_kaup = Fail[number++];
                if ((Edasi_kaup & 192) != 128) tõrge_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Edasi_kaup & 63;
                if (VALUE != 0 && VALUE < 128) tõrge_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && number + 1 < 끝) {
                int 가 = Fail[number++], SECOND_operand = Fail[number++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) tõrge_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) tõrge_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) tõrge_VALUE("invalid modified UTF-8");
            힙[viide + 2 + 길이++] = VALUE;
        }
        힙[viide + 1] = 길이; string_viide[INDEX] = viide; return viide;
    }
    static int host_märk(String VALUE) {
        int viide = lisama_salvesti(1, VALUE.length()); if (VIGA) return 0;
        for (int number = 0; number < VALUE.length(); number++) 힙[viide + 2 + number] = VALUE.charAt(number);
        return viide;
    }
    static void kirjutamine_SMS(int viide) {
        if (viide == 0) { kasutaja.Kirjutamine("null"); return; }
        if (!objekt_VALUE(viide, 1)) return;
        for (int number = 0; number < 힙[viide + 1]; number++) kasutaja.kirjutamine_märk_VALUE(힙[viide + 2 + number]);
    }
    static int number_märk(int VALUE) {
        int viide = lisama_salvesti(1, 11); if (VIGA) return 0;
        int 길이 = 0;
        if (VALUE < 0) 힙[viide + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int asukohaindeks = 1000000000; boolean Käivita_2 = false;
        while (asukohaindeks != 0) {
            int number = -(VALUE / asukohaindeks);
            if (number != 0 || Käivita_2 || asukohaindeks == 1) { 힙[viide + 2 + 길이++] = '0' + number; Käivita_2 = true; }
            VALUE %= asukohaindeks; asukohaindeks /= 10;
        }
        힙[viide + 1] = 길이; return viide;
    }
    static int 정수해독(int viide) {
        if (!objekt_VALUE(viide, 1)) return 0;
        int 길이 = 힙[viide + 1], number = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[viide + 2] == '-' || 힙[viide + 2] == '+')) { 음수 = 힙[viide + 2] == '-'; number++; }
        if (number == 길이) tõrge_VALUE("NumberFormatException");
        for (; number < 길이 && !VIGA; number++) {
            int number_VALUE = 힙[viide + 2 + number] - '0';
            if (number_VALUE < 0 || number_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && number_VALUE > (음수 ? 8 : 7)) tõrge_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - number_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (VIGA) return;
        if (raam_INDEX < 0 || raam_Virn[raam_INDEX] >= meetod_Virn[raam_meetod[raam_INDEX]]) { tõrge_VALUE("operand stack overflow"); return; }
        int 칸 = raam_INDEX * 128 + raam_Virn[raam_INDEX]++; operand_Virn_VALUE[칸] = VALUE; operand_Virn_TYPE[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (VIGA) return 0;
        if (raam_INDEX < 0 || raam_Virn[raam_INDEX] < 1) { tõrge_VALUE("operand stack underflow"); return 0; }
        int 칸 = raam_INDEX * 128 + --raam_Virn[raam_INDEX]; tagasi_saatma_TYPE = operand_Virn_TYPE[칸];
        if (TYPE_VALUE != 0 && tagasi_saatma_TYPE != TYPE_VALUE) tõrge_VALUE("operand type mismatch");
        return operand_Virn_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[raam_meetod[raam_INDEX]] || INDEX < 0 || kohalik_TYPE[raam_INDEX * 128 + INDEX] != TYPE_VALUE) { tõrge_VALUE("invalid or uninitialized local"); return; }
        넣기(kohalik_VALUE[raam_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void kirjutamine_kohalik(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[raam_meetod[raam_INDEX]] || INDEX < 0) { tõrge_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); kohalik_VALUE[raam_INDEX * 128 + INDEX] = VALUE; kohalik_TYPE[raam_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Asukoht = raam_ametikoht[raam_INDEX];
        if (Asukoht < meetod_START[raam_meetod[raam_INDEX]] || Asukoht >= meetod_lõpeta_kõne[raam_meetod[raam_INDEX]]) { tõrge_VALUE("instruction pointer out of range"); return 0; }
        raam_ametikoht[raam_INDEX]++; return Fail[Asukoht];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void liigutama_VALUE(int Asukoht) {
        int FUNCTION_VALUE = raam_meetod[raam_INDEX];
        if (Asukoht < meetod_START[FUNCTION_VALUE] || Asukoht >= meetod_lõpeta_kõne[FUNCTION_VALUE] || 경계[Asukoht] != FUNCTION_VALUE + 1) tõrge_VALUE("invalid branch target");
        else raam_ametikoht[raam_INDEX] = Asukoht;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (raam_INDEX == 31) { tõrge_VALUE("call stack limit (32)"); return; }
        int Edasi_kaup = raam_INDEX + 1;
        for (int number = 0; number < 128; number++) kohalik_TYPE[Edasi_kaup * 128 + number] = 0;
        for (int number = meetod_argument_COUNT[FUNCTION_VALUE] - 1; number >= 0; number--) {
            kohalik_VALUE[Edasi_kaup * 128 + number] = 빼기(meetod_argument_TYPE[FUNCTION_VALUE * 16 + number]); kohalik_TYPE[Edasi_kaup * 128 + number] = meetod_argument_TYPE[FUNCTION_VALUE * 16 + number];
        }
        raam_INDEX = Edasi_kaup; raam_meetod[raam_INDEX] = FUNCTION_VALUE; raam_ametikoht[raam_INDEX] = meetod_START[FUNCTION_VALUE]; raam_Virn[raam_INDEX] = 0;
    }
    static void tagasi_saatma_näitaja(int TYPE_VALUE) {
        if (TYPE_VALUE != meetod_tagasi_saatma[raam_meetod[raam_INDEX]]) { tõrge_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        raam_INDEX--; if (raam_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] voog_failinimi = new int[64];
    static void Fail_voog_CALL(int omanik_VALUE, int Nimi_2, int vorming_VALUE, int Käsk) {
        boolean Väljund = Word_SMS(omanik_VALUE, "java/io/FileOutputStream");
        int 종류 = Väljund ? 6 : 5;
        if (Käsk == 183 && Word_SMS(Nimi_2, "<init>")) {
            boolean 이어 = false;
            if (Väljund && Word_SMS(vorming_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(vorming_VALUE, "(Ljava/lang/String;)V")) { tõrge_VALUE("unsupported file stream constructor"); return; }
            int Fail_kirje_nimetus = 빼기(2), voog_VALUE = 빼기(2);
            if (!objekt_VALUE(Fail_kirje_nimetus, 1) || !objekt_VALUE(voog_VALUE, 종류) || VIGA) return;
            if (힙[voog_VALUE + 3] != 0) { tõrge_VALUE("file stream already initialized"); return; }
            int 길이 = 힙[Fail_kirje_nimetus + 1];
            if (길이 < 1 || 길이 > 63) { tõrge_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = 힙[Fail_kirje_nimetus + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { tõrge_VALUE("file stream paths currently require ASCII"); return; }
                voog_failinimi[칸] = VALUE;
            }
            voog_failinimi[길이] = 0;
            int 서술자 = kasutaja.파일서술자열기(voog_failinimi, Väljund ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { tõrge_VALUE("FileNotFoundException: file open failed"); return; }
            힙[voog_VALUE + 2] = 서술자; 힙[voog_VALUE + 3] = 1;
            return;
        }
        if (Käsk != 182) { tõrge_VALUE("invalid file stream invocation"); return; }
        int Nimi = -1, VALUE = 0;
        if (Word_SMS(Nimi_2, "close") && Word_SMS(vorming_VALUE, "()V")) Nimi = 0;
        if (!Väljund && Word_SMS(Nimi_2, "read") && Word_SMS(vorming_VALUE, "()I")) Nimi = 1;
        if (Väljund && Word_SMS(Nimi_2, "write") && Word_SMS(vorming_VALUE, "(I)V")) { Nimi = 2; VALUE = 빼기(1); }
        if (Nimi < 0) { tõrge_VALUE("unsupported file stream method"); return; }
        int voog_VALUE = 빼기(2);
        if (!objekt_VALUE(voog_VALUE, 종류) || VIGA) return;
        if (힙[voog_VALUE + 3] == 0) { tõrge_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[voog_VALUE + 2];
        if (Nimi == 0) {
            if (서술자 >= 0 && kasutaja.파일서술자닫기(서술자) < 0) tõrge_VALUE("IOException: close failed");
            힙[voog_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { tõrge_VALUE("IOException: stream closed"); return; }
        if (Nimi == 1) {
            int TULEMUS = kasutaja.파일한바이트읽기(서술자);
            if (TULEMUS < -1) tõrge_VALUE("IOException: read failed"); else 넣기(TULEMUS, 1);
        } else if (kasutaja.파일한바이트쓰기(서술자, VALUE) != 1) tõrge_VALUE("IOException: write failed");
    }
    static void CALL_meetod(int INDEX, int Käsk) {
        if (!tšekk_konstant(INDEX, 10)) return;
        int omanik_VALUE = klassinimi_SMS(상가[INDEX]), Nimi_2 = viide_nimetus(konstant_SECOND_VALUE[INDEX]), vorming_VALUE = viide_TYPE(konstant_SECOND_VALUE[INDEX]);
        if (VIGA) return;
        if (같은말(omanik_VALUE, klassinimi)) {
            if (Käsk != 184) { tõrge_VALUE("only static user methods are supported"); return; }
            for (int number = 0; number < meetod_COUNT; number++) if (같은말(Nimi_2, meetod_nimetus_SMS[number]) && 같은말(vorming_VALUE, meetod_TYPE[number])) {
                if ((meetod_pöördus[number] & 8) == 0) tõrge_VALUE("method is not static"); else 호출(number);
                return;
            }
            tõrge_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(omanik_VALUE, "java/io/FileInputStream") || Word_SMS(omanik_VALUE, "java/io/FileOutputStream")) {
            Fail_voog_CALL(omanik_VALUE, Nimi_2, vorming_VALUE, Käsk); return;
        }
        if (Käsk == 184 && Word_SMS(omanik_VALUE, "java/lang/Integer") && Word_SMS(Nimi_2, "parseInt") && Word_SMS(vorming_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Käsk == 182 && Word_SMS(omanik_VALUE, "java/io/PrintStream") && (Word_SMS(Nimi_2, "println") || Word_SMS(Nimi_2, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(vorming_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(vorming_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(vorming_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(vorming_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(vorming_VALUE, "()V") || !Word_SMS(Nimi_2, "println")) tõrge_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) tõrge_VALUE("invalid PrintStream receiver");
            if (VIGA) return;
            if (TYPE_VALUE == 1) 자바도구.kirjutamine_number(VALUE);
            if (TYPE_VALUE == 2) kasutaja.Kirjutamine(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) kasutaja.kirjutamine_märk_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) kirjutamine_SMS(VALUE);
            if (Word_SMS(Nimi_2, "println")) kasutaja.kirjutamine_märk_VALUE(10);
            return;
        }
        if (Käsk == 182 && Word_SMS(omanik_VALUE, "java/lang/String")) {
            if (Word_SMS(Nimi_2, "length") && Word_SMS(vorming_VALUE, "()I")) {
                int viide = 빼기(2); if (objekt_VALUE(viide, 1)) 넣기(힙[viide + 1], 1); return;
            }
            if (Word_SMS(Nimi_2, "charAt") && Word_SMS(vorming_VALUE, "(I)C")) {
                int allindeks_VALUE = 빼기(1), viide = 빼기(2);
                if (objekt_VALUE(viide, 1)) {
                    if (allindeks_VALUE < 0 || allindeks_VALUE >= 힙[viide + 1]) tõrge_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[viide + 2 + allindeks_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(omanik_VALUE, "java/lang/StringBuilder")) {
            if (Käsk == 183 && Word_SMS(Nimi_2, "<init>") && Word_SMS(vorming_VALUE, "()V")) { objekt_VALUE(빼기(2), 4); return; }
            if (Käsk == 182 && Word_SMS(Nimi_2, "toString") && Word_SMS(vorming_VALUE, "()Ljava/lang/String;")) {
                int viide = 빼기(2); if (objekt_VALUE(viide, 4)) 넣기(힙[viide + 2] == 0 ? host_märk("") : 힙[viide + 2], 2); return;
            }
            if (Käsk == 182 && Word_SMS(Nimi_2, "append")) {
                int Tekst = 0;
                if (Word_SMS(vorming_VALUE, "(I)Ljava/lang/StringBuilder;")) Tekst = number_märk(빼기(1));
                else if (Word_SMS(vorming_VALUE, "(Z)Ljava/lang/StringBuilder;")) Tekst = host_märk(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(vorming_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Tekst = lisama_salvesti(1, 1); if (!VIGA) 힙[Tekst + 2] = VALUE & 65535;
                }
                else if (Word_SMS(vorming_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = host_märk("null"); }
                else { tõrge_VALUE("unsupported StringBuilder append"); return; }
                int viide = 빼기(2); if (!objekt_VALUE(viide, 4) || !objekt_VALUE(Tekst, 1)) return;
                int esikaamera_VALUE = 힙[viide + 2], 앞길이 = esikaamera_VALUE == 0 ? 0 : 힙[esikaamera_VALUE + 1], 뒤길이 = 힙[Tekst + 1];
                int 새글 = lisama_salvesti(1, 앞길이 + 뒤길이); if (VIGA) return;
                for (int number = 0; number < 앞길이; number++) 힙[새글 + 2 + number] = 힙[esikaamera_VALUE + 2 + number];
                for (int number = 0; number < 뒤길이; number++) 힙[새글 + 2 + 앞길이 + number] = 힙[Tekst + 2 + number];
                힙[viide + 2] = 새글; 넣기(viide, 2); return;
            }
        }
        tõrge_VALUE("unsupported library method");
    }
    static int 배열칸(int viide, int allindeks_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(viide, TYPE_VALUE)) return 0;
        if (allindeks_VALUE < 0 || allindeks_VALUE >= 힙[viide + 1]) { tõrge_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return viide + 2 + allindeks_VALUE;
    }
    static void Täida_käsk() {
        int 남음 = 500000;
        while (raam_INDEX >= 0 && !VIGA) {
            if (--남음 == 0) { tõrge_VALUE("instruction limit (500000)"); break; }
            int Käivita_2 = raam_ametikoht[raam_INDEX], VALUE = 명바();
            if (VIGA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int number = VALUE == 18 ? 명바() : 명짧();
                if (number <= 0 || number >= konstant_COUNT) tõrge_VALUE("invalid ldc constant");
                else if (konstant_silt[number] == 3) 넣기(상가[number], 1);
                else if (konstant_silt[number] == 8) 넣기(konstant_SMS(상가[number]), 2);
                else tõrge_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { kirjutamine_kohalik(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { kirjutamine_kohalik(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { kirjutamine_kohalik(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int allindeks_VALUE = 빼기(1), viide = 빼기(2), 칸 = 배열칸(viide, allindeks_VALUE, VALUE == 46 ? 2 : 3);
                if (!VIGA) 넣기(힙[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int kaup_element = 빼기(VALUE == 79 ? 1 : 2), allindeks_VALUE = 빼기(1), viide = 빼기(2), 칸 = 배열칸(viide, allindeks_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && kaup_element != 0) objekt_VALUE(kaup_element, 1);
                if (!VIGA) 힙[칸] = kaup_element; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = tagasi_saatma_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = tagasi_saatma_TYPE, SECOND_operand = 빼기(0), SECOND_operand_TYPE = tagasi_saatma_TYPE; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_TYPE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), TULEMUS = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { tõrge_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) TULEMUS = 가 + SECOND_operand;
                if (VALUE == 100) TULEMUS = 가 - SECOND_operand;
                if (VALUE == 104) TULEMUS = 가 * SECOND_operand;
                if (VALUE == 108) TULEMUS = 가 / SECOND_operand;
                if (VALUE == 112) TULEMUS = 가 % SECOND_operand;
                if (VALUE == 120) TULEMUS = 가 << SECOND_operand;
                if (VALUE == 122) TULEMUS = 가 >> SECOND_operand;
                if (VALUE == 124) TULEMUS = 가 >>> SECOND_operand;
                if (VALUE == 126) TULEMUS = 가 & SECOND_operand;
                if (VALUE == 128) TULEMUS = 가 | SECOND_operand;
                if (VALUE == 130) TULEMUS = 가 ^ SECOND_operand;
                넣기(TULEMUS, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int kohalik_skoop = 명바(), samm_samm = (byte)명바(); 지역읽기(kohalik_skoop, 1); 넣기(빼기(1) + samm_samm, 1); kirjutamine_kohalik(kohalik_skoop, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int number = 빼기(1); 넣기(VALUE == 145 ? (byte)number : VALUE == 146 ? (char)number : (short)number, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int sihtkoht_VALUE = Käivita_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int number = 빼기(1); 갈까 = VALUE == 153 ? number == 0 : VALUE == 154 ? number != 0 : VALUE == 155 ? number < 0 : VALUE == 156 ? number >= 0 : VALUE == 157 ? number > 0 : number <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int number = 빼기(2); 갈까 = VALUE == 198 ? number == 0 : number != 0; }
                if (갈까) liigutama_VALUE(sihtkoht_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { tagasi_saatma_näitaja(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int number = 명짧(); if (!tšekk_konstant(number, 9)) continue;
                if (!Word_SMS(klassinimi_SMS(상가[number]), "java/lang/System") || !Word_SMS(viide_nimetus(konstant_SECOND_VALUE[number]), "out")
                    || !Word_SMS(viide_TYPE(konstant_SECOND_VALUE[number]), "Ljava/io/PrintStream;")) tõrge_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_meetod(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Nimi_2 = klassinimi_SMS(명짧());
                if (Word_SMS(Nimi_2, "java/lang/StringBuilder")) 넣기(lisama_salvesti(4, 1), 2);
                else if (Word_SMS(Nimi_2, "java/io/FileInputStream") || Word_SMS(Nimi_2, "java/io/FileOutputStream")) {
                    int viide = lisama_salvesti(Word_SMS(Nimi_2, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!VIGA) { 힙[viide + 2] = -1; 넣기(viide, 2); }
                } else tõrge_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) tõrge_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(klassinimi_SMS(명짧()), "java/lang/String")) tõrge_VALUE("only String[] anewarray is supported");
                int 길이 = 빼기(1); 넣기(lisama_salvesti(VALUE == 188 ? 2 : 3, 길이), 2); continue;
            }
            if (VALUE == 190) {
                int viide = 빼기(2);
                if (viide < 1 || viide >= 힙끝 - 1 || (힙[viide] != 2 && 힙[viide] != 3)) tõrge_VALUE("null or invalid array");
                else 넣기(힙[viide + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Nimi_2 = klassinimi_SMS(명짧()), viide = 빼기(2);
                if (!Word_SMS(Nimi_2, "java/lang/String")) tõrge_VALUE("unsupported checkcast");
                else if (viide != 0) objekt_VALUE(viide, 1);
                넣기(viide, 2); continue;
            }
            tõrge_VALUE("unsupported bytecode");
        }
    }
    public static int Käivita_2() {
        if (kasutaja.인수개수() == 1 && 자바도구.같음(kasutaja.Argumendid(0), "-version")) {
            kasutaja.Kirjutamine("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (kasutaja.인수개수() < 1) { kasutaja.Kirjutamine("Usage: java CLASS [ARGS]\n"); return 2; }
        int 길이 = 자바도구.Nimi_2(failinimi_SMS, kasutaja.Argumendid(0));
        if (길이 < 1 || 길이 > 57) { kasutaja.Kirjutamine("java: invalid class name\n"); return 2; }
        failinimi_SMS[길이] = '.'; failinimi_SMS[길이 + 1] = 'c'; failinimi_SMS[길이 + 2] = 'l'; failinimi_SMS[길이 + 3] = 'a'; failinimi_SMS[길이 + 4] = 's'; failinimi_SMS[길이 + 5] = 's';
        Suurus = kasutaja.파일읽기(failinimi_SMS, Fail);
        if (Suurus < 0) { kasutaja.Kirjutamine("java: cannot read class: "); 자바도구.kirjutamine_number(Suurus); kasutaja.kirjutamine_märk_VALUE(10); return 1; }
        클래스읽기(); if (VIGA) return 1;
        int märk_nimetus = konstant_SMS(klassinimi);
        if (!VIGA && 힙[märk_nimetus + 1] != 길이) tõrge_VALUE("class name does not match file");
        for (int number = 0; number < 길이 && !VIGA; number++) if (힙[märk_nimetus + 2 + number] != failinimi_SMS[number]) tõrge_VALUE("class name does not match file");
        int kirje_p_VALUE = -1;
        for (int number = 0; number < meetod_COUNT; number++) if (Word_SMS(meetod_nimetus_SMS[number], "main") && Word_SMS(meetod_TYPE[number], "([Ljava/lang/String;)V") && (meetod_pöördus[number] & 9) == 9) kirje_p_VALUE = number;
        if (kirje_p_VALUE < 0) tõrge_VALUE("public static void main(String[] args) required");
        if (VIGA) return 1;
        int Argumendid = lisama_salvesti(3, kasutaja.인수개수() - 1);
        for (int number = 1; number < kasutaja.인수개수() && !VIGA; number++) 힙[Argumendid + 1 + number] = host_märk(kasutaja.Argumendid(number));
        raam_INDEX = 0; raam_meetod[0] = kirje_p_VALUE; raam_ametikoht[0] = meetod_START[kirje_p_VALUE]; kohalik_VALUE[0] = Argumendid; kohalik_TYPE[0] = 2;
        Täida_käsk(); return VIGA ? 1 : 0;
    }
}
