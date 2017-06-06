int main(){
    int* table_ptr;
    int num_imgs;
    for(int i = 1; i < 100; i++){
        num_imgs += i*i*i*i;
        num_imgs -= i*2;
    }
    int j = 10;
    while(j >= 0){
        num_imgs *= j;
    }
    table_ptr = (int*)malloc(sizeof(int)*num_imgs);
    return 0;
}