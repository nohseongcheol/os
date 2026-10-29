// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Kōnae. 원본 whakatika_uara/hanga_pūtake rahunga_uara 시 기존 파일을 보존한다. */
public final class Pūmahara_pūnaha_kōnae {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] rahi_Rārangi = new int[8];
    static int[] tiwhikete_COUNT = new int[8], 허가들 = new int[8];
    static int[] Ingoa = new int[64];
    static int[] whakatika_uara = new int[최대크기];
    static boolean 편집중 = false;
    static boolean waipuke_uara = false;
    static int whakatika_rahi = 0;

    static boolean taki_ingoa(int[] pūāhua_uara, int roa_uara) {
        if (roa_uara < 1 || roa_uara > 63) return false;
        for (int 수 = 0; 수 < roa_uara; 수++) {
            int uara = pūāhua_uara[수];
            if (!(uara >= 'a' && uara <= 'z') && !(uara >= 'A' && uara <= 'Z')
                && !(uara >= '0' && uara <= '9') && uara != '_' && uara != '-' && uara != '.') return false;
        }
        return pūāhua_uara[0] != '.';
    }

    static int FIND_tāurunga(int[] pūāhua_uara, int roa_uara) {
        if (!taki_ingoa(pūāhua_uara, roa_uara)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + roa_uara] == 0;
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < roa_uara; kāniwha_tāurunga++) if (이름들[수 * 64 + kāniwha_tāurunga] != pūāhua_uara[kāniwha_tāurunga]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_uara(int[] pūāhua_uara, int roa_uara, int[] raraunga, int rahi) {
        if (!taki_ingoa(pūāhua_uara, roa_uara) || rahi < 0 || rahi > raraunga.length) return -22;
        if (rahi > 최대크기) return -90;
        int INDEX = FIND_tāurunga(pūāhua_uara, roa_uara);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && tiwhikete_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = pūkoro_uara.kōnae_Pūmahara() + INDEX * 최대크기;
        for (int 수 = 0; 수 < rahi; 수++) pūkoro_uara.tuhi_Pūmahara(ADDRESS + 수, raraunga[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < roa_uara ? pūāhua_uara[수] : 0;
        rahi_Rārangi[INDEX] = rahi;
        return rahi;
    }

    static void tāurunga_Rārangi() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 64 && 이름들[수 * 64 + kāniwha_tāurunga] != 0; kāniwha_tāurunga++) TEXT_Tauranga.문자(이름들[수 * 64 + kāniwha_tāurunga]);
            TEXT_Tauranga.Tuhia("  "); TEXT_Tauranga.수쓰기(rahi_Rārangi[수]); TEXT_Tauranga.Tuhia("paita_uara\n");
        }
        TEXT_Tauranga.Tuhia(Rokiroki_pūkoro_hononga.사용가능 ? "Kōnae 8칸, 파일당 16384바이트; sync로 Store_uara 장치에 보존\n"
            : "임시 Kōnae 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void tono(int[] 입력, int whakahaere, int roa_uara, int hohenga) {
        while (whakahaere < roa_uara && 입력[whakahaere] == ' ') whakahaere++;
        int 끝 = roa_uara;
        while (끝 > whakahaere && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - whakahaere;
        if (수 < 1 || 수 > 63) { TEXT_Tauranga.Tuhia("올바르지 않은 Kōnae Ingoa\n"); return; }
        for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 64; kāniwha_tāurunga++) Ingoa[kāniwha_tāurunga] = kāniwha_tāurunga < 수 ? 입력[whakahaere + kāniwha_tāurunga] : 0;
        int INDEX = FIND_tāurunga(Ingoa, 수);
        if (INDEX == -22) { TEXT_Tauranga.Tuhia("올바르지 않은 Kōnae Ingoa\n"); return; }
        if (hohenga == 0) {
            편집중 = true; whakatika_rahi = 0; waipuke_uara = false;
            TEXT_Tauranga.Tuhia("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) TEXT_Tauranga.Tuhia("파일을 찾을 수 없습니다\n");
        else if (hohenga == 1) {
            int ADDRESS = pūkoro_uara.kōnae_Pūmahara() + INDEX * 최대크기;
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < rahi_Rārangi[INDEX]; kāniwha_tāurunga++) TEXT_Tauranga.문자(pūkoro_uara.기억읽기(ADDRESS + kāniwha_tāurunga));
            TEXT_Tauranga.문자(10);
        } else { 이름들[INDEX * 64] = 0; rahi_Rārangi[INDEX] = 0; TEXT_Tauranga.Tuhia("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int roa_uara, String 문구) {
        if (roa_uara != 문구.length()) return false;
        for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < roa_uara; kāniwha_tāurunga++) if (입력[kāniwha_tāurunga] != 문구.charAt(kāniwha_tāurunga)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int roa_uara, boolean hononga_waipuke) {
        if (정확(입력, roa_uara, ".cancel")) {
            편집중 = false; TEXT_Tauranga.Tuhia("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, roa_uara, ".save")) {
            편집중 = false;
            if (waipuke_uara) { TEXT_Tauranga.Tuhia("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Ingoa[수] != 0) 수++;
            int mēhua = Store_uara(Ingoa, 수, whakatika_uara, whakatika_rahi);
            TEXT_Tauranga.Tuhia(mēhua >= 0 ? "보존한 paita_uara 수: " : "보존 rahunga_uara: ");
            TEXT_Tauranga.수쓰기(mēhua); TEXT_Tauranga.문자(10);
        } else if (hononga_waipuke || roa_uara + 1 > 최대크기 - whakatika_rahi) waipuke_uara = true;
        else {
            for (int 수 = 0; 수 < roa_uara; 수++) whakatika_uara[whakatika_rahi++] = 입력[수];
            whakatika_uara[whakatika_rahi++] = 10;
        }
    }

    static void 예제(String Kōnae, String Ihirangi_uara) {
        for (int 수 = 0; 수 < 64; 수++) Ingoa[수] = 수 < Kōnae.length() ? Kōnae.charAt(수) : 0;
        for (int 수 = 0; 수 < Ihirangi_uara.length(); 수++) whakatika_uara[수] = Ihirangi_uara.charAt(수);
        Store_uara(Ingoa, Kōnae.length(), whakatika_uara, Ihirangi_uara.length());
    }

    static void Whakarite() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int rōpū_uara = pūkoro_uara.자바파일묶음(), rahi = pūkoro_uara.자바파일묶음크기();
        if (rahi < 8 || 실행관리.수(rōpū_uara) != 0x464a4b4a) { TEXT_Tauranga.Tuhia("올바르지 않은 Java Kōnae rōpū_uara\n"); return; }
        int tuemi_COUNT = 실행관리.수(rōpū_uara + 4);
        if (tuemi_COUNT < 0 || tuemi_COUNT > 8 || tuemi_COUNT > (rahi - 8) / 72) { TEXT_Tauranga.Tuhia("올바르지 않은 Java Kōnae tāurunga_Rārangi\n"); return; }
        for (int 수 = 0; 수 < tuemi_COUNT; 수++) {
            int tāurunga_uara = rōpū_uara + 8 + 수 * 72, roa_uara = 0;
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 64; kāniwha_tāurunga++) Ingoa[kāniwha_tāurunga] = pūkoro_uara.기억읽기(tāurunga_uara + kāniwha_tāurunga);
            while (roa_uara < 64 && Ingoa[roa_uara] != 0) roa_uara++;
            int tūranga = 실행관리.수(tāurunga_uara + 64), kōnae_rahi = 실행관리.수(tāurunga_uara + 68);
            if (!taki_ingoa(Ingoa, roa_uara) || kōnae_rahi < 0 || kōnae_rahi > 최대크기 || tūranga < 8 + tuemi_COUNT * 72 || tūranga > rahi - kōnae_rahi) {
                TEXT_Tauranga.Tuhia("올바르지 않은 Java Kōnae tāurunga_uara\n"); return;
            }
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < kōnae_rahi; kāniwha_tāurunga++) whakatika_uara[kāniwha_tāurunga] = pūkoro_uara.기억읽기(rōpū_uara + tūranga + kāniwha_tāurunga);
            if (Store_uara(Ingoa, roa_uara, whakatika_uara, kōnae_rahi) < 0) { TEXT_Tauranga.Tuhia("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
