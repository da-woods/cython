import buffer_example

dtvec = buffer_example.DateTimeVector(50)
buffer_example.example_func(dtvec)

string = buffer_example.SingleString()
buffer_example.example_func2(string)

buffer_example.example_func2(dtvec)  # should fail