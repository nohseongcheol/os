// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** 입력(入力)과 tok_VALUE: 순서대로 들어오는 바이트를 읽는 kanal_unos. */
public final class ulazni_tok {
    private final java.io.InputStream 표준흐름;
    ulazni_tok(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Čitaj() throws U_I_iznimka {
        try { return 표준흐름.read();
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public int Čitaj(byte[] podaci) throws U_I_iznimka {
        try { return 표준흐름.read(podaci);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public int Čitaj(byte[] podaci, int Pokreni, int 길이) throws U_I_iznimka {
        try { return 표준흐름.read(podaci, Pokreni, 길이);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void Zatvori() throws U_I_iznimka {
        try { 표준흐름.close();
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
}
