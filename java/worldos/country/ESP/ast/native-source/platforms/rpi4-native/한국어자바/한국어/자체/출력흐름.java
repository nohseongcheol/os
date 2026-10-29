// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Salida(出力)과 흐름: 순서를 보존해 내보내는 바이트의 통로. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Escritura(int 값) throws 입출력예외 {
        try { 표준흐름.write(값);
        } catch (java.io.IOException Fallu) { throw 예외변환.입출력(Fallu); }
        catch (RuntimeException Fallu) { throw 예외변환.실행(Fallu); }
    }
    public void Escritura(byte[] 자료) throws 입출력예외 {
        try { 표준흐름.write(자료);
        } catch (java.io.IOException Fallu) { throw 예외변환.입출력(Fallu); }
        catch (RuntimeException Fallu) { throw 예외변환.실행(Fallu); }
    }
    public void Escritura(byte[] 자료, int Executar_2, int 길이) throws 입출력예외 {
        try { 표준흐름.write(자료, Executar_2, 길이);
        } catch (java.io.IOException Fallu) { throw 예외변환.입출력(Fallu); }
        catch (RuntimeException Fallu) { throw 예외변환.실행(Fallu); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Fallu) { throw 예외변환.입출력(Fallu); }
        catch (RuntimeException Fallu) { throw 예외변환.실행(Fallu); }
    }
    public void Zarrar() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Fallu) { throw 예외변환.입출력(Fallu); }
        catch (RuntimeException Fallu) { throw 예외변환.실행(Fallu); }
    }
}
