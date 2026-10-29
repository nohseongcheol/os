// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
import java.net.*;
public final class paziņa_transportēšana {
    private paziņa_transportēšana() {}
    public static paziņa Atvērt(String adrese, int porta_numurs) throws ievadizvade_izņēmums {
        try { return paziņa.Atvērt(adrese, porta_numurs);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static saņemt_ports 수신열기(int porta_numurs) throws ievadizvade_izņēmums {
        try { return saņemt_ports.Atvērt(porta_numurs);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static Socket Savienoties(String adrese, int ports_VALUE) throws ievadizvade_izņēmums {
        try { return new Socket(adrese, ports_VALUE);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static ServerSocket klausīties_dalībnieks(int ports_VALUE) throws ievadizvade_izņēmums {
        try { return new ServerSocket(ports_VALUE);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static Socket saņemt(ServerSocket serveris_VALUE) throws ievadizvade_izņēmums {
        try { return serveris_VALUE.accept();
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
}
