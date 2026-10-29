// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Чыгыш(出力)과 агым_маани: 순서를 보존해 내보내는 바이트의 канал_киргизме_жазуу. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Жазуу(int маани) throws 입출력예외 {
        try { 표준흐름.write(маани);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public void Жазуу(byte[] берилмелер) throws 입출력예외 {
        try { 표준흐름.write(берилмелер);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public void Жазуу(byte[] берилмелер, int Жүргүзүү, int узундук_маани) throws 입출력예외 {
        try { 표준흐름.write(берилмелер, Жүргүзүү, узундук_маани);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public void Жабуу() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
}
