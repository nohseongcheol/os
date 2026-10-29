// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 nazwa_pliku. 원본 Edytuj_WARTOŚĆ/kompilować_źródło awaria_WARTOŚĆ 시 기존 파일을 보존한다. */
public final class Pamięć_system_plików {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] zmienić_rozmiar_Lista = new int[8];
    static int[] otwarty_ILE_LICZB = new int[8], 허가들 = new int[8];
    static int[] Nazwa = new int[64];
    static int[] Edytuj_WARTOŚĆ = new int[최대크기];
    static boolean 편집중 = false;
    static boolean przepełnienie_WARTOŚĆ = false;
    static int Edytuj_zmienić_rozmiar = 0;

    static boolean czek_nazwa(int[] znak_WARTOŚĆ, int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ < 1 || długość_WARTOŚĆ > 63) return false;
        for (int identyfikator = 0; identyfikator < długość_WARTOŚĆ; identyfikator++) {
            int WARTOŚĆ = znak_WARTOŚĆ[identyfikator];
            if (!(WARTOŚĆ >= 'a' && WARTOŚĆ <= 'z') && !(WARTOŚĆ >= 'A' && WARTOŚĆ <= 'Z')
                && !(WARTOŚĆ >= '0' && WARTOŚĆ <= '9') && WARTOŚĆ != '_' && WARTOŚĆ != '-' && WARTOŚĆ != '.') return false;
        }
        return znak_WARTOŚĆ[0] != '.';
    }

    static int ZNAJDŹ_wpis(int[] znak_WARTOŚĆ, int długość_WARTOŚĆ) {
        if (!czek_nazwa(znak_WARTOŚĆ, długość_WARTOŚĆ)) return -22;
        for (int identyfikator = 0; identyfikator < 8; identyfikator++) {
            boolean 같음 = 이름들[identyfikator * 64 + długość_WARTOŚĆ] == 0;
            for (int gniazdo_wpis = 0; gniazdo_wpis < długość_WARTOŚĆ; gniazdo_wpis++) if (이름들[identyfikator * 64 + gniazdo_wpis] != znak_WARTOŚĆ[gniazdo_wpis]) 같음 = false;
            if (같음) return identyfikator;
        }
        return -2;
    }

    static int Store_WARTOŚĆ(int[] znak_WARTOŚĆ, int długość_WARTOŚĆ, int[] dane, int Rozmiar) {
        if (!czek_nazwa(znak_WARTOŚĆ, długość_WARTOŚĆ) || Rozmiar < 0 || Rozmiar > dane.length) return -22;
        if (Rozmiar > 최대크기) return -90;
        int INDEKS = ZNAJDŹ_wpis(znak_WARTOŚĆ, długość_WARTOŚĆ);
        if (INDEKS == -2) {
            for (int identyfikator = 0; identyfikator < 8 && INDEKS < 0; identyfikator++) if (이름들[identyfikator * 64] == 0 && otwarty_ILE_LICZB[identyfikator] == 0) INDEKS = identyfikator;
            if (INDEKS >= 0) 허가들[INDEKS] = 438;
        }
        if (INDEKS < 0) return -28;
        int Adres = urządzenie_WARTOŚĆ.Plik_Pamięć() + INDEKS * 최대크기;
        for (int identyfikator = 0; identyfikator < Rozmiar; identyfikator++) urządzenie_WARTOŚĆ.zapis_Pamięć(Adres + identyfikator, dane[identyfikator]);
        for (int identyfikator = 0; identyfikator < 64; identyfikator++) 이름들[INDEKS * 64 + identyfikator] = identyfikator < długość_WARTOŚĆ ? znak_WARTOŚĆ[identyfikator] : 0;
        zmienić_rozmiar_Lista[INDEKS] = Rozmiar;
        return Rozmiar;
    }

    static void wpis_Lista() {
        for (int identyfikator = 0; identyfikator < 8; identyfikator++) if (이름들[identyfikator * 64] != 0) {
            for (int gniazdo_wpis = 0; gniazdo_wpis < 64 && 이름들[identyfikator * 64 + gniazdo_wpis] != 0; gniazdo_wpis++) SMS_Terminal.문자(이름들[identyfikator * 64 + gniazdo_wpis]);
            SMS_Terminal.Zapis("  "); SMS_Terminal.zapis_identyfikator(zmienić_rozmiar_Lista[identyfikator]); SMS_Terminal.Zapis("bajt_WARTOŚĆ\n");
        }
        SMS_Terminal.Zapis(urządzenie_magazynujące_połączenie.systemy_informacyjne_Aktywny_9e72441a ? "nazwa_pliku 8칸, 파일당 16384바이트; sync로 Store_WARTOŚĆ 장치에 보존\n"
            : "임시 nazwa_pliku 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void polecenie(int[] wejście_WARTOŚĆ, int Uruchom_2, int długość_WARTOŚĆ, int Akcja) {
        while (Uruchom_2 < długość_WARTOŚĆ && wejście_WARTOŚĆ[Uruchom_2] == ' ') Uruchom_2++;
        int 끝 = długość_WARTOŚĆ;
        while (끝 > Uruchom_2 && wejście_WARTOŚĆ[끝 - 1] == ' ') 끝--;
        int identyfikator = 끝 - Uruchom_2;
        if (identyfikator < 1 || identyfikator > 63) { SMS_Terminal.Zapis("올바르지 않은 nazwa_pliku Nazwa\n"); return; }
        for (int gniazdo_wpis = 0; gniazdo_wpis < 64; gniazdo_wpis++) Nazwa[gniazdo_wpis] = gniazdo_wpis < identyfikator ? wejście_WARTOŚĆ[Uruchom_2 + gniazdo_wpis] : 0;
        int INDEKS = ZNAJDŹ_wpis(Nazwa, identyfikator);
        if (INDEKS == -22) { SMS_Terminal.Zapis("올바르지 않은 nazwa_pliku Nazwa\n"); return; }
        if (Akcja == 0) {
            편집중 = true; Edytuj_zmienić_rozmiar = 0; przepełnienie_WARTOŚĆ = false;
            SMS_Terminal.Zapis("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEKS < 0) SMS_Terminal.Zapis("파일을 찾을 identyfikator 없습니다\n");
        else if (Akcja == 1) {
            int Adres = urządzenie_WARTOŚĆ.Plik_Pamięć() + INDEKS * 최대크기;
            for (int gniazdo_wpis = 0; gniazdo_wpis < zmienić_rozmiar_Lista[INDEKS]; gniazdo_wpis++) SMS_Terminal.문자(urządzenie_WARTOŚĆ.기억읽기(Adres + gniazdo_wpis));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEKS * 64] = 0; zmienić_rozmiar_Lista[INDEKS] = 0; SMS_Terminal.Zapis("파일을 지웠습니다\n"); }
    }

    static boolean systemy_informacyjne_PORÓWNAJ(int[] wejście_WARTOŚĆ, int długość_WARTOŚĆ, String 문구) {
        if (długość_WARTOŚĆ != 문구.length()) return false;
        for (int gniazdo_wpis = 0; gniazdo_wpis < długość_WARTOŚĆ; gniazdo_wpis++) if (wejście_WARTOŚĆ[gniazdo_wpis] != 문구.charAt(gniazdo_wpis)) return false;
        return true;
    }

    static void Edytowane_linia(int[] wejście_WARTOŚĆ, int długość_WARTOŚĆ, boolean linia_przepełnienie) {
        if (systemy_informacyjne_PORÓWNAJ(wejście_WARTOŚĆ, długość_WARTOŚĆ, ".cancel")) {
            편집중 = false; SMS_Terminal.Zapis("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (systemy_informacyjne_PORÓWNAJ(wejście_WARTOŚĆ, długość_WARTOŚĆ, ".save")) {
            편집중 = false;
            if (przepełnienie_WARTOŚĆ) { SMS_Terminal.Zapis("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int identyfikator = 0;
            while (identyfikator < 64 && Nazwa[identyfikator] != 0) identyfikator++;
            int WYNIK = Store_WARTOŚĆ(Nazwa, identyfikator, Edytuj_WARTOŚĆ, Edytuj_zmienić_rozmiar);
            SMS_Terminal.Zapis(WYNIK >= 0 ? "보존한 bajt_WARTOŚĆ identyfikator: " : "보존 awaria_WARTOŚĆ: ");
            SMS_Terminal.zapis_identyfikator(WYNIK); SMS_Terminal.문자(10);
        } else if (linia_przepełnienie || długość_WARTOŚĆ + 1 > 최대크기 - Edytuj_zmienić_rozmiar) przepełnienie_WARTOŚĆ = true;
        else {
            for (int identyfikator = 0; identyfikator < długość_WARTOŚĆ; identyfikator++) Edytuj_WARTOŚĆ[Edytuj_zmienić_rozmiar++] = wejście_WARTOŚĆ[identyfikator];
            Edytuj_WARTOŚĆ[Edytuj_zmienić_rozmiar++] = 10;
        }
    }

    static void 예제(String nazwa_pliku, String treść_WARTOŚĆ_cb0f2404) {
        for (int identyfikator = 0; identyfikator < 64; identyfikator++) Nazwa[identyfikator] = identyfikator < nazwa_pliku.length() ? nazwa_pliku.charAt(identyfikator) : 0;
        for (int identyfikator = 0; identyfikator < treść_WARTOŚĆ_cb0f2404.length(); identyfikator++) Edytuj_WARTOŚĆ[identyfikator] = treść_WARTOŚĆ_cb0f2404.charAt(identyfikator);
        Store_WARTOŚĆ(Nazwa, nazwa_pliku.length(), Edytuj_WARTOŚĆ, treść_WARTOŚĆ_cb0f2404.length());
    }

    static void Przygotuj() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int grupa_WARTOŚĆ = urządzenie_WARTOŚĆ.자바파일묶음(), Rozmiar = urządzenie_WARTOŚĆ.자바파일묶음크기();
        if (Rozmiar < 8 || wykonanie_Menedżer.identyfikator(grupa_WARTOŚĆ) != 0x464a4b4a) { SMS_Terminal.Zapis("올바르지 않은 Java nazwa_pliku grupa_WARTOŚĆ\n"); return; }
        int towar_ILE_LICZB = wykonanie_Menedżer.identyfikator(grupa_WARTOŚĆ + 4);
        if (towar_ILE_LICZB < 0 || towar_ILE_LICZB > 8 || towar_ILE_LICZB > (Rozmiar - 8) / 72) { SMS_Terminal.Zapis("올바르지 않은 Java nazwa_pliku wpis_Lista\n"); return; }
        for (int identyfikator = 0; identyfikator < towar_ILE_LICZB; identyfikator++) {
            int wpis_WARTOŚĆ = grupa_WARTOŚĆ + 8 + identyfikator * 72, długość_WARTOŚĆ = 0;
            for (int gniazdo_wpis = 0; gniazdo_wpis < 64; gniazdo_wpis++) Nazwa[gniazdo_wpis] = urządzenie_WARTOŚĆ.기억읽기(wpis_WARTOŚĆ + gniazdo_wpis);
            while (długość_WARTOŚĆ < 64 && Nazwa[długość_WARTOŚĆ] != 0) długość_WARTOŚĆ++;
            int pozycja = wykonanie_Menedżer.identyfikator(wpis_WARTOŚĆ + 64), rozmiar_pliku = wykonanie_Menedżer.identyfikator(wpis_WARTOŚĆ + 68);
            if (!czek_nazwa(Nazwa, długość_WARTOŚĆ) || rozmiar_pliku < 0 || rozmiar_pliku > 최대크기 || pozycja < 8 + towar_ILE_LICZB * 72 || pozycja > Rozmiar - rozmiar_pliku) {
                SMS_Terminal.Zapis("올바르지 않은 Java nazwa_pliku wpis_WARTOŚĆ\n"); return;
            }
            for (int gniazdo_wpis = 0; gniazdo_wpis < rozmiar_pliku; gniazdo_wpis++) Edytuj_WARTOŚĆ[gniazdo_wpis] = urządzenie_WARTOŚĆ.기억읽기(grupa_WARTOŚĆ + pozycja + gniazdo_wpis);
            if (Store_WARTOŚĆ(Nazwa, długość_WARTOŚĆ, Edytuj_WARTOŚĆ, rozmiar_pliku) < 0) { SMS_Terminal.Zapis("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
