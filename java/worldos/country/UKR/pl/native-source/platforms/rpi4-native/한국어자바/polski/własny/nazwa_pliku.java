// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 przestrzeń_użytkownika 용어를 보존한다. bieżący_towar 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class nazwa_pliku {
    private nazwa_pliku() {}
    public static byte[] 바이트읽기(String Nazwa) throws We_Wy_wyjątek {
        try {
        FileInputStream Stream_WARTOŚĆ = new FileInputStream(Nazwa);
        try {
            byte[] 임시 = new byte[16384]; int identyfikator = 0, WARTOŚĆ;
            while ((WARTOŚĆ = Stream_WARTOŚĆ.read()) != -1) { if (identyfikator == 임시.length) throw new We_Wy_wyjątek("nazwa_pliku Rozmiar 제한"); 임시[identyfikator++] = (byte)WARTOŚĆ; }
            byte[] WYNIK = new byte[identyfikator]; System.arraycopy(임시, 0, WYNIK, 0, identyfikator); return WYNIK;
        } finally { Stream_WARTOŚĆ.close(); }
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static void zapis_bajt_WARTOŚĆ(String Nazwa, byte[] treść_WARTOŚĆ_cb0f2404) throws We_Wy_wyjątek {
        try {
        FileOutputStream Stream_WARTOŚĆ = new FileOutputStream(Nazwa);
        try { for (int Loop_INDEKS = 0; Loop_INDEKS < treść_WARTOŚĆ_cb0f2404.length; Loop_INDEKS++) Stream_WARTOŚĆ.write(treść_WARTOŚĆ_cb0f2404[Loop_INDEKS] & 255); } finally { Stream_WARTOŚĆ.close(); }
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static String Odczyt(String Nazwa) throws We_Wy_wyjątek {
        try { return 문자.odszyfrować_dane(바이트읽기(Nazwa));
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static void Zapis(String Nazwa, String treść_WARTOŚĆ_cb0f2404) throws We_Wy_wyjątek {
        try { zapis_bajt_WARTOŚĆ(Nazwa, 문자.kodować(treść_WARTOŚĆ_cb0f2404));
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
}
