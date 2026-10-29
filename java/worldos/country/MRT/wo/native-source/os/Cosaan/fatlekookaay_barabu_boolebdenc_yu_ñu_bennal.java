// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 bara_denc. 원본 soppi_xëyma/tabax_Cosaan foo_xëyma 시 기존 파일을 보존한다. */
public final class fatlekookaay_barabu_boolebdenc_yu_ñu_bennal {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] tolluwaay_lim = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] tur_253d1510 = new int[64];
    static int[] soppi_xëyma = new int[최대크기];
    static boolean 편집중 = false;
    static boolean luëppe_xëyma = false;
    static int soppi_tolluwaay = 0;

    static boolean sek_tur(int[] Araf_xëyma, int diir_xëyma) {
        if (diir_xëyma < 1 || diir_xëyma > 63) return false;
        for (int 수 = 0; 수 < diir_xëyma; 수++) {
            int xëyma = Araf_xëyma[수];
            if (!(xëyma >= 'a' && xëyma <= 'z') && !(xëyma >= 'A' && xëyma <= 'Z')
                && !(xëyma >= '0' && xëyma <= '9') && xëyma != '_' && xëyma != '-' && xëyma != '.') return false;
        }
        return Araf_xëyma[0] != '.';
    }

    static int seet_dugal_xabaar(int[] Araf_xëyma, int diir_xëyma) {
        if (!sek_tur(Araf_xëyma, diir_xëyma)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + diir_xëyma] == 0;
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < diir_xëyma; xar_xar_dugal_xabaar++) if (이름들[수 * 64 + xar_xar_dugal_xabaar] != Araf_xëyma[xar_xar_dugal_xabaar]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_xëyma(int[] Araf_xëyma, int diir_xëyma, int[] mbir, int tolluwaay) {
        if (!sek_tur(Araf_xëyma, diir_xëyma) || tolluwaay < 0 || tolluwaay > mbir.length) return -22;
        if (tolluwaay > 최대크기) return -90;
        int àlluwa_tur = seet_dugal_xabaar(Araf_xëyma, diir_xëyma);
        if (àlluwa_tur == -2) {
            for (int 수 = 0; 수 < 8 && àlluwa_tur < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) àlluwa_tur = 수;
            if (àlluwa_tur >= 0) 허가들[àlluwa_tur] = 438;
        }
        if (àlluwa_tur < 0) return -28;
        int dëkkuwaay = toftal_xëyma.bara_denc_fatlekookaay() + àlluwa_tur * 최대크기;
        for (int 수 = 0; 수 < tolluwaay; 수++) toftal_xëyma.biir_fatlekookaay(dëkkuwaay + 수, mbir[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[àlluwa_tur * 64 + 수] = 수 < diir_xëyma ? Araf_xëyma[수] : 0;
        tolluwaay_lim[àlluwa_tur] = tolluwaay;
        return tolluwaay;
    }

    static void dugal_xabaar_lim() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 64 && 이름들[수 * 64 + xar_xar_dugal_xabaar] != 0; xar_xar_dugal_xabaar++) 문자단말.문자(이름들[수 * 64 + xar_xar_dugal_xabaar]);
            문자단말.biir("  "); 문자단말.수쓰기(tolluwaay_lim[수]); 문자단말.biir("okte_xëyma\n");
        }
        문자단말.biir(Dencukaay_toftal_jokkalóo.사용가능 ? "bara_denc 8칸, 파일당 16384바이트; sync로 Store_xëyma 장치에 보존\n"
            : "임시 bara_denc 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void ndigel(int[] 입력, int daw, int diir_xëyma, int jëf) {
        while (daw < diir_xëyma && 입력[daw] == ' ') daw++;
        int 끝 = diir_xëyma;
        while (끝 > daw && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - daw;
        if (수 < 1 || 수 > 63) { 문자단말.biir("올바르지 않은 bara_denc tur_253d1510\n"); return; }
        for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 64; xar_xar_dugal_xabaar++) tur_253d1510[xar_xar_dugal_xabaar] = xar_xar_dugal_xabaar < 수 ? 입력[daw + xar_xar_dugal_xabaar] : 0;
        int àlluwa_tur = seet_dugal_xabaar(tur_253d1510, 수);
        if (àlluwa_tur == -22) { 문자단말.biir("올바르지 않은 bara_denc tur_253d1510\n"); return; }
        if (jëf == 0) {
            편집중 = true; soppi_tolluwaay = 0; luëppe_xëyma = false;
            문자단말.biir("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (àlluwa_tur < 0) 문자단말.biir("파일을 찾을 수 없습니다\n");
        else if (jëf == 1) {
            int dëkkuwaay = toftal_xëyma.bara_denc_fatlekookaay() + àlluwa_tur * 최대크기;
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < tolluwaay_lim[àlluwa_tur]; xar_xar_dugal_xabaar++) 문자단말.문자(toftal_xëyma.기억읽기(dëkkuwaay + xar_xar_dugal_xabaar));
            문자단말.문자(10);
        } else { 이름들[àlluwa_tur * 64] = 0; tolluwaay_lim[àlluwa_tur] = 0; 문자단말.biir("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int diir_xëyma, String 문구) {
        if (diir_xëyma != 문구.length()) return false;
        for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < diir_xëyma; xar_xar_dugal_xabaar++) if (입력[xar_xar_dugal_xabaar] != 문구.charAt(xar_xar_dugal_xabaar)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int diir_xëyma, boolean buum_luëppe) {
        if (정확(입력, diir_xëyma, ".cancel")) {
            편집중 = false; 문자단말.biir("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, diir_xëyma, ".save")) {
            편집중 = false;
            if (luëppe_xëyma) { 문자단말.biir("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && tur_253d1510[수] != 0) 수++;
            int 결과 = Store_xëyma(tur_253d1510, 수, soppi_xëyma, soppi_tolluwaay);
            문자단말.biir(결과 >= 0 ? "보존한 okte_xëyma 수: " : "보존 foo_xëyma: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (buum_luëppe || diir_xëyma + 1 > 최대크기 - soppi_tolluwaay) luëppe_xëyma = true;
        else {
            for (int 수 = 0; 수 < diir_xëyma; 수++) soppi_xëyma[soppi_tolluwaay++] = 입력[수];
            soppi_xëyma[soppi_tolluwaay++] = 10;
        }
    }

    static void 예제(String bara_denc, String Këmb_xëyma) {
        for (int 수 = 0; 수 < 64; 수++) tur_253d1510[수] = 수 < bara_denc.length() ? bara_denc.charAt(수) : 0;
        for (int 수 = 0; 수 < Këmb_xëyma.length(); 수++) soppi_xëyma[수] = Këmb_xëyma.charAt(수);
        Store_xëyma(tur_253d1510, bara_denc.length(), soppi_xëyma, Këmb_xëyma.length());
    }

    static void jël_matuwaay() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int mboolo_xëyma = toftal_xëyma.자바파일묶음(), tolluwaay = toftal_xëyma.자바파일묶음크기();
        if (tolluwaay < 8 || 실행관리.수(mboolo_xëyma) != 0x464a4b4a) { 문자단말.biir("올바르지 않은 Java bara_denc mboolo_xëyma\n"); return; }
        int 개수 = 실행관리.수(mboolo_xëyma + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (tolluwaay - 8) / 72) { 문자단말.biir("올바르지 않은 Java bara_denc dugal_xabaar_lim\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int dugal_xabaar_xëyma = mboolo_xëyma + 8 + 수 * 72, diir_xëyma = 0;
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 64; xar_xar_dugal_xabaar++) tur_253d1510[xar_xar_dugal_xabaar] = toftal_xëyma.기억읽기(dugal_xabaar_xëyma + xar_xar_dugal_xabaar);
            while (diir_xëyma < 64 && tur_253d1510[diir_xëyma] != 0) diir_xëyma++;
            int 위치 = 실행관리.수(dugal_xabaar_xëyma + 64), bara_denc_tolluwaay = 실행관리.수(dugal_xabaar_xëyma + 68);
            if (!sek_tur(tur_253d1510, diir_xëyma) || bara_denc_tolluwaay < 0 || bara_denc_tolluwaay > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > tolluwaay - bara_denc_tolluwaay) {
                문자단말.biir("올바르지 않은 Java bara_denc dugal_xabaar_xëyma\n"); return;
            }
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < bara_denc_tolluwaay; xar_xar_dugal_xabaar++) soppi_xëyma[xar_xar_dugal_xabaar] = toftal_xëyma.기억읽기(mboolo_xëyma + 위치 + xar_xar_dugal_xabaar);
            if (Store_xëyma(tur_253d1510, diir_xëyma, soppi_xëyma, bara_denc_tolluwaay) < 0) { 문자단말.biir("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
