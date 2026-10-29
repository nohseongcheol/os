// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;

/** 전문(電文)·Saluran_pemasukan(通路): 경계를 가진 UDP 자료를 주고받는 peserta. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int nombor_port) throws I_O_pengecualian {
        try { 표준종단 = 통신.Buka(nombor_port);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public static 전문통로 Buka(int nombor_port) throws I_O_pengecualian {
        try { return new 전문통로(nombor_port);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void e_mel_9aee63bd(String e_mel, int nombor_port, String data) throws I_O_pengecualian {
        try { 통신.e_mel_9aee63bd(표준종단, e_mel, nombor_port, data);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public String 받기() throws I_O_pengecualian {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_pengecualian {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public int nombor_port() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Tutup() { 통신.Tutup(표준종단); }
}
