// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static hubungan Buka(String e_mel, int nombor_port) throws I_O_pengecualian {
        try { return hubungan.Buka(e_mel, nombor_port);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static 수신창구 수신열기(int nombor_port) throws I_O_pengecualian {
        try { return 수신창구.Buka(nombor_port);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static Socket Sambung(String e_mel, int port_VALUE) throws I_O_pengecualian {
        try { return new Socket(e_mel, port_VALUE);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static ServerSocket dengar_peserta(int port_VALUE) throws I_O_pengecualian {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static Socket 받기(ServerSocket pelayan_VALUE) throws I_O_pengecualian {
        try { return pelayan_VALUE.accept();
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
}
