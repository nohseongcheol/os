// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
import java.net.*;
public final class ismerős_szállítás {
    private ismerős_szállítás() {}
    public static ismerős Megnyitás(String CÍM, int portszám) throws I_O_kivétel {
        try { return ismerős.Megnyitás(CÍM, portszám);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static fogad_port 수신열기(int portszám) throws I_O_kivétel {
        try { return fogad_port.Megnyitás(portszám);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static Socket Kapcsolódás(String CÍM, int port_ÉRTÉK) throws I_O_kivétel {
        try { return new Socket(CÍM, port_ÉRTÉK);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static ServerSocket figyelés_végpont(int port_ÉRTÉK) throws I_O_kivétel {
        try { return new ServerSocket(port_ÉRTÉK);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static Socket fogad(ServerSocket kiszolgáló_ÉRTÉK) throws I_O_kivétel {
        try { return kiszolgáló_ÉRTÉK.accept();
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
}
