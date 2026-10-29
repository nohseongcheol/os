// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** Pripojiť(連結)·Kanál_položka(通路): 상대와 이어진 TCP Byte_VALUE 흐름의 účastník. */
public final class kontakt {
    private final java.net.Socket 표준연결;
    kontakt(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static kontakt Otvoriť(String adresa, int číslo_portu) throws vstup_a_výstup_výnimka {
        try {
            return new kontakt(new java.net.Socket(adresa, číslo_portu));
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public vstupný_prúd_údajov vstup_VALUE() throws vstup_a_výstup_výnimka {
        try { return new vstupný_prúd_údajov(표준연결.getInputStream());
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public výstupný_prúd_údajov Výstup() throws vstup_a_výstup_výnimka {
        try { return new výstupný_prúd_údajov(표준연결.getOutputStream());
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void TIMEOUT(int 밀리초) throws vstup_a_výstup_výnimka {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public int číslo_portu() { return 표준연결.getPort(); }
    public int miestny_číslo_portu() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Zatvoriť() throws vstup_a_výstup_výnimka {
        try { 표준연결.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
}
