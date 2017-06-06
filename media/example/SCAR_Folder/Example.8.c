int main() {
    char foo[10];
    int counter;
    for (counter=0;counter!=10;counter++) {
        foo[counter]='a';
        int num_imgs = 0;
        for(int i = 1; i < 100; i++){
            num_imgs += i*i*i*i;
            num_imgs -= i*2;
        }
        printf("%s\n",foo);
    }
    return 0;
}