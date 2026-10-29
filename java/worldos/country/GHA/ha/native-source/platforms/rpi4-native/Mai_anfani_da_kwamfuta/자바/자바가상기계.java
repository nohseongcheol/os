// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fayil/스택/Manazarta/Reshe 경계를 gudanar_Umarni 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fayil = new int[16 * 16384], 임시파일 = new int[16384], Fayil_Suna_SMS = new int[512];
    static int[] Jurarre_tambari = new int[8192], 상가 = new int[8192], 상나 = new int[8192], Zare_Manazarta = new int[8192];
    static int[] tsari_Suna_SMS = new int[512], tsari_rubuta = new int[512], tsari_isa = new int[512], tsari_mamallaki = new int[512];
    static int[] tsari_Fara = new int[512], tsari_Ƙarshe = new int[512], tsari_tara = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], tsari_Tubalin_aiki_rubuta = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] na_gida_Daraja = new int[16384], na_gida_rubuta = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] allo_tsari = new int[128], 틀위치 = new int[128], allo_tara = new int[128], allo_Sharadi = new int[128], Farko_allo = new int[128];
    static int[] Aji_Ma_ana_Suna = new int[16], Aji_Ma_ana_girma = new int[16], 종부모 = new int[16], Aji_Ma_ana_Matsayi = new int[16], 종칸수 = new int[16], Farko_Aji_Ma_ana = new int[16];
    static int[] Aji_Farfajiya = new int[16 * 16], 종접면수 = new int[16];
    static int[] rami_Suna = new int[512], rami_rubuta = new int[512], rami_mamallaki = new int[512], rami_Izini = new int[512], 칸위치 = new int[512], rami_Tarin_bayani = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], TSARI_Dan_gutsuren_bayani = new int[32768], Ajiye_Lamba_mara = new int[256];
    static int Girma, 읽기위치, 함수수, Aji_Suna, allo_Indes = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, Mashigar_bayanai_Aji_Ma_ana;
    static int[] hira_allo = new int[4], hira_Matsayi = new int[4], hira_abu = new int[4], hira_tageti = new int[4], 가닥대기 = new int[4];
    static boolean Kuskure, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], Aji_hira = new int[16];

    static void Kasa_aiki_Daraja(String Microsoft_Word_SMS) {
        if (Kuskure) return;
        int ɓangare_lambar_sirri = 0;
        if (자바도구.같음(Microsoft_Word_SMS, "ArithmeticException: / by zero")) ɓangare_lambar_sirri = 4;
        if (자바도구.같음(Microsoft_Word_SMS, "NullPointerException") || 자바도구.같음(Microsoft_Word_SMS, "null or invalid array")) ɓangare_lambar_sirri = 5;
        if (자바도구.같음(Microsoft_Word_SMS, "ArrayIndexOutOfBoundsException")) ɓangare_lambar_sirri = 7;
        if (자바도구.같음(Microsoft_Word_SMS, "StringIndexOutOfBoundsException")) ɓangare_lambar_sirri = 8;
        if (자바도구.같음(Microsoft_Word_SMS, "NumberFormatException")) ɓangare_lambar_sirri = 10;
        if (자바도구.같음(Microsoft_Word_SMS, "FileNotFoundException: file open failed")) ɓangare_lambar_sirri = 12;
        if (자바도구.같음(Microsoft_Word_SMS, "IOException: stream closed") || 자바도구.같음(Microsoft_Word_SMS, "IOException: read failed") || 자바도구.같음(Microsoft_Word_SMS, "IOException: write failed")) ɓangare_lambar_sirri = 11;
        if (자바도구.같음(Microsoft_Word_SMS, "ClassCastException")) ɓangare_lambar_sirri = 14;
        if (자바도구.같음(Microsoft_Word_SMS, "NegativeArraySizeException")) ɓangare_lambar_sirri = 15;
        if (ɓangare_lambar_sirri != 0 && allo_Indes >= 0) { 예외던짐(ɓangare_lambar_sirri, Microsoft_Word_SMS); return; }
        Mai_anfani_da_kwamfuta.Yi_Rubutu("JVM error: "); Mai_anfani_da_kwamfuta.Yi_Rubutu(Microsoft_Word_SMS); Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10); Kuskure = true;
    }
    static boolean darfi(int Tafiyar_da, int Tsawo_Daraja) {
        if (Tafiyar_da < 0 || Tafiyar_da >= Fayil.length || Tsawo_Daraja < 0) return false;
        int Aji_Ma_ana = Tafiyar_da / 16384;
        return Tafiyar_da % 16384 <= Aji_Ma_ana_girma[Aji_Ma_ana] && Tsawo_Daraja <= Aji_Ma_ana_girma[Aji_Ma_ana] - Tafiyar_da % 16384;
    }
    static int bayit_Daraja() {
        if (!darfi(읽기위치, 1)) { Kasa_aiki_Daraja("truncated class file"); return 0; }
        return Fayil[읽기위치++];
    }
    static int 짧은수() { return bayit_Daraja() << 8 | bayit_Daraja(); }
    static int Lamba_mara() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int Tsawo_Daraja) { if (!darfi(읽기위치, Tsawo_Daraja)) Kasa_aiki_Daraja("invalid attribute size"); else 읽기위치 += Tsawo_Daraja; }
    static boolean Bincika_Jurarre(int 수, int 종류) {
        if (수 <= 0 || 수 >= Jurarre_tambari.length || Jurarre_tambari[수] != 종류) { Kasa_aiki_Daraja("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Tafiyar_da, int Tsawo_Daraja, String Microsoft_Word_SMS) {
        if (!darfi(Tafiyar_da, Tsawo_Daraja)) return false;
        int 읽는자리 = Tafiyar_da, 끝 = Tafiyar_da + Tsawo_Daraja;
        for (int Warware_Indes = 0; Warware_Indes < Microsoft_Word_SMS.length(); Warware_Indes++) {
            int Lambar_sirrin_harafi = Microsoft_Word_SMS.charAt(Warware_Indes);
            if (Lambar_sirrin_harafi > 0 && Lambar_sirrin_harafi < 128) { if (읽는자리 >= 끝 || Fayil[읽는자리++] != Lambar_sirrin_harafi) return false; }
            else if (Lambar_sirrin_harafi < 2048) {
                if (읽는자리 + 2 > 끝 || Fayil[읽는자리++] != (192 | (Lambar_sirrin_harafi >> 6)) || Fayil[읽는자리++] != (128 | (Lambar_sirrin_harafi & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fayil[읽는자리++] != (224 | (Lambar_sirrin_harafi >> 12)) || Fayil[읽는자리++] != (128 | ((Lambar_sirrin_harafi >> 6) & 63)) || Fayil[읽는자리++] != (128 | (Lambar_sirrin_harafi & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Microsoft_Word_SMS(int Jurarre_Daraja, String Microsoft_Word_SMS) { return Bincika_Jurarre(Jurarre_Daraja, 1) && 구간(상가[Jurarre_Daraja], 상나[Jurarre_Daraja], Microsoft_Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!Bincika_Jurarre(가, 1) || !Bincika_Jurarre(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Fayil[상가[가] + 수] != Fayil[상가[나] + 수]) return false;
        return true;
    }
    static int Aji_Suna_SMS(int 수) { return Bincika_Jurarre(수, 7) && Bincika_Jurarre(상가[수], 1) ? 상가[수] : 0; }
    static int Manazarta_Suna(int 수) { return Bincika_Jurarre(수, 12) && Bincika_Jurarre(상가[수], 1) ? 상가[수] : 0; }
    static int Manazarta_rubuta(int 수) { return Bincika_Jurarre(수, 12) && Bincika_Jurarre(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean holoko_rubuta) {
        if (읽기위치 >= 끝) { Kasa_aiki_Daraja("invalid descriptor"); return 0; }
        int Daraja = bayit_Daraja();
        if (Daraja == 'V' && holoko_rubuta) return 0;
        if (Daraja == 'I' || Daraja == 'B' || Daraja == 'C' || Daraja == 'S' || Daraja == 'Z') return 1;
        if (Daraja == '[') { 서술형(끝, false); return 2; }
        if (Daraja == 'L') {
            int Tafiyar_da = 읽기위치;
            while (읽기위치 < 끝 && Fayil[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Tafiyar_da) Kasa_aiki_Daraja("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        Kasa_aiki_Daraja("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int AIKI_Daraja) {
        int 이전 = 읽기위치, 수 = tsari_rubuta[AIKI_Daraja];
        if (!Bincika_Jurarre(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (bayit_Daraja() != '(') Kasa_aiki_Daraja("invalid method descriptor");
        int 개수 = 0;
        while (!Kuskure && 읽기위치 < 끝 && Fayil[읽기위치] != ')') {
            if (개수 == 16) { Kasa_aiki_Daraja("too many method arguments"); break; }
            tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bayit_Daraja() != ')') Kasa_aiki_Daraja("invalid method descriptor");
        함수반환[AIKI_Daraja] = 서술형(끝, true); 함수인수수[AIKI_Daraja] = 개수;
        if (읽기위치 != 끝) Kasa_aiki_Daraja("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int Daraja = 짧은수(); return Daraja == 0 ? 0 : 현재읽는종 * 512 + Daraja; }
    static int 명상수() { return tsari_mamallaki[allo_tsari[allo_Indes]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Kuskure; 수++) { Bincika_Jurarre(상번호(), 1); 건너(Lamba_mara()); }
    }
    static int Umarni_Tsawo(int Daraja) {
        if (Daraja == 16 || Daraja == 18 || Daraja == 21 || Daraja == 25 || Daraja == 54 || Daraja == 58 || Daraja == 188) return 2;
        if (Daraja == 17 || Daraja == 19 || Daraja == 132 || Daraja >= 153 && Daraja <= 167
            || Daraja >= 178 && Daraja <= 184 || Daraja == 187 || Daraja == 189 || Daraja == 192 || Daraja == 193 || Daraja == 198 || Daraja == 199) return 3;
        if (Daraja == 185 || Daraja == 200) return 5;
        if (Daraja >= 0 && Daraja <= 8 || Daraja >= 26 && Daraja <= 29 || Daraja >= 42 && Daraja <= 46 || Daraja >= 50 && Daraja <= 53
            || Daraja >= 59 && Daraja <= 62 || Daraja >= 75 && Daraja <= 79 || Daraja >= 83 && Daraja <= 95
            || Daraja == 96 || Daraja == 100 || Daraja == 104 || Daraja == 108 || Daraja == 112 || Daraja == 116
            || Daraja == 120 || Daraja == 122 || Daraja == 124 || Daraja == 126 || Daraja == 128 || Daraja == 130
            || Daraja >= 145 && Daraja <= 147 || Daraja == 172 || Daraja == 176 || Daraja == 177 || Daraja == 190 || Daraja == 191
            || Daraja == 194 || Daraja == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!darfi(읽는자리, 4)) { Kasa_aiki_Daraja("truncated bytecode operand"); return 0; }
        return Fayil[읽는자리] << 24 | Fayil[읽는자리 + 1] << 16 | Fayil[읽는자리 + 2] << 8 | Fayil[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Tafiyar_da, int 끝) {
        int Daraja = Fayil[읽는자리], Tsawo_Daraja = Umarni_Tsawo(Daraja);
        if (Daraja == 170 || Daraja == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Tafiyar_da) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (Daraja == 170 ? 12 : 8)) return 0;
            int 항목수 = Daraja == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            Tsawo_Daraja = 기준자리 - 읽는자리 + (Daraja == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (Daraja == 196 && 읽는자리 + 1 < 끝) {
            int Microsoft_Word_Tarin_bayani = Fayil[읽는자리 + 1]; Tsawo_Daraja = Microsoft_Word_Tarin_bayani == 132 ? 6 : (Microsoft_Word_Tarin_bayani == 21 || Microsoft_Word_Tarin_bayani == 25 || Microsoft_Word_Tarin_bayani == 54 || Microsoft_Word_Tarin_bayani == 58) ? 4 : 0;
        }
        return Tsawo_Daraja > 0 && Tsawo_Daraja <= 끝 - 읽는자리 ? Tsawo_Daraja : 0;
    }
    static void Bincika_Zangon_ƙarshe_Daraja(int Zangon_ƙarshe_Daraja, int AIKI_Daraja) {
        if (Zangon_ƙarshe_Daraja < tsari_Fara[AIKI_Daraja] || Zangon_ƙarshe_Daraja >= tsari_Ƙarshe[AIKI_Daraja] || 경계[Zangon_ƙarshe_Daraja] != AIKI_Daraja + 1) Kasa_aiki_Daraja("invalid branch target");
    }
    static void 클래스읽기(int Aji_Ma_ana) {
        현재읽는종 = Aji_Ma_ana; 읽기위치 = Aji_Ma_ana * 16384; Girma = 읽기위치 + Aji_Ma_ana_girma[Aji_Ma_ana];
        if (Lamba_mara() != 0xcafebabe) { Kasa_aiki_Daraja("not a class file"); return; }
        int 부판 = 짧은수(), siga_Daraja = 짧은수();
        if (siga_Daraja < 45 || siga_Daraja > 52 || 부판 != 0) { Kasa_aiki_Daraja("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = Aji_Ma_ana * 512;
        if (상수수 < 1 || 상수수 > 512) { Kasa_aiki_Daraja("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !Kuskure; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = bayit_Daraja(); Jurarre_tambari[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = Lamba_mara();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else Kasa_aiki_Daraja("unsupported constant type");
        }
        int izini_Daraja = 짧은수();
        if ((izini_Daraja & (0x2000 | 0x4000)) != 0) Kasa_aiki_Daraja("annotation/enum class unsupported");
        Aji_Ma_ana_Suna[Aji_Ma_ana] = Aji_Suna_SMS(상번호());
        종부모[Aji_Ma_ana] = Aji_Suna_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { Kasa_aiki_Daraja("interface count limit"); return; }
        종접면수[Aji_Ma_ana] = 접면수;
        for (int Warware_Indes = 0; Warware_Indes < 접면수; Warware_Indes++) Aji_Farfajiya[Aji_Ma_ana * 16 + Warware_Indes] = Aji_Suna_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { Kasa_aiki_Daraja("field count limit (512)"); return; }
        for (int Warware_Indes = 0; Warware_Indes < 필드수 && !Kuskure; Warware_Indes++) {
            int Fayil_Indes = 칸수++; rami_mamallaki[Fayil_Indes] = Aji_Ma_ana; rami_Izini[Fayil_Indes] = 짧은수(); rami_Suna[Fayil_Indes] = 상번호(); rami_rubuta[Fayil_Indes] = 상번호();
            Bincika_Jurarre(rami_Suna[Fayil_Indes], 1); Bincika_Jurarre(rami_rubuta[Fayil_Indes], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[rami_rubuta[Fayil_Indes]]; int ɓangare_lambar_sirri = 서술형(읽기위치 + 상나[rami_rubuta[Fayil_Indes]], false); 읽기위치 = 보존값;
            if ((rami_Izini[Fayil_Indes] & 8) == 0) 칸위치[Fayil_Indes] = 종칸수[Aji_Ma_ana]++;
            int siffofi_Tarin_bayani = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < siffofi_Tarin_bayani && !Kuskure; 안쪽자리++) {
                int Suna_Jurarre = 상번호(), 유효길이 = Lamba_mara();
                if (Microsoft_Word_SMS(Suna_Jurarre, "ConstantValue") && 유효길이 == 2) {
                    int Tarin_bayani_Daraja = 상번호();
                    if (ɓangare_lambar_sirri == 1 && Bincika_Jurarre(Tarin_bayani_Daraja, 3)) rami_Tarin_bayani[Fayil_Indes] = 상가[Tarin_bayani_Daraja];
                    else if (ɓangare_lambar_sirri == 2 && Bincika_Jurarre(Tarin_bayani_Daraja, 8)) rami_Tarin_bayani[Fayil_Indes] = Jurarre_SMS(상가[Tarin_bayani_Daraja]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { Kasa_aiki_Daraja("method count limit (512)"); return; }
        for (int Warware_Indes = 0; Warware_Indes < 개수 && !Kuskure; Warware_Indes++) {
            int 수 = 함수수++; tsari_mamallaki[수] = Aji_Ma_ana;
            tsari_isa[수] = 짧은수(); tsari_Suna_SMS[수] = 상번호(); tsari_rubuta[수] = 상번호();
            Bincika_Jurarre(tsari_Suna_SMS[수], 1); 서술읽기(수);
            if ((tsari_isa[수] & 8) == 0) {
                if (함수인수수[수] == 16) { Kasa_aiki_Daraja("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) tsari_Tubalin_aiki_rubuta[수 * 16 + 비교자리] = tsari_Tubalin_aiki_rubuta[수 * 16 + 비교자리 - 1];
                tsari_Tubalin_aiki_rubuta[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((tsari_isa[수] & 0x100) != 0) Kasa_aiki_Daraja("user native method unsupported");
            if (Microsoft_Word_SMS(tsari_Suna_SMS[수], "<clinit>")) Farko_Aji_Ma_ana[Aji_Ma_ana] = 수 + 1;
            for (int kyamarar_gaba_Daraja = 0; kyamarar_gaba_Daraja < 수; kyamarar_gaba_Daraja++) if (tsari_mamallaki[kyamarar_gaba_Daraja] == Aji_Ma_ana && 같은말(tsari_Suna_SMS[kyamarar_gaba_Daraja], tsari_Suna_SMS[수]) && 같은말(tsari_rubuta[kyamarar_gaba_Daraja], tsari_rubuta[수])) Kasa_aiki_Daraja("duplicate method");
            int 속성수 = 짧은수();
            for (int siffofi_Daraja = 0; siffofi_Daraja < 속성수 && !Kuskure; siffofi_Daraja++) {
                int Suna = 상번호(), Tsawo_Daraja = Lamba_mara(), Tafiyar_da = 읽기위치;
                if (!darfi(Tafiyar_da, Tsawo_Daraja)) { Kasa_aiki_Daraja("truncated method attribute"); break; }
                if (Microsoft_Word_SMS(Suna, "Code")) {
                    if (tsari_Fara[수] != 0) Kasa_aiki_Daraja("duplicate Code attribute");
                    tsari_tara[수] = 짧은수(); 함수지역[수] = 짧은수(); int lambar_sirri_Tsawo = Lamba_mara();
                    if (tsari_tara[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || lambar_sirri_Tsawo < 1 || lambar_sirri_Tsawo > 8192) Kasa_aiki_Daraja("method memory limits exceeded");
                    tsari_Fara[수] = 읽기위치; 건너(lambar_sirri_Tsawo); tsari_Ƙarshe[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { Kasa_aiki_Daraja("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int Kuskure_Manazarta = 잡기수++; 잡기함수[Kuskure_Manazarta] = 수;
                        잡기시작[Kuskure_Manazarta] = tsari_Fara[수] + 짧은수(); 잡기끝[Kuskure_Manazarta] = tsari_Fara[수] + 짧은수();
                        잡기위치[Kuskure_Manazarta] = tsari_Fara[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[Kuskure_Manazarta] = 부호값 == 0 ? 0 : Aji_Suna_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Tafiyar_da + Tsawo_Daraja) Kasa_aiki_Daraja("Code attribute size mismatch");
                } else 건너(Tsawo_Daraja);
            }
            if ((tsari_isa[수] & 0x400) != 0) continue;
            if (tsari_Fara[수] == 0) Kasa_aiki_Daraja("missing Code attribute");
            int rami_Mashigar_bayanai = tsari_Fara[수];
            while (rami_Mashigar_bayanai < tsari_Ƙarshe[수] && !Kuskure) {
                int Tsawo_Daraja = 길이읽기(rami_Mashigar_bayanai, tsari_Fara[수], tsari_Ƙarshe[수]);
                if (Tsawo_Daraja == 0) { Kasa_aiki_Daraja("unsupported or truncated bytecode"); break; }
                경계[rami_Mashigar_bayanai] = 수 + 1; rami_Mashigar_bayanai += Tsawo_Daraja;
            }
            rami_Mashigar_bayanai = tsari_Fara[수];
            while (rami_Mashigar_bayanai < tsari_Ƙarshe[수] && !Kuskure) {
                int Daraja = Fayil[rami_Mashigar_bayanai];
                if (Daraja >= 153 && Daraja <= 167 || Daraja == 198 || Daraja == 199) Bincika_Zangon_ƙarshe_Daraja(rami_Mashigar_bayanai + (short)(Fayil[rami_Mashigar_bayanai + 1] << 8 | Fayil[rami_Mashigar_bayanai + 2]), 수);
                if (Daraja == 200) Bincika_Zangon_ƙarshe_Daraja(rami_Mashigar_bayanai + 위치정수(rami_Mashigar_bayanai + 1), 수);
                if (Daraja == 170 || Daraja == 171) {
                    int 읽는자리 = rami_Mashigar_bayanai + 1; while ((읽는자리 - tsari_Fara[수]) % 4 != 0) 읽는자리++;
                    Bincika_Zangon_ƙarshe_Daraja(rami_Mashigar_bayanai + 위치정수(읽는자리), 수);
                    int 항목수 = Daraja == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += Daraja == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) Bincika_Zangon_ƙarshe_Daraja(rami_Mashigar_bayanai + 위치정수(읽는자리 + 안쪽자리 * (Daraja == 170 ? 4 : 8) + (Daraja == 170 ? 0 : 4)), 수);
                }
                rami_Mashigar_bayanai += 길이읽기(rami_Mashigar_bayanai, tsari_Fara[수], tsari_Ƙarshe[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                Bincika_Zangon_ƙarshe_Daraja(잡기시작[안쪽자리], 수); Bincika_Zangon_ƙarshe_Daraja(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != tsari_Ƙarshe[수]) Bincika_Zangon_ƙarshe_Daraja(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) Kasa_aiki_Daraja("invalid exception range");
            }
        }
        if (!Kuskure) 속성건너();
        if (읽기위치 != Girma) Kasa_aiki_Daraja("extra class file data");
    }
    static int kasafta_Wurin_adana(int 종류, int Tsawo_Daraja) { return 새기억(종류, Tsawo_Daraja); }
    static boolean abu_Daraja(int Manazarta, int 종류) {
        if (!객체유효(Manazarta)) return false;
        if (힙[Manazarta] != 종류) { Kasa_aiki_Daraja("object type mismatch"); return false; }
        return true;
    }
    static int Jurarre_SMS(int Indes) {
        if (!Bincika_Jurarre(Indes, 1)) return 0;
        if (Zare_Manazarta[Indes] != 0) return Zare_Manazarta[Indes];
        int Manazarta = kasafta_Wurin_adana(1, 상나[Indes]); if (Kuskure) return 0;
        int 끝 = 상가[Indes] + 상나[Indes], 수 = 상가[Indes], Tsawo_Daraja = 0;
        while (수 < 끝 && !Kuskure) {
            int Daraja = Fayil[수++];
            if (Daraja == 0) Kasa_aiki_Daraja("invalid modified UTF-8");
            else if (Daraja >= 192 && Daraja <= 223 && 수 < 끝) {
                int 다음 = Fayil[수++];
                if ((다음 & 192) != 128) Kasa_aiki_Daraja("invalid modified UTF-8");
                Daraja = (Daraja & 31) << 6 | 다음 & 63;
                if (Daraja != 0 && Daraja < 128) Kasa_aiki_Daraja("overlong modified UTF-8");
            } else if (Daraja >= 224 && Daraja <= 239 && 수 + 1 < 끝) {
                int 가 = Fayil[수++], 나 = Fayil[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) Kasa_aiki_Daraja("invalid modified UTF-8");
                Daraja = (Daraja & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (Daraja < 2048) Kasa_aiki_Daraja("overlong modified UTF-8");
            } else if (Daraja >= 128) Kasa_aiki_Daraja("invalid modified UTF-8");
            힙[Manazarta + 2 + Tsawo_Daraja++] = Daraja;
        }
        힙[Manazarta + 1] = Tsawo_Daraja; Zare_Manazarta[Indes] = Manazarta; return Manazarta;
    }
    static int sauka_Harafi(String Daraja) {
        int Manazarta = kasafta_Wurin_adana(1, Daraja.length()); if (Kuskure) return 0;
        for (int 수 = 0; 수 < Daraja.length(); 수++) 힙[Manazarta + 2 + 수] = Daraja.charAt(수);
        return Manazarta;
    }
    static void Rubuta_SMS(int Manazarta) {
        if (Manazarta == 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("null"); return; }
        if (!abu_Daraja(Manazarta, 1)) return;
        for (int 수 = 0; 수 < 힙[Manazarta + 1]; 수++) Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(힙[Manazarta + 2 + 수]);
    }
    static int lamba_Harafi(int Daraja) {
        int Manazarta = kasafta_Wurin_adana(1, 11); if (Kuskure) return 0;
        int Tsawo_Daraja = 0;
        if (Daraja < 0) 힙[Manazarta + 2 + Tsawo_Daraja++] = '-'; else Daraja = -Daraja;
        int 자리 = 1000000000; boolean Tafiyar_da = false;
        while (자리 != 0) {
            int 수 = -(Daraja / 자리);
            if (수 != 0 || Tafiyar_da || 자리 == 1) { 힙[Manazarta + 2 + Tsawo_Daraja++] = '0' + 수; Tafiyar_da = true; }
            Daraja %= 자리; 자리 /= 10;
        }
        힙[Manazarta + 1] = Tsawo_Daraja; return Manazarta;
    }
    static int 정수해독(int Manazarta) {
        if (!abu_Daraja(Manazarta, 1)) return 0;
        int Tsawo_Daraja = 힙[Manazarta + 1], 수 = 0, Daraja = 0; boolean 음수 = false;
        if (Tsawo_Daraja > 0 && (힙[Manazarta + 2] == '-' || 힙[Manazarta + 2] == '+')) { 음수 = 힙[Manazarta + 2] == '-'; 수++; }
        if (수 == Tsawo_Daraja) Kasa_aiki_Daraja("NumberFormatException");
        for (; 수 < Tsawo_Daraja && !Kuskure; 수++) {
            int lamba_Daraja = 힙[Manazarta + 2 + 수] - '0';
            if (lamba_Daraja < 0 || lamba_Daraja > 9 || Daraja < -214748364 || Daraja == -214748364 && lamba_Daraja > (음수 ? 8 : 7)) Kasa_aiki_Daraja("NumberFormatException");
            Daraja = Daraja * 10 - lamba_Daraja;
        }
        return 음수 ? Daraja : -Daraja;
    }
    static void 넣기(int Daraja, int rubuta_Daraja) {
        if (Kuskure) return;
        if (allo_Indes < 0 || allo_tara[allo_Indes] >= tsari_tara[allo_tsari[allo_Indes]]) { Kasa_aiki_Daraja("operand stack overflow"); return; }
        int rami_Mashigar_bayanai = allo_Indes * 128 + allo_tara[allo_Indes]++; 스택값[rami_Mashigar_bayanai] = Daraja; 스택형[rami_Mashigar_bayanai] = rubuta_Daraja;
    }
    static int 빼기(int rubuta_Daraja) {
        if (Kuskure) return 0;
        if (allo_Indes < 0 || allo_tara[allo_Indes] < 1) { Kasa_aiki_Daraja("operand stack underflow"); return 0; }
        int rami_Mashigar_bayanai = allo_Indes * 128 + --allo_tara[allo_Indes]; 반환형 = 스택형[rami_Mashigar_bayanai];
        if (rubuta_Daraja != 0 && 반환형 != rubuta_Daraja) Kasa_aiki_Daraja("operand type mismatch");
        if (반환형 == 2) Kare_Daraja(스택값[rami_Mashigar_bayanai]);
        return 스택값[rami_Mashigar_bayanai];
    }
    static void 지역읽기(int Indes, int rubuta_Daraja) {
        if (Indes >= 함수지역[allo_tsari[allo_Indes]] || Indes < 0 || na_gida_rubuta[allo_Indes * 128 + Indes] != rubuta_Daraja) { Kasa_aiki_Daraja("invalid or uninitialized local"); return; }
        넣기(na_gida_Daraja[allo_Indes * 128 + Indes], rubuta_Daraja);
    }
    static void Rubuta_na_gida(int Indes, int rubuta_Daraja) {
        if (Indes >= 함수지역[allo_tsari[allo_Indes]] || Indes < 0) { Kasa_aiki_Daraja("local index out of range"); return; }
        int Daraja = 빼기(rubuta_Daraja); na_gida_Daraja[allo_Indes * 128 + Indes] = Daraja; na_gida_rubuta[allo_Indes * 128 + Indes] = rubuta_Daraja;
    }
    static int 명바() {
        int 위치 = 틀위치[allo_Indes];
        if (위치 < tsari_Fara[allo_tsari[allo_Indes]] || 위치 >= tsari_Ƙarshe[allo_tsari[allo_Indes]]) { Kasa_aiki_Daraja("instruction pointer out of range"); return 0; }
        틀위치[allo_Indes]++; return Fayil[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void Matsar_da_Daraja(int 위치) {
        int AIKI_Daraja = allo_tsari[allo_Indes];
        if (위치 < tsari_Fara[AIKI_Daraja] || 위치 >= tsari_Ƙarshe[AIKI_Daraja] || 경계[위치] != AIKI_Daraja + 1) Kasa_aiki_Daraja("invalid branch target");
        else 틀위치[allo_Indes] = 위치;
    }
    static void 호출(int AIKI_Daraja) {
        if (allo_Indes % 32 == 31) { Kasa_aiki_Daraja("call stack limit (32)"); return; }
        int 다음 = allo_Indes + 1;
        for (int 수 = 0; 수 < 128; 수++) na_gida_rubuta[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[AIKI_Daraja] - 1; 수 >= 0; 수--) {
            na_gida_Daraja[다음 * 128 + 수] = 빼기(tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 수]); na_gida_rubuta[다음 * 128 + 수] = tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 수];
        }
        if (Kuskure) return;
        allo_Indes = 다음; Farko_allo[allo_Indes] = 0; allo_tsari[allo_Indes] = AIKI_Daraja; 틀위치[allo_Indes] = tsari_Fara[AIKI_Daraja]; allo_tara[allo_Indes] = 0;
    }
    static void 반환(int rubuta_Daraja) {
        if (rubuta_Daraja != 함수반환[allo_tsari[allo_Indes]]) { Kasa_aiki_Daraja("return type mismatch"); return; }
        int Daraja = rubuta_Daraja == 0 ? 0 : 빼기(rubuta_Daraja);
        if (Farko_allo[allo_Indes] != 0) Aji_Ma_ana_Matsayi[Farko_allo[allo_Indes] - 1] = 2;
        if (틀잠금[allo_Indes] != 0) { 잠금풀기(틀잠금[allo_Indes]); 틀잠금[allo_Indes] = 0; }
        allo_Indes--; if (allo_Indes >= 현재가닥 * 32 && rubuta_Daraja != 0) 넣기(Daraja, rubuta_Daraja);
    }
    static int[] watsuwa_Fayil_Suna = new int[64];
    static void Fayil_watsuwa_Kira(int mamallaki_Daraja, int Suna, int zubi_Daraja, int Umarni) {
        boolean 출력 = Microsoft_Word_SMS(mamallaki_Daraja, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Umarni == 183 && Microsoft_Word_SMS(Suna, "<init>")) {
            boolean 이어 = false;
            if (출력 && Microsoft_Word_SMS(zubi_Daraja, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Microsoft_Word_SMS(zubi_Daraja, "(Ljava/lang/String;)V")) { Kasa_aiki_Daraja("unsupported file stream constructor"); return; }
            int Fayil_Mashigar_bayanai_Suna = 빼기(2), watsuwa_Daraja = 빼기(2);
            if (!abu_Daraja(Fayil_Mashigar_bayanai_Suna, 1) || !abu_Daraja(watsuwa_Daraja, 종류) || Kuskure) return;
            if (힙[watsuwa_Daraja + 3] != 0) { Kasa_aiki_Daraja("file stream already initialized"); return; }
            int Tsawo_Daraja = 힙[Fayil_Mashigar_bayanai_Suna + 1];
            if (Tsawo_Daraja < 1 || Tsawo_Daraja > 63) { Kasa_aiki_Daraja("invalid file name length"); return; }
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < Tsawo_Daraja; rami_Mashigar_bayanai++) {
                int Daraja = 힙[Fayil_Mashigar_bayanai_Suna + 2 + rami_Mashigar_bayanai];
                if (Daraja < 1) { Kasa_aiki_Daraja("invalid file stream path"); return; }
                watsuwa_Fayil_Suna[rami_Mashigar_bayanai] = Daraja;
            }
            watsuwa_Fayil_Suna[Tsawo_Daraja] = 0;
            int 서술자 = Mai_anfani_da_kwamfuta.파일서술자열기(watsuwa_Fayil_Suna, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { Kasa_aiki_Daraja("FileNotFoundException: file open failed"); return; }
            힙[watsuwa_Daraja + 2] = 서술자; 힙[watsuwa_Daraja + 3] = 1;
            return;
        }
        if (Umarni != 182) { Kasa_aiki_Daraja("invalid file stream invocation"); return; }
        if ((출력 && Microsoft_Word_SMS(Suna, "write") || !출력 && Microsoft_Word_SMS(Suna, "read"))
            && (Microsoft_Word_SMS(zubi_Daraja, 출력 ? "([B)V" : "([B)I") || Microsoft_Word_SMS(zubi_Daraja, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean darfi_Daraja = Microsoft_Word_SMS(zubi_Daraja, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = darfi_Daraja ? 빼기(1) : 0, 시작점 = darfi_Daraja ? 빼기(1) : 0, Tarin_bayani_TSARI = 빼기(2), abu_Manazarta = 빼기(2);
            if (!abu_Daraja(Tarin_bayani_TSARI, 20) || !abu_Daraja(abu_Manazarta, 종류)) return;
            if (!darfi_Daraja) 항목수 = 힙[Tarin_bayani_TSARI + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[Tarin_bayani_TSARI + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[abu_Manazarta + 3] == 0 || 힙[abu_Manazarta + 2] < 0) { Kasa_aiki_Daraja("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !Kuskure) {
                int 반환값 = 출력 ? Mai_anfani_da_kwamfuta.파일한바이트쓰기(힙[abu_Manazarta + 2], 힙[Tarin_bayani_TSARI + 2 + 시작점 + 완료수]) : Mai_anfani_da_kwamfuta.파일한바이트읽기(힙[abu_Manazarta + 2]);
                if (반환값 < 0) { Kasa_aiki_Daraja(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[Tarin_bayani_TSARI + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Microsoft_Word_SMS(Suna, "flush") && Microsoft_Word_SMS(zubi_Daraja, "()V")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 종류) && 힙[abu_Manazarta + 2] < 0) Kasa_aiki_Daraja("IOException: stream closed"); return; }
        int Aiki = -1, Daraja = 0;
        if (Microsoft_Word_SMS(Suna, "close") && Microsoft_Word_SMS(zubi_Daraja, "()V")) Aiki = 0;
        if (!출력 && Microsoft_Word_SMS(Suna, "read") && Microsoft_Word_SMS(zubi_Daraja, "()I")) Aiki = 1;
        if (출력 && Microsoft_Word_SMS(Suna, "write") && Microsoft_Word_SMS(zubi_Daraja, "(I)V")) { Aiki = 2; Daraja = 빼기(1); }
        if (Aiki < 0) { Kasa_aiki_Daraja("unsupported file stream method"); return; }
        int watsuwa_Daraja = 빼기(2);
        if (!abu_Daraja(watsuwa_Daraja, 종류) || Kuskure) return;
        if (힙[watsuwa_Daraja + 3] == 0) { Kasa_aiki_Daraja("uninitialized file stream"); return; }
        int 서술자 = 힙[watsuwa_Daraja + 2];
        if (Aiki == 0) {
            if (서술자 >= 0 && Mai_anfani_da_kwamfuta.파일서술자닫기(서술자) < 0) Kasa_aiki_Daraja("IOException: close failed");
            힙[watsuwa_Daraja + 2] = -1; return;
        }
        if (서술자 < 0) { Kasa_aiki_Daraja("IOException: stream closed"); return; }
        if (Aiki == 1) {
            int 결과 = Mai_anfani_da_kwamfuta.파일한바이트읽기(서술자);
            if (결과 < -1) Kasa_aiki_Daraja("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (Mai_anfani_da_kwamfuta.파일한바이트쓰기(서술자, Daraja) != 1) Kasa_aiki_Daraja("IOException: write failed");
    }
    static void Kira_tsari(int Indes, int Umarni) {
        if (Indes <= 0 || Indes >= Jurarre_tambari.length || (Jurarre_tambari[Indes] != 10 && Jurarre_tambari[Indes] != 11)) { Kasa_aiki_Daraja("invalid method reference"); return; }
        int mamallaki_Daraja = Aji_Suna_SMS(상가[Indes]), Suna = Manazarta_Suna(상나[Indes]), zubi_Daraja = Manazarta_rubuta(상나[Indes]);
        if (Kuskure) return;
        if (기본호출(mamallaki_Daraja, Suna, zubi_Daraja, Umarni)) return;
        if (Microsoft_Word_SMS(mamallaki_Daraja, "java/io/FileInputStream") || Microsoft_Word_SMS(mamallaki_Daraja, "java/io/FileOutputStream")) {
            Fayil_watsuwa_Kira(mamallaki_Daraja, Suna, zubi_Daraja, Umarni); return;
        }
        if (Umarni == 184 && Microsoft_Word_SMS(mamallaki_Daraja, "java/lang/Integer") && Microsoft_Word_SMS(Suna, "parseInt") && Microsoft_Word_SMS(zubi_Daraja, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Umarni == 182 && Microsoft_Word_SMS(mamallaki_Daraja, "java/io/PrintStream") && (Microsoft_Word_SMS(Suna, "println") || Microsoft_Word_SMS(Suna, "print"))) {
            int rubuta_Daraja = 0, Daraja = 0;
            if (Microsoft_Word_SMS(zubi_Daraja, "(I)V")) { rubuta_Daraja = 1; Daraja = 빼기(1); }
            else if (Microsoft_Word_SMS(zubi_Daraja, "(Z)V")) { rubuta_Daraja = 2; Daraja = 빼기(1); }
            else if (Microsoft_Word_SMS(zubi_Daraja, "(C)V")) { rubuta_Daraja = 3; Daraja = 빼기(1); }
            else if (Microsoft_Word_SMS(zubi_Daraja, "(Ljava/lang/String;)V")) { rubuta_Daraja = 4; Daraja = 빼기(2); }
            else if (!Microsoft_Word_SMS(zubi_Daraja, "()V") || !Microsoft_Word_SMS(Suna, "println")) Kasa_aiki_Daraja("unsupported print descriptor");
            if (빼기(2) != -1) Kasa_aiki_Daraja("invalid PrintStream receiver");
            if (Kuskure) return;
            if (rubuta_Daraja == 1) 자바도구.수쓰기(Daraja);
            if (rubuta_Daraja == 2) Mai_anfani_da_kwamfuta.Yi_Rubutu(Daraja == 0 ? "false" : "true");
            if (rubuta_Daraja == 3) Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(Daraja & 65535);
            if (rubuta_Daraja == 4) Rubuta_SMS(Daraja);
            if (Microsoft_Word_SMS(Suna, "println")) Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10);
            return;
        }
        if (Umarni == 182 && Microsoft_Word_SMS(mamallaki_Daraja, "java/lang/String")) {
            if (Microsoft_Word_SMS(Suna, "length") && Microsoft_Word_SMS(zubi_Daraja, "()I")) {
                int Manazarta = 빼기(2); if (abu_Daraja(Manazarta, 1)) 넣기(힙[Manazarta + 1], 1); return;
            }
            if (Microsoft_Word_SMS(Suna, "charAt") && Microsoft_Word_SMS(zubi_Daraja, "(I)C")) {
                int Alamar_karkashin_harafi_Daraja = 빼기(1), Manazarta = 빼기(2);
                if (abu_Daraja(Manazarta, 1)) {
                    if (Alamar_karkashin_harafi_Daraja < 0 || Alamar_karkashin_harafi_Daraja >= 힙[Manazarta + 1]) Kasa_aiki_Daraja("StringIndexOutOfBoundsException"); else 넣기(힙[Manazarta + 2 + Alamar_karkashin_harafi_Daraja], 1);
                }
                return;
            }
        }
        if (Microsoft_Word_SMS(mamallaki_Daraja, "java/lang/StringBuilder")) {
            if (Umarni == 183 && Microsoft_Word_SMS(Suna, "<init>") && Microsoft_Word_SMS(zubi_Daraja, "()V")) { abu_Daraja(빼기(2), 4); return; }
            if (Umarni == 182 && Microsoft_Word_SMS(Suna, "toString") && Microsoft_Word_SMS(zubi_Daraja, "()Ljava/lang/String;")) {
                int Manazarta = 빼기(2); if (abu_Daraja(Manazarta, 4)) 넣기(힙[Manazarta + 2] == 0 ? sauka_Harafi("") : 힙[Manazarta + 2], 2); return;
            }
            if (Umarni == 182 && Microsoft_Word_SMS(Suna, "append")) {
                int SMS = 0;
                if (Microsoft_Word_SMS(zubi_Daraja, "(I)Ljava/lang/StringBuilder;")) SMS = lamba_Harafi(빼기(1));
                else if (Microsoft_Word_SMS(zubi_Daraja, "(Z)Ljava/lang/StringBuilder;")) SMS = sauka_Harafi(빼기(1) == 0 ? "false" : "true");
                else if (Microsoft_Word_SMS(zubi_Daraja, "(C)Ljava/lang/StringBuilder;")) {
                    int Daraja = 빼기(1); SMS = kasafta_Wurin_adana(1, 1); if (!Kuskure) 힙[SMS + 2] = Daraja & 65535;
                }
                else if (Microsoft_Word_SMS(zubi_Daraja, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = sauka_Harafi("null"); }
                else { Kasa_aiki_Daraja("unsupported StringBuilder append"); return; }
                int Manazarta = 빼기(2); if (!abu_Daraja(Manazarta, 4) || !abu_Daraja(SMS, 1)) return;
                int kyamarar_gaba_Daraja = 힙[Manazarta + 2], kyamarar_gaba_Daraja_Tsawo = kyamarar_gaba_Daraja == 0 ? 0 : 힙[kyamarar_gaba_Daraja + 1], Baya_Daraja_Tsawo = 힙[SMS + 1];
                int 새글 = kasafta_Wurin_adana(1, kyamarar_gaba_Daraja_Tsawo + Baya_Daraja_Tsawo); if (Kuskure) return;
                for (int 수 = 0; 수 < kyamarar_gaba_Daraja_Tsawo; 수++) 힙[새글 + 2 + 수] = 힙[kyamarar_gaba_Daraja + 2 + 수];
                for (int 수 = 0; 수 < Baya_Daraja_Tsawo; 수++) 힙[새글 + 2 + kyamarar_gaba_Daraja_Tsawo + 수] = 힙[SMS + 2 + 수];
                힙[Manazarta + 2] = 새글; 넣기(Manazarta, 2); return;
            }
        }
        int Aji_Ma_ana = nema_Aji_Ma_ana(mamallaki_Daraja); if (Aji_Ma_ana < 0 || Kuskure) return;
        int Fayil_Indes = nema_tsari(Aji_Ma_ana, Suna, zubi_Daraja);
        if (Fayil_Indes < 0) {
            for (int Lambar_sirrin_harafi = Aji_Ma_ana, 항목수 = 0; Lambar_sirrin_harafi >= 0 && 항목수 < 16; 항목수++, Lambar_sirrin_harafi = 부모종(Lambar_sirrin_harafi))
                if (Microsoft_Word_SMS(종부모[Lambar_sirrin_harafi], "java/lang/Thread")) { 가닥호출(Suna, zubi_Daraja, Umarni); return; }
            Kasa_aiki_Daraja("NoSuchMethodError"); return;
        }
        if (((tsari_isa[Fayil_Indes] & 8) != 0) != (Umarni == 184)) { Kasa_aiki_Daraja("method static/instance mismatch"); return; }
        if (Umarni == 184) { if (!Farko(tsari_mamallaki[Fayil_Indes], allo_Sharadi[allo_Indes])) return; }
        else {
            int 읽는자리 = allo_tara[allo_Indes] - 함수인수수[Fayil_Indes];
            if (읽는자리 < 0 || 스택형[allo_Indes * 128 + 읽는자리] != 2) { Kasa_aiki_Daraja("invalid method receiver"); return; }
            int abu_Manazarta = 스택값[allo_Indes * 128 + 읽는자리];
            if (!객체유효(abu_Manazarta)) return;
            if (힙[abu_Manazarta] < 32 || !종포함(힙[abu_Manazarta] - 32, mamallaki_Daraja)) { Kasa_aiki_Daraja("method receiver type mismatch"); return; }
            if (Umarni != 183) Fayil_Indes = nema_tsari(힙[abu_Manazarta] - 32, Suna, zubi_Daraja);
        }
        if (Fayil_Indes < 0 || (tsari_isa[Fayil_Indes] & 0x400) != 0) { Kasa_aiki_Daraja("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((tsari_isa[Fayil_Indes] & 32) != 0) {
            if (Umarni == 184) { int Lambar_sirrin_harafi = tsari_mamallaki[Fayil_Indes]; if (종잠금[Lambar_sirrin_harafi] == 0) 종잠금[Lambar_sirrin_harafi] = kasafta_Wurin_adana(8, 0); 잠금참조 = 종잠금[Lambar_sirrin_harafi]; }
            else 잠금참조 = 스택값[allo_Indes * 128 + allo_tara[allo_Indes] - 함수인수수[Fayil_Indes]];
            if (!잠금얻기(잠금참조)) { if (!Kuskure) 틀위치[allo_Indes] = allo_Sharadi[allo_Indes]; return; }
        }
        호출(Fayil_Indes); if (!Kuskure) 틀잠금[allo_Indes] = 잠금참조;
    }
    static boolean 배열저장가능(int TSARI_Manazarta, int Tarin_bayani_Daraja) {
        if (Tarin_bayani_Daraja == 0 || TSARI_Dan_gutsuren_bayani[TSARI_Manazarta] == 0) return true;
        boolean 성공여부 = TSARI_Dan_gutsuren_bayani[TSARI_Manazarta] == -1 ? (Tarin_bayani_Daraja > 0 && Tarin_bayani_Daraja < 힙끝 && 힙[Tarin_bayani_Daraja] == 1) : 맞는객체(Tarin_bayani_Daraja, TSARI_Dan_gutsuren_bayani[TSARI_Manazarta]);
        if (!성공여부 && !Kuskure) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int TSARI_rami(int Manazarta, int Alamar_karkashin_harafi_Daraja, int rubuta_Daraja) {
        if (!abu_Daraja(Manazarta, rubuta_Daraja)) return 0;
        if (Alamar_karkashin_harafi_Daraja < 0 || Alamar_karkashin_harafi_Daraja >= 힙[Manazarta + 1]) { Kasa_aiki_Daraja("ArrayIndexOutOfBoundsException"); return 0; }
        return Manazarta + 2 + Alamar_karkashin_harafi_Daraja;
    }
    static void gudanar_Umarni() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Kuskure) { if (던진객체 != 0) Mariki_banbanchi(); if (Kuskure || allo_Indes < 현재가닥 * 32) break; }
            if (allo_Indes < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!Sauya_hira()) break; 조각 = 100; }
            if (allo_Indes == 0 && Aji_Ma_ana_Matsayi[Mashigar_bayanai_Aji_Ma_ana] != 2 && !Farko(Mashigar_bayanai_Aji_Ma_ana, 틀위치[allo_Indes])) continue;
            if (allo_Indes == 현재가닥 * 32 && 현재가닥 != 0 && (tsari_isa[allo_tsari[allo_Indes]] & 32) != 0 && 틀잠금[allo_Indes] == 0) {
                int abu_Manazarta = hira_tageti[현재가닥]; if (!잠금얻기(abu_Manazarta)) { if (Kuskure) break; continue; } 틀잠금[allo_Indes] = abu_Manazarta;
            }
            잠시수 = 0;
            if (--남음 == 0) { Kasa_aiki_Daraja("instruction limit (500000)"); break; }
            int Tafiyar_da = 틀위치[allo_Indes]; allo_Sharadi[allo_Indes] = Tafiyar_da; int Daraja = 명바();
            if (Kuskure) break;
            if (Daraja == 0) continue;
            if (Daraja == 1) { 넣기(0, 2); continue; }
            if (Daraja >= 2 && Daraja <= 8) { 넣기(Daraja - 3, 1); continue; }
            if (Daraja == 16) { 넣기((byte)명바(), 1); continue; }
            if (Daraja == 17) { 넣기((short)명짧(), 1); continue; }
            if (Daraja == 18 || Daraja == 19) {
                int 수 = tsari_mamallaki[allo_tsari[allo_Indes]] * 512 + (Daraja == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= Jurarre_tambari.length) Kasa_aiki_Daraja("invalid ldc constant");
                else if (Jurarre_tambari[수] == 3) 넣기(상가[수], 1);
                else if (Jurarre_tambari[수] == 8) 넣기(Jurarre_SMS(상가[수]), 2);
                else Kasa_aiki_Daraja("unsupported ldc constant");
                continue;
            }
            if (Daraja == 21 || Daraja == 25) { 지역읽기(명바(), Daraja == 21 ? 1 : 2); continue; }
            if (Daraja >= 26 && Daraja <= 29) { 지역읽기(Daraja - 26, 1); continue; }
            if (Daraja >= 42 && Daraja <= 45) { 지역읽기(Daraja - 42, 2); continue; }
            if (Daraja == 54 || Daraja == 58) { Rubuta_na_gida(명바(), Daraja == 54 ? 1 : 2); continue; }
            if (Daraja >= 59 && Daraja <= 62) { Rubuta_na_gida(Daraja - 59, 1); continue; }
            if (Daraja >= 75 && Daraja <= 78) { Rubuta_na_gida(Daraja - 75, 2); continue; }
            if (Daraja == 46 || Daraja >= 50 && Daraja <= 53) {
                int 항목자리 = 빼기(1), abu_Manazarta = 빼기(2), ɓangare_lambar_sirri = Daraja == 46 ? 2 : Daraja == 50 ? 3 : Daraja == 51 ? 20 : Daraja == 52 ? 22 : 23;
                if (Daraja == 51 && abu_Manazarta > 0 && abu_Manazarta < 힙끝 && 힙[abu_Manazarta] == 21) ɓangare_lambar_sirri = 21;
                int 읽는자리 = TSARI_rami(abu_Manazarta, 항목자리, ɓangare_lambar_sirri); if (!Kuskure) 넣기(힙[읽는자리], Daraja == 50 ? 2 : 1); continue;
            }
            if (Daraja == 79 || Daraja >= 83 && Daraja <= 86) {
                int Mashigar_bayanai_Manazarta = 빼기(Daraja == 83 ? 2 : 1), 항목자리 = 빼기(1), abu_Manazarta = 빼기(2), ɓangare_lambar_sirri = Daraja == 79 ? 2 : Daraja == 83 ? 3 : Daraja == 84 ? 20 : Daraja == 85 ? 22 : 23;
                if (Daraja == 84 && abu_Manazarta > 0 && abu_Manazarta < 힙끝 && 힙[abu_Manazarta] == 21) ɓangare_lambar_sirri = 21;
                int 읽는자리 = TSARI_rami(abu_Manazarta, 항목자리, ɓangare_lambar_sirri);
                if (!Kuskure && ɓangare_lambar_sirri == 3 && !배열저장가능(abu_Manazarta, Mashigar_bayanai_Manazarta)) continue;
                if (!Kuskure) 힙[읽는자리] = ɓangare_lambar_sirri == 20 ? (byte)Mashigar_bayanai_Manazarta : ɓangare_lambar_sirri == 21 ? Mashigar_bayanai_Manazarta & 1 : ɓangare_lambar_sirri == 22 ? (char)Mashigar_bayanai_Manazarta : ɓangare_lambar_sirri == 23 ? (short)Mashigar_bayanai_Manazarta : Mashigar_bayanai_Manazarta;
                continue;
            }
            if (Daraja >= 87 && Daraja <= 95) { tara_Sharadi(Daraja); continue; }
            if (Daraja == 96 || Daraja == 100 || Daraja == 104 || Daraja == 108 || Daraja == 112 || Daraja == 120
                || Daraja == 122 || Daraja == 124 || Daraja == 126 || Daraja == 128 || Daraja == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((Daraja == 108 || Daraja == 112) && 나 == 0) { Kasa_aiki_Daraja("ArithmeticException: / by zero"); continue; }
                if (Daraja == 96) 결과 = 가 + 나;
                if (Daraja == 100) 결과 = 가 - 나;
                if (Daraja == 104) 결과 = 가 * 나;
                if (Daraja == 108) 결과 = 가 / 나;
                if (Daraja == 112) 결과 = 가 % 나;
                if (Daraja == 120) 결과 = 가 << 나;
                if (Daraja == 122) 결과 = 가 >> 나;
                if (Daraja == 124) 결과 = 가 >>> 나;
                if (Daraja == 126) 결과 = 가 & 나;
                if (Daraja == 128) 결과 = 가 | 나;
                if (Daraja == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (Daraja == 116) { 넣기(-빼기(1), 1); continue; }
            if (Daraja == 132) {
                int na_gida_Kima = 명바(), 증분 = (byte)명바(); 지역읽기(na_gida_Kima, 1); 넣기(빼기(1) + 증분, 1); Rubuta_na_gida(na_gida_Kima, 1); continue;
            }
            if (Daraja >= 145 && Daraja <= 147) {
                int 수 = 빼기(1); 넣기(Daraja == 145 ? (byte)수 : Daraja == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (Daraja >= 153 && Daraja <= 167 || Daraja == 198 || Daraja == 199) {
                int Zangon_ƙarshe_Daraja = Tafiyar_da + (short)명짧(); boolean 갈까 = Daraja == 167;
                if (Daraja >= 153 && Daraja <= 158) {
                    int 수 = 빼기(1); 갈까 = Daraja == 153 ? 수 == 0 : Daraja == 154 ? 수 != 0 : Daraja == 155 ? 수 < 0 : Daraja == 156 ? 수 >= 0 : Daraja == 157 ? 수 > 0 : 수 <= 0;
                } else if (Daraja >= 159 && Daraja <= 166) {
                    int 나 = 빼기(Daraja >= 165 ? 2 : 1), 가 = 빼기(Daraja >= 165 ? 2 : 1);
                    갈까 = Daraja == 159 || Daraja == 165 ? 가 == 나 : Daraja == 160 || Daraja == 166 ? 가 != 나 : Daraja == 161 ? 가 < 나 : Daraja == 162 ? 가 >= 나 : Daraja == 163 ? 가 > 나 : 가 <= 나;
                } else if (Daraja == 198 || Daraja == 199) { int 수 = 빼기(2); 갈까 = Daraja == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) Matsar_da_Daraja(Zangon_ƙarshe_Daraja); continue;
            }
            if (Daraja == 172 || Daraja == 176 || Daraja == 177) { 반환(Daraja == 172 ? 1 : Daraja == 176 ? 2 : 0); continue; }
            if (Daraja >= 178 && Daraja <= 181) { 필드호출(명상수(), Daraja, Tafiyar_da); continue; }
            if (Daraja >= 182 && Daraja <= 185) {
                int 부호값 = 명상수();
                if (Daraja == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { Kasa_aiki_Daraja("invalid invokeinterface operands"); continue; } }
                Kira_tsari(부호값, Daraja); continue;
            }
            if (Daraja == 187) { 새객체(Aji_Suna_SMS(명상수()), Tafiyar_da); continue; }
            if (Daraja == 188 || Daraja == 189) {
                int ɓangare_lambar_sirri = 3, Ƙunshiyar_na_urori = 0;
                if (Daraja == 188) { int 임시값 = 명바(); ɓangare_lambar_sirri = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else Ƙunshiyar_na_urori = Aji_Suna_SMS(명상수());
                if (ɓangare_lambar_sirri == 0) { Kasa_aiki_Daraja("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), abu_Manazarta = kasafta_Wurin_adana(ɓangare_lambar_sirri, 유효길이); if (!Kuskure) TSARI_Dan_gutsuren_bayani[abu_Manazarta] = Ƙunshiyar_na_urori; 넣기(abu_Manazarta, 2); continue;
            }
            if (Daraja == 190) {
                int abu_Manazarta = 빼기(2);
                if (객체유효(abu_Manazarta)) { int 비교자리 = 힙[abu_Manazarta]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) Kasa_aiki_Daraja("not an array"); else 넣기(힙[abu_Manazarta + 1], 1); }
                continue;
            }
            if (Daraja == 191) {
                int abu_Manazarta = 빼기(2); if (객체유효(abu_Manazarta)) { if (힙[abu_Manazarta] != 9) Kasa_aiki_Daraja("athrow requires supported Throwable"); else { 던진객체 = abu_Manazarta; Kuskure = true; } }
                continue;
            }
            if (Daraja == 192 || Daraja == 193) {
                int Suna_Jurarre = Aji_Suna_SMS(명상수()), abu_Manazarta = 빼기(2); boolean 일치여부 = 맞는객체(abu_Manazarta, Suna_Jurarre);
                if (Daraja == 193) 넣기(abu_Manazarta != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !Kuskure) Kasa_aiki_Daraja("ClassCastException"); 넣기(abu_Manazarta, 2); }
                continue;
            }
            if (Daraja == 170 || Daraja == 171) {
                int 읽는자리 = Tafiyar_da + 1, Fayil_Indes = allo_tsari[allo_Indes], Makulli_Manazarta = 빼기(1);
                while ((읽는자리 - tsari_Fara[Fayil_Indes]) % 4 != 0) 읽는자리++;
                int tageti_imel = 위치정수(읽는자리);
                if (Daraja == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (Makulli_Manazarta >= 낮은값 && Makulli_Manazarta <= 높은값) tageti_imel = 위치정수(읽는자리 + 12 + (Makulli_Manazarta - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int Warware_Indes = 0; Warware_Indes < 총수; Warware_Indes++) if (위치정수(읽는자리 + 8 + Warware_Indes * 8) == Makulli_Manazarta) tageti_imel = 위치정수(읽는자리 + 12 + Warware_Indes * 8); }
                Matsar_da_Daraja(Tafiyar_da + tageti_imel); continue;
            }
            if (Daraja == 200) { Matsar_da_Daraja(Tafiyar_da + 위치정수(Tafiyar_da + 1)); continue; }
            if (Daraja == 194 || Daraja == 195) {
                int abu_Manazarta = 빼기(2);
                if (Daraja == 195) 잠금풀기(abu_Manazarta);
                else if (!잠금얻기(abu_Manazarta) && !Kuskure) { 넣기(abu_Manazarta, 2); 틀위치[allo_Indes] = Tafiyar_da; }
                continue;
            }
            if (Daraja == 196) {
                int Umarni_lambar_sirri = 명바(), 항목자리 = 명짧();
                if (Umarni_lambar_sirri == 21 || Umarni_lambar_sirri == 25) 지역읽기(항목자리, Umarni_lambar_sirri == 21 ? 1 : 2);
                else if (Umarni_lambar_sirri == 54 || Umarni_lambar_sirri == 58) Rubuta_na_gida(항목자리, Umarni_lambar_sirri == 54 ? 1 : 2);
                else if (Umarni_lambar_sirri == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); Rubuta_na_gida(항목자리, 1); }
                else Kasa_aiki_Daraja("unsupported wide opcode");
                continue;
            }
            Kasa_aiki_Daraja("unsupported bytecode");
        }
    }
    static int nema_Aji_Ma_ana(int Suna) {
        for (int Warware_Indes = 0; Warware_Indes < 종수; Warware_Indes++) if (Aji_Ma_ana_Suna[Warware_Indes] != 0 && 같은말(Aji_Ma_ana_Suna[Warware_Indes], Suna)) return Warware_Indes;
        return loda_Aji_Ma_ana(Jurarre_SMS(Suna));
    }
    static int loda_Aji_Ma_ana(int Suna_Zare) {
        if (!abu_Daraja(Suna_Zare, 1)) return -1;
        int Tsawo_Daraja = 힙[Suna_Zare + 1];
        if (Tsawo_Daraja < 1 || Tsawo_Daraja > 505 || 종수 == 16) { Kasa_aiki_Daraja("class name/count limit"); return -1; }
        for (int Warware_Indes = 0; Warware_Indes < Tsawo_Daraja; Warware_Indes++) { int Lambar_sirrin_harafi = 힙[Suna_Zare + 2 + Warware_Indes]; Fayil_Suna_SMS[Warware_Indes] = Lambar_sirrin_harafi == '/' ? '.' : Lambar_sirrin_harafi; }
        Fayil_Suna_SMS[Tsawo_Daraja] = '.'; Fayil_Suna_SMS[Tsawo_Daraja + 1] = 'c'; Fayil_Suna_SMS[Tsawo_Daraja + 2] = 'l'; Fayil_Suna_SMS[Tsawo_Daraja + 3] = 'a'; Fayil_Suna_SMS[Tsawo_Daraja + 4] = 's'; Fayil_Suna_SMS[Tsawo_Daraja + 5] = 's'; Fayil_Suna_SMS[Tsawo_Daraja + 6] = 0;
        int Girma = Mai_anfani_da_kwamfuta.파일읽기(Fayil_Suna_SMS, 임시파일);
        if (Girma < 0) { Kasa_aiki_Daraja("ClassNotFoundException"); return -1; }
        int Aji_Ma_ana = 종수++; Aji_Ma_ana_girma[Aji_Ma_ana] = Girma;
        for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) Fayil[Aji_Ma_ana * 16384 + Warware_Indes] = 임시파일[Warware_Indes];
        클래스읽기(Aji_Ma_ana); if (Kuskure) return -1;
        int Na_hakika_Tarin_bayani = Jurarre_SMS(Aji_Ma_ana_Suna[Aji_Ma_ana]);
        if (!글같음(Na_hakika_Tarin_bayani, Suna_Zare, true)) { Kasa_aiki_Daraja("class name does not match file"); return -1; }
        int 부모 = 종부모[Aji_Ma_ana];
        if (부모 != 0 && !Microsoft_Word_SMS(부모, "java/lang/Object") && !Microsoft_Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = nema_Aji_Ma_ana(부모);
            if (Kuskure || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == Aji_Ma_ana) { Kasa_aiki_Daraja("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Fayil_Indes = 0; Fayil_Indes < 칸수; Fayil_Indes++) if (rami_mamallaki[Fayil_Indes] == Aji_Ma_ana && (rami_Izini[Fayil_Indes] & 8) == 0) 칸위치[Fayil_Indes] += 시작변위;
            종칸수[Aji_Ma_ana] += 시작변위;
        }
        return Aji_Ma_ana;
    }
    static int 부모종(int Aji_Ma_ana) {
        int Suna = 종부모[Aji_Ma_ana];
        for (int Warware_Indes = 0; Warware_Indes < 종수; Warware_Indes++) if (Suna != 0 && Aji_Ma_ana_Suna[Warware_Indes] != 0 && 같은말(Aji_Ma_ana_Suna[Warware_Indes], Suna)) return Warware_Indes;
        return -1;
    }
    static int nema_tsari(int Aji_Ma_ana, int Suna, int zubi_Daraja) {
        for (int 깊이 = 0; Aji_Ma_ana >= 0 && 깊이 < 16; 깊이++, Aji_Ma_ana = 부모종(Aji_Ma_ana)) {
            for (int Warware_Indes = 0; Warware_Indes < 함수수; Warware_Indes++) if (tsari_mamallaki[Warware_Indes] == Aji_Ma_ana && 같은말(tsari_Suna_SMS[Warware_Indes], Suna) && 같은말(tsari_rubuta[Warware_Indes], zubi_Daraja)) return Warware_Indes;
        }
        return -1;
    }
    static int Suna_tsari(int Aji_Ma_ana, String Suna, String zubi_Daraja) {
        for (int 깊이 = 0; Aji_Ma_ana >= 0 && 깊이 < 16; 깊이++, Aji_Ma_ana = 부모종(Aji_Ma_ana))
            for (int Warware_Indes = 0; Warware_Indes < 함수수; Warware_Indes++) if (tsari_mamallaki[Warware_Indes] == Aji_Ma_ana && Microsoft_Word_SMS(tsari_Suna_SMS[Warware_Indes], Suna) && Microsoft_Word_SMS(tsari_rubuta[Warware_Indes], zubi_Daraja)) return Warware_Indes;
        return -1;
    }
    static int 형종류(int Suna) { return Fayil[상가[Suna]] == 'L' || Fayil[상가[Suna]] == '[' ? 2 : 1; }
    static boolean Farko(int Aji_Ma_ana, int Umarni_Fara) {
        if (Aji_Ma_ana < 0 || Kuskure) return false;
        if (Aji_Ma_ana_Matsayi[Aji_Ma_ana] == 3) { Kasa_aiki_Daraja("NoClassDefFoundError: initialization failed"); return false; }
        if (Aji_Ma_ana_Matsayi[Aji_Ma_ana] == 1 && Aji_hira[Aji_Ma_ana] != 현재가닥) { 틀위치[allo_Indes] = Umarni_Fara; 바꿈요청 = true; return false; }
        if (Aji_Ma_ana_Matsayi[Aji_Ma_ana] != 0) return true;
        int 위 = 부모종(Aji_Ma_ana);
        if (위 >= 0 && !Farko(위, Umarni_Fara)) return false;
        Aji_Ma_ana_Matsayi[Aji_Ma_ana] = 1; Aji_hira[Aji_Ma_ana] = 현재가닥;
        if (Farko_Aji_Ma_ana[Aji_Ma_ana] != 0) {
            틀위치[allo_Indes] = Umarni_Fara;
            호출(Farko_Aji_Ma_ana[Aji_Ma_ana] - 1); if (!Kuskure) Farko_allo[allo_Indes] = Aji_Ma_ana + 1;
            return false;
        }
        Aji_Ma_ana_Matsayi[Aji_Ma_ana] = 2; return true;
    }
    static void 필드호출(int Indes, int Umarni, int Tafiyar_da) {
        if (!Bincika_Jurarre(Indes, 9)) return;
        int mamallaki_Daraja = Aji_Suna_SMS(상가[Indes]), Suna = Manazarta_Suna(상나[Indes]), zubi_Daraja = Manazarta_rubuta(상나[Indes]);
        if (Microsoft_Word_SMS(mamallaki_Daraja, "java/lang/System") && (Microsoft_Word_SMS(Suna, "out") || Microsoft_Word_SMS(Suna, "err")) && Microsoft_Word_SMS(zubi_Daraja, "Ljava/io/PrintStream;") && Umarni == 178) { 넣기(-1, 2); return; }
        int Aji_Ma_ana = nema_Aji_Ma_ana(mamallaki_Daraja); if (Aji_Ma_ana < 0 || Kuskure) return;
        int 찾음 = -1;
        for (int 읽는자리 = Aji_Ma_ana, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int Fayil_Indes = 0; Fayil_Indes < 칸수; Fayil_Indes++) if (rami_mamallaki[Fayil_Indes] == 읽는자리 && 같은말(rami_Suna[Fayil_Indes], Suna) && 같은말(rami_rubuta[Fayil_Indes], zubi_Daraja)) 찾음 = Fayil_Indes;
        if (찾음 < 0) { Kasa_aiki_Daraja("NoSuchFieldError"); return; }
        boolean Tsaye_cik_Daraja = Umarni == 178 || Umarni == 179;
        if (Tsaye_cik_Daraja != ((rami_Izini[찾음] & 8) != 0)) { Kasa_aiki_Daraja("field static/instance mismatch"); return; }
        if (Tsaye_cik_Daraja && !Farko(rami_mamallaki[찾음], Tafiyar_da)) return;
        int rubuta_Daraja = 형종류(zubi_Daraja), Daraja = 0;
        if (Umarni == 179 || Umarni == 181) Daraja = 빼기(rubuta_Daraja);
        if (Tsaye_cik_Daraja) { if (Umarni == 178) 넣기(rami_Tarin_bayani[찾음], rubuta_Daraja); else if (!Kuskure) rami_Tarin_bayani[찾음] = Daraja; return; }
        int abu_Manazarta = 빼기(2);
        if (!객체유효(abu_Manazarta)) return;
        if (힙[abu_Manazarta] < 32 || !종포함(힙[abu_Manazarta] - 32, mamallaki_Daraja)) { Kasa_aiki_Daraja("field receiver type mismatch"); return; }
        int 보관칸 = abu_Manazarta + 2 + 칸위치[찾음];
        if (Umarni == 180) 넣기(힙[보관칸], rubuta_Daraja);
        else if (!Kuskure) { 힙[보관칸] = Daraja; 힙참조[보관칸] = rubuta_Daraja == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Aji_Ma_ana, int Suna) {
        for (int 중첩깊이 = 0; Aji_Ma_ana >= 0 && 중첩깊이 < 16; 중첩깊이++, Aji_Ma_ana = 부모종(Aji_Ma_ana)) {
            if (같은말(Aji_Ma_ana_Suna[Aji_Ma_ana], Suna) || (종부모[Aji_Ma_ana] != 0 && 같은말(종부모[Aji_Ma_ana], Suna))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[Aji_Ma_ana]; 안쪽자리++) if (같은말(Aji_Farfajiya[Aji_Ma_ana * 16 + 안쪽자리], Suna)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bayit_Tarin_bayani, boolean Hanyar_shiga) {
        if (첫값 == bayit_Tarin_bayani) return true;
        if (첫값 <= 0 || bayit_Tarin_bayani <= 0 || 힙[첫값] != 1 || 힙[bayit_Tarin_bayani] != 1 || 힙[첫값 + 1] != 힙[bayit_Tarin_bayani + 1]) return false;
        for (int Warware_Indes = 0; Warware_Indes < 힙[첫값 + 1]; Warware_Indes++) {
            int gamayyar_x = 힙[첫값 + 2 + Warware_Indes], Maɓallin_Y_Mai_tsarawa = 힙[bayit_Tarin_bayani + 2 + Warware_Indes];
            if (Hanyar_shiga) { if (gamayyar_x == '.') gamayyar_x = '/'; if (Maɓallin_Y_Mai_tsarawa == '.') Maɓallin_Y_Mai_tsarawa = '/'; }
            if (gamayyar_x != Maɓallin_Y_Mai_tsarawa) return false;
        }
        return true;
    }
    static boolean 객체유효(int abu_Manazarta) {
        if (abu_Manazarta == 0) { Kasa_aiki_Daraja("NullPointerException"); return false; }
        if (abu_Manazarta < 1 || abu_Manazarta >= 힙끝 || 힙폭[abu_Manazarta] < 2 || 힙[abu_Manazarta] == 0) { Kasa_aiki_Daraja("invalid object reference"); return false; }
        return true;
    }
    static void Kare_Daraja(int abu_Manazarta) {
        if (abu_Manazarta > 0 && abu_Manazarta < 힙끝 && 힙폭[abu_Manazarta] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = abu_Manazarta;
    }
    static void Nuna_Daraja(int abu_Manazarta) {
        if (abu_Manazarta > 0 && abu_Manazarta < 힙끝 && 힙폭[abu_Manazarta] >= 2 && 힙[abu_Manazarta] != 0 && 힙표시[abu_Manazarta] == 0) {
            힙표시[abu_Manazarta] = 1; 표시대기[표시수++] = abu_Manazarta;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int Warware_Indes = 0; Warware_Indes < Zare_Manazarta.length; Warware_Indes++) Nuna_Daraja(Zare_Manazarta[Warware_Indes]);
        for (int Warware_Indes = 0; Warware_Indes < 칸수; Warware_Indes++) if ((rami_Izini[Warware_Indes] & 8) != 0 && 형종류(rami_rubuta[Warware_Indes]) == 2) Nuna_Daraja(rami_Tarin_bayani[Warware_Indes]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            Nuna_Daraja(hira_abu[임시값]); Nuna_Daraja(hira_tageti[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? allo_Indes : hira_allo[임시값];
            for (int Fayil_Indes = 임시값 * 32; Fayil_Indes <= 꼭대기자리; Fayil_Indes++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[allo_tsari[Fayil_Indes]]; 안쪽자리++) if (na_gida_rubuta[Fayil_Indes * 128 + 안쪽자리] == 2) Nuna_Daraja(na_gida_Daraja[Fayil_Indes * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < allo_tara[Fayil_Indes]; 안쪽자리++) if (스택형[Fayil_Indes * 128 + 안쪽자리] == 2) Nuna_Daraja(스택값[Fayil_Indes * 128 + 안쪽자리]);
            }
        }
        for (int Warware_Indes = 0; Warware_Indes < 화면참조.length; Warware_Indes++) Nuna_Daraja(화면참조[Warware_Indes]);
        for (int Warware_Indes = 0; Warware_Indes < 나중수; Warware_Indes++) Nuna_Daraja(나중실행[Warware_Indes]);
        for (int Warware_Indes = 0; Warware_Indes < Ajiye_Lamba_mara.length; Warware_Indes++) Nuna_Daraja(Ajiye_Lamba_mara[Warware_Indes]);
        for (int Warware_Indes = 0; Warware_Indes < 종수; Warware_Indes++) Nuna_Daraja(종잠금[Warware_Indes]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) Nuna_Daraja(검사자리);
        Nuna_Daraja(던진객체);
        for (int Warware_Indes = 0; Warware_Indes < 잠시수; Warware_Indes++) Nuna_Daraja(잠시참조[Warware_Indes]);
        while (표시수 > 0) {
            int abu_Manazarta = 표시대기[--표시수], ɓangare_lambar_sirri = 힙[abu_Manazarta];
            for (int Warware_Indes = abu_Manazarta + 2; Warware_Indes < abu_Manazarta + 힙폭[abu_Manazarta]; Warware_Indes++) if (ɓangare_lambar_sirri == 3 || ɓangare_lambar_sirri == 4 || 힙참조[Warware_Indes] != 0) Nuna_Daraja(힙[Warware_Indes]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int Tsawo_Daraja) {
        if (Tsawo_Daraja < 0) { Kasa_aiki_Daraja("NegativeArraySizeException"); return 0; }
        if (Tsawo_Daraja > 힙.length - 3) { Kasa_aiki_Daraja("object heap exhausted"); return 0; }
        int 필요수 = Tsawo_Daraja + 2, abu_Manazarta = 0;
        if (필요수 <= 힙.length - 힙끝) { abu_Manazarta = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { abu_Manazarta = 읽는자리; break; }
            if (abu_Manazarta != 0) {
                int 남은길이 = 힙폭[abu_Manazarta] - 필요수;
                if (남은길이 >= 2) { 힙폭[abu_Manazarta + 필요수] = 남은길이; 힙[abu_Manazarta + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { abu_Manazarta = 힙끝; 힙끝 += 필요수; }
        }
        if (abu_Manazarta == 0) { Kasa_aiki_Daraja("object heap exhausted"); return 0; }
        for (int Warware_Indes = 0; Warware_Indes < 필요수; Warware_Indes++) { 힙[abu_Manazarta + Warware_Indes] = 0; 힙참조[abu_Manazarta + Warware_Indes] = 0; 힙폭[abu_Manazarta + Warware_Indes] = 0; }
        TSARI_Dan_gutsuren_bayani[abu_Manazarta] = 0;
        힙폭[abu_Manazarta] = 필요수; 힙[abu_Manazarta] = 종류; 힙[abu_Manazarta + 1] = Tsawo_Daraja; Kare_Daraja(abu_Manazarta); return abu_Manazarta;
    }
    static int banbanchi_Aji(String Suna_Jurarre) {
        if (자바도구.같음(Suna_Jurarre, "java/lang/Throwable")) return 1;
        if (자바도구.같음(Suna_Jurarre, "java/lang/Exception")) return 2;
        if (자바도구.같음(Suna_Jurarre, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(Suna_Jurarre, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(Suna_Jurarre, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(Suna_Jurarre, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(Suna_Jurarre, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(Suna_Jurarre, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(Suna_Jurarre, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(Suna_Jurarre, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(Suna_Jurarre, "java/io/IOException")) return 11;
        if (자바도구.같음(Suna_Jurarre, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(Suna_Jurarre, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(Suna_Jurarre, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(Suna_Jurarre, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int banbanchi_Jurarre(int Suna) {
        for (int Warware_Indes = 1; Warware_Indes <= 41; Warware_Indes++) if (Microsoft_Word_SMS(Suna, banbanchi_Suna(Warware_Indes))) return Warware_Indes;
        return 0;
    }
    static String banbanchi_Suna(int asusu_Daraja) {
        if (asusu_Daraja == 40) return "java/lang/InterruptedException";
        if (asusu_Daraja == 41) return "한국어/자체/대기중단예외";
        if (asusu_Daraja == 39) return "java/net/SocketException";
        if (asusu_Daraja == 20) return "한국어/자체/banbanchi";
        if (asusu_Daraja == 21) return "한국어/자체/실행예외";
        if (asusu_Daraja == 22) return "한국어/자체/I_O_banbanchi";
        if (asusu_Daraja == 23) return "한국어/자체/대기시간초과예외";
        if (asusu_Daraja == 24) return "한국어/자체/주소확인예외";
        if (asusu_Daraja == 25) return "한국어/자체/파일없음예외";
        if (asusu_Daraja == 26) return "한국어/자체/통신예외";
        if (asusu_Daraja == 27) return "한국어/자체/mara_ƙarfi_Tubalin_aiki_banbanchi";
        if (asusu_Daraja == 28) return "한국어/자체/숫자형식예외";
        if (asusu_Daraja == 29) return "한국어/자체/범위예외";
        if (asusu_Daraja == 30) return "한국어/자체/배열범위예외";
        if (asusu_Daraja == 31) return "한국어/자체/문자열범위예외";
        if (asusu_Daraja == 32) return "한국어/자체/Sokakke_Manazarta_banbanchi";
        if (asusu_Daraja == 33) return "한국어/자체/산술예외";
        if (asusu_Daraja == 34) return "한국어/자체/Matsayi_banbanchi";
        if (asusu_Daraja == 35) return "한국어/자체/rubuta_watsa_banbanchi";
        if (asusu_Daraja == 36) return "한국어/자체/음수배열크기예외";
        if (asusu_Daraja == 37) return "한국어/자체/TSARI_Ajiye_Kasa_aiki";
        if (asusu_Daraja == 38) return "한국어/자체/hira_Matsayi_banbanchi";
        if (asusu_Daraja == 1) return "java/lang/Throwable"; if (asusu_Daraja == 2) return "java/lang/Exception";
        if (asusu_Daraja == 3) return "java/lang/RuntimeException"; if (asusu_Daraja == 4) return "java/lang/ArithmeticException";
        if (asusu_Daraja == 5) return "java/lang/NullPointerException"; if (asusu_Daraja == 6) return "java/lang/IndexOutOfBoundsException";
        if (asusu_Daraja == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (asusu_Daraja == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (asusu_Daraja == 9) return "java/lang/IllegalArgumentException"; if (asusu_Daraja == 10) return "java/lang/NumberFormatException";
        if (asusu_Daraja == 11) return "java/io/IOException"; if (asusu_Daraja == 12) return "java/io/FileNotFoundException";
        if (asusu_Daraja == 17) return "java/lang/ArrayStoreException";
        if (asusu_Daraja == 18) return "java/net/UnknownHostException";
        if (asusu_Daraja == 19) return "java/net/SocketTimeoutException";
        if (asusu_Daraja == 16) return "java/lang/IllegalThreadStateException";
        if (asusu_Daraja == 13) return "java/lang/IllegalStateException"; if (asusu_Daraja == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int asusu_Daraja) {
        if (asusu_Daraja == 40) return 2;
        if (asusu_Daraja == 41) return 40;
        if (asusu_Daraja == 39) return 11;
        if (asusu_Daraja == 1) return 0;
        if (asusu_Daraja == 2) return 1;
        if (asusu_Daraja == 3) return 2;
        if (asusu_Daraja == 4) return 3;
        if (asusu_Daraja == 5) return 3;
        if (asusu_Daraja == 6) return 3;
        if (asusu_Daraja == 7) return 6;
        if (asusu_Daraja == 8) return 6;
        if (asusu_Daraja == 9) return 3;
        if (asusu_Daraja == 10) return 9;
        if (asusu_Daraja == 11) return 2;
        if (asusu_Daraja == 12) return 11;
        if (asusu_Daraja == 13) return 3;
        if (asusu_Daraja == 14) return 3;
        if (asusu_Daraja == 15) return 3;
        if (asusu_Daraja == 16) return 9;
        if (asusu_Daraja == 17) return 3;
        if (asusu_Daraja == 18) return 11;
        if (asusu_Daraja == 19) return 11;
        if (asusu_Daraja == 20) return 2;
        if (asusu_Daraja == 21) return 3;
        if (asusu_Daraja == 22) return 11;
        if (asusu_Daraja == 23) return 22;
        if (asusu_Daraja == 24) return 22;
        if (asusu_Daraja == 25) return 22;
        if (asusu_Daraja == 26) return 22;
        if (asusu_Daraja == 27) return 9;
        if (asusu_Daraja == 28) return 27;
        if (asusu_Daraja == 29) return 6;
        if (asusu_Daraja == 30) return 29;
        if (asusu_Daraja == 31) return 29;
        if (asusu_Daraja == 32) return 5;
        if (asusu_Daraja == 33) return 4;
        if (asusu_Daraja == 34) return 13;
        if (asusu_Daraja == 35) return 14;
        if (asusu_Daraja == 36) return 15;
        if (asusu_Daraja == 37) return 17;
        if (asusu_Daraja == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int Na_hakika_Daraja, int 요구값) {
        for (int 깊이 = 0; Na_hakika_Daraja != 0 && 깊이 < 16; 깊이++, Na_hakika_Daraja = 예외부모(Na_hakika_Daraja))
            if (Na_hakika_Daraja == 요구값) return true;
        return false;
    }
    static void 예외던짐(int asusu_Daraja, String README_Manazarta) {
        int abu_Manazarta = 새기억(9, 2); if (Kuskure) return;
        힙[abu_Manazarta + 2] = asusu_Daraja; 힙[abu_Manazarta + 3] = sauka_Harafi(README_Manazarta); 힙참조[abu_Manazarta + 3] = 1;
        던진객체 = abu_Manazarta; Kuskure = true;
    }
    static boolean 맞는객체(int abu_Manazarta, int Suna) {
        if (abu_Manazarta == 0) return true;
        if (!객체유효(abu_Manazarta)) return false;
        int ɓangare_lambar_sirri = 힙[abu_Manazarta];
        if (Microsoft_Word_SMS(Suna, "java/lang/Object")) return true;
        if (ɓangare_lambar_sirri >= 32) return 종포함(ɓangare_lambar_sirri - 32, Suna);
        if (ɓangare_lambar_sirri == 9) { int tageti_imel = banbanchi_Jurarre(Suna); return tageti_imel != 0 && 예외포함(힙[abu_Manazarta + 2], tageti_imel); }
        if (ɓangare_lambar_sirri == 1) return Microsoft_Word_SMS(Suna, "java/lang/String") || Microsoft_Word_SMS(Suna, "java/lang/CharSequence");
        if (ɓangare_lambar_sirri == 4) return Microsoft_Word_SMS(Suna, "java/lang/StringBuilder") || Microsoft_Word_SMS(Suna, "java/lang/CharSequence");
        if (ɓangare_lambar_sirri == 10) return Microsoft_Word_SMS(Suna, "java/util/ArrayList") || Microsoft_Word_SMS(Suna, "java/util/List");
        if (ɓangare_lambar_sirri == 11) return Microsoft_Word_SMS(Suna, "java/util/HashMap") || Microsoft_Word_SMS(Suna, "java/util/Map");
        if (ɓangare_lambar_sirri == 12) return Microsoft_Word_SMS(Suna, "java/lang/Integer") || Microsoft_Word_SMS(Suna, "java/lang/Number");
        if (ɓangare_lambar_sirri >= 24 && ɓangare_lambar_sirri <= 28 && 힙[abu_Manazarta + 13] != 0) return 한국어화면종(Suna) == ɓangare_lambar_sirri || Microsoft_Word_SMS(Suna, "한국어/자체/화면구성요소");
        if (ɓangare_lambar_sirri >= 24 && ɓangare_lambar_sirri <= 28) return (한국어화면종(Suna) == 0 && 화면종(Suna) == ɓangare_lambar_sirri) || Microsoft_Word_SMS(Suna, "java/awt/Component") || Microsoft_Word_SMS(Suna, "java/awt/Container") || Microsoft_Word_SMS(Suna, "javax/swing/JComponent");
        if (ɓangare_lambar_sirri == 29) return Microsoft_Word_SMS(Suna, 힙[abu_Manazarta + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (ɓangare_lambar_sirri == 30) return Microsoft_Word_SMS(Suna, "java/awt/FlowLayout") || Microsoft_Word_SMS(Suna, "java/awt/LayoutManager");
        if (ɓangare_lambar_sirri == 17) return Microsoft_Word_SMS(Suna, "java/net/Socket");
        if (ɓangare_lambar_sirri == 18) return Microsoft_Word_SMS(Suna, "java/net/ServerSocket");
        if (ɓangare_lambar_sirri == 19) return Microsoft_Word_SMS(Suna, 힙[abu_Manazarta + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (ɓangare_lambar_sirri == 14) return Microsoft_Word_SMS(Suna, "java/net/InetAddress");
        if (ɓangare_lambar_sirri == 15) return Microsoft_Word_SMS(Suna, "java/net/DatagramSocket");
        if (ɓangare_lambar_sirri == 16) return Microsoft_Word_SMS(Suna, "java/net/DatagramPacket");
        if (ɓangare_lambar_sirri == 13) return Microsoft_Word_SMS(Suna, 힙[abu_Manazarta + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (ɓangare_lambar_sirri == 2) return Microsoft_Word_SMS(Suna, "[I"); if (ɓangare_lambar_sirri == 20) return Microsoft_Word_SMS(Suna, "[B"); if (ɓangare_lambar_sirri == 21) return Microsoft_Word_SMS(Suna, "[Z");
        if (ɓangare_lambar_sirri == 22) return Microsoft_Word_SMS(Suna, "[C"); if (ɓangare_lambar_sirri == 23) return Microsoft_Word_SMS(Suna, "[S");
        if (ɓangare_lambar_sirri != 3) return false;
        if (Microsoft_Word_SMS(Suna, "[Ljava/lang/Object;")) return true;
        int Ƙunshiyar_na_urori = TSARI_Dan_gutsuren_bayani[abu_Manazarta];
        if (Ƙunshiyar_na_urori == -1) return Microsoft_Word_SMS(Suna, "[Ljava/lang/String;") || Microsoft_Word_SMS(Suna, "[Ljava/lang/CharSequence;");
        if (Ƙunshiyar_na_urori == 0) return false;
        if (배열종비교(Ƙunshiyar_na_urori, Suna)) return true;
        if ((Microsoft_Word_SMS(Ƙunshiyar_na_urori, "java/lang/String") || Microsoft_Word_SMS(Ƙunshiyar_na_urori, "java/lang/StringBuilder")) && Microsoft_Word_SMS(Suna, "[Ljava/lang/CharSequence;")) return true;
        for (int Warware_Indes = 0; Warware_Indes < 종수; Warware_Indes++) if (같은말(Aji_Ma_ana_Suna[Warware_Indes], Ƙunshiyar_na_urori)) {
            for (int Lambar_sirrin_harafi = Warware_Indes, 중첩깊이 = 0; Lambar_sirrin_harafi >= 0 && 중첩깊이 < 16; 중첩깊이++, Lambar_sirrin_harafi = 부모종(Lambar_sirrin_harafi)) {
                if (배열종비교(종부모[Lambar_sirrin_harafi], Suna)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[Lambar_sirrin_harafi]; 안쪽자리++) if (배열종비교(Aji_Farfajiya[Lambar_sirrin_harafi * 16 + 안쪽자리], Suna)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int Suna_Jurarre, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (Suna_Jurarre == 0 || 항목수 < 4 || Fayil[검사자리] != '[' || Fayil[검사자리 + 1] != 'L' || Fayil[검사자리 + 항목수 - 1] != ';' || 상나[Suna_Jurarre] != 항목수 - 3) return false;
        for (int Warware_Indes = 0; Warware_Indes < 항목수 - 3; Warware_Indes++) if (Fayil[상가[Suna_Jurarre] + Warware_Indes] != Fayil[검사자리 + 2 + Warware_Indes]) return false;
        return true;
    }
    static void Mariki_banbanchi() {
        if (던진객체 == 0) return;
        Kuskure = false;
        while (allo_Indes >= 현재가닥 * 32) {
            int Fayil_Indes = allo_tsari[allo_Indes], 읽는자리 = allo_Sharadi[allo_Indes];
            for (int Warware_Indes = 0; Warware_Indes < 잡기수; Warware_Indes++) if (잡기함수[Warware_Indes] == Fayil_Indes && 읽는자리 >= 잡기시작[Warware_Indes] && 읽는자리 < 잡기끝[Warware_Indes]
                && (잡기종[Warware_Indes] == 0 || 맞는객체(던진객체, 잡기종[Warware_Indes]))) {
                틀위치[allo_Indes] = 잡기위치[Warware_Indes]; allo_tara[allo_Indes] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (Farko_allo[allo_Indes] != 0) Aji_Ma_ana_Matsayi[Farko_allo[allo_Indes] - 1] = 3;
            if (틀잠금[allo_Indes] != 0) { 잠금풀기(틀잠금[allo_Indes]); 틀잠금[allo_Indes] = 0; }
            allo_Indes--;
        }
        Mai_anfani_da_kwamfuta.Yi_Rubutu("Uncaught ");
        if (힙[던진객체] == 9) { Mai_anfani_da_kwamfuta.Yi_Rubutu(banbanchi_Suna(힙[던진객체 + 2])); Mai_anfani_da_kwamfuta.Yi_Rubutu(": "); Rubuta_SMS(힙[던진객체 + 3]); }
        else Mai_anfani_da_kwamfuta.Yi_Rubutu("user exception");
        Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10); 던진객체 = 0; Kuskure = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void tara_Sharadi(int Umarni_lambar_sirri) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (Umarni_lambar_sirri == 87) return;
        if (Umarni_lambar_sirri == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bayit_Tarin_bayani = 빼기(0), 둘째형식 = 반환형;
        if (Umarni_lambar_sirri == 88) return;
        if (Umarni_lambar_sirri == 90) { 넣기(첫값, 첫형식); 넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (Umarni_lambar_sirri == 92) { 넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식); 넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (Umarni_lambar_sirri == 95) { 넣기(첫값, 첫형식); 넣기(bayit_Tarin_bayani, 둘째형식); return; }
        int Lambar_sirrin_harafi = 빼기(0), 셋째형식 = 반환형;
        if (Umarni_lambar_sirri == 91) { 넣기(첫값, 첫형식); 넣기(Lambar_sirrin_harafi, 셋째형식); 넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (Umarni_lambar_sirri == 93) { 넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식); 넣기(Lambar_sirrin_harafi, 셋째형식); 넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(Lambar_sirrin_harafi, 셋째형식); 넣기(bayit_Tarin_bayani, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int Suna_Jurarre, int 시작점) {
        int ɓangare_lambar_sirri = 0, 유효길이 = 0, banbanchi_Manazarta = banbanchi_Jurarre(Suna_Jurarre);
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/lang/StringBuilder")) { ɓangare_lambar_sirri = 4; 유효길이 = 1; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/io/FileInputStream")) { ɓangare_lambar_sirri = 5; 유효길이 = 2; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/io/FileOutputStream")) { ɓangare_lambar_sirri = 6; 유효길이 = 2; }
        if (banbanchi_Manazarta != 0) { ɓangare_lambar_sirri = 9; 유효길이 = 2; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/util/ArrayList")) { ɓangare_lambar_sirri = 10; 유효길이 = 2; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/util/HashMap")) { ɓangare_lambar_sirri = 11; 유효길이 = 2; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/lang/Integer")) { ɓangare_lambar_sirri = 12; 유효길이 = 1; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/net/Socket")) { ɓangare_lambar_sirri = 17; 유효길이 = 5; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/net/ServerSocket")) { ɓangare_lambar_sirri = 18; 유효길이 = 5; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/net/DatagramSocket")) { ɓangare_lambar_sirri = 15; 유효길이 = 3; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/net/DatagramPacket")) { ɓangare_lambar_sirri = 16; 유효길이 = 4; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/lang/Thread") || Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/작업가닥")) { ɓangare_lambar_sirri = 13; 유효길이 = 2; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/lang/Object")) { ɓangare_lambar_sirri = 8; }
        if (ɓangare_lambar_sirri == 0 && 화면종(Suna_Jurarre) != 0) { ɓangare_lambar_sirri = 화면종(Suna_Jurarre); 유효길이 = 12; }
        if (ɓangare_lambar_sirri == 0) {
            int Lambar_sirrin_harafi = nema_Aji_Ma_ana(Suna_Jurarre); if (Lambar_sirrin_harafi < 0 || Kuskure || !Farko(Lambar_sirrin_harafi, 시작점)) return;
            ɓangare_lambar_sirri = 32 + Lambar_sirrin_harafi; 유효길이 = 종칸수[Lambar_sirrin_harafi];
        }
        int abu_Manazarta = kasafta_Wurin_adana(ɓangare_lambar_sirri, 유효길이); if (Kuskure) return;
        if (ɓangare_lambar_sirri == 13 && Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/작업가닥")) 힙[abu_Manazarta + 3] = 1;
        if (ɓangare_lambar_sirri >= 24 && ɓangare_lambar_sirri <= 28 && 한국어화면종(Suna_Jurarre) != 0) 힙[abu_Manazarta + 13] = 1;
        if (ɓangare_lambar_sirri == 5 || ɓangare_lambar_sirri == 6 || ɓangare_lambar_sirri == 15 || ɓangare_lambar_sirri == 17 || ɓangare_lambar_sirri == 18) 힙[abu_Manazarta + 2] = -1;
        if (ɓangare_lambar_sirri == 9) 힙[abu_Manazarta + 2] = banbanchi_Manazarta;
        넣기(abu_Manazarta, 2);
    }
    static boolean 값같음(int 첫값, int bayit_Tarin_bayani) {
        if (첫값 == bayit_Tarin_bayani) return true;
        if (첫값 == 0 || bayit_Tarin_bayani == 0 || 첫값 < 0 || bayit_Tarin_bayani < 0 || 첫값 >= 힙끝 || bayit_Tarin_bayani >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bayit_Tarin_bayani] == 1) return 글같음(첫값, bayit_Tarin_bayani, false);
        return 힙[첫값] == 12 && 힙[bayit_Tarin_bayani] == 12 && 힙[첫값 + 2] == 힙[bayit_Tarin_bayani + 2];
    }
    static int 글조각(int abu_Manazarta, int 시작자리, int 끝자리) {
        if (!abu_Daraja(abu_Manazarta, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[abu_Manazarta + 1]) { Kasa_aiki_Daraja("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = kasafta_Wurin_adana(1, 끝자리 - 시작자리); if (Kuskure) return 0;
        for (int Warware_Indes = 시작자리; Warware_Indes < 끝자리; Warware_Indes++) 힙[반환값 + 2 + Warware_Indes - 시작자리] = 힙[abu_Manazarta + 2 + Warware_Indes];
        return 반환값;
    }
    static int haɗa_SMS(int 첫값, int bayit_Tarin_bayani) {
        if (!abu_Daraja(첫값, 1) || !abu_Daraja(bayit_Tarin_bayani, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], tsari_Indes = 힙[bayit_Tarin_bayani + 1], 반환값 = kasafta_Wurin_adana(1, 항목수 + tsari_Indes); if (Kuskure) return 0;
        for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) 힙[반환값 + 2 + Warware_Indes] = 힙[첫값 + 2 + Warware_Indes];
        for (int Warware_Indes = 0; Warware_Indes < tsari_Indes; Warware_Indes++) 힙[반환값 + 2 + 항목수 + Warware_Indes] = 힙[bayit_Tarin_bayani + 2 + Warware_Indes];
        return 반환값;
    }
    static boolean 기본호출(int mamallaki, int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri) {
        if (Microsoft_Word_SMS(mamallaki, "한국어/자체/실행인수") && Umarni_lambar_sirri == 184) {
            if (Microsoft_Word_SMS(Suna_Jurarre, "개수") && Microsoft_Word_SMS(서술상수, "()I")) { 넣기(Mai_anfani_da_kwamfuta.인수개수() - 1, 1); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "SMS") && Microsoft_Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= Mai_anfani_da_kwamfuta.인수개수() - 1) 예외던짐(29, "gudanar_Umarni 인수 범위를 벗어났습니다");
                else 넣기(sauka_Harafi(Mai_anfani_da_kwamfuta.인수(순번 + 1)), 2);
                return true;
            }
            Kasa_aiki_Daraja("지원하지 않는 한국어 gudanar_Umarni 인수 호출"); return true;
        }
        if (Microsoft_Word_SMS(mamallaki, "한국어/자체/작업가닥")) { haryar_aikin_na_ura_hira(Suna_Jurarre, 서술상수, Umarni_lambar_sirri, true); return true; }
        if (한국어화면소유(mamallaki)) { 한국어화면호출(mamallaki, Suna_Jurarre, 서술상수, Umarni_lambar_sirri); return true; }
        if (화면소유(mamallaki)) { 화면호출(mamallaki, Suna_Jurarre, 서술상수, Umarni_lambar_sirri); return true; }
        if (Microsoft_Word_SMS(mamallaki, "java/net/Socket") || Microsoft_Word_SMS(mamallaki, "java/net/ServerSocket") || Microsoft_Word_SMS(mamallaki, "java/io/InputStream") || Microsoft_Word_SMS(mamallaki, "java/io/OutputStream")) { 흐름호출(mamallaki, Suna_Jurarre, 서술상수, Umarni_lambar_sirri); return true; }
        if (Microsoft_Word_SMS(mamallaki, "한국어/자체/Kwara_Daraja") && Umarni_lambar_sirri == 184) {
            if (Microsoft_Word_SMS(Suna_Jurarre, "화면너비") && Microsoft_Word_SMS(서술상수, "()I")) { 넣기(Mai_anfani_da_kwamfuta.화면너비(), 1); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "화면높이") && Microsoft_Word_SMS(서술상수, "()I")) { 넣기(Mai_anfani_da_kwamfuta.화면높이(), 1); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "밀리초") && Microsoft_Word_SMS(서술상수, "()I")) { 넣기(Mai_anfani_da_kwamfuta.밀리초(), 1); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "그림대기") && Microsoft_Word_SMS(서술상수, "()I")) { 넣기(Mai_anfani_da_kwamfuta.그림대기(), 1); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "사각형") && Microsoft_Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Maɓallin_Y_Mai_tsarawa = 빼기(1), gamayyar_x = 빼기(1); 넣기(Mai_anfani_da_kwamfuta.사각형(gamayyar_x, Maɓallin_Y_Mai_tsarawa, 너비, 높이, 색상), 1); return true; }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/net/InetAddress") || Microsoft_Word_SMS(mamallaki, "java/net/DatagramPacket") || Microsoft_Word_SMS(mamallaki, "java/net/DatagramSocket")) { 통신호출(mamallaki, Suna_Jurarre, 서술상수, Umarni_lambar_sirri); return true; }
        if (Microsoft_Word_SMS(mamallaki, "java/lang/Thread")) { 가닥호출(Suna_Jurarre, 서술상수, Umarni_lambar_sirri); return true; }
        if (Microsoft_Word_SMS(mamallaki, "java/lang/Object")) {
            if (Microsoft_Word_SMS(Suna_Jurarre, "<init>") && Microsoft_Word_SMS(서술상수, "()V") && Umarni_lambar_sirri == 183) { 객체유효(빼기(2)); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "equals") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayit_Tarin_bayani = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bayit_Tarin_bayani ? 1 : 0, 1); return true; }
        }
        if (banbanchi_Jurarre(mamallaki) != 0) {
            if (Microsoft_Word_SMS(Suna_Jurarre, "<init>") && Umarni_lambar_sirri == 183 && (Microsoft_Word_SMS(서술상수, "()V") || Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int promt = Microsoft_Word_SMS(서술상수, "()V") ? 0 : 빼기(2), abu_Manazarta = 빼기(2);
                if (abu_Daraja(abu_Manazarta, 9)) { 힙[abu_Manazarta + 3] = promt; 힙참조[abu_Manazarta + 3] = 1; } return true;
            }
            if ((Microsoft_Word_SMS(Suna_Jurarre, "getMessage") || Microsoft_Word_SMS(Suna_Jurarre, "설명")) && Microsoft_Word_SMS(서술상수, "()Ljava/lang/String;")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 9)) 넣기(힙[abu_Manazarta + 3], 2); return true; }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/lang/String")) {
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "getBytes") && (Microsoft_Word_SMS(서술상수, "()[B") || Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int Juyar_da_bayanai_zuwa_lamba_Suna = Microsoft_Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), abu_Manazarta = 빼기(2);
                if (!abu_Daraja(abu_Manazarta, 1)) return true;
                if (Juyar_da_bayanai_zuwa_lamba_Suna != 0 && !글같음(Juyar_da_bayanai_zuwa_lamba_Suna, sauka_Harafi("UTF-8"), false) && !글같음(Juyar_da_bayanai_zuwa_lamba_Suna, sauka_Harafi("UTF8"), false) && !글같음(Juyar_da_bayanai_zuwa_lamba_Suna, sauka_Harafi("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[abu_Manazarta + 1], 반환값 = kasafta_Wurin_adana(20, 항목수 * 3), 사용수 = 0; if (Kuskure) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int Lambar_sirrin_harafi = 힙[abu_Manazarta + 2 + 안쪽자리];
                    if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[abu_Manazarta + 3 + 안쪽자리] >= 0xdc00 && 힙[abu_Manazarta + 3 + 안쪽자리] <= 0xdfff) Lambar_sirrin_harafi = 0x10000 + ((Lambar_sirrin_harafi - 0xd800) << 10) + 힙[abu_Manazarta + 2 + ++안쪽자리] - 0xdc00;
                    else if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdfff) Lambar_sirrin_harafi = '?';
                    if (Lambar_sirrin_harafi < 128) 힙[반환값 + 2 + 사용수++] = Lambar_sirrin_harafi;
                    else { int 바이트수 = Lambar_sirrin_harafi < 2048 ? 2 : Lambar_sirrin_harafi < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | Lambar_sirrin_harafi >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | Lambar_sirrin_harafi >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "valueOf") && Microsoft_Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(lamba_Harafi(빼기(1)), 2); return true; }
            if (Umarni_lambar_sirri != 182) return false;
            if (Microsoft_Word_SMS(Suna_Jurarre, "equals") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayit_Tarin_bayani = 빼기(2), 첫값 = 빼기(2); if (abu_Daraja(첫값, 1)) 넣기(글같음(첫값, bayit_Tarin_bayani, false) ? 1 : 0, 1); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "isEmpty") && Microsoft_Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (abu_Daraja(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "substring") && (Microsoft_Word_SMS(서술상수, "(I)Ljava/lang/String;") || Microsoft_Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Microsoft_Word_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (abu_Daraja(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Microsoft_Word_SMS(Suna_Jurarre, "concat") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bayit_Tarin_bayani = 빼기(2), 첫값 = 빼기(2); 넣기(haɗa_SMS(첫값, bayit_Tarin_bayani), 2); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "hashCode") && Microsoft_Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_Daraja = 0; if (abu_Daraja(첫값, 1)) { for (int Warware_Indes = 0; Warware_Indes < 힙[첫값 + 1]; Warware_Indes++) hash_Daraja = hash_Daraja * 31 + 힙[첫값 + 2 + Warware_Indes]; 넣기(hash_Daraja, 1); } return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "toString") && Microsoft_Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (abu_Daraja(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/lang/Integer")) {
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "valueOf") && Microsoft_Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int Tarin_bayani_Daraja = 빼기(1), abu_Manazarta = Tarin_bayani_Daraja >= -128 && Tarin_bayani_Daraja <= 127 ? Ajiye_Lamba_mara[Tarin_bayani_Daraja + 128] : 0; if (abu_Manazarta == 0) { abu_Manazarta = kasafta_Wurin_adana(12, 1); if (!Kuskure) { 힙[abu_Manazarta + 2] = Tarin_bayani_Daraja; if (Tarin_bayani_Daraja >= -128 && Tarin_bayani_Daraja <= 127) Ajiye_Lamba_mara[Tarin_bayani_Daraja + 128] = abu_Manazarta; } } 넣기(abu_Manazarta, 2); return true; }
            if (Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(Suna_Jurarre, "<init>") && Microsoft_Word_SMS(서술상수, "(I)V")) { int Tarin_bayani_Daraja = 빼기(1), abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 12)) 힙[abu_Manazarta + 2] = Tarin_bayani_Daraja; return true; }
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "intValue") && Microsoft_Word_SMS(서술상수, "()I")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 12)) 넣기(힙[abu_Manazarta + 2], 1); return true; }
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "toString") && Microsoft_Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(lamba_Harafi(빼기(1)), 2); return true; }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/lang/Math") && Umarni_lambar_sirri == 184) {
            if (Microsoft_Word_SMS(Suna_Jurarre, "abs") && Microsoft_Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Microsoft_Word_SMS(Suna_Jurarre, "min") || Microsoft_Word_SMS(Suna_Jurarre, "max")) && Microsoft_Word_SMS(서술상수, "(II)I")) { int bayit_Tarin_bayani = 빼기(1), 첫값 = 빼기(1); 넣기(Microsoft_Word_SMS(Suna_Jurarre, "min") ? (첫값 < bayit_Tarin_bayani ? 첫값 : bayit_Tarin_bayani) : (첫값 > bayit_Tarin_bayani ? 첫값 : bayit_Tarin_bayani), 1); return true; }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/lang/System") && Umarni_lambar_sirri == 184) {
            if (Microsoft_Word_SMS(Suna_Jurarre, "gc") && Microsoft_Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "arraycopy") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), Zangon_ƙarshe_Daraja_Indes = 빼기(1), bayit_Tarin_bayani = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bayit_Tarin_bayani)) {
                    int ɓangare_lambar_sirri = 힙[첫값];
                    if (힙[bayit_Tarin_bayani] != ɓangare_lambar_sirri || (ɓangare_lambar_sirri != 2 && ɓangare_lambar_sirri != 3 && (ɓangare_lambar_sirri < 20 || ɓangare_lambar_sirri > 23))) Kasa_aiki_Daraja("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || Zangon_ƙarshe_Daraja_Indes < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || Zangon_ƙarshe_Daraja_Indes > 힙[bayit_Tarin_bayani + 1] - 항목수) Kasa_aiki_Daraja("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bayit_Tarin_bayani && Zangon_ƙarshe_Daraja_Indes > 시작자리) { for (int Warware_Indes = 항목수 - 1; Warware_Indes >= 0; Warware_Indes--) 힙[bayit_Tarin_bayani + 2 + Zangon_ƙarshe_Daraja_Indes + Warware_Indes] = 힙[첫값 + 2 + 시작자리 + Warware_Indes]; }
                    else { for (int Warware_Indes = 0; Warware_Indes < 항목수 && !Kuskure; Warware_Indes++) { int Tarin_bayani_Daraja = 힙[첫값 + 2 + 시작자리 + Warware_Indes]; if (ɓangare_lambar_sirri != 3 || 배열저장가능(bayit_Tarin_bayani, Tarin_bayani_Daraja)) 힙[bayit_Tarin_bayani + 2 + Zangon_ƙarshe_Daraja_Indes + Warware_Indes] = Tarin_bayani_Daraja; } }
                }
                return true;
            }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/util/ArrayList") || Microsoft_Word_SMS(mamallaki, "java/util/List") || Microsoft_Word_SMS(mamallaki, "java/util/HashMap") || Microsoft_Word_SMS(mamallaki, "java/util/Map")) {
            모음호출(mamallaki, Suna_Jurarre, 서술상수, Umarni_lambar_sirri); return true;
        }
        return false;
    }
    static void 모음늘리기(int abu_Manazarta, int 필요수) {
        int 이전값 = 힙[abu_Manazarta + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int Tarin_bayani_TSARI = kasafta_Wurin_adana(3, 다음자리); if (Kuskure) return;
        for (int Warware_Indes = 0; Warware_Indes < 용량값; Warware_Indes++) 힙[Tarin_bayani_TSARI + 2 + Warware_Indes] = 힙[이전값 + 2 + Warware_Indes];
        힙[abu_Manazarta + 2] = Tarin_bayani_TSARI; 힙참조[abu_Manazarta + 2] = 1;
    }
    static void 모음호출(int mamallaki, int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri) {
        boolean 대응참조 = Microsoft_Word_SMS(mamallaki, "java/util/HashMap") || Microsoft_Word_SMS(mamallaki, "java/util/Map"); int ɓangare_lambar_sirri = 대응참조 ? 11 : 10;
        if (Microsoft_Word_SMS(Suna_Jurarre, "<init>") && Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(서술상수, "()V")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, ɓangare_lambar_sirri)) 모음늘리기(abu_Manazarta, 8); return; }
        if (Umarni_lambar_sirri != 182 && Umarni_lambar_sirri != 185) { Kasa_aiki_Daraja("invalid collection invocation"); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "size") && Microsoft_Word_SMS(서술상수, "()I") || Microsoft_Word_SMS(Suna_Jurarre, "isEmpty") && Microsoft_Word_SMS(서술상수, "()Z")) {
            int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, ɓangare_lambar_sirri)) 넣기(Microsoft_Word_SMS(Suna_Jurarre, "size") ? 힙[abu_Manazarta + 3] : 힙[abu_Manazarta + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "clear") && Microsoft_Word_SMS(서술상수, "()V")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, ɓangare_lambar_sirri)) { int Tarin_bayani_TSARI = 힙[abu_Manazarta + 2]; for (int Warware_Indes = 0; Warware_Indes < 힙[Tarin_bayani_TSARI + 1]; Warware_Indes++) 힙[Tarin_bayani_TSARI + 2 + Warware_Indes] = 0; 힙[abu_Manazarta + 3] = 0; } return; }
        if (!대응참조 && Microsoft_Word_SMS(Suna_Jurarre, "add") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int Tarin_bayani_Daraja = 빼기(2), abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 10)) return;
            int 항목수 = 힙[abu_Manazarta + 3]; 모음늘리기(abu_Manazarta, 항목수 + 1); if (!Kuskure) { 힙[힙[abu_Manazarta + 2] + 2 + 항목수] = Tarin_bayani_Daraja; 힙[abu_Manazarta + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Microsoft_Word_SMS(Suna_Jurarre, "get") || Microsoft_Word_SMS(Suna_Jurarre, "remove")) && Microsoft_Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Microsoft_Word_SMS(Suna_Jurarre, "set") && Microsoft_Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Microsoft_Word_SMS(Suna_Jurarre, "set"); int Tarin_bayani_Daraja = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), abu_Manazarta = 빼기(2);
            if (!abu_Daraja(abu_Manazarta, 10)) return;
            int 항목수 = 힙[abu_Manazarta + 3], Tarin_bayani_TSARI = 힙[abu_Manazarta + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[Tarin_bayani_TSARI + 2 + 항목자리];
            if (지정여부) 힙[Tarin_bayani_TSARI + 2 + 항목자리] = Tarin_bayani_Daraja;
            if (Microsoft_Word_SMS(Suna_Jurarre, "remove")) { for (int Warware_Indes = 항목자리 + 1; Warware_Indes < 항목수; Warware_Indes++) 힙[Tarin_bayani_TSARI + 1 + Warware_Indes] = 힙[Tarin_bayani_TSARI + 2 + Warware_Indes]; 힙[Tarin_bayani_TSARI + 1 + 항목수] = 0; 힙[abu_Manazarta + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Microsoft_Word_SMS(Suna_Jurarre, "get") || Microsoft_Word_SMS(Suna_Jurarre, "remove")) && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Microsoft_Word_SMS(Suna_Jurarre, "put") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Microsoft_Word_SMS(Suna_Jurarre, "containsKey") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Microsoft_Word_SMS(Suna_Jurarre, "put"), Cire = Microsoft_Word_SMS(Suna_Jurarre, "remove");
            int Tarin_bayani_Daraja = 넣기여부 ? 빼기(2) : 0, Makulli_Manazarta = 빼기(2), abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 11)) return;
            int 항목수 = 힙[abu_Manazarta + 3], Tarin_bayani_TSARI = 힙[abu_Manazarta + 2], 찾은여부 = -1;
            for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) if (값같음(Makulli_Manazarta, 힙[Tarin_bayani_TSARI + 2 + 2 * Warware_Indes])) { 찾은여부 = Warware_Indes; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[Tarin_bayani_TSARI + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(abu_Manazarta, (항목수 + 1) * 2); Tarin_bayani_TSARI = 힙[abu_Manazarta + 2]; 찾은여부 = 항목수; if (!Kuskure) 힙[abu_Manazarta + 3] = 항목수 + 1; }
                if (!Kuskure) { 힙[Tarin_bayani_TSARI + 2 + 2 * 찾은여부] = Makulli_Manazarta; 힙[Tarin_bayani_TSARI + 3 + 2 * 찾은여부] = Tarin_bayani_Daraja; }
            }
            if (Cire && 찾은여부 >= 0) { for (int Warware_Indes = 찾은여부 + 1; Warware_Indes < 항목수; Warware_Indes++) { 힙[Tarin_bayani_TSARI + 2 * Warware_Indes] = 힙[Tarin_bayani_TSARI + 2 + 2 * Warware_Indes]; 힙[Tarin_bayani_TSARI + 1 + 2 * Warware_Indes] = 힙[Tarin_bayani_TSARI + 3 + 2 * Warware_Indes]; } 힙[Tarin_bayani_TSARI + 2 * 항목수] = 0; 힙[Tarin_bayani_TSARI + 1 + 2 * 항목수] = 0; 힙[abu_Manazarta + 3] = 항목수 - 1; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        Kasa_aiki_Daraja("unsupported collection method");
    }
    static boolean 잠금얻기(int abu_Manazarta) {
        if (!객체유효(abu_Manazarta)) return false;
        if (잠금깊이[abu_Manazarta] != 0 && 잠금주인[abu_Manazarta] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[abu_Manazarta] = 현재가닥 + 1; 잠금깊이[abu_Manazarta]++; return true;
    }
    static void 잠금풀기(int abu_Manazarta) {
        if (!객체유효(abu_Manazarta)) return;
        if (잠금깊이[abu_Manazarta] == 0 || 잠금주인[abu_Manazarta] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[abu_Manazarta] == 0) 잠금주인[abu_Manazarta] = 0;
    }
    static boolean Sauya_hira() {
        hira_allo[현재가닥] = allo_Indes;
        if (allo_Indes < 현재가닥 * 32) hira_Matsayi[현재가닥] = 3;
        for (int Warware_Indes = 0; Warware_Indes < 가닥수; Warware_Indes++) if (hira_Matsayi[Warware_Indes] == 2 && hira_Matsayi[가닥대기[Warware_Indes]] == 3) hira_Matsayi[Warware_Indes] = 1;
        for (int Warware_Indes = 1; Warware_Indes <= 가닥수; Warware_Indes++) {
            int 다음자리 = (현재가닥 + Warware_Indes) % 가닥수;
            if (hira_Matsayi[다음자리] == 1) { 현재가닥 = 다음자리; allo_Indes = hira_allo[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int Warware_Indes = 0; Warware_Indes < 가닥수; Warware_Indes++) if (hira_Matsayi[Warware_Indes] != 3) { Kasa_aiki_Daraja("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri) { haryar_aikin_na_ura_hira(Suna_Jurarre, 서술상수, Umarni_lambar_sirri, false); }
    static void haryar_aikin_na_ura_hira(int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri, boolean 한국어) {
        if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, 한국어 ? "ɗan_tsai_da_aiki" : "yield") && Microsoft_Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "currentThread") && Microsoft_Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(hira_abu[현재가닥], 2); return; }
        if (Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(Suna_Jurarre, "<init>") && (Microsoft_Word_SMS(서술상수, "()V") || Microsoft_Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int tageti_imel = Microsoft_Word_SMS(서술상수, "()V") ? 0 : 빼기(2), abu_Manazarta = 빼기(2);
            if (!객체유효(abu_Manazarta)) return;
            if (힙[abu_Manazarta] == 13) { 힙[abu_Manazarta + 2] = tageti_imel; 힙참조[abu_Manazarta + 2] = 1; }
            else if (tageti_imel != 0) Kasa_aiki_Daraja("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (Umarni_lambar_sirri == 182 && (Microsoft_Word_SMS(Suna_Jurarre, 한국어 ? "Fara_aiki" : "start") || Microsoft_Word_SMS(Suna_Jurarre, 한국어 ? "기다리기" : "join")) && Microsoft_Word_SMS(서술상수, "()V") || Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, 한국어 ? "살아있는가" : "isAlive") && Microsoft_Word_SMS(서술상수, "()Z")) {
            int abu_Manazarta = 빼기(2); if (!객체유효(abu_Manazarta)) return;
            int asusu_Daraja = -1; for (int Warware_Indes = 0; Warware_Indes < 가닥수; Warware_Indes++) if (hira_abu[Warware_Indes] == abu_Manazarta) asusu_Daraja = Warware_Indes;
            if (Microsoft_Word_SMS(Suna_Jurarre, 한국어 ? "살아있는가" : "isAlive")) { 넣기(asusu_Daraja >= 0 && hira_Matsayi[asusu_Daraja] != 3 ? 1 : 0, 1); return; }
            if (Microsoft_Word_SMS(Suna_Jurarre, 한국어 ? "기다리기" : "join")) { if (asusu_Daraja >= 0 && hira_Matsayi[asusu_Daraja] != 3) { 가닥대기[현재가닥] = asusu_Daraja; hira_Matsayi[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (asusu_Daraja >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { Kasa_aiki_Daraja("thread limit (4 including main)"); return; }
            int tageti_imel = 힙[abu_Manazarta] == 13 ? 힙[abu_Manazarta + 2] : abu_Manazarta;
            int Fayil_Indes = tageti_imel > 0 && 힙[tageti_imel] >= 32 ? Suna_tsari(힙[tageti_imel] - 32, 한국어 ? "gudanar_aiki" : "run", "()V") : -1;
            if (tageti_imel != 0 && Fayil_Indes < 0) { Kasa_aiki_Daraja("Runnable.run required"); return; }
            asusu_Daraja = 가닥수++; hira_abu[asusu_Daraja] = abu_Manazarta; hira_tageti[asusu_Daraja] = tageti_imel;
            int allo = asusu_Daraja * 32; hira_allo[asusu_Daraja] = Fayil_Indes < 0 ? allo - 1 : allo; hira_Matsayi[asusu_Daraja] = Fayil_Indes < 0 ? 3 : 1;
            if (Fayil_Indes >= 0) { allo_tsari[allo] = Fayil_Indes; 틀위치[allo] = tsari_Fara[Fayil_Indes]; na_gida_Daraja[allo * 128] = tageti_imel; na_gida_rubuta[allo * 128] = 2; }
            return;
        }
        Kasa_aiki_Daraja("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], imel_SMS = new int[16];
    static int na_gida_imel() { return imel_abu(0x7f000001); }
    static int imel_abu(int Daraja) { int abu_Manazarta = kasafta_Wurin_adana(14, 1); if (!Kuskure) 힙[abu_Manazarta + 2] = Daraja; return abu_Manazarta; }
    static int 주소해독(int abu_Manazarta) {
        if (abu_Manazarta == 0 || 글같음(abu_Manazarta, sauka_Harafi("localhost"), false)) return 0x7f000001;
        if (!abu_Daraja(abu_Manazarta, 1)) return 0;
        int Tarin_bayani_Daraja = 0, 총수 = 0, imel_bayit = 0, 자릿수 = 0, 항목수 = 힙[abu_Manazarta + 1];
        for (int Warware_Indes = 0; Warware_Indes <= 항목수; Warware_Indes++) {
            int Lambar_sirrin_harafi = Warware_Indes == 항목수 ? '.' : 힙[abu_Manazarta + 2 + Warware_Indes];
            if (Lambar_sirrin_harafi == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } Tarin_bayani_Daraja = Tarin_bayani_Daraja << 8 | imel_bayit; 총수++; imel_bayit = 자릿수 = 0; }
            else { if (Lambar_sirrin_harafi < '0' || Lambar_sirrin_harafi > '9' || ++자릿수 > 3 || (imel_bayit = imel_bayit * 10 + Lambar_sirrin_harafi - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return Tarin_bayani_Daraja;
    }
    static int imel_Harafi(int Tarin_bayani_Daraja) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int imel_bayit = Tarin_bayani_Daraja >>> 이동비트 & 255;
            if (imel_bayit >= 100) imel_SMS[항목수++] = '0' + imel_bayit / 100;
            if (imel_bayit >= 10) imel_SMS[항목수++] = '0' + imel_bayit / 10 % 10;
            imel_SMS[항목수++] = '0' + imel_bayit % 10; if (이동비트 != 0) imel_SMS[항목수++] = '.';
        }
        int abu_Manazarta = kasafta_Wurin_adana(1, 항목수); if (!Kuskure) for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) 힙[abu_Manazarta + 2 + Warware_Indes] = imel_SMS[Warware_Indes]; return abu_Manazarta;
    }
    static void 통신호출(int mamallaki, int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri) {
        if (Microsoft_Word_SMS(mamallaki, "java/net/InetAddress")) {
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "getLoopbackAddress") && Microsoft_Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(na_gida_imel(), 2); return; }
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "getByName") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int Tarin_bayani_Daraja = 주소해독(빼기(2)); if (던진객체 == 0 && !Kuskure) 넣기(imel_abu(Tarin_bayani_Daraja), 2); return;
            }
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "getHostAddress") && Microsoft_Word_SMS(서술상수, "()Ljava/lang/String;")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 14)) 넣기(imel_Harafi(힙[abu_Manazarta + 2]), 2); return; }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/net/DatagramPacket")) {
            if (Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(Suna_Jurarre, "<init>") && (Microsoft_Word_SMS(서술상수, "([BI)V") || Microsoft_Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean Zangon_ƙarshe_Daraja_Manazarta = Microsoft_Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int lambar_kafa = Zangon_ƙarshe_Daraja_Manazarta ? 빼기(1) : 0, imel_Manazarta = Zangon_ƙarshe_Daraja_Manazarta ? 빼기(2) : 0;
                int 항목수 = 빼기(1), Tarin_bayani_TSARI = 빼기(2), abu_Manazarta = 빼기(2);
                if (!abu_Daraja(abu_Manazarta, 16) || !abu_Daraja(Tarin_bayani_TSARI, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[Tarin_bayani_TSARI + 1] || lambar_kafa < 0 || lambar_kafa > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (imel_Manazarta != 0 && !abu_Daraja(imel_Manazarta, 14)) return;
                힙[abu_Manazarta + 2] = Tarin_bayani_TSARI; 힙참조[abu_Manazarta + 2] = 1; 힙[abu_Manazarta + 3] = 항목수;
                힙[abu_Manazarta + 4] = imel_Manazarta; 힙참조[abu_Manazarta + 4] = 1; 힙[abu_Manazarta + 5] = lambar_kafa; return;
            }
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "setLength") && Microsoft_Word_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[abu_Manazarta + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[abu_Manazarta + 3] = 항목수; return;
            }
            if (Umarni_lambar_sirri == 182 && (Microsoft_Word_SMS(Suna_Jurarre, "getData") && Microsoft_Word_SMS(서술상수, "()[B") || Microsoft_Word_SMS(Suna_Jurarre, "getLength") && Microsoft_Word_SMS(서술상수, "()I") || Microsoft_Word_SMS(Suna_Jurarre, "getAddress") && Microsoft_Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Microsoft_Word_SMS(Suna_Jurarre, "getPort") && Microsoft_Word_SMS(서술상수, "()I"))) {
                int abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 16)) return;
                int 항목자리 = Microsoft_Word_SMS(Suna_Jurarre, "getData") ? 2 : Microsoft_Word_SMS(Suna_Jurarre, "getLength") ? 3 : Microsoft_Word_SMS(Suna_Jurarre, "getAddress") ? 4 : 5;
                넣기(힙[abu_Manazarta + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Microsoft_Word_SMS(mamallaki, "java/net/DatagramSocket")) {
            if (Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(Suna_Jurarre, "<init>") && (Microsoft_Word_SMS(서술상수, "()V") || Microsoft_Word_SMS(서술상수, "(I)V"))) {
                int lambar_kafa = Microsoft_Word_SMS(서술상수, "()V") ? 0 : 빼기(1), abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 15)) return;
                if (lambar_kafa < 0 || lambar_kafa > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = Mai_anfani_da_kwamfuta.buɗe_Hanyar_sadarwa(lambar_kafa); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[abu_Manazarta + 2] = 열린파일번호; return;
            }
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "setSoTimeout") && Microsoft_Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[abu_Manazarta + 3] = 밀리초값; return;
            }
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "getLocalPort") && Microsoft_Word_SMS(서술상수, "()I")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 15)) 넣기(힙[abu_Manazarta + 2] < 0 ? -1 : Mai_anfani_da_kwamfuta.Hanyar_sadarwa_fot(힙[abu_Manazarta + 2]), 1); return; }
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "isClosed") && Microsoft_Word_SMS(서술상수, "()Z")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 15)) 넣기(힙[abu_Manazarta + 2] < 0 ? 1 : 0, 1); return; }
            if (Umarni_lambar_sirri == 182 && Microsoft_Word_SMS(Suna_Jurarre, "close") && Microsoft_Word_SMS(서술상수, "()V")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 15) && 힙[abu_Manazarta + 2] >= 0) { Mai_anfani_da_kwamfuta.파일서술자닫기(힙[abu_Manazarta + 2]); 힙[abu_Manazarta + 2] = -1; } return; }
            if (Umarni_lambar_sirri == 182 && (Microsoft_Word_SMS(Suna_Jurarre, "send") || Microsoft_Word_SMS(Suna_Jurarre, "receive")) && Microsoft_Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int makunshi = 빼기(2), abu_Manazarta = 빼기(2); if (!abu_Daraja(makunshi, 16) || !abu_Daraja(abu_Manazarta, 15)) return;
                int Tarin_bayani_TSARI = 힙[makunshi + 2], 유효길이 = 힙[makunshi + 3], 열린파일번호 = 힙[abu_Manazarta + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Microsoft_Word_SMS(Suna_Jurarre, "send")) {
                    if (!abu_Daraja(힙[makunshi + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Warware_Indes = 0; Warware_Indes < 유효길이; Warware_Indes++) 통신임시[Warware_Indes] = 힙[Tarin_bayani_TSARI + 2 + Warware_Indes];
                    if (Mai_anfani_da_kwamfuta.Aika_Hanyar_sadarwa(열린파일번호, 힙[힙[makunshi + 4] + 2], 힙[makunshi + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = Mai_anfani_da_kwamfuta.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = Mai_anfani_da_kwamfuta.밀리초();
                        if (힙[abu_Manazarta + 4] == 0) 힙[abu_Manazarta + 4] = 현재시각 + 1;
                        if (힙[abu_Manazarta + 3] > 0 && 현재시각 - (힙[abu_Manazarta + 4] - 1) >= 힙[abu_Manazarta + 3]) { 힙[abu_Manazarta + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(abu_Manazarta, 2); 넣기(makunshi, 2); 틀위치[allo_Indes] = allo_Sharadi[allo_Indes]; 바꿈요청 = true; return;
                    }
                    힙[abu_Manazarta + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) 힙[Tarin_bayani_TSARI + 2 + Warware_Indes] = (byte)통신임시[Warware_Indes];
                    힙[makunshi + 3] = 항목수; 힙[makunshi + 4] = imel_abu(통신임시[513]); 힙참조[makunshi + 4] = 1; 힙[makunshi + 5] = 통신임시[512];
                }
                return;
            }
        }
        Kasa_aiki_Daraja("unsupported java.net method");
    }
    static boolean 흐름대기(int abu_Manazarta) {
        int 현재시각 = Mai_anfani_da_kwamfuta.밀리초();
        if (힙[abu_Manazarta + 5] == 0) 힙[abu_Manazarta + 5] = 현재시각 + 1;
        if (힙[abu_Manazarta + 3] > 0 && 현재시각 - (힙[abu_Manazarta + 5] - 1) >= 힙[abu_Manazarta + 3]) { 힙[abu_Manazarta + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[allo_Indes] = allo_Sharadi[allo_Indes]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int mamallaki, int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri) {
        boolean 수신쪽 = Microsoft_Word_SMS(mamallaki, "java/net/ServerSocket"), watsuwa = Microsoft_Word_SMS(mamallaki, "java/io/InputStream") || Microsoft_Word_SMS(mamallaki, "java/io/OutputStream");
        if (!watsuwa && Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(Suna_Jurarre, "<init>")) {
            boolean kimiyar_bayanai_holoko_Matsayi = Microsoft_Word_SMS(서술상수, "()V"), 이름지정여부 = Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Microsoft_Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(kimiyar_bayanai_holoko_Matsayi || 수신쪽 && Microsoft_Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { Kasa_aiki_Daraja("unsupported socket constructor"); return; }
            int lambar_kafa = kimiyar_bayanai_holoko_Matsayi ? 0 : 빼기(1), imel_Manazarta = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, abu_Manazarta = 빼기(2);
            if (!abu_Daraja(abu_Manazarta, 수신쪽 ? 18 : 17)) return;
            if (lambar_kafa < 0 || lambar_kafa > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !abu_Daraja(imel_Manazarta, 14)) return;
            int Hanyar_sadarwa_imel_df3458bb = 이름지정여부 ? 주소해독(imel_Manazarta) : 주소지정여부 ? 힙[imel_Manazarta + 2] : 0x7f000001;
            if (Kuskure || 던진객체 != 0) return;
            int 열린파일번호 = Mai_anfani_da_kwamfuta.watsuwa_masarrafa(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = kimiyar_bayanai_holoko_Matsayi ? 0 : 수신쪽 ? Mai_anfani_da_kwamfuta.watsuwa_masarrafa(1, 열린파일번호, lambar_kafa) : Mai_anfani_da_kwamfuta.HAƊI_watsuwa(열린파일번호, Hanyar_sadarwa_imel_df3458bb, lambar_kafa);
            if (처리값 < 0) { Mai_anfani_da_kwamfuta.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[abu_Manazarta + 2] = 열린파일번호; 힙[abu_Manazarta + 4] = lambar_kafa; 힙[abu_Manazarta + 6] = kimiyar_bayanai_holoko_Matsayi ? 0 : 1; return;
        }
        if (!watsuwa && Microsoft_Word_SMS(Suna_Jurarre, "setSoTimeout") && Microsoft_Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[abu_Manazarta + 3] = 밀리초값; return; }
        if (!watsuwa && Microsoft_Word_SMS(Suna_Jurarre, "close") && Microsoft_Word_SMS(서술상수, "()V")) { int abu_Manazarta = 빼기(2); if (abu_Daraja(abu_Manazarta, 수신쪽 ? 18 : 17) && 힙[abu_Manazarta + 2] >= 0) { Mai_anfani_da_kwamfuta.파일서술자닫기(힙[abu_Manazarta + 2]); 힙[abu_Manazarta + 2] = -1; } return; }
        if (!watsuwa && (Microsoft_Word_SMS(Suna_Jurarre, "getLocalPort") || Microsoft_Word_SMS(Suna_Jurarre, "getPort") || Microsoft_Word_SMS(Suna_Jurarre, "isClosed") || Microsoft_Word_SMS(Suna_Jurarre, "isConnected"))) {
            int abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 수신쪽 ? 18 : 17)) return;
            넣기(Microsoft_Word_SMS(Suna_Jurarre, "isClosed") ? 힙[abu_Manazarta + 2] < 0 ? 1 : 0 : Microsoft_Word_SMS(Suna_Jurarre, "isConnected") ? 힙[abu_Manazarta + 6] : Microsoft_Word_SMS(Suna_Jurarre, "getPort") ? 힙[abu_Manazarta + 4] : 힙[abu_Manazarta + 2] < 0 ? -1 : Mai_anfani_da_kwamfuta.watsuwa_masarrafa(4, 힙[abu_Manazarta + 2], 0), 1); return;
        }
        if (수신쪽 && Microsoft_Word_SMS(Suna_Jurarre, "accept") && Microsoft_Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 18)) return; int 열린파일번호 = Mai_anfani_da_kwamfuta.watsuwa_masarrafa(3, 힙[abu_Manazarta + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(abu_Manazarta)) 넣기(abu_Manazarta, 2); return; }
            힙[abu_Manazarta + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = kasafta_Wurin_adana(17, 5); if (Kuskure) { Mai_anfani_da_kwamfuta.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = Mai_anfani_da_kwamfuta.watsuwa_masarrafa(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !watsuwa && ((Microsoft_Word_SMS(Suna_Jurarre, "getInputStream") && Microsoft_Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Microsoft_Word_SMS(Suna_Jurarre, "getOutputStream") && Microsoft_Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 17)) return; if (힙[abu_Manazarta + 2] < 0 || 힙[abu_Manazarta + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = kasafta_Wurin_adana(19, 4); if (Kuskure) return; 힙[반환값 + 2] = abu_Manazarta; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Microsoft_Word_SMS(Suna_Jurarre, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (watsuwa) {
            boolean 읽기여부 = Microsoft_Word_SMS(Suna_Jurarre, "read"), kimiyar_bayanai_Rubuta_aiki = Microsoft_Word_SMS(Suna_Jurarre, "write"), bulo = Microsoft_Word_SMS(서술상수, "([B)I") || Microsoft_Word_SMS(서술상수, "([B)V"), kimiyar_bayanai_SUBARRAY = Microsoft_Word_SMS(서술상수, "([BII)I") || Microsoft_Word_SMS(서술상수, "([BII)V");
            int 항목수 = kimiyar_bayanai_SUBARRAY ? 빼기(1) : 0, 시작변위 = kimiyar_bayanai_SUBARRAY ? 빼기(1) : 0, Tarin_bayani_TSARI = bulo || kimiyar_bayanai_SUBARRAY ? 빼기(2) : 0;
            int Tarin_bayani_Daraja = kimiyar_bayanai_Rubuta_aiki && Microsoft_Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, abu_Manazarta = 빼기(2);
            if (!abu_Daraja(abu_Manazarta, 19)) return; int 부모참조 = 힙[abu_Manazarta + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "close") && Microsoft_Word_SMS(서술상수, "()V")) { Mai_anfani_da_kwamfuta.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Microsoft_Word_SMS(Suna_Jurarre, "flush") && Microsoft_Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !kimiyar_bayanai_Rubuta_aiki) || 읽기여부 != (힙[abu_Manazarta + 3] == 0)) { Kasa_aiki_Daraja("unsupported stream operation"); return; }
            if (bulo || kimiyar_bayanai_SUBARRAY) { if (!abu_Daraja(Tarin_bayani_TSARI, 20)) return; if (bulo) 항목수 = 힙[Tarin_bayani_TSARI + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[Tarin_bayani_TSARI + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = kimiyar_bayanai_Rubuta_aiki ? 힙[abu_Manazarta + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? Mai_anfani_da_kwamfuta.파일한바이트읽기(열린파일번호) : Mai_anfani_da_kwamfuta.파일한바이트쓰기(열린파일번호, bulo || kimiyar_bayanai_SUBARRAY ? 힙[Tarin_bayani_TSARI + 2 + 시작변위 + 완료수] : Tarin_bayani_Daraja);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bulo || kimiyar_bayanai_SUBARRAY)) 힙[Tarin_bayani_TSARI + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(bulo || kimiyar_bayanai_SUBARRAY)) break;
            }
            if (처리값 == -11 && (kimiyar_bayanai_Rubuta_aiki || 완료수 == 0)) {
                힙[abu_Manazarta + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(abu_Manazarta, 2); if (bulo || kimiyar_bayanai_SUBARRAY) 넣기(Tarin_bayani_TSARI, 2); if (kimiyar_bayanai_SUBARRAY) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (kimiyar_bayanai_Rubuta_aiki && !(bulo || kimiyar_bayanai_SUBARRAY)) 넣기(Tarin_bayani_Daraja, 1); } return;
            }
            힙[abu_Manazarta + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : bulo || kimiyar_bayanai_SUBARRAY ? 완료수 : 처리값, 1); return;
        }
        Kasa_aiki_Daraja("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int Suna_Jurarre) {
        if (Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/taga")) return 24;
        if (Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/alama")) return 26;
        if (Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/maɓali")) return 27;
        if (Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/SMS_Fili")) return 28;
        if (Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int Suna_Jurarre) {
        return 한국어화면종(Suna_Jurarre) != 0 || Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/화면구성요소") || Microsoft_Word_SMS(Suna_Jurarre, "한국어/자체/Faruwa_Jerin_ayyukan_da_za_a_yi");
    }
    static int 화면종(int Suna_Jurarre) {
        int 한국어종 = 한국어화면종(Suna_Jurarre); if (한국어종 != 0) return 한국어종;
        if (Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/JFrame")) return 24;
        if (Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/JPanel")) return 25;
        if (Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/JLabel")) return 26;
        if (Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/JButton")) return 27;
        if (Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/JTextField")) return 28;
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/awt/event/ActionEvent")) return 29;
        if (Microsoft_Word_SMS(Suna_Jurarre, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int Suna_Jurarre) {
        return 화면종(Suna_Jurarre) != 0 || Microsoft_Word_SMS(Suna_Jurarre, "java/awt/Component") || Microsoft_Word_SMS(Suna_Jurarre, "java/awt/Container") || Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/JComponent") || Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/AbstractButton") || Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/text/JTextComponent") || Microsoft_Word_SMS(Suna_Jurarre, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int abu_Manazarta) { if (!객체유효(abu_Manazarta)) return false; if (힙[abu_Manazarta] < 24 || 힙[abu_Manazarta] > 28) { Kasa_aiki_Daraja("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int abu_Manazarta, int SMS_Manazarta) {
        if (SMS_Manazarta != 0 && !abu_Daraja(SMS_Manazarta, 1)) return;
        int 항목수 = SMS_Manazarta == 0 ? 0 : 힙[SMS_Manazarta + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) 화면글임시[Warware_Indes] = 힙[SMS_Manazarta + 2 + Warware_Indes];
        if (Mai_anfani_da_kwamfuta.화면글(힙[abu_Manazarta + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[abu_Manazarta + 3] = SMS_Manazarta; 힙참조[abu_Manazarta + 3] = 1;
    }
    static int 화면문자읽기(int abu_Manazarta) {
        int asusu_Daraja = 힙[abu_Manazarta + 2], 항목수 = Mai_anfani_da_kwamfuta.화면연결(8, asusu_Daraja, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { Kasa_aiki_Daraja("GUI text read failed"); return 0; }
        for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) { int 부호값 = Mai_anfani_da_kwamfuta.화면연결(9, asusu_Daraja, Warware_Indes, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = kasafta_Wurin_adana(1, 사용수); if (!Kuskure) for (int Warware_Indes = 0; Warware_Indes < 사용수; Warware_Indes++) 힙[반환값 + 2 + Warware_Indes] = 화면글임시[Warware_Indes]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 Kwara_Daraja 화면 기능에 연결한다. Swing abu_Daraja/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int mamallaki, int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri) {
        if (Microsoft_Word_SMS(mamallaki, "한국어/자체/Faruwa_Jerin_ayyukan_da_za_a_yi")) {
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "나중에실행") && Microsoft_Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int aiki_Aiki = 빼기(2); if (!객체유효(aiki_Aiki)) return;
                if (나중수 == 8) { Kasa_aiki_Daraja("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = aiki_Aiki; return;
            }
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "사건처리중인가") && Microsoft_Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            Kasa_aiki_Daraja("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Microsoft_Word_SMS(mamallaki, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!abu_Daraja(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Microsoft_Word_SMS(Suna_Jurarre, "Faruwa_tushe") && Microsoft_Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Microsoft_Word_SMS(Suna_Jurarre, "Umarni_SMS") && Microsoft_Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Microsoft_Word_SMS(Suna_Jurarre, "Indes") && Microsoft_Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else Kasa_aiki_Daraja("지원하지 않는 한국어 Aiki 알림 호출"); return;
        }
        if (Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(Suna_Jurarre, "<init>")) {
            int 종류 = 한국어화면종(mamallaki), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (Mai_anfani_da_kwamfuta.화면너비() - 폭) / 2; 세로 = (Mai_anfani_da_kwamfuta.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { Kasa_aiki_Daraja("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), Dan_gutsuren_bayani_Daraja = 빼기(2); if (!화면객체(Dan_gutsuren_bayani_Daraja)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > Mai_anfani_da_kwamfuta.화면너비() - 가로 || 높이 > Mai_anfani_da_kwamfuta.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int Indes = Mai_anfani_da_kwamfuta.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (Indes < 1 || Indes > 32) { Kasa_aiki_Daraja("화면 Dan_gutsuren_bayani_Daraja 자리가 가득 찼습니다"); return; }
            힙[Dan_gutsuren_bayani_Daraja + 2] = Indes; 화면참조[Indes - 1] = Dan_gutsuren_bayani_Daraja;
            힙[Dan_gutsuren_bayani_Daraja + 5] = 가로; 힙[Dan_gutsuren_bayani_Daraja + 6] = 세로; 힙[Dan_gutsuren_bayani_Daraja + 7] = 폭; 힙[Dan_gutsuren_bayani_Daraja + 8] = 높이; 힙[Dan_gutsuren_bayani_Daraja + 10] = 2;
            힙[Dan_gutsuren_bayani_Daraja + 4] = 받이; 힙참조[Dan_gutsuren_bayani_Daraja + 4] = 1; 힙[Dan_gutsuren_bayani_Daraja + 12] = 1;
            Mai_anfani_da_kwamfuta.화면연결(1, Indes, 가로, 세로, 폭, 높이);
            if (종류 == 24) Mai_anfani_da_kwamfuta.화면연결(7, Indes, 2, 0, 0, 0);
            화면문자설정(Dan_gutsuren_bayani_Daraja, SMS); return;
        }
        if (Umarni_lambar_sirri != 182) { Kasa_aiki_Daraja("잘못된 한국어 화면 호출 Umarni"); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "Rubuta_SMS") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), Dan_gutsuren_bayani_Daraja = 빼기(2); if (화면객체(Dan_gutsuren_bayani_Daraja)) 화면문자설정(Dan_gutsuren_bayani_Daraja, SMS); return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "글읽기") && Microsoft_Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int Dan_gutsuren_bayani_Daraja = 빼기(2); if (화면객체(Dan_gutsuren_bayani_Daraja)) 넣기(화면문자읽기(Dan_gutsuren_bayani_Daraja), 2); return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "동작맡기기") && Microsoft_Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), Dan_gutsuren_bayani_Daraja = 빼기(2);
            if (화면객체(Dan_gutsuren_bayani_Daraja)) { 힙[Dan_gutsuren_bayani_Daraja + 4] = 받이; 힙참조[Dan_gutsuren_bayani_Daraja + 4] = 1; 힙[Dan_gutsuren_bayani_Daraja + 12] = 1; } return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "ƙara_Dan_gutsuren_bayani") && Microsoft_Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int yaro_Daraja = 빼기(2), 부모 = 빼기(2); if (!화면객체(yaro_Daraja) || !화면객체(부모)) return;
            if (Mai_anfani_da_kwamfuta.화면연결(2, 힙[부모 + 2], 힙[yaro_Daraja + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[yaro_Daraja + 11] = 부모; 힙참조[yaro_Daraja + 11] = 1; return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "자리정하기") && Microsoft_Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), Dan_gutsuren_bayani_Daraja = 빼기(2); if (!화면객체(Dan_gutsuren_bayani_Daraja)) return;
            if (Mai_anfani_da_kwamfuta.화면연결(1, 힙[Dan_gutsuren_bayani_Daraja + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[Dan_gutsuren_bayani_Daraja + 5] = 가로; 힙[Dan_gutsuren_bayani_Daraja + 6] = 세로; 힙[Dan_gutsuren_bayani_Daraja + 7] = 폭; 힙[Dan_gutsuren_bayani_Daraja + 8] = 높이; return;
        }
        if ((Microsoft_Word_SMS(Suna_Jurarre, "Nuna_taga") || Microsoft_Word_SMS(Suna_Jurarre, "Rufe")) && Microsoft_Word_SMS(서술상수, "()V")) {
            boolean Sarari_Daraja = Microsoft_Word_SMS(Suna_Jurarre, "Nuna_taga"); int Dan_gutsuren_bayani_Daraja = 빼기(2); if (!화면객체(Dan_gutsuren_bayani_Daraja)) return;
            if (Mai_anfani_da_kwamfuta.화면연결(Sarari_Daraja ? 3 : 4, 힙[Dan_gutsuren_bayani_Daraja + 2], Sarari_Daraja ? 1 : 0, 0, 0, 0) < 0) { Kasa_aiki_Daraja("화면은 Shigar_da_umarni_na_kwamfuta 명령에서 실행해야 합니다"); return; }
            힙[Dan_gutsuren_bayani_Daraja + 9] = Sarari_Daraja ? 1 : 0; return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "보이는가") && Microsoft_Word_SMS(서술상수, "()Z")) { int Dan_gutsuren_bayani_Daraja = 빼기(2); if (화면객체(Dan_gutsuren_bayani_Daraja)) 넣기(힙[Dan_gutsuren_bayani_Daraja + 9], 1); return; }
        Kasa_aiki_Daraja("지원하지 않는 한국어 화면 tsari_Daraja");
    }
    static void 화면호출(int mamallaki, int Suna_Jurarre, int 서술상수, int Umarni_lambar_sirri) {
        if (Microsoft_Word_SMS(mamallaki, "javax/swing/SwingUtilities")) {
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "invokeLater") && Microsoft_Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int abu_Manazarta = 빼기(2); if (!객체유효(abu_Manazarta)) return; if (나중수 == 8) { Kasa_aiki_Daraja("invokeLater queue full"); return; } 나중실행[나중수++] = abu_Manazarta; return; }
            if (Umarni_lambar_sirri == 184 && Microsoft_Word_SMS(Suna_Jurarre, "isEventDispatchThread") && Microsoft_Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            Kasa_aiki_Daraja("unsupported SwingUtilities method"); return;
        }
        if (Microsoft_Word_SMS(mamallaki, "java/awt/event/ActionEvent")) {
            int abu_Manazarta = 빼기(2); if (!abu_Daraja(abu_Manazarta, 29)) return;
            if (Microsoft_Word_SMS(Suna_Jurarre, "getSource") && Microsoft_Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[abu_Manazarta + 2], 2);
            else if (Microsoft_Word_SMS(Suna_Jurarre, "getActionCommand") && Microsoft_Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[abu_Manazarta + 2]), 2);
            else if (Microsoft_Word_SMS(Suna_Jurarre, "getID") && Microsoft_Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else Kasa_aiki_Daraja("unsupported ActionEvent method"); return;
        }
        if (Umarni_lambar_sirri == 183 && Microsoft_Word_SMS(Suna_Jurarre, "<init>")) {
            int 열수 = 0, SMS_Manazarta = 0;
            if (Microsoft_Word_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Manazarta = 빼기(2); }
            else if (Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Manazarta = 빼기(2);
            else if (Microsoft_Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Microsoft_Word_SMS(서술상수, "()V")) { Kasa_aiki_Daraja("unsupported Swing constructor"); return; }
            int abu_Manazarta = 빼기(2); if (!객체유효(abu_Manazarta)) return;
            if (힙[abu_Manazarta] == 30) { Kasa_aiki_Daraja("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(abu_Manazarta) || 열수 < 0) return;
            int asusu_Daraja = Mai_anfani_da_kwamfuta.화면연결(0, 힙[abu_Manazarta] - 23, 0, 0, 0, 0);
            if (asusu_Daraja < 1 || asusu_Daraja > 32) { Kasa_aiki_Daraja("GUI widget slots exhausted"); return; }
            힙[abu_Manazarta + 2] = asusu_Daraja; 화면참조[asusu_Daraja - 1] = abu_Manazarta; 힙[abu_Manazarta + 5] = 힙[abu_Manazarta] == 24 ? 130 : 16; 힙[abu_Manazarta + 6] = 힙[abu_Manazarta] == 24 ? 110 : 16;
            힙[abu_Manazarta + 7] = 힙[abu_Manazarta] == 24 ? 380 : 220; 힙[abu_Manazarta + 8] = 힙[abu_Manazarta] == 24 ? 240 : 28; 힙[abu_Manazarta + 10] = 1;
            화면문자설정(abu_Manazarta, SMS_Manazarta); return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "setText") || Microsoft_Word_SMS(Suna_Jurarre, "setTitle")) { int SMS_Manazarta = 빼기(2), abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta) && Microsoft_Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(abu_Manazarta, SMS_Manazarta); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "getText") || Microsoft_Word_SMS(Suna_Jurarre, "getTitle")) { int abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta) && Microsoft_Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(abu_Manazarta), 2); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "addActionListener") && Microsoft_Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta)) { 힙[abu_Manazarta + 4] = 수신참조; 힙참조[abu_Manazarta + 4] = 1; } return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "getContentPane") && Microsoft_Word_SMS(서술상수, "()Ljava/awt/Container;")) { int abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta)) 넣기(abu_Manazarta, 2); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "setLayout") && Microsoft_Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Zagaye_Manazarta = 빼기(2), abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta) && Zagaye_Manazarta != 0) Kasa_aiki_Daraja("only absolute layout (null) is supported"); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "add") && (Microsoft_Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Microsoft_Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Zagaye_Yanayi = Microsoft_Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Zagaye_Yanayi) 빼기(2);
            int yaro_Manazarta = 빼기(2), abu_Manazarta = 빼기(2); if (!화면객체(yaro_Manazarta) || !화면객체(abu_Manazarta)) return;
            if (Mai_anfani_da_kwamfuta.화면연결(2, 힙[abu_Manazarta + 2], 힙[yaro_Manazarta + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[yaro_Manazarta + 11] = abu_Manazarta; 힙참조[yaro_Manazarta + 11] = 1; if (!Zagaye_Yanayi) 넣기(yaro_Manazarta, 2); return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "setBounds") && Microsoft_Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Maɓallin_Y_Mai_tsarawa = 빼기(1), gamayyar_x = 빼기(1), abu_Manazarta = 빼기(2); if (!화면객체(abu_Manazarta)) return;
            if (Mai_anfani_da_kwamfuta.화면연결(1, 힙[abu_Manazarta + 2], gamayyar_x, Maɓallin_Y_Mai_tsarawa, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[abu_Manazarta + 5] = gamayyar_x; 힙[abu_Manazarta + 6] = Maɓallin_Y_Mai_tsarawa; 힙[abu_Manazarta + 7] = 너비; 힙[abu_Manazarta + 8] = 높이; return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "setSize") && Microsoft_Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), abu_Manazarta = 빼기(2); if (!화면객체(abu_Manazarta)) return;
            if (Mai_anfani_da_kwamfuta.화면연결(1, 힙[abu_Manazarta + 2], 힙[abu_Manazarta + 5], 힙[abu_Manazarta + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[abu_Manazarta + 7] = 너비; 힙[abu_Manazarta + 8] = 높이; } return;
        }
        if (Microsoft_Word_SMS(Suna_Jurarre, "setLocationRelativeTo") && Microsoft_Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), abu_Manazarta = 빼기(2); if (!화면객체(abu_Manazarta)) return; if (상대배치 != 0) { Kasa_aiki_Daraja("only screen centering supported"); return; } 힙[abu_Manazarta + 5] = (Mai_anfani_da_kwamfuta.화면너비() - 힙[abu_Manazarta + 7]) / 2; 힙[abu_Manazarta + 6] = (Mai_anfani_da_kwamfuta.화면높이() - 힙[abu_Manazarta + 8]) / 2; Mai_anfani_da_kwamfuta.화면연결(1, 힙[abu_Manazarta + 2], 힙[abu_Manazarta + 5], 힙[abu_Manazarta + 6], 힙[abu_Manazarta + 7], 힙[abu_Manazarta + 8]); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "setDefaultCloseOperation") && Microsoft_Word_SMS(서술상수, "(I)V")) { int doka = 빼기(1), abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta)) { if (doka < 0 || doka > 3) 예외던짐(9, "close policy"); else { 힙[abu_Manazarta + 10] = doka; Mai_anfani_da_kwamfuta.화면연결(7, 힙[abu_Manazarta + 2], doka, 0, 0, 0); } } return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "setVisible") && Microsoft_Word_SMS(서술상수, "(Z)V")) { int Tarin_bayani_Daraja = 빼기(1), abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta)) { int 처리값 = Mai_anfani_da_kwamfuta.화면연결(3, 힙[abu_Manazarta + 2], Tarin_bayani_Daraja, 0, 0, 0); if (처리값 < 0) Kasa_aiki_Daraja("Swing requires a standalone interactive command"); else 힙[abu_Manazarta + 9] = Tarin_bayani_Daraja; } return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "dispose") && Microsoft_Word_SMS(서술상수, "()V")) { int abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta)) { Mai_anfani_da_kwamfuta.화면연결(4, 힙[abu_Manazarta + 2], 0, 0, 0, 0); 힙[abu_Manazarta + 9] = 0; } return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "repaint") || Microsoft_Word_SMS(Suna_Jurarre, "validate")) { int abu_Manazarta = 빼기(2); if (!화면객체(abu_Manazarta) || !Microsoft_Word_SMS(서술상수, "()V")) return; Mai_anfani_da_kwamfuta.화면연결(1, 힙[abu_Manazarta + 2], 힙[abu_Manazarta + 5], 힙[abu_Manazarta + 6], 힙[abu_Manazarta + 7], 힙[abu_Manazarta + 8]); return; }
        if (Microsoft_Word_SMS(Suna_Jurarre, "isVisible") && Microsoft_Word_SMS(서술상수, "()Z")) { int abu_Manazarta = 빼기(2); if (화면객체(abu_Manazarta)) 넣기(힙[abu_Manazarta + 9], 1); return; }
        Kasa_aiki_Daraja("unsupported Swing method (native subset)");
    }
    static void 사건실행(int tageti_imel, int 사건번호, boolean 한국어) {
        if (tageti_imel < 1 || 힙[tageti_imel] < 32) { Kasa_aiki_Daraja("Java event listener required"); return; }
        int Fayil_Indes = Suna_tsari(힙[tageti_imel] - 32, 사건번호 == 0 ? (한국어 ? "gudanar_aiki" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Fayil_Indes < 0) { Kasa_aiki_Daraja("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; allo_Indes = 0; hira_Matsayi[0] = 1; allo_tara[0] = 0; 틀잠금[0] = Farko_allo[0] = 0; 바꿈요청 = false;
        for (int Warware_Indes = 0; Warware_Indes < 128; Warware_Indes++) { na_gida_Daraja[Warware_Indes] = na_gida_rubuta[Warware_Indes] = 0; }
        allo_tsari[0] = Fayil_Indes; 틀위치[0] = tsari_Fara[Fayil_Indes]; na_gida_Daraja[0] = tageti_imel; na_gida_rubuta[0] = 2;
        if (사건번호 != 0) { na_gida_Daraja[1] = 사건번호; na_gida_rubuta[1] = 2; }
        사건중 = true; gudanar_Umarni(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Kuskure) {
            if (나중수 > 0) { int tageti_imel = 나중실행[0], 한국어 = 나중한국어[0]; for (int Warware_Indes = 1; Warware_Indes < 나중수; Warware_Indes++) { 나중실행[Warware_Indes - 1] = 나중실행[Warware_Indes]; 나중한국어[Warware_Indes - 1] = 나중한국어[Warware_Indes]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(tageti_imel, 0, 한국어 != 0); continue; }
            if (Mai_anfani_da_kwamfuta.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = Mai_anfani_da_kwamfuta.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { Kasa_aiki_Daraja("GUI event I/O failed"); return; }
            int asusu_Daraja = 사건번호 & 65535; if (asusu_Daraja < 1 || asusu_Daraja > 32) continue; int abu_Manazarta = 화면참조[asusu_Daraja - 1]; if (abu_Manazarta == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[abu_Manazarta + 10] != 0) 힙[abu_Manazarta + 9] = 0;
                if (힙[abu_Manazarta + 10] == 3) for (int Warware_Indes = 0; Warware_Indes < 32; Warware_Indes++) if (화면참조[Warware_Indes] != 0 && 힙[화면참조[Warware_Indes]] == 24) Mai_anfani_da_kwamfuta.화면연결(4, Warware_Indes + 1, 0, 0, 0, 0);
            } else if (힙[abu_Manazarta + 4] != 0) {
                int README_Manazarta = kasafta_Wurin_adana(29, 2); if (Kuskure) return; 힙[README_Manazarta + 2] = abu_Manazarta; 힙[README_Manazarta + 3] = 힙[abu_Manazarta + 12]; 힙참조[README_Manazarta + 2] = 1; 사건실행(힙[abu_Manazarta + 4], README_Manazarta, 힙[abu_Manazarta + 12] != 0);
            }
        }
    }
    public static int Tafiyar_da() {
        if (Mai_anfani_da_kwamfuta.인수개수() == 1 && 자바도구.같음(Mai_anfani_da_kwamfuta.인수(0), "-version")) {
            Mai_anfani_da_kwamfuta.Yi_Rubutu("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (Mai_anfani_da_kwamfuta.인수개수() < 1) { Mai_anfani_da_kwamfuta.Yi_Rubutu("Usage: java CLASS [ARGS]\n"); return 2; }
        Mashigar_bayanai_Aji_Ma_ana = loda_Aji_Ma_ana(sauka_Harafi(Mai_anfani_da_kwamfuta.인수(0))); if (Kuskure || Mashigar_bayanai_Aji_Ma_ana < 0) return 1;
        int Mashigar_bayanai_maki_Daraja = Suna_tsari(Mashigar_bayanai_Aji_Ma_ana, "Tafiyar_da", "()V");
        boolean 한국어진입 = Mashigar_bayanai_maki_Daraja >= 0 && (tsari_isa[Mashigar_bayanai_maki_Daraja] & 9) == 9;
        if (!한국어진입) Mashigar_bayanai_maki_Daraja = Suna_tsari(Mashigar_bayanai_Aji_Ma_ana, "main", "([Ljava/lang/String;)V");
        if (Mashigar_bayanai_maki_Daraja < 0 || (tsari_isa[Mashigar_bayanai_maki_Daraja] & 9) != 9) Kasa_aiki_Daraja("public static void Tafiyar_da() or main(String[] args) required");
        if (Kuskure) return 1;
        int 인수 = kasafta_Wurin_adana(3, Mai_anfani_da_kwamfuta.인수개수() - 1); TSARI_Dan_gutsuren_bayani[인수] = -1;
        for (int 수 = 1; 수 < Mai_anfani_da_kwamfuta.인수개수() && !Kuskure; 수++) 힙[인수 + 1 + 수] = sauka_Harafi(Mai_anfani_da_kwamfuta.인수(수));
        allo_Indes = 0; allo_tsari[0] = Mashigar_bayanai_maki_Daraja; 틀위치[0] = tsari_Fara[Mashigar_bayanai_maki_Daraja]; na_gida_Daraja[0] = 한국어진입 ? 0 : 인수; na_gida_rubuta[0] = 한국어진입 ? 0 : 2;
        hira_Matsayi[0] = 1; hira_abu[0] = kasafta_Wurin_adana(13, 2);
        gudanar_Umarni(); if (!Kuskure) 화면사건들(); return Kuskure ? 1 : 0;
    }
}
