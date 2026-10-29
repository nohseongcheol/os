// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** dostať_VALUE(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class dostať_port {
    private final java.net.ServerSocket 표준창구;
    private dostať_port(int číslo_portu) throws vstup_a_výstup_výnimka {
        try { 표준창구 = new java.net.ServerSocket(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static dostať_port Otvoriť(int číslo_portu) throws vstup_a_výstup_výnimka {
        try { return new dostať_port(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public kontakt dostať() throws vstup_a_výstup_výnimka {
        try { return new kontakt(표준창구.accept());
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public int číslo_portu() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws vstup_a_výstup_výnimka {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Zatvoriť() throws vstup_a_výstup_výnimka {
        try { 표준창구.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
}
