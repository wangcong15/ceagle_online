int main() {
    int check_result = 0;
    int i;
    for(i = 1; i < 100; i++){
        check_result = check_result % i + i * i;
        check_result = check_result % 2;   
    }
    while(i >= 0){
        if(i % 2 == 0){
            check_result = check_result % i + i * i;
            check_result = check_result % 2; 
        }
    }
    switch (check_result) {
        case 0:
            printf("Security check failed!\n");
            exit(-1);
            break;
        case 1:
            printf("Security check passed.\n");
            break;
        }
}
