// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. faele/스택/Tshupiso/lekala 경계를 diragatsa_Taelo 중 검사한다. */
public final class 자바가상기계 {
    static int[] faele = new int[16384], faele_leina_SMS = new int[64];
    static int[] tlhomameng_theka = new int[512], 상가 = new int[512], 상나 = new int[512], dikwalwa_Tshupiso = new int[512];
    static int[] mokgwa_leina_SMS = new int[32], mokgwa_tlanya = new int[32], mokgwa_letlelesega = new int[32];
    static int[] mokgwa_simolola = new int[32], mokgwa_kgaola = new int[32], mokgwa_kokoanyodinepe = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], mokgwa_Thulaganyo_tlanya = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] e_e_gaufi_Boleng = new int[4096], e_e_gaufi_tlanya = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] Foreimi_mokgwa = new int[32], 틀위치 = new int[32], Foreimi_kokoanyodinepe = new int[32];
    static int[] 힙 = new int[8192];
    static int lekanya, 읽기위치, 상수수, 함수수, mofuta_leina, Foreimi_tshupane = -1, 힙끝 = 1, 반환형;
    static boolean phoso;

    static void palelo_Boleng(String Lefoko_SMS) {
        if (!phoso) { modirisi.kwala("JVM error: "); modirisi.kwala(Lefoko_SMS); modirisi.kwala_Letshwao_Boleng(10); }
        phoso = true;
    }
    static boolean faelekhutshwe_ya_media(int dirisa, int boleele_Boleng) { return dirisa >= 0 && boleele_Boleng >= 0 && dirisa <= lekanya - boleele_Boleng; }
    static int baete_Boleng() {
        if (!faelekhutshwe_ya_media(읽기위치, 1)) { palelo_Boleng("truncated class file"); return 0; }
        return faele[읽기위치++];
    }
    static int 짧은수() { return baete_Boleng() << 8 | baete_Boleng(); }
    static int Palotlalo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int boleele_Boleng) { if (!faelekhutshwe_ya_media(읽기위치, boleele_Boleng)) palelo_Boleng("invalid attribute size"); else 읽기위치 += boleele_Boleng; }
    static boolean tlhola_tlhomameng(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || tlhomameng_theka[수] != 종류) { palelo_Boleng("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int dirisa, int boleele_Boleng, String Lefoko_SMS) {
        if (!faelekhutshwe_ya_media(dirisa, boleele_Boleng) || boleele_Boleng != Lefoko_SMS.length()) return false;
        for (int 수 = 0; 수 < boleele_Boleng; 수++) if (faele[dirisa + 수] != Lefoko_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Lefoko_SMS(int tlhomameng_Boleng, String Lefoko_SMS) { return tlhola_tlhomameng(tlhomameng_Boleng, 1) && 구간(상가[tlhomameng_Boleng], 상나[tlhomameng_Boleng], Lefoko_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!tlhola_tlhomameng(가, 1) || !tlhola_tlhomameng(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (faele[상가[가] + 수] != faele[상가[나] + 수]) return false;
        return true;
    }
    static int mofuta_leina_SMS(int 수) { return tlhola_tlhomameng(수, 7) && tlhola_tlhomameng(상가[수], 1) ? 상가[수] : 0; }
    static int Tshupiso_leina(int 수) { return tlhola_tlhomameng(수, 12) && tlhola_tlhomameng(상가[수], 1) ? 상가[수] : 0; }
    static int Tshupiso_tlanya(int 수) { return tlhola_tlhomameng(수, 12) && tlhola_tlhomameng(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean lolea_tlanya) {
        if (읽기위치 >= 끝) { palelo_Boleng("invalid descriptor"); return 0; }
        int Boleng = baete_Boleng();
        if (Boleng == 'V' && lolea_tlanya) return 0;
        if (Boleng == 'I' || Boleng == 'B' || Boleng == 'C' || Boleng == 'S' || Boleng == 'Z') return 1;
        if (Boleng == '[') { 서술형(끝, false); return 2; }
        if (Boleng == 'L') {
            int dirisa = 읽기위치;
            while (읽기위치 < 끝 && faele[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == dirisa) palelo_Boleng("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        palelo_Boleng("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int TIRISO_Boleng) {
        int 이전 = 읽기위치, 수 = mokgwa_tlanya[TIRISO_Boleng];
        if (!tlhola_tlhomameng(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (baete_Boleng() != '(') palelo_Boleng("invalid method descriptor");
        int 개수 = 0;
        while (!phoso && 읽기위치 < 끝 && faele[읽기위치] != ')') {
            if (개수 == 16) { palelo_Boleng("too many method arguments"); break; }
            mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || baete_Boleng() != ')') palelo_Boleng("invalid method descriptor");
        함수반환[TIRISO_Boleng] = 서술형(끝, true); 함수인수수[TIRISO_Boleng] = 개수;
        if (읽기위치 != 끝) palelo_Boleng("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !phoso; 수++) { tlhola_tlhomameng(짧은수(), 1); 건너(Palotlalo()); }
    }
    static int Taelo_boleele(int Boleng) {
        if (Boleng == 16 || Boleng == 18 || Boleng == 21 || Boleng == 25 || Boleng == 54 || Boleng == 58 || Boleng == 188) return 2;
        if (Boleng == 17 || Boleng == 19 || Boleng == 132 || Boleng >= 153 && Boleng <= 167
            || Boleng >= 178 && Boleng <= 184 || Boleng == 187 || Boleng == 189 || Boleng == 192 || Boleng == 198 || Boleng == 199) return 3;
        if (Boleng >= 0 && Boleng <= 8 || Boleng >= 26 && Boleng <= 29 || Boleng >= 42 && Boleng <= 46 || Boleng == 50
            || Boleng >= 59 && Boleng <= 62 || Boleng >= 75 && Boleng <= 79 || Boleng == 83 || Boleng == 87 || Boleng == 89 || Boleng == 95
            || Boleng == 96 || Boleng == 100 || Boleng == 104 || Boleng == 108 || Boleng == 112 || Boleng == 116
            || Boleng == 120 || Boleng == 122 || Boleng == 124 || Boleng == 126 || Boleng == 128 || Boleng == 130
            || Boleng >= 145 && Boleng <= 147 || Boleng == 172 || Boleng == 176 || Boleng == 177 || Boleng == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (Palotlalo() != 0xcafebabe) palelo_Boleng("not a class file");
        int 부판 = 짧은수(), kgaolo_Boleng = 짧은수();
        if (kgaolo_Boleng < 45 || kgaolo_Boleng > 52 || 부판 != 0) palelo_Boleng("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { palelo_Boleng("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !phoso; 수++) {
            int 종류 = baete_Boleng(); tlhomameng_theka[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = Palotlalo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else palelo_Boleng("unsupported constant type");
        }
        int tetla_Boleng = 짧은수();
        if ((tetla_Boleng & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) palelo_Boleng("unsupported class flags");
        mofuta_leina = mofuta_leina_SMS(짧은수());
        if (!Lefoko_SMS(mofuta_leina_SMS(짧은수()), "java/lang/Object")) palelo_Boleng("inheritance unsupported");
        if (짧은수() != 0) palelo_Boleng("interfaces unsupported");
        if (짧은수() != 0) palelo_Boleng("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { palelo_Boleng("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !phoso; 수++) {
            mokgwa_letlelesega[수] = 짧은수(); mokgwa_leina_SMS[수] = 짧은수(); mokgwa_tlanya[수] = 짧은수();
            tlhola_tlhomameng(mokgwa_leina_SMS[수], 1); 서술읽기(수);
            if ((mokgwa_letlelesega[수] & (0x100 | 0x400 | 0x20)) != 0) palelo_Boleng("native, abstract and synchronized methods unsupported");
            if ((mokgwa_letlelesega[수] & 8) == 0 && !Lefoko_SMS(mokgwa_leina_SMS[수], "<init>")) palelo_Boleng("instance methods unsupported");
            if (Lefoko_SMS(mokgwa_leina_SMS[수], "<clinit>")) palelo_Boleng("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(mokgwa_leina_SMS[앞], mokgwa_leina_SMS[수]) && 같은말(mokgwa_tlanya[앞], mokgwa_tlanya[수])) palelo_Boleng("duplicate method");
            int 개수 = 짧은수();
            for (int nonofo_Boleng = 0; nonofo_Boleng < 개수 && !phoso; nonofo_Boleng++) {
                int leina = 짧은수(), boleele_Boleng = Palotlalo(), dirisa = 읽기위치;
                if (!faelekhutshwe_ya_media(dirisa, boleele_Boleng)) { palelo_Boleng("truncated method attribute"); break; }
                if (Lefoko_SMS(leina, "Code")) {
                    if (mokgwa_simolola[수] != 0) palelo_Boleng("duplicate Code attribute");
                    mokgwa_kokoanyodinepe[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = Palotlalo();
                    if (mokgwa_kokoanyodinepe[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) palelo_Boleng("method memory limits exceeded");
                    mokgwa_simolola[수] = 읽기위치; 건너(코드길이); mokgwa_kgaola[수] = 읽기위치;
                    if (짧은수() != 0) palelo_Boleng("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != dirisa + boleele_Boleng) palelo_Boleng("Code attribute size mismatch");
                } else 건너(boleele_Boleng);
            }
            if (mokgwa_simolola[수] == 0) palelo_Boleng("missing Code attribute");
            int sebaka_tsenyo = mokgwa_simolola[수];
            while (sebaka_tsenyo < mokgwa_kgaola[수] && !phoso) {
                int boleele_Boleng = Taelo_boleele(faele[sebaka_tsenyo]);
                if (boleele_Boleng == 0 || boleele_Boleng > mokgwa_kgaola[수] - sebaka_tsenyo) { palelo_Boleng("unsupported or truncated bytecode"); break; }
                경계[sebaka_tsenyo] = 수 + 1; sebaka_tsenyo += boleele_Boleng;
            }
            // 실행하지 않는 경로에도 잘못된 lekala 목적지를 허용하지 않는다.
            sebaka_tsenyo = mokgwa_simolola[수];
            while (sebaka_tsenyo < mokgwa_kgaola[수] && !phoso) {
                int Boleng = faele[sebaka_tsenyo];
                if (Boleng >= 153 && Boleng <= 167 || Boleng == 198 || Boleng == 199) {
                    int bogorogelo_Boleng = sebaka_tsenyo + (short)(faele[sebaka_tsenyo + 1] << 8 | faele[sebaka_tsenyo + 2]);
                    if (bogorogelo_Boleng < mokgwa_simolola[수] || bogorogelo_Boleng >= mokgwa_kgaola[수] || 경계[bogorogelo_Boleng] != 수 + 1) palelo_Boleng("invalid branch target");
                }
                sebaka_tsenyo += Taelo_boleele(Boleng);
            }
        }
        if (!phoso) 속성건너();
        if (읽기위치 != lekanya) palelo_Boleng("extra class file data");
    }
    static int abela_Polokelo(int 종류, int boleele_Boleng) {
        if (boleele_Boleng < 0 || boleele_Boleng > 힙.length - 힙끝 - 2) { palelo_Boleng("object heap exhausted or negative array size"); return 0; }
        int Tshupiso = 힙끝; 힙끝 += boleele_Boleng + 2; 힙[Tshupiso] = 종류; 힙[Tshupiso + 1] = boleele_Boleng;
        return Tshupiso;
    }
    static boolean selwana_Boleng(int Tshupiso, int 종류) {
        if (Tshupiso < 1 || Tshupiso >= 힙끝 - 1 || 힙[Tshupiso] != 종류) { palelo_Boleng("null or invalid object reference"); return false; }
        return true;
    }
    static int tlhomameng_SMS(int tshupane) {
        if (!tlhola_tlhomameng(tshupane, 1)) return 0;
        if (dikwalwa_Tshupiso[tshupane] != 0) return dikwalwa_Tshupiso[tshupane];
        int Tshupiso = abela_Polokelo(1, 상나[tshupane]); if (phoso) return 0;
        int 끝 = 상가[tshupane] + 상나[tshupane], 수 = 상가[tshupane], boleele_Boleng = 0;
        while (수 < 끝 && !phoso) {
            int Boleng = faele[수++];
            if (Boleng == 0) palelo_Boleng("invalid modified UTF-8");
            else if (Boleng >= 192 && Boleng <= 223 && 수 < 끝) {
                int 다음 = faele[수++];
                if ((다음 & 192) != 128) palelo_Boleng("invalid modified UTF-8");
                Boleng = (Boleng & 31) << 6 | 다음 & 63;
                if (Boleng != 0 && Boleng < 128) palelo_Boleng("overlong modified UTF-8");
            } else if (Boleng >= 224 && Boleng <= 239 && 수 + 1 < 끝) {
                int 가 = faele[수++], 나 = faele[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) palelo_Boleng("invalid modified UTF-8");
                Boleng = (Boleng & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (Boleng < 2048) palelo_Boleng("overlong modified UTF-8");
            } else if (Boleng >= 128) palelo_Boleng("invalid modified UTF-8");
            힙[Tshupiso + 2 + boleele_Boleng++] = Boleng;
        }
        힙[Tshupiso + 1] = boleele_Boleng; dikwalwa_Tshupiso[tshupane] = Tshupiso; return Tshupiso;
    }
    static int pinagare_Letshwao(String Boleng) {
        int Tshupiso = abela_Polokelo(1, Boleng.length()); if (phoso) return 0;
        for (int 수 = 0; 수 < Boleng.length(); 수++) 힙[Tshupiso + 2 + 수] = Boleng.charAt(수);
        return Tshupiso;
    }
    static void kwala_SMS(int Tshupiso) {
        if (Tshupiso == 0) { modirisi.kwala("null"); return; }
        if (!selwana_Boleng(Tshupiso, 1)) return;
        for (int 수 = 0; 수 < 힙[Tshupiso + 1]; 수++) modirisi.kwala_Letshwao_Boleng(힙[Tshupiso + 2 + 수]);
    }
    static int dijite_Letshwao(int Boleng) {
        int Tshupiso = abela_Polokelo(1, 11); if (phoso) return 0;
        int boleele_Boleng = 0;
        if (Boleng < 0) 힙[Tshupiso + 2 + boleele_Boleng++] = '-'; else Boleng = -Boleng;
        int 자리 = 1000000000; boolean dirisa = false;
        while (자리 != 0) {
            int 수 = -(Boleng / 자리);
            if (수 != 0 || dirisa || 자리 == 1) { 힙[Tshupiso + 2 + boleele_Boleng++] = '0' + 수; dirisa = true; }
            Boleng %= 자리; 자리 /= 10;
        }
        힙[Tshupiso + 1] = boleele_Boleng; return Tshupiso;
    }
    static int 정수해독(int Tshupiso) {
        if (!selwana_Boleng(Tshupiso, 1)) return 0;
        int boleele_Boleng = 힙[Tshupiso + 1], 수 = 0, Boleng = 0; boolean 음수 = false;
        if (boleele_Boleng > 0 && (힙[Tshupiso + 2] == '-' || 힙[Tshupiso + 2] == '+')) { 음수 = 힙[Tshupiso + 2] == '-'; 수++; }
        if (수 == boleele_Boleng) palelo_Boleng("NumberFormatException");
        for (; 수 < boleele_Boleng && !phoso; 수++) {
            int dijite_Boleng = 힙[Tshupiso + 2 + 수] - '0';
            if (dijite_Boleng < 0 || dijite_Boleng > 9 || Boleng < -214748364 || Boleng == -214748364 && dijite_Boleng > (음수 ? 8 : 7)) palelo_Boleng("NumberFormatException");
            Boleng = Boleng * 10 - dijite_Boleng;
        }
        return 음수 ? Boleng : -Boleng;
    }
    static void 넣기(int Boleng, int tlanya_Boleng) {
        if (phoso) return;
        if (Foreimi_tshupane < 0 || Foreimi_kokoanyodinepe[Foreimi_tshupane] >= mokgwa_kokoanyodinepe[Foreimi_mokgwa[Foreimi_tshupane]]) { palelo_Boleng("operand stack overflow"); return; }
        int sebaka_tsenyo = Foreimi_tshupane * 128 + Foreimi_kokoanyodinepe[Foreimi_tshupane]++; 스택값[sebaka_tsenyo] = Boleng; 스택형[sebaka_tsenyo] = tlanya_Boleng;
    }
    static int 빼기(int tlanya_Boleng) {
        if (phoso) return 0;
        if (Foreimi_tshupane < 0 || Foreimi_kokoanyodinepe[Foreimi_tshupane] < 1) { palelo_Boleng("operand stack underflow"); return 0; }
        int sebaka_tsenyo = Foreimi_tshupane * 128 + --Foreimi_kokoanyodinepe[Foreimi_tshupane]; 반환형 = 스택형[sebaka_tsenyo];
        if (tlanya_Boleng != 0 && 반환형 != tlanya_Boleng) palelo_Boleng("operand type mismatch");
        return 스택값[sebaka_tsenyo];
    }
    static void 지역읽기(int tshupane, int tlanya_Boleng) {
        if (tshupane >= 함수지역[Foreimi_mokgwa[Foreimi_tshupane]] || tshupane < 0 || e_e_gaufi_tlanya[Foreimi_tshupane * 128 + tshupane] != tlanya_Boleng) { palelo_Boleng("invalid or uninitialized local"); return; }
        넣기(e_e_gaufi_Boleng[Foreimi_tshupane * 128 + tshupane], tlanya_Boleng);
    }
    static void kwala_e_e_gaufi(int tshupane, int tlanya_Boleng) {
        if (tshupane >= 함수지역[Foreimi_mokgwa[Foreimi_tshupane]] || tshupane < 0) { palelo_Boleng("local index out of range"); return; }
        int Boleng = 빼기(tlanya_Boleng); e_e_gaufi_Boleng[Foreimi_tshupane * 128 + tshupane] = Boleng; e_e_gaufi_tlanya[Foreimi_tshupane * 128 + tshupane] = tlanya_Boleng;
    }
    static int 명바() {
        int 위치 = 틀위치[Foreimi_tshupane];
        if (위치 < mokgwa_simolola[Foreimi_mokgwa[Foreimi_tshupane]] || 위치 >= mokgwa_kgaola[Foreimi_mokgwa[Foreimi_tshupane]]) { palelo_Boleng("instruction pointer out of range"); return 0; }
        틀위치[Foreimi_tshupane]++; return faele[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void sutisa_Boleng(int 위치) {
        int TIRISO_Boleng = Foreimi_mokgwa[Foreimi_tshupane];
        if (위치 < mokgwa_simolola[TIRISO_Boleng] || 위치 >= mokgwa_kgaola[TIRISO_Boleng] || 경계[위치] != TIRISO_Boleng + 1) palelo_Boleng("invalid branch target");
        else 틀위치[Foreimi_tshupane] = 위치;
    }
    static void 호출(int TIRISO_Boleng) {
        if (Foreimi_tshupane == 31) { palelo_Boleng("call stack limit (32)"); return; }
        int 다음 = Foreimi_tshupane + 1;
        for (int 수 = 0; 수 < 128; 수++) e_e_gaufi_tlanya[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[TIRISO_Boleng] - 1; 수 >= 0; 수--) {
            e_e_gaufi_Boleng[다음 * 128 + 수] = 빼기(mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 수]); e_e_gaufi_tlanya[다음 * 128 + 수] = mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 수];
        }
        Foreimi_tshupane = 다음; Foreimi_mokgwa[Foreimi_tshupane] = TIRISO_Boleng; 틀위치[Foreimi_tshupane] = mokgwa_simolola[TIRISO_Boleng]; Foreimi_kokoanyodinepe[Foreimi_tshupane] = 0;
    }
    static void 반환(int tlanya_Boleng) {
        if (tlanya_Boleng != 함수반환[Foreimi_mokgwa[Foreimi_tshupane]]) { palelo_Boleng("return type mismatch"); return; }
        int Boleng = tlanya_Boleng == 0 ? 0 : 빼기(tlanya_Boleng);
        Foreimi_tshupane--; if (Foreimi_tshupane >= 0 && tlanya_Boleng != 0) 넣기(Boleng, tlanya_Boleng);
    }
    static int[] moela_faele_leina = new int[64];
    static void faele_moela_letsa(int mong_Boleng, int leina, int fometa_Boleng, int Taelo) {
        boolean 출력 = Lefoko_SMS(mong_Boleng, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Taelo == 183 && Lefoko_SMS(leina, "<init>")) {
            boolean 이어 = false;
            if (출력 && Lefoko_SMS(fometa_Boleng, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Lefoko_SMS(fometa_Boleng, "(Ljava/lang/String;)V")) { palelo_Boleng("unsupported file stream constructor"); return; }
            int faele_tsenyo_leina = 빼기(2), moela_Boleng = 빼기(2);
            if (!selwana_Boleng(faele_tsenyo_leina, 1) || !selwana_Boleng(moela_Boleng, 종류) || phoso) return;
            if (힙[moela_Boleng + 3] != 0) { palelo_Boleng("file stream already initialized"); return; }
            int boleele_Boleng = 힙[faele_tsenyo_leina + 1];
            if (boleele_Boleng < 1 || boleele_Boleng > 63) { palelo_Boleng("invalid file name length"); return; }
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < boleele_Boleng; sebaka_tsenyo++) {
                int Boleng = 힙[faele_tsenyo_leina + 2 + sebaka_tsenyo];
                if (Boleng < 1 || Boleng > 127) { palelo_Boleng("file stream paths currently require ASCII"); return; }
                moela_faele_leina[sebaka_tsenyo] = Boleng;
            }
            moela_faele_leina[boleele_Boleng] = 0;
            int 서술자 = modirisi.파일서술자열기(moela_faele_leina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { palelo_Boleng("FileNotFoundException: file open failed"); return; }
            힙[moela_Boleng + 2] = 서술자; 힙[moela_Boleng + 3] = 1;
            return;
        }
        if (Taelo != 182) { palelo_Boleng("invalid file stream invocation"); return; }
        int tiro = -1, Boleng = 0;
        if (Lefoko_SMS(leina, "close") && Lefoko_SMS(fometa_Boleng, "()V")) tiro = 0;
        if (!출력 && Lefoko_SMS(leina, "read") && Lefoko_SMS(fometa_Boleng, "()I")) tiro = 1;
        if (출력 && Lefoko_SMS(leina, "write") && Lefoko_SMS(fometa_Boleng, "(I)V")) { tiro = 2; Boleng = 빼기(1); }
        if (tiro < 0) { palelo_Boleng("unsupported file stream method"); return; }
        int moela_Boleng = 빼기(2);
        if (!selwana_Boleng(moela_Boleng, 종류) || phoso) return;
        if (힙[moela_Boleng + 3] == 0) { palelo_Boleng("uninitialized file stream"); return; }
        int 서술자 = 힙[moela_Boleng + 2];
        if (tiro == 0) {
            if (서술자 >= 0 && modirisi.파일서술자닫기(서술자) < 0) palelo_Boleng("IOException: close failed");
            힙[moela_Boleng + 2] = -1; return;
        }
        if (서술자 < 0) { palelo_Boleng("IOException: stream closed"); return; }
        if (tiro == 1) {
            int 결과 = modirisi.파일한바이트읽기(서술자);
            if (결과 < -1) palelo_Boleng("IOException: read failed"); else 넣기(결과, 1);
        } else if (modirisi.파일한바이트쓰기(서술자, Boleng) != 1) palelo_Boleng("IOException: write failed");
    }
    static void letsa_mokgwa(int tshupane, int Taelo) {
        if (!tlhola_tlhomameng(tshupane, 10)) return;
        int mong_Boleng = mofuta_leina_SMS(상가[tshupane]), leina = Tshupiso_leina(상나[tshupane]), fometa_Boleng = Tshupiso_tlanya(상나[tshupane]);
        if (phoso) return;
        if (같은말(mong_Boleng, mofuta_leina)) {
            if (Taelo != 184) { palelo_Boleng("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(leina, mokgwa_leina_SMS[수]) && 같은말(fometa_Boleng, mokgwa_tlanya[수])) {
                if ((mokgwa_letlelesega[수] & 8) == 0) palelo_Boleng("method is not static"); else 호출(수);
                return;
            }
            palelo_Boleng("NoSuchMethodError"); return;
        }
        if (Lefoko_SMS(mong_Boleng, "java/io/FileInputStream") || Lefoko_SMS(mong_Boleng, "java/io/FileOutputStream")) {
            faele_moela_letsa(mong_Boleng, leina, fometa_Boleng, Taelo); return;
        }
        if (Taelo == 184 && Lefoko_SMS(mong_Boleng, "java/lang/Integer") && Lefoko_SMS(leina, "parseInt") && Lefoko_SMS(fometa_Boleng, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Taelo == 182 && Lefoko_SMS(mong_Boleng, "java/io/PrintStream") && (Lefoko_SMS(leina, "println") || Lefoko_SMS(leina, "print"))) {
            int tlanya_Boleng = 0, Boleng = 0;
            if (Lefoko_SMS(fometa_Boleng, "(I)V")) { tlanya_Boleng = 1; Boleng = 빼기(1); }
            else if (Lefoko_SMS(fometa_Boleng, "(Z)V")) { tlanya_Boleng = 2; Boleng = 빼기(1); }
            else if (Lefoko_SMS(fometa_Boleng, "(C)V")) { tlanya_Boleng = 3; Boleng = 빼기(1); }
            else if (Lefoko_SMS(fometa_Boleng, "(Ljava/lang/String;)V")) { tlanya_Boleng = 4; Boleng = 빼기(2); }
            else if (!Lefoko_SMS(fometa_Boleng, "()V") || !Lefoko_SMS(leina, "println")) palelo_Boleng("unsupported print descriptor");
            if (빼기(2) != -1) palelo_Boleng("invalid PrintStream receiver");
            if (phoso) return;
            if (tlanya_Boleng == 1) 자바도구.수쓰기(Boleng);
            if (tlanya_Boleng == 2) modirisi.kwala(Boleng == 0 ? "false" : "true");
            if (tlanya_Boleng == 3) modirisi.kwala_Letshwao_Boleng(Boleng & 65535);
            if (tlanya_Boleng == 4) kwala_SMS(Boleng);
            if (Lefoko_SMS(leina, "println")) modirisi.kwala_Letshwao_Boleng(10);
            return;
        }
        if (Taelo == 182 && Lefoko_SMS(mong_Boleng, "java/lang/String")) {
            if (Lefoko_SMS(leina, "length") && Lefoko_SMS(fometa_Boleng, "()I")) {
                int Tshupiso = 빼기(2); if (selwana_Boleng(Tshupiso, 1)) 넣기(힙[Tshupiso + 1], 1); return;
            }
            if (Lefoko_SMS(leina, "charAt") && Lefoko_SMS(fometa_Boleng, "(I)C")) {
                int sekerepitipotlana_Boleng = 빼기(1), Tshupiso = 빼기(2);
                if (selwana_Boleng(Tshupiso, 1)) {
                    if (sekerepitipotlana_Boleng < 0 || sekerepitipotlana_Boleng >= 힙[Tshupiso + 1]) palelo_Boleng("StringIndexOutOfBoundsException"); else 넣기(힙[Tshupiso + 2 + sekerepitipotlana_Boleng], 1);
                }
                return;
            }
        }
        if (Lefoko_SMS(mong_Boleng, "java/lang/StringBuilder")) {
            if (Taelo == 183 && Lefoko_SMS(leina, "<init>") && Lefoko_SMS(fometa_Boleng, "()V")) { selwana_Boleng(빼기(2), 4); return; }
            if (Taelo == 182 && Lefoko_SMS(leina, "toString") && Lefoko_SMS(fometa_Boleng, "()Ljava/lang/String;")) {
                int Tshupiso = 빼기(2); if (selwana_Boleng(Tshupiso, 4)) 넣기(힙[Tshupiso + 2] == 0 ? pinagare_Letshwao("") : 힙[Tshupiso + 2], 2); return;
            }
            if (Taelo == 182 && Lefoko_SMS(leina, "append")) {
                int SMS = 0;
                if (Lefoko_SMS(fometa_Boleng, "(I)Ljava/lang/StringBuilder;")) SMS = dijite_Letshwao(빼기(1));
                else if (Lefoko_SMS(fometa_Boleng, "(Z)Ljava/lang/StringBuilder;")) SMS = pinagare_Letshwao(빼기(1) == 0 ? "false" : "true");
                else if (Lefoko_SMS(fometa_Boleng, "(C)Ljava/lang/StringBuilder;")) {
                    int Boleng = 빼기(1); SMS = abela_Polokelo(1, 1); if (!phoso) 힙[SMS + 2] = Boleng & 65535;
                }
                else if (Lefoko_SMS(fometa_Boleng, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = pinagare_Letshwao("null"); }
                else { palelo_Boleng("unsupported StringBuilder append"); return; }
                int Tshupiso = 빼기(2); if (!selwana_Boleng(Tshupiso, 4) || !selwana_Boleng(SMS, 1)) return;
                int 앞 = 힙[Tshupiso + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Morago_Boleng_boleele = 힙[SMS + 1];
                int 새글 = abela_Polokelo(1, 앞길이 + Morago_Boleng_boleele); if (phoso) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Morago_Boleng_boleele; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[Tshupiso + 2] = 새글; 넣기(Tshupiso, 2); return;
            }
        }
        palelo_Boleng("unsupported library method");
    }
    static int setlhopha_sebaka(int Tshupiso, int sekerepitipotlana_Boleng, int tlanya_Boleng) {
        if (!selwana_Boleng(Tshupiso, tlanya_Boleng)) return 0;
        if (sekerepitipotlana_Boleng < 0 || sekerepitipotlana_Boleng >= 힙[Tshupiso + 1]) { palelo_Boleng("ArrayIndexOutOfBoundsException"); return 0; }
        return Tshupiso + 2 + sekerepitipotlana_Boleng;
    }
    static void diragatsa_Taelo() {
        int 남음 = 500000;
        while (Foreimi_tshupane >= 0 && !phoso) {
            if (--남음 == 0) { palelo_Boleng("instruction limit (500000)"); break; }
            int dirisa = 틀위치[Foreimi_tshupane], Boleng = 명바();
            if (phoso) break;
            if (Boleng == 0) continue;
            if (Boleng == 1) { 넣기(0, 2); continue; }
            if (Boleng >= 2 && Boleng <= 8) { 넣기(Boleng - 3, 1); continue; }
            if (Boleng == 16) { 넣기((byte)명바(), 1); continue; }
            if (Boleng == 17) { 넣기((short)명짧(), 1); continue; }
            if (Boleng == 18 || Boleng == 19) {
                int 수 = Boleng == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) palelo_Boleng("invalid ldc constant");
                else if (tlhomameng_theka[수] == 3) 넣기(상가[수], 1);
                else if (tlhomameng_theka[수] == 8) 넣기(tlhomameng_SMS(상가[수]), 2);
                else palelo_Boleng("unsupported ldc constant");
                continue;
            }
            if (Boleng == 21 || Boleng == 25) { 지역읽기(명바(), Boleng == 21 ? 1 : 2); continue; }
            if (Boleng >= 26 && Boleng <= 29) { 지역읽기(Boleng - 26, 1); continue; }
            if (Boleng >= 42 && Boleng <= 45) { 지역읽기(Boleng - 42, 2); continue; }
            if (Boleng == 54 || Boleng == 58) { kwala_e_e_gaufi(명바(), Boleng == 54 ? 1 : 2); continue; }
            if (Boleng >= 59 && Boleng <= 62) { kwala_e_e_gaufi(Boleng - 59, 1); continue; }
            if (Boleng >= 75 && Boleng <= 78) { kwala_e_e_gaufi(Boleng - 75, 2); continue; }
            if (Boleng == 46 || Boleng == 50) {
                int sekerepitipotlana_Boleng = 빼기(1), Tshupiso = 빼기(2), sebaka_tsenyo = setlhopha_sebaka(Tshupiso, sekerepitipotlana_Boleng, Boleng == 46 ? 2 : 3);
                if (!phoso) 넣기(힙[sebaka_tsenyo], Boleng == 46 ? 1 : 2); continue;
            }
            if (Boleng == 79 || Boleng == 83) {
                int selwana_tlhakakaelo = 빼기(Boleng == 79 ? 1 : 2), sekerepitipotlana_Boleng = 빼기(1), Tshupiso = 빼기(2), sebaka_tsenyo = setlhopha_sebaka(Tshupiso, sekerepitipotlana_Boleng, Boleng == 79 ? 2 : 3);
                if (Boleng == 83 && selwana_tlhakakaelo != 0) selwana_Boleng(selwana_tlhakakaelo, 1);
                if (!phoso) 힙[sebaka_tsenyo] = selwana_tlhakakaelo; continue;
            }
            if (Boleng == 87) { 빼기(0); continue; }
            if (Boleng == 89) { int 가 = 빼기(0), tlanya_Boleng = 반환형; 넣기(가, tlanya_Boleng); 넣기(가, tlanya_Boleng); continue; }
            if (Boleng == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (Boleng == 96 || Boleng == 100 || Boleng == 104 || Boleng == 108 || Boleng == 112 || Boleng == 120
                || Boleng == 122 || Boleng == 124 || Boleng == 126 || Boleng == 128 || Boleng == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((Boleng == 108 || Boleng == 112) && 나 == 0) { palelo_Boleng("ArithmeticException: / by zero"); continue; }
                if (Boleng == 96) 결과 = 가 + 나;
                if (Boleng == 100) 결과 = 가 - 나;
                if (Boleng == 104) 결과 = 가 * 나;
                if (Boleng == 108) 결과 = 가 / 나;
                if (Boleng == 112) 결과 = 가 % 나;
                if (Boleng == 120) 결과 = 가 << 나;
                if (Boleng == 122) 결과 = 가 >> 나;
                if (Boleng == 124) 결과 = 가 >>> 나;
                if (Boleng == 126) 결과 = 가 & 나;
                if (Boleng == 128) 결과 = 가 | 나;
                if (Boleng == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (Boleng == 116) { 넣기(-빼기(1), 1); continue; }
            if (Boleng == 132) {
                int e_e_gaufi_Mothamo = 명바(), 증분 = (byte)명바(); 지역읽기(e_e_gaufi_Mothamo, 1); 넣기(빼기(1) + 증분, 1); kwala_e_e_gaufi(e_e_gaufi_Mothamo, 1); continue;
            }
            if (Boleng >= 145 && Boleng <= 147) {
                int 수 = 빼기(1); 넣기(Boleng == 145 ? (byte)수 : Boleng == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (Boleng >= 153 && Boleng <= 167 || Boleng == 198 || Boleng == 199) {
                int bogorogelo_Boleng = dirisa + (short)명짧(); boolean 갈까 = Boleng == 167;
                if (Boleng >= 153 && Boleng <= 158) {
                    int 수 = 빼기(1); 갈까 = Boleng == 153 ? 수 == 0 : Boleng == 154 ? 수 != 0 : Boleng == 155 ? 수 < 0 : Boleng == 156 ? 수 >= 0 : Boleng == 157 ? 수 > 0 : 수 <= 0;
                } else if (Boleng >= 159 && Boleng <= 166) {
                    int 나 = 빼기(Boleng >= 165 ? 2 : 1), 가 = 빼기(Boleng >= 165 ? 2 : 1);
                    갈까 = Boleng == 159 || Boleng == 165 ? 가 == 나 : Boleng == 160 || Boleng == 166 ? 가 != 나 : Boleng == 161 ? 가 < 나 : Boleng == 162 ? 가 >= 나 : Boleng == 163 ? 가 > 나 : 가 <= 나;
                } else if (Boleng == 198 || Boleng == 199) { int 수 = 빼기(2); 갈까 = Boleng == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) sutisa_Boleng(bogorogelo_Boleng); continue;
            }
            if (Boleng == 172 || Boleng == 176 || Boleng == 177) { 반환(Boleng == 172 ? 1 : Boleng == 176 ? 2 : 0); continue; }
            if (Boleng == 178) {
                int 수 = 명짧(); if (!tlhola_tlhomameng(수, 9)) continue;
                if (!Lefoko_SMS(mofuta_leina_SMS(상가[수]), "java/lang/System") || !Lefoko_SMS(Tshupiso_leina(상나[수]), "out")
                    || !Lefoko_SMS(Tshupiso_tlanya(상나[수]), "Ljava/io/PrintStream;")) palelo_Boleng("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (Boleng == 182 || Boleng == 183 || Boleng == 184) { letsa_mokgwa(명짧(), Boleng); continue; }
            if (Boleng == 187) {
                int leina = mofuta_leina_SMS(명짧());
                if (Lefoko_SMS(leina, "java/lang/StringBuilder")) 넣기(abela_Polokelo(4, 1), 2);
                else if (Lefoko_SMS(leina, "java/io/FileInputStream") || Lefoko_SMS(leina, "java/io/FileOutputStream")) {
                    int Tshupiso = abela_Polokelo(Lefoko_SMS(leina, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!phoso) { 힙[Tshupiso + 2] = -1; 넣기(Tshupiso, 2); }
                } else palelo_Boleng("unsupported object construction");
                continue;
            }
            if (Boleng == 188 || Boleng == 189) {
                if (Boleng == 188) { if (명바() != 10) palelo_Boleng("only int[] newarray is supported"); }
                else if (!Lefoko_SMS(mofuta_leina_SMS(명짧()), "java/lang/String")) palelo_Boleng("only String[] anewarray is supported");
                int boleele_Boleng = 빼기(1); 넣기(abela_Polokelo(Boleng == 188 ? 2 : 3, boleele_Boleng), 2); continue;
            }
            if (Boleng == 190) {
                int Tshupiso = 빼기(2);
                if (Tshupiso < 1 || Tshupiso >= 힙끝 - 1 || (힙[Tshupiso] != 2 && 힙[Tshupiso] != 3)) palelo_Boleng("null or invalid array");
                else 넣기(힙[Tshupiso + 1], 1); continue;
            }
            if (Boleng == 192) {
                int leina = mofuta_leina_SMS(명짧()), Tshupiso = 빼기(2);
                if (!Lefoko_SMS(leina, "java/lang/String")) palelo_Boleng("unsupported checkcast");
                else if (Tshupiso != 0) selwana_Boleng(Tshupiso, 1);
                넣기(Tshupiso, 2); continue;
            }
            palelo_Boleng("unsupported bytecode");
        }
    }
    public static int dirisa() {
        if (modirisi.인수개수() == 1 && 자바도구.같음(modirisi.인수(0), "-version")) {
            modirisi.kwala("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (modirisi.인수개수() < 1) { modirisi.kwala("Usage: java CLASS [ARGS]\n"); return 2; }
        int boleele_Boleng = 자바도구.leina(faele_leina_SMS, modirisi.인수(0));
        if (boleele_Boleng < 1 || boleele_Boleng > 57) { modirisi.kwala("java: invalid class name\n"); return 2; }
        faele_leina_SMS[boleele_Boleng] = '.'; faele_leina_SMS[boleele_Boleng + 1] = 'c'; faele_leina_SMS[boleele_Boleng + 2] = 'l'; faele_leina_SMS[boleele_Boleng + 3] = 'a'; faele_leina_SMS[boleele_Boleng + 4] = 's'; faele_leina_SMS[boleele_Boleng + 5] = 's';
        lekanya = modirisi.파일읽기(faele_leina_SMS, faele);
        if (lekanya < 0) { modirisi.kwala("java: cannot read class: "); 자바도구.수쓰기(lekanya); modirisi.kwala_Letshwao_Boleng(10); return 1; }
        클래스읽기(); if (phoso) return 1;
        int Letshwao_leina = tlhomameng_SMS(mofuta_leina);
        if (!phoso && 힙[Letshwao_leina + 1] != boleele_Boleng) palelo_Boleng("class name does not match file");
        for (int 수 = 0; 수 < boleele_Boleng && !phoso; 수++) if (힙[Letshwao_leina + 2 + 수] != faele_leina_SMS[수]) palelo_Boleng("class name does not match file");
        int tsenyo_ntlha_Boleng = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Lefoko_SMS(mokgwa_leina_SMS[수], "main") && Lefoko_SMS(mokgwa_tlanya[수], "([Ljava/lang/String;)V") && (mokgwa_letlelesega[수] & 9) == 9) tsenyo_ntlha_Boleng = 수;
        if (tsenyo_ntlha_Boleng < 0) palelo_Boleng("public static void main(String[] args) required");
        if (phoso) return 1;
        int 인수 = abela_Polokelo(3, modirisi.인수개수() - 1);
        for (int 수 = 1; 수 < modirisi.인수개수() && !phoso; 수++) 힙[인수 + 1 + 수] = pinagare_Letshwao(modirisi.인수(수));
        Foreimi_tshupane = 0; Foreimi_mokgwa[0] = tsenyo_ntlha_Boleng; 틀위치[0] = mokgwa_simolola[tsenyo_ntlha_Boleng]; e_e_gaufi_Boleng[0] = 인수; e_e_gaufi_tlanya[0] = 2;
        diragatsa_Taelo(); return phoso ? 1 : 0;
    }
}
