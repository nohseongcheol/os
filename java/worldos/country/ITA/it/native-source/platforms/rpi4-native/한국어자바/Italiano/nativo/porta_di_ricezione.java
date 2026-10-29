// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** ricevere_VALORE(受信)·porta_VALORE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class porta_di_ricezione {
    private final java.net.ServerSocket Standard_porta;
    private porta_di_ricezione(int numero_di_porta) throws I_O_eccezione {
        try { Standard_porta = new java.net.ServerSocket(numero_di_porta);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static porta_di_ricezione Apri(int numero_di_porta) throws I_O_eccezione {
        try { return new porta_di_ricezione(numero_di_porta);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public connessione ricevere() throws I_O_eccezione {
        try { return new connessione(Standard_porta.accept());
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public int numero_di_porta() { return Standard_porta.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_eccezione {
        try { Standard_porta.setSoTimeout(밀리초);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public boolean reparto_IT_chiusa() { return Standard_porta.isClosed(); }
    public void Chiudi() throws I_O_eccezione {
        try { Standard_porta.close();
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
}
