// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;

/** výstupní_pozice(出力)과 tok_HODNOTA: 순서를 보존해 내보내는 바이트의 Kanál_položka. */
public final class výstupní_datový_proud {
    private final java.io.OutputStream Standard_tok;
    výstupní_datový_proud(java.io.OutputStream Standard_tok) { this.Standard_tok = Standard_tok; }
    public void Zápis(int HODNOTA) throws vstup_a_výstup_výjimka {
        try { Standard_tok.write(HODNOTA);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void Zápis(byte[] data) throws vstup_a_výstup_výjimka {
        try { Standard_tok.write(data);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void Zápis(byte[] data, int Spustit_2, int délka_HODNOTA) throws vstup_a_výstup_výjimka {
        try { Standard_tok.write(data, Spustit_2, délka_HODNOTA);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void 내보내기() throws vstup_a_výstup_výjimka {
        try { Standard_tok.flush();
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public void Zavřené() throws vstup_a_výstup_výjimka {
        try { Standard_tok.close();
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
}
