// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;

/** 출력(出力)과 Stream_inani: 순서를 보존해 내보내는 바이트의 umgudu_okufakwayo. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Bhala(int inani) throws 입출력예외 {
        try { 표준흐름.write(inani);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public void Bhala(byte[] imininingwane) throws 입출력예외 {
        try { 표준흐름.write(imininingwane);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public void Bhala(byte[] imininingwane, int Sebenzisa, int ubude_inani) throws 입출력예외 {
        try { 표준흐름.write(imininingwane, Sebenzisa, ubude_inani);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public void Vala() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
}
