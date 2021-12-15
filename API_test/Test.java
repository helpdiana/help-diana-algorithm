
public class Test extends Thread {

    public static void main(String[] args) {

        Cmd cmd = new Cmd();
        try {
            Thread.sleep(100);
            String commmand = cmd.inputCommand("python3 [파일명] [command line 에 들어갈 인자값]");
             Thread.sleep(1000);
            String result = cmd.execCommand(commmand);

            System.out.println(result);
            System.out.println("done");
        } catch (Exception e) {

            System.out.println("error");

        }
        

    }
}
