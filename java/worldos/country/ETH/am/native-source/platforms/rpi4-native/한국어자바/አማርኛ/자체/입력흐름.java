// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** 입력(入力)과 ልቀቅ_እሴት: 순서대로 들어오는 바이트를 읽는 ሰርጥ_ምዝግብ. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int ማንበቢያ() throws ግቤት_ውጤት_ልዩነት {
        try { return 표준흐름.read();
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public int ማንበቢያ(byte[] ውሂብ) throws ግቤት_ውጤት_ልዩነት {
        try { return 표준흐름.read(ውሂብ);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public int ማንበቢያ(byte[] ውሂብ, int ማስኬጃ, int ርዝመት_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { return 표준흐름.read(ውሂብ, ማስኬጃ, ርዝመት_እሴት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void መዝጊያ() throws ግቤት_ውጤት_ልዩነት {
        try { 표준흐름.close();
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
}
