// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** Yhdistä(連結)·Media_merkintä(通路): 상대와 이어진 TCP tavu_ARVO 흐름의 päätepiste. */
public final class yhteys {
    private final java.net.Socket Vakio_kirjasto_silta;
    yhteys(java.net.Socket Vakio_kirjasto_silta) { this.Vakio_kirjasto_silta = Vakio_kirjasto_silta; }
    public static yhteys Avaa(String OSOITE, int portin_numero) throws I_O_poikkeus {
        try {
            return new yhteys(new java.net.Socket(OSOITE, portin_numero));
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public syötevirta syöte_ARVO() throws I_O_poikkeus {
        try { return new syötevirta(Vakio_kirjasto_silta.getInputStream());
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public tietovirta tulostuspaikka() throws I_O_poikkeus {
        try { return new tietovirta(Vakio_kirjasto_silta.getOutputStream());
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public void AIKAKATKAISU(int 밀리초) throws I_O_poikkeus {
        try { Vakio_kirjasto_silta.setSoTimeout(밀리초);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public int portin_numero() { return Vakio_kirjasto_silta.getPort(); }
    public int paikallinen_portin_numero() { return Vakio_kirjasto_silta.getLocalPort(); }
    public boolean tietojärjestelmät_suljettu() { return Vakio_kirjasto_silta.isClosed(); }
    public boolean 연결됨() { return Vakio_kirjasto_silta.isConnected(); }
    public void Sulje() throws I_O_poikkeus {
        try { Vakio_kirjasto_silta.close();
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
}
