double __VERIFIER_nondet_double();
void __VERIFIER_assert(int cond) { if (!(cond)) { ERROR: __VERIFIER_error(); } return; }

int main()
{
  double x;
  x = __VERIFIER_nondet_double();

  __VERIFIER_assert(x==x);
  return 0;
}
