int main(int argc, char **argv) {    
    char buf[5012];
    int buf_len;
    buf_len = 0;
    for(int i = 1; i < 100; i++){
        if(buf_len % 2 == 0)
            buf_len += i;
    }
    memcpy(buf, argv[1], buf_len);
    return (0);
}