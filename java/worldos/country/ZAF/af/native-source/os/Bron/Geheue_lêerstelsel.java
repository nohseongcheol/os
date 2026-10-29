// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Lêer. 원본 redigeer_VALUE/bou_bron faling_VALUE 시 기존 파일을 보존한다. */
public final class Geheue_lêerstelsel {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] verstel_Lys = new int[8];
    static int[] skep_COUNT = new int[8], 허가들 = new int[8];
    static int[] Naam = new int[64];
    static int[] redigeer_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean oorloop_VALUE = false;
    static int redigeer_verstel = 0;

    static boolean tjek_naam(int[] karakter_VALUE, int lengte_VALUE) {
        if (lengte_VALUE < 1 || lengte_VALUE > 63) return false;
        for (int 수 = 0; 수 < lengte_VALUE; 수++) {
            int VALUE = karakter_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return karakter_VALUE[0] != '.';
    }

    static int FIND_inskrywing(int[] karakter_VALUE, int lengte_VALUE) {
        if (!tjek_naam(karakter_VALUE, lengte_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + lengte_VALUE] == 0;
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < lengte_VALUE; gleuf_inskrywing++) if (이름들[수 * 64 + gleuf_inskrywing] != karakter_VALUE[gleuf_inskrywing]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int bêre_VALUE(int[] karakter_VALUE, int lengte_VALUE, int[] data, int Grootte) {
        if (!tjek_naam(karakter_VALUE, lengte_VALUE) || Grootte < 0 || Grootte > data.length) return -22;
        if (Grootte > 최대크기) return -90;
        int INDEX = FIND_inskrywing(karakter_VALUE, lengte_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && skep_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int adres = mobiel_VALUE.lêer_Geheue() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Grootte; 수++) mobiel_VALUE.skryf_Geheue(adres + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < lengte_VALUE ? karakter_VALUE[수] : 0;
        verstel_Lys[INDEX] = Grootte;
        return Grootte;
    }

    static void inskrywing_Lys() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 64 && 이름들[수 * 64 + gleuf_inskrywing] != 0; gleuf_inskrywing++) SMS_Terminaal.문자(이름들[수 * 64 + gleuf_inskrywing]);
            SMS_Terminaal.Skryf("  "); SMS_Terminaal.수쓰기(verstel_Lys[수]); SMS_Terminaal.Skryf("greep_VALUE\n");
        }
        SMS_Terminaal.Skryf(Berging_mobiel_verbinding.사용가능 ? "Lêer 8칸, 파일당 16384바이트; sync로 bêre_VALUE 장치에 보존\n"
            : "임시 Lêer 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Opdrag(int[] 입력, int Loop, int lengte_VALUE, int Aksie) {
        while (Loop < lengte_VALUE && 입력[Loop] == ' ') Loop++;
        int 끝 = lengte_VALUE;
        while (끝 > Loop && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Loop;
        if (수 < 1 || 수 > 63) { SMS_Terminaal.Skryf("올바르지 않은 Lêer Naam\n"); return; }
        for (int gleuf_inskrywing = 0; gleuf_inskrywing < 64; gleuf_inskrywing++) Naam[gleuf_inskrywing] = gleuf_inskrywing < 수 ? 입력[Loop + gleuf_inskrywing] : 0;
        int INDEX = FIND_inskrywing(Naam, 수);
        if (INDEX == -22) { SMS_Terminaal.Skryf("올바르지 않은 Lêer Naam\n"); return; }
        if (Aksie == 0) {
            편집중 = true; redigeer_verstel = 0; oorloop_VALUE = false;
            SMS_Terminaal.Skryf("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminaal.Skryf("파일을 찾을 수 없습니다\n");
        else if (Aksie == 1) {
            int adres = mobiel_VALUE.lêer_Geheue() + INDEX * 최대크기;
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < verstel_Lys[INDEX]; gleuf_inskrywing++) SMS_Terminaal.문자(mobiel_VALUE.기억읽기(adres + gleuf_inskrywing));
            SMS_Terminaal.문자(10);
        } else { 이름들[INDEX * 64] = 0; verstel_Lys[INDEX] = 0; SMS_Terminaal.Skryf("파일을 지웠습니다\n"); }
    }

    static boolean 정확(int[] 입력, int lengte_VALUE, String 문구) {
        if (lengte_VALUE != 문구.length()) return false;
        for (int gleuf_inskrywing = 0; gleuf_inskrywing < lengte_VALUE; gleuf_inskrywing++) if (입력[gleuf_inskrywing] != 문구.charAt(gleuf_inskrywing)) return false;
        return true;
    }

    static void 편집줄(int[] 입력, int lengte_VALUE, boolean lyn_oorloop) {
        if (정확(입력, lengte_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminaal.Skryf("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (정확(입력, lengte_VALUE, ".save")) {
            편집중 = false;
            if (oorloop_VALUE) { SMS_Terminaal.Skryf("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Naam[수] != 0) 수++;
            int maatreël = bêre_VALUE(Naam, 수, redigeer_VALUE, redigeer_verstel);
            SMS_Terminaal.Skryf(maatreël >= 0 ? "보존한 greep_VALUE 수: " : "보존 faling_VALUE: ");
            SMS_Terminaal.수쓰기(maatreël); SMS_Terminaal.문자(10);
        } else if (lyn_oorloop || lengte_VALUE + 1 > 최대크기 - redigeer_verstel) oorloop_VALUE = true;
        else {
            for (int 수 = 0; 수 < lengte_VALUE; 수++) redigeer_VALUE[redigeer_verstel++] = 입력[수];
            redigeer_VALUE[redigeer_verstel++] = 10;
        }
    }

    static void 예제(String Lêer, String Inhoud_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Naam[수] = 수 < Lêer.length() ? Lêer.charAt(수) : 0;
        for (int 수 = 0; 수 < Inhoud_VALUE.length(); 수++) redigeer_VALUE[수] = Inhoud_VALUE.charAt(수);
        bêre_VALUE(Naam, Lêer.length(), redigeer_VALUE, Inhoud_VALUE.length());
    }

    static void Maak_gereed() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Groep_VALUE = mobiel_VALUE.자바파일묶음(), Grootte = mobiel_VALUE.자바파일묶음크기();
        if (Grootte < 8 || 실행관리.수(Groep_VALUE) != 0x464a4b4a) { SMS_Terminaal.Skryf("올바르지 않은 Java Lêer Groep_VALUE\n"); return; }
        int item_COUNT = 실행관리.수(Groep_VALUE + 4);
        if (item_COUNT < 0 || item_COUNT > 8 || item_COUNT > (Grootte - 8) / 72) { SMS_Terminaal.Skryf("올바르지 않은 Java Lêer inskrywing_Lys\n"); return; }
        for (int 수 = 0; 수 < item_COUNT; 수++) {
            int inskrywing_VALUE = Groep_VALUE + 8 + 수 * 72, lengte_VALUE = 0;
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < 64; gleuf_inskrywing++) Naam[gleuf_inskrywing] = mobiel_VALUE.기억읽기(inskrywing_VALUE + gleuf_inskrywing);
            while (lengte_VALUE < 64 && Naam[lengte_VALUE] != 0) lengte_VALUE++;
            int Posisie = 실행관리.수(inskrywing_VALUE + 64), lêer_verstel = 실행관리.수(inskrywing_VALUE + 68);
            if (!tjek_naam(Naam, lengte_VALUE) || lêer_verstel < 0 || lêer_verstel > 최대크기 || Posisie < 8 + item_COUNT * 72 || Posisie > Grootte - lêer_verstel) {
                SMS_Terminaal.Skryf("올바르지 않은 Java Lêer inskrywing_VALUE\n"); return;
            }
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < lêer_verstel; gleuf_inskrywing++) redigeer_VALUE[gleuf_inskrywing] = mobiel_VALUE.기억읽기(Groep_VALUE + Posisie + gleuf_inskrywing);
            if (bêre_VALUE(Naam, lengte_VALUE, redigeer_VALUE, lêer_verstel) < 0) { SMS_Terminaal.Skryf("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
