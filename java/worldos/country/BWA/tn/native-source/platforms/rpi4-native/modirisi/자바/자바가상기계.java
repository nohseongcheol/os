// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. faele/스택/Tshupiso/lekala 경계를 diragatsa_Taelo 중 검사한다. */
public final class 자바가상기계 {
    static int[] faele = new int[16 * 16384], 임시파일 = new int[16384], faele_leina_SMS = new int[512];
    static int[] tlhomameng_theka = new int[8192], 상가 = new int[8192], 상나 = new int[8192], dikwalwa_Tshupiso = new int[8192];
    static int[] mokgwa_leina_SMS = new int[512], mokgwa_tlanya = new int[512], mokgwa_letlelesega = new int[512], mokgwa_mong = new int[512];
    static int[] mokgwa_simolola = new int[512], mokgwa_kgaola = new int[512], mokgwa_kokoanyodinepe = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], mokgwa_Thulaganyo_tlanya = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] e_e_gaufi_Boleng = new int[16384], e_e_gaufi_tlanya = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] Foreimi_mokgwa = new int[128], 틀위치 = new int[128], Foreimi_kokoanyodinepe = new int[128], Foreimi_taelo = new int[128], go_baakanyetsa_tiriso_Foreimi = new int[128];
    static int[] mofuta_Tlhaloso_leina = new int[16], mofuta_Tlhaloso_lekanya = new int[16], 종부모 = new int[16], mofuta_Tlhaloso_kemo = new int[16], 종칸수 = new int[16], go_baakanyetsa_tiriso_mofuta_Tlhaloso = new int[16];
    static int[] mofuta_segokanyi = new int[16 * 16], 종접면수 = new int[16];
    static int[] sebaka_leina = new int[512], sebaka_tlanya = new int[512], sebaka_mong = new int[512], sebaka_ditetla = new int[512], 칸위치 = new int[512], sebaka_tshedimosetso = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], setlhopha_tlhakakaelo = new int[32768], Store_Palotlalo = new int[256];
    static int lekanya, 읽기위치, 함수수, mofuta_leina, Foreimi_tshupane = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int ga_jaana_tlhale, 가닥수 = 1, tsenyo_mofuta_Tlhaloso;
    static int[] tlhale_Foreimi = new int[4], tlhale_kemo = new int[4], tlhale_selwana = new int[4], tlhale_setotwa = new int[4], 가닥대기 = new int[4];
    static boolean phoso, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], mofuta_tlhale = new int[16];

    static void palelo_Boleng(String Lefoko_SMS) {
        if (phoso) return;
        int 분류코드 = 0;
        if (자바도구.같음(Lefoko_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Lefoko_SMS, "NullPointerException") || 자바도구.같음(Lefoko_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Lefoko_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Lefoko_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Lefoko_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Lefoko_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Lefoko_SMS, "IOException: stream closed") || 자바도구.같음(Lefoko_SMS, "IOException: read failed") || 자바도구.같음(Lefoko_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Lefoko_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Lefoko_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && Foreimi_tshupane >= 0) { 예외던짐(분류코드, Lefoko_SMS); return; }
        modirisi.kwala("JVM error: "); modirisi.kwala(Lefoko_SMS); modirisi.kwala_Letshwao_Boleng(10); phoso = true;
    }
    static boolean faelekhutshwe_ya_media(int dirisa, int boleele_Boleng) {
        if (dirisa < 0 || dirisa >= faele.length || boleele_Boleng < 0) return false;
        int mofuta_Tlhaloso = dirisa / 16384;
        return dirisa % 16384 <= mofuta_Tlhaloso_lekanya[mofuta_Tlhaloso] && boleele_Boleng <= mofuta_Tlhaloso_lekanya[mofuta_Tlhaloso] - dirisa % 16384;
    }
    static int baete_Boleng() {
        if (!faelekhutshwe_ya_media(읽기위치, 1)) { palelo_Boleng("truncated class file"); return 0; }
        return faele[읽기위치++];
    }
    static int 짧은수() { return baete_Boleng() << 8 | baete_Boleng(); }
    static int Palotlalo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int boleele_Boleng) { if (!faelekhutshwe_ya_media(읽기위치, boleele_Boleng)) palelo_Boleng("invalid attribute size"); else 읽기위치 += boleele_Boleng; }
    static boolean tlhola_tlhomameng(int 수, int 종류) {
        if (수 <= 0 || 수 >= tlhomameng_theka.length || tlhomameng_theka[수] != 종류) { palelo_Boleng("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int dirisa, int boleele_Boleng, String Lefoko_SMS) {
        if (!faelekhutshwe_ya_media(dirisa, boleele_Boleng)) return false;
        int 읽는자리 = dirisa, 끝 = dirisa + boleele_Boleng;
        for (int lupu_tshupane = 0; lupu_tshupane < Lefoko_SMS.length(); lupu_tshupane++) {
            int khoutuletshwao = Lefoko_SMS.charAt(lupu_tshupane);
            if (khoutuletshwao > 0 && khoutuletshwao < 128) { if (읽는자리 >= 끝 || faele[읽는자리++] != khoutuletshwao) return false; }
            else if (khoutuletshwao < 2048) {
                if (읽는자리 + 2 > 끝 || faele[읽는자리++] != (192 | (khoutuletshwao >> 6)) || faele[읽는자리++] != (128 | (khoutuletshwao & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || faele[읽는자리++] != (224 | (khoutuletshwao >> 12)) || faele[읽는자리++] != (128 | ((khoutuletshwao >> 6) & 63)) || faele[읽는자리++] != (128 | (khoutuletshwao & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int Boleng = 짧은수(); return Boleng == 0 ? 0 : 현재읽는종 * 512 + Boleng; }
    static int 명상수() { return mokgwa_mong[Foreimi_mokgwa[Foreimi_tshupane]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !phoso; 수++) { tlhola_tlhomameng(상번호(), 1); 건너(Palotlalo()); }
    }
    static int Taelo_boleele(int Boleng) {
        if (Boleng == 16 || Boleng == 18 || Boleng == 21 || Boleng == 25 || Boleng == 54 || Boleng == 58 || Boleng == 188) return 2;
        if (Boleng == 17 || Boleng == 19 || Boleng == 132 || Boleng >= 153 && Boleng <= 167
            || Boleng >= 178 && Boleng <= 184 || Boleng == 187 || Boleng == 189 || Boleng == 192 || Boleng == 193 || Boleng == 198 || Boleng == 199) return 3;
        if (Boleng == 185 || Boleng == 200) return 5;
        if (Boleng >= 0 && Boleng <= 8 || Boleng >= 26 && Boleng <= 29 || Boleng >= 42 && Boleng <= 46 || Boleng >= 50 && Boleng <= 53
            || Boleng >= 59 && Boleng <= 62 || Boleng >= 75 && Boleng <= 79 || Boleng >= 83 && Boleng <= 95
            || Boleng == 96 || Boleng == 100 || Boleng == 104 || Boleng == 108 || Boleng == 112 || Boleng == 116
            || Boleng == 120 || Boleng == 122 || Boleng == 124 || Boleng == 126 || Boleng == 128 || Boleng == 130
            || Boleng >= 145 && Boleng <= 147 || Boleng == 172 || Boleng == 176 || Boleng == 177 || Boleng == 190 || Boleng == 191
            || Boleng == 194 || Boleng == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!faelekhutshwe_ya_media(읽는자리, 4)) { palelo_Boleng("truncated bytecode operand"); return 0; }
        return faele[읽는자리] << 24 | faele[읽는자리 + 1] << 16 | faele[읽는자리 + 2] << 8 | faele[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int dirisa, int 끝) {
        int Boleng = faele[읽는자리], boleele_Boleng = Taelo_boleele(Boleng);
        if (Boleng == 170 || Boleng == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - dirisa) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (Boleng == 170 ? 12 : 8)) return 0;
            int 항목수 = Boleng == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            boleele_Boleng = 기준자리 - 읽는자리 + (Boleng == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (Boleng == 196 && 읽는자리 + 1 < 끝) {
            int Lefoko_tshedimosetso = faele[읽는자리 + 1]; boleele_Boleng = Lefoko_tshedimosetso == 132 ? 6 : (Lefoko_tshedimosetso == 21 || Lefoko_tshedimosetso == 25 || Lefoko_tshedimosetso == 54 || Lefoko_tshedimosetso == 58) ? 4 : 0;
        }
        return boleele_Boleng > 0 && boleele_Boleng <= 끝 - 읽는자리 ? boleele_Boleng : 0;
    }
    static void tlhola_bogorogelo_Boleng(int bogorogelo_Boleng, int TIRISO_Boleng) {
        if (bogorogelo_Boleng < mokgwa_simolola[TIRISO_Boleng] || bogorogelo_Boleng >= mokgwa_kgaola[TIRISO_Boleng] || 경계[bogorogelo_Boleng] != TIRISO_Boleng + 1) palelo_Boleng("invalid branch target");
    }
    static void 클래스읽기(int mofuta_Tlhaloso) {
        현재읽는종 = mofuta_Tlhaloso; 읽기위치 = mofuta_Tlhaloso * 16384; lekanya = 읽기위치 + mofuta_Tlhaloso_lekanya[mofuta_Tlhaloso];
        if (Palotlalo() != 0xcafebabe) { palelo_Boleng("not a class file"); return; }
        int 부판 = 짧은수(), kgaolo_Boleng = 짧은수();
        if (kgaolo_Boleng < 45 || kgaolo_Boleng > 52 || 부판 != 0) { palelo_Boleng("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = mofuta_Tlhaloso * 512;
        if (상수수 < 1 || 상수수 > 512) { palelo_Boleng("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !phoso; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = baete_Boleng(); tlhomameng_theka[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = Palotlalo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else palelo_Boleng("unsupported constant type");
        }
        int tetla_Boleng = 짧은수();
        if ((tetla_Boleng & (0x2000 | 0x4000)) != 0) palelo_Boleng("annotation/enum class unsupported");
        mofuta_Tlhaloso_leina[mofuta_Tlhaloso] = mofuta_leina_SMS(상번호());
        종부모[mofuta_Tlhaloso] = mofuta_leina_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { palelo_Boleng("interface count limit"); return; }
        종접면수[mofuta_Tlhaloso] = 접면수;
        for (int lupu_tshupane = 0; lupu_tshupane < 접면수; lupu_tshupane++) mofuta_segokanyi[mofuta_Tlhaloso * 16 + lupu_tshupane] = mofuta_leina_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { palelo_Boleng("field count limit (512)"); return; }
        for (int lupu_tshupane = 0; lupu_tshupane < 필드수 && !phoso; lupu_tshupane++) {
            int faele_tshupane = 칸수++; sebaka_mong[faele_tshupane] = mofuta_Tlhaloso; sebaka_ditetla[faele_tshupane] = 짧은수(); sebaka_leina[faele_tshupane] = 상번호(); sebaka_tlanya[faele_tshupane] = 상번호();
            tlhola_tlhomameng(sebaka_leina[faele_tshupane], 1); tlhola_tlhomameng(sebaka_tlanya[faele_tshupane], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[sebaka_tlanya[faele_tshupane]]; int 분류코드 = 서술형(읽기위치 + 상나[sebaka_tlanya[faele_tshupane]], false); 읽기위치 = 보존값;
            if ((sebaka_ditetla[faele_tshupane] & 8) == 0) 칸위치[faele_tshupane] = 종칸수[mofuta_Tlhaloso]++;
            int nonofo_tshedimosetso = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < nonofo_tshedimosetso && !phoso; 안쪽자리++) {
                int leina_tlhomameng = 상번호(), 유효길이 = Palotlalo();
                if (Lefoko_SMS(leina_tlhomameng, "ConstantValue") && 유효길이 == 2) {
                    int tshedimosetso_Boleng = 상번호();
                    if (분류코드 == 1 && tlhola_tlhomameng(tshedimosetso_Boleng, 3)) sebaka_tshedimosetso[faele_tshupane] = 상가[tshedimosetso_Boleng];
                    else if (분류코드 == 2 && tlhola_tlhomameng(tshedimosetso_Boleng, 8)) sebaka_tshedimosetso[faele_tshupane] = tlhomameng_SMS(상가[tshedimosetso_Boleng]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { palelo_Boleng("method count limit (512)"); return; }
        for (int lupu_tshupane = 0; lupu_tshupane < 개수 && !phoso; lupu_tshupane++) {
            int 수 = 함수수++; mokgwa_mong[수] = mofuta_Tlhaloso;
            mokgwa_letlelesega[수] = 짧은수(); mokgwa_leina_SMS[수] = 상번호(); mokgwa_tlanya[수] = 상번호();
            tlhola_tlhomameng(mokgwa_leina_SMS[수], 1); 서술읽기(수);
            if ((mokgwa_letlelesega[수] & 8) == 0) {
                if (함수인수수[수] == 16) { palelo_Boleng("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) mokgwa_Thulaganyo_tlanya[수 * 16 + 비교자리] = mokgwa_Thulaganyo_tlanya[수 * 16 + 비교자리 - 1];
                mokgwa_Thulaganyo_tlanya[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((mokgwa_letlelesega[수] & 0x100) != 0) palelo_Boleng("user native method unsupported");
            if (Lefoko_SMS(mokgwa_leina_SMS[수], "<clinit>")) go_baakanyetsa_tiriso_mofuta_Tlhaloso[mofuta_Tlhaloso] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (mokgwa_mong[앞] == mofuta_Tlhaloso && 같은말(mokgwa_leina_SMS[앞], mokgwa_leina_SMS[수]) && 같은말(mokgwa_tlanya[앞], mokgwa_tlanya[수])) palelo_Boleng("duplicate method");
            int 속성수 = 짧은수();
            for (int nonofo_Boleng = 0; nonofo_Boleng < 속성수 && !phoso; nonofo_Boleng++) {
                int leina = 상번호(), boleele_Boleng = Palotlalo(), dirisa = 읽기위치;
                if (!faelekhutshwe_ya_media(dirisa, boleele_Boleng)) { palelo_Boleng("truncated method attribute"); break; }
                if (Lefoko_SMS(leina, "Code")) {
                    if (mokgwa_simolola[수] != 0) palelo_Boleng("duplicate Code attribute");
                    mokgwa_kokoanyodinepe[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = Palotlalo();
                    if (mokgwa_kokoanyodinepe[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) palelo_Boleng("method memory limits exceeded");
                    mokgwa_simolola[수] = 읽기위치; 건너(코드길이); mokgwa_kgaola[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { palelo_Boleng("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int phoso_Tshupiso = 잡기수++; 잡기함수[phoso_Tshupiso] = 수;
                        잡기시작[phoso_Tshupiso] = mokgwa_simolola[수] + 짧은수(); 잡기끝[phoso_Tshupiso] = mokgwa_simolola[수] + 짧은수();
                        잡기위치[phoso_Tshupiso] = mokgwa_simolola[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[phoso_Tshupiso] = 부호값 == 0 ? 0 : mofuta_leina_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != dirisa + boleele_Boleng) palelo_Boleng("Code attribute size mismatch");
                } else 건너(boleele_Boleng);
            }
            if ((mokgwa_letlelesega[수] & 0x400) != 0) continue;
            if (mokgwa_simolola[수] == 0) palelo_Boleng("missing Code attribute");
            int sebaka_tsenyo = mokgwa_simolola[수];
            while (sebaka_tsenyo < mokgwa_kgaola[수] && !phoso) {
                int boleele_Boleng = 길이읽기(sebaka_tsenyo, mokgwa_simolola[수], mokgwa_kgaola[수]);
                if (boleele_Boleng == 0) { palelo_Boleng("unsupported or truncated bytecode"); break; }
                경계[sebaka_tsenyo] = 수 + 1; sebaka_tsenyo += boleele_Boleng;
            }
            sebaka_tsenyo = mokgwa_simolola[수];
            while (sebaka_tsenyo < mokgwa_kgaola[수] && !phoso) {
                int Boleng = faele[sebaka_tsenyo];
                if (Boleng >= 153 && Boleng <= 167 || Boleng == 198 || Boleng == 199) tlhola_bogorogelo_Boleng(sebaka_tsenyo + (short)(faele[sebaka_tsenyo + 1] << 8 | faele[sebaka_tsenyo + 2]), 수);
                if (Boleng == 200) tlhola_bogorogelo_Boleng(sebaka_tsenyo + 위치정수(sebaka_tsenyo + 1), 수);
                if (Boleng == 170 || Boleng == 171) {
                    int 읽는자리 = sebaka_tsenyo + 1; while ((읽는자리 - mokgwa_simolola[수]) % 4 != 0) 읽는자리++;
                    tlhola_bogorogelo_Boleng(sebaka_tsenyo + 위치정수(읽는자리), 수);
                    int 항목수 = Boleng == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += Boleng == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) tlhola_bogorogelo_Boleng(sebaka_tsenyo + 위치정수(읽는자리 + 안쪽자리 * (Boleng == 170 ? 4 : 8) + (Boleng == 170 ? 0 : 4)), 수);
                }
                sebaka_tsenyo += 길이읽기(sebaka_tsenyo, mokgwa_simolola[수], mokgwa_kgaola[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                tlhola_bogorogelo_Boleng(잡기시작[안쪽자리], 수); tlhola_bogorogelo_Boleng(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != mokgwa_kgaola[수]) tlhola_bogorogelo_Boleng(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) palelo_Boleng("invalid exception range");
            }
        }
        if (!phoso) 속성건너();
        if (읽기위치 != lekanya) palelo_Boleng("extra class file data");
    }
    static int abela_Polokelo(int 종류, int boleele_Boleng) { return 새기억(종류, boleele_Boleng); }
    static boolean selwana_Boleng(int Tshupiso, int 종류) {
        if (!객체유효(Tshupiso)) return false;
        if (힙[Tshupiso] != 종류) { palelo_Boleng("object type mismatch"); return false; }
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
        if (반환형 == 2) sireletsa_Boleng(스택값[sebaka_tsenyo]);
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
        if (Foreimi_tshupane % 32 == 31) { palelo_Boleng("call stack limit (32)"); return; }
        int 다음 = Foreimi_tshupane + 1;
        for (int 수 = 0; 수 < 128; 수++) e_e_gaufi_tlanya[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[TIRISO_Boleng] - 1; 수 >= 0; 수--) {
            e_e_gaufi_Boleng[다음 * 128 + 수] = 빼기(mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 수]); e_e_gaufi_tlanya[다음 * 128 + 수] = mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 수];
        }
        if (phoso) return;
        Foreimi_tshupane = 다음; go_baakanyetsa_tiriso_Foreimi[Foreimi_tshupane] = 0; Foreimi_mokgwa[Foreimi_tshupane] = TIRISO_Boleng; 틀위치[Foreimi_tshupane] = mokgwa_simolola[TIRISO_Boleng]; Foreimi_kokoanyodinepe[Foreimi_tshupane] = 0;
    }
    static void 반환(int tlanya_Boleng) {
        if (tlanya_Boleng != 함수반환[Foreimi_mokgwa[Foreimi_tshupane]]) { palelo_Boleng("return type mismatch"); return; }
        int Boleng = tlanya_Boleng == 0 ? 0 : 빼기(tlanya_Boleng);
        if (go_baakanyetsa_tiriso_Foreimi[Foreimi_tshupane] != 0) mofuta_Tlhaloso_kemo[go_baakanyetsa_tiriso_Foreimi[Foreimi_tshupane] - 1] = 2;
        if (틀잠금[Foreimi_tshupane] != 0) { 잠금풀기(틀잠금[Foreimi_tshupane]); 틀잠금[Foreimi_tshupane] = 0; }
        Foreimi_tshupane--; if (Foreimi_tshupane >= ga_jaana_tlhale * 32 && tlanya_Boleng != 0) 넣기(Boleng, tlanya_Boleng);
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
                if (Boleng < 1) { palelo_Boleng("invalid file stream path"); return; }
                moela_faele_leina[sebaka_tsenyo] = Boleng;
            }
            moela_faele_leina[boleele_Boleng] = 0;
            int 서술자 = modirisi.파일서술자열기(moela_faele_leina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { palelo_Boleng("FileNotFoundException: file open failed"); return; }
            힙[moela_Boleng + 2] = 서술자; 힙[moela_Boleng + 3] = 1;
            return;
        }
        if (Taelo != 182) { palelo_Boleng("invalid file stream invocation"); return; }
        if ((출력 && Lefoko_SMS(leina, "write") || !출력 && Lefoko_SMS(leina, "read"))
            && (Lefoko_SMS(fometa_Boleng, 출력 ? "([B)V" : "([B)I") || Lefoko_SMS(fometa_Boleng, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean faelekhutshwe_ya_media_Boleng = Lefoko_SMS(fometa_Boleng, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = faelekhutshwe_ya_media_Boleng ? 빼기(1) : 0, 시작점 = faelekhutshwe_ya_media_Boleng ? 빼기(1) : 0, tshedimosetso_setlhopha = 빼기(2), selwana_Tshupiso = 빼기(2);
            if (!selwana_Boleng(tshedimosetso_setlhopha, 20) || !selwana_Boleng(selwana_Tshupiso, 종류)) return;
            if (!faelekhutshwe_ya_media_Boleng) 항목수 = 힙[tshedimosetso_setlhopha + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[tshedimosetso_setlhopha + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[selwana_Tshupiso + 3] == 0 || 힙[selwana_Tshupiso + 2] < 0) { palelo_Boleng("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !phoso) {
                int 반환값 = 출력 ? modirisi.파일한바이트쓰기(힙[selwana_Tshupiso + 2], 힙[tshedimosetso_setlhopha + 2 + 시작점 + 완료수]) : modirisi.파일한바이트읽기(힙[selwana_Tshupiso + 2]);
                if (반환값 < 0) { palelo_Boleng(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[tshedimosetso_setlhopha + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Lefoko_SMS(leina, "flush") && Lefoko_SMS(fometa_Boleng, "()V")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 종류) && 힙[selwana_Tshupiso + 2] < 0) palelo_Boleng("IOException: stream closed"); return; }
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
            if (결과 < -1) palelo_Boleng("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (modirisi.파일한바이트쓰기(서술자, Boleng) != 1) palelo_Boleng("IOException: write failed");
    }
    static void letsa_mokgwa(int tshupane, int Taelo) {
        if (tshupane <= 0 || tshupane >= tlhomameng_theka.length || (tlhomameng_theka[tshupane] != 10 && tlhomameng_theka[tshupane] != 11)) { palelo_Boleng("invalid method reference"); return; }
        int mong_Boleng = mofuta_leina_SMS(상가[tshupane]), leina = Tshupiso_leina(상나[tshupane]), fometa_Boleng = Tshupiso_tlanya(상나[tshupane]);
        if (phoso) return;
        if (기본호출(mong_Boleng, leina, fometa_Boleng, Taelo)) return;
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
        int mofuta_Tlhaloso = batla_mofuta_Tlhaloso(mong_Boleng); if (mofuta_Tlhaloso < 0 || phoso) return;
        int faele_tshupane = batla_mokgwa(mofuta_Tlhaloso, leina, fometa_Boleng);
        if (faele_tshupane < 0) {
            for (int khoutuletshwao = mofuta_Tlhaloso, 항목수 = 0; khoutuletshwao >= 0 && 항목수 < 16; 항목수++, khoutuletshwao = 부모종(khoutuletshwao))
                if (Lefoko_SMS(종부모[khoutuletshwao], "java/lang/Thread")) { 가닥호출(leina, fometa_Boleng, Taelo); return; }
            palelo_Boleng("NoSuchMethodError"); return;
        }
        if (((mokgwa_letlelesega[faele_tshupane] & 8) != 0) != (Taelo == 184)) { palelo_Boleng("method static/instance mismatch"); return; }
        if (Taelo == 184) { if (!go_baakanyetsa_tiriso(mokgwa_mong[faele_tshupane], Foreimi_taelo[Foreimi_tshupane])) return; }
        else {
            int 읽는자리 = Foreimi_kokoanyodinepe[Foreimi_tshupane] - 함수인수수[faele_tshupane];
            if (읽는자리 < 0 || 스택형[Foreimi_tshupane * 128 + 읽는자리] != 2) { palelo_Boleng("invalid method receiver"); return; }
            int selwana_Tshupiso = 스택값[Foreimi_tshupane * 128 + 읽는자리];
            if (!객체유효(selwana_Tshupiso)) return;
            if (힙[selwana_Tshupiso] < 32 || !종포함(힙[selwana_Tshupiso] - 32, mong_Boleng)) { palelo_Boleng("method receiver type mismatch"); return; }
            if (Taelo != 183) faele_tshupane = batla_mokgwa(힙[selwana_Tshupiso] - 32, leina, fometa_Boleng);
        }
        if (faele_tshupane < 0 || (mokgwa_letlelesega[faele_tshupane] & 0x400) != 0) { palelo_Boleng("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((mokgwa_letlelesega[faele_tshupane] & 32) != 0) {
            if (Taelo == 184) { int khoutuletshwao = mokgwa_mong[faele_tshupane]; if (종잠금[khoutuletshwao] == 0) 종잠금[khoutuletshwao] = abela_Polokelo(8, 0); 잠금참조 = 종잠금[khoutuletshwao]; }
            else 잠금참조 = 스택값[Foreimi_tshupane * 128 + Foreimi_kokoanyodinepe[Foreimi_tshupane] - 함수인수수[faele_tshupane]];
            if (!잠금얻기(잠금참조)) { if (!phoso) 틀위치[Foreimi_tshupane] = Foreimi_taelo[Foreimi_tshupane]; return; }
        }
        호출(faele_tshupane); if (!phoso) 틀잠금[Foreimi_tshupane] = 잠금참조;
    }
    static boolean 배열저장가능(int setlhopha_Tshupiso, int tshedimosetso_Boleng) {
        if (tshedimosetso_Boleng == 0 || setlhopha_tlhakakaelo[setlhopha_Tshupiso] == 0) return true;
        boolean 성공여부 = setlhopha_tlhakakaelo[setlhopha_Tshupiso] == -1 ? (tshedimosetso_Boleng > 0 && tshedimosetso_Boleng < 힙끝 && 힙[tshedimosetso_Boleng] == 1) : 맞는객체(tshedimosetso_Boleng, setlhopha_tlhakakaelo[setlhopha_Tshupiso]);
        if (!성공여부 && !phoso) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int setlhopha_sebaka(int Tshupiso, int sekerepitipotlana_Boleng, int tlanya_Boleng) {
        if (!selwana_Boleng(Tshupiso, tlanya_Boleng)) return 0;
        if (sekerepitipotlana_Boleng < 0 || sekerepitipotlana_Boleng >= 힙[Tshupiso + 1]) { palelo_Boleng("ArrayIndexOutOfBoundsException"); return 0; }
        return Tshupiso + 2 + sekerepitipotlana_Boleng;
    }
    static void diragatsa_Taelo() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (phoso) { if (던진객체 != 0) 예외처리(); if (phoso || Foreimi_tshupane < ga_jaana_tlhale * 32) break; }
            if (Foreimi_tshupane < ga_jaana_tlhale * 32 || 바꿈요청 || --조각 == 0) { if (!fetola_tlhale()) break; 조각 = 100; }
            if (Foreimi_tshupane == 0 && mofuta_Tlhaloso_kemo[tsenyo_mofuta_Tlhaloso] != 2 && !go_baakanyetsa_tiriso(tsenyo_mofuta_Tlhaloso, 틀위치[Foreimi_tshupane])) continue;
            if (Foreimi_tshupane == ga_jaana_tlhale * 32 && ga_jaana_tlhale != 0 && (mokgwa_letlelesega[Foreimi_mokgwa[Foreimi_tshupane]] & 32) != 0 && 틀잠금[Foreimi_tshupane] == 0) {
                int selwana_Tshupiso = tlhale_setotwa[ga_jaana_tlhale]; if (!잠금얻기(selwana_Tshupiso)) { if (phoso) break; continue; } 틀잠금[Foreimi_tshupane] = selwana_Tshupiso;
            }
            잠시수 = 0;
            if (--남음 == 0) { palelo_Boleng("instruction limit (500000)"); break; }
            int dirisa = 틀위치[Foreimi_tshupane]; Foreimi_taelo[Foreimi_tshupane] = dirisa; int Boleng = 명바();
            if (phoso) break;
            if (Boleng == 0) continue;
            if (Boleng == 1) { 넣기(0, 2); continue; }
            if (Boleng >= 2 && Boleng <= 8) { 넣기(Boleng - 3, 1); continue; }
            if (Boleng == 16) { 넣기((byte)명바(), 1); continue; }
            if (Boleng == 17) { 넣기((short)명짧(), 1); continue; }
            if (Boleng == 18 || Boleng == 19) {
                int 수 = mokgwa_mong[Foreimi_mokgwa[Foreimi_tshupane]] * 512 + (Boleng == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= tlhomameng_theka.length) palelo_Boleng("invalid ldc constant");
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
            if (Boleng == 46 || Boleng >= 50 && Boleng <= 53) {
                int 항목자리 = 빼기(1), selwana_Tshupiso = 빼기(2), 분류코드 = Boleng == 46 ? 2 : Boleng == 50 ? 3 : Boleng == 51 ? 20 : Boleng == 52 ? 22 : 23;
                if (Boleng == 51 && selwana_Tshupiso > 0 && selwana_Tshupiso < 힙끝 && 힙[selwana_Tshupiso] == 21) 분류코드 = 21;
                int 읽는자리 = setlhopha_sebaka(selwana_Tshupiso, 항목자리, 분류코드); if (!phoso) 넣기(힙[읽는자리], Boleng == 50 ? 2 : 1); continue;
            }
            if (Boleng == 79 || Boleng >= 83 && Boleng <= 86) {
                int tsenyo_Tshupiso = 빼기(Boleng == 83 ? 2 : 1), 항목자리 = 빼기(1), selwana_Tshupiso = 빼기(2), 분류코드 = Boleng == 79 ? 2 : Boleng == 83 ? 3 : Boleng == 84 ? 20 : Boleng == 85 ? 22 : 23;
                if (Boleng == 84 && selwana_Tshupiso > 0 && selwana_Tshupiso < 힙끝 && 힙[selwana_Tshupiso] == 21) 분류코드 = 21;
                int 읽는자리 = setlhopha_sebaka(selwana_Tshupiso, 항목자리, 분류코드);
                if (!phoso && 분류코드 == 3 && !배열저장가능(selwana_Tshupiso, tsenyo_Tshupiso)) continue;
                if (!phoso) 힙[읽는자리] = 분류코드 == 20 ? (byte)tsenyo_Tshupiso : 분류코드 == 21 ? tsenyo_Tshupiso & 1 : 분류코드 == 22 ? (char)tsenyo_Tshupiso : 분류코드 == 23 ? (short)tsenyo_Tshupiso : tsenyo_Tshupiso;
                continue;
            }
            if (Boleng >= 87 && Boleng <= 95) { kokoanyodinepe_taelo(Boleng); continue; }
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
            if (Boleng >= 178 && Boleng <= 181) { 필드호출(명상수(), Boleng, dirisa); continue; }
            if (Boleng >= 182 && Boleng <= 185) {
                int 부호값 = 명상수();
                if (Boleng == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { palelo_Boleng("invalid invokeinterface operands"); continue; } }
                letsa_mokgwa(부호값, Boleng); continue;
            }
            if (Boleng == 187) { 새객체(mofuta_leina_SMS(명상수()), dirisa); continue; }
            if (Boleng == 188 || Boleng == 189) {
                int 분류코드 = 3, karolwana = 0;
                if (Boleng == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else karolwana = mofuta_leina_SMS(명상수());
                if (분류코드 == 0) { palelo_Boleng("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), selwana_Tshupiso = abela_Polokelo(분류코드, 유효길이); if (!phoso) setlhopha_tlhakakaelo[selwana_Tshupiso] = karolwana; 넣기(selwana_Tshupiso, 2); continue;
            }
            if (Boleng == 190) {
                int selwana_Tshupiso = 빼기(2);
                if (객체유효(selwana_Tshupiso)) { int 비교자리 = 힙[selwana_Tshupiso]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) palelo_Boleng("not an array"); else 넣기(힙[selwana_Tshupiso + 1], 1); }
                continue;
            }
            if (Boleng == 191) {
                int selwana_Tshupiso = 빼기(2); if (객체유효(selwana_Tshupiso)) { if (힙[selwana_Tshupiso] != 9) palelo_Boleng("athrow requires supported Throwable"); else { 던진객체 = selwana_Tshupiso; phoso = true; } }
                continue;
            }
            if (Boleng == 192 || Boleng == 193) {
                int leina_tlhomameng = mofuta_leina_SMS(명상수()), selwana_Tshupiso = 빼기(2); boolean 일치여부 = 맞는객체(selwana_Tshupiso, leina_tlhomameng);
                if (Boleng == 193) 넣기(selwana_Tshupiso != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !phoso) palelo_Boleng("ClassCastException"); 넣기(selwana_Tshupiso, 2); }
                continue;
            }
            if (Boleng == 170 || Boleng == 171) {
                int 읽는자리 = dirisa + 1, faele_tshupane = Foreimi_mokgwa[Foreimi_tshupane], taetsi_Tshupiso = 빼기(1);
                while ((읽는자리 - mokgwa_simolola[faele_tshupane]) % 4 != 0) 읽는자리++;
                int setotwa_aterese = 위치정수(읽는자리);
                if (Boleng == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (taetsi_Tshupiso >= 낮은값 && taetsi_Tshupiso <= 높은값) setotwa_aterese = 위치정수(읽는자리 + 12 + (taetsi_Tshupiso - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int lupu_tshupane = 0; lupu_tshupane < 총수; lupu_tshupane++) if (위치정수(읽는자리 + 8 + lupu_tshupane * 8) == taetsi_Tshupiso) setotwa_aterese = 위치정수(읽는자리 + 12 + lupu_tshupane * 8); }
                sutisa_Boleng(dirisa + setotwa_aterese); continue;
            }
            if (Boleng == 200) { sutisa_Boleng(dirisa + 위치정수(dirisa + 1)); continue; }
            if (Boleng == 194 || Boleng == 195) {
                int selwana_Tshupiso = 빼기(2);
                if (Boleng == 195) 잠금풀기(selwana_Tshupiso);
                else if (!잠금얻기(selwana_Tshupiso) && !phoso) { 넣기(selwana_Tshupiso, 2); 틀위치[Foreimi_tshupane] = dirisa; }
                continue;
            }
            if (Boleng == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) kwala_e_e_gaufi(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); kwala_e_e_gaufi(항목자리, 1); }
                else palelo_Boleng("unsupported wide opcode");
                continue;
            }
            palelo_Boleng("unsupported bytecode");
        }
    }
    static int batla_mofuta_Tlhaloso(int leina) {
        for (int lupu_tshupane = 0; lupu_tshupane < 종수; lupu_tshupane++) if (mofuta_Tlhaloso_leina[lupu_tshupane] != 0 && 같은말(mofuta_Tlhaloso_leina[lupu_tshupane], leina)) return lupu_tshupane;
        return tsenya_mofuta_Tlhaloso(tlhomameng_SMS(leina));
    }
    static int tsenya_mofuta_Tlhaloso(int leina_dikwalwa) {
        if (!selwana_Boleng(leina_dikwalwa, 1)) return -1;
        int boleele_Boleng = 힙[leina_dikwalwa + 1];
        if (boleele_Boleng < 1 || boleele_Boleng > 505 || 종수 == 16) { palelo_Boleng("class name/count limit"); return -1; }
        for (int lupu_tshupane = 0; lupu_tshupane < boleele_Boleng; lupu_tshupane++) { int khoutuletshwao = 힙[leina_dikwalwa + 2 + lupu_tshupane]; faele_leina_SMS[lupu_tshupane] = khoutuletshwao == '/' ? '.' : khoutuletshwao; }
        faele_leina_SMS[boleele_Boleng] = '.'; faele_leina_SMS[boleele_Boleng + 1] = 'c'; faele_leina_SMS[boleele_Boleng + 2] = 'l'; faele_leina_SMS[boleele_Boleng + 3] = 'a'; faele_leina_SMS[boleele_Boleng + 4] = 's'; faele_leina_SMS[boleele_Boleng + 5] = 's'; faele_leina_SMS[boleele_Boleng + 6] = 0;
        int lekanya = modirisi.파일읽기(faele_leina_SMS, 임시파일);
        if (lekanya < 0) { palelo_Boleng("ClassNotFoundException"); return -1; }
        int mofuta_Tlhaloso = 종수++; mofuta_Tlhaloso_lekanya[mofuta_Tlhaloso] = lekanya;
        for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) faele[mofuta_Tlhaloso * 16384 + lupu_tshupane] = 임시파일[lupu_tshupane];
        클래스읽기(mofuta_Tlhaloso); if (phoso) return -1;
        int tota_tshedimosetso = tlhomameng_SMS(mofuta_Tlhaloso_leina[mofuta_Tlhaloso]);
        if (!글같음(tota_tshedimosetso, leina_dikwalwa, true)) { palelo_Boleng("class name does not match file"); return -1; }
        int 부모 = 종부모[mofuta_Tlhaloso];
        if (부모 != 0 && !Lefoko_SMS(부모, "java/lang/Object") && !Lefoko_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = batla_mofuta_Tlhaloso(부모);
            if (phoso || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == mofuta_Tlhaloso) { palelo_Boleng("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int faele_tshupane = 0; faele_tshupane < 칸수; faele_tshupane++) if (sebaka_mong[faele_tshupane] == mofuta_Tlhaloso && (sebaka_ditetla[faele_tshupane] & 8) == 0) 칸위치[faele_tshupane] += 시작변위;
            종칸수[mofuta_Tlhaloso] += 시작변위;
        }
        return mofuta_Tlhaloso;
    }
    static int 부모종(int mofuta_Tlhaloso) {
        int leina = 종부모[mofuta_Tlhaloso];
        for (int lupu_tshupane = 0; lupu_tshupane < 종수; lupu_tshupane++) if (leina != 0 && mofuta_Tlhaloso_leina[lupu_tshupane] != 0 && 같은말(mofuta_Tlhaloso_leina[lupu_tshupane], leina)) return lupu_tshupane;
        return -1;
    }
    static int batla_mokgwa(int mofuta_Tlhaloso, int leina, int fometa_Boleng) {
        for (int 깊이 = 0; mofuta_Tlhaloso >= 0 && 깊이 < 16; 깊이++, mofuta_Tlhaloso = 부모종(mofuta_Tlhaloso)) {
            for (int lupu_tshupane = 0; lupu_tshupane < 함수수; lupu_tshupane++) if (mokgwa_mong[lupu_tshupane] == mofuta_Tlhaloso && 같은말(mokgwa_leina_SMS[lupu_tshupane], leina) && 같은말(mokgwa_tlanya[lupu_tshupane], fometa_Boleng)) return lupu_tshupane;
        }
        return -1;
    }
    static int leina_mokgwa(int mofuta_Tlhaloso, String leina, String fometa_Boleng) {
        for (int 깊이 = 0; mofuta_Tlhaloso >= 0 && 깊이 < 16; 깊이++, mofuta_Tlhaloso = 부모종(mofuta_Tlhaloso))
            for (int lupu_tshupane = 0; lupu_tshupane < 함수수; lupu_tshupane++) if (mokgwa_mong[lupu_tshupane] == mofuta_Tlhaloso && Lefoko_SMS(mokgwa_leina_SMS[lupu_tshupane], leina) && Lefoko_SMS(mokgwa_tlanya[lupu_tshupane], fometa_Boleng)) return lupu_tshupane;
        return -1;
    }
    static int 형종류(int leina) { return faele[상가[leina]] == 'L' || faele[상가[leina]] == '[' ? 2 : 1; }
    static boolean go_baakanyetsa_tiriso(int mofuta_Tlhaloso, int Taelo_simolola) {
        if (mofuta_Tlhaloso < 0 || phoso) return false;
        if (mofuta_Tlhaloso_kemo[mofuta_Tlhaloso] == 3) { palelo_Boleng("NoClassDefFoundError: initialization failed"); return false; }
        if (mofuta_Tlhaloso_kemo[mofuta_Tlhaloso] == 1 && mofuta_tlhale[mofuta_Tlhaloso] != ga_jaana_tlhale) { 틀위치[Foreimi_tshupane] = Taelo_simolola; 바꿈요청 = true; return false; }
        if (mofuta_Tlhaloso_kemo[mofuta_Tlhaloso] != 0) return true;
        int 위 = 부모종(mofuta_Tlhaloso);
        if (위 >= 0 && !go_baakanyetsa_tiriso(위, Taelo_simolola)) return false;
        mofuta_Tlhaloso_kemo[mofuta_Tlhaloso] = 1; mofuta_tlhale[mofuta_Tlhaloso] = ga_jaana_tlhale;
        if (go_baakanyetsa_tiriso_mofuta_Tlhaloso[mofuta_Tlhaloso] != 0) {
            틀위치[Foreimi_tshupane] = Taelo_simolola;
            호출(go_baakanyetsa_tiriso_mofuta_Tlhaloso[mofuta_Tlhaloso] - 1); if (!phoso) go_baakanyetsa_tiriso_Foreimi[Foreimi_tshupane] = mofuta_Tlhaloso + 1;
            return false;
        }
        mofuta_Tlhaloso_kemo[mofuta_Tlhaloso] = 2; return true;
    }
    static void 필드호출(int tshupane, int Taelo, int dirisa) {
        if (!tlhola_tlhomameng(tshupane, 9)) return;
        int mong_Boleng = mofuta_leina_SMS(상가[tshupane]), leina = Tshupiso_leina(상나[tshupane]), fometa_Boleng = Tshupiso_tlanya(상나[tshupane]);
        if (Lefoko_SMS(mong_Boleng, "java/lang/System") && (Lefoko_SMS(leina, "out") || Lefoko_SMS(leina, "err")) && Lefoko_SMS(fometa_Boleng, "Ljava/io/PrintStream;") && Taelo == 178) { 넣기(-1, 2); return; }
        int mofuta_Tlhaloso = batla_mofuta_Tlhaloso(mong_Boleng); if (mofuta_Tlhaloso < 0 || phoso) return;
        int 찾음 = -1;
        for (int 읽는자리 = mofuta_Tlhaloso, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int faele_tshupane = 0; faele_tshupane < 칸수; faele_tshupane++) if (sebaka_mong[faele_tshupane] == 읽는자리 && 같은말(sebaka_leina[faele_tshupane], leina) && 같은말(sebaka_tlanya[faele_tshupane], fometa_Boleng)) 찾음 = faele_tshupane;
        if (찾음 < 0) { palelo_Boleng("NoSuchFieldError"); return; }
        boolean e_e_emeng_Boleng = Taelo == 178 || Taelo == 179;
        if (e_e_emeng_Boleng != ((sebaka_ditetla[찾음] & 8) != 0)) { palelo_Boleng("field static/instance mismatch"); return; }
        if (e_e_emeng_Boleng && !go_baakanyetsa_tiriso(sebaka_mong[찾음], dirisa)) return;
        int tlanya_Boleng = 형종류(fometa_Boleng), Boleng = 0;
        if (Taelo == 179 || Taelo == 181) Boleng = 빼기(tlanya_Boleng);
        if (e_e_emeng_Boleng) { if (Taelo == 178) 넣기(sebaka_tshedimosetso[찾음], tlanya_Boleng); else if (!phoso) sebaka_tshedimosetso[찾음] = Boleng; return; }
        int selwana_Tshupiso = 빼기(2);
        if (!객체유효(selwana_Tshupiso)) return;
        if (힙[selwana_Tshupiso] < 32 || !종포함(힙[selwana_Tshupiso] - 32, mong_Boleng)) { palelo_Boleng("field receiver type mismatch"); return; }
        int 보관칸 = selwana_Tshupiso + 2 + 칸위치[찾음];
        if (Taelo == 180) 넣기(힙[보관칸], tlanya_Boleng);
        else if (!phoso) { 힙[보관칸] = Boleng; 힙참조[보관칸] = tlanya_Boleng == 2 ? 1 : 0; }
    }
    static boolean 종포함(int mofuta_Tlhaloso, int leina) {
        for (int 중첩깊이 = 0; mofuta_Tlhaloso >= 0 && 중첩깊이 < 16; 중첩깊이++, mofuta_Tlhaloso = 부모종(mofuta_Tlhaloso)) {
            if (같은말(mofuta_Tlhaloso_leina[mofuta_Tlhaloso], leina) || (종부모[mofuta_Tlhaloso] != 0 && 같은말(종부모[mofuta_Tlhaloso], leina))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[mofuta_Tlhaloso]; 안쪽자리++) if (같은말(mofuta_segokanyi[mofuta_Tlhaloso * 16 + 안쪽자리], leina)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int baete_tshedimosetso, boolean tsela) {
        if (첫값 == baete_tshedimosetso) return true;
        if (첫값 <= 0 || baete_tshedimosetso <= 0 || 힙[첫값] != 1 || 힙[baete_tshedimosetso] != 1 || 힙[첫값 + 1] != 힙[baete_tshedimosetso + 1]) return false;
        for (int lupu_tshupane = 0; lupu_tshupane < 힙[첫값 + 1]; lupu_tshupane++) {
            int kgokagano_ya_x = 힙[첫값 + 2 + lupu_tshupane], 세로좌표 = 힙[baete_tshedimosetso + 2 + lupu_tshupane];
            if (tsela) { if (kgokagano_ya_x == '.') kgokagano_ya_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (kgokagano_ya_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int selwana_Tshupiso) {
        if (selwana_Tshupiso == 0) { palelo_Boleng("NullPointerException"); return false; }
        if (selwana_Tshupiso < 1 || selwana_Tshupiso >= 힙끝 || 힙폭[selwana_Tshupiso] < 2 || 힙[selwana_Tshupiso] == 0) { palelo_Boleng("invalid object reference"); return false; }
        return true;
    }
    static void sireletsa_Boleng(int selwana_Tshupiso) {
        if (selwana_Tshupiso > 0 && selwana_Tshupiso < 힙끝 && 힙폭[selwana_Tshupiso] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = selwana_Tshupiso;
    }
    static void bontsha_Boleng(int selwana_Tshupiso) {
        if (selwana_Tshupiso > 0 && selwana_Tshupiso < 힙끝 && 힙폭[selwana_Tshupiso] >= 2 && 힙[selwana_Tshupiso] != 0 && 힙표시[selwana_Tshupiso] == 0) {
            힙표시[selwana_Tshupiso] = 1; 표시대기[표시수++] = selwana_Tshupiso;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int lupu_tshupane = 0; lupu_tshupane < dikwalwa_Tshupiso.length; lupu_tshupane++) bontsha_Boleng(dikwalwa_Tshupiso[lupu_tshupane]);
        for (int lupu_tshupane = 0; lupu_tshupane < 칸수; lupu_tshupane++) if ((sebaka_ditetla[lupu_tshupane] & 8) != 0 && 형종류(sebaka_tlanya[lupu_tshupane]) == 2) bontsha_Boleng(sebaka_tshedimosetso[lupu_tshupane]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            bontsha_Boleng(tlhale_selwana[임시값]); bontsha_Boleng(tlhale_setotwa[임시값]);
            int 꼭대기자리 = 임시값 == ga_jaana_tlhale ? Foreimi_tshupane : tlhale_Foreimi[임시값];
            for (int faele_tshupane = 임시값 * 32; faele_tshupane <= 꼭대기자리; faele_tshupane++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[Foreimi_mokgwa[faele_tshupane]]; 안쪽자리++) if (e_e_gaufi_tlanya[faele_tshupane * 128 + 안쪽자리] == 2) bontsha_Boleng(e_e_gaufi_Boleng[faele_tshupane * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < Foreimi_kokoanyodinepe[faele_tshupane]; 안쪽자리++) if (스택형[faele_tshupane * 128 + 안쪽자리] == 2) bontsha_Boleng(스택값[faele_tshupane * 128 + 안쪽자리]);
            }
        }
        for (int lupu_tshupane = 0; lupu_tshupane < 화면참조.length; lupu_tshupane++) bontsha_Boleng(화면참조[lupu_tshupane]);
        for (int lupu_tshupane = 0; lupu_tshupane < 나중수; lupu_tshupane++) bontsha_Boleng(나중실행[lupu_tshupane]);
        for (int lupu_tshupane = 0; lupu_tshupane < Store_Palotlalo.length; lupu_tshupane++) bontsha_Boleng(Store_Palotlalo[lupu_tshupane]);
        for (int lupu_tshupane = 0; lupu_tshupane < 종수; lupu_tshupane++) bontsha_Boleng(종잠금[lupu_tshupane]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) bontsha_Boleng(검사자리);
        bontsha_Boleng(던진객체);
        for (int lupu_tshupane = 0; lupu_tshupane < 잠시수; lupu_tshupane++) bontsha_Boleng(잠시참조[lupu_tshupane]);
        while (표시수 > 0) {
            int selwana_Tshupiso = 표시대기[--표시수], 분류코드 = 힙[selwana_Tshupiso];
            for (int lupu_tshupane = selwana_Tshupiso + 2; lupu_tshupane < selwana_Tshupiso + 힙폭[selwana_Tshupiso]; lupu_tshupane++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[lupu_tshupane] != 0) bontsha_Boleng(힙[lupu_tshupane]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int boleele_Boleng) {
        if (boleele_Boleng < 0) { palelo_Boleng("NegativeArraySizeException"); return 0; }
        if (boleele_Boleng > 힙.length - 3) { palelo_Boleng("object heap exhausted"); return 0; }
        int 필요수 = boleele_Boleng + 2, selwana_Tshupiso = 0;
        if (필요수 <= 힙.length - 힙끝) { selwana_Tshupiso = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { selwana_Tshupiso = 읽는자리; break; }
            if (selwana_Tshupiso != 0) {
                int 남은길이 = 힙폭[selwana_Tshupiso] - 필요수;
                if (남은길이 >= 2) { 힙폭[selwana_Tshupiso + 필요수] = 남은길이; 힙[selwana_Tshupiso + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { selwana_Tshupiso = 힙끝; 힙끝 += 필요수; }
        }
        if (selwana_Tshupiso == 0) { palelo_Boleng("object heap exhausted"); return 0; }
        for (int lupu_tshupane = 0; lupu_tshupane < 필요수; lupu_tshupane++) { 힙[selwana_Tshupiso + lupu_tshupane] = 0; 힙참조[selwana_Tshupiso + lupu_tshupane] = 0; 힙폭[selwana_Tshupiso + lupu_tshupane] = 0; }
        setlhopha_tlhakakaelo[selwana_Tshupiso] = 0;
        힙폭[selwana_Tshupiso] = 필요수; 힙[selwana_Tshupiso] = 종류; 힙[selwana_Tshupiso + 1] = boleele_Boleng; sireletsa_Boleng(selwana_Tshupiso); return selwana_Tshupiso;
    }
    static int 예외종(String leina_tlhomameng) {
        if (자바도구.같음(leina_tlhomameng, "java/lang/Throwable")) return 1;
        if (자바도구.같음(leina_tlhomameng, "java/lang/Exception")) return 2;
        if (자바도구.같음(leina_tlhomameng, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(leina_tlhomameng, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(leina_tlhomameng, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(leina_tlhomameng, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(leina_tlhomameng, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(leina_tlhomameng, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(leina_tlhomameng, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(leina_tlhomameng, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(leina_tlhomameng, "java/io/IOException")) return 11;
        if (자바도구.같음(leina_tlhomameng, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(leina_tlhomameng, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(leina_tlhomameng, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(leina_tlhomameng, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int leina) {
        for (int lupu_tshupane = 1; lupu_tshupane <= 41; lupu_tshupane++) if (Lefoko_SMS(leina, 예외이름(lupu_tshupane))) return lupu_tshupane;
        return 0;
    }
    static String 예외이름(int itshupo_Boleng) {
        if (itshupo_Boleng == 40) return "java/lang/InterruptedException";
        if (itshupo_Boleng == 41) return "한국어/자체/대기중단예외";
        if (itshupo_Boleng == 39) return "java/net/SocketException";
        if (itshupo_Boleng == 20) return "한국어/자체/예외";
        if (itshupo_Boleng == 21) return "한국어/자체/실행예외";
        if (itshupo_Boleng == 22) return "한국어/자체/입출력예외";
        if (itshupo_Boleng == 23) return "한국어/자체/대기시간초과예외";
        if (itshupo_Boleng == 24) return "한국어/자체/주소확인예외";
        if (itshupo_Boleng == 25) return "한국어/자체/파일없음예외";
        if (itshupo_Boleng == 26) return "한국어/자체/통신예외";
        if (itshupo_Boleng == 27) return "한국어/자체/잘못된인수예외";
        if (itshupo_Boleng == 28) return "한국어/자체/숫자형식예외";
        if (itshupo_Boleng == 29) return "한국어/자체/범위예외";
        if (itshupo_Boleng == 30) return "한국어/자체/배열범위예외";
        if (itshupo_Boleng == 31) return "한국어/자체/문자열범위예외";
        if (itshupo_Boleng == 32) return "한국어/자체/빈참조예외";
        if (itshupo_Boleng == 33) return "한국어/자체/산술예외";
        if (itshupo_Boleng == 34) return "한국어/자체/상태예외";
        if (itshupo_Boleng == 35) return "한국어/자체/형변환예외";
        if (itshupo_Boleng == 36) return "한국어/자체/음수배열크기예외";
        if (itshupo_Boleng == 37) return "한국어/자체/setlhopha_Store_palelo";
        if (itshupo_Boleng == 38) return "한국어/자체/가닥상태예외";
        if (itshupo_Boleng == 1) return "java/lang/Throwable"; if (itshupo_Boleng == 2) return "java/lang/Exception";
        if (itshupo_Boleng == 3) return "java/lang/RuntimeException"; if (itshupo_Boleng == 4) return "java/lang/ArithmeticException";
        if (itshupo_Boleng == 5) return "java/lang/NullPointerException"; if (itshupo_Boleng == 6) return "java/lang/IndexOutOfBoundsException";
        if (itshupo_Boleng == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (itshupo_Boleng == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (itshupo_Boleng == 9) return "java/lang/IllegalArgumentException"; if (itshupo_Boleng == 10) return "java/lang/NumberFormatException";
        if (itshupo_Boleng == 11) return "java/io/IOException"; if (itshupo_Boleng == 12) return "java/io/FileNotFoundException";
        if (itshupo_Boleng == 17) return "java/lang/ArrayStoreException";
        if (itshupo_Boleng == 18) return "java/net/UnknownHostException";
        if (itshupo_Boleng == 19) return "java/net/SocketTimeoutException";
        if (itshupo_Boleng == 16) return "java/lang/IllegalThreadStateException";
        if (itshupo_Boleng == 13) return "java/lang/IllegalStateException"; if (itshupo_Boleng == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int itshupo_Boleng) {
        if (itshupo_Boleng == 40) return 2;
        if (itshupo_Boleng == 41) return 40;
        if (itshupo_Boleng == 39) return 11;
        if (itshupo_Boleng == 1) return 0;
        if (itshupo_Boleng == 2) return 1;
        if (itshupo_Boleng == 3) return 2;
        if (itshupo_Boleng == 4) return 3;
        if (itshupo_Boleng == 5) return 3;
        if (itshupo_Boleng == 6) return 3;
        if (itshupo_Boleng == 7) return 6;
        if (itshupo_Boleng == 8) return 6;
        if (itshupo_Boleng == 9) return 3;
        if (itshupo_Boleng == 10) return 9;
        if (itshupo_Boleng == 11) return 2;
        if (itshupo_Boleng == 12) return 11;
        if (itshupo_Boleng == 13) return 3;
        if (itshupo_Boleng == 14) return 3;
        if (itshupo_Boleng == 15) return 3;
        if (itshupo_Boleng == 16) return 9;
        if (itshupo_Boleng == 17) return 3;
        if (itshupo_Boleng == 18) return 11;
        if (itshupo_Boleng == 19) return 11;
        if (itshupo_Boleng == 20) return 2;
        if (itshupo_Boleng == 21) return 3;
        if (itshupo_Boleng == 22) return 11;
        if (itshupo_Boleng == 23) return 22;
        if (itshupo_Boleng == 24) return 22;
        if (itshupo_Boleng == 25) return 22;
        if (itshupo_Boleng == 26) return 22;
        if (itshupo_Boleng == 27) return 9;
        if (itshupo_Boleng == 28) return 27;
        if (itshupo_Boleng == 29) return 6;
        if (itshupo_Boleng == 30) return 29;
        if (itshupo_Boleng == 31) return 29;
        if (itshupo_Boleng == 32) return 5;
        if (itshupo_Boleng == 33) return 4;
        if (itshupo_Boleng == 34) return 13;
        if (itshupo_Boleng == 35) return 14;
        if (itshupo_Boleng == 36) return 15;
        if (itshupo_Boleng == 37) return 17;
        if (itshupo_Boleng == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int tota_Boleng, int 요구값) {
        for (int 깊이 = 0; tota_Boleng != 0 && 깊이 < 16; 깊이++, tota_Boleng = 예외부모(tota_Boleng))
            if (tota_Boleng == 요구값) return true;
        return false;
    }
    static void 예외던짐(int itshupo_Boleng, String MPUISE_Tshupiso) {
        int selwana_Tshupiso = 새기억(9, 2); if (phoso) return;
        힙[selwana_Tshupiso + 2] = itshupo_Boleng; 힙[selwana_Tshupiso + 3] = pinagare_Letshwao(MPUISE_Tshupiso); 힙참조[selwana_Tshupiso + 3] = 1;
        던진객체 = selwana_Tshupiso; phoso = true;
    }
    static boolean 맞는객체(int selwana_Tshupiso, int leina) {
        if (selwana_Tshupiso == 0) return true;
        if (!객체유효(selwana_Tshupiso)) return false;
        int 분류코드 = 힙[selwana_Tshupiso];
        if (Lefoko_SMS(leina, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, leina);
        if (분류코드 == 9) { int setotwa_aterese = 예외상수(leina); return setotwa_aterese != 0 && 예외포함(힙[selwana_Tshupiso + 2], setotwa_aterese); }
        if (분류코드 == 1) return Lefoko_SMS(leina, "java/lang/String") || Lefoko_SMS(leina, "java/lang/CharSequence");
        if (분류코드 == 4) return Lefoko_SMS(leina, "java/lang/StringBuilder") || Lefoko_SMS(leina, "java/lang/CharSequence");
        if (분류코드 == 10) return Lefoko_SMS(leina, "java/util/ArrayList") || Lefoko_SMS(leina, "java/util/List");
        if (분류코드 == 11) return Lefoko_SMS(leina, "java/util/HashMap") || Lefoko_SMS(leina, "java/util/Map");
        if (분류코드 == 12) return Lefoko_SMS(leina, "java/lang/Integer") || Lefoko_SMS(leina, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[selwana_Tshupiso + 13] != 0) return 한국어화면종(leina) == 분류코드 || Lefoko_SMS(leina, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(leina) == 0 && 화면종(leina) == 분류코드) || Lefoko_SMS(leina, "java/awt/Component") || Lefoko_SMS(leina, "java/awt/Container") || Lefoko_SMS(leina, "javax/swing/JComponent");
        if (분류코드 == 29) return Lefoko_SMS(leina, 힙[selwana_Tshupiso + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Lefoko_SMS(leina, "java/awt/FlowLayout") || Lefoko_SMS(leina, "java/awt/LayoutManager");
        if (분류코드 == 17) return Lefoko_SMS(leina, "java/net/Socket");
        if (분류코드 == 18) return Lefoko_SMS(leina, "java/net/ServerSocket");
        if (분류코드 == 19) return Lefoko_SMS(leina, 힙[selwana_Tshupiso + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Lefoko_SMS(leina, "java/net/InetAddress");
        if (분류코드 == 15) return Lefoko_SMS(leina, "java/net/DatagramSocket");
        if (분류코드 == 16) return Lefoko_SMS(leina, "java/net/DatagramPacket");
        if (분류코드 == 13) return Lefoko_SMS(leina, 힙[selwana_Tshupiso + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Lefoko_SMS(leina, "[I"); if (분류코드 == 20) return Lefoko_SMS(leina, "[B"); if (분류코드 == 21) return Lefoko_SMS(leina, "[Z");
        if (분류코드 == 22) return Lefoko_SMS(leina, "[C"); if (분류코드 == 23) return Lefoko_SMS(leina, "[S");
        if (분류코드 != 3) return false;
        if (Lefoko_SMS(leina, "[Ljava/lang/Object;")) return true;
        int karolwana = setlhopha_tlhakakaelo[selwana_Tshupiso];
        if (karolwana == -1) return Lefoko_SMS(leina, "[Ljava/lang/String;") || Lefoko_SMS(leina, "[Ljava/lang/CharSequence;");
        if (karolwana == 0) return false;
        if (배열종비교(karolwana, leina)) return true;
        if ((Lefoko_SMS(karolwana, "java/lang/String") || Lefoko_SMS(karolwana, "java/lang/StringBuilder")) && Lefoko_SMS(leina, "[Ljava/lang/CharSequence;")) return true;
        for (int lupu_tshupane = 0; lupu_tshupane < 종수; lupu_tshupane++) if (같은말(mofuta_Tlhaloso_leina[lupu_tshupane], karolwana)) {
            for (int khoutuletshwao = lupu_tshupane, 중첩깊이 = 0; khoutuletshwao >= 0 && 중첩깊이 < 16; 중첩깊이++, khoutuletshwao = 부모종(khoutuletshwao)) {
                if (배열종비교(종부모[khoutuletshwao], leina)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[khoutuletshwao]; 안쪽자리++) if (배열종비교(mofuta_segokanyi[khoutuletshwao * 16 + 안쪽자리], leina)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int leina_tlhomameng, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (leina_tlhomameng == 0 || 항목수 < 4 || faele[검사자리] != '[' || faele[검사자리 + 1] != 'L' || faele[검사자리 + 항목수 - 1] != ';' || 상나[leina_tlhomameng] != 항목수 - 3) return false;
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수 - 3; lupu_tshupane++) if (faele[상가[leina_tlhomameng] + lupu_tshupane] != faele[검사자리 + 2 + lupu_tshupane]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        phoso = false;
        while (Foreimi_tshupane >= ga_jaana_tlhale * 32) {
            int faele_tshupane = Foreimi_mokgwa[Foreimi_tshupane], 읽는자리 = Foreimi_taelo[Foreimi_tshupane];
            for (int lupu_tshupane = 0; lupu_tshupane < 잡기수; lupu_tshupane++) if (잡기함수[lupu_tshupane] == faele_tshupane && 읽는자리 >= 잡기시작[lupu_tshupane] && 읽는자리 < 잡기끝[lupu_tshupane]
                && (잡기종[lupu_tshupane] == 0 || 맞는객체(던진객체, 잡기종[lupu_tshupane]))) {
                틀위치[Foreimi_tshupane] = 잡기위치[lupu_tshupane]; Foreimi_kokoanyodinepe[Foreimi_tshupane] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (go_baakanyetsa_tiriso_Foreimi[Foreimi_tshupane] != 0) mofuta_Tlhaloso_kemo[go_baakanyetsa_tiriso_Foreimi[Foreimi_tshupane] - 1] = 3;
            if (틀잠금[Foreimi_tshupane] != 0) { 잠금풀기(틀잠금[Foreimi_tshupane]); 틀잠금[Foreimi_tshupane] = 0; }
            Foreimi_tshupane--;
        }
        modirisi.kwala("Uncaught ");
        if (힙[던진객체] == 9) { modirisi.kwala(예외이름(힙[던진객체 + 2])); modirisi.kwala(": "); kwala_SMS(힙[던진객체 + 3]); }
        else modirisi.kwala("user exception");
        modirisi.kwala_Letshwao_Boleng(10); 던진객체 = 0; phoso = true;
    }
    // 이 JVM의 스택 항목은 ga_jaana_selwana category-1(int/reference)만 허용한다.
    static void kokoanyodinepe_taelo(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int baete_tshedimosetso = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식); 넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(baete_tshedimosetso, 둘째형식); return; }
        int khoutuletshwao = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(khoutuletshwao, 셋째형식); 넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식); 넣기(khoutuletshwao, 셋째형식); 넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(khoutuletshwao, 셋째형식); 넣기(baete_tshedimosetso, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int leina_tlhomameng, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(leina_tlhomameng);
        if (Lefoko_SMS(leina_tlhomameng, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Lefoko_SMS(leina_tlhomameng, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Lefoko_SMS(leina_tlhomameng, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Lefoko_SMS(leina_tlhomameng, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Lefoko_SMS(leina_tlhomameng, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Lefoko_SMS(leina_tlhomameng, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Lefoko_SMS(leina_tlhomameng, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Lefoko_SMS(leina_tlhomameng, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Lefoko_SMS(leina_tlhomameng, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Lefoko_SMS(leina_tlhomameng, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Lefoko_SMS(leina_tlhomameng, "java/lang/Thread") || Lefoko_SMS(leina_tlhomameng, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Lefoko_SMS(leina_tlhomameng, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(leina_tlhomameng) != 0) { 분류코드 = 화면종(leina_tlhomameng); 유효길이 = 12; }
        if (분류코드 == 0) {
            int khoutuletshwao = batla_mofuta_Tlhaloso(leina_tlhomameng); if (khoutuletshwao < 0 || phoso || !go_baakanyetsa_tiriso(khoutuletshwao, 시작점)) return;
            분류코드 = 32 + khoutuletshwao; 유효길이 = 종칸수[khoutuletshwao];
        }
        int selwana_Tshupiso = abela_Polokelo(분류코드, 유효길이); if (phoso) return;
        if (분류코드 == 13 && Lefoko_SMS(leina_tlhomameng, "한국어/자체/작업가닥")) 힙[selwana_Tshupiso + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(leina_tlhomameng) != 0) 힙[selwana_Tshupiso + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[selwana_Tshupiso + 2] = -1;
        if (분류코드 == 9) 힙[selwana_Tshupiso + 2] = 예외참조;
        넣기(selwana_Tshupiso, 2);
    }
    static boolean 값같음(int 첫값, int baete_tshedimosetso) {
        if (첫값 == baete_tshedimosetso) return true;
        if (첫값 == 0 || baete_tshedimosetso == 0 || 첫값 < 0 || baete_tshedimosetso < 0 || 첫값 >= 힙끝 || baete_tshedimosetso >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[baete_tshedimosetso] == 1) return 글같음(첫값, baete_tshedimosetso, false);
        return 힙[첫값] == 12 && 힙[baete_tshedimosetso] == 12 && 힙[첫값 + 2] == 힙[baete_tshedimosetso + 2];
    }
    static int 글조각(int selwana_Tshupiso, int 시작자리, int 끝자리) {
        if (!selwana_Boleng(selwana_Tshupiso, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[selwana_Tshupiso + 1]) { palelo_Boleng("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = abela_Polokelo(1, 끝자리 - 시작자리); if (phoso) return 0;
        for (int lupu_tshupane = 시작자리; lupu_tshupane < 끝자리; lupu_tshupane++) 힙[반환값 + 2 + lupu_tshupane - 시작자리] = 힙[selwana_Tshupiso + 2 + lupu_tshupane];
        return 반환값;
    }
    static int tsenela_SMS(int 첫값, int baete_tshedimosetso) {
        if (!selwana_Boleng(첫값, 1) || !selwana_Boleng(baete_tshedimosetso, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], mokgwa_tshupane = 힙[baete_tshedimosetso + 1], 반환값 = abela_Polokelo(1, 항목수 + mokgwa_tshupane); if (phoso) return 0;
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) 힙[반환값 + 2 + lupu_tshupane] = 힙[첫값 + 2 + lupu_tshupane];
        for (int lupu_tshupane = 0; lupu_tshupane < mokgwa_tshupane; lupu_tshupane++) 힙[반환값 + 2 + 항목수 + lupu_tshupane] = 힙[baete_tshedimosetso + 2 + lupu_tshupane];
        return 반환값;
    }
    static boolean 기본호출(int mong, int leina_tlhomameng, int 서술상수, int 명령코드) {
        if (Lefoko_SMS(mong, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (Lefoko_SMS(leina_tlhomameng, "개수") && Lefoko_SMS(서술상수, "()I")) { 넣기(modirisi.인수개수() - 1, 1); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "SMS") && Lefoko_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= modirisi.인수개수() - 1) 예외던짐(29, "diragatsa_Taelo 인수 범위를 벗어났습니다");
                else 넣기(pinagare_Letshwao(modirisi.인수(순번 + 1)), 2);
                return true;
            }
            palelo_Boleng("지원하지 않는 한국어 diragatsa_Taelo 인수 호출"); return true;
        }
        if (Lefoko_SMS(mong, "한국어/자체/작업가닥")) { Thulaganyo_tlhale(leina_tlhomameng, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(mong)) { 한국어화면호출(mong, leina_tlhomameng, 서술상수, 명령코드); return true; }
        if (화면소유(mong)) { 화면호출(mong, leina_tlhomameng, 서술상수, 명령코드); return true; }
        if (Lefoko_SMS(mong, "java/net/Socket") || Lefoko_SMS(mong, "java/net/ServerSocket") || Lefoko_SMS(mong, "java/io/InputStream") || Lefoko_SMS(mong, "java/io/OutputStream")) { 흐름호출(mong, leina_tlhomameng, 서술상수, 명령코드); return true; }
        if (Lefoko_SMS(mong, "한국어/자체/Khenele_Boleng") && 명령코드 == 184) {
            if (Lefoko_SMS(leina_tlhomameng, "화면너비") && Lefoko_SMS(서술상수, "()I")) { 넣기(modirisi.화면너비(), 1); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "화면높이") && Lefoko_SMS(서술상수, "()I")) { 넣기(modirisi.화면높이(), 1); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "밀리초") && Lefoko_SMS(서술상수, "()I")) { 넣기(modirisi.밀리초(), 1); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "그림대기") && Lefoko_SMS(서술상수, "()I")) { 넣기(modirisi.그림대기(), 1); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "사각형") && Lefoko_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), kgokagano_ya_x = 빼기(1); 넣기(modirisi.사각형(kgokagano_ya_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Lefoko_SMS(mong, "java/net/InetAddress") || Lefoko_SMS(mong, "java/net/DatagramPacket") || Lefoko_SMS(mong, "java/net/DatagramSocket")) { 통신호출(mong, leina_tlhomameng, 서술상수, 명령코드); return true; }
        if (Lefoko_SMS(mong, "java/lang/Thread")) { 가닥호출(leina_tlhomameng, 서술상수, 명령코드); return true; }
        if (Lefoko_SMS(mong, "java/lang/Object")) {
            if (Lefoko_SMS(leina_tlhomameng, "<init>") && Lefoko_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "equals") && Lefoko_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baete_tshedimosetso = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == baete_tshedimosetso ? 1 : 0, 1); return true; }
        }
        if (예외상수(mong) != 0) {
            if (Lefoko_SMS(leina_tlhomameng, "<init>") && 명령코드 == 183 && (Lefoko_SMS(서술상수, "()V") || Lefoko_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int kgwetlho = Lefoko_SMS(서술상수, "()V") ? 0 : 빼기(2), selwana_Tshupiso = 빼기(2);
                if (selwana_Boleng(selwana_Tshupiso, 9)) { 힙[selwana_Tshupiso + 3] = kgwetlho; 힙참조[selwana_Tshupiso + 3] = 1; } return true;
            }
            if ((Lefoko_SMS(leina_tlhomameng, "getMessage") || Lefoko_SMS(leina_tlhomameng, "설명")) && Lefoko_SMS(서술상수, "()Ljava/lang/String;")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 9)) 넣기(힙[selwana_Tshupiso + 3], 2); return true; }
        }
        if (Lefoko_SMS(mong, "java/lang/String")) {
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "getBytes") && (Lefoko_SMS(서술상수, "()[B") || Lefoko_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int khoutufatso_leina = Lefoko_SMS(서술상수, "()[B") ? 0 : 빼기(2), selwana_Tshupiso = 빼기(2);
                if (!selwana_Boleng(selwana_Tshupiso, 1)) return true;
                if (khoutufatso_leina != 0 && !글같음(khoutufatso_leina, pinagare_Letshwao("UTF-8"), false) && !글같음(khoutufatso_leina, pinagare_Letshwao("UTF8"), false) && !글같음(khoutufatso_leina, pinagare_Letshwao("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[selwana_Tshupiso + 1], 반환값 = abela_Polokelo(20, 항목수 * 3), 사용수 = 0; if (phoso) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int khoutuletshwao = 힙[selwana_Tshupiso + 2 + 안쪽자리];
                    if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[selwana_Tshupiso + 3 + 안쪽자리] >= 0xdc00 && 힙[selwana_Tshupiso + 3 + 안쪽자리] <= 0xdfff) khoutuletshwao = 0x10000 + ((khoutuletshwao - 0xd800) << 10) + 힙[selwana_Tshupiso + 2 + ++안쪽자리] - 0xdc00;
                    else if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdfff) khoutuletshwao = '?';
                    if (khoutuletshwao < 128) 힙[반환값 + 2 + 사용수++] = khoutuletshwao;
                    else { int 바이트수 = khoutuletshwao < 2048 ? 2 : khoutuletshwao < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | khoutuletshwao >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | khoutuletshwao >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "valueOf") && Lefoko_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(dijite_Letshwao(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Lefoko_SMS(leina_tlhomameng, "equals") && Lefoko_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baete_tshedimosetso = 빼기(2), 첫값 = 빼기(2); if (selwana_Boleng(첫값, 1)) 넣기(글같음(첫값, baete_tshedimosetso, false) ? 1 : 0, 1); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "isEmpty") && Lefoko_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (selwana_Boleng(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "substring") && (Lefoko_SMS(서술상수, "(I)Ljava/lang/String;") || Lefoko_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Lefoko_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (selwana_Boleng(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Lefoko_SMS(leina_tlhomameng, "concat") && Lefoko_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int baete_tshedimosetso = 빼기(2), 첫값 = 빼기(2); 넣기(tsenela_SMS(첫값, baete_tshedimosetso), 2); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "hashCode") && Lefoko_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), heše_Boleng = 0; if (selwana_Boleng(첫값, 1)) { for (int lupu_tshupane = 0; lupu_tshupane < 힙[첫값 + 1]; lupu_tshupane++) heše_Boleng = heše_Boleng * 31 + 힙[첫값 + 2 + lupu_tshupane]; 넣기(heše_Boleng, 1); } return true; }
            if (Lefoko_SMS(leina_tlhomameng, "toString") && Lefoko_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (selwana_Boleng(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Lefoko_SMS(mong, "java/lang/Integer")) {
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "valueOf") && Lefoko_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int tshedimosetso_Boleng = 빼기(1), selwana_Tshupiso = tshedimosetso_Boleng >= -128 && tshedimosetso_Boleng <= 127 ? Store_Palotlalo[tshedimosetso_Boleng + 128] : 0; if (selwana_Tshupiso == 0) { selwana_Tshupiso = abela_Polokelo(12, 1); if (!phoso) { 힙[selwana_Tshupiso + 2] = tshedimosetso_Boleng; if (tshedimosetso_Boleng >= -128 && tshedimosetso_Boleng <= 127) Store_Palotlalo[tshedimosetso_Boleng + 128] = selwana_Tshupiso; } } 넣기(selwana_Tshupiso, 2); return true; }
            if (명령코드 == 183 && Lefoko_SMS(leina_tlhomameng, "<init>") && Lefoko_SMS(서술상수, "(I)V")) { int tshedimosetso_Boleng = 빼기(1), selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 12)) 힙[selwana_Tshupiso + 2] = tshedimosetso_Boleng; return true; }
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "intValue") && Lefoko_SMS(서술상수, "()I")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 12)) 넣기(힙[selwana_Tshupiso + 2], 1); return true; }
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "toString") && Lefoko_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(dijite_Letshwao(빼기(1)), 2); return true; }
        }
        if (Lefoko_SMS(mong, "java/lang/Math") && 명령코드 == 184) {
            if (Lefoko_SMS(leina_tlhomameng, "abs") && Lefoko_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Lefoko_SMS(leina_tlhomameng, "min") || Lefoko_SMS(leina_tlhomameng, "max")) && Lefoko_SMS(서술상수, "(II)I")) { int baete_tshedimosetso = 빼기(1), 첫값 = 빼기(1); 넣기(Lefoko_SMS(leina_tlhomameng, "min") ? (첫값 < baete_tshedimosetso ? 첫값 : baete_tshedimosetso) : (첫값 > baete_tshedimosetso ? 첫값 : baete_tshedimosetso), 1); return true; }
        }
        if (Lefoko_SMS(mong, "java/lang/System") && 명령코드 == 184) {
            if (Lefoko_SMS(leina_tlhomameng, "gc") && Lefoko_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Lefoko_SMS(leina_tlhomameng, "arraycopy") && Lefoko_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), bogorogelo_Boleng_tshupane = 빼기(1), baete_tshedimosetso = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(baete_tshedimosetso)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[baete_tshedimosetso] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) palelo_Boleng("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || bogorogelo_Boleng_tshupane < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || bogorogelo_Boleng_tshupane > 힙[baete_tshedimosetso + 1] - 항목수) palelo_Boleng("ArrayIndexOutOfBoundsException");
                    else if (첫값 == baete_tshedimosetso && bogorogelo_Boleng_tshupane > 시작자리) { for (int lupu_tshupane = 항목수 - 1; lupu_tshupane >= 0; lupu_tshupane--) 힙[baete_tshedimosetso + 2 + bogorogelo_Boleng_tshupane + lupu_tshupane] = 힙[첫값 + 2 + 시작자리 + lupu_tshupane]; }
                    else { for (int lupu_tshupane = 0; lupu_tshupane < 항목수 && !phoso; lupu_tshupane++) { int tshedimosetso_Boleng = 힙[첫값 + 2 + 시작자리 + lupu_tshupane]; if (분류코드 != 3 || 배열저장가능(baete_tshedimosetso, tshedimosetso_Boleng)) 힙[baete_tshedimosetso + 2 + bogorogelo_Boleng_tshupane + lupu_tshupane] = tshedimosetso_Boleng; } }
                }
                return true;
            }
        }
        if (Lefoko_SMS(mong, "java/util/ArrayList") || Lefoko_SMS(mong, "java/util/List") || Lefoko_SMS(mong, "java/util/HashMap") || Lefoko_SMS(mong, "java/util/Map")) {
            모음호출(mong, leina_tlhomameng, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int selwana_Tshupiso, int 필요수) {
        int 이전값 = 힙[selwana_Tshupiso + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int tshedimosetso_setlhopha = abela_Polokelo(3, 다음자리); if (phoso) return;
        for (int lupu_tshupane = 0; lupu_tshupane < 용량값; lupu_tshupane++) 힙[tshedimosetso_setlhopha + 2 + lupu_tshupane] = 힙[이전값 + 2 + lupu_tshupane];
        힙[selwana_Tshupiso + 2] = tshedimosetso_setlhopha; 힙참조[selwana_Tshupiso + 2] = 1;
    }
    static void 모음호출(int mong, int leina_tlhomameng, int 서술상수, int 명령코드) {
        boolean 대응참조 = Lefoko_SMS(mong, "java/util/HashMap") || Lefoko_SMS(mong, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Lefoko_SMS(leina_tlhomameng, "<init>") && 명령코드 == 183 && Lefoko_SMS(서술상수, "()V")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 분류코드)) 모음늘리기(selwana_Tshupiso, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { palelo_Boleng("invalid collection invocation"); return; }
        if (Lefoko_SMS(leina_tlhomameng, "size") && Lefoko_SMS(서술상수, "()I") || Lefoko_SMS(leina_tlhomameng, "isEmpty") && Lefoko_SMS(서술상수, "()Z")) {
            int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 분류코드)) 넣기(Lefoko_SMS(leina_tlhomameng, "size") ? 힙[selwana_Tshupiso + 3] : 힙[selwana_Tshupiso + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "clear") && Lefoko_SMS(서술상수, "()V")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 분류코드)) { int tshedimosetso_setlhopha = 힙[selwana_Tshupiso + 2]; for (int lupu_tshupane = 0; lupu_tshupane < 힙[tshedimosetso_setlhopha + 1]; lupu_tshupane++) 힙[tshedimosetso_setlhopha + 2 + lupu_tshupane] = 0; 힙[selwana_Tshupiso + 3] = 0; } return; }
        if (!대응참조 && Lefoko_SMS(leina_tlhomameng, "add") && Lefoko_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int tshedimosetso_Boleng = 빼기(2), selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 10)) return;
            int 항목수 = 힙[selwana_Tshupiso + 3]; 모음늘리기(selwana_Tshupiso, 항목수 + 1); if (!phoso) { 힙[힙[selwana_Tshupiso + 2] + 2 + 항목수] = tshedimosetso_Boleng; 힙[selwana_Tshupiso + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Lefoko_SMS(leina_tlhomameng, "get") || Lefoko_SMS(leina_tlhomameng, "remove")) && Lefoko_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Lefoko_SMS(leina_tlhomameng, "set") && Lefoko_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Lefoko_SMS(leina_tlhomameng, "set"); int tshedimosetso_Boleng = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), selwana_Tshupiso = 빼기(2);
            if (!selwana_Boleng(selwana_Tshupiso, 10)) return;
            int 항목수 = 힙[selwana_Tshupiso + 3], tshedimosetso_setlhopha = 힙[selwana_Tshupiso + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[tshedimosetso_setlhopha + 2 + 항목자리];
            if (지정여부) 힙[tshedimosetso_setlhopha + 2 + 항목자리] = tshedimosetso_Boleng;
            if (Lefoko_SMS(leina_tlhomameng, "remove")) { for (int lupu_tshupane = 항목자리 + 1; lupu_tshupane < 항목수; lupu_tshupane++) 힙[tshedimosetso_setlhopha + 1 + lupu_tshupane] = 힙[tshedimosetso_setlhopha + 2 + lupu_tshupane]; 힙[tshedimosetso_setlhopha + 1 + 항목수] = 0; 힙[selwana_Tshupiso + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Lefoko_SMS(leina_tlhomameng, "get") || Lefoko_SMS(leina_tlhomameng, "remove")) && Lefoko_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Lefoko_SMS(leina_tlhomameng, "put") && Lefoko_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Lefoko_SMS(leina_tlhomameng, "containsKey") && Lefoko_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Lefoko_SMS(leina_tlhomameng, "put"), tlosa = Lefoko_SMS(leina_tlhomameng, "remove");
            int tshedimosetso_Boleng = 넣기여부 ? 빼기(2) : 0, taetsi_Tshupiso = 빼기(2), selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 11)) return;
            int 항목수 = 힙[selwana_Tshupiso + 3], tshedimosetso_setlhopha = 힙[selwana_Tshupiso + 2], 찾은여부 = -1;
            for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) if (값같음(taetsi_Tshupiso, 힙[tshedimosetso_setlhopha + 2 + 2 * lupu_tshupane])) { 찾은여부 = lupu_tshupane; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[tshedimosetso_setlhopha + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(selwana_Tshupiso, (항목수 + 1) * 2); tshedimosetso_setlhopha = 힙[selwana_Tshupiso + 2]; 찾은여부 = 항목수; if (!phoso) 힙[selwana_Tshupiso + 3] = 항목수 + 1; }
                if (!phoso) { 힙[tshedimosetso_setlhopha + 2 + 2 * 찾은여부] = taetsi_Tshupiso; 힙[tshedimosetso_setlhopha + 3 + 2 * 찾은여부] = tshedimosetso_Boleng; }
            }
            if (tlosa && 찾은여부 >= 0) { for (int lupu_tshupane = 찾은여부 + 1; lupu_tshupane < 항목수; lupu_tshupane++) { 힙[tshedimosetso_setlhopha + 2 * lupu_tshupane] = 힙[tshedimosetso_setlhopha + 2 + 2 * lupu_tshupane]; 힙[tshedimosetso_setlhopha + 1 + 2 * lupu_tshupane] = 힙[tshedimosetso_setlhopha + 3 + 2 * lupu_tshupane]; } 힙[tshedimosetso_setlhopha + 2 * 항목수] = 0; 힙[tshedimosetso_setlhopha + 1 + 2 * 항목수] = 0; 힙[selwana_Tshupiso + 3] = 항목수 - 1; }
            if (Lefoko_SMS(leina_tlhomameng, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        palelo_Boleng("unsupported collection method");
    }
    static boolean 잠금얻기(int selwana_Tshupiso) {
        if (!객체유효(selwana_Tshupiso)) return false;
        if (잠금깊이[selwana_Tshupiso] != 0 && 잠금주인[selwana_Tshupiso] != ga_jaana_tlhale + 1) { 바꿈요청 = true; return false; }
        잠금주인[selwana_Tshupiso] = ga_jaana_tlhale + 1; 잠금깊이[selwana_Tshupiso]++; return true;
    }
    static void 잠금풀기(int selwana_Tshupiso) {
        if (!객체유효(selwana_Tshupiso)) return;
        if (잠금깊이[selwana_Tshupiso] == 0 || 잠금주인[selwana_Tshupiso] != ga_jaana_tlhale + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[selwana_Tshupiso] == 0) 잠금주인[selwana_Tshupiso] = 0;
    }
    static boolean fetola_tlhale() {
        tlhale_Foreimi[ga_jaana_tlhale] = Foreimi_tshupane;
        if (Foreimi_tshupane < ga_jaana_tlhale * 32) tlhale_kemo[ga_jaana_tlhale] = 3;
        for (int lupu_tshupane = 0; lupu_tshupane < 가닥수; lupu_tshupane++) if (tlhale_kemo[lupu_tshupane] == 2 && tlhale_kemo[가닥대기[lupu_tshupane]] == 3) tlhale_kemo[lupu_tshupane] = 1;
        for (int lupu_tshupane = 1; lupu_tshupane <= 가닥수; lupu_tshupane++) {
            int 다음자리 = (ga_jaana_tlhale + lupu_tshupane) % 가닥수;
            if (tlhale_kemo[다음자리] == 1) { ga_jaana_tlhale = 다음자리; Foreimi_tshupane = tlhale_Foreimi[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int lupu_tshupane = 0; lupu_tshupane < 가닥수; lupu_tshupane++) if (tlhale_kemo[lupu_tshupane] != 3) { palelo_Boleng("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int leina_tlhomameng, int 서술상수, int 명령코드) { Thulaganyo_tlhale(leina_tlhomameng, 서술상수, 명령코드, false); }
    static void Thulaganyo_tlhale(int leina_tlhomameng, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, 한국어 ? "emisa_ka_nakwana_Tiro" : "yield") && Lefoko_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "currentThread") && Lefoko_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(tlhale_selwana[ga_jaana_tlhale], 2); return; }
        if (명령코드 == 183 && Lefoko_SMS(leina_tlhomameng, "<init>") && (Lefoko_SMS(서술상수, "()V") || Lefoko_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int setotwa_aterese = Lefoko_SMS(서술상수, "()V") ? 0 : 빼기(2), selwana_Tshupiso = 빼기(2);
            if (!객체유효(selwana_Tshupiso)) return;
            if (힙[selwana_Tshupiso] == 13) { 힙[selwana_Tshupiso + 2] = setotwa_aterese; 힙참조[selwana_Tshupiso + 2] = 1; }
            else if (setotwa_aterese != 0) palelo_Boleng("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Lefoko_SMS(leina_tlhomameng, 한국어 ? "simolola_Tiro" : "start") || Lefoko_SMS(leina_tlhomameng, 한국어 ? "기다리기" : "join")) && Lefoko_SMS(서술상수, "()V") || 명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, 한국어 ? "살아있는가" : "isAlive") && Lefoko_SMS(서술상수, "()Z")) {
            int selwana_Tshupiso = 빼기(2); if (!객체유효(selwana_Tshupiso)) return;
            int itshupo_Boleng = -1; for (int lupu_tshupane = 0; lupu_tshupane < 가닥수; lupu_tshupane++) if (tlhale_selwana[lupu_tshupane] == selwana_Tshupiso) itshupo_Boleng = lupu_tshupane;
            if (Lefoko_SMS(leina_tlhomameng, 한국어 ? "살아있는가" : "isAlive")) { 넣기(itshupo_Boleng >= 0 && tlhale_kemo[itshupo_Boleng] != 3 ? 1 : 0, 1); return; }
            if (Lefoko_SMS(leina_tlhomameng, 한국어 ? "기다리기" : "join")) { if (itshupo_Boleng >= 0 && tlhale_kemo[itshupo_Boleng] != 3) { 가닥대기[ga_jaana_tlhale] = itshupo_Boleng; tlhale_kemo[ga_jaana_tlhale] = 2; 바꿈요청 = true; } return; }
            if (itshupo_Boleng >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { palelo_Boleng("thread limit (4 including main)"); return; }
            int setotwa_aterese = 힙[selwana_Tshupiso] == 13 ? 힙[selwana_Tshupiso + 2] : selwana_Tshupiso;
            int faele_tshupane = setotwa_aterese > 0 && 힙[setotwa_aterese] >= 32 ? leina_mokgwa(힙[setotwa_aterese] - 32, 한국어 ? "diragatsa_Tiro" : "run", "()V") : -1;
            if (setotwa_aterese != 0 && faele_tshupane < 0) { palelo_Boleng("Runnable.run required"); return; }
            itshupo_Boleng = 가닥수++; tlhale_selwana[itshupo_Boleng] = selwana_Tshupiso; tlhale_setotwa[itshupo_Boleng] = setotwa_aterese;
            int Foreimi = itshupo_Boleng * 32; tlhale_Foreimi[itshupo_Boleng] = faele_tshupane < 0 ? Foreimi - 1 : Foreimi; tlhale_kemo[itshupo_Boleng] = faele_tshupane < 0 ? 3 : 1;
            if (faele_tshupane >= 0) { Foreimi_mokgwa[Foreimi] = faele_tshupane; 틀위치[Foreimi] = mokgwa_simolola[faele_tshupane]; e_e_gaufi_Boleng[Foreimi * 128] = setotwa_aterese; e_e_gaufi_tlanya[Foreimi * 128] = 2; }
            return;
        }
        palelo_Boleng("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], aterese_SMS = new int[16];
    static int e_e_gaufi_aterese() { return aterese_selwana(0x7f000001); }
    static int aterese_selwana(int Boleng) { int selwana_Tshupiso = abela_Polokelo(14, 1); if (!phoso) 힙[selwana_Tshupiso + 2] = Boleng; return selwana_Tshupiso; }
    static int 주소해독(int selwana_Tshupiso) {
        if (selwana_Tshupiso == 0 || 글같음(selwana_Tshupiso, pinagare_Letshwao("localhost"), false)) return 0x7f000001;
        if (!selwana_Boleng(selwana_Tshupiso, 1)) return 0;
        int tshedimosetso_Boleng = 0, 총수 = 0, aterese_baete = 0, 자릿수 = 0, 항목수 = 힙[selwana_Tshupiso + 1];
        for (int lupu_tshupane = 0; lupu_tshupane <= 항목수; lupu_tshupane++) {
            int khoutuletshwao = lupu_tshupane == 항목수 ? '.' : 힙[selwana_Tshupiso + 2 + lupu_tshupane];
            if (khoutuletshwao == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } tshedimosetso_Boleng = tshedimosetso_Boleng << 8 | aterese_baete; 총수++; aterese_baete = 자릿수 = 0; }
            else { if (khoutuletshwao < '0' || khoutuletshwao > '9' || ++자릿수 > 3 || (aterese_baete = aterese_baete * 10 + khoutuletshwao - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return tshedimosetso_Boleng;
    }
    static int aterese_Letshwao(int tshedimosetso_Boleng) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int aterese_baete = tshedimosetso_Boleng >>> 이동비트 & 255;
            if (aterese_baete >= 100) aterese_SMS[항목수++] = '0' + aterese_baete / 100;
            if (aterese_baete >= 10) aterese_SMS[항목수++] = '0' + aterese_baete / 10 % 10;
            aterese_SMS[항목수++] = '0' + aterese_baete % 10; if (이동비트 != 0) aterese_SMS[항목수++] = '.';
        }
        int selwana_Tshupiso = abela_Polokelo(1, 항목수); if (!phoso) for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) 힙[selwana_Tshupiso + 2 + lupu_tshupane] = aterese_SMS[lupu_tshupane]; return selwana_Tshupiso;
    }
    static void 통신호출(int mong, int leina_tlhomameng, int 서술상수, int 명령코드) {
        if (Lefoko_SMS(mong, "java/net/InetAddress")) {
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "getLoopbackAddress") && Lefoko_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(e_e_gaufi_aterese(), 2); return; }
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "getByName") && Lefoko_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int tshedimosetso_Boleng = 주소해독(빼기(2)); if (던진객체 == 0 && !phoso) 넣기(aterese_selwana(tshedimosetso_Boleng), 2); return;
            }
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "getHostAddress") && Lefoko_SMS(서술상수, "()Ljava/lang/String;")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 14)) 넣기(aterese_Letshwao(힙[selwana_Tshupiso + 2]), 2); return; }
        }
        if (Lefoko_SMS(mong, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Lefoko_SMS(leina_tlhomameng, "<init>") && (Lefoko_SMS(서술상수, "([BI)V") || Lefoko_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean bogorogelo_Boleng_Tshupiso = Lefoko_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = bogorogelo_Boleng_Tshupiso ? 빼기(1) : 0, aterese_Tshupiso = bogorogelo_Boleng_Tshupiso ? 빼기(2) : 0;
                int 항목수 = 빼기(1), tshedimosetso_setlhopha = 빼기(2), selwana_Tshupiso = 빼기(2);
                if (!selwana_Boleng(selwana_Tshupiso, 16) || !selwana_Boleng(tshedimosetso_setlhopha, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[tshedimosetso_setlhopha + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (aterese_Tshupiso != 0 && !selwana_Boleng(aterese_Tshupiso, 14)) return;
                힙[selwana_Tshupiso + 2] = tshedimosetso_setlhopha; 힙참조[selwana_Tshupiso + 2] = 1; 힙[selwana_Tshupiso + 3] = 항목수;
                힙[selwana_Tshupiso + 4] = aterese_Tshupiso; 힙참조[selwana_Tshupiso + 4] = 1; 힙[selwana_Tshupiso + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "setLength") && Lefoko_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[selwana_Tshupiso + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[selwana_Tshupiso + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Lefoko_SMS(leina_tlhomameng, "getData") && Lefoko_SMS(서술상수, "()[B") || Lefoko_SMS(leina_tlhomameng, "getLength") && Lefoko_SMS(서술상수, "()I") || Lefoko_SMS(leina_tlhomameng, "getAddress") && Lefoko_SMS(서술상수, "()Ljava/net/InetAddress;") || Lefoko_SMS(leina_tlhomameng, "getPort") && Lefoko_SMS(서술상수, "()I"))) {
                int selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 16)) return;
                int 항목자리 = Lefoko_SMS(leina_tlhomameng, "getData") ? 2 : Lefoko_SMS(leina_tlhomameng, "getLength") ? 3 : Lefoko_SMS(leina_tlhomameng, "getAddress") ? 4 : 5;
                넣기(힙[selwana_Tshupiso + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Lefoko_SMS(mong, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Lefoko_SMS(leina_tlhomameng, "<init>") && (Lefoko_SMS(서술상수, "()V") || Lefoko_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Lefoko_SMS(서술상수, "()V") ? 0 : 빼기(1), selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = modirisi.bula_Neteweke(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[selwana_Tshupiso + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "setSoTimeout") && Lefoko_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[selwana_Tshupiso + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "getLocalPort") && Lefoko_SMS(서술상수, "()I")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 15)) 넣기(힙[selwana_Tshupiso + 2] < 0 ? -1 : modirisi.Neteweke_gorogisetsa(힙[selwana_Tshupiso + 2]), 1); return; }
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "isClosed") && Lefoko_SMS(서술상수, "()Z")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 15)) 넣기(힙[selwana_Tshupiso + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Lefoko_SMS(leina_tlhomameng, "close") && Lefoko_SMS(서술상수, "()V")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 15) && 힙[selwana_Tshupiso + 2] >= 0) { modirisi.파일서술자닫기(힙[selwana_Tshupiso + 2]); 힙[selwana_Tshupiso + 2] = -1; } return; }
            if (명령코드 == 182 && (Lefoko_SMS(leina_tlhomameng, "send") || Lefoko_SMS(leina_tlhomameng, "receive")) && Lefoko_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int sephuthelwana = 빼기(2), selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(sephuthelwana, 16) || !selwana_Boleng(selwana_Tshupiso, 15)) return;
                int tshedimosetso_setlhopha = 힙[sephuthelwana + 2], 유효길이 = 힙[sephuthelwana + 3], 열린파일번호 = 힙[selwana_Tshupiso + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Lefoko_SMS(leina_tlhomameng, "send")) {
                    if (!selwana_Boleng(힙[sephuthelwana + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int lupu_tshupane = 0; lupu_tshupane < 유효길이; lupu_tshupane++) 통신임시[lupu_tshupane] = 힙[tshedimosetso_setlhopha + 2 + lupu_tshupane];
                    if (modirisi.romela_Neteweke(열린파일번호, 힙[힙[sephuthelwana + 4] + 2], 힙[sephuthelwana + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = modirisi.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = modirisi.밀리초();
                        if (힙[selwana_Tshupiso + 4] == 0) 힙[selwana_Tshupiso + 4] = 현재시각 + 1;
                        if (힙[selwana_Tshupiso + 3] > 0 && 현재시각 - (힙[selwana_Tshupiso + 4] - 1) >= 힙[selwana_Tshupiso + 3]) { 힙[selwana_Tshupiso + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(selwana_Tshupiso, 2); 넣기(sephuthelwana, 2); 틀위치[Foreimi_tshupane] = Foreimi_taelo[Foreimi_tshupane]; 바꿈요청 = true; return;
                    }
                    힙[selwana_Tshupiso + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) 힙[tshedimosetso_setlhopha + 2 + lupu_tshupane] = (byte)통신임시[lupu_tshupane];
                    힙[sephuthelwana + 3] = 항목수; 힙[sephuthelwana + 4] = aterese_selwana(통신임시[513]); 힙참조[sephuthelwana + 4] = 1; 힙[sephuthelwana + 5] = 통신임시[512];
                }
                return;
            }
        }
        palelo_Boleng("unsupported java.net method");
    }
    static boolean 흐름대기(int selwana_Tshupiso) {
        int 현재시각 = modirisi.밀리초();
        if (힙[selwana_Tshupiso + 5] == 0) 힙[selwana_Tshupiso + 5] = 현재시각 + 1;
        if (힙[selwana_Tshupiso + 3] > 0 && 현재시각 - (힙[selwana_Tshupiso + 5] - 1) >= 힙[selwana_Tshupiso + 3]) { 힙[selwana_Tshupiso + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[Foreimi_tshupane] = Foreimi_taelo[Foreimi_tshupane]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int mong, int leina_tlhomameng, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Lefoko_SMS(mong, "java/net/ServerSocket"), moela = Lefoko_SMS(mong, "java/io/InputStream") || Lefoko_SMS(mong, "java/io/OutputStream");
        if (!moela && 명령코드 == 183 && Lefoko_SMS(leina_tlhomameng, "<init>")) {
            boolean 빈여부 = Lefoko_SMS(서술상수, "()V"), 이름지정여부 = Lefoko_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Lefoko_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Lefoko_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { palelo_Boleng("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), aterese_Tshupiso = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, selwana_Tshupiso = 빼기(2);
            if (!selwana_Boleng(selwana_Tshupiso, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !selwana_Boleng(aterese_Tshupiso, 14)) return;
            int Neteweke_aterese = 이름지정여부 ? 주소해독(aterese_Tshupiso) : 주소지정여부 ? 힙[aterese_Tshupiso + 2] : 0x7f000001;
            if (phoso || 던진객체 != 0) return;
            int 열린파일번호 = modirisi.moela_taolo(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? modirisi.moela_taolo(1, 열린파일번호, 접속번호) : modirisi.Golaganya_moela(열린파일번호, Neteweke_aterese, 접속번호);
            if (처리값 < 0) { modirisi.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[selwana_Tshupiso + 2] = 열린파일번호; 힙[selwana_Tshupiso + 4] = 접속번호; 힙[selwana_Tshupiso + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!moela && Lefoko_SMS(leina_tlhomameng, "setSoTimeout") && Lefoko_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[selwana_Tshupiso + 3] = 밀리초값; return; }
        if (!moela && Lefoko_SMS(leina_tlhomameng, "close") && Lefoko_SMS(서술상수, "()V")) { int selwana_Tshupiso = 빼기(2); if (selwana_Boleng(selwana_Tshupiso, 수신쪽 ? 18 : 17) && 힙[selwana_Tshupiso + 2] >= 0) { modirisi.파일서술자닫기(힙[selwana_Tshupiso + 2]); 힙[selwana_Tshupiso + 2] = -1; } return; }
        if (!moela && (Lefoko_SMS(leina_tlhomameng, "getLocalPort") || Lefoko_SMS(leina_tlhomameng, "getPort") || Lefoko_SMS(leina_tlhomameng, "isClosed") || Lefoko_SMS(leina_tlhomameng, "isConnected"))) {
            int selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 수신쪽 ? 18 : 17)) return;
            넣기(Lefoko_SMS(leina_tlhomameng, "isClosed") ? 힙[selwana_Tshupiso + 2] < 0 ? 1 : 0 : Lefoko_SMS(leina_tlhomameng, "isConnected") ? 힙[selwana_Tshupiso + 6] : Lefoko_SMS(leina_tlhomameng, "getPort") ? 힙[selwana_Tshupiso + 4] : 힙[selwana_Tshupiso + 2] < 0 ? -1 : modirisi.moela_taolo(4, 힙[selwana_Tshupiso + 2], 0), 1); return;
        }
        if (수신쪽 && Lefoko_SMS(leina_tlhomameng, "accept") && Lefoko_SMS(서술상수, "()Ljava/net/Socket;")) {
            int selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 18)) return; int 열린파일번호 = modirisi.moela_taolo(3, 힙[selwana_Tshupiso + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(selwana_Tshupiso)) 넣기(selwana_Tshupiso, 2); return; }
            힙[selwana_Tshupiso + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = abela_Polokelo(17, 5); if (phoso) { modirisi.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = modirisi.moela_taolo(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !moela && ((Lefoko_SMS(leina_tlhomameng, "getInputStream") && Lefoko_SMS(서술상수, "()Ljava/io/InputStream;")) || (Lefoko_SMS(leina_tlhomameng, "getOutputStream") && Lefoko_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 17)) return; if (힙[selwana_Tshupiso + 2] < 0 || 힙[selwana_Tshupiso + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = abela_Polokelo(19, 4); if (phoso) return; 힙[반환값 + 2] = selwana_Tshupiso; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Lefoko_SMS(leina_tlhomameng, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (moela) {
            boolean 읽기여부 = Lefoko_SMS(leina_tlhomameng, "read"), 쓰기여부 = Lefoko_SMS(leina_tlhomameng, "write"), thibela = Lefoko_SMS(서술상수, "([B)I") || Lefoko_SMS(서술상수, "([B)V"), 부분배열여부 = Lefoko_SMS(서술상수, "([BII)I") || Lefoko_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, tshedimosetso_setlhopha = thibela || 부분배열여부 ? 빼기(2) : 0;
            int tshedimosetso_Boleng = 쓰기여부 && Lefoko_SMS(서술상수, "(I)V") ? 빼기(1) : 0, selwana_Tshupiso = 빼기(2);
            if (!selwana_Boleng(selwana_Tshupiso, 19)) return; int 부모참조 = 힙[selwana_Tshupiso + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Lefoko_SMS(leina_tlhomameng, "close") && Lefoko_SMS(서술상수, "()V")) { modirisi.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Lefoko_SMS(leina_tlhomameng, "flush") && Lefoko_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[selwana_Tshupiso + 3] == 0)) { palelo_Boleng("unsupported stream operation"); return; }
            if (thibela || 부분배열여부) { if (!selwana_Boleng(tshedimosetso_setlhopha, 20)) return; if (thibela) 항목수 = 힙[tshedimosetso_setlhopha + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[tshedimosetso_setlhopha + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[selwana_Tshupiso + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? modirisi.파일한바이트읽기(열린파일번호) : modirisi.파일한바이트쓰기(열린파일번호, thibela || 부분배열여부 ? 힙[tshedimosetso_setlhopha + 2 + 시작변위 + 완료수] : tshedimosetso_Boleng);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (thibela || 부분배열여부)) 힙[tshedimosetso_setlhopha + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(thibela || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[selwana_Tshupiso + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(selwana_Tshupiso, 2); if (thibela || 부분배열여부) 넣기(tshedimosetso_setlhopha, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(thibela || 부분배열여부)) 넣기(tshedimosetso_Boleng, 1); } return;
            }
            힙[selwana_Tshupiso + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : thibela || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        palelo_Boleng("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int leina_tlhomameng) {
        if (Lefoko_SMS(leina_tlhomameng, "한국어/자체/fensetere")) return 24;
        if (Lefoko_SMS(leina_tlhomameng, "한국어/자체/leibola")) return 26;
        if (Lefoko_SMS(leina_tlhomameng, "한국어/자체/konopo")) return 27;
        if (Lefoko_SMS(leina_tlhomameng, "한국어/자체/SMS_lefelo")) return 28;
        if (Lefoko_SMS(leina_tlhomameng, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int leina_tlhomameng) {
        return 한국어화면종(leina_tlhomameng) != 0 || Lefoko_SMS(leina_tlhomameng, "한국어/자체/화면구성요소") || Lefoko_SMS(leina_tlhomameng, "한국어/자체/tiragalo_diletakgatiso");
    }
    static int 화면종(int leina_tlhomameng) {
        int 한국어종 = 한국어화면종(leina_tlhomameng); if (한국어종 != 0) return 한국어종;
        if (Lefoko_SMS(leina_tlhomameng, "javax/swing/JFrame")) return 24;
        if (Lefoko_SMS(leina_tlhomameng, "javax/swing/JPanel")) return 25;
        if (Lefoko_SMS(leina_tlhomameng, "javax/swing/JLabel")) return 26;
        if (Lefoko_SMS(leina_tlhomameng, "javax/swing/JButton")) return 27;
        if (Lefoko_SMS(leina_tlhomameng, "javax/swing/JTextField")) return 28;
        if (Lefoko_SMS(leina_tlhomameng, "java/awt/event/ActionEvent")) return 29;
        if (Lefoko_SMS(leina_tlhomameng, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int leina_tlhomameng) {
        return 화면종(leina_tlhomameng) != 0 || Lefoko_SMS(leina_tlhomameng, "java/awt/Component") || Lefoko_SMS(leina_tlhomameng, "java/awt/Container") || Lefoko_SMS(leina_tlhomameng, "javax/swing/JComponent") || Lefoko_SMS(leina_tlhomameng, "javax/swing/AbstractButton") || Lefoko_SMS(leina_tlhomameng, "javax/swing/text/JTextComponent") || Lefoko_SMS(leina_tlhomameng, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int selwana_Tshupiso) { if (!객체유효(selwana_Tshupiso)) return false; if (힙[selwana_Tshupiso] < 24 || 힙[selwana_Tshupiso] > 28) { palelo_Boleng("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int selwana_Tshupiso, int SMS_Tshupiso) {
        if (SMS_Tshupiso != 0 && !selwana_Boleng(SMS_Tshupiso, 1)) return;
        int 항목수 = SMS_Tshupiso == 0 ? 0 : 힙[SMS_Tshupiso + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) 화면글임시[lupu_tshupane] = 힙[SMS_Tshupiso + 2 + lupu_tshupane];
        if (modirisi.화면글(힙[selwana_Tshupiso + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[selwana_Tshupiso + 3] = SMS_Tshupiso; 힙참조[selwana_Tshupiso + 3] = 1;
    }
    static int 화면문자읽기(int selwana_Tshupiso) {
        int itshupo_Boleng = 힙[selwana_Tshupiso + 2], 항목수 = modirisi.화면연결(8, itshupo_Boleng, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { palelo_Boleng("GUI text read failed"); return 0; }
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) { int 부호값 = modirisi.화면연결(9, itshupo_Boleng, lupu_tshupane, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = abela_Polokelo(1, 사용수); if (!phoso) for (int lupu_tshupane = 0; lupu_tshupane < 사용수; lupu_tshupane++) 힙[반환값 + 2 + lupu_tshupane] = 화면글임시[lupu_tshupane]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 Khenele_Boleng 화면 기능에 연결한다. Swing selwana_Boleng/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int mong, int leina_tlhomameng, int 서술상수, int 명령코드) {
        if (Lefoko_SMS(mong, "한국어/자체/tiragalo_diletakgatiso")) {
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "나중에실행") && Lefoko_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int Tiro_tiro = 빼기(2); if (!객체유효(Tiro_tiro)) return;
                if (나중수 == 8) { palelo_Boleng("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = Tiro_tiro; return;
            }
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "사건처리중인가") && Lefoko_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            palelo_Boleng("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Lefoko_SMS(mong, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!selwana_Boleng(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Lefoko_SMS(leina_tlhomameng, "tiragalo_Motswedi") && Lefoko_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Lefoko_SMS(leina_tlhomameng, "Taelo_SMS") && Lefoko_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Lefoko_SMS(leina_tlhomameng, "tshupane") && Lefoko_SMS(서술상수, "()I")) 넣기(1001, 1);
            else palelo_Boleng("지원하지 않는 한국어 tiro 알림 호출"); return;
        }
        if (명령코드 == 183 && Lefoko_SMS(leina_tlhomameng, "<init>")) {
            int 종류 = 한국어화면종(mong), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Lefoko_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (modirisi.화면너비() - 폭) / 2; 세로 = (modirisi.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Lefoko_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Lefoko_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { palelo_Boleng("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), tlhakakaelo_Boleng = 빼기(2); if (!화면객체(tlhakakaelo_Boleng)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > modirisi.화면너비() - 가로 || 높이 > modirisi.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int tshupane = modirisi.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (tshupane < 1 || tshupane > 32) { palelo_Boleng("화면 tlhakakaelo_Boleng 자리가 가득 찼습니다"); return; }
            힙[tlhakakaelo_Boleng + 2] = tshupane; 화면참조[tshupane - 1] = tlhakakaelo_Boleng;
            힙[tlhakakaelo_Boleng + 5] = 가로; 힙[tlhakakaelo_Boleng + 6] = 세로; 힙[tlhakakaelo_Boleng + 7] = 폭; 힙[tlhakakaelo_Boleng + 8] = 높이; 힙[tlhakakaelo_Boleng + 10] = 2;
            힙[tlhakakaelo_Boleng + 4] = 받이; 힙참조[tlhakakaelo_Boleng + 4] = 1; 힙[tlhakakaelo_Boleng + 12] = 1;
            modirisi.화면연결(1, tshupane, 가로, 세로, 폭, 높이);
            if (종류 == 24) modirisi.화면연결(7, tshupane, 2, 0, 0, 0);
            화면문자설정(tlhakakaelo_Boleng, SMS); return;
        }
        if (명령코드 != 182) { palelo_Boleng("잘못된 한국어 화면 호출 Taelo"); return; }
        if (Lefoko_SMS(leina_tlhomameng, "kwala_SMS") && Lefoko_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), tlhakakaelo_Boleng = 빼기(2); if (화면객체(tlhakakaelo_Boleng)) 화면문자설정(tlhakakaelo_Boleng, SMS); return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "글읽기") && Lefoko_SMS(서술상수, "()Ljava/lang/String;")) {
            int tlhakakaelo_Boleng = 빼기(2); if (화면객체(tlhakakaelo_Boleng)) 넣기(화면문자읽기(tlhakakaelo_Boleng), 2); return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "동작맡기기") && Lefoko_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), tlhakakaelo_Boleng = 빼기(2);
            if (화면객체(tlhakakaelo_Boleng)) { 힙[tlhakakaelo_Boleng + 4] = 받이; 힙참조[tlhakakaelo_Boleng + 4] = 1; 힙[tlhakakaelo_Boleng + 12] = 1; } return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "tsenya_tlhakakaelo") && Lefoko_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int ngwana_Boleng = 빼기(2), 부모 = 빼기(2); if (!화면객체(ngwana_Boleng) || !화면객체(부모)) return;
            if (modirisi.화면연결(2, 힙[부모 + 2], 힙[ngwana_Boleng + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[ngwana_Boleng + 11] = 부모; 힙참조[ngwana_Boleng + 11] = 1; return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "자리정하기") && Lefoko_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), tlhakakaelo_Boleng = 빼기(2); if (!화면객체(tlhakakaelo_Boleng)) return;
            if (modirisi.화면연결(1, 힙[tlhakakaelo_Boleng + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[tlhakakaelo_Boleng + 5] = 가로; 힙[tlhakakaelo_Boleng + 6] = 세로; 힙[tlhakakaelo_Boleng + 7] = 폭; 힙[tlhakakaelo_Boleng + 8] = 높이; return;
        }
        if ((Lefoko_SMS(leina_tlhomameng, "bontsha_fensetere") || Lefoko_SMS(leina_tlhomameng, "tswala")) && Lefoko_SMS(서술상수, "()V")) {
            boolean ponagalo_Boleng = Lefoko_SMS(leina_tlhomameng, "bontsha_fensetere"); int tlhakakaelo_Boleng = 빼기(2); if (!화면객체(tlhakakaelo_Boleng)) return;
            if (modirisi.화면연결(ponagalo_Boleng ? 3 : 4, 힙[tlhakakaelo_Boleng + 2], ponagalo_Boleng ? 1 : 0, 0, 0, 0) < 0) { palelo_Boleng("화면은 Tirisano 명령에서 실행해야 합니다"); return; }
            힙[tlhakakaelo_Boleng + 9] = ponagalo_Boleng ? 1 : 0; return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "보이는가") && Lefoko_SMS(서술상수, "()Z")) { int tlhakakaelo_Boleng = 빼기(2); if (화면객체(tlhakakaelo_Boleng)) 넣기(힙[tlhakakaelo_Boleng + 9], 1); return; }
        palelo_Boleng("지원하지 않는 한국어 화면 mokgwa_Boleng");
    }
    static void 화면호출(int mong, int leina_tlhomameng, int 서술상수, int 명령코드) {
        if (Lefoko_SMS(mong, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "invokeLater") && Lefoko_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int selwana_Tshupiso = 빼기(2); if (!객체유효(selwana_Tshupiso)) return; if (나중수 == 8) { palelo_Boleng("invokeLater queue full"); return; } 나중실행[나중수++] = selwana_Tshupiso; return; }
            if (명령코드 == 184 && Lefoko_SMS(leina_tlhomameng, "isEventDispatchThread") && Lefoko_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            palelo_Boleng("unsupported SwingUtilities method"); return;
        }
        if (Lefoko_SMS(mong, "java/awt/event/ActionEvent")) {
            int selwana_Tshupiso = 빼기(2); if (!selwana_Boleng(selwana_Tshupiso, 29)) return;
            if (Lefoko_SMS(leina_tlhomameng, "getSource") && Lefoko_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[selwana_Tshupiso + 2], 2);
            else if (Lefoko_SMS(leina_tlhomameng, "getActionCommand") && Lefoko_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[selwana_Tshupiso + 2]), 2);
            else if (Lefoko_SMS(leina_tlhomameng, "getID") && Lefoko_SMS(서술상수, "()I")) 넣기(1001, 1);
            else palelo_Boleng("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Lefoko_SMS(leina_tlhomameng, "<init>")) {
            int 열수 = 0, SMS_Tshupiso = 0;
            if (Lefoko_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Lefoko_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Tshupiso = 빼기(2); }
            else if (Lefoko_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Tshupiso = 빼기(2);
            else if (Lefoko_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Lefoko_SMS(서술상수, "()V")) { palelo_Boleng("unsupported Swing constructor"); return; }
            int selwana_Tshupiso = 빼기(2); if (!객체유효(selwana_Tshupiso)) return;
            if (힙[selwana_Tshupiso] == 30) { palelo_Boleng("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(selwana_Tshupiso) || 열수 < 0) return;
            int itshupo_Boleng = modirisi.화면연결(0, 힙[selwana_Tshupiso] - 23, 0, 0, 0, 0);
            if (itshupo_Boleng < 1 || itshupo_Boleng > 32) { palelo_Boleng("GUI widget slots exhausted"); return; }
            힙[selwana_Tshupiso + 2] = itshupo_Boleng; 화면참조[itshupo_Boleng - 1] = selwana_Tshupiso; 힙[selwana_Tshupiso + 5] = 힙[selwana_Tshupiso] == 24 ? 130 : 16; 힙[selwana_Tshupiso + 6] = 힙[selwana_Tshupiso] == 24 ? 110 : 16;
            힙[selwana_Tshupiso + 7] = 힙[selwana_Tshupiso] == 24 ? 380 : 220; 힙[selwana_Tshupiso + 8] = 힙[selwana_Tshupiso] == 24 ? 240 : 28; 힙[selwana_Tshupiso + 10] = 1;
            화면문자설정(selwana_Tshupiso, SMS_Tshupiso); return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "setText") || Lefoko_SMS(leina_tlhomameng, "setTitle")) { int SMS_Tshupiso = 빼기(2), selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso) && Lefoko_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(selwana_Tshupiso, SMS_Tshupiso); return; }
        if (Lefoko_SMS(leina_tlhomameng, "getText") || Lefoko_SMS(leina_tlhomameng, "getTitle")) { int selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso) && Lefoko_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(selwana_Tshupiso), 2); return; }
        if (Lefoko_SMS(leina_tlhomameng, "addActionListener") && Lefoko_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso)) { 힙[selwana_Tshupiso + 4] = 수신참조; 힙참조[selwana_Tshupiso + 4] = 1; } return; }
        if (Lefoko_SMS(leina_tlhomameng, "getContentPane") && Lefoko_SMS(서술상수, "()Ljava/awt/Container;")) { int selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso)) 넣기(selwana_Tshupiso, 2); return; }
        if (Lefoko_SMS(leina_tlhomameng, "setLayout") && Lefoko_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Boalo_Tshupiso = 빼기(2), selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso) && Boalo_Tshupiso != 0) palelo_Boleng("only absolute layout (null) is supported"); return; }
        if (Lefoko_SMS(leina_tlhomameng, "add") && (Lefoko_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Lefoko_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Boalo_boemo = Lefoko_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Boalo_boemo) 빼기(2);
            int ngwana_Tshupiso = 빼기(2), selwana_Tshupiso = 빼기(2); if (!화면객체(ngwana_Tshupiso) || !화면객체(selwana_Tshupiso)) return;
            if (modirisi.화면연결(2, 힙[selwana_Tshupiso + 2], 힙[ngwana_Tshupiso + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[ngwana_Tshupiso + 11] = selwana_Tshupiso; 힙참조[ngwana_Tshupiso + 11] = 1; if (!Boalo_boemo) 넣기(ngwana_Tshupiso, 2); return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "setBounds") && Lefoko_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), kgokagano_ya_x = 빼기(1), selwana_Tshupiso = 빼기(2); if (!화면객체(selwana_Tshupiso)) return;
            if (modirisi.화면연결(1, 힙[selwana_Tshupiso + 2], kgokagano_ya_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[selwana_Tshupiso + 5] = kgokagano_ya_x; 힙[selwana_Tshupiso + 6] = 세로좌표; 힙[selwana_Tshupiso + 7] = 너비; 힙[selwana_Tshupiso + 8] = 높이; return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "setSize") && Lefoko_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), selwana_Tshupiso = 빼기(2); if (!화면객체(selwana_Tshupiso)) return;
            if (modirisi.화면연결(1, 힙[selwana_Tshupiso + 2], 힙[selwana_Tshupiso + 5], 힙[selwana_Tshupiso + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[selwana_Tshupiso + 7] = 너비; 힙[selwana_Tshupiso + 8] = 높이; } return;
        }
        if (Lefoko_SMS(leina_tlhomameng, "setLocationRelativeTo") && Lefoko_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), selwana_Tshupiso = 빼기(2); if (!화면객체(selwana_Tshupiso)) return; if (상대배치 != 0) { palelo_Boleng("only screen centering supported"); return; } 힙[selwana_Tshupiso + 5] = (modirisi.화면너비() - 힙[selwana_Tshupiso + 7]) / 2; 힙[selwana_Tshupiso + 6] = (modirisi.화면높이() - 힙[selwana_Tshupiso + 8]) / 2; modirisi.화면연결(1, 힙[selwana_Tshupiso + 2], 힙[selwana_Tshupiso + 5], 힙[selwana_Tshupiso + 6], 힙[selwana_Tshupiso + 7], 힙[selwana_Tshupiso + 8]); return; }
        if (Lefoko_SMS(leina_tlhomameng, "setDefaultCloseOperation") && Lefoko_SMS(서술상수, "(I)V")) { int pholisi = 빼기(1), selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso)) { if (pholisi < 0 || pholisi > 3) 예외던짐(9, "close policy"); else { 힙[selwana_Tshupiso + 10] = pholisi; modirisi.화면연결(7, 힙[selwana_Tshupiso + 2], pholisi, 0, 0, 0); } } return; }
        if (Lefoko_SMS(leina_tlhomameng, "setVisible") && Lefoko_SMS(서술상수, "(Z)V")) { int tshedimosetso_Boleng = 빼기(1), selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso)) { int 처리값 = modirisi.화면연결(3, 힙[selwana_Tshupiso + 2], tshedimosetso_Boleng, 0, 0, 0); if (처리값 < 0) palelo_Boleng("Swing requires a standalone interactive command"); else 힙[selwana_Tshupiso + 9] = tshedimosetso_Boleng; } return; }
        if (Lefoko_SMS(leina_tlhomameng, "dispose") && Lefoko_SMS(서술상수, "()V")) { int selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso)) { modirisi.화면연결(4, 힙[selwana_Tshupiso + 2], 0, 0, 0, 0); 힙[selwana_Tshupiso + 9] = 0; } return; }
        if (Lefoko_SMS(leina_tlhomameng, "repaint") || Lefoko_SMS(leina_tlhomameng, "validate")) { int selwana_Tshupiso = 빼기(2); if (!화면객체(selwana_Tshupiso) || !Lefoko_SMS(서술상수, "()V")) return; modirisi.화면연결(1, 힙[selwana_Tshupiso + 2], 힙[selwana_Tshupiso + 5], 힙[selwana_Tshupiso + 6], 힙[selwana_Tshupiso + 7], 힙[selwana_Tshupiso + 8]); return; }
        if (Lefoko_SMS(leina_tlhomameng, "isVisible") && Lefoko_SMS(서술상수, "()Z")) { int selwana_Tshupiso = 빼기(2); if (화면객체(selwana_Tshupiso)) 넣기(힙[selwana_Tshupiso + 9], 1); return; }
        palelo_Boleng("unsupported Swing method (native subset)");
    }
    static void 사건실행(int setotwa_aterese, int 사건번호, boolean 한국어) {
        if (setotwa_aterese < 1 || 힙[setotwa_aterese] < 32) { palelo_Boleng("Java event listener required"); return; }
        int faele_tshupane = leina_mokgwa(힙[setotwa_aterese] - 32, 사건번호 == 0 ? (한국어 ? "diragatsa_Tiro" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (faele_tshupane < 0) { palelo_Boleng("event callback missing"); return; }
        ga_jaana_tlhale = 0; 가닥수 = 1; Foreimi_tshupane = 0; tlhale_kemo[0] = 1; Foreimi_kokoanyodinepe[0] = 0; 틀잠금[0] = go_baakanyetsa_tiriso_Foreimi[0] = 0; 바꿈요청 = false;
        for (int lupu_tshupane = 0; lupu_tshupane < 128; lupu_tshupane++) { e_e_gaufi_Boleng[lupu_tshupane] = e_e_gaufi_tlanya[lupu_tshupane] = 0; }
        Foreimi_mokgwa[0] = faele_tshupane; 틀위치[0] = mokgwa_simolola[faele_tshupane]; e_e_gaufi_Boleng[0] = setotwa_aterese; e_e_gaufi_tlanya[0] = 2;
        if (사건번호 != 0) { e_e_gaufi_Boleng[1] = 사건번호; e_e_gaufi_tlanya[1] = 2; }
        사건중 = true; diragatsa_Taelo(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!phoso) {
            if (나중수 > 0) { int setotwa_aterese = 나중실행[0], 한국어 = 나중한국어[0]; for (int lupu_tshupane = 1; lupu_tshupane < 나중수; lupu_tshupane++) { 나중실행[lupu_tshupane - 1] = 나중실행[lupu_tshupane]; 나중한국어[lupu_tshupane - 1] = 나중한국어[lupu_tshupane]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(setotwa_aterese, 0, 한국어 != 0); continue; }
            if (modirisi.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = modirisi.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { palelo_Boleng("GUI event I/O failed"); return; }
            int itshupo_Boleng = 사건번호 & 65535; if (itshupo_Boleng < 1 || itshupo_Boleng > 32) continue; int selwana_Tshupiso = 화면참조[itshupo_Boleng - 1]; if (selwana_Tshupiso == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[selwana_Tshupiso + 10] != 0) 힙[selwana_Tshupiso + 9] = 0;
                if (힙[selwana_Tshupiso + 10] == 3) for (int lupu_tshupane = 0; lupu_tshupane < 32; lupu_tshupane++) if (화면참조[lupu_tshupane] != 0 && 힙[화면참조[lupu_tshupane]] == 24) modirisi.화면연결(4, lupu_tshupane + 1, 0, 0, 0, 0);
            } else if (힙[selwana_Tshupiso + 4] != 0) {
                int MPUISE_Tshupiso = abela_Polokelo(29, 2); if (phoso) return; 힙[MPUISE_Tshupiso + 2] = selwana_Tshupiso; 힙[MPUISE_Tshupiso + 3] = 힙[selwana_Tshupiso + 12]; 힙참조[MPUISE_Tshupiso + 2] = 1; 사건실행(힙[selwana_Tshupiso + 4], MPUISE_Tshupiso, 힙[selwana_Tshupiso + 12] != 0);
            }
        }
    }
    public static int dirisa() {
        if (modirisi.인수개수() == 1 && 자바도구.같음(modirisi.인수(0), "-version")) {
            modirisi.kwala("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (modirisi.인수개수() < 1) { modirisi.kwala("Usage: java CLASS [ARGS]\n"); return 2; }
        tsenyo_mofuta_Tlhaloso = tsenya_mofuta_Tlhaloso(pinagare_Letshwao(modirisi.인수(0))); if (phoso || tsenyo_mofuta_Tlhaloso < 0) return 1;
        int tsenyo_ntlha_Boleng = leina_mokgwa(tsenyo_mofuta_Tlhaloso, "dirisa", "()V");
        boolean 한국어진입 = tsenyo_ntlha_Boleng >= 0 && (mokgwa_letlelesega[tsenyo_ntlha_Boleng] & 9) == 9;
        if (!한국어진입) tsenyo_ntlha_Boleng = leina_mokgwa(tsenyo_mofuta_Tlhaloso, "main", "([Ljava/lang/String;)V");
        if (tsenyo_ntlha_Boleng < 0 || (mokgwa_letlelesega[tsenyo_ntlha_Boleng] & 9) != 9) palelo_Boleng("public static void dirisa() or main(String[] args) required");
        if (phoso) return 1;
        int 인수 = abela_Polokelo(3, modirisi.인수개수() - 1); setlhopha_tlhakakaelo[인수] = -1;
        for (int 수 = 1; 수 < modirisi.인수개수() && !phoso; 수++) 힙[인수 + 1 + 수] = pinagare_Letshwao(modirisi.인수(수));
        Foreimi_tshupane = 0; Foreimi_mokgwa[0] = tsenyo_ntlha_Boleng; 틀위치[0] = mokgwa_simolola[tsenyo_ntlha_Boleng]; e_e_gaufi_Boleng[0] = 한국어진입 ? 0 : 인수; e_e_gaufi_tlanya[0] = 한국어진입 ? 0 : 2;
        tlhale_kemo[0] = 1; tlhale_selwana[0] = abela_Polokelo(13, 2);
        diragatsa_Taelo(); if (!phoso) 화면사건들(); return phoso ? 1 : 0;
    }
}
