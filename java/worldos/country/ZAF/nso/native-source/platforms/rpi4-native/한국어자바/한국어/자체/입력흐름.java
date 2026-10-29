// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 Stream_boleng: 순서대로 들어오는 바이트를 읽는 mokero_go_tsenya_tshedimošo. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Bala() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public int Bala(byte[] data) throws 입출력예외 {
        try { return 표준흐름.read(data);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public int Bala(byte[] data, int Diriša, int botelele_boleng) throws 입출력예외 {
        try { return 표준흐름.read(data, Diriša, botelele_boleng);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public void Tswalela() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
}
