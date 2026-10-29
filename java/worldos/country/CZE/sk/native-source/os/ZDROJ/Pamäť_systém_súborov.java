// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Súbor. 원본 úprava_VALUE/kompilovať_zdroj zlyhanie_VALUE 시 기존 파일을 보존한다. */
public final class Pamäť_systém_súborov {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] zmeniť_veľkosť_Zoznam = new int[8];
    static int[] otvoriť_COUNT = new int[8], 허가들 = new int[8];
    static int[] Názov = new int[64];
    static int[] úprava_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean pretečenie_VALUE = false;
    static int úprava_zmeniť_veľkosť = 0;

    static boolean skontrolovať_názov(int[] znak_VALUE, int dĺžka_VALUE) {
        if (dĺžka_VALUE < 1 || dĺžka_VALUE > 63) return false;
        for (int 수 = 0; 수 < dĺžka_VALUE; 수++) {
            int VALUE = znak_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return znak_VALUE[0] != '.';
    }

    static int FIND_položka(int[] znak_VALUE, int dĺžka_VALUE) {
        if (!skontrolovať_názov(znak_VALUE, dĺžka_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + dĺžka_VALUE] == 0;
            for (int 칸 = 0; 칸 < dĺžka_VALUE; 칸++) if (이름들[수 * 64 + 칸] != znak_VALUE[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] znak_VALUE, int dĺžka_VALUE, int[] údaje, int Veľkosť) {
        if (!skontrolovať_názov(znak_VALUE, dĺžka_VALUE) || Veľkosť < 0 || Veľkosť > údaje.length) return -22;
        if (Veľkosť > 최대크기) return -90;
        int INDEX = FIND_položka(znak_VALUE, dĺžka_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && otvoriť_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int adresa = telefón_VALUE.Súbor_Pamäť() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Veľkosť; 수++) telefón_VALUE.zapísať_Pamäť(adresa + 수, údaje[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < dĺžka_VALUE ? znak_VALUE[수] : 0;
        zmeniť_veľkosť_Zoznam[INDEX] = Veľkosť;
        return Veľkosť;
    }

    static void položka_Zoznam() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminál.문자(이름들[수 * 64 + 칸]);
            SMS_Terminál.Zápis("  "); SMS_Terminál.수쓰기(zmeniť_veľkosť_Zoznam[수]); SMS_Terminál.Zápis("Byte_VALUE\n");
        }
        SMS_Terminál.Zápis(úložné_zariadenie_kontakt.Informačné_systémy_Aktívny_9e72441a ? "Súbor 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Súbor 8칸, 파일당 16384바이트; skúsiť_znova_VALUE 시작하면 사라짐\n");
    }

    static void Príkaz(int[] vstup_VALUE, int Spustiť_2, int dĺžka_VALUE, int Akcia) {
        while (Spustiť_2 < dĺžka_VALUE && vstup_VALUE[Spustiť_2] == ' ') Spustiť_2++;
        int 끝 = dĺžka_VALUE;
        while (끝 > Spustiť_2 && vstup_VALUE[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Spustiť_2;
        if (수 < 1 || 수 > 63) { SMS_Terminál.Zápis("올바르지 않은 Súbor Názov\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Názov[칸] = 칸 < 수 ? vstup_VALUE[Spustiť_2 + 칸] : 0;
        int INDEX = FIND_položka(Názov, 수);
        if (INDEX == -22) { SMS_Terminál.Zápis("올바르지 않은 Súbor Názov\n"); return; }
        if (Akcia == 0) {
            편집중 = true; úprava_zmeniť_veľkosť = 0; pretečenie_VALUE = false;
            SMS_Terminál.Zápis("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminál.Zápis("파일을 찾을 수 없습니다\n");
        else if (Akcia == 1) {
            int adresa = telefón_VALUE.Súbor_Pamäť() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < zmeniť_veľkosť_Zoznam[INDEX]; 칸++) SMS_Terminál.문자(telefón_VALUE.기억읽기(adresa + 칸));
            SMS_Terminál.문자(10);
        } else { 이름들[INDEX * 64] = 0; zmeniť_veľkosť_Zoznam[INDEX] = 0; SMS_Terminál.Zápis("파일을 지웠습니다\n"); }
    }

    static boolean Informačné_systémy_EXACT(int[] vstup_VALUE, int dĺžka_VALUE, String 문구) {
        if (dĺžka_VALUE != 문구.length()) return false;
        for (int 칸 = 0; 칸 < dĺžka_VALUE; 칸++) if (vstup_VALUE[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Upravené_linka(int[] vstup_VALUE, int dĺžka_VALUE, boolean linka_pretečenie) {
        if (Informačné_systémy_EXACT(vstup_VALUE, dĺžka_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminál.Zápis("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (Informačné_systémy_EXACT(vstup_VALUE, dĺžka_VALUE, ".save")) {
            편집중 = false;
            if (pretečenie_VALUE) { SMS_Terminál.Zápis("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Názov[수] != 0) 수++;
            int KR = Store_VALUE(Názov, 수, úprava_VALUE, úprava_zmeniť_veľkosť);
            SMS_Terminál.Zápis(KR >= 0 ? "보존한 Byte_VALUE 수: " : "보존 zlyhanie_VALUE: ");
            SMS_Terminál.수쓰기(KR); SMS_Terminál.문자(10);
        } else if (linka_pretečenie || dĺžka_VALUE + 1 > 최대크기 - úprava_zmeniť_veľkosť) pretečenie_VALUE = true;
        else {
            for (int 수 = 0; 수 < dĺžka_VALUE; 수++) úprava_VALUE[úprava_zmeniť_veľkosť++] = vstup_VALUE[수];
            úprava_VALUE[úprava_zmeniť_veľkosť++] = 10;
        }
    }

    static void 예제(String Súbor, String obsah_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Názov[수] = 수 < Súbor.length() ? Súbor.charAt(수) : 0;
        for (int 수 = 0; 수 < obsah_VALUE.length(); 수++) úprava_VALUE[수] = obsah_VALUE.charAt(수);
        Store_VALUE(Názov, Súbor.length(), úprava_VALUE, obsah_VALUE.length());
    }

    static void Pripraviť() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Skupina_VALUE = telefón_VALUE.자바파일묶음(), Veľkosť = telefón_VALUE.자바파일묶음크기();
        if (Veľkosť < 8 || 실행관리.수(Skupina_VALUE) != 0x464a4b4a) { SMS_Terminál.Zápis("올바르지 않은 Java Súbor Skupina_VALUE\n"); return; }
        int položka_COUNT = 실행관리.수(Skupina_VALUE + 4);
        if (položka_COUNT < 0 || položka_COUNT > 8 || položka_COUNT > (Veľkosť - 8) / 72) { SMS_Terminál.Zápis("올바르지 않은 Java Súbor položka_Zoznam\n"); return; }
        for (int 수 = 0; 수 < položka_COUNT; 수++) {
            int položka_VALUE = Skupina_VALUE + 8 + 수 * 72, dĺžka_VALUE = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Názov[칸] = telefón_VALUE.기억읽기(položka_VALUE + 칸);
            while (dĺžka_VALUE < 64 && Názov[dĺžka_VALUE] != 0) dĺžka_VALUE++;
            int Pozícia = 실행관리.수(položka_VALUE + 64), veľkosť_súboru = 실행관리.수(položka_VALUE + 68);
            if (!skontrolovať_názov(Názov, dĺžka_VALUE) || veľkosť_súboru < 0 || veľkosť_súboru > 최대크기 || Pozícia < 8 + položka_COUNT * 72 || Pozícia > Veľkosť - veľkosť_súboru) {
                SMS_Terminál.Zápis("올바르지 않은 Java Súbor položka_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < veľkosť_súboru; 칸++) úprava_VALUE[칸] = telefón_VALUE.기억읽기(Skupina_VALUE + Pozícia + 칸);
            if (Store_VALUE(Názov, dĺžka_VALUE, úprava_VALUE, veľkosť_súboru) < 0) { SMS_Terminál.Zápis("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
