// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** Izlaz(出力)과 tok_VALUE: 순서를 보존해 내보내는 바이트의 kanal_unos. */
public final class izlazni_tok {
    private final java.io.OutputStream 표준흐름;
    izlazni_tok(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Zapisuj(int VALUE) throws U_I_iznimka {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void Zapisuj(byte[] podaci) throws U_I_iznimka {
        try { 표준흐름.write(podaci);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void Zapisuj(byte[] podaci, int Pokreni, int 길이) throws U_I_iznimka {
        try { 표준흐름.write(podaci, Pokreni, 길이);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void 내보내기() throws U_I_iznimka {
        try { 표준흐름.flush();
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void Zatvori() throws U_I_iznimka {
        try { 표준흐름.close();
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
}
