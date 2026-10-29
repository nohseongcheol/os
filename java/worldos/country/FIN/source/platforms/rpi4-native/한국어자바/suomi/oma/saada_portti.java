// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** saada_ARVO(受信)·portti_ARVO(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class saada_portti {
    private final java.net.ServerSocket Vakio_portti;
    private saada_portti(int portin_numero) throws I_O_poikkeus {
        try { Vakio_portti = new java.net.ServerSocket(portin_numero);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static saada_portti Avaa(int portin_numero) throws I_O_poikkeus {
        try { return new saada_portti(portin_numero);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public yhteys saada() throws I_O_poikkeus {
        try { return new yhteys(Vakio_portti.accept());
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public int portin_numero() { return Vakio_portti.getLocalPort(); }
    public void AIKAKATKAISU(int 밀리초) throws I_O_poikkeus {
        try { Vakio_portti.setSoTimeout(밀리초);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public boolean tietojärjestelmät_suljettu() { return Vakio_portti.isClosed(); }
    public void Sulje() throws I_O_poikkeus {
        try { Vakio_portti.close();
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
}
