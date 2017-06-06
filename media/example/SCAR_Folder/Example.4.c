int main() {
    int value;
    srand((unsigned)time(NULL));
    value = rand();
    for(int i = 0; i < 100; i++){
        if(i % 3 == 0){
            value -= rand() % i;
        }
    }
    if (value=100) {
        return(1);
    }
    return 0;
}