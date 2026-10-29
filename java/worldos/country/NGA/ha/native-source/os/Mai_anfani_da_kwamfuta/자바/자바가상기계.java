// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fayil/스택/Manazarta/Reshe 경계를 gudanar_Umarni 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fayil = new int[16384], Fayil_Suna_SMS = new int[64];
    static int[] Jurarre_tambari = new int[512], 상가 = new int[512], 상나 = new int[512], Zare_Manazarta = new int[512];
    static int[] tsari_Suna_SMS = new int[32], tsari_rubuta = new int[32], tsari_isa = new int[32];
    static int[] tsari_Fara = new int[32], tsari_Ƙarshe = new int[32], tsari_tara = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], tsari_Tubalin_aiki_rubuta = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] na_gida_Daraja = new int[4096], na_gida_rubuta = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] allo_tsari = new int[32], 틀위치 = new int[32], allo_tara = new int[32];
    static int[] 힙 = new int[8192];
    static int Girma, 읽기위치, 상수수, 함수수, Aji_Suna, allo_Indes = -1, 힙끝 = 1, 반환형;
    static boolean Kuskure;

    static void Kasa_aiki_Daraja(String Microsoft_Word_SMS) {
        if (!Kuskure) { Mai_anfani_da_kwamfuta.Yi_Rubutu("JVM error: "); Mai_anfani_da_kwamfuta.Yi_Rubutu(Microsoft_Word_SMS); Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10); }
        Kuskure = true;
    }
    static boolean darfi(int Tafiyar_da, int Tsawo_Daraja) { return Tafiyar_da >= 0 && Tsawo_Daraja >= 0 && Tafiyar_da <= Girma - Tsawo_Daraja; }
    static int bayit_Daraja() {
        if (!darfi(읽기위치, 1)) { Kasa_aiki_Daraja("truncated class file"); return 0; }
        return Fayil[읽기위치++];
    }
    static int 짧은수() { return bayit_Daraja() << 8 | bayit_Daraja(); }
    static int Lamba_mara() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int Tsawo_Daraja) { if (!darfi(읽기위치, Tsawo_Daraja)) Kasa_aiki_Daraja("invalid attribute size"); else 읽기위치 += Tsawo_Daraja; }
    static boolean Bincika_Jurarre(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || Jurarre_tambari[수] != 종류) { Kasa_aiki_Daraja("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Tafiyar_da, int Tsawo_Daraja, String Microsoft_Word_SMS) {
        if (!darfi(Tafiyar_da, Tsawo_Daraja) || Tsawo_Daraja != Microsoft_Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Tsawo_Daraja; 수++) if (Fayil[Tafiyar_da + 수] != Microsoft_Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Kuskure; 수++) { Bincika_Jurarre(짧은수(), 1); 건너(Lamba_mara()); }
    }
    static int Umarni_Tsawo(int Daraja) {
        if (Daraja == 16 || Daraja == 18 || Daraja == 21 || Daraja == 25 || Daraja == 54 || Daraja == 58 || Daraja == 188) return 2;
        if (Daraja == 17 || Daraja == 19 || Daraja == 132 || Daraja >= 153 && Daraja <= 167
            || Daraja >= 178 && Daraja <= 184 || Daraja == 187 || Daraja == 189 || Daraja == 192 || Daraja == 198 || Daraja == 199) return 3;
        if (Daraja >= 0 && Daraja <= 8 || Daraja >= 26 && Daraja <= 29 || Daraja >= 42 && Daraja <= 46 || Daraja == 50
            || Daraja >= 59 && Daraja <= 62 || Daraja >= 75 && Daraja <= 79 || Daraja == 83 || Daraja == 87 || Daraja == 89 || Daraja == 95
            || Daraja == 96 || Daraja == 100 || Daraja == 104 || Daraja == 108 || Daraja == 112 || Daraja == 116
            || Daraja == 120 || Daraja == 122 || Daraja == 124 || Daraja == 126 || Daraja == 128 || Daraja == 130
            || Daraja >= 145 && Daraja <= 147 || Daraja == 172 || Daraja == 176 || Daraja == 177 || Daraja == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (Lamba_mara() != 0xcafebabe) Kasa_aiki_Daraja("not a class file");
        int 부판 = 짧은수(), siga_Daraja = 짧은수();
        if (siga_Daraja < 45 || siga_Daraja > 52 || 부판 != 0) Kasa_aiki_Daraja("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { Kasa_aiki_Daraja("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !Kuskure; 수++) {
            int 종류 = bayit_Daraja(); Jurarre_tambari[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = Lamba_mara();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else Kasa_aiki_Daraja("unsupported constant type");
        }
        int izini_Daraja = 짧은수();
        if ((izini_Daraja & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) Kasa_aiki_Daraja("unsupported class flags");
        Aji_Suna = Aji_Suna_SMS(짧은수());
        if (!Microsoft_Word_SMS(Aji_Suna_SMS(짧은수()), "java/lang/Object")) Kasa_aiki_Daraja("inheritance unsupported");
        if (짧은수() != 0) Kasa_aiki_Daraja("interfaces unsupported");
        if (짧은수() != 0) Kasa_aiki_Daraja("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { Kasa_aiki_Daraja("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !Kuskure; 수++) {
            tsari_isa[수] = 짧은수(); tsari_Suna_SMS[수] = 짧은수(); tsari_rubuta[수] = 짧은수();
            Bincika_Jurarre(tsari_Suna_SMS[수], 1); 서술읽기(수);
            if ((tsari_isa[수] & (0x100 | 0x400 | 0x20)) != 0) Kasa_aiki_Daraja("native, abstract and synchronized methods unsupported");
            if ((tsari_isa[수] & 8) == 0 && !Microsoft_Word_SMS(tsari_Suna_SMS[수], "<init>")) Kasa_aiki_Daraja("instance methods unsupported");
            if (Microsoft_Word_SMS(tsari_Suna_SMS[수], "<clinit>")) Kasa_aiki_Daraja("class initializers unsupported");
            for (int kyamarar_gaba_Daraja = 0; kyamarar_gaba_Daraja < 수; kyamarar_gaba_Daraja++) if (같은말(tsari_Suna_SMS[kyamarar_gaba_Daraja], tsari_Suna_SMS[수]) && 같은말(tsari_rubuta[kyamarar_gaba_Daraja], tsari_rubuta[수])) Kasa_aiki_Daraja("duplicate method");
            int 개수 = 짧은수();
            for (int siffofi_Daraja = 0; siffofi_Daraja < 개수 && !Kuskure; siffofi_Daraja++) {
                int Suna = 짧은수(), Tsawo_Daraja = Lamba_mara(), Tafiyar_da = 읽기위치;
                if (!darfi(Tafiyar_da, Tsawo_Daraja)) { Kasa_aiki_Daraja("truncated method attribute"); break; }
                if (Microsoft_Word_SMS(Suna, "Code")) {
                    if (tsari_Fara[수] != 0) Kasa_aiki_Daraja("duplicate Code attribute");
                    tsari_tara[수] = 짧은수(); 함수지역[수] = 짧은수(); int lambar_sirri_Tsawo = Lamba_mara();
                    if (tsari_tara[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || lambar_sirri_Tsawo < 1 || lambar_sirri_Tsawo > 8192) Kasa_aiki_Daraja("method memory limits exceeded");
                    tsari_Fara[수] = 읽기위치; 건너(lambar_sirri_Tsawo); tsari_Ƙarshe[수] = 읽기위치;
                    if (짧은수() != 0) Kasa_aiki_Daraja("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Tafiyar_da + Tsawo_Daraja) Kasa_aiki_Daraja("Code attribute size mismatch");
                } else 건너(Tsawo_Daraja);
            }
            if (tsari_Fara[수] == 0) Kasa_aiki_Daraja("missing Code attribute");
            int rami_Mashigar_bayanai = tsari_Fara[수];
            while (rami_Mashigar_bayanai < tsari_Ƙarshe[수] && !Kuskure) {
                int Tsawo_Daraja = Umarni_Tsawo(Fayil[rami_Mashigar_bayanai]);
                if (Tsawo_Daraja == 0 || Tsawo_Daraja > tsari_Ƙarshe[수] - rami_Mashigar_bayanai) { Kasa_aiki_Daraja("unsupported or truncated bytecode"); break; }
                경계[rami_Mashigar_bayanai] = 수 + 1; rami_Mashigar_bayanai += Tsawo_Daraja;
            }
            // 실행하지 않는 경로에도 잘못된 Reshe 목적지를 허용하지 않는다.
            rami_Mashigar_bayanai = tsari_Fara[수];
            while (rami_Mashigar_bayanai < tsari_Ƙarshe[수] && !Kuskure) {
                int Daraja = Fayil[rami_Mashigar_bayanai];
                if (Daraja >= 153 && Daraja <= 167 || Daraja == 198 || Daraja == 199) {
                    int Zangon_ƙarshe_Daraja = rami_Mashigar_bayanai + (short)(Fayil[rami_Mashigar_bayanai + 1] << 8 | Fayil[rami_Mashigar_bayanai + 2]);
                    if (Zangon_ƙarshe_Daraja < tsari_Fara[수] || Zangon_ƙarshe_Daraja >= tsari_Ƙarshe[수] || 경계[Zangon_ƙarshe_Daraja] != 수 + 1) Kasa_aiki_Daraja("invalid branch target");
                }
                rami_Mashigar_bayanai += Umarni_Tsawo(Daraja);
            }
        }
        if (!Kuskure) 속성건너();
        if (읽기위치 != Girma) Kasa_aiki_Daraja("extra class file data");
    }
    static int kasafta_Wurin_adana(int 종류, int Tsawo_Daraja) {
        if (Tsawo_Daraja < 0 || Tsawo_Daraja > 힙.length - 힙끝 - 2) { Kasa_aiki_Daraja("object heap exhausted or negative array size"); return 0; }
        int Manazarta = 힙끝; 힙끝 += Tsawo_Daraja + 2; 힙[Manazarta] = 종류; 힙[Manazarta + 1] = Tsawo_Daraja;
        return Manazarta;
    }
    static boolean abu_Daraja(int Manazarta, int 종류) {
        if (Manazarta < 1 || Manazarta >= 힙끝 - 1 || 힙[Manazarta] != 종류) { Kasa_aiki_Daraja("null or invalid object reference"); return false; }
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
        if (allo_Indes == 31) { Kasa_aiki_Daraja("call stack limit (32)"); return; }
        int 다음 = allo_Indes + 1;
        for (int 수 = 0; 수 < 128; 수++) na_gida_rubuta[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[AIKI_Daraja] - 1; 수 >= 0; 수--) {
            na_gida_Daraja[다음 * 128 + 수] = 빼기(tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 수]); na_gida_rubuta[다음 * 128 + 수] = tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 수];
        }
        allo_Indes = 다음; allo_tsari[allo_Indes] = AIKI_Daraja; 틀위치[allo_Indes] = tsari_Fara[AIKI_Daraja]; allo_tara[allo_Indes] = 0;
    }
    static void 반환(int rubuta_Daraja) {
        if (rubuta_Daraja != 함수반환[allo_tsari[allo_Indes]]) { Kasa_aiki_Daraja("return type mismatch"); return; }
        int Daraja = rubuta_Daraja == 0 ? 0 : 빼기(rubuta_Daraja);
        allo_Indes--; if (allo_Indes >= 0 && rubuta_Daraja != 0) 넣기(Daraja, rubuta_Daraja);
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
                if (Daraja < 1 || Daraja > 127) { Kasa_aiki_Daraja("file stream paths currently require ASCII"); return; }
                watsuwa_Fayil_Suna[rami_Mashigar_bayanai] = Daraja;
            }
            watsuwa_Fayil_Suna[Tsawo_Daraja] = 0;
            int 서술자 = Mai_anfani_da_kwamfuta.파일서술자열기(watsuwa_Fayil_Suna, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { Kasa_aiki_Daraja("FileNotFoundException: file open failed"); return; }
            힙[watsuwa_Daraja + 2] = 서술자; 힙[watsuwa_Daraja + 3] = 1;
            return;
        }
        if (Umarni != 182) { Kasa_aiki_Daraja("invalid file stream invocation"); return; }
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
            if (결과 < -1) Kasa_aiki_Daraja("IOException: read failed"); else 넣기(결과, 1);
        } else if (Mai_anfani_da_kwamfuta.파일한바이트쓰기(서술자, Daraja) != 1) Kasa_aiki_Daraja("IOException: write failed");
    }
    static void Kira_tsari(int Indes, int Umarni) {
        if (!Bincika_Jurarre(Indes, 10)) return;
        int mamallaki_Daraja = Aji_Suna_SMS(상가[Indes]), Suna = Manazarta_Suna(상나[Indes]), zubi_Daraja = Manazarta_rubuta(상나[Indes]);
        if (Kuskure) return;
        if (같은말(mamallaki_Daraja, Aji_Suna)) {
            if (Umarni != 184) { Kasa_aiki_Daraja("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Suna, tsari_Suna_SMS[수]) && 같은말(zubi_Daraja, tsari_rubuta[수])) {
                if ((tsari_isa[수] & 8) == 0) Kasa_aiki_Daraja("method is not static"); else 호출(수);
                return;
            }
            Kasa_aiki_Daraja("NoSuchMethodError"); return;
        }
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
        Kasa_aiki_Daraja("unsupported library method");
    }
    static int TSARI_rami(int Manazarta, int Alamar_karkashin_harafi_Daraja, int rubuta_Daraja) {
        if (!abu_Daraja(Manazarta, rubuta_Daraja)) return 0;
        if (Alamar_karkashin_harafi_Daraja < 0 || Alamar_karkashin_harafi_Daraja >= 힙[Manazarta + 1]) { Kasa_aiki_Daraja("ArrayIndexOutOfBoundsException"); return 0; }
        return Manazarta + 2 + Alamar_karkashin_harafi_Daraja;
    }
    static void gudanar_Umarni() {
        int 남음 = 500000;
        while (allo_Indes >= 0 && !Kuskure) {
            if (--남음 == 0) { Kasa_aiki_Daraja("instruction limit (500000)"); break; }
            int Tafiyar_da = 틀위치[allo_Indes], Daraja = 명바();
            if (Kuskure) break;
            if (Daraja == 0) continue;
            if (Daraja == 1) { 넣기(0, 2); continue; }
            if (Daraja >= 2 && Daraja <= 8) { 넣기(Daraja - 3, 1); continue; }
            if (Daraja == 16) { 넣기((byte)명바(), 1); continue; }
            if (Daraja == 17) { 넣기((short)명짧(), 1); continue; }
            if (Daraja == 18 || Daraja == 19) {
                int 수 = Daraja == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) Kasa_aiki_Daraja("invalid ldc constant");
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
            if (Daraja == 46 || Daraja == 50) {
                int Alamar_karkashin_harafi_Daraja = 빼기(1), Manazarta = 빼기(2), rami_Mashigar_bayanai = TSARI_rami(Manazarta, Alamar_karkashin_harafi_Daraja, Daraja == 46 ? 2 : 3);
                if (!Kuskure) 넣기(힙[rami_Mashigar_bayanai], Daraja == 46 ? 1 : 2); continue;
            }
            if (Daraja == 79 || Daraja == 83) {
                int abu_Dan_gutsuren_bayani = 빼기(Daraja == 79 ? 1 : 2), Alamar_karkashin_harafi_Daraja = 빼기(1), Manazarta = 빼기(2), rami_Mashigar_bayanai = TSARI_rami(Manazarta, Alamar_karkashin_harafi_Daraja, Daraja == 79 ? 2 : 3);
                if (Daraja == 83 && abu_Dan_gutsuren_bayani != 0) abu_Daraja(abu_Dan_gutsuren_bayani, 1);
                if (!Kuskure) 힙[rami_Mashigar_bayanai] = abu_Dan_gutsuren_bayani; continue;
            }
            if (Daraja == 87) { 빼기(0); continue; }
            if (Daraja == 89) { int 가 = 빼기(0), rubuta_Daraja = 반환형; 넣기(가, rubuta_Daraja); 넣기(가, rubuta_Daraja); continue; }
            if (Daraja == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (Daraja == 178) {
                int 수 = 명짧(); if (!Bincika_Jurarre(수, 9)) continue;
                if (!Microsoft_Word_SMS(Aji_Suna_SMS(상가[수]), "java/lang/System") || !Microsoft_Word_SMS(Manazarta_Suna(상나[수]), "out")
                    || !Microsoft_Word_SMS(Manazarta_rubuta(상나[수]), "Ljava/io/PrintStream;")) Kasa_aiki_Daraja("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (Daraja == 182 || Daraja == 183 || Daraja == 184) { Kira_tsari(명짧(), Daraja); continue; }
            if (Daraja == 187) {
                int Suna = Aji_Suna_SMS(명짧());
                if (Microsoft_Word_SMS(Suna, "java/lang/StringBuilder")) 넣기(kasafta_Wurin_adana(4, 1), 2);
                else if (Microsoft_Word_SMS(Suna, "java/io/FileInputStream") || Microsoft_Word_SMS(Suna, "java/io/FileOutputStream")) {
                    int Manazarta = kasafta_Wurin_adana(Microsoft_Word_SMS(Suna, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Kuskure) { 힙[Manazarta + 2] = -1; 넣기(Manazarta, 2); }
                } else Kasa_aiki_Daraja("unsupported object construction");
                continue;
            }
            if (Daraja == 188 || Daraja == 189) {
                if (Daraja == 188) { if (명바() != 10) Kasa_aiki_Daraja("only int[] newarray is supported"); }
                else if (!Microsoft_Word_SMS(Aji_Suna_SMS(명짧()), "java/lang/String")) Kasa_aiki_Daraja("only String[] anewarray is supported");
                int Tsawo_Daraja = 빼기(1); 넣기(kasafta_Wurin_adana(Daraja == 188 ? 2 : 3, Tsawo_Daraja), 2); continue;
            }
            if (Daraja == 190) {
                int Manazarta = 빼기(2);
                if (Manazarta < 1 || Manazarta >= 힙끝 - 1 || (힙[Manazarta] != 2 && 힙[Manazarta] != 3)) Kasa_aiki_Daraja("null or invalid array");
                else 넣기(힙[Manazarta + 1], 1); continue;
            }
            if (Daraja == 192) {
                int Suna = Aji_Suna_SMS(명짧()), Manazarta = 빼기(2);
                if (!Microsoft_Word_SMS(Suna, "java/lang/String")) Kasa_aiki_Daraja("unsupported checkcast");
                else if (Manazarta != 0) abu_Daraja(Manazarta, 1);
                넣기(Manazarta, 2); continue;
            }
            Kasa_aiki_Daraja("unsupported bytecode");
        }
    }
    public static int Tafiyar_da() {
        if (Mai_anfani_da_kwamfuta.인수개수() == 1 && 자바도구.같음(Mai_anfani_da_kwamfuta.인수(0), "-version")) {
            Mai_anfani_da_kwamfuta.Yi_Rubutu("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (Mai_anfani_da_kwamfuta.인수개수() < 1) { Mai_anfani_da_kwamfuta.Yi_Rubutu("Usage: java CLASS [ARGS]\n"); return 2; }
        int Tsawo_Daraja = 자바도구.Suna(Fayil_Suna_SMS, Mai_anfani_da_kwamfuta.인수(0));
        if (Tsawo_Daraja < 1 || Tsawo_Daraja > 57) { Mai_anfani_da_kwamfuta.Yi_Rubutu("java: invalid class name\n"); return 2; }
        Fayil_Suna_SMS[Tsawo_Daraja] = '.'; Fayil_Suna_SMS[Tsawo_Daraja + 1] = 'c'; Fayil_Suna_SMS[Tsawo_Daraja + 2] = 'l'; Fayil_Suna_SMS[Tsawo_Daraja + 3] = 'a'; Fayil_Suna_SMS[Tsawo_Daraja + 4] = 's'; Fayil_Suna_SMS[Tsawo_Daraja + 5] = 's';
        Girma = Mai_anfani_da_kwamfuta.파일읽기(Fayil_Suna_SMS, Fayil);
        if (Girma < 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("java: cannot read class: "); 자바도구.수쓰기(Girma); Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10); return 1; }
        클래스읽기(); if (Kuskure) return 1;
        int Harafi_Suna = Jurarre_SMS(Aji_Suna);
        if (!Kuskure && 힙[Harafi_Suna + 1] != Tsawo_Daraja) Kasa_aiki_Daraja("class name does not match file");
        for (int 수 = 0; 수 < Tsawo_Daraja && !Kuskure; 수++) if (힙[Harafi_Suna + 2 + 수] != Fayil_Suna_SMS[수]) Kasa_aiki_Daraja("class name does not match file");
        int Mashigar_bayanai_maki_Daraja = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Microsoft_Word_SMS(tsari_Suna_SMS[수], "main") && Microsoft_Word_SMS(tsari_rubuta[수], "([Ljava/lang/String;)V") && (tsari_isa[수] & 9) == 9) Mashigar_bayanai_maki_Daraja = 수;
        if (Mashigar_bayanai_maki_Daraja < 0) Kasa_aiki_Daraja("public static void main(String[] args) required");
        if (Kuskure) return 1;
        int 인수 = kasafta_Wurin_adana(3, Mai_anfani_da_kwamfuta.인수개수() - 1);
        for (int 수 = 1; 수 < Mai_anfani_da_kwamfuta.인수개수() && !Kuskure; 수++) 힙[인수 + 1 + 수] = sauka_Harafi(Mai_anfani_da_kwamfuta.인수(수));
        allo_Indes = 0; allo_tsari[0] = Mashigar_bayanai_maki_Daraja; 틀위치[0] = tsari_Fara[Mashigar_bayanai_maki_Daraja]; na_gida_Daraja[0] = 인수; na_gida_rubuta[0] = 2;
        gudanar_Umarni(); return Kuskure ? 1 : 0;
    }
}
