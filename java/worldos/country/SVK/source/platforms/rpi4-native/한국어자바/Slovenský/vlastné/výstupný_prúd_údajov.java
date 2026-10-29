// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** Výstup(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 Kanál_položka. */
public final class výstupný_prúd_údajov {
    private final java.io.OutputStream 표준흐름;
    výstupný_prúd_údajov(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Zápis(int VALUE) throws vstup_a_výstup_výnimka {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void Zápis(byte[] údaje) throws vstup_a_výstup_výnimka {
        try { 표준흐름.write(údaje);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void Zápis(byte[] údaje, int Spustiť_2, int dĺžka_VALUE) throws vstup_a_výstup_výnimka {
        try { 표준흐름.write(údaje, Spustiť_2, dĺžka_VALUE);
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void 내보내기() throws vstup_a_výstup_výnimka {
        try { 표준흐름.flush();
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public void Zatvoriť() throws vstup_a_výstup_výnimka {
        try { 표준흐름.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
}
