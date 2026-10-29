// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा अंकगणिती_बिघाड अपवाद. */
public class अंकगणिती_बिघाड extends java.lang.ArithmeticException {
    public अंकगणिती_बिघाड() { super(); }
    public अंकगणिती_बिघाड(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
