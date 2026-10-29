// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Ihele/스택/Ireferensi/igatsha 경계를 yenza_umyalo 중 검사한다. */
public final class 자바가상기계 {
    static int[] Ihele = new int[16 * 16384], 임시파일 = new int[16384], ifayela_igama_I_SMS = new int[512];
    static int[] okungaguquki_ithegi = new int[8192], 상가 = new int[8192], 상나 = new int[8192], uchunge_Ireferensi = new int[8192];
    static int[] indlela_igama_I_SMS = new int[512], indlela_thayipha = new int[512], indlela_ungeno = new int[512], indlela_umnikazi = new int[512];
    static int[] indlela_qala = new int[512], indlela_yekisa = new int[512], indlela_Isitaki = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], indlela_i_agumenti_thayipha = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] endaweni_inani = new int[16384], endaweni_thayipha = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] uhlaka_indlela = new int[128], 틀위치 = new int[128], uhlaka_Isitaki = new int[128], uhlaka_umyalelo = new int[128], qalisa_uhlaka = new int[128];
    static int[] uhlobo_Incazelo_igama = new int[16], uhlobo_Incazelo_linganisa = new int[16], 종부모 = new int[16], uhlobo_Incazelo_isimo = new int[16], 종칸수 = new int[16], qalisa_uhlobo_Incazelo = new int[16];
    static int[] uhlobo_ukusebenzisana = new int[16 * 16], 종접면수 = new int[16];
    static int[] isikhala_igama = new int[512], isikhala_thayipha = new int[512], isikhala_umnikazi = new int[512], isikhala_izimvume = new int[512], 칸위치 = new int[512], isikhala_imininingwane = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], AMALUNGU_AFANAYO_ilungu = new int[32768], Store_inamba = new int[256];
    static int Ubungako, 읽기위치, 함수수, uhlobo_igama, uhlaka_thola_inkomba = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, okufakwayo_uhlobo_Incazelo;
    static int[] uhlu_lwemilayezo_uhlaka = new int[4], uhlu_lwemilayezo_isimo = new int[4], uhlu_lwemilayezo_into = new int[4], uhlu_lwemilayezo_impokophelo = new int[4], 가닥대기 = new int[4];
    static boolean Iphutha, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], uhlobo_uhlu_lwemilayezo = new int[16];

    static void ukwehluleka_inani(String Amagama_I_SMS) {
        if (Iphutha) return;
        int 분류코드 = 0;
        if (자바도구.같음(Amagama_I_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Amagama_I_SMS, "NullPointerException") || 자바도구.같음(Amagama_I_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Amagama_I_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Amagama_I_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Amagama_I_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Amagama_I_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Amagama_I_SMS, "IOException: stream closed") || 자바도구.같음(Amagama_I_SMS, "IOException: read failed") || 자바도구.같음(Amagama_I_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Amagama_I_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Amagama_I_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && uhlaka_thola_inkomba >= 0) { 예외던짐(분류코드, Amagama_I_SMS); return; }
        umsebenzisi.Bhala("JVM error: "); umsebenzisi.Bhala(Amagama_I_SMS); umsebenzisi.bhala_uhlamvusimo_inani(10); Iphutha = true;
    }
    static boolean isiqeshana(int Sebenzisa, int ubude_inani) {
        if (Sebenzisa < 0 || Sebenzisa >= Ihele.length || ubude_inani < 0) return false;
        int uhlobo_Incazelo = Sebenzisa / 16384;
        return Sebenzisa % 16384 <= uhlobo_Incazelo_linganisa[uhlobo_Incazelo] && ubude_inani <= uhlobo_Incazelo_linganisa[uhlobo_Incazelo] - Sebenzisa % 16384;
    }
    static int ibhayithi_inani() {
        if (!isiqeshana(읽기위치, 1)) { ukwehluleka_inani("truncated class file"); return 0; }
        return Ihele[읽기위치++];
    }
    static int 짧은수() { return ibhayithi_inani() << 8 | ibhayithi_inani(); }
    static int inamba() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int ubude_inani) { if (!isiqeshana(읽기위치, ubude_inani)) ukwehluleka_inani("invalid attribute size"); else 읽기위치 += ubude_inani; }
    static boolean hlola_okungaguquki(int 수, int 종류) {
        if (수 <= 0 || 수 >= okungaguquki_ithegi.length || okungaguquki_ithegi[수] != 종류) { ukwehluleka_inani("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Sebenzisa, int ubude_inani, String Amagama_I_SMS) {
        if (!isiqeshana(Sebenzisa, ubude_inani)) return false;
        int 읽는자리 = Sebenzisa, 끝 = Sebenzisa + ubude_inani;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Amagama_I_SMS.length(); iluphu_thola_inkomba++) {
            int ikhodi_yohlamvu = Amagama_I_SMS.charAt(iluphu_thola_inkomba);
            if (ikhodi_yohlamvu > 0 && ikhodi_yohlamvu < 128) { if (읽는자리 >= 끝 || Ihele[읽는자리++] != ikhodi_yohlamvu) return false; }
            else if (ikhodi_yohlamvu < 2048) {
                if (읽는자리 + 2 > 끝 || Ihele[읽는자리++] != (192 | (ikhodi_yohlamvu >> 6)) || Ihele[읽는자리++] != (128 | (ikhodi_yohlamvu & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Ihele[읽는자리++] != (224 | (ikhodi_yohlamvu >> 12)) || Ihele[읽는자리++] != (128 | ((ikhodi_yohlamvu >> 6) & 63)) || Ihele[읽는자리++] != (128 | (ikhodi_yohlamvu & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Amagama_I_SMS(int okungaguquki_inani, String Amagama_I_SMS) { return hlola_okungaguquki(okungaguquki_inani, 1) && 구간(상가[okungaguquki_inani], 상나[okungaguquki_inani], Amagama_I_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!hlola_okungaguquki(가, 1) || !hlola_okungaguquki(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Ihele[상가[가] + 수] != Ihele[상가[나] + 수]) return false;
        return true;
    }
    static int uhlobo_igama_I_SMS(int 수) { return hlola_okungaguquki(수, 7) && hlola_okungaguquki(상가[수], 1) ? 상가[수] : 0; }
    static int Ireferensi_igama(int 수) { return hlola_okungaguquki(수, 12) && hlola_okungaguquki(상가[수], 1) ? 상가[수] : 0; }
    static int Ireferensi_thayipha(int 수) { return hlola_okungaguquki(수, 12) && hlola_okungaguquki(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean okungasho_lutho_thayipha) {
        if (읽기위치 >= 끝) { ukwehluleka_inani("invalid descriptor"); return 0; }
        int inani = ibhayithi_inani();
        if (inani == 'V' && okungasho_lutho_thayipha) return 0;
        if (inani == 'I' || inani == 'B' || inani == 'C' || inani == 'S' || inani == 'Z') return 1;
        if (inani == '[') { 서술형(끝, false); return 2; }
        if (inani == 'L') {
            int Sebenzisa = 읽기위치;
            while (읽기위치 < 끝 && Ihele[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Sebenzisa) ukwehluleka_inani("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        ukwehluleka_inani("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int umsebenzi_inani) {
        int 이전 = 읽기위치, 수 = indlela_thayipha[umsebenzi_inani];
        if (!hlola_okungaguquki(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (ibhayithi_inani() != '(') ukwehluleka_inani("invalid method descriptor");
        int 개수 = 0;
        while (!Iphutha && 읽기위치 < 끝 && Ihele[읽기위치] != ')') {
            if (개수 == 16) { ukwehluleka_inani("too many method arguments"); break; }
            indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || ibhayithi_inani() != ')') ukwehluleka_inani("invalid method descriptor");
        함수반환[umsebenzi_inani] = 서술형(끝, true); 함수인수수[umsebenzi_inani] = 개수;
        if (읽기위치 != 끝) ukwehluleka_inani("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int inani = 짧은수(); return inani == 0 ? 0 : 현재읽는종 * 512 + inani; }
    static int 명상수() { return indlela_umnikazi[uhlaka_indlela[uhlaka_thola_inkomba]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Iphutha; 수++) { hlola_okungaguquki(상번호(), 1); 건너(inamba()); }
    }
    static int umyalo_ubude(int inani) {
        if (inani == 16 || inani == 18 || inani == 21 || inani == 25 || inani == 54 || inani == 58 || inani == 188) return 2;
        if (inani == 17 || inani == 19 || inani == 132 || inani >= 153 && inani <= 167
            || inani >= 178 && inani <= 184 || inani == 187 || inani == 189 || inani == 192 || inani == 193 || inani == 198 || inani == 199) return 3;
        if (inani == 185 || inani == 200) return 5;
        if (inani >= 0 && inani <= 8 || inani >= 26 && inani <= 29 || inani >= 42 && inani <= 46 || inani >= 50 && inani <= 53
            || inani >= 59 && inani <= 62 || inani >= 75 && inani <= 79 || inani >= 83 && inani <= 95
            || inani == 96 || inani == 100 || inani == 104 || inani == 108 || inani == 112 || inani == 116
            || inani == 120 || inani == 122 || inani == 124 || inani == 126 || inani == 128 || inani == 130
            || inani >= 145 && inani <= 147 || inani == 172 || inani == 176 || inani == 177 || inani == 190 || inani == 191
            || inani == 194 || inani == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!isiqeshana(읽는자리, 4)) { ukwehluleka_inani("truncated bytecode operand"); return 0; }
        return Ihele[읽는자리] << 24 | Ihele[읽는자리 + 1] << 16 | Ihele[읽는자리 + 2] << 8 | Ihele[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Sebenzisa, int 끝) {
        int inani = Ihele[읽는자리], ubude_inani = umyalo_ubude(inani);
        if (inani == 170 || inani == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Sebenzisa) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (inani == 170 ? 12 : 8)) return 0;
            int 항목수 = inani == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            ubude_inani = 기준자리 - 읽는자리 + (inani == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (inani == 196 && 읽는자리 + 1 < 끝) {
            int Amagama_imininingwane = Ihele[읽는자리 + 1]; ubude_inani = Amagama_imininingwane == 132 ? 6 : (Amagama_imininingwane == 21 || Amagama_imininingwane == 25 || Amagama_imininingwane == 54 || Amagama_imininingwane == 58) ? 4 : 0;
        }
        return ubude_inani > 0 && ubude_inani <= 끝 - 읽는자리 ? ubude_inani : 0;
    }
    static void hlola_isikhumulo_inani(int isikhumulo_inani, int umsebenzi_inani) {
        if (isikhumulo_inani < indlela_qala[umsebenzi_inani] || isikhumulo_inani >= indlela_yekisa[umsebenzi_inani] || 경계[isikhumulo_inani] != umsebenzi_inani + 1) ukwehluleka_inani("invalid branch target");
    }
    static void 클래스읽기(int uhlobo_Incazelo) {
        현재읽는종 = uhlobo_Incazelo; 읽기위치 = uhlobo_Incazelo * 16384; Ubungako = 읽기위치 + uhlobo_Incazelo_linganisa[uhlobo_Incazelo];
        if (inamba() != 0xcafebabe) { ukwehluleka_inani("not a class file"); return; }
        int 부판 = 짧은수(), isibuyekezo_inani = 짧은수();
        if (isibuyekezo_inani < 45 || isibuyekezo_inani > 52 || 부판 != 0) { ukwehluleka_inani("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = uhlobo_Incazelo * 512;
        if (상수수 < 1 || 상수수 > 512) { ukwehluleka_inani("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !Iphutha; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = ibhayithi_inani(); okungaguquki_ithegi[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = inamba();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else ukwehluleka_inani("unsupported constant type");
        }
        int imvume_inani = 짧은수();
        if ((imvume_inani & (0x2000 | 0x4000)) != 0) ukwehluleka_inani("annotation/enum class unsupported");
        uhlobo_Incazelo_igama[uhlobo_Incazelo] = uhlobo_igama_I_SMS(상번호());
        종부모[uhlobo_Incazelo] = uhlobo_igama_I_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { ukwehluleka_inani("interface count limit"); return; }
        종접면수[uhlobo_Incazelo] = 접면수;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 접면수; iluphu_thola_inkomba++) uhlobo_ukusebenzisana[uhlobo_Incazelo * 16 + iluphu_thola_inkomba] = uhlobo_igama_I_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { ukwehluleka_inani("field count limit (512)"); return; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 필드수 && !Iphutha; iluphu_thola_inkomba++) {
            int ifayela_thola_inkomba = 칸수++; isikhala_umnikazi[ifayela_thola_inkomba] = uhlobo_Incazelo; isikhala_izimvume[ifayela_thola_inkomba] = 짧은수(); isikhala_igama[ifayela_thola_inkomba] = 상번호(); isikhala_thayipha[ifayela_thola_inkomba] = 상번호();
            hlola_okungaguquki(isikhala_igama[ifayela_thola_inkomba], 1); hlola_okungaguquki(isikhala_thayipha[ifayela_thola_inkomba], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[isikhala_thayipha[ifayela_thola_inkomba]]; int 분류코드 = 서술형(읽기위치 + 상나[isikhala_thayipha[ifayela_thola_inkomba]], false); 읽기위치 = 보존값;
            if ((isikhala_izimvume[ifayela_thola_inkomba] & 8) == 0) 칸위치[ifayela_thola_inkomba] = 종칸수[uhlobo_Incazelo]++;
            int isibaluli_imininingwane = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < isibaluli_imininingwane && !Iphutha; 안쪽자리++) {
                int igama_okungaguquki = 상번호(), 유효길이 = inamba();
                if (Amagama_I_SMS(igama_okungaguquki, "ConstantValue") && 유효길이 == 2) {
                    int imininingwane_inani = 상번호();
                    if (분류코드 == 1 && hlola_okungaguquki(imininingwane_inani, 3)) isikhala_imininingwane[ifayela_thola_inkomba] = 상가[imininingwane_inani];
                    else if (분류코드 == 2 && hlola_okungaguquki(imininingwane_inani, 8)) isikhala_imininingwane[ifayela_thola_inkomba] = okungaguquki_I_SMS(상가[imininingwane_inani]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { ukwehluleka_inani("method count limit (512)"); return; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 개수 && !Iphutha; iluphu_thola_inkomba++) {
            int 수 = 함수수++; indlela_umnikazi[수] = uhlobo_Incazelo;
            indlela_ungeno[수] = 짧은수(); indlela_igama_I_SMS[수] = 상번호(); indlela_thayipha[수] = 상번호();
            hlola_okungaguquki(indlela_igama_I_SMS[수], 1); 서술읽기(수);
            if ((indlela_ungeno[수] & 8) == 0) {
                if (함수인수수[수] == 16) { ukwehluleka_inani("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) indlela_i_agumenti_thayipha[수 * 16 + 비교자리] = indlela_i_agumenti_thayipha[수 * 16 + 비교자리 - 1];
                indlela_i_agumenti_thayipha[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((indlela_ungeno[수] & 0x100) != 0) ukwehluleka_inani("user native method unsupported");
            if (Amagama_I_SMS(indlela_igama_I_SMS[수], "<clinit>")) qalisa_uhlobo_Incazelo[uhlobo_Incazelo] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (indlela_umnikazi[앞] == uhlobo_Incazelo && 같은말(indlela_igama_I_SMS[앞], indlela_igama_I_SMS[수]) && 같은말(indlela_thayipha[앞], indlela_thayipha[수])) ukwehluleka_inani("duplicate method");
            int 속성수 = 짧은수();
            for (int isibaluli_inani = 0; isibaluli_inani < 속성수 && !Iphutha; isibaluli_inani++) {
                int Igama = 상번호(), ubude_inani = inamba(), Sebenzisa = 읽기위치;
                if (!isiqeshana(Sebenzisa, ubude_inani)) { ukwehluleka_inani("truncated method attribute"); break; }
                if (Amagama_I_SMS(Igama, "Code")) {
                    if (indlela_qala[수] != 0) ukwehluleka_inani("duplicate Code attribute");
                    indlela_Isitaki[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = inamba();
                    if (indlela_Isitaki[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ukwehluleka_inani("method memory limits exceeded");
                    indlela_qala[수] = 읽기위치; 건너(코드길이); indlela_yekisa[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { ukwehluleka_inani("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int iphutha_Ireferensi = 잡기수++; 잡기함수[iphutha_Ireferensi] = 수;
                        잡기시작[iphutha_Ireferensi] = indlela_qala[수] + 짧은수(); 잡기끝[iphutha_Ireferensi] = indlela_qala[수] + 짧은수();
                        잡기위치[iphutha_Ireferensi] = indlela_qala[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[iphutha_Ireferensi] = 부호값 == 0 ? 0 : uhlobo_igama_I_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Sebenzisa + ubude_inani) ukwehluleka_inani("Code attribute size mismatch");
                } else 건너(ubude_inani);
            }
            if ((indlela_ungeno[수] & 0x400) != 0) continue;
            if (indlela_qala[수] == 0) ukwehluleka_inani("missing Code attribute");
            int isikhala_okufakwayo = indlela_qala[수];
            while (isikhala_okufakwayo < indlela_yekisa[수] && !Iphutha) {
                int ubude_inani = 길이읽기(isikhala_okufakwayo, indlela_qala[수], indlela_yekisa[수]);
                if (ubude_inani == 0) { ukwehluleka_inani("unsupported or truncated bytecode"); break; }
                경계[isikhala_okufakwayo] = 수 + 1; isikhala_okufakwayo += ubude_inani;
            }
            isikhala_okufakwayo = indlela_qala[수];
            while (isikhala_okufakwayo < indlela_yekisa[수] && !Iphutha) {
                int inani = Ihele[isikhala_okufakwayo];
                if (inani >= 153 && inani <= 167 || inani == 198 || inani == 199) hlola_isikhumulo_inani(isikhala_okufakwayo + (short)(Ihele[isikhala_okufakwayo + 1] << 8 | Ihele[isikhala_okufakwayo + 2]), 수);
                if (inani == 200) hlola_isikhumulo_inani(isikhala_okufakwayo + 위치정수(isikhala_okufakwayo + 1), 수);
                if (inani == 170 || inani == 171) {
                    int 읽는자리 = isikhala_okufakwayo + 1; while ((읽는자리 - indlela_qala[수]) % 4 != 0) 읽는자리++;
                    hlola_isikhumulo_inani(isikhala_okufakwayo + 위치정수(읽는자리), 수);
                    int 항목수 = inani == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += inani == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) hlola_isikhumulo_inani(isikhala_okufakwayo + 위치정수(읽는자리 + 안쪽자리 * (inani == 170 ? 4 : 8) + (inani == 170 ? 0 : 4)), 수);
                }
                isikhala_okufakwayo += 길이읽기(isikhala_okufakwayo, indlela_qala[수], indlela_yekisa[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                hlola_isikhumulo_inani(잡기시작[안쪽자리], 수); hlola_isikhumulo_inani(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != indlela_yekisa[수]) hlola_isikhumulo_inani(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) ukwehluleka_inani("invalid exception range");
            }
        }
        if (!Iphutha) 속성건너();
        if (읽기위치 != Ubungako) ukwehluleka_inani("extra class file data");
    }
    static int abela_Indawo_yokugcina(int 종류, int ubude_inani) { return 새기억(종류, ubude_inani); }
    static boolean into_inani(int Ireferensi, int 종류) {
        if (!객체유효(Ireferensi)) return false;
        if (힙[Ireferensi] != 종류) { ukwehluleka_inani("object type mismatch"); return false; }
        return true;
    }
    static int okungaguquki_I_SMS(int thola_inkomba) {
        if (!hlola_okungaguquki(thola_inkomba, 1)) return 0;
        if (uchunge_Ireferensi[thola_inkomba] != 0) return uchunge_Ireferensi[thola_inkomba];
        int Ireferensi = abela_Indawo_yokugcina(1, 상나[thola_inkomba]); if (Iphutha) return 0;
        int 끝 = 상가[thola_inkomba] + 상나[thola_inkomba], 수 = 상가[thola_inkomba], ubude_inani = 0;
        while (수 < 끝 && !Iphutha) {
            int inani = Ihele[수++];
            if (inani == 0) ukwehluleka_inani("invalid modified UTF-8");
            else if (inani >= 192 && inani <= 223 && 수 < 끝) {
                int 다음 = Ihele[수++];
                if ((다음 & 192) != 128) ukwehluleka_inani("invalid modified UTF-8");
                inani = (inani & 31) << 6 | 다음 & 63;
                if (inani != 0 && inani < 128) ukwehluleka_inani("overlong modified UTF-8");
            } else if (inani >= 224 && inani <= 239 && 수 + 1 < 끝) {
                int 가 = Ihele[수++], 나 = Ihele[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) ukwehluleka_inani("invalid modified UTF-8");
                inani = (inani & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (inani < 2048) ukwehluleka_inani("overlong modified UTF-8");
            } else if (inani >= 128) ukwehluleka_inani("invalid modified UTF-8");
            힙[Ireferensi + 2 + ubude_inani++] = inani;
        }
        힙[Ireferensi + 1] = ubude_inani; uchunge_Ireferensi[thola_inkomba] = Ireferensi; return Ireferensi;
    }
    static int singatha_uhlamvusimo(String inani) {
        int Ireferensi = abela_Indawo_yokugcina(1, inani.length()); if (Iphutha) return 0;
        for (int 수 = 0; 수 < inani.length(); 수++) 힙[Ireferensi + 2 + 수] = inani.charAt(수);
        return Ireferensi;
    }
    static void bhala_I_SMS(int Ireferensi) {
        if (Ireferensi == 0) { umsebenzisi.Bhala("null"); return; }
        if (!into_inani(Ireferensi, 1)) return;
        for (int 수 = 0; 수 < 힙[Ireferensi + 1]; 수++) umsebenzisi.bhala_uhlamvusimo_inani(힙[Ireferensi + 2 + 수]);
    }
    static int idijithi_uhlamvusimo(int inani) {
        int Ireferensi = abela_Indawo_yokugcina(1, 11); if (Iphutha) return 0;
        int ubude_inani = 0;
        if (inani < 0) 힙[Ireferensi + 2 + ubude_inani++] = '-'; else inani = -inani;
        int 자리 = 1000000000; boolean Sebenzisa = false;
        while (자리 != 0) {
            int 수 = -(inani / 자리);
            if (수 != 0 || Sebenzisa || 자리 == 1) { 힙[Ireferensi + 2 + ubude_inani++] = '0' + 수; Sebenzisa = true; }
            inani %= 자리; 자리 /= 10;
        }
        힙[Ireferensi + 1] = ubude_inani; return Ireferensi;
    }
    static int 정수해독(int Ireferensi) {
        if (!into_inani(Ireferensi, 1)) return 0;
        int ubude_inani = 힙[Ireferensi + 1], 수 = 0, inani = 0; boolean 음수 = false;
        if (ubude_inani > 0 && (힙[Ireferensi + 2] == '-' || 힙[Ireferensi + 2] == '+')) { 음수 = 힙[Ireferensi + 2] == '-'; 수++; }
        if (수 == ubude_inani) ukwehluleka_inani("NumberFormatException");
        for (; 수 < ubude_inani && !Iphutha; 수++) {
            int idijithi_inani = 힙[Ireferensi + 2 + 수] - '0';
            if (idijithi_inani < 0 || idijithi_inani > 9 || inani < -214748364 || inani == -214748364 && idijithi_inani > (음수 ? 8 : 7)) ukwehluleka_inani("NumberFormatException");
            inani = inani * 10 - idijithi_inani;
        }
        return 음수 ? inani : -inani;
    }
    static void 넣기(int inani, int thayipha_inani) {
        if (Iphutha) return;
        if (uhlaka_thola_inkomba < 0 || uhlaka_Isitaki[uhlaka_thola_inkomba] >= indlela_Isitaki[uhlaka_indlela[uhlaka_thola_inkomba]]) { ukwehluleka_inani("operand stack overflow"); return; }
        int isikhala_okufakwayo = uhlaka_thola_inkomba * 128 + uhlaka_Isitaki[uhlaka_thola_inkomba]++; 스택값[isikhala_okufakwayo] = inani; 스택형[isikhala_okufakwayo] = thayipha_inani;
    }
    static int 빼기(int thayipha_inani) {
        if (Iphutha) return 0;
        if (uhlaka_thola_inkomba < 0 || uhlaka_Isitaki[uhlaka_thola_inkomba] < 1) { ukwehluleka_inani("operand stack underflow"); return 0; }
        int isikhala_okufakwayo = uhlaka_thola_inkomba * 128 + --uhlaka_Isitaki[uhlaka_thola_inkomba]; 반환형 = 스택형[isikhala_okufakwayo];
        if (thayipha_inani != 0 && 반환형 != thayipha_inani) ukwehluleka_inani("operand type mismatch");
        if (반환형 == 2) vikela_inani(스택값[isikhala_okufakwayo]);
        return 스택값[isikhala_okufakwayo];
    }
    static void 지역읽기(int thola_inkomba, int thayipha_inani) {
        if (thola_inkomba >= 함수지역[uhlaka_indlela[uhlaka_thola_inkomba]] || thola_inkomba < 0 || endaweni_thayipha[uhlaka_thola_inkomba * 128 + thola_inkomba] != thayipha_inani) { ukwehluleka_inani("invalid or uninitialized local"); return; }
        넣기(endaweni_inani[uhlaka_thola_inkomba * 128 + thola_inkomba], thayipha_inani);
    }
    static void bhala_endaweni(int thola_inkomba, int thayipha_inani) {
        if (thola_inkomba >= 함수지역[uhlaka_indlela[uhlaka_thola_inkomba]] || thola_inkomba < 0) { ukwehluleka_inani("local index out of range"); return; }
        int inani = 빼기(thayipha_inani); endaweni_inani[uhlaka_thola_inkomba * 128 + thola_inkomba] = inani; endaweni_thayipha[uhlaka_thola_inkomba * 128 + thola_inkomba] = thayipha_inani;
    }
    static int 명바() {
        int 위치 = 틀위치[uhlaka_thola_inkomba];
        if (위치 < indlela_qala[uhlaka_indlela[uhlaka_thola_inkomba]] || 위치 >= indlela_yekisa[uhlaka_indlela[uhlaka_thola_inkomba]]) { ukwehluleka_inani("instruction pointer out of range"); return 0; }
        틀위치[uhlaka_thola_inkomba]++; return Ihele[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void susa_inani(int 위치) {
        int umsebenzi_inani = uhlaka_indlela[uhlaka_thola_inkomba];
        if (위치 < indlela_qala[umsebenzi_inani] || 위치 >= indlela_yekisa[umsebenzi_inani] || 경계[위치] != umsebenzi_inani + 1) ukwehluleka_inani("invalid branch target");
        else 틀위치[uhlaka_thola_inkomba] = 위치;
    }
    static void 호출(int umsebenzi_inani) {
        if (uhlaka_thola_inkomba % 32 == 31) { ukwehluleka_inani("call stack limit (32)"); return; }
        int 다음 = uhlaka_thola_inkomba + 1;
        for (int 수 = 0; 수 < 128; 수++) endaweni_thayipha[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[umsebenzi_inani] - 1; 수 >= 0; 수--) {
            endaweni_inani[다음 * 128 + 수] = 빼기(indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 수]); endaweni_thayipha[다음 * 128 + 수] = indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 수];
        }
        if (Iphutha) return;
        uhlaka_thola_inkomba = 다음; qalisa_uhlaka[uhlaka_thola_inkomba] = 0; uhlaka_indlela[uhlaka_thola_inkomba] = umsebenzi_inani; 틀위치[uhlaka_thola_inkomba] = indlela_qala[umsebenzi_inani]; uhlaka_Isitaki[uhlaka_thola_inkomba] = 0;
    }
    static void 반환(int thayipha_inani) {
        if (thayipha_inani != 함수반환[uhlaka_indlela[uhlaka_thola_inkomba]]) { ukwehluleka_inani("return type mismatch"); return; }
        int inani = thayipha_inani == 0 ? 0 : 빼기(thayipha_inani);
        if (qalisa_uhlaka[uhlaka_thola_inkomba] != 0) uhlobo_Incazelo_isimo[qalisa_uhlaka[uhlaka_thola_inkomba] - 1] = 2;
        if (틀잠금[uhlaka_thola_inkomba] != 0) { 잠금풀기(틀잠금[uhlaka_thola_inkomba]); 틀잠금[uhlaka_thola_inkomba] = 0; }
        uhlaka_thola_inkomba--; if (uhlaka_thola_inkomba >= 현재가닥 * 32 && thayipha_inani != 0) 넣기(inani, thayipha_inani);
    }
    static int[] Stream_ifayela_igama = new int[64];
    static void ifayela_Stream_fonela(int umnikazi_inani, int Igama, int misa_inani, int Umlayelo) {
        boolean 출력 = Amagama_I_SMS(umnikazi_inani, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Umlayelo == 183 && Amagama_I_SMS(Igama, "<init>")) {
            boolean 이어 = false;
            if (출력 && Amagama_I_SMS(misa_inani, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Amagama_I_SMS(misa_inani, "(Ljava/lang/String;)V")) { ukwehluleka_inani("unsupported file stream constructor"); return; }
            int ifayela_okufakwayo_igama = 빼기(2), Stream_inani = 빼기(2);
            if (!into_inani(ifayela_okufakwayo_igama, 1) || !into_inani(Stream_inani, 종류) || Iphutha) return;
            if (힙[Stream_inani + 3] != 0) { ukwehluleka_inani("file stream already initialized"); return; }
            int ubude_inani = 힙[ifayela_okufakwayo_igama + 1];
            if (ubude_inani < 1 || ubude_inani > 63) { ukwehluleka_inani("invalid file name length"); return; }
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < ubude_inani; isikhala_okufakwayo++) {
                int inani = 힙[ifayela_okufakwayo_igama + 2 + isikhala_okufakwayo];
                if (inani < 1) { ukwehluleka_inani("invalid file stream path"); return; }
                Stream_ifayela_igama[isikhala_okufakwayo] = inani;
            }
            Stream_ifayela_igama[ubude_inani] = 0;
            int 서술자 = umsebenzisi.파일서술자열기(Stream_ifayela_igama, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ukwehluleka_inani("FileNotFoundException: file open failed"); return; }
            힙[Stream_inani + 2] = 서술자; 힙[Stream_inani + 3] = 1;
            return;
        }
        if (Umlayelo != 182) { ukwehluleka_inani("invalid file stream invocation"); return; }
        if ((출력 && Amagama_I_SMS(Igama, "write") || !출력 && Amagama_I_SMS(Igama, "read"))
            && (Amagama_I_SMS(misa_inani, 출력 ? "([B)V" : "([B)I") || Amagama_I_SMS(misa_inani, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean isiqeshana_inani = Amagama_I_SMS(misa_inani, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = isiqeshana_inani ? 빼기(1) : 0, 시작점 = isiqeshana_inani ? 빼기(1) : 0, imininingwane_AMALUNGU_AFANAYO = 빼기(2), into_Ireferensi = 빼기(2);
            if (!into_inani(imininingwane_AMALUNGU_AFANAYO, 20) || !into_inani(into_Ireferensi, 종류)) return;
            if (!isiqeshana_inani) 항목수 = 힙[imininingwane_AMALUNGU_AFANAYO + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[imininingwane_AMALUNGU_AFANAYO + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[into_Ireferensi + 3] == 0 || 힙[into_Ireferensi + 2] < 0) { ukwehluleka_inani("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !Iphutha) {
                int 반환값 = 출력 ? umsebenzisi.파일한바이트쓰기(힙[into_Ireferensi + 2], 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 시작점 + 완료수]) : umsebenzisi.파일한바이트읽기(힙[into_Ireferensi + 2]);
                if (반환값 < 0) { ukwehluleka_inani(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Amagama_I_SMS(Igama, "flush") && Amagama_I_SMS(misa_inani, "()V")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 종류) && 힙[into_Ireferensi + 2] < 0) ukwehluleka_inani("IOException: stream closed"); return; }
        int Isenzo = -1, inani = 0;
        if (Amagama_I_SMS(Igama, "close") && Amagama_I_SMS(misa_inani, "()V")) Isenzo = 0;
        if (!출력 && Amagama_I_SMS(Igama, "read") && Amagama_I_SMS(misa_inani, "()I")) Isenzo = 1;
        if (출력 && Amagama_I_SMS(Igama, "write") && Amagama_I_SMS(misa_inani, "(I)V")) { Isenzo = 2; inani = 빼기(1); }
        if (Isenzo < 0) { ukwehluleka_inani("unsupported file stream method"); return; }
        int Stream_inani = 빼기(2);
        if (!into_inani(Stream_inani, 종류) || Iphutha) return;
        if (힙[Stream_inani + 3] == 0) { ukwehluleka_inani("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_inani + 2];
        if (Isenzo == 0) {
            if (서술자 >= 0 && umsebenzisi.파일서술자닫기(서술자) < 0) ukwehluleka_inani("IOException: close failed");
            힙[Stream_inani + 2] = -1; return;
        }
        if (서술자 < 0) { ukwehluleka_inani("IOException: stream closed"); return; }
        if (Isenzo == 1) {
            int 결과 = umsebenzisi.파일한바이트읽기(서술자);
            if (결과 < -1) ukwehluleka_inani("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (umsebenzisi.파일한바이트쓰기(서술자, inani) != 1) ukwehluleka_inani("IOException: write failed");
    }
    static void fonela_indlela(int thola_inkomba, int Umlayelo) {
        if (thola_inkomba <= 0 || thola_inkomba >= okungaguquki_ithegi.length || (okungaguquki_ithegi[thola_inkomba] != 10 && okungaguquki_ithegi[thola_inkomba] != 11)) { ukwehluleka_inani("invalid method reference"); return; }
        int umnikazi_inani = uhlobo_igama_I_SMS(상가[thola_inkomba]), Igama = Ireferensi_igama(상나[thola_inkomba]), misa_inani = Ireferensi_thayipha(상나[thola_inkomba]);
        if (Iphutha) return;
        if (기본호출(umnikazi_inani, Igama, misa_inani, Umlayelo)) return;
        if (Amagama_I_SMS(umnikazi_inani, "java/io/FileInputStream") || Amagama_I_SMS(umnikazi_inani, "java/io/FileOutputStream")) {
            ifayela_Stream_fonela(umnikazi_inani, Igama, misa_inani, Umlayelo); return;
        }
        if (Umlayelo == 184 && Amagama_I_SMS(umnikazi_inani, "java/lang/Integer") && Amagama_I_SMS(Igama, "parseInt") && Amagama_I_SMS(misa_inani, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Umlayelo == 182 && Amagama_I_SMS(umnikazi_inani, "java/io/PrintStream") && (Amagama_I_SMS(Igama, "println") || Amagama_I_SMS(Igama, "print"))) {
            int thayipha_inani = 0, inani = 0;
            if (Amagama_I_SMS(misa_inani, "(I)V")) { thayipha_inani = 1; inani = 빼기(1); }
            else if (Amagama_I_SMS(misa_inani, "(Z)V")) { thayipha_inani = 2; inani = 빼기(1); }
            else if (Amagama_I_SMS(misa_inani, "(C)V")) { thayipha_inani = 3; inani = 빼기(1); }
            else if (Amagama_I_SMS(misa_inani, "(Ljava/lang/String;)V")) { thayipha_inani = 4; inani = 빼기(2); }
            else if (!Amagama_I_SMS(misa_inani, "()V") || !Amagama_I_SMS(Igama, "println")) ukwehluleka_inani("unsupported print descriptor");
            if (빼기(2) != -1) ukwehluleka_inani("invalid PrintStream receiver");
            if (Iphutha) return;
            if (thayipha_inani == 1) 자바도구.수쓰기(inani);
            if (thayipha_inani == 2) umsebenzisi.Bhala(inani == 0 ? "false" : "true");
            if (thayipha_inani == 3) umsebenzisi.bhala_uhlamvusimo_inani(inani & 65535);
            if (thayipha_inani == 4) bhala_I_SMS(inani);
            if (Amagama_I_SMS(Igama, "println")) umsebenzisi.bhala_uhlamvusimo_inani(10);
            return;
        }
        if (Umlayelo == 182 && Amagama_I_SMS(umnikazi_inani, "java/lang/String")) {
            if (Amagama_I_SMS(Igama, "length") && Amagama_I_SMS(misa_inani, "()I")) {
                int Ireferensi = 빼기(2); if (into_inani(Ireferensi, 1)) 넣기(힙[Ireferensi + 1], 1); return;
            }
            if (Amagama_I_SMS(Igama, "charAt") && Amagama_I_SMS(misa_inani, "(I)C")) {
                int umbhalo_ongezansi_inani = 빼기(1), Ireferensi = 빼기(2);
                if (into_inani(Ireferensi, 1)) {
                    if (umbhalo_ongezansi_inani < 0 || umbhalo_ongezansi_inani >= 힙[Ireferensi + 1]) ukwehluleka_inani("StringIndexOutOfBoundsException"); else 넣기(힙[Ireferensi + 2 + umbhalo_ongezansi_inani], 1);
                }
                return;
            }
        }
        if (Amagama_I_SMS(umnikazi_inani, "java/lang/StringBuilder")) {
            if (Umlayelo == 183 && Amagama_I_SMS(Igama, "<init>") && Amagama_I_SMS(misa_inani, "()V")) { into_inani(빼기(2), 4); return; }
            if (Umlayelo == 182 && Amagama_I_SMS(Igama, "toString") && Amagama_I_SMS(misa_inani, "()Ljava/lang/String;")) {
                int Ireferensi = 빼기(2); if (into_inani(Ireferensi, 4)) 넣기(힙[Ireferensi + 2] == 0 ? singatha_uhlamvusimo("") : 힙[Ireferensi + 2], 2); return;
            }
            if (Umlayelo == 182 && Amagama_I_SMS(Igama, "append")) {
                int Itekisi = 0;
                if (Amagama_I_SMS(misa_inani, "(I)Ljava/lang/StringBuilder;")) Itekisi = idijithi_uhlamvusimo(빼기(1));
                else if (Amagama_I_SMS(misa_inani, "(Z)Ljava/lang/StringBuilder;")) Itekisi = singatha_uhlamvusimo(빼기(1) == 0 ? "false" : "true");
                else if (Amagama_I_SMS(misa_inani, "(C)Ljava/lang/StringBuilder;")) {
                    int inani = 빼기(1); Itekisi = abela_Indawo_yokugcina(1, 1); if (!Iphutha) 힙[Itekisi + 2] = inani & 65535;
                }
                else if (Amagama_I_SMS(misa_inani, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Itekisi = 빼기(2); if (Itekisi == 0) Itekisi = singatha_uhlamvusimo("null"); }
                else { ukwehluleka_inani("unsupported StringBuilder append"); return; }
                int Ireferensi = 빼기(2); if (!into_inani(Ireferensi, 4) || !into_inani(Itekisi, 1)) return;
                int 앞 = 힙[Ireferensi + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Impindamuva_inani_ubude = 힙[Itekisi + 1];
                int 새글 = abela_Indawo_yokugcina(1, 앞길이 + Impindamuva_inani_ubude); if (Iphutha) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Impindamuva_inani_ubude; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Itekisi + 2 + 수];
                힙[Ireferensi + 2] = 새글; 넣기(Ireferensi, 2); return;
            }
        }
        int uhlobo_Incazelo = thola_uhlobo_Incazelo(umnikazi_inani); if (uhlobo_Incazelo < 0 || Iphutha) return;
        int ifayela_thola_inkomba = thola_indlela(uhlobo_Incazelo, Igama, misa_inani);
        if (ifayela_thola_inkomba < 0) {
            for (int ikhodi_yohlamvu = uhlobo_Incazelo, 항목수 = 0; ikhodi_yohlamvu >= 0 && 항목수 < 16; 항목수++, ikhodi_yohlamvu = 부모종(ikhodi_yohlamvu))
                if (Amagama_I_SMS(종부모[ikhodi_yohlamvu], "java/lang/Thread")) { 가닥호출(Igama, misa_inani, Umlayelo); return; }
            ukwehluleka_inani("NoSuchMethodError"); return;
        }
        if (((indlela_ungeno[ifayela_thola_inkomba] & 8) != 0) != (Umlayelo == 184)) { ukwehluleka_inani("method static/instance mismatch"); return; }
        if (Umlayelo == 184) { if (!qalisa(indlela_umnikazi[ifayela_thola_inkomba], uhlaka_umyalelo[uhlaka_thola_inkomba])) return; }
        else {
            int 읽는자리 = uhlaka_Isitaki[uhlaka_thola_inkomba] - 함수인수수[ifayela_thola_inkomba];
            if (읽는자리 < 0 || 스택형[uhlaka_thola_inkomba * 128 + 읽는자리] != 2) { ukwehluleka_inani("invalid method receiver"); return; }
            int into_Ireferensi = 스택값[uhlaka_thola_inkomba * 128 + 읽는자리];
            if (!객체유효(into_Ireferensi)) return;
            if (힙[into_Ireferensi] < 32 || !종포함(힙[into_Ireferensi] - 32, umnikazi_inani)) { ukwehluleka_inani("method receiver type mismatch"); return; }
            if (Umlayelo != 183) ifayela_thola_inkomba = thola_indlela(힙[into_Ireferensi] - 32, Igama, misa_inani);
        }
        if (ifayela_thola_inkomba < 0 || (indlela_ungeno[ifayela_thola_inkomba] & 0x400) != 0) { ukwehluleka_inani("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((indlela_ungeno[ifayela_thola_inkomba] & 32) != 0) {
            if (Umlayelo == 184) { int ikhodi_yohlamvu = indlela_umnikazi[ifayela_thola_inkomba]; if (종잠금[ikhodi_yohlamvu] == 0) 종잠금[ikhodi_yohlamvu] = abela_Indawo_yokugcina(8, 0); 잠금참조 = 종잠금[ikhodi_yohlamvu]; }
            else 잠금참조 = 스택값[uhlaka_thola_inkomba * 128 + uhlaka_Isitaki[uhlaka_thola_inkomba] - 함수인수수[ifayela_thola_inkomba]];
            if (!잠금얻기(잠금참조)) { if (!Iphutha) 틀위치[uhlaka_thola_inkomba] = uhlaka_umyalelo[uhlaka_thola_inkomba]; return; }
        }
        호출(ifayela_thola_inkomba); if (!Iphutha) 틀잠금[uhlaka_thola_inkomba] = 잠금참조;
    }
    static boolean 배열저장가능(int AMALUNGU_AFANAYO_Ireferensi, int imininingwane_inani) {
        if (imininingwane_inani == 0 || AMALUNGU_AFANAYO_ilungu[AMALUNGU_AFANAYO_Ireferensi] == 0) return true;
        boolean 성공여부 = AMALUNGU_AFANAYO_ilungu[AMALUNGU_AFANAYO_Ireferensi] == -1 ? (imininingwane_inani > 0 && imininingwane_inani < 힙끝 && 힙[imininingwane_inani] == 1) : 맞는객체(imininingwane_inani, AMALUNGU_AFANAYO_ilungu[AMALUNGU_AFANAYO_Ireferensi]);
        if (!성공여부 && !Iphutha) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int AMALUNGU_AFANAYO_isikhala(int Ireferensi, int umbhalo_ongezansi_inani, int thayipha_inani) {
        if (!into_inani(Ireferensi, thayipha_inani)) return 0;
        if (umbhalo_ongezansi_inani < 0 || umbhalo_ongezansi_inani >= 힙[Ireferensi + 1]) { ukwehluleka_inani("ArrayIndexOutOfBoundsException"); return 0; }
        return Ireferensi + 2 + umbhalo_ongezansi_inani;
    }
    static void yenza_umyalo() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Iphutha) { if (던진객체 != 0) 예외처리(); if (Iphutha || uhlaka_thola_inkomba < 현재가닥 * 32) break; }
            if (uhlaka_thola_inkomba < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!guqulela_kokunye_uhlu_lwemilayezo()) break; 조각 = 100; }
            if (uhlaka_thola_inkomba == 0 && uhlobo_Incazelo_isimo[okufakwayo_uhlobo_Incazelo] != 2 && !qalisa(okufakwayo_uhlobo_Incazelo, 틀위치[uhlaka_thola_inkomba])) continue;
            if (uhlaka_thola_inkomba == 현재가닥 * 32 && 현재가닥 != 0 && (indlela_ungeno[uhlaka_indlela[uhlaka_thola_inkomba]] & 32) != 0 && 틀잠금[uhlaka_thola_inkomba] == 0) {
                int into_Ireferensi = uhlu_lwemilayezo_impokophelo[현재가닥]; if (!잠금얻기(into_Ireferensi)) { if (Iphutha) break; continue; } 틀잠금[uhlaka_thola_inkomba] = into_Ireferensi;
            }
            잠시수 = 0;
            if (--남음 == 0) { ukwehluleka_inani("instruction limit (500000)"); break; }
            int Sebenzisa = 틀위치[uhlaka_thola_inkomba]; uhlaka_umyalelo[uhlaka_thola_inkomba] = Sebenzisa; int inani = 명바();
            if (Iphutha) break;
            if (inani == 0) continue;
            if (inani == 1) { 넣기(0, 2); continue; }
            if (inani >= 2 && inani <= 8) { 넣기(inani - 3, 1); continue; }
            if (inani == 16) { 넣기((byte)명바(), 1); continue; }
            if (inani == 17) { 넣기((short)명짧(), 1); continue; }
            if (inani == 18 || inani == 19) {
                int 수 = indlela_umnikazi[uhlaka_indlela[uhlaka_thola_inkomba]] * 512 + (inani == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= okungaguquki_ithegi.length) ukwehluleka_inani("invalid ldc constant");
                else if (okungaguquki_ithegi[수] == 3) 넣기(상가[수], 1);
                else if (okungaguquki_ithegi[수] == 8) 넣기(okungaguquki_I_SMS(상가[수]), 2);
                else ukwehluleka_inani("unsupported ldc constant");
                continue;
            }
            if (inani == 21 || inani == 25) { 지역읽기(명바(), inani == 21 ? 1 : 2); continue; }
            if (inani >= 26 && inani <= 29) { 지역읽기(inani - 26, 1); continue; }
            if (inani >= 42 && inani <= 45) { 지역읽기(inani - 42, 2); continue; }
            if (inani == 54 || inani == 58) { bhala_endaweni(명바(), inani == 54 ? 1 : 2); continue; }
            if (inani >= 59 && inani <= 62) { bhala_endaweni(inani - 59, 1); continue; }
            if (inani >= 75 && inani <= 78) { bhala_endaweni(inani - 75, 2); continue; }
            if (inani == 46 || inani >= 50 && inani <= 53) {
                int 항목자리 = 빼기(1), into_Ireferensi = 빼기(2), 분류코드 = inani == 46 ? 2 : inani == 50 ? 3 : inani == 51 ? 20 : inani == 52 ? 22 : 23;
                if (inani == 51 && into_Ireferensi > 0 && into_Ireferensi < 힙끝 && 힙[into_Ireferensi] == 21) 분류코드 = 21;
                int 읽는자리 = AMALUNGU_AFANAYO_isikhala(into_Ireferensi, 항목자리, 분류코드); if (!Iphutha) 넣기(힙[읽는자리], inani == 50 ? 2 : 1); continue;
            }
            if (inani == 79 || inani >= 83 && inani <= 86) {
                int okufakwayo_Ireferensi = 빼기(inani == 83 ? 2 : 1), 항목자리 = 빼기(1), into_Ireferensi = 빼기(2), 분류코드 = inani == 79 ? 2 : inani == 83 ? 3 : inani == 84 ? 20 : inani == 85 ? 22 : 23;
                if (inani == 84 && into_Ireferensi > 0 && into_Ireferensi < 힙끝 && 힙[into_Ireferensi] == 21) 분류코드 = 21;
                int 읽는자리 = AMALUNGU_AFANAYO_isikhala(into_Ireferensi, 항목자리, 분류코드);
                if (!Iphutha && 분류코드 == 3 && !배열저장가능(into_Ireferensi, okufakwayo_Ireferensi)) continue;
                if (!Iphutha) 힙[읽는자리] = 분류코드 == 20 ? (byte)okufakwayo_Ireferensi : 분류코드 == 21 ? okufakwayo_Ireferensi & 1 : 분류코드 == 22 ? (char)okufakwayo_Ireferensi : 분류코드 == 23 ? (short)okufakwayo_Ireferensi : okufakwayo_Ireferensi;
                continue;
            }
            if (inani >= 87 && inani <= 95) { Isitaki_umyalelo(inani); continue; }
            if (inani == 96 || inani == 100 || inani == 104 || inani == 108 || inani == 112 || inani == 120
                || inani == 122 || inani == 124 || inani == 126 || inani == 128 || inani == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((inani == 108 || inani == 112) && 나 == 0) { ukwehluleka_inani("ArithmeticException: / by zero"); continue; }
                if (inani == 96) 결과 = 가 + 나;
                if (inani == 100) 결과 = 가 - 나;
                if (inani == 104) 결과 = 가 * 나;
                if (inani == 108) 결과 = 가 / 나;
                if (inani == 112) 결과 = 가 % 나;
                if (inani == 120) 결과 = 가 << 나;
                if (inani == 122) 결과 = 가 >> 나;
                if (inani == 124) 결과 = 가 >>> 나;
                if (inani == 126) 결과 = 가 & 나;
                if (inani == 128) 결과 = 가 | 나;
                if (inani == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (inani == 116) { 넣기(-빼기(1), 1); continue; }
            if (inani == 132) {
                int endaweni_umklamo = 명바(), 증분 = (byte)명바(); 지역읽기(endaweni_umklamo, 1); 넣기(빼기(1) + 증분, 1); bhala_endaweni(endaweni_umklamo, 1); continue;
            }
            if (inani >= 145 && inani <= 147) {
                int 수 = 빼기(1); 넣기(inani == 145 ? (byte)수 : inani == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (inani >= 153 && inani <= 167 || inani == 198 || inani == 199) {
                int isikhumulo_inani = Sebenzisa + (short)명짧(); boolean 갈까 = inani == 167;
                if (inani >= 153 && inani <= 158) {
                    int 수 = 빼기(1); 갈까 = inani == 153 ? 수 == 0 : inani == 154 ? 수 != 0 : inani == 155 ? 수 < 0 : inani == 156 ? 수 >= 0 : inani == 157 ? 수 > 0 : 수 <= 0;
                } else if (inani >= 159 && inani <= 166) {
                    int 나 = 빼기(inani >= 165 ? 2 : 1), 가 = 빼기(inani >= 165 ? 2 : 1);
                    갈까 = inani == 159 || inani == 165 ? 가 == 나 : inani == 160 || inani == 166 ? 가 != 나 : inani == 161 ? 가 < 나 : inani == 162 ? 가 >= 나 : inani == 163 ? 가 > 나 : 가 <= 나;
                } else if (inani == 198 || inani == 199) { int 수 = 빼기(2); 갈까 = inani == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) susa_inani(isikhumulo_inani); continue;
            }
            if (inani == 172 || inani == 176 || inani == 177) { 반환(inani == 172 ? 1 : inani == 176 ? 2 : 0); continue; }
            if (inani >= 178 && inani <= 181) { 필드호출(명상수(), inani, Sebenzisa); continue; }
            if (inani >= 182 && inani <= 185) {
                int 부호값 = 명상수();
                if (inani == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { ukwehluleka_inani("invalid invokeinterface operands"); continue; } }
                fonela_indlela(부호값, inani); continue;
            }
            if (inani == 187) { 새객체(uhlobo_igama_I_SMS(명상수()), Sebenzisa); continue; }
            if (inani == 188 || inani == 189) {
                int 분류코드 = 3, isixa = 0;
                if (inani == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else isixa = uhlobo_igama_I_SMS(명상수());
                if (분류코드 == 0) { ukwehluleka_inani("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), into_Ireferensi = abela_Indawo_yokugcina(분류코드, 유효길이); if (!Iphutha) AMALUNGU_AFANAYO_ilungu[into_Ireferensi] = isixa; 넣기(into_Ireferensi, 2); continue;
            }
            if (inani == 190) {
                int into_Ireferensi = 빼기(2);
                if (객체유효(into_Ireferensi)) { int 비교자리 = 힙[into_Ireferensi]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) ukwehluleka_inani("not an array"); else 넣기(힙[into_Ireferensi + 1], 1); }
                continue;
            }
            if (inani == 191) {
                int into_Ireferensi = 빼기(2); if (객체유효(into_Ireferensi)) { if (힙[into_Ireferensi] != 9) ukwehluleka_inani("athrow requires supported Throwable"); else { 던진객체 = into_Ireferensi; Iphutha = true; } }
                continue;
            }
            if (inani == 192 || inani == 193) {
                int igama_okungaguquki = uhlobo_igama_I_SMS(명상수()), into_Ireferensi = 빼기(2); boolean 일치여부 = 맞는객체(into_Ireferensi, igama_okungaguquki);
                if (inani == 193) 넣기(into_Ireferensi != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !Iphutha) ukwehluleka_inani("ClassCastException"); 넣기(into_Ireferensi, 2); }
                continue;
            }
            if (inani == 170 || inani == 171) {
                int 읽는자리 = Sebenzisa + 1, ifayela_thola_inkomba = uhlaka_indlela[uhlaka_thola_inkomba], inkomba_Ireferensi = 빼기(1);
                while ((읽는자리 - indlela_qala[ifayela_thola_inkomba]) % 4 != 0) 읽는자리++;
                int impokophelo_ikheli = 위치정수(읽는자리);
                if (inani == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (inkomba_Ireferensi >= 낮은값 && inkomba_Ireferensi <= 높은값) impokophelo_ikheli = 위치정수(읽는자리 + 12 + (inkomba_Ireferensi - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 총수; iluphu_thola_inkomba++) if (위치정수(읽는자리 + 8 + iluphu_thola_inkomba * 8) == inkomba_Ireferensi) impokophelo_ikheli = 위치정수(읽는자리 + 12 + iluphu_thola_inkomba * 8); }
                susa_inani(Sebenzisa + impokophelo_ikheli); continue;
            }
            if (inani == 200) { susa_inani(Sebenzisa + 위치정수(Sebenzisa + 1)); continue; }
            if (inani == 194 || inani == 195) {
                int into_Ireferensi = 빼기(2);
                if (inani == 195) 잠금풀기(into_Ireferensi);
                else if (!잠금얻기(into_Ireferensi) && !Iphutha) { 넣기(into_Ireferensi, 2); 틀위치[uhlaka_thola_inkomba] = Sebenzisa; }
                continue;
            }
            if (inani == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) bhala_endaweni(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); bhala_endaweni(항목자리, 1); }
                else ukwehluleka_inani("unsupported wide opcode");
                continue;
            }
            ukwehluleka_inani("unsupported bytecode");
        }
    }
    static int thola_uhlobo_Incazelo(int Igama) {
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 종수; iluphu_thola_inkomba++) if (uhlobo_Incazelo_igama[iluphu_thola_inkomba] != 0 && 같은말(uhlobo_Incazelo_igama[iluphu_thola_inkomba], Igama)) return iluphu_thola_inkomba;
        return faka_uhlobo_Incazelo(okungaguquki_I_SMS(Igama));
    }
    static int faka_uhlobo_Incazelo(int igama_uchunge) {
        if (!into_inani(igama_uchunge, 1)) return -1;
        int ubude_inani = 힙[igama_uchunge + 1];
        if (ubude_inani < 1 || ubude_inani > 505 || 종수 == 16) { ukwehluleka_inani("class name/count limit"); return -1; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < ubude_inani; iluphu_thola_inkomba++) { int ikhodi_yohlamvu = 힙[igama_uchunge + 2 + iluphu_thola_inkomba]; ifayela_igama_I_SMS[iluphu_thola_inkomba] = ikhodi_yohlamvu == '/' ? '.' : ikhodi_yohlamvu; }
        ifayela_igama_I_SMS[ubude_inani] = '.'; ifayela_igama_I_SMS[ubude_inani + 1] = 'c'; ifayela_igama_I_SMS[ubude_inani + 2] = 'l'; ifayela_igama_I_SMS[ubude_inani + 3] = 'a'; ifayela_igama_I_SMS[ubude_inani + 4] = 's'; ifayela_igama_I_SMS[ubude_inani + 5] = 's'; ifayela_igama_I_SMS[ubude_inani + 6] = 0;
        int Ubungako = umsebenzisi.파일읽기(ifayela_igama_I_SMS, 임시파일);
        if (Ubungako < 0) { ukwehluleka_inani("ClassNotFoundException"); return -1; }
        int uhlobo_Incazelo = 종수++; uhlobo_Incazelo_linganisa[uhlobo_Incazelo] = Ubungako;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) Ihele[uhlobo_Incazelo * 16384 + iluphu_thola_inkomba] = 임시파일[iluphu_thola_inkomba];
        클래스읽기(uhlobo_Incazelo); if (Iphutha) return -1;
        int ulwazi_ngokwenzekile_imininingwane = okungaguquki_I_SMS(uhlobo_Incazelo_igama[uhlobo_Incazelo]);
        if (!글같음(ulwazi_ngokwenzekile_imininingwane, igama_uchunge, true)) { ukwehluleka_inani("class name does not match file"); return -1; }
        int 부모 = 종부모[uhlobo_Incazelo];
        if (부모 != 0 && !Amagama_I_SMS(부모, "java/lang/Object") && !Amagama_I_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = thola_uhlobo_Incazelo(부모);
            if (Iphutha || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == uhlobo_Incazelo) { ukwehluleka_inani("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int ifayela_thola_inkomba = 0; ifayela_thola_inkomba < 칸수; ifayela_thola_inkomba++) if (isikhala_umnikazi[ifayela_thola_inkomba] == uhlobo_Incazelo && (isikhala_izimvume[ifayela_thola_inkomba] & 8) == 0) 칸위치[ifayela_thola_inkomba] += 시작변위;
            종칸수[uhlobo_Incazelo] += 시작변위;
        }
        return uhlobo_Incazelo;
    }
    static int 부모종(int uhlobo_Incazelo) {
        int Igama = 종부모[uhlobo_Incazelo];
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 종수; iluphu_thola_inkomba++) if (Igama != 0 && uhlobo_Incazelo_igama[iluphu_thola_inkomba] != 0 && 같은말(uhlobo_Incazelo_igama[iluphu_thola_inkomba], Igama)) return iluphu_thola_inkomba;
        return -1;
    }
    static int thola_indlela(int uhlobo_Incazelo, int Igama, int misa_inani) {
        for (int 깊이 = 0; uhlobo_Incazelo >= 0 && 깊이 < 16; 깊이++, uhlobo_Incazelo = 부모종(uhlobo_Incazelo)) {
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 함수수; iluphu_thola_inkomba++) if (indlela_umnikazi[iluphu_thola_inkomba] == uhlobo_Incazelo && 같은말(indlela_igama_I_SMS[iluphu_thola_inkomba], Igama) && 같은말(indlela_thayipha[iluphu_thola_inkomba], misa_inani)) return iluphu_thola_inkomba;
        }
        return -1;
    }
    static int igama_indlela(int uhlobo_Incazelo, String Igama, String misa_inani) {
        for (int 깊이 = 0; uhlobo_Incazelo >= 0 && 깊이 < 16; 깊이++, uhlobo_Incazelo = 부모종(uhlobo_Incazelo))
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 함수수; iluphu_thola_inkomba++) if (indlela_umnikazi[iluphu_thola_inkomba] == uhlobo_Incazelo && Amagama_I_SMS(indlela_igama_I_SMS[iluphu_thola_inkomba], Igama) && Amagama_I_SMS(indlela_thayipha[iluphu_thola_inkomba], misa_inani)) return iluphu_thola_inkomba;
        return -1;
    }
    static int 형종류(int Igama) { return Ihele[상가[Igama]] == 'L' || Ihele[상가[Igama]] == '[' ? 2 : 1; }
    static boolean qalisa(int uhlobo_Incazelo, int umyalo_qala) {
        if (uhlobo_Incazelo < 0 || Iphutha) return false;
        if (uhlobo_Incazelo_isimo[uhlobo_Incazelo] == 3) { ukwehluleka_inani("NoClassDefFoundError: initialization failed"); return false; }
        if (uhlobo_Incazelo_isimo[uhlobo_Incazelo] == 1 && uhlobo_uhlu_lwemilayezo[uhlobo_Incazelo] != 현재가닥) { 틀위치[uhlaka_thola_inkomba] = umyalo_qala; 바꿈요청 = true; return false; }
        if (uhlobo_Incazelo_isimo[uhlobo_Incazelo] != 0) return true;
        int 위 = 부모종(uhlobo_Incazelo);
        if (위 >= 0 && !qalisa(위, umyalo_qala)) return false;
        uhlobo_Incazelo_isimo[uhlobo_Incazelo] = 1; uhlobo_uhlu_lwemilayezo[uhlobo_Incazelo] = 현재가닥;
        if (qalisa_uhlobo_Incazelo[uhlobo_Incazelo] != 0) {
            틀위치[uhlaka_thola_inkomba] = umyalo_qala;
            호출(qalisa_uhlobo_Incazelo[uhlobo_Incazelo] - 1); if (!Iphutha) qalisa_uhlaka[uhlaka_thola_inkomba] = uhlobo_Incazelo + 1;
            return false;
        }
        uhlobo_Incazelo_isimo[uhlobo_Incazelo] = 2; return true;
    }
    static void 필드호출(int thola_inkomba, int Umlayelo, int Sebenzisa) {
        if (!hlola_okungaguquki(thola_inkomba, 9)) return;
        int umnikazi_inani = uhlobo_igama_I_SMS(상가[thola_inkomba]), Igama = Ireferensi_igama(상나[thola_inkomba]), misa_inani = Ireferensi_thayipha(상나[thola_inkomba]);
        if (Amagama_I_SMS(umnikazi_inani, "java/lang/System") && (Amagama_I_SMS(Igama, "out") || Amagama_I_SMS(Igama, "err")) && Amagama_I_SMS(misa_inani, "Ljava/io/PrintStream;") && Umlayelo == 178) { 넣기(-1, 2); return; }
        int uhlobo_Incazelo = thola_uhlobo_Incazelo(umnikazi_inani); if (uhlobo_Incazelo < 0 || Iphutha) return;
        int 찾음 = -1;
        for (int 읽는자리 = uhlobo_Incazelo, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int ifayela_thola_inkomba = 0; ifayela_thola_inkomba < 칸수; ifayela_thola_inkomba++) if (isikhala_umnikazi[ifayela_thola_inkomba] == 읽는자리 && 같은말(isikhala_igama[ifayela_thola_inkomba], Igama) && 같은말(isikhala_thayipha[ifayela_thola_inkomba], misa_inani)) 찾음 = ifayela_thola_inkomba;
        if (찾음 < 0) { ukwehluleka_inani("NoSuchFieldError"); return; }
        boolean ngaguquki_inani = Umlayelo == 178 || Umlayelo == 179;
        if (ngaguquki_inani != ((isikhala_izimvume[찾음] & 8) != 0)) { ukwehluleka_inani("field static/instance mismatch"); return; }
        if (ngaguquki_inani && !qalisa(isikhala_umnikazi[찾음], Sebenzisa)) return;
        int thayipha_inani = 형종류(misa_inani), inani = 0;
        if (Umlayelo == 179 || Umlayelo == 181) inani = 빼기(thayipha_inani);
        if (ngaguquki_inani) { if (Umlayelo == 178) 넣기(isikhala_imininingwane[찾음], thayipha_inani); else if (!Iphutha) isikhala_imininingwane[찾음] = inani; return; }
        int into_Ireferensi = 빼기(2);
        if (!객체유효(into_Ireferensi)) return;
        if (힙[into_Ireferensi] < 32 || !종포함(힙[into_Ireferensi] - 32, umnikazi_inani)) { ukwehluleka_inani("field receiver type mismatch"); return; }
        int 보관칸 = into_Ireferensi + 2 + 칸위치[찾음];
        if (Umlayelo == 180) 넣기(힙[보관칸], thayipha_inani);
        else if (!Iphutha) { 힙[보관칸] = inani; 힙참조[보관칸] = thayipha_inani == 2 ? 1 : 0; }
    }
    static boolean 종포함(int uhlobo_Incazelo, int Igama) {
        for (int 중첩깊이 = 0; uhlobo_Incazelo >= 0 && 중첩깊이 < 16; 중첩깊이++, uhlobo_Incazelo = 부모종(uhlobo_Incazelo)) {
            if (같은말(uhlobo_Incazelo_igama[uhlobo_Incazelo], Igama) || (종부모[uhlobo_Incazelo] != 0 && 같은말(종부모[uhlobo_Incazelo], Igama))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[uhlobo_Incazelo]; 안쪽자리++) if (같은말(uhlobo_ukusebenzisana[uhlobo_Incazelo * 16 + 안쪽자리], Igama)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int ibhayithi_imininingwane, boolean Indlela_2) {
        if (첫값 == ibhayithi_imininingwane) return true;
        if (첫값 <= 0 || ibhayithi_imininingwane <= 0 || 힙[첫값] != 1 || 힙[ibhayithi_imininingwane] != 1 || 힙[첫값 + 1] != 힙[ibhayithi_imininingwane + 1]) return false;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 힙[첫값 + 1]; iluphu_thola_inkomba++) {
            int okuxhumanisa_u_x = 힙[첫값 + 2 + iluphu_thola_inkomba], 세로좌표 = 힙[ibhayithi_imininingwane + 2 + iluphu_thola_inkomba];
            if (Indlela_2) { if (okuxhumanisa_u_x == '.') okuxhumanisa_u_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (okuxhumanisa_u_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int into_Ireferensi) {
        if (into_Ireferensi == 0) { ukwehluleka_inani("NullPointerException"); return false; }
        if (into_Ireferensi < 1 || into_Ireferensi >= 힙끝 || 힙폭[into_Ireferensi] < 2 || 힙[into_Ireferensi] == 0) { ukwehluleka_inani("invalid object reference"); return false; }
        return true;
    }
    static void vikela_inani(int into_Ireferensi) {
        if (into_Ireferensi > 0 && into_Ireferensi < 힙끝 && 힙폭[into_Ireferensi] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = into_Ireferensi;
    }
    static void khombisa_inani(int into_Ireferensi) {
        if (into_Ireferensi > 0 && into_Ireferensi < 힙끝 && 힙폭[into_Ireferensi] >= 2 && 힙[into_Ireferensi] != 0 && 힙표시[into_Ireferensi] == 0) {
            힙표시[into_Ireferensi] = 1; 표시대기[표시수++] = into_Ireferensi;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < uchunge_Ireferensi.length; iluphu_thola_inkomba++) khombisa_inani(uchunge_Ireferensi[iluphu_thola_inkomba]);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 칸수; iluphu_thola_inkomba++) if ((isikhala_izimvume[iluphu_thola_inkomba] & 8) != 0 && 형종류(isikhala_thayipha[iluphu_thola_inkomba]) == 2) khombisa_inani(isikhala_imininingwane[iluphu_thola_inkomba]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            khombisa_inani(uhlu_lwemilayezo_into[임시값]); khombisa_inani(uhlu_lwemilayezo_impokophelo[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? uhlaka_thola_inkomba : uhlu_lwemilayezo_uhlaka[임시값];
            for (int ifayela_thola_inkomba = 임시값 * 32; ifayela_thola_inkomba <= 꼭대기자리; ifayela_thola_inkomba++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[uhlaka_indlela[ifayela_thola_inkomba]]; 안쪽자리++) if (endaweni_thayipha[ifayela_thola_inkomba * 128 + 안쪽자리] == 2) khombisa_inani(endaweni_inani[ifayela_thola_inkomba * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < uhlaka_Isitaki[ifayela_thola_inkomba]; 안쪽자리++) if (스택형[ifayela_thola_inkomba * 128 + 안쪽자리] == 2) khombisa_inani(스택값[ifayela_thola_inkomba * 128 + 안쪽자리]);
            }
        }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 화면참조.length; iluphu_thola_inkomba++) khombisa_inani(화면참조[iluphu_thola_inkomba]);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 나중수; iluphu_thola_inkomba++) khombisa_inani(나중실행[iluphu_thola_inkomba]);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Store_inamba.length; iluphu_thola_inkomba++) khombisa_inani(Store_inamba[iluphu_thola_inkomba]);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 종수; iluphu_thola_inkomba++) khombisa_inani(종잠금[iluphu_thola_inkomba]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) khombisa_inani(검사자리);
        khombisa_inani(던진객체);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 잠시수; iluphu_thola_inkomba++) khombisa_inani(잠시참조[iluphu_thola_inkomba]);
        while (표시수 > 0) {
            int into_Ireferensi = 표시대기[--표시수], 분류코드 = 힙[into_Ireferensi];
            for (int iluphu_thola_inkomba = into_Ireferensi + 2; iluphu_thola_inkomba < into_Ireferensi + 힙폭[into_Ireferensi]; iluphu_thola_inkomba++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[iluphu_thola_inkomba] != 0) khombisa_inani(힙[iluphu_thola_inkomba]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int ubude_inani) {
        if (ubude_inani < 0) { ukwehluleka_inani("NegativeArraySizeException"); return 0; }
        if (ubude_inani > 힙.length - 3) { ukwehluleka_inani("object heap exhausted"); return 0; }
        int 필요수 = ubude_inani + 2, into_Ireferensi = 0;
        if (필요수 <= 힙.length - 힙끝) { into_Ireferensi = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { into_Ireferensi = 읽는자리; break; }
            if (into_Ireferensi != 0) {
                int 남은길이 = 힙폭[into_Ireferensi] - 필요수;
                if (남은길이 >= 2) { 힙폭[into_Ireferensi + 필요수] = 남은길이; 힙[into_Ireferensi + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { into_Ireferensi = 힙끝; 힙끝 += 필요수; }
        }
        if (into_Ireferensi == 0) { ukwehluleka_inani("object heap exhausted"); return 0; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 필요수; iluphu_thola_inkomba++) { 힙[into_Ireferensi + iluphu_thola_inkomba] = 0; 힙참조[into_Ireferensi + iluphu_thola_inkomba] = 0; 힙폭[into_Ireferensi + iluphu_thola_inkomba] = 0; }
        AMALUNGU_AFANAYO_ilungu[into_Ireferensi] = 0;
        힙폭[into_Ireferensi] = 필요수; 힙[into_Ireferensi] = 종류; 힙[into_Ireferensi + 1] = ubude_inani; vikela_inani(into_Ireferensi); return into_Ireferensi;
    }
    static int 예외종(String igama_okungaguquki) {
        if (자바도구.같음(igama_okungaguquki, "java/lang/Throwable")) return 1;
        if (자바도구.같음(igama_okungaguquki, "java/lang/Exception")) return 2;
        if (자바도구.같음(igama_okungaguquki, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(igama_okungaguquki, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(igama_okungaguquki, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(igama_okungaguquki, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(igama_okungaguquki, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(igama_okungaguquki, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(igama_okungaguquki, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(igama_okungaguquki, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(igama_okungaguquki, "java/io/IOException")) return 11;
        if (자바도구.같음(igama_okungaguquki, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(igama_okungaguquki, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(igama_okungaguquki, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(igama_okungaguquki, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Igama) {
        for (int iluphu_thola_inkomba = 1; iluphu_thola_inkomba <= 41; iluphu_thola_inkomba++) if (Amagama_I_SMS(Igama, 예외이름(iluphu_thola_inkomba))) return iluphu_thola_inkomba;
        return 0;
    }
    static String 예외이름(int ubutho_inani) {
        if (ubutho_inani == 40) return "java/lang/InterruptedException";
        if (ubutho_inani == 41) return "Isi_Zulu/자체/대기중단예외";
        if (ubutho_inani == 39) return "java/net/SocketException";
        if (ubutho_inani == 20) return "Isi_Zulu/자체/예외";
        if (ubutho_inani == 21) return "Isi_Zulu/자체/실행예외";
        if (ubutho_inani == 22) return "Isi_Zulu/자체/입출력예외";
        if (ubutho_inani == 23) return "Isi_Zulu/자체/대기시간초과예외";
        if (ubutho_inani == 24) return "Isi_Zulu/자체/주소확인예외";
        if (ubutho_inani == 25) return "Isi_Zulu/자체/파일없음예외";
        if (ubutho_inani == 26) return "Isi_Zulu/자체/통신예외";
        if (ubutho_inani == 27) return "Isi_Zulu/자체/잘못된인수예외";
        if (ubutho_inani == 28) return "Isi_Zulu/자체/숫자형식예외";
        if (ubutho_inani == 29) return "Isi_Zulu/자체/범위예외";
        if (ubutho_inani == 30) return "Isi_Zulu/자체/배열범위예외";
        if (ubutho_inani == 31) return "Isi_Zulu/자체/문자열범위예외";
        if (ubutho_inani == 32) return "Isi_Zulu/자체/빈참조예외";
        if (ubutho_inani == 33) return "Isi_Zulu/자체/산술예외";
        if (ubutho_inani == 34) return "Isi_Zulu/자체/상태예외";
        if (ubutho_inani == 35) return "Isi_Zulu/자체/형변환예외";
        if (ubutho_inani == 36) return "Isi_Zulu/자체/음수배열크기예외";
        if (ubutho_inani == 37) return "Isi_Zulu/자체/AMALUNGU_AFANAYO_Store_ukwehluleka";
        if (ubutho_inani == 38) return "Isi_Zulu/자체/가닥상태예외";
        if (ubutho_inani == 1) return "java/lang/Throwable"; if (ubutho_inani == 2) return "java/lang/Exception";
        if (ubutho_inani == 3) return "java/lang/RuntimeException"; if (ubutho_inani == 4) return "java/lang/ArithmeticException";
        if (ubutho_inani == 5) return "java/lang/NullPointerException"; if (ubutho_inani == 6) return "java/lang/IndexOutOfBoundsException";
        if (ubutho_inani == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (ubutho_inani == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (ubutho_inani == 9) return "java/lang/IllegalArgumentException"; if (ubutho_inani == 10) return "java/lang/NumberFormatException";
        if (ubutho_inani == 11) return "java/io/IOException"; if (ubutho_inani == 12) return "java/io/FileNotFoundException";
        if (ubutho_inani == 17) return "java/lang/ArrayStoreException";
        if (ubutho_inani == 18) return "java/net/UnknownHostException";
        if (ubutho_inani == 19) return "java/net/SocketTimeoutException";
        if (ubutho_inani == 16) return "java/lang/IllegalThreadStateException";
        if (ubutho_inani == 13) return "java/lang/IllegalStateException"; if (ubutho_inani == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int ubutho_inani) {
        if (ubutho_inani == 40) return 2;
        if (ubutho_inani == 41) return 40;
        if (ubutho_inani == 39) return 11;
        if (ubutho_inani == 1) return 0;
        if (ubutho_inani == 2) return 1;
        if (ubutho_inani == 3) return 2;
        if (ubutho_inani == 4) return 3;
        if (ubutho_inani == 5) return 3;
        if (ubutho_inani == 6) return 3;
        if (ubutho_inani == 7) return 6;
        if (ubutho_inani == 8) return 6;
        if (ubutho_inani == 9) return 3;
        if (ubutho_inani == 10) return 9;
        if (ubutho_inani == 11) return 2;
        if (ubutho_inani == 12) return 11;
        if (ubutho_inani == 13) return 3;
        if (ubutho_inani == 14) return 3;
        if (ubutho_inani == 15) return 3;
        if (ubutho_inani == 16) return 9;
        if (ubutho_inani == 17) return 3;
        if (ubutho_inani == 18) return 11;
        if (ubutho_inani == 19) return 11;
        if (ubutho_inani == 20) return 2;
        if (ubutho_inani == 21) return 3;
        if (ubutho_inani == 22) return 11;
        if (ubutho_inani == 23) return 22;
        if (ubutho_inani == 24) return 22;
        if (ubutho_inani == 25) return 22;
        if (ubutho_inani == 26) return 22;
        if (ubutho_inani == 27) return 9;
        if (ubutho_inani == 28) return 27;
        if (ubutho_inani == 29) return 6;
        if (ubutho_inani == 30) return 29;
        if (ubutho_inani == 31) return 29;
        if (ubutho_inani == 32) return 5;
        if (ubutho_inani == 33) return 4;
        if (ubutho_inani == 34) return 13;
        if (ubutho_inani == 35) return 14;
        if (ubutho_inani == 36) return 15;
        if (ubutho_inani == 37) return 17;
        if (ubutho_inani == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int ulwazi_ngokwenzekile_inani, int 요구값) {
        for (int 깊이 = 0; ulwazi_ngokwenzekile_inani != 0 && 깊이 < 16; 깊이++, ulwazi_ngokwenzekile_inani = 예외부모(ulwazi_ngokwenzekile_inani))
            if (ulwazi_ngokwenzekile_inani == 요구값) return true;
        return false;
    }
    static void 예외던짐(int ubutho_inani, String NGIFUNDE_Ireferensi) {
        int into_Ireferensi = 새기억(9, 2); if (Iphutha) return;
        힙[into_Ireferensi + 2] = ubutho_inani; 힙[into_Ireferensi + 3] = singatha_uhlamvusimo(NGIFUNDE_Ireferensi); 힙참조[into_Ireferensi + 3] = 1;
        던진객체 = into_Ireferensi; Iphutha = true;
    }
    static boolean 맞는객체(int into_Ireferensi, int Igama) {
        if (into_Ireferensi == 0) return true;
        if (!객체유효(into_Ireferensi)) return false;
        int 분류코드 = 힙[into_Ireferensi];
        if (Amagama_I_SMS(Igama, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Igama);
        if (분류코드 == 9) { int impokophelo_ikheli = 예외상수(Igama); return impokophelo_ikheli != 0 && 예외포함(힙[into_Ireferensi + 2], impokophelo_ikheli); }
        if (분류코드 == 1) return Amagama_I_SMS(Igama, "java/lang/String") || Amagama_I_SMS(Igama, "java/lang/CharSequence");
        if (분류코드 == 4) return Amagama_I_SMS(Igama, "java/lang/StringBuilder") || Amagama_I_SMS(Igama, "java/lang/CharSequence");
        if (분류코드 == 10) return Amagama_I_SMS(Igama, "java/util/ArrayList") || Amagama_I_SMS(Igama, "java/util/List");
        if (분류코드 == 11) return Amagama_I_SMS(Igama, "java/util/HashMap") || Amagama_I_SMS(Igama, "java/util/Map");
        if (분류코드 == 12) return Amagama_I_SMS(Igama, "java/lang/Integer") || Amagama_I_SMS(Igama, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[into_Ireferensi + 13] != 0) return 한국어화면종(Igama) == 분류코드 || Amagama_I_SMS(Igama, "Isi_Zulu/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Igama) == 0 && 화면종(Igama) == 분류코드) || Amagama_I_SMS(Igama, "java/awt/Component") || Amagama_I_SMS(Igama, "java/awt/Container") || Amagama_I_SMS(Igama, "javax/swing/JComponent");
        if (분류코드 == 29) return Amagama_I_SMS(Igama, 힙[into_Ireferensi + 3] != 0 ? "Isi_Zulu/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Amagama_I_SMS(Igama, "java/awt/FlowLayout") || Amagama_I_SMS(Igama, "java/awt/LayoutManager");
        if (분류코드 == 17) return Amagama_I_SMS(Igama, "java/net/Socket");
        if (분류코드 == 18) return Amagama_I_SMS(Igama, "java/net/ServerSocket");
        if (분류코드 == 19) return Amagama_I_SMS(Igama, 힙[into_Ireferensi + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Amagama_I_SMS(Igama, "java/net/InetAddress");
        if (분류코드 == 15) return Amagama_I_SMS(Igama, "java/net/DatagramSocket");
        if (분류코드 == 16) return Amagama_I_SMS(Igama, "java/net/DatagramPacket");
        if (분류코드 == 13) return Amagama_I_SMS(Igama, 힙[into_Ireferensi + 3] != 0 ? "Isi_Zulu/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Amagama_I_SMS(Igama, "[I"); if (분류코드 == 20) return Amagama_I_SMS(Igama, "[B"); if (분류코드 == 21) return Amagama_I_SMS(Igama, "[Z");
        if (분류코드 == 22) return Amagama_I_SMS(Igama, "[C"); if (분류코드 == 23) return Amagama_I_SMS(Igama, "[S");
        if (분류코드 != 3) return false;
        if (Amagama_I_SMS(Igama, "[Ljava/lang/Object;")) return true;
        int isixa = AMALUNGU_AFANAYO_ilungu[into_Ireferensi];
        if (isixa == -1) return Amagama_I_SMS(Igama, "[Ljava/lang/String;") || Amagama_I_SMS(Igama, "[Ljava/lang/CharSequence;");
        if (isixa == 0) return false;
        if (배열종비교(isixa, Igama)) return true;
        if ((Amagama_I_SMS(isixa, "java/lang/String") || Amagama_I_SMS(isixa, "java/lang/StringBuilder")) && Amagama_I_SMS(Igama, "[Ljava/lang/CharSequence;")) return true;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 종수; iluphu_thola_inkomba++) if (같은말(uhlobo_Incazelo_igama[iluphu_thola_inkomba], isixa)) {
            for (int ikhodi_yohlamvu = iluphu_thola_inkomba, 중첩깊이 = 0; ikhodi_yohlamvu >= 0 && 중첩깊이 < 16; 중첩깊이++, ikhodi_yohlamvu = 부모종(ikhodi_yohlamvu)) {
                if (배열종비교(종부모[ikhodi_yohlamvu], Igama)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[ikhodi_yohlamvu]; 안쪽자리++) if (배열종비교(uhlobo_ukusebenzisana[ikhodi_yohlamvu * 16 + 안쪽자리], Igama)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int igama_okungaguquki, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (igama_okungaguquki == 0 || 항목수 < 4 || Ihele[검사자리] != '[' || Ihele[검사자리 + 1] != 'L' || Ihele[검사자리 + 항목수 - 1] != ';' || 상나[igama_okungaguquki] != 항목수 - 3) return false;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수 - 3; iluphu_thola_inkomba++) if (Ihele[상가[igama_okungaguquki] + iluphu_thola_inkomba] != Ihele[검사자리 + 2 + iluphu_thola_inkomba]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Iphutha = false;
        while (uhlaka_thola_inkomba >= 현재가닥 * 32) {
            int ifayela_thola_inkomba = uhlaka_indlela[uhlaka_thola_inkomba], 읽는자리 = uhlaka_umyalelo[uhlaka_thola_inkomba];
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 잡기수; iluphu_thola_inkomba++) if (잡기함수[iluphu_thola_inkomba] == ifayela_thola_inkomba && 읽는자리 >= 잡기시작[iluphu_thola_inkomba] && 읽는자리 < 잡기끝[iluphu_thola_inkomba]
                && (잡기종[iluphu_thola_inkomba] == 0 || 맞는객체(던진객체, 잡기종[iluphu_thola_inkomba]))) {
                틀위치[uhlaka_thola_inkomba] = 잡기위치[iluphu_thola_inkomba]; uhlaka_Isitaki[uhlaka_thola_inkomba] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (qalisa_uhlaka[uhlaka_thola_inkomba] != 0) uhlobo_Incazelo_isimo[qalisa_uhlaka[uhlaka_thola_inkomba] - 1] = 3;
            if (틀잠금[uhlaka_thola_inkomba] != 0) { 잠금풀기(틀잠금[uhlaka_thola_inkomba]); 틀잠금[uhlaka_thola_inkomba] = 0; }
            uhlaka_thola_inkomba--;
        }
        umsebenzisi.Bhala("Uncaught ");
        if (힙[던진객체] == 9) { umsebenzisi.Bhala(예외이름(힙[던진객체 + 2])); umsebenzisi.Bhala(": "); bhala_I_SMS(힙[던진객체 + 3]); }
        else umsebenzisi.Bhala("user exception");
        umsebenzisi.bhala_uhlamvusimo_inani(10); 던진객체 = 0; Iphutha = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Isitaki_umyalelo(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int ibhayithi_imininingwane = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식); 넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(ibhayithi_imininingwane, 둘째형식); return; }
        int ikhodi_yohlamvu = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(ikhodi_yohlamvu, 셋째형식); 넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식); 넣기(ikhodi_yohlamvu, 셋째형식); 넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(ikhodi_yohlamvu, 셋째형식); 넣기(ibhayithi_imininingwane, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int igama_okungaguquki, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(igama_okungaguquki);
        if (Amagama_I_SMS(igama_okungaguquki, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/lang/Thread") || Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Amagama_I_SMS(igama_okungaguquki, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(igama_okungaguquki) != 0) { 분류코드 = 화면종(igama_okungaguquki); 유효길이 = 12; }
        if (분류코드 == 0) {
            int ikhodi_yohlamvu = thola_uhlobo_Incazelo(igama_okungaguquki); if (ikhodi_yohlamvu < 0 || Iphutha || !qalisa(ikhodi_yohlamvu, 시작점)) return;
            분류코드 = 32 + ikhodi_yohlamvu; 유효길이 = 종칸수[ikhodi_yohlamvu];
        }
        int into_Ireferensi = abela_Indawo_yokugcina(분류코드, 유효길이); if (Iphutha) return;
        if (분류코드 == 13 && Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/작업가닥")) 힙[into_Ireferensi + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(igama_okungaguquki) != 0) 힙[into_Ireferensi + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[into_Ireferensi + 2] = -1;
        if (분류코드 == 9) 힙[into_Ireferensi + 2] = 예외참조;
        넣기(into_Ireferensi, 2);
    }
    static boolean 값같음(int 첫값, int ibhayithi_imininingwane) {
        if (첫값 == ibhayithi_imininingwane) return true;
        if (첫값 == 0 || ibhayithi_imininingwane == 0 || 첫값 < 0 || ibhayithi_imininingwane < 0 || 첫값 >= 힙끝 || ibhayithi_imininingwane >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[ibhayithi_imininingwane] == 1) return 글같음(첫값, ibhayithi_imininingwane, false);
        return 힙[첫값] == 12 && 힙[ibhayithi_imininingwane] == 12 && 힙[첫값 + 2] == 힙[ibhayithi_imininingwane + 2];
    }
    static int 글조각(int into_Ireferensi, int 시작자리, int 끝자리) {
        if (!into_inani(into_Ireferensi, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[into_Ireferensi + 1]) { ukwehluleka_inani("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = abela_Indawo_yokugcina(1, 끝자리 - 시작자리); if (Iphutha) return 0;
        for (int iluphu_thola_inkomba = 시작자리; iluphu_thola_inkomba < 끝자리; iluphu_thola_inkomba++) 힙[반환값 + 2 + iluphu_thola_inkomba - 시작자리] = 힙[into_Ireferensi + 2 + iluphu_thola_inkomba];
        return 반환값;
    }
    static int joyina_I_SMS(int 첫값, int ibhayithi_imininingwane) {
        if (!into_inani(첫값, 1) || !into_inani(ibhayithi_imininingwane, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], indlela_thola_inkomba = 힙[ibhayithi_imininingwane + 1], 반환값 = abela_Indawo_yokugcina(1, 항목수 + indlela_thola_inkomba); if (Iphutha) return 0;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 힙[반환값 + 2 + iluphu_thola_inkomba] = 힙[첫값 + 2 + iluphu_thola_inkomba];
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < indlela_thola_inkomba; iluphu_thola_inkomba++) 힙[반환값 + 2 + 항목수 + iluphu_thola_inkomba] = 힙[ibhayithi_imininingwane + 2 + iluphu_thola_inkomba];
        return 반환값;
    }
    static boolean 기본호출(int umnikazi, int igama_okungaguquki, int 서술상수, int 명령코드) {
        if (Amagama_I_SMS(umnikazi, "Isi_Zulu/자체/실행인수") && 명령코드 == 184) {
            if (Amagama_I_SMS(igama_okungaguquki, "개수") && Amagama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.인수개수() - 1, 1); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "Itekisi") && Amagama_I_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= umsebenzisi.인수개수() - 1) 예외던짐(29, "yenza_umyalo 인수 범위를 벗어났습니다");
                else 넣기(singatha_uhlamvusimo(umsebenzisi.인수(순번 + 1)), 2);
                return true;
            }
            ukwehluleka_inani("지원하지 않는 Isi_Zulu yenza_umyalo 인수 호출"); return true;
        }
        if (Amagama_I_SMS(umnikazi, "Isi_Zulu/자체/작업가닥")) { Inqubo_uhlu_lwemilayezo(igama_okungaguquki, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(umnikazi)) { 한국어화면호출(umnikazi, igama_okungaguquki, 서술상수, 명령코드); return true; }
        if (화면소유(umnikazi)) { 화면호출(umnikazi, igama_okungaguquki, 서술상수, 명령코드); return true; }
        if (Amagama_I_SMS(umnikazi, "java/net/Socket") || Amagama_I_SMS(umnikazi, "java/net/ServerSocket") || Amagama_I_SMS(umnikazi, "java/io/InputStream") || Amagama_I_SMS(umnikazi, "java/io/OutputStream")) { 흐름호출(umnikazi, igama_okungaguquki, 서술상수, 명령코드); return true; }
        if (Amagama_I_SMS(umnikazi, "Isi_Zulu/자체/ikhenela_inani") && 명령코드 == 184) {
            if (Amagama_I_SMS(igama_okungaguquki, "화면너비") && Amagama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.화면너비(), 1); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "화면높이") && Amagama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.화면높이(), 1); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "밀리초") && Amagama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.밀리초(), 1); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "그림대기") && Amagama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.그림대기(), 1); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "사각형") && Amagama_I_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), okuxhumanisa_u_x = 빼기(1); 넣기(umsebenzisi.사각형(okuxhumanisa_u_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Amagama_I_SMS(umnikazi, "java/net/InetAddress") || Amagama_I_SMS(umnikazi, "java/net/DatagramPacket") || Amagama_I_SMS(umnikazi, "java/net/DatagramSocket")) { 통신호출(umnikazi, igama_okungaguquki, 서술상수, 명령코드); return true; }
        if (Amagama_I_SMS(umnikazi, "java/lang/Thread")) { 가닥호출(igama_okungaguquki, 서술상수, 명령코드); return true; }
        if (Amagama_I_SMS(umnikazi, "java/lang/Object")) {
            if (Amagama_I_SMS(igama_okungaguquki, "<init>") && Amagama_I_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "equals") && Amagama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int ibhayithi_imininingwane = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == ibhayithi_imininingwane ? 1 : 0, 1); return true; }
        }
        if (예외상수(umnikazi) != 0) {
            if (Amagama_I_SMS(igama_okungaguquki, "<init>") && 명령코드 == 183 && (Amagama_I_SMS(서술상수, "()V") || Amagama_I_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int ozokusebenzisa = Amagama_I_SMS(서술상수, "()V") ? 0 : 빼기(2), into_Ireferensi = 빼기(2);
                if (into_inani(into_Ireferensi, 9)) { 힙[into_Ireferensi + 3] = ozokusebenzisa; 힙참조[into_Ireferensi + 3] = 1; } return true;
            }
            if ((Amagama_I_SMS(igama_okungaguquki, "getMessage") || Amagama_I_SMS(igama_okungaguquki, "설명")) && Amagama_I_SMS(서술상수, "()Ljava/lang/String;")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 9)) 넣기(힙[into_Ireferensi + 3], 2); return true; }
        }
        if (Amagama_I_SMS(umnikazi, "java/lang/String")) {
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "getBytes") && (Amagama_I_SMS(서술상수, "()[B") || Amagama_I_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int ukubhala_ngokufihla_igama = Amagama_I_SMS(서술상수, "()[B") ? 0 : 빼기(2), into_Ireferensi = 빼기(2);
                if (!into_inani(into_Ireferensi, 1)) return true;
                if (ukubhala_ngokufihla_igama != 0 && !글같음(ukubhala_ngokufihla_igama, singatha_uhlamvusimo("UTF-8"), false) && !글같음(ukubhala_ngokufihla_igama, singatha_uhlamvusimo("UTF8"), false) && !글같음(ukubhala_ngokufihla_igama, singatha_uhlamvusimo("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[into_Ireferensi + 1], 반환값 = abela_Indawo_yokugcina(20, 항목수 * 3), 사용수 = 0; if (Iphutha) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int ikhodi_yohlamvu = 힙[into_Ireferensi + 2 + 안쪽자리];
                    if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[into_Ireferensi + 3 + 안쪽자리] >= 0xdc00 && 힙[into_Ireferensi + 3 + 안쪽자리] <= 0xdfff) ikhodi_yohlamvu = 0x10000 + ((ikhodi_yohlamvu - 0xd800) << 10) + 힙[into_Ireferensi + 2 + ++안쪽자리] - 0xdc00;
                    else if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdfff) ikhodi_yohlamvu = '?';
                    if (ikhodi_yohlamvu < 128) 힙[반환값 + 2 + 사용수++] = ikhodi_yohlamvu;
                    else { int 바이트수 = ikhodi_yohlamvu < 2048 ? 2 : ikhodi_yohlamvu < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | ikhodi_yohlamvu >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | ikhodi_yohlamvu >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "valueOf") && Amagama_I_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(idijithi_uhlamvusimo(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Amagama_I_SMS(igama_okungaguquki, "equals") && Amagama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int ibhayithi_imininingwane = 빼기(2), 첫값 = 빼기(2); if (into_inani(첫값, 1)) 넣기(글같음(첫값, ibhayithi_imininingwane, false) ? 1 : 0, 1); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "isEmpty") && Amagama_I_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (into_inani(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "substring") && (Amagama_I_SMS(서술상수, "(I)Ljava/lang/String;") || Amagama_I_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Amagama_I_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (into_inani(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Amagama_I_SMS(igama_okungaguquki, "concat") && Amagama_I_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int ibhayithi_imininingwane = 빼기(2), 첫값 = 빼기(2); 넣기(joyina_I_SMS(첫값, ibhayithi_imininingwane), 2); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "hashCode") && Amagama_I_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), i_hash_inani = 0; if (into_inani(첫값, 1)) { for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 힙[첫값 + 1]; iluphu_thola_inkomba++) i_hash_inani = i_hash_inani * 31 + 힙[첫값 + 2 + iluphu_thola_inkomba]; 넣기(i_hash_inani, 1); } return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "toString") && Amagama_I_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (into_inani(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Amagama_I_SMS(umnikazi, "java/lang/Integer")) {
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "valueOf") && Amagama_I_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int imininingwane_inani = 빼기(1), into_Ireferensi = imininingwane_inani >= -128 && imininingwane_inani <= 127 ? Store_inamba[imininingwane_inani + 128] : 0; if (into_Ireferensi == 0) { into_Ireferensi = abela_Indawo_yokugcina(12, 1); if (!Iphutha) { 힙[into_Ireferensi + 2] = imininingwane_inani; if (imininingwane_inani >= -128 && imininingwane_inani <= 127) Store_inamba[imininingwane_inani + 128] = into_Ireferensi; } } 넣기(into_Ireferensi, 2); return true; }
            if (명령코드 == 183 && Amagama_I_SMS(igama_okungaguquki, "<init>") && Amagama_I_SMS(서술상수, "(I)V")) { int imininingwane_inani = 빼기(1), into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 12)) 힙[into_Ireferensi + 2] = imininingwane_inani; return true; }
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "intValue") && Amagama_I_SMS(서술상수, "()I")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 12)) 넣기(힙[into_Ireferensi + 2], 1); return true; }
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "toString") && Amagama_I_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(idijithi_uhlamvusimo(빼기(1)), 2); return true; }
        }
        if (Amagama_I_SMS(umnikazi, "java/lang/Math") && 명령코드 == 184) {
            if (Amagama_I_SMS(igama_okungaguquki, "abs") && Amagama_I_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Amagama_I_SMS(igama_okungaguquki, "min") || Amagama_I_SMS(igama_okungaguquki, "max")) && Amagama_I_SMS(서술상수, "(II)I")) { int ibhayithi_imininingwane = 빼기(1), 첫값 = 빼기(1); 넣기(Amagama_I_SMS(igama_okungaguquki, "min") ? (첫값 < ibhayithi_imininingwane ? 첫값 : ibhayithi_imininingwane) : (첫값 > ibhayithi_imininingwane ? 첫값 : ibhayithi_imininingwane), 1); return true; }
        }
        if (Amagama_I_SMS(umnikazi, "java/lang/System") && 명령코드 == 184) {
            if (Amagama_I_SMS(igama_okungaguquki, "gc") && Amagama_I_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Amagama_I_SMS(igama_okungaguquki, "arraycopy") && Amagama_I_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), isikhumulo_inani_thola_inkomba = 빼기(1), ibhayithi_imininingwane = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(ibhayithi_imininingwane)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[ibhayithi_imininingwane] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) ukwehluleka_inani("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || isikhumulo_inani_thola_inkomba < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || isikhumulo_inani_thola_inkomba > 힙[ibhayithi_imininingwane + 1] - 항목수) ukwehluleka_inani("ArrayIndexOutOfBoundsException");
                    else if (첫값 == ibhayithi_imininingwane && isikhumulo_inani_thola_inkomba > 시작자리) { for (int iluphu_thola_inkomba = 항목수 - 1; iluphu_thola_inkomba >= 0; iluphu_thola_inkomba--) 힙[ibhayithi_imininingwane + 2 + isikhumulo_inani_thola_inkomba + iluphu_thola_inkomba] = 힙[첫값 + 2 + 시작자리 + iluphu_thola_inkomba]; }
                    else { for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수 && !Iphutha; iluphu_thola_inkomba++) { int imininingwane_inani = 힙[첫값 + 2 + 시작자리 + iluphu_thola_inkomba]; if (분류코드 != 3 || 배열저장가능(ibhayithi_imininingwane, imininingwane_inani)) 힙[ibhayithi_imininingwane + 2 + isikhumulo_inani_thola_inkomba + iluphu_thola_inkomba] = imininingwane_inani; } }
                }
                return true;
            }
        }
        if (Amagama_I_SMS(umnikazi, "java/util/ArrayList") || Amagama_I_SMS(umnikazi, "java/util/List") || Amagama_I_SMS(umnikazi, "java/util/HashMap") || Amagama_I_SMS(umnikazi, "java/util/Map")) {
            모음호출(umnikazi, igama_okungaguquki, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int into_Ireferensi, int 필요수) {
        int 이전값 = 힙[into_Ireferensi + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int imininingwane_AMALUNGU_AFANAYO = abela_Indawo_yokugcina(3, 다음자리); if (Iphutha) return;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 용량값; iluphu_thola_inkomba++) 힙[imininingwane_AMALUNGU_AFANAYO + 2 + iluphu_thola_inkomba] = 힙[이전값 + 2 + iluphu_thola_inkomba];
        힙[into_Ireferensi + 2] = imininingwane_AMALUNGU_AFANAYO; 힙참조[into_Ireferensi + 2] = 1;
    }
    static void 모음호출(int umnikazi, int igama_okungaguquki, int 서술상수, int 명령코드) {
        boolean 대응참조 = Amagama_I_SMS(umnikazi, "java/util/HashMap") || Amagama_I_SMS(umnikazi, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Amagama_I_SMS(igama_okungaguquki, "<init>") && 명령코드 == 183 && Amagama_I_SMS(서술상수, "()V")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 분류코드)) 모음늘리기(into_Ireferensi, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { ukwehluleka_inani("invalid collection invocation"); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "size") && Amagama_I_SMS(서술상수, "()I") || Amagama_I_SMS(igama_okungaguquki, "isEmpty") && Amagama_I_SMS(서술상수, "()Z")) {
            int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 분류코드)) 넣기(Amagama_I_SMS(igama_okungaguquki, "size") ? 힙[into_Ireferensi + 3] : 힙[into_Ireferensi + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "clear") && Amagama_I_SMS(서술상수, "()V")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 분류코드)) { int imininingwane_AMALUNGU_AFANAYO = 힙[into_Ireferensi + 2]; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 힙[imininingwane_AMALUNGU_AFANAYO + 1]; iluphu_thola_inkomba++) 힙[imininingwane_AMALUNGU_AFANAYO + 2 + iluphu_thola_inkomba] = 0; 힙[into_Ireferensi + 3] = 0; } return; }
        if (!대응참조 && Amagama_I_SMS(igama_okungaguquki, "add") && Amagama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int imininingwane_inani = 빼기(2), into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 10)) return;
            int 항목수 = 힙[into_Ireferensi + 3]; 모음늘리기(into_Ireferensi, 항목수 + 1); if (!Iphutha) { 힙[힙[into_Ireferensi + 2] + 2 + 항목수] = imininingwane_inani; 힙[into_Ireferensi + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Amagama_I_SMS(igama_okungaguquki, "get") || Amagama_I_SMS(igama_okungaguquki, "remove")) && Amagama_I_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Amagama_I_SMS(igama_okungaguquki, "set") && Amagama_I_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Amagama_I_SMS(igama_okungaguquki, "set"); int imininingwane_inani = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), into_Ireferensi = 빼기(2);
            if (!into_inani(into_Ireferensi, 10)) return;
            int 항목수 = 힙[into_Ireferensi + 3], imininingwane_AMALUNGU_AFANAYO = 힙[into_Ireferensi + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 항목자리];
            if (지정여부) 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 항목자리] = imininingwane_inani;
            if (Amagama_I_SMS(igama_okungaguquki, "remove")) { for (int iluphu_thola_inkomba = 항목자리 + 1; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 힙[imininingwane_AMALUNGU_AFANAYO + 1 + iluphu_thola_inkomba] = 힙[imininingwane_AMALUNGU_AFANAYO + 2 + iluphu_thola_inkomba]; 힙[imininingwane_AMALUNGU_AFANAYO + 1 + 항목수] = 0; 힙[into_Ireferensi + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Amagama_I_SMS(igama_okungaguquki, "get") || Amagama_I_SMS(igama_okungaguquki, "remove")) && Amagama_I_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Amagama_I_SMS(igama_okungaguquki, "put") && Amagama_I_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Amagama_I_SMS(igama_okungaguquki, "containsKey") && Amagama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Amagama_I_SMS(igama_okungaguquki, "put"), khipha = Amagama_I_SMS(igama_okungaguquki, "remove");
            int imininingwane_inani = 넣기여부 ? 빼기(2) : 0, inkomba_Ireferensi = 빼기(2), into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 11)) return;
            int 항목수 = 힙[into_Ireferensi + 3], imininingwane_AMALUNGU_AFANAYO = 힙[into_Ireferensi + 2], 찾은여부 = -1;
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) if (값같음(inkomba_Ireferensi, 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 2 * iluphu_thola_inkomba])) { 찾은여부 = iluphu_thola_inkomba; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[imininingwane_AMALUNGU_AFANAYO + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(into_Ireferensi, (항목수 + 1) * 2); imininingwane_AMALUNGU_AFANAYO = 힙[into_Ireferensi + 2]; 찾은여부 = 항목수; if (!Iphutha) 힙[into_Ireferensi + 3] = 항목수 + 1; }
                if (!Iphutha) { 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 2 * 찾은여부] = inkomba_Ireferensi; 힙[imininingwane_AMALUNGU_AFANAYO + 3 + 2 * 찾은여부] = imininingwane_inani; }
            }
            if (khipha && 찾은여부 >= 0) { for (int iluphu_thola_inkomba = 찾은여부 + 1; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) { 힙[imininingwane_AMALUNGU_AFANAYO + 2 * iluphu_thola_inkomba] = 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 2 * iluphu_thola_inkomba]; 힙[imininingwane_AMALUNGU_AFANAYO + 1 + 2 * iluphu_thola_inkomba] = 힙[imininingwane_AMALUNGU_AFANAYO + 3 + 2 * iluphu_thola_inkomba]; } 힙[imininingwane_AMALUNGU_AFANAYO + 2 * 항목수] = 0; 힙[imininingwane_AMALUNGU_AFANAYO + 1 + 2 * 항목수] = 0; 힙[into_Ireferensi + 3] = 항목수 - 1; }
            if (Amagama_I_SMS(igama_okungaguquki, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        ukwehluleka_inani("unsupported collection method");
    }
    static boolean 잠금얻기(int into_Ireferensi) {
        if (!객체유효(into_Ireferensi)) return false;
        if (잠금깊이[into_Ireferensi] != 0 && 잠금주인[into_Ireferensi] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[into_Ireferensi] = 현재가닥 + 1; 잠금깊이[into_Ireferensi]++; return true;
    }
    static void 잠금풀기(int into_Ireferensi) {
        if (!객체유효(into_Ireferensi)) return;
        if (잠금깊이[into_Ireferensi] == 0 || 잠금주인[into_Ireferensi] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[into_Ireferensi] == 0) 잠금주인[into_Ireferensi] = 0;
    }
    static boolean guqulela_kokunye_uhlu_lwemilayezo() {
        uhlu_lwemilayezo_uhlaka[현재가닥] = uhlaka_thola_inkomba;
        if (uhlaka_thola_inkomba < 현재가닥 * 32) uhlu_lwemilayezo_isimo[현재가닥] = 3;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 가닥수; iluphu_thola_inkomba++) if (uhlu_lwemilayezo_isimo[iluphu_thola_inkomba] == 2 && uhlu_lwemilayezo_isimo[가닥대기[iluphu_thola_inkomba]] == 3) uhlu_lwemilayezo_isimo[iluphu_thola_inkomba] = 1;
        for (int iluphu_thola_inkomba = 1; iluphu_thola_inkomba <= 가닥수; iluphu_thola_inkomba++) {
            int 다음자리 = (현재가닥 + iluphu_thola_inkomba) % 가닥수;
            if (uhlu_lwemilayezo_isimo[다음자리] == 1) { 현재가닥 = 다음자리; uhlaka_thola_inkomba = uhlu_lwemilayezo_uhlaka[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 가닥수; iluphu_thola_inkomba++) if (uhlu_lwemilayezo_isimo[iluphu_thola_inkomba] != 3) { ukwehluleka_inani("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int igama_okungaguquki, int 서술상수, int 명령코드) { Inqubo_uhlu_lwemilayezo(igama_okungaguquki, 서술상수, 명령코드, false); }
    static void Inqubo_uhlu_lwemilayezo(int igama_okungaguquki, int 서술상수, int 명령코드, boolean Isi_Zulu) {
        if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, Isi_Zulu ? "misa_okwesikhashana_umsebenzi" : "yield") && Amagama_I_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "currentThread") && Amagama_I_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(uhlu_lwemilayezo_into[현재가닥], 2); return; }
        if (명령코드 == 183 && Amagama_I_SMS(igama_okungaguquki, "<init>") && (Amagama_I_SMS(서술상수, "()V") || Amagama_I_SMS(서술상수, Isi_Zulu ? "(LIsi_Zulu/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int impokophelo_ikheli = Amagama_I_SMS(서술상수, "()V") ? 0 : 빼기(2), into_Ireferensi = 빼기(2);
            if (!객체유효(into_Ireferensi)) return;
            if (힙[into_Ireferensi] == 13) { 힙[into_Ireferensi + 2] = impokophelo_ikheli; 힙참조[into_Ireferensi + 2] = 1; }
            else if (impokophelo_ikheli != 0) ukwehluleka_inani("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Amagama_I_SMS(igama_okungaguquki, Isi_Zulu ? "qala_umsebenzi" : "start") || Amagama_I_SMS(igama_okungaguquki, Isi_Zulu ? "기다리기" : "join")) && Amagama_I_SMS(서술상수, "()V") || 명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, Isi_Zulu ? "살아있는가" : "isAlive") && Amagama_I_SMS(서술상수, "()Z")) {
            int into_Ireferensi = 빼기(2); if (!객체유효(into_Ireferensi)) return;
            int ubutho_inani = -1; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 가닥수; iluphu_thola_inkomba++) if (uhlu_lwemilayezo_into[iluphu_thola_inkomba] == into_Ireferensi) ubutho_inani = iluphu_thola_inkomba;
            if (Amagama_I_SMS(igama_okungaguquki, Isi_Zulu ? "살아있는가" : "isAlive")) { 넣기(ubutho_inani >= 0 && uhlu_lwemilayezo_isimo[ubutho_inani] != 3 ? 1 : 0, 1); return; }
            if (Amagama_I_SMS(igama_okungaguquki, Isi_Zulu ? "기다리기" : "join")) { if (ubutho_inani >= 0 && uhlu_lwemilayezo_isimo[ubutho_inani] != 3) { 가닥대기[현재가닥] = ubutho_inani; uhlu_lwemilayezo_isimo[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (ubutho_inani >= 0) { 예외던짐(Isi_Zulu ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { ukwehluleka_inani("thread limit (4 including main)"); return; }
            int impokophelo_ikheli = 힙[into_Ireferensi] == 13 ? 힙[into_Ireferensi + 2] : into_Ireferensi;
            int ifayela_thola_inkomba = impokophelo_ikheli > 0 && 힙[impokophelo_ikheli] >= 32 ? igama_indlela(힙[impokophelo_ikheli] - 32, Isi_Zulu ? "yenza_umsebenzi" : "run", "()V") : -1;
            if (impokophelo_ikheli != 0 && ifayela_thola_inkomba < 0) { ukwehluleka_inani("Runnable.run required"); return; }
            ubutho_inani = 가닥수++; uhlu_lwemilayezo_into[ubutho_inani] = into_Ireferensi; uhlu_lwemilayezo_impokophelo[ubutho_inani] = impokophelo_ikheli;
            int uhlaka = ubutho_inani * 32; uhlu_lwemilayezo_uhlaka[ubutho_inani] = ifayela_thola_inkomba < 0 ? uhlaka - 1 : uhlaka; uhlu_lwemilayezo_isimo[ubutho_inani] = ifayela_thola_inkomba < 0 ? 3 : 1;
            if (ifayela_thola_inkomba >= 0) { uhlaka_indlela[uhlaka] = ifayela_thola_inkomba; 틀위치[uhlaka] = indlela_qala[ifayela_thola_inkomba]; endaweni_inani[uhlaka * 128] = impokophelo_ikheli; endaweni_thayipha[uhlaka * 128] = 2; }
            return;
        }
        ukwehluleka_inani("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ikheli_I_SMS = new int[16];
    static int endaweni_ikheli() { return ikheli_into(0x7f000001); }
    static int ikheli_into(int inani) { int into_Ireferensi = abela_Indawo_yokugcina(14, 1); if (!Iphutha) 힙[into_Ireferensi + 2] = inani; return into_Ireferensi; }
    static int 주소해독(int into_Ireferensi) {
        if (into_Ireferensi == 0 || 글같음(into_Ireferensi, singatha_uhlamvusimo("localhost"), false)) return 0x7f000001;
        if (!into_inani(into_Ireferensi, 1)) return 0;
        int imininingwane_inani = 0, 총수 = 0, ikheli_ibhayithi = 0, 자릿수 = 0, 항목수 = 힙[into_Ireferensi + 1];
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba <= 항목수; iluphu_thola_inkomba++) {
            int ikhodi_yohlamvu = iluphu_thola_inkomba == 항목수 ? '.' : 힙[into_Ireferensi + 2 + iluphu_thola_inkomba];
            if (ikhodi_yohlamvu == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } imininingwane_inani = imininingwane_inani << 8 | ikheli_ibhayithi; 총수++; ikheli_ibhayithi = 자릿수 = 0; }
            else { if (ikhodi_yohlamvu < '0' || ikhodi_yohlamvu > '9' || ++자릿수 > 3 || (ikheli_ibhayithi = ikheli_ibhayithi * 10 + ikhodi_yohlamvu - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return imininingwane_inani;
    }
    static int ikheli_uhlamvusimo(int imininingwane_inani) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ikheli_ibhayithi = imininingwane_inani >>> 이동비트 & 255;
            if (ikheli_ibhayithi >= 100) ikheli_I_SMS[항목수++] = '0' + ikheli_ibhayithi / 100;
            if (ikheli_ibhayithi >= 10) ikheli_I_SMS[항목수++] = '0' + ikheli_ibhayithi / 10 % 10;
            ikheli_I_SMS[항목수++] = '0' + ikheli_ibhayithi % 10; if (이동비트 != 0) ikheli_I_SMS[항목수++] = '.';
        }
        int into_Ireferensi = abela_Indawo_yokugcina(1, 항목수); if (!Iphutha) for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 힙[into_Ireferensi + 2 + iluphu_thola_inkomba] = ikheli_I_SMS[iluphu_thola_inkomba]; return into_Ireferensi;
    }
    static void 통신호출(int umnikazi, int igama_okungaguquki, int 서술상수, int 명령코드) {
        if (Amagama_I_SMS(umnikazi, "java/net/InetAddress")) {
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "getLoopbackAddress") && Amagama_I_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(endaweni_ikheli(), 2); return; }
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "getByName") && Amagama_I_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int imininingwane_inani = 주소해독(빼기(2)); if (던진객체 == 0 && !Iphutha) 넣기(ikheli_into(imininingwane_inani), 2); return;
            }
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "getHostAddress") && Amagama_I_SMS(서술상수, "()Ljava/lang/String;")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 14)) 넣기(ikheli_uhlamvusimo(힙[into_Ireferensi + 2]), 2); return; }
        }
        if (Amagama_I_SMS(umnikazi, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Amagama_I_SMS(igama_okungaguquki, "<init>") && (Amagama_I_SMS(서술상수, "([BI)V") || Amagama_I_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean isikhumulo_inani_Ireferensi = Amagama_I_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = isikhumulo_inani_Ireferensi ? 빼기(1) : 0, ikheli_Ireferensi = isikhumulo_inani_Ireferensi ? 빼기(2) : 0;
                int 항목수 = 빼기(1), imininingwane_AMALUNGU_AFANAYO = 빼기(2), into_Ireferensi = 빼기(2);
                if (!into_inani(into_Ireferensi, 16) || !into_inani(imininingwane_AMALUNGU_AFANAYO, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[imininingwane_AMALUNGU_AFANAYO + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ikheli_Ireferensi != 0 && !into_inani(ikheli_Ireferensi, 14)) return;
                힙[into_Ireferensi + 2] = imininingwane_AMALUNGU_AFANAYO; 힙참조[into_Ireferensi + 2] = 1; 힙[into_Ireferensi + 3] = 항목수;
                힙[into_Ireferensi + 4] = ikheli_Ireferensi; 힙참조[into_Ireferensi + 4] = 1; 힙[into_Ireferensi + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "setLength") && Amagama_I_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[into_Ireferensi + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[into_Ireferensi + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Amagama_I_SMS(igama_okungaguquki, "getData") && Amagama_I_SMS(서술상수, "()[B") || Amagama_I_SMS(igama_okungaguquki, "getLength") && Amagama_I_SMS(서술상수, "()I") || Amagama_I_SMS(igama_okungaguquki, "getAddress") && Amagama_I_SMS(서술상수, "()Ljava/net/InetAddress;") || Amagama_I_SMS(igama_okungaguquki, "getPort") && Amagama_I_SMS(서술상수, "()I"))) {
                int into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 16)) return;
                int 항목자리 = Amagama_I_SMS(igama_okungaguquki, "getData") ? 2 : Amagama_I_SMS(igama_okungaguquki, "getLength") ? 3 : Amagama_I_SMS(igama_okungaguquki, "getAddress") ? 4 : 5;
                넣기(힙[into_Ireferensi + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Amagama_I_SMS(umnikazi, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Amagama_I_SMS(igama_okungaguquki, "<init>") && (Amagama_I_SMS(서술상수, "()V") || Amagama_I_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Amagama_I_SMS(서술상수, "()V") ? 0 : 빼기(1), into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = umsebenzisi.vula_iNethiwekhi(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[into_Ireferensi + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "setSoTimeout") && Amagama_I_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[into_Ireferensi + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "getLocalPort") && Amagama_I_SMS(서술상수, "()I")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 15)) 넣기(힙[into_Ireferensi + 2] < 0 ? -1 : umsebenzisi.iNethiwekhi_intuba(힙[into_Ireferensi + 2]), 1); return; }
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "isClosed") && Amagama_I_SMS(서술상수, "()Z")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 15)) 넣기(힙[into_Ireferensi + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Amagama_I_SMS(igama_okungaguquki, "close") && Amagama_I_SMS(서술상수, "()V")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 15) && 힙[into_Ireferensi + 2] >= 0) { umsebenzisi.파일서술자닫기(힙[into_Ireferensi + 2]); 힙[into_Ireferensi + 2] = -1; } return; }
            if (명령코드 == 182 && (Amagama_I_SMS(igama_okungaguquki, "send") || Amagama_I_SMS(igama_okungaguquki, "receive")) && Amagama_I_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int iphakethe = 빼기(2), into_Ireferensi = 빼기(2); if (!into_inani(iphakethe, 16) || !into_inani(into_Ireferensi, 15)) return;
                int imininingwane_AMALUNGU_AFANAYO = 힙[iphakethe + 2], 유효길이 = 힙[iphakethe + 3], 열린파일번호 = 힙[into_Ireferensi + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Amagama_I_SMS(igama_okungaguquki, "send")) {
                    if (!into_inani(힙[iphakethe + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 유효길이; iluphu_thola_inkomba++) 통신임시[iluphu_thola_inkomba] = 힙[imininingwane_AMALUNGU_AFANAYO + 2 + iluphu_thola_inkomba];
                    if (umsebenzisi.Thumela_iNethiwekhi(열린파일번호, 힙[힙[iphakethe + 4] + 2], 힙[iphakethe + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = umsebenzisi.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = umsebenzisi.밀리초();
                        if (힙[into_Ireferensi + 4] == 0) 힙[into_Ireferensi + 4] = 현재시각 + 1;
                        if (힙[into_Ireferensi + 3] > 0 && 현재시각 - (힙[into_Ireferensi + 4] - 1) >= 힙[into_Ireferensi + 3]) { 힙[into_Ireferensi + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(into_Ireferensi, 2); 넣기(iphakethe, 2); 틀위치[uhlaka_thola_inkomba] = uhlaka_umyalelo[uhlaka_thola_inkomba]; 바꿈요청 = true; return;
                    }
                    힙[into_Ireferensi + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 힙[imininingwane_AMALUNGU_AFANAYO + 2 + iluphu_thola_inkomba] = (byte)통신임시[iluphu_thola_inkomba];
                    힙[iphakethe + 3] = 항목수; 힙[iphakethe + 4] = ikheli_into(통신임시[513]); 힙참조[iphakethe + 4] = 1; 힙[iphakethe + 5] = 통신임시[512];
                }
                return;
            }
        }
        ukwehluleka_inani("unsupported java.net method");
    }
    static boolean 흐름대기(int into_Ireferensi) {
        int 현재시각 = umsebenzisi.밀리초();
        if (힙[into_Ireferensi + 5] == 0) 힙[into_Ireferensi + 5] = 현재시각 + 1;
        if (힙[into_Ireferensi + 3] > 0 && 현재시각 - (힙[into_Ireferensi + 5] - 1) >= 힙[into_Ireferensi + 3]) { 힙[into_Ireferensi + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[uhlaka_thola_inkomba] = uhlaka_umyalelo[uhlaka_thola_inkomba]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int umnikazi, int igama_okungaguquki, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Amagama_I_SMS(umnikazi, "java/net/ServerSocket"), Stream = Amagama_I_SMS(umnikazi, "java/io/InputStream") || Amagama_I_SMS(umnikazi, "java/io/OutputStream");
        if (!Stream && 명령코드 == 183 && Amagama_I_SMS(igama_okungaguquki, "<init>")) {
            boolean 빈여부 = Amagama_I_SMS(서술상수, "()V"), 이름지정여부 = Amagama_I_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Amagama_I_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Amagama_I_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { ukwehluleka_inani("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), ikheli_Ireferensi = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, into_Ireferensi = 빼기(2);
            if (!into_inani(into_Ireferensi, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !into_inani(ikheli_Ireferensi, 14)) return;
            int iNethiwekhi_ikheli = 이름지정여부 ? 주소해독(ikheli_Ireferensi) : 주소지정여부 ? 힙[ikheli_Ireferensi + 2] : 0x7f000001;
            if (Iphutha || 던진객체 != 0) return;
            int 열린파일번호 = umsebenzisi.Stream_isilawuli(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? umsebenzisi.Stream_isilawuli(1, 열린파일번호, 접속번호) : umsebenzisi.xhuma_Stream(열린파일번호, iNethiwekhi_ikheli, 접속번호);
            if (처리값 < 0) { umsebenzisi.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[into_Ireferensi + 2] = 열린파일번호; 힙[into_Ireferensi + 4] = 접속번호; 힙[into_Ireferensi + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Amagama_I_SMS(igama_okungaguquki, "setSoTimeout") && Amagama_I_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[into_Ireferensi + 3] = 밀리초값; return; }
        if (!Stream && Amagama_I_SMS(igama_okungaguquki, "close") && Amagama_I_SMS(서술상수, "()V")) { int into_Ireferensi = 빼기(2); if (into_inani(into_Ireferensi, 수신쪽 ? 18 : 17) && 힙[into_Ireferensi + 2] >= 0) { umsebenzisi.파일서술자닫기(힙[into_Ireferensi + 2]); 힙[into_Ireferensi + 2] = -1; } return; }
        if (!Stream && (Amagama_I_SMS(igama_okungaguquki, "getLocalPort") || Amagama_I_SMS(igama_okungaguquki, "getPort") || Amagama_I_SMS(igama_okungaguquki, "isClosed") || Amagama_I_SMS(igama_okungaguquki, "isConnected"))) {
            int into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 수신쪽 ? 18 : 17)) return;
            넣기(Amagama_I_SMS(igama_okungaguquki, "isClosed") ? 힙[into_Ireferensi + 2] < 0 ? 1 : 0 : Amagama_I_SMS(igama_okungaguquki, "isConnected") ? 힙[into_Ireferensi + 6] : Amagama_I_SMS(igama_okungaguquki, "getPort") ? 힙[into_Ireferensi + 4] : 힙[into_Ireferensi + 2] < 0 ? -1 : umsebenzisi.Stream_isilawuli(4, 힙[into_Ireferensi + 2], 0), 1); return;
        }
        if (수신쪽 && Amagama_I_SMS(igama_okungaguquki, "accept") && Amagama_I_SMS(서술상수, "()Ljava/net/Socket;")) {
            int into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 18)) return; int 열린파일번호 = umsebenzisi.Stream_isilawuli(3, 힙[into_Ireferensi + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(into_Ireferensi)) 넣기(into_Ireferensi, 2); return; }
            힙[into_Ireferensi + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = abela_Indawo_yokugcina(17, 5); if (Iphutha) { umsebenzisi.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = umsebenzisi.Stream_isilawuli(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Amagama_I_SMS(igama_okungaguquki, "getInputStream") && Amagama_I_SMS(서술상수, "()Ljava/io/InputStream;")) || (Amagama_I_SMS(igama_okungaguquki, "getOutputStream") && Amagama_I_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 17)) return; if (힙[into_Ireferensi + 2] < 0 || 힙[into_Ireferensi + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = abela_Indawo_yokugcina(19, 4); if (Iphutha) return; 힙[반환값 + 2] = into_Ireferensi; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Amagama_I_SMS(igama_okungaguquki, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Amagama_I_SMS(igama_okungaguquki, "read"), 쓰기여부 = Amagama_I_SMS(igama_okungaguquki, "write"), vimbela = Amagama_I_SMS(서술상수, "([B)I") || Amagama_I_SMS(서술상수, "([B)V"), 부분배열여부 = Amagama_I_SMS(서술상수, "([BII)I") || Amagama_I_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, imininingwane_AMALUNGU_AFANAYO = vimbela || 부분배열여부 ? 빼기(2) : 0;
            int imininingwane_inani = 쓰기여부 && Amagama_I_SMS(서술상수, "(I)V") ? 빼기(1) : 0, into_Ireferensi = 빼기(2);
            if (!into_inani(into_Ireferensi, 19)) return; int 부모참조 = 힙[into_Ireferensi + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Amagama_I_SMS(igama_okungaguquki, "close") && Amagama_I_SMS(서술상수, "()V")) { umsebenzisi.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Amagama_I_SMS(igama_okungaguquki, "flush") && Amagama_I_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[into_Ireferensi + 3] == 0)) { ukwehluleka_inani("unsupported stream operation"); return; }
            if (vimbela || 부분배열여부) { if (!into_inani(imininingwane_AMALUNGU_AFANAYO, 20)) return; if (vimbela) 항목수 = 힙[imininingwane_AMALUNGU_AFANAYO + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[imininingwane_AMALUNGU_AFANAYO + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[into_Ireferensi + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? umsebenzisi.파일한바이트읽기(열린파일번호) : umsebenzisi.파일한바이트쓰기(열린파일번호, vimbela || 부분배열여부 ? 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 시작변위 + 완료수] : imininingwane_inani);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (vimbela || 부분배열여부)) 힙[imininingwane_AMALUNGU_AFANAYO + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(vimbela || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[into_Ireferensi + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(into_Ireferensi, 2); if (vimbela || 부분배열여부) 넣기(imininingwane_AMALUNGU_AFANAYO, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(vimbela || 부분배열여부)) 넣기(imininingwane_inani, 1); } return;
            }
            힙[into_Ireferensi + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : vimbela || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        ukwehluleka_inani("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int igama_okungaguquki) {
        if (Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/ifasitela")) return 24;
        if (Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/uphawu")) return 26;
        if (Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/inkinobho")) return 27;
        if (Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/I_SMS_inkundla_indawana")) return 28;
        if (Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int igama_okungaguquki) {
        return 한국어화면종(igama_okungaguquki) != 0 || Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/화면구성요소") || Amagama_I_SMS(igama_okungaguquki, "Isi_Zulu/자체/isigameko_ujenge");
    }
    static int 화면종(int igama_okungaguquki) {
        int 한국어종 = 한국어화면종(igama_okungaguquki); if (한국어종 != 0) return 한국어종;
        if (Amagama_I_SMS(igama_okungaguquki, "javax/swing/JFrame")) return 24;
        if (Amagama_I_SMS(igama_okungaguquki, "javax/swing/JPanel")) return 25;
        if (Amagama_I_SMS(igama_okungaguquki, "javax/swing/JLabel")) return 26;
        if (Amagama_I_SMS(igama_okungaguquki, "javax/swing/JButton")) return 27;
        if (Amagama_I_SMS(igama_okungaguquki, "javax/swing/JTextField")) return 28;
        if (Amagama_I_SMS(igama_okungaguquki, "java/awt/event/ActionEvent")) return 29;
        if (Amagama_I_SMS(igama_okungaguquki, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int igama_okungaguquki) {
        return 화면종(igama_okungaguquki) != 0 || Amagama_I_SMS(igama_okungaguquki, "java/awt/Component") || Amagama_I_SMS(igama_okungaguquki, "java/awt/Container") || Amagama_I_SMS(igama_okungaguquki, "javax/swing/JComponent") || Amagama_I_SMS(igama_okungaguquki, "javax/swing/AbstractButton") || Amagama_I_SMS(igama_okungaguquki, "javax/swing/text/JTextComponent") || Amagama_I_SMS(igama_okungaguquki, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int into_Ireferensi) { if (!객체유효(into_Ireferensi)) return false; if (힙[into_Ireferensi] < 24 || 힙[into_Ireferensi] > 28) { ukwehluleka_inani("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int into_Ireferensi, int I_SMS_Ireferensi) {
        if (I_SMS_Ireferensi != 0 && !into_inani(I_SMS_Ireferensi, 1)) return;
        int 항목수 = I_SMS_Ireferensi == 0 ? 0 : 힙[I_SMS_Ireferensi + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 화면글임시[iluphu_thola_inkomba] = 힙[I_SMS_Ireferensi + 2 + iluphu_thola_inkomba];
        if (umsebenzisi.화면글(힙[into_Ireferensi + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[into_Ireferensi + 3] = I_SMS_Ireferensi; 힙참조[into_Ireferensi + 3] = 1;
    }
    static int 화면문자읽기(int into_Ireferensi) {
        int ubutho_inani = 힙[into_Ireferensi + 2], 항목수 = umsebenzisi.화면연결(8, ubutho_inani, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { ukwehluleka_inani("GUI text read failed"); return 0; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) { int 부호값 = umsebenzisi.화면연결(9, ubutho_inani, iluphu_thola_inkomba, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = abela_Indawo_yokugcina(1, 사용수); if (!Iphutha) for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 사용수; iluphu_thola_inkomba++) 힙[반환값 + 2 + iluphu_thola_inkomba] = 화면글임시[iluphu_thola_inkomba]; return 반환값;
    }
    /* Isi_Zulu 객체를 직접 만들고 ikhenela_inani 화면 기능에 연결한다. Swing into_inani/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int umnikazi, int igama_okungaguquki, int 서술상수, int 명령코드) {
        if (Amagama_I_SMS(umnikazi, "Isi_Zulu/자체/isigameko_ujenge")) {
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "나중에실행") && Amagama_I_SMS(서술상수, "(LIsi_Zulu/자체/실행할일;)V")) {
                int umsebenzi_isenzo = 빼기(2); if (!객체유효(umsebenzi_isenzo)) return;
                if (나중수 == 8) { ukwehluleka_inani("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = umsebenzi_isenzo; return;
            }
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "사건처리중인가") && Amagama_I_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ukwehluleka_inani("지원하지 않는 Isi_Zulu 화면 일정 호출"); return;
        }
        if (Amagama_I_SMS(umnikazi, "Isi_Zulu/자체/동작알림")) {
            int 알림 = 빼기(2); if (!into_inani(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Amagama_I_SMS(igama_okungaguquki, "isigameko_umthombo") && Amagama_I_SMS(서술상수, "()LIsi_Zulu/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Amagama_I_SMS(igama_okungaguquki, "umyalo_I_SMS") && Amagama_I_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Amagama_I_SMS(igama_okungaguquki, "thola_inkomba") && Amagama_I_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ukwehluleka_inani("지원하지 않는 Isi_Zulu Isenzo 알림 호출"); return;
        }
        if (명령코드 == 183 && Amagama_I_SMS(igama_okungaguquki, "<init>")) {
            int 종류 = 한국어화면종(umnikazi), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Amagama_I_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (umsebenzisi.화면너비() - 폭) / 2; 세로 = (umsebenzisi.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Amagama_I_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Amagama_I_SMS(서술상수, "(Ljava/lang/String;IIIILIsi_Zulu/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { ukwehluleka_inani("지원하지 않는 Isi_Zulu 화면 생성자"); return; }
            int Itekisi = 빼기(2), ilungu_inani = 빼기(2); if (!화면객체(ilungu_inani)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > umsebenzisi.화면너비() - 가로 || 높이 > umsebenzisi.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int thola_inkomba = umsebenzisi.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (thola_inkomba < 1 || thola_inkomba > 32) { ukwehluleka_inani("화면 ilungu_inani 자리가 가득 찼습니다"); return; }
            힙[ilungu_inani + 2] = thola_inkomba; 화면참조[thola_inkomba - 1] = ilungu_inani;
            힙[ilungu_inani + 5] = 가로; 힙[ilungu_inani + 6] = 세로; 힙[ilungu_inani + 7] = 폭; 힙[ilungu_inani + 8] = 높이; 힙[ilungu_inani + 10] = 2;
            힙[ilungu_inani + 4] = 받이; 힙참조[ilungu_inani + 4] = 1; 힙[ilungu_inani + 12] = 1;
            umsebenzisi.화면연결(1, thola_inkomba, 가로, 세로, 폭, 높이);
            if (종류 == 24) umsebenzisi.화면연결(7, thola_inkomba, 2, 0, 0, 0);
            화면문자설정(ilungu_inani, Itekisi); return;
        }
        if (명령코드 != 182) { ukwehluleka_inani("잘못된 Isi_Zulu 화면 호출 Umlayelo"); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "bhala_I_SMS") && Amagama_I_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Itekisi = 빼기(2), ilungu_inani = 빼기(2); if (화면객체(ilungu_inani)) 화면문자설정(ilungu_inani, Itekisi); return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "글읽기") && Amagama_I_SMS(서술상수, "()Ljava/lang/String;")) {
            int ilungu_inani = 빼기(2); if (화면객체(ilungu_inani)) 넣기(화면문자읽기(ilungu_inani), 2); return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "동작맡기기") && Amagama_I_SMS(서술상수, "(LIsi_Zulu/자체/동작받이;)V")) {
            int 받이 = 빼기(2), ilungu_inani = 빼기(2);
            if (화면객체(ilungu_inani)) { 힙[ilungu_inani + 4] = 받이; 힙참조[ilungu_inani + 4] = 1; 힙[ilungu_inani + 12] = 1; } return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "hlanganisa_ilungu") && Amagama_I_SMS(서술상수, "(LIsi_Zulu/자체/화면구성요소;)V")) {
            int ingane_inani = 빼기(2), 부모 = 빼기(2); if (!화면객체(ingane_inani) || !화면객체(부모)) return;
            if (umsebenzisi.화면연결(2, 힙[부모 + 2], 힙[ingane_inani + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[ingane_inani + 11] = 부모; 힙참조[ingane_inani + 11] = 1; return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "자리정하기") && Amagama_I_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), ilungu_inani = 빼기(2); if (!화면객체(ilungu_inani)) return;
            if (umsebenzisi.화면연결(1, 힙[ilungu_inani + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[ilungu_inani + 5] = 가로; 힙[ilungu_inani + 6] = 세로; 힙[ilungu_inani + 7] = 폭; 힙[ilungu_inani + 8] = 높이; return;
        }
        if ((Amagama_I_SMS(igama_okungaguquki, "khombisa_ifasitela") || Amagama_I_SMS(igama_okungaguquki, "Vala")) && Amagama_I_SMS(서술상수, "()V")) {
            boolean ukubonakala_inani = Amagama_I_SMS(igama_okungaguquki, "khombisa_ifasitela"); int ilungu_inani = 빼기(2); if (!화면객체(ilungu_inani)) return;
            if (umsebenzisi.화면연결(ukubonakala_inani ? 3 : 4, 힙[ilungu_inani + 2], ukubonakala_inani ? 1 : 0, 0, 0, 0) < 0) { ukwehluleka_inani("화면은 ingxoxo_nekhompiyutha 명령에서 실행해야 합니다"); return; }
            힙[ilungu_inani + 9] = ukubonakala_inani ? 1 : 0; return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "보이는가") && Amagama_I_SMS(서술상수, "()Z")) { int ilungu_inani = 빼기(2); if (화면객체(ilungu_inani)) 넣기(힙[ilungu_inani + 9], 1); return; }
        ukwehluleka_inani("지원하지 않는 Isi_Zulu 화면 indlela_inani");
    }
    static void 화면호출(int umnikazi, int igama_okungaguquki, int 서술상수, int 명령코드) {
        if (Amagama_I_SMS(umnikazi, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "invokeLater") && Amagama_I_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int into_Ireferensi = 빼기(2); if (!객체유효(into_Ireferensi)) return; if (나중수 == 8) { ukwehluleka_inani("invokeLater queue full"); return; } 나중실행[나중수++] = into_Ireferensi; return; }
            if (명령코드 == 184 && Amagama_I_SMS(igama_okungaguquki, "isEventDispatchThread") && Amagama_I_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ukwehluleka_inani("unsupported SwingUtilities method"); return;
        }
        if (Amagama_I_SMS(umnikazi, "java/awt/event/ActionEvent")) {
            int into_Ireferensi = 빼기(2); if (!into_inani(into_Ireferensi, 29)) return;
            if (Amagama_I_SMS(igama_okungaguquki, "getSource") && Amagama_I_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[into_Ireferensi + 2], 2);
            else if (Amagama_I_SMS(igama_okungaguquki, "getActionCommand") && Amagama_I_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[into_Ireferensi + 2]), 2);
            else if (Amagama_I_SMS(igama_okungaguquki, "getID") && Amagama_I_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ukwehluleka_inani("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Amagama_I_SMS(igama_okungaguquki, "<init>")) {
            int 열수 = 0, I_SMS_Ireferensi = 0;
            if (Amagama_I_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Amagama_I_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); I_SMS_Ireferensi = 빼기(2); }
            else if (Amagama_I_SMS(서술상수, "(Ljava/lang/String;)V")) I_SMS_Ireferensi = 빼기(2);
            else if (Amagama_I_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Amagama_I_SMS(서술상수, "()V")) { ukwehluleka_inani("unsupported Swing constructor"); return; }
            int into_Ireferensi = 빼기(2); if (!객체유효(into_Ireferensi)) return;
            if (힙[into_Ireferensi] == 30) { ukwehluleka_inani("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(into_Ireferensi) || 열수 < 0) return;
            int ubutho_inani = umsebenzisi.화면연결(0, 힙[into_Ireferensi] - 23, 0, 0, 0, 0);
            if (ubutho_inani < 1 || ubutho_inani > 32) { ukwehluleka_inani("GUI widget slots exhausted"); return; }
            힙[into_Ireferensi + 2] = ubutho_inani; 화면참조[ubutho_inani - 1] = into_Ireferensi; 힙[into_Ireferensi + 5] = 힙[into_Ireferensi] == 24 ? 130 : 16; 힙[into_Ireferensi + 6] = 힙[into_Ireferensi] == 24 ? 110 : 16;
            힙[into_Ireferensi + 7] = 힙[into_Ireferensi] == 24 ? 380 : 220; 힙[into_Ireferensi + 8] = 힙[into_Ireferensi] == 24 ? 240 : 28; 힙[into_Ireferensi + 10] = 1;
            화면문자설정(into_Ireferensi, I_SMS_Ireferensi); return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "setText") || Amagama_I_SMS(igama_okungaguquki, "setTitle")) { int I_SMS_Ireferensi = 빼기(2), into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi) && Amagama_I_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(into_Ireferensi, I_SMS_Ireferensi); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "getText") || Amagama_I_SMS(igama_okungaguquki, "getTitle")) { int into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi) && Amagama_I_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(into_Ireferensi), 2); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "addActionListener") && Amagama_I_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi)) { 힙[into_Ireferensi + 4] = 수신참조; 힙참조[into_Ireferensi + 4] = 1; } return; }
        if (Amagama_I_SMS(igama_okungaguquki, "getContentPane") && Amagama_I_SMS(서술상수, "()Ljava/awt/Container;")) { int into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi)) 넣기(into_Ireferensi, 2); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "setLayout") && Amagama_I_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int I_layout_Ireferensi = 빼기(2), into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi) && I_layout_Ireferensi != 0) ukwehluleka_inani("only absolute layout (null) is supported"); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "add") && (Amagama_I_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Amagama_I_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean I_layout_isimo = Amagama_I_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (I_layout_isimo) 빼기(2);
            int ingane_Ireferensi = 빼기(2), into_Ireferensi = 빼기(2); if (!화면객체(ingane_Ireferensi) || !화면객체(into_Ireferensi)) return;
            if (umsebenzisi.화면연결(2, 힙[into_Ireferensi + 2], 힙[ingane_Ireferensi + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[ingane_Ireferensi + 11] = into_Ireferensi; 힙참조[ingane_Ireferensi + 11] = 1; if (!I_layout_isimo) 넣기(ingane_Ireferensi, 2); return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "setBounds") && Amagama_I_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), okuxhumanisa_u_x = 빼기(1), into_Ireferensi = 빼기(2); if (!화면객체(into_Ireferensi)) return;
            if (umsebenzisi.화면연결(1, 힙[into_Ireferensi + 2], okuxhumanisa_u_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[into_Ireferensi + 5] = okuxhumanisa_u_x; 힙[into_Ireferensi + 6] = 세로좌표; 힙[into_Ireferensi + 7] = 너비; 힙[into_Ireferensi + 8] = 높이; return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "setSize") && Amagama_I_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), into_Ireferensi = 빼기(2); if (!화면객체(into_Ireferensi)) return;
            if (umsebenzisi.화면연결(1, 힙[into_Ireferensi + 2], 힙[into_Ireferensi + 5], 힙[into_Ireferensi + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[into_Ireferensi + 7] = 너비; 힙[into_Ireferensi + 8] = 높이; } return;
        }
        if (Amagama_I_SMS(igama_okungaguquki, "setLocationRelativeTo") && Amagama_I_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), into_Ireferensi = 빼기(2); if (!화면객체(into_Ireferensi)) return; if (상대배치 != 0) { ukwehluleka_inani("only screen centering supported"); return; } 힙[into_Ireferensi + 5] = (umsebenzisi.화면너비() - 힙[into_Ireferensi + 7]) / 2; 힙[into_Ireferensi + 6] = (umsebenzisi.화면높이() - 힙[into_Ireferensi + 8]) / 2; umsebenzisi.화면연결(1, 힙[into_Ireferensi + 2], 힙[into_Ireferensi + 5], 힙[into_Ireferensi + 6], 힙[into_Ireferensi + 7], 힙[into_Ireferensi + 8]); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "setDefaultCloseOperation") && Amagama_I_SMS(서술상수, "(I)V")) { int inqubomgomo = 빼기(1), into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi)) { if (inqubomgomo < 0 || inqubomgomo > 3) 예외던짐(9, "close policy"); else { 힙[into_Ireferensi + 10] = inqubomgomo; umsebenzisi.화면연결(7, 힙[into_Ireferensi + 2], inqubomgomo, 0, 0, 0); } } return; }
        if (Amagama_I_SMS(igama_okungaguquki, "setVisible") && Amagama_I_SMS(서술상수, "(Z)V")) { int imininingwane_inani = 빼기(1), into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi)) { int 처리값 = umsebenzisi.화면연결(3, 힙[into_Ireferensi + 2], imininingwane_inani, 0, 0, 0); if (처리값 < 0) ukwehluleka_inani("Swing requires a standalone interactive command"); else 힙[into_Ireferensi + 9] = imininingwane_inani; } return; }
        if (Amagama_I_SMS(igama_okungaguquki, "dispose") && Amagama_I_SMS(서술상수, "()V")) { int into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi)) { umsebenzisi.화면연결(4, 힙[into_Ireferensi + 2], 0, 0, 0, 0); 힙[into_Ireferensi + 9] = 0; } return; }
        if (Amagama_I_SMS(igama_okungaguquki, "repaint") || Amagama_I_SMS(igama_okungaguquki, "validate")) { int into_Ireferensi = 빼기(2); if (!화면객체(into_Ireferensi) || !Amagama_I_SMS(서술상수, "()V")) return; umsebenzisi.화면연결(1, 힙[into_Ireferensi + 2], 힙[into_Ireferensi + 5], 힙[into_Ireferensi + 6], 힙[into_Ireferensi + 7], 힙[into_Ireferensi + 8]); return; }
        if (Amagama_I_SMS(igama_okungaguquki, "isVisible") && Amagama_I_SMS(서술상수, "()Z")) { int into_Ireferensi = 빼기(2); if (화면객체(into_Ireferensi)) 넣기(힙[into_Ireferensi + 9], 1); return; }
        ukwehluleka_inani("unsupported Swing method (native subset)");
    }
    static void 사건실행(int impokophelo_ikheli, int 사건번호, boolean Isi_Zulu) {
        if (impokophelo_ikheli < 1 || 힙[impokophelo_ikheli] < 32) { ukwehluleka_inani("Java event listener required"); return; }
        int ifayela_thola_inkomba = igama_indlela(힙[impokophelo_ikheli] - 32, 사건번호 == 0 ? (Isi_Zulu ? "yenza_umsebenzi" : "run") : (Isi_Zulu ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Isi_Zulu ? "(LIsi_Zulu/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (ifayela_thola_inkomba < 0) { ukwehluleka_inani("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; uhlaka_thola_inkomba = 0; uhlu_lwemilayezo_isimo[0] = 1; uhlaka_Isitaki[0] = 0; 틀잠금[0] = qalisa_uhlaka[0] = 0; 바꿈요청 = false;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 128; iluphu_thola_inkomba++) { endaweni_inani[iluphu_thola_inkomba] = endaweni_thayipha[iluphu_thola_inkomba] = 0; }
        uhlaka_indlela[0] = ifayela_thola_inkomba; 틀위치[0] = indlela_qala[ifayela_thola_inkomba]; endaweni_inani[0] = impokophelo_ikheli; endaweni_thayipha[0] = 2;
        if (사건번호 != 0) { endaweni_inani[1] = 사건번호; endaweni_thayipha[1] = 2; }
        사건중 = true; yenza_umyalo(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Iphutha) {
            if (나중수 > 0) { int impokophelo_ikheli = 나중실행[0], Isi_Zulu = 나중한국어[0]; for (int iluphu_thola_inkomba = 1; iluphu_thola_inkomba < 나중수; iluphu_thola_inkomba++) { 나중실행[iluphu_thola_inkomba - 1] = 나중실행[iluphu_thola_inkomba]; 나중한국어[iluphu_thola_inkomba - 1] = 나중한국어[iluphu_thola_inkomba]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(impokophelo_ikheli, 0, Isi_Zulu != 0); continue; }
            if (umsebenzisi.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = umsebenzisi.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { ukwehluleka_inani("GUI event I/O failed"); return; }
            int ubutho_inani = 사건번호 & 65535; if (ubutho_inani < 1 || ubutho_inani > 32) continue; int into_Ireferensi = 화면참조[ubutho_inani - 1]; if (into_Ireferensi == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[into_Ireferensi + 10] != 0) 힙[into_Ireferensi + 9] = 0;
                if (힙[into_Ireferensi + 10] == 3) for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 32; iluphu_thola_inkomba++) if (화면참조[iluphu_thola_inkomba] != 0 && 힙[화면참조[iluphu_thola_inkomba]] == 24) umsebenzisi.화면연결(4, iluphu_thola_inkomba + 1, 0, 0, 0, 0);
            } else if (힙[into_Ireferensi + 4] != 0) {
                int NGIFUNDE_Ireferensi = abela_Indawo_yokugcina(29, 2); if (Iphutha) return; 힙[NGIFUNDE_Ireferensi + 2] = into_Ireferensi; 힙[NGIFUNDE_Ireferensi + 3] = 힙[into_Ireferensi + 12]; 힙참조[NGIFUNDE_Ireferensi + 2] = 1; 사건실행(힙[into_Ireferensi + 4], NGIFUNDE_Ireferensi, 힙[into_Ireferensi + 12] != 0);
            }
        }
    }
    public static int Sebenzisa() {
        if (umsebenzisi.인수개수() == 1 && 자바도구.같음(umsebenzisi.인수(0), "-version")) {
            umsebenzisi.Bhala("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (umsebenzisi.인수개수() < 1) { umsebenzisi.Bhala("Usage: java CLASS [ARGS]\n"); return 2; }
        okufakwayo_uhlobo_Incazelo = faka_uhlobo_Incazelo(singatha_uhlamvusimo(umsebenzisi.인수(0))); if (Iphutha || okufakwayo_uhlobo_Incazelo < 0) return 1;
        int okufakwayo_iphoyinti_inani = igama_indlela(okufakwayo_uhlobo_Incazelo, "Sebenzisa", "()V");
        boolean 한국어진입 = okufakwayo_iphoyinti_inani >= 0 && (indlela_ungeno[okufakwayo_iphoyinti_inani] & 9) == 9;
        if (!한국어진입) okufakwayo_iphoyinti_inani = igama_indlela(okufakwayo_uhlobo_Incazelo, "main", "([Ljava/lang/String;)V");
        if (okufakwayo_iphoyinti_inani < 0 || (indlela_ungeno[okufakwayo_iphoyinti_inani] & 9) != 9) ukwehluleka_inani("public static void Sebenzisa() or main(String[] args) required");
        if (Iphutha) return 1;
        int 인수 = abela_Indawo_yokugcina(3, umsebenzisi.인수개수() - 1); AMALUNGU_AFANAYO_ilungu[인수] = -1;
        for (int 수 = 1; 수 < umsebenzisi.인수개수() && !Iphutha; 수++) 힙[인수 + 1 + 수] = singatha_uhlamvusimo(umsebenzisi.인수(수));
        uhlaka_thola_inkomba = 0; uhlaka_indlela[0] = okufakwayo_iphoyinti_inani; 틀위치[0] = indlela_qala[okufakwayo_iphoyinti_inani]; endaweni_inani[0] = 한국어진입 ? 0 : 인수; endaweni_thayipha[0] = 한국어진입 ? 0 : 2;
        uhlu_lwemilayezo_isimo[0] = 1; uhlu_lwemilayezo_into[0] = abela_Indawo_yokugcina(13, 2);
        yenza_umyalo(); if (!Iphutha) 화면사건들(); return Iphutha ? 1 : 0;
    }
}
