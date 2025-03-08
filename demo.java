class Main {
    public static void main(String[] args) {
        int i, j, n = 10, c = 1, p = 2;
        int[] a = new int[n]; // Declare an array of size n
        for(i=1;i<n;i++){
            a[i]+=c;
            c+=p;
            p+=1;
            for(j=2;j<p;j++){
                if(p%2==0){
                    p+=1;
                    break;
                }
            }
        }
        for(i=1;i<n;i++){
            System.out.print(a[i] + " ");
        }
        // Code logic goes here (for loop, etc.)
    }
}
