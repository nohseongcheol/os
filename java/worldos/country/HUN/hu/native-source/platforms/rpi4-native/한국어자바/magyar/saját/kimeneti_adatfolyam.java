// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** Kimenet(出力)과 Stream_ÉRTÉK: 순서를 보존해 내보내는 바이트의 Csatorna_bejegyzés. */
public final class kimeneti_adatfolyam {
    private final java.io.OutputStream Standard_Stream;
    kimeneti_adatfolyam(java.io.OutputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public void Írás(int ÉRTÉK) throws I_O_kivétel {
        try { Standard_Stream.write(ÉRTÉK);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void Írás(byte[] adat) throws I_O_kivétel {
        try { Standard_Stream.write(adat);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void Írás(byte[] adat, int Futtatás, int hossz_ÉRTÉK) throws I_O_kivétel {
        try { Standard_Stream.write(adat, Futtatás, hossz_ÉRTÉK);
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void 내보내기() throws I_O_kivétel {
        try { Standard_Stream.flush();
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public void Bezárás() throws I_O_kivétel {
        try { Standard_Stream.close();
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
}
