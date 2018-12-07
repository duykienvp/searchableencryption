/**
 * Copyright (c) 2016, Kevin Lewi
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
 * REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
 * INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
 * LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
 * OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
 * PERFORMANCE OF THIS SOFTWARE.
 */

#ifndef _GEN_MATRICES_H_
#define _GEN_MATRICES_H_

#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <gmp.h>
#include <assert.h>
#include <omp.h>
#include <flint/fmpz_mat.h>
#include "cryptorand.h"

/**
 * Generates an n x n matrix where each entry is a random integer mod p. Also
 * generates the determinant of this matrix and its transposed adjugate matrix
 * (all mod p). The resulting values are print to stdout.
 *
 * The format for the printing is as follows, for a randomly generated matrix M:
 * det(M)
 * M
 * adj(M)^T  (the transpose of the adjugate of M)
 *
 * Each is separated by a newline.
 *
 * To handle errors, before the printing is done, if
 * - there is an error in generating the random values for M
 * - M is non-invertible
 * - M * adj(M) != det(M) * I
 * then an error is thrown, and nothing is printed.
 *
 * If the simulated string is non-zero, then a simulated setup procedure is run
 * (where the entries of the adjugate and the value det are chosen uniformly at
 * random).
 *
 * @param n_str The string representation of n in base 10
 * @param p_str The string representation of p in base 10
 * @param seed A string seed
 * @param simulated A string representing the boolean of whether or not to
 * simulate the setup procedure (without correctness)
 * @return void
 */
void print_random_matrices_with_adj(char *n_str, char *p_str, char *simulated,
    char *seed);


/**
 * Generates an n x n matrix M where each entry is a random integer mod p. Also
 * generates the determinant of this matrix and its transposed adjugate matrix
 * (all mod p). The resulting values are stored in the provided variables.
 *
 *
 * To handle errors, before the printing is done, if
 * - there is an error in generating the random values for M
 * - M is non-invertible
 * - M * adj(M) != det(M) * I
 * then an error is thrown, and nothing is printed.
 *
 * If the is_simulated_setup is non-zero, then a simulated setup procedure is run
 * (where the entries of the adjugate and the value det are chosen uniformly at
 * random).
 *
 * All matrix should be initialized with correct size. Only modp is initialized with correct value of p
 *
 * @param n matrix size
 * @param is_simulated_setup the boolean of whether or not to
 * simulate the setup procedure (without correctness)
 * @param randstate random state of cryptorand
 * @param det determinant matrix
 * @param M n x n matrix M
 * @param adjugate n x n adjugate matrix of M
 * @param prod n x n product matrix (for internal testing)
 * @param check n x n check matrix (for internal testing)
 * @return boolean value for whether error occurred or not
 */
int random_matrices_with_adj(int n, int is_simulated_setup,
                             cryptorand_t randstate, fmpz_t modp,
                             fmpz_t det, fmpz_mat_t M, fmpz_mat_t adjugate,
                             fmpz_mat_t prod, fmpz_mat_t check);

/**
 * Wrapper around fmpz_mat_mul, which simply multiplies two matrices b and c and
 * stores the result in a. Then, each entry of a is modded by p.
 *
 * All matrices are of dimension n x n.
 *
 * @param a The product of the two matrices
 * @param b The first matrix
 * @param c The second matrix
 * @param n The dimension of all matrices
 * @param p The modulus
 * @return void
 */
void fmpz_mat_mul_modp(fmpz_mat_t a, fmpz_mat_t b, fmpz_mat_t c, int n,
    fmpz_t p);

/**
 * Computes the determinant of the matrix a, of dimension n x n, mod p. The
 * result is stored in det.
 *
 * This function uses Gaussian elimination to compute the determinant, and has
 * complexity O(n^3).
 *
 * @param det The determinant, to be stored
 * @param a The matrix to compute the determinant of
 * @param n The dimension of the matrix
 * @param p The modulus
 * @return void
 */
void fmpz_modp_matrix_det(fmpz_t det, fmpz_mat_t a, int n, fmpz_t p);

/**
 * Computes the adjugate of the matrix a, of dimension n x n, mod p. The result
 * is stored in b.
 *
 * @param det The adjugate of the matrix, to be stored
 * @param a The matrix to compute the determinant of
 * @param n The dimension of the matrix
 * @param p The modulus
 * @return void
 */
void fmpz_modp_matrix_adjugate(fmpz_mat_t b, fmpz_mat_t a, int n, fmpz_t p);

#endif /* _GEN_MATRICES_H_ */
