// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा अवैध_वितर्क_अपवाद अपवाद. */
public class अवैध_वितर्क_अपवाद extends java.lang.IllegalArgumentException {
    public अवैध_वितर्क_अपवाद() { super(); }
    public अवैध_वितर्क_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
