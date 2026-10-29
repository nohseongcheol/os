// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fil. 원본 redigere_VALUE/byggje_kjelde feil_VALUE 시 기존 파일을 보존한다. */
public final class Minne_filsystem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] endre_storleik_Liste = new int[8];
    static int[] opne_COUNT = new int[8], 허가들 = new int[8];
    static int[] Namn = new int[64];
    static int[] redigere_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean overflyt_VALUE = false;
    static int redigere_endre_storleik = 0;

    static boolean sjekk_namn(int[] teikn_VALUE, int lengd_VALUE) {
        if (lengd_VALUE < 1 || lengd_VALUE > 63) return false;
        for (int 수 = 0; 수 < lengd_VALUE; 수++) {
            int VALUE = teikn_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return teikn_VALUE[0] != '.';
    }

    static int Søk_oppføring(int[] teikn_VALUE, int lengd_VALUE) {
        if (!sjekk_namn(teikn_VALUE, lengd_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + lengd_VALUE] == 0;
            for (int felt_oppføring = 0; felt_oppføring < lengd_VALUE; felt_oppføring++) if (이름들[수 * 64 + felt_oppføring] != teikn_VALUE[felt_oppføring]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] teikn_VALUE, int lengd_VALUE, int[] data, int Storleik) {
        if (!sjekk_namn(teikn_VALUE, lengd_VALUE) || Storleik < 0 || Storleik > data.length) return -22;
        if (Storleik > 최대크기) return -90;
        int INDEX = Søk_oppføring(teikn_VALUE, lengd_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && opne_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int ADDRESS = mobil_VALUE.fil_Minne() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Storleik; 수++) mobil_VALUE.skrive_Minne(ADDRESS + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < lengd_VALUE ? teikn_VALUE[수] : 0;
        endre_storleik_Liste[INDEX] = Storleik;
        return Storleik;
    }

    static void oppføring_Liste() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int felt_oppføring = 0; felt_oppføring < 64 && 이름들[수 * 64 + felt_oppføring] != 0; felt_oppføring++) SMS_Terminal.문자(이름들[수 * 64 + felt_oppføring]);
            SMS_Terminal.Skriv("  "); SMS_Terminal.수쓰기(endre_storleik_Liste[수]); SMS_Terminal.Skriv("byte_VALUE\n");
        }
        SMS_Terminal.Skriv(Lagring_mobil_kontakt.informasjonsteknologi_barn ? "Fil 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Fil 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Kommando(int[] 입력, int Køyr_2, int lengd_VALUE, int Handling) {
        while (Køyr_2 < lengd_VALUE && 입력[Køyr_2] == ' ') Køyr_2++;
        int 끝 = lengd_VALUE;
        while (끝 > Køyr_2 && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Køyr_2;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Skriv("올바르지 않은 Fil Namn\n"); return; }
        for (int felt_oppføring = 0; felt_oppføring < 64; felt_oppføring++) Namn[felt_oppføring] = felt_oppføring < 수 ? 입력[Køyr_2 + felt_oppføring] : 0;
        int INDEX = Søk_oppføring(Namn, 수);
        if (INDEX == -22) { SMS_Terminal.Skriv("올바르지 않은 Fil Namn\n"); return; }
        if (Handling == 0) {
            편집중 = true; redigere_endre_storleik = 0; overflyt_VALUE = false;
            SMS_Terminal.Skriv("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Skriv("파일을 찾을 수 없습니다\n");
        else if (Handling == 1) {
            int ADDRESS = mobil_VALUE.fil_Minne() + INDEX * 최대크기;
            for (int felt_oppføring = 0; felt_oppføring < endre_storleik_Liste[INDEX]; felt_oppføring++) SMS_Terminal.문자(mobil_VALUE.기억읽기(ADDRESS + felt_oppføring));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; endre_storleik_Liste[INDEX] = 0; SMS_Terminal.Skriv("파일을 지웠습니다\n"); }
    }

    static boolean informasjonsteknologi_EXACT(int[] 입력, int lengd_VALUE, String 문구) {
        if (lengd_VALUE != 문구.length()) return false;
        for (int felt_oppføring = 0; felt_oppføring < lengd_VALUE; felt_oppføring++) if (입력[felt_oppføring] != 문구.charAt(felt_oppføring)) return false;
        return true;
    }

    static void Redigert_line(int[] 입력, int lengd_VALUE, boolean line_overflyt) {
        if (informasjonsteknologi_EXACT(입력, lengd_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.Skriv("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informasjonsteknologi_EXACT(입력, lengd_VALUE, ".save")) {
            편집중 = false;
            if (overflyt_VALUE) { SMS_Terminal.Skriv("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Namn[수] != 0) 수++;
            int forretningsmål = Store_VALUE(Namn, 수, redigere_VALUE, redigere_endre_storleik);
            SMS_Terminal.Skriv(forretningsmål >= 0 ? "보존한 byte_VALUE 수: " : "보존 feil_VALUE: ");
            SMS_Terminal.수쓰기(forretningsmål); SMS_Terminal.문자(10);
        } else if (line_overflyt || lengd_VALUE + 1 > 최대크기 - redigere_endre_storleik) overflyt_VALUE = true;
        else {
            for (int 수 = 0; 수 < lengd_VALUE; 수++) redigere_VALUE[redigere_endre_storleik++] = 입력[수];
            redigere_VALUE[redigere_endre_storleik++] = 10;
        }
    }

    static void 예제(String Fil, String Innhald_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Namn[수] = 수 < Fil.length() ? Fil.charAt(수) : 0;
        for (int 수 = 0; 수 < Innhald_VALUE.length(); 수++) redigere_VALUE[수] = Innhald_VALUE.charAt(수);
        Store_VALUE(Namn, Fil.length(), redigere_VALUE, Innhald_VALUE.length());
    }

    static void Klargjer() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int gruppe_VALUE = mobil_VALUE.자바파일묶음(), Storleik = mobil_VALUE.자바파일묶음크기();
        if (Storleik < 8 || 실행관리.수(gruppe_VALUE) != 0x464a4b4a) { SMS_Terminal.Skriv("올바르지 않은 Java Fil gruppe_VALUE\n"); return; }
        int vare_COUNT = 실행관리.수(gruppe_VALUE + 4);
        if (vare_COUNT < 0 || vare_COUNT > 8 || vare_COUNT > (Storleik - 8) / 72) { SMS_Terminal.Skriv("올바르지 않은 Java Fil oppføring_Liste\n"); return; }
        for (int 수 = 0; 수 < vare_COUNT; 수++) {
            int oppføring_VALUE = gruppe_VALUE + 8 + 수 * 72, lengd_VALUE = 0;
            for (int felt_oppføring = 0; felt_oppføring < 64; felt_oppføring++) Namn[felt_oppføring] = mobil_VALUE.기억읽기(oppføring_VALUE + felt_oppføring);
            while (lengd_VALUE < 64 && Namn[lengd_VALUE] != 0) lengd_VALUE++;
            int Posisjon = 실행관리.수(oppføring_VALUE + 64), fil_endre_storleik = 실행관리.수(oppføring_VALUE + 68);
            if (!sjekk_namn(Namn, lengd_VALUE) || fil_endre_storleik < 0 || fil_endre_storleik > 최대크기 || Posisjon < 8 + vare_COUNT * 72 || Posisjon > Storleik - fil_endre_storleik) {
                SMS_Terminal.Skriv("올바르지 않은 Java Fil oppføring_VALUE\n"); return;
            }
            for (int felt_oppføring = 0; felt_oppføring < fil_endre_storleik; felt_oppføring++) redigere_VALUE[felt_oppføring] = mobil_VALUE.기억읽기(gruppe_VALUE + Posisjon + felt_oppføring);
            if (Store_VALUE(Namn, lengd_VALUE, redigere_VALUE, fil_endre_storleik) < 0) { SMS_Terminal.Skriv("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
