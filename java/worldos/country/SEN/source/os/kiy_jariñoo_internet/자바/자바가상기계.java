// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. bara_denc/스택/Royukaay/car 경계를 def_ndigel 중 검사한다. */
public final class 자바가상기계 {
    static int[] bara_denc = new int[16384], bara_denc_tur_SMS = new int[64];
    static int[] Lees_dul_soppi_xàmme = new int[512], 상가 = new int[512], 상나 = new int[512], araf_yu_bennoo_Royukaay = new int[512];
    static int[] doxalin_tur_SMS = new int[32], doxalin_xeet = new int[32], doxalin_jot = new int[32];
    static int[] doxalin_Door = new int[32], doxalin_jeexal = new int[32], doxalin_Tegalo = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], doxalin_Tegtal_xeet = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] dënnd_xëyma = new int[4096], dënnd_xeet = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] kadar_doxalin = new int[32], 틀위치 = new int[32], kadar_Tegalo = new int[32];
    static int[] 힙 = new int[8192];
    static int tolluwaay, 읽기위치, 상수수, 함수수, maas_tur, kadar_àlluwa_tur = -1, 힙끝 = 1, 반환형;
    static boolean njumte;

    static void foo_xëyma(String Word_SMS) {
        if (!njumte) { kiy_jariñoo_internet.biir("JVM error: "); kiy_jariñoo_internet.biir(Word_SMS); kiy_jariñoo_internet.biir_Araf_xëyma(10); }
        njumte = true;
    }
    static boolean kilip(int daw, int diir_xëyma) { return daw >= 0 && diir_xëyma >= 0 && daw <= tolluwaay - diir_xëyma; }
    static int okte_xëyma() {
        if (!kilip(읽기위치, 1)) { foo_xëyma("truncated class file"); return 0; }
        return bara_denc[읽기위치++];
    }
    static int 짧은수() { return okte_xëyma() << 8 | okte_xëyma(); }
    static int lëmm() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int diir_xëyma) { if (!kilip(읽기위치, diir_xëyma)) foo_xëyma("invalid attribute size"); else 읽기위치 += diir_xëyma; }
    static boolean sek_Lees_dul_soppi(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || Lees_dul_soppi_xàmme[수] != 종류) { foo_xëyma("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int daw, int diir_xëyma, String Word_SMS) {
        if (!kilip(daw, diir_xëyma) || diir_xëyma != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < diir_xëyma; 수++) if (bara_denc[daw + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int Lees_dul_soppi_xëyma, String Word_SMS) { return sek_Lees_dul_soppi(Lees_dul_soppi_xëyma, 1) && 구간(상가[Lees_dul_soppi_xëyma], 상나[Lees_dul_soppi_xëyma], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!sek_Lees_dul_soppi(가, 1) || !sek_Lees_dul_soppi(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (bara_denc[상가[가] + 수] != bara_denc[상가[나] + 수]) return false;
        return true;
    }
    static int maas_tur_SMS(int 수) { return sek_Lees_dul_soppi(수, 7) && sek_Lees_dul_soppi(상가[수], 1) ? 상가[수] : 0; }
    static int Royukaay_tur(int 수) { return sek_Lees_dul_soppi(수, 12) && sek_Lees_dul_soppi(상가[수], 1) ? 상가[수] : 0; }
    static int Royukaay_xeet(int 수) { return sek_Lees_dul_soppi(수, 12) && sek_Lees_dul_soppi(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean neen_xeet) {
        if (읽기위치 >= 끝) { foo_xëyma("invalid descriptor"); return 0; }
        int xëyma = okte_xëyma();
        if (xëyma == 'V' && neen_xeet) return 0;
        if (xëyma == 'I' || xëyma == 'B' || xëyma == 'C' || xëyma == 'S' || xëyma == 'Z') return 1;
        if (xëyma == '[') { 서술형(끝, false); return 2; }
        if (xëyma == 'L') {
            int daw = 읽기위치;
            while (읽기위치 < 끝 && bara_denc[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == daw) foo_xëyma("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        foo_xëyma("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int liëey_xëyma) {
        int 이전 = 읽기위치, 수 = doxalin_xeet[liëey_xëyma];
        if (!sek_Lees_dul_soppi(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (okte_xëyma() != '(') foo_xëyma("invalid method descriptor");
        int 개수 = 0;
        while (!njumte && 읽기위치 < 끝 && bara_denc[읽기위치] != ')') {
            if (개수 == 16) { foo_xëyma("too many method arguments"); break; }
            doxalin_Tegtal_xeet[liëey_xëyma * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || okte_xëyma() != ')') foo_xëyma("invalid method descriptor");
        함수반환[liëey_xëyma] = 서술형(끝, true); 함수인수수[liëey_xëyma] = 개수;
        if (읽기위치 != 끝) foo_xëyma("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !njumte; 수++) { sek_Lees_dul_soppi(짧은수(), 1); 건너(lëmm()); }
    }
    static int ndigel_diir(int xëyma) {
        if (xëyma == 16 || xëyma == 18 || xëyma == 21 || xëyma == 25 || xëyma == 54 || xëyma == 58 || xëyma == 188) return 2;
        if (xëyma == 17 || xëyma == 19 || xëyma == 132 || xëyma >= 153 && xëyma <= 167
            || xëyma >= 178 && xëyma <= 184 || xëyma == 187 || xëyma == 189 || xëyma == 192 || xëyma == 198 || xëyma == 199) return 3;
        if (xëyma >= 0 && xëyma <= 8 || xëyma >= 26 && xëyma <= 29 || xëyma >= 42 && xëyma <= 46 || xëyma == 50
            || xëyma >= 59 && xëyma <= 62 || xëyma >= 75 && xëyma <= 79 || xëyma == 83 || xëyma == 87 || xëyma == 89 || xëyma == 95
            || xëyma == 96 || xëyma == 100 || xëyma == 104 || xëyma == 108 || xëyma == 112 || xëyma == 116
            || xëyma == 120 || xëyma == 122 || xëyma == 124 || xëyma == 126 || xëyma == 128 || xëyma == 130
            || xëyma >= 145 && xëyma <= 147 || xëyma == 172 || xëyma == 176 || xëyma == 177 || xëyma == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (lëmm() != 0xcafebabe) foo_xëyma("not a class file");
        int 부판 = 짧은수(), taalif_xëyma = 짧은수();
        if (taalif_xëyma < 45 || taalif_xëyma > 52 || 부판 != 0) foo_xëyma("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { foo_xëyma("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !njumte; 수++) {
            int 종류 = okte_xëyma(); Lees_dul_soppi_xàmme[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = lëmm();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else foo_xëyma("unsupported constant type");
        }
        int sañ_sañ_xëyma = 짧은수();
        if ((sañ_sañ_xëyma & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) foo_xëyma("unsupported class flags");
        maas_tur = maas_tur_SMS(짧은수());
        if (!Word_SMS(maas_tur_SMS(짧은수()), "java/lang/Object")) foo_xëyma("inheritance unsupported");
        if (짧은수() != 0) foo_xëyma("interfaces unsupported");
        if (짧은수() != 0) foo_xëyma("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { foo_xëyma("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !njumte; 수++) {
            doxalin_jot[수] = 짧은수(); doxalin_tur_SMS[수] = 짧은수(); doxalin_xeet[수] = 짧은수();
            sek_Lees_dul_soppi(doxalin_tur_SMS[수], 1); 서술읽기(수);
            if ((doxalin_jot[수] & (0x100 | 0x400 | 0x20)) != 0) foo_xëyma("native, abstract and synchronized methods unsupported");
            if ((doxalin_jot[수] & 8) == 0 && !Word_SMS(doxalin_tur_SMS[수], "<init>")) foo_xëyma("instance methods unsupported");
            if (Word_SMS(doxalin_tur_SMS[수], "<clinit>")) foo_xëyma("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(doxalin_tur_SMS[앞], doxalin_tur_SMS[수]) && 같은말(doxalin_xeet[앞], doxalin_xeet[수])) foo_xëyma("duplicate method");
            int 개수 = 짧은수();
            for (int jagle_xëyma = 0; jagle_xëyma < 개수 && !njumte; jagle_xëyma++) {
                int tur_253d1510 = 짧은수(), diir_xëyma = lëmm(), daw = 읽기위치;
                if (!kilip(daw, diir_xëyma)) { foo_xëyma("truncated method attribute"); break; }
                if (Word_SMS(tur_253d1510, "Code")) {
                    if (doxalin_Door[수] != 0) foo_xëyma("duplicate Code attribute");
                    doxalin_Tegalo[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = lëmm();
                    if (doxalin_Tegalo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) foo_xëyma("method memory limits exceeded");
                    doxalin_Door[수] = 읽기위치; 건너(코드길이); doxalin_jeexal[수] = 읽기위치;
                    if (짧은수() != 0) foo_xëyma("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != daw + diir_xëyma) foo_xëyma("Code attribute size mismatch");
                } else 건너(diir_xëyma);
            }
            if (doxalin_Door[수] == 0) foo_xëyma("missing Code attribute");
            int xar_xar_dugal_xabaar = doxalin_Door[수];
            while (xar_xar_dugal_xabaar < doxalin_jeexal[수] && !njumte) {
                int diir_xëyma = ndigel_diir(bara_denc[xar_xar_dugal_xabaar]);
                if (diir_xëyma == 0 || diir_xëyma > doxalin_jeexal[수] - xar_xar_dugal_xabaar) { foo_xëyma("unsupported or truncated bytecode"); break; }
                경계[xar_xar_dugal_xabaar] = 수 + 1; xar_xar_dugal_xabaar += diir_xëyma;
            }
            // 실행하지 않는 경로에도 잘못된 car 목적지를 허용하지 않는다.
            xar_xar_dugal_xabaar = doxalin_Door[수];
            while (xar_xar_dugal_xabaar < doxalin_jeexal[수] && !njumte) {
                int xëyma = bara_denc[xar_xar_dugal_xabaar];
                if (xëyma >= 153 && xëyma <= 167 || xëyma == 198 || xëyma == 199) {
                    int jëmmukaay_xëyma = xar_xar_dugal_xabaar + (short)(bara_denc[xar_xar_dugal_xabaar + 1] << 8 | bara_denc[xar_xar_dugal_xabaar + 2]);
                    if (jëmmukaay_xëyma < doxalin_Door[수] || jëmmukaay_xëyma >= doxalin_jeexal[수] || 경계[jëmmukaay_xëyma] != 수 + 1) foo_xëyma("invalid branch target");
                }
                xar_xar_dugal_xabaar += ndigel_diir(xëyma);
            }
        }
        if (!njumte) 속성건너();
        if (읽기위치 != tolluwaay) foo_xëyma("extra class file data");
    }
    static int jagleel_Dencukaay(int 종류, int diir_xëyma) {
        if (diir_xëyma < 0 || diir_xëyma > 힙.length - 힙끝 - 2) { foo_xëyma("object heap exhausted or negative array size"); return 0; }
        int Royukaay = 힙끝; 힙끝 += diir_xëyma + 2; 힙[Royukaay] = 종류; 힙[Royukaay + 1] = diir_xëyma;
        return Royukaay;
    }
    static boolean yëf_xëyma(int Royukaay, int 종류) {
        if (Royukaay < 1 || Royukaay >= 힙끝 - 1 || 힙[Royukaay] != 종류) { foo_xëyma("null or invalid object reference"); return false; }
        return true;
    }
    static int Lees_dul_soppi_SMS(int àlluwa_tur) {
        if (!sek_Lees_dul_soppi(àlluwa_tur, 1)) return 0;
        if (araf_yu_bennoo_Royukaay[àlluwa_tur] != 0) return araf_yu_bennoo_Royukaay[àlluwa_tur];
        int Royukaay = jagleel_Dencukaay(1, 상나[àlluwa_tur]); if (njumte) return 0;
        int 끝 = 상가[àlluwa_tur] + 상나[àlluwa_tur], 수 = 상가[àlluwa_tur], diir_xëyma = 0;
        while (수 < 끝 && !njumte) {
            int xëyma = bara_denc[수++];
            if (xëyma == 0) foo_xëyma("invalid modified UTF-8");
            else if (xëyma >= 192 && xëyma <= 223 && 수 < 끝) {
                int 다음 = bara_denc[수++];
                if ((다음 & 192) != 128) foo_xëyma("invalid modified UTF-8");
                xëyma = (xëyma & 31) << 6 | 다음 & 63;
                if (xëyma != 0 && xëyma < 128) foo_xëyma("overlong modified UTF-8");
            } else if (xëyma >= 224 && xëyma <= 239 && 수 + 1 < 끝) {
                int 가 = bara_denc[수++], 나 = bara_denc[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) foo_xëyma("invalid modified UTF-8");
                xëyma = (xëyma & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (xëyma < 2048) foo_xëyma("overlong modified UTF-8");
            } else if (xëyma >= 128) foo_xëyma("invalid modified UTF-8");
            힙[Royukaay + 2 + diir_xëyma++] = xëyma;
        }
        힙[Royukaay + 1] = diir_xëyma; araf_yu_bennoo_Royukaay[àlluwa_tur] = Royukaay; return Royukaay;
    }
    static int dalal_Araf(String xëyma) {
        int Royukaay = jagleel_Dencukaay(1, xëyma.length()); if (njumte) return 0;
        for (int 수 = 0; 수 < xëyma.length(); 수++) 힙[Royukaay + 2 + 수] = xëyma.charAt(수);
        return Royukaay;
    }
    static void biir_SMS(int Royukaay) {
        if (Royukaay == 0) { kiy_jariñoo_internet.biir("null"); return; }
        if (!yëf_xëyma(Royukaay, 1)) return;
        for (int 수 = 0; 수 < 힙[Royukaay + 1]; 수++) kiy_jariñoo_internet.biir_Araf_xëyma(힙[Royukaay + 2 + 수]);
    }
    static int siifar_Araf(int xëyma) {
        int Royukaay = jagleel_Dencukaay(1, 11); if (njumte) return 0;
        int diir_xëyma = 0;
        if (xëyma < 0) 힙[Royukaay + 2 + diir_xëyma++] = '-'; else xëyma = -xëyma;
        int 자리 = 1000000000; boolean daw = false;
        while (자리 != 0) {
            int 수 = -(xëyma / 자리);
            if (수 != 0 || daw || 자리 == 1) { 힙[Royukaay + 2 + diir_xëyma++] = '0' + 수; daw = true; }
            xëyma %= 자리; 자리 /= 10;
        }
        힙[Royukaay + 1] = diir_xëyma; return Royukaay;
    }
    static int 정수해독(int Royukaay) {
        if (!yëf_xëyma(Royukaay, 1)) return 0;
        int diir_xëyma = 힙[Royukaay + 1], 수 = 0, xëyma = 0; boolean 음수 = false;
        if (diir_xëyma > 0 && (힙[Royukaay + 2] == '-' || 힙[Royukaay + 2] == '+')) { 음수 = 힙[Royukaay + 2] == '-'; 수++; }
        if (수 == diir_xëyma) foo_xëyma("NumberFormatException");
        for (; 수 < diir_xëyma && !njumte; 수++) {
            int siifar_xëyma = 힙[Royukaay + 2 + 수] - '0';
            if (siifar_xëyma < 0 || siifar_xëyma > 9 || xëyma < -214748364 || xëyma == -214748364 && siifar_xëyma > (음수 ? 8 : 7)) foo_xëyma("NumberFormatException");
            xëyma = xëyma * 10 - siifar_xëyma;
        }
        return 음수 ? xëyma : -xëyma;
    }
    static void 넣기(int xëyma, int xeet_xëyma) {
        if (njumte) return;
        if (kadar_àlluwa_tur < 0 || kadar_Tegalo[kadar_àlluwa_tur] >= doxalin_Tegalo[kadar_doxalin[kadar_àlluwa_tur]]) { foo_xëyma("operand stack overflow"); return; }
        int xar_xar_dugal_xabaar = kadar_àlluwa_tur * 128 + kadar_Tegalo[kadar_àlluwa_tur]++; 스택값[xar_xar_dugal_xabaar] = xëyma; 스택형[xar_xar_dugal_xabaar] = xeet_xëyma;
    }
    static int 빼기(int xeet_xëyma) {
        if (njumte) return 0;
        if (kadar_àlluwa_tur < 0 || kadar_Tegalo[kadar_àlluwa_tur] < 1) { foo_xëyma("operand stack underflow"); return 0; }
        int xar_xar_dugal_xabaar = kadar_àlluwa_tur * 128 + --kadar_Tegalo[kadar_àlluwa_tur]; 반환형 = 스택형[xar_xar_dugal_xabaar];
        if (xeet_xëyma != 0 && 반환형 != xeet_xëyma) foo_xëyma("operand type mismatch");
        return 스택값[xar_xar_dugal_xabaar];
    }
    static void 지역읽기(int àlluwa_tur, int xeet_xëyma) {
        if (àlluwa_tur >= 함수지역[kadar_doxalin[kadar_àlluwa_tur]] || àlluwa_tur < 0 || dënnd_xeet[kadar_àlluwa_tur * 128 + àlluwa_tur] != xeet_xëyma) { foo_xëyma("invalid or uninitialized local"); return; }
        넣기(dënnd_xëyma[kadar_àlluwa_tur * 128 + àlluwa_tur], xeet_xëyma);
    }
    static void biir_dënnd(int àlluwa_tur, int xeet_xëyma) {
        if (àlluwa_tur >= 함수지역[kadar_doxalin[kadar_àlluwa_tur]] || àlluwa_tur < 0) { foo_xëyma("local index out of range"); return; }
        int xëyma = 빼기(xeet_xëyma); dënnd_xëyma[kadar_àlluwa_tur * 128 + àlluwa_tur] = xëyma; dënnd_xeet[kadar_àlluwa_tur * 128 + àlluwa_tur] = xeet_xëyma;
    }
    static int 명바() {
        int 위치 = 틀위치[kadar_àlluwa_tur];
        if (위치 < doxalin_Door[kadar_doxalin[kadar_àlluwa_tur]] || 위치 >= doxalin_jeexal[kadar_doxalin[kadar_àlluwa_tur]]) { foo_xëyma("instruction pointer out of range"); return 0; }
        틀위치[kadar_àlluwa_tur]++; return bara_denc[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void toxal_xëyma(int 위치) {
        int liëey_xëyma = kadar_doxalin[kadar_àlluwa_tur];
        if (위치 < doxalin_Door[liëey_xëyma] || 위치 >= doxalin_jeexal[liëey_xëyma] || 경계[위치] != liëey_xëyma + 1) foo_xëyma("invalid branch target");
        else 틀위치[kadar_àlluwa_tur] = 위치;
    }
    static void 호출(int liëey_xëyma) {
        if (kadar_àlluwa_tur == 31) { foo_xëyma("call stack limit (32)"); return; }
        int 다음 = kadar_àlluwa_tur + 1;
        for (int 수 = 0; 수 < 128; 수++) dënnd_xeet[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[liëey_xëyma] - 1; 수 >= 0; 수--) {
            dënnd_xëyma[다음 * 128 + 수] = 빼기(doxalin_Tegtal_xeet[liëey_xëyma * 16 + 수]); dënnd_xeet[다음 * 128 + 수] = doxalin_Tegtal_xeet[liëey_xëyma * 16 + 수];
        }
        kadar_àlluwa_tur = 다음; kadar_doxalin[kadar_àlluwa_tur] = liëey_xëyma; 틀위치[kadar_àlluwa_tur] = doxalin_Door[liëey_xëyma]; kadar_Tegalo[kadar_àlluwa_tur] = 0;
    }
    static void 반환(int xeet_xëyma) {
        if (xeet_xëyma != 함수반환[kadar_doxalin[kadar_àlluwa_tur]]) { foo_xëyma("return type mismatch"); return; }
        int xëyma = xeet_xëyma == 0 ? 0 : 빼기(xeet_xëyma);
        kadar_àlluwa_tur--; if (kadar_àlluwa_tur >= 0 && xeet_xëyma != 0) 넣기(xëyma, xeet_xëyma);
    }
    static int[] dawal_bara_denc_tur = new int[64];
    static void bara_denc_dawal_Wuute(int boroom_xëyma, int tur_253d1510, int dayo_xëyma, int ndigel) {
        boolean 출력 = Word_SMS(boroom_xëyma, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (ndigel == 183 && Word_SMS(tur_253d1510, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(dayo_xëyma, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(dayo_xëyma, "(Ljava/lang/String;)V")) { foo_xëyma("unsupported file stream constructor"); return; }
            int bara_denc_dugal_xabaar_tur = 빼기(2), dawal_xëyma = 빼기(2);
            if (!yëf_xëyma(bara_denc_dugal_xabaar_tur, 1) || !yëf_xëyma(dawal_xëyma, 종류) || njumte) return;
            if (힙[dawal_xëyma + 3] != 0) { foo_xëyma("file stream already initialized"); return; }
            int diir_xëyma = 힙[bara_denc_dugal_xabaar_tur + 1];
            if (diir_xëyma < 1 || diir_xëyma > 63) { foo_xëyma("invalid file name length"); return; }
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < diir_xëyma; xar_xar_dugal_xabaar++) {
                int xëyma = 힙[bara_denc_dugal_xabaar_tur + 2 + xar_xar_dugal_xabaar];
                if (xëyma < 1 || xëyma > 127) { foo_xëyma("file stream paths currently require ASCII"); return; }
                dawal_bara_denc_tur[xar_xar_dugal_xabaar] = xëyma;
            }
            dawal_bara_denc_tur[diir_xëyma] = 0;
            int 서술자 = kiy_jariñoo_internet.파일서술자열기(dawal_bara_denc_tur, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { foo_xëyma("FileNotFoundException: file open failed"); return; }
            힙[dawal_xëyma + 2] = 서술자; 힙[dawal_xëyma + 3] = 1;
            return;
        }
        if (ndigel != 182) { foo_xëyma("invalid file stream invocation"); return; }
        int jëf = -1, xëyma = 0;
        if (Word_SMS(tur_253d1510, "close") && Word_SMS(dayo_xëyma, "()V")) jëf = 0;
        if (!출력 && Word_SMS(tur_253d1510, "read") && Word_SMS(dayo_xëyma, "()I")) jëf = 1;
        if (출력 && Word_SMS(tur_253d1510, "write") && Word_SMS(dayo_xëyma, "(I)V")) { jëf = 2; xëyma = 빼기(1); }
        if (jëf < 0) { foo_xëyma("unsupported file stream method"); return; }
        int dawal_xëyma = 빼기(2);
        if (!yëf_xëyma(dawal_xëyma, 종류) || njumte) return;
        if (힙[dawal_xëyma + 3] == 0) { foo_xëyma("uninitialized file stream"); return; }
        int 서술자 = 힙[dawal_xëyma + 2];
        if (jëf == 0) {
            if (서술자 >= 0 && kiy_jariñoo_internet.파일서술자닫기(서술자) < 0) foo_xëyma("IOException: close failed");
            힙[dawal_xëyma + 2] = -1; return;
        }
        if (서술자 < 0) { foo_xëyma("IOException: stream closed"); return; }
        if (jëf == 1) {
            int 결과 = kiy_jariñoo_internet.파일한바이트읽기(서술자);
            if (결과 < -1) foo_xëyma("IOException: read failed"); else 넣기(결과, 1);
        } else if (kiy_jariñoo_internet.파일한바이트쓰기(서술자, xëyma) != 1) foo_xëyma("IOException: write failed");
    }
    static void Wuute_doxalin(int àlluwa_tur, int ndigel) {
        if (!sek_Lees_dul_soppi(àlluwa_tur, 10)) return;
        int boroom_xëyma = maas_tur_SMS(상가[àlluwa_tur]), tur_253d1510 = Royukaay_tur(상나[àlluwa_tur]), dayo_xëyma = Royukaay_xeet(상나[àlluwa_tur]);
        if (njumte) return;
        if (같은말(boroom_xëyma, maas_tur)) {
            if (ndigel != 184) { foo_xëyma("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(tur_253d1510, doxalin_tur_SMS[수]) && 같은말(dayo_xëyma, doxalin_xeet[수])) {
                if ((doxalin_jot[수] & 8) == 0) foo_xëyma("method is not static"); else 호출(수);
                return;
            }
            foo_xëyma("NoSuchMethodError"); return;
        }
        if (Word_SMS(boroom_xëyma, "java/io/FileInputStream") || Word_SMS(boroom_xëyma, "java/io/FileOutputStream")) {
            bara_denc_dawal_Wuute(boroom_xëyma, tur_253d1510, dayo_xëyma, ndigel); return;
        }
        if (ndigel == 184 && Word_SMS(boroom_xëyma, "java/lang/Integer") && Word_SMS(tur_253d1510, "parseInt") && Word_SMS(dayo_xëyma, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (ndigel == 182 && Word_SMS(boroom_xëyma, "java/io/PrintStream") && (Word_SMS(tur_253d1510, "println") || Word_SMS(tur_253d1510, "print"))) {
            int xeet_xëyma = 0, xëyma = 0;
            if (Word_SMS(dayo_xëyma, "(I)V")) { xeet_xëyma = 1; xëyma = 빼기(1); }
            else if (Word_SMS(dayo_xëyma, "(Z)V")) { xeet_xëyma = 2; xëyma = 빼기(1); }
            else if (Word_SMS(dayo_xëyma, "(C)V")) { xeet_xëyma = 3; xëyma = 빼기(1); }
            else if (Word_SMS(dayo_xëyma, "(Ljava/lang/String;)V")) { xeet_xëyma = 4; xëyma = 빼기(2); }
            else if (!Word_SMS(dayo_xëyma, "()V") || !Word_SMS(tur_253d1510, "println")) foo_xëyma("unsupported print descriptor");
            if (빼기(2) != -1) foo_xëyma("invalid PrintStream receiver");
            if (njumte) return;
            if (xeet_xëyma == 1) 자바도구.수쓰기(xëyma);
            if (xeet_xëyma == 2) kiy_jariñoo_internet.biir(xëyma == 0 ? "false" : "true");
            if (xeet_xëyma == 3) kiy_jariñoo_internet.biir_Araf_xëyma(xëyma & 65535);
            if (xeet_xëyma == 4) biir_SMS(xëyma);
            if (Word_SMS(tur_253d1510, "println")) kiy_jariñoo_internet.biir_Araf_xëyma(10);
            return;
        }
        if (ndigel == 182 && Word_SMS(boroom_xëyma, "java/lang/String")) {
            if (Word_SMS(tur_253d1510, "length") && Word_SMS(dayo_xëyma, "()I")) {
                int Royukaay = 빼기(2); if (yëf_xëyma(Royukaay, 1)) 넣기(힙[Royukaay + 1], 1); return;
            }
            if (Word_SMS(tur_253d1510, "charAt") && Word_SMS(dayo_xëyma, "(I)C")) {
                int dajale_xëyma = 빼기(1), Royukaay = 빼기(2);
                if (yëf_xëyma(Royukaay, 1)) {
                    if (dajale_xëyma < 0 || dajale_xëyma >= 힙[Royukaay + 1]) foo_xëyma("StringIndexOutOfBoundsException"); else 넣기(힙[Royukaay + 2 + dajale_xëyma], 1);
                }
                return;
            }
        }
        if (Word_SMS(boroom_xëyma, "java/lang/StringBuilder")) {
            if (ndigel == 183 && Word_SMS(tur_253d1510, "<init>") && Word_SMS(dayo_xëyma, "()V")) { yëf_xëyma(빼기(2), 4); return; }
            if (ndigel == 182 && Word_SMS(tur_253d1510, "toString") && Word_SMS(dayo_xëyma, "()Ljava/lang/String;")) {
                int Royukaay = 빼기(2); if (yëf_xëyma(Royukaay, 4)) 넣기(힙[Royukaay + 2] == 0 ? dalal_Araf("") : 힙[Royukaay + 2], 2); return;
            }
            if (ndigel == 182 && Word_SMS(tur_253d1510, "append")) {
                int Tekst = 0;
                if (Word_SMS(dayo_xëyma, "(I)Ljava/lang/StringBuilder;")) Tekst = siifar_Araf(빼기(1));
                else if (Word_SMS(dayo_xëyma, "(Z)Ljava/lang/StringBuilder;")) Tekst = dalal_Araf(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(dayo_xëyma, "(C)Ljava/lang/StringBuilder;")) {
                    int xëyma = 빼기(1); Tekst = jagleel_Dencukaay(1, 1); if (!njumte) 힙[Tekst + 2] = xëyma & 65535;
                }
                else if (Word_SMS(dayo_xëyma, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = dalal_Araf("null"); }
                else { foo_xëyma("unsupported StringBuilder append"); return; }
                int Royukaay = 빼기(2); if (!yëf_xëyma(Royukaay, 4) || !yëf_xëyma(Tekst, 1)) return;
                int 앞 = 힙[Royukaay + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], woñeeku_xëyma_diir = 힙[Tekst + 1];
                int 새글 = jagleel_Dencukaay(1, 앞길이 + woñeeku_xëyma_diir); if (njumte) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < woñeeku_xëyma_diir; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Tekst + 2 + 수];
                힙[Royukaay + 2] = 새글; 넣기(Royukaay, 2); return;
            }
        }
        foo_xëyma("unsupported library method");
    }
    static int TABLO_xar_xar(int Royukaay, int dajale_xëyma, int xeet_xëyma) {
        if (!yëf_xëyma(Royukaay, xeet_xëyma)) return 0;
        if (dajale_xëyma < 0 || dajale_xëyma >= 힙[Royukaay + 1]) { foo_xëyma("ArrayIndexOutOfBoundsException"); return 0; }
        return Royukaay + 2 + dajale_xëyma;
    }
    static void def_ndigel() {
        int 남음 = 500000;
        while (kadar_àlluwa_tur >= 0 && !njumte) {
            if (--남음 == 0) { foo_xëyma("instruction limit (500000)"); break; }
            int daw = 틀위치[kadar_àlluwa_tur], xëyma = 명바();
            if (njumte) break;
            if (xëyma == 0) continue;
            if (xëyma == 1) { 넣기(0, 2); continue; }
            if (xëyma >= 2 && xëyma <= 8) { 넣기(xëyma - 3, 1); continue; }
            if (xëyma == 16) { 넣기((byte)명바(), 1); continue; }
            if (xëyma == 17) { 넣기((short)명짧(), 1); continue; }
            if (xëyma == 18 || xëyma == 19) {
                int 수 = xëyma == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) foo_xëyma("invalid ldc constant");
                else if (Lees_dul_soppi_xàmme[수] == 3) 넣기(상가[수], 1);
                else if (Lees_dul_soppi_xàmme[수] == 8) 넣기(Lees_dul_soppi_SMS(상가[수]), 2);
                else foo_xëyma("unsupported ldc constant");
                continue;
            }
            if (xëyma == 21 || xëyma == 25) { 지역읽기(명바(), xëyma == 21 ? 1 : 2); continue; }
            if (xëyma >= 26 && xëyma <= 29) { 지역읽기(xëyma - 26, 1); continue; }
            if (xëyma >= 42 && xëyma <= 45) { 지역읽기(xëyma - 42, 2); continue; }
            if (xëyma == 54 || xëyma == 58) { biir_dënnd(명바(), xëyma == 54 ? 1 : 2); continue; }
            if (xëyma >= 59 && xëyma <= 62) { biir_dënnd(xëyma - 59, 1); continue; }
            if (xëyma >= 75 && xëyma <= 78) { biir_dënnd(xëyma - 75, 2); continue; }
            if (xëyma == 46 || xëyma == 50) {
                int dajale_xëyma = 빼기(1), Royukaay = 빼기(2), xar_xar_dugal_xabaar = TABLO_xar_xar(Royukaay, dajale_xëyma, xëyma == 46 ? 2 : 3);
                if (!njumte) 넣기(힙[xar_xar_dugal_xabaar], xëyma == 46 ? 1 : 2); continue;
            }
            if (xëyma == 79 || xëyma == 83) {
                int ëmbeef_cër = 빼기(xëyma == 79 ? 1 : 2), dajale_xëyma = 빼기(1), Royukaay = 빼기(2), xar_xar_dugal_xabaar = TABLO_xar_xar(Royukaay, dajale_xëyma, xëyma == 79 ? 2 : 3);
                if (xëyma == 83 && ëmbeef_cër != 0) yëf_xëyma(ëmbeef_cër, 1);
                if (!njumte) 힙[xar_xar_dugal_xabaar] = ëmbeef_cër; continue;
            }
            if (xëyma == 87) { 빼기(0); continue; }
            if (xëyma == 89) { int 가 = 빼기(0), xeet_xëyma = 반환형; 넣기(가, xeet_xëyma); 넣기(가, xeet_xëyma); continue; }
            if (xëyma == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (xëyma == 96 || xëyma == 100 || xëyma == 104 || xëyma == 108 || xëyma == 112 || xëyma == 120
                || xëyma == 122 || xëyma == 124 || xëyma == 126 || xëyma == 128 || xëyma == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((xëyma == 108 || xëyma == 112) && 나 == 0) { foo_xëyma("ArithmeticException: / by zero"); continue; }
                if (xëyma == 96) 결과 = 가 + 나;
                if (xëyma == 100) 결과 = 가 - 나;
                if (xëyma == 104) 결과 = 가 * 나;
                if (xëyma == 108) 결과 = 가 / 나;
                if (xëyma == 112) 결과 = 가 % 나;
                if (xëyma == 120) 결과 = 가 << 나;
                if (xëyma == 122) 결과 = 가 >> 나;
                if (xëyma == 124) 결과 = 가 >>> 나;
                if (xëyma == 126) 결과 = 가 & 나;
                if (xëyma == 128) 결과 = 가 | 나;
                if (xëyma == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (xëyma == 116) { 넣기(-빼기(1), 1); continue; }
            if (xëyma == 132) {
                int dënnd_nameef = 명바(), 증분 = (byte)명바(); 지역읽기(dënnd_nameef, 1); 넣기(빼기(1) + 증분, 1); biir_dënnd(dënnd_nameef, 1); continue;
            }
            if (xëyma >= 145 && xëyma <= 147) {
                int 수 = 빼기(1); 넣기(xëyma == 145 ? (byte)수 : xëyma == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (xëyma >= 153 && xëyma <= 167 || xëyma == 198 || xëyma == 199) {
                int jëmmukaay_xëyma = daw + (short)명짧(); boolean 갈까 = xëyma == 167;
                if (xëyma >= 153 && xëyma <= 158) {
                    int 수 = 빼기(1); 갈까 = xëyma == 153 ? 수 == 0 : xëyma == 154 ? 수 != 0 : xëyma == 155 ? 수 < 0 : xëyma == 156 ? 수 >= 0 : xëyma == 157 ? 수 > 0 : 수 <= 0;
                } else if (xëyma >= 159 && xëyma <= 166) {
                    int 나 = 빼기(xëyma >= 165 ? 2 : 1), 가 = 빼기(xëyma >= 165 ? 2 : 1);
                    갈까 = xëyma == 159 || xëyma == 165 ? 가 == 나 : xëyma == 160 || xëyma == 166 ? 가 != 나 : xëyma == 161 ? 가 < 나 : xëyma == 162 ? 가 >= 나 : xëyma == 163 ? 가 > 나 : 가 <= 나;
                } else if (xëyma == 198 || xëyma == 199) { int 수 = 빼기(2); 갈까 = xëyma == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) toxal_xëyma(jëmmukaay_xëyma); continue;
            }
            if (xëyma == 172 || xëyma == 176 || xëyma == 177) { 반환(xëyma == 172 ? 1 : xëyma == 176 ? 2 : 0); continue; }
            if (xëyma == 178) {
                int 수 = 명짧(); if (!sek_Lees_dul_soppi(수, 9)) continue;
                if (!Word_SMS(maas_tur_SMS(상가[수]), "java/lang/System") || !Word_SMS(Royukaay_tur(상나[수]), "out")
                    || !Word_SMS(Royukaay_xeet(상나[수]), "Ljava/io/PrintStream;")) foo_xëyma("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (xëyma == 182 || xëyma == 183 || xëyma == 184) { Wuute_doxalin(명짧(), xëyma); continue; }
            if (xëyma == 187) {
                int tur_253d1510 = maas_tur_SMS(명짧());
                if (Word_SMS(tur_253d1510, "java/lang/StringBuilder")) 넣기(jagleel_Dencukaay(4, 1), 2);
                else if (Word_SMS(tur_253d1510, "java/io/FileInputStream") || Word_SMS(tur_253d1510, "java/io/FileOutputStream")) {
                    int Royukaay = jagleel_Dencukaay(Word_SMS(tur_253d1510, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!njumte) { 힙[Royukaay + 2] = -1; 넣기(Royukaay, 2); }
                } else foo_xëyma("unsupported object construction");
                continue;
            }
            if (xëyma == 188 || xëyma == 189) {
                if (xëyma == 188) { if (명바() != 10) foo_xëyma("only int[] newarray is supported"); }
                else if (!Word_SMS(maas_tur_SMS(명짧()), "java/lang/String")) foo_xëyma("only String[] anewarray is supported");
                int diir_xëyma = 빼기(1); 넣기(jagleel_Dencukaay(xëyma == 188 ? 2 : 3, diir_xëyma), 2); continue;
            }
            if (xëyma == 190) {
                int Royukaay = 빼기(2);
                if (Royukaay < 1 || Royukaay >= 힙끝 - 1 || (힙[Royukaay] != 2 && 힙[Royukaay] != 3)) foo_xëyma("null or invalid array");
                else 넣기(힙[Royukaay + 1], 1); continue;
            }
            if (xëyma == 192) {
                int tur_253d1510 = maas_tur_SMS(명짧()), Royukaay = 빼기(2);
                if (!Word_SMS(tur_253d1510, "java/lang/String")) foo_xëyma("unsupported checkcast");
                else if (Royukaay != 0) yëf_xëyma(Royukaay, 1);
                넣기(Royukaay, 2); continue;
            }
            foo_xëyma("unsupported bytecode");
        }
    }
    public static int daw() {
        if (kiy_jariñoo_internet.인수개수() == 1 && 자바도구.같음(kiy_jariñoo_internet.인수(0), "-version")) {
            kiy_jariñoo_internet.biir("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (kiy_jariñoo_internet.인수개수() < 1) { kiy_jariñoo_internet.biir("Usage: java CLASS [ARGS]\n"); return 2; }
        int diir_xëyma = 자바도구.tur_253d1510(bara_denc_tur_SMS, kiy_jariñoo_internet.인수(0));
        if (diir_xëyma < 1 || diir_xëyma > 57) { kiy_jariñoo_internet.biir("java: invalid class name\n"); return 2; }
        bara_denc_tur_SMS[diir_xëyma] = '.'; bara_denc_tur_SMS[diir_xëyma + 1] = 'c'; bara_denc_tur_SMS[diir_xëyma + 2] = 'l'; bara_denc_tur_SMS[diir_xëyma + 3] = 'a'; bara_denc_tur_SMS[diir_xëyma + 4] = 's'; bara_denc_tur_SMS[diir_xëyma + 5] = 's';
        tolluwaay = kiy_jariñoo_internet.파일읽기(bara_denc_tur_SMS, bara_denc);
        if (tolluwaay < 0) { kiy_jariñoo_internet.biir("java: cannot read class: "); 자바도구.수쓰기(tolluwaay); kiy_jariñoo_internet.biir_Araf_xëyma(10); return 1; }
        클래스읽기(); if (njumte) return 1;
        int Araf_tur = Lees_dul_soppi_SMS(maas_tur);
        if (!njumte && 힙[Araf_tur + 1] != diir_xëyma) foo_xëyma("class name does not match file");
        for (int 수 = 0; 수 < diir_xëyma && !njumte; 수++) if (힙[Araf_tur + 2 + 수] != bara_denc_tur_SMS[수]) foo_xëyma("class name does not match file");
        int dugal_xabaar_Tomb_xëyma = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Word_SMS(doxalin_tur_SMS[수], "main") && Word_SMS(doxalin_xeet[수], "([Ljava/lang/String;)V") && (doxalin_jot[수] & 9) == 9) dugal_xabaar_Tomb_xëyma = 수;
        if (dugal_xabaar_Tomb_xëyma < 0) foo_xëyma("public static void main(String[] args) required");
        if (njumte) return 1;
        int 인수 = jagleel_Dencukaay(3, kiy_jariñoo_internet.인수개수() - 1);
        for (int 수 = 1; 수 < kiy_jariñoo_internet.인수개수() && !njumte; 수++) 힙[인수 + 1 + 수] = dalal_Araf(kiy_jariñoo_internet.인수(수));
        kadar_àlluwa_tur = 0; kadar_doxalin[0] = dugal_xabaar_Tomb_xëyma; 틀위치[0] = doxalin_Door[dugal_xabaar_Tomb_xëyma]; dënnd_xëyma[0] = 인수; dënnd_xeet[0] = 2;
        def_ndigel(); return njumte ? 1 : 0;
    }
}
