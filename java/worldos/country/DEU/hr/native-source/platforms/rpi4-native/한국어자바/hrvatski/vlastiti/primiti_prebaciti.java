// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** primiti_VALUE(受信)·prebaciti_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class primiti_prebaciti {
    private final java.net.ServerSocket 표준창구;
    private primiti_prebaciti(int broj_priključka) throws U_I_iznimka {
        try { 표준창구 = new java.net.ServerSocket(broj_priključka);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static primiti_prebaciti Otvori(int broj_priključka) throws U_I_iznimka {
        try { return new primiti_prebaciti(broj_priključka);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public veza primiti() throws U_I_iznimka {
        try { return new veza(표준창구.accept());
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public int broj_priključka() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws U_I_iznimka {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Zatvori() throws U_I_iznimka {
        try { 표준창구.close();
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
}
