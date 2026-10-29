// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** datagramma(電文)·Canale_voce(通路): 경계를 가진 UDP 자료를 주고받는 endpoint. */
public final class datagramma_Canale {
    private final java.net.DatagramSocket Standard_endpoint;
    private datagramma_Canale(int numero_di_porta) throws I_O_eccezione {
        try { Standard_endpoint = comunicazione.Apri(numero_di_porta);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static datagramma_Canale Apri(int numero_di_porta) throws I_O_eccezione {
        try { return new datagramma_Canale(numero_di_porta);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void inviare(String e_mail, int numero_di_porta, String dati) throws I_O_eccezione {
        try { comunicazione.inviare(Standard_endpoint, e_mail, numero_di_porta, dati);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public String ricevere() throws I_O_eccezione {
        try { return comunicazione.ricevere(Standard_endpoint);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_eccezione {
        try { comunicazione.TIMEOUT(Standard_endpoint, 밀리초);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public int numero_di_porta() { return Standard_endpoint.getLocalPort(); }
    public boolean reparto_IT_chiusa() { return Standard_endpoint.isClosed(); }
    public void Chiudi() { comunicazione.Chiudi(Standard_endpoint); }
}
