// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Wielka_Brytania.JGbrOS.testy;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Wielka_Brytania.JGbrOS.Pamięć_region.Pamięć_Menedżer;
import Wielka_Brytania.JGbrOS.Pamięć_region.strona_Menedżer;
import Wielka_Brytania.JGbrOS.wejście_WARTOŚĆ.wejście_konkurs;
import Wielka_Brytania.JGbrOS.작업.Proces_WARTOŚĆ;
import Wielka_Brytania.JGbrOS.wywołanie_systemowe.wywołanie_systemowe;
import Wielka_Brytania.JGbrOS.system_plików.wykonywalny_moduł_ładujący;
import Wielka_Brytania.JGbrOS.jądro.jądro;
import Wielka_Brytania.JGbrOS.host.host_sprzęt;
import Wielka_Brytania.JGbrOS.przerwanie.przerwanie_Menedżer;
import Wielka_Brytania.JGbrOS.deskryptor_wpis.Globalna_deskryptor_tabela;
import Wielka_Brytania.JGbrOS.urządzenie_magazynujące.고급기술결합장치;
import Wielka_Brytania.JGbrOS.urządzenie_WARTOŚĆ.akcesorium_magistrala_Menedżer;
import Wielka_Brytania.JGbrOS.sieć_Stos.sieć_Narzędzia;
import Wielka_Brytania.JGbrOS.sieć_Stos.warstwa_sieciowa;
import Wielka_Brytania.JGbrOS.urządzenie_WARTOŚĆ.Zegar;
import Wielka_Brytania.JGbrOS.deskryptor_wpis.zadanie_Stan_odcinek;
import Wielka_Brytania.JGbrOS.화면.znak_wyświetlać;
import Wielka_Brytania.JGbrOS.system_plików.partycja_podstawowa_tabela;

public final class 전체시험 {
    private static int przekazać_ILE_LICZB;

    private 전체시험() {
    }

    public static void main(String[] parametr_argument) {
        host_sprzęt urządzenie_WARTOŚĆ = new host_sprzęt();
        jądro jądro_WARTOŚĆ = new jądro(urządzenie_WARTOŚĆ);
        jądro_WARTOŚĆ.Uruchom_2();

        test_Pamięć(jądro_WARTOŚĆ);
        쪽관리시험(jądro_WARTOŚĆ);
        파일과과정시험(jądro_WARTOŚĆ);
        실행파일시험(jądro_WARTOŚĆ);
        test_wejście(jądro_WARTOŚĆ);
        test_sprzęt(urządzenie_WARTOŚĆ);
        개입중단과서술자시험();
        test_Pamięć_ORAZ_Sieć();
        화면과시계시험();

        System.out.println("JGbrOS testy przekazać_WARTOŚĆ: " + przekazać_ILE_LICZB);
    }

    private static void test_Pamięć(jądro jądro_WARTOŚĆ) {
        Pamięć_Menedżer Menedżer_WARTOŚĆ = jądro_WARTOŚĆ.Pamięć_region();
        int 첫주소 = Menedżer_WARTOŚĆ.정렬할당(100, 64);
        확인((첫주소 & 63) == 0, "wyrównać_WARTOŚĆ przydzielić_Pamięć");
        Menedżer_WARTOŚĆ.zapis_bajt_WARTOŚĆ(첫주소, (byte) 0x5a);
        확인(Menedżer_WARTOŚĆ.바이트읽기(첫주소) == (byte) 0x5a, "물리 Pamięć_region 읽고 Zapis");
        int 사용전 = Menedżer_WARTOŚĆ.사용크기();
        Menedżer_WARTOŚĆ.wersja_Pamięć(첫주소);
        확인(Menedżer_WARTOŚĆ.사용크기() < 사용전, "Pamięć_region wersja_Pamięć");
    }

    private static void 쪽관리시험(jądro jądro_WARTOŚĆ) {
        strona_Menedżer Menedżer_WARTOŚĆ = jądro_WARTOŚĆ.쪽관리();
        strona_Menedżer.przestrzeń_adresowa nadrzędny_SPACJA = Menedżer_WARTOŚĆ.새주소공간();
        Menedżer_WARTOŚĆ.MAP_strona(nadrzędny_SPACJA, 0x1000, true);
        Menedżer_WARTOŚĆ.zapis_bajt_WARTOŚĆ(nadrzędny_SPACJA, 0x1010, (byte) 7);
        strona_Menedżer.przestrzeń_adresowa dziecko_SPACJA = Menedżer_WARTOŚĆ.쓰기시복사복제(nadrzędny_SPACJA);
        Menedżer_WARTOŚĆ.zapis_bajt_WARTOŚĆ(dziecko_SPACJA, 0x1010, (byte) 9);
        확인(Menedżer_WARTOŚĆ.바이트읽기(nadrzędny_SPACJA, 0x1010) == 7, "Zapis 시 kopiować_WARTOŚĆ nadrzędny_WARTOŚĆ 격리");
        확인(Menedżer_WARTOŚĆ.바이트읽기(dziecko_SPACJA, 0x1010) == 9, "Zapis 시 kopiować_WARTOŚĆ dziecko_WARTOŚĆ Zapis");
    }

    private static void 파일과과정시험(jądro jądro_WARTOŚĆ) {
        byte[] treść_WARTOŚĆ_cb0f2404 = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        jądro_WARTOŚĆ.system_plików().dołączać_Plik("testy", treść_WARTOŚĆ_cb0f2404);
        Proces_WARTOŚĆ nadrzędny_WARTOŚĆ = jądro_WARTOŚĆ.첫과정();
        wywołanie_systemowe 호출 = jądro_WARTOŚĆ.wywołanie_systemowe();
        int deskryptor_wpis = 호출.Otwórz(nadrzędny_WARTOŚĆ, "/testy", wywołanie_systemowe.tylko_do_odczytu_flaga);
        확인(deskryptor_wpis >= 3, "nazwa_pliku Otwórz");

        byte[] odbierać_cel = new byte[treść_WARTOŚĆ_cb0f2404.length];
        확인(호출.Odczyt(nadrzędny_WARTOŚĆ, deskryptor_wpis, odbierać_cel, odbierać_cel.length) == treść_WARTOŚĆ_cb0f2404.length, "nazwa_pliku Odczyt");
        확인(Arrays.equals(treść_WARTOŚĆ_cb0f2404, odbierać_cel), "nazwa_pliku treść_WARTOŚĆ_cb0f2404");
        확인(호출.przenosić_stanowisko(nadrzędny_WARTOŚĆ, deskryptor_wpis, 0, wywołanie_systemowe.Search_START) == 0, "nazwa_pliku pozycja przenosić_WARTOŚĆ");

        int 복제서술자 = 호출.Duplikuj_deskryptor(nadrzędny_WARTOŚĆ, deskryptor_wpis);
        확인(복제서술자 >= 0, "deskryptor_wpis klon_WARTOŚĆ");
        Proces_WARTOŚĆ dziecko_WARTOŚĆ = 호출.klon_Proces(nadrzędny_WARTOŚĆ);
        확인(dziecko_WARTOŚĆ.identyfikator_WARTOŚĆ() != nadrzędny_WARTOŚĆ.identyfikator_WARTOŚĆ(), "Proces_WARTOŚĆ identyfikator_WARTOŚĆ 분리");
        확인(dziecko_WARTOŚĆ.nadrzędny_identyfikator() == nadrzędny_WARTOŚĆ.identyfikator_WARTOŚĆ(), "nadrzędny_WARTOŚĆ Proces_WARTOŚĆ identyfikator_WARTOŚĆ");
        확인(호출.Zamknięte(dziecko_WARTOŚĆ, deskryptor_wpis) == 0 && nadrzędny_WARTOŚĆ.Plik_deskryptor().systemy_informacyjne_otwarty(deskryptor_wpis), "dziecko_WARTOŚĆ Zamknięte 격리");

        int Wstecz_Koniec = 호출.zwiększenie_stanu_program_przerwa(nadrzędny_WARTOŚĆ, 8192);
        확인(Wstecz_Koniec == 0x06000000, "program_f5044b9b 끝 늘리기");
        확인(nadrzędny_WARTOŚĆ.program_przerwa() == 0x06002000, "program_f5044b9b 끝 반영");
        확인(dziecko_WARTOŚĆ.program_przerwa() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        dziecko_WARTOŚĆ.wyjść_program(7);
        확인(호출.자식기다리기(nadrzędny_WARTOŚĆ, dziecko_WARTOŚĆ.identyfikator_WARTOŚĆ(), false) == (7 << 8), "dziecko_WARTOŚĆ wyjść_program 기다리기");
        확인(호출.접근가능("testy", 1) == -13, "Wykonaj_polecenie pozwolenie_WARTOŚĆ odrzucić_WARTOŚĆ");
        확인(호출.identyfikator_użytkownika() == 0 && 호출.grupa_identyfikator() == 0, "사용자와 무리 identyfikator_WARTOŚĆ");
        확인("/".equals(호출.bieżący_Lista_zadań(2)) && 호출.zmiana_Lista_zadań("/") == 0, "bieżący_towar 작업 wpis_Lista");
        확인(호출.systemy_informacyjne_Terminal(nadrzędny_WARTOŚĆ, 1), "표준 pozycja_wyjścia 단말");
        확인("JGbrOS".equals(호출.System_Szczegóły().System_nazwa()), "system_operacyjny_WARTOŚĆ msinfo32_exe");
    }

    private static void 실행파일시험(jądro jądro_WARTOŚĆ) {
        byte[] dane = new byte[92];
        dane[0] = 0x7f;
        dane[1] = 'E';
        dane[2] = 'L';
        dane[3] = 'F';
        dane[4] = 1;
        dane[5] = 1;
        zapis_liczba_całkowita_WARTOŚĆ(dane, 24, 0x04001000);
        zapis_liczba_całkowita_WARTOŚĆ(dane, 32, 52);
        짧은정수쓰기(dane, 46, 40);
        짧은정수쓰기(dane, 48, 1);
        zapis_liczba_całkowita_WARTOŚĆ(dane, 56, 8);
        zapis_liczba_całkowita_WARTOŚĆ(dane, 60, 2);
        zapis_liczba_całkowita_WARTOŚĆ(dane, 64, 0x04002000);
        zapis_liczba_całkowita_WARTOŚĆ(dane, 72, 64);

        wykonywalny_moduł_ładujący.OBRAZ OBRAZ_WARTOŚĆ = new wykonywalny_moduł_ładujący().검사(dane);
        확인(OBRAZ_WARTOŚĆ.START_ADRES() == 0x04001000, "ELF Uruchom_2 Adres");
        확인(OBRAZ_WARTOŚĆ.구역들().size() == 1 && OBRAZ_WARTOŚĆ.구역들().get(0).Rodzaj_WARTOŚĆ() == 8, "ELF 빈 dane obszar_WARTOŚĆ_366e0bfa");
        int deskryptor_wpis = jądro_WARTOŚĆ.wywołanie_systemowe().Otwórz(jądro_WARTOŚĆ.첫과정(), "testy", wywołanie_systemowe.tylko_do_odczytu_flaga);
        확인(jądro_WARTOŚĆ.wywołanie_systemowe().sterowanie_plikiem(jądro_WARTOŚĆ.첫과정(), deskryptor_wpis, 2, 1) == 0, "Wykonaj_polecenie 시 Zamknięte Ustawienia");
        확인(jądro_WARTOŚĆ.wywołanie_systemowe().Wykonaj_polecenie(jądro_WARTOŚĆ.첫과정(), dane, new String[] {"testy", "값"}, new String[] {"Język=polski"}) == 0, "ELF Wykonaj_polecenie OBRAZ_WARTOŚĆ 적재");
        확인(jądro_WARTOŚĆ.첫과정().wykonanie_START_ADRES() == 0x04001000, "Wykonaj_polecenie Uruchom_2 Adres 반영");
        확인(jądro_WARTOŚĆ.첫과정().wykonanie_argument().length == 2 && jądro_WARTOŚĆ.첫과정().środowisko_WARTOŚĆ().length == 1, "Wykonaj_polecenie 인자와 środowisko");
        확인(!jądro_WARTOŚĆ.첫과정().Plik_deskryptor().systemy_informacyjne_otwarty(deskryptor_wpis), "Wykonaj_polecenie 시 deskryptor_wpis Zamknięte");
        확인(jądro_WARTOŚĆ.쪽관리().바이트읽기(jądro_WARTOŚĆ.첫과정().przestrzeń_adresowa(), 0x04002000) == 0, "빈 dane obszar_WARTOŚĆ_366e0bfa zero_operand inicjuj");
    }

    private static void test_wejście(jądro jądro_WARTOŚĆ) {
        jądro_WARTOŚĆ.입력관리().Klucz_niedziałający('가');
        jądro_WARTOŚĆ.입력관리().쥐이동(3, -2);
        wejście_konkurs 첫사건 = jądro_WARTOŚĆ.입력관리().Dalej_konkurs();
        wejście_konkurs SEKUNDA_konkurs = jądro_WARTOŚĆ.입력관리().Dalej_konkurs();
        확인(첫사건.rodzaj_zdarzenia() == wejście_konkurs.Rodzaj_WARTOŚĆ.Klucz_niedziałający, "자판 Wydarzenie");
        확인(SEKUNDA_konkurs.첫째값() == 3 && SEKUNDA_konkurs.SEKUNDA_WARTOŚĆ() == -2, "쥐 przenosić_WARTOŚĆ Wydarzenie");
    }

    private static void test_sprzęt(host_sprzęt urządzenie_WARTOŚĆ) {
        urządzenie_WARTOŚĆ.zapis_port_bajt(0x3f8, 0xab);
        확인(urządzenie_WARTOŚĆ.포트바이트읽기(0x3f8) == 0xab, "sprzęt_port We_Wy granica_WARTOŚĆ");
        확인(urządzenie_WARTOŚĆ.직렬기록().contains("JGbrOS"), "직렬 LOG_zapis");
    }

    private static void 개입중단과서술자시험() {
        przerwanie_Menedżer Menedżer_WARTOŚĆ = new przerwanie_Menedżer();
        Menedżer_WARTOŚĆ.rejestr_wpis(0x21, Pamięć_ADRES -> Pamięć_ADRES + 4);
        Menedżer_WARTOŚĆ.włączyć();
        확인(Menedżer_WARTOŚĆ.rozproszony_WARTOŚĆ(0x21, 100) == 104, "przerwanie rozproszony_WARTOŚĆ");
        Menedżer_WARTOŚĆ.dezaktywować();
        확인(Menedżer_WARTOŚĆ.rozproszony_WARTOŚĆ(0x21, 100) == 100, "przerwanie dezaktywować");

        Globalna_deskryptor_tabela deskryptor_tabela = new Globalna_deskryptor_tabela();
        deskryptor_tabela.set_wartość_domyślna();
        확인(deskryptor_tabela.조각들().size() == 5, "전역 deskryptor_tabela");
        zadanie_Stan_odcinek zadanie_Stan = new zadanie_Stan_odcinek();
        zadanie_Stan.특권쌓임공간설정(0x10, 0x800000);
        확인(zadanie_Stan.Stos_zero_blok() == 0x10 && zadanie_Stan.Stos_zero_ADRES() == 0x800000, "작업 Stan_WARTOŚĆ obszar_WARTOŚĆ_366e0bfa");
    }

    private static void test_Pamięć_ORAZ_Sieć() {
        고급기술결합장치 urządzenie_magazynujące = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.obszar_zmienić_rozmiar];
        byte[] 읽은자료 = new byte[고급기술결합장치.obszar_zmienić_rozmiar];
        쓸자료[17] = 42;
        urządzenie_magazynujące.Zapis(2, 쓸자료);
        urządzenie_magazynujące.Odczyt(2, 읽은자료);
        확인(읽은자료[17] == 42, "ATA obszar_WARTOŚĆ_366e0bfa 읽고 Zapis");

        akcesorium_magistrala_Menedżer akcesorium = new akcesorium_magistrala_Menedżer();
        akcesorium.발견(new akcesorium_magistrala_Menedżer.urządzenie_WARTOŚĆ(0x1022, 0x2000, 0xc000, 11));
        확인(akcesorium.ZNAJDŹ_wpis(0x1022, 0x2000) != null, "주변 urządzenie_WARTOŚĆ ZNAJDŹ_wpis");

        byte[] Ethernet_kadr = new byte[34];
        Ethernet_kadr[12] = 0x08;
        Ethernet_kadr[13] = 0x00;
        Ethernet_kadr[14] = 0x45;
        확인(sieć_Narzędzia.Ethernet_LITERY_WIELKIE_protokół(Ethernet_kadr) == 0x0800, "이더넷 상위 wartość_kontraktu");
        확인(sieć_Narzędzia.systemy_informacyjne_IPV_4_protokół(Ethernet_kadr, 14), "상호통신망규약 4판");
        확인(sieć_Narzędzia.chmura_suma_kontrolna(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 suma_kontrolna");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        zapis_liczba_całkowita_WARTOŚĆ(첫구역, 454, 63);
        zapis_liczba_całkowita_WARTOŚĆ(첫구역, 458, 1024);
        확인(new partycja_podstawowa_tabela().Odczyt(첫구역).size() == 1, "wartość_domyślna 분할 영역표");

        warstwa_sieciowa warstwa_WARTOŚĆ = new warstwa_sieciowa();
        int[] KWOTA_WYKUP_ILE_LICZB = new int[1];
        warstwa_WARTOŚĆ.rejestr_użytkownik_dane_lekcja(7, (dane, Uruchom_2, długość_WARTOŚĆ) -> KWOTA_WYKUP_ILE_LICZB[0]++);
        byte[] kadr_INDEKS = new byte[14 + 20 + 8];
        kadr_INDEKS[12] = 0x08;
        kadr_INDEKS[13] = 0x00;
        kadr_INDEKS[14] = 0x45;
        kadr_INDEKS[16] = 0;
        kadr_INDEKS[17] = 28;
        kadr_INDEKS[23] = 17;
        kadr_INDEKS[36] = 0;
        kadr_INDEKS[37] = 7;
        확인(warstwa_WARTOŚĆ.odbierać_Ethernet(kadr_INDEKS) && KWOTA_WYKUP_ILE_LICZB[0] == 1, "przestrzeń_użytkownika dane lekcja_WARTOŚĆ rozproszony_WARTOŚĆ");
    }

    private static void 화면과시계시험() {
        znak_wyświetlać 화면 = new znak_wyświetlać();
        화면.pozycja_wyjścia("가나\n다");
        확인(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 pozycja_wyjścia");
        Zegar Zegar = new Zegar(100);
        for (int INDEKS = 0; INDEKS < 10; INDEKS++) {
            Zegar.틱();
        }
        확인(Zegar.지난밀리초() == 100, "Zegar 틱 KONWERTUJ_WARTOŚĆ");
    }

    private static void zapis_liczba_całkowita_WARTOŚĆ(byte[] dane, int pozycja, int WARTOŚĆ) {
        dane[pozycja] = (byte) WARTOŚĆ;
        dane[pozycja + 1] = (byte) (WARTOŚĆ >>> 8);
        dane[pozycja + 2] = (byte) (WARTOŚĆ >>> 16);
        dane[pozycja + 3] = (byte) (WARTOŚĆ >>> 24);
    }

    private static void 짧은정수쓰기(byte[] dane, int pozycja, int WARTOŚĆ) {
        dane[pozycja] = (byte) WARTOŚĆ;
        dane[pozycja + 1] = (byte) (WARTOŚĆ >>> 8);
    }

    private static void 확인(boolean choroba, String Nazwa) {
        if (!choroba) {
            throw new AssertionError("awaria_WARTOŚĆ: " + Nazwa);
        }
        przekazać_ILE_LICZB++;
        System.out.println("przekazać_WARTOŚĆ: " + Nazwa);
    }
}
