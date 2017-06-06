int main(){
    char *s = "Golden Global View";
    char d[20];
    memcpy(d, s, returnChunkSize(d));
    d[strlen(s)] = '\0';
    printf("%s", d);
    return 0;
}
int returnChunkSize(char* a) {
    return strlen(a);
}