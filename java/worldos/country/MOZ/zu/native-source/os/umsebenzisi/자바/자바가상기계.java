// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Ihele/스택/Ireferensi/igatsha 경계를 yenza_umyalo 중 검사한다. */
public final class 자바가상기계 {
    static int[] Ihele = new int[16384], ifayela_igama_I_SMS = new int[64];
    static int[] okungaguquki_ithegi = new int[512], 상가 = new int[512], 상나 = new int[512], uchunge_Ireferensi = new int[512];
    static int[] indlela_igama_I_SMS = new int[32], indlela_thayipha = new int[32], indlela_ungeno = new int[32];
    static int[] indlela_qala = new int[32], indlela_yekisa = new int[32], indlela_Isitaki = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], indlela_i_agumenti_thayipha = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] endaweni_inani = new int[4096], endaweni_thayipha = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] uhlaka_indlela = new int[32], 틀위치 = new int[32], uhlaka_Isitaki = new int[32];
    static int[] 힙 = new int[8192];
    static int Ubungako, 읽기위치, 상수수, 함수수, uhlobo_igama, uhlaka_thola_inkomba = -1, 힙끝 = 1, 반환형;
    static boolean Iphutha;

    static void ukwehluleka_inani(String Amagama_I_SMS) {
        if (!Iphutha) { umsebenzisi.Bhala("JVM error: "); umsebenzisi.Bhala(Amagama_I_SMS); umsebenzisi.bhala_uhlamvusimo_inani(10); }
        Iphutha = true;
    }
    static boolean isiqeshana(int Sebenzisa, int ubude_inani) { return Sebenzisa >= 0 && ubude_inani >= 0 && Sebenzisa <= Ubungako - ubude_inani; }
    static int ibhayithi_inani() {
        if (!isiqeshana(읽기위치, 1)) { ukwehluleka_inani("truncated class file"); return 0; }
        return Ihele[읽기위치++];
    }
    static int 짧은수() { return ibhayithi_inani() << 8 | ibhayithi_inani(); }
    static int inamba() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int ubude_inani) { if (!isiqeshana(읽기위치, ubude_inani)) ukwehluleka_inani("invalid attribute size"); else 읽기위치 += ubude_inani; }
    static boolean hlola_okungaguquki(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || okungaguquki_ithegi[수] != 종류) { ukwehluleka_inani("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Sebenzisa, int ubude_inani, String Amagama_I_SMS) {
        if (!isiqeshana(Sebenzisa, ubude_inani) || ubude_inani != Amagama_I_SMS.length()) return false;
        for (int 수 = 0; 수 < ubude_inani; 수++) if (Ihele[Sebenzisa + 수] != Amagama_I_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Iphutha; 수++) { hlola_okungaguquki(짧은수(), 1); 건너(inamba()); }
    }
    static int umyalo_ubude(int inani) {
        if (inani == 16 || inani == 18 || inani == 21 || inani == 25 || inani == 54 || inani == 58 || inani == 188) return 2;
        if (inani == 17 || inani == 19 || inani == 132 || inani >= 153 && inani <= 167
            || inani >= 178 && inani <= 184 || inani == 187 || inani == 189 || inani == 192 || inani == 198 || inani == 199) return 3;
        if (inani >= 0 && inani <= 8 || inani >= 26 && inani <= 29 || inani >= 42 && inani <= 46 || inani == 50
            || inani >= 59 && inani <= 62 || inani >= 75 && inani <= 79 || inani == 83 || inani == 87 || inani == 89 || inani == 95
            || inani == 96 || inani == 100 || inani == 104 || inani == 108 || inani == 112 || inani == 116
            || inani == 120 || inani == 122 || inani == 124 || inani == 126 || inani == 128 || inani == 130
            || inani >= 145 && inani <= 147 || inani == 172 || inani == 176 || inani == 177 || inani == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (inamba() != 0xcafebabe) ukwehluleka_inani("not a class file");
        int 부판 = 짧은수(), isibuyekezo_inani = 짧은수();
        if (isibuyekezo_inani < 45 || isibuyekezo_inani > 52 || 부판 != 0) ukwehluleka_inani("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { ukwehluleka_inani("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !Iphutha; 수++) {
            int 종류 = ibhayithi_inani(); okungaguquki_ithegi[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = inamba();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else ukwehluleka_inani("unsupported constant type");
        }
        int imvume_inani = 짧은수();
        if ((imvume_inani & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) ukwehluleka_inani("unsupported class flags");
        uhlobo_igama = uhlobo_igama_I_SMS(짧은수());
        if (!Amagama_I_SMS(uhlobo_igama_I_SMS(짧은수()), "java/lang/Object")) ukwehluleka_inani("inheritance unsupported");
        if (짧은수() != 0) ukwehluleka_inani("interfaces unsupported");
        if (짧은수() != 0) ukwehluleka_inani("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { ukwehluleka_inani("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !Iphutha; 수++) {
            indlela_ungeno[수] = 짧은수(); indlela_igama_I_SMS[수] = 짧은수(); indlela_thayipha[수] = 짧은수();
            hlola_okungaguquki(indlela_igama_I_SMS[수], 1); 서술읽기(수);
            if ((indlela_ungeno[수] & (0x100 | 0x400 | 0x20)) != 0) ukwehluleka_inani("native, abstract and synchronized methods unsupported");
            if ((indlela_ungeno[수] & 8) == 0 && !Amagama_I_SMS(indlela_igama_I_SMS[수], "<init>")) ukwehluleka_inani("instance methods unsupported");
            if (Amagama_I_SMS(indlela_igama_I_SMS[수], "<clinit>")) ukwehluleka_inani("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(indlela_igama_I_SMS[앞], indlela_igama_I_SMS[수]) && 같은말(indlela_thayipha[앞], indlela_thayipha[수])) ukwehluleka_inani("duplicate method");
            int 개수 = 짧은수();
            for (int isibaluli_inani = 0; isibaluli_inani < 개수 && !Iphutha; isibaluli_inani++) {
                int Igama = 짧은수(), ubude_inani = inamba(), Sebenzisa = 읽기위치;
                if (!isiqeshana(Sebenzisa, ubude_inani)) { ukwehluleka_inani("truncated method attribute"); break; }
                if (Amagama_I_SMS(Igama, "Code")) {
                    if (indlela_qala[수] != 0) ukwehluleka_inani("duplicate Code attribute");
                    indlela_Isitaki[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = inamba();
                    if (indlela_Isitaki[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ukwehluleka_inani("method memory limits exceeded");
                    indlela_qala[수] = 읽기위치; 건너(코드길이); indlela_yekisa[수] = 읽기위치;
                    if (짧은수() != 0) ukwehluleka_inani("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Sebenzisa + ubude_inani) ukwehluleka_inani("Code attribute size mismatch");
                } else 건너(ubude_inani);
            }
            if (indlela_qala[수] == 0) ukwehluleka_inani("missing Code attribute");
            int isikhala_okufakwayo = indlela_qala[수];
            while (isikhala_okufakwayo < indlela_yekisa[수] && !Iphutha) {
                int ubude_inani = umyalo_ubude(Ihele[isikhala_okufakwayo]);
                if (ubude_inani == 0 || ubude_inani > indlela_yekisa[수] - isikhala_okufakwayo) { ukwehluleka_inani("unsupported or truncated bytecode"); break; }
                경계[isikhala_okufakwayo] = 수 + 1; isikhala_okufakwayo += ubude_inani;
            }
            // 실행하지 않는 경로에도 잘못된 igatsha 목적지를 허용하지 않는다.
            isikhala_okufakwayo = indlela_qala[수];
            while (isikhala_okufakwayo < indlela_yekisa[수] && !Iphutha) {
                int inani = Ihele[isikhala_okufakwayo];
                if (inani >= 153 && inani <= 167 || inani == 198 || inani == 199) {
                    int isikhumulo_inani = isikhala_okufakwayo + (short)(Ihele[isikhala_okufakwayo + 1] << 8 | Ihele[isikhala_okufakwayo + 2]);
                    if (isikhumulo_inani < indlela_qala[수] || isikhumulo_inani >= indlela_yekisa[수] || 경계[isikhumulo_inani] != 수 + 1) ukwehluleka_inani("invalid branch target");
                }
                isikhala_okufakwayo += umyalo_ubude(inani);
            }
        }
        if (!Iphutha) 속성건너();
        if (읽기위치 != Ubungako) ukwehluleka_inani("extra class file data");
    }
    static int abela_Indawo_yokugcina(int 종류, int ubude_inani) {
        if (ubude_inani < 0 || ubude_inani > 힙.length - 힙끝 - 2) { ukwehluleka_inani("object heap exhausted or negative array size"); return 0; }
        int Ireferensi = 힙끝; 힙끝 += ubude_inani + 2; 힙[Ireferensi] = 종류; 힙[Ireferensi + 1] = ubude_inani;
        return Ireferensi;
    }
    static boolean into_inani(int Ireferensi, int 종류) {
        if (Ireferensi < 1 || Ireferensi >= 힙끝 - 1 || 힙[Ireferensi] != 종류) { ukwehluleka_inani("null or invalid object reference"); return false; }
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
        if (uhlaka_thola_inkomba == 31) { ukwehluleka_inani("call stack limit (32)"); return; }
        int 다음 = uhlaka_thola_inkomba + 1;
        for (int 수 = 0; 수 < 128; 수++) endaweni_thayipha[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[umsebenzi_inani] - 1; 수 >= 0; 수--) {
            endaweni_inani[다음 * 128 + 수] = 빼기(indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 수]); endaweni_thayipha[다음 * 128 + 수] = indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 수];
        }
        uhlaka_thola_inkomba = 다음; uhlaka_indlela[uhlaka_thola_inkomba] = umsebenzi_inani; 틀위치[uhlaka_thola_inkomba] = indlela_qala[umsebenzi_inani]; uhlaka_Isitaki[uhlaka_thola_inkomba] = 0;
    }
    static void 반환(int thayipha_inani) {
        if (thayipha_inani != 함수반환[uhlaka_indlela[uhlaka_thola_inkomba]]) { ukwehluleka_inani("return type mismatch"); return; }
        int inani = thayipha_inani == 0 ? 0 : 빼기(thayipha_inani);
        uhlaka_thola_inkomba--; if (uhlaka_thola_inkomba >= 0 && thayipha_inani != 0) 넣기(inani, thayipha_inani);
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
                if (inani < 1 || inani > 127) { ukwehluleka_inani("file stream paths currently require ASCII"); return; }
                Stream_ifayela_igama[isikhala_okufakwayo] = inani;
            }
            Stream_ifayela_igama[ubude_inani] = 0;
            int 서술자 = umsebenzisi.파일서술자열기(Stream_ifayela_igama, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ukwehluleka_inani("FileNotFoundException: file open failed"); return; }
            힙[Stream_inani + 2] = 서술자; 힙[Stream_inani + 3] = 1;
            return;
        }
        if (Umlayelo != 182) { ukwehluleka_inani("invalid file stream invocation"); return; }
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
            if (결과 < -1) ukwehluleka_inani("IOException: read failed"); else 넣기(결과, 1);
        } else if (umsebenzisi.파일한바이트쓰기(서술자, inani) != 1) ukwehluleka_inani("IOException: write failed");
    }
    static void fonela_indlela(int thola_inkomba, int Umlayelo) {
        if (!hlola_okungaguquki(thola_inkomba, 10)) return;
        int umnikazi_inani = uhlobo_igama_I_SMS(상가[thola_inkomba]), Igama = Ireferensi_igama(상나[thola_inkomba]), misa_inani = Ireferensi_thayipha(상나[thola_inkomba]);
        if (Iphutha) return;
        if (같은말(umnikazi_inani, uhlobo_igama)) {
            if (Umlayelo != 184) { ukwehluleka_inani("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Igama, indlela_igama_I_SMS[수]) && 같은말(misa_inani, indlela_thayipha[수])) {
                if ((indlela_ungeno[수] & 8) == 0) ukwehluleka_inani("method is not static"); else 호출(수);
                return;
            }
            ukwehluleka_inani("NoSuchMethodError"); return;
        }
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
        ukwehluleka_inani("unsupported library method");
    }
    static int AMALUNGU_AFANAYO_isikhala(int Ireferensi, int umbhalo_ongezansi_inani, int thayipha_inani) {
        if (!into_inani(Ireferensi, thayipha_inani)) return 0;
        if (umbhalo_ongezansi_inani < 0 || umbhalo_ongezansi_inani >= 힙[Ireferensi + 1]) { ukwehluleka_inani("ArrayIndexOutOfBoundsException"); return 0; }
        return Ireferensi + 2 + umbhalo_ongezansi_inani;
    }
    static void yenza_umyalo() {
        int 남음 = 500000;
        while (uhlaka_thola_inkomba >= 0 && !Iphutha) {
            if (--남음 == 0) { ukwehluleka_inani("instruction limit (500000)"); break; }
            int Sebenzisa = 틀위치[uhlaka_thola_inkomba], inani = 명바();
            if (Iphutha) break;
            if (inani == 0) continue;
            if (inani == 1) { 넣기(0, 2); continue; }
            if (inani >= 2 && inani <= 8) { 넣기(inani - 3, 1); continue; }
            if (inani == 16) { 넣기((byte)명바(), 1); continue; }
            if (inani == 17) { 넣기((short)명짧(), 1); continue; }
            if (inani == 18 || inani == 19) {
                int 수 = inani == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) ukwehluleka_inani("invalid ldc constant");
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
            if (inani == 46 || inani == 50) {
                int umbhalo_ongezansi_inani = 빼기(1), Ireferensi = 빼기(2), isikhala_okufakwayo = AMALUNGU_AFANAYO_isikhala(Ireferensi, umbhalo_ongezansi_inani, inani == 46 ? 2 : 3);
                if (!Iphutha) 넣기(힙[isikhala_okufakwayo], inani == 46 ? 1 : 2); continue;
            }
            if (inani == 79 || inani == 83) {
                int utho_ilungu = 빼기(inani == 79 ? 1 : 2), umbhalo_ongezansi_inani = 빼기(1), Ireferensi = 빼기(2), isikhala_okufakwayo = AMALUNGU_AFANAYO_isikhala(Ireferensi, umbhalo_ongezansi_inani, inani == 79 ? 2 : 3);
                if (inani == 83 && utho_ilungu != 0) into_inani(utho_ilungu, 1);
                if (!Iphutha) 힙[isikhala_okufakwayo] = utho_ilungu; continue;
            }
            if (inani == 87) { 빼기(0); continue; }
            if (inani == 89) { int 가 = 빼기(0), thayipha_inani = 반환형; 넣기(가, thayipha_inani); 넣기(가, thayipha_inani); continue; }
            if (inani == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (inani == 178) {
                int 수 = 명짧(); if (!hlola_okungaguquki(수, 9)) continue;
                if (!Amagama_I_SMS(uhlobo_igama_I_SMS(상가[수]), "java/lang/System") || !Amagama_I_SMS(Ireferensi_igama(상나[수]), "out")
                    || !Amagama_I_SMS(Ireferensi_thayipha(상나[수]), "Ljava/io/PrintStream;")) ukwehluleka_inani("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (inani == 182 || inani == 183 || inani == 184) { fonela_indlela(명짧(), inani); continue; }
            if (inani == 187) {
                int Igama = uhlobo_igama_I_SMS(명짧());
                if (Amagama_I_SMS(Igama, "java/lang/StringBuilder")) 넣기(abela_Indawo_yokugcina(4, 1), 2);
                else if (Amagama_I_SMS(Igama, "java/io/FileInputStream") || Amagama_I_SMS(Igama, "java/io/FileOutputStream")) {
                    int Ireferensi = abela_Indawo_yokugcina(Amagama_I_SMS(Igama, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Iphutha) { 힙[Ireferensi + 2] = -1; 넣기(Ireferensi, 2); }
                } else ukwehluleka_inani("unsupported object construction");
                continue;
            }
            if (inani == 188 || inani == 189) {
                if (inani == 188) { if (명바() != 10) ukwehluleka_inani("only int[] newarray is supported"); }
                else if (!Amagama_I_SMS(uhlobo_igama_I_SMS(명짧()), "java/lang/String")) ukwehluleka_inani("only String[] anewarray is supported");
                int ubude_inani = 빼기(1); 넣기(abela_Indawo_yokugcina(inani == 188 ? 2 : 3, ubude_inani), 2); continue;
            }
            if (inani == 190) {
                int Ireferensi = 빼기(2);
                if (Ireferensi < 1 || Ireferensi >= 힙끝 - 1 || (힙[Ireferensi] != 2 && 힙[Ireferensi] != 3)) ukwehluleka_inani("null or invalid array");
                else 넣기(힙[Ireferensi + 1], 1); continue;
            }
            if (inani == 192) {
                int Igama = uhlobo_igama_I_SMS(명짧()), Ireferensi = 빼기(2);
                if (!Amagama_I_SMS(Igama, "java/lang/String")) ukwehluleka_inani("unsupported checkcast");
                else if (Ireferensi != 0) into_inani(Ireferensi, 1);
                넣기(Ireferensi, 2); continue;
            }
            ukwehluleka_inani("unsupported bytecode");
        }
    }
    public static int Sebenzisa() {
        if (umsebenzisi.인수개수() == 1 && 자바도구.같음(umsebenzisi.인수(0), "-version")) {
            umsebenzisi.Bhala("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (umsebenzisi.인수개수() < 1) { umsebenzisi.Bhala("Usage: java CLASS [ARGS]\n"); return 2; }
        int ubude_inani = 자바도구.Igama(ifayela_igama_I_SMS, umsebenzisi.인수(0));
        if (ubude_inani < 1 || ubude_inani > 57) { umsebenzisi.Bhala("java: invalid class name\n"); return 2; }
        ifayela_igama_I_SMS[ubude_inani] = '.'; ifayela_igama_I_SMS[ubude_inani + 1] = 'c'; ifayela_igama_I_SMS[ubude_inani + 2] = 'l'; ifayela_igama_I_SMS[ubude_inani + 3] = 'a'; ifayela_igama_I_SMS[ubude_inani + 4] = 's'; ifayela_igama_I_SMS[ubude_inani + 5] = 's';
        Ubungako = umsebenzisi.파일읽기(ifayela_igama_I_SMS, Ihele);
        if (Ubungako < 0) { umsebenzisi.Bhala("java: cannot read class: "); 자바도구.수쓰기(Ubungako); umsebenzisi.bhala_uhlamvusimo_inani(10); return 1; }
        클래스읽기(); if (Iphutha) return 1;
        int uhlamvusimo_igama = okungaguquki_I_SMS(uhlobo_igama);
        if (!Iphutha && 힙[uhlamvusimo_igama + 1] != ubude_inani) ukwehluleka_inani("class name does not match file");
        for (int 수 = 0; 수 < ubude_inani && !Iphutha; 수++) if (힙[uhlamvusimo_igama + 2 + 수] != ifayela_igama_I_SMS[수]) ukwehluleka_inani("class name does not match file");
        int okufakwayo_iphoyinti_inani = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Amagama_I_SMS(indlela_igama_I_SMS[수], "main") && Amagama_I_SMS(indlela_thayipha[수], "([Ljava/lang/String;)V") && (indlela_ungeno[수] & 9) == 9) okufakwayo_iphoyinti_inani = 수;
        if (okufakwayo_iphoyinti_inani < 0) ukwehluleka_inani("public static void main(String[] args) required");
        if (Iphutha) return 1;
        int 인수 = abela_Indawo_yokugcina(3, umsebenzisi.인수개수() - 1);
        for (int 수 = 1; 수 < umsebenzisi.인수개수() && !Iphutha; 수++) 힙[인수 + 1 + 수] = singatha_uhlamvusimo(umsebenzisi.인수(수));
        uhlaka_thola_inkomba = 0; uhlaka_indlela[0] = okufakwayo_iphoyinti_inani; 틀위치[0] = indlela_qala[okufakwayo_iphoyinti_inani]; endaweni_inani[0] = 인수; endaweni_thayipha[0] = 2;
        yenza_umyalo(); return Iphutha ? 1 : 0;
    }
}
