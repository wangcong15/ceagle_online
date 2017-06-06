int main(){
    int para = 0;
    for(int i = 0; i < 100; i++){
        if(i % 3 == 0){
            para += i * i;
        }
    }
    int (*pt2Function) (float, char, char)=pt2;
    int result2 = (*pt2Function) (para, 'a', 'b');
    return 0;
}
int pt2(float a, char b, char c){
    return 1;
}