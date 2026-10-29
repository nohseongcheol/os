// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** primiti_VALUE(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class primiti_port {
    private final java.net.ServerSocket 표준창구;
    private primiti_port(int broj_porta) throws U_I_izuzetak {
        try { 표준창구 = new java.net.ServerSocket(broj_porta);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static primiti_port otvoren(int broj_porta) throws U_I_izuzetak {
        try { return new primiti_port(broj_porta);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public veza primiti() throws U_I_izuzetak {
        try { return new veza(표준창구.accept());
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public int broj_porta() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws U_I_izuzetak {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Zatvori() throws U_I_izuzetak {
        try { 표준창구.close();
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
}
