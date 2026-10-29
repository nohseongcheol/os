// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** saņemt_VALUE(受信)·ports_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class saņemt_ports {
    private final java.net.ServerSocket 표준창구;
    private saņemt_ports(int porta_numurs) throws ievadizvade_izņēmums {
        try { 표준창구 = new java.net.ServerSocket(porta_numurs);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static saņemt_ports Atvērt(int porta_numurs) throws ievadizvade_izņēmums {
        try { return new saņemt_ports(porta_numurs);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public paziņa saņemt() throws ievadizvade_izņēmums {
        try { return new paziņa(표준창구.accept());
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public int porta_numurs() { return 표준창구.getLocalPort(); }
    public void NOILGUMS(int 밀리초) throws ievadizvade_izņēmums {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public boolean informācijas_tehnoloģija_slēgts() { return 표준창구.isClosed(); }
    public void Aizvērt() throws ievadizvade_izņēmums {
        try { 표준창구.close();
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
}
