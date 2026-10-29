// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 faele. 원본 Tseleganya_Boleng/aga_Motswedi palelo_Boleng 시 기존 파일을 보존한다. */
public final class memori_setsamaisadifaele {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] lekanya_lenaane = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] leina = new int[64];
    static int[] Tseleganya_Boleng = new int[최대크기];
    static boolean 편집중 = false;
    static boolean penologo_Boleng = false;
    static int Tseleganya_lekanya = 0;

    static boolean tlhola_leina(int[] Letshwao_Boleng, int boleele_Boleng) {
        if (boleele_Boleng < 1 || boleele_Boleng > 63) return false;
        for (int 수 = 0; 수 < boleele_Boleng; 수++) {
            int Boleng = Letshwao_Boleng[수];
            if (!(Boleng >= 'a' && Boleng <= 'z') && !(Boleng >= 'A' && Boleng <= 'Z')
                && !(Boleng >= '0' && Boleng <= '9') && Boleng != '_' && Boleng != '-' && Boleng != '.') return false;
        }
        return Letshwao_Boleng[0] != '.';
    }

    static int batla_tsenyo(int[] Letshwao_Boleng, int boleele_Boleng) {
        if (!tlhola_leina(Letshwao_Boleng, boleele_Boleng)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + boleele_Boleng] == 0;
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < boleele_Boleng; sebaka_tsenyo++) if (이름들[수 * 64 + sebaka_tsenyo] != Letshwao_Boleng[sebaka_tsenyo]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_Boleng(int[] Letshwao_Boleng, int boleele_Boleng, int[] tshedimosetso, int lekanya) {
        if (!tlhola_leina(Letshwao_Boleng, boleele_Boleng) || lekanya < 0 || lekanya > tshedimosetso.length) return -22;
        if (lekanya > 최대크기) return -90;
        int tshupane = batla_tsenyo(Letshwao_Boleng, boleele_Boleng);
        if (tshupane == -2) {
            for (int 수 = 0; 수 < 8 && tshupane < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) tshupane = 수;
            if (tshupane >= 0) 허가들[tshupane] = 438;
        }
        if (tshupane < 0) return -28;
        int aterese = mobaele_Boleng.faele_memori() + tshupane * 최대크기;
        for (int 수 = 0; 수 < lekanya; 수++) mobaele_Boleng.kwala_memori(aterese + 수, tshedimosetso[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[tshupane * 64 + 수] = 수 < boleele_Boleng ? Letshwao_Boleng[수] : 0;
        lekanya_lenaane[tshupane] = lekanya;
        return lekanya;
    }

    static void tsenyo_lenaane() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 64 && 이름들[수 * 64 + sebaka_tsenyo] != 0; sebaka_tsenyo++) 문자단말.문자(이름들[수 * 64 + sebaka_tsenyo]);
            문자단말.kwala("  "); 문자단말.수쓰기(lekanya_lenaane[수]); 문자단말.kwala("baete_Boleng\n");
        }
        문자단말.kwala(Polokelo_mobaele_Kgolagano.사용가능 ? "faele 8칸, 파일당 16384바이트; sync로 Store_Boleng 장치에 보존\n"
            : "임시 faele 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Taelo(int[] 입력, int dirisa, int boleele_Boleng, int tiro) {
        while (dirisa < boleele_Boleng && 입력[dirisa] == ' ') dirisa++;
        int 끝 = boleele_Boleng;
        while (끝 > dirisa && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - dirisa;
        if (수 < 1 || 수 > 63) { 문자단말.kwala("올바르지 않은 faele leina\n"); return; }
        for (int sebaka_tsenyo = 0; sebaka_tsenyo < 64; sebaka_tsenyo++) leina[sebaka_tsenyo] = sebaka_tsenyo < 수 ? 입력[dirisa + sebaka_tsenyo] : 0;
        int tshupane = batla_tsenyo(leina, 수);
        if (tshupane == -22) { 문자단말.kwala("올바르지 않은 faele leina\n"); return; }
        if (tiro == 0) {
            편집중 = true; Tseleganya_lekanya = 0; penologo_Boleng = false;
            문자단말.kwala("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (tshupane < 0) 문자단말.kwala("파일을 찾을 수 없습니다\n");
        else if (tiro == 1) {
            int aterese = mobaele_Boleng.faele_memori() + tshupane * 최대크기;
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < lekanya_lenaane[tshupane]; sebaka_tsenyo++) 문자단말.문자(mobaele_Boleng.기억읽기(aterese + sebaka_tsenyo));
            문자단말.문자(10);
        } else { 이름들[tshupane * 64] = 0; lekanya_lenaane[tshupane] = 0; 문자단말.kwala("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int boleele_Boleng, String 문구) {
        if (boleele_Boleng != 문구.length()) return false;
        for (int sebaka_tsenyo = 0; sebaka_tsenyo < boleele_Boleng; sebaka_tsenyo++) if (입력[sebaka_tsenyo] != 문구.charAt(sebaka_tsenyo)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int boleele_Boleng, boolean Mola_penologo) {
        if (정확(입력, boleele_Boleng, ".cancel")) {
            편집중 = false; 문자단말.kwala("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, boleele_Boleng, ".save")) {
            편집중 = false;
            if (penologo_Boleng) { 문자단말.kwala("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && leina[수] != 0) 수++;
            int 결과 = Store_Boleng(leina, 수, Tseleganya_Boleng, Tseleganya_lekanya);
            문자단말.kwala(결과 >= 0 ? "보존한 baete_Boleng 수: " : "보존 palelo_Boleng: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (Mola_penologo || boleele_Boleng + 1 > 최대크기 - Tseleganya_lekanya) penologo_Boleng = true;
        else {
            for (int 수 = 0; 수 < boleele_Boleng; 수++) Tseleganya_Boleng[Tseleganya_lekanya++] = 입력[수];
            Tseleganya_Boleng[Tseleganya_lekanya++] = 10;
        }
    }

    static void 예제(String faele, String Diteng_Boleng) {
        for (int 수 = 0; 수 < 64; 수++) leina[수] = 수 < faele.length() ? faele.charAt(수) : 0;
        for (int 수 = 0; 수 < Diteng_Boleng.length(); 수++) Tseleganya_Boleng[수] = Diteng_Boleng.charAt(수);
        Store_Boleng(leina, faele.length(), Tseleganya_Boleng, Diteng_Boleng.length());
    }

    static void Baakanya() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int setlhopha_Boleng = mobaele_Boleng.자바파일묶음(), lekanya = mobaele_Boleng.자바파일묶음크기();
        if (lekanya < 8 || 실행관리.수(setlhopha_Boleng) != 0x464a4b4a) { 문자단말.kwala("올바르지 않은 Java faele setlhopha_Boleng\n"); return; }
        int 개수 = 실행관리.수(setlhopha_Boleng + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (lekanya - 8) / 72) { 문자단말.kwala("올바르지 않은 Java faele tsenyo_lenaane\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int tsenyo_Boleng = setlhopha_Boleng + 8 + 수 * 72, boleele_Boleng = 0;
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 64; sebaka_tsenyo++) leina[sebaka_tsenyo] = mobaele_Boleng.기억읽기(tsenyo_Boleng + sebaka_tsenyo);
            while (boleele_Boleng < 64 && leina[boleele_Boleng] != 0) boleele_Boleng++;
            int 위치 = 실행관리.수(tsenyo_Boleng + 64), faele_lekanya = 실행관리.수(tsenyo_Boleng + 68);
            if (!tlhola_leina(leina, boleele_Boleng) || faele_lekanya < 0 || faele_lekanya > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > lekanya - faele_lekanya) {
                문자단말.kwala("올바르지 않은 Java faele tsenyo_Boleng\n"); return;
            }
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < faele_lekanya; sebaka_tsenyo++) Tseleganya_Boleng[sebaka_tsenyo] = mobaele_Boleng.기억읽기(setlhopha_Boleng + 위치 + sebaka_tsenyo);
            if (Store_Boleng(leina, boleele_Boleng, Tseleganya_Boleng, faele_lekanya) < 0) { 문자단말.kwala("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
