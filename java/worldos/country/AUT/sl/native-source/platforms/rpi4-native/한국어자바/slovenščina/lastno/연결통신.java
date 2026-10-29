// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static povezava Odpri(String naslov, int številka_vrat) throws V_I_izjema {
        try { return povezava.Odpri(naslov, številka_vrat);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static sprejeti_sprejemati_prejeti_prejemati_vrata 수신열기(int številka_vrat) throws V_I_izjema {
        try { return sprejeti_sprejemati_prejeti_prejemati_vrata.Odpri(številka_vrat);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static Socket Poveži(String naslov, int vrata_VALUE) throws V_I_izjema {
        try { return new Socket(naslov, vrata_VALUE);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static ServerSocket poslušati_končna_točka(int vrata_VALUE) throws V_I_izjema {
        try { return new ServerSocket(vrata_VALUE);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static Socket sprejeti_sprejemati_prejeti_prejemati(ServerSocket strežnik_VALUE) throws V_I_izjema {
        try { return strežnik_VALUE.accept();
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
}
