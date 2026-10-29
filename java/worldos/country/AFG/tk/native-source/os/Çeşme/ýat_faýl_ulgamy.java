// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Faýl. 원본 redaktirle_baha/düz_gor näsazlyk_baha 시 기존 파일을 보존한다. */
public final class ýat_faýl_ulgamy {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ölçegi_üýtget_Sanaw = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Ad = new int[64];
    static int[] redaktirle_baha = new int[최대크기];
    static boolean 편집중 = false;
    static boolean gyrmalanma_baha = false;
    static int redaktirle_ölçegi_üýtget = 0;

    static boolean derňe_at(int[] nyşan_baha_068c2631, int dowamlylyk_baha) {
        if (dowamlylyk_baha < 1 || dowamlylyk_baha > 63) return false;
        for (int 수 = 0; 수 < dowamlylyk_baha; 수++) {
            int baha = nyşan_baha_068c2631[수];
            if (!(baha >= 'a' && baha <= 'z') && !(baha >= 'A' && baha <= 'Z')
                && !(baha >= '0' && baha <= '9') && baha != '_' && baha != '-' && baha != '.') return false;
        }
        return nyşan_baha_068c2631[0] != '.';
    }

    static int tap_girizmeklik(int[] nyşan_baha_068c2631, int dowamlylyk_baha) {
        if (!derňe_at(nyşan_baha_068c2631, dowamlylyk_baha)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + dowamlylyk_baha] == 0;
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < dowamlylyk_baha; ýer_girizmeklik++) if (이름들[수 * 64 + ýer_girizmeklik] != nyşan_baha_068c2631[ýer_girizmeklik]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_baha(int[] nyşan_baha_068c2631, int dowamlylyk_baha, int[] maglumat, int Ululyk) {
        if (!derňe_at(nyşan_baha_068c2631, dowamlylyk_baha) || Ululyk < 0 || Ululyk > maglumat.length) return -22;
        if (Ululyk > 최대크기) return -90;
        int indeks = tap_girizmeklik(nyşan_baha_068c2631, dowamlylyk_baha);
        if (indeks == -2) {
            for (int 수 = 0; 수 < 8 && indeks < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) indeks = 수;
            if (indeks >= 0) 허가들[indeks] = 438;
        }
        if (indeks < 0) return -28;
        int salgy = enjam_baha.faýl_ýat() + indeks * 최대크기;
        for (int 수 = 0; 수 < Ululyk; 수++) enjam_baha.ýaz_ýat(salgy + 수, maglumat[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[indeks * 64 + 수] = 수 < dowamlylyk_baha ? nyşan_baha_068c2631[수] : 0;
        ölçegi_üýtget_Sanaw[indeks] = Ululyk;
        return Ululyk;
    }

    static void girizmeklik_Sanaw() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 64 && 이름들[수 * 64 + ýer_girizmeklik] != 0; ýer_girizmeklik++) 문자단말.문자(이름들[수 * 64 + ýer_girizmeklik]);
            문자단말.Ýaz("  "); 문자단말.수쓰기(ölçegi_üýtget_Sanaw[수]); 문자단말.Ýaz("baýt_baha\n");
        }
        문자단말.Ýaz(Ammar_enjam_birikme.사용가능 ? "Faýl 8칸, 파일당 16384바이트; sync로 Store_baha 장치에 보존\n"
            : "임시 Faýl 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void buýruk(int[] 입력, int Bitir, int dowamlylyk_baha, int iş) {
        while (Bitir < dowamlylyk_baha && 입력[Bitir] == ' ') Bitir++;
        int 끝 = dowamlylyk_baha;
        while (끝 > Bitir && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Bitir;
        if (수 < 1 || 수 > 63) { 문자단말.Ýaz("올바르지 않은 Faýl Ad\n"); return; }
        for (int ýer_girizmeklik = 0; ýer_girizmeklik < 64; ýer_girizmeklik++) Ad[ýer_girizmeklik] = ýer_girizmeklik < 수 ? 입력[Bitir + ýer_girizmeklik] : 0;
        int indeks = tap_girizmeklik(Ad, 수);
        if (indeks == -22) { 문자단말.Ýaz("올바르지 않은 Faýl Ad\n"); return; }
        if (iş == 0) {
            편집중 = true; redaktirle_ölçegi_üýtget = 0; gyrmalanma_baha = false;
            문자단말.Ýaz("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (indeks < 0) 문자단말.Ýaz("파일을 찾을 수 없습니다\n");
        else if (iş == 1) {
            int salgy = enjam_baha.faýl_ýat() + indeks * 최대크기;
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < ölçegi_üýtget_Sanaw[indeks]; ýer_girizmeklik++) 문자단말.문자(enjam_baha.기억읽기(salgy + ýer_girizmeklik));
            문자단말.문자(10);
        } else { 이름들[indeks * 64] = 0; ölçegi_üýtget_Sanaw[indeks] = 0; 문자단말.Ýaz("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int dowamlylyk_baha, String 문구) {
        if (dowamlylyk_baha != 문구.length()) return false;
        for (int ýer_girizmeklik = 0; ýer_girizmeklik < dowamlylyk_baha; ýer_girizmeklik++) if (입력[ýer_girizmeklik] != 문구.charAt(ýer_girizmeklik)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int dowamlylyk_baha, boolean setir_gyrmalanma) {
        if (정확(입력, dowamlylyk_baha, ".cancel")) {
            편집중 = false; 문자단말.Ýaz("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, dowamlylyk_baha, ".save")) {
            편집중 = false;
            if (gyrmalanma_baha) { 문자단말.Ýaz("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Ad[수] != 0) 수++;
            int 결과 = Store_baha(Ad, 수, redaktirle_baha, redaktirle_ölçegi_üýtget);
            문자단말.Ýaz(결과 >= 0 ? "보존한 baýt_baha 수: " : "보존 näsazlyk_baha: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (setir_gyrmalanma || dowamlylyk_baha + 1 > 최대크기 - redaktirle_ölçegi_üýtget) gyrmalanma_baha = true;
        else {
            for (int 수 = 0; 수 < dowamlylyk_baha; 수++) redaktirle_baha[redaktirle_ölçegi_üýtget++] = 입력[수];
            redaktirle_baha[redaktirle_ölçegi_üýtget++] = 10;
        }
    }

    static void 예제(String Faýl, String Mazmun_baha) {
        for (int 수 = 0; 수 < 64; 수++) Ad[수] = 수 < Faýl.length() ? Faýl.charAt(수) : 0;
        for (int 수 = 0; 수 < Mazmun_baha.length(); 수++) redaktirle_baha[수] = Mazmun_baha.charAt(수);
        Store_baha(Ad, Faýl.length(), redaktirle_baha, Mazmun_baha.length());
    }

    static void Taýýarla() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int topar_baha = enjam_baha.자바파일묶음(), Ululyk = enjam_baha.자바파일묶음크기();
        if (Ululyk < 8 || 실행관리.수(topar_baha) != 0x464a4b4a) { 문자단말.Ýaz("올바르지 않은 Java Faýl topar_baha\n"); return; }
        int 개수 = 실행관리.수(topar_baha + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Ululyk - 8) / 72) { 문자단말.Ýaz("올바르지 않은 Java Faýl girizmeklik_Sanaw\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int girizmeklik_baha = topar_baha + 8 + 수 * 72, dowamlylyk_baha = 0;
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < 64; ýer_girizmeklik++) Ad[ýer_girizmeklik] = enjam_baha.기억읽기(girizmeklik_baha + ýer_girizmeklik);
            while (dowamlylyk_baha < 64 && Ad[dowamlylyk_baha] != 0) dowamlylyk_baha++;
            int 위치 = 실행관리.수(girizmeklik_baha + 64), faýl_ölçegi_üýtget = 실행관리.수(girizmeklik_baha + 68);
            if (!derňe_at(Ad, dowamlylyk_baha) || faýl_ölçegi_üýtget < 0 || faýl_ölçegi_üýtget > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Ululyk - faýl_ölçegi_üýtget) {
                문자단말.Ýaz("올바르지 않은 Java Faýl girizmeklik_baha\n"); return;
            }
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < faýl_ölçegi_üýtget; ýer_girizmeklik++) redaktirle_baha[ýer_girizmeklik] = enjam_baha.기억읽기(topar_baha + 위치 + ýer_girizmeklik);
            if (Store_baha(Ad, dowamlylyk_baha, redaktirle_baha, faýl_ölçegi_üýtget) < 0) { 문자단말.Ýaz("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
