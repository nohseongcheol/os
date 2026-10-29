// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;

/** 출력(出力)과 ወሓዚ_ዋጋ: 순서를 보존해 내보내는 바이트의 ጣብያ_ምእታው. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ጸሓፍ(int ዋጋ) throws 입출력예외 {
        try { 표준흐름.write(ዋጋ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public void ጸሓፍ(byte[] ሓበሬታ) throws 입출력예외 {
        try { 표준흐름.write(ሓበሬታ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public void ጸሓፍ(byte[] ሓበሬታ, int ኣኺድ, int ንውሓት_ዋጋ) throws 입출력예외 {
        try { 표준흐름.write(ሓበሬታ, ኣኺድ, ንውሓት_ዋጋ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public void ዕጸው() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
}
