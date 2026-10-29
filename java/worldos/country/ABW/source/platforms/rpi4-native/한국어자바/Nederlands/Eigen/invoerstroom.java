// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** invoer_WAARDE(入力)과 Stream_WAARDE: 순서대로 들어오는 바이트를 읽는 Kanaal_invoer. */
public final class invoerstroom {
    private final java.io.InputStream Standard_Stream;
    invoerstroom(java.io.InputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public int Lezen() throws I_O_uitzondering {
        try { return Standard_Stream.read();
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public int Lezen(byte[] gegevens) throws I_O_uitzondering {
        try { return Standard_Stream.read(gegevens);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public int Lezen(byte[] gegevens, int starten, int tijdsduur_WAARDE) throws I_O_uitzondering {
        try { return Standard_Stream.read(gegevens, starten, tijdsduur_WAARDE);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void Sluiten() throws I_O_uitzondering {
        try { Standard_Stream.close();
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
}
