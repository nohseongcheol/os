// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fáìlì/스택/Ìtọ́ka/ẹ̀ka 경계를 ṣiṣẹ́_àṣẹ 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fáìlì = new int[16 * 16384], 임시파일 = new int[16384], fáìlì_orúkọ_SMS = new int[512];
    static int[] aláìṣeéyípadà_sàmì = new int[8192], 상가 = new int[8192], 상나 = new int[8192], fọ́nrán_Ìtọ́ka = new int[8192];
    static int[] ìlànà_orúkọ_SMS = new int[512], ìlànà_irú = new int[512], ìlànà_wáyè_sí = new int[512], ìlànà_Oníǹkan = new int[512];
    static int[] ìlànà_bẹ̀rẹ̀ = new int[512], ìlànà_parí = new int[512], ìlànà_kójọ = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], ìlànà_ágúmẹ́ntì_irú = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] agbègbè_iye = new int[16384], agbègbè_irú = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] férèmù_ìlànà = new int[128], 틀위치 = new int[128], férèmù_kójọ = new int[128], férèmù_ìtọ́sọ́nà = new int[128], pàjùbà_férèmù = new int[128];
    static int[] ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ = new int[16], ọ̀wọ́_Ìsọ̀tumọ̀_ìwọn = new int[16], 종부모 = new int[16], ọ̀wọ́_Ìsọ̀tumọ̀_ipò = new int[16], 종칸수 = new int[16], pàjùbà_ọ̀wọ́_Ìsọ̀tumọ̀ = new int[16];
    static int[] ọ̀wọ́_atọ́kùn = new int[16 * 16], 종접면수 = new int[16];
    static int[] ààyè_ìfàyọkàsí_orúkọ = new int[512], ààyè_ìfàyọkàsí_irú = new int[512], ààyè_ìfàyọkàsí_Oníǹkan = new int[512], ààyè_ìfàyọkàsí_ìyànda = new int[512], 칸위치 = new int[512], ààyè_ìfàyọkàsí_détà = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ÀRÉÈ_ìdá_ìpìlẹ̀ = new int[32768], Store_nọ́ńbà_odindi = new int[256];
    static int Ìwọ̀n, 읽기위치, 함수수, ọ̀wọ́_orúkọ, férèmù_wá_atọ̀ka_àkóónú = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, ìgbéwọlé_ọ̀wọ́_Ìsọ̀tumọ̀;
    static int[] èròjà_atẹ̀lélànà_férèmù = new int[4], èròjà_atẹ̀lélànà_ipò = new int[4], èròjà_atẹ̀lélànà_nǹkan = new int[4], èròjà_atẹ̀lélànà_àfojúsùn = new int[4], 가닥대기 = new int[4];
    static boolean àṣìṣe, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], ọ̀wọ́_èròjà_atẹ̀lélànà = new int[16];

    static void ìkùnà_iye(String Ọ̀rọ̀_SMS) {
        if (àṣìṣe) return;
        int 분류코드 = 0;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "NullPointerException") || 자바도구.같음(Ọ̀rọ̀_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "IOException: stream closed") || 자바도구.같음(Ọ̀rọ̀_SMS, "IOException: read failed") || 자바도구.같음(Ọ̀rọ̀_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Ọ̀rọ̀_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && férèmù_wá_atọ̀ka_àkóónú >= 0) { 예외던짐(분류코드, Ọ̀rọ̀_SMS); return; }
        aṣàmúlò.Kọ("JVM error: "); aṣàmúlò.Kọ(Ọ̀rọ̀_SMS); aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10); àṣìṣe = true;
    }
    static boolean ní_ṣókí(int Rọ́ọ̀nù, int gígùn_iye) {
        if (Rọ́ọ̀nù < 0 || Rọ́ọ̀nù >= Fáìlì.length || gígùn_iye < 0) return false;
        int ọ̀wọ́_Ìsọ̀tumọ̀ = Rọ́ọ̀nù / 16384;
        return Rọ́ọ̀nù % 16384 <= ọ̀wọ́_Ìsọ̀tumọ̀_ìwọn[ọ̀wọ́_Ìsọ̀tumọ̀] && gígùn_iye <= ọ̀wọ́_Ìsọ̀tumọ̀_ìwọn[ọ̀wọ́_Ìsọ̀tumọ̀] - Rọ́ọ̀nù % 16384;
    }
    static int báìtì_iye() {
        if (!ní_ṣókí(읽기위치, 1)) { ìkùnà_iye("truncated class file"); return 0; }
        return Fáìlì[읽기위치++];
    }
    static int 짧은수() { return báìtì_iye() << 8 | báìtì_iye(); }
    static int nọ́ńbà_odindi() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int gígùn_iye) { if (!ní_ṣókí(읽기위치, gígùn_iye)) ìkùnà_iye("invalid attribute size"); else 읽기위치 += gígùn_iye; }
    static boolean ṣàyẹ̀wò_aláìṣeéyípadà(int 수, int 종류) {
        if (수 <= 0 || 수 >= aláìṣeéyípadà_sàmì.length || aláìṣeéyípadà_sàmì[수] != 종류) { ìkùnà_iye("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Rọ́ọ̀nù, int gígùn_iye, String Ọ̀rọ̀_SMS) {
        if (!ní_ṣókí(Rọ́ọ̀nù, gígùn_iye)) return false;
        int 읽는자리 = Rọ́ọ̀nù, 끝 = Rọ́ọ̀nù + gígùn_iye;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ọ̀rọ̀_SMS.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = Ọ̀rọ̀_SMS.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú);
            if (kóòdù_ẹyọ_ọ̀rọ̀ > 0 && kóòdù_ẹyọ_ọ̀rọ̀ < 128) { if (읽는자리 >= 끝 || Fáìlì[읽는자리++] != kóòdù_ẹyọ_ọ̀rọ̀) return false; }
            else if (kóòdù_ẹyọ_ọ̀rọ̀ < 2048) {
                if (읽는자리 + 2 > 끝 || Fáìlì[읽는자리++] != (192 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 6)) || Fáìlì[읽는자리++] != (128 | (kóòdù_ẹyọ_ọ̀rọ̀ & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fáìlì[읽는자리++] != (224 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 12)) || Fáìlì[읽는자리++] != (128 | ((kóòdù_ẹyọ_ọ̀rọ̀ >> 6) & 63)) || Fáìlì[읽는자리++] != (128 | (kóòdù_ẹyọ_ọ̀rọ̀ & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Ọ̀rọ̀_SMS(int aláìṣeéyípadà_iye, String Ọ̀rọ̀_SMS) { return ṣàyẹ̀wò_aláìṣeéyípadà(aláìṣeéyípadà_iye, 1) && 구간(상가[aláìṣeéyípadà_iye], 상나[aláìṣeéyípadà_iye], Ọ̀rọ̀_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!ṣàyẹ̀wò_aláìṣeéyípadà(가, 1) || !ṣàyẹ̀wò_aláìṣeéyípadà(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Fáìlì[상가[가] + 수] != Fáìlì[상가[나] + 수]) return false;
        return true;
    }
    static int ọ̀wọ́_orúkọ_SMS(int 수) { return ṣàyẹ̀wò_aláìṣeéyípadà(수, 7) && ṣàyẹ̀wò_aláìṣeéyípadà(상가[수], 1) ? 상가[수] : 0; }
    static int Ìtọ́ka_orúkọ(int 수) { return ṣàyẹ̀wò_aláìṣeéyípadà(수, 12) && ṣàyẹ̀wò_aláìṣeéyípadà(상가[수], 1) ? 상가[수] : 0; }
    static int Ìtọ́ka_irú(int 수) { return ṣàyẹ̀wò_aláìṣeéyípadà(수, 12) && ṣàyẹ̀wò_aláìṣeéyípadà(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean òfìfo_irú) {
        if (읽기위치 >= 끝) { ìkùnà_iye("invalid descriptor"); return 0; }
        int iye = báìtì_iye();
        if (iye == 'V' && òfìfo_irú) return 0;
        if (iye == 'I' || iye == 'B' || iye == 'C' || iye == 'S' || iye == 'Z') return 1;
        if (iye == '[') { 서술형(끝, false); return 2; }
        if (iye == 'L') {
            int Rọ́ọ̀nù = 읽기위치;
            while (읽기위치 < 끝 && Fáìlì[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Rọ́ọ̀nù) ìkùnà_iye("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        ìkùnà_iye("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int ÀKÀNṢEFỌMÚLÀ_iye) {
        int 이전 = 읽기위치, 수 = ìlànà_irú[ÀKÀNṢEFỌMÚLÀ_iye];
        if (!ṣàyẹ̀wò_aláìṣeéyípadà(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (báìtì_iye() != '(') ìkùnà_iye("invalid method descriptor");
        int 개수 = 0;
        while (!àṣìṣe && 읽기위치 < 끝 && Fáìlì[읽기위치] != ')') {
            if (개수 == 16) { ìkùnà_iye("too many method arguments"); break; }
            ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || báìtì_iye() != ')') ìkùnà_iye("invalid method descriptor");
        함수반환[ÀKÀNṢEFỌMÚLÀ_iye] = 서술형(끝, true); 함수인수수[ÀKÀNṢEFỌMÚLÀ_iye] = 개수;
        if (읽기위치 != 끝) ìkùnà_iye("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int iye = 짧은수(); return iye == 0 ? 0 : 현재읽는종 * 512 + iye; }
    static int 명상수() { return ìlànà_Oníǹkan[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !àṣìṣe; 수++) { ṣàyẹ̀wò_aláìṣeéyípadà(상번호(), 1); 건너(nọ́ńbà_odindi()); }
    }
    static int àṣẹ_gígùn(int iye) {
        if (iye == 16 || iye == 18 || iye == 21 || iye == 25 || iye == 54 || iye == 58 || iye == 188) return 2;
        if (iye == 17 || iye == 19 || iye == 132 || iye >= 153 && iye <= 167
            || iye >= 178 && iye <= 184 || iye == 187 || iye == 189 || iye == 192 || iye == 193 || iye == 198 || iye == 199) return 3;
        if (iye == 185 || iye == 200) return 5;
        if (iye >= 0 && iye <= 8 || iye >= 26 && iye <= 29 || iye >= 42 && iye <= 46 || iye >= 50 && iye <= 53
            || iye >= 59 && iye <= 62 || iye >= 75 && iye <= 79 || iye >= 83 && iye <= 95
            || iye == 96 || iye == 100 || iye == 104 || iye == 108 || iye == 112 || iye == 116
            || iye == 120 || iye == 122 || iye == 124 || iye == 126 || iye == 128 || iye == 130
            || iye >= 145 && iye <= 147 || iye == 172 || iye == 176 || iye == 177 || iye == 190 || iye == 191
            || iye == 194 || iye == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!ní_ṣókí(읽는자리, 4)) { ìkùnà_iye("truncated bytecode operand"); return 0; }
        return Fáìlì[읽는자리] << 24 | Fáìlì[읽는자리 + 1] << 16 | Fáìlì[읽는자리 + 2] << 8 | Fáìlì[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Rọ́ọ̀nù, int 끝) {
        int iye = Fáìlì[읽는자리], gígùn_iye = àṣẹ_gígùn(iye);
        if (iye == 170 || iye == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Rọ́ọ̀nù) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (iye == 170 ? 12 : 8)) return 0;
            int 항목수 = iye == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            gígùn_iye = 기준자리 - 읽는자리 + (iye == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (iye == 196 && 읽는자리 + 1 < 끝) {
            int Ọ̀rọ̀_détà = Fáìlì[읽는자리 + 1]; gígùn_iye = Ọ̀rọ̀_détà == 132 ? 6 : (Ọ̀rọ̀_détà == 21 || Ọ̀rọ̀_détà == 25 || Ọ̀rọ̀_détà == 54 || Ọ̀rọ̀_détà == 58) ? 4 : 0;
        }
        return gígùn_iye > 0 && gígùn_iye <= 끝 - 읽는자리 ? gígùn_iye : 0;
    }
    static void ṣàyẹ̀wò_èbúté_iye(int èbúté_iye, int ÀKÀNṢEFỌMÚLÀ_iye) {
        if (èbúté_iye < ìlànà_bẹ̀rẹ̀[ÀKÀNṢEFỌMÚLÀ_iye] || èbúté_iye >= ìlànà_parí[ÀKÀNṢEFỌMÚLÀ_iye] || 경계[èbúté_iye] != ÀKÀNṢEFỌMÚLÀ_iye + 1) ìkùnà_iye("invalid branch target");
    }
    static void 클래스읽기(int ọ̀wọ́_Ìsọ̀tumọ̀) {
        현재읽는종 = ọ̀wọ́_Ìsọ̀tumọ̀; 읽기위치 = ọ̀wọ́_Ìsọ̀tumọ̀ * 16384; Ìwọ̀n = 읽기위치 + ọ̀wọ́_Ìsọ̀tumọ̀_ìwọn[ọ̀wọ́_Ìsọ̀tumọ̀];
        if (nọ́ńbà_odindi() != 0xcafebabe) { ìkùnà_iye("not a class file"); return; }
        int 부판 = 짧은수(), ẹ̀yà_iye = 짧은수();
        if (ẹ̀yà_iye < 45 || ẹ̀yà_iye > 52 || 부판 != 0) { ìkùnà_iye("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = ọ̀wọ́_Ìsọ̀tumọ̀ * 512;
        if (상수수 < 1 || 상수수 > 512) { ìkùnà_iye("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !àṣìṣe; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = báìtì_iye(); aláìṣeéyípadà_sàmì[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = nọ́ńbà_odindi();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else ìkùnà_iye("unsupported constant type");
        }
        int Ìyànda_iye = 짧은수();
        if ((Ìyànda_iye & (0x2000 | 0x4000)) != 0) ìkùnà_iye("annotation/enum class unsupported");
        ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ọ̀wọ́_Ìsọ̀tumọ̀] = ọ̀wọ́_orúkọ_SMS(상번호());
        종부모[ọ̀wọ́_Ìsọ̀tumọ̀] = ọ̀wọ́_orúkọ_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { ìkùnà_iye("interface count limit"); return; }
        종접면수[ọ̀wọ́_Ìsọ̀tumọ̀] = 접면수;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 접면수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ọ̀wọ́_atọ́kùn[ọ̀wọ́_Ìsọ̀tumọ̀ * 16 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = ọ̀wọ́_orúkọ_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { ìkùnà_iye("field count limit (512)"); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 필드수 && !àṣìṣe; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int fáìlì_wá_atọ̀ka_àkóónú = 칸수++; ààyè_ìfàyọkàsí_Oníǹkan[fáìlì_wá_atọ̀ka_àkóónú] = ọ̀wọ́_Ìsọ̀tumọ̀; ààyè_ìfàyọkàsí_ìyànda[fáìlì_wá_atọ̀ka_àkóónú] = 짧은수(); ààyè_ìfàyọkàsí_orúkọ[fáìlì_wá_atọ̀ka_àkóónú] = 상번호(); ààyè_ìfàyọkàsí_irú[fáìlì_wá_atọ̀ka_àkóónú] = 상번호();
            ṣàyẹ̀wò_aláìṣeéyípadà(ààyè_ìfàyọkàsí_orúkọ[fáìlì_wá_atọ̀ka_àkóónú], 1); ṣàyẹ̀wò_aláìṣeéyípadà(ààyè_ìfàyọkàsí_irú[fáìlì_wá_atọ̀ka_àkóónú], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[ààyè_ìfàyọkàsí_irú[fáìlì_wá_atọ̀ka_àkóónú]]; int 분류코드 = 서술형(읽기위치 + 상나[ààyè_ìfàyọkàsí_irú[fáìlì_wá_atọ̀ka_àkóónú]], false); 읽기위치 = 보존값;
            if ((ààyè_ìfàyọkàsí_ìyànda[fáìlì_wá_atọ̀ka_àkóónú] & 8) == 0) 칸위치[fáìlì_wá_atọ̀ka_àkóónú] = 종칸수[ọ̀wọ́_Ìsọ̀tumọ̀]++;
            int àwòmọ́_détà = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < àwòmọ́_détà && !àṣìṣe; 안쪽자리++) {
                int orúkọ_aláìṣeéyípadà = 상번호(), 유효길이 = nọ́ńbà_odindi();
                if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "ConstantValue") && 유효길이 == 2) {
                    int détà_iye = 상번호();
                    if (분류코드 == 1 && ṣàyẹ̀wò_aláìṣeéyípadà(détà_iye, 3)) ààyè_ìfàyọkàsí_détà[fáìlì_wá_atọ̀ka_àkóónú] = 상가[détà_iye];
                    else if (분류코드 == 2 && ṣàyẹ̀wò_aláìṣeéyípadà(détà_iye, 8)) ààyè_ìfàyọkàsí_détà[fáìlì_wá_atọ̀ka_àkóónú] = aláìṣeéyípadà_SMS(상가[détà_iye]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { ìkùnà_iye("method count limit (512)"); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 개수 && !àṣìṣe; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int 수 = 함수수++; ìlànà_Oníǹkan[수] = ọ̀wọ́_Ìsọ̀tumọ̀;
            ìlànà_wáyè_sí[수] = 짧은수(); ìlànà_orúkọ_SMS[수] = 상번호(); ìlànà_irú[수] = 상번호();
            ṣàyẹ̀wò_aláìṣeéyípadà(ìlànà_orúkọ_SMS[수], 1); 서술읽기(수);
            if ((ìlànà_wáyè_sí[수] & 8) == 0) {
                if (함수인수수[수] == 16) { ìkùnà_iye("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) ìlànà_ágúmẹ́ntì_irú[수 * 16 + 비교자리] = ìlànà_ágúmẹ́ntì_irú[수 * 16 + 비교자리 - 1];
                ìlànà_ágúmẹ́ntì_irú[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((ìlànà_wáyè_sí[수] & 0x100) != 0) ìkùnà_iye("user native method unsupported");
            if (Ọ̀rọ̀_SMS(ìlànà_orúkọ_SMS[수], "<clinit>")) pàjùbà_ọ̀wọ́_Ìsọ̀tumọ̀[ọ̀wọ́_Ìsọ̀tumọ̀] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (ìlànà_Oníǹkan[앞] == ọ̀wọ́_Ìsọ̀tumọ̀ && 같은말(ìlànà_orúkọ_SMS[앞], ìlànà_orúkọ_SMS[수]) && 같은말(ìlànà_irú[앞], ìlànà_irú[수])) ìkùnà_iye("duplicate method");
            int 속성수 = 짧은수();
            for (int àwòmọ́_iye = 0; àwòmọ́_iye < 속성수 && !àṣìṣe; àwòmọ́_iye++) {
                int Orúkọ = 상번호(), gígùn_iye = nọ́ńbà_odindi(), Rọ́ọ̀nù = 읽기위치;
                if (!ní_ṣókí(Rọ́ọ̀nù, gígùn_iye)) { ìkùnà_iye("truncated method attribute"); break; }
                if (Ọ̀rọ̀_SMS(Orúkọ, "Code")) {
                    if (ìlànà_bẹ̀rẹ̀[수] != 0) ìkùnà_iye("duplicate Code attribute");
                    ìlànà_kójọ[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = nọ́ńbà_odindi();
                    if (ìlànà_kójọ[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ìkùnà_iye("method memory limits exceeded");
                    ìlànà_bẹ̀rẹ̀[수] = 읽기위치; 건너(코드길이); ìlànà_parí[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { ìkùnà_iye("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int àṣìṣe_Ìtọ́ka = 잡기수++; 잡기함수[àṣìṣe_Ìtọ́ka] = 수;
                        잡기시작[àṣìṣe_Ìtọ́ka] = ìlànà_bẹ̀rẹ̀[수] + 짧은수(); 잡기끝[àṣìṣe_Ìtọ́ka] = ìlànà_bẹ̀rẹ̀[수] + 짧은수();
                        잡기위치[àṣìṣe_Ìtọ́ka] = ìlànà_bẹ̀rẹ̀[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[àṣìṣe_Ìtọ́ka] = 부호값 == 0 ? 0 : ọ̀wọ́_orúkọ_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Rọ́ọ̀nù + gígùn_iye) ìkùnà_iye("Code attribute size mismatch");
                } else 건너(gígùn_iye);
            }
            if ((ìlànà_wáyè_sí[수] & 0x400) != 0) continue;
            if (ìlànà_bẹ̀rẹ̀[수] == 0) ìkùnà_iye("missing Code attribute");
            int ààyè_ìfàyọkàsí_ìgbéwọlé = ìlànà_bẹ̀rẹ̀[수];
            while (ààyè_ìfàyọkàsí_ìgbéwọlé < ìlànà_parí[수] && !àṣìṣe) {
                int gígùn_iye = 길이읽기(ààyè_ìfàyọkàsí_ìgbéwọlé, ìlànà_bẹ̀rẹ̀[수], ìlànà_parí[수]);
                if (gígùn_iye == 0) { ìkùnà_iye("unsupported or truncated bytecode"); break; }
                경계[ààyè_ìfàyọkàsí_ìgbéwọlé] = 수 + 1; ààyè_ìfàyọkàsí_ìgbéwọlé += gígùn_iye;
            }
            ààyè_ìfàyọkàsí_ìgbéwọlé = ìlànà_bẹ̀rẹ̀[수];
            while (ààyè_ìfàyọkàsí_ìgbéwọlé < ìlànà_parí[수] && !àṣìṣe) {
                int iye = Fáìlì[ààyè_ìfàyọkàsí_ìgbéwọlé];
                if (iye >= 153 && iye <= 167 || iye == 198 || iye == 199) ṣàyẹ̀wò_èbúté_iye(ààyè_ìfàyọkàsí_ìgbéwọlé + (short)(Fáìlì[ààyè_ìfàyọkàsí_ìgbéwọlé + 1] << 8 | Fáìlì[ààyè_ìfàyọkàsí_ìgbéwọlé + 2]), 수);
                if (iye == 200) ṣàyẹ̀wò_èbúté_iye(ààyè_ìfàyọkàsí_ìgbéwọlé + 위치정수(ààyè_ìfàyọkàsí_ìgbéwọlé + 1), 수);
                if (iye == 170 || iye == 171) {
                    int 읽는자리 = ààyè_ìfàyọkàsí_ìgbéwọlé + 1; while ((읽는자리 - ìlànà_bẹ̀rẹ̀[수]) % 4 != 0) 읽는자리++;
                    ṣàyẹ̀wò_èbúté_iye(ààyè_ìfàyọkàsí_ìgbéwọlé + 위치정수(읽는자리), 수);
                    int 항목수 = iye == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += iye == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) ṣàyẹ̀wò_èbúté_iye(ààyè_ìfàyọkàsí_ìgbéwọlé + 위치정수(읽는자리 + 안쪽자리 * (iye == 170 ? 4 : 8) + (iye == 170 ? 0 : 4)), 수);
                }
                ààyè_ìfàyọkàsí_ìgbéwọlé += 길이읽기(ààyè_ìfàyọkàsí_ìgbéwọlé, ìlànà_bẹ̀rẹ̀[수], ìlànà_parí[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                ṣàyẹ̀wò_èbúté_iye(잡기시작[안쪽자리], 수); ṣàyẹ̀wò_èbúté_iye(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != ìlànà_parí[수]) ṣàyẹ̀wò_èbúté_iye(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) ìkùnà_iye("invalid exception range");
            }
        }
        if (!àṣìṣe) 속성건너();
        if (읽기위치 != Ìwọ̀n) ìkùnà_iye("extra class file data");
    }
    static int pín_Ibi_ìpamọ́(int 종류, int gígùn_iye) { return 새기억(종류, gígùn_iye); }
    static boolean nǹkan_iye(int Ìtọ́ka, int 종류) {
        if (!객체유효(Ìtọ́ka)) return false;
        if (힙[Ìtọ́ka] != 종류) { ìkùnà_iye("object type mismatch"); return false; }
        return true;
    }
    static int aláìṣeéyípadà_SMS(int wá_atọ̀ka_àkóónú) {
        if (!ṣàyẹ̀wò_aláìṣeéyípadà(wá_atọ̀ka_àkóónú, 1)) return 0;
        if (fọ́nrán_Ìtọ́ka[wá_atọ̀ka_àkóónú] != 0) return fọ́nrán_Ìtọ́ka[wá_atọ̀ka_àkóónú];
        int Ìtọ́ka = pín_Ibi_ìpamọ́(1, 상나[wá_atọ̀ka_àkóónú]); if (àṣìṣe) return 0;
        int 끝 = 상가[wá_atọ̀ka_àkóónú] + 상나[wá_atọ̀ka_àkóónú], 수 = 상가[wá_atọ̀ka_àkóónú], gígùn_iye = 0;
        while (수 < 끝 && !àṣìṣe) {
            int iye = Fáìlì[수++];
            if (iye == 0) ìkùnà_iye("invalid modified UTF-8");
            else if (iye >= 192 && iye <= 223 && 수 < 끝) {
                int 다음 = Fáìlì[수++];
                if ((다음 & 192) != 128) ìkùnà_iye("invalid modified UTF-8");
                iye = (iye & 31) << 6 | 다음 & 63;
                if (iye != 0 && iye < 128) ìkùnà_iye("overlong modified UTF-8");
            } else if (iye >= 224 && iye <= 239 && 수 + 1 < 끝) {
                int 가 = Fáìlì[수++], 나 = Fáìlì[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) ìkùnà_iye("invalid modified UTF-8");
                iye = (iye & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (iye < 2048) ìkùnà_iye("overlong modified UTF-8");
            } else if (iye >= 128) ìkùnà_iye("invalid modified UTF-8");
            힙[Ìtọ́ka + 2 + gígùn_iye++] = iye;
        }
        힙[Ìtọ́ka + 1] = gígùn_iye; fọ́nrán_Ìtọ́ka[wá_atọ̀ka_àkóónú] = Ìtọ́ka; return Ìtọ́ka;
    }
    static int olùpèsè_ẹyọ_ọ̀rọ̀(String iye) {
        int Ìtọ́ka = pín_Ibi_ìpamọ́(1, iye.length()); if (àṣìṣe) return 0;
        for (int 수 = 0; 수 < iye.length(); 수++) 힙[Ìtọ́ka + 2 + 수] = iye.charAt(수);
        return Ìtọ́ka;
    }
    static void kọ_SMS(int Ìtọ́ka) {
        if (Ìtọ́ka == 0) { aṣàmúlò.Kọ("null"); return; }
        if (!nǹkan_iye(Ìtọ́ka, 1)) return;
        for (int 수 = 0; 수 < 힙[Ìtọ́ka + 1]; 수++) aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(힙[Ìtọ́ka + 2 + 수]);
    }
    static int díjììtì_ẹyọ_ọ̀rọ̀(int iye) {
        int Ìtọ́ka = pín_Ibi_ìpamọ́(1, 11); if (àṣìṣe) return 0;
        int gígùn_iye = 0;
        if (iye < 0) 힙[Ìtọ́ka + 2 + gígùn_iye++] = '-'; else iye = -iye;
        int 자리 = 1000000000; boolean Rọ́ọ̀nù = false;
        while (자리 != 0) {
            int 수 = -(iye / 자리);
            if (수 != 0 || Rọ́ọ̀nù || 자리 == 1) { 힙[Ìtọ́ka + 2 + gígùn_iye++] = '0' + 수; Rọ́ọ̀nù = true; }
            iye %= 자리; 자리 /= 10;
        }
        힙[Ìtọ́ka + 1] = gígùn_iye; return Ìtọ́ka;
    }
    static int 정수해독(int Ìtọ́ka) {
        if (!nǹkan_iye(Ìtọ́ka, 1)) return 0;
        int gígùn_iye = 힙[Ìtọ́ka + 1], 수 = 0, iye = 0; boolean 음수 = false;
        if (gígùn_iye > 0 && (힙[Ìtọ́ka + 2] == '-' || 힙[Ìtọ́ka + 2] == '+')) { 음수 = 힙[Ìtọ́ka + 2] == '-'; 수++; }
        if (수 == gígùn_iye) ìkùnà_iye("NumberFormatException");
        for (; 수 < gígùn_iye && !àṣìṣe; 수++) {
            int díjììtì_iye = 힙[Ìtọ́ka + 2 + 수] - '0';
            if (díjììtì_iye < 0 || díjììtì_iye > 9 || iye < -214748364 || iye == -214748364 && díjììtì_iye > (음수 ? 8 : 7)) ìkùnà_iye("NumberFormatException");
            iye = iye * 10 - díjììtì_iye;
        }
        return 음수 ? iye : -iye;
    }
    static void 넣기(int iye, int irú_iye) {
        if (àṣìṣe) return;
        if (férèmù_wá_atọ̀ka_àkóónú < 0 || férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú] >= ìlànà_kójọ[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]]) { ìkùnà_iye("operand stack overflow"); return; }
        int ààyè_ìfàyọkàsí_ìgbéwọlé = férèmù_wá_atọ̀ka_àkóónú * 128 + férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú]++; 스택값[ààyè_ìfàyọkàsí_ìgbéwọlé] = iye; 스택형[ààyè_ìfàyọkàsí_ìgbéwọlé] = irú_iye;
    }
    static int 빼기(int irú_iye) {
        if (àṣìṣe) return 0;
        if (férèmù_wá_atọ̀ka_àkóónú < 0 || férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú] < 1) { ìkùnà_iye("operand stack underflow"); return 0; }
        int ààyè_ìfàyọkàsí_ìgbéwọlé = férèmù_wá_atọ̀ka_àkóónú * 128 + --férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú]; 반환형 = 스택형[ààyè_ìfàyọkàsí_ìgbéwọlé];
        if (irú_iye != 0 && 반환형 != irú_iye) ìkùnà_iye("operand type mismatch");
        if (반환형 == 2) dáàbòbò_iye(스택값[ààyè_ìfàyọkàsí_ìgbéwọlé]);
        return 스택값[ààyè_ìfàyọkàsí_ìgbéwọlé];
    }
    static void 지역읽기(int wá_atọ̀ka_àkóónú, int irú_iye) {
        if (wá_atọ̀ka_àkóónú >= 함수지역[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]] || wá_atọ̀ka_àkóónú < 0 || agbègbè_irú[férèmù_wá_atọ̀ka_àkóónú * 128 + wá_atọ̀ka_àkóónú] != irú_iye) { ìkùnà_iye("invalid or uninitialized local"); return; }
        넣기(agbègbè_iye[férèmù_wá_atọ̀ka_àkóónú * 128 + wá_atọ̀ka_àkóónú], irú_iye);
    }
    static void kọ_agbègbè(int wá_atọ̀ka_àkóónú, int irú_iye) {
        if (wá_atọ̀ka_àkóónú >= 함수지역[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]] || wá_atọ̀ka_àkóónú < 0) { ìkùnà_iye("local index out of range"); return; }
        int iye = 빼기(irú_iye); agbègbè_iye[férèmù_wá_atọ̀ka_àkóónú * 128 + wá_atọ̀ka_àkóónú] = iye; agbègbè_irú[férèmù_wá_atọ̀ka_àkóónú * 128 + wá_atọ̀ka_àkóónú] = irú_iye;
    }
    static int 명바() {
        int 위치 = 틀위치[férèmù_wá_atọ̀ka_àkóónú];
        if (위치 < ìlànà_bẹ̀rẹ̀[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]] || 위치 >= ìlànà_parí[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]]) { ìkùnà_iye("instruction pointer out of range"); return 0; }
        틀위치[férèmù_wá_atọ̀ka_àkóónú]++; return Fáìlì[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void gbé_iye(int 위치) {
        int ÀKÀNṢEFỌMÚLÀ_iye = férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú];
        if (위치 < ìlànà_bẹ̀rẹ̀[ÀKÀNṢEFỌMÚLÀ_iye] || 위치 >= ìlànà_parí[ÀKÀNṢEFỌMÚLÀ_iye] || 경계[위치] != ÀKÀNṢEFỌMÚLÀ_iye + 1) ìkùnà_iye("invalid branch target");
        else 틀위치[férèmù_wá_atọ̀ka_àkóónú] = 위치;
    }
    static void 호출(int ÀKÀNṢEFỌMÚLÀ_iye) {
        if (férèmù_wá_atọ̀ka_àkóónú % 32 == 31) { ìkùnà_iye("call stack limit (32)"); return; }
        int 다음 = férèmù_wá_atọ̀ka_àkóónú + 1;
        for (int 수 = 0; 수 < 128; 수++) agbègbè_irú[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[ÀKÀNṢEFỌMÚLÀ_iye] - 1; 수 >= 0; 수--) {
            agbègbè_iye[다음 * 128 + 수] = 빼기(ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수]); agbègbè_irú[다음 * 128 + 수] = ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수];
        }
        if (àṣìṣe) return;
        férèmù_wá_atọ̀ka_àkóónú = 다음; pàjùbà_férèmù[férèmù_wá_atọ̀ka_àkóónú] = 0; férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú] = ÀKÀNṢEFỌMÚLÀ_iye; 틀위치[férèmù_wá_atọ̀ka_àkóónú] = ìlànà_bẹ̀rẹ̀[ÀKÀNṢEFỌMÚLÀ_iye]; férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú] = 0;
    }
    static void 반환(int irú_iye) {
        if (irú_iye != 함수반환[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]]) { ìkùnà_iye("return type mismatch"); return; }
        int iye = irú_iye == 0 ? 0 : 빼기(irú_iye);
        if (pàjùbà_férèmù[férèmù_wá_atọ̀ka_àkóónú] != 0) ọ̀wọ́_Ìsọ̀tumọ̀_ipò[pàjùbà_férèmù[férèmù_wá_atọ̀ka_àkóónú] - 1] = 2;
        if (틀잠금[férèmù_wá_atọ̀ka_àkóónú] != 0) { 잠금풀기(틀잠금[férèmù_wá_atọ̀ka_àkóónú]); 틀잠금[férèmù_wá_atọ̀ka_àkóónú] = 0; }
        férèmù_wá_atọ̀ka_àkóónú--; if (férèmù_wá_atọ̀ka_àkóónú >= 현재가닥 * 32 && irú_iye != 0) 넣기(iye, irú_iye);
    }
    static int[] Stream_fáìlì_orúkọ = new int[64];
    static void fáìlì_Stream_pè(int Oníǹkan_iye, int Orúkọ, int ìgúnrégé_iye, int Àṣẹ) {
        boolean 출력 = Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Àṣẹ == 183 && Ọ̀rọ̀_SMS(Orúkọ, "<init>")) {
            boolean 이어 = false;
            if (출력 && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(Ljava/lang/String;)V")) { ìkùnà_iye("unsupported file stream constructor"); return; }
            int fáìlì_ìgbéwọlé_orúkọ = 빼기(2), Stream_iye = 빼기(2);
            if (!nǹkan_iye(fáìlì_ìgbéwọlé_orúkọ, 1) || !nǹkan_iye(Stream_iye, 종류) || àṣìṣe) return;
            if (힙[Stream_iye + 3] != 0) { ìkùnà_iye("file stream already initialized"); return; }
            int gígùn_iye = 힙[fáìlì_ìgbéwọlé_orúkọ + 1];
            if (gígùn_iye < 1 || gígùn_iye > 63) { ìkùnà_iye("invalid file name length"); return; }
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < gígùn_iye; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
                int iye = 힙[fáìlì_ìgbéwọlé_orúkọ + 2 + ààyè_ìfàyọkàsí_ìgbéwọlé];
                if (iye < 1) { ìkùnà_iye("invalid file stream path"); return; }
                Stream_fáìlì_orúkọ[ààyè_ìfàyọkàsí_ìgbéwọlé] = iye;
            }
            Stream_fáìlì_orúkọ[gígùn_iye] = 0;
            int 서술자 = aṣàmúlò.파일서술자열기(Stream_fáìlì_orúkọ, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ìkùnà_iye("FileNotFoundException: file open failed"); return; }
            힙[Stream_iye + 2] = 서술자; 힙[Stream_iye + 3] = 1;
            return;
        }
        if (Àṣẹ != 182) { ìkùnà_iye("invalid file stream invocation"); return; }
        if ((출력 && Ọ̀rọ̀_SMS(Orúkọ, "write") || !출력 && Ọ̀rọ̀_SMS(Orúkọ, "read"))
            && (Ọ̀rọ̀_SMS(ìgúnrégé_iye, 출력 ? "([B)V" : "([B)I") || Ọ̀rọ̀_SMS(ìgúnrégé_iye, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean ní_ṣókí_iye = Ọ̀rọ̀_SMS(ìgúnrégé_iye, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = ní_ṣókí_iye ? 빼기(1) : 0, 시작점 = ní_ṣókí_iye ? 빼기(1) : 0, détà_ÀRÉÈ = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2);
            if (!nǹkan_iye(détà_ÀRÉÈ, 20) || !nǹkan_iye(nǹkan_Ìtọ́ka, 종류)) return;
            if (!ní_ṣókí_iye) 항목수 = 힙[détà_ÀRÉÈ + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[détà_ÀRÉÈ + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[nǹkan_Ìtọ́ka + 3] == 0 || 힙[nǹkan_Ìtọ́ka + 2] < 0) { ìkùnà_iye("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !àṣìṣe) {
                int 반환값 = 출력 ? aṣàmúlò.파일한바이트쓰기(힙[nǹkan_Ìtọ́ka + 2], 힙[détà_ÀRÉÈ + 2 + 시작점 + 완료수]) : aṣàmúlò.파일한바이트읽기(힙[nǹkan_Ìtọ́ka + 2]);
                if (반환값 < 0) { ìkùnà_iye(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[détà_ÀRÉÈ + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Ọ̀rọ̀_SMS(Orúkọ, "flush") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "()V")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 종류) && 힙[nǹkan_Ìtọ́ka + 2] < 0) ìkùnà_iye("IOException: stream closed"); return; }
        int ìṣe = -1, iye = 0;
        if (Ọ̀rọ̀_SMS(Orúkọ, "close") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "()V")) ìṣe = 0;
        if (!출력 && Ọ̀rọ̀_SMS(Orúkọ, "read") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "()I")) ìṣe = 1;
        if (출력 && Ọ̀rọ̀_SMS(Orúkọ, "write") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(I)V")) { ìṣe = 2; iye = 빼기(1); }
        if (ìṣe < 0) { ìkùnà_iye("unsupported file stream method"); return; }
        int Stream_iye = 빼기(2);
        if (!nǹkan_iye(Stream_iye, 종류) || àṣìṣe) return;
        if (힙[Stream_iye + 3] == 0) { ìkùnà_iye("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_iye + 2];
        if (ìṣe == 0) {
            if (서술자 >= 0 && aṣàmúlò.파일서술자닫기(서술자) < 0) ìkùnà_iye("IOException: close failed");
            힙[Stream_iye + 2] = -1; return;
        }
        if (서술자 < 0) { ìkùnà_iye("IOException: stream closed"); return; }
        if (ìṣe == 1) {
            int 결과 = aṣàmúlò.파일한바이트읽기(서술자);
            if (결과 < -1) ìkùnà_iye("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (aṣàmúlò.파일한바이트쓰기(서술자, iye) != 1) ìkùnà_iye("IOException: write failed");
    }
    static void pè_ìlànà(int wá_atọ̀ka_àkóónú, int Àṣẹ) {
        if (wá_atọ̀ka_àkóónú <= 0 || wá_atọ̀ka_àkóónú >= aláìṣeéyípadà_sàmì.length || (aláìṣeéyípadà_sàmì[wá_atọ̀ka_àkóónú] != 10 && aláìṣeéyípadà_sàmì[wá_atọ̀ka_àkóónú] != 11)) { ìkùnà_iye("invalid method reference"); return; }
        int Oníǹkan_iye = ọ̀wọ́_orúkọ_SMS(상가[wá_atọ̀ka_àkóónú]), Orúkọ = Ìtọ́ka_orúkọ(상나[wá_atọ̀ka_àkóónú]), ìgúnrégé_iye = Ìtọ́ka_irú(상나[wá_atọ̀ka_àkóónú]);
        if (àṣìṣe) return;
        if (기본호출(Oníǹkan_iye, Orúkọ, ìgúnrégé_iye, Àṣẹ)) return;
        if (Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/io/FileInputStream") || Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/io/FileOutputStream")) {
            fáìlì_Stream_pè(Oníǹkan_iye, Orúkọ, ìgúnrégé_iye, Àṣẹ); return;
        }
        if (Àṣẹ == 184 && Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/lang/Integer") && Ọ̀rọ̀_SMS(Orúkọ, "parseInt") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Àṣẹ == 182 && Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/io/PrintStream") && (Ọ̀rọ̀_SMS(Orúkọ, "println") || Ọ̀rọ̀_SMS(Orúkọ, "print"))) {
            int irú_iye = 0, iye = 0;
            if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(I)V")) { irú_iye = 1; iye = 빼기(1); }
            else if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(Z)V")) { irú_iye = 2; iye = 빼기(1); }
            else if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(C)V")) { irú_iye = 3; iye = 빼기(1); }
            else if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(Ljava/lang/String;)V")) { irú_iye = 4; iye = 빼기(2); }
            else if (!Ọ̀rọ̀_SMS(ìgúnrégé_iye, "()V") || !Ọ̀rọ̀_SMS(Orúkọ, "println")) ìkùnà_iye("unsupported print descriptor");
            if (빼기(2) != -1) ìkùnà_iye("invalid PrintStream receiver");
            if (àṣìṣe) return;
            if (irú_iye == 1) 자바도구.수쓰기(iye);
            if (irú_iye == 2) aṣàmúlò.Kọ(iye == 0 ? "false" : "true");
            if (irú_iye == 3) aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(iye & 65535);
            if (irú_iye == 4) kọ_SMS(iye);
            if (Ọ̀rọ̀_SMS(Orúkọ, "println")) aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10);
            return;
        }
        if (Àṣẹ == 182 && Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/lang/String")) {
            if (Ọ̀rọ̀_SMS(Orúkọ, "length") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "()I")) {
                int Ìtọ́ka = 빼기(2); if (nǹkan_iye(Ìtọ́ka, 1)) 넣기(힙[Ìtọ́ka + 1], 1); return;
            }
            if (Ọ̀rọ̀_SMS(Orúkọ, "charAt") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(I)C")) {
                int òǹtẹ̀_ìsàlẹ̀_iye = 빼기(1), Ìtọ́ka = 빼기(2);
                if (nǹkan_iye(Ìtọ́ka, 1)) {
                    if (òǹtẹ̀_ìsàlẹ̀_iye < 0 || òǹtẹ̀_ìsàlẹ̀_iye >= 힙[Ìtọ́ka + 1]) ìkùnà_iye("StringIndexOutOfBoundsException"); else 넣기(힙[Ìtọ́ka + 2 + òǹtẹ̀_ìsàlẹ̀_iye], 1);
                }
                return;
            }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/lang/StringBuilder")) {
            if (Àṣẹ == 183 && Ọ̀rọ̀_SMS(Orúkọ, "<init>") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "()V")) { nǹkan_iye(빼기(2), 4); return; }
            if (Àṣẹ == 182 && Ọ̀rọ̀_SMS(Orúkọ, "toString") && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "()Ljava/lang/String;")) {
                int Ìtọ́ka = 빼기(2); if (nǹkan_iye(Ìtọ́ka, 4)) 넣기(힙[Ìtọ́ka + 2] == 0 ? olùpèsè_ẹyọ_ọ̀rọ̀("") : 힙[Ìtọ́ka + 2], 2); return;
            }
            if (Àṣẹ == 182 && Ọ̀rọ̀_SMS(Orúkọ, "append")) {
                int SMS = 0;
                if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(I)Ljava/lang/StringBuilder;")) SMS = díjììtì_ẹyọ_ọ̀rọ̀(빼기(1));
                else if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(Z)Ljava/lang/StringBuilder;")) SMS = olùpèsè_ẹyọ_ọ̀rọ̀(빼기(1) == 0 ? "false" : "true");
                else if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(C)Ljava/lang/StringBuilder;")) {
                    int iye = 빼기(1); SMS = pín_Ibi_ìpamọ́(1, 1); if (!àṣìṣe) 힙[SMS + 2] = iye & 65535;
                }
                else if (Ọ̀rọ̀_SMS(ìgúnrégé_iye, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = olùpèsè_ẹyọ_ọ̀rọ̀("null"); }
                else { ìkùnà_iye("unsupported StringBuilder append"); return; }
                int Ìtọ́ka = 빼기(2); if (!nǹkan_iye(Ìtọ́ka, 4) || !nǹkan_iye(SMS, 1)) return;
                int 앞 = 힙[Ìtọ́ka + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Padà_sẹ́yìn_iye_gígùn = 힙[SMS + 1];
                int 새글 = pín_Ibi_ìpamọ́(1, 앞길이 + Padà_sẹ́yìn_iye_gígùn); if (àṣìṣe) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Padà_sẹ́yìn_iye_gígùn; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[Ìtọ́ka + 2] = 새글; 넣기(Ìtọ́ka, 2); return;
            }
        }
        int ọ̀wọ́_Ìsọ̀tumọ̀ = wá_ọ̀wọ́_Ìsọ̀tumọ̀(Oníǹkan_iye); if (ọ̀wọ́_Ìsọ̀tumọ̀ < 0 || àṣìṣe) return;
        int fáìlì_wá_atọ̀ka_àkóónú = wá_ìlànà(ọ̀wọ́_Ìsọ̀tumọ̀, Orúkọ, ìgúnrégé_iye);
        if (fáìlì_wá_atọ̀ka_àkóónú < 0) {
            for (int kóòdù_ẹyọ_ọ̀rọ̀ = ọ̀wọ́_Ìsọ̀tumọ̀, 항목수 = 0; kóòdù_ẹyọ_ọ̀rọ̀ >= 0 && 항목수 < 16; 항목수++, kóòdù_ẹyọ_ọ̀rọ̀ = 부모종(kóòdù_ẹyọ_ọ̀rọ̀))
                if (Ọ̀rọ̀_SMS(종부모[kóòdù_ẹyọ_ọ̀rọ̀], "java/lang/Thread")) { 가닥호출(Orúkọ, ìgúnrégé_iye, Àṣẹ); return; }
            ìkùnà_iye("NoSuchMethodError"); return;
        }
        if (((ìlànà_wáyè_sí[fáìlì_wá_atọ̀ka_àkóónú] & 8) != 0) != (Àṣẹ == 184)) { ìkùnà_iye("method static/instance mismatch"); return; }
        if (Àṣẹ == 184) { if (!pàjùbà(ìlànà_Oníǹkan[fáìlì_wá_atọ̀ka_àkóónú], férèmù_ìtọ́sọ́nà[férèmù_wá_atọ̀ka_àkóónú])) return; }
        else {
            int 읽는자리 = férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú] - 함수인수수[fáìlì_wá_atọ̀ka_àkóónú];
            if (읽는자리 < 0 || 스택형[férèmù_wá_atọ̀ka_àkóónú * 128 + 읽는자리] != 2) { ìkùnà_iye("invalid method receiver"); return; }
            int nǹkan_Ìtọ́ka = 스택값[férèmù_wá_atọ̀ka_àkóónú * 128 + 읽는자리];
            if (!객체유효(nǹkan_Ìtọ́ka)) return;
            if (힙[nǹkan_Ìtọ́ka] < 32 || !종포함(힙[nǹkan_Ìtọ́ka] - 32, Oníǹkan_iye)) { ìkùnà_iye("method receiver type mismatch"); return; }
            if (Àṣẹ != 183) fáìlì_wá_atọ̀ka_àkóónú = wá_ìlànà(힙[nǹkan_Ìtọ́ka] - 32, Orúkọ, ìgúnrégé_iye);
        }
        if (fáìlì_wá_atọ̀ka_àkóónú < 0 || (ìlànà_wáyè_sí[fáìlì_wá_atọ̀ka_àkóónú] & 0x400) != 0) { ìkùnà_iye("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((ìlànà_wáyè_sí[fáìlì_wá_atọ̀ka_àkóónú] & 32) != 0) {
            if (Àṣẹ == 184) { int kóòdù_ẹyọ_ọ̀rọ̀ = ìlànà_Oníǹkan[fáìlì_wá_atọ̀ka_àkóónú]; if (종잠금[kóòdù_ẹyọ_ọ̀rọ̀] == 0) 종잠금[kóòdù_ẹyọ_ọ̀rọ̀] = pín_Ibi_ìpamọ́(8, 0); 잠금참조 = 종잠금[kóòdù_ẹyọ_ọ̀rọ̀]; }
            else 잠금참조 = 스택값[férèmù_wá_atọ̀ka_àkóónú * 128 + férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú] - 함수인수수[fáìlì_wá_atọ̀ka_àkóónú]];
            if (!잠금얻기(잠금참조)) { if (!àṣìṣe) 틀위치[férèmù_wá_atọ̀ka_àkóónú] = férèmù_ìtọ́sọ́nà[férèmù_wá_atọ̀ka_àkóónú]; return; }
        }
        호출(fáìlì_wá_atọ̀ka_àkóónú); if (!àṣìṣe) 틀잠금[férèmù_wá_atọ̀ka_àkóónú] = 잠금참조;
    }
    static boolean 배열저장가능(int ÀRÉÈ_Ìtọ́ka, int détà_iye) {
        if (détà_iye == 0 || ÀRÉÈ_ìdá_ìpìlẹ̀[ÀRÉÈ_Ìtọ́ka] == 0) return true;
        boolean 성공여부 = ÀRÉÈ_ìdá_ìpìlẹ̀[ÀRÉÈ_Ìtọ́ka] == -1 ? (détà_iye > 0 && détà_iye < 힙끝 && 힙[détà_iye] == 1) : 맞는객체(détà_iye, ÀRÉÈ_ìdá_ìpìlẹ̀[ÀRÉÈ_Ìtọ́ka]);
        if (!성공여부 && !àṣìṣe) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ÀRÉÈ_ààyè_ìfàyọkàsí(int Ìtọ́ka, int òǹtẹ̀_ìsàlẹ̀_iye, int irú_iye) {
        if (!nǹkan_iye(Ìtọ́ka, irú_iye)) return 0;
        if (òǹtẹ̀_ìsàlẹ̀_iye < 0 || òǹtẹ̀_ìsàlẹ̀_iye >= 힙[Ìtọ́ka + 1]) { ìkùnà_iye("ArrayIndexOutOfBoundsException"); return 0; }
        return Ìtọ́ka + 2 + òǹtẹ̀_ìsàlẹ̀_iye;
    }
    static void ṣiṣẹ́_àṣẹ() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (àṣìṣe) { if (던진객체 != 0) 예외처리(); if (àṣìṣe || férèmù_wá_atọ̀ka_àkóónú < 현재가닥 * 32) break; }
            if (férèmù_wá_atọ̀ka_àkóónú < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!ṣèpapòdà_èròjà_atẹ̀lélànà()) break; 조각 = 100; }
            if (férèmù_wá_atọ̀ka_àkóónú == 0 && ọ̀wọ́_Ìsọ̀tumọ̀_ipò[ìgbéwọlé_ọ̀wọ́_Ìsọ̀tumọ̀] != 2 && !pàjùbà(ìgbéwọlé_ọ̀wọ́_Ìsọ̀tumọ̀, 틀위치[férèmù_wá_atọ̀ka_àkóónú])) continue;
            if (férèmù_wá_atọ̀ka_àkóónú == 현재가닥 * 32 && 현재가닥 != 0 && (ìlànà_wáyè_sí[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]] & 32) != 0 && 틀잠금[férèmù_wá_atọ̀ka_àkóónú] == 0) {
                int nǹkan_Ìtọ́ka = èròjà_atẹ̀lélànà_àfojúsùn[현재가닥]; if (!잠금얻기(nǹkan_Ìtọ́ka)) { if (àṣìṣe) break; continue; } 틀잠금[férèmù_wá_atọ̀ka_àkóónú] = nǹkan_Ìtọ́ka;
            }
            잠시수 = 0;
            if (--남음 == 0) { ìkùnà_iye("instruction limit (500000)"); break; }
            int Rọ́ọ̀nù = 틀위치[férèmù_wá_atọ̀ka_àkóónú]; férèmù_ìtọ́sọ́nà[férèmù_wá_atọ̀ka_àkóónú] = Rọ́ọ̀nù; int iye = 명바();
            if (àṣìṣe) break;
            if (iye == 0) continue;
            if (iye == 1) { 넣기(0, 2); continue; }
            if (iye >= 2 && iye <= 8) { 넣기(iye - 3, 1); continue; }
            if (iye == 16) { 넣기((byte)명바(), 1); continue; }
            if (iye == 17) { 넣기((short)명짧(), 1); continue; }
            if (iye == 18 || iye == 19) {
                int 수 = ìlànà_Oníǹkan[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]] * 512 + (iye == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= aláìṣeéyípadà_sàmì.length) ìkùnà_iye("invalid ldc constant");
                else if (aláìṣeéyípadà_sàmì[수] == 3) 넣기(상가[수], 1);
                else if (aláìṣeéyípadà_sàmì[수] == 8) 넣기(aláìṣeéyípadà_SMS(상가[수]), 2);
                else ìkùnà_iye("unsupported ldc constant");
                continue;
            }
            if (iye == 21 || iye == 25) { 지역읽기(명바(), iye == 21 ? 1 : 2); continue; }
            if (iye >= 26 && iye <= 29) { 지역읽기(iye - 26, 1); continue; }
            if (iye >= 42 && iye <= 45) { 지역읽기(iye - 42, 2); continue; }
            if (iye == 54 || iye == 58) { kọ_agbègbè(명바(), iye == 54 ? 1 : 2); continue; }
            if (iye >= 59 && iye <= 62) { kọ_agbègbè(iye - 59, 1); continue; }
            if (iye >= 75 && iye <= 78) { kọ_agbègbè(iye - 75, 2); continue; }
            if (iye == 46 || iye >= 50 && iye <= 53) {
                int 항목자리 = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2), 분류코드 = iye == 46 ? 2 : iye == 50 ? 3 : iye == 51 ? 20 : iye == 52 ? 22 : 23;
                if (iye == 51 && nǹkan_Ìtọ́ka > 0 && nǹkan_Ìtọ́ka < 힙끝 && 힙[nǹkan_Ìtọ́ka] == 21) 분류코드 = 21;
                int 읽는자리 = ÀRÉÈ_ààyè_ìfàyọkàsí(nǹkan_Ìtọ́ka, 항목자리, 분류코드); if (!àṣìṣe) 넣기(힙[읽는자리], iye == 50 ? 2 : 1); continue;
            }
            if (iye == 79 || iye >= 83 && iye <= 86) {
                int ìgbéwọlé_Ìtọ́ka = 빼기(iye == 83 ? 2 : 1), 항목자리 = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2), 분류코드 = iye == 79 ? 2 : iye == 83 ? 3 : iye == 84 ? 20 : iye == 85 ? 22 : 23;
                if (iye == 84 && nǹkan_Ìtọ́ka > 0 && nǹkan_Ìtọ́ka < 힙끝 && 힙[nǹkan_Ìtọ́ka] == 21) 분류코드 = 21;
                int 읽는자리 = ÀRÉÈ_ààyè_ìfàyọkàsí(nǹkan_Ìtọ́ka, 항목자리, 분류코드);
                if (!àṣìṣe && 분류코드 == 3 && !배열저장가능(nǹkan_Ìtọ́ka, ìgbéwọlé_Ìtọ́ka)) continue;
                if (!àṣìṣe) 힙[읽는자리] = 분류코드 == 20 ? (byte)ìgbéwọlé_Ìtọ́ka : 분류코드 == 21 ? ìgbéwọlé_Ìtọ́ka & 1 : 분류코드 == 22 ? (char)ìgbéwọlé_Ìtọ́ka : 분류코드 == 23 ? (short)ìgbéwọlé_Ìtọ́ka : ìgbéwọlé_Ìtọ́ka;
                continue;
            }
            if (iye >= 87 && iye <= 95) { kójọ_ìtọ́sọ́nà(iye); continue; }
            if (iye == 96 || iye == 100 || iye == 104 || iye == 108 || iye == 112 || iye == 120
                || iye == 122 || iye == 124 || iye == 126 || iye == 128 || iye == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((iye == 108 || iye == 112) && 나 == 0) { ìkùnà_iye("ArithmeticException: / by zero"); continue; }
                if (iye == 96) 결과 = 가 + 나;
                if (iye == 100) 결과 = 가 - 나;
                if (iye == 104) 결과 = 가 * 나;
                if (iye == 108) 결과 = 가 / 나;
                if (iye == 112) 결과 = 가 % 나;
                if (iye == 120) 결과 = 가 << 나;
                if (iye == 122) 결과 = 가 >> 나;
                if (iye == 124) 결과 = 가 >>> 나;
                if (iye == 126) 결과 = 가 & 나;
                if (iye == 128) 결과 = 가 | 나;
                if (iye == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (iye == 116) { 넣기(-빼기(1), 1); continue; }
            if (iye == 132) {
                int agbègbè_sàkání = 명바(), 증분 = (byte)명바(); 지역읽기(agbègbè_sàkání, 1); 넣기(빼기(1) + 증분, 1); kọ_agbègbè(agbègbè_sàkání, 1); continue;
            }
            if (iye >= 145 && iye <= 147) {
                int 수 = 빼기(1); 넣기(iye == 145 ? (byte)수 : iye == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (iye >= 153 && iye <= 167 || iye == 198 || iye == 199) {
                int èbúté_iye = Rọ́ọ̀nù + (short)명짧(); boolean 갈까 = iye == 167;
                if (iye >= 153 && iye <= 158) {
                    int 수 = 빼기(1); 갈까 = iye == 153 ? 수 == 0 : iye == 154 ? 수 != 0 : iye == 155 ? 수 < 0 : iye == 156 ? 수 >= 0 : iye == 157 ? 수 > 0 : 수 <= 0;
                } else if (iye >= 159 && iye <= 166) {
                    int 나 = 빼기(iye >= 165 ? 2 : 1), 가 = 빼기(iye >= 165 ? 2 : 1);
                    갈까 = iye == 159 || iye == 165 ? 가 == 나 : iye == 160 || iye == 166 ? 가 != 나 : iye == 161 ? 가 < 나 : iye == 162 ? 가 >= 나 : iye == 163 ? 가 > 나 : 가 <= 나;
                } else if (iye == 198 || iye == 199) { int 수 = 빼기(2); 갈까 = iye == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) gbé_iye(èbúté_iye); continue;
            }
            if (iye == 172 || iye == 176 || iye == 177) { 반환(iye == 172 ? 1 : iye == 176 ? 2 : 0); continue; }
            if (iye >= 178 && iye <= 181) { 필드호출(명상수(), iye, Rọ́ọ̀nù); continue; }
            if (iye >= 182 && iye <= 185) {
                int 부호값 = 명상수();
                if (iye == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { ìkùnà_iye("invalid invokeinterface operands"); continue; } }
                pè_ìlànà(부호값, iye); continue;
            }
            if (iye == 187) { 새객체(ọ̀wọ́_orúkọ_SMS(명상수()), Rọ́ọ̀nù); continue; }
            if (iye == 188 || iye == 189) {
                int 분류코드 = 3, ẹ̀yà = 0;
                if (iye == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else ẹ̀yà = ọ̀wọ́_orúkọ_SMS(명상수());
                if (분류코드 == 0) { ìkùnà_iye("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), nǹkan_Ìtọ́ka = pín_Ibi_ìpamọ́(분류코드, 유효길이); if (!àṣìṣe) ÀRÉÈ_ìdá_ìpìlẹ̀[nǹkan_Ìtọ́ka] = ẹ̀yà; 넣기(nǹkan_Ìtọ́ka, 2); continue;
            }
            if (iye == 190) {
                int nǹkan_Ìtọ́ka = 빼기(2);
                if (객체유효(nǹkan_Ìtọ́ka)) { int 비교자리 = 힙[nǹkan_Ìtọ́ka]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) ìkùnà_iye("not an array"); else 넣기(힙[nǹkan_Ìtọ́ka + 1], 1); }
                continue;
            }
            if (iye == 191) {
                int nǹkan_Ìtọ́ka = 빼기(2); if (객체유효(nǹkan_Ìtọ́ka)) { if (힙[nǹkan_Ìtọ́ka] != 9) ìkùnà_iye("athrow requires supported Throwable"); else { 던진객체 = nǹkan_Ìtọ́ka; àṣìṣe = true; } }
                continue;
            }
            if (iye == 192 || iye == 193) {
                int orúkọ_aláìṣeéyípadà = ọ̀wọ́_orúkọ_SMS(명상수()), nǹkan_Ìtọ́ka = 빼기(2); boolean 일치여부 = 맞는객체(nǹkan_Ìtọ́ka, orúkọ_aláìṣeéyípadà);
                if (iye == 193) 넣기(nǹkan_Ìtọ́ka != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !àṣìṣe) ìkùnà_iye("ClassCastException"); 넣기(nǹkan_Ìtọ́ka, 2); }
                continue;
            }
            if (iye == 170 || iye == 171) {
                int 읽는자리 = Rọ́ọ̀nù + 1, fáìlì_wá_atọ̀ka_àkóónú = férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú], bọ́tìnnì_Ìtọ́ka = 빼기(1);
                while ((읽는자리 - ìlànà_bẹ̀rẹ̀[fáìlì_wá_atọ̀ka_àkóónú]) % 4 != 0) 읽는자리++;
                int àfojúsùn_àdírẹ́ẹ̀sì = 위치정수(읽는자리);
                if (iye == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (bọ́tìnnì_Ìtọ́ka >= 낮은값 && bọ́tìnnì_Ìtọ́ka <= 높은값) àfojúsùn_àdírẹ́ẹ̀sì = 위치정수(읽는자리 + 12 + (bọ́tìnnì_Ìtọ́ka - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 총수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (위치정수(읽는자리 + 8 + ṣetúnṣe_wá_atọ̀ka_àkóónú * 8) == bọ́tìnnì_Ìtọ́ka) àfojúsùn_àdírẹ́ẹ̀sì = 위치정수(읽는자리 + 12 + ṣetúnṣe_wá_atọ̀ka_àkóónú * 8); }
                gbé_iye(Rọ́ọ̀nù + àfojúsùn_àdírẹ́ẹ̀sì); continue;
            }
            if (iye == 200) { gbé_iye(Rọ́ọ̀nù + 위치정수(Rọ́ọ̀nù + 1)); continue; }
            if (iye == 194 || iye == 195) {
                int nǹkan_Ìtọ́ka = 빼기(2);
                if (iye == 195) 잠금풀기(nǹkan_Ìtọ́ka);
                else if (!잠금얻기(nǹkan_Ìtọ́ka) && !àṣìṣe) { 넣기(nǹkan_Ìtọ́ka, 2); 틀위치[férèmù_wá_atọ̀ka_àkóónú] = Rọ́ọ̀nù; }
                continue;
            }
            if (iye == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) kọ_agbègbè(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); kọ_agbègbè(항목자리, 1); }
                else ìkùnà_iye("unsupported wide opcode");
                continue;
            }
            ìkùnà_iye("unsupported bytecode");
        }
    }
    static int wá_ọ̀wọ́_Ìsọ̀tumọ̀(int Orúkọ) {
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 종수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú] != 0 && 같은말(ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú], Orúkọ)) return ṣetúnṣe_wá_atọ̀ka_àkóónú;
        return ki_ọ̀wọ́_Ìsọ̀tumọ̀(aláìṣeéyípadà_SMS(Orúkọ));
    }
    static int ki_ọ̀wọ́_Ìsọ̀tumọ̀(int orúkọ_fọ́nrán) {
        if (!nǹkan_iye(orúkọ_fọ́nrán, 1)) return -1;
        int gígùn_iye = 힙[orúkọ_fọ́nrán + 1];
        if (gígùn_iye < 1 || gígùn_iye > 505 || 종수 == 16) { ìkùnà_iye("class name/count limit"); return -1; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < gígùn_iye; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int kóòdù_ẹyọ_ọ̀rọ̀ = 힙[orúkọ_fọ́nrán + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú]; fáìlì_orúkọ_SMS[ṣetúnṣe_wá_atọ̀ka_àkóónú] = kóòdù_ẹyọ_ọ̀rọ̀ == '/' ? '.' : kóòdù_ẹyọ_ọ̀rọ̀; }
        fáìlì_orúkọ_SMS[gígùn_iye] = '.'; fáìlì_orúkọ_SMS[gígùn_iye + 1] = 'c'; fáìlì_orúkọ_SMS[gígùn_iye + 2] = 'l'; fáìlì_orúkọ_SMS[gígùn_iye + 3] = 'a'; fáìlì_orúkọ_SMS[gígùn_iye + 4] = 's'; fáìlì_orúkọ_SMS[gígùn_iye + 5] = 's'; fáìlì_orúkọ_SMS[gígùn_iye + 6] = 0;
        int Ìwọ̀n = aṣàmúlò.파일읽기(fáìlì_orúkọ_SMS, 임시파일);
        if (Ìwọ̀n < 0) { ìkùnà_iye("ClassNotFoundException"); return -1; }
        int ọ̀wọ́_Ìsọ̀tumọ̀ = 종수++; ọ̀wọ́_Ìsọ̀tumọ̀_ìwọn[ọ̀wọ́_Ìsọ̀tumọ̀] = Ìwọ̀n;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) Fáìlì[ọ̀wọ́_Ìsọ̀tumọ̀ * 16384 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 임시파일[ṣetúnṣe_wá_atọ̀ka_àkóónú];
        클래스읽기(ọ̀wọ́_Ìsọ̀tumọ̀); if (àṣìṣe) return -1;
        int gangan_détà = aláìṣeéyípadà_SMS(ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ọ̀wọ́_Ìsọ̀tumọ̀]);
        if (!글같음(gangan_détà, orúkọ_fọ́nrán, true)) { ìkùnà_iye("class name does not match file"); return -1; }
        int 부모 = 종부모[ọ̀wọ́_Ìsọ̀tumọ̀];
        if (부모 != 0 && !Ọ̀rọ̀_SMS(부모, "java/lang/Object") && !Ọ̀rọ̀_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = wá_ọ̀wọ́_Ìsọ̀tumọ̀(부모);
            if (àṣìṣe || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == ọ̀wọ́_Ìsọ̀tumọ̀) { ìkùnà_iye("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int fáìlì_wá_atọ̀ka_àkóónú = 0; fáìlì_wá_atọ̀ka_àkóónú < 칸수; fáìlì_wá_atọ̀ka_àkóónú++) if (ààyè_ìfàyọkàsí_Oníǹkan[fáìlì_wá_atọ̀ka_àkóónú] == ọ̀wọ́_Ìsọ̀tumọ̀ && (ààyè_ìfàyọkàsí_ìyànda[fáìlì_wá_atọ̀ka_àkóónú] & 8) == 0) 칸위치[fáìlì_wá_atọ̀ka_àkóónú] += 시작변위;
            종칸수[ọ̀wọ́_Ìsọ̀tumọ̀] += 시작변위;
        }
        return ọ̀wọ́_Ìsọ̀tumọ̀;
    }
    static int 부모종(int ọ̀wọ́_Ìsọ̀tumọ̀) {
        int Orúkọ = 종부모[ọ̀wọ́_Ìsọ̀tumọ̀];
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 종수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (Orúkọ != 0 && ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú] != 0 && 같은말(ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú], Orúkọ)) return ṣetúnṣe_wá_atọ̀ka_àkóónú;
        return -1;
    }
    static int wá_ìlànà(int ọ̀wọ́_Ìsọ̀tumọ̀, int Orúkọ, int ìgúnrégé_iye) {
        for (int 깊이 = 0; ọ̀wọ́_Ìsọ̀tumọ̀ >= 0 && 깊이 < 16; 깊이++, ọ̀wọ́_Ìsọ̀tumọ̀ = 부모종(ọ̀wọ́_Ìsọ̀tumọ̀)) {
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 함수수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (ìlànà_Oníǹkan[ṣetúnṣe_wá_atọ̀ka_àkóónú] == ọ̀wọ́_Ìsọ̀tumọ̀ && 같은말(ìlànà_orúkọ_SMS[ṣetúnṣe_wá_atọ̀ka_àkóónú], Orúkọ) && 같은말(ìlànà_irú[ṣetúnṣe_wá_atọ̀ka_àkóónú], ìgúnrégé_iye)) return ṣetúnṣe_wá_atọ̀ka_àkóónú;
        }
        return -1;
    }
    static int orúkọ_ìlànà(int ọ̀wọ́_Ìsọ̀tumọ̀, String Orúkọ, String ìgúnrégé_iye) {
        for (int 깊이 = 0; ọ̀wọ́_Ìsọ̀tumọ̀ >= 0 && 깊이 < 16; 깊이++, ọ̀wọ́_Ìsọ̀tumọ̀ = 부모종(ọ̀wọ́_Ìsọ̀tumọ̀))
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 함수수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (ìlànà_Oníǹkan[ṣetúnṣe_wá_atọ̀ka_àkóónú] == ọ̀wọ́_Ìsọ̀tumọ̀ && Ọ̀rọ̀_SMS(ìlànà_orúkọ_SMS[ṣetúnṣe_wá_atọ̀ka_àkóónú], Orúkọ) && Ọ̀rọ̀_SMS(ìlànà_irú[ṣetúnṣe_wá_atọ̀ka_àkóónú], ìgúnrégé_iye)) return ṣetúnṣe_wá_atọ̀ka_àkóónú;
        return -1;
    }
    static int 형종류(int Orúkọ) { return Fáìlì[상가[Orúkọ]] == 'L' || Fáìlì[상가[Orúkọ]] == '[' ? 2 : 1; }
    static boolean pàjùbà(int ọ̀wọ́_Ìsọ̀tumọ̀, int àṣẹ_bẹ̀rẹ̀) {
        if (ọ̀wọ́_Ìsọ̀tumọ̀ < 0 || àṣìṣe) return false;
        if (ọ̀wọ́_Ìsọ̀tumọ̀_ipò[ọ̀wọ́_Ìsọ̀tumọ̀] == 3) { ìkùnà_iye("NoClassDefFoundError: initialization failed"); return false; }
        if (ọ̀wọ́_Ìsọ̀tumọ̀_ipò[ọ̀wọ́_Ìsọ̀tumọ̀] == 1 && ọ̀wọ́_èròjà_atẹ̀lélànà[ọ̀wọ́_Ìsọ̀tumọ̀] != 현재가닥) { 틀위치[férèmù_wá_atọ̀ka_àkóónú] = àṣẹ_bẹ̀rẹ̀; 바꿈요청 = true; return false; }
        if (ọ̀wọ́_Ìsọ̀tumọ̀_ipò[ọ̀wọ́_Ìsọ̀tumọ̀] != 0) return true;
        int 위 = 부모종(ọ̀wọ́_Ìsọ̀tumọ̀);
        if (위 >= 0 && !pàjùbà(위, àṣẹ_bẹ̀rẹ̀)) return false;
        ọ̀wọ́_Ìsọ̀tumọ̀_ipò[ọ̀wọ́_Ìsọ̀tumọ̀] = 1; ọ̀wọ́_èròjà_atẹ̀lélànà[ọ̀wọ́_Ìsọ̀tumọ̀] = 현재가닥;
        if (pàjùbà_ọ̀wọ́_Ìsọ̀tumọ̀[ọ̀wọ́_Ìsọ̀tumọ̀] != 0) {
            틀위치[férèmù_wá_atọ̀ka_àkóónú] = àṣẹ_bẹ̀rẹ̀;
            호출(pàjùbà_ọ̀wọ́_Ìsọ̀tumọ̀[ọ̀wọ́_Ìsọ̀tumọ̀] - 1); if (!àṣìṣe) pàjùbà_férèmù[férèmù_wá_atọ̀ka_àkóónú] = ọ̀wọ́_Ìsọ̀tumọ̀ + 1;
            return false;
        }
        ọ̀wọ́_Ìsọ̀tumọ̀_ipò[ọ̀wọ́_Ìsọ̀tumọ̀] = 2; return true;
    }
    static void 필드호출(int wá_atọ̀ka_àkóónú, int Àṣẹ, int Rọ́ọ̀nù) {
        if (!ṣàyẹ̀wò_aláìṣeéyípadà(wá_atọ̀ka_àkóónú, 9)) return;
        int Oníǹkan_iye = ọ̀wọ́_orúkọ_SMS(상가[wá_atọ̀ka_àkóónú]), Orúkọ = Ìtọ́ka_orúkọ(상나[wá_atọ̀ka_àkóónú]), ìgúnrégé_iye = Ìtọ́ka_irú(상나[wá_atọ̀ka_àkóónú]);
        if (Ọ̀rọ̀_SMS(Oníǹkan_iye, "java/lang/System") && (Ọ̀rọ̀_SMS(Orúkọ, "out") || Ọ̀rọ̀_SMS(Orúkọ, "err")) && Ọ̀rọ̀_SMS(ìgúnrégé_iye, "Ljava/io/PrintStream;") && Àṣẹ == 178) { 넣기(-1, 2); return; }
        int ọ̀wọ́_Ìsọ̀tumọ̀ = wá_ọ̀wọ́_Ìsọ̀tumọ̀(Oníǹkan_iye); if (ọ̀wọ́_Ìsọ̀tumọ̀ < 0 || àṣìṣe) return;
        int 찾음 = -1;
        for (int 읽는자리 = ọ̀wọ́_Ìsọ̀tumọ̀, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int fáìlì_wá_atọ̀ka_àkóónú = 0; fáìlì_wá_atọ̀ka_àkóónú < 칸수; fáìlì_wá_atọ̀ka_àkóónú++) if (ààyè_ìfàyọkàsí_Oníǹkan[fáìlì_wá_atọ̀ka_àkóónú] == 읽는자리 && 같은말(ààyè_ìfàyọkàsí_orúkọ[fáìlì_wá_atọ̀ka_àkóónú], Orúkọ) && 같은말(ààyè_ìfàyọkàsí_irú[fáìlì_wá_atọ̀ka_àkóónú], ìgúnrégé_iye)) 찾음 = fáìlì_wá_atọ̀ka_àkóónú;
        if (찾음 < 0) { ìkùnà_iye("NoSuchFieldError"); return; }
        boolean ìdágún_iye = Àṣẹ == 178 || Àṣẹ == 179;
        if (ìdágún_iye != ((ààyè_ìfàyọkàsí_ìyànda[찾음] & 8) != 0)) { ìkùnà_iye("field static/instance mismatch"); return; }
        if (ìdágún_iye && !pàjùbà(ààyè_ìfàyọkàsí_Oníǹkan[찾음], Rọ́ọ̀nù)) return;
        int irú_iye = 형종류(ìgúnrégé_iye), iye = 0;
        if (Àṣẹ == 179 || Àṣẹ == 181) iye = 빼기(irú_iye);
        if (ìdágún_iye) { if (Àṣẹ == 178) 넣기(ààyè_ìfàyọkàsí_détà[찾음], irú_iye); else if (!àṣìṣe) ààyè_ìfàyọkàsí_détà[찾음] = iye; return; }
        int nǹkan_Ìtọ́ka = 빼기(2);
        if (!객체유효(nǹkan_Ìtọ́ka)) return;
        if (힙[nǹkan_Ìtọ́ka] < 32 || !종포함(힙[nǹkan_Ìtọ́ka] - 32, Oníǹkan_iye)) { ìkùnà_iye("field receiver type mismatch"); return; }
        int 보관칸 = nǹkan_Ìtọ́ka + 2 + 칸위치[찾음];
        if (Àṣẹ == 180) 넣기(힙[보관칸], irú_iye);
        else if (!àṣìṣe) { 힙[보관칸] = iye; 힙참조[보관칸] = irú_iye == 2 ? 1 : 0; }
    }
    static boolean 종포함(int ọ̀wọ́_Ìsọ̀tumọ̀, int Orúkọ) {
        for (int 중첩깊이 = 0; ọ̀wọ́_Ìsọ̀tumọ̀ >= 0 && 중첩깊이 < 16; 중첩깊이++, ọ̀wọ́_Ìsọ̀tumọ̀ = 부모종(ọ̀wọ́_Ìsọ̀tumọ̀)) {
            if (같은말(ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ọ̀wọ́_Ìsọ̀tumọ̀], Orúkọ) || (종부모[ọ̀wọ́_Ìsọ̀tumọ̀] != 0 && 같은말(종부모[ọ̀wọ́_Ìsọ̀tumọ̀], Orúkọ))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[ọ̀wọ́_Ìsọ̀tumọ̀]; 안쪽자리++) if (같은말(ọ̀wọ́_atọ́kùn[ọ̀wọ́_Ìsọ̀tumọ̀ * 16 + 안쪽자리], Orúkọ)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int báìtì_détà, boolean ọ̀nà) {
        if (첫값 == báìtì_détà) return true;
        if (첫값 <= 0 || báìtì_détà <= 0 || 힙[첫값] != 1 || 힙[báìtì_détà] != 1 || 힙[첫값 + 1] != 힙[báìtì_détà + 1]) return false;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 힙[첫값 + 1]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int ibi_ìtọ́kasí_x = 힙[첫값 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú], 세로좌표 = 힙[báìtì_détà + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
            if (ọ̀nà) { if (ibi_ìtọ́kasí_x == '.') ibi_ìtọ́kasí_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (ibi_ìtọ́kasí_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int nǹkan_Ìtọ́ka) {
        if (nǹkan_Ìtọ́ka == 0) { ìkùnà_iye("NullPointerException"); return false; }
        if (nǹkan_Ìtọ́ka < 1 || nǹkan_Ìtọ́ka >= 힙끝 || 힙폭[nǹkan_Ìtọ́ka] < 2 || 힙[nǹkan_Ìtọ́ka] == 0) { ìkùnà_iye("invalid object reference"); return false; }
        return true;
    }
    static void dáàbòbò_iye(int nǹkan_Ìtọ́ka) {
        if (nǹkan_Ìtọ́ka > 0 && nǹkan_Ìtọ́ka < 힙끝 && 힙폭[nǹkan_Ìtọ́ka] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = nǹkan_Ìtọ́ka;
    }
    static void ṣàfihàn_iye(int nǹkan_Ìtọ́ka) {
        if (nǹkan_Ìtọ́ka > 0 && nǹkan_Ìtọ́ka < 힙끝 && 힙폭[nǹkan_Ìtọ́ka] >= 2 && 힙[nǹkan_Ìtọ́ka] != 0 && 힙표시[nǹkan_Ìtọ́ka] == 0) {
            힙표시[nǹkan_Ìtọ́ka] = 1; 표시대기[표시수++] = nǹkan_Ìtọ́ka;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < fọ́nrán_Ìtọ́ka.length; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàfihàn_iye(fọ́nrán_Ìtọ́ka[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 칸수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if ((ààyè_ìfàyọkàsí_ìyànda[ṣetúnṣe_wá_atọ̀ka_àkóónú] & 8) != 0 && 형종류(ààyè_ìfàyọkàsí_irú[ṣetúnṣe_wá_atọ̀ka_àkóónú]) == 2) ṣàfihàn_iye(ààyè_ìfàyọkàsí_détà[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            ṣàfihàn_iye(èròjà_atẹ̀lélànà_nǹkan[임시값]); ṣàfihàn_iye(èròjà_atẹ̀lélànà_àfojúsùn[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? férèmù_wá_atọ̀ka_àkóónú : èròjà_atẹ̀lélànà_férèmù[임시값];
            for (int fáìlì_wá_atọ̀ka_àkóónú = 임시값 * 32; fáìlì_wá_atọ̀ka_àkóónú <= 꼭대기자리; fáìlì_wá_atọ̀ka_àkóónú++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[férèmù_ìlànà[fáìlì_wá_atọ̀ka_àkóónú]]; 안쪽자리++) if (agbègbè_irú[fáìlì_wá_atọ̀ka_àkóónú * 128 + 안쪽자리] == 2) ṣàfihàn_iye(agbègbè_iye[fáìlì_wá_atọ̀ka_àkóónú * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < férèmù_kójọ[fáìlì_wá_atọ̀ka_àkóónú]; 안쪽자리++) if (스택형[fáìlì_wá_atọ̀ka_àkóónú * 128 + 안쪽자리] == 2) ṣàfihàn_iye(스택값[fáìlì_wá_atọ̀ka_àkóónú * 128 + 안쪽자리]);
            }
        }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 화면참조.length; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàfihàn_iye(화면참조[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 나중수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàfihàn_iye(나중실행[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Store_nọ́ńbà_odindi.length; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàfihàn_iye(Store_nọ́ńbà_odindi[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 종수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàfihàn_iye(종잠금[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) ṣàfihàn_iye(검사자리);
        ṣàfihàn_iye(던진객체);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 잠시수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàfihàn_iye(잠시참조[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        while (표시수 > 0) {
            int nǹkan_Ìtọ́ka = 표시대기[--표시수], 분류코드 = 힙[nǹkan_Ìtọ́ka];
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = nǹkan_Ìtọ́ka + 2; ṣetúnṣe_wá_atọ̀ka_àkóónú < nǹkan_Ìtọ́ka + 힙폭[nǹkan_Ìtọ́ka]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[ṣetúnṣe_wá_atọ̀ka_àkóónú] != 0) ṣàfihàn_iye(힙[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int gígùn_iye) {
        if (gígùn_iye < 0) { ìkùnà_iye("NegativeArraySizeException"); return 0; }
        if (gígùn_iye > 힙.length - 3) { ìkùnà_iye("object heap exhausted"); return 0; }
        int 필요수 = gígùn_iye + 2, nǹkan_Ìtọ́ka = 0;
        if (필요수 <= 힙.length - 힙끝) { nǹkan_Ìtọ́ka = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { nǹkan_Ìtọ́ka = 읽는자리; break; }
            if (nǹkan_Ìtọ́ka != 0) {
                int 남은길이 = 힙폭[nǹkan_Ìtọ́ka] - 필요수;
                if (남은길이 >= 2) { 힙폭[nǹkan_Ìtọ́ka + 필요수] = 남은길이; 힙[nǹkan_Ìtọ́ka + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { nǹkan_Ìtọ́ka = 힙끝; 힙끝 += 필요수; }
        }
        if (nǹkan_Ìtọ́ka == 0) { ìkùnà_iye("object heap exhausted"); return 0; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 필요수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { 힙[nǹkan_Ìtọ́ka + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 0; 힙참조[nǹkan_Ìtọ́ka + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 0; 힙폭[nǹkan_Ìtọ́ka + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 0; }
        ÀRÉÈ_ìdá_ìpìlẹ̀[nǹkan_Ìtọ́ka] = 0;
        힙폭[nǹkan_Ìtọ́ka] = 필요수; 힙[nǹkan_Ìtọ́ka] = 종류; 힙[nǹkan_Ìtọ́ka + 1] = gígùn_iye; dáàbòbò_iye(nǹkan_Ìtọ́ka); return nǹkan_Ìtọ́ka;
    }
    static int 예외종(String orúkọ_aláìṣeéyípadà) {
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/Throwable")) return 1;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/Exception")) return 2;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/io/IOException")) return 11;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(orúkọ_aláìṣeéyípadà, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Orúkọ) {
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 1; ṣetúnṣe_wá_atọ̀ka_àkóónú <= 41; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (Ọ̀rọ̀_SMS(Orúkọ, 예외이름(ṣetúnṣe_wá_atọ̀ka_àkóónú))) return ṣetúnṣe_wá_atọ̀ka_àkóónú;
        return 0;
    }
    static String 예외이름(int àkọọ́lẹ̀_iye) {
        if (àkọọ́lẹ̀_iye == 40) return "java/lang/InterruptedException";
        if (àkọọ́lẹ̀_iye == 41) return "한국어/자체/대기중단예외";
        if (àkọọ́lẹ̀_iye == 39) return "java/net/SocketException";
        if (àkọọ́lẹ̀_iye == 20) return "한국어/자체/예외";
        if (àkọọ́lẹ̀_iye == 21) return "한국어/자체/실행예외";
        if (àkọọ́lẹ̀_iye == 22) return "한국어/자체/입출력예외";
        if (àkọọ́lẹ̀_iye == 23) return "한국어/자체/대기시간초과예외";
        if (àkọọ́lẹ̀_iye == 24) return "한국어/자체/주소확인예외";
        if (àkọọ́lẹ̀_iye == 25) return "한국어/자체/파일없음예외";
        if (àkọọ́lẹ̀_iye == 26) return "한국어/자체/통신예외";
        if (àkọọ́lẹ̀_iye == 27) return "한국어/자체/잘못된인수예외";
        if (àkọọ́lẹ̀_iye == 28) return "한국어/자체/숫자형식예외";
        if (àkọọ́lẹ̀_iye == 29) return "한국어/자체/범위예외";
        if (àkọọ́lẹ̀_iye == 30) return "한국어/자체/배열범위예외";
        if (àkọọ́lẹ̀_iye == 31) return "한국어/자체/문자열범위예외";
        if (àkọọ́lẹ̀_iye == 32) return "한국어/자체/빈참조예외";
        if (àkọọ́lẹ̀_iye == 33) return "한국어/자체/산술예외";
        if (àkọọ́lẹ̀_iye == 34) return "한국어/자체/상태예외";
        if (àkọọ́lẹ̀_iye == 35) return "한국어/자체/형변환예외";
        if (àkọọ́lẹ̀_iye == 36) return "한국어/자체/음수배열크기예외";
        if (àkọọ́lẹ̀_iye == 37) return "한국어/자체/ÀRÉÈ_Store_ìkùnà";
        if (àkọọ́lẹ̀_iye == 38) return "한국어/자체/가닥상태예외";
        if (àkọọ́lẹ̀_iye == 1) return "java/lang/Throwable"; if (àkọọ́lẹ̀_iye == 2) return "java/lang/Exception";
        if (àkọọ́lẹ̀_iye == 3) return "java/lang/RuntimeException"; if (àkọọ́lẹ̀_iye == 4) return "java/lang/ArithmeticException";
        if (àkọọ́lẹ̀_iye == 5) return "java/lang/NullPointerException"; if (àkọọ́lẹ̀_iye == 6) return "java/lang/IndexOutOfBoundsException";
        if (àkọọ́lẹ̀_iye == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (àkọọ́lẹ̀_iye == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (àkọọ́lẹ̀_iye == 9) return "java/lang/IllegalArgumentException"; if (àkọọ́lẹ̀_iye == 10) return "java/lang/NumberFormatException";
        if (àkọọ́lẹ̀_iye == 11) return "java/io/IOException"; if (àkọọ́lẹ̀_iye == 12) return "java/io/FileNotFoundException";
        if (àkọọ́lẹ̀_iye == 17) return "java/lang/ArrayStoreException";
        if (àkọọ́lẹ̀_iye == 18) return "java/net/UnknownHostException";
        if (àkọọ́lẹ̀_iye == 19) return "java/net/SocketTimeoutException";
        if (àkọọ́lẹ̀_iye == 16) return "java/lang/IllegalThreadStateException";
        if (àkọọ́lẹ̀_iye == 13) return "java/lang/IllegalStateException"; if (àkọọ́lẹ̀_iye == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int àkọọ́lẹ̀_iye) {
        if (àkọọ́lẹ̀_iye == 40) return 2;
        if (àkọọ́lẹ̀_iye == 41) return 40;
        if (àkọọ́lẹ̀_iye == 39) return 11;
        if (àkọọ́lẹ̀_iye == 1) return 0;
        if (àkọọ́lẹ̀_iye == 2) return 1;
        if (àkọọ́lẹ̀_iye == 3) return 2;
        if (àkọọ́lẹ̀_iye == 4) return 3;
        if (àkọọ́lẹ̀_iye == 5) return 3;
        if (àkọọ́lẹ̀_iye == 6) return 3;
        if (àkọọ́lẹ̀_iye == 7) return 6;
        if (àkọọ́lẹ̀_iye == 8) return 6;
        if (àkọọ́lẹ̀_iye == 9) return 3;
        if (àkọọ́lẹ̀_iye == 10) return 9;
        if (àkọọ́lẹ̀_iye == 11) return 2;
        if (àkọọ́lẹ̀_iye == 12) return 11;
        if (àkọọ́lẹ̀_iye == 13) return 3;
        if (àkọọ́lẹ̀_iye == 14) return 3;
        if (àkọọ́lẹ̀_iye == 15) return 3;
        if (àkọọ́lẹ̀_iye == 16) return 9;
        if (àkọọ́lẹ̀_iye == 17) return 3;
        if (àkọọ́lẹ̀_iye == 18) return 11;
        if (àkọọ́lẹ̀_iye == 19) return 11;
        if (àkọọ́lẹ̀_iye == 20) return 2;
        if (àkọọ́lẹ̀_iye == 21) return 3;
        if (àkọọ́lẹ̀_iye == 22) return 11;
        if (àkọọ́lẹ̀_iye == 23) return 22;
        if (àkọọ́lẹ̀_iye == 24) return 22;
        if (àkọọ́lẹ̀_iye == 25) return 22;
        if (àkọọ́lẹ̀_iye == 26) return 22;
        if (àkọọ́lẹ̀_iye == 27) return 9;
        if (àkọọ́lẹ̀_iye == 28) return 27;
        if (àkọọ́lẹ̀_iye == 29) return 6;
        if (àkọọ́lẹ̀_iye == 30) return 29;
        if (àkọọ́lẹ̀_iye == 31) return 29;
        if (àkọọ́lẹ̀_iye == 32) return 5;
        if (àkọọ́lẹ̀_iye == 33) return 4;
        if (àkọọ́lẹ̀_iye == 34) return 13;
        if (àkọọ́lẹ̀_iye == 35) return 14;
        if (àkọọ́lẹ̀_iye == 36) return 15;
        if (àkọọ́lẹ̀_iye == 37) return 17;
        if (àkọọ́lẹ̀_iye == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int gangan_iye, int 요구값) {
        for (int 깊이 = 0; gangan_iye != 0 && 깊이 < 16; 깊이++, gangan_iye = 예외부모(gangan_iye))
            if (gangan_iye == 요구값) return true;
        return false;
    }
    static void 예외던짐(int àkọọ́lẹ̀_iye, String KÀ_MÍ_Ìtọ́ka) {
        int nǹkan_Ìtọ́ka = 새기억(9, 2); if (àṣìṣe) return;
        힙[nǹkan_Ìtọ́ka + 2] = àkọọ́lẹ̀_iye; 힙[nǹkan_Ìtọ́ka + 3] = olùpèsè_ẹyọ_ọ̀rọ̀(KÀ_MÍ_Ìtọ́ka); 힙참조[nǹkan_Ìtọ́ka + 3] = 1;
        던진객체 = nǹkan_Ìtọ́ka; àṣìṣe = true;
    }
    static boolean 맞는객체(int nǹkan_Ìtọ́ka, int Orúkọ) {
        if (nǹkan_Ìtọ́ka == 0) return true;
        if (!객체유효(nǹkan_Ìtọ́ka)) return false;
        int 분류코드 = 힙[nǹkan_Ìtọ́ka];
        if (Ọ̀rọ̀_SMS(Orúkọ, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Orúkọ);
        if (분류코드 == 9) { int àfojúsùn_àdírẹ́ẹ̀sì = 예외상수(Orúkọ); return àfojúsùn_àdírẹ́ẹ̀sì != 0 && 예외포함(힙[nǹkan_Ìtọ́ka + 2], àfojúsùn_àdírẹ́ẹ̀sì); }
        if (분류코드 == 1) return Ọ̀rọ̀_SMS(Orúkọ, "java/lang/String") || Ọ̀rọ̀_SMS(Orúkọ, "java/lang/CharSequence");
        if (분류코드 == 4) return Ọ̀rọ̀_SMS(Orúkọ, "java/lang/StringBuilder") || Ọ̀rọ̀_SMS(Orúkọ, "java/lang/CharSequence");
        if (분류코드 == 10) return Ọ̀rọ̀_SMS(Orúkọ, "java/util/ArrayList") || Ọ̀rọ̀_SMS(Orúkọ, "java/util/List");
        if (분류코드 == 11) return Ọ̀rọ̀_SMS(Orúkọ, "java/util/HashMap") || Ọ̀rọ̀_SMS(Orúkọ, "java/util/Map");
        if (분류코드 == 12) return Ọ̀rọ̀_SMS(Orúkọ, "java/lang/Integer") || Ọ̀rọ̀_SMS(Orúkọ, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[nǹkan_Ìtọ́ka + 13] != 0) return 한국어화면종(Orúkọ) == 분류코드 || Ọ̀rọ̀_SMS(Orúkọ, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Orúkọ) == 0 && 화면종(Orúkọ) == 분류코드) || Ọ̀rọ̀_SMS(Orúkọ, "java/awt/Component") || Ọ̀rọ̀_SMS(Orúkọ, "java/awt/Container") || Ọ̀rọ̀_SMS(Orúkọ, "javax/swing/JComponent");
        if (분류코드 == 29) return Ọ̀rọ̀_SMS(Orúkọ, 힙[nǹkan_Ìtọ́ka + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Ọ̀rọ̀_SMS(Orúkọ, "java/awt/FlowLayout") || Ọ̀rọ̀_SMS(Orúkọ, "java/awt/LayoutManager");
        if (분류코드 == 17) return Ọ̀rọ̀_SMS(Orúkọ, "java/net/Socket");
        if (분류코드 == 18) return Ọ̀rọ̀_SMS(Orúkọ, "java/net/ServerSocket");
        if (분류코드 == 19) return Ọ̀rọ̀_SMS(Orúkọ, 힙[nǹkan_Ìtọ́ka + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Ọ̀rọ̀_SMS(Orúkọ, "java/net/InetAddress");
        if (분류코드 == 15) return Ọ̀rọ̀_SMS(Orúkọ, "java/net/DatagramSocket");
        if (분류코드 == 16) return Ọ̀rọ̀_SMS(Orúkọ, "java/net/DatagramPacket");
        if (분류코드 == 13) return Ọ̀rọ̀_SMS(Orúkọ, 힙[nǹkan_Ìtọ́ka + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Ọ̀rọ̀_SMS(Orúkọ, "[I"); if (분류코드 == 20) return Ọ̀rọ̀_SMS(Orúkọ, "[B"); if (분류코드 == 21) return Ọ̀rọ̀_SMS(Orúkọ, "[Z");
        if (분류코드 == 22) return Ọ̀rọ̀_SMS(Orúkọ, "[C"); if (분류코드 == 23) return Ọ̀rọ̀_SMS(Orúkọ, "[S");
        if (분류코드 != 3) return false;
        if (Ọ̀rọ̀_SMS(Orúkọ, "[Ljava/lang/Object;")) return true;
        int ẹ̀yà = ÀRÉÈ_ìdá_ìpìlẹ̀[nǹkan_Ìtọ́ka];
        if (ẹ̀yà == -1) return Ọ̀rọ̀_SMS(Orúkọ, "[Ljava/lang/String;") || Ọ̀rọ̀_SMS(Orúkọ, "[Ljava/lang/CharSequence;");
        if (ẹ̀yà == 0) return false;
        if (배열종비교(ẹ̀yà, Orúkọ)) return true;
        if ((Ọ̀rọ̀_SMS(ẹ̀yà, "java/lang/String") || Ọ̀rọ̀_SMS(ẹ̀yà, "java/lang/StringBuilder")) && Ọ̀rọ̀_SMS(Orúkọ, "[Ljava/lang/CharSequence;")) return true;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 종수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (같은말(ọ̀wọ́_Ìsọ̀tumọ̀_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú], ẹ̀yà)) {
            for (int kóòdù_ẹyọ_ọ̀rọ̀ = ṣetúnṣe_wá_atọ̀ka_àkóónú, 중첩깊이 = 0; kóòdù_ẹyọ_ọ̀rọ̀ >= 0 && 중첩깊이 < 16; 중첩깊이++, kóòdù_ẹyọ_ọ̀rọ̀ = 부모종(kóòdù_ẹyọ_ọ̀rọ̀)) {
                if (배열종비교(종부모[kóòdù_ẹyọ_ọ̀rọ̀], Orúkọ)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[kóòdù_ẹyọ_ọ̀rọ̀]; 안쪽자리++) if (배열종비교(ọ̀wọ́_atọ́kùn[kóòdù_ẹyọ_ọ̀rọ̀ * 16 + 안쪽자리], Orúkọ)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int orúkọ_aláìṣeéyípadà, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (orúkọ_aláìṣeéyípadà == 0 || 항목수 < 4 || Fáìlì[검사자리] != '[' || Fáìlì[검사자리 + 1] != 'L' || Fáìlì[검사자리 + 항목수 - 1] != ';' || 상나[orúkọ_aláìṣeéyípadà] != 항목수 - 3) return false;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수 - 3; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (Fáìlì[상가[orúkọ_aláìṣeéyípadà] + ṣetúnṣe_wá_atọ̀ka_àkóónú] != Fáìlì[검사자리 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        àṣìṣe = false;
        while (férèmù_wá_atọ̀ka_àkóónú >= 현재가닥 * 32) {
            int fáìlì_wá_atọ̀ka_àkóónú = férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú], 읽는자리 = férèmù_ìtọ́sọ́nà[férèmù_wá_atọ̀ka_àkóónú];
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 잡기수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (잡기함수[ṣetúnṣe_wá_atọ̀ka_àkóónú] == fáìlì_wá_atọ̀ka_àkóónú && 읽는자리 >= 잡기시작[ṣetúnṣe_wá_atọ̀ka_àkóónú] && 읽는자리 < 잡기끝[ṣetúnṣe_wá_atọ̀ka_àkóónú]
                && (잡기종[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 0 || 맞는객체(던진객체, 잡기종[ṣetúnṣe_wá_atọ̀ka_àkóónú]))) {
                틀위치[férèmù_wá_atọ̀ka_àkóónú] = 잡기위치[ṣetúnṣe_wá_atọ̀ka_àkóónú]; férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (pàjùbà_férèmù[férèmù_wá_atọ̀ka_àkóónú] != 0) ọ̀wọ́_Ìsọ̀tumọ̀_ipò[pàjùbà_férèmù[férèmù_wá_atọ̀ka_àkóónú] - 1] = 3;
            if (틀잠금[férèmù_wá_atọ̀ka_àkóónú] != 0) { 잠금풀기(틀잠금[férèmù_wá_atọ̀ka_àkóónú]); 틀잠금[férèmù_wá_atọ̀ka_àkóónú] = 0; }
            férèmù_wá_atọ̀ka_àkóónú--;
        }
        aṣàmúlò.Kọ("Uncaught ");
        if (힙[던진객체] == 9) { aṣàmúlò.Kọ(예외이름(힙[던진객체 + 2])); aṣàmúlò.Kọ(": "); kọ_SMS(힙[던진객체 + 3]); }
        else aṣàmúlò.Kọ("user exception");
        aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10); 던진객체 = 0; àṣìṣe = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void kójọ_ìtọ́sọ́nà(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int báìtì_détà = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식); 넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(báìtì_détà, 둘째형식); return; }
        int kóòdù_ẹyọ_ọ̀rọ̀ = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(kóòdù_ẹyọ_ọ̀rọ̀, 셋째형식); 넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식); 넣기(kóòdù_ẹyọ_ọ̀rọ̀, 셋째형식); 넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kóòdù_ẹyọ_ọ̀rọ̀, 셋째형식); 넣기(báìtì_détà, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int orúkọ_aláìṣeéyípadà, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(orúkọ_aláìṣeéyípadà);
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/lang/Thread") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(orúkọ_aláìṣeéyípadà) != 0) { 분류코드 = 화면종(orúkọ_aláìṣeéyípadà); 유효길이 = 12; }
        if (분류코드 == 0) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = wá_ọ̀wọ́_Ìsọ̀tumọ̀(orúkọ_aláìṣeéyípadà); if (kóòdù_ẹyọ_ọ̀rọ̀ < 0 || àṣìṣe || !pàjùbà(kóòdù_ẹyọ_ọ̀rọ̀, 시작점)) return;
            분류코드 = 32 + kóòdù_ẹyọ_ọ̀rọ̀; 유효길이 = 종칸수[kóòdù_ẹyọ_ọ̀rọ̀];
        }
        int nǹkan_Ìtọ́ka = pín_Ibi_ìpamọ́(분류코드, 유효길이); if (àṣìṣe) return;
        if (분류코드 == 13 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/작업가닥")) 힙[nǹkan_Ìtọ́ka + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(orúkọ_aláìṣeéyípadà) != 0) 힙[nǹkan_Ìtọ́ka + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[nǹkan_Ìtọ́ka + 2] = -1;
        if (분류코드 == 9) 힙[nǹkan_Ìtọ́ka + 2] = 예외참조;
        넣기(nǹkan_Ìtọ́ka, 2);
    }
    static boolean 값같음(int 첫값, int báìtì_détà) {
        if (첫값 == báìtì_détà) return true;
        if (첫값 == 0 || báìtì_détà == 0 || 첫값 < 0 || báìtì_détà < 0 || 첫값 >= 힙끝 || báìtì_détà >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[báìtì_détà] == 1) return 글같음(첫값, báìtì_détà, false);
        return 힙[첫값] == 12 && 힙[báìtì_détà] == 12 && 힙[첫값 + 2] == 힙[báìtì_détà + 2];
    }
    static int 글조각(int nǹkan_Ìtọ́ka, int 시작자리, int 끝자리) {
        if (!nǹkan_iye(nǹkan_Ìtọ́ka, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[nǹkan_Ìtọ́ka + 1]) { ìkùnà_iye("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = pín_Ibi_ìpamọ́(1, 끝자리 - 시작자리); if (àṣìṣe) return 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < 끝자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[반환값 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú - 시작자리] = 힙[nǹkan_Ìtọ́ka + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        return 반환값;
    }
    static int ìsomọ́_SMS(int 첫값, int báìtì_détà) {
        if (!nǹkan_iye(첫값, 1) || !nǹkan_iye(báìtì_détà, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], ìlànà_wá_atọ̀ka_àkóónú = 힙[báìtì_détà + 1], 반환값 = pín_Ibi_ìpamọ́(1, 항목수 + ìlànà_wá_atọ̀ka_àkóónú); if (àṣìṣe) return 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[반환값 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[첫값 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ìlànà_wá_atọ̀ka_àkóónú; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[반환값 + 2 + 항목수 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[báìtì_détà + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        return 반환값;
    }
    static boolean 기본호출(int Oníǹkan, int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드) {
        if (Ọ̀rọ̀_SMS(Oníǹkan, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "개수") && Ọ̀rọ̀_SMS(서술상수, "()I")) { 넣기(aṣàmúlò.인수개수() - 1, 1); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "SMS") && Ọ̀rọ̀_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= aṣàmúlò.인수개수() - 1) 예외던짐(29, "ṣiṣẹ́_àṣẹ 인수 범위를 벗어났습니다");
                else 넣기(olùpèsè_ẹyọ_ọ̀rọ̀(aṣàmúlò.인수(순번 + 1)), 2);
                return true;
            }
            ìkùnà_iye("지원하지 않는 한국어 ṣiṣẹ́_àṣẹ 인수 호출"); return true;
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "한국어/자체/작업가닥")) { Ìlànà_èròjà_atẹ̀lélànà(orúkọ_aláìṣeéyípadà, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(Oníǹkan)) { 한국어화면호출(Oníǹkan, orúkọ_aláìṣeéyípadà, 서술상수, 명령코드); return true; }
        if (화면소유(Oníǹkan)) { 화면호출(Oníǹkan, orúkọ_aláìṣeéyípadà, 서술상수, 명령코드); return true; }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/net/Socket") || Ọ̀rọ̀_SMS(Oníǹkan, "java/net/ServerSocket") || Ọ̀rọ̀_SMS(Oníǹkan, "java/io/InputStream") || Ọ̀rọ̀_SMS(Oníǹkan, "java/io/OutputStream")) { 흐름호출(Oníǹkan, orúkọ_aláìṣeéyípadà, 서술상수, 명령코드); return true; }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "한국어/자체/kánẹ́ẹ̀lì_iye") && 명령코드 == 184) {
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "화면너비") && Ọ̀rọ̀_SMS(서술상수, "()I")) { 넣기(aṣàmúlò.화면너비(), 1); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "화면높이") && Ọ̀rọ̀_SMS(서술상수, "()I")) { 넣기(aṣàmúlò.화면높이(), 1); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "밀리초") && Ọ̀rọ̀_SMS(서술상수, "()I")) { 넣기(aṣàmúlò.밀리초(), 1); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "그림대기") && Ọ̀rọ̀_SMS(서술상수, "()I")) { 넣기(aṣàmúlò.그림대기(), 1); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "사각형") && Ọ̀rọ̀_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), ibi_ìtọ́kasí_x = 빼기(1); 넣기(aṣàmúlò.사각형(ibi_ìtọ́kasí_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/net/InetAddress") || Ọ̀rọ̀_SMS(Oníǹkan, "java/net/DatagramPacket") || Ọ̀rọ̀_SMS(Oníǹkan, "java/net/DatagramSocket")) { 통신호출(Oníǹkan, orúkọ_aláìṣeéyípadà, 서술상수, 명령코드); return true; }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/lang/Thread")) { 가닥호출(orúkọ_aláìṣeéyípadà, 서술상수, 명령코드); return true; }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/lang/Object")) {
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>") && Ọ̀rọ̀_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "equals") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int báìtì_détà = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == báìtì_détà ? 1 : 0, 1); return true; }
        }
        if (예외상수(Oníǹkan) != 0) {
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>") && 명령코드 == 183 && (Ọ̀rọ̀_SMS(서술상수, "()V") || Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int ìgún_ní_kẹ́ṣẹ́ = Ọ̀rọ̀_SMS(서술상수, "()V") ? 0 : 빼기(2), nǹkan_Ìtọ́ka = 빼기(2);
                if (nǹkan_iye(nǹkan_Ìtọ́ka, 9)) { 힙[nǹkan_Ìtọ́ka + 3] = ìgún_ní_kẹ́ṣẹ́; 힙참조[nǹkan_Ìtọ́ka + 3] = 1; } return true;
            }
            if ((Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getMessage") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "설명")) && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/String;")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 9)) 넣기(힙[nǹkan_Ìtọ́ka + 3], 2); return true; }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/lang/String")) {
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getBytes") && (Ọ̀rọ̀_SMS(서술상수, "()[B") || Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int pípàrokò_orúkọ = Ọ̀rọ̀_SMS(서술상수, "()[B") ? 0 : 빼기(2), nǹkan_Ìtọ́ka = 빼기(2);
                if (!nǹkan_iye(nǹkan_Ìtọ́ka, 1)) return true;
                if (pípàrokò_orúkọ != 0 && !글같음(pípàrokò_orúkọ, olùpèsè_ẹyọ_ọ̀rọ̀("UTF-8"), false) && !글같음(pípàrokò_orúkọ, olùpèsè_ẹyọ_ọ̀rọ̀("UTF8"), false) && !글같음(pípàrokò_orúkọ, olùpèsè_ẹyọ_ọ̀rọ̀("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[nǹkan_Ìtọ́ka + 1], 반환값 = pín_Ibi_ìpamọ́(20, 항목수 * 3), 사용수 = 0; if (àṣìṣe) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int kóòdù_ẹyọ_ọ̀rọ̀ = 힙[nǹkan_Ìtọ́ka + 2 + 안쪽자리];
                    if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[nǹkan_Ìtọ́ka + 3 + 안쪽자리] >= 0xdc00 && 힙[nǹkan_Ìtọ́ka + 3 + 안쪽자리] <= 0xdfff) kóòdù_ẹyọ_ọ̀rọ̀ = 0x10000 + ((kóòdù_ẹyọ_ọ̀rọ̀ - 0xd800) << 10) + 힙[nǹkan_Ìtọ́ka + 2 + ++안쪽자리] - 0xdc00;
                    else if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff) kóòdù_ẹyọ_ọ̀rọ̀ = '?';
                    if (kóòdù_ẹyọ_ọ̀rọ̀ < 128) 힙[반환값 + 2 + 사용수++] = kóòdù_ẹyọ_ọ̀rọ̀;
                    else { int 바이트수 = kóòdù_ẹyọ_ọ̀rọ̀ < 2048 ? 2 : kóòdù_ẹyọ_ọ̀rọ̀ < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | kóòdù_ẹyọ_ọ̀rọ̀ >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kóòdù_ẹyọ_ọ̀rọ̀ >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "valueOf") && Ọ̀rọ̀_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(díjììtì_ẹyọ_ọ̀rọ̀(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "equals") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int báìtì_détà = 빼기(2), 첫값 = 빼기(2); if (nǹkan_iye(첫값, 1)) 넣기(글같음(첫값, báìtì_détà, false) ? 1 : 0, 1); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isEmpty") && Ọ̀rọ̀_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (nǹkan_iye(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "substring") && (Ọ̀rọ̀_SMS(서술상수, "(I)Ljava/lang/String;") || Ọ̀rọ̀_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Ọ̀rọ̀_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (nǹkan_iye(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "concat") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int báìtì_détà = 빼기(2), 첫값 = 빼기(2); 넣기(ìsomọ́_SMS(첫값, báìtì_détà), 2); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "hashCode") && Ọ̀rọ̀_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), burú_iye = 0; if (nǹkan_iye(첫값, 1)) { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 힙[첫값 + 1]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) burú_iye = burú_iye * 31 + 힙[첫값 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú]; 넣기(burú_iye, 1); } return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "toString") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (nǹkan_iye(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/lang/Integer")) {
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "valueOf") && Ọ̀rọ̀_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int détà_iye = 빼기(1), nǹkan_Ìtọ́ka = détà_iye >= -128 && détà_iye <= 127 ? Store_nọ́ńbà_odindi[détà_iye + 128] : 0; if (nǹkan_Ìtọ́ka == 0) { nǹkan_Ìtọ́ka = pín_Ibi_ìpamọ́(12, 1); if (!àṣìṣe) { 힙[nǹkan_Ìtọ́ka + 2] = détà_iye; if (détà_iye >= -128 && détà_iye <= 127) Store_nọ́ńbà_odindi[détà_iye + 128] = nǹkan_Ìtọ́ka; } } 넣기(nǹkan_Ìtọ́ka, 2); return true; }
            if (명령코드 == 183 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>") && Ọ̀rọ̀_SMS(서술상수, "(I)V")) { int détà_iye = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 12)) 힙[nǹkan_Ìtọ́ka + 2] = détà_iye; return true; }
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "intValue") && Ọ̀rọ̀_SMS(서술상수, "()I")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 12)) 넣기(힙[nǹkan_Ìtọ́ka + 2], 1); return true; }
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "toString") && Ọ̀rọ̀_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(díjììtì_ẹyọ_ọ̀rọ̀(빼기(1)), 2); return true; }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/lang/Math") && 명령코드 == 184) {
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "abs") && Ọ̀rọ̀_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "min") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "max")) && Ọ̀rọ̀_SMS(서술상수, "(II)I")) { int báìtì_détà = 빼기(1), 첫값 = 빼기(1); 넣기(Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "min") ? (첫값 < báìtì_détà ? 첫값 : báìtì_détà) : (첫값 > báìtì_détà ? 첫값 : báìtì_détà), 1); return true; }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/lang/System") && 명령코드 == 184) {
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "gc") && Ọ̀rọ̀_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "arraycopy") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), èbúté_iye_wá_atọ̀ka_àkóónú = 빼기(1), báìtì_détà = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(báìtì_détà)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[báìtì_détà] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) ìkùnà_iye("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || èbúté_iye_wá_atọ̀ka_àkóónú < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || èbúté_iye_wá_atọ̀ka_àkóónú > 힙[báìtì_détà + 1] - 항목수) ìkùnà_iye("ArrayIndexOutOfBoundsException");
                    else if (첫값 == báìtì_détà && èbúté_iye_wá_atọ̀ka_àkóónú > 시작자리) { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 항목수 - 1; ṣetúnṣe_wá_atọ̀ka_àkóónú >= 0; ṣetúnṣe_wá_atọ̀ka_àkóónú--) 힙[báìtì_détà + 2 + èbúté_iye_wá_atọ̀ka_àkóónú + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[첫값 + 2 + 시작자리 + ṣetúnṣe_wá_atọ̀ka_àkóónú]; }
                    else { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수 && !àṣìṣe; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int détà_iye = 힙[첫값 + 2 + 시작자리 + ṣetúnṣe_wá_atọ̀ka_àkóónú]; if (분류코드 != 3 || 배열저장가능(báìtì_détà, détà_iye)) 힙[báìtì_détà + 2 + èbúté_iye_wá_atọ̀ka_àkóónú + ṣetúnṣe_wá_atọ̀ka_àkóónú] = détà_iye; } }
                }
                return true;
            }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/util/ArrayList") || Ọ̀rọ̀_SMS(Oníǹkan, "java/util/List") || Ọ̀rọ̀_SMS(Oníǹkan, "java/util/HashMap") || Ọ̀rọ̀_SMS(Oníǹkan, "java/util/Map")) {
            모음호출(Oníǹkan, orúkọ_aláìṣeéyípadà, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int nǹkan_Ìtọ́ka, int 필요수) {
        int 이전값 = 힙[nǹkan_Ìtọ́ka + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int détà_ÀRÉÈ = pín_Ibi_ìpamọ́(3, 다음자리); if (àṣìṣe) return;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 용량값; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[détà_ÀRÉÈ + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[이전값 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        힙[nǹkan_Ìtọ́ka + 2] = détà_ÀRÉÈ; 힙참조[nǹkan_Ìtọ́ka + 2] = 1;
    }
    static void 모음호출(int Oníǹkan, int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드) {
        boolean 대응참조 = Ọ̀rọ̀_SMS(Oníǹkan, "java/util/HashMap") || Ọ̀rọ̀_SMS(Oníǹkan, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>") && 명령코드 == 183 && Ọ̀rọ̀_SMS(서술상수, "()V")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 분류코드)) 모음늘리기(nǹkan_Ìtọ́ka, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { ìkùnà_iye("invalid collection invocation"); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "size") && Ọ̀rọ̀_SMS(서술상수, "()I") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isEmpty") && Ọ̀rọ̀_SMS(서술상수, "()Z")) {
            int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 분류코드)) 넣기(Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "size") ? 힙[nǹkan_Ìtọ́ka + 3] : 힙[nǹkan_Ìtọ́ka + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "clear") && Ọ̀rọ̀_SMS(서술상수, "()V")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 분류코드)) { int détà_ÀRÉÈ = 힙[nǹkan_Ìtọ́ka + 2]; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 힙[détà_ÀRÉÈ + 1]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[détà_ÀRÉÈ + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 0; 힙[nǹkan_Ìtọ́ka + 3] = 0; } return; }
        if (!대응참조 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "add") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int détà_iye = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 10)) return;
            int 항목수 = 힙[nǹkan_Ìtọ́ka + 3]; 모음늘리기(nǹkan_Ìtọ́ka, 항목수 + 1); if (!àṣìṣe) { 힙[힙[nǹkan_Ìtọ́ka + 2] + 2 + 항목수] = détà_iye; 힙[nǹkan_Ìtọ́ka + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "get") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "remove")) && Ọ̀rọ̀_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "set") && Ọ̀rọ̀_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "set"); int détà_iye = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2);
            if (!nǹkan_iye(nǹkan_Ìtọ́ka, 10)) return;
            int 항목수 = 힙[nǹkan_Ìtọ́ka + 3], détà_ÀRÉÈ = 힙[nǹkan_Ìtọ́ka + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[détà_ÀRÉÈ + 2 + 항목자리];
            if (지정여부) 힙[détà_ÀRÉÈ + 2 + 항목자리] = détà_iye;
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "remove")) { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 항목자리 + 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[détà_ÀRÉÈ + 1 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[détà_ÀRÉÈ + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú]; 힙[détà_ÀRÉÈ + 1 + 항목수] = 0; 힙[nǹkan_Ìtọ́ka + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "get") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "remove")) && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "put") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "containsKey") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "put"), ṣèmúkúro = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "remove");
            int détà_iye = 넣기여부 ? 빼기(2) : 0, bọ́tìnnì_Ìtọ́ka = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 11)) return;
            int 항목수 = 힙[nǹkan_Ìtọ́ka + 3], détà_ÀRÉÈ = 힙[nǹkan_Ìtọ́ka + 2], 찾은여부 = -1;
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (값같음(bọ́tìnnì_Ìtọ́ka, 힙[détà_ÀRÉÈ + 2 + 2 * ṣetúnṣe_wá_atọ̀ka_àkóónú])) { 찾은여부 = ṣetúnṣe_wá_atọ̀ka_àkóónú; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[détà_ÀRÉÈ + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(nǹkan_Ìtọ́ka, (항목수 + 1) * 2); détà_ÀRÉÈ = 힙[nǹkan_Ìtọ́ka + 2]; 찾은여부 = 항목수; if (!àṣìṣe) 힙[nǹkan_Ìtọ́ka + 3] = 항목수 + 1; }
                if (!àṣìṣe) { 힙[détà_ÀRÉÈ + 2 + 2 * 찾은여부] = bọ́tìnnì_Ìtọ́ka; 힙[détà_ÀRÉÈ + 3 + 2 * 찾은여부] = détà_iye; }
            }
            if (ṣèmúkúro && 찾은여부 >= 0) { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 찾은여부 + 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { 힙[détà_ÀRÉÈ + 2 * ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[détà_ÀRÉÈ + 2 + 2 * ṣetúnṣe_wá_atọ̀ka_àkóónú]; 힙[détà_ÀRÉÈ + 1 + 2 * ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[détà_ÀRÉÈ + 3 + 2 * ṣetúnṣe_wá_atọ̀ka_àkóónú]; } 힙[détà_ÀRÉÈ + 2 * 항목수] = 0; 힙[détà_ÀRÉÈ + 1 + 2 * 항목수] = 0; 힙[nǹkan_Ìtọ́ka + 3] = 항목수 - 1; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        ìkùnà_iye("unsupported collection method");
    }
    static boolean 잠금얻기(int nǹkan_Ìtọ́ka) {
        if (!객체유효(nǹkan_Ìtọ́ka)) return false;
        if (잠금깊이[nǹkan_Ìtọ́ka] != 0 && 잠금주인[nǹkan_Ìtọ́ka] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[nǹkan_Ìtọ́ka] = 현재가닥 + 1; 잠금깊이[nǹkan_Ìtọ́ka]++; return true;
    }
    static void 잠금풀기(int nǹkan_Ìtọ́ka) {
        if (!객체유효(nǹkan_Ìtọ́ka)) return;
        if (잠금깊이[nǹkan_Ìtọ́ka] == 0 || 잠금주인[nǹkan_Ìtọ́ka] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[nǹkan_Ìtọ́ka] == 0) 잠금주인[nǹkan_Ìtọ́ka] = 0;
    }
    static boolean ṣèpapòdà_èròjà_atẹ̀lélànà() {
        èròjà_atẹ̀lélànà_férèmù[현재가닥] = férèmù_wá_atọ̀ka_àkóónú;
        if (férèmù_wá_atọ̀ka_àkóónú < 현재가닥 * 32) èròjà_atẹ̀lélànà_ipò[현재가닥] = 3;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 가닥수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (èròjà_atẹ̀lélànà_ipò[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 2 && èròjà_atẹ̀lélànà_ipò[가닥대기[ṣetúnṣe_wá_atọ̀ka_àkóónú]] == 3) èròjà_atẹ̀lélànà_ipò[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 1;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 1; ṣetúnṣe_wá_atọ̀ka_àkóónú <= 가닥수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int 다음자리 = (현재가닥 + ṣetúnṣe_wá_atọ̀ka_àkóónú) % 가닥수;
            if (èròjà_atẹ̀lélànà_ipò[다음자리] == 1) { 현재가닥 = 다음자리; férèmù_wá_atọ̀ka_àkóónú = èròjà_atẹ̀lélànà_férèmù[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 가닥수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (èròjà_atẹ̀lélànà_ipò[ṣetúnṣe_wá_atọ̀ka_àkóónú] != 3) { ìkùnà_iye("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드) { Ìlànà_èròjà_atẹ̀lélànà(orúkọ_aláìṣeéyípadà, 서술상수, 명령코드, false); }
    static void Ìlànà_èròjà_atẹ̀lélànà(int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, 한국어 ? "ti_dádúró_díẹ̀_iṣẹ́" : "yield") && Ọ̀rọ̀_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "currentThread") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(èròjà_atẹ̀lélànà_nǹkan[현재가닥], 2); return; }
        if (명령코드 == 183 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>") && (Ọ̀rọ̀_SMS(서술상수, "()V") || Ọ̀rọ̀_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int àfojúsùn_àdírẹ́ẹ̀sì = Ọ̀rọ̀_SMS(서술상수, "()V") ? 0 : 빼기(2), nǹkan_Ìtọ́ka = 빼기(2);
            if (!객체유효(nǹkan_Ìtọ́ka)) return;
            if (힙[nǹkan_Ìtọ́ka] == 13) { 힙[nǹkan_Ìtọ́ka + 2] = àfojúsùn_àdírẹ́ẹ̀sì; 힙참조[nǹkan_Ìtọ́ka + 2] = 1; }
            else if (àfojúsùn_àdírẹ́ẹ̀sì != 0) ìkùnà_iye("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, 한국어 ? "bẹ̀rẹ̀_iṣẹ́" : "start") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, 한국어 ? "기다리기" : "join")) && Ọ̀rọ̀_SMS(서술상수, "()V") || 명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, 한국어 ? "살아있는가" : "isAlive") && Ọ̀rọ̀_SMS(서술상수, "()Z")) {
            int nǹkan_Ìtọ́ka = 빼기(2); if (!객체유효(nǹkan_Ìtọ́ka)) return;
            int àkọọ́lẹ̀_iye = -1; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 가닥수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (èròjà_atẹ̀lélànà_nǹkan[ṣetúnṣe_wá_atọ̀ka_àkóónú] == nǹkan_Ìtọ́ka) àkọọ́lẹ̀_iye = ṣetúnṣe_wá_atọ̀ka_àkóónú;
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, 한국어 ? "살아있는가" : "isAlive")) { 넣기(àkọọ́lẹ̀_iye >= 0 && èròjà_atẹ̀lélànà_ipò[àkọọ́lẹ̀_iye] != 3 ? 1 : 0, 1); return; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, 한국어 ? "기다리기" : "join")) { if (àkọọ́lẹ̀_iye >= 0 && èròjà_atẹ̀lélànà_ipò[àkọọ́lẹ̀_iye] != 3) { 가닥대기[현재가닥] = àkọọ́lẹ̀_iye; èròjà_atẹ̀lélànà_ipò[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (àkọọ́lẹ̀_iye >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { ìkùnà_iye("thread limit (4 including main)"); return; }
            int àfojúsùn_àdírẹ́ẹ̀sì = 힙[nǹkan_Ìtọ́ka] == 13 ? 힙[nǹkan_Ìtọ́ka + 2] : nǹkan_Ìtọ́ka;
            int fáìlì_wá_atọ̀ka_àkóónú = àfojúsùn_àdírẹ́ẹ̀sì > 0 && 힙[àfojúsùn_àdírẹ́ẹ̀sì] >= 32 ? orúkọ_ìlànà(힙[àfojúsùn_àdírẹ́ẹ̀sì] - 32, 한국어 ? "ṣiṣẹ́_iṣẹ́" : "run", "()V") : -1;
            if (àfojúsùn_àdírẹ́ẹ̀sì != 0 && fáìlì_wá_atọ̀ka_àkóónú < 0) { ìkùnà_iye("Runnable.run required"); return; }
            àkọọ́lẹ̀_iye = 가닥수++; èròjà_atẹ̀lélànà_nǹkan[àkọọ́lẹ̀_iye] = nǹkan_Ìtọ́ka; èròjà_atẹ̀lélànà_àfojúsùn[àkọọ́lẹ̀_iye] = àfojúsùn_àdírẹ́ẹ̀sì;
            int férèmù = àkọọ́lẹ̀_iye * 32; èròjà_atẹ̀lélànà_férèmù[àkọọ́lẹ̀_iye] = fáìlì_wá_atọ̀ka_àkóónú < 0 ? férèmù - 1 : férèmù; èròjà_atẹ̀lélànà_ipò[àkọọ́lẹ̀_iye] = fáìlì_wá_atọ̀ka_àkóónú < 0 ? 3 : 1;
            if (fáìlì_wá_atọ̀ka_àkóónú >= 0) { férèmù_ìlànà[férèmù] = fáìlì_wá_atọ̀ka_àkóónú; 틀위치[férèmù] = ìlànà_bẹ̀rẹ̀[fáìlì_wá_atọ̀ka_àkóónú]; agbègbè_iye[férèmù * 128] = àfojúsùn_àdírẹ́ẹ̀sì; agbègbè_irú[férèmù * 128] = 2; }
            return;
        }
        ìkùnà_iye("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], àdírẹ́ẹ̀sì_SMS = new int[16];
    static int agbègbè_àdírẹ́ẹ̀sì() { return àdírẹ́ẹ̀sì_nǹkan(0x7f000001); }
    static int àdírẹ́ẹ̀sì_nǹkan(int iye) { int nǹkan_Ìtọ́ka = pín_Ibi_ìpamọ́(14, 1); if (!àṣìṣe) 힙[nǹkan_Ìtọ́ka + 2] = iye; return nǹkan_Ìtọ́ka; }
    static int 주소해독(int nǹkan_Ìtọ́ka) {
        if (nǹkan_Ìtọ́ka == 0 || 글같음(nǹkan_Ìtọ́ka, olùpèsè_ẹyọ_ọ̀rọ̀("localhost"), false)) return 0x7f000001;
        if (!nǹkan_iye(nǹkan_Ìtọ́ka, 1)) return 0;
        int détà_iye = 0, 총수 = 0, àdírẹ́ẹ̀sì_báìtì = 0, 자릿수 = 0, 항목수 = 힙[nǹkan_Ìtọ́ka + 1];
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú <= 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = ṣetúnṣe_wá_atọ̀ka_àkóónú == 항목수 ? '.' : 힙[nǹkan_Ìtọ́ka + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
            if (kóòdù_ẹyọ_ọ̀rọ̀ == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } détà_iye = détà_iye << 8 | àdírẹ́ẹ̀sì_báìtì; 총수++; àdírẹ́ẹ̀sì_báìtì = 자릿수 = 0; }
            else { if (kóòdù_ẹyọ_ọ̀rọ̀ < '0' || kóòdù_ẹyọ_ọ̀rọ̀ > '9' || ++자릿수 > 3 || (àdírẹ́ẹ̀sì_báìtì = àdírẹ́ẹ̀sì_báìtì * 10 + kóòdù_ẹyọ_ọ̀rọ̀ - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return détà_iye;
    }
    static int àdírẹ́ẹ̀sì_ẹyọ_ọ̀rọ̀(int détà_iye) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int àdírẹ́ẹ̀sì_báìtì = détà_iye >>> 이동비트 & 255;
            if (àdírẹ́ẹ̀sì_báìtì >= 100) àdírẹ́ẹ̀sì_SMS[항목수++] = '0' + àdírẹ́ẹ̀sì_báìtì / 100;
            if (àdírẹ́ẹ̀sì_báìtì >= 10) àdírẹ́ẹ̀sì_SMS[항목수++] = '0' + àdírẹ́ẹ̀sì_báìtì / 10 % 10;
            àdírẹ́ẹ̀sì_SMS[항목수++] = '0' + àdírẹ́ẹ̀sì_báìtì % 10; if (이동비트 != 0) àdírẹ́ẹ̀sì_SMS[항목수++] = '.';
        }
        int nǹkan_Ìtọ́ka = pín_Ibi_ìpamọ́(1, 항목수); if (!àṣìṣe) for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[nǹkan_Ìtọ́ka + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = àdírẹ́ẹ̀sì_SMS[ṣetúnṣe_wá_atọ̀ka_àkóónú]; return nǹkan_Ìtọ́ka;
    }
    static void 통신호출(int Oníǹkan, int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드) {
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/net/InetAddress")) {
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getLoopbackAddress") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(agbègbè_àdírẹ́ẹ̀sì(), 2); return; }
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getByName") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int détà_iye = 주소해독(빼기(2)); if (던진객체 == 0 && !àṣìṣe) 넣기(àdírẹ́ẹ̀sì_nǹkan(détà_iye), 2); return;
            }
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getHostAddress") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/String;")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 14)) 넣기(àdírẹ́ẹ̀sì_ẹyọ_ọ̀rọ̀(힙[nǹkan_Ìtọ́ka + 2]), 2); return; }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>") && (Ọ̀rọ̀_SMS(서술상수, "([BI)V") || Ọ̀rọ̀_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean èbúté_iye_Ìtọ́ka = Ọ̀rọ̀_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = èbúté_iye_Ìtọ́ka ? 빼기(1) : 0, àdírẹ́ẹ̀sì_Ìtọ́ka = èbúté_iye_Ìtọ́ka ? 빼기(2) : 0;
                int 항목수 = 빼기(1), détà_ÀRÉÈ = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2);
                if (!nǹkan_iye(nǹkan_Ìtọ́ka, 16) || !nǹkan_iye(détà_ÀRÉÈ, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[détà_ÀRÉÈ + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (àdírẹ́ẹ̀sì_Ìtọ́ka != 0 && !nǹkan_iye(àdírẹ́ẹ̀sì_Ìtọ́ka, 14)) return;
                힙[nǹkan_Ìtọ́ka + 2] = détà_ÀRÉÈ; 힙참조[nǹkan_Ìtọ́ka + 2] = 1; 힙[nǹkan_Ìtọ́ka + 3] = 항목수;
                힙[nǹkan_Ìtọ́ka + 4] = àdírẹ́ẹ̀sì_Ìtọ́ka; 힙참조[nǹkan_Ìtọ́ka + 4] = 1; 힙[nǹkan_Ìtọ́ka + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setLength") && Ọ̀rọ̀_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[nǹkan_Ìtọ́ka + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[nǹkan_Ìtọ́ka + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getData") && Ọ̀rọ̀_SMS(서술상수, "()[B") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getLength") && Ọ̀rọ̀_SMS(서술상수, "()I") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getAddress") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/net/InetAddress;") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getPort") && Ọ̀rọ̀_SMS(서술상수, "()I"))) {
                int nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 16)) return;
                int 항목자리 = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getData") ? 2 : Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getLength") ? 3 : Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getAddress") ? 4 : 5;
                넣기(힙[nǹkan_Ìtọ́ka + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>") && (Ọ̀rọ̀_SMS(서술상수, "()V") || Ọ̀rọ̀_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Ọ̀rọ̀_SMS(서술상수, "()V") ? 0 : 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = aṣàmúlò.ṣí_Alásopọ̀(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[nǹkan_Ìtọ́ka + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setSoTimeout") && Ọ̀rọ̀_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[nǹkan_Ìtọ́ka + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getLocalPort") && Ọ̀rọ̀_SMS(서술상수, "()I")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 15)) 넣기(힙[nǹkan_Ìtọ́ka + 2] < 0 ? -1 : aṣàmúlò.Alásopọ̀_ojú(힙[nǹkan_Ìtọ́ka + 2]), 1); return; }
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isClosed") && Ọ̀rọ̀_SMS(서술상수, "()Z")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 15)) 넣기(힙[nǹkan_Ìtọ́ka + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "close") && Ọ̀rọ̀_SMS(서술상수, "()V")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 15) && 힙[nǹkan_Ìtọ́ka + 2] >= 0) { aṣàmúlò.파일서술자닫기(힙[nǹkan_Ìtọ́ka + 2]); 힙[nǹkan_Ìtọ́ka + 2] = -1; } return; }
            if (명령코드 == 182 && (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "send") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "receive")) && Ọ̀rọ̀_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(전문참조, 16) || !nǹkan_iye(nǹkan_Ìtọ́ka, 15)) return;
                int détà_ÀRÉÈ = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[nǹkan_Ìtọ́ka + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "send")) {
                    if (!nǹkan_iye(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 유효길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 통신임시[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[détà_ÀRÉÈ + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
                    if (aṣàmúlò.í_meèlì_Alásopọ̀(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = aṣàmúlò.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = aṣàmúlò.밀리초();
                        if (힙[nǹkan_Ìtọ́ka + 4] == 0) 힙[nǹkan_Ìtọ́ka + 4] = 현재시각 + 1;
                        if (힙[nǹkan_Ìtọ́ka + 3] > 0 && 현재시각 - (힙[nǹkan_Ìtọ́ka + 4] - 1) >= 힙[nǹkan_Ìtọ́ka + 3]) { 힙[nǹkan_Ìtọ́ka + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(nǹkan_Ìtọ́ka, 2); 넣기(전문참조, 2); 틀위치[férèmù_wá_atọ̀ka_àkóónú] = férèmù_ìtọ́sọ́nà[férèmù_wá_atọ̀ka_àkóónú]; 바꿈요청 = true; return;
                    }
                    힙[nǹkan_Ìtọ́ka + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[détà_ÀRÉÈ + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = (byte)통신임시[ṣetúnṣe_wá_atọ̀ka_àkóónú];
                    힙[전문참조 + 3] = 항목수; 힙[전문참조 + 4] = àdírẹ́ẹ̀sì_nǹkan(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        ìkùnà_iye("unsupported java.net method");
    }
    static boolean 흐름대기(int nǹkan_Ìtọ́ka) {
        int 현재시각 = aṣàmúlò.밀리초();
        if (힙[nǹkan_Ìtọ́ka + 5] == 0) 힙[nǹkan_Ìtọ́ka + 5] = 현재시각 + 1;
        if (힙[nǹkan_Ìtọ́ka + 3] > 0 && 현재시각 - (힙[nǹkan_Ìtọ́ka + 5] - 1) >= 힙[nǹkan_Ìtọ́ka + 3]) { 힙[nǹkan_Ìtọ́ka + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[férèmù_wá_atọ̀ka_àkóónú] = férèmù_ìtọ́sọ́nà[férèmù_wá_atọ̀ka_àkóónú]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int Oníǹkan, int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Ọ̀rọ̀_SMS(Oníǹkan, "java/net/ServerSocket"), Stream = Ọ̀rọ̀_SMS(Oníǹkan, "java/io/InputStream") || Ọ̀rọ̀_SMS(Oníǹkan, "java/io/OutputStream");
        if (!Stream && 명령코드 == 183 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>")) {
            boolean 빈여부 = Ọ̀rọ̀_SMS(서술상수, "()V"), 이름지정여부 = Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Ọ̀rọ̀_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Ọ̀rọ̀_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { ìkùnà_iye("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), àdírẹ́ẹ̀sì_Ìtọ́ka = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, nǹkan_Ìtọ́ka = 빼기(2);
            if (!nǹkan_iye(nǹkan_Ìtọ́ka, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !nǹkan_iye(àdírẹ́ẹ̀sì_Ìtọ́ka, 14)) return;
            int Alásopọ̀_àdírẹ́ẹ̀sì = 이름지정여부 ? 주소해독(àdírẹ́ẹ̀sì_Ìtọ́ka) : 주소지정여부 ? 힙[àdírẹ́ẹ̀sì_Ìtọ́ka + 2] : 0x7f000001;
            if (àṣìṣe || 던진객체 != 0) return;
            int 열린파일번호 = aṣàmúlò.Stream_ìdarí(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? aṣàmúlò.Stream_ìdarí(1, 열린파일번호, 접속번호) : aṣàmúlò.SOMỌ́_Stream(열린파일번호, Alásopọ̀_àdírẹ́ẹ̀sì, 접속번호);
            if (처리값 < 0) { aṣàmúlò.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[nǹkan_Ìtọ́ka + 2] = 열린파일번호; 힙[nǹkan_Ìtọ́ka + 4] = 접속번호; 힙[nǹkan_Ìtọ́ka + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setSoTimeout") && Ọ̀rọ̀_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[nǹkan_Ìtọ́ka + 3] = 밀리초값; return; }
        if (!Stream && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "close") && Ọ̀rọ̀_SMS(서술상수, "()V")) { int nǹkan_Ìtọ́ka = 빼기(2); if (nǹkan_iye(nǹkan_Ìtọ́ka, 수신쪽 ? 18 : 17) && 힙[nǹkan_Ìtọ́ka + 2] >= 0) { aṣàmúlò.파일서술자닫기(힙[nǹkan_Ìtọ́ka + 2]); 힙[nǹkan_Ìtọ́ka + 2] = -1; } return; }
        if (!Stream && (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getLocalPort") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getPort") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isClosed") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isConnected"))) {
            int nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 수신쪽 ? 18 : 17)) return;
            넣기(Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isClosed") ? 힙[nǹkan_Ìtọ́ka + 2] < 0 ? 1 : 0 : Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isConnected") ? 힙[nǹkan_Ìtọ́ka + 6] : Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getPort") ? 힙[nǹkan_Ìtọ́ka + 4] : 힙[nǹkan_Ìtọ́ka + 2] < 0 ? -1 : aṣàmúlò.Stream_ìdarí(4, 힙[nǹkan_Ìtọ́ka + 2], 0), 1); return;
        }
        if (수신쪽 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "accept") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/net/Socket;")) {
            int nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 18)) return; int 열린파일번호 = aṣàmúlò.Stream_ìdarí(3, 힙[nǹkan_Ìtọ́ka + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(nǹkan_Ìtọ́ka)) 넣기(nǹkan_Ìtọ́ka, 2); return; }
            힙[nǹkan_Ìtọ́ka + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = pín_Ibi_ìpamọ́(17, 5); if (àṣìṣe) { aṣàmúlò.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = aṣàmúlò.Stream_ìdarí(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getInputStream") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/io/InputStream;")) || (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getOutputStream") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 17)) return; if (힙[nǹkan_Ìtọ́ka + 2] < 0 || 힙[nǹkan_Ìtọ́ka + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = pín_Ibi_ìpamọ́(19, 4); if (àṣìṣe) return; 힙[반환값 + 2] = nǹkan_Ìtọ́ka; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "read"), 쓰기여부 = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "write"), sèdíwọ = Ọ̀rọ̀_SMS(서술상수, "([B)I") || Ọ̀rọ̀_SMS(서술상수, "([B)V"), 부분배열여부 = Ọ̀rọ̀_SMS(서술상수, "([BII)I") || Ọ̀rọ̀_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, détà_ÀRÉÈ = sèdíwọ || 부분배열여부 ? 빼기(2) : 0;
            int détà_iye = 쓰기여부 && Ọ̀rọ̀_SMS(서술상수, "(I)V") ? 빼기(1) : 0, nǹkan_Ìtọ́ka = 빼기(2);
            if (!nǹkan_iye(nǹkan_Ìtọ́ka, 19)) return; int 부모참조 = 힙[nǹkan_Ìtọ́ka + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "close") && Ọ̀rọ̀_SMS(서술상수, "()V")) { aṣàmúlò.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "flush") && Ọ̀rọ̀_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[nǹkan_Ìtọ́ka + 3] == 0)) { ìkùnà_iye("unsupported stream operation"); return; }
            if (sèdíwọ || 부분배열여부) { if (!nǹkan_iye(détà_ÀRÉÈ, 20)) return; if (sèdíwọ) 항목수 = 힙[détà_ÀRÉÈ + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[détà_ÀRÉÈ + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[nǹkan_Ìtọ́ka + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? aṣàmúlò.파일한바이트읽기(열린파일번호) : aṣàmúlò.파일한바이트쓰기(열린파일번호, sèdíwọ || 부분배열여부 ? 힙[détà_ÀRÉÈ + 2 + 시작변위 + 완료수] : détà_iye);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (sèdíwọ || 부분배열여부)) 힙[détà_ÀRÉÈ + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(sèdíwọ || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[nǹkan_Ìtọ́ka + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(nǹkan_Ìtọ́ka, 2); if (sèdíwọ || 부분배열여부) 넣기(détà_ÀRÉÈ, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(sèdíwọ || 부분배열여부)) 넣기(détà_iye, 1); } return;
            }
            힙[nǹkan_Ìtọ́ka + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : sèdíwọ || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        ìkùnà_iye("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int orúkọ_aláìṣeéyípadà) {
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/wínńdò")) return 24;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/àkọlé")) return 26;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/bọ́tìnnì")) return 27;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/SMS_àayè_wúnrẹ̀n")) return 28;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int orúkọ_aláìṣeéyípadà) {
        return 한국어화면종(orúkọ_aláìṣeéyípadà) != 0 || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/화면구성요소") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "한국어/자체/ìgbéṣẹ̀_ìtòléra");
    }
    static int 화면종(int orúkọ_aláìṣeéyípadà) {
        int 한국어종 = 한국어화면종(orúkọ_aláìṣeéyípadà); if (한국어종 != 0) return 한국어종;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/JFrame")) return 24;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/JPanel")) return 25;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/JLabel")) return 26;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/JButton")) return 27;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/JTextField")) return 28;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/awt/event/ActionEvent")) return 29;
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int orúkọ_aláìṣeéyípadà) {
        return 화면종(orúkọ_aláìṣeéyípadà) != 0 || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/awt/Component") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "java/awt/Container") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/JComponent") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/AbstractButton") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/text/JTextComponent") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int nǹkan_Ìtọ́ka) { if (!객체유효(nǹkan_Ìtọ́ka)) return false; if (힙[nǹkan_Ìtọ́ka] < 24 || 힙[nǹkan_Ìtọ́ka] > 28) { ìkùnà_iye("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int nǹkan_Ìtọ́ka, int SMS_Ìtọ́ka) {
        if (SMS_Ìtọ́ka != 0 && !nǹkan_iye(SMS_Ìtọ́ka, 1)) return;
        int 항목수 = SMS_Ìtọ́ka == 0 ? 0 : 힙[SMS_Ìtọ́ka + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 화면글임시[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 힙[SMS_Ìtọ́ka + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        if (aṣàmúlò.화면글(힙[nǹkan_Ìtọ́ka + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[nǹkan_Ìtọ́ka + 3] = SMS_Ìtọ́ka; 힙참조[nǹkan_Ìtọ́ka + 3] = 1;
    }
    static int 화면문자읽기(int nǹkan_Ìtọ́ka) {
        int àkọọ́lẹ̀_iye = 힙[nǹkan_Ìtọ́ka + 2], 항목수 = aṣàmúlò.화면연결(8, àkọọ́lẹ̀_iye, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { ìkùnà_iye("GUI text read failed"); return 0; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int 부호값 = aṣàmúlò.화면연결(9, àkọọ́lẹ̀_iye, ṣetúnṣe_wá_atọ̀ka_àkóónú, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = pín_Ibi_ìpamọ́(1, 사용수); if (!àṣìṣe) for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 사용수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 힙[반환값 + 2 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 화면글임시[ṣetúnṣe_wá_atọ̀ka_àkóónú]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 kánẹ́ẹ̀lì_iye 화면 기능에 연결한다. Swing nǹkan_iye/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int Oníǹkan, int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드) {
        if (Ọ̀rọ̀_SMS(Oníǹkan, "한국어/자체/ìgbéṣẹ̀_ìtòléra")) {
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "나중에실행") && Ọ̀rọ̀_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int iṣẹ́_ìṣe = 빼기(2); if (!객체유효(iṣẹ́_ìṣe)) return;
                if (나중수 == 8) { ìkùnà_iye("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = iṣẹ́_ìṣe; return;
            }
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "사건처리중인가") && Ọ̀rọ̀_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ìkùnà_iye("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!nǹkan_iye(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "ìgbéṣẹ̀_orísun") && Ọ̀rọ̀_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "àṣẹ_SMS") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "wá_atọ̀ka_àkóónú") && Ọ̀rọ̀_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ìkùnà_iye("지원하지 않는 한국어 ìṣe 알림 호출"); return;
        }
        if (명령코드 == 183 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>")) {
            int 종류 = 한국어화면종(Oníǹkan), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (aṣàmúlò.화면너비() - 폭) / 2; 세로 = (aṣàmúlò.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { ìkùnà_iye("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), ìdá_ìpìlẹ̀_iye = 빼기(2); if (!화면객체(ìdá_ìpìlẹ̀_iye)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > aṣàmúlò.화면너비() - 가로 || 높이 > aṣàmúlò.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int wá_atọ̀ka_àkóónú = aṣàmúlò.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (wá_atọ̀ka_àkóónú < 1 || wá_atọ̀ka_àkóónú > 32) { ìkùnà_iye("화면 ìdá_ìpìlẹ̀_iye 자리가 가득 찼습니다"); return; }
            힙[ìdá_ìpìlẹ̀_iye + 2] = wá_atọ̀ka_àkóónú; 화면참조[wá_atọ̀ka_àkóónú - 1] = ìdá_ìpìlẹ̀_iye;
            힙[ìdá_ìpìlẹ̀_iye + 5] = 가로; 힙[ìdá_ìpìlẹ̀_iye + 6] = 세로; 힙[ìdá_ìpìlẹ̀_iye + 7] = 폭; 힙[ìdá_ìpìlẹ̀_iye + 8] = 높이; 힙[ìdá_ìpìlẹ̀_iye + 10] = 2;
            힙[ìdá_ìpìlẹ̀_iye + 4] = 받이; 힙참조[ìdá_ìpìlẹ̀_iye + 4] = 1; 힙[ìdá_ìpìlẹ̀_iye + 12] = 1;
            aṣàmúlò.화면연결(1, wá_atọ̀ka_àkóónú, 가로, 세로, 폭, 높이);
            if (종류 == 24) aṣàmúlò.화면연결(7, wá_atọ̀ka_àkóónú, 2, 0, 0, 0);
            화면문자설정(ìdá_ìpìlẹ̀_iye, SMS); return;
        }
        if (명령코드 != 182) { ìkùnà_iye("잘못된 한국어 화면 호출 Àṣẹ"); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "kọ_SMS") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), ìdá_ìpìlẹ̀_iye = 빼기(2); if (화면객체(ìdá_ìpìlẹ̀_iye)) 화면문자설정(ìdá_ìpìlẹ̀_iye, SMS); return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "글읽기") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/String;")) {
            int ìdá_ìpìlẹ̀_iye = 빼기(2); if (화면객체(ìdá_ìpìlẹ̀_iye)) 넣기(화면문자읽기(ìdá_ìpìlẹ̀_iye), 2); return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "동작맡기기") && Ọ̀rọ̀_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), ìdá_ìpìlẹ̀_iye = 빼기(2);
            if (화면객체(ìdá_ìpìlẹ̀_iye)) { 힙[ìdá_ìpìlẹ̀_iye + 4] = 받이; 힙참조[ìdá_ìpìlẹ̀_iye + 4] = 1; 힙[ìdá_ìpìlẹ̀_iye + 12] = 1; } return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "ròmọ́_ìdá_ìpìlẹ̀") && Ọ̀rọ̀_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int ọmọ_iye = 빼기(2), 부모 = 빼기(2); if (!화면객체(ọmọ_iye) || !화면객체(부모)) return;
            if (aṣàmúlò.화면연결(2, 힙[부모 + 2], 힙[ọmọ_iye + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[ọmọ_iye + 11] = 부모; 힙참조[ọmọ_iye + 11] = 1; return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "자리정하기") && Ọ̀rọ̀_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), ìdá_ìpìlẹ̀_iye = 빼기(2); if (!화면객체(ìdá_ìpìlẹ̀_iye)) return;
            if (aṣàmúlò.화면연결(1, 힙[ìdá_ìpìlẹ̀_iye + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[ìdá_ìpìlẹ̀_iye + 5] = 가로; 힙[ìdá_ìpìlẹ̀_iye + 6] = 세로; 힙[ìdá_ìpìlẹ̀_iye + 7] = 폭; 힙[ìdá_ìpìlẹ̀_iye + 8] = 높이; return;
        }
        if ((Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "ṣàfihàn_wínńdò") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "Ti")) && Ọ̀rọ̀_SMS(서술상수, "()V")) {
            boolean aṣeérí_iye = Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "ṣàfihàn_wínńdò"); int ìdá_ìpìlẹ̀_iye = 빼기(2); if (!화면객체(ìdá_ìpìlẹ̀_iye)) return;
            if (aṣàmúlò.화면연결(aṣeérí_iye ? 3 : 4, 힙[ìdá_ìpìlẹ̀_iye + 2], aṣeérí_iye ? 1 : 0, 0, 0, 0) < 0) { ìkùnà_iye("화면은 ìjọṣepọ̀ 명령에서 실행해야 합니다"); return; }
            힙[ìdá_ìpìlẹ̀_iye + 9] = aṣeérí_iye ? 1 : 0; return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "보이는가") && Ọ̀rọ̀_SMS(서술상수, "()Z")) { int ìdá_ìpìlẹ̀_iye = 빼기(2); if (화면객체(ìdá_ìpìlẹ̀_iye)) 넣기(힙[ìdá_ìpìlẹ̀_iye + 9], 1); return; }
        ìkùnà_iye("지원하지 않는 한국어 화면 ìlànà_iye");
    }
    static void 화면호출(int Oníǹkan, int orúkọ_aláìṣeéyípadà, int 서술상수, int 명령코드) {
        if (Ọ̀rọ̀_SMS(Oníǹkan, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "invokeLater") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int nǹkan_Ìtọ́ka = 빼기(2); if (!객체유효(nǹkan_Ìtọ́ka)) return; if (나중수 == 8) { ìkùnà_iye("invokeLater queue full"); return; } 나중실행[나중수++] = nǹkan_Ìtọ́ka; return; }
            if (명령코드 == 184 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isEventDispatchThread") && Ọ̀rọ̀_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ìkùnà_iye("unsupported SwingUtilities method"); return;
        }
        if (Ọ̀rọ̀_SMS(Oníǹkan, "java/awt/event/ActionEvent")) {
            int nǹkan_Ìtọ́ka = 빼기(2); if (!nǹkan_iye(nǹkan_Ìtọ́ka, 29)) return;
            if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getSource") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[nǹkan_Ìtọ́ka + 2], 2);
            else if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getActionCommand") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[nǹkan_Ìtọ́ka + 2]), 2);
            else if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getID") && Ọ̀rọ̀_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ìkùnà_iye("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "<init>")) {
            int 열수 = 0, SMS_Ìtọ́ka = 0;
            if (Ọ̀rọ̀_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Ìtọ́ka = 빼기(2); }
            else if (Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Ìtọ́ka = 빼기(2);
            else if (Ọ̀rọ̀_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Ọ̀rọ̀_SMS(서술상수, "()V")) { ìkùnà_iye("unsupported Swing constructor"); return; }
            int nǹkan_Ìtọ́ka = 빼기(2); if (!객체유효(nǹkan_Ìtọ́ka)) return;
            if (힙[nǹkan_Ìtọ́ka] == 30) { ìkùnà_iye("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(nǹkan_Ìtọ́ka) || 열수 < 0) return;
            int àkọọ́lẹ̀_iye = aṣàmúlò.화면연결(0, 힙[nǹkan_Ìtọ́ka] - 23, 0, 0, 0, 0);
            if (àkọọ́lẹ̀_iye < 1 || àkọọ́lẹ̀_iye > 32) { ìkùnà_iye("GUI widget slots exhausted"); return; }
            힙[nǹkan_Ìtọ́ka + 2] = àkọọ́lẹ̀_iye; 화면참조[àkọọ́lẹ̀_iye - 1] = nǹkan_Ìtọ́ka; 힙[nǹkan_Ìtọ́ka + 5] = 힙[nǹkan_Ìtọ́ka] == 24 ? 130 : 16; 힙[nǹkan_Ìtọ́ka + 6] = 힙[nǹkan_Ìtọ́ka] == 24 ? 110 : 16;
            힙[nǹkan_Ìtọ́ka + 7] = 힙[nǹkan_Ìtọ́ka] == 24 ? 380 : 220; 힙[nǹkan_Ìtọ́ka + 8] = 힙[nǹkan_Ìtọ́ka] == 24 ? 240 : 28; 힙[nǹkan_Ìtọ́ka + 10] = 1;
            화면문자설정(nǹkan_Ìtọ́ka, SMS_Ìtọ́ka); return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setText") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setTitle")) { int SMS_Ìtọ́ka = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka) && Ọ̀rọ̀_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(nǹkan_Ìtọ́ka, SMS_Ìtọ́ka); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getText") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getTitle")) { int nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka) && Ọ̀rọ̀_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(nǹkan_Ìtọ́ka), 2); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "addActionListener") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka)) { 힙[nǹkan_Ìtọ́ka + 4] = 수신참조; 힙참조[nǹkan_Ìtọ́ka + 4] = 1; } return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "getContentPane") && Ọ̀rọ̀_SMS(서술상수, "()Ljava/awt/Container;")) { int nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka)) 넣기(nǹkan_Ìtọ́ka, 2); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setLayout") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int ètò_ìrísí_Ìtọ́ka = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka) && ètò_ìrísí_Ìtọ́ka != 0) ìkùnà_iye("only absolute layout (null) is supported"); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "add") && (Ọ̀rọ̀_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Ọ̀rọ̀_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean ètò_ìrísí_kání = Ọ̀rọ̀_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (ètò_ìrísí_kání) 빼기(2);
            int ọmọ_Ìtọ́ka = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (!화면객체(ọmọ_Ìtọ́ka) || !화면객체(nǹkan_Ìtọ́ka)) return;
            if (aṣàmúlò.화면연결(2, 힙[nǹkan_Ìtọ́ka + 2], 힙[ọmọ_Ìtọ́ka + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[ọmọ_Ìtọ́ka + 11] = nǹkan_Ìtọ́ka; 힙참조[ọmọ_Ìtọ́ka + 11] = 1; if (!ètò_ìrísí_kání) 넣기(ọmọ_Ìtọ́ka, 2); return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setBounds") && Ọ̀rọ̀_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), ibi_ìtọ́kasí_x = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (!화면객체(nǹkan_Ìtọ́ka)) return;
            if (aṣàmúlò.화면연결(1, 힙[nǹkan_Ìtọ́ka + 2], ibi_ìtọ́kasí_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[nǹkan_Ìtọ́ka + 5] = ibi_ìtọ́kasí_x; 힙[nǹkan_Ìtọ́ka + 6] = 세로좌표; 힙[nǹkan_Ìtọ́ka + 7] = 너비; 힙[nǹkan_Ìtọ́ka + 8] = 높이; return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setSize") && Ọ̀rọ̀_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (!화면객체(nǹkan_Ìtọ́ka)) return;
            if (aṣàmúlò.화면연결(1, 힙[nǹkan_Ìtọ́ka + 2], 힙[nǹkan_Ìtọ́ka + 5], 힙[nǹkan_Ìtọ́ka + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[nǹkan_Ìtọ́ka + 7] = 너비; 힙[nǹkan_Ìtọ́ka + 8] = 높이; } return;
        }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setLocationRelativeTo") && Ọ̀rọ̀_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), nǹkan_Ìtọ́ka = 빼기(2); if (!화면객체(nǹkan_Ìtọ́ka)) return; if (상대배치 != 0) { ìkùnà_iye("only screen centering supported"); return; } 힙[nǹkan_Ìtọ́ka + 5] = (aṣàmúlò.화면너비() - 힙[nǹkan_Ìtọ́ka + 7]) / 2; 힙[nǹkan_Ìtọ́ka + 6] = (aṣàmúlò.화면높이() - 힙[nǹkan_Ìtọ́ka + 8]) / 2; aṣàmúlò.화면연결(1, 힙[nǹkan_Ìtọ́ka + 2], 힙[nǹkan_Ìtọ́ka + 5], 힙[nǹkan_Ìtọ́ka + 6], 힙[nǹkan_Ìtọ́ka + 7], 힙[nǹkan_Ìtọ́ka + 8]); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setDefaultCloseOperation") && Ọ̀rọ̀_SMS(서술상수, "(I)V")) { int ìlànà = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka)) { if (ìlànà < 0 || ìlànà > 3) 예외던짐(9, "close policy"); else { 힙[nǹkan_Ìtọ́ka + 10] = ìlànà; aṣàmúlò.화면연결(7, 힙[nǹkan_Ìtọ́ka + 2], ìlànà, 0, 0, 0); } } return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "setVisible") && Ọ̀rọ̀_SMS(서술상수, "(Z)V")) { int détà_iye = 빼기(1), nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka)) { int 처리값 = aṣàmúlò.화면연결(3, 힙[nǹkan_Ìtọ́ka + 2], détà_iye, 0, 0, 0); if (처리값 < 0) ìkùnà_iye("Swing requires a standalone interactive command"); else 힙[nǹkan_Ìtọ́ka + 9] = détà_iye; } return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "dispose") && Ọ̀rọ̀_SMS(서술상수, "()V")) { int nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka)) { aṣàmúlò.화면연결(4, 힙[nǹkan_Ìtọ́ka + 2], 0, 0, 0, 0); 힙[nǹkan_Ìtọ́ka + 9] = 0; } return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "repaint") || Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "validate")) { int nǹkan_Ìtọ́ka = 빼기(2); if (!화면객체(nǹkan_Ìtọ́ka) || !Ọ̀rọ̀_SMS(서술상수, "()V")) return; aṣàmúlò.화면연결(1, 힙[nǹkan_Ìtọ́ka + 2], 힙[nǹkan_Ìtọ́ka + 5], 힙[nǹkan_Ìtọ́ka + 6], 힙[nǹkan_Ìtọ́ka + 7], 힙[nǹkan_Ìtọ́ka + 8]); return; }
        if (Ọ̀rọ̀_SMS(orúkọ_aláìṣeéyípadà, "isVisible") && Ọ̀rọ̀_SMS(서술상수, "()Z")) { int nǹkan_Ìtọ́ka = 빼기(2); if (화면객체(nǹkan_Ìtọ́ka)) 넣기(힙[nǹkan_Ìtọ́ka + 9], 1); return; }
        ìkùnà_iye("unsupported Swing method (native subset)");
    }
    static void 사건실행(int àfojúsùn_àdírẹ́ẹ̀sì, int 사건번호, boolean 한국어) {
        if (àfojúsùn_àdírẹ́ẹ̀sì < 1 || 힙[àfojúsùn_àdírẹ́ẹ̀sì] < 32) { ìkùnà_iye("Java event listener required"); return; }
        int fáìlì_wá_atọ̀ka_àkóónú = orúkọ_ìlànà(힙[àfojúsùn_àdírẹ́ẹ̀sì] - 32, 사건번호 == 0 ? (한국어 ? "ṣiṣẹ́_iṣẹ́" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fáìlì_wá_atọ̀ka_àkóónú < 0) { ìkùnà_iye("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; férèmù_wá_atọ̀ka_àkóónú = 0; èròjà_atẹ̀lélànà_ipò[0] = 1; férèmù_kójọ[0] = 0; 틀잠금[0] = pàjùbà_férèmù[0] = 0; 바꿈요청 = false;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 128; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { agbègbè_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú] = agbègbè_irú[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 0; }
        férèmù_ìlànà[0] = fáìlì_wá_atọ̀ka_àkóónú; 틀위치[0] = ìlànà_bẹ̀rẹ̀[fáìlì_wá_atọ̀ka_àkóónú]; agbègbè_iye[0] = àfojúsùn_àdírẹ́ẹ̀sì; agbègbè_irú[0] = 2;
        if (사건번호 != 0) { agbègbè_iye[1] = 사건번호; agbègbè_irú[1] = 2; }
        사건중 = true; ṣiṣẹ́_àṣẹ(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!àṣìṣe) {
            if (나중수 > 0) { int àfojúsùn_àdírẹ́ẹ̀sì = 나중실행[0], 한국어 = 나중한국어[0]; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 나중수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { 나중실행[ṣetúnṣe_wá_atọ̀ka_àkóónú - 1] = 나중실행[ṣetúnṣe_wá_atọ̀ka_àkóónú]; 나중한국어[ṣetúnṣe_wá_atọ̀ka_àkóónú - 1] = 나중한국어[ṣetúnṣe_wá_atọ̀ka_àkóónú]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(àfojúsùn_àdírẹ́ẹ̀sì, 0, 한국어 != 0); continue; }
            if (aṣàmúlò.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = aṣàmúlò.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { ìkùnà_iye("GUI event I/O failed"); return; }
            int àkọọ́lẹ̀_iye = 사건번호 & 65535; if (àkọọ́lẹ̀_iye < 1 || àkọọ́lẹ̀_iye > 32) continue; int nǹkan_Ìtọ́ka = 화면참조[àkọọ́lẹ̀_iye - 1]; if (nǹkan_Ìtọ́ka == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[nǹkan_Ìtọ́ka + 10] != 0) 힙[nǹkan_Ìtọ́ka + 9] = 0;
                if (힙[nǹkan_Ìtọ́ka + 10] == 3) for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 32; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (화면참조[ṣetúnṣe_wá_atọ̀ka_àkóónú] != 0 && 힙[화면참조[ṣetúnṣe_wá_atọ̀ka_àkóónú]] == 24) aṣàmúlò.화면연결(4, ṣetúnṣe_wá_atọ̀ka_àkóónú + 1, 0, 0, 0, 0);
            } else if (힙[nǹkan_Ìtọ́ka + 4] != 0) {
                int KÀ_MÍ_Ìtọ́ka = pín_Ibi_ìpamọ́(29, 2); if (àṣìṣe) return; 힙[KÀ_MÍ_Ìtọ́ka + 2] = nǹkan_Ìtọ́ka; 힙[KÀ_MÍ_Ìtọ́ka + 3] = 힙[nǹkan_Ìtọ́ka + 12]; 힙참조[KÀ_MÍ_Ìtọ́ka + 2] = 1; 사건실행(힙[nǹkan_Ìtọ́ka + 4], KÀ_MÍ_Ìtọ́ka, 힙[nǹkan_Ìtọ́ka + 12] != 0);
            }
        }
    }
    public static int Rọ́ọ̀nù() {
        if (aṣàmúlò.인수개수() == 1 && 자바도구.같음(aṣàmúlò.인수(0), "-version")) {
            aṣàmúlò.Kọ("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (aṣàmúlò.인수개수() < 1) { aṣàmúlò.Kọ("Usage: java CLASS [ARGS]\n"); return 2; }
        ìgbéwọlé_ọ̀wọ́_Ìsọ̀tumọ̀ = ki_ọ̀wọ́_Ìsọ̀tumọ̀(olùpèsè_ẹyọ_ọ̀rọ̀(aṣàmúlò.인수(0))); if (àṣìṣe || ìgbéwọlé_ọ̀wọ́_Ìsọ̀tumọ̀ < 0) return 1;
        int ìgbéwọlé_kókó_iye = orúkọ_ìlànà(ìgbéwọlé_ọ̀wọ́_Ìsọ̀tumọ̀, "Rọ́ọ̀nù", "()V");
        boolean 한국어진입 = ìgbéwọlé_kókó_iye >= 0 && (ìlànà_wáyè_sí[ìgbéwọlé_kókó_iye] & 9) == 9;
        if (!한국어진입) ìgbéwọlé_kókó_iye = orúkọ_ìlànà(ìgbéwọlé_ọ̀wọ́_Ìsọ̀tumọ̀, "main", "([Ljava/lang/String;)V");
        if (ìgbéwọlé_kókó_iye < 0 || (ìlànà_wáyè_sí[ìgbéwọlé_kókó_iye] & 9) != 9) ìkùnà_iye("public static void Rọ́ọ̀nù() or main(String[] args) required");
        if (àṣìṣe) return 1;
        int 인수 = pín_Ibi_ìpamọ́(3, aṣàmúlò.인수개수() - 1); ÀRÉÈ_ìdá_ìpìlẹ̀[인수] = -1;
        for (int 수 = 1; 수 < aṣàmúlò.인수개수() && !àṣìṣe; 수++) 힙[인수 + 1 + 수] = olùpèsè_ẹyọ_ọ̀rọ̀(aṣàmúlò.인수(수));
        férèmù_wá_atọ̀ka_àkóónú = 0; férèmù_ìlànà[0] = ìgbéwọlé_kókó_iye; 틀위치[0] = ìlànà_bẹ̀rẹ̀[ìgbéwọlé_kókó_iye]; agbègbè_iye[0] = 한국어진입 ? 0 : 인수; agbègbè_irú[0] = 한국어진입 ? 0 : 2;
        èròjà_atẹ̀lélànà_ipò[0] = 1; èròjà_atẹ̀lélànà_nǹkan[0] = pín_Ibi_ìpamọ́(13, 2);
        ṣiṣẹ́_àṣẹ(); if (!àṣìṣe) 화면사건들(); return àṣìṣe ? 1 : 0;
    }
}
