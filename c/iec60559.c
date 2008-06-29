/*
 * File:    iec60559.c
 * Author:  <pete.forman@westerngeco.com>
 * Version: 1.2
 * Date:    2000-10-11
 * Updated: 2002-02-19
 */

#include <ctype.h>
#include <float.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_PRINTF_G 255   /* size of temp buffer used by printf("%g") */

#if defined(USE_DTOA)
/*
 * These two functions are David M. Gay's implementations.  The _dmg suffix is
 * to distinguish them from those in libc.
 */
char *dtoa_dmg(double d, int mode, int ndigits, int *decpt, int *sign,
               char **rve);
double strtod_dmg(const char *s00, char **se);
#endif

int main(int argc, char **argv)
{
    union {
        double d;
        unsigned char c[8];
    } u = {1.0};
    char printf_buf[MAX_PRINTF_G];
    int i;
    int big_endian = (u.c[0] != 0);
    double check;

    if (argc != 2) {
        printf("Usage: iec60559 number_or_pattern\n"
               "Number may also be Inf or NaN on some platforms\n"
               "Pattern should start %% and be followed by hex digits\n");
        exit (EXIT_FAILURE);
    }

    if (argv[1][0] != '%') {
        u.d = strtod(argv[1], NULL);
#if defined(USE_DTOA)
        check = strtod_dmg(argv[1], NULL);
        if (memcmp(&check, &u.d, 8) != 0) {  /* do not compare doubles */
            printf("Warning: builtin and netlib versions of strtod differ\n");
        }
#endif
    } else {
        char *p = argv[1] + 1;
        unsigned int ui;

        for (i = 0; i < 8; ++i) {
            if (p && isxdigit((int) *p)) {
                if (isxdigit((int) *(p + 1))) {
                    sscanf(p, "%2x", &ui);
                    u.c[i] = (unsigned char) ui;
                } else {
                    sscanf(p, "%1x", &ui);
                    u.c[i] = (unsigned char) (ui << 4);
                    p = NULL;
                }
            } else {
                u.c[i] = 0;
                p = NULL;
            }
            if (p) {
                p += 2;
            }
        }
        if (!big_endian) {
            unsigned char tmp;
            for (i = 0; i < 4; ++i) {
                tmp = u.c[i];
                u.c[i] = u.c[7 - i];
                u.c[7 - i] = tmp;
            }
        }
        
    }

    /* print the minimum no. of characters, try the lower precision first */
    if (fabs(u.d) <= DBL_MIN) {
        /* scope for improvement here */
        i = 1;
    } else {
        i = 15;
    }
    for (; i <= 17; ++i) {
        sprintf(printf_buf, "%.*g", i, u.d);
        check = strtod(printf_buf, NULL);
        if (memcmp(&check, &u.d, 8) == 0) {
            printf("%s", printf_buf);
            break;
        }
    }
    if (i == 17 + 1) {
        /* should never reach here */
        printf("approximately %.18g", u.d);
    }

    printf(" stored as %%");
    if (big_endian) {
        for (i = 0; i < 8; ++i) {
            printf("%02x", u.c[i]);
        }
    } else {
        for (i = 7; i >= 0; --i) {
            printf("%02x", u.c[i]);
        }
    }
    printf("\n");

#if defined(USE_DTOA)
    {
        int decpt;
        int sign;
        const char *p = dtoa_dmg(u.d, 0, 24, &decpt, &sign, NULL);

        printf("%s", (sign == 0 ? "" : "-"));
        if (decpt == 9999) {
            printf("%s", p);
        } else {
            if (strlen(p) > 1) {
                printf("%.1s.%s", p, p + 1);
            } else {
                printf("%s", p);
            }
            printf("e%+03d", decpt - 1);
        }
        printf(" from dtoa()\n");
    }
#endif

    return EXIT_SUCCESS;
}

