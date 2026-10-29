// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fáìlì/스택/Ìtọ́ka/ẹ̀ka 경계를 ṣiṣẹ́_àṣẹ 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fáìlì = new int[16384], fáìlì_orúkọ_SMS = new int[64];
    static int[] aláìṣeéyípadà_sàmì = new int[512], 상가 = new int[512], 상나 = new int[512], fọ́nrán_Ìtọ́ka = new int[512];
    static int[] ìlànà_orúkọ_SMS = new int[32], ìlànà_irú = new int[32], ìlànà_wáyè_sí = new int[32];
    static int[] ìlànà_bẹ̀rẹ̀ = new int[32], ìlànà_parí = new int[32], ìlànà_kójọ = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], ìlànà_ágúmẹ́ntì_irú = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] agbègbè_iye = new int[4096], agbègbè_irú = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] férèmù_ìlànà = new int[32], 틀위치 = new int[32], férèmù_kójọ = new int[32];
    static int[] 힙 = new int[8192];
    static int Ìwọ̀n, 읽기위치, 상수수, 함수수, ọ̀wọ́_orúkọ, férèmù_wá_atọ̀ka_àkóónú = -1, 힙끝 = 1, 반환형;
    static boolean àṣìṣe;

    static void ìkùnà_iye(String Ọ̀rọ̀_SMS) {
        if (!àṣìṣe) { aṣàmúlò.Kọ("JVM error: "); aṣàmúlò.Kọ(Ọ̀rọ̀_SMS); aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10); }
        àṣìṣe = true;
    }
    static boolean ní_ṣókí(int Rọ́ọ̀nù, int gígùn_iye) { return Rọ́ọ̀nù >= 0 && gígùn_iye >= 0 && Rọ́ọ̀nù <= Ìwọ̀n - gígùn_iye; }
    static int báìtì_iye() {
        if (!ní_ṣókí(읽기위치, 1)) { ìkùnà_iye("truncated class file"); return 0; }
        return Fáìlì[읽기위치++];
    }
    static int 짧은수() { return báìtì_iye() << 8 | báìtì_iye(); }
    static int nọ́ńbà_odindi() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int gígùn_iye) { if (!ní_ṣókí(읽기위치, gígùn_iye)) ìkùnà_iye("invalid attribute size"); else 읽기위치 += gígùn_iye; }
    static boolean ṣàyẹ̀wò_aláìṣeéyípadà(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || aláìṣeéyípadà_sàmì[수] != 종류) { ìkùnà_iye("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Rọ́ọ̀nù, int gígùn_iye, String Ọ̀rọ̀_SMS) {
        if (!ní_ṣókí(Rọ́ọ̀nù, gígùn_iye) || gígùn_iye != Ọ̀rọ̀_SMS.length()) return false;
        for (int 수 = 0; 수 < gígùn_iye; 수++) if (Fáìlì[Rọ́ọ̀nù + 수] != Ọ̀rọ̀_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !àṣìṣe; 수++) { ṣàyẹ̀wò_aláìṣeéyípadà(짧은수(), 1); 건너(nọ́ńbà_odindi()); }
    }
    static int àṣẹ_gígùn(int iye) {
        if (iye == 16 || iye == 18 || iye == 21 || iye == 25 || iye == 54 || iye == 58 || iye == 188) return 2;
        if (iye == 17 || iye == 19 || iye == 132 || iye >= 153 && iye <= 167
            || iye >= 178 && iye <= 184 || iye == 187 || iye == 189 || iye == 192 || iye == 198 || iye == 199) return 3;
        if (iye >= 0 && iye <= 8 || iye >= 26 && iye <= 29 || iye >= 42 && iye <= 46 || iye == 50
            || iye >= 59 && iye <= 62 || iye >= 75 && iye <= 79 || iye == 83 || iye == 87 || iye == 89 || iye == 95
            || iye == 96 || iye == 100 || iye == 104 || iye == 108 || iye == 112 || iye == 116
            || iye == 120 || iye == 122 || iye == 124 || iye == 126 || iye == 128 || iye == 130
            || iye >= 145 && iye <= 147 || iye == 172 || iye == 176 || iye == 177 || iye == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (nọ́ńbà_odindi() != 0xcafebabe) ìkùnà_iye("not a class file");
        int 부판 = 짧은수(), ẹ̀yà_iye = 짧은수();
        if (ẹ̀yà_iye < 45 || ẹ̀yà_iye > 52 || 부판 != 0) ìkùnà_iye("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { ìkùnà_iye("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !àṣìṣe; 수++) {
            int 종류 = báìtì_iye(); aláìṣeéyípadà_sàmì[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = nọ́ńbà_odindi();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else ìkùnà_iye("unsupported constant type");
        }
        int Ìyànda_iye = 짧은수();
        if ((Ìyànda_iye & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) ìkùnà_iye("unsupported class flags");
        ọ̀wọ́_orúkọ = ọ̀wọ́_orúkọ_SMS(짧은수());
        if (!Ọ̀rọ̀_SMS(ọ̀wọ́_orúkọ_SMS(짧은수()), "java/lang/Object")) ìkùnà_iye("inheritance unsupported");
        if (짧은수() != 0) ìkùnà_iye("interfaces unsupported");
        if (짧은수() != 0) ìkùnà_iye("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { ìkùnà_iye("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !àṣìṣe; 수++) {
            ìlànà_wáyè_sí[수] = 짧은수(); ìlànà_orúkọ_SMS[수] = 짧은수(); ìlànà_irú[수] = 짧은수();
            ṣàyẹ̀wò_aláìṣeéyípadà(ìlànà_orúkọ_SMS[수], 1); 서술읽기(수);
            if ((ìlànà_wáyè_sí[수] & (0x100 | 0x400 | 0x20)) != 0) ìkùnà_iye("native, abstract and synchronized methods unsupported");
            if ((ìlànà_wáyè_sí[수] & 8) == 0 && !Ọ̀rọ̀_SMS(ìlànà_orúkọ_SMS[수], "<init>")) ìkùnà_iye("instance methods unsupported");
            if (Ọ̀rọ̀_SMS(ìlànà_orúkọ_SMS[수], "<clinit>")) ìkùnà_iye("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(ìlànà_orúkọ_SMS[앞], ìlànà_orúkọ_SMS[수]) && 같은말(ìlànà_irú[앞], ìlànà_irú[수])) ìkùnà_iye("duplicate method");
            int 개수 = 짧은수();
            for (int àwòmọ́_iye = 0; àwòmọ́_iye < 개수 && !àṣìṣe; àwòmọ́_iye++) {
                int Orúkọ = 짧은수(), gígùn_iye = nọ́ńbà_odindi(), Rọ́ọ̀nù = 읽기위치;
                if (!ní_ṣókí(Rọ́ọ̀nù, gígùn_iye)) { ìkùnà_iye("truncated method attribute"); break; }
                if (Ọ̀rọ̀_SMS(Orúkọ, "Code")) {
                    if (ìlànà_bẹ̀rẹ̀[수] != 0) ìkùnà_iye("duplicate Code attribute");
                    ìlànà_kójọ[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = nọ́ńbà_odindi();
                    if (ìlànà_kójọ[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ìkùnà_iye("method memory limits exceeded");
                    ìlànà_bẹ̀rẹ̀[수] = 읽기위치; 건너(코드길이); ìlànà_parí[수] = 읽기위치;
                    if (짧은수() != 0) ìkùnà_iye("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Rọ́ọ̀nù + gígùn_iye) ìkùnà_iye("Code attribute size mismatch");
                } else 건너(gígùn_iye);
            }
            if (ìlànà_bẹ̀rẹ̀[수] == 0) ìkùnà_iye("missing Code attribute");
            int ààyè_ìfàyọkàsí_ìgbéwọlé = ìlànà_bẹ̀rẹ̀[수];
            while (ààyè_ìfàyọkàsí_ìgbéwọlé < ìlànà_parí[수] && !àṣìṣe) {
                int gígùn_iye = àṣẹ_gígùn(Fáìlì[ààyè_ìfàyọkàsí_ìgbéwọlé]);
                if (gígùn_iye == 0 || gígùn_iye > ìlànà_parí[수] - ààyè_ìfàyọkàsí_ìgbéwọlé) { ìkùnà_iye("unsupported or truncated bytecode"); break; }
                경계[ààyè_ìfàyọkàsí_ìgbéwọlé] = 수 + 1; ààyè_ìfàyọkàsí_ìgbéwọlé += gígùn_iye;
            }
            // 실행하지 않는 경로에도 잘못된 ẹ̀ka 목적지를 허용하지 않는다.
            ààyè_ìfàyọkàsí_ìgbéwọlé = ìlànà_bẹ̀rẹ̀[수];
            while (ààyè_ìfàyọkàsí_ìgbéwọlé < ìlànà_parí[수] && !àṣìṣe) {
                int iye = Fáìlì[ààyè_ìfàyọkàsí_ìgbéwọlé];
                if (iye >= 153 && iye <= 167 || iye == 198 || iye == 199) {
                    int èbúté_iye = ààyè_ìfàyọkàsí_ìgbéwọlé + (short)(Fáìlì[ààyè_ìfàyọkàsí_ìgbéwọlé + 1] << 8 | Fáìlì[ààyè_ìfàyọkàsí_ìgbéwọlé + 2]);
                    if (èbúté_iye < ìlànà_bẹ̀rẹ̀[수] || èbúté_iye >= ìlànà_parí[수] || 경계[èbúté_iye] != 수 + 1) ìkùnà_iye("invalid branch target");
                }
                ààyè_ìfàyọkàsí_ìgbéwọlé += àṣẹ_gígùn(iye);
            }
        }
        if (!àṣìṣe) 속성건너();
        if (읽기위치 != Ìwọ̀n) ìkùnà_iye("extra class file data");
    }
    static int pín_Ibi_ìpamọ́(int 종류, int gígùn_iye) {
        if (gígùn_iye < 0 || gígùn_iye > 힙.length - 힙끝 - 2) { ìkùnà_iye("object heap exhausted or negative array size"); return 0; }
        int Ìtọ́ka = 힙끝; 힙끝 += gígùn_iye + 2; 힙[Ìtọ́ka] = 종류; 힙[Ìtọ́ka + 1] = gígùn_iye;
        return Ìtọ́ka;
    }
    static boolean nǹkan_iye(int Ìtọ́ka, int 종류) {
        if (Ìtọ́ka < 1 || Ìtọ́ka >= 힙끝 - 1 || 힙[Ìtọ́ka] != 종류) { ìkùnà_iye("null or invalid object reference"); return false; }
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
        if (férèmù_wá_atọ̀ka_àkóónú == 31) { ìkùnà_iye("call stack limit (32)"); return; }
        int 다음 = férèmù_wá_atọ̀ka_àkóónú + 1;
        for (int 수 = 0; 수 < 128; 수++) agbègbè_irú[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[ÀKÀNṢEFỌMÚLÀ_iye] - 1; 수 >= 0; 수--) {
            agbègbè_iye[다음 * 128 + 수] = 빼기(ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수]); agbègbè_irú[다음 * 128 + 수] = ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수];
        }
        férèmù_wá_atọ̀ka_àkóónú = 다음; férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú] = ÀKÀNṢEFỌMÚLÀ_iye; 틀위치[férèmù_wá_atọ̀ka_àkóónú] = ìlànà_bẹ̀rẹ̀[ÀKÀNṢEFỌMÚLÀ_iye]; férèmù_kójọ[férèmù_wá_atọ̀ka_àkóónú] = 0;
    }
    static void 반환(int irú_iye) {
        if (irú_iye != 함수반환[férèmù_ìlànà[férèmù_wá_atọ̀ka_àkóónú]]) { ìkùnà_iye("return type mismatch"); return; }
        int iye = irú_iye == 0 ? 0 : 빼기(irú_iye);
        férèmù_wá_atọ̀ka_àkóónú--; if (férèmù_wá_atọ̀ka_àkóónú >= 0 && irú_iye != 0) 넣기(iye, irú_iye);
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
                if (iye < 1 || iye > 127) { ìkùnà_iye("file stream paths currently require ASCII"); return; }
                Stream_fáìlì_orúkọ[ààyè_ìfàyọkàsí_ìgbéwọlé] = iye;
            }
            Stream_fáìlì_orúkọ[gígùn_iye] = 0;
            int 서술자 = aṣàmúlò.파일서술자열기(Stream_fáìlì_orúkọ, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ìkùnà_iye("FileNotFoundException: file open failed"); return; }
            힙[Stream_iye + 2] = 서술자; 힙[Stream_iye + 3] = 1;
            return;
        }
        if (Àṣẹ != 182) { ìkùnà_iye("invalid file stream invocation"); return; }
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
            if (결과 < -1) ìkùnà_iye("IOException: read failed"); else 넣기(결과, 1);
        } else if (aṣàmúlò.파일한바이트쓰기(서술자, iye) != 1) ìkùnà_iye("IOException: write failed");
    }
    static void pè_ìlànà(int wá_atọ̀ka_àkóónú, int Àṣẹ) {
        if (!ṣàyẹ̀wò_aláìṣeéyípadà(wá_atọ̀ka_àkóónú, 10)) return;
        int Oníǹkan_iye = ọ̀wọ́_orúkọ_SMS(상가[wá_atọ̀ka_àkóónú]), Orúkọ = Ìtọ́ka_orúkọ(상나[wá_atọ̀ka_àkóónú]), ìgúnrégé_iye = Ìtọ́ka_irú(상나[wá_atọ̀ka_àkóónú]);
        if (àṣìṣe) return;
        if (같은말(Oníǹkan_iye, ọ̀wọ́_orúkọ)) {
            if (Àṣẹ != 184) { ìkùnà_iye("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Orúkọ, ìlànà_orúkọ_SMS[수]) && 같은말(ìgúnrégé_iye, ìlànà_irú[수])) {
                if ((ìlànà_wáyè_sí[수] & 8) == 0) ìkùnà_iye("method is not static"); else 호출(수);
                return;
            }
            ìkùnà_iye("NoSuchMethodError"); return;
        }
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
        ìkùnà_iye("unsupported library method");
    }
    static int ÀRÉÈ_ààyè_ìfàyọkàsí(int Ìtọ́ka, int òǹtẹ̀_ìsàlẹ̀_iye, int irú_iye) {
        if (!nǹkan_iye(Ìtọ́ka, irú_iye)) return 0;
        if (òǹtẹ̀_ìsàlẹ̀_iye < 0 || òǹtẹ̀_ìsàlẹ̀_iye >= 힙[Ìtọ́ka + 1]) { ìkùnà_iye("ArrayIndexOutOfBoundsException"); return 0; }
        return Ìtọ́ka + 2 + òǹtẹ̀_ìsàlẹ̀_iye;
    }
    static void ṣiṣẹ́_àṣẹ() {
        int 남음 = 500000;
        while (férèmù_wá_atọ̀ka_àkóónú >= 0 && !àṣìṣe) {
            if (--남음 == 0) { ìkùnà_iye("instruction limit (500000)"); break; }
            int Rọ́ọ̀nù = 틀위치[férèmù_wá_atọ̀ka_àkóónú], iye = 명바();
            if (àṣìṣe) break;
            if (iye == 0) continue;
            if (iye == 1) { 넣기(0, 2); continue; }
            if (iye >= 2 && iye <= 8) { 넣기(iye - 3, 1); continue; }
            if (iye == 16) { 넣기((byte)명바(), 1); continue; }
            if (iye == 17) { 넣기((short)명짧(), 1); continue; }
            if (iye == 18 || iye == 19) {
                int 수 = iye == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) ìkùnà_iye("invalid ldc constant");
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
            if (iye == 46 || iye == 50) {
                int òǹtẹ̀_ìsàlẹ̀_iye = 빼기(1), Ìtọ́ka = 빼기(2), ààyè_ìfàyọkàsí_ìgbéwọlé = ÀRÉÈ_ààyè_ìfàyọkàsí(Ìtọ́ka, òǹtẹ̀_ìsàlẹ̀_iye, iye == 46 ? 2 : 3);
                if (!àṣìṣe) 넣기(힙[ààyè_ìfàyọkàsí_ìgbéwọlé], iye == 46 ? 1 : 2); continue;
            }
            if (iye == 79 || iye == 83) {
                int wúnrẹ̀n_ìdá_ìpìlẹ̀ = 빼기(iye == 79 ? 1 : 2), òǹtẹ̀_ìsàlẹ̀_iye = 빼기(1), Ìtọ́ka = 빼기(2), ààyè_ìfàyọkàsí_ìgbéwọlé = ÀRÉÈ_ààyè_ìfàyọkàsí(Ìtọ́ka, òǹtẹ̀_ìsàlẹ̀_iye, iye == 79 ? 2 : 3);
                if (iye == 83 && wúnrẹ̀n_ìdá_ìpìlẹ̀ != 0) nǹkan_iye(wúnrẹ̀n_ìdá_ìpìlẹ̀, 1);
                if (!àṣìṣe) 힙[ààyè_ìfàyọkàsí_ìgbéwọlé] = wúnrẹ̀n_ìdá_ìpìlẹ̀; continue;
            }
            if (iye == 87) { 빼기(0); continue; }
            if (iye == 89) { int 가 = 빼기(0), irú_iye = 반환형; 넣기(가, irú_iye); 넣기(가, irú_iye); continue; }
            if (iye == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (iye == 178) {
                int 수 = 명짧(); if (!ṣàyẹ̀wò_aláìṣeéyípadà(수, 9)) continue;
                if (!Ọ̀rọ̀_SMS(ọ̀wọ́_orúkọ_SMS(상가[수]), "java/lang/System") || !Ọ̀rọ̀_SMS(Ìtọ́ka_orúkọ(상나[수]), "out")
                    || !Ọ̀rọ̀_SMS(Ìtọ́ka_irú(상나[수]), "Ljava/io/PrintStream;")) ìkùnà_iye("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (iye == 182 || iye == 183 || iye == 184) { pè_ìlànà(명짧(), iye); continue; }
            if (iye == 187) {
                int Orúkọ = ọ̀wọ́_orúkọ_SMS(명짧());
                if (Ọ̀rọ̀_SMS(Orúkọ, "java/lang/StringBuilder")) 넣기(pín_Ibi_ìpamọ́(4, 1), 2);
                else if (Ọ̀rọ̀_SMS(Orúkọ, "java/io/FileInputStream") || Ọ̀rọ̀_SMS(Orúkọ, "java/io/FileOutputStream")) {
                    int Ìtọ́ka = pín_Ibi_ìpamọ́(Ọ̀rọ̀_SMS(Orúkọ, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!àṣìṣe) { 힙[Ìtọ́ka + 2] = -1; 넣기(Ìtọ́ka, 2); }
                } else ìkùnà_iye("unsupported object construction");
                continue;
            }
            if (iye == 188 || iye == 189) {
                if (iye == 188) { if (명바() != 10) ìkùnà_iye("only int[] newarray is supported"); }
                else if (!Ọ̀rọ̀_SMS(ọ̀wọ́_orúkọ_SMS(명짧()), "java/lang/String")) ìkùnà_iye("only String[] anewarray is supported");
                int gígùn_iye = 빼기(1); 넣기(pín_Ibi_ìpamọ́(iye == 188 ? 2 : 3, gígùn_iye), 2); continue;
            }
            if (iye == 190) {
                int Ìtọ́ka = 빼기(2);
                if (Ìtọ́ka < 1 || Ìtọ́ka >= 힙끝 - 1 || (힙[Ìtọ́ka] != 2 && 힙[Ìtọ́ka] != 3)) ìkùnà_iye("null or invalid array");
                else 넣기(힙[Ìtọ́ka + 1], 1); continue;
            }
            if (iye == 192) {
                int Orúkọ = ọ̀wọ́_orúkọ_SMS(명짧()), Ìtọ́ka = 빼기(2);
                if (!Ọ̀rọ̀_SMS(Orúkọ, "java/lang/String")) ìkùnà_iye("unsupported checkcast");
                else if (Ìtọ́ka != 0) nǹkan_iye(Ìtọ́ka, 1);
                넣기(Ìtọ́ka, 2); continue;
            }
            ìkùnà_iye("unsupported bytecode");
        }
    }
    public static int Rọ́ọ̀nù() {
        if (aṣàmúlò.인수개수() == 1 && 자바도구.같음(aṣàmúlò.인수(0), "-version")) {
            aṣàmúlò.Kọ("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (aṣàmúlò.인수개수() < 1) { aṣàmúlò.Kọ("Usage: java CLASS [ARGS]\n"); return 2; }
        int gígùn_iye = 자바도구.Orúkọ(fáìlì_orúkọ_SMS, aṣàmúlò.인수(0));
        if (gígùn_iye < 1 || gígùn_iye > 57) { aṣàmúlò.Kọ("java: invalid class name\n"); return 2; }
        fáìlì_orúkọ_SMS[gígùn_iye] = '.'; fáìlì_orúkọ_SMS[gígùn_iye + 1] = 'c'; fáìlì_orúkọ_SMS[gígùn_iye + 2] = 'l'; fáìlì_orúkọ_SMS[gígùn_iye + 3] = 'a'; fáìlì_orúkọ_SMS[gígùn_iye + 4] = 's'; fáìlì_orúkọ_SMS[gígùn_iye + 5] = 's';
        Ìwọ̀n = aṣàmúlò.파일읽기(fáìlì_orúkọ_SMS, Fáìlì);
        if (Ìwọ̀n < 0) { aṣàmúlò.Kọ("java: cannot read class: "); 자바도구.수쓰기(Ìwọ̀n); aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10); return 1; }
        클래스읽기(); if (àṣìṣe) return 1;
        int ẹyọ_ọ̀rọ̀_orúkọ = aláìṣeéyípadà_SMS(ọ̀wọ́_orúkọ);
        if (!àṣìṣe && 힙[ẹyọ_ọ̀rọ̀_orúkọ + 1] != gígùn_iye) ìkùnà_iye("class name does not match file");
        for (int 수 = 0; 수 < gígùn_iye && !àṣìṣe; 수++) if (힙[ẹyọ_ọ̀rọ̀_orúkọ + 2 + 수] != fáìlì_orúkọ_SMS[수]) ìkùnà_iye("class name does not match file");
        int ìgbéwọlé_kókó_iye = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Ọ̀rọ̀_SMS(ìlànà_orúkọ_SMS[수], "main") && Ọ̀rọ̀_SMS(ìlànà_irú[수], "([Ljava/lang/String;)V") && (ìlànà_wáyè_sí[수] & 9) == 9) ìgbéwọlé_kókó_iye = 수;
        if (ìgbéwọlé_kókó_iye < 0) ìkùnà_iye("public static void main(String[] args) required");
        if (àṣìṣe) return 1;
        int 인수 = pín_Ibi_ìpamọ́(3, aṣàmúlò.인수개수() - 1);
        for (int 수 = 1; 수 < aṣàmúlò.인수개수() && !àṣìṣe; 수++) 힙[인수 + 1 + 수] = olùpèsè_ẹyọ_ọ̀rọ̀(aṣàmúlò.인수(수));
        férèmù_wá_atọ̀ka_àkóónú = 0; férèmù_ìlànà[0] = ìgbéwọlé_kókó_iye; 틀위치[0] = ìlànà_bẹ̀rẹ̀[ìgbéwọlé_kókó_iye]; agbègbè_iye[0] = 인수; agbègbè_irú[0] = 2;
        ṣiṣẹ́_àṣẹ(); return àṣìṣe ? 1 : 0;
    }
}
