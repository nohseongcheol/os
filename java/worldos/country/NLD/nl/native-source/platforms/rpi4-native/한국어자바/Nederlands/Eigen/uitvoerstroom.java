// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** tekstuitvoer(出力)과 Stream_WAARDE: 순서를 보존해 내보내는 바이트의 Kanaal_invoer. */
public final class uitvoerstroom {
    private final java.io.OutputStream Standard_Stream;
    uitvoerstroom(java.io.OutputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public void Schrijven(int WAARDE) throws I_O_uitzondering {
        try { Standard_Stream.write(WAARDE);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void Schrijven(byte[] gegevens) throws I_O_uitzondering {
        try { Standard_Stream.write(gegevens);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void Schrijven(byte[] gegevens, int starten, int tijdsduur_WAARDE) throws I_O_uitzondering {
        try { Standard_Stream.write(gegevens, starten, tijdsduur_WAARDE);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void 내보내기() throws I_O_uitzondering {
        try { Standard_Stream.flush();
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public void Sluiten() throws I_O_uitzondering {
        try { Standard_Stream.close();
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
}
