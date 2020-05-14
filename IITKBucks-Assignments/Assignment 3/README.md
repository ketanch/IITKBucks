# TASK 3
This program takes details of a transaction and returns the transaction ID.
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
