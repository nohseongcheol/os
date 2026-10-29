// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 Stream_baha: 순서대로 들어오는 바이트를 읽는 kanal_girizmeklik. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Oka() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public int Oka(byte[] maglumat) throws 입출력예외 {
        try { return 표준흐름.read(maglumat);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public int Oka(byte[] maglumat, int Bitir, int dowamlylyk_baha) throws 입출력예외 {
        try { return 표준흐름.read(maglumat, Bitir, dowamlylyk_baha);
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
    public void Ýap() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Hata) { throw 예외변환.I_O(Hata); }
        catch (RuntimeException Hata) { throw 예외변환.ýerine_ýetir_buýruk(Hata); }
    }
}
