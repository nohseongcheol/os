// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 moela_Boleng: 순서대로 들어오는 바이트를 읽는 mosele_tsenyo. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public int 읽기(byte[] tshedimosetso) throws 입출력예외 {
        try { return 표준흐름.read(tshedimosetso);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public int 읽기(byte[] tshedimosetso, int dirisa, int boleele_Boleng) throws 입출력예외 {
        try { return 표준흐름.read(tshedimosetso, dirisa, boleele_Boleng);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public void tswala() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
}
