// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** bevitel_ÉRTÉK(入力)과 Stream_ÉRTÉK: 순서대로 들어오는 바이트를 읽는 Csatorna_bejegyzés. */
public final class bemeneti_adatfolyam {
    private final java.io.InputStream Standard_Stream;
    bemeneti_adatfolyam(java.io.InputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public int Olvasás() throws I_O_kivétel {
        try { return Standard_Stream.read();
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public int Olvasás(byte[] adat) throws I_O_kivétel {
        try { return Standard_Stream.read(adat);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public int Olvasás(byte[] adat, int Futtatás, int hossz_ÉRTÉK) throws I_O_kivétel {
        try { return Standard_Stream.read(adat, Futtatás, hossz_ÉRTÉK);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void Bezárás() throws I_O_kivétel {
        try { Standard_Stream.close();
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
}
