// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** totoo_data Java kaso_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void tiyakin_kumpirmahin(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int checksum(int[] VALUE, int run, int haba_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) SUM_VALUE += VALUE[run + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Ihanda(int haba_VALUE) {
        Network_Stack.CLEAN_Proseso();
        tiyakin_kumpirmahin(Network_Stack.buksan(5000) == 3);
        int[] frame_INDEX = Network_Stack.입력틀;
        Arrays.fill(frame_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) frame_INDEX[INDEX] = Network_driver.device_email[INDEX];
        Network_Stack.넣기16(frame_INDEX, 12, 0x0800);
        frame_INDEX[14] = 0x45; frame_INDEX[22] = 64; frame_INDEX[23] = 17;
        Network_Stack.넣기16(frame_INDEX, 16, 28 + haba_VALUE);
        Network_Stack.넣기32(frame_INDEX, 26, 0x0a000202); Network_Stack.넣기32(frame_INDEX, 30, Network_Stack.내주소);
        Network_Stack.넣기16(frame_INDEX, 34, 4321); Network_Stack.넣기16(frame_INDEX, 36, 5000); Network_Stack.넣기16(frame_INDEX, 38, haba_VALUE + 8);
        for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) frame_INDEX[42 + INDEX] = INDEX & 255;
        set_checksum(haba_VALUE);
    }
    static void set_checksum(int haba_VALUE) {
        int[] frame_INDEX = Network_Stack.입력틀;
        Network_Stack.넣기16(frame_INDEX, 24, 0); Network_Stack.넣기16(frame_INDEX, 40, 0);
        Network_Stack.넣기16(frame_INDEX, 24, checksum(frame_INDEX, 14, 20, 0));
        int 초기 = Network_Stack.가상머리합(Network_Stack.integer_buong_numero_32(frame_INDEX, 26), Network_Stack.내주소, haba_VALUE + 8);
        int SUM_VALUE = checksum(frame_INDEX, 34, haba_VALUE + 8, 초기);
        Network_Stack.넣기16(frame_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void tanggihan_VALUE(int haba_VALUE) { Network_Stack.Proseso_frame(haba_VALUE); tiyakin_kumpirmahin(Network_Stack.RECEIVED_haba[0] == -1); }
    public static void main(String[] 인수) {
        for (int haba_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Ihanda(haba_VALUE); Network_Stack.Proseso_frame(haba_VALUE + 42);
            tiyakin_kumpirmahin(Network_Stack.RECEIVED_haba[0] == haba_VALUE);
            tiyakin_kumpirmahin(Network_Stack.RECEIVED_email[0] == 0x0a000202 && Network_Stack.RECEIVED_numero_ng_port[0] == 4321);
            for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) tiyakin_kumpirmahin(Network_Stack.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int haba_VALUE = 0; haba_VALUE < 42; haba_VALUE++) { Ihanda(0); tanggihan_VALUE(haba_VALUE); }
        Ihanda(1025); tanggihan_VALUE(1067);
        Ihanda(2); Network_Stack.입력틀[24] ^= 1; tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[42] ^= 1; tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.넣기16(Network_Stack.입력틀, 38, 7); tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.넣기16(Network_Stack.입력틀, 38, 65535); tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[14] = 0x4f; tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[14] = 0x44; tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[20] = 0x20; set_checksum(2); tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[21] = 1; set_checksum(2); tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[33] = 99; set_checksum(2); tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[0] ^= 1; tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.입력틀[23] = 6; set_checksum(2); tanggihan_VALUE(44);
        Ihanda(2); Network_Stack.넣기16(Network_Stack.입력틀, 40, 0); Network_Stack.Proseso_frame(44); tiyakin_kumpirmahin(Network_Stack.RECEIVED_haba[0] == 2);
        int[] sukat = new int[4];
        tiyakin_kumpirmahin(Network_Stack.받기(3, sukat, 1, 0) == -90);
        tiyakin_kumpirmahin(Network_Stack.받기(3, sukat, 4, 0) == -11);
        Ihanda(2); Network_Stack.Proseso_frame(44); int alisin_VALUE = Network_Stack.폐기수;
        Network_Stack.Proseso_frame(44); tiyakin_kumpirmahin(Network_Stack.폐기수 == alisin_VALUE + 1);
        Network_Stack.CLEAN_Proseso(); tiyakin_kumpirmahin(Network_Stack.buksan(5000) == 3);
        tiyakin_kumpirmahin(Network_Stack.buksan(5000) == -98); tiyakin_kumpirmahin(Network_Stack.buksan(0) == 4);
        tiyakin_kumpirmahin(Network_Stack.buksan(0) == 5); tiyakin_kumpirmahin(Network_Stack.buksan(0) == 6); tiyakin_kumpirmahin(Network_Stack.buksan(0) == -24);
        tiyakin_kumpirmahin(Network_Stack.isara(4) == 0); tiyakin_kumpirmahin(Network_Stack.isara(4) == -9);
        Network_Stack.찾은주소 = Network_Stack.entrada_VALUE;
        tiyakin_kumpirmahin(Network_Stack.i_email(3, Network_Stack.entrada_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Network_driver.kamakailan_VALUE;
        tiyakin_kumpirmahin(checksum(보냄, 14, 20, 0) == 0);
        tiyakin_kumpirmahin(checksum(보냄, 34, 11, Network_Stack.가상머리합(Network_Stack.내주소, Network_Stack.entrada_VALUE, 11)) == 0);
        tiyakin_kumpirmahin(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
