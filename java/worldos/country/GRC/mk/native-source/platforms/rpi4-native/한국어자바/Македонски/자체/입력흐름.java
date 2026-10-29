// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 канал_внес. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Читај() throws В_И_исклучок {
        try { return 표준흐름.read();
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public int Читај(byte[] податоци) throws В_И_исклучок {
        try { return 표준흐름.read(податоци);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public int Читај(byte[] податоци, int Изврши_2, int должина_VALUE) throws В_И_исклучок {
        try { return 표준흐름.read(податоци, Изврши_2, должина_VALUE);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public void Затвори() throws В_И_исклучок {
        try { 표준흐름.close();
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
}
