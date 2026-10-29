// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** syöte_ARVO(入力)과 virta_ARVO: 순서대로 들어오는 바이트를 읽는 Media_merkintä. */
public final class syötevirta {
    private final java.io.InputStream Vakio_virta;
    syötevirta(java.io.InputStream Vakio_virta) { this.Vakio_virta = Vakio_virta; }
    public int Luku() throws I_O_poikkeus {
        try { return Vakio_virta.read();
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public int Luku(byte[] data) throws I_O_poikkeus {
        try { return Vakio_virta.read(data);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public int Luku(byte[] data, int Suorita_2, int kesto_ARVO) throws I_O_poikkeus {
        try { return Vakio_virta.read(data, Suorita_2, kesto_ARVO);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void Sulje() throws I_O_poikkeus {
        try { Vakio_virta.close();
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
}
