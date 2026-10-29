// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** utmatningsposition(出力)과 flöde_värde: 순서를 보존해 내보내는 바이트의 Kanal_post. */
public final class utdataström {
    private final java.io.OutputStream Standard_flöde;
    utdataström(java.io.OutputStream Standard_flöde) { this.Standard_flöde = Standard_flöde; }
    public void Skriv(int värde) throws indata_utleverans_fel {
        try { Standard_flöde.write(värde);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void Skriv(byte[] data) throws indata_utleverans_fel {
        try { Standard_flöde.write(data);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void Skriv(byte[] data, int Kör, int längd_värde) throws indata_utleverans_fel {
        try { Standard_flöde.write(data, Kör, längd_värde);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void 내보내기() throws indata_utleverans_fel {
        try { Standard_flöde.flush();
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void Stäng() throws indata_utleverans_fel {
        try { Standard_flöde.close();
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
}
