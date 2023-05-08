package sit218;

import java.util.Scanner;

public class SpotBugs {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scanner = new Scanner(System.in);
		System.out.print("Enter your name: ");
		String name = scanner.nextLine();
		String test = "naeem";
		scanner.close();
	if (name == test)
	{
		System.out.print("bug found");
			}
	else
	{
		System.out.print("bug not found\n");
		System.out.print(test + "\n");
		System.out.print(name + "\n");
	}
	}

}
