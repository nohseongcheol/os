// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;

/** Připojit(連結)·Kanál_položka(通路): 상대와 이어진 TCP bajt_HODNOTA 흐름의 účastník. */
public final class kontakt {
    private final java.net.Socket Standard_knihovna_most;
    kontakt(java.net.Socket Standard_knihovna_most) { this.Standard_knihovna_most = Standard_knihovna_most; }
    public static kontakt Otevřít(String Adresa, int číslo_portu) throws vstup_a_výstup_výjimka {
        try {
            return new kontakt(new java.net.Socket(Adresa, číslo_portu));
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public vstupní_datový_proud vstup_HODNOTA() throws vstup_a_výstup_výjimka {
        try { return new vstupní_datový_proud(Standard_knihovna_most.getInputStream());
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public výstupní_datový_proud výstupní_pozice() throws vstup_a_výstup_výjimka {
        try { return new výstupní_datový_proud(Standard_knihovna_most.getOutputStream());
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void TIMEOUT(int 밀리초) throws vstup_a_výstup_výjimka {
        try { Standard_knihovna_most.setSoTimeout(밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public int číslo_portu() { return Standard_knihovna_most.getPort(); }
    public int místní_číslo_portu() { return Standard_knihovna_most.getLocalPort(); }
    public boolean informační_systémy_uzavřeno() { return Standard_knihovna_most.isClosed(); }
    public boolean 연결됨() { return Standard_knihovna_most.isConnected(); }
    public void Zavřené() throws vstup_a_výstup_výjimka {
        try { Standard_knihovna_most.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
}
