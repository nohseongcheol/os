// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** indata_värde(入力)과 flöde_värde: 순서대로 들어오는 바이트를 읽는 Kanal_post. */
public final class indataström {
    private final java.io.InputStream Standard_flöde;
    indataström(java.io.InputStream Standard_flöde) { this.Standard_flöde = Standard_flöde; }
    public int Läs() throws indata_utleverans_fel {
        try { return Standard_flöde.read();
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public int Läs(byte[] data) throws indata_utleverans_fel {
        try { return Standard_flöde.read(data);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public int Läs(byte[] data, int Kör, int längd_värde) throws indata_utleverans_fel {
        try { return Standard_flöde.read(data, Kör, längd_värde);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void Stäng() throws indata_utleverans_fel {
        try { Standard_flöde.close();
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
}
