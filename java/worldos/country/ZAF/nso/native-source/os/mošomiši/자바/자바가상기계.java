// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Faele/스택/Dipadišo/lekala 경계를 phethagatša_taelo 중 검사한다. */
public final class 자바가상기계 {
    static int[] Faele = new int[16384], faele_leina_SMS = new int[64];
    static int[] ya_go_se_fetoge_leswao = new int[512], 상가 = new int[512], 상나 = new int[512], molokoloko_Dipadišo = new int[512];
    static int[] mokgwa_leina_SMS = new int[32], mokgwa_thaepa = new int[32], mokgwa_fihlelela = new int[32];
    static int[] mokgwa_Thomišo = new int[32], mokgwa_fetša = new int[32], mokgwa_kgoboko = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], mokgwa_akumente_thaepa = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] kgauswi_boleng = new int[4096], kgauswi_thaepa = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] freime_mokgwa = new int[32], 틀위치 = new int[32], freime_kgoboko = new int[32];
    static int[] 힙 = new int[8192];
    static int Bogolo, 읽기위치, 상수수, 함수수, legoro_leina, freime_lokela = -1, 힙끝 = 1, 반환형;
    static boolean Phošo;

    static void go_palelwa_boleng(String Thalokontšu_SMS) {
        if (!Phošo) { mošomiši.Ngwala("JVM error: "); mošomiši.Ngwala(Thalokontšu_SMS); mošomiši.ngwala_tlhaka_boleng(10); }
        Phošo = true;
    }
    static boolean setsopolwa(int Diriša, int botelele_boleng) { return Diriša >= 0 && botelele_boleng >= 0 && Diriša <= Bogolo - botelele_boleng; }
    static int paete_boleng() {
        if (!setsopolwa(읽기위치, 1)) { go_palelwa_boleng("truncated class file"); return 0; }
        return Faele[읽기위치++];
    }
    static int 짧은수() { return paete_boleng() << 8 | paete_boleng(); }
    static int palotlalo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int botelele_boleng) { if (!setsopolwa(읽기위치, botelele_boleng)) go_palelwa_boleng("invalid attribute size"); else 읽기위치 += botelele_boleng; }
    static boolean lekola_ya_go_se_fetoge(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || ya_go_se_fetoge_leswao[수] != 종류) { go_palelwa_boleng("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Diriša, int botelele_boleng, String Thalokontšu_SMS) {
        if (!setsopolwa(Diriša, botelele_boleng) || botelele_boleng != Thalokontšu_SMS.length()) return false;
        for (int 수 = 0; 수 < botelele_boleng; 수++) if (Faele[Diriša + 수] != Thalokontšu_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Thalokontšu_SMS(int ya_go_se_fetoge_boleng, String Thalokontšu_SMS) { return lekola_ya_go_se_fetoge(ya_go_se_fetoge_boleng, 1) && 구간(상가[ya_go_se_fetoge_boleng], 상나[ya_go_se_fetoge_boleng], Thalokontšu_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!lekola_ya_go_se_fetoge(가, 1) || !lekola_ya_go_se_fetoge(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Faele[상가[가] + 수] != Faele[상가[나] + 수]) return false;
        return true;
    }
    static int legoro_leina_SMS(int 수) { return lekola_ya_go_se_fetoge(수, 7) && lekola_ya_go_se_fetoge(상가[수], 1) ? 상가[수] : 0; }
    static int Dipadišo_leina(int 수) { return lekola_ya_go_se_fetoge(수, 12) && lekola_ya_go_se_fetoge(상가[수], 1) ? 상가[수] : 0; }
    static int Dipadišo_thaepa(int 수) { return lekola_ya_go_se_fetoge(수, 12) && lekola_ya_go_se_fetoge(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean hloka_selo_thaepa) {
        if (읽기위치 >= 끝) { go_palelwa_boleng("invalid descriptor"); return 0; }
        int boleng = paete_boleng();
        if (boleng == 'V' && hloka_selo_thaepa) return 0;
        if (boleng == 'I' || boleng == 'B' || boleng == 'C' || boleng == 'S' || boleng == 'Z') return 1;
        if (boleng == '[') { 서술형(끝, false); return 2; }
        if (boleng == 'L') {
            int Diriša = 읽기위치;
            while (읽기위치 < 끝 && Faele[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Diriša) go_palelwa_boleng("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        go_palelwa_boleng("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int TIRO_boleng) {
        int 이전 = 읽기위치, 수 = mokgwa_thaepa[TIRO_boleng];
        if (!lekola_ya_go_se_fetoge(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (paete_boleng() != '(') go_palelwa_boleng("invalid method descriptor");
        int 개수 = 0;
        while (!Phošo && 읽기위치 < 끝 && Faele[읽기위치] != ')') {
            if (개수 == 16) { go_palelwa_boleng("too many method arguments"); break; }
            mokgwa_akumente_thaepa[TIRO_boleng * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || paete_boleng() != ')') go_palelwa_boleng("invalid method descriptor");
        함수반환[TIRO_boleng] = 서술형(끝, true); 함수인수수[TIRO_boleng] = 개수;
        if (읽기위치 != 끝) go_palelwa_boleng("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Phošo; 수++) { lekola_ya_go_se_fetoge(짧은수(), 1); 건너(palotlalo()); }
    }
    static int taelo_botelele(int boleng) {
        if (boleng == 16 || boleng == 18 || boleng == 21 || boleng == 25 || boleng == 54 || boleng == 58 || boleng == 188) return 2;
        if (boleng == 17 || boleng == 19 || boleng == 132 || boleng >= 153 && boleng <= 167
            || boleng >= 178 && boleng <= 184 || boleng == 187 || boleng == 189 || boleng == 192 || boleng == 198 || boleng == 199) return 3;
        if (boleng >= 0 && boleng <= 8 || boleng >= 26 && boleng <= 29 || boleng >= 42 && boleng <= 46 || boleng == 50
            || boleng >= 59 && boleng <= 62 || boleng >= 75 && boleng <= 79 || boleng == 83 || boleng == 87 || boleng == 89 || boleng == 95
            || boleng == 96 || boleng == 100 || boleng == 104 || boleng == 108 || boleng == 112 || boleng == 116
            || boleng == 120 || boleng == 122 || boleng == 124 || boleng == 126 || boleng == 128 || boleng == 130
            || boleng >= 145 && boleng <= 147 || boleng == 172 || boleng == 176 || boleng == 177 || boleng == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (palotlalo() != 0xcafebabe) go_palelwa_boleng("not a class file");
        int 부판 = 짧은수(), bešene_boleng = 짧은수();
        if (bešene_boleng < 45 || bešene_boleng > 52 || 부판 != 0) go_palelwa_boleng("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { go_palelwa_boleng("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !Phošo; 수++) {
            int 종류 = paete_boleng(); ya_go_se_fetoge_leswao[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = palotlalo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else go_palelwa_boleng("unsupported constant type");
        }
        int tumelelo_boleng = 짧은수();
        if ((tumelelo_boleng & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) go_palelwa_boleng("unsupported class flags");
        legoro_leina = legoro_leina_SMS(짧은수());
        if (!Thalokontšu_SMS(legoro_leina_SMS(짧은수()), "java/lang/Object")) go_palelwa_boleng("inheritance unsupported");
        if (짧은수() != 0) go_palelwa_boleng("interfaces unsupported");
        if (짧은수() != 0) go_palelwa_boleng("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { go_palelwa_boleng("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !Phošo; 수++) {
            mokgwa_fihlelela[수] = 짧은수(); mokgwa_leina_SMS[수] = 짧은수(); mokgwa_thaepa[수] = 짧은수();
            lekola_ya_go_se_fetoge(mokgwa_leina_SMS[수], 1); 서술읽기(수);
            if ((mokgwa_fihlelela[수] & (0x100 | 0x400 | 0x20)) != 0) go_palelwa_boleng("native, abstract and synchronized methods unsupported");
            if ((mokgwa_fihlelela[수] & 8) == 0 && !Thalokontšu_SMS(mokgwa_leina_SMS[수], "<init>")) go_palelwa_boleng("instance methods unsupported");
            if (Thalokontšu_SMS(mokgwa_leina_SMS[수], "<clinit>")) go_palelwa_boleng("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(mokgwa_leina_SMS[앞], mokgwa_leina_SMS[수]) && 같은말(mokgwa_thaepa[앞], mokgwa_thaepa[수])) go_palelwa_boleng("duplicate method");
            int 개수 = 짧은수();
            for (int tlhaodi_ya_faele_boleng = 0; tlhaodi_ya_faele_boleng < 개수 && !Phošo; tlhaodi_ya_faele_boleng++) {
                int Leina = 짧은수(), botelele_boleng = palotlalo(), Diriša = 읽기위치;
                if (!setsopolwa(Diriša, botelele_boleng)) { go_palelwa_boleng("truncated method attribute"); break; }
                if (Thalokontšu_SMS(Leina, "Code")) {
                    if (mokgwa_Thomišo[수] != 0) go_palelwa_boleng("duplicate Code attribute");
                    mokgwa_kgoboko[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = palotlalo();
                    if (mokgwa_kgoboko[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) go_palelwa_boleng("method memory limits exceeded");
                    mokgwa_Thomišo[수] = 읽기위치; 건너(코드길이); mokgwa_fetša[수] = 읽기위치;
                    if (짧은수() != 0) go_palelwa_boleng("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Diriša + botelele_boleng) go_palelwa_boleng("Code attribute size mismatch");
                } else 건너(botelele_boleng);
            }
            if (mokgwa_Thomišo[수] == 0) go_palelwa_boleng("missing Code attribute");
            int sekgobana_go_tsenya_tshedimošo = mokgwa_Thomišo[수];
            while (sekgobana_go_tsenya_tshedimošo < mokgwa_fetša[수] && !Phošo) {
                int botelele_boleng = taelo_botelele(Faele[sekgobana_go_tsenya_tshedimošo]);
                if (botelele_boleng == 0 || botelele_boleng > mokgwa_fetša[수] - sekgobana_go_tsenya_tshedimošo) { go_palelwa_boleng("unsupported or truncated bytecode"); break; }
                경계[sekgobana_go_tsenya_tshedimošo] = 수 + 1; sekgobana_go_tsenya_tshedimošo += botelele_boleng;
            }
            // 실행하지 않는 경로에도 잘못된 lekala 목적지를 허용하지 않는다.
            sekgobana_go_tsenya_tshedimošo = mokgwa_Thomišo[수];
            while (sekgobana_go_tsenya_tshedimošo < mokgwa_fetša[수] && !Phošo) {
                int boleng = Faele[sekgobana_go_tsenya_tshedimošo];
                if (boleng >= 153 && boleng <= 167 || boleng == 198 || boleng == 199) {
                    int boyo_boleng = sekgobana_go_tsenya_tshedimošo + (short)(Faele[sekgobana_go_tsenya_tshedimošo + 1] << 8 | Faele[sekgobana_go_tsenya_tshedimošo + 2]);
                    if (boyo_boleng < mokgwa_Thomišo[수] || boyo_boleng >= mokgwa_fetša[수] || 경계[boyo_boleng] != 수 + 1) go_palelwa_boleng("invalid branch target");
                }
                sekgobana_go_tsenya_tshedimošo += taelo_botelele(boleng);
            }
        }
        if (!Phošo) 속성건너();
        if (읽기위치 != Bogolo) go_palelwa_boleng("extra class file data");
    }
    static int aba_Bobolokelo(int 종류, int botelele_boleng) {
        if (botelele_boleng < 0 || botelele_boleng > 힙.length - 힙끝 - 2) { go_palelwa_boleng("object heap exhausted or negative array size"); return 0; }
        int Dipadišo = 힙끝; 힙끝 += botelele_boleng + 2; 힙[Dipadišo] = 종류; 힙[Dipadišo + 1] = botelele_boleng;
        return Dipadišo;
    }
    static boolean selo_boleng(int Dipadišo, int 종류) {
        if (Dipadišo < 1 || Dipadišo >= 힙끝 - 1 || 힙[Dipadišo] != 종류) { go_palelwa_boleng("null or invalid object reference"); return false; }
        return true;
    }
    static int ya_go_se_fetoge_SMS(int lokela) {
        if (!lekola_ya_go_se_fetoge(lokela, 1)) return 0;
        if (molokoloko_Dipadišo[lokela] != 0) return molokoloko_Dipadišo[lokela];
        int Dipadišo = aba_Bobolokelo(1, 상나[lokela]); if (Phošo) return 0;
        int 끝 = 상가[lokela] + 상나[lokela], 수 = 상가[lokela], botelele_boleng = 0;
        while (수 < 끝 && !Phošo) {
            int boleng = Faele[수++];
            if (boleng == 0) go_palelwa_boleng("invalid modified UTF-8");
            else if (boleng >= 192 && boleng <= 223 && 수 < 끝) {
                int 다음 = Faele[수++];
                if ((다음 & 192) != 128) go_palelwa_boleng("invalid modified UTF-8");
                boleng = (boleng & 31) << 6 | 다음 & 63;
                if (boleng != 0 && boleng < 128) go_palelwa_boleng("overlong modified UTF-8");
            } else if (boleng >= 224 && boleng <= 239 && 수 + 1 < 끝) {
                int 가 = Faele[수++], 나 = Faele[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) go_palelwa_boleng("invalid modified UTF-8");
                boleng = (boleng & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (boleng < 2048) go_palelwa_boleng("overlong modified UTF-8");
            } else if (boleng >= 128) go_palelwa_boleng("invalid modified UTF-8");
            힙[Dipadišo + 2 + botelele_boleng++] = boleng;
        }
        힙[Dipadišo + 1] = botelele_boleng; molokoloko_Dipadišo[lokela] = Dipadišo; return Dipadišo;
    }
    static int go_nea_ditirelo_tlhaka(String boleng) {
        int Dipadišo = aba_Bobolokelo(1, boleng.length()); if (Phošo) return 0;
        for (int 수 = 0; 수 < boleng.length(); 수++) 힙[Dipadišo + 2 + 수] = boleng.charAt(수);
        return Dipadišo;
    }
    static void ngwala_SMS(int Dipadišo) {
        if (Dipadišo == 0) { mošomiši.Ngwala("null"); return; }
        if (!selo_boleng(Dipadišo, 1)) return;
        for (int 수 = 0; 수 < 힙[Dipadišo + 1]; 수++) mošomiši.ngwala_tlhaka_boleng(힙[Dipadišo + 2 + 수]);
    }
    static int 수문자(int boleng) {
        int Dipadišo = aba_Bobolokelo(1, 11); if (Phošo) return 0;
        int botelele_boleng = 0;
        if (boleng < 0) 힙[Dipadišo + 2 + botelele_boleng++] = '-'; else boleng = -boleng;
        int 자리 = 1000000000; boolean Diriša = false;
        while (자리 != 0) {
            int 수 = -(boleng / 자리);
            if (수 != 0 || Diriša || 자리 == 1) { 힙[Dipadišo + 2 + botelele_boleng++] = '0' + 수; Diriša = true; }
            boleng %= 자리; 자리 /= 10;
        }
        힙[Dipadišo + 1] = botelele_boleng; return Dipadišo;
    }
    static int 정수해독(int Dipadišo) {
        if (!selo_boleng(Dipadišo, 1)) return 0;
        int botelele_boleng = 힙[Dipadišo + 1], 수 = 0, boleng = 0; boolean 음수 = false;
        if (botelele_boleng > 0 && (힙[Dipadišo + 2] == '-' || 힙[Dipadišo + 2] == '+')) { 음수 = 힙[Dipadišo + 2] == '-'; 수++; }
        if (수 == botelele_boleng) go_palelwa_boleng("NumberFormatException");
        for (; 수 < botelele_boleng && !Phošo; 수++) {
            int 숫자 = 힙[Dipadišo + 2 + 수] - '0';
            if (숫자 < 0 || 숫자 > 9 || boleng < -214748364 || boleng == -214748364 && 숫자 > (음수 ? 8 : 7)) go_palelwa_boleng("NumberFormatException");
            boleng = boleng * 10 - 숫자;
        }
        return 음수 ? boleng : -boleng;
    }
    static void 넣기(int boleng, int thaepa_boleng) {
        if (Phošo) return;
        if (freime_lokela < 0 || freime_kgoboko[freime_lokela] >= mokgwa_kgoboko[freime_mokgwa[freime_lokela]]) { go_palelwa_boleng("operand stack overflow"); return; }
        int sekgobana_go_tsenya_tshedimošo = freime_lokela * 128 + freime_kgoboko[freime_lokela]++; 스택값[sekgobana_go_tsenya_tshedimošo] = boleng; 스택형[sekgobana_go_tsenya_tshedimošo] = thaepa_boleng;
    }
    static int 빼기(int thaepa_boleng) {
        if (Phošo) return 0;
        if (freime_lokela < 0 || freime_kgoboko[freime_lokela] < 1) { go_palelwa_boleng("operand stack underflow"); return 0; }
        int sekgobana_go_tsenya_tshedimošo = freime_lokela * 128 + --freime_kgoboko[freime_lokela]; 반환형 = 스택형[sekgobana_go_tsenya_tshedimošo];
        if (thaepa_boleng != 0 && 반환형 != thaepa_boleng) go_palelwa_boleng("operand type mismatch");
        return 스택값[sekgobana_go_tsenya_tshedimošo];
    }
    static void 지역읽기(int lokela, int thaepa_boleng) {
        if (lokela >= 함수지역[freime_mokgwa[freime_lokela]] || lokela < 0 || kgauswi_thaepa[freime_lokela * 128 + lokela] != thaepa_boleng) { go_palelwa_boleng("invalid or uninitialized local"); return; }
        넣기(kgauswi_boleng[freime_lokela * 128 + lokela], thaepa_boleng);
    }
    static void ngwala_kgauswi(int lokela, int thaepa_boleng) {
        if (lokela >= 함수지역[freime_mokgwa[freime_lokela]] || lokela < 0) { go_palelwa_boleng("local index out of range"); return; }
        int boleng = 빼기(thaepa_boleng); kgauswi_boleng[freime_lokela * 128 + lokela] = boleng; kgauswi_thaepa[freime_lokela * 128 + lokela] = thaepa_boleng;
    }
    static int 명바() {
        int 위치 = 틀위치[freime_lokela];
        if (위치 < mokgwa_Thomišo[freime_mokgwa[freime_lokela]] || 위치 >= mokgwa_fetša[freime_mokgwa[freime_lokela]]) { go_palelwa_boleng("instruction pointer out of range"); return 0; }
        틀위치[freime_lokela]++; return Faele[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void šuthiša_boleng(int 위치) {
        int TIRO_boleng = freime_mokgwa[freime_lokela];
        if (위치 < mokgwa_Thomišo[TIRO_boleng] || 위치 >= mokgwa_fetša[TIRO_boleng] || 경계[위치] != TIRO_boleng + 1) go_palelwa_boleng("invalid branch target");
        else 틀위치[freime_lokela] = 위치;
    }
    static void 호출(int TIRO_boleng) {
        if (freime_lokela == 31) { go_palelwa_boleng("call stack limit (32)"); return; }
        int 다음 = freime_lokela + 1;
        for (int 수 = 0; 수 < 128; 수++) kgauswi_thaepa[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[TIRO_boleng] - 1; 수 >= 0; 수--) {
            kgauswi_boleng[다음 * 128 + 수] = 빼기(mokgwa_akumente_thaepa[TIRO_boleng * 16 + 수]); kgauswi_thaepa[다음 * 128 + 수] = mokgwa_akumente_thaepa[TIRO_boleng * 16 + 수];
        }
        freime_lokela = 다음; freime_mokgwa[freime_lokela] = TIRO_boleng; 틀위치[freime_lokela] = mokgwa_Thomišo[TIRO_boleng]; freime_kgoboko[freime_lokela] = 0;
    }
    static void 반환(int thaepa_boleng) {
        if (thaepa_boleng != 함수반환[freime_mokgwa[freime_lokela]]) { go_palelwa_boleng("return type mismatch"); return; }
        int boleng = thaepa_boleng == 0 ? 0 : 빼기(thaepa_boleng);
        freime_lokela--; if (freime_lokela >= 0 && thaepa_boleng != 0) 넣기(boleng, thaepa_boleng);
    }
    static int[] Stream_faele_leina = new int[64];
    static void faele_Stream_founa(int mong_boleng, int Leina, int fomete_boleng, int Taelo) {
        boolean 출력 = Thalokontšu_SMS(mong_boleng, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Taelo == 183 && Thalokontšu_SMS(Leina, "<init>")) {
            boolean 이어 = false;
            if (출력 && Thalokontšu_SMS(fomete_boleng, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Thalokontšu_SMS(fomete_boleng, "(Ljava/lang/String;)V")) { go_palelwa_boleng("unsupported file stream constructor"); return; }
            int faele_go_tsenya_tshedimošo_leina = 빼기(2), Stream_boleng = 빼기(2);
            if (!selo_boleng(faele_go_tsenya_tshedimošo_leina, 1) || !selo_boleng(Stream_boleng, 종류) || Phošo) return;
            if (힙[Stream_boleng + 3] != 0) { go_palelwa_boleng("file stream already initialized"); return; }
            int botelele_boleng = 힙[faele_go_tsenya_tshedimošo_leina + 1];
            if (botelele_boleng < 1 || botelele_boleng > 63) { go_palelwa_boleng("invalid file name length"); return; }
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < botelele_boleng; sekgobana_go_tsenya_tshedimošo++) {
                int boleng = 힙[faele_go_tsenya_tshedimošo_leina + 2 + sekgobana_go_tsenya_tshedimošo];
                if (boleng < 1 || boleng > 127) { go_palelwa_boleng("file stream paths currently require ASCII"); return; }
                Stream_faele_leina[sekgobana_go_tsenya_tshedimošo] = boleng;
            }
            Stream_faele_leina[botelele_boleng] = 0;
            int 서술자 = mošomiši.파일서술자열기(Stream_faele_leina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { go_palelwa_boleng("FileNotFoundException: file open failed"); return; }
            힙[Stream_boleng + 2] = 서술자; 힙[Stream_boleng + 3] = 1;
            return;
        }
        if (Taelo != 182) { go_palelwa_boleng("invalid file stream invocation"); return; }
        int Mogato = -1, boleng = 0;
        if (Thalokontšu_SMS(Leina, "close") && Thalokontšu_SMS(fomete_boleng, "()V")) Mogato = 0;
        if (!출력 && Thalokontšu_SMS(Leina, "read") && Thalokontšu_SMS(fomete_boleng, "()I")) Mogato = 1;
        if (출력 && Thalokontšu_SMS(Leina, "write") && Thalokontšu_SMS(fomete_boleng, "(I)V")) { Mogato = 2; boleng = 빼기(1); }
        if (Mogato < 0) { go_palelwa_boleng("unsupported file stream method"); return; }
        int Stream_boleng = 빼기(2);
        if (!selo_boleng(Stream_boleng, 종류) || Phošo) return;
        if (힙[Stream_boleng + 3] == 0) { go_palelwa_boleng("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_boleng + 2];
        if (Mogato == 0) {
            if (서술자 >= 0 && mošomiši.파일서술자닫기(서술자) < 0) go_palelwa_boleng("IOException: close failed");
            힙[Stream_boleng + 2] = -1; return;
        }
        if (서술자 < 0) { go_palelwa_boleng("IOException: stream closed"); return; }
        if (Mogato == 1) {
            int 결과 = mošomiši.파일한바이트읽기(서술자);
            if (결과 < -1) go_palelwa_boleng("IOException: read failed"); else 넣기(결과, 1);
        } else if (mošomiši.파일한바이트쓰기(서술자, boleng) != 1) go_palelwa_boleng("IOException: write failed");
    }
    static void founa_mokgwa(int lokela, int Taelo) {
        if (!lekola_ya_go_se_fetoge(lokela, 10)) return;
        int mong_boleng = legoro_leina_SMS(상가[lokela]), Leina = Dipadišo_leina(상나[lokela]), fomete_boleng = Dipadišo_thaepa(상나[lokela]);
        if (Phošo) return;
        if (같은말(mong_boleng, legoro_leina)) {
            if (Taelo != 184) { go_palelwa_boleng("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Leina, mokgwa_leina_SMS[수]) && 같은말(fomete_boleng, mokgwa_thaepa[수])) {
                if ((mokgwa_fihlelela[수] & 8) == 0) go_palelwa_boleng("method is not static"); else 호출(수);
                return;
            }
            go_palelwa_boleng("NoSuchMethodError"); return;
        }
        if (Thalokontšu_SMS(mong_boleng, "java/io/FileInputStream") || Thalokontšu_SMS(mong_boleng, "java/io/FileOutputStream")) {
            faele_Stream_founa(mong_boleng, Leina, fomete_boleng, Taelo); return;
        }
        if (Taelo == 184 && Thalokontšu_SMS(mong_boleng, "java/lang/Integer") && Thalokontšu_SMS(Leina, "parseInt") && Thalokontšu_SMS(fomete_boleng, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Taelo == 182 && Thalokontšu_SMS(mong_boleng, "java/io/PrintStream") && (Thalokontšu_SMS(Leina, "println") || Thalokontšu_SMS(Leina, "print"))) {
            int thaepa_boleng = 0, boleng = 0;
            if (Thalokontšu_SMS(fomete_boleng, "(I)V")) { thaepa_boleng = 1; boleng = 빼기(1); }
            else if (Thalokontšu_SMS(fomete_boleng, "(Z)V")) { thaepa_boleng = 2; boleng = 빼기(1); }
            else if (Thalokontšu_SMS(fomete_boleng, "(C)V")) { thaepa_boleng = 3; boleng = 빼기(1); }
            else if (Thalokontšu_SMS(fomete_boleng, "(Ljava/lang/String;)V")) { thaepa_boleng = 4; boleng = 빼기(2); }
            else if (!Thalokontšu_SMS(fomete_boleng, "()V") || !Thalokontšu_SMS(Leina, "println")) go_palelwa_boleng("unsupported print descriptor");
            if (빼기(2) != -1) go_palelwa_boleng("invalid PrintStream receiver");
            if (Phošo) return;
            if (thaepa_boleng == 1) 자바도구.수쓰기(boleng);
            if (thaepa_boleng == 2) mošomiši.Ngwala(boleng == 0 ? "false" : "true");
            if (thaepa_boleng == 3) mošomiši.ngwala_tlhaka_boleng(boleng & 65535);
            if (thaepa_boleng == 4) ngwala_SMS(boleng);
            if (Thalokontšu_SMS(Leina, "println")) mošomiši.ngwala_tlhaka_boleng(10);
            return;
        }
        if (Taelo == 182 && Thalokontšu_SMS(mong_boleng, "java/lang/String")) {
            if (Thalokontšu_SMS(Leina, "length") && Thalokontšu_SMS(fomete_boleng, "()I")) {
                int Dipadišo = 빼기(2); if (selo_boleng(Dipadišo, 1)) 넣기(힙[Dipadišo + 1], 1); return;
            }
            if (Thalokontšu_SMS(Leina, "charAt") && Thalokontšu_SMS(fomete_boleng, "(I)C")) {
                int sapskripte_boleng = 빼기(1), Dipadišo = 빼기(2);
                if (selo_boleng(Dipadišo, 1)) {
                    if (sapskripte_boleng < 0 || sapskripte_boleng >= 힙[Dipadišo + 1]) go_palelwa_boleng("StringIndexOutOfBoundsException"); else 넣기(힙[Dipadišo + 2 + sapskripte_boleng], 1);
                }
                return;
            }
        }
        if (Thalokontšu_SMS(mong_boleng, "java/lang/StringBuilder")) {
            if (Taelo == 183 && Thalokontšu_SMS(Leina, "<init>") && Thalokontšu_SMS(fomete_boleng, "()V")) { selo_boleng(빼기(2), 4); return; }
            if (Taelo == 182 && Thalokontšu_SMS(Leina, "toString") && Thalokontšu_SMS(fomete_boleng, "()Ljava/lang/String;")) {
                int Dipadišo = 빼기(2); if (selo_boleng(Dipadišo, 4)) 넣기(힙[Dipadišo + 2] == 0 ? go_nea_ditirelo_tlhaka("") : 힙[Dipadišo + 2], 2); return;
            }
            if (Taelo == 182 && Thalokontšu_SMS(Leina, "append")) {
                int Sengwalwa = 0;
                if (Thalokontšu_SMS(fomete_boleng, "(I)Ljava/lang/StringBuilder;")) Sengwalwa = 수문자(빼기(1));
                else if (Thalokontšu_SMS(fomete_boleng, "(Z)Ljava/lang/StringBuilder;")) Sengwalwa = go_nea_ditirelo_tlhaka(빼기(1) == 0 ? "false" : "true");
                else if (Thalokontšu_SMS(fomete_boleng, "(C)Ljava/lang/StringBuilder;")) {
                    int boleng = 빼기(1); Sengwalwa = aba_Bobolokelo(1, 1); if (!Phošo) 힙[Sengwalwa + 2] = boleng & 65535;
                }
                else if (Thalokontšu_SMS(fomete_boleng, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Sengwalwa = 빼기(2); if (Sengwalwa == 0) Sengwalwa = go_nea_ditirelo_tlhaka("null"); }
                else { go_palelwa_boleng("unsupported StringBuilder append"); return; }
                int Dipadišo = 빼기(2); if (!selo_boleng(Dipadišo, 4) || !selo_boleng(Sengwalwa, 1)) return;
                int 앞 = 힙[Dipadišo + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Morago_boleng_botelele = 힙[Sengwalwa + 1];
                int 새글 = aba_Bobolokelo(1, 앞길이 + Morago_boleng_botelele); if (Phošo) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Morago_boleng_botelele; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Sengwalwa + 2 + 수];
                힙[Dipadišo + 2] = 새글; 넣기(Dipadišo, 2); return;
            }
        }
        go_palelwa_boleng("unsupported library method");
    }
    static int arei_sekgobana(int Dipadišo, int sapskripte_boleng, int thaepa_boleng) {
        if (!selo_boleng(Dipadišo, thaepa_boleng)) return 0;
        if (sapskripte_boleng < 0 || sapskripte_boleng >= 힙[Dipadišo + 1]) { go_palelwa_boleng("ArrayIndexOutOfBoundsException"); return 0; }
        return Dipadišo + 2 + sapskripte_boleng;
    }
    static void phethagatša_taelo() {
        int 남음 = 500000;
        while (freime_lokela >= 0 && !Phošo) {
            if (--남음 == 0) { go_palelwa_boleng("instruction limit (500000)"); break; }
            int Diriša = 틀위치[freime_lokela], boleng = 명바();
            if (Phošo) break;
            if (boleng == 0) continue;
            if (boleng == 1) { 넣기(0, 2); continue; }
            if (boleng >= 2 && boleng <= 8) { 넣기(boleng - 3, 1); continue; }
            if (boleng == 16) { 넣기((byte)명바(), 1); continue; }
            if (boleng == 17) { 넣기((short)명짧(), 1); continue; }
            if (boleng == 18 || boleng == 19) {
                int 수 = boleng == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) go_palelwa_boleng("invalid ldc constant");
                else if (ya_go_se_fetoge_leswao[수] == 3) 넣기(상가[수], 1);
                else if (ya_go_se_fetoge_leswao[수] == 8) 넣기(ya_go_se_fetoge_SMS(상가[수]), 2);
                else go_palelwa_boleng("unsupported ldc constant");
                continue;
            }
            if (boleng == 21 || boleng == 25) { 지역읽기(명바(), boleng == 21 ? 1 : 2); continue; }
            if (boleng >= 26 && boleng <= 29) { 지역읽기(boleng - 26, 1); continue; }
            if (boleng >= 42 && boleng <= 45) { 지역읽기(boleng - 42, 2); continue; }
            if (boleng == 54 || boleng == 58) { ngwala_kgauswi(명바(), boleng == 54 ? 1 : 2); continue; }
            if (boleng >= 59 && boleng <= 62) { ngwala_kgauswi(boleng - 59, 1); continue; }
            if (boleng >= 75 && boleng <= 78) { ngwala_kgauswi(boleng - 75, 2); continue; }
            if (boleng == 46 || boleng == 50) {
                int sapskripte_boleng = 빼기(1), Dipadišo = 빼기(2), sekgobana_go_tsenya_tshedimošo = arei_sekgobana(Dipadišo, sapskripte_boleng, boleng == 46 ? 2 : 3);
                if (!Phošo) 넣기(힙[sekgobana_go_tsenya_tshedimošo], boleng == 46 ? 1 : 2); continue;
            }
            if (boleng == 79 || boleng == 83) {
                int aetheme_elemente = 빼기(boleng == 79 ? 1 : 2), sapskripte_boleng = 빼기(1), Dipadišo = 빼기(2), sekgobana_go_tsenya_tshedimošo = arei_sekgobana(Dipadišo, sapskripte_boleng, boleng == 79 ? 2 : 3);
                if (boleng == 83 && aetheme_elemente != 0) selo_boleng(aetheme_elemente, 1);
                if (!Phošo) 힙[sekgobana_go_tsenya_tshedimošo] = aetheme_elemente; continue;
            }
            if (boleng == 87) { 빼기(0); continue; }
            if (boleng == 89) { int 가 = 빼기(0), thaepa_boleng = 반환형; 넣기(가, thaepa_boleng); 넣기(가, thaepa_boleng); continue; }
            if (boleng == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (boleng == 96 || boleng == 100 || boleng == 104 || boleng == 108 || boleng == 112 || boleng == 120
                || boleng == 122 || boleng == 124 || boleng == 126 || boleng == 128 || boleng == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((boleng == 108 || boleng == 112) && 나 == 0) { go_palelwa_boleng("ArithmeticException: / by zero"); continue; }
                if (boleng == 96) 결과 = 가 + 나;
                if (boleng == 100) 결과 = 가 - 나;
                if (boleng == 104) 결과 = 가 * 나;
                if (boleng == 108) 결과 = 가 / 나;
                if (boleng == 112) 결과 = 가 % 나;
                if (boleng == 120) 결과 = 가 << 나;
                if (boleng == 122) 결과 = 가 >> 나;
                if (boleng == 124) 결과 = 가 >>> 나;
                if (boleng == 126) 결과 = 가 & 나;
                if (boleng == 128) 결과 = 가 | 나;
                if (boleng == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (boleng == 116) { 넣기(-빼기(1), 1); continue; }
            if (boleng == 132) {
                int kgauswi_skoupo = 명바(), 증분 = (byte)명바(); 지역읽기(kgauswi_skoupo, 1); 넣기(빼기(1) + 증분, 1); ngwala_kgauswi(kgauswi_skoupo, 1); continue;
            }
            if (boleng >= 145 && boleng <= 147) {
                int 수 = 빼기(1); 넣기(boleng == 145 ? (byte)수 : boleng == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (boleng >= 153 && boleng <= 167 || boleng == 198 || boleng == 199) {
                int boyo_boleng = Diriša + (short)명짧(); boolean 갈까 = boleng == 167;
                if (boleng >= 153 && boleng <= 158) {
                    int 수 = 빼기(1); 갈까 = boleng == 153 ? 수 == 0 : boleng == 154 ? 수 != 0 : boleng == 155 ? 수 < 0 : boleng == 156 ? 수 >= 0 : boleng == 157 ? 수 > 0 : 수 <= 0;
                } else if (boleng >= 159 && boleng <= 166) {
                    int 나 = 빼기(boleng >= 165 ? 2 : 1), 가 = 빼기(boleng >= 165 ? 2 : 1);
                    갈까 = boleng == 159 || boleng == 165 ? 가 == 나 : boleng == 160 || boleng == 166 ? 가 != 나 : boleng == 161 ? 가 < 나 : boleng == 162 ? 가 >= 나 : boleng == 163 ? 가 > 나 : 가 <= 나;
                } else if (boleng == 198 || boleng == 199) { int 수 = 빼기(2); 갈까 = boleng == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) šuthiša_boleng(boyo_boleng); continue;
            }
            if (boleng == 172 || boleng == 176 || boleng == 177) { 반환(boleng == 172 ? 1 : boleng == 176 ? 2 : 0); continue; }
            if (boleng == 178) {
                int 수 = 명짧(); if (!lekola_ya_go_se_fetoge(수, 9)) continue;
                if (!Thalokontšu_SMS(legoro_leina_SMS(상가[수]), "java/lang/System") || !Thalokontšu_SMS(Dipadišo_leina(상나[수]), "out")
                    || !Thalokontšu_SMS(Dipadišo_thaepa(상나[수]), "Ljava/io/PrintStream;")) go_palelwa_boleng("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (boleng == 182 || boleng == 183 || boleng == 184) { founa_mokgwa(명짧(), boleng); continue; }
            if (boleng == 187) {
                int Leina = legoro_leina_SMS(명짧());
                if (Thalokontšu_SMS(Leina, "java/lang/StringBuilder")) 넣기(aba_Bobolokelo(4, 1), 2);
                else if (Thalokontšu_SMS(Leina, "java/io/FileInputStream") || Thalokontšu_SMS(Leina, "java/io/FileOutputStream")) {
                    int Dipadišo = aba_Bobolokelo(Thalokontšu_SMS(Leina, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Phošo) { 힙[Dipadišo + 2] = -1; 넣기(Dipadišo, 2); }
                } else go_palelwa_boleng("unsupported object construction");
                continue;
            }
            if (boleng == 188 || boleng == 189) {
                if (boleng == 188) { if (명바() != 10) go_palelwa_boleng("only int[] newarray is supported"); }
                else if (!Thalokontšu_SMS(legoro_leina_SMS(명짧()), "java/lang/String")) go_palelwa_boleng("only String[] anewarray is supported");
                int botelele_boleng = 빼기(1); 넣기(aba_Bobolokelo(boleng == 188 ? 2 : 3, botelele_boleng), 2); continue;
            }
            if (boleng == 190) {
                int Dipadišo = 빼기(2);
                if (Dipadišo < 1 || Dipadišo >= 힙끝 - 1 || (힙[Dipadišo] != 2 && 힙[Dipadišo] != 3)) go_palelwa_boleng("null or invalid array");
                else 넣기(힙[Dipadišo + 1], 1); continue;
            }
            if (boleng == 192) {
                int Leina = legoro_leina_SMS(명짧()), Dipadišo = 빼기(2);
                if (!Thalokontšu_SMS(Leina, "java/lang/String")) go_palelwa_boleng("unsupported checkcast");
                else if (Dipadišo != 0) selo_boleng(Dipadišo, 1);
                넣기(Dipadišo, 2); continue;
            }
            go_palelwa_boleng("unsupported bytecode");
        }
    }
    public static int Diriša() {
        if (mošomiši.인수개수() == 1 && 자바도구.같음(mošomiši.인수(0), "-version")) {
            mošomiši.Ngwala("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (mošomiši.인수개수() < 1) { mošomiši.Ngwala("Usage: java CLASS [ARGS]\n"); return 2; }
        int botelele_boleng = 자바도구.Leina(faele_leina_SMS, mošomiši.인수(0));
        if (botelele_boleng < 1 || botelele_boleng > 57) { mošomiši.Ngwala("java: invalid class name\n"); return 2; }
        faele_leina_SMS[botelele_boleng] = '.'; faele_leina_SMS[botelele_boleng + 1] = 'c'; faele_leina_SMS[botelele_boleng + 2] = 'l'; faele_leina_SMS[botelele_boleng + 3] = 'a'; faele_leina_SMS[botelele_boleng + 4] = 's'; faele_leina_SMS[botelele_boleng + 5] = 's';
        Bogolo = mošomiši.파일읽기(faele_leina_SMS, Faele);
        if (Bogolo < 0) { mošomiši.Ngwala("java: cannot read class: "); 자바도구.수쓰기(Bogolo); mošomiši.ngwala_tlhaka_boleng(10); return 1; }
        클래스읽기(); if (Phošo) return 1;
        int tlhaka_leina = ya_go_se_fetoge_SMS(legoro_leina);
        if (!Phošo && 힙[tlhaka_leina + 1] != botelele_boleng) go_palelwa_boleng("class name does not match file");
        for (int 수 = 0; 수 < botelele_boleng && !Phošo; 수++) if (힙[tlhaka_leina + 2 + 수] != faele_leina_SMS[수]) go_palelwa_boleng("class name does not match file");
        int go_tsenya_tshedimošo_ntlha_boleng = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Thalokontšu_SMS(mokgwa_leina_SMS[수], "main") && Thalokontšu_SMS(mokgwa_thaepa[수], "([Ljava/lang/String;)V") && (mokgwa_fihlelela[수] & 9) == 9) go_tsenya_tshedimošo_ntlha_boleng = 수;
        if (go_tsenya_tshedimošo_ntlha_boleng < 0) go_palelwa_boleng("public static void main(String[] args) required");
        if (Phošo) return 1;
        int 인수 = aba_Bobolokelo(3, mošomiši.인수개수() - 1);
        for (int 수 = 1; 수 < mošomiši.인수개수() && !Phošo; 수++) 힙[인수 + 1 + 수] = go_nea_ditirelo_tlhaka(mošomiši.인수(수));
        freime_lokela = 0; freime_mokgwa[0] = go_tsenya_tshedimošo_ntlha_boleng; 틀위치[0] = mokgwa_Thomišo[go_tsenya_tshedimošo_ntlha_boleng]; kgauswi_boleng[0] = 인수; kgauswi_thaepa[0] = 2;
        phethagatša_taelo(); return Phošo ? 1 : 0;
    }
}
