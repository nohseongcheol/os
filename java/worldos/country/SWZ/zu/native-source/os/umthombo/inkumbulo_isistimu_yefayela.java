// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Ihele. 원본 hlela_inani/akha_umthombo ukwehluleka_inani 시 기존 파일을 보존한다. */
public final class inkumbulo_isistimu_yefayela {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] linganisa_Uhlu = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Igama = new int[64];
    static int[] hlela_inani = new int[최대크기];
    static boolean 편집중 = false;
    static boolean ukukapaka_inani = false;
    static int hlela_linganisa = 0;

    static boolean hlola_igama(int[] uhlamvusimo_inani, int ubude_inani) {
        if (ubude_inani < 1 || ubude_inani > 63) return false;
        for (int 수 = 0; 수 < ubude_inani; 수++) {
            int inani = uhlamvusimo_inani[수];
            if (!(inani >= 'a' && inani <= 'z') && !(inani >= 'A' && inani <= 'Z')
                && !(inani >= '0' && inani <= '9') && inani != '_' && inani != '-' && inani != '.') return false;
        }
        return uhlamvusimo_inani[0] != '.';
    }

    static int thola_okufakwayo(int[] uhlamvusimo_inani, int ubude_inani) {
        if (!hlola_igama(uhlamvusimo_inani, ubude_inani)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + ubude_inani] == 0;
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < ubude_inani; isikhala_okufakwayo++) if (이름들[수 * 64 + isikhala_okufakwayo] != uhlamvusimo_inani[isikhala_okufakwayo]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_inani(int[] uhlamvusimo_inani, int ubude_inani, int[] imininingwane, int Ubungako) {
        if (!hlola_igama(uhlamvusimo_inani, ubude_inani) || Ubungako < 0 || Ubungako > imininingwane.length) return -22;
        if (Ubungako > 최대크기) return -90;
        int thola_inkomba = thola_okufakwayo(uhlamvusimo_inani, ubude_inani);
        if (thola_inkomba == -2) {
            for (int 수 = 0; 수 < 8 && thola_inkomba < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) thola_inkomba = 수;
            if (thola_inkomba >= 0) 허가들[thola_inkomba] = 438;
        }
        if (thola_inkomba < 0) return -28;
        int ikheli = idivayisi_inani.ifayela_inkumbulo() + thola_inkomba * 최대크기;
        for (int 수 = 0; 수 < Ubungako; 수++) idivayisi_inani.bhala_inkumbulo(ikheli + 수, imininingwane[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[thola_inkomba * 64 + 수] = 수 < ubude_inani ? uhlamvusimo_inani[수] : 0;
        linganisa_Uhlu[thola_inkomba] = Ubungako;
        return Ubungako;
    }

    static void okufakwayo_Uhlu() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 64 && 이름들[수 * 64 + isikhala_okufakwayo] != 0; isikhala_okufakwayo++) 문자단말.문자(이름들[수 * 64 + isikhala_okufakwayo]);
            문자단말.Bhala("  "); 문자단말.수쓰기(linganisa_Uhlu[수]); 문자단말.Bhala("ibhayithi_inani\n");
        }
        문자단말.Bhala(Indawo_yokugcina_idivayisi_uxhumano.사용가능 ? "Ihele 8칸, 파일당 16384바이트; sync로 Store_inani 장치에 보존\n"
            : "임시 Ihele 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Umlayelo(int[] 입력, int Sebenzisa, int ubude_inani, int Isenzo) {
        while (Sebenzisa < ubude_inani && 입력[Sebenzisa] == ' ') Sebenzisa++;
        int 끝 = ubude_inani;
        while (끝 > Sebenzisa && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Sebenzisa;
        if (수 < 1 || 수 > 63) { 문자단말.Bhala("올바르지 않은 Ihele Igama\n"); return; }
        for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 64; isikhala_okufakwayo++) Igama[isikhala_okufakwayo] = isikhala_okufakwayo < 수 ? 입력[Sebenzisa + isikhala_okufakwayo] : 0;
        int thola_inkomba = thola_okufakwayo(Igama, 수);
        if (thola_inkomba == -22) { 문자단말.Bhala("올바르지 않은 Ihele Igama\n"); return; }
        if (Isenzo == 0) {
            편집중 = true; hlela_linganisa = 0; ukukapaka_inani = false;
            문자단말.Bhala("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (thola_inkomba < 0) 문자단말.Bhala("파일을 찾을 수 없습니다\n");
        else if (Isenzo == 1) {
            int ikheli = idivayisi_inani.ifayela_inkumbulo() + thola_inkomba * 최대크기;
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < linganisa_Uhlu[thola_inkomba]; isikhala_okufakwayo++) 문자단말.문자(idivayisi_inani.기억읽기(ikheli + isikhala_okufakwayo));
            문자단말.문자(10);
        } else { 이름들[thola_inkomba * 64] = 0; linganisa_Uhlu[thola_inkomba] = 0; 문자단말.Bhala("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int ubude_inani, String 문구) {
        if (ubude_inani != 문구.length()) return false;
        for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < ubude_inani; isikhala_okufakwayo++) if (입력[isikhala_okufakwayo] != 문구.charAt(isikhala_okufakwayo)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int ubude_inani, boolean umugqa_ukukapaka) {
        if (정확(입력, ubude_inani, ".cancel")) {
            편집중 = false; 문자단말.Bhala("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, ubude_inani, ".save")) {
            편집중 = false;
            if (ukukapaka_inani) { 문자단말.Bhala("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Igama[수] != 0) 수++;
            int 결과 = Store_inani(Igama, 수, hlela_inani, hlela_linganisa);
            문자단말.Bhala(결과 >= 0 ? "보존한 ibhayithi_inani 수: " : "보존 ukwehluleka_inani: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (umugqa_ukukapaka || ubude_inani + 1 > 최대크기 - hlela_linganisa) ukukapaka_inani = true;
        else {
            for (int 수 = 0; 수 < ubude_inani; 수++) hlela_inani[hlela_linganisa++] = 입력[수];
            hlela_inani[hlela_linganisa++] = 10;
        }
    }

    static void 예제(String Ihele, String Okuqukethwe_inani) {
        for (int 수 = 0; 수 < 64; 수++) Igama[수] = 수 < Ihele.length() ? Ihele.charAt(수) : 0;
        for (int 수 = 0; 수 < Okuqukethwe_inani.length(); 수++) hlela_inani[수] = Okuqukethwe_inani.charAt(수);
        Store_inani(Igama, Ihele.length(), hlela_inani, Okuqukethwe_inani.length());
    }

    static void Hlela() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int iqoqo_inani = idivayisi_inani.자바파일묶음(), Ubungako = idivayisi_inani.자바파일묶음크기();
        if (Ubungako < 8 || 실행관리.수(iqoqo_inani) != 0x464a4b4a) { 문자단말.Bhala("올바르지 않은 Java Ihele iqoqo_inani\n"); return; }
        int 개수 = 실행관리.수(iqoqo_inani + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Ubungako - 8) / 72) { 문자단말.Bhala("올바르지 않은 Java Ihele okufakwayo_Uhlu\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int okufakwayo_inani = iqoqo_inani + 8 + 수 * 72, ubude_inani = 0;
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 64; isikhala_okufakwayo++) Igama[isikhala_okufakwayo] = idivayisi_inani.기억읽기(okufakwayo_inani + isikhala_okufakwayo);
            while (ubude_inani < 64 && Igama[ubude_inani] != 0) ubude_inani++;
            int 위치 = 실행관리.수(okufakwayo_inani + 64), ifayela_linganisa = 실행관리.수(okufakwayo_inani + 68);
            if (!hlola_igama(Igama, ubude_inani) || ifayela_linganisa < 0 || ifayela_linganisa > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Ubungako - ifayela_linganisa) {
                문자단말.Bhala("올바르지 않은 Java Ihele okufakwayo_inani\n"); return;
            }
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < ifayela_linganisa; isikhala_okufakwayo++) hlela_inani[isikhala_okufakwayo] = idivayisi_inani.기억읽기(iqoqo_inani + 위치 + isikhala_okufakwayo);
            if (Store_inani(Igama, ubude_inani, hlela_inani, ifayela_linganisa) < 0) { 문자단말.Bhala("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
