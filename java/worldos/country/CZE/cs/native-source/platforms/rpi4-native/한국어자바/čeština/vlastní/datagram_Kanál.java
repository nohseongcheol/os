// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;

/** datagram(電文)·Kanál_položka(通路): 경계를 가진 UDP 자료를 주고받는 účastník. */
public final class datagram_Kanál {
    private final java.net.DatagramSocket Standard_účastník;
    private datagram_Kanál(int číslo_portu) throws vstup_a_výstup_výjimka {
        try { Standard_účastník = komunikace.Otevřít(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static datagram_Kanál Otevřít(int číslo_portu) throws vstup_a_výstup_výjimka {
        try { return new datagram_Kanál(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void poslat(String Adresa, int číslo_portu, String data) throws vstup_a_výstup_výjimka {
        try { komunikace.poslat(Standard_účastník, Adresa, číslo_portu, data);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public String dostat() throws vstup_a_výstup_výjimka {
        try { return komunikace.dostat(Standard_účastník);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void TIMEOUT(int 밀리초) throws vstup_a_výstup_výjimka {
        try { komunikace.TIMEOUT(Standard_účastník, 밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public int číslo_portu() { return Standard_účastník.getLocalPort(); }
    public boolean informační_systémy_uzavřeno() { return Standard_účastník.isClosed(); }
    public void Zavřené() { komunikace.Zavřené(Standard_účastník); }
}
