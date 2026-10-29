// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import java.awt.event.*;
import java.util.concurrent.atomic.*;
import javax.swing.*;

public final class InputFeatures {
    public static void main(String[] args) {
        try { verify(args); } catch (Throwable error) { error.printStackTrace(); System.exit(1); }
    }
    static void verify(String[] args) throws Exception {
        AtomicReference<JFrame> window=new AtomicReference<>();AtomicReference<JTextArea> input=new AtomicReference<>();
        SwingUtilities.invokeAndWait(()->{JFrame frame=new JFrame("Unicode input");JTextArea text=new JTextArea();text.setFont(new Font("Dialog",Font.PLAIN,28));frame.add(text);frame.setSize(600,300);frame.setLocation(100,100);frame.setVisible(true);text.requestFocusInWindow();input.set(text);window.set(frame);});
        Robot robot=new Robot();robot.setAutoDelay(100);robot.waitForIdle();Thread.sleep(1000);
        AtomicReference<Point> point=new AtomicReference<>();SwingUtilities.invokeAndWait(()->point.set(input.get().getLocationOnScreen()));
        robot.mouseMove(point.get().x+50,point.get().y+50);robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
        Process select=new ProcessBuilder("fcitx5-remote","-s","keyboard-us").start();if(select.waitFor()!=0)throw new AssertionError("Input engine unavailable");
        new ProcessBuilder("fcitx5-remote","-o").start().waitFor();
        Thread.sleep(1000);
        robot.keyPress(KeyEvent.VK_CONTROL);robot.keyPress(KeyEvent.VK_SHIFT);robot.keyPress(KeyEvent.VK_U);robot.keyRelease(KeyEvent.VK_U);robot.keyRelease(KeyEvent.VK_SHIFT);robot.keyRelease(KeyEvent.VK_CONTROL);
        Thread.sleep(2000);
        for(int key:new int[]{KeyEvent.VK_A,KeyEvent.VK_C,KeyEvent.VK_0,KeyEvent.VK_0}){robot.keyPress(key);robot.keyRelease(key);Thread.sleep(500);}
        // Wait for XIM preedit delivery before requesting the Unicode commit.
        Thread.sleep(1500);
        robot.keyPress(KeyEvent.VK_SPACE);robot.keyRelease(KeyEvent.VK_SPACE);
        robot.waitForIdle();Thread.sleep(1000);AtomicReference<String> result=new AtomicReference<>();SwingUtilities.invokeAndWait(()->result.set(input.get().getText()));
        for(int attempt=0;attempt<60 && !"가".equals(result.get());attempt++){ Thread.sleep(500); SwingUtilities.invokeAndWait(()->result.set(input.get().getText())); }
        javax.imageio.ImageIO.write(robot.createScreenCapture(new Rectangle(Toolkit.getDefaultToolkit().getScreenSize())),"png",new java.io.File("/home/user/workspace/input.png"));
        if(!"가".equals(result.get()))throw new AssertionError("Unicode XIM input: "+result.get());
        System.out.println("PASS fcitx-unicode-keyboard-input");SwingUtilities.invokeAndWait(()->window.get().dispose());System.exit(0);
    }
}
