#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/*  Given a start string and desired checksum
 *  find a set of chars that gives a zero checksum
 */
char *forge(char *start, int slen) {
  int buflen = 4096;
  char *suffix = malloc(buflen);
  memset(suffix, 0, buflen);
  unsigned int sum = 0;
  // Work forward normally on prefix string:
  for(int i = 0; i < slen; i++) {
    sum = (sum >> 1) | ((sum & 1) << 15);
    sum += start[i];
    sum &= 0xffff;
    fprintf(stderr, "pfx sum is %05d\n", sum);
  }

  // Char 0:
  if(sum == 0) {
    // Already done. Return.
    return suffix;
  }
  sum = (sum >> 1) | ((sum & 1) << 15);
  suffix[0] = (~sum) & 0x007F;
  if(suffix[0] < ' ') {
    fprintf(stderr, "First char is nonprintable!");
  }
  sum += suffix[0];
  fprintf(stderr, "ch0 sum is %05d\n", sum);

  for(int i = 1; i < buflen; i++) {
    sum = (sum >> 1) | ((sum & 1) << 15);

    if((sum & 0xFF80) == 0xFF80) {
      // All high bits set. Final character.
      suffix[i] = ((~sum) & 0x007f);
      if(suffix[i] < ' ') {
        fprintf(stderr, "Last character unprintable");
        // I probably want to fix this case somehow
      }
      if(suffix[i] & 1) {
        // We need to set bit 2 so that adding the last bit
        // causes all of them to roll over to 0.
        suffix[i-1] |= 2;
      }
      suffix[i] |= 1;
      return suffix;
    }

    suffix[i] = (~sum) & 0x0040;
    if(!suffix[i]) suffix[i] = 0x0020;
    sum += suffix[i];
    sum &= 0xffff;
    fprintf(stderr, "ch%01d sum is %05d\n", i, sum);
  }

  // Failure case
  free(suffix);
  return 0;
}

int main(int argc, char **argv) {
  char *buf = malloc(4096 * 4096);
  FILE *fp = fopen (argv[1], "rb");
  int ch, len = 0;
  while ((ch = getc (fp)) != EOF) {
    buf[len++] = ch;
    putchar(ch);
  }
  char *s = forge(buf, len);
  printf("%s", s);
  return 0;
}
//
//L@@@ q