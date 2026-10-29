// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** Verbinden(連結)·Kanaal_invoer(通路): 상대와 이어진 TCP byte_WAARDE 흐름의 eindpunt. */
public final class verbinding {
    private final java.net.Socket Standard_bibliotheek_brug;
    verbinding(java.net.Socket Standard_bibliotheek_brug) { this.Standard_bibliotheek_brug = Standard_bibliotheek_brug; }
    public static verbinding Openen(String ADRES, int poortnummer) throws I_O_uitzondering {
        try {
            return new verbinding(new java.net.Socket(ADRES, poortnummer));
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public invoerstroom invoer_WAARDE() throws I_O_uitzondering {
        try { return new invoerstroom(Standard_bibliotheek_brug.getInputStream());
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public uitvoerstroom tekstuitvoer() throws I_O_uitzondering {
        try { return new uitvoerstroom(Standard_bibliotheek_brug.getOutputStream());
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_uitzondering {
        try { Standard_bibliotheek_brug.setSoTimeout(밀리초);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public int poortnummer() { return Standard_bibliotheek_brug.getPort(); }
    public int lokaal_poortnummer() { return Standard_bibliotheek_brug.getLocalPort(); }
    public boolean informatie_afgesloten() { return Standard_bibliotheek_brug.isClosed(); }
    public boolean 연결됨() { return Standard_bibliotheek_brug.isConnected(); }
    public void Sluiten() throws I_O_uitzondering {
        try { Standard_bibliotheek_brug.close();
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
}
