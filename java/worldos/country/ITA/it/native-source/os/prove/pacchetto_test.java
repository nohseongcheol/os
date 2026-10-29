// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** effettivo_dati Java valore_di_contratto 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class pacchetto_test {
    static int ripetizione_CONTA_NUMERI = 0;
    static void verificare(boolean VALORE) { if (!VALORE) throw new AssertionError("case " + ripetizione_CONTA_NUMERI); ripetizione_CONTA_NUMERI++; }
    static int checksum(int[] VALORE, int avvia, int durata_VALORE, int stato_iniziale) {
        int SUM_VALORE = stato_iniziale;
        for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) SUM_VALORE += VALORE[avvia + INDICE] << ((INDICE & 1) == 0 ? 8 : 0);
        SUM_VALORE = (SUM_VALORE & 65535) + (SUM_VALORE >>> 16);
        SUM_VALORE = (SUM_VALORE & 65535) + (SUM_VALORE >>> 16);
        return ~SUM_VALORE & 65535;
    }
    static void Prepara(int durata_VALORE) {
        rete_Pila.LIBERA_Processi();
        verificare(rete_Pila.Apri(5000) == 3);
        int[] frame_INDICE = rete_Pila.input_frame;
        Arrays.fill(frame_INDICE, 0);
        for (int INDICE = 0; INDICE < 6; INDICE++) frame_INDICE[INDICE] = rete_driver.cellulare_e_mail[INDICE];
        rete_Pila.넣기16(frame_INDICE, 12, 0x0800);
        frame_INDICE[14] = 0x45; frame_INDICE[22] = 64; frame_INDICE[23] = 17;
        rete_Pila.넣기16(frame_INDICE, 16, 28 + durata_VALORE);
        rete_Pila.넣기32(frame_INDICE, 26, 0x0a000202); rete_Pila.넣기32(frame_INDICE, 30, rete_Pila.내주소);
        rete_Pila.넣기16(frame_INDICE, 34, 4321); rete_Pila.넣기16(frame_INDICE, 36, 5000); rete_Pila.넣기16(frame_INDICE, 38, durata_VALORE + 8);
        for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) frame_INDICE[42 + INDICE] = INDICE & 255;
        set_checksum(durata_VALORE);
    }
    static void set_checksum(int durata_VALORE) {
        int[] frame_INDICE = rete_Pila.input_frame;
        rete_Pila.넣기16(frame_INDICE, 24, 0); rete_Pila.넣기16(frame_INDICE, 40, 0);
        rete_Pila.넣기16(frame_INDICE, 24, checksum(frame_INDICE, 14, 20, 0));
        int stato_iniziale = rete_Pila.가상머리합(rete_Pila.intero_32(frame_INDICE, 26), rete_Pila.내주소, durata_VALORE + 8);
        int SUM_VALORE = checksum(frame_INDICE, 34, durata_VALORE + 8, stato_iniziale);
        rete_Pila.넣기16(frame_INDICE, 40, SUM_VALORE == 0 ? 65535 : SUM_VALORE);
    }
    static void rifiutare_VALORE(int durata_VALORE) { rete_Pila.Processi_frame(durata_VALORE); verificare(rete_Pila.RICEV_SCAD_durata[0] == -1); }
    public static void main(String[] argomenti) {
        for (int durata_VALORE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Prepara(durata_VALORE); rete_Pila.Processi_frame(durata_VALORE + 42);
            verificare(rete_Pila.RICEV_SCAD_durata[0] == durata_VALORE);
            verificare(rete_Pila.RICEV_SCAD_e_mail[0] == 0x0a000202 && rete_Pila.RICEV_SCAD_numero_di_porta[0] == 4321);
            for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) verificare(rete_Pila.RICEV_SCAD_dati[INDICE] == (INDICE & 255));
        }
        for (int durata_VALORE = 0; durata_VALORE < 42; durata_VALORE++) { Prepara(0); rifiutare_VALORE(durata_VALORE); }
        Prepara(1025); rifiutare_VALORE(1067);
        Prepara(2); rete_Pila.input_frame[24] ^= 1; rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[42] ^= 1; rifiutare_VALORE(44);
        Prepara(2); rete_Pila.넣기16(rete_Pila.input_frame, 38, 7); rifiutare_VALORE(44);
        Prepara(2); rete_Pila.넣기16(rete_Pila.input_frame, 38, 65535); rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[14] = 0x4f; rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[14] = 0x44; rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[20] = 0x20; set_checksum(2); rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[21] = 1; set_checksum(2); rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[33] = 99; set_checksum(2); rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[0] ^= 1; rifiutare_VALORE(44);
        Prepara(2); rete_Pila.input_frame[23] = 6; set_checksum(2); rifiutare_VALORE(44);
        Prepara(2); rete_Pila.넣기16(rete_Pila.input_frame, 40, 0); rete_Pila.Processi_frame(44); verificare(rete_Pila.RICEV_SCAD_durata[0] == 2);
        int[] risultato = new int[4];
        verificare(rete_Pila.ricevere(3, risultato, 1, 0) == -90);
        verificare(rete_Pila.ricevere(3, risultato, 4, 0) == -11);
        Prepara(2); rete_Pila.Processi_frame(44); int discard_VALORE = rete_Pila.폐기수;
        rete_Pila.Processi_frame(44); verificare(rete_Pila.폐기수 == discard_VALORE + 1);
        rete_Pila.LIBERA_Processi(); verificare(rete_Pila.Apri(5000) == 3);
        verificare(rete_Pila.Apri(5000) == -98); verificare(rete_Pila.Apri(0) == 4);
        verificare(rete_Pila.Apri(0) == 5); verificare(rete_Pila.Apri(0) == 6); verificare(rete_Pila.Apri(0) == -24);
        verificare(rete_Pila.Chiudi(4) == 0); verificare(rete_Pila.Chiudi(4) == -9);
        rete_Pila.찾은주소 = rete_Pila.gateway_VALORE;
        verificare(rete_Pila.inviare(3, rete_Pila.gateway_VALORE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = rete_driver.recenti_VALORE;
        verificare(checksum(보냄, 14, 20, 0) == 0);
        verificare(checksum(보냄, 34, 11, rete_Pila.가상머리합(rete_Pila.내주소, rete_Pila.gateway_VALORE, 11)) == 0);
        verificare(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + ripetizione_CONTA_NUMERI + " assertions");
    }
}
