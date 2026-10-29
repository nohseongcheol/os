// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Datoteka. 원본 Uredi_VALUE/programski_prevesti_izvor kvar_VALUE 시 기존 파일을 보존한다. */
public final class Memorija_datotečni_sustav {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] promijeniti_veličinu_Popis = new int[8];
    static int[] otvoreno_COUNT = new int[8], 허가들 = new int[8];
    static int[] Ime = new int[64];
    static int[] Uredi_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean preljev_VALUE = false;
    static int Uredi_promijeniti_veličinu = 0;

    static boolean 이름검사(int[] znak_VALUE, int 길이) {
        if (길이 < 1 || 길이 > 63) return false;
        for (int 수 = 0; 수 < 길이; 수++) {
            int VALUE = znak_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return znak_VALUE[0] != '.';
    }

    static int FIND_unos(int[] znak_VALUE, int 길이) {
        if (!이름검사(znak_VALUE, 길이)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + 길이] == 0;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (이름들[수 * 64 + 칸] != znak_VALUE[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] znak_VALUE, int 길이, int[] podaci, int Veličina) {
        if (!이름검사(znak_VALUE, 길이) || Veličina < 0 || Veličina > podaci.length) return -22;
        if (Veličina > 최대크기) return -90;
        int INDEX = FIND_unos(znak_VALUE, 길이);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && otvoreno_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int adresa = uređaj_VALUE.Datoteka_Memorija() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Veličina; 수++) uređaj_VALUE.zapisivanje_Memorija(adresa + 수, podaci[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < 길이 ? znak_VALUE[수] : 0;
        promijeniti_veličinu_Popis[INDEX] = Veličina;
        return Veličina;
    }

    static void unos_Popis() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.Zapisuj("  "); SMS_Terminal.수쓰기(promijeniti_veličinu_Popis[수]); SMS_Terminal.Zapisuj("bajt_VALUE\n");
        }
        SMS_Terminal.Zapisuj(uređaj_za_pohranu_veza.odjel_informacijske_tehnologije_Aktivan_9e72441a ? "Datoteka 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Datoteka 8칸, 파일당 16384바이트; pokušati_ponovno_VALUE 시작하면 사라짐\n");
    }

    static void Naredba(int[] 입력, int Pokreni, int 길이, int Aktivnost) {
        while (Pokreni < 길이 && 입력[Pokreni] == ' ') Pokreni++;
        int 끝 = 길이;
        while (끝 > Pokreni && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Pokreni;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Zapisuj("올바르지 않은 Datoteka Ime\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Ime[칸] = 칸 < 수 ? 입력[Pokreni + 칸] : 0;
        int INDEX = FIND_unos(Ime, 수);
        if (INDEX == -22) { SMS_Terminal.Zapisuj("올바르지 않은 Datoteka Ime\n"); return; }
        if (Aktivnost == 0) {
            편집중 = true; Uredi_promijeniti_veličinu = 0; preljev_VALUE = false;
            SMS_Terminal.Zapisuj("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Zapisuj("파일을 찾을 수 없습니다\n");
        else if (Aktivnost == 1) {
            int adresa = uređaj_VALUE.Datoteka_Memorija() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < promijeniti_veličinu_Popis[INDEX]; 칸++) SMS_Terminal.문자(uređaj_VALUE.기억읽기(adresa + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; promijeniti_veličinu_Popis[INDEX] = 0; SMS_Terminal.Zapisuj("파일을 지웠습니다\n"); }
    }

    static boolean odjel_informacijske_tehnologije_EXACT(int[] 입력, int 길이, String 문구) {
        if (길이 != 문구.length()) return false;
        for (int 칸 = 0; 칸 < 길이; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Uređivano_red(int[] 입력, int 길이, boolean red_preljev) {
        if (odjel_informacijske_tehnologije_EXACT(입력, 길이, ".cancel")) {
            편집중 = false; SMS_Terminal.Zapisuj("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (odjel_informacijske_tehnologije_EXACT(입력, 길이, ".save")) {
            편집중 = false;
            if (preljev_VALUE) { SMS_Terminal.Zapisuj("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Ime[수] != 0) 수++;
            int REZULTAT = Store_VALUE(Ime, 수, Uredi_VALUE, Uredi_promijeniti_veličinu);
            SMS_Terminal.Zapisuj(REZULTAT >= 0 ? "보존한 bajt_VALUE 수: " : "보존 kvar_VALUE: ");
            SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.문자(10);
        } else if (red_preljev || 길이 + 1 > 최대크기 - Uredi_promijeniti_veličinu) preljev_VALUE = true;
        else {
            for (int 수 = 0; 수 < 길이; 수++) Uredi_VALUE[Uredi_promijeniti_veličinu++] = 입력[수];
            Uredi_VALUE[Uredi_promijeniti_veličinu++] = 10;
        }
    }

    static void 예제(String Datoteka, String Sadržaj_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Ime[수] = 수 < Datoteka.length() ? Datoteka.charAt(수) : 0;
        for (int 수 = 0; 수 < Sadržaj_VALUE.length(); 수++) Uredi_VALUE[수] = Sadržaj_VALUE.charAt(수);
        Store_VALUE(Ime, Datoteka.length(), Uredi_VALUE, Sadržaj_VALUE.length());
    }

    static void Pripremi() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupa_VALUE = uređaj_VALUE.자바파일묶음(), Veličina = uređaj_VALUE.자바파일묶음크기();
        if (Veličina < 8 || 실행관리.수(Grupa_VALUE) != 0x464a4b4a) { SMS_Terminal.Zapisuj("올바르지 않은 Java Datoteka Grupa_VALUE\n"); return; }
        int artikl_COUNT = 실행관리.수(Grupa_VALUE + 4);
        if (artikl_COUNT < 0 || artikl_COUNT > 8 || artikl_COUNT > (Veličina - 8) / 72) { SMS_Terminal.Zapisuj("올바르지 않은 Java Datoteka unos_Popis\n"); return; }
        for (int 수 = 0; 수 < artikl_COUNT; 수++) {
            int unos_VALUE = Grupa_VALUE + 8 + 수 * 72, 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Ime[칸] = uređaj_VALUE.기억읽기(unos_VALUE + 칸);
            while (길이 < 64 && Ime[길이] != 0) 길이++;
            int Položaj = 실행관리.수(unos_VALUE + 64), veličina_datoteke = 실행관리.수(unos_VALUE + 68);
            if (!이름검사(Ime, 길이) || veličina_datoteke < 0 || veličina_datoteke > 최대크기 || Položaj < 8 + artikl_COUNT * 72 || Položaj > Veličina - veličina_datoteke) {
                SMS_Terminal.Zapisuj("올바르지 않은 Java Datoteka unos_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < veličina_datoteke; 칸++) Uredi_VALUE[칸] = uređaj_VALUE.기억읽기(Grupa_VALUE + Položaj + 칸);
            if (Store_VALUE(Ime, 길이, Uredi_VALUE, veličina_datoteke) < 0) { SMS_Terminal.Zapisuj("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
