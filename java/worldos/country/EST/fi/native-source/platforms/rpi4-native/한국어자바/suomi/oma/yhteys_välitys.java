// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
import java.net.*;
public final class yhteys_välitys {
    private yhteys_välitys() {}
    public static yhteys Avaa(String OSOITE, int portin_numero) throws I_O_poikkeus {
        try { return yhteys.Avaa(OSOITE, portin_numero);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static saada_portti 수신열기(int portin_numero) throws I_O_poikkeus {
        try { return saada_portti.Avaa(portin_numero);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static Socket Yhdistä(String OSOITE, int portti_ARVO) throws I_O_poikkeus {
        try { return new Socket(OSOITE, portti_ARVO);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static ServerSocket kuunnella_päätepiste(int portti_ARVO) throws I_O_poikkeus {
        try { return new ServerSocket(portti_ARVO);
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static Socket saada(ServerSocket palvelin_ARVO) throws I_O_poikkeus {
        try { return palvelin_ARVO.accept();
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
}
