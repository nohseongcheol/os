// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.nativo.connessione;
import Italiano.nativo.실행인수;
import Italiano.nativo.datagramma_Canale;
import Italiano.nativo.문자;
import Italiano.nativo.uscitaTesto;
import Italiano.nativo.검사;
import Italiano.nativo.flusso_di_input;
import Italiano.nativo.I_O_eccezione;

public class EsempioRete {
    public static void avvia() throws I_O_eccezione {
        // host: python3 strumenti/예제되돌림.py --tcp-port 9000 --udp-port 9001
        connessione Connetti = connessione.Apri("10.0.2.2", 문자.analizzare_intero(실행인수.testo(0)));
        try {
            Connetti.TIMEOUT(700);
            byte[] documento = 문자.codificare("JAVA TCP it\n");
            Connetti.uscitaTesto().Scrittura(documento);
            flusso_di_input input_VALORE = Connetti.input_VALORE();
            for (int numero = 0; numero < 문자.byte_CONTA_NUMERI(documento); numero++) {
                검사.참인지(input_VALORE.Lettura() == (documento[numero] & 255), "TCP replica 불일치");
            }
        } finally { Connetti.Chiudi(); }
        datagramma_Canale endpoint = datagramma_Canale.Apri(0);
        try {
            endpoint.TIMEOUT(700);
            endpoint.inviare("10.0.2.2", 문자.analizzare_intero(실행인수.testo(1)), "JAVA UDP it");
            검사.참인지(문자.같음(endpoint.ricevere(), "JAVA UDP it"), "UDP replica 불일치");
        } finally { endpoint.Chiudi(); }
        uscitaTesto.scrivere_riga("JAVA 네트워크 verificare: TCP UDP it");
    }
}
