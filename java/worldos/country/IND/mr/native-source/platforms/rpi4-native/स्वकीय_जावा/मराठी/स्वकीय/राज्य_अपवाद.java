// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा राज्य_अपवाद अपवाद. */
public class राज्य_अपवाद extends java.lang.IllegalStateException {
    public राज्य_अपवाद() { super(); }
    public राज्य_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
