// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Faele/스택/Dipadišo/lekala 경계를 phethagatša_taelo 중 검사한다. */
public final class 자바가상기계 {
    static int[] Faele = new int[16 * 16384], 임시파일 = new int[16384], faele_leina_SMS = new int[512];
    static int[] ya_go_se_fetoge_leswao = new int[8192], 상가 = new int[8192], 상나 = new int[8192], molokoloko_Dipadišo = new int[8192];
    static int[] mokgwa_leina_SMS = new int[512], mokgwa_thaepa = new int[512], mokgwa_fihlelela = new int[512], mokgwa_mong = new int[512];
    static int[] mokgwa_Thomišo = new int[512], mokgwa_fetša = new int[512], mokgwa_kgoboko = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], mokgwa_akumente_thaepa = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] kgauswi_boleng = new int[16384], kgauswi_thaepa = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] freime_mokgwa = new int[128], 틀위치 = new int[128], freime_kgoboko = new int[128], freime_taelo = new int[128], thomiša_freime = new int[128];
    static int[] legoro_Tlhaloso_leina = new int[16], legoro_Tlhaloso_bogolo = new int[16], 종부모 = new int[16], legoro_Tlhaloso_boemo = new int[16], 종칸수 = new int[16], thomiša_legoro_Tlhaloso = new int[16];
    static int[] legoro_lefelokgokagano = new int[16 * 16], 종접면수 = new int[16];
    static int[] sekgobana_leina = new int[512], sekgobana_thaepa = new int[512], sekgobana_mong = new int[512], sekgobana_ditumelelo = new int[512], 칸위치 = new int[512], sekgobana_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], arei_elemente = new int[32768], lota_palotlalo = new int[256];
    static int Bogolo, 읽기위치, 함수수, legoro_leina, freime_lokela = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, go_tsenya_tshedimošo_legoro_Tlhaloso;
    static int[] threte_freime = new int[4], threte_boemo = new int[4], threte_selo = new int[4], threte_nepo = new int[4], 가닥대기 = new int[4];
    static boolean Phošo, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], legoro_threte = new int[16];

    static void go_palelwa_boleng(String Thalokontšu_SMS) {
        if (Phošo) return;
        int 분류코드 = 0;
        if (자바도구.같음(Thalokontšu_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Thalokontšu_SMS, "NullPointerException") || 자바도구.같음(Thalokontšu_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Thalokontšu_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Thalokontšu_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Thalokontšu_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Thalokontšu_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Thalokontšu_SMS, "IOException: stream closed") || 자바도구.같음(Thalokontšu_SMS, "IOException: read failed") || 자바도구.같음(Thalokontšu_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Thalokontšu_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Thalokontšu_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && freime_lokela >= 0) { 예외던짐(분류코드, Thalokontšu_SMS); return; }
        mošomiši.Ngwala("JVM error: "); mošomiši.Ngwala(Thalokontšu_SMS); mošomiši.ngwala_tlhaka_boleng(10); Phošo = true;
    }
    static boolean setsopolwa(int Diriša, int botelele_boleng) {
        if (Diriša < 0 || Diriša >= Faele.length || botelele_boleng < 0) return false;
        int legoro_Tlhaloso = Diriša / 16384;
        return Diriša % 16384 <= legoro_Tlhaloso_bogolo[legoro_Tlhaloso] && botelele_boleng <= legoro_Tlhaloso_bogolo[legoro_Tlhaloso] - Diriša % 16384;
    }
    static int paete_boleng() {
        if (!setsopolwa(읽기위치, 1)) { go_palelwa_boleng("truncated class file"); return 0; }
        return Faele[읽기위치++];
    }
    static int 짧은수() { return paete_boleng() << 8 | paete_boleng(); }
    static int palotlalo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int botelele_boleng) { if (!setsopolwa(읽기위치, botelele_boleng)) go_palelwa_boleng("invalid attribute size"); else 읽기위치 += botelele_boleng; }
    static boolean lekola_ya_go_se_fetoge(int 수, int 종류) {
        if (수 <= 0 || 수 >= ya_go_se_fetoge_leswao.length || ya_go_se_fetoge_leswao[수] != 종류) { go_palelwa_boleng("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Diriša, int botelele_boleng, String Thalokontšu_SMS) {
        if (!setsopolwa(Diriša, botelele_boleng)) return false;
        int 읽는자리 = Diriša, 끝 = Diriša + botelele_boleng;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Thalokontšu_SMS.length(); ditaelopoeletšwa_lokela++) {
            int khouto_ya_tlhaka = Thalokontšu_SMS.charAt(ditaelopoeletšwa_lokela);
            if (khouto_ya_tlhaka > 0 && khouto_ya_tlhaka < 128) { if (읽는자리 >= 끝 || Faele[읽는자리++] != khouto_ya_tlhaka) return false; }
            else if (khouto_ya_tlhaka < 2048) {
                if (읽는자리 + 2 > 끝 || Faele[읽는자리++] != (192 | (khouto_ya_tlhaka >> 6)) || Faele[읽는자리++] != (128 | (khouto_ya_tlhaka & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Faele[읽는자리++] != (224 | (khouto_ya_tlhaka >> 12)) || Faele[읽는자리++] != (128 | ((khouto_ya_tlhaka >> 6) & 63)) || Faele[읽는자리++] != (128 | (khouto_ya_tlhaka & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int boleng = 짧은수(); return boleng == 0 ? 0 : 현재읽는종 * 512 + boleng; }
    static int 명상수() { return mokgwa_mong[freime_mokgwa[freime_lokela]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Phošo; 수++) { lekola_ya_go_se_fetoge(상번호(), 1); 건너(palotlalo()); }
    }
    static int taelo_botelele(int boleng) {
        if (boleng == 16 || boleng == 18 || boleng == 21 || boleng == 25 || boleng == 54 || boleng == 58 || boleng == 188) return 2;
        if (boleng == 17 || boleng == 19 || boleng == 132 || boleng >= 153 && boleng <= 167
            || boleng >= 178 && boleng <= 184 || boleng == 187 || boleng == 189 || boleng == 192 || boleng == 193 || boleng == 198 || boleng == 199) return 3;
        if (boleng == 185 || boleng == 200) return 5;
        if (boleng >= 0 && boleng <= 8 || boleng >= 26 && boleng <= 29 || boleng >= 42 && boleng <= 46 || boleng >= 50 && boleng <= 53
            || boleng >= 59 && boleng <= 62 || boleng >= 75 && boleng <= 79 || boleng >= 83 && boleng <= 95
            || boleng == 96 || boleng == 100 || boleng == 104 || boleng == 108 || boleng == 112 || boleng == 116
            || boleng == 120 || boleng == 122 || boleng == 124 || boleng == 126 || boleng == 128 || boleng == 130
            || boleng >= 145 && boleng <= 147 || boleng == 172 || boleng == 176 || boleng == 177 || boleng == 190 || boleng == 191
            || boleng == 194 || boleng == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!setsopolwa(읽는자리, 4)) { go_palelwa_boleng("truncated bytecode operand"); return 0; }
        return Faele[읽는자리] << 24 | Faele[읽는자리 + 1] << 16 | Faele[읽는자리 + 2] << 8 | Faele[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Diriša, int 끝) {
        int boleng = Faele[읽는자리], botelele_boleng = taelo_botelele(boleng);
        if (boleng == 170 || boleng == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Diriša) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (boleng == 170 ? 12 : 8)) return 0;
            int 항목수 = boleng == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            botelele_boleng = 기준자리 - 읽는자리 + (boleng == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (boleng == 196 && 읽는자리 + 1 < 끝) {
            int Thalokontšu_data = Faele[읽는자리 + 1]; botelele_boleng = Thalokontšu_data == 132 ? 6 : (Thalokontšu_data == 21 || Thalokontšu_data == 25 || Thalokontšu_data == 54 || Thalokontšu_data == 58) ? 4 : 0;
        }
        return botelele_boleng > 0 && botelele_boleng <= 끝 - 읽는자리 ? botelele_boleng : 0;
    }
    static void lekola_boyo_boleng(int boyo_boleng, int TIRO_boleng) {
        if (boyo_boleng < mokgwa_Thomišo[TIRO_boleng] || boyo_boleng >= mokgwa_fetša[TIRO_boleng] || 경계[boyo_boleng] != TIRO_boleng + 1) go_palelwa_boleng("invalid branch target");
    }
    static void 클래스읽기(int legoro_Tlhaloso) {
        현재읽는종 = legoro_Tlhaloso; 읽기위치 = legoro_Tlhaloso * 16384; Bogolo = 읽기위치 + legoro_Tlhaloso_bogolo[legoro_Tlhaloso];
        if (palotlalo() != 0xcafebabe) { go_palelwa_boleng("not a class file"); return; }
        int 부판 = 짧은수(), bešene_boleng = 짧은수();
        if (bešene_boleng < 45 || bešene_boleng > 52 || 부판 != 0) { go_palelwa_boleng("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = legoro_Tlhaloso * 512;
        if (상수수 < 1 || 상수수 > 512) { go_palelwa_boleng("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !Phošo; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = paete_boleng(); ya_go_se_fetoge_leswao[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = palotlalo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else go_palelwa_boleng("unsupported constant type");
        }
        int tumelelo_boleng = 짧은수();
        if ((tumelelo_boleng & (0x2000 | 0x4000)) != 0) go_palelwa_boleng("annotation/enum class unsupported");
        legoro_Tlhaloso_leina[legoro_Tlhaloso] = legoro_leina_SMS(상번호());
        종부모[legoro_Tlhaloso] = legoro_leina_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { go_palelwa_boleng("interface count limit"); return; }
        종접면수[legoro_Tlhaloso] = 접면수;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 접면수; ditaelopoeletšwa_lokela++) legoro_lefelokgokagano[legoro_Tlhaloso * 16 + ditaelopoeletšwa_lokela] = legoro_leina_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { go_palelwa_boleng("field count limit (512)"); return; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 필드수 && !Phošo; ditaelopoeletšwa_lokela++) {
            int faele_lokela = 칸수++; sekgobana_mong[faele_lokela] = legoro_Tlhaloso; sekgobana_ditumelelo[faele_lokela] = 짧은수(); sekgobana_leina[faele_lokela] = 상번호(); sekgobana_thaepa[faele_lokela] = 상번호();
            lekola_ya_go_se_fetoge(sekgobana_leina[faele_lokela], 1); lekola_ya_go_se_fetoge(sekgobana_thaepa[faele_lokela], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[sekgobana_thaepa[faele_lokela]]; int 분류코드 = 서술형(읽기위치 + 상나[sekgobana_thaepa[faele_lokela]], false); 읽기위치 = 보존값;
            if ((sekgobana_ditumelelo[faele_lokela] & 8) == 0) 칸위치[faele_lokela] = 종칸수[legoro_Tlhaloso]++;
            int tlhaodi_ya_faele_data = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < tlhaodi_ya_faele_data && !Phošo; 안쪽자리++) {
                int leina_ya_go_se_fetoge = 상번호(), 유효길이 = palotlalo();
                if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "ConstantValue") && 유효길이 == 2) {
                    int data_boleng = 상번호();
                    if (분류코드 == 1 && lekola_ya_go_se_fetoge(data_boleng, 3)) sekgobana_data[faele_lokela] = 상가[data_boleng];
                    else if (분류코드 == 2 && lekola_ya_go_se_fetoge(data_boleng, 8)) sekgobana_data[faele_lokela] = ya_go_se_fetoge_SMS(상가[data_boleng]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { go_palelwa_boleng("method count limit (512)"); return; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 개수 && !Phošo; ditaelopoeletšwa_lokela++) {
            int 수 = 함수수++; mokgwa_mong[수] = legoro_Tlhaloso;
            mokgwa_fihlelela[수] = 짧은수(); mokgwa_leina_SMS[수] = 상번호(); mokgwa_thaepa[수] = 상번호();
            lekola_ya_go_se_fetoge(mokgwa_leina_SMS[수], 1); 서술읽기(수);
            if ((mokgwa_fihlelela[수] & 8) == 0) {
                if (함수인수수[수] == 16) { go_palelwa_boleng("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) mokgwa_akumente_thaepa[수 * 16 + 비교자리] = mokgwa_akumente_thaepa[수 * 16 + 비교자리 - 1];
                mokgwa_akumente_thaepa[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((mokgwa_fihlelela[수] & 0x100) != 0) go_palelwa_boleng("user native method unsupported");
            if (Thalokontšu_SMS(mokgwa_leina_SMS[수], "<clinit>")) thomiša_legoro_Tlhaloso[legoro_Tlhaloso] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (mokgwa_mong[앞] == legoro_Tlhaloso && 같은말(mokgwa_leina_SMS[앞], mokgwa_leina_SMS[수]) && 같은말(mokgwa_thaepa[앞], mokgwa_thaepa[수])) go_palelwa_boleng("duplicate method");
            int 속성수 = 짧은수();
            for (int tlhaodi_ya_faele_boleng = 0; tlhaodi_ya_faele_boleng < 속성수 && !Phošo; tlhaodi_ya_faele_boleng++) {
                int Leina = 상번호(), botelele_boleng = palotlalo(), Diriša = 읽기위치;
                if (!setsopolwa(Diriša, botelele_boleng)) { go_palelwa_boleng("truncated method attribute"); break; }
                if (Thalokontšu_SMS(Leina, "Code")) {
                    if (mokgwa_Thomišo[수] != 0) go_palelwa_boleng("duplicate Code attribute");
                    mokgwa_kgoboko[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = palotlalo();
                    if (mokgwa_kgoboko[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) go_palelwa_boleng("method memory limits exceeded");
                    mokgwa_Thomišo[수] = 읽기위치; 건너(코드길이); mokgwa_fetša[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { go_palelwa_boleng("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int phošo_Dipadišo = 잡기수++; 잡기함수[phošo_Dipadišo] = 수;
                        잡기시작[phošo_Dipadišo] = mokgwa_Thomišo[수] + 짧은수(); 잡기끝[phošo_Dipadišo] = mokgwa_Thomišo[수] + 짧은수();
                        잡기위치[phošo_Dipadišo] = mokgwa_Thomišo[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[phošo_Dipadišo] = 부호값 == 0 ? 0 : legoro_leina_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Diriša + botelele_boleng) go_palelwa_boleng("Code attribute size mismatch");
                } else 건너(botelele_boleng);
            }
            if ((mokgwa_fihlelela[수] & 0x400) != 0) continue;
            if (mokgwa_Thomišo[수] == 0) go_palelwa_boleng("missing Code attribute");
            int sekgobana_go_tsenya_tshedimošo = mokgwa_Thomišo[수];
            while (sekgobana_go_tsenya_tshedimošo < mokgwa_fetša[수] && !Phošo) {
                int botelele_boleng = 길이읽기(sekgobana_go_tsenya_tshedimošo, mokgwa_Thomišo[수], mokgwa_fetša[수]);
                if (botelele_boleng == 0) { go_palelwa_boleng("unsupported or truncated bytecode"); break; }
                경계[sekgobana_go_tsenya_tshedimošo] = 수 + 1; sekgobana_go_tsenya_tshedimošo += botelele_boleng;
            }
            sekgobana_go_tsenya_tshedimošo = mokgwa_Thomišo[수];
            while (sekgobana_go_tsenya_tshedimošo < mokgwa_fetša[수] && !Phošo) {
                int boleng = Faele[sekgobana_go_tsenya_tshedimošo];
                if (boleng >= 153 && boleng <= 167 || boleng == 198 || boleng == 199) lekola_boyo_boleng(sekgobana_go_tsenya_tshedimošo + (short)(Faele[sekgobana_go_tsenya_tshedimošo + 1] << 8 | Faele[sekgobana_go_tsenya_tshedimošo + 2]), 수);
                if (boleng == 200) lekola_boyo_boleng(sekgobana_go_tsenya_tshedimošo + 위치정수(sekgobana_go_tsenya_tshedimošo + 1), 수);
                if (boleng == 170 || boleng == 171) {
                    int 읽는자리 = sekgobana_go_tsenya_tshedimošo + 1; while ((읽는자리 - mokgwa_Thomišo[수]) % 4 != 0) 읽는자리++;
                    lekola_boyo_boleng(sekgobana_go_tsenya_tshedimošo + 위치정수(읽는자리), 수);
                    int 항목수 = boleng == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += boleng == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) lekola_boyo_boleng(sekgobana_go_tsenya_tshedimošo + 위치정수(읽는자리 + 안쪽자리 * (boleng == 170 ? 4 : 8) + (boleng == 170 ? 0 : 4)), 수);
                }
                sekgobana_go_tsenya_tshedimošo += 길이읽기(sekgobana_go_tsenya_tshedimošo, mokgwa_Thomišo[수], mokgwa_fetša[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                lekola_boyo_boleng(잡기시작[안쪽자리], 수); lekola_boyo_boleng(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != mokgwa_fetša[수]) lekola_boyo_boleng(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) go_palelwa_boleng("invalid exception range");
            }
        }
        if (!Phošo) 속성건너();
        if (읽기위치 != Bogolo) go_palelwa_boleng("extra class file data");
    }
    static int aba_Bobolokelo(int 종류, int botelele_boleng) { return 새기억(종류, botelele_boleng); }
    static boolean selo_boleng(int Dipadišo, int 종류) {
        if (!객체유효(Dipadišo)) return false;
        if (힙[Dipadišo] != 종류) { go_palelwa_boleng("object type mismatch"); return false; }
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
        if (반환형 == 2) šireletša_boleng(스택값[sekgobana_go_tsenya_tshedimošo]);
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
        if (freime_lokela % 32 == 31) { go_palelwa_boleng("call stack limit (32)"); return; }
        int 다음 = freime_lokela + 1;
        for (int 수 = 0; 수 < 128; 수++) kgauswi_thaepa[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[TIRO_boleng] - 1; 수 >= 0; 수--) {
            kgauswi_boleng[다음 * 128 + 수] = 빼기(mokgwa_akumente_thaepa[TIRO_boleng * 16 + 수]); kgauswi_thaepa[다음 * 128 + 수] = mokgwa_akumente_thaepa[TIRO_boleng * 16 + 수];
        }
        if (Phošo) return;
        freime_lokela = 다음; thomiša_freime[freime_lokela] = 0; freime_mokgwa[freime_lokela] = TIRO_boleng; 틀위치[freime_lokela] = mokgwa_Thomišo[TIRO_boleng]; freime_kgoboko[freime_lokela] = 0;
    }
    static void 반환(int thaepa_boleng) {
        if (thaepa_boleng != 함수반환[freime_mokgwa[freime_lokela]]) { go_palelwa_boleng("return type mismatch"); return; }
        int boleng = thaepa_boleng == 0 ? 0 : 빼기(thaepa_boleng);
        if (thomiša_freime[freime_lokela] != 0) legoro_Tlhaloso_boemo[thomiša_freime[freime_lokela] - 1] = 2;
        if (틀잠금[freime_lokela] != 0) { 잠금풀기(틀잠금[freime_lokela]); 틀잠금[freime_lokela] = 0; }
        freime_lokela--; if (freime_lokela >= 현재가닥 * 32 && thaepa_boleng != 0) 넣기(boleng, thaepa_boleng);
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
                if (boleng < 1) { go_palelwa_boleng("invalid file stream path"); return; }
                Stream_faele_leina[sekgobana_go_tsenya_tshedimošo] = boleng;
            }
            Stream_faele_leina[botelele_boleng] = 0;
            int 서술자 = mošomiši.파일서술자열기(Stream_faele_leina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { go_palelwa_boleng("FileNotFoundException: file open failed"); return; }
            힙[Stream_boleng + 2] = 서술자; 힙[Stream_boleng + 3] = 1;
            return;
        }
        if (Taelo != 182) { go_palelwa_boleng("invalid file stream invocation"); return; }
        if ((출력 && Thalokontšu_SMS(Leina, "write") || !출력 && Thalokontšu_SMS(Leina, "read"))
            && (Thalokontšu_SMS(fomete_boleng, 출력 ? "([B)V" : "([B)I") || Thalokontšu_SMS(fomete_boleng, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean setsopolwa_boleng = Thalokontšu_SMS(fomete_boleng, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = setsopolwa_boleng ? 빼기(1) : 0, 시작점 = setsopolwa_boleng ? 빼기(1) : 0, data_arei = 빼기(2), selo_Dipadišo = 빼기(2);
            if (!selo_boleng(data_arei, 20) || !selo_boleng(selo_Dipadišo, 종류)) return;
            if (!setsopolwa_boleng) 항목수 = 힙[data_arei + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[data_arei + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[selo_Dipadišo + 3] == 0 || 힙[selo_Dipadišo + 2] < 0) { go_palelwa_boleng("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !Phošo) {
                int 반환값 = 출력 ? mošomiši.파일한바이트쓰기(힙[selo_Dipadišo + 2], 힙[data_arei + 2 + 시작점 + 완료수]) : mošomiši.파일한바이트읽기(힙[selo_Dipadišo + 2]);
                if (반환값 < 0) { go_palelwa_boleng(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[data_arei + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Thalokontšu_SMS(Leina, "flush") && Thalokontšu_SMS(fomete_boleng, "()V")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 종류) && 힙[selo_Dipadišo + 2] < 0) go_palelwa_boleng("IOException: stream closed"); return; }
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
            if (결과 < -1) go_palelwa_boleng("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (mošomiši.파일한바이트쓰기(서술자, boleng) != 1) go_palelwa_boleng("IOException: write failed");
    }
    static void founa_mokgwa(int lokela, int Taelo) {
        if (lokela <= 0 || lokela >= ya_go_se_fetoge_leswao.length || (ya_go_se_fetoge_leswao[lokela] != 10 && ya_go_se_fetoge_leswao[lokela] != 11)) { go_palelwa_boleng("invalid method reference"); return; }
        int mong_boleng = legoro_leina_SMS(상가[lokela]), Leina = Dipadišo_leina(상나[lokela]), fomete_boleng = Dipadišo_thaepa(상나[lokela]);
        if (Phošo) return;
        if (기본호출(mong_boleng, Leina, fomete_boleng, Taelo)) return;
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
        int legoro_Tlhaloso = hwetša_legoro_Tlhaloso(mong_boleng); if (legoro_Tlhaloso < 0 || Phošo) return;
        int faele_lokela = hwetša_mokgwa(legoro_Tlhaloso, Leina, fomete_boleng);
        if (faele_lokela < 0) {
            for (int khouto_ya_tlhaka = legoro_Tlhaloso, 항목수 = 0; khouto_ya_tlhaka >= 0 && 항목수 < 16; 항목수++, khouto_ya_tlhaka = 부모종(khouto_ya_tlhaka))
                if (Thalokontšu_SMS(종부모[khouto_ya_tlhaka], "java/lang/Thread")) { 가닥호출(Leina, fomete_boleng, Taelo); return; }
            go_palelwa_boleng("NoSuchMethodError"); return;
        }
        if (((mokgwa_fihlelela[faele_lokela] & 8) != 0) != (Taelo == 184)) { go_palelwa_boleng("method static/instance mismatch"); return; }
        if (Taelo == 184) { if (!thomiša(mokgwa_mong[faele_lokela], freime_taelo[freime_lokela])) return; }
        else {
            int 읽는자리 = freime_kgoboko[freime_lokela] - 함수인수수[faele_lokela];
            if (읽는자리 < 0 || 스택형[freime_lokela * 128 + 읽는자리] != 2) { go_palelwa_boleng("invalid method receiver"); return; }
            int selo_Dipadišo = 스택값[freime_lokela * 128 + 읽는자리];
            if (!객체유효(selo_Dipadišo)) return;
            if (힙[selo_Dipadišo] < 32 || !종포함(힙[selo_Dipadišo] - 32, mong_boleng)) { go_palelwa_boleng("method receiver type mismatch"); return; }
            if (Taelo != 183) faele_lokela = hwetša_mokgwa(힙[selo_Dipadišo] - 32, Leina, fomete_boleng);
        }
        if (faele_lokela < 0 || (mokgwa_fihlelela[faele_lokela] & 0x400) != 0) { go_palelwa_boleng("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((mokgwa_fihlelela[faele_lokela] & 32) != 0) {
            if (Taelo == 184) { int khouto_ya_tlhaka = mokgwa_mong[faele_lokela]; if (종잠금[khouto_ya_tlhaka] == 0) 종잠금[khouto_ya_tlhaka] = aba_Bobolokelo(8, 0); 잠금참조 = 종잠금[khouto_ya_tlhaka]; }
            else 잠금참조 = 스택값[freime_lokela * 128 + freime_kgoboko[freime_lokela] - 함수인수수[faele_lokela]];
            if (!잠금얻기(잠금참조)) { if (!Phošo) 틀위치[freime_lokela] = freime_taelo[freime_lokela]; return; }
        }
        호출(faele_lokela); if (!Phošo) 틀잠금[freime_lokela] = 잠금참조;
    }
    static boolean 배열저장가능(int arei_Dipadišo, int data_boleng) {
        if (data_boleng == 0 || arei_elemente[arei_Dipadišo] == 0) return true;
        boolean 성공여부 = arei_elemente[arei_Dipadišo] == -1 ? (data_boleng > 0 && data_boleng < 힙끝 && 힙[data_boleng] == 1) : 맞는객체(data_boleng, arei_elemente[arei_Dipadišo]);
        if (!성공여부 && !Phošo) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int arei_sekgobana(int Dipadišo, int sapskripte_boleng, int thaepa_boleng) {
        if (!selo_boleng(Dipadišo, thaepa_boleng)) return 0;
        if (sapskripte_boleng < 0 || sapskripte_boleng >= 힙[Dipadišo + 1]) { go_palelwa_boleng("ArrayIndexOutOfBoundsException"); return 0; }
        return Dipadišo + 2 + sapskripte_boleng;
    }
    static void phethagatša_taelo() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Phošo) { if (던진객체 != 0) 예외처리(); if (Phošo || freime_lokela < 현재가닥 * 32) break; }
            if (freime_lokela < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!fetogela_threte()) break; 조각 = 100; }
            if (freime_lokela == 0 && legoro_Tlhaloso_boemo[go_tsenya_tshedimošo_legoro_Tlhaloso] != 2 && !thomiša(go_tsenya_tshedimošo_legoro_Tlhaloso, 틀위치[freime_lokela])) continue;
            if (freime_lokela == 현재가닥 * 32 && 현재가닥 != 0 && (mokgwa_fihlelela[freime_mokgwa[freime_lokela]] & 32) != 0 && 틀잠금[freime_lokela] == 0) {
                int selo_Dipadišo = threte_nepo[현재가닥]; if (!잠금얻기(selo_Dipadišo)) { if (Phošo) break; continue; } 틀잠금[freime_lokela] = selo_Dipadišo;
            }
            잠시수 = 0;
            if (--남음 == 0) { go_palelwa_boleng("instruction limit (500000)"); break; }
            int Diriša = 틀위치[freime_lokela]; freime_taelo[freime_lokela] = Diriša; int boleng = 명바();
            if (Phošo) break;
            if (boleng == 0) continue;
            if (boleng == 1) { 넣기(0, 2); continue; }
            if (boleng >= 2 && boleng <= 8) { 넣기(boleng - 3, 1); continue; }
            if (boleng == 16) { 넣기((byte)명바(), 1); continue; }
            if (boleng == 17) { 넣기((short)명짧(), 1); continue; }
            if (boleng == 18 || boleng == 19) {
                int 수 = mokgwa_mong[freime_mokgwa[freime_lokela]] * 512 + (boleng == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= ya_go_se_fetoge_leswao.length) go_palelwa_boleng("invalid ldc constant");
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
            if (boleng == 46 || boleng >= 50 && boleng <= 53) {
                int 항목자리 = 빼기(1), selo_Dipadišo = 빼기(2), 분류코드 = boleng == 46 ? 2 : boleng == 50 ? 3 : boleng == 51 ? 20 : boleng == 52 ? 22 : 23;
                if (boleng == 51 && selo_Dipadišo > 0 && selo_Dipadišo < 힙끝 && 힙[selo_Dipadišo] == 21) 분류코드 = 21;
                int 읽는자리 = arei_sekgobana(selo_Dipadišo, 항목자리, 분류코드); if (!Phošo) 넣기(힙[읽는자리], boleng == 50 ? 2 : 1); continue;
            }
            if (boleng == 79 || boleng >= 83 && boleng <= 86) {
                int go_tsenya_tshedimošo_Dipadišo = 빼기(boleng == 83 ? 2 : 1), 항목자리 = 빼기(1), selo_Dipadišo = 빼기(2), 분류코드 = boleng == 79 ? 2 : boleng == 83 ? 3 : boleng == 84 ? 20 : boleng == 85 ? 22 : 23;
                if (boleng == 84 && selo_Dipadišo > 0 && selo_Dipadišo < 힙끝 && 힙[selo_Dipadišo] == 21) 분류코드 = 21;
                int 읽는자리 = arei_sekgobana(selo_Dipadišo, 항목자리, 분류코드);
                if (!Phošo && 분류코드 == 3 && !배열저장가능(selo_Dipadišo, go_tsenya_tshedimošo_Dipadišo)) continue;
                if (!Phošo) 힙[읽는자리] = 분류코드 == 20 ? (byte)go_tsenya_tshedimošo_Dipadišo : 분류코드 == 21 ? go_tsenya_tshedimošo_Dipadišo & 1 : 분류코드 == 22 ? (char)go_tsenya_tshedimošo_Dipadišo : 분류코드 == 23 ? (short)go_tsenya_tshedimošo_Dipadišo : go_tsenya_tshedimošo_Dipadišo;
                continue;
            }
            if (boleng >= 87 && boleng <= 95) { kgoboko_taelo(boleng); continue; }
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
            if (boleng >= 178 && boleng <= 181) { 필드호출(명상수(), boleng, Diriša); continue; }
            if (boleng >= 182 && boleng <= 185) {
                int 부호값 = 명상수();
                if (boleng == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { go_palelwa_boleng("invalid invokeinterface operands"); continue; } }
                founa_mokgwa(부호값, boleng); continue;
            }
            if (boleng == 187) { 새객체(legoro_leina_SMS(명상수()), Diriša); continue; }
            if (boleng == 188 || boleng == 189) {
                int 분류코드 = 3, karolo = 0;
                if (boleng == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else karolo = legoro_leina_SMS(명상수());
                if (분류코드 == 0) { go_palelwa_boleng("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), selo_Dipadišo = aba_Bobolokelo(분류코드, 유효길이); if (!Phošo) arei_elemente[selo_Dipadišo] = karolo; 넣기(selo_Dipadišo, 2); continue;
            }
            if (boleng == 190) {
                int selo_Dipadišo = 빼기(2);
                if (객체유효(selo_Dipadišo)) { int 비교자리 = 힙[selo_Dipadišo]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) go_palelwa_boleng("not an array"); else 넣기(힙[selo_Dipadišo + 1], 1); }
                continue;
            }
            if (boleng == 191) {
                int selo_Dipadišo = 빼기(2); if (객체유효(selo_Dipadišo)) { if (힙[selo_Dipadišo] != 9) go_palelwa_boleng("athrow requires supported Throwable"); else { 던진객체 = selo_Dipadišo; Phošo = true; } }
                continue;
            }
            if (boleng == 192 || boleng == 193) {
                int leina_ya_go_se_fetoge = legoro_leina_SMS(명상수()), selo_Dipadišo = 빼기(2); boolean 일치여부 = 맞는객체(selo_Dipadišo, leina_ya_go_se_fetoge);
                if (boleng == 193) 넣기(selo_Dipadišo != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !Phošo) go_palelwa_boleng("ClassCastException"); 넣기(selo_Dipadišo, 2); }
                continue;
            }
            if (boleng == 170 || boleng == 171) {
                int 읽는자리 = Diriša + 1, faele_lokela = freime_mokgwa[freime_lokela], khii_Dipadišo = 빼기(1);
                while ((읽는자리 - mokgwa_Thomišo[faele_lokela]) % 4 != 0) 읽는자리++;
                int nepo_atrese = 위치정수(읽는자리);
                if (boleng == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (khii_Dipadišo >= 낮은값 && khii_Dipadišo <= 높은값) nepo_atrese = 위치정수(읽는자리 + 12 + (khii_Dipadišo - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 총수; ditaelopoeletšwa_lokela++) if (위치정수(읽는자리 + 8 + ditaelopoeletšwa_lokela * 8) == khii_Dipadišo) nepo_atrese = 위치정수(읽는자리 + 12 + ditaelopoeletšwa_lokela * 8); }
                šuthiša_boleng(Diriša + nepo_atrese); continue;
            }
            if (boleng == 200) { šuthiša_boleng(Diriša + 위치정수(Diriša + 1)); continue; }
            if (boleng == 194 || boleng == 195) {
                int selo_Dipadišo = 빼기(2);
                if (boleng == 195) 잠금풀기(selo_Dipadišo);
                else if (!잠금얻기(selo_Dipadišo) && !Phošo) { 넣기(selo_Dipadišo, 2); 틀위치[freime_lokela] = Diriša; }
                continue;
            }
            if (boleng == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) ngwala_kgauswi(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); ngwala_kgauswi(항목자리, 1); }
                else go_palelwa_boleng("unsupported wide opcode");
                continue;
            }
            go_palelwa_boleng("unsupported bytecode");
        }
    }
    static int hwetša_legoro_Tlhaloso(int Leina) {
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 종수; ditaelopoeletšwa_lokela++) if (legoro_Tlhaloso_leina[ditaelopoeletšwa_lokela] != 0 && 같은말(legoro_Tlhaloso_leina[ditaelopoeletšwa_lokela], Leina)) return ditaelopoeletšwa_lokela;
        return laiša_legoro_Tlhaloso(ya_go_se_fetoge_SMS(Leina));
    }
    static int laiša_legoro_Tlhaloso(int leina_molokoloko) {
        if (!selo_boleng(leina_molokoloko, 1)) return -1;
        int botelele_boleng = 힙[leina_molokoloko + 1];
        if (botelele_boleng < 1 || botelele_boleng > 505 || 종수 == 16) { go_palelwa_boleng("class name/count limit"); return -1; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < botelele_boleng; ditaelopoeletšwa_lokela++) { int khouto_ya_tlhaka = 힙[leina_molokoloko + 2 + ditaelopoeletšwa_lokela]; faele_leina_SMS[ditaelopoeletšwa_lokela] = khouto_ya_tlhaka == '/' ? '.' : khouto_ya_tlhaka; }
        faele_leina_SMS[botelele_boleng] = '.'; faele_leina_SMS[botelele_boleng + 1] = 'c'; faele_leina_SMS[botelele_boleng + 2] = 'l'; faele_leina_SMS[botelele_boleng + 3] = 'a'; faele_leina_SMS[botelele_boleng + 4] = 's'; faele_leina_SMS[botelele_boleng + 5] = 's'; faele_leina_SMS[botelele_boleng + 6] = 0;
        int Bogolo = mošomiši.파일읽기(faele_leina_SMS, 임시파일);
        if (Bogolo < 0) { go_palelwa_boleng("ClassNotFoundException"); return -1; }
        int legoro_Tlhaloso = 종수++; legoro_Tlhaloso_bogolo[legoro_Tlhaloso] = Bogolo;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) Faele[legoro_Tlhaloso * 16384 + ditaelopoeletšwa_lokela] = 임시파일[ditaelopoeletšwa_lokela];
        클래스읽기(legoro_Tlhaloso); if (Phošo) return -1;
        int kgonthe_data = ya_go_se_fetoge_SMS(legoro_Tlhaloso_leina[legoro_Tlhaloso]);
        if (!글같음(kgonthe_data, leina_molokoloko, true)) { go_palelwa_boleng("class name does not match file"); return -1; }
        int 부모 = 종부모[legoro_Tlhaloso];
        if (부모 != 0 && !Thalokontšu_SMS(부모, "java/lang/Object") && !Thalokontšu_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = hwetša_legoro_Tlhaloso(부모);
            if (Phošo || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == legoro_Tlhaloso) { go_palelwa_boleng("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int faele_lokela = 0; faele_lokela < 칸수; faele_lokela++) if (sekgobana_mong[faele_lokela] == legoro_Tlhaloso && (sekgobana_ditumelelo[faele_lokela] & 8) == 0) 칸위치[faele_lokela] += 시작변위;
            종칸수[legoro_Tlhaloso] += 시작변위;
        }
        return legoro_Tlhaloso;
    }
    static int 부모종(int legoro_Tlhaloso) {
        int Leina = 종부모[legoro_Tlhaloso];
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 종수; ditaelopoeletšwa_lokela++) if (Leina != 0 && legoro_Tlhaloso_leina[ditaelopoeletšwa_lokela] != 0 && 같은말(legoro_Tlhaloso_leina[ditaelopoeletšwa_lokela], Leina)) return ditaelopoeletšwa_lokela;
        return -1;
    }
    static int hwetša_mokgwa(int legoro_Tlhaloso, int Leina, int fomete_boleng) {
        for (int 깊이 = 0; legoro_Tlhaloso >= 0 && 깊이 < 16; 깊이++, legoro_Tlhaloso = 부모종(legoro_Tlhaloso)) {
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 함수수; ditaelopoeletšwa_lokela++) if (mokgwa_mong[ditaelopoeletšwa_lokela] == legoro_Tlhaloso && 같은말(mokgwa_leina_SMS[ditaelopoeletšwa_lokela], Leina) && 같은말(mokgwa_thaepa[ditaelopoeletšwa_lokela], fomete_boleng)) return ditaelopoeletšwa_lokela;
        }
        return -1;
    }
    static int leina_mokgwa(int legoro_Tlhaloso, String Leina, String fomete_boleng) {
        for (int 깊이 = 0; legoro_Tlhaloso >= 0 && 깊이 < 16; 깊이++, legoro_Tlhaloso = 부모종(legoro_Tlhaloso))
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 함수수; ditaelopoeletšwa_lokela++) if (mokgwa_mong[ditaelopoeletšwa_lokela] == legoro_Tlhaloso && Thalokontšu_SMS(mokgwa_leina_SMS[ditaelopoeletšwa_lokela], Leina) && Thalokontšu_SMS(mokgwa_thaepa[ditaelopoeletšwa_lokela], fomete_boleng)) return ditaelopoeletšwa_lokela;
        return -1;
    }
    static int 형종류(int Leina) { return Faele[상가[Leina]] == 'L' || Faele[상가[Leina]] == '[' ? 2 : 1; }
    static boolean thomiša(int legoro_Tlhaloso, int taelo_Thomišo) {
        if (legoro_Tlhaloso < 0 || Phošo) return false;
        if (legoro_Tlhaloso_boemo[legoro_Tlhaloso] == 3) { go_palelwa_boleng("NoClassDefFoundError: initialization failed"); return false; }
        if (legoro_Tlhaloso_boemo[legoro_Tlhaloso] == 1 && legoro_threte[legoro_Tlhaloso] != 현재가닥) { 틀위치[freime_lokela] = taelo_Thomišo; 바꿈요청 = true; return false; }
        if (legoro_Tlhaloso_boemo[legoro_Tlhaloso] != 0) return true;
        int 위 = 부모종(legoro_Tlhaloso);
        if (위 >= 0 && !thomiša(위, taelo_Thomišo)) return false;
        legoro_Tlhaloso_boemo[legoro_Tlhaloso] = 1; legoro_threte[legoro_Tlhaloso] = 현재가닥;
        if (thomiša_legoro_Tlhaloso[legoro_Tlhaloso] != 0) {
            틀위치[freime_lokela] = taelo_Thomišo;
            호출(thomiša_legoro_Tlhaloso[legoro_Tlhaloso] - 1); if (!Phošo) thomiša_freime[freime_lokela] = legoro_Tlhaloso + 1;
            return false;
        }
        legoro_Tlhaloso_boemo[legoro_Tlhaloso] = 2; return true;
    }
    static void 필드호출(int lokela, int Taelo, int Diriša) {
        if (!lekola_ya_go_se_fetoge(lokela, 9)) return;
        int mong_boleng = legoro_leina_SMS(상가[lokela]), Leina = Dipadišo_leina(상나[lokela]), fomete_boleng = Dipadišo_thaepa(상나[lokela]);
        if (Thalokontšu_SMS(mong_boleng, "java/lang/System") && (Thalokontšu_SMS(Leina, "out") || Thalokontšu_SMS(Leina, "err")) && Thalokontšu_SMS(fomete_boleng, "Ljava/io/PrintStream;") && Taelo == 178) { 넣기(-1, 2); return; }
        int legoro_Tlhaloso = hwetša_legoro_Tlhaloso(mong_boleng); if (legoro_Tlhaloso < 0 || Phošo) return;
        int 찾음 = -1;
        for (int 읽는자리 = legoro_Tlhaloso, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int faele_lokela = 0; faele_lokela < 칸수; faele_lokela++) if (sekgobana_mong[faele_lokela] == 읽는자리 && 같은말(sekgobana_leina[faele_lokela], Leina) && 같은말(sekgobana_thaepa[faele_lokela], fomete_boleng)) 찾음 = faele_lokela;
        if (찾음 < 0) { go_palelwa_boleng("NoSuchFieldError"); return; }
        boolean ya_go_se_fetoge_boleng_f430d3f5 = Taelo == 178 || Taelo == 179;
        if (ya_go_se_fetoge_boleng_f430d3f5 != ((sekgobana_ditumelelo[찾음] & 8) != 0)) { go_palelwa_boleng("field static/instance mismatch"); return; }
        if (ya_go_se_fetoge_boleng_f430d3f5 && !thomiša(sekgobana_mong[찾음], Diriša)) return;
        int thaepa_boleng = 형종류(fomete_boleng), boleng = 0;
        if (Taelo == 179 || Taelo == 181) boleng = 빼기(thaepa_boleng);
        if (ya_go_se_fetoge_boleng_f430d3f5) { if (Taelo == 178) 넣기(sekgobana_data[찾음], thaepa_boleng); else if (!Phošo) sekgobana_data[찾음] = boleng; return; }
        int selo_Dipadišo = 빼기(2);
        if (!객체유효(selo_Dipadišo)) return;
        if (힙[selo_Dipadišo] < 32 || !종포함(힙[selo_Dipadišo] - 32, mong_boleng)) { go_palelwa_boleng("field receiver type mismatch"); return; }
        int 보관칸 = selo_Dipadišo + 2 + 칸위치[찾음];
        if (Taelo == 180) 넣기(힙[보관칸], thaepa_boleng);
        else if (!Phošo) { 힙[보관칸] = boleng; 힙참조[보관칸] = thaepa_boleng == 2 ? 1 : 0; }
    }
    static boolean 종포함(int legoro_Tlhaloso, int Leina) {
        for (int 중첩깊이 = 0; legoro_Tlhaloso >= 0 && 중첩깊이 < 16; 중첩깊이++, legoro_Tlhaloso = 부모종(legoro_Tlhaloso)) {
            if (같은말(legoro_Tlhaloso_leina[legoro_Tlhaloso], Leina) || (종부모[legoro_Tlhaloso] != 0 && 같은말(종부모[legoro_Tlhaloso], Leina))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[legoro_Tlhaloso]; 안쪽자리++) if (같은말(legoro_lefelokgokagano[legoro_Tlhaloso * 16 + 안쪽자리], Leina)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int paete_data, boolean Tsejana) {
        if (첫값 == paete_data) return true;
        if (첫값 <= 0 || paete_data <= 0 || 힙[첫값] != 1 || 힙[paete_data] != 1 || 힙[첫값 + 1] != 힙[paete_data + 1]) return false;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 힙[첫값 + 1]; ditaelopoeletšwa_lokela++) {
            int kamano_ya_x = 힙[첫값 + 2 + ditaelopoeletšwa_lokela], 세로좌표 = 힙[paete_data + 2 + ditaelopoeletšwa_lokela];
            if (Tsejana) { if (kamano_ya_x == '.') kamano_ya_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (kamano_ya_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int selo_Dipadišo) {
        if (selo_Dipadišo == 0) { go_palelwa_boleng("NullPointerException"); return false; }
        if (selo_Dipadišo < 1 || selo_Dipadišo >= 힙끝 || 힙폭[selo_Dipadišo] < 2 || 힙[selo_Dipadišo] == 0) { go_palelwa_boleng("invalid object reference"); return false; }
        return true;
    }
    static void šireletša_boleng(int selo_Dipadišo) {
        if (selo_Dipadišo > 0 && selo_Dipadišo < 힙끝 && 힙폭[selo_Dipadišo] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = selo_Dipadišo;
    }
    static void bontšha_boleng(int selo_Dipadišo) {
        if (selo_Dipadišo > 0 && selo_Dipadišo < 힙끝 && 힙폭[selo_Dipadišo] >= 2 && 힙[selo_Dipadišo] != 0 && 힙표시[selo_Dipadišo] == 0) {
            힙표시[selo_Dipadišo] = 1; 표시대기[표시수++] = selo_Dipadišo;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < molokoloko_Dipadišo.length; ditaelopoeletšwa_lokela++) bontšha_boleng(molokoloko_Dipadišo[ditaelopoeletšwa_lokela]);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 칸수; ditaelopoeletšwa_lokela++) if ((sekgobana_ditumelelo[ditaelopoeletšwa_lokela] & 8) != 0 && 형종류(sekgobana_thaepa[ditaelopoeletšwa_lokela]) == 2) bontšha_boleng(sekgobana_data[ditaelopoeletšwa_lokela]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            bontšha_boleng(threte_selo[임시값]); bontšha_boleng(threte_nepo[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? freime_lokela : threte_freime[임시값];
            for (int faele_lokela = 임시값 * 32; faele_lokela <= 꼭대기자리; faele_lokela++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[freime_mokgwa[faele_lokela]]; 안쪽자리++) if (kgauswi_thaepa[faele_lokela * 128 + 안쪽자리] == 2) bontšha_boleng(kgauswi_boleng[faele_lokela * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < freime_kgoboko[faele_lokela]; 안쪽자리++) if (스택형[faele_lokela * 128 + 안쪽자리] == 2) bontšha_boleng(스택값[faele_lokela * 128 + 안쪽자리]);
            }
        }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 화면참조.length; ditaelopoeletšwa_lokela++) bontšha_boleng(화면참조[ditaelopoeletšwa_lokela]);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 나중수; ditaelopoeletšwa_lokela++) bontšha_boleng(나중실행[ditaelopoeletšwa_lokela]);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < lota_palotlalo.length; ditaelopoeletšwa_lokela++) bontšha_boleng(lota_palotlalo[ditaelopoeletšwa_lokela]);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 종수; ditaelopoeletšwa_lokela++) bontšha_boleng(종잠금[ditaelopoeletšwa_lokela]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) bontšha_boleng(검사자리);
        bontšha_boleng(던진객체);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 잠시수; ditaelopoeletšwa_lokela++) bontšha_boleng(잠시참조[ditaelopoeletšwa_lokela]);
        while (표시수 > 0) {
            int selo_Dipadišo = 표시대기[--표시수], 분류코드 = 힙[selo_Dipadišo];
            for (int ditaelopoeletšwa_lokela = selo_Dipadišo + 2; ditaelopoeletšwa_lokela < selo_Dipadišo + 힙폭[selo_Dipadišo]; ditaelopoeletšwa_lokela++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[ditaelopoeletšwa_lokela] != 0) bontšha_boleng(힙[ditaelopoeletšwa_lokela]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int botelele_boleng) {
        if (botelele_boleng < 0) { go_palelwa_boleng("NegativeArraySizeException"); return 0; }
        if (botelele_boleng > 힙.length - 3) { go_palelwa_boleng("object heap exhausted"); return 0; }
        int 필요수 = botelele_boleng + 2, selo_Dipadišo = 0;
        if (필요수 <= 힙.length - 힙끝) { selo_Dipadišo = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { selo_Dipadišo = 읽는자리; break; }
            if (selo_Dipadišo != 0) {
                int 남은길이 = 힙폭[selo_Dipadišo] - 필요수;
                if (남은길이 >= 2) { 힙폭[selo_Dipadišo + 필요수] = 남은길이; 힙[selo_Dipadišo + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { selo_Dipadišo = 힙끝; 힙끝 += 필요수; }
        }
        if (selo_Dipadišo == 0) { go_palelwa_boleng("object heap exhausted"); return 0; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 필요수; ditaelopoeletšwa_lokela++) { 힙[selo_Dipadišo + ditaelopoeletšwa_lokela] = 0; 힙참조[selo_Dipadišo + ditaelopoeletšwa_lokela] = 0; 힙폭[selo_Dipadišo + ditaelopoeletšwa_lokela] = 0; }
        arei_elemente[selo_Dipadišo] = 0;
        힙폭[selo_Dipadišo] = 필요수; 힙[selo_Dipadišo] = 종류; 힙[selo_Dipadišo + 1] = botelele_boleng; šireletša_boleng(selo_Dipadišo); return selo_Dipadišo;
    }
    static int 예외종(String leina_ya_go_se_fetoge) {
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/Throwable")) return 1;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/Exception")) return 2;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/io/IOException")) return 11;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(leina_ya_go_se_fetoge, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Leina) {
        for (int ditaelopoeletšwa_lokela = 1; ditaelopoeletšwa_lokela <= 41; ditaelopoeletšwa_lokela++) if (Thalokontšu_SMS(Leina, 예외이름(ditaelopoeletšwa_lokela))) return ditaelopoeletšwa_lokela;
        return 0;
    }
    static String 예외이름(int akhaonte_boleng) {
        if (akhaonte_boleng == 40) return "java/lang/InterruptedException";
        if (akhaonte_boleng == 41) return "한국어/자체/대기중단예외";
        if (akhaonte_boleng == 39) return "java/net/SocketException";
        if (akhaonte_boleng == 20) return "한국어/자체/예외";
        if (akhaonte_boleng == 21) return "한국어/자체/실행예외";
        if (akhaonte_boleng == 22) return "한국어/자체/입출력예외";
        if (akhaonte_boleng == 23) return "한국어/자체/대기시간초과예외";
        if (akhaonte_boleng == 24) return "한국어/자체/주소확인예외";
        if (akhaonte_boleng == 25) return "한국어/자체/파일없음예외";
        if (akhaonte_boleng == 26) return "한국어/자체/통신예외";
        if (akhaonte_boleng == 27) return "한국어/자체/잘못된인수예외";
        if (akhaonte_boleng == 28) return "한국어/자체/숫자형식예외";
        if (akhaonte_boleng == 29) return "한국어/자체/범위예외";
        if (akhaonte_boleng == 30) return "한국어/자체/배열범위예외";
        if (akhaonte_boleng == 31) return "한국어/자체/문자열범위예외";
        if (akhaonte_boleng == 32) return "한국어/자체/빈참조예외";
        if (akhaonte_boleng == 33) return "한국어/자체/산술예외";
        if (akhaonte_boleng == 34) return "한국어/자체/상태예외";
        if (akhaonte_boleng == 35) return "한국어/자체/형변환예외";
        if (akhaonte_boleng == 36) return "한국어/자체/음수배열크기예외";
        if (akhaonte_boleng == 37) return "한국어/자체/arei_lota_go_palelwa";
        if (akhaonte_boleng == 38) return "한국어/자체/가닥상태예외";
        if (akhaonte_boleng == 1) return "java/lang/Throwable"; if (akhaonte_boleng == 2) return "java/lang/Exception";
        if (akhaonte_boleng == 3) return "java/lang/RuntimeException"; if (akhaonte_boleng == 4) return "java/lang/ArithmeticException";
        if (akhaonte_boleng == 5) return "java/lang/NullPointerException"; if (akhaonte_boleng == 6) return "java/lang/IndexOutOfBoundsException";
        if (akhaonte_boleng == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (akhaonte_boleng == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (akhaonte_boleng == 9) return "java/lang/IllegalArgumentException"; if (akhaonte_boleng == 10) return "java/lang/NumberFormatException";
        if (akhaonte_boleng == 11) return "java/io/IOException"; if (akhaonte_boleng == 12) return "java/io/FileNotFoundException";
        if (akhaonte_boleng == 17) return "java/lang/ArrayStoreException";
        if (akhaonte_boleng == 18) return "java/net/UnknownHostException";
        if (akhaonte_boleng == 19) return "java/net/SocketTimeoutException";
        if (akhaonte_boleng == 16) return "java/lang/IllegalThreadStateException";
        if (akhaonte_boleng == 13) return "java/lang/IllegalStateException"; if (akhaonte_boleng == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int akhaonte_boleng) {
        if (akhaonte_boleng == 40) return 2;
        if (akhaonte_boleng == 41) return 40;
        if (akhaonte_boleng == 39) return 11;
        if (akhaonte_boleng == 1) return 0;
        if (akhaonte_boleng == 2) return 1;
        if (akhaonte_boleng == 3) return 2;
        if (akhaonte_boleng == 4) return 3;
        if (akhaonte_boleng == 5) return 3;
        if (akhaonte_boleng == 6) return 3;
        if (akhaonte_boleng == 7) return 6;
        if (akhaonte_boleng == 8) return 6;
        if (akhaonte_boleng == 9) return 3;
        if (akhaonte_boleng == 10) return 9;
        if (akhaonte_boleng == 11) return 2;
        if (akhaonte_boleng == 12) return 11;
        if (akhaonte_boleng == 13) return 3;
        if (akhaonte_boleng == 14) return 3;
        if (akhaonte_boleng == 15) return 3;
        if (akhaonte_boleng == 16) return 9;
        if (akhaonte_boleng == 17) return 3;
        if (akhaonte_boleng == 18) return 11;
        if (akhaonte_boleng == 19) return 11;
        if (akhaonte_boleng == 20) return 2;
        if (akhaonte_boleng == 21) return 3;
        if (akhaonte_boleng == 22) return 11;
        if (akhaonte_boleng == 23) return 22;
        if (akhaonte_boleng == 24) return 22;
        if (akhaonte_boleng == 25) return 22;
        if (akhaonte_boleng == 26) return 22;
        if (akhaonte_boleng == 27) return 9;
        if (akhaonte_boleng == 28) return 27;
        if (akhaonte_boleng == 29) return 6;
        if (akhaonte_boleng == 30) return 29;
        if (akhaonte_boleng == 31) return 29;
        if (akhaonte_boleng == 32) return 5;
        if (akhaonte_boleng == 33) return 4;
        if (akhaonte_boleng == 34) return 13;
        if (akhaonte_boleng == 35) return 14;
        if (akhaonte_boleng == 36) return 15;
        if (akhaonte_boleng == 37) return 17;
        if (akhaonte_boleng == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int kgonthe_boleng, int 요구값) {
        for (int 깊이 = 0; kgonthe_boleng != 0 && 깊이 < 16; 깊이++, kgonthe_boleng = 예외부모(kgonthe_boleng))
            if (kgonthe_boleng == 요구값) return true;
        return false;
    }
    static void 예외던짐(int akhaonte_boleng, String faele_ya_MPALE_Dipadišo) {
        int selo_Dipadišo = 새기억(9, 2); if (Phošo) return;
        힙[selo_Dipadišo + 2] = akhaonte_boleng; 힙[selo_Dipadišo + 3] = go_nea_ditirelo_tlhaka(faele_ya_MPALE_Dipadišo); 힙참조[selo_Dipadišo + 3] = 1;
        던진객체 = selo_Dipadišo; Phošo = true;
    }
    static boolean 맞는객체(int selo_Dipadišo, int Leina) {
        if (selo_Dipadišo == 0) return true;
        if (!객체유효(selo_Dipadišo)) return false;
        int 분류코드 = 힙[selo_Dipadišo];
        if (Thalokontšu_SMS(Leina, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Leina);
        if (분류코드 == 9) { int nepo_atrese = 예외상수(Leina); return nepo_atrese != 0 && 예외포함(힙[selo_Dipadišo + 2], nepo_atrese); }
        if (분류코드 == 1) return Thalokontšu_SMS(Leina, "java/lang/String") || Thalokontšu_SMS(Leina, "java/lang/CharSequence");
        if (분류코드 == 4) return Thalokontšu_SMS(Leina, "java/lang/StringBuilder") || Thalokontšu_SMS(Leina, "java/lang/CharSequence");
        if (분류코드 == 10) return Thalokontšu_SMS(Leina, "java/util/ArrayList") || Thalokontšu_SMS(Leina, "java/util/List");
        if (분류코드 == 11) return Thalokontšu_SMS(Leina, "java/util/HashMap") || Thalokontšu_SMS(Leina, "java/util/Map");
        if (분류코드 == 12) return Thalokontšu_SMS(Leina, "java/lang/Integer") || Thalokontšu_SMS(Leina, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[selo_Dipadišo + 13] != 0) return 한국어화면종(Leina) == 분류코드 || Thalokontšu_SMS(Leina, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Leina) == 0 && 화면종(Leina) == 분류코드) || Thalokontšu_SMS(Leina, "java/awt/Component") || Thalokontšu_SMS(Leina, "java/awt/Container") || Thalokontšu_SMS(Leina, "javax/swing/JComponent");
        if (분류코드 == 29) return Thalokontšu_SMS(Leina, 힙[selo_Dipadišo + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Thalokontšu_SMS(Leina, "java/awt/FlowLayout") || Thalokontšu_SMS(Leina, "java/awt/LayoutManager");
        if (분류코드 == 17) return Thalokontšu_SMS(Leina, "java/net/Socket");
        if (분류코드 == 18) return Thalokontšu_SMS(Leina, "java/net/ServerSocket");
        if (분류코드 == 19) return Thalokontšu_SMS(Leina, 힙[selo_Dipadišo + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Thalokontšu_SMS(Leina, "java/net/InetAddress");
        if (분류코드 == 15) return Thalokontšu_SMS(Leina, "java/net/DatagramSocket");
        if (분류코드 == 16) return Thalokontšu_SMS(Leina, "java/net/DatagramPacket");
        if (분류코드 == 13) return Thalokontšu_SMS(Leina, 힙[selo_Dipadišo + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Thalokontšu_SMS(Leina, "[I"); if (분류코드 == 20) return Thalokontšu_SMS(Leina, "[B"); if (분류코드 == 21) return Thalokontšu_SMS(Leina, "[Z");
        if (분류코드 == 22) return Thalokontšu_SMS(Leina, "[C"); if (분류코드 == 23) return Thalokontšu_SMS(Leina, "[S");
        if (분류코드 != 3) return false;
        if (Thalokontšu_SMS(Leina, "[Ljava/lang/Object;")) return true;
        int karolo = arei_elemente[selo_Dipadišo];
        if (karolo == -1) return Thalokontšu_SMS(Leina, "[Ljava/lang/String;") || Thalokontšu_SMS(Leina, "[Ljava/lang/CharSequence;");
        if (karolo == 0) return false;
        if (배열종비교(karolo, Leina)) return true;
        if ((Thalokontšu_SMS(karolo, "java/lang/String") || Thalokontšu_SMS(karolo, "java/lang/StringBuilder")) && Thalokontšu_SMS(Leina, "[Ljava/lang/CharSequence;")) return true;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 종수; ditaelopoeletšwa_lokela++) if (같은말(legoro_Tlhaloso_leina[ditaelopoeletšwa_lokela], karolo)) {
            for (int khouto_ya_tlhaka = ditaelopoeletšwa_lokela, 중첩깊이 = 0; khouto_ya_tlhaka >= 0 && 중첩깊이 < 16; 중첩깊이++, khouto_ya_tlhaka = 부모종(khouto_ya_tlhaka)) {
                if (배열종비교(종부모[khouto_ya_tlhaka], Leina)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[khouto_ya_tlhaka]; 안쪽자리++) if (배열종비교(legoro_lefelokgokagano[khouto_ya_tlhaka * 16 + 안쪽자리], Leina)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int leina_ya_go_se_fetoge, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (leina_ya_go_se_fetoge == 0 || 항목수 < 4 || Faele[검사자리] != '[' || Faele[검사자리 + 1] != 'L' || Faele[검사자리 + 항목수 - 1] != ';' || 상나[leina_ya_go_se_fetoge] != 항목수 - 3) return false;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수 - 3; ditaelopoeletšwa_lokela++) if (Faele[상가[leina_ya_go_se_fetoge] + ditaelopoeletšwa_lokela] != Faele[검사자리 + 2 + ditaelopoeletšwa_lokela]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Phošo = false;
        while (freime_lokela >= 현재가닥 * 32) {
            int faele_lokela = freime_mokgwa[freime_lokela], 읽는자리 = freime_taelo[freime_lokela];
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 잡기수; ditaelopoeletšwa_lokela++) if (잡기함수[ditaelopoeletšwa_lokela] == faele_lokela && 읽는자리 >= 잡기시작[ditaelopoeletšwa_lokela] && 읽는자리 < 잡기끝[ditaelopoeletšwa_lokela]
                && (잡기종[ditaelopoeletšwa_lokela] == 0 || 맞는객체(던진객체, 잡기종[ditaelopoeletšwa_lokela]))) {
                틀위치[freime_lokela] = 잡기위치[ditaelopoeletšwa_lokela]; freime_kgoboko[freime_lokela] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (thomiša_freime[freime_lokela] != 0) legoro_Tlhaloso_boemo[thomiša_freime[freime_lokela] - 1] = 3;
            if (틀잠금[freime_lokela] != 0) { 잠금풀기(틀잠금[freime_lokela]); 틀잠금[freime_lokela] = 0; }
            freime_lokela--;
        }
        mošomiši.Ngwala("Uncaught ");
        if (힙[던진객체] == 9) { mošomiši.Ngwala(예외이름(힙[던진객체 + 2])); mošomiši.Ngwala(": "); ngwala_SMS(힙[던진객체 + 3]); }
        else mošomiši.Ngwala("user exception");
        mošomiši.ngwala_tlhaka_boleng(10); 던진객체 = 0; Phošo = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void kgoboko_taelo(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int paete_data = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식); 넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(paete_data, 둘째형식); return; }
        int khouto_ya_tlhaka = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(khouto_ya_tlhaka, 셋째형식); 넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식); 넣기(khouto_ya_tlhaka, 셋째형식); 넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(khouto_ya_tlhaka, 셋째형식); 넣기(paete_data, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int leina_ya_go_se_fetoge, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(leina_ya_go_se_fetoge);
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/lang/Thread") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(leina_ya_go_se_fetoge) != 0) { 분류코드 = 화면종(leina_ya_go_se_fetoge); 유효길이 = 12; }
        if (분류코드 == 0) {
            int khouto_ya_tlhaka = hwetša_legoro_Tlhaloso(leina_ya_go_se_fetoge); if (khouto_ya_tlhaka < 0 || Phošo || !thomiša(khouto_ya_tlhaka, 시작점)) return;
            분류코드 = 32 + khouto_ya_tlhaka; 유효길이 = 종칸수[khouto_ya_tlhaka];
        }
        int selo_Dipadišo = aba_Bobolokelo(분류코드, 유효길이); if (Phošo) return;
        if (분류코드 == 13 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/작업가닥")) 힙[selo_Dipadišo + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(leina_ya_go_se_fetoge) != 0) 힙[selo_Dipadišo + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[selo_Dipadišo + 2] = -1;
        if (분류코드 == 9) 힙[selo_Dipadišo + 2] = 예외참조;
        넣기(selo_Dipadišo, 2);
    }
    static boolean 값같음(int 첫값, int paete_data) {
        if (첫값 == paete_data) return true;
        if (첫값 == 0 || paete_data == 0 || 첫값 < 0 || paete_data < 0 || 첫값 >= 힙끝 || paete_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[paete_data] == 1) return 글같음(첫값, paete_data, false);
        return 힙[첫값] == 12 && 힙[paete_data] == 12 && 힙[첫값 + 2] == 힙[paete_data + 2];
    }
    static int 글조각(int selo_Dipadišo, int 시작자리, int 끝자리) {
        if (!selo_boleng(selo_Dipadišo, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[selo_Dipadišo + 1]) { go_palelwa_boleng("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = aba_Bobolokelo(1, 끝자리 - 시작자리); if (Phošo) return 0;
        for (int ditaelopoeletšwa_lokela = 시작자리; ditaelopoeletšwa_lokela < 끝자리; ditaelopoeletšwa_lokela++) 힙[반환값 + 2 + ditaelopoeletšwa_lokela - 시작자리] = 힙[selo_Dipadišo + 2 + ditaelopoeletšwa_lokela];
        return 반환값;
    }
    static int kopanyo_SMS(int 첫값, int paete_data) {
        if (!selo_boleng(첫값, 1) || !selo_boleng(paete_data, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], mokgwa_lokela = 힙[paete_data + 1], 반환값 = aba_Bobolokelo(1, 항목수 + mokgwa_lokela); if (Phošo) return 0;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 힙[반환값 + 2 + ditaelopoeletšwa_lokela] = 힙[첫값 + 2 + ditaelopoeletšwa_lokela];
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < mokgwa_lokela; ditaelopoeletšwa_lokela++) 힙[반환값 + 2 + 항목수 + ditaelopoeletšwa_lokela] = 힙[paete_data + 2 + ditaelopoeletšwa_lokela];
        return 반환값;
    }
    static boolean 기본호출(int mong, int leina_ya_go_se_fetoge, int 서술상수, int 명령코드) {
        if (Thalokontšu_SMS(mong, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "개수") && Thalokontšu_SMS(서술상수, "()I")) { 넣기(mošomiši.인수개수() - 1, 1); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "Sengwalwa") && Thalokontšu_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= mošomiši.인수개수() - 1) 예외던짐(29, "phethagatša_taelo 인수 범위를 벗어났습니다");
                else 넣기(go_nea_ditirelo_tlhaka(mošomiši.인수(순번 + 1)), 2);
                return true;
            }
            go_palelwa_boleng("지원하지 않는 한국어 phethagatša_taelo 인수 호출"); return true;
        }
        if (Thalokontšu_SMS(mong, "한국어/자체/작업가닥")) { tiragalo_threte(leina_ya_go_se_fetoge, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(mong)) { 한국어화면호출(mong, leina_ya_go_se_fetoge, 서술상수, 명령코드); return true; }
        if (화면소유(mong)) { 화면호출(mong, leina_ya_go_se_fetoge, 서술상수, 명령코드); return true; }
        if (Thalokontšu_SMS(mong, "java/net/Socket") || Thalokontšu_SMS(mong, "java/net/ServerSocket") || Thalokontšu_SMS(mong, "java/io/InputStream") || Thalokontšu_SMS(mong, "java/io/OutputStream")) { 흐름호출(mong, leina_ya_go_se_fetoge, 서술상수, 명령코드); return true; }
        if (Thalokontšu_SMS(mong, "한국어/자체/khenele_boleng") && 명령코드 == 184) {
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "화면너비") && Thalokontšu_SMS(서술상수, "()I")) { 넣기(mošomiši.화면너비(), 1); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "화면높이") && Thalokontšu_SMS(서술상수, "()I")) { 넣기(mošomiši.화면높이(), 1); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "밀리초") && Thalokontšu_SMS(서술상수, "()I")) { 넣기(mošomiši.밀리초(), 1); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "그림대기") && Thalokontšu_SMS(서술상수, "()I")) { 넣기(mošomiši.그림대기(), 1); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "사각형") && Thalokontšu_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), kamano_ya_x = 빼기(1); 넣기(mošomiši.사각형(kamano_ya_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Thalokontšu_SMS(mong, "java/net/InetAddress") || Thalokontšu_SMS(mong, "java/net/DatagramPacket") || Thalokontšu_SMS(mong, "java/net/DatagramSocket")) { 통신호출(mong, leina_ya_go_se_fetoge, 서술상수, 명령코드); return true; }
        if (Thalokontšu_SMS(mong, "java/lang/Thread")) { 가닥호출(leina_ya_go_se_fetoge, 서술상수, 명령코드); return true; }
        if (Thalokontšu_SMS(mong, "java/lang/Object")) {
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>") && Thalokontšu_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "equals") && Thalokontšu_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int paete_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == paete_data ? 1 : 0, 1); return true; }
        }
        if (예외상수(mong) != 0) {
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>") && 명령코드 == 183 && (Thalokontšu_SMS(서술상수, "()V") || Thalokontšu_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int temoši = Thalokontšu_SMS(서술상수, "()V") ? 0 : 빼기(2), selo_Dipadišo = 빼기(2);
                if (selo_boleng(selo_Dipadišo, 9)) { 힙[selo_Dipadišo + 3] = temoši; 힙참조[selo_Dipadišo + 3] = 1; } return true;
            }
            if ((Thalokontšu_SMS(leina_ya_go_se_fetoge, "getMessage") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "설명")) && Thalokontšu_SMS(서술상수, "()Ljava/lang/String;")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 9)) 넣기(힙[selo_Dipadišo + 3], 2); return true; }
        }
        if (Thalokontšu_SMS(mong, "java/lang/String")) {
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "getBytes") && (Thalokontšu_SMS(서술상수, "()[B") || Thalokontšu_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int go_enkhouta_leina = Thalokontšu_SMS(서술상수, "()[B") ? 0 : 빼기(2), selo_Dipadišo = 빼기(2);
                if (!selo_boleng(selo_Dipadišo, 1)) return true;
                if (go_enkhouta_leina != 0 && !글같음(go_enkhouta_leina, go_nea_ditirelo_tlhaka("UTF-8"), false) && !글같음(go_enkhouta_leina, go_nea_ditirelo_tlhaka("UTF8"), false) && !글같음(go_enkhouta_leina, go_nea_ditirelo_tlhaka("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[selo_Dipadišo + 1], 반환값 = aba_Bobolokelo(20, 항목수 * 3), 사용수 = 0; if (Phošo) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int khouto_ya_tlhaka = 힙[selo_Dipadišo + 2 + 안쪽자리];
                    if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[selo_Dipadišo + 3 + 안쪽자리] >= 0xdc00 && 힙[selo_Dipadišo + 3 + 안쪽자리] <= 0xdfff) khouto_ya_tlhaka = 0x10000 + ((khouto_ya_tlhaka - 0xd800) << 10) + 힙[selo_Dipadišo + 2 + ++안쪽자리] - 0xdc00;
                    else if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdfff) khouto_ya_tlhaka = '?';
                    if (khouto_ya_tlhaka < 128) 힙[반환값 + 2 + 사용수++] = khouto_ya_tlhaka;
                    else { int 바이트수 = khouto_ya_tlhaka < 2048 ? 2 : khouto_ya_tlhaka < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | khouto_ya_tlhaka >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | khouto_ya_tlhaka >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "valueOf") && Thalokontšu_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "equals") && Thalokontšu_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int paete_data = 빼기(2), 첫값 = 빼기(2); if (selo_boleng(첫값, 1)) 넣기(글같음(첫값, paete_data, false) ? 1 : 0, 1); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "isEmpty") && Thalokontšu_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (selo_boleng(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "substring") && (Thalokontšu_SMS(서술상수, "(I)Ljava/lang/String;") || Thalokontšu_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Thalokontšu_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (selo_boleng(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "concat") && Thalokontšu_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int paete_data = 빼기(2), 첫값 = 빼기(2); 넣기(kopanyo_SMS(첫값, paete_data), 2); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "hashCode") && Thalokontšu_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), haše_boleng = 0; if (selo_boleng(첫값, 1)) { for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 힙[첫값 + 1]; ditaelopoeletšwa_lokela++) haše_boleng = haše_boleng * 31 + 힙[첫값 + 2 + ditaelopoeletšwa_lokela]; 넣기(haše_boleng, 1); } return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "toString") && Thalokontšu_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (selo_boleng(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Thalokontšu_SMS(mong, "java/lang/Integer")) {
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "valueOf") && Thalokontšu_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_boleng = 빼기(1), selo_Dipadišo = data_boleng >= -128 && data_boleng <= 127 ? lota_palotlalo[data_boleng + 128] : 0; if (selo_Dipadišo == 0) { selo_Dipadišo = aba_Bobolokelo(12, 1); if (!Phošo) { 힙[selo_Dipadišo + 2] = data_boleng; if (data_boleng >= -128 && data_boleng <= 127) lota_palotlalo[data_boleng + 128] = selo_Dipadišo; } } 넣기(selo_Dipadišo, 2); return true; }
            if (명령코드 == 183 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>") && Thalokontšu_SMS(서술상수, "(I)V")) { int data_boleng = 빼기(1), selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 12)) 힙[selo_Dipadišo + 2] = data_boleng; return true; }
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "intValue") && Thalokontšu_SMS(서술상수, "()I")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 12)) 넣기(힙[selo_Dipadišo + 2], 1); return true; }
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "toString") && Thalokontšu_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
        }
        if (Thalokontšu_SMS(mong, "java/lang/Math") && 명령코드 == 184) {
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "abs") && Thalokontšu_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Thalokontšu_SMS(leina_ya_go_se_fetoge, "min") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "max")) && Thalokontšu_SMS(서술상수, "(II)I")) { int paete_data = 빼기(1), 첫값 = 빼기(1); 넣기(Thalokontšu_SMS(leina_ya_go_se_fetoge, "min") ? (첫값 < paete_data ? 첫값 : paete_data) : (첫값 > paete_data ? 첫값 : paete_data), 1); return true; }
        }
        if (Thalokontšu_SMS(mong, "java/lang/System") && 명령코드 == 184) {
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "gc") && Thalokontšu_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "arraycopy") && Thalokontšu_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), boyo_boleng_lokela = 빼기(1), paete_data = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(paete_data)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[paete_data] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) go_palelwa_boleng("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || boyo_boleng_lokela < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || boyo_boleng_lokela > 힙[paete_data + 1] - 항목수) go_palelwa_boleng("ArrayIndexOutOfBoundsException");
                    else if (첫값 == paete_data && boyo_boleng_lokela > 시작자리) { for (int ditaelopoeletšwa_lokela = 항목수 - 1; ditaelopoeletšwa_lokela >= 0; ditaelopoeletšwa_lokela--) 힙[paete_data + 2 + boyo_boleng_lokela + ditaelopoeletšwa_lokela] = 힙[첫값 + 2 + 시작자리 + ditaelopoeletšwa_lokela]; }
                    else { for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수 && !Phošo; ditaelopoeletšwa_lokela++) { int data_boleng = 힙[첫값 + 2 + 시작자리 + ditaelopoeletšwa_lokela]; if (분류코드 != 3 || 배열저장가능(paete_data, data_boleng)) 힙[paete_data + 2 + boyo_boleng_lokela + ditaelopoeletšwa_lokela] = data_boleng; } }
                }
                return true;
            }
        }
        if (Thalokontšu_SMS(mong, "java/util/ArrayList") || Thalokontšu_SMS(mong, "java/util/List") || Thalokontšu_SMS(mong, "java/util/HashMap") || Thalokontšu_SMS(mong, "java/util/Map")) {
            모음호출(mong, leina_ya_go_se_fetoge, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int selo_Dipadišo, int 필요수) {
        int 이전값 = 힙[selo_Dipadišo + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int data_arei = aba_Bobolokelo(3, 다음자리); if (Phošo) return;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 용량값; ditaelopoeletšwa_lokela++) 힙[data_arei + 2 + ditaelopoeletšwa_lokela] = 힙[이전값 + 2 + ditaelopoeletšwa_lokela];
        힙[selo_Dipadišo + 2] = data_arei; 힙참조[selo_Dipadišo + 2] = 1;
    }
    static void 모음호출(int mong, int leina_ya_go_se_fetoge, int 서술상수, int 명령코드) {
        boolean 대응참조 = Thalokontšu_SMS(mong, "java/util/HashMap") || Thalokontšu_SMS(mong, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>") && 명령코드 == 183 && Thalokontšu_SMS(서술상수, "()V")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 분류코드)) 모음늘리기(selo_Dipadišo, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { go_palelwa_boleng("invalid collection invocation"); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "size") && Thalokontšu_SMS(서술상수, "()I") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "isEmpty") && Thalokontšu_SMS(서술상수, "()Z")) {
            int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 분류코드)) 넣기(Thalokontšu_SMS(leina_ya_go_se_fetoge, "size") ? 힙[selo_Dipadišo + 3] : 힙[selo_Dipadišo + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "clear") && Thalokontšu_SMS(서술상수, "()V")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 분류코드)) { int data_arei = 힙[selo_Dipadišo + 2]; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 힙[data_arei + 1]; ditaelopoeletšwa_lokela++) 힙[data_arei + 2 + ditaelopoeletšwa_lokela] = 0; 힙[selo_Dipadišo + 3] = 0; } return; }
        if (!대응참조 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "add") && Thalokontšu_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_boleng = 빼기(2), selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 10)) return;
            int 항목수 = 힙[selo_Dipadišo + 3]; 모음늘리기(selo_Dipadišo, 항목수 + 1); if (!Phošo) { 힙[힙[selo_Dipadišo + 2] + 2 + 항목수] = data_boleng; 힙[selo_Dipadišo + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Thalokontšu_SMS(leina_ya_go_se_fetoge, "get") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "remove")) && Thalokontšu_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "set") && Thalokontšu_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Thalokontšu_SMS(leina_ya_go_se_fetoge, "set"); int data_boleng = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), selo_Dipadišo = 빼기(2);
            if (!selo_boleng(selo_Dipadišo, 10)) return;
            int 항목수 = 힙[selo_Dipadišo + 3], data_arei = 힙[selo_Dipadišo + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_arei + 2 + 항목자리];
            if (지정여부) 힙[data_arei + 2 + 항목자리] = data_boleng;
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "remove")) { for (int ditaelopoeletšwa_lokela = 항목자리 + 1; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 힙[data_arei + 1 + ditaelopoeletšwa_lokela] = 힙[data_arei + 2 + ditaelopoeletšwa_lokela]; 힙[data_arei + 1 + 항목수] = 0; 힙[selo_Dipadišo + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Thalokontšu_SMS(leina_ya_go_se_fetoge, "get") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "remove")) && Thalokontšu_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "put") && Thalokontšu_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "containsKey") && Thalokontšu_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Thalokontšu_SMS(leina_ya_go_se_fetoge, "put"), tloša = Thalokontšu_SMS(leina_ya_go_se_fetoge, "remove");
            int data_boleng = 넣기여부 ? 빼기(2) : 0, khii_Dipadišo = 빼기(2), selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 11)) return;
            int 항목수 = 힙[selo_Dipadišo + 3], data_arei = 힙[selo_Dipadišo + 2], 찾은여부 = -1;
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) if (값같음(khii_Dipadišo, 힙[data_arei + 2 + 2 * ditaelopoeletšwa_lokela])) { 찾은여부 = ditaelopoeletšwa_lokela; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_arei + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(selo_Dipadišo, (항목수 + 1) * 2); data_arei = 힙[selo_Dipadišo + 2]; 찾은여부 = 항목수; if (!Phošo) 힙[selo_Dipadišo + 3] = 항목수 + 1; }
                if (!Phošo) { 힙[data_arei + 2 + 2 * 찾은여부] = khii_Dipadišo; 힙[data_arei + 3 + 2 * 찾은여부] = data_boleng; }
            }
            if (tloša && 찾은여부 >= 0) { for (int ditaelopoeletšwa_lokela = 찾은여부 + 1; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) { 힙[data_arei + 2 * ditaelopoeletšwa_lokela] = 힙[data_arei + 2 + 2 * ditaelopoeletšwa_lokela]; 힙[data_arei + 1 + 2 * ditaelopoeletšwa_lokela] = 힙[data_arei + 3 + 2 * ditaelopoeletšwa_lokela]; } 힙[data_arei + 2 * 항목수] = 0; 힙[data_arei + 1 + 2 * 항목수] = 0; 힙[selo_Dipadišo + 3] = 항목수 - 1; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        go_palelwa_boleng("unsupported collection method");
    }
    static boolean 잠금얻기(int selo_Dipadišo) {
        if (!객체유효(selo_Dipadišo)) return false;
        if (잠금깊이[selo_Dipadišo] != 0 && 잠금주인[selo_Dipadišo] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[selo_Dipadišo] = 현재가닥 + 1; 잠금깊이[selo_Dipadišo]++; return true;
    }
    static void 잠금풀기(int selo_Dipadišo) {
        if (!객체유효(selo_Dipadišo)) return;
        if (잠금깊이[selo_Dipadišo] == 0 || 잠금주인[selo_Dipadišo] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[selo_Dipadišo] == 0) 잠금주인[selo_Dipadišo] = 0;
    }
    static boolean fetogela_threte() {
        threte_freime[현재가닥] = freime_lokela;
        if (freime_lokela < 현재가닥 * 32) threte_boemo[현재가닥] = 3;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 가닥수; ditaelopoeletšwa_lokela++) if (threte_boemo[ditaelopoeletšwa_lokela] == 2 && threte_boemo[가닥대기[ditaelopoeletšwa_lokela]] == 3) threte_boemo[ditaelopoeletšwa_lokela] = 1;
        for (int ditaelopoeletšwa_lokela = 1; ditaelopoeletšwa_lokela <= 가닥수; ditaelopoeletšwa_lokela++) {
            int 다음자리 = (현재가닥 + ditaelopoeletšwa_lokela) % 가닥수;
            if (threte_boemo[다음자리] == 1) { 현재가닥 = 다음자리; freime_lokela = threte_freime[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 가닥수; ditaelopoeletšwa_lokela++) if (threte_boemo[ditaelopoeletšwa_lokela] != 3) { go_palelwa_boleng("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int leina_ya_go_se_fetoge, int 서술상수, int 명령코드) { tiragalo_threte(leina_ya_go_se_fetoge, 서술상수, 명령코드, false); }
    static void tiragalo_threte(int leina_ya_go_se_fetoge, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, 한국어 ? "e_thibetšwe_mošomo" : "yield") && Thalokontšu_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "currentThread") && Thalokontšu_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(threte_selo[현재가닥], 2); return; }
        if (명령코드 == 183 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>") && (Thalokontšu_SMS(서술상수, "()V") || Thalokontšu_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int nepo_atrese = Thalokontšu_SMS(서술상수, "()V") ? 0 : 빼기(2), selo_Dipadišo = 빼기(2);
            if (!객체유효(selo_Dipadišo)) return;
            if (힙[selo_Dipadišo] == 13) { 힙[selo_Dipadišo + 2] = nepo_atrese; 힙참조[selo_Dipadišo + 2] = 1; }
            else if (nepo_atrese != 0) go_palelwa_boleng("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Thalokontšu_SMS(leina_ya_go_se_fetoge, 한국어 ? "Thomišo_mošomo" : "start") || Thalokontšu_SMS(leina_ya_go_se_fetoge, 한국어 ? "기다리기" : "join")) && Thalokontšu_SMS(서술상수, "()V") || 명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, 한국어 ? "살아있는가" : "isAlive") && Thalokontšu_SMS(서술상수, "()Z")) {
            int selo_Dipadišo = 빼기(2); if (!객체유효(selo_Dipadišo)) return;
            int akhaonte_boleng = -1; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 가닥수; ditaelopoeletšwa_lokela++) if (threte_selo[ditaelopoeletšwa_lokela] == selo_Dipadišo) akhaonte_boleng = ditaelopoeletšwa_lokela;
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, 한국어 ? "살아있는가" : "isAlive")) { 넣기(akhaonte_boleng >= 0 && threte_boemo[akhaonte_boleng] != 3 ? 1 : 0, 1); return; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, 한국어 ? "기다리기" : "join")) { if (akhaonte_boleng >= 0 && threte_boemo[akhaonte_boleng] != 3) { 가닥대기[현재가닥] = akhaonte_boleng; threte_boemo[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (akhaonte_boleng >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { go_palelwa_boleng("thread limit (4 including main)"); return; }
            int nepo_atrese = 힙[selo_Dipadišo] == 13 ? 힙[selo_Dipadišo + 2] : selo_Dipadišo;
            int faele_lokela = nepo_atrese > 0 && 힙[nepo_atrese] >= 32 ? leina_mokgwa(힙[nepo_atrese] - 32, 한국어 ? "phethagatša_mošomo" : "run", "()V") : -1;
            if (nepo_atrese != 0 && faele_lokela < 0) { go_palelwa_boleng("Runnable.run required"); return; }
            akhaonte_boleng = 가닥수++; threte_selo[akhaonte_boleng] = selo_Dipadišo; threte_nepo[akhaonte_boleng] = nepo_atrese;
            int freime = akhaonte_boleng * 32; threte_freime[akhaonte_boleng] = faele_lokela < 0 ? freime - 1 : freime; threte_boemo[akhaonte_boleng] = faele_lokela < 0 ? 3 : 1;
            if (faele_lokela >= 0) { freime_mokgwa[freime] = faele_lokela; 틀위치[freime] = mokgwa_Thomišo[faele_lokela]; kgauswi_boleng[freime * 128] = nepo_atrese; kgauswi_thaepa[freime * 128] = 2; }
            return;
        }
        go_palelwa_boleng("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], atrese_SMS = new int[16];
    static int kgauswi_atrese() { return atrese_selo(0x7f000001); }
    static int atrese_selo(int boleng) { int selo_Dipadišo = aba_Bobolokelo(14, 1); if (!Phošo) 힙[selo_Dipadišo + 2] = boleng; return selo_Dipadišo; }
    static int 주소해독(int selo_Dipadišo) {
        if (selo_Dipadišo == 0 || 글같음(selo_Dipadišo, go_nea_ditirelo_tlhaka("localhost"), false)) return 0x7f000001;
        if (!selo_boleng(selo_Dipadišo, 1)) return 0;
        int data_boleng = 0, 총수 = 0, atrese_paete = 0, 자릿수 = 0, 항목수 = 힙[selo_Dipadišo + 1];
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela <= 항목수; ditaelopoeletšwa_lokela++) {
            int khouto_ya_tlhaka = ditaelopoeletšwa_lokela == 항목수 ? '.' : 힙[selo_Dipadišo + 2 + ditaelopoeletšwa_lokela];
            if (khouto_ya_tlhaka == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_boleng = data_boleng << 8 | atrese_paete; 총수++; atrese_paete = 자릿수 = 0; }
            else { if (khouto_ya_tlhaka < '0' || khouto_ya_tlhaka > '9' || ++자릿수 > 3 || (atrese_paete = atrese_paete * 10 + khouto_ya_tlhaka - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_boleng;
    }
    static int atrese_tlhaka(int data_boleng) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int atrese_paete = data_boleng >>> 이동비트 & 255;
            if (atrese_paete >= 100) atrese_SMS[항목수++] = '0' + atrese_paete / 100;
            if (atrese_paete >= 10) atrese_SMS[항목수++] = '0' + atrese_paete / 10 % 10;
            atrese_SMS[항목수++] = '0' + atrese_paete % 10; if (이동비트 != 0) atrese_SMS[항목수++] = '.';
        }
        int selo_Dipadišo = aba_Bobolokelo(1, 항목수); if (!Phošo) for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 힙[selo_Dipadišo + 2 + ditaelopoeletšwa_lokela] = atrese_SMS[ditaelopoeletšwa_lokela]; return selo_Dipadišo;
    }
    static void 통신호출(int mong, int leina_ya_go_se_fetoge, int 서술상수, int 명령코드) {
        if (Thalokontšu_SMS(mong, "java/net/InetAddress")) {
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "getLoopbackAddress") && Thalokontšu_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(kgauswi_atrese(), 2); return; }
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "getByName") && Thalokontšu_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_boleng = 주소해독(빼기(2)); if (던진객체 == 0 && !Phošo) 넣기(atrese_selo(data_boleng), 2); return;
            }
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "getHostAddress") && Thalokontšu_SMS(서술상수, "()Ljava/lang/String;")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 14)) 넣기(atrese_tlhaka(힙[selo_Dipadišo + 2]), 2); return; }
        }
        if (Thalokontšu_SMS(mong, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>") && (Thalokontšu_SMS(서술상수, "([BI)V") || Thalokontšu_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean boyo_boleng_Dipadišo = Thalokontšu_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = boyo_boleng_Dipadišo ? 빼기(1) : 0, atrese_Dipadišo = boyo_boleng_Dipadišo ? 빼기(2) : 0;
                int 항목수 = 빼기(1), data_arei = 빼기(2), selo_Dipadišo = 빼기(2);
                if (!selo_boleng(selo_Dipadišo, 16) || !selo_boleng(data_arei, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[data_arei + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (atrese_Dipadišo != 0 && !selo_boleng(atrese_Dipadišo, 14)) return;
                힙[selo_Dipadišo + 2] = data_arei; 힙참조[selo_Dipadišo + 2] = 1; 힙[selo_Dipadišo + 3] = 항목수;
                힙[selo_Dipadišo + 4] = atrese_Dipadišo; 힙참조[selo_Dipadišo + 4] = 1; 힙[selo_Dipadišo + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "setLength") && Thalokontšu_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[selo_Dipadišo + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[selo_Dipadišo + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getData") && Thalokontšu_SMS(서술상수, "()[B") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "getLength") && Thalokontšu_SMS(서술상수, "()I") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "getAddress") && Thalokontšu_SMS(서술상수, "()Ljava/net/InetAddress;") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "getPort") && Thalokontšu_SMS(서술상수, "()I"))) {
                int selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 16)) return;
                int 항목자리 = Thalokontšu_SMS(leina_ya_go_se_fetoge, "getData") ? 2 : Thalokontšu_SMS(leina_ya_go_se_fetoge, "getLength") ? 3 : Thalokontšu_SMS(leina_ya_go_se_fetoge, "getAddress") ? 4 : 5;
                넣기(힙[selo_Dipadišo + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Thalokontšu_SMS(mong, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>") && (Thalokontšu_SMS(서술상수, "()V") || Thalokontšu_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Thalokontšu_SMS(서술상수, "()V") ? 0 : 빼기(1), selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = mošomiši.bula_Netweke(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[selo_Dipadišo + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "setSoTimeout") && Thalokontšu_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[selo_Dipadišo + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "getLocalPort") && Thalokontšu_SMS(서술상수, "()I")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 15)) 넣기(힙[selo_Dipadišo + 2] < 0 ? -1 : mošomiši.Netweke_phote(힙[selo_Dipadišo + 2]), 1); return; }
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "isClosed") && Thalokontšu_SMS(서술상수, "()Z")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 15)) 넣기(힙[selo_Dipadišo + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "close") && Thalokontšu_SMS(서술상수, "()V")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 15) && 힙[selo_Dipadišo + 2] >= 0) { mošomiši.파일서술자닫기(힙[selo_Dipadišo + 2]); 힙[selo_Dipadišo + 2] = -1; } return; }
            if (명령코드 == 182 && (Thalokontšu_SMS(leina_ya_go_se_fetoge, "send") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "receive")) && Thalokontšu_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int sephuthelwana = 빼기(2), selo_Dipadišo = 빼기(2); if (!selo_boleng(sephuthelwana, 16) || !selo_boleng(selo_Dipadišo, 15)) return;
                int data_arei = 힙[sephuthelwana + 2], 유효길이 = 힙[sephuthelwana + 3], 열린파일번호 = 힙[selo_Dipadišo + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "send")) {
                    if (!selo_boleng(힙[sephuthelwana + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 유효길이; ditaelopoeletšwa_lokela++) 통신임시[ditaelopoeletšwa_lokela] = 힙[data_arei + 2 + ditaelopoeletšwa_lokela];
                    if (mošomiši.Romela_Netweke(열린파일번호, 힙[힙[sephuthelwana + 4] + 2], 힙[sephuthelwana + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = mošomiši.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = mošomiši.밀리초();
                        if (힙[selo_Dipadišo + 4] == 0) 힙[selo_Dipadišo + 4] = 현재시각 + 1;
                        if (힙[selo_Dipadišo + 3] > 0 && 현재시각 - (힙[selo_Dipadišo + 4] - 1) >= 힙[selo_Dipadišo + 3]) { 힙[selo_Dipadišo + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(selo_Dipadišo, 2); 넣기(sephuthelwana, 2); 틀위치[freime_lokela] = freime_taelo[freime_lokela]; 바꿈요청 = true; return;
                    }
                    힙[selo_Dipadišo + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 힙[data_arei + 2 + ditaelopoeletšwa_lokela] = (byte)통신임시[ditaelopoeletšwa_lokela];
                    힙[sephuthelwana + 3] = 항목수; 힙[sephuthelwana + 4] = atrese_selo(통신임시[513]); 힙참조[sephuthelwana + 4] = 1; 힙[sephuthelwana + 5] = 통신임시[512];
                }
                return;
            }
        }
        go_palelwa_boleng("unsupported java.net method");
    }
    static boolean 흐름대기(int selo_Dipadišo) {
        int 현재시각 = mošomiši.밀리초();
        if (힙[selo_Dipadišo + 5] == 0) 힙[selo_Dipadišo + 5] = 현재시각 + 1;
        if (힙[selo_Dipadišo + 3] > 0 && 현재시각 - (힙[selo_Dipadišo + 5] - 1) >= 힙[selo_Dipadišo + 3]) { 힙[selo_Dipadišo + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[freime_lokela] = freime_taelo[freime_lokela]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int mong, int leina_ya_go_se_fetoge, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Thalokontšu_SMS(mong, "java/net/ServerSocket"), Stream = Thalokontšu_SMS(mong, "java/io/InputStream") || Thalokontšu_SMS(mong, "java/io/OutputStream");
        if (!Stream && 명령코드 == 183 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>")) {
            boolean 빈여부 = Thalokontšu_SMS(서술상수, "()V"), 이름지정여부 = Thalokontšu_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Thalokontšu_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Thalokontšu_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { go_palelwa_boleng("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), atrese_Dipadišo = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, selo_Dipadišo = 빼기(2);
            if (!selo_boleng(selo_Dipadišo, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !selo_boleng(atrese_Dipadišo, 14)) return;
            int Netweke_atrese = 이름지정여부 ? 주소해독(atrese_Dipadišo) : 주소지정여부 ? 힙[atrese_Dipadišo + 2] : 0x7f000001;
            if (Phošo || 던진객체 != 0) return;
            int 열린파일번호 = mošomiši.Stream_taolo(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? mošomiši.Stream_taolo(1, 열린파일번호, 접속번호) : mošomiši.KGOKAGANYA_Stream(열린파일번호, Netweke_atrese, 접속번호);
            if (처리값 < 0) { mošomiši.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[selo_Dipadišo + 2] = 열린파일번호; 힙[selo_Dipadišo + 4] = 접속번호; 힙[selo_Dipadišo + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Thalokontšu_SMS(leina_ya_go_se_fetoge, "setSoTimeout") && Thalokontšu_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[selo_Dipadišo + 3] = 밀리초값; return; }
        if (!Stream && Thalokontšu_SMS(leina_ya_go_se_fetoge, "close") && Thalokontšu_SMS(서술상수, "()V")) { int selo_Dipadišo = 빼기(2); if (selo_boleng(selo_Dipadišo, 수신쪽 ? 18 : 17) && 힙[selo_Dipadišo + 2] >= 0) { mošomiši.파일서술자닫기(힙[selo_Dipadišo + 2]); 힙[selo_Dipadišo + 2] = -1; } return; }
        if (!Stream && (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getLocalPort") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "getPort") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "isClosed") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "isConnected"))) {
            int selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 수신쪽 ? 18 : 17)) return;
            넣기(Thalokontšu_SMS(leina_ya_go_se_fetoge, "isClosed") ? 힙[selo_Dipadišo + 2] < 0 ? 1 : 0 : Thalokontšu_SMS(leina_ya_go_se_fetoge, "isConnected") ? 힙[selo_Dipadišo + 6] : Thalokontšu_SMS(leina_ya_go_se_fetoge, "getPort") ? 힙[selo_Dipadišo + 4] : 힙[selo_Dipadišo + 2] < 0 ? -1 : mošomiši.Stream_taolo(4, 힙[selo_Dipadišo + 2], 0), 1); return;
        }
        if (수신쪽 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "accept") && Thalokontšu_SMS(서술상수, "()Ljava/net/Socket;")) {
            int selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 18)) return; int 열린파일번호 = mošomiši.Stream_taolo(3, 힙[selo_Dipadišo + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(selo_Dipadišo)) 넣기(selo_Dipadišo, 2); return; }
            힙[selo_Dipadišo + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = aba_Bobolokelo(17, 5); if (Phošo) { mošomiši.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = mošomiši.Stream_taolo(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Thalokontšu_SMS(leina_ya_go_se_fetoge, "getInputStream") && Thalokontšu_SMS(서술상수, "()Ljava/io/InputStream;")) || (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getOutputStream") && Thalokontšu_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 17)) return; if (힙[selo_Dipadišo + 2] < 0 || 힙[selo_Dipadišo + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = aba_Bobolokelo(19, 4); if (Phošo) return; 힙[반환값 + 2] = selo_Dipadišo; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Thalokontšu_SMS(leina_ya_go_se_fetoge, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Thalokontšu_SMS(leina_ya_go_se_fetoge, "read"), 쓰기여부 = Thalokontšu_SMS(leina_ya_go_se_fetoge, "write"), thibela = Thalokontšu_SMS(서술상수, "([B)I") || Thalokontšu_SMS(서술상수, "([B)V"), 부분배열여부 = Thalokontšu_SMS(서술상수, "([BII)I") || Thalokontšu_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, data_arei = thibela || 부분배열여부 ? 빼기(2) : 0;
            int data_boleng = 쓰기여부 && Thalokontšu_SMS(서술상수, "(I)V") ? 빼기(1) : 0, selo_Dipadišo = 빼기(2);
            if (!selo_boleng(selo_Dipadišo, 19)) return; int 부모참조 = 힙[selo_Dipadišo + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "close") && Thalokontšu_SMS(서술상수, "()V")) { mošomiši.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "flush") && Thalokontšu_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[selo_Dipadišo + 3] == 0)) { go_palelwa_boleng("unsupported stream operation"); return; }
            if (thibela || 부분배열여부) { if (!selo_boleng(data_arei, 20)) return; if (thibela) 항목수 = 힙[data_arei + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[data_arei + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[selo_Dipadišo + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? mošomiši.파일한바이트읽기(열린파일번호) : mošomiši.파일한바이트쓰기(열린파일번호, thibela || 부분배열여부 ? 힙[data_arei + 2 + 시작변위 + 완료수] : data_boleng);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (thibela || 부분배열여부)) 힙[data_arei + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(thibela || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[selo_Dipadišo + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(selo_Dipadišo, 2); if (thibela || 부분배열여부) 넣기(data_arei, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(thibela || 부분배열여부)) 넣기(data_boleng, 1); } return;
            }
            힙[selo_Dipadišo + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : thibela || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        go_palelwa_boleng("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int leina_ya_go_se_fetoge) {
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/lefastere")) return 24;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/leibole")) return 26;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/konope")) return 27;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/SMS_lefelwana")) return 28;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int leina_ya_go_se_fetoge) {
        return 한국어화면종(leina_ya_go_se_fetoge) != 0 || Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/화면구성요소") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "한국어/자체/tiragalo_lenaneotetelo");
    }
    static int 화면종(int leina_ya_go_se_fetoge) {
        int 한국어종 = 한국어화면종(leina_ya_go_se_fetoge); if (한국어종 != 0) return 한국어종;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/JFrame")) return 24;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/JPanel")) return 25;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/JLabel")) return 26;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/JButton")) return 27;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/JTextField")) return 28;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/awt/event/ActionEvent")) return 29;
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int leina_ya_go_se_fetoge) {
        return 화면종(leina_ya_go_se_fetoge) != 0 || Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/awt/Component") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "java/awt/Container") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/JComponent") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/AbstractButton") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/text/JTextComponent") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int selo_Dipadišo) { if (!객체유효(selo_Dipadišo)) return false; if (힙[selo_Dipadišo] < 24 || 힙[selo_Dipadišo] > 28) { go_palelwa_boleng("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int selo_Dipadišo, int SMS_Dipadišo) {
        if (SMS_Dipadišo != 0 && !selo_boleng(SMS_Dipadišo, 1)) return;
        int 항목수 = SMS_Dipadišo == 0 ? 0 : 힙[SMS_Dipadišo + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 화면글임시[ditaelopoeletšwa_lokela] = 힙[SMS_Dipadišo + 2 + ditaelopoeletšwa_lokela];
        if (mošomiši.화면글(힙[selo_Dipadišo + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[selo_Dipadišo + 3] = SMS_Dipadišo; 힙참조[selo_Dipadišo + 3] = 1;
    }
    static int 화면문자읽기(int selo_Dipadišo) {
        int akhaonte_boleng = 힙[selo_Dipadišo + 2], 항목수 = mošomiši.화면연결(8, akhaonte_boleng, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { go_palelwa_boleng("GUI text read failed"); return 0; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) { int 부호값 = mošomiši.화면연결(9, akhaonte_boleng, ditaelopoeletšwa_lokela, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = aba_Bobolokelo(1, 사용수); if (!Phošo) for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 사용수; ditaelopoeletšwa_lokela++) 힙[반환값 + 2 + ditaelopoeletšwa_lokela] = 화면글임시[ditaelopoeletšwa_lokela]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 khenele_boleng 화면 기능에 연결한다. Swing selo_boleng/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int mong, int leina_ya_go_se_fetoge, int 서술상수, int 명령코드) {
        if (Thalokontšu_SMS(mong, "한국어/자체/tiragalo_lenaneotetelo")) {
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "나중에실행") && Thalokontšu_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int mošomo_tiro = 빼기(2); if (!객체유효(mošomo_tiro)) return;
                if (나중수 == 8) { go_palelwa_boleng("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = mošomo_tiro; return;
            }
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "사건처리중인가") && Thalokontšu_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            go_palelwa_boleng("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Thalokontšu_SMS(mong, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!selo_boleng(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "tiragalo_mohlodi") && Thalokontšu_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "taelo_SMS") && Thalokontšu_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "lokela") && Thalokontšu_SMS(서술상수, "()I")) 넣기(1001, 1);
            else go_palelwa_boleng("지원하지 않는 한국어 Mogato 알림 호출"); return;
        }
        if (명령코드 == 183 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>")) {
            int 종류 = 한국어화면종(mong), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Thalokontšu_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (mošomiši.화면너비() - 폭) / 2; 세로 = (mošomiši.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Thalokontšu_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Thalokontšu_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { go_palelwa_boleng("지원하지 않는 한국어 화면 생성자"); return; }
            int Sengwalwa = 빼기(2), elemente_boleng = 빼기(2); if (!화면객체(elemente_boleng)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > mošomiši.화면너비() - 가로 || 높이 > mošomiši.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int lokela = mošomiši.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (lokela < 1 || lokela > 32) { go_palelwa_boleng("화면 elemente_boleng 자리가 가득 찼습니다"); return; }
            힙[elemente_boleng + 2] = lokela; 화면참조[lokela - 1] = elemente_boleng;
            힙[elemente_boleng + 5] = 가로; 힙[elemente_boleng + 6] = 세로; 힙[elemente_boleng + 7] = 폭; 힙[elemente_boleng + 8] = 높이; 힙[elemente_boleng + 10] = 2;
            힙[elemente_boleng + 4] = 받이; 힙참조[elemente_boleng + 4] = 1; 힙[elemente_boleng + 12] = 1;
            mošomiši.화면연결(1, lokela, 가로, 세로, 폭, 높이);
            if (종류 == 24) mošomiši.화면연결(7, lokela, 2, 0, 0, 0);
            화면문자설정(elemente_boleng, Sengwalwa); return;
        }
        if (명령코드 != 182) { go_palelwa_boleng("잘못된 한국어 화면 호출 Taelo"); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "ngwala_SMS") && Thalokontšu_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Sengwalwa = 빼기(2), elemente_boleng = 빼기(2); if (화면객체(elemente_boleng)) 화면문자설정(elemente_boleng, Sengwalwa); return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "글읽기") && Thalokontšu_SMS(서술상수, "()Ljava/lang/String;")) {
            int elemente_boleng = 빼기(2); if (화면객체(elemente_boleng)) 넣기(화면문자읽기(elemente_boleng), 2); return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "동작맡기기") && Thalokontšu_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), elemente_boleng = 빼기(2);
            if (화면객체(elemente_boleng)) { 힙[elemente_boleng + 4] = 받이; 힙참조[elemente_boleng + 4] = 1; 힙[elemente_boleng + 12] = 1; } return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "oketša_elemente") && Thalokontšu_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int ngwana_boleng = 빼기(2), 부모 = 빼기(2); if (!화면객체(ngwana_boleng) || !화면객체(부모)) return;
            if (mošomiši.화면연결(2, 힙[부모 + 2], 힙[ngwana_boleng + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[ngwana_boleng + 11] = 부모; 힙참조[ngwana_boleng + 11] = 1; return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "자리정하기") && Thalokontšu_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), elemente_boleng = 빼기(2); if (!화면객체(elemente_boleng)) return;
            if (mošomiši.화면연결(1, 힙[elemente_boleng + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elemente_boleng + 5] = 가로; 힙[elemente_boleng + 6] = 세로; 힙[elemente_boleng + 7] = 폭; 힙[elemente_boleng + 8] = 높이; return;
        }
        if ((Thalokontšu_SMS(leina_ya_go_se_fetoge, "bontšha_lefastere") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "Tswalela")) && Thalokontšu_SMS(서술상수, "()V")) {
            boolean ponagalo_boleng = Thalokontšu_SMS(leina_ya_go_se_fetoge, "bontšha_lefastere"); int elemente_boleng = 빼기(2); if (!화면객체(elemente_boleng)) return;
            if (mošomiši.화면연결(ponagalo_boleng ? 3 : 4, 힙[elemente_boleng + 2], ponagalo_boleng ? 1 : 0, 0, 0, 0) < 0) { go_palelwa_boleng("화면은 ya_kgokagano 명령에서 실행해야 합니다"); return; }
            힙[elemente_boleng + 9] = ponagalo_boleng ? 1 : 0; return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "보이는가") && Thalokontšu_SMS(서술상수, "()Z")) { int elemente_boleng = 빼기(2); if (화면객체(elemente_boleng)) 넣기(힙[elemente_boleng + 9], 1); return; }
        go_palelwa_boleng("지원하지 않는 한국어 화면 mokgwa_boleng");
    }
    static void 화면호출(int mong, int leina_ya_go_se_fetoge, int 서술상수, int 명령코드) {
        if (Thalokontšu_SMS(mong, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "invokeLater") && Thalokontšu_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int selo_Dipadišo = 빼기(2); if (!객체유효(selo_Dipadišo)) return; if (나중수 == 8) { go_palelwa_boleng("invokeLater queue full"); return; } 나중실행[나중수++] = selo_Dipadišo; return; }
            if (명령코드 == 184 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "isEventDispatchThread") && Thalokontšu_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            go_palelwa_boleng("unsupported SwingUtilities method"); return;
        }
        if (Thalokontšu_SMS(mong, "java/awt/event/ActionEvent")) {
            int selo_Dipadišo = 빼기(2); if (!selo_boleng(selo_Dipadišo, 29)) return;
            if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getSource") && Thalokontšu_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[selo_Dipadišo + 2], 2);
            else if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getActionCommand") && Thalokontšu_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[selo_Dipadišo + 2]), 2);
            else if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getID") && Thalokontšu_SMS(서술상수, "()I")) 넣기(1001, 1);
            else go_palelwa_boleng("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Thalokontšu_SMS(leina_ya_go_se_fetoge, "<init>")) {
            int 열수 = 0, SMS_Dipadišo = 0;
            if (Thalokontšu_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Thalokontšu_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Dipadišo = 빼기(2); }
            else if (Thalokontšu_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Dipadišo = 빼기(2);
            else if (Thalokontšu_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Thalokontšu_SMS(서술상수, "()V")) { go_palelwa_boleng("unsupported Swing constructor"); return; }
            int selo_Dipadišo = 빼기(2); if (!객체유효(selo_Dipadišo)) return;
            if (힙[selo_Dipadišo] == 30) { go_palelwa_boleng("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(selo_Dipadišo) || 열수 < 0) return;
            int akhaonte_boleng = mošomiši.화면연결(0, 힙[selo_Dipadišo] - 23, 0, 0, 0, 0);
            if (akhaonte_boleng < 1 || akhaonte_boleng > 32) { go_palelwa_boleng("GUI widget slots exhausted"); return; }
            힙[selo_Dipadišo + 2] = akhaonte_boleng; 화면참조[akhaonte_boleng - 1] = selo_Dipadišo; 힙[selo_Dipadišo + 5] = 힙[selo_Dipadišo] == 24 ? 130 : 16; 힙[selo_Dipadišo + 6] = 힙[selo_Dipadišo] == 24 ? 110 : 16;
            힙[selo_Dipadišo + 7] = 힙[selo_Dipadišo] == 24 ? 380 : 220; 힙[selo_Dipadišo + 8] = 힙[selo_Dipadišo] == 24 ? 240 : 28; 힙[selo_Dipadišo + 10] = 1;
            화면문자설정(selo_Dipadišo, SMS_Dipadišo); return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "setText") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "setTitle")) { int SMS_Dipadišo = 빼기(2), selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo) && Thalokontšu_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(selo_Dipadišo, SMS_Dipadišo); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getText") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "getTitle")) { int selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo) && Thalokontšu_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(selo_Dipadišo), 2); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "addActionListener") && Thalokontšu_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo)) { 힙[selo_Dipadišo + 4] = 수신참조; 힙참조[selo_Dipadišo + 4] = 1; } return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "getContentPane") && Thalokontšu_SMS(서술상수, "()Ljava/awt/Container;")) { int selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo)) 넣기(selo_Dipadišo, 2); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "setLayout") && Thalokontšu_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Sebopego_Dipadišo = 빼기(2), selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo) && Sebopego_Dipadišo != 0) go_palelwa_boleng("only absolute layout (null) is supported"); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "add") && (Thalokontšu_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Thalokontšu_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Sebopego_seemo = Thalokontšu_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Sebopego_seemo) 빼기(2);
            int ngwana_Dipadišo = 빼기(2), selo_Dipadišo = 빼기(2); if (!화면객체(ngwana_Dipadišo) || !화면객체(selo_Dipadišo)) return;
            if (mošomiši.화면연결(2, 힙[selo_Dipadišo + 2], 힙[ngwana_Dipadišo + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[ngwana_Dipadišo + 11] = selo_Dipadišo; 힙참조[ngwana_Dipadišo + 11] = 1; if (!Sebopego_seemo) 넣기(ngwana_Dipadišo, 2); return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "setBounds") && Thalokontšu_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), kamano_ya_x = 빼기(1), selo_Dipadišo = 빼기(2); if (!화면객체(selo_Dipadišo)) return;
            if (mošomiši.화면연결(1, 힙[selo_Dipadišo + 2], kamano_ya_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[selo_Dipadišo + 5] = kamano_ya_x; 힙[selo_Dipadišo + 6] = 세로좌표; 힙[selo_Dipadišo + 7] = 너비; 힙[selo_Dipadišo + 8] = 높이; return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "setSize") && Thalokontšu_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), selo_Dipadišo = 빼기(2); if (!화면객체(selo_Dipadišo)) return;
            if (mošomiši.화면연결(1, 힙[selo_Dipadišo + 2], 힙[selo_Dipadišo + 5], 힙[selo_Dipadišo + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[selo_Dipadišo + 7] = 너비; 힙[selo_Dipadišo + 8] = 높이; } return;
        }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "setLocationRelativeTo") && Thalokontšu_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), selo_Dipadišo = 빼기(2); if (!화면객체(selo_Dipadišo)) return; if (상대배치 != 0) { go_palelwa_boleng("only screen centering supported"); return; } 힙[selo_Dipadišo + 5] = (mošomiši.화면너비() - 힙[selo_Dipadišo + 7]) / 2; 힙[selo_Dipadišo + 6] = (mošomiši.화면높이() - 힙[selo_Dipadišo + 8]) / 2; mošomiši.화면연결(1, 힙[selo_Dipadišo + 2], 힙[selo_Dipadišo + 5], 힙[selo_Dipadišo + 6], 힙[selo_Dipadišo + 7], 힙[selo_Dipadišo + 8]); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "setDefaultCloseOperation") && Thalokontšu_SMS(서술상수, "(I)V")) { int pholisi = 빼기(1), selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo)) { if (pholisi < 0 || pholisi > 3) 예외던짐(9, "close policy"); else { 힙[selo_Dipadišo + 10] = pholisi; mošomiši.화면연결(7, 힙[selo_Dipadišo + 2], pholisi, 0, 0, 0); } } return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "setVisible") && Thalokontšu_SMS(서술상수, "(Z)V")) { int data_boleng = 빼기(1), selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo)) { int 처리값 = mošomiši.화면연결(3, 힙[selo_Dipadišo + 2], data_boleng, 0, 0, 0); if (처리값 < 0) go_palelwa_boleng("Swing requires a standalone interactive command"); else 힙[selo_Dipadišo + 9] = data_boleng; } return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "dispose") && Thalokontšu_SMS(서술상수, "()V")) { int selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo)) { mošomiši.화면연결(4, 힙[selo_Dipadišo + 2], 0, 0, 0, 0); 힙[selo_Dipadišo + 9] = 0; } return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "repaint") || Thalokontšu_SMS(leina_ya_go_se_fetoge, "validate")) { int selo_Dipadišo = 빼기(2); if (!화면객체(selo_Dipadišo) || !Thalokontšu_SMS(서술상수, "()V")) return; mošomiši.화면연결(1, 힙[selo_Dipadišo + 2], 힙[selo_Dipadišo + 5], 힙[selo_Dipadišo + 6], 힙[selo_Dipadišo + 7], 힙[selo_Dipadišo + 8]); return; }
        if (Thalokontšu_SMS(leina_ya_go_se_fetoge, "isVisible") && Thalokontšu_SMS(서술상수, "()Z")) { int selo_Dipadišo = 빼기(2); if (화면객체(selo_Dipadišo)) 넣기(힙[selo_Dipadišo + 9], 1); return; }
        go_palelwa_boleng("unsupported Swing method (native subset)");
    }
    static void 사건실행(int nepo_atrese, int 사건번호, boolean 한국어) {
        if (nepo_atrese < 1 || 힙[nepo_atrese] < 32) { go_palelwa_boleng("Java event listener required"); return; }
        int faele_lokela = leina_mokgwa(힙[nepo_atrese] - 32, 사건번호 == 0 ? (한국어 ? "phethagatša_mošomo" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (faele_lokela < 0) { go_palelwa_boleng("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; freime_lokela = 0; threte_boemo[0] = 1; freime_kgoboko[0] = 0; 틀잠금[0] = thomiša_freime[0] = 0; 바꿈요청 = false;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 128; ditaelopoeletšwa_lokela++) { kgauswi_boleng[ditaelopoeletšwa_lokela] = kgauswi_thaepa[ditaelopoeletšwa_lokela] = 0; }
        freime_mokgwa[0] = faele_lokela; 틀위치[0] = mokgwa_Thomišo[faele_lokela]; kgauswi_boleng[0] = nepo_atrese; kgauswi_thaepa[0] = 2;
        if (사건번호 != 0) { kgauswi_boleng[1] = 사건번호; kgauswi_thaepa[1] = 2; }
        사건중 = true; phethagatša_taelo(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Phošo) {
            if (나중수 > 0) { int nepo_atrese = 나중실행[0], 한국어 = 나중한국어[0]; for (int ditaelopoeletšwa_lokela = 1; ditaelopoeletšwa_lokela < 나중수; ditaelopoeletšwa_lokela++) { 나중실행[ditaelopoeletšwa_lokela - 1] = 나중실행[ditaelopoeletšwa_lokela]; 나중한국어[ditaelopoeletšwa_lokela - 1] = 나중한국어[ditaelopoeletšwa_lokela]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(nepo_atrese, 0, 한국어 != 0); continue; }
            if (mošomiši.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = mošomiši.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { go_palelwa_boleng("GUI event I/O failed"); return; }
            int akhaonte_boleng = 사건번호 & 65535; if (akhaonte_boleng < 1 || akhaonte_boleng > 32) continue; int selo_Dipadišo = 화면참조[akhaonte_boleng - 1]; if (selo_Dipadišo == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[selo_Dipadišo + 10] != 0) 힙[selo_Dipadišo + 9] = 0;
                if (힙[selo_Dipadišo + 10] == 3) for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 32; ditaelopoeletšwa_lokela++) if (화면참조[ditaelopoeletšwa_lokela] != 0 && 힙[화면참조[ditaelopoeletšwa_lokela]] == 24) mošomiši.화면연결(4, ditaelopoeletšwa_lokela + 1, 0, 0, 0, 0);
            } else if (힙[selo_Dipadišo + 4] != 0) {
                int faele_ya_MPALE_Dipadišo = aba_Bobolokelo(29, 2); if (Phošo) return; 힙[faele_ya_MPALE_Dipadišo + 2] = selo_Dipadišo; 힙[faele_ya_MPALE_Dipadišo + 3] = 힙[selo_Dipadišo + 12]; 힙참조[faele_ya_MPALE_Dipadišo + 2] = 1; 사건실행(힙[selo_Dipadišo + 4], faele_ya_MPALE_Dipadišo, 힙[selo_Dipadišo + 12] != 0);
            }
        }
    }
    public static int Diriša() {
        if (mošomiši.인수개수() == 1 && 자바도구.같음(mošomiši.인수(0), "-version")) {
            mošomiši.Ngwala("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (mošomiši.인수개수() < 1) { mošomiši.Ngwala("Usage: java CLASS [ARGS]\n"); return 2; }
        go_tsenya_tshedimošo_legoro_Tlhaloso = laiša_legoro_Tlhaloso(go_nea_ditirelo_tlhaka(mošomiši.인수(0))); if (Phošo || go_tsenya_tshedimošo_legoro_Tlhaloso < 0) return 1;
        int go_tsenya_tshedimošo_ntlha_boleng = leina_mokgwa(go_tsenya_tshedimošo_legoro_Tlhaloso, "Diriša", "()V");
        boolean 한국어진입 = go_tsenya_tshedimošo_ntlha_boleng >= 0 && (mokgwa_fihlelela[go_tsenya_tshedimošo_ntlha_boleng] & 9) == 9;
        if (!한국어진입) go_tsenya_tshedimošo_ntlha_boleng = leina_mokgwa(go_tsenya_tshedimošo_legoro_Tlhaloso, "main", "([Ljava/lang/String;)V");
        if (go_tsenya_tshedimošo_ntlha_boleng < 0 || (mokgwa_fihlelela[go_tsenya_tshedimošo_ntlha_boleng] & 9) != 9) go_palelwa_boleng("public static void Diriša() or main(String[] args) required");
        if (Phošo) return 1;
        int 인수 = aba_Bobolokelo(3, mošomiši.인수개수() - 1); arei_elemente[인수] = -1;
        for (int 수 = 1; 수 < mošomiši.인수개수() && !Phošo; 수++) 힙[인수 + 1 + 수] = go_nea_ditirelo_tlhaka(mošomiši.인수(수));
        freime_lokela = 0; freime_mokgwa[0] = go_tsenya_tshedimošo_ntlha_boleng; 틀위치[0] = mokgwa_Thomišo[go_tsenya_tshedimošo_ntlha_boleng]; kgauswi_boleng[0] = 한국어진입 ? 0 : 인수; kgauswi_thaepa[0] = 한국어진입 ? 0 : 2;
        threte_boemo[0] = 1; threte_selo[0] = aba_Bobolokelo(13, 2);
        phethagatša_taelo(); if (!Phošo) 화면사건들(); return Phošo ? 1 : 0;
    }
}
