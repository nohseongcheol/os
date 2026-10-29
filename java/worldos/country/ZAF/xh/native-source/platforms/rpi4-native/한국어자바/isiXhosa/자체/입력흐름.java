// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;

/** 입력(入力)과 Stream_ixabiso: 순서대로 들어오는 바이트를 읽는 ijelo_ufako_nkcukacha. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Funda() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public int Funda(byte[] iingcombolo) throws 입출력예외 {
        try { return 표준흐름.read(iingcombolo);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public int Funda(byte[] iingcombolo, int Phumeza, int ubude_ixabiso) throws 입출력예외 {
        try { return 표준흐름.read(iingcombolo, Phumeza, ubude_ixabiso);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public void Vala() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
}
