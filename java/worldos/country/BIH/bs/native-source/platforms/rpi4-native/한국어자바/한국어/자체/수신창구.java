// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int broj_priključka) throws U_I_izuzetak {
        try { 표준창구 = new java.net.ServerSocket(broj_priključka);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static 수신창구 Otvori(int broj_priključka) throws U_I_izuzetak {
        try { return new 수신창구(broj_priključka);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public veza 받기() throws U_I_izuzetak {
        try { return new veza(표준창구.accept());
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public int broj_priključka() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws U_I_izuzetak {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Zatvori() throws U_I_izuzetak {
        try { 표준창구.close();
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
}
