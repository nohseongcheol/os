// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 Stream_boleng: 순서를 보존해 내보내는 바이트의 mokero_go_tsenya_tshedimošo. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Ngwala(int boleng) throws 입출력예외 {
        try { 표준흐름.write(boleng);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public void Ngwala(byte[] data) throws 입출력예외 {
        try { 표준흐름.write(data);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public void Ngwala(byte[] data, int Diriša, int botelele_boleng) throws 입출력예외 {
        try { 표준흐름.write(data, Diriša, botelele_boleng);
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public void Tswalela() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
}
