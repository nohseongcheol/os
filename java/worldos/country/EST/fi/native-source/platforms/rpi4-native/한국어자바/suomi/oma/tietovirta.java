// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** tulostuspaikka(出力)과 virta_ARVO: 순서를 보존해 내보내는 바이트의 Media_merkintä. */
public final class tietovirta {
    private final java.io.OutputStream Vakio_virta;
    tietovirta(java.io.OutputStream Vakio_virta) { this.Vakio_virta = Vakio_virta; }
    public void Kirjoitus(int ARVO) throws I_O_poikkeus {
        try { Vakio_virta.write(ARVO);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void Kirjoitus(byte[] data) throws I_O_poikkeus {
        try { Vakio_virta.write(data);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void Kirjoitus(byte[] data, int Suorita_2, int kesto_ARVO) throws I_O_poikkeus {
        try { Vakio_virta.write(data, Suorita_2, kesto_ARVO);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void 내보내기() throws I_O_poikkeus {
        try { Vakio_virta.flush();
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void Sulje() throws I_O_poikkeus {
        try { Vakio_virta.close();
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
}
