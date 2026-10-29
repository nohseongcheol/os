// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** Utgang(出力)과 strøm_VERDI: 순서를 보존해 내보내는 바이트의 Kanal_oppføring. */
public final class utdataflyt {
    private final java.io.OutputStream Standard_strøm;
    utdataflyt(java.io.OutputStream Standard_strøm) { this.Standard_strøm = Standard_strøm; }
    public void Skriv(int VERDI) throws I_U_unntak {
        try { Standard_strøm.write(VERDI);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void Skriv(byte[] data) throws I_U_unntak {
        try { Standard_strøm.write(data);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void Skriv(byte[] data, int Kjør_2, int lengde_VERDI) throws I_U_unntak {
        try { Standard_strøm.write(data, Kjør_2, lengde_VERDI);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void 내보내기() throws I_U_unntak {
        try { Standard_strøm.flush();
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void Lukk() throws I_U_unntak {
        try { Standard_strøm.close();
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
}
