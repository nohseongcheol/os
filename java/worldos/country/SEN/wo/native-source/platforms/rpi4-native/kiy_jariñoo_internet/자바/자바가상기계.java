// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. bara_denc/스택/Royukaay/car 경계를 def_ndigel 중 검사한다. */
public final class 자바가상기계 {
    static int[] bara_denc = new int[16 * 16384], 임시파일 = new int[16384], bara_denc_tur_SMS = new int[512];
    static int[] Lees_dul_soppi_xàmme = new int[8192], 상가 = new int[8192], 상나 = new int[8192], araf_yu_bennoo_Royukaay = new int[8192];
    static int[] doxalin_tur_SMS = new int[512], doxalin_xeet = new int[512], doxalin_jot = new int[512], doxalin_boroom = new int[512];
    static int[] doxalin_Door = new int[512], doxalin_jeexal = new int[512], doxalin_Tegalo = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], doxalin_Tegtal_xeet = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] dënnd_xëyma = new int[16384], dënnd_xeet = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] kadar_doxalin = new int[128], 틀위치 = new int[128], kadar_Tegalo = new int[128], kadar_ndigal = new int[128], doortal_kadar = new int[128];
    static int[] maas_Tekki_baat_tur = new int[16], maas_Tekki_baat_tolluwaay = new int[16], 종부모 = new int[16], maas_Tekki_baat_nekkin = new int[16], 종칸수 = new int[16], doortal_maas_Tekki_baat = new int[16];
    static int[] maas_jaarukaay = new int[16 * 16], 종접면수 = new int[16];
    static int[] xar_xar_tur = new int[512], xar_xar_xeet = new int[512], xar_xar_boroom = new int[512], xar_xar_sañ_sañ = new int[512], 칸위치 = new int[512], xar_xar_mbir = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], TABLO_cër = new int[32768], Store_lëmm = new int[256];
    static int tolluwaay, 읽기위치, 함수수, maas_tur, kadar_àlluwa_tur = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, dugal_xabaar_maas_Tekki_baat;
    static int[] buumug_jokkale_kadar = new int[4], buumug_jokkale_nekkin = new int[4], buumug_jokkale_yëf = new int[4], buumug_jokkale_luñu_name = new int[4], 가닥대기 = new int[4];
    static boolean njumte, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], maas_buumug_jokkale = new int[16];

    static void foo_xëyma(String Word_SMS) {
        if (njumte) return;
        int 분류코드 = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && kadar_àlluwa_tur >= 0) { 예외던짐(분류코드, Word_SMS); return; }
        kiy_jariñoo_internet.biir("JVM error: "); kiy_jariñoo_internet.biir(Word_SMS); kiy_jariñoo_internet.biir_Araf_xëyma(10); njumte = true;
    }
    static boolean kilip(int daw, int diir_xëyma) {
        if (daw < 0 || daw >= bara_denc.length || diir_xëyma < 0) return false;
        int maas_Tekki_baat = daw / 16384;
        return daw % 16384 <= maas_Tekki_baat_tolluwaay[maas_Tekki_baat] && diir_xëyma <= maas_Tekki_baat_tolluwaay[maas_Tekki_baat] - daw % 16384;
    }
    static int okte_xëyma() {
        if (!kilip(읽기위치, 1)) { foo_xëyma("truncated class file"); return 0; }
        return bara_denc[읽기위치++];
    }
    static int 짧은수() { return okte_xëyma() << 8 | okte_xëyma(); }
    static int lëmm() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int diir_xëyma) { if (!kilip(읽기위치, diir_xëyma)) foo_xëyma("invalid attribute size"); else 읽기위치 += diir_xëyma; }
    static boolean sek_Lees_dul_soppi(int 수, int 종류) {
        if (수 <= 0 || 수 >= Lees_dul_soppi_xàmme.length || Lees_dul_soppi_xàmme[수] != 종류) { foo_xëyma("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int daw, int diir_xëyma, String Word_SMS) {
        if (!kilip(daw, diir_xëyma)) return false;
        int 읽는자리 = daw, 끝 = daw + diir_xëyma;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < Word_SMS.length(); wërngël_àlluwa_tur++) {
            int kotu_araf = Word_SMS.charAt(wërngël_àlluwa_tur);
            if (kotu_araf > 0 && kotu_araf < 128) { if (읽는자리 >= 끝 || bara_denc[읽는자리++] != kotu_araf) return false; }
            else if (kotu_araf < 2048) {
                if (읽는자리 + 2 > 끝 || bara_denc[읽는자리++] != (192 | (kotu_araf >> 6)) || bara_denc[읽는자리++] != (128 | (kotu_araf & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || bara_denc[읽는자리++] != (224 | (kotu_araf >> 12)) || bara_denc[읽는자리++] != (128 | ((kotu_araf >> 6) & 63)) || bara_denc[읽는자리++] != (128 | (kotu_araf & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int xëyma = 짧은수(); return xëyma == 0 ? 0 : 현재읽는종 * 512 + xëyma; }
    static int 명상수() { return doxalin_boroom[kadar_doxalin[kadar_àlluwa_tur]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !njumte; 수++) { sek_Lees_dul_soppi(상번호(), 1); 건너(lëmm()); }
    }
    static int ndigel_diir(int xëyma) {
        if (xëyma == 16 || xëyma == 18 || xëyma == 21 || xëyma == 25 || xëyma == 54 || xëyma == 58 || xëyma == 188) return 2;
        if (xëyma == 17 || xëyma == 19 || xëyma == 132 || xëyma >= 153 && xëyma <= 167
            || xëyma >= 178 && xëyma <= 184 || xëyma == 187 || xëyma == 189 || xëyma == 192 || xëyma == 193 || xëyma == 198 || xëyma == 199) return 3;
        if (xëyma == 185 || xëyma == 200) return 5;
        if (xëyma >= 0 && xëyma <= 8 || xëyma >= 26 && xëyma <= 29 || xëyma >= 42 && xëyma <= 46 || xëyma >= 50 && xëyma <= 53
            || xëyma >= 59 && xëyma <= 62 || xëyma >= 75 && xëyma <= 79 || xëyma >= 83 && xëyma <= 95
            || xëyma == 96 || xëyma == 100 || xëyma == 104 || xëyma == 108 || xëyma == 112 || xëyma == 116
            || xëyma == 120 || xëyma == 122 || xëyma == 124 || xëyma == 126 || xëyma == 128 || xëyma == 130
            || xëyma >= 145 && xëyma <= 147 || xëyma == 172 || xëyma == 176 || xëyma == 177 || xëyma == 190 || xëyma == 191
            || xëyma == 194 || xëyma == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!kilip(읽는자리, 4)) { foo_xëyma("truncated bytecode operand"); return 0; }
        return bara_denc[읽는자리] << 24 | bara_denc[읽는자리 + 1] << 16 | bara_denc[읽는자리 + 2] << 8 | bara_denc[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int daw, int 끝) {
        int xëyma = bara_denc[읽는자리], diir_xëyma = ndigel_diir(xëyma);
        if (xëyma == 170 || xëyma == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - daw) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (xëyma == 170 ? 12 : 8)) return 0;
            int 항목수 = xëyma == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            diir_xëyma = 기준자리 - 읽는자리 + (xëyma == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (xëyma == 196 && 읽는자리 + 1 < 끝) {
            int Word_mbir = bara_denc[읽는자리 + 1]; diir_xëyma = Word_mbir == 132 ? 6 : (Word_mbir == 21 || Word_mbir == 25 || Word_mbir == 54 || Word_mbir == 58) ? 4 : 0;
        }
        return diir_xëyma > 0 && diir_xëyma <= 끝 - 읽는자리 ? diir_xëyma : 0;
    }
    static void sek_jëmmukaay_xëyma(int jëmmukaay_xëyma, int liëey_xëyma) {
        if (jëmmukaay_xëyma < doxalin_Door[liëey_xëyma] || jëmmukaay_xëyma >= doxalin_jeexal[liëey_xëyma] || 경계[jëmmukaay_xëyma] != liëey_xëyma + 1) foo_xëyma("invalid branch target");
    }
    static void 클래스읽기(int maas_Tekki_baat) {
        현재읽는종 = maas_Tekki_baat; 읽기위치 = maas_Tekki_baat * 16384; tolluwaay = 읽기위치 + maas_Tekki_baat_tolluwaay[maas_Tekki_baat];
        if (lëmm() != 0xcafebabe) { foo_xëyma("not a class file"); return; }
        int 부판 = 짧은수(), taalif_xëyma = 짧은수();
        if (taalif_xëyma < 45 || taalif_xëyma > 52 || 부판 != 0) { foo_xëyma("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = maas_Tekki_baat * 512;
        if (상수수 < 1 || 상수수 > 512) { foo_xëyma("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !njumte; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = okte_xëyma(); Lees_dul_soppi_xàmme[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = lëmm();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else foo_xëyma("unsupported constant type");
        }
        int sañ_sañ_xëyma = 짧은수();
        if ((sañ_sañ_xëyma & (0x2000 | 0x4000)) != 0) foo_xëyma("annotation/enum class unsupported");
        maas_Tekki_baat_tur[maas_Tekki_baat] = maas_tur_SMS(상번호());
        종부모[maas_Tekki_baat] = maas_tur_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { foo_xëyma("interface count limit"); return; }
        종접면수[maas_Tekki_baat] = 접면수;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 접면수; wërngël_àlluwa_tur++) maas_jaarukaay[maas_Tekki_baat * 16 + wërngël_àlluwa_tur] = maas_tur_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { foo_xëyma("field count limit (512)"); return; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 필드수 && !njumte; wërngël_àlluwa_tur++) {
            int bara_denc_àlluwa_tur = 칸수++; xar_xar_boroom[bara_denc_àlluwa_tur] = maas_Tekki_baat; xar_xar_sañ_sañ[bara_denc_àlluwa_tur] = 짧은수(); xar_xar_tur[bara_denc_àlluwa_tur] = 상번호(); xar_xar_xeet[bara_denc_àlluwa_tur] = 상번호();
            sek_Lees_dul_soppi(xar_xar_tur[bara_denc_àlluwa_tur], 1); sek_Lees_dul_soppi(xar_xar_xeet[bara_denc_àlluwa_tur], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[xar_xar_xeet[bara_denc_àlluwa_tur]]; int 분류코드 = 서술형(읽기위치 + 상나[xar_xar_xeet[bara_denc_àlluwa_tur]], false); 읽기위치 = 보존값;
            if ((xar_xar_sañ_sañ[bara_denc_àlluwa_tur] & 8) == 0) 칸위치[bara_denc_àlluwa_tur] = 종칸수[maas_Tekki_baat]++;
            int jagle_mbir = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < jagle_mbir && !njumte; 안쪽자리++) {
                int tur_Lees_dul_soppi = 상번호(), 유효길이 = lëmm();
                if (Word_SMS(tur_Lees_dul_soppi, "ConstantValue") && 유효길이 == 2) {
                    int mbir_xëyma = 상번호();
                    if (분류코드 == 1 && sek_Lees_dul_soppi(mbir_xëyma, 3)) xar_xar_mbir[bara_denc_àlluwa_tur] = 상가[mbir_xëyma];
                    else if (분류코드 == 2 && sek_Lees_dul_soppi(mbir_xëyma, 8)) xar_xar_mbir[bara_denc_àlluwa_tur] = Lees_dul_soppi_SMS(상가[mbir_xëyma]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { foo_xëyma("method count limit (512)"); return; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 개수 && !njumte; wërngël_àlluwa_tur++) {
            int 수 = 함수수++; doxalin_boroom[수] = maas_Tekki_baat;
            doxalin_jot[수] = 짧은수(); doxalin_tur_SMS[수] = 상번호(); doxalin_xeet[수] = 상번호();
            sek_Lees_dul_soppi(doxalin_tur_SMS[수], 1); 서술읽기(수);
            if ((doxalin_jot[수] & 8) == 0) {
                if (함수인수수[수] == 16) { foo_xëyma("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) doxalin_Tegtal_xeet[수 * 16 + 비교자리] = doxalin_Tegtal_xeet[수 * 16 + 비교자리 - 1];
                doxalin_Tegtal_xeet[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((doxalin_jot[수] & 0x100) != 0) foo_xëyma("user native method unsupported");
            if (Word_SMS(doxalin_tur_SMS[수], "<clinit>")) doortal_maas_Tekki_baat[maas_Tekki_baat] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (doxalin_boroom[앞] == maas_Tekki_baat && 같은말(doxalin_tur_SMS[앞], doxalin_tur_SMS[수]) && 같은말(doxalin_xeet[앞], doxalin_xeet[수])) foo_xëyma("duplicate method");
            int 속성수 = 짧은수();
            for (int jagle_xëyma = 0; jagle_xëyma < 속성수 && !njumte; jagle_xëyma++) {
                int tur_253d1510 = 상번호(), diir_xëyma = lëmm(), daw = 읽기위치;
                if (!kilip(daw, diir_xëyma)) { foo_xëyma("truncated method attribute"); break; }
                if (Word_SMS(tur_253d1510, "Code")) {
                    if (doxalin_Door[수] != 0) foo_xëyma("duplicate Code attribute");
                    doxalin_Tegalo[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = lëmm();
                    if (doxalin_Tegalo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) foo_xëyma("method memory limits exceeded");
                    doxalin_Door[수] = 읽기위치; 건너(코드길이); doxalin_jeexal[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { foo_xëyma("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int njumte_Royukaay = 잡기수++; 잡기함수[njumte_Royukaay] = 수;
                        잡기시작[njumte_Royukaay] = doxalin_Door[수] + 짧은수(); 잡기끝[njumte_Royukaay] = doxalin_Door[수] + 짧은수();
                        잡기위치[njumte_Royukaay] = doxalin_Door[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[njumte_Royukaay] = 부호값 == 0 ? 0 : maas_tur_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != daw + diir_xëyma) foo_xëyma("Code attribute size mismatch");
                } else 건너(diir_xëyma);
            }
            if ((doxalin_jot[수] & 0x400) != 0) continue;
            if (doxalin_Door[수] == 0) foo_xëyma("missing Code attribute");
            int xar_xar_dugal_xabaar = doxalin_Door[수];
            while (xar_xar_dugal_xabaar < doxalin_jeexal[수] && !njumte) {
                int diir_xëyma = 길이읽기(xar_xar_dugal_xabaar, doxalin_Door[수], doxalin_jeexal[수]);
                if (diir_xëyma == 0) { foo_xëyma("unsupported or truncated bytecode"); break; }
                경계[xar_xar_dugal_xabaar] = 수 + 1; xar_xar_dugal_xabaar += diir_xëyma;
            }
            xar_xar_dugal_xabaar = doxalin_Door[수];
            while (xar_xar_dugal_xabaar < doxalin_jeexal[수] && !njumte) {
                int xëyma = bara_denc[xar_xar_dugal_xabaar];
                if (xëyma >= 153 && xëyma <= 167 || xëyma == 198 || xëyma == 199) sek_jëmmukaay_xëyma(xar_xar_dugal_xabaar + (short)(bara_denc[xar_xar_dugal_xabaar + 1] << 8 | bara_denc[xar_xar_dugal_xabaar + 2]), 수);
                if (xëyma == 200) sek_jëmmukaay_xëyma(xar_xar_dugal_xabaar + 위치정수(xar_xar_dugal_xabaar + 1), 수);
                if (xëyma == 170 || xëyma == 171) {
                    int 읽는자리 = xar_xar_dugal_xabaar + 1; while ((읽는자리 - doxalin_Door[수]) % 4 != 0) 읽는자리++;
                    sek_jëmmukaay_xëyma(xar_xar_dugal_xabaar + 위치정수(읽는자리), 수);
                    int 항목수 = xëyma == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += xëyma == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) sek_jëmmukaay_xëyma(xar_xar_dugal_xabaar + 위치정수(읽는자리 + 안쪽자리 * (xëyma == 170 ? 4 : 8) + (xëyma == 170 ? 0 : 4)), 수);
                }
                xar_xar_dugal_xabaar += 길이읽기(xar_xar_dugal_xabaar, doxalin_Door[수], doxalin_jeexal[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                sek_jëmmukaay_xëyma(잡기시작[안쪽자리], 수); sek_jëmmukaay_xëyma(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != doxalin_jeexal[수]) sek_jëmmukaay_xëyma(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) foo_xëyma("invalid exception range");
            }
        }
        if (!njumte) 속성건너();
        if (읽기위치 != tolluwaay) foo_xëyma("extra class file data");
    }
    static int jagleel_Dencukaay(int 종류, int diir_xëyma) { return 새기억(종류, diir_xëyma); }
    static boolean yëf_xëyma(int Royukaay, int 종류) {
        if (!객체유효(Royukaay)) return false;
        if (힙[Royukaay] != 종류) { foo_xëyma("object type mismatch"); return false; }
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
        if (반환형 == 2) saama_xëyma(스택값[xar_xar_dugal_xabaar]);
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
        if (kadar_àlluwa_tur % 32 == 31) { foo_xëyma("call stack limit (32)"); return; }
        int 다음 = kadar_àlluwa_tur + 1;
        for (int 수 = 0; 수 < 128; 수++) dënnd_xeet[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[liëey_xëyma] - 1; 수 >= 0; 수--) {
            dënnd_xëyma[다음 * 128 + 수] = 빼기(doxalin_Tegtal_xeet[liëey_xëyma * 16 + 수]); dënnd_xeet[다음 * 128 + 수] = doxalin_Tegtal_xeet[liëey_xëyma * 16 + 수];
        }
        if (njumte) return;
        kadar_àlluwa_tur = 다음; doortal_kadar[kadar_àlluwa_tur] = 0; kadar_doxalin[kadar_àlluwa_tur] = liëey_xëyma; 틀위치[kadar_àlluwa_tur] = doxalin_Door[liëey_xëyma]; kadar_Tegalo[kadar_àlluwa_tur] = 0;
    }
    static void 반환(int xeet_xëyma) {
        if (xeet_xëyma != 함수반환[kadar_doxalin[kadar_àlluwa_tur]]) { foo_xëyma("return type mismatch"); return; }
        int xëyma = xeet_xëyma == 0 ? 0 : 빼기(xeet_xëyma);
        if (doortal_kadar[kadar_àlluwa_tur] != 0) maas_Tekki_baat_nekkin[doortal_kadar[kadar_àlluwa_tur] - 1] = 2;
        if (틀잠금[kadar_àlluwa_tur] != 0) { 잠금풀기(틀잠금[kadar_àlluwa_tur]); 틀잠금[kadar_àlluwa_tur] = 0; }
        kadar_àlluwa_tur--; if (kadar_àlluwa_tur >= 현재가닥 * 32 && xeet_xëyma != 0) 넣기(xëyma, xeet_xëyma);
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
                if (xëyma < 1) { foo_xëyma("invalid file stream path"); return; }
                dawal_bara_denc_tur[xar_xar_dugal_xabaar] = xëyma;
            }
            dawal_bara_denc_tur[diir_xëyma] = 0;
            int 서술자 = kiy_jariñoo_internet.파일서술자열기(dawal_bara_denc_tur, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { foo_xëyma("FileNotFoundException: file open failed"); return; }
            힙[dawal_xëyma + 2] = 서술자; 힙[dawal_xëyma + 3] = 1;
            return;
        }
        if (ndigel != 182) { foo_xëyma("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(tur_253d1510, "write") || !출력 && Word_SMS(tur_253d1510, "read"))
            && (Word_SMS(dayo_xëyma, 출력 ? "([B)V" : "([B)I") || Word_SMS(dayo_xëyma, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean kilip_xëyma = Word_SMS(dayo_xëyma, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = kilip_xëyma ? 빼기(1) : 0, 시작점 = kilip_xëyma ? 빼기(1) : 0, mbir_TABLO = 빼기(2), yëf_Royukaay = 빼기(2);
            if (!yëf_xëyma(mbir_TABLO, 20) || !yëf_xëyma(yëf_Royukaay, 종류)) return;
            if (!kilip_xëyma) 항목수 = 힙[mbir_TABLO + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[mbir_TABLO + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[yëf_Royukaay + 3] == 0 || 힙[yëf_Royukaay + 2] < 0) { foo_xëyma("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !njumte) {
                int 반환값 = 출력 ? kiy_jariñoo_internet.파일한바이트쓰기(힙[yëf_Royukaay + 2], 힙[mbir_TABLO + 2 + 시작점 + 완료수]) : kiy_jariñoo_internet.파일한바이트읽기(힙[yëf_Royukaay + 2]);
                if (반환값 < 0) { foo_xëyma(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[mbir_TABLO + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_SMS(tur_253d1510, "flush") && Word_SMS(dayo_xëyma, "()V")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 종류) && 힙[yëf_Royukaay + 2] < 0) foo_xëyma("IOException: stream closed"); return; }
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
            if (결과 < -1) foo_xëyma("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (kiy_jariñoo_internet.파일한바이트쓰기(서술자, xëyma) != 1) foo_xëyma("IOException: write failed");
    }
    static void Wuute_doxalin(int àlluwa_tur, int ndigel) {
        if (àlluwa_tur <= 0 || àlluwa_tur >= Lees_dul_soppi_xàmme.length || (Lees_dul_soppi_xàmme[àlluwa_tur] != 10 && Lees_dul_soppi_xàmme[àlluwa_tur] != 11)) { foo_xëyma("invalid method reference"); return; }
        int boroom_xëyma = maas_tur_SMS(상가[àlluwa_tur]), tur_253d1510 = Royukaay_tur(상나[àlluwa_tur]), dayo_xëyma = Royukaay_xeet(상나[àlluwa_tur]);
        if (njumte) return;
        if (기본호출(boroom_xëyma, tur_253d1510, dayo_xëyma, ndigel)) return;
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
        int maas_Tekki_baat = seet_maas_Tekki_baat(boroom_xëyma); if (maas_Tekki_baat < 0 || njumte) return;
        int bara_denc_àlluwa_tur = seet_doxalin(maas_Tekki_baat, tur_253d1510, dayo_xëyma);
        if (bara_denc_àlluwa_tur < 0) {
            for (int kotu_araf = maas_Tekki_baat, 항목수 = 0; kotu_araf >= 0 && 항목수 < 16; 항목수++, kotu_araf = 부모종(kotu_araf))
                if (Word_SMS(종부모[kotu_araf], "java/lang/Thread")) { 가닥호출(tur_253d1510, dayo_xëyma, ndigel); return; }
            foo_xëyma("NoSuchMethodError"); return;
        }
        if (((doxalin_jot[bara_denc_àlluwa_tur] & 8) != 0) != (ndigel == 184)) { foo_xëyma("method static/instance mismatch"); return; }
        if (ndigel == 184) { if (!doortal(doxalin_boroom[bara_denc_àlluwa_tur], kadar_ndigal[kadar_àlluwa_tur])) return; }
        else {
            int 읽는자리 = kadar_Tegalo[kadar_àlluwa_tur] - 함수인수수[bara_denc_àlluwa_tur];
            if (읽는자리 < 0 || 스택형[kadar_àlluwa_tur * 128 + 읽는자리] != 2) { foo_xëyma("invalid method receiver"); return; }
            int yëf_Royukaay = 스택값[kadar_àlluwa_tur * 128 + 읽는자리];
            if (!객체유효(yëf_Royukaay)) return;
            if (힙[yëf_Royukaay] < 32 || !종포함(힙[yëf_Royukaay] - 32, boroom_xëyma)) { foo_xëyma("method receiver type mismatch"); return; }
            if (ndigel != 183) bara_denc_àlluwa_tur = seet_doxalin(힙[yëf_Royukaay] - 32, tur_253d1510, dayo_xëyma);
        }
        if (bara_denc_àlluwa_tur < 0 || (doxalin_jot[bara_denc_àlluwa_tur] & 0x400) != 0) { foo_xëyma("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((doxalin_jot[bara_denc_àlluwa_tur] & 32) != 0) {
            if (ndigel == 184) { int kotu_araf = doxalin_boroom[bara_denc_àlluwa_tur]; if (종잠금[kotu_araf] == 0) 종잠금[kotu_araf] = jagleel_Dencukaay(8, 0); 잠금참조 = 종잠금[kotu_araf]; }
            else 잠금참조 = 스택값[kadar_àlluwa_tur * 128 + kadar_Tegalo[kadar_àlluwa_tur] - 함수인수수[bara_denc_àlluwa_tur]];
            if (!잠금얻기(잠금참조)) { if (!njumte) 틀위치[kadar_àlluwa_tur] = kadar_ndigal[kadar_àlluwa_tur]; return; }
        }
        호출(bara_denc_àlluwa_tur); if (!njumte) 틀잠금[kadar_àlluwa_tur] = 잠금참조;
    }
    static boolean 배열저장가능(int TABLO_Royukaay, int mbir_xëyma) {
        if (mbir_xëyma == 0 || TABLO_cër[TABLO_Royukaay] == 0) return true;
        boolean 성공여부 = TABLO_cër[TABLO_Royukaay] == -1 ? (mbir_xëyma > 0 && mbir_xëyma < 힙끝 && 힙[mbir_xëyma] == 1) : 맞는객체(mbir_xëyma, TABLO_cër[TABLO_Royukaay]);
        if (!성공여부 && !njumte) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int TABLO_xar_xar(int Royukaay, int dajale_xëyma, int xeet_xëyma) {
        if (!yëf_xëyma(Royukaay, xeet_xëyma)) return 0;
        if (dajale_xëyma < 0 || dajale_xëyma >= 힙[Royukaay + 1]) { foo_xëyma("ArrayIndexOutOfBoundsException"); return 0; }
        return Royukaay + 2 + dajale_xëyma;
    }
    static void def_ndigel() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (njumte) { if (던진객체 != 0) 예외처리(); if (njumte || kadar_àlluwa_tur < 현재가닥 * 32) break; }
            if (kadar_àlluwa_tur < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!jalantu_buumug_jokkale()) break; 조각 = 100; }
            if (kadar_àlluwa_tur == 0 && maas_Tekki_baat_nekkin[dugal_xabaar_maas_Tekki_baat] != 2 && !doortal(dugal_xabaar_maas_Tekki_baat, 틀위치[kadar_àlluwa_tur])) continue;
            if (kadar_àlluwa_tur == 현재가닥 * 32 && 현재가닥 != 0 && (doxalin_jot[kadar_doxalin[kadar_àlluwa_tur]] & 32) != 0 && 틀잠금[kadar_àlluwa_tur] == 0) {
                int yëf_Royukaay = buumug_jokkale_luñu_name[현재가닥]; if (!잠금얻기(yëf_Royukaay)) { if (njumte) break; continue; } 틀잠금[kadar_àlluwa_tur] = yëf_Royukaay;
            }
            잠시수 = 0;
            if (--남음 == 0) { foo_xëyma("instruction limit (500000)"); break; }
            int daw = 틀위치[kadar_àlluwa_tur]; kadar_ndigal[kadar_àlluwa_tur] = daw; int xëyma = 명바();
            if (njumte) break;
            if (xëyma == 0) continue;
            if (xëyma == 1) { 넣기(0, 2); continue; }
            if (xëyma >= 2 && xëyma <= 8) { 넣기(xëyma - 3, 1); continue; }
            if (xëyma == 16) { 넣기((byte)명바(), 1); continue; }
            if (xëyma == 17) { 넣기((short)명짧(), 1); continue; }
            if (xëyma == 18 || xëyma == 19) {
                int 수 = doxalin_boroom[kadar_doxalin[kadar_àlluwa_tur]] * 512 + (xëyma == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= Lees_dul_soppi_xàmme.length) foo_xëyma("invalid ldc constant");
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
            if (xëyma == 46 || xëyma >= 50 && xëyma <= 53) {
                int 항목자리 = 빼기(1), yëf_Royukaay = 빼기(2), 분류코드 = xëyma == 46 ? 2 : xëyma == 50 ? 3 : xëyma == 51 ? 20 : xëyma == 52 ? 22 : 23;
                if (xëyma == 51 && yëf_Royukaay > 0 && yëf_Royukaay < 힙끝 && 힙[yëf_Royukaay] == 21) 분류코드 = 21;
                int 읽는자리 = TABLO_xar_xar(yëf_Royukaay, 항목자리, 분류코드); if (!njumte) 넣기(힙[읽는자리], xëyma == 50 ? 2 : 1); continue;
            }
            if (xëyma == 79 || xëyma >= 83 && xëyma <= 86) {
                int dugal_xabaar_Royukaay = 빼기(xëyma == 83 ? 2 : 1), 항목자리 = 빼기(1), yëf_Royukaay = 빼기(2), 분류코드 = xëyma == 79 ? 2 : xëyma == 83 ? 3 : xëyma == 84 ? 20 : xëyma == 85 ? 22 : 23;
                if (xëyma == 84 && yëf_Royukaay > 0 && yëf_Royukaay < 힙끝 && 힙[yëf_Royukaay] == 21) 분류코드 = 21;
                int 읽는자리 = TABLO_xar_xar(yëf_Royukaay, 항목자리, 분류코드);
                if (!njumte && 분류코드 == 3 && !배열저장가능(yëf_Royukaay, dugal_xabaar_Royukaay)) continue;
                if (!njumte) 힙[읽는자리] = 분류코드 == 20 ? (byte)dugal_xabaar_Royukaay : 분류코드 == 21 ? dugal_xabaar_Royukaay & 1 : 분류코드 == 22 ? (char)dugal_xabaar_Royukaay : 분류코드 == 23 ? (short)dugal_xabaar_Royukaay : dugal_xabaar_Royukaay;
                continue;
            }
            if (xëyma >= 87 && xëyma <= 95) { Tegalo_ndigal(xëyma); continue; }
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
            if (xëyma >= 178 && xëyma <= 181) { 필드호출(명상수(), xëyma, daw); continue; }
            if (xëyma >= 182 && xëyma <= 185) {
                int 부호값 = 명상수();
                if (xëyma == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { foo_xëyma("invalid invokeinterface operands"); continue; } }
                Wuute_doxalin(부호값, xëyma); continue;
            }
            if (xëyma == 187) { 새객체(maas_tur_SMS(명상수()), daw); continue; }
            if (xëyma == 188 || xëyma == 189) {
                int 분류코드 = 3, bu_ci_bokk = 0;
                if (xëyma == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else bu_ci_bokk = maas_tur_SMS(명상수());
                if (분류코드 == 0) { foo_xëyma("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), yëf_Royukaay = jagleel_Dencukaay(분류코드, 유효길이); if (!njumte) TABLO_cër[yëf_Royukaay] = bu_ci_bokk; 넣기(yëf_Royukaay, 2); continue;
            }
            if (xëyma == 190) {
                int yëf_Royukaay = 빼기(2);
                if (객체유효(yëf_Royukaay)) { int 비교자리 = 힙[yëf_Royukaay]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) foo_xëyma("not an array"); else 넣기(힙[yëf_Royukaay + 1], 1); }
                continue;
            }
            if (xëyma == 191) {
                int yëf_Royukaay = 빼기(2); if (객체유효(yëf_Royukaay)) { if (힙[yëf_Royukaay] != 9) foo_xëyma("athrow requires supported Throwable"); else { 던진객체 = yëf_Royukaay; njumte = true; } }
                continue;
            }
            if (xëyma == 192 || xëyma == 193) {
                int tur_Lees_dul_soppi = maas_tur_SMS(명상수()), yëf_Royukaay = 빼기(2); boolean 일치여부 = 맞는객체(yëf_Royukaay, tur_Lees_dul_soppi);
                if (xëyma == 193) 넣기(yëf_Royukaay != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !njumte) foo_xëyma("ClassCastException"); 넣기(yëf_Royukaay, 2); }
                continue;
            }
            if (xëyma == 170 || xëyma == 171) {
                int 읽는자리 = daw + 1, bara_denc_àlluwa_tur = kadar_doxalin[kadar_àlluwa_tur], kër_Royukaay = 빼기(1);
                while ((읽는자리 - doxalin_Door[bara_denc_àlluwa_tur]) % 4 != 0) 읽는자리++;
                int luñu_name_dëkkuwaay = 위치정수(읽는자리);
                if (xëyma == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (kër_Royukaay >= 낮은값 && kër_Royukaay <= 높은값) luñu_name_dëkkuwaay = 위치정수(읽는자리 + 12 + (kër_Royukaay - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 총수; wërngël_àlluwa_tur++) if (위치정수(읽는자리 + 8 + wërngël_àlluwa_tur * 8) == kër_Royukaay) luñu_name_dëkkuwaay = 위치정수(읽는자리 + 12 + wërngël_àlluwa_tur * 8); }
                toxal_xëyma(daw + luñu_name_dëkkuwaay); continue;
            }
            if (xëyma == 200) { toxal_xëyma(daw + 위치정수(daw + 1)); continue; }
            if (xëyma == 194 || xëyma == 195) {
                int yëf_Royukaay = 빼기(2);
                if (xëyma == 195) 잠금풀기(yëf_Royukaay);
                else if (!잠금얻기(yëf_Royukaay) && !njumte) { 넣기(yëf_Royukaay, 2); 틀위치[kadar_àlluwa_tur] = daw; }
                continue;
            }
            if (xëyma == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) biir_dënnd(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); biir_dënnd(항목자리, 1); }
                else foo_xëyma("unsupported wide opcode");
                continue;
            }
            foo_xëyma("unsupported bytecode");
        }
    }
    static int seet_maas_Tekki_baat(int tur_253d1510) {
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 종수; wërngël_àlluwa_tur++) if (maas_Tekki_baat_tur[wërngël_àlluwa_tur] != 0 && 같은말(maas_Tekki_baat_tur[wërngël_àlluwa_tur], tur_253d1510)) return wërngël_àlluwa_tur;
        return Yab_maas_Tekki_baat(Lees_dul_soppi_SMS(tur_253d1510));
    }
    static int Yab_maas_Tekki_baat(int tur_araf_yu_bennoo) {
        if (!yëf_xëyma(tur_araf_yu_bennoo, 1)) return -1;
        int diir_xëyma = 힙[tur_araf_yu_bennoo + 1];
        if (diir_xëyma < 1 || diir_xëyma > 505 || 종수 == 16) { foo_xëyma("class name/count limit"); return -1; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < diir_xëyma; wërngël_àlluwa_tur++) { int kotu_araf = 힙[tur_araf_yu_bennoo + 2 + wërngël_àlluwa_tur]; bara_denc_tur_SMS[wërngël_àlluwa_tur] = kotu_araf == '/' ? '.' : kotu_araf; }
        bara_denc_tur_SMS[diir_xëyma] = '.'; bara_denc_tur_SMS[diir_xëyma + 1] = 'c'; bara_denc_tur_SMS[diir_xëyma + 2] = 'l'; bara_denc_tur_SMS[diir_xëyma + 3] = 'a'; bara_denc_tur_SMS[diir_xëyma + 4] = 's'; bara_denc_tur_SMS[diir_xëyma + 5] = 's'; bara_denc_tur_SMS[diir_xëyma + 6] = 0;
        int tolluwaay = kiy_jariñoo_internet.파일읽기(bara_denc_tur_SMS, 임시파일);
        if (tolluwaay < 0) { foo_xëyma("ClassNotFoundException"); return -1; }
        int maas_Tekki_baat = 종수++; maas_Tekki_baat_tolluwaay[maas_Tekki_baat] = tolluwaay;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) bara_denc[maas_Tekki_baat * 16384 + wërngël_àlluwa_tur] = 임시파일[wërngël_àlluwa_tur];
        클래스읽기(maas_Tekki_baat); if (njumte) return -1;
        int liteew_mbir = Lees_dul_soppi_SMS(maas_Tekki_baat_tur[maas_Tekki_baat]);
        if (!글같음(liteew_mbir, tur_araf_yu_bennoo, true)) { foo_xëyma("class name does not match file"); return -1; }
        int 부모 = 종부모[maas_Tekki_baat];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = seet_maas_Tekki_baat(부모);
            if (njumte || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == maas_Tekki_baat) { foo_xëyma("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int bara_denc_àlluwa_tur = 0; bara_denc_àlluwa_tur < 칸수; bara_denc_àlluwa_tur++) if (xar_xar_boroom[bara_denc_àlluwa_tur] == maas_Tekki_baat && (xar_xar_sañ_sañ[bara_denc_àlluwa_tur] & 8) == 0) 칸위치[bara_denc_àlluwa_tur] += 시작변위;
            종칸수[maas_Tekki_baat] += 시작변위;
        }
        return maas_Tekki_baat;
    }
    static int 부모종(int maas_Tekki_baat) {
        int tur_253d1510 = 종부모[maas_Tekki_baat];
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 종수; wërngël_àlluwa_tur++) if (tur_253d1510 != 0 && maas_Tekki_baat_tur[wërngël_àlluwa_tur] != 0 && 같은말(maas_Tekki_baat_tur[wërngël_àlluwa_tur], tur_253d1510)) return wërngël_àlluwa_tur;
        return -1;
    }
    static int seet_doxalin(int maas_Tekki_baat, int tur_253d1510, int dayo_xëyma) {
        for (int 깊이 = 0; maas_Tekki_baat >= 0 && 깊이 < 16; 깊이++, maas_Tekki_baat = 부모종(maas_Tekki_baat)) {
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 함수수; wërngël_àlluwa_tur++) if (doxalin_boroom[wërngël_àlluwa_tur] == maas_Tekki_baat && 같은말(doxalin_tur_SMS[wërngël_àlluwa_tur], tur_253d1510) && 같은말(doxalin_xeet[wërngël_àlluwa_tur], dayo_xëyma)) return wërngël_àlluwa_tur;
        }
        return -1;
    }
    static int tur_doxalin(int maas_Tekki_baat, String tur_253d1510, String dayo_xëyma) {
        for (int 깊이 = 0; maas_Tekki_baat >= 0 && 깊이 < 16; 깊이++, maas_Tekki_baat = 부모종(maas_Tekki_baat))
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 함수수; wërngël_àlluwa_tur++) if (doxalin_boroom[wërngël_àlluwa_tur] == maas_Tekki_baat && Word_SMS(doxalin_tur_SMS[wërngël_àlluwa_tur], tur_253d1510) && Word_SMS(doxalin_xeet[wërngël_àlluwa_tur], dayo_xëyma)) return wërngël_àlluwa_tur;
        return -1;
    }
    static int 형종류(int tur_253d1510) { return bara_denc[상가[tur_253d1510]] == 'L' || bara_denc[상가[tur_253d1510]] == '[' ? 2 : 1; }
    static boolean doortal(int maas_Tekki_baat, int ndigel_Door) {
        if (maas_Tekki_baat < 0 || njumte) return false;
        if (maas_Tekki_baat_nekkin[maas_Tekki_baat] == 3) { foo_xëyma("NoClassDefFoundError: initialization failed"); return false; }
        if (maas_Tekki_baat_nekkin[maas_Tekki_baat] == 1 && maas_buumug_jokkale[maas_Tekki_baat] != 현재가닥) { 틀위치[kadar_àlluwa_tur] = ndigel_Door; 바꿈요청 = true; return false; }
        if (maas_Tekki_baat_nekkin[maas_Tekki_baat] != 0) return true;
        int 위 = 부모종(maas_Tekki_baat);
        if (위 >= 0 && !doortal(위, ndigel_Door)) return false;
        maas_Tekki_baat_nekkin[maas_Tekki_baat] = 1; maas_buumug_jokkale[maas_Tekki_baat] = 현재가닥;
        if (doortal_maas_Tekki_baat[maas_Tekki_baat] != 0) {
            틀위치[kadar_àlluwa_tur] = ndigel_Door;
            호출(doortal_maas_Tekki_baat[maas_Tekki_baat] - 1); if (!njumte) doortal_kadar[kadar_àlluwa_tur] = maas_Tekki_baat + 1;
            return false;
        }
        maas_Tekki_baat_nekkin[maas_Tekki_baat] = 2; return true;
    }
    static void 필드호출(int àlluwa_tur, int ndigel, int daw) {
        if (!sek_Lees_dul_soppi(àlluwa_tur, 9)) return;
        int boroom_xëyma = maas_tur_SMS(상가[àlluwa_tur]), tur_253d1510 = Royukaay_tur(상나[àlluwa_tur]), dayo_xëyma = Royukaay_xeet(상나[àlluwa_tur]);
        if (Word_SMS(boroom_xëyma, "java/lang/System") && (Word_SMS(tur_253d1510, "out") || Word_SMS(tur_253d1510, "err")) && Word_SMS(dayo_xëyma, "Ljava/io/PrintStream;") && ndigel == 178) { 넣기(-1, 2); return; }
        int maas_Tekki_baat = seet_maas_Tekki_baat(boroom_xëyma); if (maas_Tekki_baat < 0 || njumte) return;
        int 찾음 = -1;
        for (int 읽는자리 = maas_Tekki_baat, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int bara_denc_àlluwa_tur = 0; bara_denc_àlluwa_tur < 칸수; bara_denc_àlluwa_tur++) if (xar_xar_boroom[bara_denc_àlluwa_tur] == 읽는자리 && 같은말(xar_xar_tur[bara_denc_àlluwa_tur], tur_253d1510) && 같은말(xar_xar_xeet[bara_denc_àlluwa_tur], dayo_xëyma)) 찾음 = bara_denc_àlluwa_tur;
        if (찾음 < 0) { foo_xëyma("NoSuchFieldError"); return; }
        boolean Soppeekoodi_xëyma = ndigel == 178 || ndigel == 179;
        if (Soppeekoodi_xëyma != ((xar_xar_sañ_sañ[찾음] & 8) != 0)) { foo_xëyma("field static/instance mismatch"); return; }
        if (Soppeekoodi_xëyma && !doortal(xar_xar_boroom[찾음], daw)) return;
        int xeet_xëyma = 형종류(dayo_xëyma), xëyma = 0;
        if (ndigel == 179 || ndigel == 181) xëyma = 빼기(xeet_xëyma);
        if (Soppeekoodi_xëyma) { if (ndigel == 178) 넣기(xar_xar_mbir[찾음], xeet_xëyma); else if (!njumte) xar_xar_mbir[찾음] = xëyma; return; }
        int yëf_Royukaay = 빼기(2);
        if (!객체유효(yëf_Royukaay)) return;
        if (힙[yëf_Royukaay] < 32 || !종포함(힙[yëf_Royukaay] - 32, boroom_xëyma)) { foo_xëyma("field receiver type mismatch"); return; }
        int 보관칸 = yëf_Royukaay + 2 + 칸위치[찾음];
        if (ndigel == 180) 넣기(힙[보관칸], xeet_xëyma);
        else if (!njumte) { 힙[보관칸] = xëyma; 힙참조[보관칸] = xeet_xëyma == 2 ? 1 : 0; }
    }
    static boolean 종포함(int maas_Tekki_baat, int tur_253d1510) {
        for (int 중첩깊이 = 0; maas_Tekki_baat >= 0 && 중첩깊이 < 16; 중첩깊이++, maas_Tekki_baat = 부모종(maas_Tekki_baat)) {
            if (같은말(maas_Tekki_baat_tur[maas_Tekki_baat], tur_253d1510) || (종부모[maas_Tekki_baat] != 0 && 같은말(종부모[maas_Tekki_baat], tur_253d1510))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[maas_Tekki_baat]; 안쪽자리++) if (같은말(maas_jaarukaay[maas_Tekki_baat * 16 + 안쪽자리], tur_253d1510)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int okte_mbir, boolean Yoonu_jëmale) {
        if (첫값 == okte_mbir) return true;
        if (첫값 <= 0 || okte_mbir <= 0 || 힙[첫값] != 1 || 힙[okte_mbir] != 1 || 힙[첫값 + 1] != 힙[okte_mbir + 1]) return false;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 힙[첫값 + 1]; wërngël_àlluwa_tur++) {
            int rëddu_iks_yi = 힙[첫값 + 2 + wërngël_àlluwa_tur], 세로좌표 = 힙[okte_mbir + 2 + wërngël_àlluwa_tur];
            if (Yoonu_jëmale) { if (rëddu_iks_yi == '.') rëddu_iks_yi = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (rëddu_iks_yi != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int yëf_Royukaay) {
        if (yëf_Royukaay == 0) { foo_xëyma("NullPointerException"); return false; }
        if (yëf_Royukaay < 1 || yëf_Royukaay >= 힙끝 || 힙폭[yëf_Royukaay] < 2 || 힙[yëf_Royukaay] == 0) { foo_xëyma("invalid object reference"); return false; }
        return true;
    }
    static void saama_xëyma(int yëf_Royukaay) {
        if (yëf_Royukaay > 0 && yëf_Royukaay < 힙끝 && 힙폭[yëf_Royukaay] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = yëf_Royukaay;
    }
    static void féeñal_xëyma(int yëf_Royukaay) {
        if (yëf_Royukaay > 0 && yëf_Royukaay < 힙끝 && 힙폭[yëf_Royukaay] >= 2 && 힙[yëf_Royukaay] != 0 && 힙표시[yëf_Royukaay] == 0) {
            힙표시[yëf_Royukaay] = 1; 표시대기[표시수++] = yëf_Royukaay;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < araf_yu_bennoo_Royukaay.length; wërngël_àlluwa_tur++) féeñal_xëyma(araf_yu_bennoo_Royukaay[wërngël_àlluwa_tur]);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 칸수; wërngël_àlluwa_tur++) if ((xar_xar_sañ_sañ[wërngël_àlluwa_tur] & 8) != 0 && 형종류(xar_xar_xeet[wërngël_àlluwa_tur]) == 2) féeñal_xëyma(xar_xar_mbir[wërngël_àlluwa_tur]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            féeñal_xëyma(buumug_jokkale_yëf[임시값]); féeñal_xëyma(buumug_jokkale_luñu_name[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? kadar_àlluwa_tur : buumug_jokkale_kadar[임시값];
            for (int bara_denc_àlluwa_tur = 임시값 * 32; bara_denc_àlluwa_tur <= 꼭대기자리; bara_denc_àlluwa_tur++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[kadar_doxalin[bara_denc_àlluwa_tur]]; 안쪽자리++) if (dënnd_xeet[bara_denc_àlluwa_tur * 128 + 안쪽자리] == 2) féeñal_xëyma(dënnd_xëyma[bara_denc_àlluwa_tur * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < kadar_Tegalo[bara_denc_àlluwa_tur]; 안쪽자리++) if (스택형[bara_denc_àlluwa_tur * 128 + 안쪽자리] == 2) féeñal_xëyma(스택값[bara_denc_àlluwa_tur * 128 + 안쪽자리]);
            }
        }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 화면참조.length; wërngël_àlluwa_tur++) féeñal_xëyma(화면참조[wërngël_àlluwa_tur]);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 나중수; wërngël_àlluwa_tur++) féeñal_xëyma(나중실행[wërngël_àlluwa_tur]);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < Store_lëmm.length; wërngël_àlluwa_tur++) féeñal_xëyma(Store_lëmm[wërngël_àlluwa_tur]);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 종수; wërngël_àlluwa_tur++) féeñal_xëyma(종잠금[wërngël_àlluwa_tur]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) féeñal_xëyma(검사자리);
        féeñal_xëyma(던진객체);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 잠시수; wërngël_àlluwa_tur++) féeñal_xëyma(잠시참조[wërngël_àlluwa_tur]);
        while (표시수 > 0) {
            int yëf_Royukaay = 표시대기[--표시수], 분류코드 = 힙[yëf_Royukaay];
            for (int wërngël_àlluwa_tur = yëf_Royukaay + 2; wërngël_àlluwa_tur < yëf_Royukaay + 힙폭[yëf_Royukaay]; wërngël_àlluwa_tur++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[wërngël_àlluwa_tur] != 0) féeñal_xëyma(힙[wërngël_àlluwa_tur]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int diir_xëyma) {
        if (diir_xëyma < 0) { foo_xëyma("NegativeArraySizeException"); return 0; }
        if (diir_xëyma > 힙.length - 3) { foo_xëyma("object heap exhausted"); return 0; }
        int 필요수 = diir_xëyma + 2, yëf_Royukaay = 0;
        if (필요수 <= 힙.length - 힙끝) { yëf_Royukaay = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { yëf_Royukaay = 읽는자리; break; }
            if (yëf_Royukaay != 0) {
                int 남은길이 = 힙폭[yëf_Royukaay] - 필요수;
                if (남은길이 >= 2) { 힙폭[yëf_Royukaay + 필요수] = 남은길이; 힙[yëf_Royukaay + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { yëf_Royukaay = 힙끝; 힙끝 += 필요수; }
        }
        if (yëf_Royukaay == 0) { foo_xëyma("object heap exhausted"); return 0; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 필요수; wërngël_àlluwa_tur++) { 힙[yëf_Royukaay + wërngël_àlluwa_tur] = 0; 힙참조[yëf_Royukaay + wërngël_àlluwa_tur] = 0; 힙폭[yëf_Royukaay + wërngël_àlluwa_tur] = 0; }
        TABLO_cër[yëf_Royukaay] = 0;
        힙폭[yëf_Royukaay] = 필요수; 힙[yëf_Royukaay] = 종류; 힙[yëf_Royukaay + 1] = diir_xëyma; saama_xëyma(yëf_Royukaay); return yëf_Royukaay;
    }
    static int 예외종(String tur_Lees_dul_soppi) {
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/Throwable")) return 1;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/Exception")) return 2;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/io/IOException")) return 11;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(tur_Lees_dul_soppi, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int tur_253d1510) {
        for (int wërngël_àlluwa_tur = 1; wërngël_àlluwa_tur <= 41; wërngël_àlluwa_tur++) if (Word_SMS(tur_253d1510, 예외이름(wërngël_àlluwa_tur))) return wërngël_àlluwa_tur;
        return 0;
    }
    static String 예외이름(int sàq_xëyma) {
        if (sàq_xëyma == 40) return "java/lang/InterruptedException";
        if (sàq_xëyma == 41) return "한국어/자체/대기중단예외";
        if (sàq_xëyma == 39) return "java/net/SocketException";
        if (sàq_xëyma == 20) return "한국어/자체/예외";
        if (sàq_xëyma == 21) return "한국어/자체/실행예외";
        if (sàq_xëyma == 22) return "한국어/자체/입출력예외";
        if (sàq_xëyma == 23) return "한국어/자체/대기시간초과예외";
        if (sàq_xëyma == 24) return "한국어/자체/주소확인예외";
        if (sàq_xëyma == 25) return "한국어/자체/파일없음예외";
        if (sàq_xëyma == 26) return "한국어/자체/통신예외";
        if (sàq_xëyma == 27) return "한국어/자체/잘못된인수예외";
        if (sàq_xëyma == 28) return "한국어/자체/숫자형식예외";
        if (sàq_xëyma == 29) return "한국어/자체/범위예외";
        if (sàq_xëyma == 30) return "한국어/자체/배열범위예외";
        if (sàq_xëyma == 31) return "한국어/자체/문자열범위예외";
        if (sàq_xëyma == 32) return "한국어/자체/빈참조예외";
        if (sàq_xëyma == 33) return "한국어/자체/산술예외";
        if (sàq_xëyma == 34) return "한국어/자체/상태예외";
        if (sàq_xëyma == 35) return "한국어/자체/형변환예외";
        if (sàq_xëyma == 36) return "한국어/자체/음수배열크기예외";
        if (sàq_xëyma == 37) return "한국어/자체/TABLO_Store_foo";
        if (sàq_xëyma == 38) return "한국어/자체/가닥상태예외";
        if (sàq_xëyma == 1) return "java/lang/Throwable"; if (sàq_xëyma == 2) return "java/lang/Exception";
        if (sàq_xëyma == 3) return "java/lang/RuntimeException"; if (sàq_xëyma == 4) return "java/lang/ArithmeticException";
        if (sàq_xëyma == 5) return "java/lang/NullPointerException"; if (sàq_xëyma == 6) return "java/lang/IndexOutOfBoundsException";
        if (sàq_xëyma == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (sàq_xëyma == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (sàq_xëyma == 9) return "java/lang/IllegalArgumentException"; if (sàq_xëyma == 10) return "java/lang/NumberFormatException";
        if (sàq_xëyma == 11) return "java/io/IOException"; if (sàq_xëyma == 12) return "java/io/FileNotFoundException";
        if (sàq_xëyma == 17) return "java/lang/ArrayStoreException";
        if (sàq_xëyma == 18) return "java/net/UnknownHostException";
        if (sàq_xëyma == 19) return "java/net/SocketTimeoutException";
        if (sàq_xëyma == 16) return "java/lang/IllegalThreadStateException";
        if (sàq_xëyma == 13) return "java/lang/IllegalStateException"; if (sàq_xëyma == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int sàq_xëyma) {
        if (sàq_xëyma == 40) return 2;
        if (sàq_xëyma == 41) return 40;
        if (sàq_xëyma == 39) return 11;
        if (sàq_xëyma == 1) return 0;
        if (sàq_xëyma == 2) return 1;
        if (sàq_xëyma == 3) return 2;
        if (sàq_xëyma == 4) return 3;
        if (sàq_xëyma == 5) return 3;
        if (sàq_xëyma == 6) return 3;
        if (sàq_xëyma == 7) return 6;
        if (sàq_xëyma == 8) return 6;
        if (sàq_xëyma == 9) return 3;
        if (sàq_xëyma == 10) return 9;
        if (sàq_xëyma == 11) return 2;
        if (sàq_xëyma == 12) return 11;
        if (sàq_xëyma == 13) return 3;
        if (sàq_xëyma == 14) return 3;
        if (sàq_xëyma == 15) return 3;
        if (sàq_xëyma == 16) return 9;
        if (sàq_xëyma == 17) return 3;
        if (sàq_xëyma == 18) return 11;
        if (sàq_xëyma == 19) return 11;
        if (sàq_xëyma == 20) return 2;
        if (sàq_xëyma == 21) return 3;
        if (sàq_xëyma == 22) return 11;
        if (sàq_xëyma == 23) return 22;
        if (sàq_xëyma == 24) return 22;
        if (sàq_xëyma == 25) return 22;
        if (sàq_xëyma == 26) return 22;
        if (sàq_xëyma == 27) return 9;
        if (sàq_xëyma == 28) return 27;
        if (sàq_xëyma == 29) return 6;
        if (sàq_xëyma == 30) return 29;
        if (sàq_xëyma == 31) return 29;
        if (sàq_xëyma == 32) return 5;
        if (sàq_xëyma == 33) return 4;
        if (sàq_xëyma == 34) return 13;
        if (sàq_xëyma == 35) return 14;
        if (sàq_xëyma == 36) return 15;
        if (sàq_xëyma == 37) return 17;
        if (sàq_xëyma == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int liteew_xëyma, int 요구값) {
        for (int 깊이 = 0; liteew_xëyma != 0 && 깊이 < 16; 깊이++, liteew_xëyma = 예외부모(liteew_xëyma))
            if (liteew_xëyma == 요구값) return true;
        return false;
    }
    static void 예외던짐(int sàq_xëyma, String JANG_MA_Royukaay) {
        int yëf_Royukaay = 새기억(9, 2); if (njumte) return;
        힙[yëf_Royukaay + 2] = sàq_xëyma; 힙[yëf_Royukaay + 3] = dalal_Araf(JANG_MA_Royukaay); 힙참조[yëf_Royukaay + 3] = 1;
        던진객체 = yëf_Royukaay; njumte = true;
    }
    static boolean 맞는객체(int yëf_Royukaay, int tur_253d1510) {
        if (yëf_Royukaay == 0) return true;
        if (!객체유효(yëf_Royukaay)) return false;
        int 분류코드 = 힙[yëf_Royukaay];
        if (Word_SMS(tur_253d1510, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, tur_253d1510);
        if (분류코드 == 9) { int luñu_name_dëkkuwaay = 예외상수(tur_253d1510); return luñu_name_dëkkuwaay != 0 && 예외포함(힙[yëf_Royukaay + 2], luñu_name_dëkkuwaay); }
        if (분류코드 == 1) return Word_SMS(tur_253d1510, "java/lang/String") || Word_SMS(tur_253d1510, "java/lang/CharSequence");
        if (분류코드 == 4) return Word_SMS(tur_253d1510, "java/lang/StringBuilder") || Word_SMS(tur_253d1510, "java/lang/CharSequence");
        if (분류코드 == 10) return Word_SMS(tur_253d1510, "java/util/ArrayList") || Word_SMS(tur_253d1510, "java/util/List");
        if (분류코드 == 11) return Word_SMS(tur_253d1510, "java/util/HashMap") || Word_SMS(tur_253d1510, "java/util/Map");
        if (분류코드 == 12) return Word_SMS(tur_253d1510, "java/lang/Integer") || Word_SMS(tur_253d1510, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[yëf_Royukaay + 13] != 0) return 한국어화면종(tur_253d1510) == 분류코드 || Word_SMS(tur_253d1510, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(tur_253d1510) == 0 && 화면종(tur_253d1510) == 분류코드) || Word_SMS(tur_253d1510, "java/awt/Component") || Word_SMS(tur_253d1510, "java/awt/Container") || Word_SMS(tur_253d1510, "javax/swing/JComponent");
        if (분류코드 == 29) return Word_SMS(tur_253d1510, 힙[yëf_Royukaay + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Word_SMS(tur_253d1510, "java/awt/FlowLayout") || Word_SMS(tur_253d1510, "java/awt/LayoutManager");
        if (분류코드 == 17) return Word_SMS(tur_253d1510, "java/net/Socket");
        if (분류코드 == 18) return Word_SMS(tur_253d1510, "java/net/ServerSocket");
        if (분류코드 == 19) return Word_SMS(tur_253d1510, 힙[yëf_Royukaay + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Word_SMS(tur_253d1510, "java/net/InetAddress");
        if (분류코드 == 15) return Word_SMS(tur_253d1510, "java/net/DatagramSocket");
        if (분류코드 == 16) return Word_SMS(tur_253d1510, "java/net/DatagramPacket");
        if (분류코드 == 13) return Word_SMS(tur_253d1510, 힙[yëf_Royukaay + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Word_SMS(tur_253d1510, "[I"); if (분류코드 == 20) return Word_SMS(tur_253d1510, "[B"); if (분류코드 == 21) return Word_SMS(tur_253d1510, "[Z");
        if (분류코드 == 22) return Word_SMS(tur_253d1510, "[C"); if (분류코드 == 23) return Word_SMS(tur_253d1510, "[S");
        if (분류코드 != 3) return false;
        if (Word_SMS(tur_253d1510, "[Ljava/lang/Object;")) return true;
        int bu_ci_bokk = TABLO_cër[yëf_Royukaay];
        if (bu_ci_bokk == -1) return Word_SMS(tur_253d1510, "[Ljava/lang/String;") || Word_SMS(tur_253d1510, "[Ljava/lang/CharSequence;");
        if (bu_ci_bokk == 0) return false;
        if (배열종비교(bu_ci_bokk, tur_253d1510)) return true;
        if ((Word_SMS(bu_ci_bokk, "java/lang/String") || Word_SMS(bu_ci_bokk, "java/lang/StringBuilder")) && Word_SMS(tur_253d1510, "[Ljava/lang/CharSequence;")) return true;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 종수; wërngël_àlluwa_tur++) if (같은말(maas_Tekki_baat_tur[wërngël_àlluwa_tur], bu_ci_bokk)) {
            for (int kotu_araf = wërngël_àlluwa_tur, 중첩깊이 = 0; kotu_araf >= 0 && 중첩깊이 < 16; 중첩깊이++, kotu_araf = 부모종(kotu_araf)) {
                if (배열종비교(종부모[kotu_araf], tur_253d1510)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[kotu_araf]; 안쪽자리++) if (배열종비교(maas_jaarukaay[kotu_araf * 16 + 안쪽자리], tur_253d1510)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int tur_Lees_dul_soppi, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (tur_Lees_dul_soppi == 0 || 항목수 < 4 || bara_denc[검사자리] != '[' || bara_denc[검사자리 + 1] != 'L' || bara_denc[검사자리 + 항목수 - 1] != ';' || 상나[tur_Lees_dul_soppi] != 항목수 - 3) return false;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수 - 3; wërngël_àlluwa_tur++) if (bara_denc[상가[tur_Lees_dul_soppi] + wërngël_àlluwa_tur] != bara_denc[검사자리 + 2 + wërngël_àlluwa_tur]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        njumte = false;
        while (kadar_àlluwa_tur >= 현재가닥 * 32) {
            int bara_denc_àlluwa_tur = kadar_doxalin[kadar_àlluwa_tur], 읽는자리 = kadar_ndigal[kadar_àlluwa_tur];
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 잡기수; wërngël_àlluwa_tur++) if (잡기함수[wërngël_àlluwa_tur] == bara_denc_àlluwa_tur && 읽는자리 >= 잡기시작[wërngël_àlluwa_tur] && 읽는자리 < 잡기끝[wërngël_àlluwa_tur]
                && (잡기종[wërngël_àlluwa_tur] == 0 || 맞는객체(던진객체, 잡기종[wërngël_àlluwa_tur]))) {
                틀위치[kadar_àlluwa_tur] = 잡기위치[wërngël_àlluwa_tur]; kadar_Tegalo[kadar_àlluwa_tur] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (doortal_kadar[kadar_àlluwa_tur] != 0) maas_Tekki_baat_nekkin[doortal_kadar[kadar_àlluwa_tur] - 1] = 3;
            if (틀잠금[kadar_àlluwa_tur] != 0) { 잠금풀기(틀잠금[kadar_àlluwa_tur]); 틀잠금[kadar_àlluwa_tur] = 0; }
            kadar_àlluwa_tur--;
        }
        kiy_jariñoo_internet.biir("Uncaught ");
        if (힙[던진객체] == 9) { kiy_jariñoo_internet.biir(예외이름(힙[던진객체 + 2])); kiy_jariñoo_internet.biir(": "); biir_SMS(힙[던진객체 + 3]); }
        else kiy_jariñoo_internet.biir("user exception");
        kiy_jariñoo_internet.biir_Araf_xëyma(10); 던진객체 = 0; njumte = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Tegalo_ndigal(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int okte_mbir = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식); 넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(okte_mbir, 둘째형식); return; }
        int kotu_araf = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(kotu_araf, 셋째형식); 넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식); 넣기(kotu_araf, 셋째형식); 넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kotu_araf, 셋째형식); 넣기(okte_mbir, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int tur_Lees_dul_soppi, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(tur_Lees_dul_soppi);
        if (Word_SMS(tur_Lees_dul_soppi, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/lang/Thread") || Word_SMS(tur_Lees_dul_soppi, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Word_SMS(tur_Lees_dul_soppi, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(tur_Lees_dul_soppi) != 0) { 분류코드 = 화면종(tur_Lees_dul_soppi); 유효길이 = 12; }
        if (분류코드 == 0) {
            int kotu_araf = seet_maas_Tekki_baat(tur_Lees_dul_soppi); if (kotu_araf < 0 || njumte || !doortal(kotu_araf, 시작점)) return;
            분류코드 = 32 + kotu_araf; 유효길이 = 종칸수[kotu_araf];
        }
        int yëf_Royukaay = jagleel_Dencukaay(분류코드, 유효길이); if (njumte) return;
        if (분류코드 == 13 && Word_SMS(tur_Lees_dul_soppi, "한국어/자체/작업가닥")) 힙[yëf_Royukaay + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(tur_Lees_dul_soppi) != 0) 힙[yëf_Royukaay + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[yëf_Royukaay + 2] = -1;
        if (분류코드 == 9) 힙[yëf_Royukaay + 2] = 예외참조;
        넣기(yëf_Royukaay, 2);
    }
    static boolean 값같음(int 첫값, int okte_mbir) {
        if (첫값 == okte_mbir) return true;
        if (첫값 == 0 || okte_mbir == 0 || 첫값 < 0 || okte_mbir < 0 || 첫값 >= 힙끝 || okte_mbir >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[okte_mbir] == 1) return 글같음(첫값, okte_mbir, false);
        return 힙[첫값] == 12 && 힙[okte_mbir] == 12 && 힙[첫값 + 2] == 힙[okte_mbir + 2];
    }
    static int 글조각(int yëf_Royukaay, int 시작자리, int 끝자리) {
        if (!yëf_xëyma(yëf_Royukaay, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[yëf_Royukaay + 1]) { foo_xëyma("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = jagleel_Dencukaay(1, 끝자리 - 시작자리); if (njumte) return 0;
        for (int wërngël_àlluwa_tur = 시작자리; wërngël_àlluwa_tur < 끝자리; wërngël_àlluwa_tur++) 힙[반환값 + 2 + wërngël_àlluwa_tur - 시작자리] = 힙[yëf_Royukaay + 2 + wërngël_àlluwa_tur];
        return 반환값;
    }
    static int bokk_SMS(int 첫값, int okte_mbir) {
        if (!yëf_xëyma(첫값, 1) || !yëf_xëyma(okte_mbir, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], doxalin_àlluwa_tur = 힙[okte_mbir + 1], 반환값 = jagleel_Dencukaay(1, 항목수 + doxalin_àlluwa_tur); if (njumte) return 0;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 힙[반환값 + 2 + wërngël_àlluwa_tur] = 힙[첫값 + 2 + wërngël_àlluwa_tur];
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < doxalin_àlluwa_tur; wërngël_àlluwa_tur++) 힙[반환값 + 2 + 항목수 + wërngël_àlluwa_tur] = 힙[okte_mbir + 2 + wërngël_àlluwa_tur];
        return 반환값;
    }
    static boolean 기본호출(int boroom, int tur_Lees_dul_soppi, int 서술상수, int 명령코드) {
        if (Word_SMS(boroom, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (Word_SMS(tur_Lees_dul_soppi, "개수") && Word_SMS(서술상수, "()I")) { 넣기(kiy_jariñoo_internet.인수개수() - 1, 1); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "Tekst") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= kiy_jariñoo_internet.인수개수() - 1) 예외던짐(29, "def_ndigel 인수 범위를 벗어났습니다");
                else 넣기(dalal_Araf(kiy_jariñoo_internet.인수(순번 + 1)), 2);
                return true;
            }
            foo_xëyma("지원하지 않는 한국어 def_ndigel 인수 호출"); return true;
        }
        if (Word_SMS(boroom, "한국어/자체/작업가닥")) { yokkute_buumug_jokkale(tur_Lees_dul_soppi, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(boroom)) { 한국어화면호출(boroom, tur_Lees_dul_soppi, 서술상수, 명령코드); return true; }
        if (화면소유(boroom)) { 화면호출(boroom, tur_Lees_dul_soppi, 서술상수, 명령코드); return true; }
        if (Word_SMS(boroom, "java/net/Socket") || Word_SMS(boroom, "java/net/ServerSocket") || Word_SMS(boroom, "java/io/InputStream") || Word_SMS(boroom, "java/io/OutputStream")) { 흐름호출(boroom, tur_Lees_dul_soppi, 서술상수, 명령코드); return true; }
        if (Word_SMS(boroom, "한국어/자체/xoox_xëyma") && 명령코드 == 184) {
            if (Word_SMS(tur_Lees_dul_soppi, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(kiy_jariñoo_internet.화면너비(), 1); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(kiy_jariñoo_internet.화면높이(), 1); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(kiy_jariñoo_internet.밀리초(), 1); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(kiy_jariñoo_internet.그림대기(), 1); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), rëddu_iks_yi = 빼기(1); 넣기(kiy_jariñoo_internet.사각형(rëddu_iks_yi, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(boroom, "java/net/InetAddress") || Word_SMS(boroom, "java/net/DatagramPacket") || Word_SMS(boroom, "java/net/DatagramSocket")) { 통신호출(boroom, tur_Lees_dul_soppi, 서술상수, 명령코드); return true; }
        if (Word_SMS(boroom, "java/lang/Thread")) { 가닥호출(tur_Lees_dul_soppi, 서술상수, 명령코드); return true; }
        if (Word_SMS(boroom, "java/lang/Object")) {
            if (Word_SMS(tur_Lees_dul_soppi, "<init>") && Word_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int okte_mbir = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == okte_mbir ? 1 : 0, 1); return true; }
        }
        if (예외상수(boroom) != 0) {
            if (Word_SMS(tur_Lees_dul_soppi, "<init>") && 명령코드 == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int xaar_jëf = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), yëf_Royukaay = 빼기(2);
                if (yëf_xëyma(yëf_Royukaay, 9)) { 힙[yëf_Royukaay + 3] = xaar_jëf; 힙참조[yëf_Royukaay + 3] = 1; } return true;
            }
            if ((Word_SMS(tur_Lees_dul_soppi, "getMessage") || Word_SMS(tur_Lees_dul_soppi, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 9)) 넣기(힙[yëf_Royukaay + 3], 2); return true; }
        }
        if (Word_SMS(boroom, "java/lang/String")) {
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int nëbbin_ci_lim_tur = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), yëf_Royukaay = 빼기(2);
                if (!yëf_xëyma(yëf_Royukaay, 1)) return true;
                if (nëbbin_ci_lim_tur != 0 && !글같음(nëbbin_ci_lim_tur, dalal_Araf("UTF-8"), false) && !글같음(nëbbin_ci_lim_tur, dalal_Araf("UTF8"), false) && !글같음(nëbbin_ci_lim_tur, dalal_Araf("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[yëf_Royukaay + 1], 반환값 = jagleel_Dencukaay(20, 항목수 * 3), 사용수 = 0; if (njumte) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int kotu_araf = 힙[yëf_Royukaay + 2 + 안쪽자리];
                    if (kotu_araf >= 0xd800 && kotu_araf <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[yëf_Royukaay + 3 + 안쪽자리] >= 0xdc00 && 힙[yëf_Royukaay + 3 + 안쪽자리] <= 0xdfff) kotu_araf = 0x10000 + ((kotu_araf - 0xd800) << 10) + 힙[yëf_Royukaay + 2 + ++안쪽자리] - 0xdc00;
                    else if (kotu_araf >= 0xd800 && kotu_araf <= 0xdfff) kotu_araf = '?';
                    if (kotu_araf < 128) 힙[반환값 + 2 + 사용수++] = kotu_araf;
                    else { int 바이트수 = kotu_araf < 2048 ? 2 : kotu_araf < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | kotu_araf >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kotu_araf >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siifar_Araf(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Word_SMS(tur_Lees_dul_soppi, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int okte_mbir = 빼기(2), 첫값 = 빼기(2); if (yëf_xëyma(첫값, 1)) 넣기(글같음(첫값, okte_mbir, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (yëf_xëyma(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (yëf_xëyma(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(tur_Lees_dul_soppi, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int okte_mbir = 빼기(2), 첫값 = 빼기(2); 넣기(bokk_SMS(첫값, okte_mbir), 2); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), caabiy_teqale_bi_xëyma = 0; if (yëf_xëyma(첫값, 1)) { for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 힙[첫값 + 1]; wërngël_àlluwa_tur++) caabiy_teqale_bi_xëyma = caabiy_teqale_bi_xëyma * 31 + 힙[첫값 + 2 + wërngël_àlluwa_tur]; 넣기(caabiy_teqale_bi_xëyma, 1); } return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (yëf_xëyma(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(boroom, "java/lang/Integer")) {
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int mbir_xëyma = 빼기(1), yëf_Royukaay = mbir_xëyma >= -128 && mbir_xëyma <= 127 ? Store_lëmm[mbir_xëyma + 128] : 0; if (yëf_Royukaay == 0) { yëf_Royukaay = jagleel_Dencukaay(12, 1); if (!njumte) { 힙[yëf_Royukaay + 2] = mbir_xëyma; if (mbir_xëyma >= -128 && mbir_xëyma <= 127) Store_lëmm[mbir_xëyma + 128] = yëf_Royukaay; } } 넣기(yëf_Royukaay, 2); return true; }
            if (명령코드 == 183 && Word_SMS(tur_Lees_dul_soppi, "<init>") && Word_SMS(서술상수, "(I)V")) { int mbir_xëyma = 빼기(1), yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 12)) 힙[yëf_Royukaay + 2] = mbir_xëyma; return true; }
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "intValue") && Word_SMS(서술상수, "()I")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 12)) 넣기(힙[yëf_Royukaay + 2], 1); return true; }
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siifar_Araf(빼기(1)), 2); return true; }
        }
        if (Word_SMS(boroom, "java/lang/Math") && 명령코드 == 184) {
            if (Word_SMS(tur_Lees_dul_soppi, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(tur_Lees_dul_soppi, "min") || Word_SMS(tur_Lees_dul_soppi, "max")) && Word_SMS(서술상수, "(II)I")) { int okte_mbir = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(tur_Lees_dul_soppi, "min") ? (첫값 < okte_mbir ? 첫값 : okte_mbir) : (첫값 > okte_mbir ? 첫값 : okte_mbir), 1); return true; }
        }
        if (Word_SMS(boroom, "java/lang/System") && 명령코드 == 184) {
            if (Word_SMS(tur_Lees_dul_soppi, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(tur_Lees_dul_soppi, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), jëmmukaay_xëyma_àlluwa_tur = 빼기(1), okte_mbir = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(okte_mbir)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[okte_mbir] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) foo_xëyma("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || jëmmukaay_xëyma_àlluwa_tur < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || jëmmukaay_xëyma_àlluwa_tur > 힙[okte_mbir + 1] - 항목수) foo_xëyma("ArrayIndexOutOfBoundsException");
                    else if (첫값 == okte_mbir && jëmmukaay_xëyma_àlluwa_tur > 시작자리) { for (int wërngël_àlluwa_tur = 항목수 - 1; wërngël_àlluwa_tur >= 0; wërngël_àlluwa_tur--) 힙[okte_mbir + 2 + jëmmukaay_xëyma_àlluwa_tur + wërngël_àlluwa_tur] = 힙[첫값 + 2 + 시작자리 + wërngël_àlluwa_tur]; }
                    else { for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수 && !njumte; wërngël_àlluwa_tur++) { int mbir_xëyma = 힙[첫값 + 2 + 시작자리 + wërngël_àlluwa_tur]; if (분류코드 != 3 || 배열저장가능(okte_mbir, mbir_xëyma)) 힙[okte_mbir + 2 + jëmmukaay_xëyma_àlluwa_tur + wërngël_àlluwa_tur] = mbir_xëyma; } }
                }
                return true;
            }
        }
        if (Word_SMS(boroom, "java/util/ArrayList") || Word_SMS(boroom, "java/util/List") || Word_SMS(boroom, "java/util/HashMap") || Word_SMS(boroom, "java/util/Map")) {
            모음호출(boroom, tur_Lees_dul_soppi, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int yëf_Royukaay, int 필요수) {
        int 이전값 = 힙[yëf_Royukaay + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int mbir_TABLO = jagleel_Dencukaay(3, 다음자리); if (njumte) return;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 용량값; wërngël_àlluwa_tur++) 힙[mbir_TABLO + 2 + wërngël_àlluwa_tur] = 힙[이전값 + 2 + wërngël_àlluwa_tur];
        힙[yëf_Royukaay + 2] = mbir_TABLO; 힙참조[yëf_Royukaay + 2] = 1;
    }
    static void 모음호출(int boroom, int tur_Lees_dul_soppi, int 서술상수, int 명령코드) {
        boolean 대응참조 = Word_SMS(boroom, "java/util/HashMap") || Word_SMS(boroom, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Word_SMS(tur_Lees_dul_soppi, "<init>") && 명령코드 == 183 && Word_SMS(서술상수, "()V")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 분류코드)) 모음늘리기(yëf_Royukaay, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { foo_xëyma("invalid collection invocation"); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "size") && Word_SMS(서술상수, "()I") || Word_SMS(tur_Lees_dul_soppi, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 분류코드)) 넣기(Word_SMS(tur_Lees_dul_soppi, "size") ? 힙[yëf_Royukaay + 3] : 힙[yëf_Royukaay + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "clear") && Word_SMS(서술상수, "()V")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 분류코드)) { int mbir_TABLO = 힙[yëf_Royukaay + 2]; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 힙[mbir_TABLO + 1]; wërngël_àlluwa_tur++) 힙[mbir_TABLO + 2 + wërngël_àlluwa_tur] = 0; 힙[yëf_Royukaay + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(tur_Lees_dul_soppi, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int mbir_xëyma = 빼기(2), yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 10)) return;
            int 항목수 = 힙[yëf_Royukaay + 3]; 모음늘리기(yëf_Royukaay, 항목수 + 1); if (!njumte) { 힙[힙[yëf_Royukaay + 2] + 2 + 항목수] = mbir_xëyma; 힙[yëf_Royukaay + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(tur_Lees_dul_soppi, "get") || Word_SMS(tur_Lees_dul_soppi, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(tur_Lees_dul_soppi, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(tur_Lees_dul_soppi, "set"); int mbir_xëyma = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), yëf_Royukaay = 빼기(2);
            if (!yëf_xëyma(yëf_Royukaay, 10)) return;
            int 항목수 = 힙[yëf_Royukaay + 3], mbir_TABLO = 힙[yëf_Royukaay + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[mbir_TABLO + 2 + 항목자리];
            if (지정여부) 힙[mbir_TABLO + 2 + 항목자리] = mbir_xëyma;
            if (Word_SMS(tur_Lees_dul_soppi, "remove")) { for (int wërngël_àlluwa_tur = 항목자리 + 1; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 힙[mbir_TABLO + 1 + wërngël_àlluwa_tur] = 힙[mbir_TABLO + 2 + wërngël_àlluwa_tur]; 힙[mbir_TABLO + 1 + 항목수] = 0; 힙[yëf_Royukaay + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(tur_Lees_dul_soppi, "get") || Word_SMS(tur_Lees_dul_soppi, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(tur_Lees_dul_soppi, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(tur_Lees_dul_soppi, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(tur_Lees_dul_soppi, "put"), dandal = Word_SMS(tur_Lees_dul_soppi, "remove");
            int mbir_xëyma = 넣기여부 ? 빼기(2) : 0, kër_Royukaay = 빼기(2), yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 11)) return;
            int 항목수 = 힙[yëf_Royukaay + 3], mbir_TABLO = 힙[yëf_Royukaay + 2], 찾은여부 = -1;
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) if (값같음(kër_Royukaay, 힙[mbir_TABLO + 2 + 2 * wërngël_àlluwa_tur])) { 찾은여부 = wërngël_àlluwa_tur; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[mbir_TABLO + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(yëf_Royukaay, (항목수 + 1) * 2); mbir_TABLO = 힙[yëf_Royukaay + 2]; 찾은여부 = 항목수; if (!njumte) 힙[yëf_Royukaay + 3] = 항목수 + 1; }
                if (!njumte) { 힙[mbir_TABLO + 2 + 2 * 찾은여부] = kër_Royukaay; 힙[mbir_TABLO + 3 + 2 * 찾은여부] = mbir_xëyma; }
            }
            if (dandal && 찾은여부 >= 0) { for (int wërngël_àlluwa_tur = 찾은여부 + 1; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) { 힙[mbir_TABLO + 2 * wërngël_àlluwa_tur] = 힙[mbir_TABLO + 2 + 2 * wërngël_àlluwa_tur]; 힙[mbir_TABLO + 1 + 2 * wërngël_àlluwa_tur] = 힙[mbir_TABLO + 3 + 2 * wërngël_àlluwa_tur]; } 힙[mbir_TABLO + 2 * 항목수] = 0; 힙[mbir_TABLO + 1 + 2 * 항목수] = 0; 힙[yëf_Royukaay + 3] = 항목수 - 1; }
            if (Word_SMS(tur_Lees_dul_soppi, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        foo_xëyma("unsupported collection method");
    }
    static boolean 잠금얻기(int yëf_Royukaay) {
        if (!객체유효(yëf_Royukaay)) return false;
        if (잠금깊이[yëf_Royukaay] != 0 && 잠금주인[yëf_Royukaay] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[yëf_Royukaay] = 현재가닥 + 1; 잠금깊이[yëf_Royukaay]++; return true;
    }
    static void 잠금풀기(int yëf_Royukaay) {
        if (!객체유효(yëf_Royukaay)) return;
        if (잠금깊이[yëf_Royukaay] == 0 || 잠금주인[yëf_Royukaay] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[yëf_Royukaay] == 0) 잠금주인[yëf_Royukaay] = 0;
    }
    static boolean jalantu_buumug_jokkale() {
        buumug_jokkale_kadar[현재가닥] = kadar_àlluwa_tur;
        if (kadar_àlluwa_tur < 현재가닥 * 32) buumug_jokkale_nekkin[현재가닥] = 3;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 가닥수; wërngël_àlluwa_tur++) if (buumug_jokkale_nekkin[wërngël_àlluwa_tur] == 2 && buumug_jokkale_nekkin[가닥대기[wërngël_àlluwa_tur]] == 3) buumug_jokkale_nekkin[wërngël_àlluwa_tur] = 1;
        for (int wërngël_àlluwa_tur = 1; wërngël_àlluwa_tur <= 가닥수; wërngël_àlluwa_tur++) {
            int 다음자리 = (현재가닥 + wërngël_àlluwa_tur) % 가닥수;
            if (buumug_jokkale_nekkin[다음자리] == 1) { 현재가닥 = 다음자리; kadar_àlluwa_tur = buumug_jokkale_kadar[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 가닥수; wërngël_àlluwa_tur++) if (buumug_jokkale_nekkin[wërngël_àlluwa_tur] != 3) { foo_xëyma("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int tur_Lees_dul_soppi, int 서술상수, int 명령코드) { yokkute_buumug_jokkale(tur_Lees_dul_soppi, 서술상수, 명령코드, false); }
    static void yokkute_buumug_jokkale(int tur_Lees_dul_soppi, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, 한국어 ? "dakkal_ligeey" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(buumug_jokkale_yëf[현재가닥], 2); return; }
        if (명령코드 == 183 && Word_SMS(tur_Lees_dul_soppi, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int luñu_name_dëkkuwaay = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), yëf_Royukaay = 빼기(2);
            if (!객체유효(yëf_Royukaay)) return;
            if (힙[yëf_Royukaay] == 13) { 힙[yëf_Royukaay + 2] = luñu_name_dëkkuwaay; 힙참조[yëf_Royukaay + 2] = 1; }
            else if (luñu_name_dëkkuwaay != 0) foo_xëyma("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Word_SMS(tur_Lees_dul_soppi, 한국어 ? "Door_ligeey" : "start") || Word_SMS(tur_Lees_dul_soppi, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || 명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int yëf_Royukaay = 빼기(2); if (!객체유효(yëf_Royukaay)) return;
            int sàq_xëyma = -1; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 가닥수; wërngël_àlluwa_tur++) if (buumug_jokkale_yëf[wërngël_àlluwa_tur] == yëf_Royukaay) sàq_xëyma = wërngël_àlluwa_tur;
            if (Word_SMS(tur_Lees_dul_soppi, 한국어 ? "살아있는가" : "isAlive")) { 넣기(sàq_xëyma >= 0 && buumug_jokkale_nekkin[sàq_xëyma] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(tur_Lees_dul_soppi, 한국어 ? "기다리기" : "join")) { if (sàq_xëyma >= 0 && buumug_jokkale_nekkin[sàq_xëyma] != 3) { 가닥대기[현재가닥] = sàq_xëyma; buumug_jokkale_nekkin[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (sàq_xëyma >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { foo_xëyma("thread limit (4 including main)"); return; }
            int luñu_name_dëkkuwaay = 힙[yëf_Royukaay] == 13 ? 힙[yëf_Royukaay + 2] : yëf_Royukaay;
            int bara_denc_àlluwa_tur = luñu_name_dëkkuwaay > 0 && 힙[luñu_name_dëkkuwaay] >= 32 ? tur_doxalin(힙[luñu_name_dëkkuwaay] - 32, 한국어 ? "def_ligeey" : "run", "()V") : -1;
            if (luñu_name_dëkkuwaay != 0 && bara_denc_àlluwa_tur < 0) { foo_xëyma("Runnable.run required"); return; }
            sàq_xëyma = 가닥수++; buumug_jokkale_yëf[sàq_xëyma] = yëf_Royukaay; buumug_jokkale_luñu_name[sàq_xëyma] = luñu_name_dëkkuwaay;
            int kadar = sàq_xëyma * 32; buumug_jokkale_kadar[sàq_xëyma] = bara_denc_àlluwa_tur < 0 ? kadar - 1 : kadar; buumug_jokkale_nekkin[sàq_xëyma] = bara_denc_àlluwa_tur < 0 ? 3 : 1;
            if (bara_denc_àlluwa_tur >= 0) { kadar_doxalin[kadar] = bara_denc_àlluwa_tur; 틀위치[kadar] = doxalin_Door[bara_denc_àlluwa_tur]; dënnd_xëyma[kadar * 128] = luñu_name_dëkkuwaay; dënnd_xeet[kadar * 128] = 2; }
            return;
        }
        foo_xëyma("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], dëkkuwaay_SMS = new int[16];
    static int dënnd_dëkkuwaay() { return dëkkuwaay_yëf(0x7f000001); }
    static int dëkkuwaay_yëf(int xëyma) { int yëf_Royukaay = jagleel_Dencukaay(14, 1); if (!njumte) 힙[yëf_Royukaay + 2] = xëyma; return yëf_Royukaay; }
    static int 주소해독(int yëf_Royukaay) {
        if (yëf_Royukaay == 0 || 글같음(yëf_Royukaay, dalal_Araf("localhost"), false)) return 0x7f000001;
        if (!yëf_xëyma(yëf_Royukaay, 1)) return 0;
        int mbir_xëyma = 0, 총수 = 0, dëkkuwaay_okte = 0, 자릿수 = 0, 항목수 = 힙[yëf_Royukaay + 1];
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur <= 항목수; wërngël_àlluwa_tur++) {
            int kotu_araf = wërngël_àlluwa_tur == 항목수 ? '.' : 힙[yëf_Royukaay + 2 + wërngël_àlluwa_tur];
            if (kotu_araf == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } mbir_xëyma = mbir_xëyma << 8 | dëkkuwaay_okte; 총수++; dëkkuwaay_okte = 자릿수 = 0; }
            else { if (kotu_araf < '0' || kotu_araf > '9' || ++자릿수 > 3 || (dëkkuwaay_okte = dëkkuwaay_okte * 10 + kotu_araf - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return mbir_xëyma;
    }
    static int dëkkuwaay_Araf(int mbir_xëyma) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int dëkkuwaay_okte = mbir_xëyma >>> 이동비트 & 255;
            if (dëkkuwaay_okte >= 100) dëkkuwaay_SMS[항목수++] = '0' + dëkkuwaay_okte / 100;
            if (dëkkuwaay_okte >= 10) dëkkuwaay_SMS[항목수++] = '0' + dëkkuwaay_okte / 10 % 10;
            dëkkuwaay_SMS[항목수++] = '0' + dëkkuwaay_okte % 10; if (이동비트 != 0) dëkkuwaay_SMS[항목수++] = '.';
        }
        int yëf_Royukaay = jagleel_Dencukaay(1, 항목수); if (!njumte) for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 힙[yëf_Royukaay + 2 + wërngël_àlluwa_tur] = dëkkuwaay_SMS[wërngël_àlluwa_tur]; return yëf_Royukaay;
    }
    static void 통신호출(int boroom, int tur_Lees_dul_soppi, int 서술상수, int 명령코드) {
        if (Word_SMS(boroom, "java/net/InetAddress")) {
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(dënnd_dëkkuwaay(), 2); return; }
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int mbir_xëyma = 주소해독(빼기(2)); if (던진객체 == 0 && !njumte) 넣기(dëkkuwaay_yëf(mbir_xëyma), 2); return;
            }
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 14)) 넣기(dëkkuwaay_Araf(힙[yëf_Royukaay + 2]), 2); return; }
        }
        if (Word_SMS(boroom, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Word_SMS(tur_Lees_dul_soppi, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean jëmmukaay_xëyma_Royukaay = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = jëmmukaay_xëyma_Royukaay ? 빼기(1) : 0, dëkkuwaay_Royukaay = jëmmukaay_xëyma_Royukaay ? 빼기(2) : 0;
                int 항목수 = 빼기(1), mbir_TABLO = 빼기(2), yëf_Royukaay = 빼기(2);
                if (!yëf_xëyma(yëf_Royukaay, 16) || !yëf_xëyma(mbir_TABLO, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[mbir_TABLO + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (dëkkuwaay_Royukaay != 0 && !yëf_xëyma(dëkkuwaay_Royukaay, 14)) return;
                힙[yëf_Royukaay + 2] = mbir_TABLO; 힙참조[yëf_Royukaay + 2] = 1; 힙[yëf_Royukaay + 3] = 항목수;
                힙[yëf_Royukaay + 4] = dëkkuwaay_Royukaay; 힙참조[yëf_Royukaay + 4] = 1; 힙[yëf_Royukaay + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[yëf_Royukaay + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[yëf_Royukaay + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Word_SMS(tur_Lees_dul_soppi, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(tur_Lees_dul_soppi, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(tur_Lees_dul_soppi, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(tur_Lees_dul_soppi, "getPort") && Word_SMS(서술상수, "()I"))) {
                int yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 16)) return;
                int 항목자리 = Word_SMS(tur_Lees_dul_soppi, "getData") ? 2 : Word_SMS(tur_Lees_dul_soppi, "getLength") ? 3 : Word_SMS(tur_Lees_dul_soppi, "getAddress") ? 4 : 5;
                넣기(힙[yëf_Royukaay + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(boroom, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Word_SMS(tur_Lees_dul_soppi, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = kiy_jariñoo_internet.sos_mbaal(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[yëf_Royukaay + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[yëf_Royukaay + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "getLocalPort") && Word_SMS(서술상수, "()I")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 15)) 넣기(힙[yëf_Royukaay + 2] < 0 ? -1 : kiy_jariñoo_internet.mbaal_jël(힙[yëf_Royukaay + 2]), 1); return; }
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "isClosed") && Word_SMS(서술상수, "()Z")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 15)) 넣기(힙[yëf_Royukaay + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Word_SMS(tur_Lees_dul_soppi, "close") && Word_SMS(서술상수, "()V")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 15) && 힙[yëf_Royukaay + 2] >= 0) { kiy_jariñoo_internet.파일서술자닫기(힙[yëf_Royukaay + 2]); 힙[yëf_Royukaay + 2] = -1; } return; }
            if (명령코드 == 182 && (Word_SMS(tur_Lees_dul_soppi, "send") || Word_SMS(tur_Lees_dul_soppi, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), yëf_Royukaay = 빼기(2); if (!yëf_xëyma(전문참조, 16) || !yëf_xëyma(yëf_Royukaay, 15)) return;
                int mbir_TABLO = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[yëf_Royukaay + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(tur_Lees_dul_soppi, "send")) {
                    if (!yëf_xëyma(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 유효길이; wërngël_àlluwa_tur++) 통신임시[wërngël_àlluwa_tur] = 힙[mbir_TABLO + 2 + wërngël_àlluwa_tur];
                    if (kiy_jariñoo_internet.Yónnee_mbaal(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = kiy_jariñoo_internet.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = kiy_jariñoo_internet.밀리초();
                        if (힙[yëf_Royukaay + 4] == 0) 힙[yëf_Royukaay + 4] = 현재시각 + 1;
                        if (힙[yëf_Royukaay + 3] > 0 && 현재시각 - (힙[yëf_Royukaay + 4] - 1) >= 힙[yëf_Royukaay + 3]) { 힙[yëf_Royukaay + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(yëf_Royukaay, 2); 넣기(전문참조, 2); 틀위치[kadar_àlluwa_tur] = kadar_ndigal[kadar_àlluwa_tur]; 바꿈요청 = true; return;
                    }
                    힙[yëf_Royukaay + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 힙[mbir_TABLO + 2 + wërngël_àlluwa_tur] = (byte)통신임시[wërngël_àlluwa_tur];
                    힙[전문참조 + 3] = 항목수; 힙[전문참조 + 4] = dëkkuwaay_yëf(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        foo_xëyma("unsupported java.net method");
    }
    static boolean 흐름대기(int yëf_Royukaay) {
        int 현재시각 = kiy_jariñoo_internet.밀리초();
        if (힙[yëf_Royukaay + 5] == 0) 힙[yëf_Royukaay + 5] = 현재시각 + 1;
        if (힙[yëf_Royukaay + 3] > 0 && 현재시각 - (힙[yëf_Royukaay + 5] - 1) >= 힙[yëf_Royukaay + 3]) { 힙[yëf_Royukaay + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[kadar_àlluwa_tur] = kadar_ndigal[kadar_àlluwa_tur]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int boroom, int tur_Lees_dul_soppi, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Word_SMS(boroom, "java/net/ServerSocket"), dawal = Word_SMS(boroom, "java/io/InputStream") || Word_SMS(boroom, "java/io/OutputStream");
        if (!dawal && 명령코드 == 183 && Word_SMS(tur_Lees_dul_soppi, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { foo_xëyma("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), dëkkuwaay_Royukaay = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, yëf_Royukaay = 빼기(2);
            if (!yëf_xëyma(yëf_Royukaay, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !yëf_xëyma(dëkkuwaay_Royukaay, 14)) return;
            int mbaal_dëkkuwaay = 이름지정여부 ? 주소해독(dëkkuwaay_Royukaay) : 주소지정여부 ? 힙[dëkkuwaay_Royukaay + 2] : 0x7f000001;
            if (njumte || 던진객체 != 0) return;
            int 열린파일번호 = kiy_jariñoo_internet.dawal_Saytu_doxinu_ordinateur(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? kiy_jariñoo_internet.dawal_Saytu_doxinu_ordinateur(1, 열린파일번호, 접속번호) : kiy_jariñoo_internet.JOKKOO_dawal(열린파일번호, mbaal_dëkkuwaay, 접속번호);
            if (처리값 < 0) { kiy_jariñoo_internet.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[yëf_Royukaay + 2] = 열린파일번호; 힙[yëf_Royukaay + 4] = 접속번호; 힙[yëf_Royukaay + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!dawal && Word_SMS(tur_Lees_dul_soppi, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[yëf_Royukaay + 3] = 밀리초값; return; }
        if (!dawal && Word_SMS(tur_Lees_dul_soppi, "close") && Word_SMS(서술상수, "()V")) { int yëf_Royukaay = 빼기(2); if (yëf_xëyma(yëf_Royukaay, 수신쪽 ? 18 : 17) && 힙[yëf_Royukaay + 2] >= 0) { kiy_jariñoo_internet.파일서술자닫기(힙[yëf_Royukaay + 2]); 힙[yëf_Royukaay + 2] = -1; } return; }
        if (!dawal && (Word_SMS(tur_Lees_dul_soppi, "getLocalPort") || Word_SMS(tur_Lees_dul_soppi, "getPort") || Word_SMS(tur_Lees_dul_soppi, "isClosed") || Word_SMS(tur_Lees_dul_soppi, "isConnected"))) {
            int yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(tur_Lees_dul_soppi, "isClosed") ? 힙[yëf_Royukaay + 2] < 0 ? 1 : 0 : Word_SMS(tur_Lees_dul_soppi, "isConnected") ? 힙[yëf_Royukaay + 6] : Word_SMS(tur_Lees_dul_soppi, "getPort") ? 힙[yëf_Royukaay + 4] : 힙[yëf_Royukaay + 2] < 0 ? -1 : kiy_jariñoo_internet.dawal_Saytu_doxinu_ordinateur(4, 힙[yëf_Royukaay + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(tur_Lees_dul_soppi, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 18)) return; int 열린파일번호 = kiy_jariñoo_internet.dawal_Saytu_doxinu_ordinateur(3, 힙[yëf_Royukaay + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(yëf_Royukaay)) 넣기(yëf_Royukaay, 2); return; }
            힙[yëf_Royukaay + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = jagleel_Dencukaay(17, 5); if (njumte) { kiy_jariñoo_internet.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = kiy_jariñoo_internet.dawal_Saytu_doxinu_ordinateur(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !dawal && ((Word_SMS(tur_Lees_dul_soppi, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(tur_Lees_dul_soppi, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 17)) return; if (힙[yëf_Royukaay + 2] < 0 || 힙[yëf_Royukaay + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = jagleel_Dencukaay(19, 4); if (njumte) return; 힙[반환값 + 2] = yëf_Royukaay; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(tur_Lees_dul_soppi, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (dawal) {
            boolean 읽기여부 = Word_SMS(tur_Lees_dul_soppi, "read"), 쓰기여부 = Word_SMS(tur_Lees_dul_soppi, "write"), gatandu = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), 부분배열여부 = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, mbir_TABLO = gatandu || 부분배열여부 ? 빼기(2) : 0;
            int mbir_xëyma = 쓰기여부 && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, yëf_Royukaay = 빼기(2);
            if (!yëf_xëyma(yëf_Royukaay, 19)) return; int 부모참조 = 힙[yëf_Royukaay + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(tur_Lees_dul_soppi, "close") && Word_SMS(서술상수, "()V")) { kiy_jariñoo_internet.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(tur_Lees_dul_soppi, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[yëf_Royukaay + 3] == 0)) { foo_xëyma("unsupported stream operation"); return; }
            if (gatandu || 부분배열여부) { if (!yëf_xëyma(mbir_TABLO, 20)) return; if (gatandu) 항목수 = 힙[mbir_TABLO + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[mbir_TABLO + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[yëf_Royukaay + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? kiy_jariñoo_internet.파일한바이트읽기(열린파일번호) : kiy_jariñoo_internet.파일한바이트쓰기(열린파일번호, gatandu || 부분배열여부 ? 힙[mbir_TABLO + 2 + 시작변위 + 완료수] : mbir_xëyma);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (gatandu || 부분배열여부)) 힙[mbir_TABLO + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(gatandu || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[yëf_Royukaay + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(yëf_Royukaay, 2); if (gatandu || 부분배열여부) 넣기(mbir_TABLO, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(gatandu || 부분배열여부)) 넣기(mbir_xëyma, 1); } return;
            }
            힙[yëf_Royukaay + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : gatandu || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        foo_xëyma("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int tur_Lees_dul_soppi) {
        if (Word_SMS(tur_Lees_dul_soppi, "한국어/자체/palanteer")) return 24;
        if (Word_SMS(tur_Lees_dul_soppi, "한국어/자체/tur")) return 26;
        if (Word_SMS(tur_Lees_dul_soppi, "한국어/자체/butoñ")) return 27;
        if (Word_SMS(tur_Lees_dul_soppi, "한국어/자체/SMS_barabu_denc_ab_joxe")) return 28;
        if (Word_SMS(tur_Lees_dul_soppi, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int tur_Lees_dul_soppi) {
        return 한국어화면종(tur_Lees_dul_soppi) != 0 || Word_SMS(tur_Lees_dul_soppi, "한국어/자체/화면구성요소") || Word_SMS(tur_Lees_dul_soppi, "한국어/자체/xewxew_Topplante_xaarandi");
    }
    static int 화면종(int tur_Lees_dul_soppi) {
        int 한국어종 = 한국어화면종(tur_Lees_dul_soppi); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(tur_Lees_dul_soppi, "javax/swing/JFrame")) return 24;
        if (Word_SMS(tur_Lees_dul_soppi, "javax/swing/JPanel")) return 25;
        if (Word_SMS(tur_Lees_dul_soppi, "javax/swing/JLabel")) return 26;
        if (Word_SMS(tur_Lees_dul_soppi, "javax/swing/JButton")) return 27;
        if (Word_SMS(tur_Lees_dul_soppi, "javax/swing/JTextField")) return 28;
        if (Word_SMS(tur_Lees_dul_soppi, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(tur_Lees_dul_soppi, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int tur_Lees_dul_soppi) {
        return 화면종(tur_Lees_dul_soppi) != 0 || Word_SMS(tur_Lees_dul_soppi, "java/awt/Component") || Word_SMS(tur_Lees_dul_soppi, "java/awt/Container") || Word_SMS(tur_Lees_dul_soppi, "javax/swing/JComponent") || Word_SMS(tur_Lees_dul_soppi, "javax/swing/AbstractButton") || Word_SMS(tur_Lees_dul_soppi, "javax/swing/text/JTextComponent") || Word_SMS(tur_Lees_dul_soppi, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int yëf_Royukaay) { if (!객체유효(yëf_Royukaay)) return false; if (힙[yëf_Royukaay] < 24 || 힙[yëf_Royukaay] > 28) { foo_xëyma("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int yëf_Royukaay, int SMS_Royukaay) {
        if (SMS_Royukaay != 0 && !yëf_xëyma(SMS_Royukaay, 1)) return;
        int 항목수 = SMS_Royukaay == 0 ? 0 : 힙[SMS_Royukaay + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 화면글임시[wërngël_àlluwa_tur] = 힙[SMS_Royukaay + 2 + wërngël_àlluwa_tur];
        if (kiy_jariñoo_internet.화면글(힙[yëf_Royukaay + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[yëf_Royukaay + 3] = SMS_Royukaay; 힙참조[yëf_Royukaay + 3] = 1;
    }
    static int 화면문자읽기(int yëf_Royukaay) {
        int sàq_xëyma = 힙[yëf_Royukaay + 2], 항목수 = kiy_jariñoo_internet.화면연결(8, sàq_xëyma, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { foo_xëyma("GUI text read failed"); return 0; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) { int 부호값 = kiy_jariñoo_internet.화면연결(9, sàq_xëyma, wërngël_àlluwa_tur, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = jagleel_Dencukaay(1, 사용수); if (!njumte) for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 사용수; wërngël_àlluwa_tur++) 힙[반환값 + 2 + wërngël_àlluwa_tur] = 화면글임시[wërngël_àlluwa_tur]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 xoox_xëyma 화면 기능에 연결한다. Swing yëf_xëyma/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int boroom, int tur_Lees_dul_soppi, int 서술상수, int 명령코드) {
        if (Word_SMS(boroom, "한국어/자체/xewxew_Topplante_xaarandi")) {
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int ligeey_jëf = 빼기(2); if (!객체유효(ligeey_jëf)) return;
                if (나중수 == 8) { foo_xëyma("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = ligeey_jëf; return;
            }
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            foo_xëyma("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(boroom, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!yëf_xëyma(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(tur_Lees_dul_soppi, "xewxew_Cosaan") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(tur_Lees_dul_soppi, "ndigel_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(tur_Lees_dul_soppi, "àlluwa_tur") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else foo_xëyma("지원하지 않는 한국어 jëf 알림 호출"); return;
        }
        if (명령코드 == 183 && Word_SMS(tur_Lees_dul_soppi, "<init>")) {
            int 종류 = 한국어화면종(boroom), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (kiy_jariñoo_internet.화면너비() - 폭) / 2; 세로 = (kiy_jariñoo_internet.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { foo_xëyma("지원하지 않는 한국어 화면 생성자"); return; }
            int Tekst = 빼기(2), cër_xëyma = 빼기(2); if (!화면객체(cër_xëyma)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > kiy_jariñoo_internet.화면너비() - 가로 || 높이 > kiy_jariñoo_internet.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int àlluwa_tur = kiy_jariñoo_internet.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (àlluwa_tur < 1 || àlluwa_tur > 32) { foo_xëyma("화면 cër_xëyma 자리가 가득 찼습니다"); return; }
            힙[cër_xëyma + 2] = àlluwa_tur; 화면참조[àlluwa_tur - 1] = cër_xëyma;
            힙[cër_xëyma + 5] = 가로; 힙[cër_xëyma + 6] = 세로; 힙[cër_xëyma + 7] = 폭; 힙[cër_xëyma + 8] = 높이; 힙[cër_xëyma + 10] = 2;
            힙[cër_xëyma + 4] = 받이; 힙참조[cër_xëyma + 4] = 1; 힙[cër_xëyma + 12] = 1;
            kiy_jariñoo_internet.화면연결(1, àlluwa_tur, 가로, 세로, 폭, 높이);
            if (종류 == 24) kiy_jariñoo_internet.화면연결(7, àlluwa_tur, 2, 0, 0, 0);
            화면문자설정(cër_xëyma, Tekst); return;
        }
        if (명령코드 != 182) { foo_xëyma("잘못된 한국어 화면 호출 ndigel"); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "biir_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Tekst = 빼기(2), cër_xëyma = 빼기(2); if (화면객체(cër_xëyma)) 화면문자설정(cër_xëyma, Tekst); return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int cër_xëyma = 빼기(2); if (화면객체(cër_xëyma)) 넣기(화면문자읽기(cër_xëyma), 2); return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), cër_xëyma = 빼기(2);
            if (화면객체(cër_xëyma)) { 힙[cër_xëyma + 4] = 받이; 힙참조[cër_xëyma + 4] = 1; 힙[cër_xëyma + 12] = 1; } return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "mottal_cër") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int xale_xëyma = 빼기(2), 부모 = 빼기(2); if (!화면객체(xale_xëyma) || !화면객체(부모)) return;
            if (kiy_jariñoo_internet.화면연결(2, 힙[부모 + 2], 힙[xale_xëyma + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[xale_xëyma + 11] = 부모; 힙참조[xale_xëyma + 11] = 1; return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), cër_xëyma = 빼기(2); if (!화면객체(cër_xëyma)) return;
            if (kiy_jariñoo_internet.화면연결(1, 힙[cër_xëyma + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[cër_xëyma + 5] = 가로; 힙[cër_xëyma + 6] = 세로; 힙[cër_xëyma + 7] = 폭; 힙[cër_xëyma + 8] = 높이; return;
        }
        if ((Word_SMS(tur_Lees_dul_soppi, "féeñal_palanteer") || Word_SMS(tur_Lees_dul_soppi, "Tej")) && Word_SMS(서술상수, "()V")) {
            boolean feeñin_xëyma = Word_SMS(tur_Lees_dul_soppi, "féeñal_palanteer"); int cër_xëyma = 빼기(2); if (!화면객체(cër_xëyma)) return;
            if (kiy_jariñoo_internet.화면연결(feeñin_xëyma ? 3 : 4, 힙[cër_xëyma + 2], feeñin_xëyma ? 1 : 0, 0, 0, 0) < 0) { foo_xëyma("화면은 duglante 명령에서 실행해야 합니다"); return; }
            힙[cër_xëyma + 9] = feeñin_xëyma ? 1 : 0; return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "보이는가") && Word_SMS(서술상수, "()Z")) { int cër_xëyma = 빼기(2); if (화면객체(cër_xëyma)) 넣기(힙[cër_xëyma + 9], 1); return; }
        foo_xëyma("지원하지 않는 한국어 화면 doxalin_xëyma");
    }
    static void 화면호출(int boroom, int tur_Lees_dul_soppi, int 서술상수, int 명령코드) {
        if (Word_SMS(boroom, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int yëf_Royukaay = 빼기(2); if (!객체유효(yëf_Royukaay)) return; if (나중수 == 8) { foo_xëyma("invokeLater queue full"); return; } 나중실행[나중수++] = yëf_Royukaay; return; }
            if (명령코드 == 184 && Word_SMS(tur_Lees_dul_soppi, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            foo_xëyma("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(boroom, "java/awt/event/ActionEvent")) {
            int yëf_Royukaay = 빼기(2); if (!yëf_xëyma(yëf_Royukaay, 29)) return;
            if (Word_SMS(tur_Lees_dul_soppi, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[yëf_Royukaay + 2], 2);
            else if (Word_SMS(tur_Lees_dul_soppi, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[yëf_Royukaay + 2]), 2);
            else if (Word_SMS(tur_Lees_dul_soppi, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else foo_xëyma("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Word_SMS(tur_Lees_dul_soppi, "<init>")) {
            int 열수 = 0, SMS_Royukaay = 0;
            if (Word_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Royukaay = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Royukaay = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { foo_xëyma("unsupported Swing constructor"); return; }
            int yëf_Royukaay = 빼기(2); if (!객체유효(yëf_Royukaay)) return;
            if (힙[yëf_Royukaay] == 30) { foo_xëyma("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(yëf_Royukaay) || 열수 < 0) return;
            int sàq_xëyma = kiy_jariñoo_internet.화면연결(0, 힙[yëf_Royukaay] - 23, 0, 0, 0, 0);
            if (sàq_xëyma < 1 || sàq_xëyma > 32) { foo_xëyma("GUI widget slots exhausted"); return; }
            힙[yëf_Royukaay + 2] = sàq_xëyma; 화면참조[sàq_xëyma - 1] = yëf_Royukaay; 힙[yëf_Royukaay + 5] = 힙[yëf_Royukaay] == 24 ? 130 : 16; 힙[yëf_Royukaay + 6] = 힙[yëf_Royukaay] == 24 ? 110 : 16;
            힙[yëf_Royukaay + 7] = 힙[yëf_Royukaay] == 24 ? 380 : 220; 힙[yëf_Royukaay + 8] = 힙[yëf_Royukaay] == 24 ? 240 : 28; 힙[yëf_Royukaay + 10] = 1;
            화면문자설정(yëf_Royukaay, SMS_Royukaay); return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "setText") || Word_SMS(tur_Lees_dul_soppi, "setTitle")) { int SMS_Royukaay = 빼기(2), yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(yëf_Royukaay, SMS_Royukaay); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "getText") || Word_SMS(tur_Lees_dul_soppi, "getTitle")) { int yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(yëf_Royukaay), 2); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay)) { 힙[yëf_Royukaay + 4] = 수신참조; 힙참조[yëf_Royukaay + 4] = 1; } return; }
        if (Word_SMS(tur_Lees_dul_soppi, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay)) 넣기(yëf_Royukaay, 2); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Tëralin_Royukaay = 빼기(2), yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay) && Tëralin_Royukaay != 0) foo_xëyma("only absolute layout (null) is supported"); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Tëralin_anam = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Tëralin_anam) 빼기(2);
            int xale_Royukaay = 빼기(2), yëf_Royukaay = 빼기(2); if (!화면객체(xale_Royukaay) || !화면객체(yëf_Royukaay)) return;
            if (kiy_jariñoo_internet.화면연결(2, 힙[yëf_Royukaay + 2], 힙[xale_Royukaay + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[xale_Royukaay + 11] = yëf_Royukaay; 힙참조[xale_Royukaay + 11] = 1; if (!Tëralin_anam) 넣기(xale_Royukaay, 2); return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), rëddu_iks_yi = 빼기(1), yëf_Royukaay = 빼기(2); if (!화면객체(yëf_Royukaay)) return;
            if (kiy_jariñoo_internet.화면연결(1, 힙[yëf_Royukaay + 2], rëddu_iks_yi, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[yëf_Royukaay + 5] = rëddu_iks_yi; 힙[yëf_Royukaay + 6] = 세로좌표; 힙[yëf_Royukaay + 7] = 너비; 힙[yëf_Royukaay + 8] = 높이; return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), yëf_Royukaay = 빼기(2); if (!화면객체(yëf_Royukaay)) return;
            if (kiy_jariñoo_internet.화면연결(1, 힙[yëf_Royukaay + 2], 힙[yëf_Royukaay + 5], 힙[yëf_Royukaay + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[yëf_Royukaay + 7] = 너비; 힙[yëf_Royukaay + 8] = 높이; } return;
        }
        if (Word_SMS(tur_Lees_dul_soppi, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), yëf_Royukaay = 빼기(2); if (!화면객체(yëf_Royukaay)) return; if (상대배치 != 0) { foo_xëyma("only screen centering supported"); return; } 힙[yëf_Royukaay + 5] = (kiy_jariñoo_internet.화면너비() - 힙[yëf_Royukaay + 7]) / 2; 힙[yëf_Royukaay + 6] = (kiy_jariñoo_internet.화면높이() - 힙[yëf_Royukaay + 8]) / 2; kiy_jariñoo_internet.화면연결(1, 힙[yëf_Royukaay + 2], 힙[yëf_Royukaay + 5], 힙[yëf_Royukaay + 6], 힙[yëf_Royukaay + 7], 힙[yëf_Royukaay + 8]); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int sàrt = 빼기(1), yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay)) { if (sàrt < 0 || sàrt > 3) 예외던짐(9, "close policy"); else { 힙[yëf_Royukaay + 10] = sàrt; kiy_jariñoo_internet.화면연결(7, 힙[yëf_Royukaay + 2], sàrt, 0, 0, 0); } } return; }
        if (Word_SMS(tur_Lees_dul_soppi, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int mbir_xëyma = 빼기(1), yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay)) { int 처리값 = kiy_jariñoo_internet.화면연결(3, 힙[yëf_Royukaay + 2], mbir_xëyma, 0, 0, 0); if (처리값 < 0) foo_xëyma("Swing requires a standalone interactive command"); else 힙[yëf_Royukaay + 9] = mbir_xëyma; } return; }
        if (Word_SMS(tur_Lees_dul_soppi, "dispose") && Word_SMS(서술상수, "()V")) { int yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay)) { kiy_jariñoo_internet.화면연결(4, 힙[yëf_Royukaay + 2], 0, 0, 0, 0); 힙[yëf_Royukaay + 9] = 0; } return; }
        if (Word_SMS(tur_Lees_dul_soppi, "repaint") || Word_SMS(tur_Lees_dul_soppi, "validate")) { int yëf_Royukaay = 빼기(2); if (!화면객체(yëf_Royukaay) || !Word_SMS(서술상수, "()V")) return; kiy_jariñoo_internet.화면연결(1, 힙[yëf_Royukaay + 2], 힙[yëf_Royukaay + 5], 힙[yëf_Royukaay + 6], 힙[yëf_Royukaay + 7], 힙[yëf_Royukaay + 8]); return; }
        if (Word_SMS(tur_Lees_dul_soppi, "isVisible") && Word_SMS(서술상수, "()Z")) { int yëf_Royukaay = 빼기(2); if (화면객체(yëf_Royukaay)) 넣기(힙[yëf_Royukaay + 9], 1); return; }
        foo_xëyma("unsupported Swing method (native subset)");
    }
    static void 사건실행(int luñu_name_dëkkuwaay, int 사건번호, boolean 한국어) {
        if (luñu_name_dëkkuwaay < 1 || 힙[luñu_name_dëkkuwaay] < 32) { foo_xëyma("Java event listener required"); return; }
        int bara_denc_àlluwa_tur = tur_doxalin(힙[luñu_name_dëkkuwaay] - 32, 사건번호 == 0 ? (한국어 ? "def_ligeey" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (bara_denc_àlluwa_tur < 0) { foo_xëyma("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; kadar_àlluwa_tur = 0; buumug_jokkale_nekkin[0] = 1; kadar_Tegalo[0] = 0; 틀잠금[0] = doortal_kadar[0] = 0; 바꿈요청 = false;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 128; wërngël_àlluwa_tur++) { dënnd_xëyma[wërngël_àlluwa_tur] = dënnd_xeet[wërngël_àlluwa_tur] = 0; }
        kadar_doxalin[0] = bara_denc_àlluwa_tur; 틀위치[0] = doxalin_Door[bara_denc_àlluwa_tur]; dënnd_xëyma[0] = luñu_name_dëkkuwaay; dënnd_xeet[0] = 2;
        if (사건번호 != 0) { dënnd_xëyma[1] = 사건번호; dënnd_xeet[1] = 2; }
        사건중 = true; def_ndigel(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!njumte) {
            if (나중수 > 0) { int luñu_name_dëkkuwaay = 나중실행[0], 한국어 = 나중한국어[0]; for (int wërngël_àlluwa_tur = 1; wërngël_àlluwa_tur < 나중수; wërngël_àlluwa_tur++) { 나중실행[wërngël_àlluwa_tur - 1] = 나중실행[wërngël_àlluwa_tur]; 나중한국어[wërngël_àlluwa_tur - 1] = 나중한국어[wërngël_àlluwa_tur]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(luñu_name_dëkkuwaay, 0, 한국어 != 0); continue; }
            if (kiy_jariñoo_internet.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = kiy_jariñoo_internet.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { foo_xëyma("GUI event I/O failed"); return; }
            int sàq_xëyma = 사건번호 & 65535; if (sàq_xëyma < 1 || sàq_xëyma > 32) continue; int yëf_Royukaay = 화면참조[sàq_xëyma - 1]; if (yëf_Royukaay == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[yëf_Royukaay + 10] != 0) 힙[yëf_Royukaay + 9] = 0;
                if (힙[yëf_Royukaay + 10] == 3) for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 32; wërngël_àlluwa_tur++) if (화면참조[wërngël_àlluwa_tur] != 0 && 힙[화면참조[wërngël_àlluwa_tur]] == 24) kiy_jariñoo_internet.화면연결(4, wërngël_àlluwa_tur + 1, 0, 0, 0, 0);
            } else if (힙[yëf_Royukaay + 4] != 0) {
                int JANG_MA_Royukaay = jagleel_Dencukaay(29, 2); if (njumte) return; 힙[JANG_MA_Royukaay + 2] = yëf_Royukaay; 힙[JANG_MA_Royukaay + 3] = 힙[yëf_Royukaay + 12]; 힙참조[JANG_MA_Royukaay + 2] = 1; 사건실행(힙[yëf_Royukaay + 4], JANG_MA_Royukaay, 힙[yëf_Royukaay + 12] != 0);
            }
        }
    }
    public static int daw() {
        if (kiy_jariñoo_internet.인수개수() == 1 && 자바도구.같음(kiy_jariñoo_internet.인수(0), "-version")) {
            kiy_jariñoo_internet.biir("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (kiy_jariñoo_internet.인수개수() < 1) { kiy_jariñoo_internet.biir("Usage: java CLASS [ARGS]\n"); return 2; }
        dugal_xabaar_maas_Tekki_baat = Yab_maas_Tekki_baat(dalal_Araf(kiy_jariñoo_internet.인수(0))); if (njumte || dugal_xabaar_maas_Tekki_baat < 0) return 1;
        int dugal_xabaar_Tomb_xëyma = tur_doxalin(dugal_xabaar_maas_Tekki_baat, "daw", "()V");
        boolean 한국어진입 = dugal_xabaar_Tomb_xëyma >= 0 && (doxalin_jot[dugal_xabaar_Tomb_xëyma] & 9) == 9;
        if (!한국어진입) dugal_xabaar_Tomb_xëyma = tur_doxalin(dugal_xabaar_maas_Tekki_baat, "main", "([Ljava/lang/String;)V");
        if (dugal_xabaar_Tomb_xëyma < 0 || (doxalin_jot[dugal_xabaar_Tomb_xëyma] & 9) != 9) foo_xëyma("public static void daw() or main(String[] args) required");
        if (njumte) return 1;
        int 인수 = jagleel_Dencukaay(3, kiy_jariñoo_internet.인수개수() - 1); TABLO_cër[인수] = -1;
        for (int 수 = 1; 수 < kiy_jariñoo_internet.인수개수() && !njumte; 수++) 힙[인수 + 1 + 수] = dalal_Araf(kiy_jariñoo_internet.인수(수));
        kadar_àlluwa_tur = 0; kadar_doxalin[0] = dugal_xabaar_Tomb_xëyma; 틀위치[0] = doxalin_Door[dugal_xabaar_Tomb_xëyma]; dënnd_xëyma[0] = 한국어진입 ? 0 : 인수; dënnd_xeet[0] = 한국어진입 ? 0 : 2;
        buumug_jokkale_nekkin[0] = 1; buumug_jokkale_yëf[0] = jagleel_Dencukaay(13, 2);
        def_ndigel(); if (!njumte) 화면사건들(); return njumte ? 1 : 0;
    }
}
