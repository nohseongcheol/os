// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** inndata_VERDI(入力)과 strøm_VERDI: 순서대로 들어오는 바이트를 읽는 Kanal_oppføring. */
public final class inndataflyt {
    private final java.io.InputStream Standard_strøm;
    inndataflyt(java.io.InputStream Standard_strøm) { this.Standard_strøm = Standard_strøm; }
    public int Les() throws I_U_unntak {
        try { return Standard_strøm.read();
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public int Les(byte[] data) throws I_U_unntak {
        try { return Standard_strøm.read(data);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public int Les(byte[] data, int Kjør_2, int lengde_VERDI) throws I_U_unntak {
        try { return Standard_strøm.read(data, Kjør_2, lengde_VERDI);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void Lukk() throws I_U_unntak {
        try { Standard_strøm.close();
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
}
