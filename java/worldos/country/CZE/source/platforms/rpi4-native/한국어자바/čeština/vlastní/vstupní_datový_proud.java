// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;

/** vstup_HODNOTA(入力)과 tok_HODNOTA: 순서대로 들어오는 바이트를 읽는 Kanál_položka. */
public final class vstupní_datový_proud {
    private final java.io.InputStream Standard_tok;
    vstupní_datový_proud(java.io.InputStream Standard_tok) { this.Standard_tok = Standard_tok; }
    public int Čtení() throws vstup_a_výstup_výjimka {
        try { return Standard_tok.read();
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public int Čtení(byte[] data) throws vstup_a_výstup_výjimka {
        try { return Standard_tok.read(data);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public int Čtení(byte[] data, int Spustit_2, int délka_HODNOTA) throws vstup_a_výstup_výjimka {
        try { return Standard_tok.read(data, Spustit_2, délka_HODNOTA);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void Zavřené() throws vstup_a_výstup_výjimka {
        try { Standard_tok.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
}
