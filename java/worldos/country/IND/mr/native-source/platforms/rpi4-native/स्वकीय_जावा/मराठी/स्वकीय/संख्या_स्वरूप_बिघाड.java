// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा संख्या_स्वरूप_बिघाड अपवाद. */
public class संख्या_स्वरूप_बिघाड extends अवैध_वितर्क_अपवाद {
    public संख्या_स्वरूप_बिघाड() { super(); }
    public संख्या_स्वरूप_बिघाड(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
