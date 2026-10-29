// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 tiedoston_nimi. 원본 muutos_ARVO/kääntää_lähde virhe_ARVO 시 기존 파일을 보존한다. */
public final class Muisti_tiedostojärjestelmä {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] muuttaa_kokoa_luettelo = new int[8];
    static int[] avata_LASKE = new int[8], 허가들 = new int[8];
    static int[] Nimi = new int[64];
    static int[] muutos_ARVO = new int[최대크기];
    static boolean 편집중 = false;
    static boolean ylivuoto_ARVO = false;
    static int muutos_muuttaa_kokoa = 0;

    static boolean sekki_nimi(int[] merkki_ARVO, int kesto_ARVO) {
        if (kesto_ARVO < 1 || kesto_ARVO > 63) return false;
        for (int numero = 0; numero < kesto_ARVO; numero++) {
            int ARVO = merkki_ARVO[numero];
            if (!(ARVO >= 'a' && ARVO <= 'z') && !(ARVO >= 'A' && ARVO <= 'Z')
                && !(ARVO >= '0' && ARVO <= '9') && ARVO != '_' && ARVO != '-' && ARVO != '.') return false;
        }
        return merkki_ARVO[0] != '.';
    }

    static int ETSI_merkintä(int[] merkki_ARVO, int kesto_ARVO) {
        if (!sekki_nimi(merkki_ARVO, kesto_ARVO)) return -22;
        for (int numero = 0; numero < 8; numero++) {
            boolean 같음 = 이름들[numero * 64 + kesto_ARVO] == 0;
            for (int paikka_merkintä = 0; paikka_merkintä < kesto_ARVO; paikka_merkintä++) if (이름들[numero * 64 + paikka_merkintä] != merkki_ARVO[paikka_merkintä]) 같음 = false;
            if (같음) return numero;
        }
        return -2;
    }

    static int Store_ARVO(int[] merkki_ARVO, int kesto_ARVO, int[] data, int Koko) {
        if (!sekki_nimi(merkki_ARVO, kesto_ARVO) || Koko < 0 || Koko > data.length) return -22;
        if (Koko > 최대크기) return -90;
        int INDEKSI = ETSI_merkintä(merkki_ARVO, kesto_ARVO);
        if (INDEKSI == -2) {
            for (int numero = 0; numero < 8 && INDEKSI < 0; numero++) if (이름들[numero * 64] == 0 && avata_LASKE[numero] == 0) INDEKSI = numero;
            if (INDEKSI >= 0) 허가들[INDEKSI] = 438;
        }
        if (INDEKSI < 0) return -28;
        int OSOITE = laite_ARVO.Tiedosto_Muisti() + INDEKSI * 최대크기;
        for (int numero = 0; numero < Koko; numero++) laite_ARVO.kirjoitus_Muisti(OSOITE + numero, data[numero]);
        for (int numero = 0; numero < 64; numero++) 이름들[INDEKSI * 64 + numero] = numero < kesto_ARVO ? merkki_ARVO[numero] : 0;
        muuttaa_kokoa_luettelo[INDEKSI] = Koko;
        return Koko;
    }

    static void merkintä_luettelo() {
        for (int numero = 0; numero < 8; numero++) if (이름들[numero * 64] != 0) {
            for (int paikka_merkintä = 0; paikka_merkintä < 64 && 이름들[numero * 64 + paikka_merkintä] != 0; paikka_merkintä++) SMS_Pääte.문자(이름들[numero * 64 + paikka_merkintä]);
            SMS_Pääte.Kirjoitus("  "); SMS_Pääte.kirjoitus_numero(muuttaa_kokoa_luettelo[numero]); SMS_Pääte.Kirjoitus("tavu_ARVO\n");
        }
        SMS_Pääte.Kirjoitus(tallennuslaite_yhteys.tietojärjestelmät_Aktiivinen_9e72441a ? "tiedoston_nimi 8칸, 파일당 16384바이트; sync로 Store_ARVO 장치에 보존\n"
            : "임시 tiedoston_nimi 8칸, 파일당 16384바이트; yrittää_uudelleen_ARVO 시작하면 사라짐\n");
    }

    static void komento(int[] syöte_ARVO, int Suorita_2, int kesto_ARVO, int Toiminto) {
        while (Suorita_2 < kesto_ARVO && syöte_ARVO[Suorita_2] == ' ') Suorita_2++;
        int 끝 = kesto_ARVO;
        while (끝 > Suorita_2 && syöte_ARVO[끝 - 1] == ' ') 끝--;
        int numero = 끝 - Suorita_2;
        if (numero < 1 || numero > 63) { SMS_Pääte.Kirjoitus("올바르지 않은 tiedoston_nimi Nimi\n"); return; }
        for (int paikka_merkintä = 0; paikka_merkintä < 64; paikka_merkintä++) Nimi[paikka_merkintä] = paikka_merkintä < numero ? syöte_ARVO[Suorita_2 + paikka_merkintä] : 0;
        int INDEKSI = ETSI_merkintä(Nimi, numero);
        if (INDEKSI == -22) { SMS_Pääte.Kirjoitus("올바르지 않은 tiedoston_nimi Nimi\n"); return; }
        if (Toiminto == 0) {
            편집중 = true; muutos_muuttaa_kokoa = 0; ylivuoto_ARVO = false;
            SMS_Pääte.Kirjoitus("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEKSI < 0) SMS_Pääte.Kirjoitus("파일을 찾을 numero 없습니다\n");
        else if (Toiminto == 1) {
            int OSOITE = laite_ARVO.Tiedosto_Muisti() + INDEKSI * 최대크기;
            for (int paikka_merkintä = 0; paikka_merkintä < muuttaa_kokoa_luettelo[INDEKSI]; paikka_merkintä++) SMS_Pääte.문자(laite_ARVO.lukea_Muisti(OSOITE + paikka_merkintä));
            SMS_Pääte.문자(10);
        } else { 이름들[INDEKSI * 64] = 0; muuttaa_kokoa_luettelo[INDEKSI] = 0; SMS_Pääte.Kirjoitus("파일을 지웠습니다\n"); }
    }

    static boolean tietojärjestelmät_VERTAA(int[] syöte_ARVO, int kesto_ARVO, String 문구) {
        if (kesto_ARVO != 문구.length()) return false;
        for (int paikka_merkintä = 0; paikka_merkintä < kesto_ARVO; paikka_merkintä++) if (syöte_ARVO[paikka_merkintä] != 문구.charAt(paikka_merkintä)) return false;
        return true;
    }

    static void Muokattu_rivi(int[] syöte_ARVO, int kesto_ARVO, boolean rivi_ylivuoto) {
        if (tietojärjestelmät_VERTAA(syöte_ARVO, kesto_ARVO, ".cancel")) {
            편집중 = false; SMS_Pääte.Kirjoitus("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (tietojärjestelmät_VERTAA(syöte_ARVO, kesto_ARVO, ".save")) {
            편집중 = false;
            if (ylivuoto_ARVO) { SMS_Pääte.Kirjoitus("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int numero = 0;
            while (numero < 64 && Nimi[numero] != 0) numero++;
            int TULOS = Store_ARVO(Nimi, numero, muutos_ARVO, muutos_muuttaa_kokoa);
            SMS_Pääte.Kirjoitus(TULOS >= 0 ? "보존한 tavu_ARVO numero: " : "보존 virhe_ARVO: ");
            SMS_Pääte.kirjoitus_numero(TULOS); SMS_Pääte.문자(10);
        } else if (rivi_ylivuoto || kesto_ARVO + 1 > 최대크기 - muutos_muuttaa_kokoa) ylivuoto_ARVO = true;
        else {
            for (int numero = 0; numero < kesto_ARVO; numero++) muutos_ARVO[muutos_muuttaa_kokoa++] = syöte_ARVO[numero];
            muutos_ARVO[muutos_muuttaa_kokoa++] = 10;
        }
    }

    static void 예제(String tiedoston_nimi, String Sisältö_ARVO) {
        for (int numero = 0; numero < 64; numero++) Nimi[numero] = numero < tiedoston_nimi.length() ? tiedoston_nimi.charAt(numero) : 0;
        for (int numero = 0; numero < Sisältö_ARVO.length(); numero++) muutos_ARVO[numero] = Sisältö_ARVO.charAt(numero);
        Store_ARVO(Nimi, tiedoston_nimi.length(), muutos_ARVO, Sisältö_ARVO.length());
    }

    static void Valmistele() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Ryhmä_ARVO = laite_ARVO.자바파일묶음(), Koko = laite_ARVO.자바파일묶음크기();
        if (Koko < 8 || suoritus_Valvoja.numero(Ryhmä_ARVO) != 0x464a4b4a) { SMS_Pääte.Kirjoitus("올바르지 않은 Java tiedoston_nimi Ryhmä_ARVO\n"); return; }
        int kohde_LASKE = suoritus_Valvoja.numero(Ryhmä_ARVO + 4);
        if (kohde_LASKE < 0 || kohde_LASKE > 8 || kohde_LASKE > (Koko - 8) / 72) { SMS_Pääte.Kirjoitus("올바르지 않은 Java tiedoston_nimi merkintä_luettelo\n"); return; }
        for (int numero = 0; numero < kohde_LASKE; numero++) {
            int merkintä_ARVO_962f286b = Ryhmä_ARVO + 8 + numero * 72, kesto_ARVO = 0;
            for (int paikka_merkintä = 0; paikka_merkintä < 64; paikka_merkintä++) Nimi[paikka_merkintä] = laite_ARVO.lukea_Muisti(merkintä_ARVO_962f286b + paikka_merkintä);
            while (kesto_ARVO < 64 && Nimi[kesto_ARVO] != 0) kesto_ARVO++;
            int paikka = suoritus_Valvoja.numero(merkintä_ARVO_962f286b + 64), tiedostokoko = suoritus_Valvoja.numero(merkintä_ARVO_962f286b + 68);
            if (!sekki_nimi(Nimi, kesto_ARVO) || tiedostokoko < 0 || tiedostokoko > 최대크기 || paikka < 8 + kohde_LASKE * 72 || paikka > Koko - tiedostokoko) {
                SMS_Pääte.Kirjoitus("올바르지 않은 Java tiedoston_nimi merkintä_ARVO_962f286b\n"); return;
            }
            for (int paikka_merkintä = 0; paikka_merkintä < tiedostokoko; paikka_merkintä++) muutos_ARVO[paikka_merkintä] = laite_ARVO.lukea_Muisti(Ryhmä_ARVO + paikka + paikka_merkintä);
            if (Store_ARVO(Nimi, kesto_ARVO, muutos_ARVO, tiedostokoko) < 0) { SMS_Pääte.Kirjoitus("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
