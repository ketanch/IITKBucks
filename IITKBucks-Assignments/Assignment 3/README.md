# TASK 3
This program(ass3.py) takes details of a transaction and returns the transaction ID.
Run the code using:
>python ass3.py

ass3.py uses classes and functions from header.py so make sure they are in the same directory.

Format of a transaction is:
><no_of_input><input_data><no_of_output><output_data>

<input_data> has format:
><transaction_ID><index_of_output><length_of_signature><signature>

<output_data> has format:
><no_of_coins><length_of_public_key><public_key>

The program converts the above data into a byte stream and saves it in a file whose name is:
```
<hexdump of sha256hash of the byte stream>.dat
```
The .dat file in this folder is an example output whose inputs are:
```

ENTER NO OF INPUTS: 1
1 .
Enter transaction ID(sha256): 64b67ef5895aa172ca6aba2f9b824f9a31271851f59cdea9c184d89add2c20a2
Enter index of output: 1 
Enter valid signature(hex): 3fb58651e04cf02f2008827c7c793edb1c92eefd7476971ebb97fcbb5982bd2921f8db92ddfbc0470a8b7e5f39f80980fb712dfdd74050fddd8ae1bc9b55bb83e54410d5e0702ad2d1682307bd695712c06634fecac1a9882f8ef6e82cc8b7033d82387eb8f1df068cd9230dbd94d5dcaaec2034a6db41581c22fee08820e50a

ENTER NO OF OUTPUTS: 1
1 .
Enter no of coins: 1234
Enter path to public key: ./public.pem

Transaction made successfully
```
