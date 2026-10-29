// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** wejście_WARTOŚĆ(入力)과 Stream_WARTOŚĆ: 순서대로 들어오는 바이트를 읽는 Kanał_wpis. */
public final class strumień_wejściowy {
    private final java.io.InputStream Standard_Stream;
    strumień_wejściowy(java.io.InputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public int Odczyt() throws We_Wy_wyjątek {
        try { return Standard_Stream.read();
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public int Odczyt(byte[] dane) throws We_Wy_wyjątek {
        try { return Standard_Stream.read(dane);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public int Odczyt(byte[] dane, int Uruchom_2, int długość_WARTOŚĆ) throws We_Wy_wyjątek {
        try { return Standard_Stream.read(dane, Uruchom_2, długość_WARTOŚĆ);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void Zamknięte() throws We_Wy_wyjątek {
        try { Standard_Stream.close();
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
}
