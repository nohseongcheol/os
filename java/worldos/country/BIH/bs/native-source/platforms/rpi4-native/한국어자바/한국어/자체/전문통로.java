// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·kanal_unos(通路): 경계를 가진 UDP 자료를 주고받는 završna_tačka. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int broj_priključka) throws U_I_izuzetak {
        try { 표준종단 = 통신.Otvori(broj_priključka);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static 전문통로 Otvori(int broj_priključka) throws U_I_izuzetak {
        try { return new 전문통로(broj_priključka);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public void poslati(String adresa, int broj_priključka, String podaci) throws U_I_izuzetak {
        try { 통신.poslati(표준종단, adresa, broj_priključka, podaci);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public String 받기() throws U_I_izuzetak {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public void TIMEOUT(int 밀리초) throws U_I_izuzetak {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public int broj_priključka() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Zatvori() { 통신.Zatvori(표준종단); }
}
