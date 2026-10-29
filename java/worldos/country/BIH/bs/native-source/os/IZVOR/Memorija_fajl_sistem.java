// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fajl. 원본 uređivati_VALUE/napraviti_izvor neuspjeh_VALUE 시 기존 파일을 보존한다. */
public final class Memorija_fajl_sistem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] podesiti_veličinu_spisak = new int[8];
    static int[] kreirati_COUNT = new int[8], 허가들 = new int[8];
    static int[] Naziv = new int[64];
    static int[] uređivati_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean prelijevanje_VALUE = false;
    static int uređivati_podesiti_veličinu = 0;

    static boolean ček_naziv(int[] znak_VALUE, int dužina_VALUE) {
        if (dužina_VALUE < 1 || dužina_VALUE > 63) return false;
        for (int 수 = 0; 수 < dužina_VALUE; 수++) {
            int VALUE = znak_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return znak_VALUE[0] != '.';
    }

    static int FIND_unos(int[] znak_VALUE, int dužina_VALUE) {
        if (!ček_naziv(znak_VALUE, dužina_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + dužina_VALUE] == 0;
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < dužina_VALUE; prostor_za_unos_unos++) if (이름들[수 * 64 + prostor_za_unos_unos] != znak_VALUE[prostor_za_unos_unos]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] znak_VALUE, int dužina_VALUE, int[] podaci, int Veličina) {
        if (!ček_naziv(znak_VALUE, dužina_VALUE) || Veličina < 0 || Veličina > podaci.length) return -22;
        if (Veličina > 최대크기) return -90;
        int INDEX = FIND_unos(znak_VALUE, dužina_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && kreirati_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int adresa = uređaj_VALUE.fajl_Memorija() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Veličina; 수++) uređaj_VALUE.pisati_Memorija(adresa + 수, podaci[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < dužina_VALUE ? znak_VALUE[수] : 0;
        podesiti_veličinu_spisak[INDEX] = Veličina;
        return Veličina;
    }

    static void unos_spisak() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 64 && 이름들[수 * 64 + prostor_za_unos_unos] != 0; prostor_za_unos_unos++) SMS_Terminal.문자(이름들[수 * 64 + prostor_za_unos_unos]);
            SMS_Terminal.Piši("  "); SMS_Terminal.수쓰기(podesiti_veličinu_spisak[수]); SMS_Terminal.Piši("bajt_VALUE\n");
        }
        SMS_Terminal.Piši(Pohrana_uređaj_veza.odjel_za_informacijske_tehnologije_dostupan ? "Fajl 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Fajl 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Naredba(int[] 입력, int Pokreni, int dužina_VALUE, int radnja) {
        while (Pokreni < dužina_VALUE && 입력[Pokreni] == ' ') Pokreni++;
        int 끝 = dužina_VALUE;
        while (끝 > Pokreni && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Pokreni;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Piši("올바르지 않은 Fajl Naziv\n"); return; }
        for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 64; prostor_za_unos_unos++) Naziv[prostor_za_unos_unos] = prostor_za_unos_unos < 수 ? 입력[Pokreni + prostor_za_unos_unos] : 0;
        int INDEX = FIND_unos(Naziv, 수);
        if (INDEX == -22) { SMS_Terminal.Piši("올바르지 않은 Fajl Naziv\n"); return; }
        if (radnja == 0) {
            편집중 = true; uređivati_podesiti_veličinu = 0; prelijevanje_VALUE = false;
            SMS_Terminal.Piši("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Piši("파일을 찾을 수 없습니다\n");
        else if (radnja == 1) {
            int adresa = uređaj_VALUE.fajl_Memorija() + INDEX * 최대크기;
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < podesiti_veličinu_spisak[INDEX]; prostor_za_unos_unos++) SMS_Terminal.문자(uređaj_VALUE.기억읽기(adresa + prostor_za_unos_unos));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; podesiti_veličinu_spisak[INDEX] = 0; SMS_Terminal.Piši("파일을 지웠습니다\n"); }
    }

    static boolean odjel_za_informacijske_tehnologije_EXACT(int[] 입력, int dužina_VALUE, String 문구) {
        if (dužina_VALUE != 문구.length()) return false;
        for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < dužina_VALUE; prostor_za_unos_unos++) if (입력[prostor_za_unos_unos] != 문구.charAt(prostor_za_unos_unos)) return false;
        return true;
    }

    static void Uređivano_redak(int[] 입력, int dužina_VALUE, boolean redak_prelijevanje) {
        if (odjel_za_informacijske_tehnologije_EXACT(입력, dužina_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.Piši("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (odjel_za_informacijske_tehnologije_EXACT(입력, dužina_VALUE, ".save")) {
            편집중 = false;
            if (prelijevanje_VALUE) { SMS_Terminal.Piši("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Naziv[수] != 0) 수++;
            int mjera = Store_VALUE(Naziv, 수, uređivati_VALUE, uređivati_podesiti_veličinu);
            SMS_Terminal.Piši(mjera >= 0 ? "보존한 bajt_VALUE 수: " : "보존 neuspjeh_VALUE: ");
            SMS_Terminal.수쓰기(mjera); SMS_Terminal.문자(10);
        } else if (redak_prelijevanje || dužina_VALUE + 1 > 최대크기 - uređivati_podesiti_veličinu) prelijevanje_VALUE = true;
        else {
            for (int 수 = 0; 수 < dužina_VALUE; 수++) uređivati_VALUE[uređivati_podesiti_veličinu++] = 입력[수];
            uređivati_VALUE[uređivati_podesiti_veličinu++] = 10;
        }
    }

    static void 예제(String Fajl, String Sadržaj_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Naziv[수] = 수 < Fajl.length() ? Fajl.charAt(수) : 0;
        for (int 수 = 0; 수 < Sadržaj_VALUE.length(); 수++) uređivati_VALUE[수] = Sadržaj_VALUE.charAt(수);
        Store_VALUE(Naziv, Fajl.length(), uređivati_VALUE, Sadržaj_VALUE.length());
    }

    static void Pripremiti() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupa_VALUE = uređaj_VALUE.자바파일묶음(), Veličina = uređaj_VALUE.자바파일묶음크기();
        if (Veličina < 8 || 실행관리.수(Grupa_VALUE) != 0x464a4b4a) { SMS_Terminal.Piši("올바르지 않은 Java Fajl Grupa_VALUE\n"); return; }
        int stavka_COUNT = 실행관리.수(Grupa_VALUE + 4);
        if (stavka_COUNT < 0 || stavka_COUNT > 8 || stavka_COUNT > (Veličina - 8) / 72) { SMS_Terminal.Piši("올바르지 않은 Java Fajl unos_spisak\n"); return; }
        for (int 수 = 0; 수 < stavka_COUNT; 수++) {
            int unos_VALUE = Grupa_VALUE + 8 + 수 * 72, dužina_VALUE = 0;
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 64; prostor_za_unos_unos++) Naziv[prostor_za_unos_unos] = uređaj_VALUE.기억읽기(unos_VALUE + prostor_za_unos_unos);
            while (dužina_VALUE < 64 && Naziv[dužina_VALUE] != 0) dužina_VALUE++;
            int Pozicija = 실행관리.수(unos_VALUE + 64), fajl_podesiti_veličinu = 실행관리.수(unos_VALUE + 68);
            if (!ček_naziv(Naziv, dužina_VALUE) || fajl_podesiti_veličinu < 0 || fajl_podesiti_veličinu > 최대크기 || Pozicija < 8 + stavka_COUNT * 72 || Pozicija > Veličina - fajl_podesiti_veličinu) {
                SMS_Terminal.Piši("올바르지 않은 Java Fajl unos_VALUE\n"); return;
            }
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < fajl_podesiti_veličinu; prostor_za_unos_unos++) uređivati_VALUE[prostor_za_unos_unos] = uređaj_VALUE.기억읽기(Grupa_VALUE + Pozicija + prostor_za_unos_unos);
            if (Store_VALUE(Naziv, dužina_VALUE, uređivati_VALUE, fajl_podesiti_veličinu) < 0) { SMS_Terminal.Piši("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
