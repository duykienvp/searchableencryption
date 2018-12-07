# An Implementation of Several Searchable Encryption Schemes #

This project aims to implement several searchable encryption schemes.
Internally, it uses [Charm] as the main prototype library.
 
The code for Function-Hiding Inner Product Encryption component is originally from [fhipe](https://github.com/kevinlewi/fhipe) of Kevin Lewi.

Authors:
 * Kien Nguyen, University of Southern California

Contact Kien Nguyen for questions about the code:
  kien.nguyen@usc.edu
  
## Modules ##

This library ships with the following modules:
 * **Hidden Vector Encryption**: In [hve.py], 
 hidden vector encryption using composite groups. Based on Appendix A of [Ghinita '14]
 * **Hidden Vector Encryption with Groups of Prime Order**: in [hveprime.py], based on [Iovino '08]   
 * **Inner Product Encryption:** In [ipe.py], implements function-hiding
   inner product encryption. See [Kim '16]
 * **Two-input Functional Encryption.** In [tife.py], implements secret-key
   small-domain two-input functional encryption for arbitrary functions
   See [Kim '16].
   
There are also other testing and benchmarking scripts.


## Prerequisites ##

Make sure you have the following installed:
 * [Python 3](https://www.python.org/)
 * [GMP 6.x](http://gmplib.org/)
 * [PBC](http://crypto.stanford.edu/pbc/download.html)
 * [OpenSSL](http://www.openssl.org/source/)
 * [Charm]
 * [Flint](http://www.flintlib.org/)

You can also see the installation for Ubuntu 18.04 in [Dockerfile].

## Installation ##
If you need to use [fhipe] component, please compile the source code first.

    git clone --recursive https://github.com/USC-InfoLab/searchable-encryption
    cd searchable-encryption
    # change the CFLAGS in [Makefile](/Makefile) to the corresponding OS
    sudo make
    
Otherwise, the [hve] component is simply a Python component

## Running Tests ##

	pip3 install pytest
    pytest
    

## Usage ##
Use the [taskexecutor.py] script to run program.
The script takes the following arguments:
  * `--task`: the task to execute. 
  Tasks are: 
    * `test`: for testing specific functionality
    * `benchmark`: for benchmarking
  * `--scheme`: the scheme to execute. 
  Schemes are: 
    * `hve`: Hidden Vector Encryption 
    * `hvehe`: Hidden Vector Encryption with Hierarchical Encoding
    * `hvege`: Hidden Vector Encryption with Gray Encoding 
    * `hveprime`: Hidden Vector Encryption with Groups of Prime Order 
    * `ipe`: Inner Product Encryption
    * `tife`: Two-input Functional Encryption
  
  
## Note ##
`benchmark` is currently only tested with `hve` scheme. 

## Docker ##
The project also contains a [Dockerfile] for Docker installation. 

[taskexecutor.py]: /taskexecutor.py    
[fhipe]: /searchableencryption/fhipe/
[ipe.py]: /searchableencryption/fhipe/ipe.py
[tife.py]: /searchableencryption/fhipe/tife.py
[hve]: /searchableencryption/hve
[hve.py]: /searchableencryption/hve/hve.py
[hveprime.py]: /searchableencryption/hve/hveprime.py
[Charm]: http://charm-crypto.io/
[Kim '16]: https://eprint.iacr.org/2016/440
[Ghinita '14]: https://dl.acm.org/citation.cfm?id=2557559
[Iovino '08]: https://dl.acm.org/citation.cfm?id=1431889
[Dockerfile]: /Dockerfile

