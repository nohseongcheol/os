// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** Kapcsolódás(連結)·Csatorna_bejegyzés(通路): 상대와 이어진 TCP bájt_ÉRTÉK 흐름의 végpont. */
public final class ismerős {
    private final java.net.Socket Standard_kódtár_híd;
    ismerős(java.net.Socket Standard_kódtár_híd) { this.Standard_kódtár_híd = Standard_kódtár_híd; }
    public static ismerős Megnyitás(String CÍM, int portszám) throws I_O_kivétel {
        try {
            return new ismerős(new java.net.Socket(CÍM, portszám));
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public bemeneti_adatfolyam bevitel_ÉRTÉK() throws I_O_kivétel {
        try { return new bemeneti_adatfolyam(Standard_kódtár_híd.getInputStream());
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public kimeneti_adatfolyam Kimenet() throws I_O_kivétel {
        try { return new kimeneti_adatfolyam(Standard_kódtár_híd.getOutputStream());
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void IDŐTÚLLÉPÉS(int 밀리초) throws I_O_kivétel {
        try { Standard_kódtár_híd.setSoTimeout(밀리초);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public int portszám() { return Standard_kódtár_híd.getPort(); }
    public int helyi_portszám() { return Standard_kódtár_híd.getLocalPort(); }
    public boolean informatikai_részleg_lezárt() { return Standard_kódtár_híd.isClosed(); }
    public boolean 연결됨() { return Standard_kódtár_híd.isConnected(); }
    public void Bezárás() throws I_O_kivétel {
        try { Standard_kódtár_híd.close();
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
}
