// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;

/** 출력(出力)과 strim_VALUE: 순서를 보존해 내보내는 바이트의 Saluran_pemasukan. */
public final class strim_output {
    private final java.io.OutputStream 표준흐름;
    strim_output(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Tulis(int VALUE) throws I_O_pengecualian {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void Tulis(byte[] data) throws I_O_pengecualian {
        try { 표준흐름.write(data);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void Tulis(byte[] data, int Jalan, int kepanjangan_VALUE) throws I_O_pengecualian {
        try { 표준흐름.write(data, Jalan, kepanjangan_VALUE);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void 내보내기() throws I_O_pengecualian {
        try { 표준흐름.flush();
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void Tutup() throws I_O_pengecualian {
        try { 표준흐름.close();
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
}
