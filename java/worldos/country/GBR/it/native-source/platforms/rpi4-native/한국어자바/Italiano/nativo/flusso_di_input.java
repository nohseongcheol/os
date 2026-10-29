// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** input_VALORE(入力)과 Stream_VALORE: 순서대로 들어오는 바이트를 읽는 Canale_voce. */
public final class flusso_di_input {
    private final java.io.InputStream Standard_Stream;
    flusso_di_input(java.io.InputStream Standard_Stream) { this.Standard_Stream = Standard_Stream; }
    public int Lettura() throws I_O_eccezione {
        try { return Standard_Stream.read();
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public int Lettura(byte[] dati) throws I_O_eccezione {
        try { return Standard_Stream.read(dati);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public int Lettura(byte[] dati, int avvia, int durata_VALORE) throws I_O_eccezione {
        try { return Standard_Stream.read(dati, avvia, durata_VALORE);
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public void Chiudi() throws I_O_eccezione {
        try { Standard_Stream.close();
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
}
