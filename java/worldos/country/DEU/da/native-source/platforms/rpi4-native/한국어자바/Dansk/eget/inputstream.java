// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** input_VÆRDI(入力)과 strøm_VÆRDI: 순서대로 들어오는 바이트를 읽는 Kanal_post. */
public final class inputstream {
    private final java.io.InputStream Standard_strøm;
    inputstream(java.io.InputStream Standard_strøm) { this.Standard_strøm = Standard_strøm; }
    public int Læse() throws I_O_undtagelse {
        try { return Standard_strøm.read();
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public int Læse(byte[] data) throws I_O_undtagelse {
        try { return Standard_strøm.read(data);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public int Læse(byte[] data, int Kør_2, int varighed_VÆRDI) throws I_O_undtagelse {
        try { return Standard_strøm.read(data, Kør_2, varighed_VÆRDI);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void Luk() throws I_O_undtagelse {
        try { Standard_strøm.close();
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
}
