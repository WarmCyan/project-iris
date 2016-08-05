import LowLevel as ll

print("\n---------------- RUN ----------------\n")

#ll.ExecutePythonFile("intro")
#ll.ExecutePythonFile("intro")
#ll.debug = True

ll.WritePythonFile("test", """print("Hello world!! How's it going?")""")
ll.ExecutePythonFile("test")
ll.ExecutePythonFile("test")

print("\n=====================================\n")
