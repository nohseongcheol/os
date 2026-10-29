// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** datagram(電文)·Kanál_položka(通路): 경계를 가진 UDP 자료를 주고받는 účastník. */
public final class datagram_Kanál {
    private final java.net.DatagramSocket 표준종단;
    private datagram_Kanál(int číslo_portu) throws vstup_a_výstup_výnimka {
        try { 표준종단 = 통신.Otvoriť(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static datagram_Kanál Otvoriť(int číslo_portu) throws vstup_a_výstup_výnimka {
        try { return new datagram_Kanál(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void odoslať(String adresa, int číslo_portu, String údaje) throws vstup_a_výstup_výnimka {
        try { 통신.odoslať(표준종단, adresa, číslo_portu, údaje);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public String dostať() throws vstup_a_výstup_výnimka {
        try { return 통신.dostať(표준종단);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void TIMEOUT(int 밀리초) throws vstup_a_výstup_výnimka {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public int číslo_portu() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Zatvoriť() { 통신.Zatvoriť(표준종단); }
}
