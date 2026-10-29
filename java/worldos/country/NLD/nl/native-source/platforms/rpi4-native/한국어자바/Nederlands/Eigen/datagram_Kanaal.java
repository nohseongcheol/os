// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** datagram(電文)·Kanaal_invoer(通路): 경계를 가진 UDP 자료를 주고받는 eindpunt. */
public final class datagram_Kanaal {
    private final java.net.DatagramSocket Standard_eindpunt;
    private datagram_Kanaal(int poortnummer) throws I_O_uitzondering {
        try { Standard_eindpunt = communicatie.Openen(poortnummer);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static datagram_Kanaal Openen(int poortnummer) throws I_O_uitzondering {
        try { return new datagram_Kanaal(poortnummer);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void e_mailen(String ADRES, int poortnummer, String gegevens) throws I_O_uitzondering {
        try { communicatie.e_mailen(Standard_eindpunt, ADRES, poortnummer, gegevens);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public String ontvangen() throws I_O_uitzondering {
        try { return communicatie.ontvangen(Standard_eindpunt);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_uitzondering {
        try { communicatie.TIMEOUT(Standard_eindpunt, 밀리초);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public int poortnummer() { return Standard_eindpunt.getLocalPort(); }
    public boolean informatie_afgesloten() { return Standard_eindpunt.isClosed(); }
    public void Sluiten() { communicatie.Sluiten(Standard_eindpunt); }
}
