// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fáìlì. 원본 ṣàtúnṣe_iye/ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun ìkùnà_iye 시 기존 파일을 보존한다. */
public final class ibi_ìpamọ́_ìlànà_ètò_fáìlì {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ìwọn_Àtòkọ = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Orúkọ = new int[64];
    static int[] ṣàtúnṣe_iye = new int[최대크기];
    static boolean 편집중 = false;
    static boolean rékọjá_iye = false;
    static int ṣàtúnṣe_ìwọn = 0;

    static boolean ṣàyẹ̀wò_orúkọ(int[] ẹyọ_ọ̀rọ̀_iye, int gígùn_iye) {
        if (gígùn_iye < 1 || gígùn_iye > 63) return false;
        for (int 수 = 0; 수 < gígùn_iye; 수++) {
            int iye = ẹyọ_ọ̀rọ̀_iye[수];
            if (!(iye >= 'a' && iye <= 'z') && !(iye >= 'A' && iye <= 'Z')
                && !(iye >= '0' && iye <= '9') && iye != '_' && iye != '-' && iye != '.') return false;
        }
        return ẹyọ_ọ̀rọ̀_iye[0] != '.';
    }

    static int wá_ìgbéwọlé(int[] ẹyọ_ọ̀rọ̀_iye, int gígùn_iye) {
        if (!ṣàyẹ̀wò_orúkọ(ẹyọ_ọ̀rọ̀_iye, gígùn_iye)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + gígùn_iye] == 0;
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < gígùn_iye; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (이름들[수 * 64 + ààyè_ìfàyọkàsí_ìgbéwọlé] != ẹyọ_ọ̀rọ̀_iye[ààyè_ìfàyọkàsí_ìgbéwọlé]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_iye(int[] ẹyọ_ọ̀rọ̀_iye, int gígùn_iye, int[] détà, int Ìwọ̀n) {
        if (!ṣàyẹ̀wò_orúkọ(ẹyọ_ọ̀rọ̀_iye, gígùn_iye) || Ìwọ̀n < 0 || Ìwọ̀n > détà.length) return -22;
        if (Ìwọ̀n > 최대크기) return -90;
        int wá_atọ̀ka_àkóónú = wá_ìgbéwọlé(ẹyọ_ọ̀rọ̀_iye, gígùn_iye);
        if (wá_atọ̀ka_àkóónú == -2) {
            for (int 수 = 0; 수 < 8 && wá_atọ̀ka_àkóónú < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) wá_atọ̀ka_àkóónú = 수;
            if (wá_atọ̀ka_àkóónú >= 0) 허가들[wá_atọ̀ka_àkóónú] = 438;
        }
        if (wá_atọ̀ka_àkóónú < 0) return -28;
        int àdírẹ́ẹ̀sì = ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + wá_atọ̀ka_àkóónú * 최대크기;
        for (int 수 = 0; 수 < Ìwọ̀n; 수++) ohun_èlò_iye.kọ_ibi_ìpamọ́(àdírẹ́ẹ̀sì + 수, détà[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[wá_atọ̀ka_àkóónú * 64 + 수] = 수 < gígùn_iye ? ẹyọ_ọ̀rọ̀_iye[수] : 0;
        ìwọn_Àtòkọ[wá_atọ̀ka_àkóónú] = Ìwọ̀n;
        return Ìwọ̀n;
    }

    static void ìgbéwọlé_Àtòkọ() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 64 && 이름들[수 * 64 + ààyè_ìfàyọkàsí_ìgbéwọlé] != 0; ààyè_ìfàyọkàsí_ìgbéwọlé++) 문자단말.문자(이름들[수 * 64 + ààyè_ìfàyọkàsí_ìgbéwọlé]);
            문자단말.Kọ("  "); 문자단말.수쓰기(ìwọn_Àtòkọ[수]); 문자단말.Kọ("báìtì_iye\n");
        }
        문자단말.Kọ(Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.사용가능 ? "Fáìlì 8칸, 파일당 16384바이트; sync로 Store_iye 장치에 보존\n"
            : "임시 Fáìlì 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Àṣẹ(int[] 입력, int Rọ́ọ̀nù, int gígùn_iye, int ìṣe) {
        while (Rọ́ọ̀nù < gígùn_iye && 입력[Rọ́ọ̀nù] == ' ') Rọ́ọ̀nù++;
        int 끝 = gígùn_iye;
        while (끝 > Rọ́ọ̀nù && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Rọ́ọ̀nù;
        if (수 < 1 || 수 > 63) { 문자단말.Kọ("올바르지 않은 Fáìlì Orúkọ\n"); return; }
        for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 64; ààyè_ìfàyọkàsí_ìgbéwọlé++) Orúkọ[ààyè_ìfàyọkàsí_ìgbéwọlé] = ààyè_ìfàyọkàsí_ìgbéwọlé < 수 ? 입력[Rọ́ọ̀nù + ààyè_ìfàyọkàsí_ìgbéwọlé] : 0;
        int wá_atọ̀ka_àkóónú = wá_ìgbéwọlé(Orúkọ, 수);
        if (wá_atọ̀ka_àkóónú == -22) { 문자단말.Kọ("올바르지 않은 Fáìlì Orúkọ\n"); return; }
        if (ìṣe == 0) {
            편집중 = true; ṣàtúnṣe_ìwọn = 0; rékọjá_iye = false;
            문자단말.Kọ("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (wá_atọ̀ka_àkóónú < 0) 문자단말.Kọ("파일을 찾을 수 없습니다\n");
        else if (ìṣe == 1) {
            int àdírẹ́ẹ̀sì = ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + wá_atọ̀ka_àkóónú * 최대크기;
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < ìwọn_Àtòkọ[wá_atọ̀ka_àkóónú]; ààyè_ìfàyọkàsí_ìgbéwọlé++) 문자단말.문자(ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + ààyè_ìfàyọkàsí_ìgbéwọlé));
            문자단말.문자(10);
        } else { 이름들[wá_atọ̀ka_àkóónú * 64] = 0; ìwọn_Àtòkọ[wá_atọ̀ka_àkóónú] = 0; 문자단말.Kọ("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int gígùn_iye, String 문구) {
        if (gígùn_iye != 문구.length()) return false;
        for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < gígùn_iye; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (입력[ààyè_ìfàyọkàsí_ìgbéwọlé] != 문구.charAt(ààyè_ìfàyọkàsí_ìgbéwọlé)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int gígùn_iye, boolean ìlà_rékọjá) {
        if (정확(입력, gígùn_iye, ".cancel")) {
            편집중 = false; 문자단말.Kọ("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, gígùn_iye, ".save")) {
            편집중 = false;
            if (rékọjá_iye) { 문자단말.Kọ("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Orúkọ[수] != 0) 수++;
            int 결과 = Store_iye(Orúkọ, 수, ṣàtúnṣe_iye, ṣàtúnṣe_ìwọn);
            문자단말.Kọ(결과 >= 0 ? "보존한 báìtì_iye 수: " : "보존 ìkùnà_iye: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (ìlà_rékọjá || gígùn_iye + 1 > 최대크기 - ṣàtúnṣe_ìwọn) rékọjá_iye = true;
        else {
            for (int 수 = 0; 수 < gígùn_iye; 수++) ṣàtúnṣe_iye[ṣàtúnṣe_ìwọn++] = 입력[수];
            ṣàtúnṣe_iye[ṣàtúnṣe_ìwọn++] = 10;
        }
    }

    static void 예제(String Fáìlì, String Àkóónú_iye) {
        for (int 수 = 0; 수 < 64; 수++) Orúkọ[수] = 수 < Fáìlì.length() ? Fáìlì.charAt(수) : 0;
        for (int 수 = 0; 수 < Àkóónú_iye.length(); 수++) ṣàtúnṣe_iye[수] = Àkóónú_iye.charAt(수);
        Store_iye(Orúkọ, Fáìlì.length(), ṣàtúnṣe_iye, Àkóónú_iye.length());
    }

    static void gbaradì() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Àjọṣe_iye = ohun_èlò_iye.자바파일묶음(), Ìwọ̀n = ohun_èlò_iye.자바파일묶음크기();
        if (Ìwọ̀n < 8 || 실행관리.수(Àjọṣe_iye) != 0x464a4b4a) { 문자단말.Kọ("올바르지 않은 Java Fáìlì Àjọṣe_iye\n"); return; }
        int 개수 = 실행관리.수(Àjọṣe_iye + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Ìwọ̀n - 8) / 72) { 문자단말.Kọ("올바르지 않은 Java Fáìlì ìgbéwọlé_Àtòkọ\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int ìgbéwọlé_iye = Àjọṣe_iye + 8 + 수 * 72, gígùn_iye = 0;
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 64; ààyè_ìfàyọkàsí_ìgbéwọlé++) Orúkọ[ààyè_ìfàyọkàsí_ìgbéwọlé] = ohun_èlò_iye.기억읽기(ìgbéwọlé_iye + ààyè_ìfàyọkàsí_ìgbéwọlé);
            while (gígùn_iye < 64 && Orúkọ[gígùn_iye] != 0) gígùn_iye++;
            int 위치 = 실행관리.수(ìgbéwọlé_iye + 64), fáìlì_ìwọn = 실행관리.수(ìgbéwọlé_iye + 68);
            if (!ṣàyẹ̀wò_orúkọ(Orúkọ, gígùn_iye) || fáìlì_ìwọn < 0 || fáìlì_ìwọn > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Ìwọ̀n - fáìlì_ìwọn) {
                문자단말.Kọ("올바르지 않은 Java Fáìlì ìgbéwọlé_iye\n"); return;
            }
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < fáìlì_ìwọn; ààyè_ìfàyọkàsí_ìgbéwọlé++) ṣàtúnṣe_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] = ohun_èlò_iye.기억읽기(Àjọṣe_iye + 위치 + ààyè_ìfàyọkàsí_ìgbéwọlé);
            if (Store_iye(Orúkọ, gígùn_iye, ṣàtúnṣe_iye, fáìlì_ìwọn) < 0) { 문자단말.Kọ("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
