// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** ontvangen_WAARDE(受信)·poort_WAARDE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class ontvangen_poort {
    private final java.net.ServerSocket Standard_poort;
    private ontvangen_poort(int poortnummer) throws I_O_uitzondering {
        try { Standard_poort = new java.net.ServerSocket(poortnummer);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static ontvangen_poort Openen(int poortnummer) throws I_O_uitzondering {
        try { return new ontvangen_poort(poortnummer);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public verbinding ontvangen() throws I_O_uitzondering {
        try { return new verbinding(Standard_poort.accept());
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public int poortnummer() { return Standard_poort.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_uitzondering {
        try { Standard_poort.setSoTimeout(밀리초);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public boolean informatie_afgesloten() { return Standard_poort.isClosed(); }
    public void Sluiten() throws I_O_uitzondering {
        try { Standard_poort.close();
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
}
