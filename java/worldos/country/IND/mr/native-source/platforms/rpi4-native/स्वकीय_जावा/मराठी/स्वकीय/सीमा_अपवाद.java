// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा सीमा_अपवाद अपवाद. */
public class सीमा_अपवाद extends java.lang.IndexOutOfBoundsException {
    public सीमा_अपवाद() { super(); }
    public सीमा_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
