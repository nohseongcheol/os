// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** datagram(電文)·Kanal_vnos(通路): 경계를 가진 UDP 자료를 주고받는 končna_točka. */
public final class datagram_Kanal {
    private final java.net.DatagramSocket 표준종단;
    private datagram_Kanal(int številka_vrat) throws V_I_izjema {
        try { 표준종단 = 통신.Odpri(številka_vrat);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static datagram_Kanal Odpri(int številka_vrat) throws V_I_izjema {
        try { return new datagram_Kanal(številka_vrat);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void poslati(String naslov, int številka_vrat, String podatki) throws V_I_izjema {
        try { 통신.poslati(표준종단, naslov, številka_vrat, podatki);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public String sprejeti_sprejemati_prejeti_prejemati() throws V_I_izjema {
        try { return 통신.sprejeti_sprejemati_prejeti_prejemati(표준종단);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void TIMEOUT(int 밀리초) throws V_I_izjema {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public int številka_vrat() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Zapri() { 통신.Zapri(표준종단); }
}
