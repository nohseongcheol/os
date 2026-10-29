// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static veza otvoren(String adresa, int broj_porta) throws U_I_izuzetak {
        try { return veza.otvoren(adresa, broj_porta);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static primiti_port 수신열기(int broj_porta) throws U_I_izuzetak {
        try { return primiti_port.otvoren(broj_porta);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static Socket veze(String adresa, int port_VALUE) throws U_I_izuzetak {
        try { return new Socket(adresa, port_VALUE);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static ServerSocket slušati_učesnik(int port_VALUE) throws U_I_izuzetak {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static Socket primiti(ServerSocket server_VALUE) throws U_I_izuzetak {
        try { return server_VALUE.accept();
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
}
