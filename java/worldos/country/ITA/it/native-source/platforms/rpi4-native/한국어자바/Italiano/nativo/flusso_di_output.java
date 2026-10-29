// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** uscitaTesto(出力)과 Stream_VALORE: 순서를 보존해 내보내는 바이트의 Canale_voce. */
public final class flusso_di_output {
    private final java.io.OutputStream Standard_Stream;
    flusso_di_output(java.io.OutputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public void Scrittura(int VALORE) throws I_O_eccezione {
        try { Standard_Stream.write(VALORE);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void Scrittura(byte[] dati) throws I_O_eccezione {
        try { Standard_Stream.write(dati);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void Scrittura(byte[] dati, int avvia, int durata_VALORE) throws I_O_eccezione {
        try { Standard_Stream.write(dati, avvia, durata_VALORE);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void 내보내기() throws I_O_eccezione {
        try { Standard_Stream.flush();
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void Chiudi() throws I_O_eccezione {
        try { Standard_Stream.close();
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
}
