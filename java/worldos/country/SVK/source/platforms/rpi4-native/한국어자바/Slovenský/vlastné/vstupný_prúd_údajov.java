// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** vstup_VALUE(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 Kanál_položka. */
public final class vstupný_prúd_údajov {
    private final java.io.InputStream 표준흐름;
    vstupný_prúd_údajov(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Čítanie() throws vstup_a_výstup_výnimka {
        try { return 표준흐름.read();
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public int Čítanie(byte[] údaje) throws vstup_a_výstup_výnimka {
        try { return 표준흐름.read(údaje);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public int Čítanie(byte[] údaje, int Spustiť_2, int dĺžka_VALUE) throws vstup_a_výstup_výnimka {
        try { return 표준흐름.read(údaje, Spustiť_2, dĺžka_VALUE);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void Zatvoriť() throws vstup_a_výstup_výnimka {
        try { 표준흐름.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
}
