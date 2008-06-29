/* Investigate Solaris problems with bus errors.
 *
 * Author:  pete.forman@westerngeco.com
 * Date:    2000-08-03
 * Updated: 2001-01-16
 *
 * On Solaris, compile this file with -g -xO0 and zero or one of -dalign,
 * -misalign, -misalign2.  Specifying none of those three corresponds to
 * "-misalign4".  The -xO0 (or higher) seems to be needed to enable the align
 * directives.  -fast implies -xO4 and -dalign.  On this single file, -misalign2
 * is equivalent to -misalign.  Compile this file in two pieces to illustrate
 * -misalign2:
 *     cc -Xc -DPART=1 -xO0 -misalign2 -c align.c -o align_1.o
 *     cc -Xc -DPART=2 -xO0 -misalign2 -c align.c -o align_2.o
 *     cc align_1.o align_2.o -o align
 *
 * AIX, Cygwin and Linux have no alignment requirements.
 * IRIX requires doubles to be on 8 byte boundaries, with no options.
 * Solaris requires doubles to be on 8, 4, 2 or any byte boundaries depending on
 *   compiler options.
 * Note that it is actually the CPU rather than OS that is important. 
 *
 *
 * Of related interest are the rules for packing.  The above discussion is for
 * accessing doubles.  The packing rules say how doubles and other 8 byte types
 * are aligned.  Set -DPACK=n on IRIX or Solaris to experiment.
 *
 * AIX and Linux by default align to 4 byte boundaries.  They can be made to
 *   pack to 8 bytes by -qalign=natural and -malign-double respectively.  Cygwin
 *   always aligns to 8 byte boundaries.  Other options allow packing to 1 or 2
 *   bytes.  Gcc can alter packing using its __attribute__ extension.
 * IRIX and Solaris align to 8 byte boundaries with no compiler options.  They
 *   both however support #pragma pack (n) within the code.
 */

#define _POSIX_C_SOURCE 1
#define _POSIX_SOURCE 1  /* needed for AIX */

#include <setjmp.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

#if PART != 2
#if defined(PACK)
#pragma pack(PACK)
#endif
typedef struct PackTest {
    char c;  /* packing rules will insert 0 - 7 dummy bytes after c */
    double d;
} PackTest;
#if defined(PACK)
#if defined(__sgi)
#pragma pack(0)
#else /* Solaris */
#pragma pack()
#endif /* defined(__sgi) */
#endif /* defined(PACK) */

sigjmp_buf env;
struct sigaction sa;
sigset_t set;

void wrappedStoreDouble(void *);
void storeDouble(void *);
void handler(int);

int main(void)
{
    double d[2] = {0};
    char *p = (char *) &d[0];
    PackTest packTest;

    if (sizeof(PackTest) == sizeof(char) + sizeof(double)) {
        printf("packTest is located at 0x%lx and is tightly packed\n",
               (unsigned long) &packTest.c);
    } else {
        printf("double member is aligned on %ld bytes\n",
               (long) ((char *) &packTest.d - (char *) &packTest.c));
    }

    sa.sa_handler = handler;
    sigaction(SIGBUS, &sa, NULL);
    sigemptyset(&set);
    sigaddset(&set, SIGBUS);
    
    wrappedStoreDouble(p);     /* should work */
    wrappedStoreDouble(p + 8); /* should work */
    wrappedStoreDouble(p + 4); /* will fail if compiled with -dalign */
    wrappedStoreDouble(p + 2); /* will fail unless compiled with -misalign2 */
    wrappedStoreDouble(p + 1); /* will fail unless compiled with -misalign */
    wrappedStoreDouble(p);     /* should work */

    return EXIT_SUCCESS;
}

void wrappedStoreDouble(void *p)
{
    printf("calling storeDouble(0x%lx) ... ", (unsigned long) p);
    fflush(stdout);
    if (!sigsetjmp(env, 0)) {
        storeDouble(p);
        printf(" ==> no problem\n");
    }
    else {
        printf(" ==> Bus error detected, ignoring it\n");
        sigprocmask(SIG_UNBLOCK, &set, NULL);
    }
}

void handler(int i)
{
    siglongjmp(env, 1);
}
#endif /* PART != 2 */

#if PART != 1
void storeDouble(void * pv)
{
  double *pd = pv;

  *pd = 0.3;
}
#endif /* PART1 != 1 */

