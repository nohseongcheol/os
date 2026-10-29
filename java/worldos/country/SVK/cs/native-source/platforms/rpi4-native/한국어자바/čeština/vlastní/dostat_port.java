// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;

/** dostat_HODNOTA(受信)·port_HODNOTA(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class dostat_port {
    private final java.net.ServerSocket Standard_port;
    private dostat_port(int číslo_portu) throws vstup_a_výstup_výjimka {
        try { Standard_port = new java.net.ServerSocket(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static dostat_port Otevřít(int číslo_portu) throws vstup_a_výstup_výjimka {
        try { return new dostat_port(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public kontakt dostat() throws vstup_a_výstup_výjimka {
        try { return new kontakt(Standard_port.accept());
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public int číslo_portu() { return Standard_port.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws vstup_a_výstup_výjimka {
        try { Standard_port.setSoTimeout(밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public boolean informační_systémy_uzavřeno() { return Standard_port.isClosed(); }
    public void Zavřené() throws vstup_a_výstup_výjimka {
        try { Standard_port.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
}
