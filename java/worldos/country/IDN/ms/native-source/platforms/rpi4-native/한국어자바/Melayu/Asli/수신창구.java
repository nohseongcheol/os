// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;

/** 수신(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int nombor_port) throws I_O_pengecualian {
        try { 표준창구 = new java.net.ServerSocket(nombor_port);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static 수신창구 Buka(int nombor_port) throws I_O_pengecualian {
        try { return new 수신창구(nombor_port);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public hubungan 받기() throws I_O_pengecualian {
        try { return new hubungan(표준창구.accept());
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public int nombor_port() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_pengecualian {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Tutup() throws I_O_pengecualian {
        try { 표준창구.close();
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
}
