// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
import java.net.*;
public final class connessione_trasporto {
    private connessione_trasporto() {}
    public static connessione Apri(String e_mail, int numero_di_porta) throws I_O_eccezione {
        try { return connessione.Apri(e_mail, numero_di_porta);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static porta_di_ricezione 수신열기(int numero_di_porta) throws I_O_eccezione {
        try { return porta_di_ricezione.Apri(numero_di_porta);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static Socket Connetti(String e_mail, int porta_VALORE) throws I_O_eccezione {
        try { return new Socket(e_mail, porta_VALORE);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static ServerSocket essere_in_ascolto_endpoint(int porta_VALORE) throws I_O_eccezione {
        try { return new ServerSocket(porta_VALORE);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static Socket ricevere(ServerSocket server_VALORE) throws I_O_eccezione {
        try { return server_VALORE.accept();
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
}
