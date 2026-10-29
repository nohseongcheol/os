// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा निष्पादन_अपवाद अपवाद. */
public class निष्पादन_अपवाद extends java.lang.RuntimeException {
    public निष्पादन_अपवाद() { super(); }
    public निष्पादन_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
