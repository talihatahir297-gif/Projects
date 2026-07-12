import java.io.*;
import java.util.ArrayList;
class NumberGuessing {
    public static void main(String[] args) {
        int numberToGuess = (int) (Math.random() * 50) + 1;
        int userGuess = 0;
        int lives = 6 ; 
        java.util.Scanner scanner = new java.util.Scanner(System.in);
     

        System.out.println("Welcome to the Number Guessing Game!");
        System.out.println("I have selected a number between 1 and 50");
        System.out.println("You have 6 lives in total.");
        try {
            File myfile = new File("game.txt");
            myfile.createNewFile();
            System.out.println("File created successfully!");
        } catch (Exception e) {
            
            e.printStackTrace();
            System.out.println("There is an error in ur creation plz try again.");
        }
           ArrayList <Integer> list = new ArrayList<>();

        while (userGuess != numberToGuess && lives > 0) {
            System.out.print("Enter your guess: ");
            userGuess = scanner.nextInt();
                if(list.contains(userGuess)){
                System.out.println("The number is already in the list plz try some other.");
                continue;
            }
            else{
                list.add(userGuess);
                System.out.println("OK keep going buddy!");
            }

            if (userGuess < numberToGuess) {
                System.out.println("Too low! Try again.");
                lives--;
             } else if (userGuess > numberToGuess) {
                System.out.println("Too high! Try again.");
                lives--;
               } 
            
               else {
                System.out.println("Congratulations! You've guessed the number!");
                
            }
        
            try {
                FileWriter myfile = new FileWriter("game.txt",true);
                myfile.write(userGuess + "\n");
                myfile.close();
            } catch (IOException e) {
               
                e.printStackTrace();
            }
        }
            if (lives==0){
                System.out.println("Sorry Dear you are out now !");
                System.out.println("The right number is :" + numberToGuess);
            }
        scanner.close();
    }
}