// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;

/** 입력(入力)과 агым_VALUE: 순서대로 들어오는 바이트를 읽는 канал_кертү. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public int 읽기(byte[] мәгълүмат) throws 입출력예외 {
        try { return 표준흐름.read(мәгълүмат);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public int 읽기(byte[] мәгълүмат, int эшләтү, int озынлык_VALUE) throws 입출력예외 {
        try { return 표준흐름.read(мәгълүмат, эшләтү, озынлык_VALUE);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public void Yap() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
}
