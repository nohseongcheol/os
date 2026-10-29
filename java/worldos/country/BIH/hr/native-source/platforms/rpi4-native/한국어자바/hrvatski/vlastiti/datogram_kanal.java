// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** datogram(電文)·kanal_unos(通路): 경계를 가진 UDP 자료를 주고받는 sudionik. */
public final class datogram_kanal {
    private final java.net.DatagramSocket 표준종단;
    private datogram_kanal(int broj_priključka) throws U_I_iznimka {
        try { 표준종단 = 통신.Otvori(broj_priključka);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static datogram_kanal Otvori(int broj_priključka) throws U_I_iznimka {
        try { return new datogram_kanal(broj_priključka);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void slati(String adresa, int broj_priključka, String podaci) throws U_I_iznimka {
        try { 통신.slati(표준종단, adresa, broj_priključka, podaci);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public String primiti() throws U_I_iznimka {
        try { return 통신.primiti(표준종단);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void TIMEOUT(int 밀리초) throws U_I_iznimka {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public int broj_priključka() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Zatvori() { 통신.Zatvori(표준종단); }
}
