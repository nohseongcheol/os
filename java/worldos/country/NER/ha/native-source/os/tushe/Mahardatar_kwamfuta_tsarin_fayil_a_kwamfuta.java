// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fayil. 원본 gyaran_Daraja/Gina_tushe Kasa_aiki_Daraja 시 기존 파일을 보존한다. */
public final class Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] girma_Jeri = new int[8];
    static int[] 열림수 = new int[8], 허가들 = new int[8];
    static int[] Suna = new int[64];
    static int[] gyaran_Daraja = new int[최대크기];
    static boolean 편집중 = false;
    static boolean Mamayar_bayanai_Daraja = false;
    static int gyaran_girma = 0;

    static boolean Bincika_Suna(int[] Harafi_Daraja, int Tsawo_Daraja) {
        if (Tsawo_Daraja < 1 || Tsawo_Daraja > 63) return false;
        for (int 수 = 0; 수 < Tsawo_Daraja; 수++) {
            int Daraja = Harafi_Daraja[수];
            if (!(Daraja >= 'a' && Daraja <= 'z') && !(Daraja >= 'A' && Daraja <= 'Z')
                && !(Daraja >= '0' && Daraja <= '9') && Daraja != '_' && Daraja != '-' && Daraja != '.') return false;
        }
        return Harafi_Daraja[0] != '.';
    }

    static int nema_Mashigar_bayanai(int[] Harafi_Daraja, int Tsawo_Daraja) {
        if (!Bincika_Suna(Harafi_Daraja, Tsawo_Daraja)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + Tsawo_Daraja] == 0;
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < Tsawo_Daraja; rami_Mashigar_bayanai++) if (이름들[수 * 64 + rami_Mashigar_bayanai] != Harafi_Daraja[rami_Mashigar_bayanai]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Ajiye_Daraja(int[] Harafi_Daraja, int Tsawo_Daraja, int[] Tarin_bayani, int Girma) {
        if (!Bincika_Suna(Harafi_Daraja, Tsawo_Daraja) || Girma < 0 || Girma > Tarin_bayani.length) return -22;
        if (Girma > 최대크기) return -90;
        int Indes = nema_Mashigar_bayanai(Harafi_Daraja, Tsawo_Daraja);
        if (Indes == -2) {
            for (int 수 = 0; 수 < 8 && Indes < 0; 수++) if (이름들[수 * 64] == 0 && 열림수[수] == 0) Indes = 수;
            if (Indes >= 0) 허가들[Indes] = 438;
        }
        if (Indes < 0) return -28;
        int imel = na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Indes * 최대크기;
        for (int 수 = 0; 수 < Girma; 수++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(imel + 수, Tarin_bayani[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[Indes * 64 + 수] = 수 < Tsawo_Daraja ? Harafi_Daraja[수] : 0;
        girma_Jeri[Indes] = Girma;
        return Girma;
    }

    static void Mashigar_bayanai_Jeri() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 64 && 이름들[수 * 64 + rami_Mashigar_bayanai] != 0; rami_Mashigar_bayanai++) 문자단말.문자(이름들[수 * 64 + rami_Mashigar_bayanai]);
            문자단말.Yi_Rubutu("  "); 문자단말.수쓰기(girma_Jeri[수]); 문자단말.Yi_Rubutu("bayit_Daraja\n");
        }
        문자단말.Yi_Rubutu(Wurin_adana_na_ura_haɗi.kimiyar_bayanai_Aiki_9e72441a ? "Fayil 8칸, 파일당 16384바이트; sync로 Ajiye_Daraja 장치에 보존\n"
            : "임시 Fayil 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Umarni(int[] 입력, int Tafiyar_da, int Tsawo_Daraja, int Aiki) {
        while (Tafiyar_da < Tsawo_Daraja && 입력[Tafiyar_da] == ' ') Tafiyar_da++;
        int 끝 = Tsawo_Daraja;
        while (끝 > Tafiyar_da && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Tafiyar_da;
        if (수 < 1 || 수 > 63) { 문자단말.Yi_Rubutu("올바르지 않은 Fayil Suna\n"); return; }
        for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 64; rami_Mashigar_bayanai++) Suna[rami_Mashigar_bayanai] = rami_Mashigar_bayanai < 수 ? 입력[Tafiyar_da + rami_Mashigar_bayanai] : 0;
        int Indes = nema_Mashigar_bayanai(Suna, 수);
        if (Indes == -22) { 문자단말.Yi_Rubutu("올바르지 않은 Fayil Suna\n"); return; }
        if (Aiki == 0) {
            편집중 = true; gyaran_girma = 0; Mamayar_bayanai_Daraja = false;
            문자단말.Yi_Rubutu("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (Indes < 0) 문자단말.Yi_Rubutu("파일을 찾을 수 없습니다\n");
        else if (Aiki == 1) {
            int imel = na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Indes * 최대크기;
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < girma_Jeri[Indes]; rami_Mashigar_bayanai++) 문자단말.문자(na_ura_Daraja.기억읽기(imel + rami_Mashigar_bayanai));
            문자단말.문자(10);
        } else { 이름들[Indes * 64] = 0; girma_Jeri[Indes] = 0; 문자단말.Yi_Rubutu("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int Tsawo_Daraja, String 문구) {
        if (Tsawo_Daraja != 문구.length()) return false;
        for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < Tsawo_Daraja; rami_Mashigar_bayanai++) if (입력[rami_Mashigar_bayanai] != 문구.charAt(rami_Mashigar_bayanai)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int Tsawo_Daraja, boolean Layi_Mamayar_bayanai) {
        if (정확(입력, Tsawo_Daraja, ".cancel")) {
            편집중 = false; 문자단말.Yi_Rubutu("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, Tsawo_Daraja, ".save")) {
            편집중 = false;
            if (Mamayar_bayanai_Daraja) { 문자단말.Yi_Rubutu("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Suna[수] != 0) 수++;
            int 결과 = Ajiye_Daraja(Suna, 수, gyaran_Daraja, gyaran_girma);
            문자단말.Yi_Rubutu(결과 >= 0 ? "보존한 bayit_Daraja 수: " : "보존 Kasa_aiki_Daraja: ");
            문자단말.수쓰기(결과); 문자단말.문자(10);
        } else if (Layi_Mamayar_bayanai || Tsawo_Daraja + 1 > 최대크기 - gyaran_girma) Mamayar_bayanai_Daraja = true;
        else {
            for (int 수 = 0; 수 < Tsawo_Daraja; 수++) gyaran_Daraja[gyaran_girma++] = 입력[수];
            gyaran_Daraja[gyaran_girma++] = 10;
        }
    }

    static void 예제(String Fayil, String kunshiya_Daraja) {
        for (int 수 = 0; 수 < 64; 수++) Suna[수] = 수 < Fayil.length() ? Fayil.charAt(수) : 0;
        for (int 수 = 0; 수 < kunshiya_Daraja.length(); 수++) gyaran_Daraja[수] = kunshiya_Daraja.charAt(수);
        Ajiye_Daraja(Suna, Fayil.length(), gyaran_Daraja, kunshiya_Daraja.length());
    }

    static void Shirya() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int gungu_Daraja = na_ura_Daraja.자바파일묶음(), Girma = na_ura_Daraja.자바파일묶음크기();
        if (Girma < 8 || 실행관리.수(gungu_Daraja) != 0x464a4b4a) { 문자단말.Yi_Rubutu("올바르지 않은 Java Fayil gungu_Daraja\n"); return; }
        int 개수 = 실행관리.수(gungu_Daraja + 4);
        if (개수 < 0 || 개수 > 8 || 개수 > (Girma - 8) / 72) { 문자단말.Yi_Rubutu("올바르지 않은 Java Fayil Mashigar_bayanai_Jeri\n"); return; }
        for (int 수 = 0; 수 < 개수; 수++) {
            int Mashigar_bayanai_Daraja = gungu_Daraja + 8 + 수 * 72, Tsawo_Daraja = 0;
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 64; rami_Mashigar_bayanai++) Suna[rami_Mashigar_bayanai] = na_ura_Daraja.기억읽기(Mashigar_bayanai_Daraja + rami_Mashigar_bayanai);
            while (Tsawo_Daraja < 64 && Suna[Tsawo_Daraja] != 0) Tsawo_Daraja++;
            int 위치 = 실행관리.수(Mashigar_bayanai_Daraja + 64), Fayil_girma = 실행관리.수(Mashigar_bayanai_Daraja + 68);
            if (!Bincika_Suna(Suna, Tsawo_Daraja) || Fayil_girma < 0 || Fayil_girma > 최대크기 || 위치 < 8 + 개수 * 72 || 위치 > Girma - Fayil_girma) {
                문자단말.Yi_Rubutu("올바르지 않은 Java Fayil Mashigar_bayanai_Daraja\n"); return;
            }
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < Fayil_girma; rami_Mashigar_bayanai++) gyaran_Daraja[rami_Mashigar_bayanai] = na_ura_Daraja.기억읽기(gungu_Daraja + 위치 + rami_Mashigar_bayanai);
            if (Ajiye_Daraja(Suna, Tsawo_Daraja, gyaran_Daraja, Fayil_girma) < 0) { 문자단말.Yi_Rubutu("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
