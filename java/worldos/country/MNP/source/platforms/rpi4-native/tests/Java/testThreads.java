// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class counterValue {
    int number;
    synchronized void addValues() { int frontValue = number; Thread.yield(); number = frontValue + 1; }
}
class TaskAction implements Runnable {
    counterValue counterReference; TaskAction(counterValue counterReference) { this.counterReference = counterReference; }
    public void run() { for (int i = 0; i < 20; i++) counterReference.addValues(); }
}
class threadValue extends Thread { public void run() { synchronized (testThreads.lockValue) { testThreads.isComplete = 1; } } }
public class testThreads {
    static Object lockValue = new Object(); static int isComplete;
    public static void main(String[] a) throws Exception {
        counterValue counterReference = new counterValue(); Thread oneValue = new Thread(new TaskAction(counterReference)); Thread twoValue = new Thread(new TaskAction(counterReference));
        oneValue.start(); twoValue.start(); oneValue.join(); twoValue.join(); System.out.println(counterReference.number); System.out.println(oneValue.isAlive());
        threadValue thirdItem = new threadValue(); thirdItem.start(); thirdItem.join(); System.out.println(isComplete);
        try { oneValue.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 rejectValue"); }
        System.out.println("threadValue isComplete");
    }
}
