// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** werkelijk_gegevens Java contractwaarde 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class pakket_test {
    static int herhaling_AANTAL = 0;
    static void bevestigen(boolean WAARDE) { if (!WAARDE) throw new AssertionError("case " + herhaling_AANTAL); herhaling_AANTAL++; }
    static int controlesom(int[] WAARDE, int starten, int tijdsduur_WAARDE, int begintoestand) {
        int SOM_WAARDE = begintoestand;
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) SOM_WAARDE += WAARDE[starten + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SOM_WAARDE = (SOM_WAARDE & 65535) + (SOM_WAARDE >>> 16);
        SOM_WAARDE = (SOM_WAARDE & 65535) + (SOM_WAARDE >>> 16);
        return ~SOM_WAARDE & 65535;
    }
    static void Bereid_voor(int tijdsduur_WAARDE) {
        net_stack.Verscherpt_Proces();
        bevestigen(net_stack.Openen(5000) == 3);
        int[] frame_INDEX = net_stack.invoer_frame;
        Arrays.fill(frame_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) frame_INDEX[INDEX] = net_stuurprogramma.mobiel_ADRES[INDEX];
        net_stack.넣기16(frame_INDEX, 12, 0x0800);
        frame_INDEX[14] = 0x45; frame_INDEX[22] = 64; frame_INDEX[23] = 17;
        net_stack.넣기16(frame_INDEX, 16, 28 + tijdsduur_WAARDE);
        net_stack.넣기32(frame_INDEX, 26, 0x0a000202); net_stack.넣기32(frame_INDEX, 30, net_stack.내주소);
        net_stack.넣기16(frame_INDEX, 34, 4321); net_stack.넣기16(frame_INDEX, 36, 5000); net_stack.넣기16(frame_INDEX, 38, tijdsduur_WAARDE + 8);
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) frame_INDEX[42 + INDEX] = INDEX & 255;
        set_controlesom(tijdsduur_WAARDE);
    }
    static void set_controlesom(int tijdsduur_WAARDE) {
        int[] frame_INDEX = net_stack.invoer_frame;
        net_stack.넣기16(frame_INDEX, 24, 0); net_stack.넣기16(frame_INDEX, 40, 0);
        net_stack.넣기16(frame_INDEX, 24, controlesom(frame_INDEX, 14, 20, 0));
        int begintoestand = net_stack.가상머리합(net_stack.geheel_getal_32(frame_INDEX, 26), net_stack.내주소, tijdsduur_WAARDE + 8);
        int SOM_WAARDE = controlesom(frame_INDEX, 34, tijdsduur_WAARDE + 8, begintoestand);
        net_stack.넣기16(frame_INDEX, 40, SOM_WAARDE == 0 ? 65535 : SOM_WAARDE);
    }
    static void weigeren_WAARDE(int tijdsduur_WAARDE) { net_stack.Proces_frame(tijdsduur_WAARDE); bevestigen(net_stack.OPBRENGST_tijdsduur[0] == -1); }
    public static void main(String[] argumenten) {
        for (int tijdsduur_WAARDE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Bereid_voor(tijdsduur_WAARDE); net_stack.Proces_frame(tijdsduur_WAARDE + 42);
            bevestigen(net_stack.OPBRENGST_tijdsduur[0] == tijdsduur_WAARDE);
            bevestigen(net_stack.OPBRENGST_ADRES[0] == 0x0a000202 && net_stack.OPBRENGST_poortnummer[0] == 4321);
            for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) bevestigen(net_stack.OPBRENGST_gegevens[INDEX] == (INDEX & 255));
        }
        for (int tijdsduur_WAARDE = 0; tijdsduur_WAARDE < 42; tijdsduur_WAARDE++) { Bereid_voor(0); weigeren_WAARDE(tijdsduur_WAARDE); }
        Bereid_voor(1025); weigeren_WAARDE(1067);
        Bereid_voor(2); net_stack.invoer_frame[24] ^= 1; weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[42] ^= 1; weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.넣기16(net_stack.invoer_frame, 38, 7); weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.넣기16(net_stack.invoer_frame, 38, 65535); weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[14] = 0x4f; weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[14] = 0x44; weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[20] = 0x20; set_controlesom(2); weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[21] = 1; set_controlesom(2); weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[33] = 99; set_controlesom(2); weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[0] ^= 1; weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.invoer_frame[23] = 6; set_controlesom(2); weigeren_WAARDE(44);
        Bereid_voor(2); net_stack.넣기16(net_stack.invoer_frame, 40, 0); net_stack.Proces_frame(44); bevestigen(net_stack.OPBRENGST_tijdsduur[0] == 2);
        int[] resultaat = new int[4];
        bevestigen(net_stack.ontvangen(3, resultaat, 1, 0) == -90);
        bevestigen(net_stack.ontvangen(3, resultaat, 4, 0) == -11);
        Bereid_voor(2); net_stack.Proces_frame(44); int verwijderen_WAARDE = net_stack.폐기수;
        net_stack.Proces_frame(44); bevestigen(net_stack.폐기수 == verwijderen_WAARDE + 1);
        net_stack.Verscherpt_Proces(); bevestigen(net_stack.Openen(5000) == 3);
        bevestigen(net_stack.Openen(5000) == -98); bevestigen(net_stack.Openen(0) == 4);
        bevestigen(net_stack.Openen(0) == 5); bevestigen(net_stack.Openen(0) == 6); bevestigen(net_stack.Openen(0) == -24);
        bevestigen(net_stack.Sluiten(4) == 0); bevestigen(net_stack.Sluiten(4) == -9);
        net_stack.찾은주소 = net_stack.gateway_WAARDE;
        bevestigen(net_stack.e_mailen(3, net_stack.gateway_WAARDE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = net_stuurprogramma.recent_WAARDE;
        bevestigen(controlesom(보냄, 14, 20, 0) == 0);
        bevestigen(controlesom(보냄, 34, 11, net_stack.가상머리합(net_stack.내주소, net_stack.gateway_WAARDE, 11)) == 0);
        bevestigen(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + herhaling_AANTAL + " assertions");
    }
}
