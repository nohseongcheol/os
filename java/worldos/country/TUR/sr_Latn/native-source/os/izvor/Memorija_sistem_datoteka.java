// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Datoteka. 원본 Uredi_VALUE/kompajlirati_izvor otkazivanje_VALUE 시 기존 파일을 보존한다. */
public final class Memorija_sistem_datoteka {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] promeniti_veličinu_Lista = new int[8];
    static int[] otvoren_COUNT = new int[8], 허가들 = new int[8];
    static int[] ime = new int[64];
    static int[] Uredi_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean višak_VALUE = false;
    static int Uredi_promeniti_veličinu = 0;

    static boolean proveriti_ime(int[] znak_VALUE, int 길이) {
        if (길이 < 1 || 길이 > 63) return false;
        for (int 수 = 0; 수 < 길이; 수++) {
            int VALUE = znak_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return znak_VALUE[0] != '.';
    }

    static int FIND_stavka(int[] znak_VALUE, int 길이) {
        if (!proveriti_ime(znak_VALUE, 길이)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + 길이] == 0;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (이름들[수 * 64 + 칸] != znak_VALUE[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] znak_VALUE, int 길이, int[] podaci, int promeniti_veličinu) {
        if (!proveriti_ime(znak_VALUE, 길이) || promeniti_veličinu < 0 || promeniti_veličinu > podaci.length) return -22;
        if (promeniti_veličinu > 최대크기) return -90;
        int INDEX = FIND_stavka(znak_VALUE, 길이);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && otvoren_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int adresa = uređaj_VALUE.Datoteka_Memorija() + INDEX * 최대크기;
        for (int 수 = 0; 수 < promeniti_veličinu; 수++) uređaj_VALUE.기억쓰기(adresa + 수, podaci[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < 길이 ? znak_VALUE[수] : 0;
        promeniti_veličinu_Lista[INDEX] = promeniti_veličinu;
        return promeniti_veličinu;
    }

    static void stavka_Lista() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.쓰기("  "); SMS_Terminal.수쓰기(promeniti_veličinu_Lista[수]); SMS_Terminal.쓰기("bajt_VALUE\n");
        }
        SMS_Terminal.쓰기(uređaj_za_skladištenje_veza.informatičko_odeljenje_Aktivan_9e72441a ? "Datoteka 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Datoteka 8칸, 파일당 16384바이트; pokušati_ponovo_VALUE 시작하면 사라짐\n");
    }

    static void komanda(int[] 입력, int koristiti, int 길이, int radnja) {
        while (koristiti < 길이 && 입력[koristiti] == ' ') koristiti++;
        int 끝 = 길이;
        while (끝 > koristiti && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - koristiti;
        if (수 < 1 || 수 > 63) { SMS_Terminal.쓰기("올바르지 않은 Datoteka ime\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) ime[칸] = 칸 < 수 ? 입력[koristiti + 칸] : 0;
        int INDEX = FIND_stavka(ime, 수);
        if (INDEX == -22) { SMS_Terminal.쓰기("올바르지 않은 Datoteka ime\n"); return; }
        if (radnja == 0) {
            편집중 = true; Uredi_promeniti_veličinu = 0; višak_VALUE = false;
            SMS_Terminal.쓰기("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.쓰기("파일을 찾을 수 없습니다\n");
        else if (radnja == 1) {
            int adresa = uređaj_VALUE.Datoteka_Memorija() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < promeniti_veličinu_Lista[INDEX]; 칸++) SMS_Terminal.문자(uređaj_VALUE.기억읽기(adresa + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; promeniti_veličinu_Lista[INDEX] = 0; SMS_Terminal.쓰기("파일을 지웠습니다\n"); }
    }

    static boolean informatičko_odeljenje_EXACT(int[] 입력, int 길이, String 문구) {
        if (길이 != 문구.length()) return false;
        for (int 칸 = 0; 칸 < 길이; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Uređivano_red(int[] 입력, int 길이, boolean red_višak) {
        if (informatičko_odeljenje_EXACT(입력, 길이, ".cancel")) {
            편집중 = false; SMS_Terminal.쓰기("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informatičko_odeljenje_EXACT(입력, 길이, ".save")) {
            편집중 = false;
            if (višak_VALUE) { SMS_Terminal.쓰기("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && ime[수] != 0) 수++;
            int KR = Store_VALUE(ime, 수, Uredi_VALUE, Uredi_promeniti_veličinu);
            SMS_Terminal.쓰기(KR >= 0 ? "보존한 bajt_VALUE 수: " : "보존 otkazivanje_VALUE: ");
            SMS_Terminal.수쓰기(KR); SMS_Terminal.문자(10);
        } else if (red_višak || 길이 + 1 > 최대크기 - Uredi_promeniti_veličinu) višak_VALUE = true;
        else {
            for (int 수 = 0; 수 < 길이; 수++) Uredi_VALUE[Uredi_promeniti_veličinu++] = 입력[수];
            Uredi_VALUE[Uredi_promeniti_veličinu++] = 10;
        }
    }

    static void 예제(String Datoteka, String Sadržaj_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) ime[수] = 수 < Datoteka.length() ? Datoteka.charAt(수) : 0;
        for (int 수 = 0; 수 < Sadržaj_VALUE.length(); 수++) Uredi_VALUE[수] = Sadržaj_VALUE.charAt(수);
        Store_VALUE(ime, Datoteka.length(), Uredi_VALUE, Sadržaj_VALUE.length());
    }

    static void Pripremi() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Grupa_VALUE = uređaj_VALUE.자바파일묶음(), promeniti_veličinu = uređaj_VALUE.자바파일묶음크기();
        if (promeniti_veličinu < 8 || 실행관리.수(Grupa_VALUE) != 0x464a4b4a) { SMS_Terminal.쓰기("올바르지 않은 Java Datoteka Grupa_VALUE\n"); return; }
        int stavka_COUNT = 실행관리.수(Grupa_VALUE + 4);
        if (stavka_COUNT < 0 || stavka_COUNT > 8 || stavka_COUNT > (promeniti_veličinu - 8) / 72) { SMS_Terminal.쓰기("올바르지 않은 Java Datoteka stavka_Lista\n"); return; }
        for (int 수 = 0; 수 < stavka_COUNT; 수++) {
            int stavka_VALUE = Grupa_VALUE + 8 + 수 * 72, 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) ime[칸] = uređaj_VALUE.기억읽기(stavka_VALUE + 칸);
            while (길이 < 64 && ime[길이] != 0) 길이++;
            int pozicija = 실행관리.수(stavka_VALUE + 64), veličina_datoteke = 실행관리.수(stavka_VALUE + 68);
            if (!proveriti_ime(ime, 길이) || veličina_datoteke < 0 || veličina_datoteke > 최대크기 || pozicija < 8 + stavka_COUNT * 72 || pozicija > promeniti_veličinu - veličina_datoteke) {
                SMS_Terminal.쓰기("올바르지 않은 Java Datoteka stavka_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < veličina_datoteke; 칸++) Uredi_VALUE[칸] = uređaj_VALUE.기억읽기(Grupa_VALUE + pozicija + 칸);
            if (Store_VALUE(ime, 길이, Uredi_VALUE, veličina_datoteke) < 0) { SMS_Terminal.쓰기("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
