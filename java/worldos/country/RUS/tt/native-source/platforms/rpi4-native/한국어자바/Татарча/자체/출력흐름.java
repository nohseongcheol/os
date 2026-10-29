// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;

/** 출력(出力)과 агым_VALUE: 순서를 보존해 내보내는 바이트의 канал_кертү. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void язу(int VALUE) throws 입출력예외 {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public void язу(byte[] мәгълүмат) throws 입출력예외 {
        try { 표준흐름.write(мәгълүмат);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public void язу(byte[] мәгълүмат, int эшләтү, int озынлык_VALUE) throws 입출력예외 {
        try { 표준흐름.write(мәгълүмат, эшләтү, озынлык_VALUE);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public void Yap() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
}
