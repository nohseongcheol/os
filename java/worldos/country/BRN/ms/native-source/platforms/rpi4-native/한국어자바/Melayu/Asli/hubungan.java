// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;

/** Sambung(連結)·Saluran_pemasukan(通路): 상대와 이어진 TCP bait_VALUE 흐름의 peserta. */
public final class hubungan {
    private final java.net.Socket 표준연결;
    hubungan(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static hubungan Buka(String e_mel, int nombor_port) throws I_O_pengecualian {
        try {
            return new hubungan(new java.net.Socket(e_mel, nombor_port));
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public strim_input 입력() throws I_O_pengecualian {
        try { return new strim_input(표준연결.getInputStream());
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public strim_output 출력() throws I_O_pengecualian {
        try { return new strim_output(표준연결.getOutputStream());
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_pengecualian {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public int nombor_port() { return 표준연결.getPort(); }
    public int setempat_nombor_port() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Tutup() throws I_O_pengecualian {
        try { 표준연결.close();
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
}
