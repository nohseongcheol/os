// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static veza Otvori(String adresa, int broj_priključka) throws U_I_izuzetak {
        try { return veza.Otvori(adresa, broj_priključka);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static 수신창구 수신열기(int broj_priključka) throws U_I_izuzetak {
        try { return 수신창구.Otvori(broj_priključka);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static Socket Spoji_se(String adresa, int port_VALUE) throws U_I_izuzetak {
        try { return new Socket(adresa, port_VALUE);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static ServerSocket slušati_završna_tačka(int port_VALUE) throws U_I_izuzetak {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static Socket 받기(ServerSocket server_VALUE) throws U_I_izuzetak {
        try { return server_VALUE.accept();
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
}
