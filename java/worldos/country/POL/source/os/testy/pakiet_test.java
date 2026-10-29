// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** rzeczywisty_dane Java wartość_kontraktu 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class pakiet_test {
    static int powtórzenie_ILE_LICZB = 0;
    static void 확인(boolean WARTOŚĆ) { if (!WARTOŚĆ) throw new AssertionError("case " + powtórzenie_ILE_LICZB); powtórzenie_ILE_LICZB++; }
    static int suma_kontrolna(int[] WARTOŚĆ, int Uruchom_2, int długość_WARTOŚĆ, int stan_początkowy) {
        int SUMA_WARTOŚĆ = stan_początkowy;
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) SUMA_WARTOŚĆ += WARTOŚĆ[Uruchom_2 + INDEKS] << ((INDEKS & 1) == 0 ? 8 : 0);
        SUMA_WARTOŚĆ = (SUMA_WARTOŚĆ & 65535) + (SUMA_WARTOŚĆ >>> 16);
        SUMA_WARTOŚĆ = (SUMA_WARTOŚĆ & 65535) + (SUMA_WARTOŚĆ >>> 16);
        return ~SUMA_WARTOŚĆ & 65535;
    }
    static void Przygotuj(int długość_WARTOŚĆ) {
        sieć_Stos.OCZYŚĆ_Proces();
        확인(sieć_Stos.Otwórz(5000) == 3);
        int[] kadr_INDEKS = sieć_Stos.wejście_kadr;
        Arrays.fill(kadr_INDEKS, 0);
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) kadr_INDEKS[INDEKS] = sieć_sterownik.urządzenie_ADRES[INDEKS];
        sieć_Stos.넣기16(kadr_INDEKS, 12, 0x0800);
        kadr_INDEKS[14] = 0x45; kadr_INDEKS[22] = 64; kadr_INDEKS[23] = 17;
        sieć_Stos.넣기16(kadr_INDEKS, 16, 28 + długość_WARTOŚĆ);
        sieć_Stos.넣기32(kadr_INDEKS, 26, 0x0a000202); sieć_Stos.넣기32(kadr_INDEKS, 30, sieć_Stos.내주소);
        sieć_Stos.넣기16(kadr_INDEKS, 34, 4321); sieć_Stos.넣기16(kadr_INDEKS, 36, 5000); sieć_Stos.넣기16(kadr_INDEKS, 38, długość_WARTOŚĆ + 8);
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) kadr_INDEKS[42 + INDEKS] = INDEKS & 255;
        set_suma_kontrolna(długość_WARTOŚĆ);
    }
    static void set_suma_kontrolna(int długość_WARTOŚĆ) {
        int[] kadr_INDEKS = sieć_Stos.wejście_kadr;
        sieć_Stos.넣기16(kadr_INDEKS, 24, 0); sieć_Stos.넣기16(kadr_INDEKS, 40, 0);
        sieć_Stos.넣기16(kadr_INDEKS, 24, suma_kontrolna(kadr_INDEKS, 14, 20, 0));
        int stan_początkowy = sieć_Stos.가상머리합(sieć_Stos.liczba_całkowita_32(kadr_INDEKS, 26), sieć_Stos.내주소, długość_WARTOŚĆ + 8);
        int SUMA_WARTOŚĆ = suma_kontrolna(kadr_INDEKS, 34, długość_WARTOŚĆ + 8, stan_początkowy);
        sieć_Stos.넣기16(kadr_INDEKS, 40, SUMA_WARTOŚĆ == 0 ? 65535 : SUMA_WARTOŚĆ);
    }
    static void odrzucić_WARTOŚĆ(int długość_WARTOŚĆ) { sieć_Stos.Proces_kadr(długość_WARTOŚĆ); 확인(sieć_Stos.KWOTA_WYKUP_długość[0] == -1); }
    public static void main(String[] argumenty) {
        for (int długość_WARTOŚĆ : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Przygotuj(długość_WARTOŚĆ); sieć_Stos.Proces_kadr(długość_WARTOŚĆ + 42);
            확인(sieć_Stos.KWOTA_WYKUP_długość[0] == długość_WARTOŚĆ);
            확인(sieć_Stos.KWOTA_WYKUP_ADRES[0] == 0x0a000202 && sieć_Stos.KWOTA_WYKUP_numer_portu[0] == 4321);
            for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) 확인(sieć_Stos.KWOTA_WYKUP_dane[INDEKS] == (INDEKS & 255));
        }
        for (int długość_WARTOŚĆ = 0; długość_WARTOŚĆ < 42; długość_WARTOŚĆ++) { Przygotuj(0); odrzucić_WARTOŚĆ(długość_WARTOŚĆ); }
        Przygotuj(1025); odrzucić_WARTOŚĆ(1067);
        Przygotuj(2); sieć_Stos.wejście_kadr[24] ^= 1; odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[42] ^= 1; odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.넣기16(sieć_Stos.wejście_kadr, 38, 7); odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.넣기16(sieć_Stos.wejście_kadr, 38, 65535); odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[14] = 0x4f; odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[14] = 0x44; odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[20] = 0x20; set_suma_kontrolna(2); odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[21] = 1; set_suma_kontrolna(2); odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[33] = 99; set_suma_kontrolna(2); odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[0] ^= 1; odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.wejście_kadr[23] = 6; set_suma_kontrolna(2); odrzucić_WARTOŚĆ(44);
        Przygotuj(2); sieć_Stos.넣기16(sieć_Stos.wejście_kadr, 40, 0); sieć_Stos.Proces_kadr(44); 확인(sieć_Stos.KWOTA_WYKUP_długość[0] == 2);
        int[] WYNIK = new int[4];
        확인(sieć_Stos.odbierać(3, WYNIK, 1, 0) == -90);
        확인(sieć_Stos.odbierać(3, WYNIK, 4, 0) == -11);
        Przygotuj(2); sieć_Stos.Proces_kadr(44); int odrzut_WARTOŚĆ = sieć_Stos.폐기수;
        sieć_Stos.Proces_kadr(44); 확인(sieć_Stos.폐기수 == odrzut_WARTOŚĆ + 1);
        sieć_Stos.OCZYŚĆ_Proces(); 확인(sieć_Stos.Otwórz(5000) == 3);
        확인(sieć_Stos.Otwórz(5000) == -98); 확인(sieć_Stos.Otwórz(0) == 4);
        확인(sieć_Stos.Otwórz(0) == 5); 확인(sieć_Stos.Otwórz(0) == 6); 확인(sieć_Stos.Otwórz(0) == -24);
        확인(sieć_Stos.Zamknięte(4) == 0); 확인(sieć_Stos.Zamknięte(4) == -9);
        sieć_Stos.찾은주소 = sieć_Stos.brama_WARTOŚĆ;
        확인(sieć_Stos.wysłać(3, sieć_Stos.brama_WARTOŚĆ, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = sieć_sterownik.ostatnio_WARTOŚĆ;
        확인(suma_kontrolna(보냄, 14, 20, 0) == 0);
        확인(suma_kontrolna(보냄, 34, 11, sieć_Stos.가상머리합(sieć_Stos.내주소, sieć_Stos.brama_WARTOŚĆ, 11)) == 0);
        확인(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + powtórzenie_ILE_LICZB + " assertions");
    }
}
