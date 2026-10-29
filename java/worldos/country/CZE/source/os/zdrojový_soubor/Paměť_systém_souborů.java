// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 název_souboru. 원본 úprava_HODNOTA/kompilovat_zdroj selhání_HODNOTA 시 기존 파일을 보존한다. */
public final class Paměť_systém_souborů {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] změnit_velikost_Seznam = new int[8];
    static int[] otevřít_POČET = new int[8], 허가들 = new int[8];
    static int[] Název = new int[64];
    static int[] úprava_HODNOTA = new int[최대크기];
    static boolean 편집중 = false;
    static boolean přetečení_HODNOTA = false;
    static int úprava_změnit_velikost = 0;

    static boolean šek_název(int[] znak_HODNOTA, int délka_HODNOTA) {
        if (délka_HODNOTA < 1 || délka_HODNOTA > 63) return false;
        for (int číslo = 0; číslo < délka_HODNOTA; číslo++) {
            int HODNOTA = znak_HODNOTA[číslo];
            if (!(HODNOTA >= 'a' && HODNOTA <= 'z') && !(HODNOTA >= 'A' && HODNOTA <= 'Z')
                && !(HODNOTA >= '0' && HODNOTA <= '9') && HODNOTA != '_' && HODNOTA != '-' && HODNOTA != '.') return false;
        }
        return znak_HODNOTA[0] != '.';
    }

    static int NAJÍT_položka(int[] znak_HODNOTA, int délka_HODNOTA) {
        if (!šek_název(znak_HODNOTA, délka_HODNOTA)) return -22;
        for (int číslo = 0; číslo < 8; číslo++) {
            boolean 같음 = 이름들[číslo * 64 + délka_HODNOTA] == 0;
            for (int přihrádka_položka = 0; přihrádka_položka < délka_HODNOTA; přihrádka_položka++) if (이름들[číslo * 64 + přihrádka_položka] != znak_HODNOTA[přihrádka_položka]) 같음 = false;
            if (같음) return číslo;
        }
        return -2;
    }

    static int Store_HODNOTA(int[] znak_HODNOTA, int délka_HODNOTA, int[] data, int Velikost) {
        if (!šek_název(znak_HODNOTA, délka_HODNOTA) || Velikost < 0 || Velikost > data.length) return -22;
        if (Velikost > 최대크기) return -90;
        int INDEX = NAJÍT_položka(znak_HODNOTA, délka_HODNOTA);
        if (INDEX == -2) {
            for (int číslo = 0; číslo < 8 && INDEX < 0; číslo++) if (이름들[číslo * 64] == 0 && otevřít_POČET[číslo] == 0) INDEX = číslo;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int Adresa = mobilní_HODNOTA.Soubor_Paměť() + INDEX * 최대크기;
        for (int číslo = 0; číslo < Velikost; číslo++) mobilní_HODNOTA.zápis_Paměť(Adresa + číslo, data[číslo]);
        for (int číslo = 0; číslo < 64; číslo++) 이름들[INDEX * 64 + číslo] = číslo < délka_HODNOTA ? znak_HODNOTA[číslo] : 0;
        změnit_velikost_Seznam[INDEX] = Velikost;
        return Velikost;
    }

    static void položka_Seznam() {
        for (int číslo = 0; číslo < 8; číslo++) if (이름들[číslo * 64] != 0) {
            for (int přihrádka_položka = 0; přihrádka_položka < 64 && 이름들[číslo * 64 + přihrádka_položka] != 0; přihrádka_položka++) SMS_Terminál.문자(이름들[číslo * 64 + přihrádka_položka]);
            SMS_Terminál.Zápis("  "); SMS_Terminál.zápis_číslo(změnit_velikost_Seznam[číslo]); SMS_Terminál.Zápis("bajt_HODNOTA\n");
        }
        SMS_Terminál.Zápis(úložiště_kontakt.informační_systémy_online ? "název_souboru 8칸, 파일당 16384바이트; sync로 Store_HODNOTA 장치에 보존\n"
            : "임시 název_souboru 8칸, 파일당 16384바이트; zkusit_znovu_HODNOTA 시작하면 사라짐\n");
    }

    static void příkaz(int[] vstup_HODNOTA, int Spustit_2, int délka_HODNOTA, int Akce) {
        while (Spustit_2 < délka_HODNOTA && vstup_HODNOTA[Spustit_2] == ' ') Spustit_2++;
        int 끝 = délka_HODNOTA;
        while (끝 > Spustit_2 && vstup_HODNOTA[끝 - 1] == ' ') 끝--;
        int číslo = 끝 - Spustit_2;
        if (číslo < 1 || číslo > 63) { SMS_Terminál.Zápis("올바르지 않은 název_souboru Název\n"); return; }
        for (int přihrádka_položka = 0; přihrádka_položka < 64; přihrádka_položka++) Název[přihrádka_položka] = přihrádka_položka < číslo ? vstup_HODNOTA[Spustit_2 + přihrádka_položka] : 0;
        int INDEX = NAJÍT_položka(Název, číslo);
        if (INDEX == -22) { SMS_Terminál.Zápis("올바르지 않은 název_souboru Název\n"); return; }
        if (Akce == 0) {
            편집중 = true; úprava_změnit_velikost = 0; přetečení_HODNOTA = false;
            SMS_Terminál.Zápis("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminál.Zápis("파일을 찾을 číslo 없습니다\n");
        else if (Akce == 1) {
            int Adresa = mobilní_HODNOTA.Soubor_Paměť() + INDEX * 최대크기;
            for (int přihrádka_položka = 0; přihrádka_položka < změnit_velikost_Seznam[INDEX]; přihrádka_položka++) SMS_Terminál.문자(mobilní_HODNOTA.기억읽기(Adresa + přihrádka_položka));
            SMS_Terminál.문자(10);
        } else { 이름들[INDEX * 64] = 0; změnit_velikost_Seznam[INDEX] = 0; SMS_Terminál.Zápis("파일을 지웠습니다\n"); }
    }

    static boolean informační_systémy_STEJNÉ(int[] vstup_HODNOTA, int délka_HODNOTA, String 문구) {
        if (délka_HODNOTA != 문구.length()) return false;
        for (int přihrádka_položka = 0; přihrádka_položka < délka_HODNOTA; přihrádka_položka++) if (vstup_HODNOTA[přihrádka_položka] != 문구.charAt(přihrádka_položka)) return false;
        return true;
    }

    static void Upraveno_čára(int[] vstup_HODNOTA, int délka_HODNOTA, boolean čára_přetečení) {
        if (informační_systémy_STEJNÉ(vstup_HODNOTA, délka_HODNOTA, ".cancel")) {
            편집중 = false; SMS_Terminál.Zápis("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informační_systémy_STEJNÉ(vstup_HODNOTA, délka_HODNOTA, ".save")) {
            편집중 = false;
            if (přetečení_HODNOTA) { SMS_Terminál.Zápis("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int číslo = 0;
            while (číslo < 64 && Název[číslo] != 0) číslo++;
            int VÝSLEDEK = Store_HODNOTA(Název, číslo, úprava_HODNOTA, úprava_změnit_velikost);
            SMS_Terminál.Zápis(VÝSLEDEK >= 0 ? "보존한 bajt_HODNOTA číslo: " : "보존 selhání_HODNOTA: ");
            SMS_Terminál.zápis_číslo(VÝSLEDEK); SMS_Terminál.문자(10);
        } else if (čára_přetečení || délka_HODNOTA + 1 > 최대크기 - úprava_změnit_velikost) přetečení_HODNOTA = true;
        else {
            for (int číslo = 0; číslo < délka_HODNOTA; číslo++) úprava_HODNOTA[úprava_změnit_velikost++] = vstup_HODNOTA[číslo];
            úprava_HODNOTA[úprava_změnit_velikost++] = 10;
        }
    }

    static void 예제(String název_souboru, String Obsah_HODNOTA) {
        for (int číslo = 0; číslo < 64; číslo++) Název[číslo] = číslo < název_souboru.length() ? název_souboru.charAt(číslo) : 0;
        for (int číslo = 0; číslo < Obsah_HODNOTA.length(); číslo++) úprava_HODNOTA[číslo] = Obsah_HODNOTA.charAt(číslo);
        Store_HODNOTA(Název, název_souboru.length(), úprava_HODNOTA, Obsah_HODNOTA.length());
    }

    static void Připravit() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Skupina_HODNOTA = mobilní_HODNOTA.자바파일묶음(), Velikost = mobilní_HODNOTA.자바파일묶음크기();
        if (Velikost < 8 || spuštění_Správce.číslo(Skupina_HODNOTA) != 0x464a4b4a) { SMS_Terminál.Zápis("올바르지 않은 Java název_souboru Skupina_HODNOTA\n"); return; }
        int zboží_POČET = spuštění_Správce.číslo(Skupina_HODNOTA + 4);
        if (zboží_POČET < 0 || zboží_POČET > 8 || zboží_POČET > (Velikost - 8) / 72) { SMS_Terminál.Zápis("올바르지 않은 Java název_souboru položka_Seznam\n"); return; }
        for (int číslo = 0; číslo < zboží_POČET; číslo++) {
            int položka_HODNOTA = Skupina_HODNOTA + 8 + číslo * 72, délka_HODNOTA = 0;
            for (int přihrádka_položka = 0; přihrádka_položka < 64; přihrádka_položka++) Název[přihrádka_položka] = mobilní_HODNOTA.기억읽기(položka_HODNOTA + přihrádka_položka);
            while (délka_HODNOTA < 64 && Název[délka_HODNOTA] != 0) délka_HODNOTA++;
            int pozice = spuštění_Správce.číslo(položka_HODNOTA + 64), velikost_souboru = spuštění_Správce.číslo(položka_HODNOTA + 68);
            if (!šek_název(Název, délka_HODNOTA) || velikost_souboru < 0 || velikost_souboru > 최대크기 || pozice < 8 + zboží_POČET * 72 || pozice > Velikost - velikost_souboru) {
                SMS_Terminál.Zápis("올바르지 않은 Java název_souboru položka_HODNOTA\n"); return;
            }
            for (int přihrádka_položka = 0; přihrádka_položka < velikost_souboru; přihrádka_položka++) úprava_HODNOTA[přihrádka_položka] = mobilní_HODNOTA.기억읽기(Skupina_HODNOTA + pozice + přihrádka_položka);
            if (Store_HODNOTA(Název, délka_HODNOTA, úprava_HODNOTA, velikost_souboru) < 0) { SMS_Terminál.Zápis("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
