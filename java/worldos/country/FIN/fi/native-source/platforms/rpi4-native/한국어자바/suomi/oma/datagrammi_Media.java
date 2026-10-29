// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** datagrammi(電文)·Media_merkintä(通路): 경계를 가진 UDP 자료를 주고받는 päätepiste. */
public final class datagrammi_Media {
    private final java.net.DatagramSocket Vakio_päätepiste;
    private datagrammi_Media(int portin_numero) throws I_O_poikkeus {
        try { Vakio_päätepiste = 통신.Avaa(portin_numero);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static datagrammi_Media Avaa(int portin_numero) throws I_O_poikkeus {
        try { return new datagrammi_Media(portin_numero);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void lähettää(String OSOITE, int portin_numero, String data) throws I_O_poikkeus {
        try { 통신.lähettää(Vakio_päätepiste, OSOITE, portin_numero, data);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public String saada() throws I_O_poikkeus {
        try { return 통신.saada(Vakio_päätepiste);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void AIKAKATKAISU(int 밀리초) throws I_O_poikkeus {
        try { 통신.AIKAKATKAISU(Vakio_päätepiste, 밀리초);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public int portin_numero() { return Vakio_päätepiste.getLocalPort(); }
    public boolean tietojärjestelmät_suljettu() { return Vakio_päätepiste.isClosed(); }
    public void Sulje() { 통신.Sulje(Vakio_päätepiste); }
}
