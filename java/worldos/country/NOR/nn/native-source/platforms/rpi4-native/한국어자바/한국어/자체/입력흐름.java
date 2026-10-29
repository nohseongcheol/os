// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 kanal_oppføring. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Les() throws I_U_unntak {
        try { return 표준흐름.read();
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public int Les(byte[] data) throws I_U_unntak {
        try { return 표준흐름.read(data);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public int Les(byte[] data, int Køyr_2, int lengd_VALUE) throws I_U_unntak {
        try { return 표준흐름.read(data, Køyr_2, lengd_VALUE);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void Lukk() throws I_U_unntak {
        try { 표준흐름.close();
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
}
