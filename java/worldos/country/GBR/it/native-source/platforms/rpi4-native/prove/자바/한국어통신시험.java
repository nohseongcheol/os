// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.nativo.*;

/** 동일 바이트코드를 OpenJDK와 nativo JVM에서 실행하는 comunicazione 계약 prove. */
public class 한국어통신시험 {
    public static void main(String[] argomenti) throws I_O_eccezione {
        porta_di_ricezione porta_VALORE = connessione_trasporto.수신열기(0);
        connessione guest_VALORE = connessione_trasporto.Apri("127.0.0.1", porta_VALORE.numero_di_porta());
        connessione proprietario_identificatore = porta_VALORE.ricevere();
        guest_VALORE.TIMEOUT(200); proprietario_identificatore.TIMEOUT(200);
        검사.참인지(guest_VALORE.연결됨() && !guest_VALORE.reparto_IT_chiusa(), "Connetti Stato_VALORE");
        검사.참인지(proprietario_identificatore.numero_di_porta() == guest_VALORE.locale_numero_di_porta(), "peer_VALORE numero_di_porta");
        검사.참인지(guest_VALORE.numero_di_porta() == proprietario_identificatore.locale_numero_di_porta(), "locale_Scope numero_di_porta");
        flusso_di_input input_VALORE = proprietario_identificatore.input_VALORE(); flusso_di_output output_pagina = guest_VALORE.uscitaTesto();
        byte[] documento = 문자.codificare("한글 Stream_VALORE");
        output_pagina.Scrittura(documento, 0, documento.length); output_pagina.내보내기();
        byte[] RICEV_SCAD_SMS = new byte[documento.length];
        int 읽은수 = 0;
        while (읽은수 < RICEV_SCAD_SMS.length) {
            int 더읽음 = input_VALORE.Lettura(RICEV_SCAD_SMS, 읽은수, RICEV_SCAD_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 file 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.decifrare_dati(RICEV_SCAD_SMS), "한글 Stream_VALORE"), "부분 읽기와 Scrittura");
        output_pagina.Scrittura(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = input_VALORE.Lettura(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "array_VALORE Lettura");
        if (첫읽기 == 1) 두바이트[1] = (byte)input_VALORE.Lettura();
        검사.참인지(두바이트[1] == 18, "나머지 Lettura");
        proprietario_identificatore.uscitaTesto().Scrittura(255);
        검사.참인지(guest_VALORE.input_VALORE().Lettura() == 255, "Codifica_VALORE 없는 한 byte_VALORE");
        output_pagina.Chiudi();
        검사.참인지(guest_VALORE.reparto_IT_chiusa() && input_VALORE.Lettura() == -1, "닫기와 file 끝");
        input_VALORE.Chiudi(); 검사.참인지(proprietario_identificatore.reparto_IT_chiusa(), "input_VALORE Stream_VALORE Chiudi");
        guest_VALORE.Chiudi(); proprietario_identificatore.Chiudi();
        porta_VALORE.TIMEOUT(15);
        boolean esecuzione_TIMEOUT = false;
        try { porta_VALORE.ricevere(); } catch (aspetta_TIMEOUT_eccezione 예상한오류) { esecuzione_TIMEOUT = true; }
        검사.참인지(esecuzione_TIMEOUT, "ricevere_VALORE TIMEOUT");
        porta_VALORE.Chiudi(); 검사.참인지(porta_VALORE.reparto_IT_chiusa(), "porta_di_ricezione Chiudi");
        datagramma_Canale 받는곳 = datagramma_Canale.Apri(0), 보내는곳 = datagramma_Canale.Apri(0);
        받는곳.TIMEOUT(200);
        보내는곳.inviare("127.0.0.1", 받는곳.numero_di_porta(), "datagramma 한글");
        검사.참인지(문자.같음(받는곳.ricevere(), "datagramma 한글"), "datagramma 송수신");
        보내는곳.Chiudi(); 받는곳.Chiudi();
        검사.참인지(보내는곳.reparto_IT_chiusa() && 받는곳.reparto_IT_chiusa(), "datagramma Chiudi");
        uscitaTesto.scrivere_riga("Italiano comunicazione verificare: Connetti datagramma Stream_VALORE esecuzione_TIMEOUT Chiudi");
    }
}
