// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** sprejeti_sprejemati_prejeti_prejemati_VALUE(受信)·vrata_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class sprejeti_sprejemati_prejeti_prejemati_vrata {
    private final java.net.ServerSocket 표준창구;
    private sprejeti_sprejemati_prejeti_prejemati_vrata(int številka_vrat) throws V_I_izjema {
        try { 표준창구 = new java.net.ServerSocket(številka_vrat);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static sprejeti_sprejemati_prejeti_prejemati_vrata Odpri(int številka_vrat) throws V_I_izjema {
        try { return new sprejeti_sprejemati_prejeti_prejemati_vrata(številka_vrat);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public povezava sprejeti_sprejemati_prejeti_prejemati() throws V_I_izjema {
        try { return new povezava(표준창구.accept());
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public int številka_vrat() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws V_I_izjema {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Zapri() throws V_I_izjema {
        try { 표준창구.close();
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
}
