// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** fogad_ÉRTÉK(受信)·port_ÉRTÉK(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class fogad_port {
    private final java.net.ServerSocket Standard_port;
    private fogad_port(int portszám) throws I_O_kivétel {
        try { Standard_port = new java.net.ServerSocket(portszám);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static fogad_port Megnyitás(int portszám) throws I_O_kivétel {
        try { return new fogad_port(portszám);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public ismerős fogad() throws I_O_kivétel {
        try { return new ismerős(Standard_port.accept());
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public int portszám() { return Standard_port.getLocalPort(); }
    public void IDŐTÚLLÉPÉS(int 밀리초) throws I_O_kivétel {
        try { Standard_port.setSoTimeout(밀리초);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public boolean informatikai_részleg_lezárt() { return Standard_port.isClosed(); }
    public void Bezárás() throws I_O_kivétel {
        try { Standard_port.close();
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
}
