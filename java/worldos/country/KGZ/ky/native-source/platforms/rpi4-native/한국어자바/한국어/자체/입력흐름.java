// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 агым_маани: 순서대로 들어오는 바이트를 읽는 канал_киргизме_жазуу. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Окуу() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public int Окуу(byte[] берилмелер) throws 입출력예외 {
        try { return 표준흐름.read(берилмелер);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public int Окуу(byte[] берилмелер, int Жүргүзүү, int узундук_маани) throws 입출력예외 {
        try { return 표준흐름.read(берилмелер, Жүргүзүү, узундук_маани);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public void Жабуу() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
}
