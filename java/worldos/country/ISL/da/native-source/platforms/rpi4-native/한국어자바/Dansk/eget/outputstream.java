// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** Udgang(出力)과 strøm_VÆRDI: 순서를 보존해 내보내는 바이트의 Kanal_post. */
public final class outputstream {
    private final java.io.OutputStream Standard_strøm;
    outputstream(java.io.OutputStream Standard_strøm) { this.Standard_strøm = Standard_strøm; }
    public void Skrive(int VÆRDI) throws I_O_undtagelse {
        try { Standard_strøm.write(VÆRDI);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void Skrive(byte[] data) throws I_O_undtagelse {
        try { Standard_strøm.write(data);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void Skrive(byte[] data, int Kør_2, int varighed_VÆRDI) throws I_O_undtagelse {
        try { Standard_strøm.write(data, Kør_2, varighed_VÆRDI);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void 내보내기() throws I_O_undtagelse {
        try { Standard_strøm.flush();
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void Luk() throws I_O_undtagelse {
        try { Standard_strøm.close();
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
}
