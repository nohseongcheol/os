// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** datagram(電文)·Csatorna_bejegyzés(通路): 경계를 가진 UDP 자료를 주고받는 végpont. */
public final class datagram_Csatorna {
    private final java.net.DatagramSocket Standard_végpont;
    private datagram_Csatorna(int portszám) throws I_O_kivétel {
        try { Standard_végpont = kommunikáció.Megnyitás(portszám);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static datagram_Csatorna Megnyitás(int portszám) throws I_O_kivétel {
        try { return new datagram_Csatorna(portszám);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void küld(String CÍM, int portszám, String adat) throws I_O_kivétel {
        try { kommunikáció.küld(Standard_végpont, CÍM, portszám, adat);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public String fogad() throws I_O_kivétel {
        try { return kommunikáció.fogad(Standard_végpont);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void IDŐTÚLLÉPÉS(int 밀리초) throws I_O_kivétel {
        try { kommunikáció.IDŐTÚLLÉPÉS(Standard_végpont, 밀리초);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public int portszám() { return Standard_végpont.getLocalPort(); }
    public boolean informatikai_részleg_lezárt() { return Standard_végpont.isClosed(); }
    public void Bezárás() { kommunikáció.Bezárás(Standard_végpont); }
}
