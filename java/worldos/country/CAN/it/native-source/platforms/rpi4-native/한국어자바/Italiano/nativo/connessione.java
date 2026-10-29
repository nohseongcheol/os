// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** Connetti(連結)·Canale_voce(通路): 상대와 이어진 TCP byte_VALORE 흐름의 endpoint. */
public final class connessione {
    private final java.net.Socket Standard_Catalogo_bridge;
    connessione(java.net.Socket Standard_Catalogo_bridge) { this.Standard_Catalogo_bridge = Standard_Catalogo_bridge; }
    public static connessione Apri(String e_mail, int numero_di_porta) throws I_O_eccezione {
        try {
            return new connessione(new java.net.Socket(e_mail, numero_di_porta));
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public flusso_di_input input_VALORE() throws I_O_eccezione {
        try { return new flusso_di_input(Standard_Catalogo_bridge.getInputStream());
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public flusso_di_output uscitaTesto() throws I_O_eccezione {
        try { return new flusso_di_output(Standard_Catalogo_bridge.getOutputStream());
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_eccezione {
        try { Standard_Catalogo_bridge.setSoTimeout(밀리초);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public int numero_di_porta() { return Standard_Catalogo_bridge.getPort(); }
    public int locale_numero_di_porta() { return Standard_Catalogo_bridge.getLocalPort(); }
    public boolean reparto_IT_chiusa() { return Standard_Catalogo_bridge.isClosed(); }
    public boolean 연결됨() { return Standard_Catalogo_bridge.isConnected(); }
    public void Chiudi() throws I_O_eccezione {
        try { Standard_Catalogo_bridge.close();
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
}
