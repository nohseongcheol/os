// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** Poveži(連結)·Kanal_vnos(通路): 상대와 이어진 TCP bajt_VALUE 흐름의 končna_točka. */
public final class povezava {
    private final java.net.Socket 표준연결;
    povezava(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static povezava Odpri(String naslov, int številka_vrat) throws V_I_izjema {
        try {
            return new povezava(new java.net.Socket(naslov, številka_vrat));
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public vhodni_tok 입력() throws V_I_izjema {
        try { return new vhodni_tok(표준연결.getInputStream());
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public izhodni_tok Izpis() throws V_I_izjema {
        try { return new izhodni_tok(표준연결.getOutputStream());
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void TIMEOUT(int 밀리초) throws V_I_izjema {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public int številka_vrat() { return 표준연결.getPort(); }
    public int lokalen_krajeven_številka_vrat() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Zapri() throws V_I_izjema {
        try { 표준연결.close();
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
}
