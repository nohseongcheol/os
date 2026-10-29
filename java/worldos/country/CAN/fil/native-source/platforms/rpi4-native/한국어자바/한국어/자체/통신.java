// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 digit_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket buksan(int port_VALUE) throws I_O_pagbubukod {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static void i_email(DatagramSocket 종단, int port_VALUE, String Nilalaman_VALUE) throws I_O_pagbubukod {
        try {
        i_email(종단, "127.0.0.1", port_VALUE, Nilalaman_VALUE);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static void i_email(DatagramSocket 종단, String email, int port_VALUE, String Nilalaman_VALUE) throws I_O_pagbubukod {
        try {
        byte[] byte_VALUE = 문자.부호화(Nilalaman_VALUE);
        종단.send(new DatagramPacket(byte_VALUE, byte_VALUE.length, InetAddress.getByName(email), port_VALUE));
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static String 받기(DatagramSocket 종단) throws I_O_pagbubukod {
        try {
        byte[] byte_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_VALUE, byte_VALUE.length); 종단.receive(전문);
        byte[] sukat = new byte[전문.getLength()]; System.arraycopy(byte_VALUE, 0, sukat, 0, sukat.length); return 문자.i_decrypt_data(sukat);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws I_O_pagbubukod {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static void isara(DatagramSocket 종단) { 종단.close(); }
}
