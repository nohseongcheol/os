// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Skrá. 원본 breyta_VALUE/þýða_uppruni bilun_VALUE 시 기존 파일을 보존한다. */
public final class Minni_skrárkerfi {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] breyta_stærð_Listi = new int[8];
    static int[] opið_COUNT = new int[8], 허가들 = new int[8];
    static int[] Heiti = new int[64];
    static int[] breyta_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean yfirflæði_VALUE = false;
    static int breyta_breyta_stærð = 0;

    static boolean athuga_heiti(int[] stafur_VALUE, int lengd_VALUE) {
        if (lengd_VALUE < 1 || lengd_VALUE > 63) return false;
        for (int númer = 0; númer < lengd_VALUE; númer++) {
            int VALUE = stafur_VALUE[númer];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return stafur_VALUE[0] != '.';
    }

    static int FIND_færsla(int[] stafur_VALUE, int lengd_VALUE) {
        if (!athuga_heiti(stafur_VALUE, lengd_VALUE)) return -22;
        for (int númer = 0; númer < 8; númer++) {
            boolean 같음 = 이름들[númer * 64 + lengd_VALUE] == 0;
            for (int rauf_færsla = 0; rauf_færsla < lengd_VALUE; rauf_færsla++) if (이름들[númer * 64 + rauf_færsla] != stafur_VALUE[rauf_færsla]) 같음 = false;
            if (같음) return númer;
        }
        return -2;
    }

    static int Store_VALUE(int[] stafur_VALUE, int lengd_VALUE, int[] gögn, int Stærð) {
        if (!athuga_heiti(stafur_VALUE, lengd_VALUE) || Stærð < 0 || Stærð > gögn.length) return -22;
        if (Stærð > 최대크기) return -90;
        int INDEX = FIND_færsla(stafur_VALUE, lengd_VALUE);
        if (INDEX == -2) {
            for (int númer = 0; númer < 8 && INDEX < 0; númer++) if (이름들[númer * 64] == 0 && opið_COUNT[númer] == 0) INDEX = númer;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int slóð = tæki_VALUE.skrá_Minni() + INDEX * 최대크기;
        for (int númer = 0; númer < Stærð; númer++) tæki_VALUE.skrifa_Minni(slóð + númer, gögn[númer]);
        for (int númer = 0; númer < 64; númer++) 이름들[INDEX * 64 + númer] = númer < lengd_VALUE ? stafur_VALUE[númer] : 0;
        breyta_stærð_Listi[INDEX] = Stærð;
        return Stærð;
    }

    static void færsla_Listi() {
        for (int númer = 0; númer < 8; númer++) if (이름들[númer * 64] != 0) {
            for (int rauf_færsla = 0; rauf_færsla < 64 && 이름들[númer * 64 + rauf_færsla] != 0; rauf_færsla++) SMS_Endastöð.문자(이름들[númer * 64 + rauf_færsla]);
            SMS_Endastöð.Skrift("  "); SMS_Endastöð.skrifa_númer(breyta_stærð_Listi[númer]); SMS_Endastöð.Skrift("bæti_VALUE\n");
        }
        SMS_Endastöð.Skrift(geymsla_tæki_tenging.upplýsingatækni_Laus_9e72441a ? "Skrá 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Skrá 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Skipun(int[] 입력, int Keyra_2, int lengd_VALUE, int Aðgerð) {
        while (Keyra_2 < lengd_VALUE && 입력[Keyra_2] == ' ') Keyra_2++;
        int 끝 = lengd_VALUE;
        while (끝 > Keyra_2 && 입력[끝 - 1] == ' ') 끝--;
        int númer = 끝 - Keyra_2;
        if (númer < 1 || númer > 63) { SMS_Endastöð.Skrift("올바르지 않은 Skrá Heiti\n"); return; }
        for (int rauf_færsla = 0; rauf_færsla < 64; rauf_færsla++) Heiti[rauf_færsla] = rauf_færsla < númer ? 입력[Keyra_2 + rauf_færsla] : 0;
        int INDEX = FIND_færsla(Heiti, númer);
        if (INDEX == -22) { SMS_Endastöð.Skrift("올바르지 않은 Skrá Heiti\n"); return; }
        if (Aðgerð == 0) {
            편집중 = true; breyta_breyta_stærð = 0; yfirflæði_VALUE = false;
            SMS_Endastöð.Skrift("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Endastöð.Skrift("파일을 찾을 númer 없습니다\n");
        else if (Aðgerð == 1) {
            int slóð = tæki_VALUE.skrá_Minni() + INDEX * 최대크기;
            for (int rauf_færsla = 0; rauf_færsla < breyta_stærð_Listi[INDEX]; rauf_færsla++) SMS_Endastöð.문자(tæki_VALUE.기억읽기(slóð + rauf_færsla));
            SMS_Endastöð.문자(10);
        } else { 이름들[INDEX * 64] = 0; breyta_stærð_Listi[INDEX] = 0; SMS_Endastöð.Skrift("파일을 지웠습니다\n"); }
    }

    static boolean upplýsingatækni_EXACT(int[] 입력, int lengd_VALUE, String 문구) {
        if (lengd_VALUE != 문구.length()) return false;
        for (int rauf_færsla = 0; rauf_færsla < lengd_VALUE; rauf_færsla++) if (입력[rauf_færsla] != 문구.charAt(rauf_færsla)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int lengd_VALUE, boolean lína_yfirflæði) {
        if (upplýsingatækni_EXACT(입력, lengd_VALUE, ".cancel")) {
            편집중 = false; SMS_Endastöð.Skrift("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (upplýsingatækni_EXACT(입력, lengd_VALUE, ".save")) {
            편집중 = false;
            if (yfirflæði_VALUE) { SMS_Endastöð.Skrift("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int númer = 0;
            while (númer < 64 && Heiti[númer] != 0) númer++;
            int NIÐURSTAÐA = Store_VALUE(Heiti, númer, breyta_VALUE, breyta_breyta_stærð);
            SMS_Endastöð.Skrift(NIÐURSTAÐA >= 0 ? "보존한 bæti_VALUE númer: " : "보존 bilun_VALUE: ");
            SMS_Endastöð.skrifa_númer(NIÐURSTAÐA); SMS_Endastöð.문자(10);
        } else if (lína_yfirflæði || lengd_VALUE + 1 > 최대크기 - breyta_breyta_stærð) yfirflæði_VALUE = true;
        else {
            for (int númer = 0; númer < lengd_VALUE; númer++) breyta_VALUE[breyta_breyta_stærð++] = 입력[númer];
            breyta_VALUE[breyta_breyta_stærð++] = 10;
        }
    }

    static void 예제(String Skrá, String Efni_VALUE) {
        for (int númer = 0; númer < 64; númer++) Heiti[númer] = númer < Skrá.length() ? Skrá.charAt(númer) : 0;
        for (int númer = 0; númer < Efni_VALUE.length(); númer++) breyta_VALUE[númer] = Efni_VALUE.charAt(númer);
        Store_VALUE(Heiti, Skrá.length(), breyta_VALUE, Efni_VALUE.length());
    }

    static void Undirbúa() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Hópur_VALUE = tæki_VALUE.자바파일묶음(), Stærð = tæki_VALUE.자바파일묶음크기();
        if (Stærð < 8 || 실행관리.númer(Hópur_VALUE) != 0x464a4b4a) { SMS_Endastöð.Skrift("올바르지 않은 Java Skrá Hópur_VALUE\n"); return; }
        int vara_COUNT = 실행관리.númer(Hópur_VALUE + 4);
        if (vara_COUNT < 0 || vara_COUNT > 8 || vara_COUNT > (Stærð - 8) / 72) { SMS_Endastöð.Skrift("올바르지 않은 Java Skrá færsla_Listi\n"); return; }
        for (int númer = 0; númer < vara_COUNT; númer++) {
            int færsla_VALUE = Hópur_VALUE + 8 + númer * 72, lengd_VALUE = 0;
            for (int rauf_færsla = 0; rauf_færsla < 64; rauf_færsla++) Heiti[rauf_færsla] = tæki_VALUE.기억읽기(færsla_VALUE + rauf_færsla);
            while (lengd_VALUE < 64 && Heiti[lengd_VALUE] != 0) lengd_VALUE++;
            int Staðsetning = 실행관리.númer(færsla_VALUE + 64), skrá_breyta_stærð = 실행관리.númer(færsla_VALUE + 68);
            if (!athuga_heiti(Heiti, lengd_VALUE) || skrá_breyta_stærð < 0 || skrá_breyta_stærð > 최대크기 || Staðsetning < 8 + vara_COUNT * 72 || Staðsetning > Stærð - skrá_breyta_stærð) {
                SMS_Endastöð.Skrift("올바르지 않은 Java Skrá færsla_VALUE\n"); return;
            }
            for (int rauf_færsla = 0; rauf_færsla < skrá_breyta_stærð; rauf_færsla++) breyta_VALUE[rauf_færsla] = tæki_VALUE.기억읽기(Hópur_VALUE + Staðsetning + rauf_færsla);
            if (Store_VALUE(Heiti, lengd_VALUE, breyta_VALUE, skrá_breyta_stærð) < 0) { SMS_Endastöð.Skrift("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
