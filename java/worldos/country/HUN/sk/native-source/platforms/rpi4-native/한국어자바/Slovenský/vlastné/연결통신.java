// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static kontakt Otvoriť(String adresa, int číslo_portu) throws vstup_a_výstup_výnimka {
        try { return kontakt.Otvoriť(adresa, číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static dostať_port 수신열기(int číslo_portu) throws vstup_a_výstup_výnimka {
        try { return dostať_port.Otvoriť(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static Socket Pripojiť(String adresa, int port_VALUE) throws vstup_a_výstup_výnimka {
        try { return new Socket(adresa, port_VALUE);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static ServerSocket načúvať_účastník(int port_VALUE) throws vstup_a_výstup_výnimka {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static Socket dostať(ServerSocket server_VALUE) throws vstup_a_výstup_výnimka {
        try { return server_VALUE.accept();
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
}
