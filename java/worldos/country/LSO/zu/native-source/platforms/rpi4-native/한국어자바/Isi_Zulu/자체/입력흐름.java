// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;

/** 입력(入力)과 Stream_inani: 순서대로 들어오는 바이트를 읽는 umgudu_okufakwayo. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Funda() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public int Funda(byte[] imininingwane) throws 입출력예외 {
        try { return 표준흐름.read(imininingwane);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public int Funda(byte[] imininingwane, int Sebenzisa, int ubude_inani) throws 입출력예외 {
        try { return 표준흐름.read(imininingwane, Sebenzisa, ubude_inani);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public void Vala() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
}
