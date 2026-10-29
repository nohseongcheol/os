// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Utdata(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 kanal_oppføring. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Skriv(int VALUE) throws I_U_unntak {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void Skriv(byte[] data) throws I_U_unntak {
        try { 표준흐름.write(data);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void Skriv(byte[] data, int Køyr_2, int lengd_VALUE) throws I_U_unntak {
        try { 표준흐름.write(data, Køyr_2, lengd_VALUE);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void 내보내기() throws I_U_unntak {
        try { 표준흐름.flush();
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void Lukk() throws I_U_unntak {
        try { 표준흐름.close();
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
}
