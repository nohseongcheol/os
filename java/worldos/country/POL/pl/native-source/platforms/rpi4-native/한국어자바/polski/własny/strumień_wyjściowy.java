// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** pozycja_wyjścia(出力)과 Stream_WARTOŚĆ: 순서를 보존해 내보내는 바이트의 Kanał_wpis. */
public final class strumień_wyjściowy {
    private final java.io.OutputStream Standard_Stream;
    strumień_wyjściowy(java.io.OutputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public void Zapis(int WARTOŚĆ) throws We_Wy_wyjątek {
        try { Standard_Stream.write(WARTOŚĆ);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void Zapis(byte[] dane) throws We_Wy_wyjątek {
        try { Standard_Stream.write(dane);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void Zapis(byte[] dane, int Uruchom_2, int długość_WARTOŚĆ) throws We_Wy_wyjątek {
        try { Standard_Stream.write(dane, Uruchom_2, długość_WARTOŚĆ);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void 내보내기() throws We_Wy_wyjątek {
        try { Standard_Stream.flush();
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void Zamknięte() throws We_Wy_wyjątek {
        try { Standard_Stream.close();
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
}
