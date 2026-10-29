// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Datoteka. 원본 Uredi_VALUE/prevajati_vir napaka_VALUE 시 기존 파일을 보존한다. */
public final class pomnilnik_datotečni_sistem {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] spremeniti_velikost_Seznam = new int[8];
    static int[] odprto_COUNT = new int[8], 허가들 = new int[8];
    static int[] Ime = new int[64];
    static int[] Uredi_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean presežek_VALUE = false;
    static int Uredi_spremeniti_velikost = 0;

    static boolean preveriti_ime(int[] znak_VALUE, int 길이) {
        if (길이 < 1 || 길이 > 63) return false;
        for (int 수 = 0; 수 < 길이; 수++) {
            int VALUE = znak_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return znak_VALUE[0] != '.';
    }

    static int FIND_vnos(int[] znak_VALUE, int 길이) {
        if (!preveriti_ime(znak_VALUE, 길이)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + 길이] == 0;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (이름들[수 * 64 + 칸] != znak_VALUE[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] znak_VALUE, int 길이, int[] podatki, int Velikost) {
        if (!preveriti_ime(znak_VALUE, 길이) || Velikost < 0 || Velikost > podatki.length) return -22;
        if (Velikost > 최대크기) return -90;
        int INDEX = FIND_vnos(znak_VALUE, 길이);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && odprto_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int naslov = naprava_VALUE.Datoteka_pomnilnik() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Velikost; 수++) naprava_VALUE.pisati_pomnilnik(naslov + 수, podatki[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < 길이 ? znak_VALUE[수] : 0;
        spremeniti_velikost_Seznam[INDEX] = Velikost;
        return Velikost;
    }

    static void vnos_Seznam() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.Pisanje("  "); SMS_Terminal.수쓰기(spremeniti_velikost_Seznam[수]); SMS_Terminal.Pisanje("bajt_VALUE\n");
        }
        SMS_Terminal.Pisanje(naprava_za_shranjevanje_povezava.informacijska_tehnologija_Dejaven_9e72441a ? "Datoteka 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 Datoteka 8칸, 파일당 16384바이트; znova_poskusiti_VALUE 시작하면 사라짐\n");
    }

    static void Ukaz(int[] 입력, int Zaženi, int 길이, int Dejanje) {
        while (Zaženi < 길이 && 입력[Zaženi] == ' ') Zaženi++;
        int 끝 = 길이;
        while (끝 > Zaženi && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Zaženi;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Pisanje("올바르지 않은 Datoteka Ime\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Ime[칸] = 칸 < 수 ? 입력[Zaženi + 칸] : 0;
        int INDEX = FIND_vnos(Ime, 수);
        if (INDEX == -22) { SMS_Terminal.Pisanje("올바르지 않은 Datoteka Ime\n"); return; }
        if (Dejanje == 0) {
            편집중 = true; Uredi_spremeniti_velikost = 0; presežek_VALUE = false;
            SMS_Terminal.Pisanje("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Pisanje("파일을 찾을 수 없습니다\n");
        else if (Dejanje == 1) {
            int naslov = naprava_VALUE.Datoteka_pomnilnik() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < spremeniti_velikost_Seznam[INDEX]; 칸++) SMS_Terminal.문자(naprava_VALUE.기억읽기(naslov + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; spremeniti_velikost_Seznam[INDEX] = 0; SMS_Terminal.Pisanje("파일을 지웠습니다\n"); }
    }

    static boolean informacijska_tehnologija_EXACT(int[] 입력, int 길이, String 문구) {
        if (길이 != 문구.length()) return false;
        for (int 칸 = 0; 칸 < 길이; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Urejeno_linija(int[] 입력, int 길이, boolean linija_presežek) {
        if (informacijska_tehnologija_EXACT(입력, 길이, ".cancel")) {
            편집중 = false; SMS_Terminal.Pisanje("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (informacijska_tehnologija_EXACT(입력, 길이, ".save")) {
            편집중 = false;
            if (presežek_VALUE) { SMS_Terminal.Pisanje("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Ime[수] != 0) 수++;
            int REZULTAT = Store_VALUE(Ime, 수, Uredi_VALUE, Uredi_spremeniti_velikost);
            SMS_Terminal.Pisanje(REZULTAT >= 0 ? "보존한 bajt_VALUE 수: " : "보존 napaka_VALUE: ");
            SMS_Terminal.수쓰기(REZULTAT); SMS_Terminal.문자(10);
        } else if (linija_presežek || 길이 + 1 > 최대크기 - Uredi_spremeniti_velikost) presežek_VALUE = true;
        else {
            for (int 수 = 0; 수 < 길이; 수++) Uredi_VALUE[Uredi_spremeniti_velikost++] = 입력[수];
            Uredi_VALUE[Uredi_spremeniti_velikost++] = 10;
        }
    }

    static void 예제(String Datoteka, String vsebina_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Ime[수] = 수 < Datoteka.length() ? Datoteka.charAt(수) : 0;
        for (int 수 = 0; 수 < vsebina_VALUE.length(); 수++) Uredi_VALUE[수] = vsebina_VALUE.charAt(수);
        Store_VALUE(Ime, Datoteka.length(), Uredi_VALUE, vsebina_VALUE.length());
    }

    static void Pripravi() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Skupina_VALUE = naprava_VALUE.자바파일묶음(), Velikost = naprava_VALUE.자바파일묶음크기();
        if (Velikost < 8 || 실행관리.수(Skupina_VALUE) != 0x464a4b4a) { SMS_Terminal.Pisanje("올바르지 않은 Java Datoteka Skupina_VALUE\n"); return; }
        int element_COUNT = 실행관리.수(Skupina_VALUE + 4);
        if (element_COUNT < 0 || element_COUNT > 8 || element_COUNT > (Velikost - 8) / 72) { SMS_Terminal.Pisanje("올바르지 않은 Java Datoteka vnos_Seznam\n"); return; }
        for (int 수 = 0; 수 < element_COUNT; 수++) {
            int vnos_VALUE = Skupina_VALUE + 8 + 수 * 72, 길이 = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Ime[칸] = naprava_VALUE.기억읽기(vnos_VALUE + 칸);
            while (길이 < 64 && Ime[길이] != 0) 길이++;
            int Položaj = 실행관리.수(vnos_VALUE + 64), velikost_datoteke = 실행관리.수(vnos_VALUE + 68);
            if (!preveriti_ime(Ime, 길이) || velikost_datoteke < 0 || velikost_datoteke > 최대크기 || Položaj < 8 + element_COUNT * 72 || Položaj > Velikost - velikost_datoteke) {
                SMS_Terminal.Pisanje("올바르지 않은 Java Datoteka vnos_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < velikost_datoteke; 칸++) Uredi_VALUE[칸] = naprava_VALUE.기억읽기(Skupina_VALUE + Položaj + 칸);
            if (Store_VALUE(Ime, 길이, Uredi_VALUE, velikost_datoteke) < 0) { SMS_Terminal.Pisanje("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
