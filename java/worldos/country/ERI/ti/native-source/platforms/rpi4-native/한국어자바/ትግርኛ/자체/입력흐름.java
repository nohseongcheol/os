// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;

/** 입력(入力)과 ወሓዚ_ዋጋ: 순서대로 들어오는 바이트를 읽는 ጣብያ_ምእታው. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public int 읽기(byte[] ሓበሬታ) throws 입출력예외 {
        try { return 표준흐름.read(ሓበሬታ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public int 읽기(byte[] ሓበሬታ, int ኣኺድ, int ንውሓት_ዋጋ) throws 입출력예외 {
        try { return 표준흐름.read(ሓበሬታ, ኣኺድ, ንውሓት_ዋጋ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public void ዕጸው() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
}
