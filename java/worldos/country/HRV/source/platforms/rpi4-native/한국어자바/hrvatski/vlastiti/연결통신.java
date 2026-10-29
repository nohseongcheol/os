// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static veza Otvori(String adresa, int broj_priključka) throws U_I_iznimka {
        try { return veza.Otvori(adresa, broj_priključka);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static primiti_prebaciti 수신열기(int broj_priključka) throws U_I_iznimka {
        try { return primiti_prebaciti.Otvori(broj_priključka);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static Socket Spoji_se(String adresa, int prebaciti_VALUE) throws U_I_iznimka {
        try { return new Socket(adresa, prebaciti_VALUE);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static ServerSocket osluškivati_sudionik(int prebaciti_VALUE) throws U_I_iznimka {
        try { return new ServerSocket(prebaciti_VALUE);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static Socket primiti(ServerSocket server_VALUE) throws U_I_iznimka {
        try { return server_VALUE.accept();
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
}
