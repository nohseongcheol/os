// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** datagram(電文)·Kanal_stavka(通路): 경계를 가진 UDP 자료를 주고받는 učesnik. */
public final class datagram_Kanal {
    private final java.net.DatagramSocket 표준종단;
    private datagram_Kanal(int broj_porta) throws U_I_izuzetak {
        try { 표준종단 = 통신.otvoren(broj_porta);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static datagram_Kanal otvoren(int broj_porta) throws U_I_izuzetak {
        try { return new datagram_Kanal(broj_porta);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void poslati(String adresa, int broj_porta, String podaci) throws U_I_izuzetak {
        try { 통신.poslati(표준종단, adresa, broj_porta, podaci);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public String primiti() throws U_I_izuzetak {
        try { return 통신.primiti(표준종단);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void TIMEOUT(int 밀리초) throws U_I_izuzetak {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public int broj_porta() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Zatvori() { 통신.Zatvori(표준종단); }
}
