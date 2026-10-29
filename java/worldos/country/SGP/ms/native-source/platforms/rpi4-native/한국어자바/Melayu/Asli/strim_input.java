// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;

/** 입력(入力)과 strim_VALUE: 순서대로 들어오는 바이트를 읽는 Saluran_pemasukan. */
public final class strim_input {
    private final java.io.InputStream 표준흐름;
    strim_input(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Baca() throws I_O_pengecualian {
        try { return 표준흐름.read();
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public int Baca(byte[] data) throws I_O_pengecualian {
        try { return 표준흐름.read(data);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public int Baca(byte[] data, int Jalan, int kepanjangan_VALUE) throws I_O_pengecualian {
        try { return 표준흐름.read(data, Jalan, kepanjangan_VALUE);
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
    public void Tutup() throws I_O_pengecualian {
        try { 표준흐름.close();
        } catch (java.io.IOException RALAT) { throw tukar_pengecualian.I_O(RALAT); }
        catch (RuntimeException RALAT) { throw tukar_pengecualian.laksanakan_perintah(RALAT); }
    }
}
