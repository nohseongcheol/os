// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** rzeczywisty_dane rozruch_maszyny 후 호출되는 Java punkt_wejścia. JVM과 host 운영체제에 의존하지 않는다. */
public final class jądro {
    static int suma_WARTOŚĆ(int 끝) {
        int SUMA_WARTOŚĆ = 0;
        for (int INDEKS = 1; INDEKS <= 끝; INDEKS++) SUMA_WARTOŚĆ += INDEKS;
        return SUMA_WARTOŚĆ;
    }

    static boolean testy() {
        int[] 값들 = new int[4];
        값들[2] = suma_WARTOŚĆ(10);
        int negatywny_WARTOŚĆ = -7;
        int 최소 = 0x80000000;
        int Dywizja_KR = -1;
        int INDEKS = Pamięć_region.przydzielić_Pamięć();
        boolean przekazać_WARTOŚĆ = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && negatywny_WARTOŚĆ / 3 == -2 && negatywny_WARTOŚĆ % 3 == -1 && 최소 / Dywizja_KR == 최소
            && 최소 % Dywizja_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEKS >= 0 && Pamięć_region.Zwrot_KR(INDEKS) && !Pamięć_region.Zwrot_KR(INDEKS);
        SMS_Terminal.Zapis(przekazać_WARTOŚĆ ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return przekazać_WARTOŚĆ;
    }

    public static void Uruchom_2() {
        SMS_Terminal.Przygotuj();
        SMS_Terminal.Zapis("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Zapis("자바 기계어 jądro_WARTOŚĆ Uruchom_2\n");
        if (urządzenie_WARTOŚĆ.부팅표식() != 0x2badb002) {
            SMS_Terminal.Zapis("BAD MULTIBOOT MAGIC\n");
            urządzenie_WARTOŚĆ.정지();
        }
        if (!testy()) urządzenie_WARTOŚĆ.정지();
        if (Pamięć_region.LITERY_WIELKIE_Pamięć_zmienić_rozmiar() < 15360) {
            SMS_Terminal.Zapis("At least 16 MiB RAM required\n");
            urządzenie_WARTOŚĆ.정지();
        }
        urządzenie_WARTOŚĆ.Przygotuj_użytkownik_program();
        SMS_Terminal.Zapis("USER ELF: ring 3 / paging / int 0x80\n");
        sieć_sterownik.Przygotuj();
        sieć_Stos.OCZYŚĆ_Proces();
        Pamięć_system_plików.Przygotuj();
        파일보존.Przygotuj();
        polecenie_interpreter.Uruchom_2();
    }
}
